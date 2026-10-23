---
类型: 源码教学
源文件: "/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py"
阅读方式: 实际完整源码与函数核对
---

> [!info] 在项目里的职责
> 这里的“推理”是按注册规则找到固定四节点三条边的链，检查来源后构造成RiskPath并排序。没有神经网络参数、图嵌入、传播概率或因果学习。

源码入口：[src/option_risk/graph_reasoner.py 第1行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py:1>)。本篇依据最终提交目录，源码保持只读；完整逐字源码由知识库档案区保存，本篇聚焦如何理解和讲解。

## 输入、输出和上下游

MultiDiGraph或node-link字典 → RiskPath列表；再组合为KnowledgeGraphResult并构建固定查询索引。

直接导入模块：`__future__`, `collections.abc`, `copy`, `math`, `typing`, `networkx`, `pandas`, `.contracts`, `.knowledge_graph`, `.knowledge_schema`。


## 一项市场异常为何可能产生两条路径

例如ATM压力1.2且原等级1：

- Evidence→Anomaly→Mechanism→RiskConsequence，讲可能的风险维度。
- 同样前三节点→WarningState，说明当前市场证据支持原状态。

两条路径共享前三节点和前两条边，但结论与path_id不同；不是两个独立异常事件。质量项只产生到ConfidenceState的路径，永远不产生正式预警支持链。

`discover_risk_paths`没有调用最短路径或全路径算法。它遍历FEATURE_RULES，逐层找唯一匹配节点，再找精确关系边。固定三跳的好处是可复核、没有循环爆炸；代价是无法自动发现未知机制或跨品种传播。

## 为什么排序要完全确定

先市场后质量，之后严重度降序、有限压力优先/降序、规则order、后果优先预警、最后path_id。市场证据排在质量前不会抹掉质量：完整查询可保留，限制段也说明置信度。排序是展示政策，不是“因果概率”。同输入但排列浮动会使缓存审计、Notebook快照与评委复核难以比较，因此有明确并列规则。

问：为什么root_evidence不等于active_paths前三条？答：root_evidence沿排序路径保序去重Evidence；主图则直接取前三路径，因此主图可能只出现两项不同指标。

## 逐个类与函数查阅

每个锚点都指向当前源文件的实际定义。嵌套函数属于所在外层算法；`self`表示实例状态，不是额外业务输入。

### `_nodes_for_feature` · 43—54行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py:43>)。按节点类型和feature_name筛当前图节点。

输入/输出接口：`(graph: nx.MultiDiGraph, *, node_type: NodeType, feature_name: str)` → `list[str]`。

### `_one_feature_node` · 57—72行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py:57>)。每特征每层最多一个，缺失可None、重复拒绝。

输入/输出接口：`(graph: nx.MultiDiGraph, *, node_type: NodeType, feature_name: str)` → `str | None`。

### `_state_node` · 75—85行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py:75>)。WarningState/ConfidenceState必须唯一。

输入/输出接口：`(graph: nx.MultiDiGraph, node_type: NodeType)` → `str`。

### `_checked_edge` · 88—126行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py:88>)。只允许登记关系，核对边ID、规则、版本、时间及端点品种。

输入/输出接口：`(graph: nx.MultiDiGraph, source: str, target: str, *, allowed_relations: set[str], rule: FeatureRule, product: str, timestamp: pd.Timestamp, optional: bool=False)` → `tuple[str, str] | None`。

### `_check_node_chain` · 129—164行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py:129>)。校验四层类型、同品种同事件、相同特征/规则及后果身份。

输入/输出接口：`(graph: nx.MultiDiGraph, node_ids: tuple[str, str, str, str], *, terminal_type: NodeType, rule: FeatureRule, product: str, timestamp: pd.Timestamp)` → `None`。

### `_terminal_code` · 167—178行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py:167>)。按市场后果/原预警/置信结论确定末端身份码。

输入/输出接口：`(graph: nx.MultiDiGraph, terminal_node_id: str, terminal_type: NodeType, rule: FeatureRule)` → `str`。

### `_make_path` · 181—232行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py:181>)。把已验证四结点三边装成RiskPath，ID含品种、时间、特征与末端。

输入/输出接口：`(graph: nx.MultiDiGraph, *, rule: FeatureRule, evidence_id: str, anomaly_id: str, mechanism_id: str, conclusion_id: str, terminal_type: NodeType, edge_parts: tuple[tuple[str, str], tuple[str, str], tuple[str, str]])` → `RiskPath`。

### `discover_risk_paths` · 235—372行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py:235>)。遍历十二规则而非任意图搜索；质量只到置信，市场到后果并可到原预警。

输入/输出接口：`(graph: nx.MultiDiGraph | Mapping[str, Any])` → `list[RiskPath]`。

### `_path_rule` · 375—378行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py:375>)。每条路径必须带唯一注册规则ID。

输入/输出接口：`(path: RiskPath)` → `FeatureRule`。

### `_terminal_order` · 381—388行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py:381>)。对后果/预警/置信末端给稳定次序。

输入/输出接口：`(path: RiskPath)` → `int`。

### `rank_risk_paths` · 391—419行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py:391>)。市场先于质量，再按严重度、有限压力降序、规则顺序、末端与ID排序。

输入/输出接口：`(paths: Sequence[RiskPath])` → `list[RiskPath]`。

### `rank_risk_paths.key` · 395—417行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py:395>)。排序键没有概率含义，最后ID打破并列保证确定性。

输入/输出接口：`(path: RiskPath)` → `tuple[Any, ...]`。

### `_unique` · 422—423行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py:422>)。保序去重。

输入/输出接口：`(values: Iterable[str])` → `tuple[str, ...]`。

### `_build_query_index` · 426—458行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py:426>)。由规范路径重建根证据、预警、后果、质量和异常→路径索引。

输入/输出接口：`(graph: nx.MultiDiGraph, paths: Sequence[RiskPath])` → `dict[str, Any]`。

### `build_graph_result` · 461—521行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py:461>)。重新发现路径，验解释引用、缺证据类型，封装JSON图、计数与索引。

输入/输出接口：`(graph: nx.MultiDiGraph, *, missing_evidence, explanation_sections=(), explanation_text='', explanation_confidence='normal')` → `KnowledgeGraphResult`。

## 面试先讲清楚这一问

**问：排序最高代表因果可能性最大吗？**

答：不代表。排序优先市场路径，再按特征严重度、压力、注册顺序和稳定ID，属于展示与审计排序。

继续学习：[[20 - Agent如何把一次请求变成可复核风险判断]] → [[21 - 动态知识图谱的机制与推理边界]] → [[22 - 可追溯、防未来与运行身份]] → [[23 - 界面、真实案例与35品种验收]]。
