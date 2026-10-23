---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py>)

SHA-256：`e54cdc1655bdefe2931ac2d537f8b07c98e61bd0fc30aa65e2286ff6c1353ac1`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from copy import deepcopy

import pandas as pd

from .contracts import ExplanationSection, KnowledgeGraphResult, RiskPath
from .graph_reasoner import _build_query_index, discover_risk_paths
from .knowledge_graph import (
    KnowledgeGraphError,
    KnowledgeGraphValidationError,
    graph_from_node_link,
    graph_to_node_link,
)
from .knowledge_schema import KG_RULE_VERSION, KG_SCHEMA_VERSION, NodeType


class UnknownGraphNodeError(KnowledgeGraphError):
    """Raised when an exact graph node lookup cannot satisfy the preset query."""


def _unique(values):
    return tuple(dict.fromkeys(values))


def _same_exact_json_structure(actual, expected):
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return set(actual) == set(expected) and all(
            _same_exact_json_structure(actual[key], value)
            for key, value in expected.items()
        )
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(
            _same_exact_json_structure(left, right)
            for left, right in zip(actual, expected, strict=True)
        )
    return actual == expected


class GraphQueryService:
    """Read-only preset queries over a fully revalidated graph result."""

    def __init__(self, result: KnowledgeGraphResult) -> None:
        if not isinstance(result, KnowledgeGraphResult):
            raise KnowledgeGraphValidationError(
                "GraphQueryService requires a KnowledgeGraphResult"
            )
        if result.status != "ready":
            raise KnowledgeGraphValidationError(
                "GraphQueryService requires a ready KnowledgeGraphResult"
            )
        graph = graph_from_node_link(result.graph_json)
        if (
            result.schema_version != KG_SCHEMA_VERSION
            or result.schema_version != graph.graph["schema_version"]
        ):
            raise KnowledgeGraphValidationError("KnowledgeGraphResult schema version mismatch")
        if (
            result.rule_version != KG_RULE_VERSION
            or result.rule_version != graph.graph["rule_version"]
        ):
            raise KnowledgeGraphValidationError("KnowledgeGraphResult rule version mismatch")
        if result.product != graph.graph["product"]:
            raise KnowledgeGraphValidationError("KnowledgeGraphResult product mismatch")
        if (
            not isinstance(result.timestamp, pd.Timestamp)
            or result.timestamp != graph.graph["timestamp"]
        ):
            raise KnowledgeGraphValidationError("KnowledgeGraphResult timestamp mismatch")
        if type(result.node_count) is not int or result.node_count != graph.number_of_nodes():
            raise KnowledgeGraphValidationError("KnowledgeGraphResult node count mismatch")
        if type(result.edge_count) is not int or result.edge_count != graph.number_of_edges():
            raise KnowledgeGraphValidationError("KnowledgeGraphResult edge count mismatch")

        canonical_paths = tuple(discover_risk_paths(graph))
        if any(not isinstance(path, RiskPath) for path in result.active_paths):
            raise KnowledgeGraphValidationError(
                "KnowledgeGraphResult active_paths contains a malformed record"
            )
        supplied_ids = [path.path_id for path in result.active_paths]
        if len(supplied_ids) != len(set(supplied_ids)):
            raise KnowledgeGraphValidationError("KnowledgeGraphResult has duplicate path IDs")
        if type(result.active_path_count) is not int or result.active_path_count != len(
            canonical_paths
        ):
            raise KnowledgeGraphValidationError("KnowledgeGraphResult path count mismatch")
        if tuple(result.active_paths) != canonical_paths:
            raise KnowledgeGraphValidationError(
                "KnowledgeGraphResult paths are not the canonical discovered paths"
            )

        expected_roots = _unique(path.evidence_node_id for path in canonical_paths)
        expected_consequences = _unique(
            path.conclusion_node_id
            for path in canonical_paths
            if graph.nodes[path.conclusion_node_id]["node_type"]
            == NodeType.RISK_CONSEQUENCE.value
        )
        if tuple(result.root_evidence) != expected_roots:
            raise KnowledgeGraphValidationError("KnowledgeGraphResult root index mismatch")
        if tuple(result.possible_consequences) != expected_consequences:
            raise KnowledgeGraphValidationError(
                "KnowledgeGraphResult consequence index mismatch"
            )
        canonical_ids = {path.path_id for path in canonical_paths}
        if any(
            not isinstance(section, ExplanationSection)
            for section in result.explanation_sections
        ):
            raise KnowledgeGraphValidationError(
                "KnowledgeGraphResult explanation_sections contains a malformed record"
            )
        if any(
            path_id not in canonical_ids
            for section in result.explanation_sections
            for path_id in section.path_ids
        ):
            raise KnowledgeGraphValidationError(
                "KnowledgeGraphResult explanation references an unknown path"
            )
        expected_query_index = _build_query_index(graph, canonical_paths)
        if not _same_exact_json_structure(result.query_index, expected_query_index):
            raise KnowledgeGraphValidationError(
                "KnowledgeGraphResult query index is not canonical"
            )

        payload = graph_to_node_link(graph)
        node_records = {}
        for row in payload["nodes"]:
            record = dict(row)
            record.pop("id", None)
            node_records[record["node_id"]] = record
        self._graph = graph
        self._paths = canonical_paths
        self._root_ids = expected_roots
        self._consequence_ids = expected_consequences
        self._node_records = node_records

    def _node_copy(self, node_id):
        return deepcopy(self._node_records[node_id])

    def _path_copies(self, paths):
        return deepcopy([path.to_dict() for path in paths])

    def root_evidence(self, limit=3):
        if type(limit) is not int:
            raise TypeError("limit must be a strict integer")
        if limit < 0:
            raise ValueError("limit must be non-negative")
        return [self._node_copy(node_id) for node_id in self._root_ids[:limit]]

    def paths_to_alert(self):
        return self._path_copies(
            path
            for path in self._paths
            if self._graph.nodes[path.conclusion_node_id]["node_type"]
            == NodeType.WARNING_STATE.value
        )

    def possible_consequences(self):
        return [self._node_copy(node_id) for node_id in self._consequence_ids]

    def quality_limitations(self):
        return self._path_copies(
            path
            for path in self._paths
            if self._graph.nodes[path.conclusion_node_id]["node_type"]
            == NodeType.CONFIDENCE_STATE.value
        )

    def inspect_node(self, node_id):
        if not isinstance(node_id, str) or node_id not in self._node_records:
            raise UnknownGraphNodeError(f"Unknown exact graph node ID: {node_id!r}")
        return self._node_copy(node_id)

    def paths_from_anomaly(self, anomaly_id):
        if (
            not isinstance(anomaly_id, str)
            or anomaly_id not in self._node_records
            or self._graph.nodes[anomaly_id]["node_type"] != NodeType.ANOMALY.value
        ):
            raise UnknownGraphNodeError(
                f"Unknown exact Anomaly node ID: {anomaly_id!r}"
            )
        return self._path_copies(
            path for path in self._paths if path.anomaly_node_id == anomaly_id
        )


__all__ = ["GraphQueryService", "UnknownGraphNodeError"]
````

</details>
