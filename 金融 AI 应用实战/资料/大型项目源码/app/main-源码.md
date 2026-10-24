---
type: 原始源码副本
---

来源：`app/main.py`。原始完整文件，未修改代码。

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
import re
import asyncio

from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.logging_config import setup_logging
from app.core.response import safe_error_message
import jwt as _jwt
from app.routers import auth_db as auth, analysis, screening, health, favorites, config, reports, database, operation_logs, tags, news_data, usage_statistics, model_capabilities, cache, logs
from app.routers import mcp, tools
from app.routers import agent_configs
from app.routers import skills as skills_router
from app.routers import stocks as stocks_router
from app.routers import notifications as notifications_router
from app.routers import websocket_notifications as websocket_notifications_router
from app.routers import scheduler as scheduler_router
from app.data.scheduler.engine import SchedulerEngine
from app.services.scheduler_service import set_scheduler_instance
from app.middleware.operation_log_middleware import OperationLogMiddleware
from app.routers.health import get_version

def _sanitize_url(url: str) -> str:

    return re.sub(r'://([^@:]+):([^@]+)@', r'://***@', url)

async def _print_config_summary(logger):
    try:
        logger.info("=" * 70)
        logger.info("📋 Zhenshabi Configuration Summary")
        logger.info("=" * 70)

        from pathlib import Path
        from app.core.config import redact_env_line

        current_dir = Path.cwd()
        logger.info(f"📁 Current working directory: {current_dir}")

        env_files_to_check = [
            current_dir / ".env",
            current_dir / "app" / ".env",
            Path(__file__).parent.parent / ".env",
        ]

        logger.info("🔍 Checking .env file locations:")
        env_file_found = False
        for env_file in env_files_to_check:
            if env_file.exists():
                logger.info(f"  ✅ Found: {env_file} (size: {env_file.stat().st_size} bytes)")
                env_file_found = True
                try:
                    with open(env_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()[:5]
                        logger.info("     Preview (first 5 lines):")
                        for i, raw_line in enumerate(lines, 1):
                            safe_line = redact_env_line(raw_line.rstrip("\n"))
                            logger.info(f"       {i}: {safe_line}")
                except Exception as e:
                    logger.warning(f"     Could not preview file: {e}")
            else:
                logger.info(f"  ❌ Not found: {env_file}")
        
        if not env_file_found:
            logger.warning("⚠️  No .env file found in checked locations")
        
        logger.info("⚙️  Pydantic Settings Configuration:")
        logger.info(f"  • Settings class: {settings.__class__.__name__}")
        logger.info(f"  • Config source: {getattr(settings.model_config, 'env_file', 'Not specified')}")
        logger.info(f"  • Encoding: {getattr(settings.model_config, 'env_file_encoding', 'Not specified')}")
        
        key_settings = ['HOST', 'PORT', 'DEBUG', 'MONGODB_HOST', 'REDIS_HOST']
        logger.info("  • Key settings sources:")
        for setting_name in key_settings:
            env_var_name = setting_name
            from app.core.env import get_env
            env_value = get_env(env_var_name)
            config_value = getattr(settings, setting_name, None)
            if env_value is not None:
                logger.info(f"    - {setting_name}: from environment variable ({config_value})")
            else:
                logger.info(f"    - {setting_name}: using default value ({config_value})")
        
        env = "Production" if settings.is_production else "Development"
        logger.info(f"Environment: {env}")

        logger.info(f"MongoDB: {settings.MONGODB_HOST}:{settings.MONGODB_PORT}/{settings.MONGODB_DATABASE}")
        logger.info(f"Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}")

        if settings.HTTP_PROXY or settings.HTTPS_PROXY:
            logger.info("Proxy Configuration:")
            if settings.HTTP_PROXY:
                logger.info(f"  HTTP_PROXY: {_sanitize_url(settings.HTTP_PROXY)}")
            if settings.HTTPS_PROXY:
                logger.info(f"  HTTPS_PROXY: {_sanitize_url(settings.HTTPS_PROXY)}")
            if settings.NO_PROXY:
                no_proxy_list = settings.NO_PROXY.split(',')
                if len(no_proxy_list) <= 3:
                    logger.info(f"  NO_PROXY: {settings.NO_PROXY}")
                else:
                    logger.info(f"  NO_PROXY: {','.join(no_proxy_list[:3])}... ({len(no_proxy_list)} domains)")
            logger.info("  ✅ Proxy environment variables set successfully")
        else:
            logger.info("Proxy: Not configured (direct connection)")

        try:
            from app.services.config_service import config_service
            config = await config_service.get_system_config()
            if config and config.llm_configs:
                enabled_llms = [llm for llm in config.llm_configs if llm.enabled]
                logger.info(f"Enabled LLMs: {len(enabled_llms)}")
                if enabled_llms:
                    for llm in enabled_llms[:3]:
                        logger.info(f"  • {llm.provider}: {llm.model_name}")
                    if len(enabled_llms) > 3:
                        logger.info(f"  • ... and {len(enabled_llms) - 3} more")
                else:
                    logger.warning("⚠️  No LLM enabled. Please configure at least one LLM in Web UI.")
            else:
                logger.warning("⚠️  No LLM configured. Please configure at least one LLM in Web UI.")
        except Exception as e:
            logger.warning(f"⚠️  Failed to check LLM configs: {e}")

        try:
            if config and config.data_source_configs:
                enabled_sources = [ds for ds in config.data_source_configs if ds.enabled]
                logger.info(f"Enabled Data Sources: {len(enabled_sources)}")
                if enabled_sources:
                    for ds in enabled_sources[:3]:
                        logger.info(f"  • {ds.type.value}: {ds.name}")
                    if len(enabled_sources) > 3:
                        logger.info(f"  • ... and {len(enabled_sources) - 3} more")
            else:
                logger.info("Data Sources: Using default (AKShare)")
        except Exception as e:
            logger.warning(f"⚠️  Failed to check data source configs: {e}")

        logger.info("=" * 70)
    except Exception as e:
        logger.error(f"Failed to print config summary: {e}")

async def _init_database(logger):
    await init_db()

    from app.services.user_service import user_service
    from app.core.database import get_mongo_db
    user_service.set_database(get_mongo_db())
    logger.info("✅ UserService 数据库连接已初始化")

async def _init_secrets(logger):

    try:
        from app.services.secret_service import SecretService
        secrets = await SecretService.ensure_secrets()
        if secrets:
            logger.info(f"✅ 安全密钥已就绪（{len(secrets)} 个）")
        SecretService.persist_to_env()
        logger.debug("安全密钥已同步到 os.environ（多 worker 兼容）")
    except Exception as e:
        logger.warning(f"⚠️  安全密钥初始化失败: {e}，将使用运行期随机密钥")

async def _init_system_defaults(logger):
    from app.services.system_init_service import SystemInitService
    await SystemInitService.initialize_system()

async def _migrate_protocol_to_providers(logger):
    from app.services.config.llm_service import LLMService
    result = await LLMService().migrate_model_protocol_to_providers()
    if result.get("migrated_providers") or result.get("cleaned_configs"):
        logger.info(f"🔄 协议字段上移厂家级迁移完成: {result}")

async def _init_config_bridge(logger):
    try:
        from app.core.config_bridge import bridge_config_to_env
        bridge_success = await asyncio.wait_for(bridge_config_to_env(), timeout=30)
        if not bridge_success:
            logger.warning("⚠️  配置桥接未成功完成，Zhenshabi 将使用 .env 文件中的配置")
    except asyncio.TimeoutError:
        logger.error("❌ 配置桥接超时（30 秒），启动流程将降级使用 .env 配置")
    except Exception as e:
        logger.warning(f"⚠️  配置桥接失败: {e}")

async def _apply_dynamic_settings(logger):
    try:
        from app.services.config_provider import provider as config_provider
        eff = await config_provider.get_effective_system_settings()

        from app.engine.config.runtime_settings import set_cached_settings
        set_cached_settings(eff)

        desired_level = str(eff.get("log_level", "INFO")).upper()
        setup_logging(log_level=desired_level)
        for name in ("webapi", "worker", "uvicorn", "fastapi"):
            logging.getLogger(name).setLevel(desired_level)
        try:
            from app.middleware.operation_log_middleware import set_operation_log_enabled
            set_operation_log_enabled(bool(eff.get("enable_monitoring", True)))
        except Exception as e:
            logging.getLogger(__name__).debug(f"设置操作日志开关失败: {e}")
    except Exception as e:
        logging.getLogger(__name__).warning(f"Failed to apply dynamic settings: {e}")

async def _init_scheduler(logger):
    from apscheduler.schedulers.asyncio import AsyncIOScheduler

    apscheduler = AsyncIOScheduler(timezone=settings.TIMEZONE)
    engine = SchedulerEngine(scheduler=apscheduler)
    engine.start()

    from app.data.scheduler.monitors import SchedulerMonitor
    monitor = SchedulerMonitor()
    monitor.start(apscheduler)
    logger.info("✅ 调度任务监控已启动（超时检测 + 统计 + 并发保护）")

    set_scheduler_instance(apscheduler)
    logger.info("调度器服务已初始化（统一调度引擎）")
    return apscheduler

async def _init_mcp(logger):
    from app.llm.mcp import service as mcp_service
    from app.core.task_registry import task_registry

    logger.info("🔧 初始化 MCP 连接管理器（新层 MCPManager）...")
    connected = await mcp_service.startup()

    async def mcp_health_check_loop():
        while True:
            try:
                for name in list(mcp_service.enabled_server_configs()):
                    await mcp_service.ping_server(name)
                await asyncio.sleep(30)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"MCP 健康检查失败: {e}")
                await asyncio.sleep(30)

    task_registry.register(
        mcp_health_check_loop(),
        name="mcp_health_check",
        critical=False,
    )
    logger.info(f"✅ MCP 连接已初始化（{connected} 个 server），健康检查任务已启动")
    return None

