---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/queries/backtest_report.sql](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/queries/backtest_report.sql>)

SHA-256：`43d4d89a53d54195187cac2a95a46938a26822458fcd4360d9160355fa54e306`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````sql
-- DuckDB: reproduce the headline test and CVaR metrics from the saved run summary.
SELECT
    test_metrics.event_precision AS event_precision,
    test_metrics.event_recall AS event_recall,
    test_metrics.average_lead_minutes AS average_lead_minutes,
    test_metrics.rows AS evaluated_rows,
    test_metrics.event_count AS event_count,
    cvar_backtest.long.baseline_cvar95 AS long_baseline_cvar95,
    cvar_backtest.long.warning_cvar95 AS long_warning_cvar95,
    cvar_backtest.short.baseline_cvar95 AS short_baseline_cvar95,
    cvar_backtest.short.warning_cvar95 AS short_warning_cvar95,
    cvar_backtest.average_improvement_rate AS average_cvar_improvement_rate,
    cvar_backtest.random_warning_date_baseline.median AS random_date_median_improvement,
    cvar_backtest.random_warning_date_baseline.model_percentile_among_random_dates
        AS model_percentile_among_random_dates
FROM read_json_auto('outputs/demo/run_summary.json');
````

</details>
