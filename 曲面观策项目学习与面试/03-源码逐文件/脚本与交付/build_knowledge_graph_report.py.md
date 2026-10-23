---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 这份文件的作用

核对正式图谱证据并生成第二问离线报告。源文件：[build_knowledge_graph_report.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py>)。

## 输入、输出与核心逻辑

输入knowledge_graph_acceptance_full.json、五案例snapshot、可选真实人工评分汇总；输出HTML。

_reconcile_acceptance逐品种复核数量、版本、状态、图谱和三门禁；_reconcile_snapshot用验收文件SHA绑定快照并重新运行固定查询核对答案。_load_review_summary验证算术但不虚构评分。HTML只展示最多三条代表路径，保留五案例与35行表。

## 与其他文件的关系

正式JSON是源，HTML是展示；不应逆向修改JSON以让报告好看。没有评分时页面明确待完成。_safe_html拒绝脚本/外链，_atomic_write防止半写发布。

## 函数与责任定位

|函数/类|源位置|要理解的职责|
|---|---|---|
|`_reject_constant`|[51](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:51>)|生成reject_constant这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_load_json`|[55](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:55>)|生成load_json这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_strict_int`|[65](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:65>)|生成strict_int这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_nonempty`|[71](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:71>)|生成nonempty这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_reconcile_acceptance`|[77](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:77>)|逐行重算并核对正式验收数量与状态|
|`_reconcile_snapshot`|[194](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:194>)|校验快照身份、真实/合成计数与固定查询答案|
|`_load_review_summary`|[298](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:298>)|核对已有真实评分汇总的有限值和算术|
|`_fmt_number`|[344](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:344>)|生成fmt_number这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_node_records`|[350](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:350>)|生成node_records这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_svg_label`|[357](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:357>)|生成svg_label这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_representative_svg`|[364](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:364>)|生成representative_svg这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_representative_mobile`|[419](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:419>)|生成representative_mobile这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_requirement_rows`|[440](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:440>)|生成requirement_rows这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_schema_rows`|[458](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:458>)|生成schema_rows这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_mapping_rows`|[476](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:476>)|生成mapping_rows这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_case_cards`|[491](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:491>)|生成case_cards这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_product_rows`|[528](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:528>)|生成product_rows这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_check_cards`|[549](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:549>)|生成check_cards这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_review_panel`|[563](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:563>)|生成review_panel这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_html_document`|[580](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:580>)|生成html_document这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_safe_html`|[641](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:641>)|拒绝脚本及外部资源引用|
|`_atomic_write`|[649](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:649>)|暂存写入、flush/fsync、原子替换输出|
|`build_report`|[673](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:673>)|Reconcile formal evidence, then atomically publish a safe offline report.|
|`parse_args`|[698](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:698>)|定义命令行参数与默认路径|
|`main`|[724](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py:724>)|解析参数、调用本文件主业务并处理输出|

## 面试自测

如果上游证据缺失或过期，本脚本应生成一份看似完整的新成绩吗？

> [!success]- 答案
> 不应。先核查输入与身份；报告只整理已有证据，验收脚本必须明确拒绝不完整产物。脚本成功生成HTML也不意味着重新训练过模型。
