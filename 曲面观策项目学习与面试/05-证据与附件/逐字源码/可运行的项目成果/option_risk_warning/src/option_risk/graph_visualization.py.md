---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/graph_visualization.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_visualization.py>)

SHA-256：`d9f229fa0805b397699813da1bc6426f4508bbb5b2ab1cd8e08406a798ad3028`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from collections.abc import Iterable

import plotly.graph_objects as go

from .contracts import KnowledgeGraphResult, RiskPath
from .graph_queries import GraphQueryService
from .knowledge_graph import graph_from_node_link
from .knowledge_schema import NodeType


_LAYER_X = {
    NodeType.EVIDENCE.value: 0,
    NodeType.ANOMALY.value: 1,
    NodeType.MECHANISM.value: 2,
    NodeType.RISK_CONSEQUENCE.value: 3,
    NodeType.WARNING_STATE.value: 3,
    NodeType.CONFIDENCE_STATE.value: 3,
}
_NODE_COLORS = {
    NodeType.EVIDENCE.value: "#4C78A8",
    NodeType.ANOMALY.value: "#E45756",
    NodeType.MECHANISM.value: "#72B7B2",
    NodeType.RISK_CONSEQUENCE.value: "#F2CF5B",
    NodeType.WARNING_STATE.value: "#B279A2",
    NodeType.CONFIDENCE_STATE.value: "#9D755D",
}


def _strict_path_cap(max_paths: int) -> int:
    if type(max_paths) is not int:
        raise TypeError("max_paths must be a strict integer in the range 1..3")
    if max_paths not in {1, 2, 3}:
        raise ValueError("max_paths must be in the range 1..3")
    return max_paths


def _path_node_ids(path: RiskPath) -> tuple[str, str, str, str]:
    return (
        path.evidence_node_id,
        path.anomaly_node_id,
        path.mechanism_node_id,
        path.conclusion_node_id,
    )


def _node_hover(record: dict[str, object]) -> str:
    rows = [
        f"<b>{record['label']}</b>",
        f"类型：{record['node_type']}",
        f"品种：{record['product']}",
        f"时间：{record['source_timestamp']}",
    ]
    if record["node_type"] == NodeType.EVIDENCE.value:
        rows.extend(
            (
                f"当前值：{record.get('current_value')}",
                f"动态阈值：{record.get('reference_value')}",
                f"压力：{record.get('pressure_ratio')}",
                f"方向：{record.get('direction')}",
                f"数据源：{record.get('source')}",
                f"规则ID：{record.get('rule_id')}",
            )
        )
    elif record.get("rule_id") is not None:
        rows.append(f"规则ID：{record['rule_id']}")
    return "<br>".join(rows)


def _display_label(value: object) -> str:
    """Keep the four fixed columns legible on a phone without changing hover data."""
    label = str(value)
    return "<br>".join(label[index : index + 7] for index in range(0, len(label), 7))


def _path_edges(paths: Iterable[RiskPath]) -> list[str]:
    edge_ids: list[str] = []
    for path in paths:
        for edge_id in path.edge_ids:
            if edge_id not in edge_ids:
                edge_ids.append(edge_id)
    return edge_ids


