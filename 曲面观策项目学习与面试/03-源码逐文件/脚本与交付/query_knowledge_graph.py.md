---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 这份文件的作用

从命令行查询单Agent生成的图谱。源文件：[query_knowledge_graph.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/query_knowledge_graph.py>)。

## 输入、输出与核心逻辑

品种、时点、数据源和固定query名称；输出严格JSON或非0退出。

参数层限定root-evidence、alert-paths、consequences、quality-limitations、node-detail五个CLI选项；node-detail必须精确node-id。内部调用Agent.analyze后构建GraphQueryService，节点错误和不可用图都会拒绝。

## 与其他文件的关系

Python服务还有paths_from_anomaly，但CLI并未列为独立query选项；不要把API能力列表与CLI选项混为一谈。固定查询不是自由自然语言问答，也不是第二个Agent。

## 函数与责任定位

|函数/类|源位置|要理解的职责|
|---|---|---|
|`_force_utf8_streams`|[27](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/query_knowledge_graph.py:27>)|生成force_utf8_streams这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`build_parser`|[35](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/query_knowledge_graph.py:35>)|定义命令行参数合同|
|`_validate_query_arguments`|[51](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/query_knowledge_graph.py:51>)|限制node-id只用于精确节点查询|
|`_agent_config`|[64](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/query_knowledge_graph.py:64>)|生成agent_config这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_query_records`|[74](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/query_knowledge_graph.py:74>)|把固定查询名称分派给GraphQueryService|
|`main`|[91](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/query_knowledge_graph.py:91>)|解析参数、调用本文件主业务并处理输出|

## 面试自测

如果上游证据缺失或过期，本脚本应生成一份看似完整的新成绩吗？

> [!success]- 答案
> 不应。先核查输入与身份；报告只整理已有证据，验收脚本必须明确拒绝不完整产物。脚本成功生成HTML也不意味着重新训练过模型。
