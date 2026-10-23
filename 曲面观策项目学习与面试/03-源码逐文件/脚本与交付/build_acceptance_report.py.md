---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 这份文件的作用

把第一问的历史AG回测摘要与品种验收整理成报告数据模型。源文件：[build_acceptance_report.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_acceptance_report.py>)。

## 输入、输出与核心逻辑

输入run_summary与agent_acceptance两个JSON；输出artifact JSON。它不是训练脚本，也不重新跑Agent。

_metric_row将实际值与目标统一为报告行；build_artifact整理指标卡、品种覆盖、等级分布、CVaR表、限制说明和来源字段。snapshot.datasets保存表格数据，manifest保存视图布局，sources保存出处。

## 与其他文件的关系

build_artifact → render_acceptance_html.render_html → 第一问HTML。报告写“仅问题1”反映历史报告范围；不能把它当作最终系统不含问题2的证据。

## 函数与责任定位

|函数/类|源位置|要理解的职责|
|---|---|---|
|`_read_json`|[13](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_acceptance_report.py:13>)|读取JSON源证据，不作模型训练|
|`_metric_row`|[17](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_acceptance_report.py:17>)|计算单项报告实际/目标/是否达标展示行|
|`build_artifact`|[41](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_acceptance_report.py:41>)|把摘要和验收转为可渲染的数据与布局|
|`main`|[410](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_acceptance_report.py:410>)|解析参数、调用本文件主业务并处理输出|

## 面试自测

如果上游证据缺失或过期，本脚本应生成一份看似完整的新成绩吗？

> [!success]- 答案
> 不应。先核查输入与身份；报告只整理已有证据，验收脚本必须明确拒绝不完整产物。脚本成功生成HTML也不意味着重新训练过模型。
