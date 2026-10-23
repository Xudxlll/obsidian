---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/interactive.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/interactive.py>)

SHA-256：`1334483e3a504db6ba75bee29c803d6cb53b240b08b8145b055483bd8fd2c7f3`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from collections.abc import Mapping

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .contracts import SurfacePayload


LEVEL_COLORS = {0: "#2E7D32", 1: "#D4A017", 2: "#E87500", 3: "#C62828"}
LEVEL_SYMBOLS = {0: "circle-open", 1: "diamond-open", 2: "triangle-up", 3: "x"}
METRIC_LABELS = {
    "iv": "隐含波动率 IV",
    "delta": "Delta",
    "gamma": "Gamma",
    "vega": "Vega",
    "theta": "Theta",
}


def _title(label: str, surface: SurfacePayload, product: str) -> str:
    return (
        f"{label}<br><sup>{product} | {surface.timestamp:%Y-%m-%d %H:%M} | "
        "横轴 ln(K/F)，纵轴 T=dte/365</sup>"
    )


def _layout(figure: go.Figure, title: str, height: int = 520) -> go.Figure:
    figure.update_layout(
        title=title,
        template="plotly_white",
        height=height,
        margin=dict(l=55, r=35, t=90, b=55),
        font=dict(family="Microsoft YaHei, Arial, sans-serif", color="#202733"),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FAFBFC",
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0),
    )
    return figure


def iv_surface_figure(surface: SurfacePayload, product: str) -> go.Figure:
    x_mesh, y_mesh = np.meshgrid(surface.log_moneyness, surface.time_to_expiry)
    figure = go.Figure(
        data=[
            go.Surface(
                x=x_mesh,
                y=y_mesh,
                z=surface.values,
                colorscale="Viridis",
                connectgaps=False,
                colorbar=dict(title="IV"),
                hovertemplate="ln(K/F)=%{x:.3f}<br>T=%{y:.4f}年<br>IV=%{z:.4f}<extra></extra>",
            )
        ]
    )
    figure.update_layout(
        scene=dict(
            xaxis_title="对数价内外程度 ln(K/F)",
            yaxis_title="到期时间 T（年）",
            zaxis_title="隐含波动率 IV",
            bgcolor="#FFFFFF",
        )
    )
    return _layout(figure, _title("IV三维曲面", surface, product), height=610)


def surface_heatmap_figure(surface: SurfacePayload, product: str) -> go.Figure:
    figure = go.Figure(
        go.Heatmap(
            x=surface.log_moneyness,
            y=surface.time_to_expiry,
            z=surface.values,
            colorscale="Viridis",
            connectgaps=False,
            colorbar=dict(title=METRIC_LABELS.get(surface.metric, surface.metric.upper())),
            hovertemplate="ln(K/F)=%{x:.3f}<br>T=%{y:.4f}年<br>值=%{z:.5f}<extra></extra>",
        )
    )
    figure.update_xaxes(title_text="对数价内外程度 ln(K/F)")
    figure.update_yaxes(title_text="到期时间 T（年）")
    label = METRIC_LABELS.get(surface.metric, surface.metric.upper())
    return _layout(figure, _title(f"{label}热力图", surface, product), height=480)


def greeks_figure(surfaces: Mapping[str, SurfacePayload], product: str) -> go.Figure:
    metrics = ["delta", "gamma", "vega", "theta"]
    figure = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=[METRIC_LABELS[metric] for metric in metrics],
        horizontal_spacing=0.12,
        vertical_spacing=0.14,
    )
    for position, metric in enumerate(metrics):
        surface = surfaces[metric]
        row, column = divmod(position, 2)
        diverging = metric in {"delta", "theta"}
        figure.add_trace(
            go.Heatmap(
                x=surface.log_moneyness,
                y=surface.time_to_expiry,
                z=surface.values,
                colorscale="RdBu" if diverging else "Viridis",
                zmid=0 if diverging else None,
                showscale=True,
                colorbar=dict(len=0.38, y=0.78 if row == 0 else 0.22, x=0.43 if column == 0 else 1.0),
                hovertemplate=(
                    f"{METRIC_LABELS[metric]}<br>ln(K/F)=%{{x:.3f}}<br>"
                    "T=%{y:.4f}年<br>值=%{z:.6f}<extra></extra>"
                ),
            ),
            row=row + 1,
            col=column + 1,
        )
        figure.update_xaxes(title_text="ln(K/F)", row=row + 1, col=column + 1)
        figure.update_yaxes(title_text="T（年）", row=row + 1, col=column + 1)
    timestamp = surfaces["delta"].timestamp
    return _layout(
        figure,
        f"Greeks曲面热力图<br><sup>{product} | {timestamp:%Y-%m-%d %H:%M} | 与IV使用同一网格</sup>",
        height=720,
    )


