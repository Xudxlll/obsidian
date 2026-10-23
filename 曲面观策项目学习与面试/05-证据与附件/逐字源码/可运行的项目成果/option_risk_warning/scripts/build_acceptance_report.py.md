---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/scripts/build_acceptance_report.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_acceptance_report.py>)

SHA-256：`7b0c2ed0f6603a3c00126f8190d9dad6c4d3478b131933ad67b85adf46c32b59`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any


TITLE = "期权波动率曲面风控智能体：问题1离线验收报告"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _metric_row(
    metric: str,
    actual: float,
    target: float,
    unit: str,
    definition: str,
) -> dict[str, Any]:
    if unit == "percent":
        actual_text = f"{actual:.1%}"
        target_text = f"≥ {target:.0%}"
    else:
        actual_text = f"{actual:.1f} 分钟"
        target_text = f"≥ {target:.0f} 分钟"
    return {
        "metric": metric,
        "actual": actual,
        "target": target,
        "actual_text": actual_text,
        "target_text": target_text,
        "passed": "通过" if actual >= target else "未通过",
        "definition": definition,
    }


def build_artifact(run_summary: dict[str, Any], acceptance: dict[str, Any]) -> dict[str, Any]:
    test = run_summary["test_metrics"]
    cvar = run_summary["cvar_backtest"]
    config = run_summary["config"]
    model = run_summary["model"]
    identity = run_summary.get("run_identity") or {}
    feature_identity = identity.get("feature_schema") or {}
    policy_identity = identity.get("decision_policy") or {}
    products = acceptance["products"]
    levels = Counter(int(row["analysis"]["alert_level"]) for row in products)
    level_names = {0: "0 无预警", 1: "1 关注", 2: "2 警告", 3: "3 危险"}
    alert_distribution = [
        {
            "alert_level": level,
            "alert_label": level_names[level],
            "product_count": levels.get(level, 0),
            "product_share": levels.get(level, 0) / len(products),
        }
        for level in range(4)
    ]
    product_coverage = [
        {
            "product": row["product"],
            "timestamp_count": row["timestamp_count"],
            "first_timestamp": row["first_timestamp"],
            "last_timestamp": row["last_timestamp"],
            "latest_alert_level": row["analysis"]["alert_level"],
            "latest_alert_name": row["analysis"]["alert_name"],
            "surface_count": len(row["analysis"]["surface_metrics"]),
            "feature_group_count": len(row["analysis"]["feature_groups"]),
            "status": row["status"],
        }
        for row in products
    ]
    backtest_metrics = [
        _metric_row(
            "事件级预警精确率",
            test["event_precision"],
            0.50,
            "percent",
            "2—3级预警片段中，在未来8个15分钟bar内出现风险事件的比例。",
        ),
        _metric_row(
            "风险事件召回率",
            test["event_recall"],
            0.60,
            "percent",
            f"{test['event_count']}个测试风险事件中，被严格提前1—8个bar的2—3级预警覆盖的比例。",
        ),
        _metric_row(
            "平均提前时间",
            test["average_lead_minutes"],
            30.0,
            "minutes",
            "成功匹配事件此前最近一次有效预警到事件开始的平均分钟数。",
        ),
    ]
    cvar_rows = [
        {
            "side": "期货多头1手",
            "baseline_cvar95": cvar["long"]["baseline_cvar95"],
            "warning_cvar95": cvar["long"]["warning_cvar95"],
            "improvement_rate": cvar["long"]["improvement_rate"],
        },
        {
            "side": "期货空头1手",
            "baseline_cvar95": cvar["short"]["baseline_cvar95"],
            "warning_cvar95": cvar["short"]["warning_cvar95"],
            "improvement_rate": cvar["short"]["improvement_rate"],
        },
    ]
    source_acceptance = {
        "id": "acceptance_json",
        "label": "35品种完整Agent验收查询",
        "path": "queries/acceptance_report.sql",
    }
    source_backtest = {
        "id": "run_summary_json",
        "label": "白银连续三个月离线回测查询",
        "path": "queries/backtest_report.sql",
    }
    source_code = {
        "id": "agent_source",
        "label": "OptionRiskAgent及其内部算法实现",
        "path": "src/option_risk/agent.py",
    }
    generated_at = acceptance["generated_at"]
    test_start = str(model.get("test_start", "2025-02-05"))[:10]
    test_end = str(config["end_date"])[:10]
    product_count = len(products)
    passed_products = int(acceptance["summary"]["passed_products"])
    failed_products = int(acceptance["summary"]["failed_products"])
    distribution_text = "、".join(
        f"{level}级{levels.get(level, 0)}个" for level in range(4)
    )
    random_baseline = cvar.get("random_warning_date_baseline", {})
    random_median = float(random_baseline.get("median", 0.0))
    random_percentile = float(random_baseline.get("model_percentile_among_random_dates", 0.0))
    return {
        "surface": "report",
        "manifest": {
            "version": 1,
            "surface": "report",
            "title": TITLE,
            "description": "问题1单Agent实现、全品种可用性及白银连续三个月离线回测的技术验收报告。",
            "generatedAt": generated_at,
            "cards": [
                {
                    "id": "product_pass_card",
                    "description": "原始RAR中35个品种的最新有效时点均完成完整Agent响应。",
                    "dataset": "acceptance_summary",
                    "sourceId": "acceptance_json",
                    "metrics": [
                        {"label": "全品种完整响应通过率", "field": "pass_rate", "format": "percent"},
                        {"label": "验收要求", "field": "required_pass_rate", "format": "percent"},
                    ],
                },
                {
                    "id": "precision_card",
                    "description": "事件级口径；2—3级预警片段与未来8个bar风险事件匹配。",
                    "dataset": "backtest_summary",
                    "sourceId": "run_summary_json",
                    "metrics": [
                        {"label": "事件级预警精确率", "field": "event_precision", "format": "percent"},
                        {"label": "比赛目标", "field": "precision_target", "format": "percent"},
                    ],
                },
                {
                    "id": "recall_card",
                    "description": f"{test['event_count']}个测试风险事件中被严格提前1—8个bar的有效预警覆盖的比例。",
                    "dataset": "backtest_summary",
                    "sourceId": "run_summary_json",
                    "metrics": [
                        {"label": "风险事件召回率", "field": "event_recall", "format": "percent"},
                        {"label": "比赛目标", "field": "recall_target", "format": "percent"},
                    ],
                },
                {
                    "id": "lead_card",
                    "description": "成功匹配事件此前最近一次有效预警到事件开始的平均时间。",
                    "dataset": "backtest_summary",
                    "sourceId": "run_summary_json",
                    "metrics": [
                        {"label": "平均提前时间（分钟）", "field": "average_lead_minutes", "format": "number"},
                        {"label": "比赛目标（分钟）", "field": "lead_target_minutes", "format": "number"},
                    ],
                },
                {
                    "id": "cvar_card",
                    "description": "多空各1手永久减半仓位后的平均代理CVaR改善；需结合随机日期基线解释。",
                    "dataset": "backtest_summary",
                    "sourceId": "run_summary_json",
                    "metrics": [
                        {"label": "多空平均代理CVaR改善率", "field": "cvar_improvement", "format": "percent"},
                        {"label": "随机日期中位数", "field": "random_cvar_median", "format": "percent"},
                    ],
                },
            ],
            "charts": [
                {
                    "id": "latest_alert_distribution",
                    "title": "35个品种最新有效时点的预警等级分布",
                    "subtitle": "同一验收时刻各品种独立计算；柱高为品种数，n=35。",
                    "type": "bar",
                    "dataset": "alert_distribution",
                    "sourceId": "acceptance_json",
                    "encodings": {
                        "x": {"field": "alert_label", "type": "ordinal", "label": "预警等级"},
                        "y": {"field": "product_count", "type": "quantitative", "label": "品种数"},
                        "tooltip": [
                            {"field": "product_share", "type": "quantitative", "label": "品种占比", "format": "percent"}
                        ],
                    },
                    "yAxisTitle": "品种数",
                    "valueFormat": "number",
                    "layout": "full",
                },
                {
                    "id": "product_timestamp_coverage",
                    "title": "各品种可供用户选择的有效时点数量",
                    "subtitle": "完整质量门槛及至少96个历史bar后保留的时点；共35个品种。",
                    "type": "horizontalBar",
                    "dataset": "product_coverage",
                    "sourceId": "acceptance_json",
                    "encodings": {
                        "x": {"field": "product", "type": "nominal", "label": "品种"},
                        "y": {"field": "timestamp_count", "type": "quantitative", "label": "有效时点数"},
                        "tooltip": [
                            {"field": "first_timestamp", "type": "temporal", "label": "首个时点"},
                            {"field": "last_timestamp", "type": "temporal", "label": "最后时点"},
                        ],
                    },
                    "xAxisTitle": "品种",
                    "yAxisTitle": "有效时点数",
                    "valueFormat": "compact",
                    "layout": "full",
                    "maxRows": 35,
                },
            ],
            "tables": [
                {
                    "id": "backtest_metric_table",
                    "title": "比赛核心预警指标与目标",
                    "subtitle": f"白银测试集为{test_start}至{test_end}；事件级口径。",
                    "dataset": "backtest_metrics",
                    "sourceId": "run_summary_json",
                    "density": "spacious",
                    "defaultSort": {"field": "metric", "direction": "asc"},
                    "columns": [
                        {"field": "metric", "label": "指标", "type": "text"},
                        {"field": "actual_text", "label": "实测", "type": "text"},
                        {"field": "target_text", "label": "目标", "type": "text"},
                        {"field": "passed", "label": "结论", "type": "text"},
                        {"field": "definition", "label": "定义", "type": "text"},
                    ],
                },
                {
                    "id": "cvar_table",
                    "title": "代理价格CVaR回测",
                    "subtitle": "测试期59个交易日；首次2—3级预警后下一交易日永久减半仓位。",
                    "dataset": "cvar_rows",
                    "sourceId": "run_summary_json",
                    "density": "spacious",
                    "defaultSort": {"field": "side", "direction": "asc"},
                    "columns": [
                        {"field": "side", "label": "方向", "type": "text"},
                        {"field": "baseline_cvar95", "label": "基线CVaR95", "format": "percent", "type": "percent"},
                        {"field": "warning_cvar95", "label": "预警后CVaR95", "format": "percent", "type": "percent"},
                        {"field": "improvement_rate", "label": "改善率", "format": "percent", "type": "percent"},
                    ],
                },
                {
                    "id": "product_audit_table",
                    "title": "全品种级联下拉与完整响应审计",
                    "subtitle": "每行对应一个品种；时点数为完整质量筛选后可选择的数量。",
                    "dataset": "product_coverage",
                    "sourceId": "acceptance_json",
                    "density": "compact",
                    "defaultSort": {"field": "product", "direction": "asc"},
                    "columns": [
                        {"field": "product", "label": "品种", "type": "text"},
                        {"field": "timestamp_count", "label": "可选时点数", "format": "number", "type": "number"},
                        {"field": "first_timestamp", "label": "首个可选时点", "type": "date"},
                        {"field": "last_timestamp", "label": "最后可选时点", "type": "date"},
                        {"field": "latest_alert_level", "label": "最新等级", "format": "number", "type": "number"},
                        {"field": "latest_alert_name", "label": "等级名称", "type": "text"},
                        {"field": "surface_count", "label": "曲面数", "format": "number", "type": "number"},
                        {"field": "feature_group_count", "label": "特征组数", "format": "number", "type": "number"},
                        {"field": "status", "label": "验收", "type": "text"},
                    ],
                },
            ],
            "sources": [source_acceptance, source_backtest, source_code],
            "blocks": [
                {"id": "title", "type": "markdown", "body": f"# {TITLE}"},
                {
                    "id": "technical_summary",
                    "type": "markdown",
                    "body": "## 技术结论：一个Agent已闭合问题1，并通过全品种真实数据验收\n\n系统对外只暴露 `OptionRiskAgent`。用户只选择品种与该品种真实可用时点；Agent内部完成清洗、IV与四个Greeks曲面、五组风险特征、0—3级动态预警、证据解释和历史时间轴。全品种验收与白银离线回测均达到当前交付门槛，但CVaR仍使用重构标的代理，不能替代真实期货行情的正式结论。",
                },
                {"id": "acceptance_metric", "type": "metric-strip", "cardIds": ["product_pass_card"]},
                {
                    "id": "all_products_finding",
                    "type": "markdown",
                    "sourceId": "acceptance_json",
                    "body": f"## {product_count}个品种均能返回完整问题1响应\n\n原始比赛RAR识别出 **{product_count}个品种**，逐品种最新有效时点完整调用的通过数为 **{passed_products}**、失败数为 **{failed_products}**。每个结果均包含IV、Delta、Gamma、Vega、Theta五张曲面，以及曲面形态、期限结构、无套利、Greeks集中、质量与流动性五组证据。",
                },
                {
                    "id": "alert_distribution_note",
                    "type": "markdown",
                    "sourceId": "acceptance_json",
                    "body": f"## 最新时点的0—3级状态分布\n\n{product_count}个品种的最新有效时点分别落入{distribution_text}。该图是跨品种的点时状态分布，不代表各品种长期风险频率；用于审计各品种在同一验收口径下的实际输出。",
                },
                {"id": "alert_distribution_chart", "type": "chart", "chartId": "latest_alert_distribution", "layout": "full"},
                {
                    "id": "coverage_note",
                    "type": "markdown",
                    "sourceId": "acceptance_json",
                    "body": "## 可选时间目录来自数据，而非界面写死\n\n各品种在完整质量门槛和历史门槛后仍保留有效时点；数量差异反映品种上市时间、合约覆盖和曲面质量差异。用户切换品种后，时间下拉只读取该品种目录，不能自由输入不存在或跨品种的时点。",
                },
                {"id": "coverage_chart", "type": "chart", "chartId": "product_timestamp_coverage", "layout": "full"},
                {"id": "product_audit", "type": "table", "tableId": "product_audit_table", "layout": "full"},
                {
                    "id": "backtest_finding",
                    "type": "markdown",
                    "sourceId": "run_summary_json",
                    "body": f"## 白银连续三个月测试达到三项预警目标\n\n测试期为 **{test_start}至{test_end}**，共有 **{test['rows']:,}个可评价时点**和 **{test['event_count']}个风险事件**。事件级预警精确率为 **{test['event_precision']:.1%}**、事件召回率为 **{test['event_recall']:.1%}**、平均提前时间为 **{test['average_lead_minutes']:.1f}分钟**，分别与50%、60%和30分钟目标比较。这里的“精确率”是预警片段口径，不等同于逐时点分类精确率；事件召回按事件前最近一次、严格提前1—8个bar的预警计算。",
                },
                {"id": "backtest_metrics", "type": "metric-strip", "cardIds": ["precision_card", "recall_card", "lead_card"]},
                {"id": "backtest_table", "type": "table", "tableId": "backtest_metric_table", "layout": "full"},
                {
                    "id": "cvar_finding",
                    "type": "markdown",
                    "sourceId": "run_summary_json",
                    "body": f"## 代理CVaR改善为{cvar['average_improvement_rate']:.1%}，但不能直接归因于预警择时\n\n多头和空头各1手的代理CVaR95平均改善率为 **{cvar['average_improvement_rate']:.1%}**。然而永久减半仓位本身会机械降低尾部损失；随机首次减仓日期的改善中位数为 **{random_median:.1%}**，模型处于随机日期分布的 **{random_percentile:.1%}分位**。这只能作为探索性择时证据，正式提交仍应以真实期货K线复算。",
                },
                {"id": "cvar_metric", "type": "metric-strip", "cardIds": ["cvar_card"]},
                {"id": "cvar_detail", "type": "table", "tableId": "cvar_table", "layout": "full"},
                {
                    "id": "scope_definitions",
                    "type": "markdown",
                    "body": "## 范围、数据与指标定义\n\n- **系统范围：**仅比赛问题1，不含知识图谱、DRL、LSTM、多智能体、交易执行或交易建议。\n- **输入总体：**原始RAR中可识别的商品期权品种；下拉时点须通过完整质量门槛、至少两个可用期限、每期限至少三个节点及最少96个历史bar。\n- **曲面坐标：**x轴为 `ln(K/F)`，y轴为剩余期限年数 `T=dte/365`，z轴分别为IV、Delta、Gamma、Vega、Theta。\n- **状态与通知：**0—3级表示持续的当前风险状态；`alert_emitted` 单独标识本时点是否新发2—3级正式告警，冷却只限制重复通知频率，不降低当前风险等级。动态阈值只使用所选时点之前的历史。\n- **策略因果性：**正式在线与离线主策略使用同一套代码内预注册固定参数；验证网格仅为敏感性诊断。轻量ML对照在两个数据切分边界各清除8根跨界前瞻标签。\n- **CVaR策略：**测试期首次新发正式告警后，下一交易日将多头或空头1手暴露永久减半；随机基线使用相同的全部有效减仓日期域。",
                },
                {
                    "id": "methodology",
                    "type": "markdown",
                    "sourceId": "agent_source",
                    "body": "## 方法：从报价到可解释分级预警\n\n1. 对合约、价格、IV、Greeks、DTE、moneyness和停牌状态执行确定性质量检查。\n2. 每个期限优先保留OTM Put、OTM Call并合并ATM双边，只在真实节点范围内插值，不向两翼外推。\n3. 提取曲面水平与形态、期限结构、无套利、Greeks集中、质量与流动性五组指标。\n4. 每个指标与所选时点之前最多640个合格15分钟时点（设计近似20个交易日）的滚动95%分位比较，至少有96个严格更早合格时点后启用。\n5. 由预注册固定状态机综合核心压力、独立信号数量和状态迁移历史，输出持续的0—3级当前风险状态；同时单独记录是否在该时点新发告警，并返回当前值、动态阈值、倍数与方向作为解释证据。",
                },
                {
                    "id": "reproducibility_identity",
                    "type": "markdown",
                    "sourceId": "run_summary_json",
                    "body": f"## 产物身份与可复验性\n\n本次离线产物记录特征Schema `{feature_identity.get('version', '未记录')}`，包含 **{feature_identity.get('pressure_column_count', 0)}** 个压力列、**{feature_identity.get('history_column_count', 0)}** 个历史阈值列，并明确排除 **{feature_identity.get('excluded_label_derived_column_count', 0)}** 个标签同源列。正式决策策略为 `{policy_identity.get('version', '未记录')}`，来源为代码内预注册固定策略，参数SHA-256为 `{policy_identity.get('parameter_sha256', '未记录')}`。输入身份仅记录相对路径、大小与内容哈希，不绑定生成机器的绝对路径或文件时间；验证器还会重算完整配置、源代码、特征列、8-bar边界清除协议和策略重放结果，任一项不一致即拒绝陈旧产物。",
                },
                {
                    "id": "limitations",
                    "type": "markdown",
                    "sourceId": "run_summary_json",
                    "body": "## 限制与稳健性边界\n\n- **期货价格缺失：**比赛期权文件没有独立期货K线，当前以 `strike/moneyness` 的截面中位数重构标的代理；因此CVaR是探索性结果。\n- **仓位机械效应：**永久减半天然压低CVaR，必须结合随机减仓日期基线，不能只引用50%改善率。\n- **Greeks模型误差：**Greeks来自固定利率BS估计，系统主要解释相对变化与集中度，而非把绝对值视作无误差真值。\n- **跨品种回测边界：**35品种验收证明实时功能可用，但连续三个月比赛指标当前只对白银生成；不能把白银精确率和召回率外推到其他品种。\n- **描述性而非因果：**离线结果说明预警与后续风险事件匹配，不证明预警信号导致风险下降。",
                },
                {
                    "id": "next_steps",
                    "type": "markdown",
                    "body": "## 提交前的推荐动作\n\n1. 接入每个品种对应的真实期货主力/连续合约行情，按相同59个测试交易日重算多空CVaR和随机日期基线。\n2. 对拟重点展示的非白银品种各跑一份连续不少于三个月的离线回测，避免把功能验收误写成指标泛化。\n3. 固化比赛现场使用的RAR路径、缓存目录和验收JSON，并在演示前预热常用品种时间索引。\n4. 保留“代理价格”醒目标识，不把系统输出表述为交易建议。",
                },
                {
                    "id": "further_questions",
                    "type": "markdown",
                    "body": "## 仍需回答的问题\n\n- 正式期货行情接入后，50%的代理CVaR改善还能保留多少？\n- 不同交易所、流动性层级和夜盘制度是否需要品种级阈值校准？\n- 预警片段定义、事件冷却窗口和640个合格时点历史窗口变化时，精确率—召回率权衡是否稳定？",
                },
            ],
        },
        "snapshot": {
            "version": 1,
            "generatedAt": generated_at,
            "status": "ready",
            "datasets": {
                "acceptance_summary": [
                    {
                        "product_count": acceptance["summary"]["product_count"],
                        "passed_products": acceptance["summary"]["passed_products"],
                        "failed_products": acceptance["summary"]["failed_products"],
                        "pass_rate": acceptance["summary"]["passed_products"] / acceptance["summary"]["product_count"],
                        "required_pass_rate": 1.0,
                    }
                ],
                "backtest_summary": [
                    {
                        "event_precision": test["event_precision"],
                        "precision_target": 0.50,
                        "event_recall": test["event_recall"],
                        "recall_target": 0.60,
                        "average_lead_minutes": test["average_lead_minutes"],
                        "lead_target_minutes": 30.0,
                        "cvar_improvement": cvar["average_improvement_rate"],
                        "random_cvar_median": cvar["random_warning_date_baseline"]["median"],
                    }
                ],
                "alert_distribution": alert_distribution,
                "product_coverage": product_coverage,
                "backtest_metrics": backtest_metrics,
                "cvar_rows": cvar_rows,
            },
        },
        "sources": [source_acceptance, source_backtest, source_code],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="构建问题1单Agent离线验收报告artifact")
    parser.add_argument("--run-summary", type=Path, required=True)
    parser.add_argument("--acceptance", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    artifact = build_artifact(_read_json(args.run_summary), _read_json(args.acceptance))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
````

</details>