def _check_default_secrets(logger: logging.Logger):

    from app.core.config import is_using_default_secret, settings as _settings

    is_production = not bool(getattr(_settings, "DEBUG", True))
    for env_key in ("JWT_SECRET", "CSRF_SECRET"):
        if not is_using_default_secret(env_key):
            continue
        if is_production:
            logger.error(
                f"{'!' * 70}\n"
                f"  FATAL: {env_key} 使用了默认/示例值，生产环境禁止启动！\n"
                f"  请在 .env 中设置强随机密钥后重试。\n"
                f"{'!' * 70}"
            )
            raise RuntimeError(
                f"{env_key} 在生产模式下使用了不安全默认值，启动被拒绝"
            )
        logger.warning(
            f"{'!' * 70}\n"
            f"  SECURITY WARNING: {env_key} is using a default/docker value!\n"
            f"  This is insecure for production. Please set a strong secret in .env.\n"
            f"{'!' * 70}"
        )

async def lifespan(app: FastAPI):
    setup_logging()
    logger = logging.getLogger("app.main")

    try:
        import asyncio as _asyncio
        from concurrent.futures import ThreadPoolExecutor
        from app.core.config import settings as _settings
        loop = _asyncio.get_running_loop()
        loop.set_default_executor(
            ThreadPoolExecutor(max_workers=_settings.ASYNC_THREAD_POOL_SIZE)
        )
        logger.info(
            f"🔧 默认异步线程池上限: {_settings.ASYNC_THREAD_POOL_SIZE}"
        )
    except Exception as e:
        logger.warning(f"⚠️ 设置默认线程池上限失败: {e}")

    from app.core.startup_validator import validate_startup_config
    validate_startup_config()

    _check_default_secrets(logger)

    await _init_database(logger)

    from app.core.async_utils import set_main_loop
    set_main_loop(asyncio.get_running_loop())

    from app.services.token_usage_recorder import token_usage_recorder
    token_usage_recorder.set_server_loop(asyncio.get_running_loop())

    await _init_secrets(logger)
    await _init_system_defaults(logger)
    await _migrate_protocol_to_providers(logger)
    await _init_config_bridge(logger)
    await _apply_dynamic_settings(logger)

    from app.middleware.rate_limit import start_redis_recovery_loop, stop_redis_recovery_loop
    start_redis_recovery_loop()

    await _print_config_summary(logger)

    logger.info("Zhenshabi FastAPI backend started")

    scheduler = None
    try:
        scheduler = await _init_scheduler(logger)
    except Exception as e:
        logger.error(f"❌ 调度器启动失败: {e}", exc_info=True)
        raise

    try:
        await _init_mcp(logger)
    except Exception as e:
        logger.error(f"❌ MCP 初始化失败: {e}", exc_info=True)
        logger.warning("⚠️  应用将在 MCP 功能不可用的情况下继续运行")

    from app.data.monitoring.source_health import SourceHealthMonitor
    health_monitor = SourceHealthMonitor()
    health_monitor.start()
    logger.info("✅ 数据源健康监控已启动（每 30s 刷入 MongoDB）")

    try:
        from app.engine.tools.skill.dependency_installer import (
            ensure_all_skills_dependencies,
        )
        result = await ensure_all_skills_dependencies()
        logger.info(
            f"✅ Skill 依赖检查完成: total={result['total']}, "
            f"installed={result['installed']}, "
            f"failed={result['failed']}, skipped={result['skipped']}"
        )
    except Exception as e:
        logger.warning(f"⚠️  Skill 依赖启动安装失败（不阻塞启动）: {e}")

    try:
        yield
    finally:
        try:
            from app.middleware.rate_limit import stop_redis_recovery_loop
            stop_redis_recovery_loop()
        except Exception as e:
            logger.warning(f"Redis 自愈协程停止失败: {e}")

        try:
            health_monitor.stop()
            logger.info("🛑 数据源健康监控已停止")
        except Exception as e:
            logger.warning(f"数据源健康监控停止失败: {e}")

        try:
            from app.llm.mcp import service as mcp_service
            await mcp_service.shutdown()
            logger.info("🛑 MCP 连接已关闭")
        except Exception as e:
            logger.warning(f"MCP 连接关闭失败: {e}")

        try:
            from app.data.scheduler.monitors import SchedulerMonitor
            monitor = SchedulerMonitor()
            monitor.stop()
            logger.info("🛑 调度任务监控已停止")
        except Exception as e:
            logger.warning(f"调度任务监控停止失败: {e}")

        if scheduler:
            try:
                scheduler.shutdown(wait=True)
                logger.info("🛑 Scheduler stopped")
            except Exception as e:
                logger.warning(f"Scheduler shutdown error: {e}")

        try:
            from app.services.analysis_service import get_analysis_service
            svc = get_analysis_service()
            svc._shutdown_pool(wait=True)
            logger.info("🛑 Analysis service thread pool stopped")
        except Exception as e:
            logger.warning(f"Analysis service thread pool shutdown error: {e}")

        try:
            from app.core.task_registry import task_registry
            await task_registry.shutdown(timeout=5.0)
            stats = task_registry.get_stats()
            logger.info(
                f"🛑 TaskRegistry shutdown 完成: created={stats['total_created']} "
                f"completed={stats['total_completed']} failed={stats['total_failed']}"
            )
        except Exception as e:
            logger.warning(f"TaskRegistry shutdown 失败: {e}")

        await close_db()
        logger.info("Zhenshabi FastAPI backend stopped")

