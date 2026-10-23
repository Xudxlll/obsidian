---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 这份文件的作用

生成第一问历史离线结果的Notebook伴随展示。源文件：[build_notebook.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_notebook.py>)。

## 输入、输出与核心逻辑

读取outputs/demo的完整离线表、模型摘要与PNG；生成notebooks/01_end_to_end_demo.ipynb。

build_notebook编排数据质量、曲面图片、风险特征、状态通知、事件评估、CVaR、消融与官方事件核验。execute_notebook自上而下执行且不允许错误。

## 与其他文件的关系

最终包只带02 Notebook和轻量demo JSON，缺本脚本期望的Parquet与PNG，不能直接运行成功。代码包含历史简化插值描述，讲正式IV拟合应以当前surfaces与total_variance实现为准。

## 函数与责任定位

|函数/类|源位置|要理解的职责|
|---|---|---|
|`build_notebook`|[10](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_notebook.py:10>)|构建固定顺序的Markdown/代码单元|
|`execute_notebook`|[182](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_notebook.py:182>)|执行全部单元并在无错误后发布|
|`main`|[198](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_notebook.py:198>)|解析参数、调用本文件主业务并处理输出|

## 面试自测

如果上游证据缺失或过期，本脚本应生成一份看似完整的新成绩吗？

> [!success]- 答案
> 不应。先核查输入与身份；报告只整理已有证据，验收脚本必须明确拒绝不完整产物。脚本成功生成HTML也不意味着重新训练过模型。
