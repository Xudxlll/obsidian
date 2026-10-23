---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/visualization.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/visualization.py>)

SHA-256：`1234f1d89e772393f8340e7e1d21657d11f6bd9239f6d942d063132eada4373f`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .decision import DecisionPolicy
from .surfaces import SURFACE_METRICS, SurfaceGrid, surface_grid


LEVEL_COLORS = {0: "#94A3B8", 1: "#D4A72C", 2: "#E67E22", 3: "#C2413B"}
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def _formal_timeline_pressure(alerts: pd.DataFrame) -> tuple[pd.Series, str]:
    """Return the causal pressure that drives the formal canonical policy."""

    if "core_risk_pressure" not in alerts:
        raise ValueError("Formal alert timeline requires core_risk_pressure")
    pressure = pd.to_numeric(alerts["core_risk_pressure"], errors="coerce").astype(float)
    return pressure, "核心动态风险压力"


def plot_surface_3d(grid: SurfaceGrid, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    x_mesh, y_mesh = np.meshgrid(grid.log_moneyness, grid.dte)
    values = np.ma.masked_invalid(grid.values)
    figure = plt.figure(figsize=(10, 7), constrained_layout=True)
    axis = figure.add_subplot(111, projection="3d")
    axis.plot_surface(x_mesh, y_mesh, values, cmap="viridis", linewidth=0.2, antialiased=True)
    axis.set_xlabel("对数价内外程度 ln(K/F)")
    axis.set_ylabel("剩余到期天数")
    axis.set_zlabel(grid.metric.upper())
    axis.set_title(f"{grid.metric.upper()} 曲面 | {grid.timestamp:%Y-%m-%d %H:%M}")
    axis.view_init(elev=28, azim=-125)
    figure.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(figure)
    return output_path


def plot_greeks_heatmaps(
    nodes: pd.DataFrame, timestamp: pd.Timestamp, output_path: str | Path
) -> Path:
    output_path = Path(output_path)
    figure, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    for axis, metric in zip(axes.flat, ["delta", "gamma", "vega", "theta"], strict=True):
        grid = surface_grid(nodes, metric, timestamp=timestamp)
        image = axis.imshow(
            grid.values,
            aspect="auto",
            origin="lower",
            extent=[grid.log_moneyness.min(), grid.log_moneyness.max(), grid.dte.min(), grid.dte.max()],
            cmap="coolwarm" if metric in {"delta", "theta"} else "viridis",
        )
        axis.set_title(metric.upper())
        axis.set_xlabel("对数价内外程度 ln(K/F)")
        axis.set_ylabel("剩余到期天数")
        figure.colorbar(image, ax=axis, shrink=0.82)
    figure.suptitle(f"希腊字母曲面 | {timestamp:%Y-%m-%d %H:%M}", fontsize=14)
    figure.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(figure)
    return output_path


def plot_alert_timeline(alerts: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    view = alerts.loc[alerts["split"].eq("test")].copy()
    if view.empty:
        view = alerts.tail(1000).copy()
    figure, axes = plt.subplots(2, 1, figsize=(14, 7), sharex=True, constrained_layout=True)
    axes[0].plot(view.index, view["atm_iv"], color="#2457A6", linewidth=1.3, label="ATM IV")
    for level in [1, 2, 3]:
        points = view.loc[view["alert_level"].eq(level)]
        axes[0].scatter(
            points.index,
            points["atm_iv"],
            s={1: 8, 2: 28, 3: 42}[level],
            color=LEVEL_COLORS[level],
            label=f"等级 {level}",
            alpha={1: 0.35, 2: 0.90, 3: 0.95}[level],
        )
    axes[0].set_ylabel("ATM隐含波动率")
    axes[0].set_title("ATM隐含波动率与预警等级 | 连续三个月测试期")
    axes[0].legend(ncol=4, loc="upper left")
    axes[0].grid(alpha=0.18)

    pressure, pressure_label = _formal_timeline_pressure(view)
    policy = DecisionPolicy()
    axes[1].plot(
        view.index,
        pressure,
        color="#6B4C9A",
        linewidth=1.2,
        label=pressure_label,
    )
    axes[1].axhline(
        policy.warning_pressure,
        color=LEVEL_COLORS[2],
        linestyle="--",
        linewidth=1.0,
        label=f"2级状态阈值 {policy.warning_pressure:.2f}",
    )
    axes[1].axhline(
        policy.danger_core_pressure,
        color=LEVEL_COLORS[3],
        linestyle=":",
        linewidth=1.0,
        label=f"3级核心阈值 {policy.danger_core_pressure:.2f}（另需多信号）",
    )
    axes[1].set_ylabel("核心压力 / 滚动95%阈值")
    axes[1].set_xlabel("市场时间")
    finite_pressure = pressure[np.isfinite(pressure)]
    upper = (
        max(policy.danger_core_pressure * 1.08, float(finite_pressure.max()) * 1.05)
        if len(finite_pressure)
        else policy.danger_core_pressure * 1.08
    )
    axes[1].set_ylim(0.0, upper)
    axes[1].legend(ncol=3, loc="upper left")
    axes[1].grid(alpha=0.18)
    figure.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(figure)
    return output_path


def save_snapshot_grids(
    nodes: pd.DataFrame, timestamp: pd.Timestamp, output_path: str | Path
) -> Path:
    output_path = Path(output_path)
    payload: dict[str, np.ndarray | str] = {"timestamp": str(timestamp)}
    for metric in SURFACE_METRICS:
        grid = surface_grid(nodes, metric, timestamp=timestamp)
        payload[f"{metric}_values"] = grid.values
        payload[f"{metric}_x"] = grid.log_moneyness
        payload[f"{metric}_dte"] = grid.dte
    np.savez_compressed(output_path, **payload)
    return output_path
````

</details>