app = FastAPI(
    title="Zhenshabi API",
    description="股票分析与批量队列系统 API",
    version=get_version(),
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-Requested-With",
        "X-CSRF-Token",
        "X-Request-ID",
    ],
)

from app.middleware.csrf import CSRFMiddleware
app.add_middleware(CSRFMiddleware)

app.add_middleware(OperationLogMiddleware)

from app.middleware.rate_limit import RateLimitMiddleware, QuotaMiddleware
app.add_middleware(QuotaMiddleware)
app.add_middleware(RateLimitMiddleware)

from app.middleware.request_id import RequestIDMiddleware
app.add_middleware(RequestIDMiddleware)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)

    if isinstance(exc, ValueError):
        logging.warning(f"Validation error: {exc}")
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": safe_error_message(exc, "请求参数无效"),
                    "request_id": request_id
                }
            }
        )

    if isinstance(exc, PermissionError):
        logging.warning(f"Permission denied: {exc}")
        return JSONResponse(
            status_code=403,
            content={
                "error": {
                    "code": "PERMISSION_DENIED",
                    "message": "权限不足",
                    "request_id": request_id
                }
            }
        )

    if isinstance(exc, FileNotFoundError):
        logging.warning(f"Resource not found: {exc}")
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "code": "RESOURCE_NOT_FOUND",
                    "message": "请求的资源不存在",
                    "request_id": request_id
                }
            }
        )

    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Internal server error occurred",
                "request_id": request_id
            }
        }
    )

