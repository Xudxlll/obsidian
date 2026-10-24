from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import logging

from .config import load_config
from .core.base import BaseLLMClient
from .core.factory import create_client

logger = logging.getLogger("app.llm.providers")

_PROVIDER_PROTOCOL = {
    "anthropic": "anthropic",
    "claude": "anthropic",
    "ark": "anthropic",
    "volcengine": "anthropic",
}
DEFAULT_PROTOCOL = "openai"

@dataclass
class ResolvedProvider:
    protocol: str
    model: str
    api_key: str
    base_url: Optional[str]
    source: str
    provider: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    timeout: Optional[int] = None
    retry_times: Optional[int] = None
    context_window: Optional[int] = None
    thinking_budget: Optional[int] = None
    thinking_effort: Optional[str] = None
    max_concurrency: Optional[int] = None

@dataclass
class EngineClientBundle:

    primary: BaseLLMClient
    fallback: Optional[BaseLLMClient] = None
    retry_times: Optional[int] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    context_window: Optional[int] = None
    upper_limit: Optional[int] = None
    max_concurrency: Optional[int] = None
    _meta: Dict[str, Any] = field(default_factory=dict)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.primary, name)

    @classmethod
    def from_client(cls, client: BaseLLMClient) -> "EngineClientBundle":
        return cls(primary=client)

def infer_protocol(provider: str, protocol: Optional[str] = None) -> str:
    if protocol:
        p = protocol.strip().lower()
        if p in ("anthropic", "openai"):
            return p
        logger.warning(f"⚠️ [providers] 未知 protocol '{protocol}'，按厂家名推断")
    return _PROVIDER_PROTOCOL.get((provider or "").strip().lower(), DEFAULT_PROTOCOL)

def _pick_candidates(configs: List[Dict[str, Any]], role: str = "both") -> List[Dict[str, Any]]:
    candidates = [
        c
        for c in configs
        if c.get("enabled", True) and (c.get("suitable_roles") or ["both"])
        and (role in (c.get("suitable_roles") or ["both"]) or "both" in (c.get("suitable_roles") or []))
    ]
    return sorted(candidates, key=lambda c: c.get("priority", 0), reverse=True)

