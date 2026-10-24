import logging
import math
import os
import re
import threading
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from app.data.schema.base.enums import FreshnessState

logger = logging.getLogger(__name__)

def _strip_nan(value: Any) -> Any:

    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return value
    if isinstance(value, dict):
        return {k: _strip_nan(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_strip_nan(v) for v in value]
    if isinstance(value, tuple):
        return tuple(_strip_nan(v) for v in value)
    return value

class Reader:

    def __init__(self):
        self._repo_cache: Dict[str, Any] = {}
        self._refresh_queue = None
        self._repo_lock = threading.Lock()
        self._freshness_rules_cache: Optional[Dict] = None
        self._freshness_rules_mtime: float = 0.0
        self._freshness_rules_lock = threading.Lock()

    def _get_repo(self, domain: str):
        if domain in self._repo_cache:
            return self._repo_cache[domain]

        with self._repo_lock:
            if domain in self._repo_cache:
                return self._repo_cache[domain]

            from app.data.storage.mongo.repositories import (
                BasicInfoRepo, DailyQuotesRepo, DailyIndicatorsRepo,
                AdjFactorsRepo, CorporateActionsRepo, FinancialDataRepo,
                MarketQuotesRepo, NewsRepo, TradeCalendarRepo,
                IntradayQuotesRepo, MoneyFlowRepo, MarginTradingRepo,
                DragonTigerRepo, BlockTradeRepo,
                ConnectStatusRepo, SouthboundHoldingRepo, PrePostMarketRepo,
            )

            repo_map = {
                "basic_info": BasicInfoRepo,
                "trade_calendar": TradeCalendarRepo,
                "daily_quotes": DailyQuotesRepo,
                "daily_indicators": DailyIndicatorsRepo,
                "adj_factors": AdjFactorsRepo,
                "corporate_actions": CorporateActionsRepo,
                "financial_data": FinancialDataRepo,
                "market_quotes": MarketQuotesRepo,
                "news": NewsRepo,
                "intraday_quotes": IntradayQuotesRepo,
                "money_flow": MoneyFlowRepo,
                "margin_trading": MarginTradingRepo,
                "dragon_tiger": DragonTigerRepo,
                "block_trade": BlockTradeRepo,
                "connect_status": ConnectStatusRepo,
                "southbound_holding": SouthboundHoldingRepo,
                "pre_post_market": PrePostMarketRepo,
            }

            repo_cls = repo_map.get(domain)
            if repo_cls:
                repo = repo_cls()
                self._repo_cache[domain] = repo
                return repo
            return None

    async def get_data(
        self, market: str, domain: str, symbol: Optional[str] = None,
        start_date: Optional[str] = None, end_date: Optional[str] = None,
        filters: Optional[Dict] = None,
    ) -> Tuple[Optional[Any], str]:

        repo = self._get_repo(domain)
        if not repo:
            return None, FreshnessState.UNKNOWN

        filters = filters or {}
        data = None

        if domain == "basic_info":
            if symbol:
                data = await repo.get_by_symbol(symbol, market)
            else:
                limit = filters.get("limit", 0)
                data = await repo.get_all(market, limit=limit)

        elif domain == "trade_calendar":
            exchange = filters.get("exchange",
                                   "SSE" if market == "CN" else "HKEX" if market == "HK" else "NYSE")
            data = await repo.get_range(exchange, market,
                                        start_date or "1970-01-01", end_date or "2099-12-31")

        elif domain in ("daily_quotes", "daily_indicators", "adj_factors", "corporate_actions"):
            if symbol:
                period_filter = filters.get("period") if filters else None
                extra_kwargs = {}
                if period_filter and domain == "daily_quotes":
                    extra_kwargs["period"] = period_filter
                data = await repo.get_by_symbol_and_range(
                    symbol, market,
                    start_date or "1970-01-01", end_date or "2099-12-31",
                    **extra_kwargs,
                )

        elif domain == "financial_data":
            if symbol:
                statement_type = filters.get("statement_type")
                data = await repo.get_by_symbol(symbol, market, statement_type=statement_type)

        elif domain == "market_quotes":
            if symbol:
                data = await repo.get_by_symbol(symbol, market)
            else:
                limit = filters.get("limit", 100)
                data = await repo.get_all(market, limit=limit)

        elif domain == "news":
            if symbol:
                limit = filters.get("limit", 20)
                data = await repo.get_by_symbol(symbol, market, limit=limit)
            else:
                limit = filters.get("limit", 100)
                data = await repo.get_all(market, limit=limit)

        elif domain == "intraday_quotes":
            if symbol:
                freq = filters.get("freq")
                data = await repo.get_by_symbol_and_range(
                    symbol, market,
                    start_date or "1970-01-01 00:00:00",
                    end_date or "2099-12-31 23:59:59",
                    freq=freq,
                )

        elif domain == "money_flow":
            if symbol:
                data = await repo.get_by_symbol_and_range(
                    symbol, market,
                    start_date or "1970-01-01", end_date or "2099-12-31",
                )

        elif domain == "margin_trading":
            if symbol:
                data = await repo.get_by_symbol_and_range(
                    symbol, market,
                    start_date or "1970-01-01", end_date or "2099-12-31",
                )

        elif domain == "dragon_tiger":
            if symbol:
                limit = filters.get("limit", 50)
                data = await repo.get_by_symbol(symbol, market, limit=limit)
            elif start_date:
                limit = filters.get("limit", 100)
                data = await repo.get_by_date(start_date, market, limit=limit)

        elif domain == "block_trade":
            if symbol:
                limit = filters.get("limit", 50)
                data = await repo.get_by_symbol(symbol, market, limit=limit)
            else:
                limit = filters.get("limit", 100)
                data = await repo.get_by_date_range(
                    market,
                    start_date or "1970-01-01", end_date or "2099-12-31",
                    limit=limit,
                )

        elif domain == "connect_status":
            limit = filters.get("limit", 100)
            data = await repo.get_by_date_range(
                market,
                start_date or "1970-01-01", end_date or "2099-12-31",
                limit=limit,
            )

        elif domain == "southbound_holding":
            if symbol:
                data = await repo.get_by_symbol_and_range(
                    symbol, market,
                    start_date or "1970-01-01", end_date or "2099-12-31",
                )

        elif domain == "pre_post_market":
            if symbol:
                session_type = filters.get("session_type")
                data = await repo.get_by_symbol_and_range(
                    symbol, market,
                    start_date or "1970-01-01", end_date or "2099-12-31",
                    session_type=session_type,
                )
            else:
                limit = filters.get("limit", 100)
                data = await repo.get_by_symbol("", market, limit=limit)

        if not data:
            return None, FreshnessState.UNKNOWN

        freshness = await self.check_freshness(market, symbol or "", domain, data)

        if freshness == FreshnessState.STALE and symbol:
            await self.notify_refresh_async(market, symbol, domain)

        return _strip_nan(data), freshness

    _LATEST_SORT_FIELDS: Dict[str, str] = {
        "trade_calendar": "cal_date",
        "daily_quotes": "trade_date",
        "daily_indicators": "trade_date",
        "adj_factors": "trade_date",
        "corporate_actions": "trade_date",
        "intraday_quotes": "trade_date",
        "money_flow": "trade_date",
        "margin_trading": "trade_date",
        "dragon_tiger": "trade_date",
        "block_trade": "trade_date",
        "southbound_holding": "trade_date",
        "pre_post_market": "trade_date",
        "financial_data": "report_period",
        "news": "updated_at",
        "basic_info": "updated_at",
        "market_quotes": "updated_at",
        "connect_status": "updated_at",
    }

    MAX_BATCH_SYMBOLS = 500

    @classmethod
    def _latest_sort_field(cls, domain: str) -> str:
        return cls._LATEST_SORT_FIELDS.get(domain, "updated_at")

    @staticmethod
    def _normalize_projection(projection: Optional[Dict]) -> Dict:
        if projection is None:
            return {"_id": 0}
        proj = dict(projection)
        if "_id" not in proj:
            proj["_id"] = 0
        return proj

    def _get_coll(self, market: str, domain: str):
        from app.data.storage.mongo.client import get_motor_db
        from app.data.storage.mongo.collections import get_collection_name

        db = get_motor_db()
        return db[get_collection_name(domain, market)]

    async def read_latest(
        self, market: str, domain: str, symbol: str,
        projection: Optional[Dict] = None,
    ) -> Optional[Dict]:

        sort_field = self._latest_sort_field(domain)
        sort_spec = [(sort_field, -1), ("updated_at", -1)]
        coll = self._get_coll(market, domain)
        doc = await coll.find_one(
            {"symbol": symbol},
            self._normalize_projection(projection),
            sort=sort_spec,
        )
        return _strip_nan(doc) if doc else None

    async def read_latest_batch(
        self, market: str, domain: str, symbols: List[str],
        projection: Optional[Dict] = None,
    ) -> Dict[str, Dict]:

        symbols = list(symbols or [])
        if len(symbols) > self.MAX_BATCH_SYMBOLS:
            raise ValueError(
                f"symbols 数量 {len(symbols)} 超过上限 {self.MAX_BATCH_SYMBOLS}，请分批调用"
            )
        if not symbols:
            return {}

        sort_field = self._latest_sort_field(domain)
        pipeline: List[Dict] = [
            {"$match": {"symbol": {"$in": symbols}}},
            {"$sort": {sort_field: -1, "updated_at": -1}},
            {"$group": {"_id": "$symbol", "doc": {"$first": "$$ROOT"}}},
            {"$replaceRoot": {"newRoot": "$doc"}},
        ]
        proj = self._normalize_projection(projection)
        if proj != {"_id": 0}:
            pipeline.append({"$project": proj})

        coll = self._get_coll(market, domain)
        result: Dict[str, Dict] = {}
        async for doc in coll.aggregate(pipeline):
            s = doc.get("symbol")
            if s:
                result[s] = _strip_nan(doc)
        return result

    async def read_batch(
        self, market: str, domain: str, symbols: List[str],
        projection: Optional[Dict] = None,
        sort: Optional[List[Tuple[str, int]]] = None,
        limit: int = 0,
    ) -> List[Dict]:
        symbols = list(symbols or [])
        if not symbols:
            return []

        coll = self._get_coll(market, domain)
        cursor = coll.find(
            {"symbol": {"$in": symbols}},
            self._normalize_projection(projection),
        )
        if sort:
            cursor = cursor.sort(sort)
        if limit and limit > 0:
            cursor = cursor.limit(limit)
        docs = await cursor.to_list(length=None)
        return _strip_nan(docs)

    async def search_basic_info(
        self, market: str, query: str,
        fields: Optional[List[str]] = None,
        limit: int = 20,
    ) -> List[Dict]:

        fields = fields or ["symbol", "name"]
        safe = re.escape(query)
        conditions = []
        for f in fields:
            pattern = f"^{safe}" if f == "symbol" else f".*{safe}.*"
            conditions.append({f: {"$regex": pattern, "$options": "i"}})

        coll = self._get_coll(market, "basic_info")
        cursor = coll.find({"$or": conditions}, {"_id": 0}).limit(limit)
        docs = await cursor.to_list(length=limit)
        return _strip_nan(docs)

    def _load_freshness_rules(self) -> Dict:

        from app.data.config import load_yaml

        yaml_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "freshness_rules.yaml"
        )
        try:
            mtime = os.path.getmtime(yaml_path)
        except OSError:
            mtime = 0

        with self._freshness_rules_lock:
            if (
                self._freshness_rules_cache is not None
                and mtime == self._freshness_rules_mtime
            ):
                return self._freshness_rules_cache
            rules = load_yaml("freshness_rules.yaml")
            self._freshness_rules_cache = rules
            self._freshness_rules_mtime = mtime
            return rules

    async def check_freshness(
        self, market: str, symbol: str, domain: str, data: Any = None
    ) -> str:
        rules = self._load_freshness_rules()
        market_rules = rules.get(market, {})
        domain_rule = market_rules.get(domain)

        if not domain_rule:
            return FreshnessState.UNKNOWN

        updated_at = None
        if isinstance(data, dict):
            updated_at = data.get("updated_at")
        elif isinstance(data, list) and data:
            candidates = [
                d.get("updated_at")
                for d in data
                if isinstance(d, dict) and d.get("updated_at")
            ]
            if candidates:
                updated_at = max(candidates)

        if not updated_at:
            return FreshnessState.UNKNOWN

        try:
            if isinstance(updated_at, datetime):
                updated = updated_at
            elif isinstance(updated_at, str):
                iso_str = updated_at.replace("Z", "+00:00") if updated_at.endswith("Z") else updated_at
                updated = datetime.fromisoformat(iso_str)
            else:
                return FreshnessState.UNKNOWN

            if updated.tzinfo is None:
                updated = updated.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)

            rule_type = domain_rule.get("rule_type", "time_window")

            if rule_type == "time_window":
                threshold_hours = domain_rule.get("threshold_hours")
                threshold_minutes = domain_rule.get("threshold_minutes")
                if threshold_hours:
                    threshold_sec = threshold_hours * 3600
                elif threshold_minutes:
                    threshold_sec = threshold_minutes * 60
                else:
                    return FreshnessState.UNKNOWN

                age_seconds = (now - updated).total_seconds()
                return FreshnessState.FRESH if age_seconds < threshold_sec else FreshnessState.STALE

            elif rule_type == "trading_day_after_close":
                threshold_minutes = domain_rule.get("threshold_minutes", 60)
                age_minutes = (now - updated).total_seconds() / 60
                return FreshnessState.FRESH if age_minutes < threshold_minutes else FreshnessState.STALE

        except (ValueError, TypeError, AttributeError):
            return FreshnessState.UNKNOWN

        return FreshnessState.UNKNOWN

    async def notify_refresh_async(self, market: str, symbol: str, domain: str) -> None:
        try:
            if self._refresh_queue is None:
                from app.data.storage.redis.pubsub import RefreshQueue
                self._refresh_queue = RefreshQueue()
            await self._refresh_queue.publish_refresh(market, symbol, domain)
        except Exception as e:
            logger.debug(f"异步刷新通知失败: {e}")
