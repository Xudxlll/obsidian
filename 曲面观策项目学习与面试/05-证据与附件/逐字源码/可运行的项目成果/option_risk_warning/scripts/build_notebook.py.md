---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/scripts/build_notebook.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_notebook.py>)

SHA-256：`75727c1700333edc9e9523d40cb20073b96ccc4400fe48db4641580261cdca9d`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from pathlib import Path
import sys

import nbformat as nbf
from nbclient import NotebookClient


def build_notebook() -> nbf.NotebookNode:
    notebook = nbf.v4.new_notebook()
    notebook["metadata"]["kernelspec"] = {
        "display_name": "option-risk-warning",
        "language": "python",
        "name": "python3",
    }
    notebook["metadata"]["language_info"] = {
        "name": "python",
        "version": f"{sys.version_info.major}.{sys.version_info.minor}",
    }
    notebook["cells"] = [
        nbf.v4.new_markdown_cell(
            "# 问题1：波动率曲面、Greeks、风险特征与分级预警\n\n"
            "本 Notebook 是交付结果的可复核伴随文件：交互式 `OptionRiskAgent` 已在原始RAR的"
            "35个品种上完成真实查询验收；连续三个月预警指标和CVaR回测目前以白银为样本。"
            "回测数字来自 `outputs/demo`，测试期为2025-02至2025-04。"
        ),
        nbf.v4.new_markdown_cell(
            "## 0. 单Agent与全品种验收\n\n"
            "对外业务入口只有 `OptionRiskAgent`；用户选择品种后，时间下拉只显示该品种"
            "能够形成完整曲面且具备历史阈值的时点。下表直接读取35品种完整响应验收结果。"
        ),
        nbf.v4.new_code_cell(
            "from pathlib import Path\n"
            "import json\n"
            "import pandas as pd\n"
            "from IPython.display import Image, display\n\n"
            "ROOT = Path.cwd()\n"
            "if not (ROOT / 'outputs').exists():\n"
            "    ROOT = ROOT.parent\n"
            "OUT = ROOT / 'outputs' / 'demo'\n"
            "acceptance = json.loads((ROOT / 'outputs' / 'agent_acceptance_full.json').read_text(encoding='utf-8'))\n"
            "pd.DataFrame([{\n"
            "    '公开业务Agent': ', '.join(acceptance['public_agent_surface']['agent_classes']),\n"
            "    '识别品种数': acceptance['summary']['product_count'],\n"
            "    '完整响应通过数': acceptance['summary']['passed_products'],\n"
            "    '完整响应失败数': acceptance['summary']['failed_products'],\n"
            "}])"
        ),
        nbf.v4.new_code_cell(
            "summary = json.loads((OUT / 'run_summary.json').read_text(encoding='utf-8'))\n"
            "features = pd.read_parquet(OUT / 'risk_features.parquet').set_index('datetime')\n"
            "warnings = pd.read_parquet(OUT / 'warning_predictions.parquet').set_index('datetime')\n"
            "print(f'项目目录: {ROOT}')\n"
            "print(f'曲面快照数: {summary[\"surface\"][\"snapshot_count\"]:,}')"
        ),
        nbf.v4.new_code_cell(
            "identity = summary['run_identity']\n"
            "print(f\"正式策略完整参数哈希: {identity['decision_policy']['parameter_sha256']}\")\n"
            "pd.Series({\n"
            "    '特征Schema': identity['feature_schema']['version'],\n"
            "    '压力列/历史阈值列': f\"{identity['feature_schema']['pressure_column_count']}/"
            "{identity['feature_schema']['history_column_count']}\",\n"
            "    '排除标签同源列': identity['feature_schema']['excluded_label_derived_column_count'],\n"
            "    '决策策略版本': identity['decision_policy']['version'],\n"
            "    '正式策略来源': identity['decision_policy']['selection_data'],\n"
            "    '决策参数哈希': identity['decision_policy']['parameter_sha256'],\n"
            "    '固定样本外协议': identity['evaluation_protocol']['name'],\n"
            "}, name='可复现身份')"
        ),
        nbf.v4.new_markdown_cell(
            "## 1. 数据质量门禁\n\n"
            "质量检查先于建模。停牌、错误期限/价内外程度、异常价格和跨品种行会被排除；"
            "IV 求解下限值单独标记并禁止进入曲面插值。"
        ),
        nbf.v4.new_code_cell(
            "quality = summary['quality']\n"
            "pd.Series({\n"
            "    '扫描文件数': quality['files_scanned'],\n"
            "    '扫描行数': quality['rows_scanned'],\n"
            "    '清洗后行数': quality['clean_rows'],\n"
            "    '保留率': quality['clean_rate'],\n"
            "    'IV求解下限占比': quality['iv_solver_floor_rate_in_clean_data'],\n"
            "    'Schema变体数': quality['schema_variant_count'],\n"
            "}).to_frame('值')"
        ),
        nbf.v4.new_markdown_cell(
            "## 2. 从期限曲线得到 IV 曲面\n\n"
            "固定一个时刻，对每个 DTE 分别得到一条 `ln(K/F) → IV` 曲线；"
            "把不同 DTE 的曲线按纵向排列，在各自真实支持区间内插值，即得到曲面。"
            "图中空白处代表没有真实报价支持，程序没有外推。"
        ),
        nbf.v4.new_code_cell("display(Image(filename=str(OUT / 'figures' / 'latest_iv_surface.png'), width=900))"),
        nbf.v4.new_markdown_cell(
            "## 3. Greeks 曲面\n\n"
            "Delta、Gamma、Vega、Theta 与 IV 使用同一组期限和价内外程度节点，"
            "因此可以直接观察风险敏感度在执行价与期限两个方向上的集中和迁移。"
        ),
        nbf.v4.new_code_cell("display(Image(filename=str(OUT / 'figures' / 'latest_greeks_surfaces.png'), width=1000))"),
        nbf.v4.new_markdown_cell(
            "## 4. 可审计风险特征\n\n"
            "特征覆盖曲面水平/形态、期限结构、无套利几何、Greeks 集中度、"
            "流动性/质量和时间变化。下面展示最新 8 个时刻的关键字段。"
        ),
        nbf.v4.new_code_cell(
            "key_features = [\n"
            "    'atm_iv', 'skew_asymmetry', 'smile_curvature', 'term_slope',\n"
            "    'convexity_violation_ratio', 'max_local_iv_jump',\n"
            "    'put_call_parity_p95_error', 'calendar_variance_violation_ratio',\n"
            "    'gamma_hhi', 'vega_hhi', 'core_risk_pressure', 'surface_coverage'\n"
            "]\n"
            "features[key_features].tail(8).round(4)"
        ),
        nbf.v4.new_markdown_cell(
            "## 5. 四级预警与测试期时间轴\n\n"
            "等级 0/1/2/3 分别表示无预警、关注、警告、危险。"
            "等级表示持续的当前风险状态；`alert_emitted=True` 才表示本时点新发正式告警。"
            "持续高风险阶段保持2/3级；冷却窗口限制持续阶段的重复通知频率，"
            "风险退出后再次进入则视为新事件并立即通知。"
        ),
        nbf.v4.new_code_cell("display(Image(filename=str(OUT / 'figures' / 'test_alert_timeline.png'), width=1100))"),
        nbf.v4.new_code_cell(
            "test_warnings = warnings.query(\"split == 'test' and alert_emitted == True\")\n"
            "test_warnings[['decision_score', 'alert_level', 'alert_name', 'alert_emitted', 'transition_reason',\n"
            "               'policy_version', 'explanation']].tail(12)"
        ),
        nbf.v4.new_markdown_cell("## 6. 验收指标与 CVaR 回测"),
        nbf.v4.new_code_cell(
            "metrics = pd.DataFrame([\n"
            "    {'方法': '预注册固定动态状态机（正式主策略）', **summary['test_metrics']},\n"
            "    {'方法': '固定阈值基线', **summary['rule_baseline_test_metrics']},\n"
            "])\n"
            "metrics[['方法','event_precision','event_recall','average_lead_minutes',\n"
            "         'precision_target_met','recall_target_met','lead_target_met']]"
        ),
        nbf.v4.new_code_cell(
            "cvar = summary['cvar_backtest']\n"
            "pd.DataFrame([cvar['long'], cvar['short']]).set_index('side')"
        ),
        nbf.v4.new_code_cell(
            "pd.Series(cvar['random_warning_date_baseline'], name='随机预警时点对照')"
        ),
        nbf.v4.new_markdown_cell(
            "原始CVaR改善包含‘仓位减半’的机械效果，不能直接归因于模型。"
            "上表用1000个随机减仓日期给出参照分布。"
        ),
        nbf.v4.new_markdown_cell(
            "## 7. 标签同源特征消融与官方极端事件核验\n\n"
            "轻量机器学习只作为对照：模型与阈值在训练/验证期冻结，并在训练→验证、"
            "验证→测试边界清除跨界的8根前瞻标签；连续三个月测试期不复用测试标签。"
            "正式0—3级输出来自代码内预注册固定的可解释动态状态机，验证网格只作敏感性分析。"
        ),
        nbf.v4.new_code_cell(
            "ablation = summary['feature_leakage_ablation']\n"
            "pd.DataFrame([\n"
            " {'模型':'ML消融：剔除标签同源列', **ablation['raw_only_ml_model']},\n"
            " {'模型':'消融对照：保留标签同源列', **ablation['with_label_derived_features']},\n"
            "])[['模型','event_precision','event_recall','average_lead_minutes']]"
        ),
        nbf.v4.new_code_cell(
            "official = pd.read_csv(OUT / 'official_event_comparison.csv')\n"
            "official[['start_date','end_date','event_description','split_at_start',\n"
            "          'prewarned_within_8_bars','alerted_during_event']]"
        ),
        nbf.v4.new_markdown_cell(
            "官方CSV实际有17条记录（赛题文字写18条）；当前9个月白银样本覆盖3条，"
            "连续三个月测试期只覆盖其中1条。该对照不参与模型调参。"
        ),
        nbf.v4.new_markdown_cell(
            "## 8. 重新运行完整链路\n\n"
            "在项目根目录执行：\n\n"
            "```powershell\n"
            ".\\.venv\\Scripts\\python.exe -m option_risk.cli run --data-dir .\\data\\demo "
            "--output-dir .\\outputs\\demo --product ag --start-date 2024-08-01 --end-date 2025-04-30\n"
            "```\n\n"
            "这里不把知识图谱或 DRL 冒充为问题1成果；它们属于赛题问题2/3的进阶模块。"
        ),
    ]
    return notebook


def execute_notebook(
    notebook: nbf.NotebookNode,
    working_directory: str | Path,
) -> nbf.NotebookNode:
    """Execute every code cell and fail instead of saving a partial notebook."""

    client = NotebookClient(
        notebook,
        timeout=300,
        kernel_name="python3",
        allow_errors=False,
        resources={"metadata": {"path": str(Path(working_directory).resolve())}},
    )
    return client.execute()


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    output = project_root / "notebooks" / "01_end_to_end_demo.ipynb"
    output.parent.mkdir(parents=True, exist_ok=True)
    executed = execute_notebook(build_notebook(), project_root)
    nbf.write(executed, output)
    print(output.resolve())


if __name__ == "__main__":
    main()
````

</details>
