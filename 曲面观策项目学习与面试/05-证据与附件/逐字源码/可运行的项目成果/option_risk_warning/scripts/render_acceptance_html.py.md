---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/scripts/render_acceptance_html.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/render_acceptance_html.py>)

SHA-256：`2eeff645c758dffc95d0c77e2aa35d5fcb83172c72291078b06ece1e198460fb`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import argparse
from html import escape
import json
import math
from pathlib import Path
import sys
from typing import Any, Mapping


DEFAULT_TITLE = "期权波动率曲面风控智能体：问题1离线验收报告"
REQUIRED_DATASETS = {
    "acceptance_summary",
    "backtest_summary",
    "alert_distribution",
    "product_coverage",
    "backtest_metrics",
    "cvar_rows",
}


class ArtifactError(ValueError):
    """Raised when the report artifact does not satisfy the renderer contract."""


def _as_mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ArtifactError(f"{label} must be an object")
    return value


def _as_rows(value: object, label: str) -> list[Mapping[str, Any]]:
    if not isinstance(value, list) or not all(isinstance(row, Mapping) for row in value):
        raise ArtifactError(f"{label} must be an array of objects")
    return value


def _one_row(datasets: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    rows = _as_rows(datasets.get(name), f"snapshot.datasets.{name}")
    if len(rows) != 1:
        raise ArtifactError(f"snapshot.datasets.{name} must contain exactly one row")
    return rows[0]


def _number(row: Mapping[str, Any], field: str, label: str) -> float:
    value = row.get(field)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ArtifactError(f"{label}.{field} must be numeric")
    number = float(value)
    if not math.isfinite(number):
        raise ArtifactError(f"{label}.{field} must be finite")
    return number


def _integer(row: Mapping[str, Any], field: str, label: str) -> int:
    number = _number(row, field, label)
    if not number.is_integer():
        raise ArtifactError(f"{label}.{field} must be an integer")
    return int(number)


def _text(value: object) -> str:
    return escape(str(value), quote=True)


def _percent(value: float) -> str:
    return f"{value:.1%}"


def _metric_cards(rows: list[Mapping[str, Any]]) -> str:
    if len(rows) != 3:
        raise ArtifactError("snapshot.datasets.backtest_metrics must contain three rows")
    cards: list[str] = []
    for index, row in enumerate(rows):
        label = f"snapshot.datasets.backtest_metrics[{index}]"
        actual = row.get("actual_text")
        target = row.get("target_text")
        if actual is None or target is None:
            raise ArtifactError(f"{label} is missing display values")
        passed = str(row.get("passed", ""))
        outcome_class = "pass" if passed == "通过" else "review"
        cards.append(
            f"""
            <article class="metric-card">
              <div class="metric-topline"><span>{_text(row.get('metric', '未命名指标'))}</span><span class="pill {outcome_class}">{_text(passed or '未标记')}</span></div>
              <div class="metric-value">{_text(actual)}</div>
              <div class="metric-target">目标 {_text(target)}</div>
              <p>{_text(row.get('definition', ''))}</p>
            </article>"""
        )
    return "".join(cards)


def _distribution_svg(rows: list[Mapping[str, Any]]) -> str:
    if len(rows) != 4:
        raise ArtifactError("snapshot.datasets.alert_distribution must contain four rows")
    parsed: list[tuple[int, str, int, float]] = []
    for index, row in enumerate(rows):
        label = f"snapshot.datasets.alert_distribution[{index}]"
        level = _integer(row, "alert_level", label)
        count = _integer(row, "product_count", label)
        share = _number(row, "product_share", label)
        if level not in range(4) or count < 0 or not 0 <= share <= 1:
            raise ArtifactError(f"{label} contains an invalid level, count, or share")
        parsed.append((level, str(row.get("alert_label", level)), count, share))
    parsed.sort(key=lambda item: item[0])
    if [item[0] for item in parsed] != [0, 1, 2, 3]:
        raise ArtifactError("alert_distribution must contain levels 0, 1, 2, and 3")

    max_count = max(1, *(item[2] for item in parsed))
    fills = ["#64748b", "#2563eb", "#d97706", "#dc2626"]
    shapes: list[str] = []
    for position, (level, label, count, share) in enumerate(parsed):
        x = 55 + position * 165
        bar_height = 150 * count / max_count
        y = 195 - bar_height
        shapes.append(
            f"""
            <g>
              <rect x="{x}" y="{y:.2f}" width="108" height="{bar_height:.2f}" rx="9" fill="{fills[level]}"></rect>
              <text x="{x + 54}" y="{max(24, y - 10):.2f}" text-anchor="middle" class="chart-value">{count} 个</text>
              <text x="{x + 54}" y="222" text-anchor="middle" class="chart-label">{_text(label)}</text>
              <text x="{x + 54}" y="244" text-anchor="middle" class="chart-share">{_percent(share)}</text>
            </g>"""
        )
    return f"""
      <svg class="distribution-chart" viewBox="0 0 710 260" role="img" aria-labelledby="distribution-title distribution-desc">
        <title id="distribution-title">0—3级状态分布</title>
        <desc id="distribution-desc">四个预警等级对应的品种数量和占比</desc>
        <line x1="36" y1="196" x2="690" y2="196" stroke="#cbd5e1" stroke-width="1"></line>
        {''.join(shapes)}
      </svg>"""


def _product_rows(rows: list[Mapping[str, Any]], expected_count: int) -> str:
    if len(rows) != expected_count:
        raise ArtifactError(
            "product_coverage row count does not match acceptance_summary.product_count"
        )
    rendered: list[str] = []
    for index, row in enumerate(rows):
        label = f"snapshot.datasets.product_coverage[{index}]"
        timestamp_count = _integer(row, "timestamp_count", label)
        level = _integer(row, "latest_alert_level", label)
        surface_count = _integer(row, "surface_count", label)
        feature_count = _integer(row, "feature_group_count", label)
        if level not in range(4) or min(timestamp_count, surface_count, feature_count) < 0:
            raise ArtifactError(f"{label} contains an invalid count or alert level")
        status = str(row.get("status", ""))
        status_class = "pass" if status == "passed" else "review"
        rendered.append(
            f"""
            <tr class="product-row">
              <td class="product-code">{_text(row.get('product', ''))}</td>
              <td class="numeric">{timestamp_count:,}</td>
              <td>{_text(str(row.get('first_timestamp', '')).replace('T', ' '))}</td>
              <td>{_text(str(row.get('last_timestamp', '')).replace('T', ' '))}</td>
              <td><span class="level level-{level}">{level} · {_text(row.get('latest_alert_name', ''))}</span></td>
              <td class="numeric">{surface_count}</td>
              <td class="numeric">{feature_count}</td>
              <td><span class="pill {status_class}">{_text(status)}</span></td>
            </tr>"""
        )
    return "".join(rendered)


def _cvar_rows(rows: list[Mapping[str, Any]]) -> str:
    if not rows:
        raise ArtifactError("snapshot.datasets.cvar_rows must not be empty")
    rendered: list[str] = []
    for index, row in enumerate(rows):
        label = f"snapshot.datasets.cvar_rows[{index}]"
        baseline = _number(row, "baseline_cvar95", label)
        warning = _number(row, "warning_cvar95", label)
        improvement = _number(row, "improvement_rate", label)
        rendered.append(
            f"""
            <tr>
              <td>{_text(row.get('side', ''))}</td>
              <td class="numeric">{_percent(baseline)}</td>
              <td class="numeric">{_percent(warning)}</td>
              <td class="numeric positive">{_percent(improvement)}</td>
            </tr>"""
        )
    return "".join(rendered)


CSS = """
:root {
  color-scheme: light;
  --ink: #172033;
  --muted: #5f6b7a;
  --line: #dbe3ee;
  --paper: #ffffff;
  --canvas: #f4f7fb;
  --navy: #102a43;
  --blue: #2563eb;
  --blue-soft: #eaf1ff;
  --green: #15803d;
  --green-soft: #e9f8ef;
  --amber: #b45309;
  --amber-soft: #fff5df;
  --red: #b91c1c;
  --red-soft: #feecec;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; background: var(--canvas); }
body { margin: 0; color: var(--ink); background: var(--canvas); line-height: 1.65; }
.page { width: min(1180px, calc(100% - 40px)); margin: 32px auto 64px; }
.hero { position: relative; overflow: hidden; padding: 48px; color: #fff; background: linear-gradient(135deg, #0f2742, #174f78); border-radius: 24px; box-shadow: 0 20px 55px rgba(15, 39, 66, .18); }
.hero::after { content: ""; position: absolute; width: 310px; height: 310px; right: -95px; top: -135px; border-radius: 50%; background: rgba(255,255,255,.08); }
.eyebrow { margin: 0 0 12px; color: #b9ddff; font-size: 13px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
h1 { max-width: 850px; margin: 0; font-size: clamp(31px, 5vw, 52px); line-height: 1.15; letter-spacing: -.025em; }
.hero-summary { max-width: 880px; margin: 20px 0 0; color: #dcecff; font-size: 17px; }
.hero-meta { display: flex; flex-wrap: wrap; gap: 10px 20px; margin-top: 28px; color: #c6def2; font-size: 13px; }
.section { margin-top: 28px; padding: 30px; background: var(--paper); border: 1px solid var(--line); border-radius: 18px; box-shadow: 0 8px 30px rgba(28, 52, 84, .06); }
.section-heading { display: flex; align-items: end; justify-content: space-between; gap: 24px; margin-bottom: 22px; }
.section-heading h2 { margin: 0; color: var(--navy); font-size: 25px; letter-spacing: -.015em; }
.section-heading p { max-width: 670px; margin: 5px 0 0; color: var(--muted); }
.acceptance-grid { display: grid; grid-template-columns: minmax(240px, .75fr) 2fr; gap: 20px; }
.acceptance-card { display: grid; place-content: center; min-height: 210px; padding: 24px; text-align: center; background: var(--green-soft); border: 1px solid #b9e5c8; border-radius: 16px; }
.acceptance-value { color: var(--green); font-size: 48px; font-weight: 800; letter-spacing: -.04em; }
.acceptance-label { color: #326b46; font-weight: 700; }
.acceptance-copy { padding: 18px 4px; }
.acceptance-copy h3 { margin: 0 0 10px; color: var(--navy); font-size: 22px; }
.acceptance-copy p { margin: 0 0 12px; color: var(--muted); }
.metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.metric-card { padding: 22px; border: 1px solid var(--line); border-radius: 15px; background: linear-gradient(180deg, #fff, #f8fbff); }
.metric-topline { display: flex; align-items: start; justify-content: space-between; gap: 12px; color: var(--navy); font-weight: 750; }
.metric-value { margin-top: 18px; color: var(--blue); font-size: 36px; font-weight: 800; line-height: 1; letter-spacing: -.03em; }
.metric-target { margin-top: 10px; color: var(--muted); font-size: 13px; }
.metric-card p { margin: 15px 0 0; color: var(--muted); font-size: 13px; }
.pill { display: inline-flex; align-items: center; padding: 3px 9px; border-radius: 999px; font-size: 12px; font-weight: 750; white-space: nowrap; }
.pill.pass { color: var(--green); background: var(--green-soft); }
.pill.review { color: var(--amber); background: var(--amber-soft); }
.distribution-wrap { display: grid; grid-template-columns: minmax(0, 1.6fr) minmax(260px, .7fr); gap: 22px; align-items: center; }
.distribution-chart { display: block; width: 100%; min-height: 260px; border-radius: 14px; background: #f8fafc; }
.chart-value { fill: var(--ink); font-size: 15px; font-weight: 750; }
.chart-label { fill: var(--ink); font-size: 13px; font-weight: 700; }
.chart-share { fill: var(--muted); font-size: 12px; }
.callout { padding: 20px; color: #28435d; background: var(--blue-soft); border-left: 4px solid var(--blue); border-radius: 10px; }
.callout strong { display: block; color: var(--navy); margin-bottom: 6px; }
.table-wrap { overflow-x: auto; border: 1px solid var(--line); border-radius: 13px; }
table { width: 100%; border-collapse: collapse; background: #fff; font-size: 13px; }
th { padding: 12px 14px; color: #3e5268; background: #f1f5f9; text-align: left; font-size: 12px; letter-spacing: .015em; white-space: nowrap; }
td { padding: 11px 14px; border-top: 1px solid #e8edf3; vertical-align: middle; white-space: nowrap; }
tbody tr:hover { background: #f8fbff; }
.product-code { color: var(--navy); font-weight: 800; }
.numeric { text-align: right; font-variant-numeric: tabular-nums; }
.positive { color: var(--green); font-weight: 750; }
.level { display: inline-flex; min-width: 92px; padding: 3px 9px; border-radius: 999px; font-weight: 700; }
.level-0 { color: #475569; background: #edf1f5; }
.level-1 { color: #1d4ed8; background: #e8efff; }
.level-2 { color: #a04b00; background: #fff1d6; }
.level-3 { color: #b91c1c; background: #fee8e8; }
.cvar-summary { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 18px; }
.summary-tile { padding: 20px; background: #f8fafc; border: 1px solid var(--line); border-radius: 14px; }
.summary-tile span { display: block; color: var(--muted); font-size: 13px; }
.summary-tile strong { display: block; margin-top: 6px; color: var(--navy); font-size: 30px; }
.prose-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.prose-card { padding: 22px; border: 1px solid var(--line); border-radius: 14px; background: #fbfcfe; }
.prose-card h3 { margin: 0 0 12px; color: var(--navy); font-size: 18px; }
.prose-card p, .prose-card li { color: var(--muted); font-size: 14px; }
.prose-card ol, .prose-card ul { margin: 0; padding-left: 20px; }
code { padding: 2px 6px; color: #174467; background: #edf4fa; border-radius: 5px; font-family: Consolas, "SFMono-Regular", monospace; font-size: .9em; }
footer { padding: 28px 8px 0; color: var(--muted); text-align: center; font-size: 12px; }
@media (max-width: 850px) {
  .page { width: min(100% - 24px, 1180px); margin-top: 12px; }
  .hero { padding: 32px 24px; border-radius: 18px; }
  .section { padding: 22px 18px; }
  .acceptance-grid, .distribution-wrap, .prose-grid { grid-template-columns: 1fr; }
  .metrics { grid-template-columns: 1fr; }
  .cvar-summary { grid-template-columns: 1fr; }
}
@media print {
  body { background: #fff; }
  .page { width: 100%; margin: 0; }
  .hero, .section { box-shadow: none; break-inside: avoid; }
  .section { margin-top: 16px; }
}
"""


def render_html(artifact: Mapping[str, Any]) -> str:
    snapshot = _as_mapping(artifact.get("snapshot"), "snapshot")
    datasets = _as_mapping(snapshot.get("datasets"), "snapshot.datasets")
    missing = sorted(REQUIRED_DATASETS - set(datasets))
    if missing:
        raise ArtifactError(f"artifact is missing datasets: {', '.join(missing)}")

    acceptance = _one_row(datasets, "acceptance_summary")
    backtest = _one_row(datasets, "backtest_summary")
    distribution = _as_rows(datasets["alert_distribution"], "alert_distribution")
    products = _as_rows(datasets["product_coverage"], "product_coverage")
    metrics = _as_rows(datasets["backtest_metrics"], "backtest_metrics")
    cvar = _as_rows(datasets["cvar_rows"], "cvar_rows")

    product_count = _integer(acceptance, "product_count", "acceptance_summary")
    passed = _integer(acceptance, "passed_products", "acceptance_summary")
    failed = _integer(acceptance, "failed_products", "acceptance_summary")
    pass_rate = _number(acceptance, "pass_rate", "acceptance_summary")
    if product_count <= 0 or min(passed, failed) < 0 or passed + failed != product_count:
        raise ArtifactError("acceptance_summary counts are inconsistent")

    cvar_improvement = _number(backtest, "cvar_improvement", "backtest_summary")
    random_median = _number(backtest, "random_cvar_median", "backtest_summary")
    manifest = artifact.get("manifest")
    manifest = manifest if isinstance(manifest, Mapping) else {}
    title = manifest.get("title", DEFAULT_TITLE)
    description = manifest.get(
        "description",
        "问题1单Agent实现、全品种可用性及连续三个月离线回测的技术验收报告。",
    )
    generated_at = artifact.get("generatedAt") or snapshot.get("generatedAt") or "未记录"
    status = snapshot.get("status", "未记录")
    overall = "全部通过" if failed == 0 and passed == product_count else "存在待复核项"

    metric_html = _metric_cards(metrics)
    distribution_html = _distribution_svg(distribution)
    products_html = _product_rows(products, product_count)
    cvar_html = _cvar_rows(cvar)

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; script-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'">
  <meta name="description" content="{_text(description)}">
  <title>{_text(title)}</title>
  <style>{CSS}</style>
</head>
<body>
  <main class="page">
    <header class="hero">
      <p class="eyebrow">Option Risk · Offline Acceptance</p>
      <h1>{_text(title)}</h1>
      <p class="hero-summary">{_text(description)}</p>
      <div class="hero-meta"><span>结论：{_text(overall)}</span><span>Artifact 状态：{_text(status)}</span><span>生成时间：{_text(generated_at)}</span></div>
    </header>

    <section class="section" aria-labelledby="acceptance-heading">
      <div class="section-heading"><div><h2 id="acceptance-heading">全品种功能验收</h2><p>逐品种使用真实可选时点完成曲面、特征、分级状态、解释与时间轴响应。</p></div><span class="pill {'pass' if failed == 0 else 'review'}">{_text(overall)}</span></div>
      <div class="acceptance-grid">
        <div class="acceptance-card"><div class="acceptance-value">{passed} / {product_count}</div><div class="acceptance-label">完整响应通过 · {_percent(pass_rate)}</div></div>
        <div class="acceptance-copy"><h3>{product_count} 个品种均纳入同一验收口径</h3><p>通过 {passed} 个，失败 {failed} 个。每个产品行均保留可选时点范围、最新0—3级状态、曲面数、特征组数与验收状态，便于逐项复核。</p><div class="callout"><strong>结论边界</strong>全品种验收证明交互式 Agent 功能可运行；连续三个月的比赛指标仍是单独的样本外回测结论。</div></div>
      </div>
    </section>

    <section class="section" aria-labelledby="metrics-heading">
      <div class="section-heading"><div><h2 id="metrics-heading">三项核心预警指标</h2><p>实测值与 artifact 中固化的比赛目标直接并列；精确率和召回率采用事件级口径。</p></div></div>
      <div class="metrics">{metric_html}</div>
    </section>

    <section class="section" aria-labelledby="distribution-heading">
      <div class="section-heading"><div><h2 id="distribution-heading">35品种最新时点的0—3级状态分布</h2><p>这是各品种最新有效时点的横截面状态，不代表长期预警频率。</p></div></div>
      <div class="distribution-wrap">{distribution_html}<div class="callout"><strong>状态与通知分离</strong>0—3级是持续的当前风险状态；正式告警是否在本时点新发由独立字段记录，冷却期不应降低当前等级。</div></div>
    </section>

    <section class="section" aria-labelledby="coverage-heading">
      <div class="section-heading"><div><h2 id="coverage-heading">35品种时点覆盖与响应审计</h2><p>表内完整保留 artifact 的全部产品；时点数来自质量与历史门槛后的真实目录。</p></div></div>
      <div class="table-wrap"><table><thead><tr><th>品种</th><th class="numeric">可选时点</th><th>首个时点</th><th>最后时点</th><th>最新状态</th><th class="numeric">曲面</th><th class="numeric">特征组</th><th>验收</th></tr></thead><tbody>{products_html}</tbody></table></div>
    </section>

    <section class="section" aria-labelledby="cvar-heading">
      <div class="section-heading"><div><h2 id="cvar-heading">代理CVaR与随机日期基线</h2><p>减半仓位会机械降低尾部损失，因此必须把预警方案与同规则随机减仓日期对照。</p></div></div>
      <div class="cvar-summary"><div class="summary-tile"><span>多空平均代理CVaR改善</span><strong>{_percent(cvar_improvement)}</strong></div><div class="summary-tile"><span>随机日期基线中位数</span><strong>{_percent(random_median)}</strong></div></div>
      <div class="table-wrap"><table><thead><tr><th>方向</th><th class="numeric">基线CVaR95</th><th class="numeric">预警后CVaR95</th><th class="numeric">改善率</th></tr></thead><tbody>{cvar_html}</tbody></table></div>
    </section>

    <section class="section" aria-labelledby="method-heading">
      <div class="section-heading"><div><h2 id="method-heading">方法、可复验性与限制</h2><p>报告仅把 artifact 固化事实转成可读页面，不连接网络，也不重新计算业务指标。</p></div></div>
      <div class="prose-grid">
        <article class="prose-card"><h3>方法</h3><ol><li>对报价、IV、Greeks、期限与流动性执行确定性质量检查。</li><li>从曲面形态、期限结构、无套利、Greeks集中及质量流动性形成解释证据。</li><li>动态参考只使用所选时点之前的历史；主策略由同一预注册状态机输出0—3级状态。</li><li>轻量ML对照在训练—验证、验证—测试边界清除跨界前瞻标签。</li></ol></article>
        <article class="prose-card"><h3>可复验性</h3><p>输入为一个 UTF-8 artifact JSON；本脚本仅使用 Python 标准库。Artifact 版本 <code>{_text(manifest.get('version', '未记录'))}</code>，Snapshot 版本 <code>{_text(snapshot.get('version', '未记录'))}</code>，状态 <code>{_text(status)}</code>。</p><p>重复执行同一 <code>--artifact</code> 与 <code>--output</code> 命令即可重建本单文件HTML；所有CSS均内联，CSP禁止网络连接与脚本执行。</p></article>
        <article class="prose-card"><h3>限制</h3><ul><li>比赛期权数据缺少独立期货K线，CVaR基于重构标的代理，只能作探索性证据。</li><li>永久减半仓位本身会降低CVaR，不能把全部改善归因于预警择时。</li><li>35品种功能验收不等于三个月指标可外推到全部品种。</li><li>离线匹配是描述性证据，不构成因果结论或交易建议。</li></ul></article>
      </div>
    </section>
    <footer>自包含离线报告 · 无外部字体、CDN、脚本或网络请求 · 数据来自传入 artifact</footer>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="将验收artifact渲染为自包含离线HTML")
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        payload = json.loads(args.artifact.read_text(encoding="utf-8"))
        artifact = _as_mapping(payload, "artifact")
        rendered = render_html(artifact)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    except (ArtifactError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"无法生成验收HTML：{exc}", file=sys.stderr)
        return 2
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
````

</details>