def term_curves_figure(surface: SurfacePayload, product: str) -> go.Figure:
    figure = go.Figure()
    dash_styles = ["solid", "dash", "dot", "dashdot"]
    symbols = ["circle", "diamond", "square", "triangle-up"]
    for index, maturity in enumerate(surface.time_to_expiry):
        values = surface.values[index]
        supported = np.isfinite(values)
        if not supported.any():
            continue
        days = int(round(float(maturity) * 365))
        figure.add_trace(
            go.Scatter(
                x=surface.log_moneyness[supported],
                y=values[supported],
                mode="lines+markers",
                name=f"{days}天（T={maturity:.3f}）",
                line=dict(width=2, dash=dash_styles[index % len(dash_styles)]),
                marker=dict(size=5, symbol=symbols[index % len(symbols)]),
                hovertemplate="ln(K/F)=%{x:.3f}<br>IV=%{y:.4f}<extra>%{fullData.name}</extra>",
            )
        )
    figure.update_xaxes(title_text="对数价内外程度 ln(K/F)", zeroline=True, zerolinecolor="#586271")
    figure.update_yaxes(title_text="隐含波动率 IV")
    return _layout(figure, _title("不同期限IV曲线", surface, product), height=480)


def timeline_figure(
    timeline: pd.DataFrame,
    selected_timestamp: pd.Timestamp | str,
    product: str,
) -> go.Figure:
    selected_timestamp = pd.Timestamp(selected_timestamp)
    view = timeline.loc[timeline.index <= selected_timestamp].copy()
    figure = go.Figure()
    if not view.empty:
        figure.add_trace(
            go.Scatter(
                x=view.index,
                y=view["core_risk_pressure"],
                mode="lines",
                name="核心动态风险压力",
                line=dict(color="#2457A6", width=2),
                hovertemplate="%{x|%Y-%m-%d %H:%M}<br>核心压力=%{y:.3f}<extra></extra>",
            )
        )
        figure.add_trace(
            go.Scatter(
                x=view.index,
                y=view["dynamic_boundary"],
                mode="lines",
                name="2级状态阈值 0.98",
                line=dict(color=LEVEL_COLORS[2], width=1.5, dash="dash"),
                hovertemplate="2级状态阈值=%{y:.2f}<extra></extra>",
            )
        )
        figure.add_trace(
            go.Scatter(
                x=view.index,
                y=view["danger_core_boundary"],
                mode="lines",
                name="3级核心阈值 1.50（另需多信号）",
                line=dict(color=LEVEL_COLORS[3], width=1.5, dash="dot"),
                hovertemplate="3级核心阈值=%{y:.2f}，另需多信号<extra></extra>",
            )
        )
        for level in [0, 1, 2, 3]:
            points = view.loc[view["alert_level"].eq(level)]
            if points.empty:
                continue
            figure.add_trace(
                go.Scatter(
                    x=points.index,
                    y=points["core_risk_pressure"],
                    mode="markers",
                    name=f"等级{level}",
                    marker=dict(
                        color=LEVEL_COLORS[level],
                        symbol=LEVEL_SYMBOLS[level],
                        size=7 if level < 2 else 10,
                        line=dict(color="#202733", width=0.6),
                    ),
                    hovertemplate=(
                        f"等级{level}<br>%{{x|%Y-%m-%d %H:%M}}<br>"
                        "核心压力=%{y:.3f}<extra></extra>"
                    ),
                )
            )
    figure.update_xaxes(title_text="市场时间")
    figure.update_yaxes(title_text="核心压力 / 滚动95%阈值", rangemode="tozero")
    return _layout(
        figure,
        f"预警时间轴<br><sup>{product} | 截止 {selected_timestamp:%Y-%m-%d %H:%M} | 不显示未来数据</sup>",
        height=500,
    )
````

</details>
