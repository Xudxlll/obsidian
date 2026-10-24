import asyncio
import atexit
import uuid
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import concurrent.futures

from app.engine.runtime import AnalysisRuntime
from app.engine.default_config import DEFAULT_CONFIG
from app.utils.runtime_paths import get_analysis_results_dir
from app.data.core.interface import DataInterface
from app.utils.stock_utils import StockUtils
from app.utils.dataflow_utils import get_trading_date_range

from app.models.analysis import (
    AnalysisParameters,
    AnalysisTask,
    AnalysisBatch,
    AnalysisStatus,
    BatchStatus,
    SingleAnalysisRequest,
    BatchAnalysisRequest,
)
from app.models.user import PyObjectId
from app.models.notification import NotificationCreate
from bson import ObjectId
from app.core.database import get_mongo_db, get_mongo_db_sync, get_redis_client
from app.services.queue_service import QueueService
from app.services.usage_statistics_service import UsageStatisticsService
from app.services.progress.tracker import RedisProgressTracker, get_progress_by_id
from app.services.config_service import config_service
from app.services.config_provider import provider as config_provider
from app.services.memory_state_manager import get_memory_state_manager, TaskStatus
from app.services.progress.log_handler import (
    register_analysis_tracker,
    unregister_analysis_tracker,
)
from app.services.websocket_manager import get_websocket_manager
from app.core.config import settings
from app.utils.timezone import now_utc, now_config_tz, format_date_short, format_iso
from app.llm.mcp import service as mcp_service

logger = logging.getLogger("app.services.analysis_service")

try:
    _di = DataInterface.get_instance()

    def _get_stock_info_safe(stock_code: str):

        from app.core.async_utils import run_async

        try:
            result = run_async(_di.read("CN", "basic_info", symbol=stock_code))
            return result.get("data") if result else None
        except Exception as e:
            logger.debug(f"获取股票信息失败: {e}")
            return None
except Exception as e:
    logger.debug(f"DataInterface 初始化失败，_get_stock_info_safe 不可用: {e}")
    _get_stock_info_safe = None

_TASK_STATUS_MESSAGES: Dict[str, str] = {
    "pending": "任务排队中…",
    "queued": "任务排队中…",
    "running": "任务分析中…",
    "completed": "任务已完成",
    "failed": "任务执行失败",
    "cancelled": "任务已取消",
    "canceled": "任务已取消",
}

async def get_provider_by_model_name(model_name: str) -> str:
    try:
        system_config = await config_service.get_system_config()
        if not system_config or not system_config.llm_configs:
            logger.warning("⚠️ 系统配置为空，使用默认供应商映射")
            return _get_default_provider_by_model(model_name)

        for llm_config in system_config.llm_configs:
            if llm_config.model_name == model_name:
                provider = (
                    llm_config.provider.value
                    if hasattr(llm_config.provider, "value")
                    else str(llm_config.provider)
                )
                logger.info(f"✅ 从数据库找到模型 {model_name} 的供应商: {provider}")
                return provider

        logger.warning(f"⚠️ 数据库中未找到模型 {model_name}，使用默认映射")
        return _get_default_provider_by_model(model_name)

    except Exception as e:
        logger.error(f"❌ 查找模型供应商失败: {e}")
        return _get_default_provider_by_model(model_name)

def get_provider_by_model_name_sync(model_name: str) -> str:
    provider_info = get_provider_and_url_by_model_sync(model_name)
    return provider_info["provider"]

from app.core.lru_cache import BoundedLRUCache

_model_metadata_cache: BoundedLRUCache = BoundedLRUCache(
    maxsize=32, ttl=300, name="model_metadata_cache"
)
_MODEL_API_KEY_PLACEHOLDER = "__resolved_at_runtime__"

def _resolve_api_key_sync(
    db, provider: str, model_api_key: Optional[str]
) -> Optional[str]:

    if model_api_key and model_api_key.strip() and model_api_key != "your-api-key":
        return model_api_key.strip()
    provider_doc = db.llm_providers.find_one({"name": provider})
    if provider_doc and provider_doc.get("api_key"):
        provider_api_key = provider_doc["api_key"]
        if (
            provider_api_key
            and provider_api_key.strip()
            and provider_api_key != "your-api-key"
        ):
            return provider_api_key.strip()
    return None

def get_provider_and_url_by_model_sync(model_name: str) -> dict:

    cached = _model_metadata_cache.get(model_name)
    if cached:
        api_key = _resolve_api_key_sync(get_mongo_db_sync(), cached["provider"], None)
        return {
            "provider": cached["provider"],
            "backend_url": cached["backend_url"],
            "api_key": api_key,
        }

    try:
        db = get_mongo_db_sync()
        configs_collection = db.system_configs
        doc = configs_collection.find_one({"is_active": True}, sort=[("version", -1)])

        if doc and "llm_configs" in doc:
            llm_configs = doc["llm_configs"]

            for config_dict in llm_configs:
                if config_dict.get("model_name") == model_name:
                    provider = config_dict.get("provider")
                    api_base = config_dict.get("api_base")
                    model_api_key = config_dict.get("api_key")

                    providers_collection = db.llm_providers
                    provider_doc = providers_collection.find_one({"name": provider})

                    api_key = _resolve_api_key_sync(db, provider, model_api_key)

                    if not api_key:
                        logger.warning(
                            f"⚠️ [同步查询] 未找到 {provider} 的 API Key，请在 Web UI 配置管理中添加"
                        )

                    backend_url = None
                    if api_base:
                        backend_url = api_base
                        logger.info(
                            f"✅ [同步查询] 模型 {model_name} 使用自定义 API: {api_base}"
                        )
                    elif provider_doc and provider_doc.get("default_base_url"):
                        backend_url = provider_doc["default_base_url"]
                        logger.info(
                            f"✅ [同步查询] 模型 {model_name} 使用厂家默认 API: {backend_url}"
                        )
                    else:
                        backend_url = _get_default_backend_url(provider)
                        logger.warning(
                            f"⚠️ [同步查询] 厂家 {provider} 没有配置 default_base_url，使用硬编码默认值"
                        )

                    _model_metadata_cache.set(
                        model_name,
                        {
                            "provider": provider,
                            "backend_url": backend_url,
                        },
                    )
                    return {
                        "provider": provider,
                        "backend_url": backend_url,
                        "api_key": api_key,
                    }
        logger.warning(f"⚠️ [同步查询] 数据库中未找到模型 {model_name}，使用默认映射")
        provider = _get_default_provider_by_model(model_name)

        try:
            providers_collection = db.llm_providers
            provider_doc = providers_collection.find_one({"name": provider})

            backend_url = _get_default_backend_url(provider)
            if provider_doc:
                if provider_doc.get("default_base_url"):
                    backend_url = provider_doc["default_base_url"]
                    logger.info(
                        f"✅ [同步查询] 使用厂家 {provider} 的 default_base_url: {backend_url}"
                    )

            api_key = _resolve_api_key_sync(db, provider, None)
            if not api_key:
                logger.warning(
                    f"⚠️ [同步查询] 厂家 {provider} 无 API Key，请在 Web UI 配置管理中添加"
                )

            _model_metadata_cache.set(
                model_name,
                {
                    "provider": provider,
                    "backend_url": backend_url,
                },
            )
            return {
                "provider": provider,
                "backend_url": backend_url,
                "api_key": api_key,
            }
        except Exception as e:
            logger.warning(f"⚠️ [同步查询] 无法查询厂家配置: {e}")

        result = {
            "provider": provider,
            "backend_url": _get_default_backend_url(provider),
            "api_key": None,
        }
        _model_metadata_cache.set(
            model_name,
            {
                "provider": provider,
                "backend_url": result["backend_url"],
            },
        )
        return result
    except Exception as e:
        logger.error(f"❌ [同步查询] 查找模型供应商失败: {e}")
        provider = _get_default_provider_by_model(model_name)
        fallback_result = {
            "provider": provider,
            "backend_url": _get_default_backend_url(provider),
            "api_key": None,
        }
        _model_metadata_cache.set(
            model_name,
            {
                "provider": provider,
                "backend_url": fallback_result["backend_url"],
            },
        )
        return fallback_result

