---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 文件作用

第一问AG离线实验的历史摘要。

记录配置、清洗数、特征、逻辑回归对照、正式策略、测试事件指标、CVaR、消融、官方事件与run_identity。多数实际预测Parquet和joblib未随最终轻量包交付，摘要可读但不能代替逐行复算。

源文件：[run_summary.json](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/outputs/demo/run_summary.json>)。

## 顶层结构

`project`, `config`, `quality`, `surface`, `model`, `primary_warning_policy`, `alert_policy_walk_forward`, `validation_metrics`, `test_metrics`, `rule_baseline_test_metrics`, `feature_leakage_ablation`, `cvar_backtest`, `official_event_comparison`, `outputs`, `run_identity`。

## 上下游

由Agent验收、离线pipeline或快照脚本生成，报告脚本读取；正式在线决策不从报告反向学习参数。身份、时间、来源和统计分母必须一起核对。

## 面试自测

为什么不能只截一张“passed”的图作为泛化能力证明？

> [!success]- 答案
> passed取决于具体检查合同、品种、时点、数据和代码版本。功能可用性、数值一致性、预测效果、因果解释和实际经济收益是不同主张。
