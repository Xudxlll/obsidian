---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 文件作用

五种解释案例的便携快照。

4个真实案例（0/1/2级和质量受限）加1个synthetic_contract的3级案例。保存Agent摘要、完整图、固定查询和解释，绑定正式验收SHA。它是案例回放证据，不是训练集或长期图数据库。

源文件：[knowledge_graph_snapshot.json](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/outputs/demo/knowledge_graph_snapshot.json>)。

## 顶层结构

`format_version`, `schema_version`, `rule_version`, `generated_at`, `formal_acceptance_sha256`, `case_count`, `real_case_count`, `synthetic_contract_case_count`, `synthetic_contract_boundary`, `cases`。

## 上下游

由Agent验收、离线pipeline或快照脚本生成，报告脚本读取；正式在线决策不从报告反向学习参数。身份、时间、来源和统计分母必须一起核对。

## 面试自测

为什么不能只截一张“passed”的图作为泛化能力证明？

> [!success]- 答案
> passed取决于具体检查合同、品种、时点、数据和代码版本。功能可用性、数值一致性、预测效果、因果解释和实际经济收益是不同主张。
