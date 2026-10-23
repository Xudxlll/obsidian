---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/scripts/query_knowledge_graph.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/query_knowledge_graph.py>)

SHA-256：`dfe521ba03a2901f12c773bb46aa33c859c771735c44b88a54f8ee7cd7c07429`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import argparse
from collections.abc import Sequence
import json
from pathlib import Path
import re
import sys

from option_risk.agent import OptionRiskAgent
from option_risk.config import AgentConfig
from option_risk.errors import OptionRiskAgentError
from option_risk.graph_queries import GraphQueryService
from option_risk.knowledge_graph import KnowledgeGraphError


QUERY_NAMES = (
    "root-evidence",
    "alert-paths",
    "consequences",
    "quality-limitations",
    "node-detail",
)
NODE_ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*(?::[A-Za-z0-9_.:-]+)+$")


def _force_utf8_streams() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", newline="\n")
        except (AttributeError, OSError):
            pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="查询单Agent生成的期权风险知识图谱",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--data-dir", type=Path)
    source.add_argument("--archive-path", type=Path)
    parser.add_argument("--cache-dir", type=Path, default=Path("data/agent_cache"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--product", required=True)
    parser.add_argument("--timestamp", required=True)
    parser.add_argument("--query", choices=QUERY_NAMES, required=True)
    parser.add_argument("--node-id")
    return parser


def _validate_query_arguments(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> None:
    if args.query == "node-detail":
        if args.node_id is None:
            parser.error("node-detail requires --node-id")
        if not NODE_ID_PATTERN.fullmatch(args.node_id):
            parser.error("--node-id must be an exact registered graph node ID")
    elif args.node_id is not None:
        parser.error("--node-id is only valid with node-detail")


def _agent_config(args: argparse.Namespace) -> AgentConfig:
    data_source = args.data_dir or (args.cache_dir / "archive_source")
    return AgentConfig(
        data_source=data_source,
        cache_dir=args.cache_dir,
        output_dir=args.output_dir,
        archive_path=args.archive_path,
    )


def _query_records(
    service: GraphQueryService,
    query: str,
    node_id: str | None,
) -> list[dict]:
    if query == "root-evidence":
        return service.root_evidence(limit=3)
    if query == "alert-paths":
        return service.paths_to_alert()
    if query == "consequences":
        return service.possible_consequences()
    if query == "quality-limitations":
        return service.quality_limitations()
    assert query == "node-detail" and node_id is not None
    return [service.inspect_node(node_id)]


def main(argv: Sequence[str] | None = None) -> int:
    _force_utf8_streams()
    parser = build_parser()
    args = parser.parse_args(argv)
    _validate_query_arguments(parser, args)
    try:
        agent = OptionRiskAgent(_agent_config(args))
        result = agent.analyze(args.product, args.timestamp)
        graph_result = result.knowledge_graph
        if graph_result is None:
            raise KnowledgeGraphError("Knowledge graph is unavailable: missing result")
        if graph_result.status != "ready":
            detail = f": {graph_result.error_message}" if graph_result.error_message else ""
            raise KnowledgeGraphError(
                f"Knowledge graph status is {graph_result.status}{detail}"
            )
        service = GraphQueryService(graph_result)
        records = _query_records(service, args.query, args.node_id)
        if not isinstance(records, list):
            raise TypeError("Query records must be a list")
        payload = {
            "product": result.product,
            "timestamp": result.timestamp.isoformat(),
            "schema_version": graph_result.schema_version,
            "rule_version": graph_result.rule_version,
            "query": args.query,
            "record_count": len(records),
            "records": records,
        }
        serialized = json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            allow_nan=False,
        )
    except (
        OptionRiskAgentError,
        KnowledgeGraphError,
        AssertionError,
        TypeError,
        ValueError,
    ) as error:
        print(f"Error: {error}", file=sys.stderr, flush=True)
        return 1
    print(serialized, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
````

</details>
