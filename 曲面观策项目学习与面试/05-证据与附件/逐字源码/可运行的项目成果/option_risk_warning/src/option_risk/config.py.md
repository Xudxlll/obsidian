---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/config.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/config.py>)

SHA-256：`3ca4d3870a1438bd2ecd9b859bd83c1bb424f511f0a4e8cd47008330d9ef8da4`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(slots=True)
class PipelineConfig:
    """All assumptions that materially affect the risk warning pipeline."""

    product: str = "ag"
    start_date: str | None = None
    end_date: str | None = None
    timezone: str = "Asia/Shanghai"

    min_dte: int = 2
    max_dte: int = 180
    min_moneyness: float = 0.70
    max_moneyness: float = 1.30
    atm_log_band: float = 0.03
    wing_log_min: float = 0.05
    wing_log_max: float = 0.15
    iv_min: float = 0.0005
    iv_max: float = 5.0
    iv_solver_floor: float = 0.0010002979543060064
    iv_floor_tolerance: float = 1e-8
    risk_free_rate: float = 0.02

    min_quotes_per_snapshot: int = 20
    min_expiries_per_snapshot: int = 2
    expected_quotes_per_expiry: int = 12

    bars_per_trading_day: int = 32
    historical_days: int = 20
    min_history_bars: int = 96
    short_change_bars: int = 4
    lead_bars: int = 2
    horizon_bars: int = 8
    event_cooldown_bars: int = 8
    deterioration_quantile: float = 0.95

    validation_months: int = 1
    test_months: int = 3
    random_state: int = 42
    alert_policy_min_signals: int = 2
    alert_policy_persistence_bars: int = 2

    @property
    def historical_window_bars(self) -> int:
        return self.bars_per_trading_day * self.historical_days

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    @classmethod
    def from_paths(
        cls,
        product: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> "PipelineConfig":
        return cls(product=product.lower(), start_date=start_date, end_date=end_date)


@dataclass(slots=True)
class PipelinePaths:
    data_dir: Path
    output_dir: Path

    def ensure(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "figures").mkdir(parents=True, exist_ok=True)


@dataclass(slots=True)
class AgentConfig:
    """Runtime configuration supplied by deployment, not by dashboard users."""

    data_source: Path | None = None
    cache_dir: Path = Path("data/agent_cache")
    output_dir: Path | None = None
    archive_path: Path | None = None
    lookback_calendar_days: int = 45
    config_version: str = "agent-v1"

    def __post_init__(self) -> None:
        self.cache_dir = Path(self.cache_dir).resolve()
        if self.data_source is None:
            self.data_source = (self.cache_dir / "archive_source").resolve()
        else:
            self.data_source = Path(self.data_source).resolve()
        if self.output_dir is None:
            self.output_dir = (self.cache_dir / "outputs").resolve()
        else:
            self.output_dir = Path(self.output_dir).resolve()
        if self.archive_path is not None:
            self.archive_path = Path(self.archive_path).resolve()

    def ensure_directories(self) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        assert self.output_dir is not None
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def pipeline_config(
        self,
        product: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> PipelineConfig:
        return PipelineConfig.from_paths(product, start_date, end_date)
````

</details>
