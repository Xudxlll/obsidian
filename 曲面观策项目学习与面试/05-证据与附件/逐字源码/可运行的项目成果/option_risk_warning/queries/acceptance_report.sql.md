---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/queries/acceptance_report.sql](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/queries/acceptance_report.sql>)

SHA-256：`9b00d00faf7321ad4c2cb8b7ad1e0ae180daf41e241f6a05b570cf33ca4a8253`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````sql
-- DuckDB: reproduce the report rows from the full 35-product Agent acceptance JSON.
WITH acceptance AS (
    SELECT *
    FROM read_json_auto('outputs/agent_acceptance_full.json')
),
product_rows AS (
    SELECT UNNEST(products) AS product_result
    FROM acceptance
)
SELECT
    product_result.product AS product,
    product_result.status AS status,
    product_result.timestamp_count AS timestamp_count,
    product_result.first_timestamp AS first_timestamp,
    product_result.last_timestamp AS last_timestamp,
    product_result.analysis.alert_level AS latest_alert_level,
    product_result.analysis.alert_name AS latest_alert_name,
    ARRAY_LENGTH(product_result.analysis.surface_metrics) AS surface_count,
    ARRAY_LENGTH(product_result.analysis.feature_groups) AS feature_group_count
FROM product_rows
ORDER BY product;
````

</details>
