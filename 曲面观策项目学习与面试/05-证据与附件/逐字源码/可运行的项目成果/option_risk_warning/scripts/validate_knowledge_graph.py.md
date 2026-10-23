---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/scripts/validate_knowledge_graph.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/validate_knowledge_graph.py>)

SHA-256：`71c9dde27a6c8528eed6b1974ae5adcb10ed0005f42f39dacf20e129f7c654b6`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import argparse
from collections.abc import Sequence
import json
from pathlib import Path
import sys

from option_risk.agent import OptionRiskAgent
from option_risk.config import AgentConfig
from option_risk.errors import OptionRiskAgentError
from option_risk.knowledge_graph import KnowledgeGraphError
from option_risk.validation import validate_knowledge_graph_deployment


MANDATORY_GLOBAL_CHECK_NAMES = frozenset(
    {"deterministic", "no_future", "content_safety"}
)


def _force_utf8_streams() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", newline="\n")
        except (AttributeError, OSError):
            pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="执行问题二知识图谱正式验收",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--data-dir", type=Path)
    source.add_argument("--archive-path", type=Path)
    parser.add_argument("--cache-dir", type=Path, default=Path("data/agent_cache"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--products", nargs="*")
    parser.add_argument("--report", type=Path)
    return parser


def _agent_config(args: argparse.Namespace) -> AgentConfig:
    data_source = args.data_dir or (args.cache_dir / "archive_source")
    return AgentConfig(
        data_source=data_source,
        cache_dir=args.cache_dir,
        output_dir=args.output_dir,
        archive_path=args.archive_path,
    )


def _write_report_atomically(report_path: Path, serialized: str) -> None:
    report_path = report_path.resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = report_path.with_name(f".{report_path.name}.tmp")
    try:
        temporary.write_bytes(serialized.encode("utf-8"))
        temporary.replace(report_path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _global_checks_allow_success(payload: dict) -> bool:
    checks = payload.get("global_checks")
    # Preserve compatibility with the original Problem 1/report-only callers.
    if checks is None or checks == {}:
        return True
    if type(checks) is not dict:
        return False
    return (
        MANDATORY_GLOBAL_CHECK_NAMES.issubset(checks)
        and all(
            type(check) is dict and check.get("passed") is True
            for check in checks.values()
        )
    )


def main(argv: Sequence[str] | None = None) -> int:
    _force_utf8_streams()
    parser = build_parser()
    args = parser.parse_args(argv)
    report_path = args.report or (args.output_dir / "knowledge_graph_acceptance_full.json")
    try:
        agent = OptionRiskAgent(_agent_config(args))
        payload = validate_knowledge_graph_deployment(
            agent,
            product_codes=args.products or None,
            progress=lambda message: print(message, file=sys.stderr, flush=True),
        )
        serialized = json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            allow_nan=False,
        )
        _write_report_atomically(report_path, serialized)
    except (
        OptionRiskAgentError,
        KnowledgeGraphError,
        AssertionError,
        TypeError,
        ValueError,
        OSError,
    ) as error:
        print(f"Error: {error}", file=sys.stderr, flush=True)
        return 1
    print(serialized, flush=True)
    summary_passed = payload.get("summary", {}).get("status") == "passed"
    return 0 if summary_passed and _global_checks_allow_success(payload) else 1


if __name__ == "__main__":
    raise SystemExit(main())
````

</details>