@app.exception_handler(_jwt.ExpiredSignatureError)
async def jwt_expired_handler(request: Request, exc: _jwt.ExpiredSignatureError):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=401,
        content={
            "error": {
                "code": "TOKEN_EXPIRED",
                "message": "登录已过期，请重新登录",
                "request_id": request_id
            }
        }
    )

@app.exception_handler(_jwt.InvalidTokenError)
async def jwt_invalid_handler(request: Request, exc: _jwt.InvalidTokenError):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=401,
        content={
            "error": {
                "code": "TOKEN_INVALID",
                "message": "认证信息无效",
                "request_id": request_id
            }
        }
    )

@app.exception_handler(RuntimeError)
async def runtime_error_handler(request: Request, exc: RuntimeError):
    request_id = getattr(request.state, "request_id", None)
    logging.error(f"Runtime error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "RUNTIME_ERROR",
                "message": safe_error_message(exc, "服务暂时不可用"),
                "request_id": request_id
            }
        }
    )

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(analysis.router)
app.include_router(reports.router)
app.include_router(screening.router)
app.include_router(favorites.router)
app.include_router(stocks_router.router)
app.include_router(tags.router)
app.include_router(config.router)
app.include_router(model_capabilities.router)
app.include_router(usage_statistics.router)
app.include_router(database.router)
app.include_router(cache.router)
app.include_router(operation_logs.router)
app.include_router(logs.router)
from app.routers import system_config as system_config_router
app.include_router(system_config_router.router)
app.include_router(mcp.router)
app.include_router(tools.router)
app.include_router(agent_configs.router)

app.include_router(skills_router.router)

app.include_router(notifications_router.router)

app.include_router(websocket_notifications_router.router)

app.include_router(scheduler_router.router)

app.include_router(news_data.router)

from app.routers.cn import data as cn_data, sync as cn_sync
from app.routers.hk import data as hk_data, sync as hk_sync
from app.routers.us import data as us_data, sync as us_sync

app.include_router(cn_data.router)
app.include_router(cn_sync.router)
app.include_router(hk_data.router)
app.include_router(hk_sync.router)
app.include_router(us_data.router)
app.include_router(us_sync.router)

@app.get("/")
async def root():
    logging.getLogger("app.main").debug("Root path accessed")
    return {
        "name": "Zhenshabi API",
        "version": get_version(),
        "status": "running",
        "docs_url": "/docs" if settings.DEBUG else None
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_config=None,
        log_level="info",
        reload_dirs=["app"] if settings.DEBUG else None,
        reload_excludes=[
            "__pycache__",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".git",
            ".pytest_cache",
            "*.log",
            "*.tmp"
        ] if settings.DEBUG else None,
        reload_includes=["*.py"] if settings.DEBUG else None
    )

```
