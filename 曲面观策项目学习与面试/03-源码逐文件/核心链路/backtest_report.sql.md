---
类型: 源码教学
模块: 核心链路
源文件: "queries/backtest_report.sql"
依据: 最终提交项目静态源码
---

> [!abstract] 一句话定位
> **直接抽取已保存离线报告的回测字段**。没有用SQL重算CVaR或事件匹配。

源文件：[queries/backtest_report.sql](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/queries/backtest_report.sql:1>)。本文解释实际实现；逐字源码请结合知识库的源码档案阅读。

## 输入、输出与上下游

从outputs/demo/run_summary.json读嵌套字段，输出测试事件Precision/Recall/平均lead、评估行数、事件数、多空CVaR、平均改善、随机日期中位改善和模型经验分位。读到的数值属于文件对应那次run，必须结合run_identity确认当前性。

## 逐个理解核心对象与函数

### SELECT（2—15行）

对test_metrics和cvar_backtest嵌套结构取字段并设平面别名，使报告可导出为一行比较表。long/short为两个假设方向，不代表同时持有。random median和model percentile是核心归因辅助项，不能只保留改善率。

### FROM（16行）

DuckDB read_json_auto直接读取保存的summary；数据、模型和规则一旦变更，只有重新生成匹配身份的summary才会让本查询反映新结果。

## 关键推导、具体例子与真实边界

若event_precision=.55、event_recall=.65、average_lead_minutes=40，它们必须按alerts.py的事件口径解释，不能写“每个预警至少提前40分钟”。若平均CVaR改善.40、随机中位.38，差仅.02（2个百分点），不能将40%都归于预警预测价值。

## 面试怎么讲，追问怎么答

**问：你写了SQL独立复核算法吗？** 此SQL是报告字段抽取，不是独立复现算法。独立复核需要从预测/日收益明细重新匹配与计算。

## 下一步学习

[[曲面观策项目学习与面试/02-循序学习/核心07-CVaR回测到底证明了什么.md|核心07-CVaR回测到底证明了什么]]
