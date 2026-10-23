---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 文件作用

第一问报告的数据与布局中间文件。

surface=report，manifest保存指标卡/图/表/解释段布局，snapshot.datasets保存真正展示的数据，sources指向验收JSON与SQL来源。render_acceptance_html只渲染它；这不是在线模型参数。

源文件：[问题1-Agent离线验收报告.artifact.json](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/outputs/问题1-Agent离线验收报告.artifact.json>)。

## 顶层结构

`surface`, `manifest`, `snapshot`, `sources`。

## 上下游

由Agent验收、离线pipeline或快照脚本生成，报告脚本读取；正式在线决策不从报告反向学习参数。身份、时间、来源和统计分母必须一起核对。

## 面试自测

为什么不能只截一张“passed”的图作为泛化能力证明？

> [!success]- 答案
> passed取决于具体检查合同、品种、时点、数据和代码版本。功能可用性、数值一致性、预测效果、因果解释和实际经济收益是不同主张。