def resolve_provider(
    configs: List[Dict[str, Any]],
    role: str = "both",
    provider_defaults: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Optional[ResolvedProvider]:

    candidates = _pick_candidates(configs, role)
    if not candidates:
        return None
    cfg = candidates[0]
    defaults = (provider_defaults or {}).get((cfg.get("provider") or "").strip().lower()) or {}
    api_key = cfg.get("api_key") or defaults.get("api_key") or ""
    base_url = cfg.get("api_base") or cfg.get("custom_endpoint") or defaults.get("default_base_url") or None
    return ResolvedProvider(
        protocol=infer_protocol(cfg.get("provider", ""), defaults.get("protocol")),
        model=cfg["model_name"],
        api_key=api_key,
        base_url=base_url,
        source="db",
        provider=cfg.get("provider"),
        max_tokens=cfg.get("max_tokens"),
        temperature=cfg.get("temperature"),
        timeout=cfg.get("timeout"),
        retry_times=cfg.get("retry_times"),
        context_window=cfg.get("context_window"),
        thinking_budget=cfg.get("thinking_budget"),
        thinking_effort=cfg.get("thinking_effort"),
        max_concurrency=cfg.get("max_concurrency"),
    )

def _resolve_fallback(
    configs: List[Dict[str, Any]],
    role: str,
    primary_model: str,
    provider_defaults: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Optional[ResolvedProvider]:
    candidates = _pick_candidates(configs, role)
    for cfg in candidates[1:]:
        if cfg["model_name"] != primary_model:
            defaults = (provider_defaults or {}).get((cfg.get("provider") or "").strip().lower()) or {}
            return ResolvedProvider(
                protocol=infer_protocol(cfg.get("provider", ""), defaults.get("protocol")),
                model=cfg["model_name"],
                api_key=cfg.get("api_key") or defaults.get("api_key") or "",
                base_url=(
                    cfg.get("api_base") or cfg.get("custom_endpoint")
                    or defaults.get("default_base_url") or None
                ),
                source="db",
                provider=cfg.get("provider"),
                thinking_budget=cfg.get("thinking_budget"),
                thinking_effort=cfg.get("thinking_effort"),
            )
    return None

def resolve_from_env(protocol_hint: str = "anthropic") -> ResolvedProvider:
    env_cfg = load_config()
    return ResolvedProvider(
        protocol=protocol_hint,
        model=env_cfg.default_model,
        api_key=env_cfg.api_key,
        base_url=(
            env_cfg.anthropic_base_url if protocol_hint == "anthropic" else env_cfg.openai_base_url
        ),
        source="env",
    )

def build_client(resolved: ResolvedProvider) -> BaseLLMClient:

    return create_client(
        resolved.protocol,
        model=resolved.model,
        api_key=resolved.api_key,
        base_url=resolved.base_url,
        max_tokens=resolved.max_tokens,
        timeout=resolved.timeout,
        temperature=resolved.temperature,
        thinking_budget=resolved.thinking_budget,
        thinking_effort=resolved.thinking_effort,
        provider=resolved.provider,
    )

_CONFIG_FIELDS = (
    "provider", "model_name", "api_key", "api_base", "custom_endpoint",
    "enabled", "suitable_roles", "priority",
    "max_tokens", "temperature", "timeout", "retry_times", "context_window",
    "thinking_budget", "thinking_effort", "max_concurrency",
)

def _normalize_llm_configs(raw_configs: Any) -> List[Dict[str, Any]]:
    configs: List[Dict[str, Any]] = []
    for c in raw_configs or []:
        if not isinstance(c, dict) or not c.get("model_name"):
            continue
        item = {k: c.get(k) for k in _CONFIG_FIELDS}
        item["api_base"] = c.get("api_base") or c.get("custom_endpoint")
        item["enabled"] = c.get("enabled", True)
        item["suitable_roles"] = c.get("suitable_roles") or ["both"]
        item["priority"] = c.get("priority", 0)
        configs.append(item)
    return configs

def _normalize_provider_defaults(provider_docs: Any) -> Dict[str, Dict[str, Any]]:
    defaults: Dict[str, Dict[str, Any]] = {}
    for p in provider_docs or []:
        if not isinstance(p, dict) or not p.get("name"):
            continue
        defaults[str(p["name"]).strip().lower()] = {
            "api_key": p.get("api_key") or "",
            "default_base_url": p.get("default_base_url") or None,
            "protocol": p.get("protocol") or None,
        }
    return defaults

def _build_catalog_index(catalog_docs: Any) -> Dict[str, Dict[str, Optional[int]]]:
    index: Dict[str, Dict[str, Optional[int]]] = {}
    for doc in catalog_docs or []:
        if not isinstance(doc, dict):
            continue
        provider = (doc.get("provider") or "").strip().lower()
        for m in doc.get("models") or []:
            name = m.get("name")
            if not name:
                continue
            length = m.get("context_length")
            max_tokens = m.get("max_tokens")
            index[f"{provider}|{name}"] = {
                "context_length": length if isinstance(length, int) and length > 0 else None,
                "max_tokens": max_tokens if isinstance(max_tokens, int) and max_tokens > 0 else None,
            }
    return index

async def _load_catalog_index_async() -> Dict[str, Dict[str, Optional[int]]]:
    try:
        from app.core.database import get_mongo_db

        db = get_mongo_db()
        cursor = db.model_catalog.find(
            {},
            {"provider": 1, "models.name": 1, "models.max_tokens": 1, "models.context_length": 1},
        )
        docs = await cursor.to_list(200)
        return _build_catalog_index(docs)
    except Exception as e:
        logger.warning(f"[providers] 异步读取 model_catalog 失败: {e}")
        return {}

async def _load_provider_defaults_async() -> Dict[str, Dict[str, Any]]:
    try:
        from app.core.database import get_mongo_db

        db = get_mongo_db()
        docs = await db.llm_providers.find(
            {}, {"name": 1, "api_key": 1, "default_base_url": 1, "protocol": 1}
        ).to_list(200)
        return _normalize_provider_defaults(docs)
    except Exception as e:
        logger.warning(f"[providers] 异步读取厂家配置失败: {e}")
        return {}

def _load_all_sync() -> tuple:
    try:
        from app.core.database import get_mongo_db_sync

        db = get_mongo_db_sync()
        doc = db.system_configs.find_one({"is_active": True}, sort=[("version", -1)])
        configs = _normalize_llm_configs((doc or {}).get("llm_configs"))
        provider_docs = list(
            db.llm_providers.find(
                {}, {"name": 1, "api_key": 1, "default_base_url": 1, "protocol": 1}
            ).limit(200)
        )
        catalog_docs = list(db.model_catalog.find({}, {"provider": 1, "models": 1}).limit(200))
        return configs, _normalize_provider_defaults(provider_docs), _build_catalog_index(catalog_docs)
    except Exception as e:
        logger.warning(f"[providers] 同步读取数据库配置失败: {e}")
        return [], {}, {}

async def _resolve_role_bundle(
    role: str,
    configs: List[Dict[str, Any]],
    provider_defaults: Dict[str, Dict[str, Any]],
    catalog_index: Dict[str, Dict[str, Optional[int]]],
) -> EngineClientBundle:

    from .limits import resolve_output_limits, set_catalog_index

    if catalog_index:
        set_catalog_index(catalog_index)

    resolved = resolve_provider(configs, role, provider_defaults)
    if resolved is None:
        resolved = resolve_from_env()
        logger.info(f"[providers] role={role} 无数据库配置，使用 .env 回退 ({resolved.model})")

    provider = next(
        (c.get("provider", "") for c in configs if c.get("model_name") == resolved.model), ""
    ).strip().lower()
    limits_ = resolve_output_limits(
        resolved.model,
        provider or None,
        db_max_tokens=resolved.max_tokens,
        db_context_window=resolved.context_window,
    )
    bundle_max_tokens = resolved.max_tokens or limits_.max_tokens
    bundle_context_window = resolved.context_window or limits_.context_window
    logger.info(
        f"[providers] role={role} → {resolved.protocol}:{resolved.model} "
        f"(数据库配置, base_url={resolved.base_url or '默认'}, "
        f"max_tokens={bundle_max_tokens}, upper_limit={limits_.upper_limit}, "
        f"context_window={bundle_context_window or '未知'})"
    )

    fallback_resolved = _resolve_fallback(configs, role, resolved.model, provider_defaults)
    fallback_client = None
    if fallback_resolved is not None and fallback_resolved.api_key:
        try:
            fallback_client = build_client(fallback_resolved)
            logger.info(
                f"[providers] role={role} fallback → {fallback_resolved.protocol}:{fallback_resolved.model}"
            )
        except Exception as e:
            logger.warning(f"⚠️ [providers] role={role} fallback 客户端构建失败: {e}")

    return EngineClientBundle(
        primary=build_client(resolved),
        fallback=fallback_client,
        retry_times=resolved.retry_times,
        max_tokens=bundle_max_tokens,
        temperature=resolved.temperature,
        context_window=bundle_context_window,
        upper_limit=limits_.upper_limit,
        max_concurrency=resolved.max_concurrency,
        _meta={"limit_key": f"{provider}|{resolved.model}".strip('|').lower(), "model": resolved.model},
    )

async def resolve_task_override_bundle(
    model: str,
    *,
    provider: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Optional[EngineClientBundle]:

    configs: List[Dict[str, Any]] = []
    provider_defaults: Dict[str, Dict[str, Any]] = {}
    catalog_index: Dict[str, Dict[str, Optional[int]]] = {}
    try:
        from app.services.config import config_service

        system_config = await config_service.get_system_config()
        configs = _normalize_llm_configs(
            [c.model_dump() for c in (system_config.llm_configs or [])]
        )
        if configs:
            provider_defaults = await _load_provider_defaults_async()
            catalog_index = await _load_catalog_index_async()
    except Exception as e:
        logger.warning(f"[providers] 任务覆盖读取数据库配置失败: {e}")
    if not configs:
        configs, provider_defaults, catalog_index = _load_all_sync()

    inherit = next((c for c in configs if c.get("model_name") == model), None) or {}
    prov = provider or inherit.get("provider") or "openai"
    defaults = provider_defaults.get(prov.strip().lower()) or {}

    from .limits import resolve_output_limits, set_catalog_index

    if catalog_index:
        set_catalog_index(catalog_index)
    limits_ = resolve_output_limits(
        model,
        prov,
        db_max_tokens=inherit.get("max_tokens"),
        db_context_window=inherit.get("context_window"),
    )
    db_max = inherit.get("max_tokens")
    db_window = inherit.get("context_window")

    resolved = ResolvedProvider(
        protocol=infer_protocol(prov, defaults.get("protocol")),
        model=model,
        api_key=api_key or inherit.get("api_key") or defaults.get("api_key") or "",
        base_url=base_url or inherit.get("api_base") or defaults.get("default_base_url") or None,
        source="engine-config",
        provider=prov,
        max_tokens=db_max or limits_.max_tokens,
        temperature=inherit.get("temperature"),
        timeout=inherit.get("timeout"),
        retry_times=inherit.get("retry_times"),
        context_window=db_window or limits_.context_window,
        thinking_budget=inherit.get("thinking_budget"),
        thinking_effort=inherit.get("thinking_effort"),
        max_concurrency=inherit.get("max_concurrency"),
    )
    if not resolved.api_key:
        return None
    bundle = EngineClientBundle(
        primary=build_client(resolved),
        fallback=None,
        retry_times=resolved.retry_times,
        max_tokens=resolved.max_tokens,
        temperature=resolved.temperature,
        context_window=resolved.context_window,
        upper_limit=limits_.upper_limit,
        max_concurrency=resolved.max_concurrency,
        _meta={"limit_key": f"{prov}|{model}".strip('|').lower(), "model": model},
    )
    logger.info(
        f"[providers] 任务覆盖 → {resolved.protocol}:{model} "
        f"(max_tokens={resolved.max_tokens}, upper_limit={limits_.upper_limit}, "
        f"context_window={resolved.context_window or '未知'})"
    )
    return bundle

async def get_engine_clients() -> Dict[str, EngineClientBundle]:

    configs: List[Dict[str, Any]] = []
    provider_defaults: Dict[str, Dict[str, Any]] = {}
    catalog_index: Dict[str, Dict[str, Optional[int]]] = {}
    try:
        from app.services.config import config_service

        system_config = await config_service.get_system_config()
        configs = _normalize_llm_configs(
            [c.model_dump() for c in (system_config.llm_configs or [])]
        )
    except Exception as e:
        logger.info(f"[providers] 数据库配置不可用: {e}")
    if configs:
        provider_defaults = await _load_provider_defaults_async()
        catalog_index = await _load_catalog_index_async()
    else:
        configs, provider_defaults, catalog_index = _load_all_sync()
        if configs:
            logger.info("[providers] motor 不可用，已通过 pymongo 同步读取数据库配置")

    bundles: Dict[str, EngineClientBundle] = {}
    for role in ("analyst", "debate"):
        bundles[role] = await _resolve_role_bundle(role, configs, provider_defaults, catalog_index)
    return bundles
