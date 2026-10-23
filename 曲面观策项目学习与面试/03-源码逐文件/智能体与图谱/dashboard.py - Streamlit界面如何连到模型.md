---
类型: 源码教学
源文件: "/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py"
阅读方式: 实际完整源码与函数核对
---

> [!info] 在项目里的职责
> 唯一业务界面让用户从真实目录选择品种与有效时间，点击后调用一次agent.analyze；六页签展示同一AgentResult。图谱显示前会重新校验路径、解释和问题1状态。

源码入口：[src/option_risk/dashboard.py 第1行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:1>)。本篇依据最终提交目录，源码保持只读；完整逐字源码由知识库档案区保存，本篇聚焦如何理解和讲解。

## 输入、输出和上下游

用户选择 + OptionRiskAgent → Streamlit组件；内部没有训练、风险阈值调参，也没有自由文本问答。

直接导入模块：`__future__`, `os`, `dataclasses`, `pathlib`, `pandas`, `streamlit`, `option_risk.agent`, `option_risk.config`, `option_risk.contracts`, `option_risk.errors`, `option_risk.graph_queries`, `option_risk.graph_visualization`, `option_risk.graph_explanation`, `option_risk.knowledge_graph`, `option_risk.knowledge_schema`, `option_risk.interactive`。


## 一次会话的状态边界

Streamlit交互会重运行页面。Agent资源按会话缓存，`agent_result`存已计算结果；只有点按钮才调用分析。切品种时递增selection_generation，清掉旧结果和图谱选择，使新的时间下拉无法沿用旧品种选项。图节点选择key包含品种和时点，节点详情再走精确查询，过期ID只提示，不显示旧事件。

`_validated_graph_view`先检查结构与路径，又重新生成解释，最后把WarningState与AgentResult的品种/时点/等级/通知/分数/迁移/哈希逐项比较。界面没有权力把图谱文字改为另一种市场结论。

## 用户能看到的六个视角

Agent决策回答当前状态与理由；图谱回答登记证据路径；曲面回答风险如何随价内外与期限分布；特征表给精确值；时间轴显示过去状态；离线回测展示已存在的评估。这六页都属于同一业务结果，不是六个模型。

风险分数不是预测概率，清洗有效率不是预测精度，期限数不是节点数，回测CVaR改善不是Agent的减仓建议。没有离线结果的品种仍可点时分析，页面显示“未生成”，不捏造指标。

## 静态阅读与真实界面验证

本篇从源码核对结构；静态存在六个页签不等于已在当前机器浏览器逐一验证布局、交互与下载。当前交付设计文档的浏览器QA声明属于原交付记录，需与本次复现证据分开。

## 逐个类与函数查阅

每个锚点都指向当前源文件的实际定义。嵌套函数属于所在外层算法；`self`表示实例状态，不是额外业务输入。

### `_agent_from_environment` · 40—53行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:40>)。按会话缓存资源实例化唯一Agent，路径变化会构成新资源键。

输入/输出接口：`(data_source: str, cache_dir: str, output_dir: str, archive_path: str)` → `OptionRiskAgent`。

### `_runtime_paths` · 56—63行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:56>)。从四个环境变量取数据/缓存/输出/压缩包位置，否则用本地默认。

输入/输出接口：`()` → `tuple[str, str, str, str]`。

### `_styles` · 66—82行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:66>)。注入卡片、理由条和指标样式。

输入/输出接口：`()` → `None`。

### `_render_summary` · 85—104行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:85>)。渲染等级、分数、清洗率、期限数、价格来源并明确代理价格限制。

输入/输出接口：`(result: AgentResult)` → `None`。

### `_render_decision` · 107—120行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:107>)。显示正式原因、策略审计和本时点是否新发通知。

输入/输出接口：`(result: AgentResult)` → `None`。

### `_render_surfaces` · 123—130行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:123>)。同一结果画IV曲面、IV热力、期限微笑与Greeks。

输入/输出接口：`(result: AgentResult)` → `None`。

### `_feature_column_config` · 133—139行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:133>)。数值精度和变化率的表格显示配置。

输入/输出接口：`()` → `dict[str, object]`。

### `_render_features` · 142—164行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:142>)。把FeatureEvidence列转中文，按压力降序显示完整证据。

输入/输出接口：`(result: AgentResult)` → `None`。

### `_render_evaluation` · 167—192行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:167>)。只展示已有离线指标，提示固定样本外区间及CVaR探索限制。

输入/输出接口：`(result: AgentResult)` → `None`。

### `_preset_query_rows` · 195—213行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:195>)。将六个固定中文问题精确映射到只读查询/规范路径视图。

输入/输出接口：`(service: GraphQueryService, graph_result, label: str)` → `list[dict[str, object]]`。

### `_selected_node_detail` · 216—222行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:216>)。精确节点查询，未知/过期节点返回None。

输入/输出接口：`(service: GraphQueryService, selected_node_id: object)` → `dict[str, object] | None`。

### `_selection_node_id` · 225—236行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:225>)。兼容Plotly选择返回对象/字典，从customdata提取节点ID。

输入/输出接口：`(selection: object)` → `object`。

### `_validated_graph_view` · 239—272行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:239>)。复验查询服务、重渲染解释，再逐字段对照图谱WarningState与AgentResult。

输入/输出接口：`(graph_result, result: AgentResult)`。

### `_render_knowledge_graph` · 275—336行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:275>)。图谱失败给提示；成功显示五段解释、前三路径、选点审计和固定查询。

输入/输出接口：`(result: AgentResult)` → `None`。

### `_render_result` · 339—365行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:339>)。把同一结果分到六个页签。

输入/输出接口：`(result: AgentResult)` → `None`。

### `render_dashboard` · 368—442行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:368>)。目录下拉→切品种清会话→有效时点下拉→点击调用analyze→展示结果。

输入/输出接口：`(agent: OptionRiskAgent)` → `None`。

### `main` · 445—452行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py:445>)。配置页面并从运行路径创建Agent进入界面。

输入/输出接口：`()` → `None`。

## 面试先讲清楚这一问

**问：为什么切换品种要清状态？**

答：防止把旧品种结果、旧节点选中状态和新时点选项混在一起；session_state中按事件生成key，并清理旧图谱选择。

继续学习：[[20 - Agent如何把一次请求变成可复核风险判断]] → [[21 - 动态知识图谱的机制与推理边界]] → [[22 - 可追溯、防未来与运行身份]] → [[23 - 界面、真实案例与35品种验收]]。