def knowledge_graph_figure(
    result: KnowledgeGraphResult, max_paths: int = 3
) -> go.Figure:
    """Render canonical active paths in stable Evidence→Conclusion columns."""
    max_paths = _strict_path_cap(max_paths)
    GraphQueryService(result)
    paths = tuple(result.active_paths[:max_paths])
    figure = go.Figure()
    if not paths:
        figure.update_layout(
            annotations=[
                {
                    "text": "没有活跃异常/接近阈值证据路径。",
                    "showarrow": False,
                    "x": 0.5,
                    "y": 0.5,
                    "xref": "paper",
                    "yref": "paper",
                }
            ],
            meta={"path_ids": [], "node_ids": [], "edge_ids": []},
            margin={"l": 20, "r": 20, "t": 30, "b": 20},
            height=320,
        )
        return figure

    graph = graph_from_node_link(result.graph_json)
    node_tracks: dict[str, list[int]] = {}
    node_ids: list[str] = []
    for track, path in enumerate(paths):
        for node_id in _path_node_ids(path):
            if node_id not in node_tracks:
                node_tracks[node_id] = []
                node_ids.append(node_id)
            node_tracks[node_id].append(-track)
    node_positions = {
        node_id: (_LAYER_X[graph.nodes[node_id]["node_type"]], sum(tracks) / len(tracks))
        for node_id, tracks in node_tracks.items()
    }
    edge_ids = _path_edges(paths)
    edge_records: dict[str, tuple[str, str, dict[str, object]]] = {}
    for source, target, edge_id, data in graph.edges(keys=True, data=True):
        if edge_id in edge_ids:
            edge_records[str(edge_id)] = (str(source), str(target), dict(data))

    figure.add_trace(
        go.Scatter(
            name="图谱节点",
            mode="markers+text",
            x=[node_positions[node_id][0] for node_id in node_ids],
            y=[node_positions[node_id][1] for node_id in node_ids],
            text=[_display_label(graph.nodes[node_id]["label"]) for node_id in node_ids],
            textposition="top center",
            customdata=[
                [node_id, graph.nodes[node_id]["node_type"]] for node_id in node_ids
            ],
            hovertext=[_node_hover(dict(graph.nodes[node_id])) for node_id in node_ids],
            hovertemplate="%{hovertext}<extra></extra>",
            marker={
                "size": 18,
                "color": [
                    _NODE_COLORS[graph.nodes[node_id]["node_type"]]
                    for node_id in node_ids
                ],
                "line": {"color": "#FFFFFF", "width": 1},
            },
            textfont={"size": 10, "color": "#374151"},
        )
    )
    quality_paths = [
        path
        for path in paths
        if graph.nodes[path.conclusion_node_id]["node_type"]
        == NodeType.CONFIDENCE_STATE.value
    ]
    annotations = []
    for edge_id in edge_ids:
        source, target, record = edge_records[edge_id]
        source_x, source_y = node_positions[source]
        target_x, target_y = node_positions[target]
        label = str(record["relation_type"])
        annotations.append(
            {
                "x": target_x,
                "y": target_y,
                "ax": source_x,
                "ay": source_y,
                "xref": "x",
                "yref": "y",
                "axref": "x",
                "ayref": "y",
                "text": label,
                "showarrow": True,
                "arrowhead": 2,
                "arrowsize": 1,
                "arrowwidth": 1.4,
                "arrowcolor": "#6B7280",
                "font": {"size": 8, "color": "#374151"},
            }
        )
    if quality_paths:
        confidence_x, confidence_y = node_positions[
            quality_paths[0].conclusion_node_id
        ]
        annotations.append(
            {
                "x": confidence_x,
                "y": confidence_y - 0.28,
                "xref": "x",
                "yref": "y",
                "text": "置信度路径",
                "showarrow": False,
                "font": {"size": 10, "color": "#9D755D"},
            }
        )
    figure.update_layout(
        clickmode="event+select",
        showlegend=False,
        hovermode="closest",
        annotations=annotations,
        meta={
            "path_ids": [path.path_id for path in paths],
            "node_ids": node_ids,
            "edge_ids": edge_ids,
        },
        margin={"l": 30, "r": 30, "t": 35, "b": 30},
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis={
            "range": [-0.35, 3.35],
            "tickvals": [0, 1, 2, 3],
            "ticktext": ["Evidence", "Anomaly", "Mechanism", "Conclusion"],
            "fixedrange": True,
            "showgrid": True,
            "gridcolor": "#E5E7EB",
            "zeroline": False,
        },
        yaxis={"visible": False, "fixedrange": True},
    )
    return figure


__all__ = ["knowledge_graph_figure"]
````

</details>
