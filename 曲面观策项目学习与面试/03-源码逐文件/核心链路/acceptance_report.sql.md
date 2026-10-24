---
类型: 源码教学
模块: 核心链路
源文件: "queries/acceptance_report.sql"
依据: 最终提交项目静态源码
---

> [!abstract] 一句话定位
> **从保存的完整Agent验收JSON还原逐品种摘要**。SQL是结果查询层，不执行Agent验收，也不会重新计算曲面。

源文件：[queries/acceptance_report.sql](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/queries/acceptance_report.sql:1>)。本文解释实际实现；逐字源码请结合知识库的源码档案阅读。

## 输入、输出与上下游

在DuckDB中读取outputs/agent_acceptance_full.json。输入要求顶层有products数组，产品对象含status、timestamp范围和analysis字段；输出逐品种验收行并按product排序。上游是CLI validate生成的验收文件，下游是报告表格。

## 逐个理解核心对象与函数

### WITH acceptance（2—5行）

read_json_auto读取指定路径并推断嵌套结构；相对路径依赖执行时工作目录。文件缺失、旧schema或字段类型变化会导致失败或错误口径，不能把路径存在当验收已通过。

### product_rows（6—9行）

UNNEST(products)把一个products数组展开为一行一个product_result结构体；这是展开嵌套结果而不是联表拉行情。

### SELECT与ORDER BY（10—21行）

提取品种、状态、可选时点数、首末时点、最新分析级别/名称，并用ARRAY_LENGTH统计返回的surface_metrics与feature_groups长度。count反映响应结构项目数，不等于每个网格都有足够非缺失节点。

## 关键推导、具体例子与真实边界

例如一个产品surface_metrics=[iv,delta,gamma,vega,theta]，surface_count=5只证明返回五种指标名；完整拟合质量还应看Agent验收的状态和每一响应内部证据。注释写“35-product”是预期报告范围，不会在SQL中强制35个或assert全部passed。

## 面试怎么讲，追问怎么答

**问：SQL证明35个品种都能跑吗？** SQL只读取既有报告；还需核对报告来源、实际35行、status及完整分析是否执行，特别排除catalog-only报告。

## 下一步学习

[[曲面观策项目学习与面试/02-循序学习/核心08-离线Pipeline与单时点Agent的完整关系.md|核心08-离线Pipeline与单时点Agent的完整关系]]
