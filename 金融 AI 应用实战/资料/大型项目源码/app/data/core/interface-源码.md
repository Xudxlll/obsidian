---
type: 原始源码副本
---

来源：`app/data/core/interface.py`。原始完整文件，未修改代码。

```python
import logging
import threading
from typing import Dict, List, Optional

from app.data.core.result import RefreshResult
from app.data.core.reader import Reader
from app.data.core.refresh_service import DataRefreshService
from app.data.core.registry.capability import CapabilityRegistry
from app.data.core.registry.priority import PriorityConfig

logger = logging.getLogger(__name__)

_instance: Optional["DataInterface"] = None
_instance_lock = threading.Lock()

class DataInterface:

    def __init__(self, sync_trigger_callback=None):
        self.reader = Reader()
        self._registry = CapabilityRegistry()
        self._priority = PriorityConfig()
        self.refresh_service = DataRefreshService(self._registry, self._priority)
        self._sync_trigger_callback = sync_trigger_callback

        from app.data.storage.mongo.repositories.metadata_repo import MetadataRepo

        self._metadata_repo = MetadataRepo()

    @classmethod
    def get_instance(cls) -> "DataInterface":
        global _instance
        if _instance is None:
            with _instance_lock:
                if _instance is None:
                    _instance = cls()
        return _instance

    @classmethod
    def reset_instance(cls) -> None:
        global _instance
        with _instance_lock:
            _instance = None

    async def read(
        self,
        market: str,
        domain: str,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        filters: Optional[Dict] = None,
    ) -> Dict:

        data, freshness = await self.reader.get_data(
            market,
            domain,
            symbol,
            start_date=start_date,
            end_date=end_date,
            filters=filters,
        )
        return {
            "data": data,
            "freshness": freshness,
            "market": market,
            "symbol": symbol,
            "domain": domain,
        }

    async def read_latest(
        self,
        market: str,
        domain: str,
        symbol: str,
        projection: Optional[Dict] = None,
    ) -> Optional[Dict]:
        return await self.reader.read_latest(market, domain, symbol, projection)

    async def read_latest_batch(
        self,
        market: str,
        domain: str,
        symbols: List[str],
        projection: Optional[Dict] = None,
    ) -> Dict[str, Dict]:
        return await self.reader.read_latest_batch(
            market, domain, symbols, projection
        )

    async def read_batch(
        self,
        market: str,
        domain: str,
        symbols: List[str],
        projection: Optional[Dict] = None,
        sort: Optional[List] = None,
        limit: int = 0,
    ) -> List[Dict]:
        return await self.reader.read_batch(
            market, domain, symbols, projection, sort, limit
        )

    async def search_basic_info(
        self,
        market: str,
        query: str,
        fields: Optional[List[str]] = None,
        limit: int = 20,
    ) -> List[Dict]:
        return await self.reader.search_basic_info(market, query, fields, limit)

    async def screen(
        self,
        market: str,
        stage: str,
        filters: Optional[Dict] = None,
        projection: Optional[Dict] = None,
        sort: Optional[List] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Dict:
        from app.data.query.screening_query import ScreeningQueryService

        return await ScreeningQueryService().screen(
            market, stage,
            filters=filters,
            projection=projection,
            sort=sort,
            skip=skip,
            limit=limit,
        )

    async def refresh(
        self,
        market: str,
        symbol: str,
        domains: Optional[List[str]] = None,
        force: bool = False,
        timeout: int = 30,
    ) -> RefreshResult:
        return await self.refresh_service.refresh(
            market, symbol, domains, force, timeout
        )

    async def trigger_sync(
        self,
        market: str,
        domain: str,
        mode: Optional[str] = None,
        source: Optional[str] = None,
    ) -> str:

        from datetime import datetime, timezone

        task_id = (
            f"sync_{market}_{domain}_{int(datetime.now(timezone.utc).timestamp())}"
        )

        if self._sync_trigger_callback:
            try:
                import inspect

                result = self._sync_trigger_callback(market, domain)
                if inspect.iscoroutine(result):
                    result = await result
                if result:
                    logger.info(f"通过回调触发同步: {result}")
                    return result
            except Exception as e:
                logger.warning(f"回调触发失败: {e}")

        try:
            from app.worker.scheduler_setup import get_scheduler_engine

            engine = get_scheduler_engine()
            if engine:
                result = engine.run_job_now(market, domain, mode=mode, source=source)
                if result.get("status") in ("triggered", "already_running"):
                    logger.info(f"通过调度引擎触发同步: {result['task_id']}")
                    return result["task_id"]
        except Exception as e:
            logger.warning(f"调度引擎触发失败，降级到直接同步: {e}")

        repo = self._metadata_repo
        await repo.insert_event(
            {
                "market": market,
                "event_type": "SYNC_START",
                "domain": domain,
                "task_id": task_id,
            }
        )
        logger.info(f"记录同步事件（降级模式）: {task_id}")
        return task_id

    async def get_running_sync_tasks(self, market: str) -> List[Dict]:

        try:
            from app.data.scheduler.monitors import SchedulerMonitor

            monitor = SchedulerMonitor()
            if not getattr(monitor, "_running", False):
                return []
            return [
                r for r in monitor.get_running_tasks()
                if r.get("task_id", "").startswith(f"{market}:")
            ]
        except Exception as e:
            logger.debug(f"获取运行中同步任务失败: {e}")
            return []

    async def get_sync_status(
        self, market: str, domain: Optional[str] = None,
        trigger: Optional[str] = None,
    ) -> List[Dict]:

        return await self._metadata_repo.get_all_checkpoints(market, domain, trigger)

    async def get_sync_events(
        self, market: str, domain: Optional[str] = None, limit: int = 50
    ) -> List[Dict]:
        return await self._metadata_repo.get_events(market, domain, limit)

    async def get_source_health(self, market: str) -> List[Dict]:
        mongo_health = await self._metadata_repo.get_all_health(market)

        if mongo_health:
            return mongo_health

        from app.data.monitoring.source_health import SourceHealthMonitor

        monitor = SourceHealthMonitor()
        return monitor.get_all_health(market)

    def get_capability_registry(self) -> CapabilityRegistry:
        return self._registry

    async def get_domain_health(self, market: str) -> Dict:

        from app.data.core.health import DomainHealthCalculator, HEALTH_SNAPSHOT_MAX_AGE_HOURS

        calculator = DomainHealthCalculator()
        domains = self._registry.get_domains(market)
        degraded_fields: List[str] = []

        domain_stats = await self.get_domain_stats(market, domains)

        checkpoints: List[Dict] = []
        try:
            checkpoints = await self._metadata_repo.get_all_checkpoints(market)
        except Exception as e:
            degraded_fields.append("sync_checkpoints")
            logger.warning(f"读取 {market} sync_checkpoints 失败: {e}")

        health_items: List[Dict] = []
        try:
            health_items = await self.get_source_health(market)
        except Exception as e:
            degraded_fields.append("source_health")
            logger.warning(f"读取 {market} source_health 失败: {e}")

        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        fresh_health: List[Dict] = []
        for item in health_items:
            age = DomainHealthCalculator._age_hours(item.get("updated_at"), now)
            if age is not None and age > HEALTH_SNAPSHOT_MAX_AGE_HOURS:
                continue
            fresh_health.append(item)

        sources_by_domain: Dict[str, List[Dict]] = {}
        for item in fresh_health:
            sources_by_domain.setdefault(item.get("domain", ""), []).append(item)

        latest_cp: Dict[str, Dict] = {}
        for cp in checkpoints:
            latest_cp.setdefault(cp.get("domain", ""), cp)

        basic_info_total: Optional[int] = None
        symbol_counts: Dict[str, int] = {}
        try:
            from app.data.storage.mongo.client import get_motor_db
            from app.data.storage.mongo.collections import get_collection_name

            db = get_motor_db()
            basic_coll = db[get_collection_name("basic_info", market)]
            basic_info_total = await basic_coll.count_documents({})
            for domain in domains:
                if calculator._is_coverage_exempt(domain):
                    continue
                coll = db[get_collection_name(domain, market)]
                pipeline = [{"$group": {"_id": "$symbol"}}, {"$count": "n"}]
                agg = await coll.aggregate(pipeline).to_list(length=1)
                symbol_counts[domain] = agg[0]["n"] if agg else 0
        except Exception as e:
            degraded_fields.append("coverage")
            logger.warning(f"计算 {market} 覆盖率失败: {e}")

        domain_health = []
        for domain in domains:
            stats = domain_stats.get(domain, {})
            cp = latest_cp.get(domain)
            coverage = None
            if basic_info_total and symbol_counts.get(domain) is not None:
                coverage = round(symbol_counts[domain] / basic_info_total, 4)
            domain_health.append(calculator.evaluate(
                market=market,
                domain=domain,
                record_count=stats.get("records", 0),
                last_sync_time=(cp or {}).get("last_sync_time") or stats.get("last_updated"),
                checkpoint_success=bool(cp and cp.get("status") == "success"),
                sources=sources_by_domain.get(domain),
                coverage=coverage,
                monitoring_available=bool(fresh_health) or bool(sources_by_domain),
            ))

        summary = DomainHealthCalculator.summarize(domain_health)
        summary["degraded_fields"] = degraded_fields
        return {"domains": domain_health, "summary": summary}

    async def get_config(self, market: str, domain: str) -> Optional[Dict]:
        return await self._metadata_repo.get_config(
            "data_source_priority", market, domain
        )

    async def update_config(
        self, market: str, domain: str, sources: List[str], updated_by: str = "user"
    ) -> bool:
        await self._metadata_repo.upsert_config(
            "data_source_priority",
            market,
            domain,
            {"sources": sources},
            updated_by,
        )
        self._priority.invalidate_cache(market, domain)
        logger.info(f"更新优先级: {market}/{domain} → {sources}")
        return True

    async def get_domain_stats(
        self, market: str, domains: List[str]
    ) -> Dict[str, Dict]:
        from app.data.storage.mongo.client import get_motor_db
        from app.data.storage.mongo.collections import get_collection_name

        db = get_motor_db()
        stats: Dict[str, Dict] = {}
        for domain in domains:
            try:
                coll = db[get_collection_name(domain, market)]
                count = await coll.count_documents({})
                last_doc = await coll.find_one(
                    {},
                    {"updated_at": 1},
                    sort=[("updated_at", -1)],
                )
                stats[domain] = {
                    "records": count,
                    "last_updated": last_doc.get("updated_at") if last_doc else None,
                }
            except Exception as e:
                logger.debug(f"获取域统计失败: {domain}: {e}")
                stats[domain] = {"records": 0, "last_updated": None}
        return stats

    async def get_quotes_stats(self, market: str) -> Dict[str, int]:

        from app.data.storage.mongo.client import get_motor_db
        from app.data.storage.mongo.collections import get_collection_name

        db = get_motor_db()
        coll = db[get_collection_name("daily_quotes", market)]
        total_records = await coll.count_documents({})
        pipeline = [{"$group": {"_id": "$symbol"}}, {"$count": "n"}]
        cursor = coll.aggregate(pipeline)
        agg = await cursor.to_list(length=1)
        total_symbols = agg[0]["n"] if agg else 0
        return {"total_records": total_records, "total_symbols": total_symbols}

    async def get_quality_overview(
        self, market: str, domains: List[str]
    ) -> Dict[str, Dict]:
        from app.data.storage.mongo.client import get_motor_db
        from app.data.storage.mongo.collections import get_collection_name

        db = get_motor_db()
        overview: Dict[str, Dict] = {}
        for domain in domains:
            try:
                coll = db[get_collection_name(domain, market)]
                total = await coll.count_documents({})
                missing_symbol = await coll.count_documents(
                    {"symbol": {"$exists": False}}
                )
                latest_doc = await coll.find_one(
                    {"trade_date": {"$exists": True}},
                    sort=[("trade_date", -1)],
                )
                latest_date = latest_doc.get("trade_date") if latest_doc else None
                overview[domain] = {
                    "total_records": total,
                    "missing_symbol": missing_symbol,
                    "completeness": round((total - missing_symbol) / total, 3)
                    if total > 0
                    else 0.0,
                    "empty": total == 0,
                    "latest_date": latest_date,
                }
            except Exception as e:
                overview[domain] = {"error": str(e)}
        return overview

    async def check_domain_quality(self, market: str, domain: str) -> Dict:
        from app.data.storage.mongo.client import get_motor_db
        from app.data.storage.mongo.collections import get_collection_name
        from datetime import datetime, timedelta, timezone

        _REQUIRED_FIELDS: Dict[str, List[str]] = {
            "daily_quotes": ["symbol", "trade_date", "close"],
            "daily_indicators": ["symbol", "trade_date"],
            "financial_data": ["symbol", "report_period"],
            "basic_info": ["symbol"],
        }
        _TIMESERIES_DOMAINS = ("daily_quotes", "daily_indicators", "adj_factors")

        db = get_motor_db()
        coll = db[get_collection_name(domain, market)]
        total = await coll.count_documents({})
        stats: Dict = {"total_records": total, "issues": []}

        if total == 0:
            stats["status"] = "empty"
            return stats

        required = _REQUIRED_FIELDS.get(domain, ["symbol"])
        for field in required:
            missing_count = await coll.count_documents(
                {
                    "$or": [{field: {"$exists": False}}, {field: None}, {field: ""}],
                }
            )
            if missing_count > 0:
                stats["issues"].append(
                    {
                        "type": "missing_field",
                        "field": field,
                        "count": missing_count,
                        "percentage": round(missing_count / total * 100, 2),
                    }
                )

        if domain in _TIMESERIES_DOMAINS:
            thirty_days_ago = (
                datetime.now(timezone.utc) - timedelta(days=30)
            ).strftime("%Y-%m-%d")
            try:
                pipeline = [
                    {"$match": {"trade_date": {"$gte": thirty_days_ago}}},
                    {"$group": {"_id": "$trade_date", "count": {"$sum": 1}}},
                    {"$sort": {"_id": 1}},
                ]
                cursor = coll.aggregate(pipeline)
                date_counts = await cursor.to_list(length=None)
                trading_days_covered = len(date_counts)
                try:
                    cal_coll = db[get_collection_name("trade_calendar", market)]
                    expected_days = await cal_coll.count_documents(
                        {
                            "is_open": 1,
                            "cal_date": {"$gte": thirty_days_ago},
                        }
                    )
                except Exception as e:
                    logger.debug(f"交易日历查询失败: {e}")
                    expected_days = None
                stats["date_continuity"] = {
                    "trading_days_covered": trading_days_covered,
                    "expected_trading_days": expected_days,
                    "coverage_rate": round(trading_days_covered / expected_days, 3)
                    if expected_days
                    else None,
                    "period": "last_30_days",
                }
            except Exception as e:
                stats["date_continuity"] = {"error": str(e)}

        if domain == "daily_quotes":
            try:
                bi_coll = db[get_collection_name("basic_info", market)]
                active_stocks = await bi_coll.count_documents({"list_status": "L"})
                if active_stocks > 0:
                    latest = await coll.find_one(sort=[("trade_date", -1)])
                    if latest:
                        latest_date = latest.get("trade_date", "")
                        covered = await coll.count_documents(
                            {"trade_date": latest_date}
                        )
                        stats["stock_coverage"] = {
                            "active_stocks": active_stocks,
                            "covered_stocks": covered,
                            "coverage_rate": round(covered / active_stocks, 3),
                            "latest_date": latest_date,
                        }
            except Exception as e:
                stats["stock_coverage"] = {"error": str(e)}

        stats["status"] = "ok" if not stats["issues"] else "warning"
        return stats

```