def _get_default_backend_url(provider: str) -> str:
    default_urls = {
        "google": "https://generativelanguage.googleapis.com/v1beta",
        "dashscope": "https://dashscope.aliyuncs.com/api/v1",
        "openai": "https://api.openai.com/v1",
        "deepseek": "https://api.deepseek.com",
        "anthropic": "https://api.anthropic.com",
        "openrouter": "https://openrouter.ai/api/v1",
        "qianfan": "https://qianfan.baidubce.com/v2",
        "302ai": "https://api.302.ai/v1",
    }

    url = default_urls.get(
        provider, "https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    return url

def _get_default_provider_by_model(model_name: str) -> str:
    model_provider_map = {
        "qwen-turbo": "dashscope",
        "qwen-plus": "dashscope",
        "qwen-max": "dashscope",
        "qwen-plus-latest": "dashscope",
        "qwen-max-longcontext": "dashscope",
        "gpt-3.5-turbo": "openai",
        "gpt-4": "openai",
        "gpt-4-turbo": "openai",
        "gpt-4o": "openai",
        "gpt-4o-mini": "openai",
        "gemini-pro": "google",
        "gemini-2.0-flash": "google",
        "gemini-2.0-flash-thinking-exp": "google",
        "deepseek-chat": "deepseek",
        "deepseek-coder": "deepseek",
        "deepseek-v4-flash": "deepseek",
        "deepseek-v4-pro": "deepseek",
        "deepseek-reasoner": "deepseek",
        "glm-4": "zhipu",
        "glm-3-turbo": "zhipu",
        "chatglm3-6b": "zhipu",
    }
    provider = model_provider_map.get(model_name, "dashscope")
    return provider

_DEPRECATED_MODELS = {
    "deepseek-chat": ("deepseek-v4-flash", "2026/07/24"),
    "deepseek-reasoner": ("deepseek-v4-pro", "2026/07/24"),
}

def create_analysis_config(
    selected_analysts: list,
    analyst_model: str,
    debate_model: str,
    llm_provider: str,
    market_type: str = "A股",
    analyst_model_config: dict = None,
    debate_model_config: dict = None,
) -> dict:

    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = llm_provider
    config["debate_llm"] = debate_model
    config["analyst_llm"] = analyst_model

    for model_name in [analyst_model, debate_model]:
        if model_name in _DEPRECATED_MODELS:
            replacement, date = _DEPRECATED_MODELS[model_name]
            logger.warning(
                f"[Deprecation] 模型 '{model_name}' 将于 {date} 弃用，"
                f"请迁移至 '{replacement}'"
            )

    config["max_debate_rounds"] = 1
    config["max_risk_discuss_rounds"] = 1
    config["memory_enabled"] = True
    config["online_tools"] = True

    try:
        analyst_provider_info = get_provider_and_url_by_model_sync(analyst_model)
        debate_provider_info = get_provider_and_url_by_model_sync(debate_model)

        config["backend_url"] = analyst_provider_info["backend_url"]
        config["analyst_api_key"] = analyst_provider_info.get("api_key")
        config["debate_api_key"] = debate_provider_info.get("api_key")

        config["analyst_provider"] = analyst_provider_info["provider"]
        config["debate_provider"] = debate_provider_info["provider"]
        config["analyst_backend_url"] = analyst_provider_info["backend_url"]
        config["debate_backend_url"] = debate_provider_info["backend_url"]
    except Exception as e:
        logger.warning(f"⚠️  无法从数据库获取 backend_url 和 API Key: {e}")
        config["backend_url"] = _get_default_backend_url(llm_provider)
        config["analyst_provider"] = llm_provider
        config["debate_provider"] = llm_provider
        config["analyst_backend_url"] = config["backend_url"]
        config["debate_backend_url"] = config["backend_url"]

    config["selected_analysts"] = selected_analysts
    config["debug"] = False

    if analyst_model_config:
        config["analyst_model_config"] = analyst_model_config
    if debate_model_config:
        config["debate_model_config"] = debate_model_config

    config.setdefault("phase2_enabled", False)
    config.setdefault("phase2_debate_rounds", 1)
    config.setdefault("phase3_enabled", False)
    config.setdefault("phase3_debate_rounds", 1)
    config.setdefault("phase4_enabled", True)
    config.setdefault("phase4_debate_rounds", 1)
    config.setdefault("max_debate_rounds", 1)
    config.setdefault("max_risk_discuss_rounds", 1)

    return config

class AnalysisService:

    def __init__(self):
        self._trading_graph_cache = {}
        self.memory_manager = get_memory_state_manager()
        self._progress_trackers: Dict[str, RedisProgressTracker] = {}
        from app.core.lru_cache import BoundedLRUCache

        self._stock_name_cache = BoundedLRUCache(maxsize=512, name="stock_name_cache")
        pool_workers = getattr(settings, "ANALYSIS_THREAD_POOL_SIZE", 3)
        self._thread_pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=pool_workers
        )
        atexit.register(self._shutdown_pool)
        logger.info(f"🔧 [服务初始化] 线程池最大并发数: {pool_workers}")

        try:
            redis_client = get_redis_client()
            self.queue_service = QueueService(redis_client)
            self.usage_service = UsageStatisticsService()
        except Exception as e:
            logger.warning(f"⚠️ 队列或统计服务初始化失败: {e}")

        try:
            self.memory_manager.set_websocket_manager(get_websocket_manager())
        except ImportError:
            logger.warning("⚠️ WebSocket 管理器不可用")

        logger.info(f"🔧 [服务初始化] AnalysisService 实例ID: {id(self)}")

    def _shutdown_pool(self, wait: bool = False):
        try:
            if self._thread_pool:
                self._thread_pool.shutdown(wait=wait)
        except Exception as e:
            logger.debug(f"线程池关闭失败（atexit 阶段可能日志已关闭）: {e}")

    async def _update_progress_async(self, task_id: str, progress: int, message: str):
        try:
            await self.memory_manager.update_task_status(
                task_id=task_id,
                status=TaskStatus.RUNNING,
                progress=progress,
                message=message,
                current_step=message,
            )
            db = get_mongo_db()
            await db.analysis_tasks.update_one(
                {"task_id": task_id},
                {
                    "$set": {
                        "progress": progress,
                        "current_step": message,
                        "message": message,
                        "updated_at": now_utc(),
                    }
                },
            )
        except Exception as e:
            logger.warning(f"⚠️ [异步更新] 失败: {e}")

    def _resolve_stock_name(self, code: Optional[str]) -> str:
        if not code:
            return ""
        cached = self._stock_name_cache.get(code)
        if cached:
            return cached
        name = None
        try:
            if _get_stock_info_safe:
                info = _get_stock_info_safe(code)
                if isinstance(info, dict):
                    name = info.get("name")
        except Exception as e:
            logger.debug(f"解析股票名称失败: {e}")
        if not name:
            name = f"股票{code}"
        self._stock_name_cache.set(code, name)
        return name

    def _enrich_stock_names(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        try:
            for t in tasks:
                code = t.get("stock_code") or t.get("stock_symbol")
                name = t.get("stock_name")
                if not name and code:
                    cached = self._stock_name_cache.get(code)
                    t["stock_name"] = cached if cached else f"股票{code}"
        except Exception as e:
            logger.warning(f"⚠️ 补齐股票名称时出现异常: {e}")
        return tasks

    async def _convert_user_id_async(self, user_id: str) -> PyObjectId:
        try:
            if user_id == "admin":
                try:
                    db = get_mongo_db()
                    admin_doc = await db.users.find_one(
                        {"username": "admin"}, {"_id": 1}
                    )
                    if admin_doc:
                        return PyObjectId(admin_doc["_id"])
                except Exception as e:
                    logger.warning(f"⚠️ 异步查询 admin 用户失败: {e}")
                raise ValueError("无法确定 admin 用户的 ObjectId")
            return PyObjectId(ObjectId(user_id))
        except Exception as e:
            logger.warning(f"⚠️ 用户ID转换失败: user_id={user_id}, error={e}")
            raise ValueError(f"无效的用户ID: {user_id}") from e

    def _serialize_for_response(self, value: Any) -> Any:
        if isinstance(value, ObjectId):
            return str(value)
        if isinstance(value, list):
            return [self._serialize_for_response(v) for v in value]
        if isinstance(value, dict):
            return {k: self._serialize_for_response(v) for k, v in value.items()}
        return value

    def _get_sync_mongo_db(self):
        from app.core.database import get_mongo_db_sync

        return get_mongo_db_sync()

    def _get_trading_graph(self, config: Dict[str, Any]) -> AnalysisRuntime:
        selected = config.get("selected_analysts") or []
        if not selected:
            raise ValueError(
                "selected_analysts 不能为空，请先在阶段1配置分析师后再发起任务。"
            )
        return AnalysisRuntime(
            selected_analysts=selected, debug=config.get("debug", False), config=config
        )

    def _auto_enable_mcp(
        self, config: Dict[str, Any], selected_tool_ids: Optional[List[str]] = None
    ) -> None:

        if config.get("enable_mcp"):
            return

        try:
            enabled = mcp_service.enabled_server_configs()
            if enabled:
                config["enable_mcp"] = True
                config.setdefault("mcp_tool_ids", selected_tool_ids or [])
                logger.info(f"自动启用MCP工具: {len(enabled)} 个 server")
            else:
                logger.info("MCP支持已检测，无可用外部工具")
        except Exception as exc:
            logger.warning(f"自动注入MCP工具失败: {exc}")

    async def create_analysis_task(
        self, user_id: str, request: SingleAnalysisRequest
    ) -> Dict[str, Any]:
        try:
            task_id = str(uuid.uuid4())
            stock_code = request.get_symbol()
            if not stock_code:
                raise ValueError("股票代码不能为空")

            logger.info(f"📝 创建分析任务: {task_id} - {stock_code}")

            await self.memory_manager.create_task(
                task_id=task_id,
                user_id=user_id,
                stock_code=stock_code,
                parameters=request.parameters.model_dump()
                if request.parameters
                else {},
                stock_name=self._resolve_stock_name(stock_code),
            )

            code = stock_code
            name = self._resolve_stock_name(code)
            parameters = request.parameters.model_dump() if request.parameters else {}
            try:
                db = get_mongo_db()
                await db.analysis_tasks.update_one(
                    {"task_id": task_id},
                    {
                        "$setOnInsert": {
                            "task_id": task_id,
                            "user_id": user_id,
                            "stock_code": code,
                            "stock_symbol": code,
                            "stock_name": name,
                            "status": "pending",
                            "progress": 0,
                            "created_at": now_utc(),
                            "parameters": parameters,
                        }
                    },
                    upsert=True,
                )
            except Exception as e:
                logger.error(f"❌ 创建任务时写入MongoDB失败: {e}")

            return {
                "task_id": task_id,
                "status": "pending",
                "message": "任务已创建，等待执行",
            }

        except Exception as e:
            logger.error(f"❌ 创建分析任务失败: {e}")
            raise

    async def execute_analysis_background(
        self, task_id: str, user_id: str, request: SingleAnalysisRequest
    ):
        stock_code = request.get_symbol()
        progress_tracker = None
        try:
            logger.info(f"🚀 开始后台执行分析任务: {task_id}")

            from app.utils.stock_validator import prepare_stock_data_async

            market_type = (
                request.parameters.market_type if request.parameters else "A股"
            )
            analysis_date = (
                request.parameters.analysis_date if request.parameters else None
            )

            if analysis_date and isinstance(analysis_date, datetime):
                analysis_date = analysis_date.strftime("%Y-%m-%d")
            elif analysis_date and isinstance(analysis_date, str):
                try:
                    parsed_date = datetime.strptime(analysis_date, "%Y-%m-%d")
                    analysis_date = parsed_date.strftime("%Y-%m-%d")
                except ValueError:
                    analysis_date = format_date_short(now_config_tz())

            validation_result = await prepare_stock_data_async(
                stock_code=stock_code,
                market_type=market_type,
                period_days=30,
                analysis_date=analysis_date,
            )

            if not validation_result.is_valid:
                error_msg = f"❌ 股票代码无效: {validation_result.error_message}"
                await self.memory_manager.update_task_status(
                    task_id=task_id,
                    status=AnalysisStatus.FAILED,
                    progress=0,
                    error_message=error_msg,
                )
                await self._update_task_status(
                    task_id, AnalysisStatus.FAILED, 0, error_message=error_msg
                )
                return

            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                logger.warning("无法获取当前事件循环，WebSocket 推送可能失效")
                loop = None

            phase_config = {
                "phase2_enabled": getattr(request.parameters, "phase2_enabled", False)
                if request.parameters
                else False,
                "phase2_debate_rounds": getattr(
                    request.parameters, "phase2_debate_rounds", 2
                )
                if request.parameters
                else 1,
                "phase3_enabled": getattr(request.parameters, "phase3_enabled", False)
                if request.parameters
                else False,
                "phase3_debate_rounds": getattr(
                    request.parameters, "phase3_debate_rounds", 2
                )
                if request.parameters
                else 1,
                "phase4_enabled": True,
                "phase4_debate_rounds": 1,
            }

            selected_analysts = (
                request.parameters.selected_analysts
                if request.parameters and request.parameters.selected_analysts
                else []
            )
            if not selected_analysts:
                raise ValueError(
                    "selected_analysts 不能为空，请先在阶段1配置并选择分析师。"
                )

            def progress_callback(data):
                if not loop:
                    return
                try:
                    ws_manager = get_websocket_manager()
                    message = {
                        "type": "progress_update",
                        "task_id": task_id,
                        "status": data.get("status"),
                        "progress": data.get("progress_percentage"),
                        "message": data.get("last_message"),
                        "current_step": data.get("current_step"),
                        "steps": data.get("steps"),
                    }
                    asyncio.run_coroutine_threadsafe(
                        ws_manager.send_progress_update(task_id, message), loop
                    )
                except Exception as e:
                    logger.error(f"WebSocket 广播失败: {e}")

            def create_progress_tracker():
                return RedisProgressTracker(
                    task_id=task_id,
                    analysts=selected_analysts,
                    phase_config=phase_config,
                    llm_provider=_get_default_provider_by_model(
                        getattr(request.parameters, "analyst_model", "qwen-turbo")
                    ),
                    on_update=progress_callback,
                )

            progress_tracker = await asyncio.to_thread(create_progress_tracker)
            self._progress_trackers[task_id] = progress_tracker
            register_analysis_tracker(task_id, progress_tracker)

            await asyncio.to_thread(
                progress_tracker.update_progress,
                {"progress_percentage": 5, "last_message": "🚀 开始股票分析"},
            )
            await self.memory_manager.update_task_status(
                task_id=task_id,
                status=TaskStatus.RUNNING,
                progress=5,
                message="分析开始...",
                current_step="initialization",
            )
            await self._update_task_status(task_id, AnalysisStatus.PROCESSING, 5)

            selected_mcp_tools = []
            if request.parameters:
                selected_mcp_tools = (
                    getattr(request.parameters, "mcp_tool_ids", None)
                    or getattr(request.parameters, "mcp_tools", [])
                    or []
                )
                if selected_mcp_tools:
                    logger.info(f"MCP工具选择: {selected_mcp_tools}")

            result = await self._execute_analysis_sync(
                task_id,
                user_id,
                request,
                progress_tracker,
                mcp_tool_ids=selected_mcp_tools,
            )

            await asyncio.to_thread(progress_tracker.mark_completed)

            await self._save_analysis_results_complete(task_id, result)

            await self.memory_manager.update_task_status(
                task_id=task_id,
                status=TaskStatus.COMPLETED,
                progress=100,
                message="分析完成",
                current_step="completed",
                result_data=result,
            )
            await self._update_task_status(task_id, AnalysisStatus.COMPLETED, 100)

            try:
                from app.services.notifications_service import get_notifications_service

                svc = get_notifications_service()
                summary = str(result.get("summary", ""))[:120]
                await svc.create_and_publish(
                    payload=NotificationCreate(
                        user_id=str(user_id),
                        type="analysis",
                        title=f"{stock_code} 分析完成",
                        content=summary,
                        link=f"/stocks/{stock_code}",
                        source="analysis",
                    )
                )
            except Exception as e:
                logger.debug(f"发送分析完成通知失败: {e}")

        except Exception as e:
            logger.error(f"❌ 后台分析任务失败: {task_id} - {e}")
            if progress_tracker:
                progress_tracker.mark_failed(str(e))
            await self.memory_manager.update_task_status(
                task_id=task_id,
                status=TaskStatus.FAILED,
                progress=0,
                message="分析失败",
                error_message=str(e),
            )
            await self._update_task_status(task_id, AnalysisStatus.FAILED, 0, str(e))
        finally:
            if task_id in self._progress_trackers:
                del self._progress_trackers[task_id]
            unregister_analysis_tracker(task_id)

    async def submit_single_analysis(
        self, user_id: str, request: SingleAnalysisRequest
    ) -> Dict[str, Any]:
        return await self.create_analysis_task(user_id, request)

    async def submit_batch_analysis(
        self, user_id: str, request: BatchAnalysisRequest
    ) -> Dict[str, Any]:
        try:
            batch_id = str(uuid.uuid4())
            converted_user_id = await self._convert_user_id_async(user_id)

            effective_settings = await config_provider.get_effective_system_settings()
            params = request.parameters or AnalysisParameters()

            if not getattr(params, "analyst_model", None) or not getattr(params, "debate_model", None):
                from app.services.model_capability_service import (
                    get_model_capability_service,
                )

                rec_analyst, rec_debate = (
                    get_model_capability_service().recommend_models()
                )
                if not getattr(params, "analyst_model", None):
                    params.analyst_model = effective_settings.get("analyst_model") or rec_analyst
                if not getattr(params, "debate_model", None):
                    params.debate_model = effective_settings.get("debate_model") or rec_debate

            stock_symbols = request.get_symbols()

            batch = AnalysisBatch(
                batch_id=batch_id,
                user_id=converted_user_id,
                title=request.title,
                description=request.description,
                total_tasks=len(stock_symbols),
                parameters=params,
                status=BatchStatus.PENDING,
            )

            tasks = []
            for symbol in stock_symbols:
                task_id = str(uuid.uuid4())
                task = AnalysisTask(
                    task_id=task_id,
                    batch_id=batch_id,
                    user_id=converted_user_id,
                    symbol=symbol,
                    stock_code=symbol,
                    parameters=batch.parameters,
                    status=AnalysisStatus.PENDING,
                )
                tasks.append(task)

            db = get_mongo_db()
            await db.analysis_batches.insert_one(batch.dict(by_alias=True))
            await db.analysis_tasks.insert_many(
                [task.dict(by_alias=True) for task in tasks]
            )

            for task in tasks:
                queue_params = task.parameters.dict() if task.parameters else {}
                queue_params.update(
                    {
                        "task_id": task.task_id,
                        "symbol": task.symbol,
                        "stock_code": task.symbol,
                        "user_id": str(task.user_id),
                        "batch_id": task.batch_id,
                        "created_at": task.created_at.isoformat()
                        if task.created_at
                        else None,
                    }
                )
                await self.queue_service.enqueue_task(
                    user_id=str(converted_user_id),
                    symbol=task.symbol,
                    params=queue_params,
                    batch_id=task.batch_id,
                )

            return {
                "batch_id": batch_id,
                "total_tasks": len(tasks),
                "status": BatchStatus.PENDING,
                "message": f"已提交{len(tasks)}个分析任务到队列",
            }
        except Exception as e:
            logger.error(f"提交批量分析任务失败: {e}")
            raise

    async def cancel_task(self, task_id: str) -> bool:
        try:
            await self._update_task_status(task_id, AnalysisStatus.CANCELLED, 0)
            await self.queue_service.cancel_task(task_id)
            return True
        except Exception as e:
            logger.error(f"取消任务失败: {task_id} - {e}")
            return False

    async def _execute_analysis_sync(
        self,
        task_id: str,
        user_id: str,
        request: SingleAnalysisRequest,
        progress_tracker: Optional[RedisProgressTracker] = None,
        mcp_tool_ids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            self._thread_pool,
            self._run_analysis_sync,
            task_id,
            user_id,
            request,
            progress_tracker,
            mcp_tool_ids or [],
            loop,
        )
        return result

    @staticmethod
    def _normalize_symbol_for_data(symbol: str, market: str) -> str:
        symbol = (symbol or "").strip()
        if market == "CN":
            return symbol.replace(".SZ", "").replace(".SH", "").replace(".BJ", "").zfill(6)
        if market == "HK":
            return symbol.replace(".HK", "").replace(".hk", "").zfill(5)
        return symbol.upper()

    def _prefetch_stock_data(
        self,
        market: str,
        symbol: str,
    ) -> Dict[str, str]:

        from app.core.async_utils import run_async
        from app.data.core.interface import DataInterface

        di = DataInterface.get_instance()
        result = run_async(
            di.refresh(
                market,
                symbol,
                domains=None,
                force=False,
                timeout=60,
            )
        )

        domain_statuses = {}
        for domain, dr in result.domains.items():
            domain_statuses[domain] = dr.status
            if dr.status == "failed":
                logger.warning(f"📊 [数据预拉取] {domain} 失败: {dr.error}")
            else:
                logger.info(
                    f"📊 [数据预拉取] {domain}: {dr.status} ({dr.record_count} 条, {dr.latency_ms}ms)"
                )

        refreshed = sum(1 for s in domain_statuses.values() if s == "refreshed")
        fresh = sum(1 for s in domain_statuses.values() if s == "fresh")
        failed = sum(1 for s in domain_statuses.values() if s in ("failed", "timeout"))
        logger.info(
            f"📊 [数据预拉取] 完成: {refreshed} 个域刷新, {fresh} 个域已是最新, {failed} 个域失败"
        )

        return domain_statuses

    def _run_analysis_sync(
        self,
        task_id: str,
        user_id: str,
        request: SingleAnalysisRequest,
        progress_tracker: Optional[RedisProgressTracker] = None,
        mcp_tool_ids: Optional[List[str]] = None,
        server_loop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> Dict[str, Any]:
        task_mcp_manager = None

        try:
            from app.engine.agents.analysts.dynamic_analyst import DynamicAnalystFactory
            from app.llm.mcp.task_manager import (
                get_task_mcp_manager,
                remove_task_mcp_manager,
            )

            task_mcp_manager = get_task_mcp_manager(task_id)
            logger.info(f"🔧 [任务管理器] 创建任务级 MCP 管理器: {task_id}")

            def update_progress_sync(progress: int, message: str, step: str):
                try:
                    if progress_tracker:
                        progress_tracker.update_progress(
                            {"progress_percentage": progress, "last_message": message}
                        )

                    self.memory_manager.update_task_status_sync(
                        task_id=task_id,
                        status=TaskStatus.RUNNING,
                        progress=progress,
                        message=message,
                        current_step=step,
                    )

                    sync_db = self._get_sync_mongo_db()
                    if sync_db is not None:
                        sync_db.analysis_tasks.update_one(
                            {"task_id": task_id},
                            {
                                "$set": {
                                    "progress": progress,
                                    "current_step": step,
                                    "message": message,
                                    "updated_at": now_utc(),
                                }
                            },
                        )
                except Exception as e:
                    logger.warning(f"⚠️ [Sync] 更新进度失败: {e}")

            update_progress_sync(6, "⚙️ 配置分析参数", "configuration")

            selected_analysts = []
            if request.parameters:
                selected_analysts = [
                    str(a).strip()
                    for a in getattr(request.parameters, "selected_analysts", [])
                    if a
                ]
            if not selected_analysts:
                raise ValueError(
                    "selected_analysts 不能为空，请先在阶段1配置并选择分析师。"
                )

            try:
                lookup = DynamicAnalystFactory.build_lookup_map()
                normalized: List[str] = []
                seen = set()
                for key in selected_analysts:
                    mapped = key
                    if key in lookup:
                        mapped = (
                            lookup[key].get("slug")
                            or lookup[key].get("internal_key")
                            or key
                        )
                    if mapped and mapped not in seen:
                        normalized.append(mapped)
                        seen.add(mapped)
                selected_analysts = normalized
            except Exception as e:
                logger.warning(f"⚠️ 规范化分析师列表失败，使用原始输入: {e}")

            if not selected_analysts:
                raise ValueError(
                    "selected_analysts 不能为空，请先在阶段1配置并选择分析师。"
                )

            logger.info(f"📋 [分析师选择] 最终分析师列表: {selected_analysts}")

            from app.services.model_capability_service import (
                get_model_capability_service,
            )

            capability_service = get_model_capability_service()

            if (
                request.parameters
                and getattr(request.parameters, "analyst_model", None)
                and getattr(request.parameters, "debate_model", None)
            ):
                analyst_model = request.parameters.analyst_model
                debate_model = request.parameters.debate_model
            else:
                analyst_model, debate_model = capability_service.recommend_models()

            if not analyst_model or not debate_model:
                raise ValueError(
                    "未添加任何启用的模型，请先在 设置 → 模型配置 中添加并启用模型"
                )

            for _mn in [analyst_model, debate_model]:
                if _mn in _DEPRECATED_MODELS:
                    _repl, _date = _DEPRECATED_MODELS[_mn]
                    logger.warning(
                        f"[Deprecation] 模型 '{_mn}' 将于 {_date} 弃用，"
                        f"请迁移至 '{_repl}'"
                    )

            analyst_provider_info = get_provider_and_url_by_model_sync(analyst_model)
            debate_provider_info = get_provider_and_url_by_model_sync(debate_model)
            analyst_provider = analyst_provider_info["provider"]

            if request.parameters and request.parameters.market_type:
                market_type = request.parameters.market_type
            else:
                try:
                    market_info = StockUtils.get_market_info(request.get_symbol())
                    if market_info.get("is_china"):
                        market_type = "A股"
                    elif market_info.get("is_hk"):
                        market_type = "港股"
                    elif market_info.get("is_us"):
                        market_type = "美股"
                    else:
                        market_type = "A股"
                    logger.info(
                        f"📊 [自动识别] 股票 {request.get_symbol()} 市场类型: {market_type}"
                    )
                except Exception as e:
                    logger.warning(f"⚠️ 无法识别股票市场类型: {e}，使用默认值 'A股'")
                    market_type = "A股"

            config = create_analysis_config(
                selected_analysts=selected_analysts,
                analyst_model=analyst_model,
                debate_model=debate_model,
                llm_provider=analyst_provider,
                market_type=market_type,
            )

            selected_mcp_tools: List[str] = []
            if mcp_tool_ids:
                selected_mcp_tools = list(mcp_tool_ids)
            elif request.parameters:
                selected_mcp_tools = (
                    getattr(request.parameters, "mcp_tool_ids", None)
                    or getattr(request.parameters, "mcp_tools", [])
                    or []
                )

            if selected_mcp_tools:
                config["enable_mcp"] = True
                config["mcp_tool_ids"] = selected_mcp_tools
                logger.info(f"启用MCP工具（按选择过滤）: {len(selected_mcp_tools)}个")

            self._auto_enable_mcp(config, selected_mcp_tools)

            if request.parameters:
                config["phase2_enabled"] = getattr(
                    request.parameters, "phase2_enabled", False
                )
                config["phase2_debate_rounds"] = getattr(
                    request.parameters, "phase2_debate_rounds", 2
                )
                config["phase3_enabled"] = getattr(
                    request.parameters, "phase3_enabled", False
                )
                config["phase3_debate_rounds"] = getattr(
                    request.parameters, "phase3_debate_rounds", 2
                )
                config["phase4_enabled"] = True
                config["phase4_debate_rounds"] = 1
            else:
                config.setdefault("phase2_enabled", False)
                config.setdefault("phase3_enabled", False)
                config.setdefault("phase4_enabled", True)
                config.setdefault("phase2_debate_rounds", 1)
                config.setdefault("phase3_debate_rounds", 1)
                config.setdefault("phase4_debate_rounds", 1)

            config["max_debate_rounds"] = config.get("phase2_debate_rounds", 1)
            config["max_risk_discuss_rounds"] = config.get("phase3_debate_rounds", 1)

            config["analyst_provider"] = analyst_provider
            config["debate_provider"] = debate_provider_info["provider"]
            config["analyst_backend_url"] = analyst_provider_info["backend_url"]
            config["debate_backend_url"] = debate_provider_info["backend_url"]
            config["backend_url"] = analyst_provider_info["backend_url"]

            config["task_mcp_manager"] = task_mcp_manager
            config["task_id"] = task_id
            logger.info(f"🔧 [任务管理器] 已将 MCP 管理器注入配置: task_id={task_id}")

            update_progress_sync(8, "🚀 初始化AI分析引擎", "engine_initialization")

            try:
                from app.engine.tools.datasources.domain_checker import AvailabilityCache
                from app.engine.tools.datasources.registry import DATASOURCE_REGISTRY

                _market_map = {"A股": "CN", "港股": "HK", "美股": "US"}
                _market = _market_map.get(market_type, "CN")
                _cache = AvailabilityCache.get_instance()
                from app.core.async_utils import run_async

                run_async(_cache.compute(_market, DATASOURCE_REGISTRY))
                logger.info(
                    f"📊 [工具可用性] 市场={_market}, 结果={_cache.all_results}"
                )
            except Exception as _e:
                logger.warning(f"⚠️ [工具可用性] 预计算失败（不影响分析）: {_e}")

            _prefetch_enabled = True
            if request.parameters is not None:
                _prefetch_enabled = bool(getattr(request.parameters, "prefetch_data", True))
            if _prefetch_enabled:
                update_progress_sync(10, "📊 预拉取股票数据...", "data_prefetch")
                try:
                    _prefetch_symbol = self._normalize_symbol_for_data(
                        request.get_symbol(), _market
                    )
                    prefetch_result = self._prefetch_stock_data(_market, _prefetch_symbol)
                    logger.info(f"📊 [数据预拉取] 结果: {prefetch_result}")
                    run_async(_cache.compute(_market, DATASOURCE_REGISTRY))
                    logger.info(f"📊 [工具可用性] 预拉取后重新计算: {_cache.all_results}")
                except Exception as _prefetch_err:
                    logger.warning(
                        f"⚠️ [数据预拉取] 失败（不影响分析，使用现有数据）: {_prefetch_err}"
                    )
                update_progress_sync(12, "📊 数据预拉取完成", "data_prefetch_done")
            else:
                logger.info("📊 [数据预拉取] 用户已关闭，直接使用库内数据")
                update_progress_sync(12, "📊 跳过数据预拉取（使用库内数据）", "data_prefetch_skipped")

            import time

            graph_init_start = time.time()
            logger.info("⏱️ [性能追踪] 开始创建 AnalysisRuntime...")

            trading_graph = self._get_trading_graph(config)

            graph_init_elapsed = time.time() - graph_init_start
            logger.info(
                f"⏱️ [性能追踪] AnalysisRuntime 创建完成，耗时: {graph_init_elapsed:.2f} 秒 ({graph_init_elapsed / 60:.2f} 分钟)"
            )

            if graph_init_elapsed > 60:
                logger.warning(
                    "⚠️ [性能瓶颈] AnalysisRuntime 初始化耗时超过 1 分钟！这是主要性能瓶颈！"
                )

            start_time = now_config_tz()
            analysis_date = format_date_short(now_config_tz())
            if request.parameters and request.parameters.analysis_date:
                ad = request.parameters.analysis_date
                if isinstance(ad, datetime):
                    analysis_date = ad.strftime("%Y-%m-%d")
                elif isinstance(ad, str):
                    analysis_date = ad

            data_start_date, data_end_date = get_trading_date_range(
                analysis_date, lookback_days=10
            )
            logger.info(
                f"📅 分析目标日期: {analysis_date}, 数据范围: {data_start_date} 至 {data_end_date}"
            )

            update_progress_sync(15, "🤖 开始多智能体协作分析", "agent_analysis")

            def graph_progress_callback(payload: dict):
                try:
                    if not progress_tracker:
                        return
                    percent = int(payload.get("percent") or 0)
                    step_text = str(payload.get("step_text") or "")
                    completed = payload.get("completed")
                    total = payload.get("total")
                    message = (
                        f"{step_text}（{completed}/{total}）"
                        if completed and total else step_text
                    )
                    current_progress = progress_tracker.progress_data.get(
                        "progress_percentage", 0
                    )
                    if percent >= current_progress:
                        update_progress_sync(percent, message, step_text)
                    else:
                        progress_tracker.update_progress({"last_message": message})
                except Exception as e:
                    logger.debug(f"进度回调更新失败: {e}")

            from app.services.analysis_events import create_event_sink, release_event_sink

            event_sink = create_event_sink(
                task_id, server_loop=server_loop, on_progress=graph_progress_callback
            )
            try:
                state, decision = trading_graph.propagate_sync(
                    request.stock_code,
                    analysis_date,
                    task_id=task_id,
                    event_sink=event_sink,
                    user_id=user_id,
                    progress_range=(15, 92),
                )
            finally:
                release_event_sink(task_id, server_loop=server_loop)

            update_progress_sync(95, "处理分析结果...", "result_processing")
            execution_time = (now_config_tz() - start_time).total_seconds()

            reports = self._extract_reports_from_state(state)

            structured_summary = state.get("structured_summary") or {}

            summary_text = ""
            if structured_summary and structured_summary.get("analysis_summary"):
                summary_text = structured_summary.get("analysis_summary")
            elif isinstance(decision, dict):
                summary_text = str(decision.get("summary", ""))[:200]

            recommendation_text = ""
            if structured_summary and structured_summary.get(
                "investment_recommendation"
            ):
                recommendation_text = structured_summary.get(
                    "investment_recommendation"
                )
            elif isinstance(decision, dict):
                recommendation_text = str(decision.get("recommendation", ""))

            result = {
                "stock_code": request.stock_code,
                "stock_symbol": request.stock_code,
                "analysis_date": analysis_date,
                "market_type": market_type,
                "summary": summary_text,
                "recommendation": recommendation_text,
                "confidence_score": decision.get("confidence_score", 0.0)
                if isinstance(decision, dict)
                else 0.0,
                "risk_level": decision.get("risk_level", "中等")
                if isinstance(decision, dict)
                else "中等",
                "detailed_analysis": decision,
                "execution_time": execution_time,
                "state": state,
                "structured_summary": structured_summary,
                "reports": reports,
                "decision": decision,
                "model_info": decision.get("model_info", "Unknown")
                if isinstance(decision, dict)
                else "Unknown",
                "analysts": request.parameters.selected_analysts
                if request.parameters
                else [],
            }
            return result

        except Exception as e:
            logger.error(f"❌ 分析执行失败: {task_id} - {e}")
            raise

        finally:
            if task_mcp_manager is not None:
                try:
                    asyncio.get_running_loop()
                    from app.core.task_registry import task_registry

                    task_registry.register(
                        remove_task_mcp_manager(task_id),
                        name=f"mcp_cleanup_{task_id}",
                        critical=False,
                    )
                    logger.info(
                        f"🔧 [任务管理器] 已调度清理任务级 MCP 管理器: {task_id}"
                    )
                except RuntimeError:
                    try:
                        from app.llm.mcp.task_manager import _task_managers

                        _task_managers.invalidate(task_id)
                        logger.info(
                            f"🔧 [任务管理器] 已同步失效任务级 MCP 管理器: {task_id}"
                        )
                    except Exception as e:
                        logger.warning(f"⚠️ [任务管理器] 同步清理失败: {e}")
                except Exception as e:
                    logger.warning(f"⚠️ [任务管理器] 清理任务管理器失败: {e}")

    def _extract_reports_from_state(self, state: dict) -> dict:
        reports = {}
        if not isinstance(state, dict):
            return reports

        known_non_report_keys = [
            "trader_investment_plan",
            "investment_plan",
            "final_trade_decision",
        ]

        report_keys_found = [
            k
            for k in state.keys()
            if k.endswith("_report") or k in known_non_report_keys
        ]
        logger.info(f"[报告提取] state中发现的报告键: {report_keys_found}")

        for key in state.keys():
            if key.endswith("_report") or key in known_non_report_keys:
                content = state[key]
                if content:
                    if isinstance(content, str):
                        reports[key] = content
                    elif hasattr(content, "content") and isinstance(
                        content.content, str
                    ):
                        reports[key] = content.content
                    else:
                        try:
                            reports[key] = str(content)
                        except Exception as e:
                            logger.warning(
                                f"[报告提取] 无法提取报告 {key}: 类型={type(content)}, 错误: {e}"
                            )

        logger.info(f"[报告提取] 根级报告: {list(reports.keys())}")

        if "investment_debate_state" in state and isinstance(
            state["investment_debate_state"], dict
        ):
            inv_state = state["investment_debate_state"]
            for state_key, report_key in {
                "bull_history": "bull_researcher",
                "bear_history": "bear_researcher",
                "judge_decision": "research_team_decision",
            }.items():
                if state_key in inv_state and inv_state[state_key]:
                    reports[report_key] = inv_state[state_key]

        if "risk_debate_state" in state and isinstance(
            state["risk_debate_state"], dict
        ):
            risk_state = state["risk_debate_state"]
            for state_key, report_key in {
                "risky_history": "risky_analyst",
                "safe_history": "safe_analyst",
                "neutral_history": "neutral_analyst",
                "judge_decision": "risk_management_decision",
            }.items():
                if state_key in risk_state and risk_state[state_key]:
                    reports[report_key] = risk_state[state_key]

        if "reports" in state and isinstance(state["reports"], dict):
            dynamic_reports = state["reports"]
            logger.info(
                f"[报告提取] 从 reports 字典发现 {len(dynamic_reports)} 个: {list(dynamic_reports.keys())}"
            )
            for key, content in dynamic_reports.items():
                if key not in reports and content:
                    reports[key] = content if isinstance(content, str) else str(content)

        if "messages" in state and isinstance(state["messages"], list):
            from app.llm.core.types import Message, Role

            messages_reports_count = 0
            for msg in reversed(state["messages"]):
                msg_name = getattr(msg, "name", "")
                if (
                    isinstance(msg, Message)
                    and msg.role == Role.ASSISTANT
                    and msg_name
                    and msg_name.endswith("_report")
                ):
                    report_key = msg.name
                    if report_key not in reports:
                        content = msg.content
                        if content and isinstance(content, str):
                            reports[report_key] = content
                            messages_reports_count += 1
            if messages_reports_count > 0:
                logger.info(
                    f"[报告提取] 从消息历史中恢复了 {messages_reports_count} 个报告"
                )

        return reports

    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        global_memory_manager = get_memory_state_manager()
        result = await global_memory_manager.get_task_dict(task_id)
        if result:
            redis_progress = get_progress_by_id(task_id)
            if redis_progress:
                result.update(
                    {
                        "progress": redis_progress.get(
                            "progress_percentage", result.get("progress", 0)
                        ),
                        "message": redis_progress.get(
                            "last_message", result.get("message", "")
                        ),
                        "steps": redis_progress.get("steps", []),
                    }
                )
        return result

    async def list_user_tasks(
        self,
        user_id: str,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        if status in ("processing", "running"):
            status = "running"

        query = {"user_id": user_id}
        if status == "running":
            query["status"] = {"$in": ["running", "pending", "processing"]}
        elif status:
            query["status"] = status

        try:
            db = get_mongo_db()
            cursor = (
                db.analysis_tasks.find(query)
                .sort("created_at", -1)
                .skip(offset)
                .limit(limit)
            )
            db_tasks = await cursor.to_list(length=limit)

            task_ids = [t.get("task_id") for t in db_tasks if t.get("task_id")]
            memory_map = self.memory_manager.batch_get_task_dicts(task_ids)

            results = []
            for task in db_tasks:
                if "_id" in task:
                    task["_id"] = str(task["_id"])

                task_id = task.get("task_id")
                if task_id and task_id in memory_map:
                    memory_task = memory_map[task_id]
                    task["status"] = memory_task.get("status", task.get("status"))
                    task["progress"] = memory_task.get("progress", task.get("progress"))
                    task["message"] = memory_task.get("message", task.get("message"))
                    task["current_step"] = memory_task.get(
                        "current_step", task.get("current_step")
                    )

                results.append(task)

            enriched = self._enrich_stock_names(results)
            return self._serialize_for_response(enriched)

        except Exception as e:
            logger.error(f"❌ 获取用户任务列表失败 (DB): {e}")
            status_enum = None
            if status:
                try:
                    status_enum = TaskStatus(status)
                except ValueError:
                    pass

            tasks = await self.memory_manager.list_user_tasks(
                user_id=user_id, status=status_enum, limit=limit, offset=offset
            )
            enriched = self._enrich_stock_names(tasks)
            return self._serialize_for_response(enriched)

    async def query_user_tasks(
        self,
        user_id: str,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        symbol: Optional[str] = None,
        market_type: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        if status == "processing":
            status = "running"

        query = {"user_id": user_id}

        if status:
            if status == "running":
                query["status"] = {"$in": ["running", "pending", "processing"]}
            else:
                query["status"] = status

        if symbol:
            query["$or"] = [
                {"symbol": symbol},
                {"stock_code": symbol},
                {"stock_symbol": symbol},
            ]

        if market_type:
            query["parameters.market_type"] = market_type

        date_query = {}
        if start_date:
            try:
                s_date = datetime.strptime(start_date, "%Y-%m-%d")
                date_query["$gte"] = s_date
            except Exception as e:
                logger.debug(f"日期解析失败: start_date={start_date}: {e}")
                pass
        if end_date:
            try:
                e_date = datetime.strptime(end_date, "%Y-%m-%d")
                e_date = e_date.replace(
                    hour=23, minute=59, second=59, microsecond=999999
                )
                date_query["$lte"] = e_date
            except Exception as e:
                logger.debug(f"日期解析失败: end_date={end_date}: {e}")
                pass

        if date_query:
            query["created_at"] = date_query

        try:
            db = get_mongo_db()

            total = await db.analysis_tasks.count_documents(query)

            skip = (page - 1) * page_size
            cursor = (
                db.analysis_tasks.find(query)
                .sort("created_at", -1)
                .skip(skip)
                .limit(page_size)
            )
            db_tasks = await cursor.to_list(length=page_size)

            task_ids = [t.get("task_id") for t in db_tasks if t.get("task_id")]
            memory_map = self.memory_manager.batch_get_task_dicts(task_ids)

            results = []
            for task in db_tasks:
                if "_id" in task:
                    task["_id"] = str(task["_id"])

                task_id = task.get("task_id")
                if task_id and task_id in memory_map:
                    memory_task = memory_map[task_id]
                    task["status"] = memory_task.get("status", task.get("status"))
                    task["progress"] = memory_task.get("progress", task.get("progress"))
                    task["message"] = memory_task.get("message", task.get("message"))
                    task["current_step"] = memory_task.get(
                        "current_step", task.get("current_step")
                    )

                results.append(task)

            enriched_tasks = self._enrich_stock_names(results)

            return self._serialize_for_response(
                {
                    "tasks": enriched_tasks,
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                }
            )

        except Exception as e:
            logger.error(f"❌ 查询用户任务列表失败 (DB): {e}")
            all_tasks = await self.list_user_tasks(
                user_id, status, limit=1000
            )

            filtered = []
            for t in all_tasks:
                if symbol:
                    s = t.get("symbol") or t.get("stock_code") or t.get("stock_symbol")
                    if s != symbol:
                        continue
                if (
                    market_type
                    and t.get("parameters", {}).get("market_type") != market_type
                ):
                    continue
                filtered.append(t)

            start = (page - 1) * page_size
            paginated = filtered[start : start + page_size]

            return self._serialize_for_response(
                {
                    "tasks": paginated,
                    "total": len(filtered),
                    "page": page,
                    "page_size": page_size,
                }
            )

    async def _update_task_status(
        self,
        task_id: str,
        status: AnalysisStatus,
        progress: int,
        error_message: str = None,
    ):
        try:
            db = get_mongo_db()
            update_data = {
                "status": status,
                "progress": progress,
                "updated_at": now_utc(),
            }
            if status == AnalysisStatus.PROCESSING and progress == 10:
                update_data["started_at"] = now_utc()
            elif status == AnalysisStatus.COMPLETED:
                update_data["completed_at"] = now_utc()
            elif status == AnalysisStatus.FAILED:
                update_data["last_error"] = error_message
                update_data["completed_at"] = now_utc()
            await db.analysis_tasks.update_one(
                {"task_id": task_id}, {"$set": update_data}
            )
        except Exception as e:
            logger.error(f"❌ 更新任务状态失败: {task_id} - {e}")

    async def _save_analysis_results_complete(
        self, task_id: str, result: Dict[str, Any]
    ):
        try:
            stock_symbol = result.get("stock_symbol") or result.get(
                "stock_code", "UNKNOWN"
            )
            await self._save_modular_reports_to_data_dir(result, stock_symbol)
            await self._save_analysis_result_web_style(task_id, result)
        except Exception as e:
            logger.error(f"❌ 保存结果失败: {e}")

    async def _save_modular_reports_to_data_dir(
        self, result: Dict[str, Any], stock_symbol: str
    ) -> Dict[str, str]:
        try:
            runtime_base = settings.RUNTIME_BASE_DIR
            results_dir = get_analysis_results_dir(runtime_base)

            analysis_date_raw = result.get("analysis_date", now_config_tz())

            if isinstance(analysis_date_raw, datetime):
                analysis_date_str = analysis_date_raw.strftime("%Y-%m-%d")
            elif isinstance(analysis_date_raw, str):
                try:
                    datetime.strptime(analysis_date_raw, "%Y-%m-%d")
                    analysis_date_str = analysis_date_raw
                except ValueError:
                    analysis_date_str = format_date_short(now_config_tz())
            else:
                analysis_date_str = format_date_short(now_config_tz())

            stock_dir = results_dir / stock_symbol / analysis_date_str
            reports_dir = stock_dir / "reports"
            await asyncio.to_thread(reports_dir.mkdir, parents=True, exist_ok=True)

            log_file = stock_dir / "message_tool.log"
            await asyncio.to_thread(log_file.touch, exist_ok=True)

            reports = result.get("reports", {})
            saved_files = {}

            known_report_titles = {
                "investment_plan": "投资决策报告",
                "trader_investment_plan": "交易计划报告",
                "bull_researcher": "看涨研究报告",
                "bear_researcher": "看跌研究报告",
                "research_team_decision": "研究团队决策报告",
                "risky_analyst": "激进风险分析报告",
                "safe_analyst": "保守风险分析报告",
                "neutral_analyst": "中性风险分析报告",
                "risk_management_decision": "风险管理团队决策报告",
                "risk_manager_decision": "风险管理团队决策报告",
            }

            try:
                from app.engine.agents.analysts.dynamic_analyst import (
                    DynamicAnalystFactory,
                )

                for agent in DynamicAnalystFactory.get_all_agents():
                    slug = agent.get("slug", "")
                    name = agent.get("name", "")
                    if slug and name:
                        internal_key = slug.replace("-analyst", "").replace("-", "_")
                        report_key = f"{internal_key}_report"
                        known_report_titles[report_key] = f"{name}报告"
            except Exception as e:
                logger.warning(f"⚠️ 无法从配置文件加载报告标题: {e}")

            for report_key, report_content in reports.items():
                try:
                    if report_content:
                        filename = f"{report_key}.md"
                        title = known_report_titles.get(
                            report_key, report_key.replace("_", " ").title() + "报告"
                        )

                        file_path = reports_dir / filename
                        await asyncio.to_thread(
                            file_path.write_text, report_content, encoding="utf-8"
                        )

                        saved_files[report_key] = str(file_path)
                        logger.info(f"✅ 保存模块报告: {file_path} ({title})")
                except Exception as e:
                    logger.warning(f"⚠️ 保存模块 {report_key} 失败: {e}")

            decision = result.get("decision", {})
            if decision:
                decision_content = f"# {stock_symbol} 最终投资决策\n\n"
                if isinstance(decision, dict):
                    decision_content += "## 投资建议\n\n"
                    decision_content += f"**行动**: {decision.get('action', 'N/A')}\n\n"
                    decision_content += (
                        f"**置信度**: {decision.get('confidence', 0):.1%}\n\n"
                    )
                    decision_content += (
                        f"**风险评分**: {decision.get('risk_score', 0):.1%}\n\n"
                    )
                    decision_content += (
                        f"**目标价位**: {decision.get('target_price', 'N/A')}\n\n"
                    )
                    decision_content += f"## 分析推理\n\n{decision.get('reasoning', '暂无分析推理')}\n\n"
                else:
                    decision_content += f"{str(decision)}\n\n"

                decision_file = reports_dir / "final_trade_decision.md"
                await asyncio.to_thread(
                    decision_file.write_text, decision_content, encoding="utf-8"
                )
                saved_files["final_trade_decision"] = str(decision_file)

            metadata = {
                "stock_symbol": stock_symbol,
                "analysis_date": analysis_date_str,
                "timestamp": format_iso(now_config_tz()),
                "analysts": result.get("analysts", []),
                "status": "completed",
                "reports_count": len(saved_files),
                "report_types": list(saved_files.keys()),
            }

            metadata_file = reports_dir.parent / "analysis_metadata.json"
            await asyncio.to_thread(
                metadata_file.write_text,
                json.dumps(metadata, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            return saved_files
        except Exception as e:
            logger.error(f"❌ 保存分模块报告失败: {e}")
            return {}

    async def _save_analysis_result_web_style(
        self, task_id: str, result: Dict[str, Any]
    ):
        try:
            db = get_mongo_db()
            stock_symbol = result.get("stock_symbol") or result.get(
                "stock_code", "UNKNOWN"
            )
            timestamp = now_utc()
            analysis_id = (
                result.get("analysis_id")
                or f"{stock_symbol}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
            )

            raw_reports = result.get("reports") or {}
            cleaned_reports: Dict[str, str] = {}
            if isinstance(raw_reports, dict):
                for key, value in raw_reports.items():
                    if value is None:
                        continue
                    if isinstance(value, str):
                        content = value.strip()
                    else:
                        content = json.dumps(value, ensure_ascii=False, indent=2)
                    if content:
                        cleaned_reports[key] = content

            analysis_date = result.get("analysis_date") or timestamp.strftime(
                "%Y-%m-%d"
            )
            summary = result.get("summary", "")
            recommendation = result.get("recommendation", "")
            risk_level = result.get("risk_level", "中等")
            confidence_score = result.get("confidence_score", 0.0)
            key_points = result.get("key_points") or []
            analysts = result.get("analysts") or result.get("selected_analysts") or []
            model_info = (
                result.get("model_info") or result.get("llm_model") or "Unknown"
            )
            tokens_used = result.get("tokens_used") or result.get(
                "token_usage", {}
            ).get("total_tokens", 0)
            token_usage_detail = {}
            try:
                usage_rows = await db.token_usage.aggregate(
                    [
                        {"$match": {"task_id": task_id}},
                        {
                            "$group": {
                                "_id": None,
                                "input_tokens": {"$sum": {"$ifNull": ["$input_tokens", 0]}},
                                "output_tokens": {"$sum": {"$ifNull": ["$output_tokens", 0]}},
                                "cache_read_tokens": {"$sum": {"$ifNull": ["$cache_read_input_tokens", 0]}},
                                "cache_creation_tokens": {"$sum": {"$ifNull": ["$cache_creation_input_tokens", 0]}},
                                "cost": {"$sum": {"$ifNull": ["$cost", 0.0]}},
                            }
                        },
                    ]
                ).to_list(length=1)
                if usage_rows:
                    row = usage_rows[0]
                    token_usage_detail = {
                        "input_tokens": row.get("input_tokens", 0),
                        "output_tokens": row.get("output_tokens", 0),
                        "cache_read_tokens": row.get("cache_read_tokens", 0),
                        "cache_creation_tokens": row.get("cache_creation_tokens", 0),
                        "cost": row.get("cost", 0.0),
                    }
                    tokens_used = (
                        token_usage_detail["input_tokens"]
                        + token_usage_detail["output_tokens"]
                    )
            except Exception as usage_err:
                logger.warning(f"⚠️ token 用量回填失败 task={task_id}: {usage_err}")
            execution_time = result.get("execution_time", 0)
            structured_summary = result.get("structured_summary") or {}
            market_type = (
                result.get("market_type")
                or result.get("parameters", {}).get("market_type")
                or "A股"
            )

            document = {
                "analysis_id": analysis_id,
                "stock_symbol": stock_symbol,
                "stock_name": self._resolve_stock_name(stock_symbol),
                "analysis_date": analysis_date,
                "market_type": market_type,
                "status": result.get("status", "completed"),
                "decision": result.get("decision", {}),
                "structured_summary": structured_summary,
                "task_id": task_id,
                "created_at": timestamp,
                "updated_at": timestamp,
                "summary": summary,
                "recommendation": recommendation,
                "reports": cleaned_reports,
                "confidence_score": confidence_score,
                "risk_level": risk_level,
                "key_points": key_points,
                "analysts": analysts,
                "model_info": model_info,
                "tokens_used": tokens_used,
                "token_usage_detail": token_usage_detail,
                "execution_time": execution_time,
                "source": result.get("source", "analysis_service"),
            }

            insert_result = await db.analysis_reports.insert_one(document)

            document_for_task = {**document, "_id": insert_result.inserted_id}
            await db.analysis_tasks.update_one(
                {"task_id": task_id}, {"$set": {"result": document_for_task}}
            )
        except Exception as e:
            logger.error(f"❌ 保存DB结果失败: {e}")

    async def get_task_with_status_fallback(
        self,
        task_id: str,
        user_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:

        status_info, _ = await self._get_status_with_record(task_id, user_id)
        return status_info

    async def _get_status_with_record(
        self,
        task_id: str,
        user_id: Optional[str] = None,
    ) -> Tuple[Optional[Dict[str, Any]], Dict[str, Any]]:

        result = await self.get_task_status(task_id)
        if result:
            if user_id is None:
                return result, {}
            owner = result.get("user_id")
            if owner is None or owner == user_id:
                return result, {}
            logger.warning(
                f"⚠️ 用户 {user_id} 越权访问任务状态 task_id={task_id} (owner={owner})"
            )
            return None, {}

        try:
            db = get_mongo_db()
            filter_doc: Dict[str, Any] = {"task_id": task_id}
            if user_id is not None:
                filter_doc["$or"] = [
                    {"user_id": user_id},
                    {"user_id": {"$exists": False}},
                    {"user_id": None},
                ]
            task_result = await db.analysis_tasks.find_one(filter_doc)
        except Exception as e:
            logger.warning(
                f"⚠️ get_task_with_status_fallback 查询 analysis_tasks 失败: {e}"
            )
            task_result = None

        if task_result:
            status = task_result.get("status", "pending")
            progress = task_result.get("progress", 0)
            start_time = task_result.get("started_at") or task_result.get("created_at")
            end_time = task_result.get("completed_at")
            elapsed_time = 0.0
            if start_time and status in {"pending", "running"}:
                end_ref = end_time or now_utc()
                elapsed_time = (end_ref - start_time).total_seconds()
            elif start_time and end_time:
                elapsed_time = (end_time - start_time).total_seconds()

            message = _TASK_STATUS_MESSAGES.get(status, "任务进行中…")

            status_dict = {
                "task_id": task_id,
                "status": status,
                "progress": progress,
                "message": message,
                "current_step": status,
                "start_time": start_time,
                "end_time": end_time,
                "elapsed_time": elapsed_time,
                "remaining_time": 0,
                "estimated_total_time": 0,
                "symbol": task_result.get("symbol") or task_result.get("stock_code"),
                "stock_code": task_result.get("symbol")
                or task_result.get("stock_code"),
                "stock_symbol": task_result.get("symbol")
                or task_result.get("stock_code"),
                "source": "mongodb_tasks",
            }
            return status_dict, task_result

        report = await self._find_report_by_task_id(task_id, user_id)
        if report:
            start_time = report.get("created_at")
            end_time = report.get("updated_at")
            elapsed_time = 0
            if start_time and end_time:
                elapsed_time = (end_time - start_time).total_seconds()

            report_dict = {
                "task_id": task_id,
                "status": "completed",
                "progress": 100,
                "message": "分析完成（从历史记录恢复）",
                "current_step": "completed",
                "start_time": start_time,
                "end_time": end_time,
                "elapsed_time": elapsed_time,
                "remaining_time": 0,
                "estimated_total_time": elapsed_time,
                "stock_code": report.get("stock_symbol"),
                "stock_symbol": report.get("stock_symbol"),
                "source": "mongodb_reports",
            }
            return report_dict, {}

        return None, {}

    async def get_task_overview(
        self,
        task_id: str,
        user_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:

        status_info, record = await self._get_status_with_record(task_id, user_id)
        if not status_info:
            return None

        if not record and status_info.get("source") != "mongodb_reports":
            try:
                db = get_mongo_db()
                filter_doc: Dict[str, Any] = {"task_id": task_id}
                if user_id is not None:
                    filter_doc["$or"] = [
                        {"user_id": user_id},
                        {"user_id": {"$exists": False}},
                        {"user_id": None},
                    ]
                record = await db.analysis_tasks.find_one(filter_doc) or {}
            except Exception as e:
                logger.warning(f"⚠️ get_task_overview 查询 analysis_tasks 失败: {e}")
                record = {}

        parameters = record.get("parameters")
        if not isinstance(parameters, dict):
            mem_task = await self.memory_manager.get_task_dict(task_id)
            parameters = (mem_task or {}).get("parameters")
        if not isinstance(parameters, dict):
            parameters = {}
        market_type = (
            parameters.get("market_type") or record.get("market_type") or "A股"
        )

        return {
            "task_id": task_id,
            "status": record.get("status") or status_info.get("status"),
            "symbol": record.get("symbol")
            or record.get("stock_code")
            or status_info.get("symbol")
            or status_info.get("stock_symbol"),
            "market_type": market_type,
            "parameters": parameters,
            "created_at": record.get("created_at"),
            "started_at": record.get("started_at") or status_info.get("start_time"),
            "completed_at": record.get("completed_at") or status_info.get("end_time"),
        }

    async def _find_report_by_task_id(
        self,
        task_id: str,
        user_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:

        try:
            db = get_mongo_db()
            filter_doc: Dict[str, Any] = {"task_id": task_id}
            if user_id is not None:
                filter_doc["$or"] = [
                    {"user_id": user_id},
                    {"user_id": {"$exists": False}},
                    {"user_id": None},
                ]
            report = await db.analysis_reports.find_one(filter_doc)
            if report:
                return report

            tasks_filter: Dict[str, Any] = {"task_id": task_id}
            if user_id is not None:
                tasks_filter["$or"] = [
                    {"user_id": user_id},
                    {"user_id": {"$exists": False}},
                    {"user_id": None},
                ]
            tasks_doc = await db.analysis_tasks.find_one(
                tasks_filter, {"result.analysis_id": 1}
            )
            if tasks_doc:
                analysis_id = tasks_doc.get("result", {}).get("analysis_id")
                if analysis_id:
                    return await db.analysis_reports.find_one(
                        {"analysis_id": analysis_id}
                    )
        except Exception as e:
            logger.warning(f"⚠️ _find_report_by_task_id 失败: {e}")
        return None

    async def get_task_result_data(
        self,
        task_id: str,
        user_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:

        task_status = await self.get_task_status(task_id)
        if (
            task_status
            and task_status.get("status") == "completed"
            and task_status.get("result_data")
        ):
            if user_id is None:
                return task_status["result_data"]
            owner = task_status.get("user_id")
            if owner is None or owner == user_id:
                return task_status["result_data"]
            logger.warning(
                f"⚠️ 用户 {user_id} 越权读取任务结果 task_id={task_id} (owner={owner})"
            )
            return None

        mongo_result = await self._find_report_by_task_id(task_id, user_id)
        if mongo_result:
            result_data = {
                "analysis_id": mongo_result.get("analysis_id"),
                "stock_symbol": mongo_result.get("stock_symbol"),
                "stock_code": mongo_result.get("stock_symbol"),
                "analysis_date": mongo_result.get("analysis_date"),
                "summary": mongo_result.get("summary", ""),
                "recommendation": mongo_result.get("recommendation", ""),
                "confidence_score": mongo_result.get("confidence_score", 0.0),
                "risk_level": mongo_result.get("risk_level", "中等"),
                "key_points": mongo_result.get("key_points", []),
                "execution_time": mongo_result.get("execution_time", 0),
                "tokens_used": mongo_result.get("tokens_used", 0),
                "analysts": mongo_result.get("analysts", []),
                "reports": mongo_result.get("reports", {}),
                "created_at": mongo_result.get("created_at"),
                "updated_at": mongo_result.get("updated_at"),
                "status": mongo_result.get("status", "completed"),
                "decision": mongo_result.get("decision", {}),
                "source": "mongodb",
            }
            return result_data

        try:
            db = get_mongo_db()
            fallback_filter: Dict[str, Any] = {"task_id": task_id}
            if user_id is not None:
                fallback_filter["$or"] = [
                    {"user_id": user_id},
                    {"user_id": {"$exists": False}},
                    {"user_id": None},
                ]
            tasks_doc = await db.analysis_tasks.find_one(
                fallback_filter,
                {
                    "result": 1,
                    "symbol": 1,
                    "stock_code": 1,
                    "created_at": 1,
                    "completed_at": 1,
                },
            )
            if tasks_doc and tasks_doc.get("result"):
                r = tasks_doc["result"] or {}
                symbol = (
                    tasks_doc.get("symbol")
                    or tasks_doc.get("stock_code")
                    or r.get("stock_symbol")
                    or r.get("stock_code")
                )
                return {
                    "analysis_id": r.get("analysis_id"),
                    "stock_symbol": symbol,
                    "stock_code": symbol,
                    "analysis_date": r.get("analysis_date"),
                    "summary": r.get("summary", ""),
                    "recommendation": r.get("recommendation", ""),
                    "confidence_score": r.get("confidence_score", 0.0),
                    "risk_level": r.get("risk_level", "中等"),
                    "key_points": r.get("key_points", []),
                    "execution_time": r.get("execution_time", 0),
                    "tokens_used": r.get("tokens_used", 0),
                    "analysts": r.get("analysts", []),
                    "reports": r.get("reports", {}),
                    "state": r.get("state", {}),
                    "detailed_analysis": r.get("detailed_analysis", {}),
                    "created_at": tasks_doc.get("created_at"),
                    "updated_at": tasks_doc.get("completed_at"),
                    "status": r.get("status", "completed"),
                    "decision": r.get("decision", {}),
                    "source": "analysis_tasks",
                }
        except Exception as e:
            logger.warning(
                f"⚠️ get_task_result_data 从 analysis_tasks.result 兜底失败: {e}"
            )

        return None

    async def mark_task_failed(
        self, task_id: str, error_message: str = "用户手动标记为失败"
    ) -> bool:
        try:
            await self.memory_manager.update_task_status(
                task_id=task_id,
                status=TaskStatus.FAILED,
                message="手动标记为失败",
                error_message=error_message,
            )

            db = get_mongo_db()
            result = await db.analysis_tasks.update_one(
                {"task_id": task_id},
                {
                    "$set": {
                        "status": "failed",
                        "last_error": error_message,
                        "completed_at": now_utc(),
                        "updated_at": now_utc(),
                    }
                },
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"❌ mark_task_failed 失败: {e}")
            return False

    async def validate_task_ownership(self, task_id: str, user_id: str) -> bool:

        task = await self.memory_manager.get_task_dict(task_id)
        if task and task.get("user_id") == user_id:
            return True

        try:
            db = get_mongo_db()
            task_doc = await db.analysis_tasks.find_one(
                {"task_id": task_id}, {"user_id": 1}
            )
            return task_doc is not None and task_doc.get("user_id") == user_id
        except Exception as e:
            logger.error(f"❌ validate_task_ownership 查询失败: {e}")
            return False

    async def delete_task_by_id(
        self, task_id: str, user_id: Optional[str] = None
    ) -> bool:

        try:
            filter_doc: Dict[str, Any] = {"task_id": task_id}
            if user_id is not None:
                filter_doc["user_id"] = user_id

            db = get_mongo_db()
            result = await db.analysis_tasks.delete_one(filter_doc)

            if result.deleted_count > 0:
                await self.memory_manager.remove_task(task_id)
                return True

            if user_id is not None:
                existing = await db.analysis_tasks.find_one(
                    {"task_id": task_id}, {"user_id": 1}
                )
                if existing and existing.get("user_id") != user_id:
                    logger.warning(f"⚠️ 用户 {user_id} 尝试删除非本人任务: {task_id}")
                    return False

            await self.memory_manager.remove_task(task_id)
            return False
        except Exception as e:
            logger.error(f"❌ delete_task_by_id 失败: {e}")
            return False

    async def get_analysis_stats(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        market_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        try:
            db = get_mongo_db()
            query: Dict[str, Any] = {}
            if start_date or end_date:
                date_query: Dict[str, Any] = {}
                if start_date:
                    date_query["$gte"] = start_date
                if end_date:
                    date_query["$lte"] = end_date
                query["created_at"] = date_query
            if market_type:
                query["market_type"] = market_type

            total = await db.analysis_reports.count_documents(query)
            completed = await db.analysis_reports.count_documents(
                {**query, "status": "completed"}
            )
            failed = await db.analysis_reports.count_documents(
                {**query, "status": "failed"}
            )

            pipeline_date = [
                {"$match": query},
                {
                    "$group": {
                        "_id": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": "$created_at",
                            }
                        },
                        "count": {"$sum": 1},
                    }
                },
                {"$sort": {"_id": -1}},
                {"$limit": 30},
            ]
            by_date = []
            async for doc in db.analysis_reports.aggregate(pipeline_date):
                by_date.append({"date": doc["_id"], "count": doc["count"]})

            pipeline_market = [
                {"$match": query},
                {"$group": {"_id": "$market_type", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
            ]
            by_market = []
            async for doc in db.analysis_reports.aggregate(pipeline_market):
                by_market.append(
                    {"market": doc["_id"] or "未知", "count": doc["count"]}
                )

            return {
                "total_analyses": total,
                "successful_analyses": completed,
                "failed_analyses": failed,
                "avg_duration": 0,
                "total_tokens": 0,
                "total_cost": 0,
                "popular_stocks": [],
                "analysis_by_date": by_date,
                "analysis_by_market": by_market,
            }
        except Exception as e:
            logger.error(f"❌ get_analysis_stats 失败: {e}")
            raise

    async def search_stock_basic_info(
        self,
        query: str,
        market: Optional[str] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        try:
            from app.data.core.interface import DataInterface

            di = DataInterface.get_instance()
            docs = await di.search_basic_info(
                "CN", query, fields=["symbol", "name"], limit=limit
            )

            results = []
            for doc in docs:
                if market and doc.get("market") != market:
                    continue
                results.append(
                    {
                        "symbol": doc.get("symbol", ""),
                        "name": doc.get("name", ""),
                        "market": doc.get("market", "A股"),
                        "type": "stock",
                    }
                )
            return results
        except Exception as e:
            logger.error(f"❌ search_stock_basic_info 失败: {e}")
            raise

analysis_service: Optional[AnalysisService] = None

def get_analysis_service() -> AnalysisService:
    global analysis_service
    if analysis_service is None:
        analysis_service = AnalysisService()
    return analysis_service
