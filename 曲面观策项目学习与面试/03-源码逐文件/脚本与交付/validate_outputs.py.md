---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 这份文件的作用

对第一问完整离线产物做独立重算与身份检查。源文件：[validate_outputs.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/validate_outputs.py>)。

## 输入、输出与核心逻辑

要求features、labels、predictions、joblib、npz、CSV、图像等15项；默认outputs/demo。

_provenance_checks复算数据/配置/源树身份及正式策略重放；main重算事件指标和多空CVaR，检查三个月切分、26列排除、1000随机基线、17官方事件。_notebook_artifact_checks检查执行与当前参数；_html_artifact_checks逐字重渲染对比。

## 与其他文件的关系

轻量demo只有JSON，直接运行会缺risk_features.parquet；历史validation_report全true不能代替当前目录检查。脚本含固定日期/月份与35品种口径，泛化到新样本需调整验收合同，而非把硬编码当模型规律。

## 函数与责任定位

|函数/类|源位置|要理解的职责|
|---|---|---|
|`_html_artifact_checks`|[40](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/validate_outputs.py:40>)|用当前渲染器逐字比较交付HTML|
|`_notebook_artifact_checks`|[81](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/validate_outputs.py:81>)|核对Notebook存在、执行、无错误、参数与指标|
|`_close`|[150](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/validate_outputs.py:150>)|生成close这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_cvar95`|[158](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/validate_outputs.py:158>)|取收益最差5%尾部均值的负号|
|`_discover_identity_inputs`|[164](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/validate_outputs.py:164>)|生成discover_identity_inputs这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_build_parser`|[175](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/validate_outputs.py:175>)|生成build_parser这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_usable_validation_data_root`|[194](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/validate_outputs.py:194>)|生成usable_validation_data_root这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_select_validation_data_root`|[201](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/validate_outputs.py:201>)|依显式路径、项目演示目录、旧身份根选择输入|
|`_agent_policy_identity_complete`|[228](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/validate_outputs.py:228>)|生成agent_policy_identity_complete这一局部报告/验证结构，按名称在完整源码中展开其字段与断言|
|`_provenance_checks`|[253](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/validate_outputs.py:253>)|重算数据/代码/配置身份并重放状态机|
|`main`|[337](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/validate_outputs.py:337>)|解析参数、调用本文件主业务并处理输出|

## 面试自测

如果上游证据缺失或过期，本脚本应生成一份看似完整的新成绩吗？

> [!success]- 答案
> 不应。先核查输入与身份；报告只整理已有证据，验收脚本必须明确拒绝不完整产物。脚本成功生成HTML也不意味着重新训练过模型。
