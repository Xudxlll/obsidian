---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 这份文件的作用

生成并执行问题二Notebook及五种代表快照。源文件：[build_knowledge_graph_notebook.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py>)。

## 输入、输出与核心逻辑

Notebook以一个OptionRiskAgent读取真实ag时点；快照输入还需要35品种正式验收JSON，输出真实0/1/2、质量受限、合成3级。

build_notebook确定11个单元；execute_notebook禁止错误并原子发布。build_snapshot先校验35品种验收，优先取验收中的真实案例，数据不覆盖时用预设AG候选。_synthetic_level_three显式构造契约输入且标注不代表市场；_portable_value移除主机绝对路径。

## 与其他文件的关系

快照与评分模板、问题二HTML相连；Notebook是另一个演示入口。--snapshot-only与--notebook-only互斥。不要默认执行main覆盖原交付，学习复现使用独立副本。

## 函数与责任定位

|函数/类|源位置|要理解的职责|
|---|---|---|
|`_cell`|[51](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:51>)|生成cell这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`build_notebook`|[56](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:56>)|构建固定顺序的Markdown/代码单元|
|`execute_notebook`|[248](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:248>)|执行全部单元并在无错误后发布|
|`_strict_json`|[288](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:288>)|生成strict_json这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_validate_acceptance`|[298](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:298>)|核对35品种及三项正式门禁的先决证据|
|`_case_queries`|[341](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:341>)|对一个结果执行所有预设查询并保存回答|
|`_result_summary`|[367](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:367>)|生成result_summary这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_portable_value`|[385](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:385>)|去掉主机专属绝对路径保留相对溯源|
|`_portable_real_graph`|[406](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:406>)|用可移植溯源重建同一正式规则图|
|`_snapshot_case`|[446](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:446>)|把身份、图、查询、解释和路径引用组装成案例|
|`_real_case`|[484](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:484>)|检查真实案例等级和质量场景是否与请求匹配|
|`_contract_evidence`|[504](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:504>)|为合成测试调整证据压力并明确来源|
|`_synthetic_level_three`|[524](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:524>)|构造3级合同检查输入，不用于市场业绩|
|`_accepted_candidates`|[583](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:583>)|从正式验收中选择0/1/2与质量受限候选|
|`_analyze_candidate`|[601](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:601>)|候选存在且时点有效才调用真实Agent|
|`_atomic_json`|[615](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:615>)|严格JSON序列化后原子发布|
|`build_snapshot`|[646](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:646>)|从真实Agent生成四案例并附一个标注的3级契约案例|
|`_source_environment`|[708](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:708>)|临时设定数据环境变量并在结束后恢复|
|`parse_args`|[731](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:731>)|定义命令行参数与默认路径|
|`main`|[759](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py:759>)|解析参数、调用本文件主业务并处理输出|

## 面试自测

如果上游证据缺失或过期，本脚本应生成一份看似完整的新成绩吗？

> [!success]- 答案
> 不应。先核查输入与身份；报告只整理已有证据，验收脚本必须明确拒绝不完整产物。脚本成功生成HTML也不意味着重新训练过模型。
