---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 文件作用

当前合并代码的35品种端到端历史验收。

2026-08-30 UTC生成，summary为35/35通过、0失败；逐品种只分析最新有效时间点，记录5曲面、5组证据、策略身份、图谱状态。不是35品种三个月收益回测。

源文件：[agent_acceptance_full.json](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/outputs/agent_acceptance_full.json>)。

## 顶层结构

`generated_at`, `mode`, `public_agent_surface`, `summary`, `products`。

## 上下游

由Agent验收、离线pipeline或快照脚本生成，报告脚本读取；正式在线决策不从报告反向学习参数。身份、时间、来源和统计分母必须一起核对。

## 面试自测

为什么不能只截一张“passed”的图作为泛化能力证明？

> [!success]- 答案
> passed取决于具体检查合同、品种、时点、数据和代码版本。功能可用性、数值一致性、预测效果、因果解释和实际经济收益是不同主张。
