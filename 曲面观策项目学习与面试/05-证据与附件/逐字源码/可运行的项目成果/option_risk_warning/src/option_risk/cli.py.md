---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/cli.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/cli.py>)

SHA-256：`cfb0c0774c94611050b5bbb9335b87ca945ca30369130fe0959db4de83b27899`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import os
from pathlib import Path
import subprocess
import sys
from collections.abc import Sequence

from .agent import OptionRiskAgent
from .config import AgentConfig, PipelineConfig
from .pipeline import run_pipeline
from .validation import validate_deployment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="期权波动率曲面单Agent风控预警系统")
    subparsers = parser.add_subparsers(dest="command", required=True)

    catalog = subparsers.add_parser("catalog", help="列出数据源中的真实品种及覆盖范围")
    _add_agent_source_arguments(catalog)

    analyze = subparsers.add_parser("analyze", help="由唯一Agent分析精确的品种和时间点")
    _add_agent_source_arguments(analyze)
    analyze.add_argument("--product", required=True)
    analyze.add_argument("--timestamp", required=True)

    run = subparsers.add_parser("run", help="Run cleaning, surface, features, labels and warning")
    run.add_argument("--data-dir", type=Path, required=True)
    run.add_argument("--output-dir", type=Path, required=True)
    run.add_argument("--product", default="ag")
    run.add_argument("--start-date")
    run.add_argument("--end-date")

    serve = subparsers.add_parser("serve", help="启动Streamlit单Agent控制台")
    _add_agent_source_arguments(serve)
    serve.add_argument("--port", type=int, default=8501)

    validate = subparsers.add_parser("validate", help="验收品种目录或完整Agent响应")
    _add_agent_source_arguments(validate)
    validate.add_argument(
        "--catalog-only",
        action="store_true",
        help="只校验每个品种的可选时间目录，不执行完整曲面分析",
    )
    validate.add_argument("--products", nargs="*", help="可选：只验收指定品种")
    validate.add_argument("--report", type=Path, help="机器可读JSON验收报告路径")
    return parser


def _add_agent_source_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--data-dir", type=Path)
    parser.add_argument("--archive-path", type=Path)
    parser.add_argument("--cache-dir", type=Path, default=Path("data/agent_cache"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))


def _agent_config(args: argparse.Namespace, parser: argparse.ArgumentParser) -> AgentConfig:
    if args.data_dir is None and args.archive_path is None:
        parser.error("catalog/analyze/serve/validate 至少需要 --data-dir 或 --archive-path")
    data_source = args.data_dir or (args.cache_dir / "archive_source")
    return AgentConfig(
        data_source=data_source,
        cache_dir=args.cache_dir,
        output_dir=args.output_dir,
        archive_path=args.archive_path,
    )


def _product_payload(agent: OptionRiskAgent) -> dict[str, object]:
    products = []
    for product in agent.list_products():
        row = asdict(product)
        row["start"] = product.start.isoformat() if product.start is not None else None
        row["end"] = product.end.isoformat() if product.end is not None else None
        products.append(row)
    return {"product_count": len(products), "products": products}


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "run":
        config = PipelineConfig.from_paths(args.product, args.start_date, args.end_date)
        summary = run_pipeline(args.data_dir, args.output_dir, config)
        print(json.dumps(summary, ensure_ascii=False, indent=2, default=str))
        return 0
    agent_config = _agent_config(args, parser)
    if args.command == "catalog":
        agent = OptionRiskAgent(agent_config)
        print(json.dumps(_product_payload(agent), ensure_ascii=False, indent=2))
        return 0
    if args.command == "analyze":
        agent = OptionRiskAgent(agent_config)
        result = agent.analyze(args.product, args.timestamp)
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        return 0
    if args.command == "validate":
        agent = OptionRiskAgent(agent_config)
        payload = validate_deployment(
            agent,
            analyze=not args.catalog_only,
            product_codes=args.products or None,
            progress=lambda message: print(message, file=sys.stderr, flush=True),
        )
        assert agent_config.output_dir is not None
        report_path = args.report or (agent_config.output_dir / "agent_acceptance.json")
        report_path = Path(report_path).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if payload.get("summary", {}).get("status") == "passed" else 1
    if args.command == "serve":
        dashboard_path = Path(__file__).with_name("dashboard.py")
        environment = os.environ.copy()
        environment["OPTION_RISK_DATA_SOURCE"] = str(agent_config.data_source)
        environment["OPTION_RISK_CACHE_DIR"] = str(agent_config.cache_dir)
        assert agent_config.output_dir is not None
        environment["OPTION_RISK_OUTPUT_DIR"] = str(agent_config.output_dir)
        environment["OPTION_RISK_ARCHIVE_PATH"] = (
            str(agent_config.archive_path) if agent_config.archive_path is not None else ""
        )
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(dashboard_path),
                "--server.port",
                str(args.port),
            ],
            check=False,
            env=environment,
        )
        return int(completed.returncode)
    parser.error(f"未知命令：{args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
````

</details>
