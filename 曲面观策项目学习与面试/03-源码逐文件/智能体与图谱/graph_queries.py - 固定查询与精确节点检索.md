---
类型: 源码教学
源文件: "/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py"
阅读方式: 实际完整源码与函数核对
---

> [!info] 在项目里的职责
> 把已验证图谱包装成六类只读查询。构造服务时恢复原图、重新发现规范路径、校验计数/索引/版本；查询不是把用户自然语言交给LLM，也不是开放式图搜索。

源码入口：[src/option_risk/graph_queries.py 第1行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py:1>)。本篇依据最终提交目录，源码保持只读；完整逐字源码由知识库档案区保存，本篇聚焦如何理解和讲解。

## 输入、输出和上下游

ready KnowledgeGraphResult → 节点记录或路径字典列表；返回deepcopy，未知精确ID抛UnknownGraphNodeError。

直接导入模块：`__future__`, `copy`, `pandas`, `.contracts`, `.graph_reasoner`, `.knowledge_graph`, `.knowledge_schema`。


## 六个接口的语义不要混

| 接口 | 返回 | 空结果如何理解 |
|---|---|---|
| root_evidence(limit=3) | 排序去重的活动证据节点 | 当前无活动证据，不等于原始12项证据不存在 |
| paths_to_alert() | 终点为原WarningState的路径 | 0级、或只有质量/持续性状态时可为空 |
| possible_consequences() | 市场后果节点 | 质量不是市场后果 |
| quality_limitations() | 置信限制路径 | 当前无已激活质量项，不保证数据完美 |
| inspect_node(node_id) | 当前图精确节点 | 未知ID抛错，不猜名字 |
| paths_from_anomaly(anomaly_id) | 通过该异常的全部规范链 | 必须是当前图的Anomaly ID |

界面中文“为什么是当前等级”只是一个预设标签，实际调 `paths_to_alert()`。它展示的是规则支持链，不是反事实归因、SHAP贡献分解或自动因果解释。用户不能随便问“央行政策为什么导致白银上涨”并得到答案。

例如查 `evidence:ag:20250407T101500:atm_iv`，服务只有在该图里真有此ID时才返回；对另一时点同名指标，需要另一个事件的精确ID。所有返回深拷贝，调用者把压力改成99不会污染下次查询。

## 逐个类与函数查阅

每个锚点都指向当前源文件的实际定义。嵌套函数属于所在外层算法；`self`表示实例状态，不是额外业务输入。

### `UnknownGraphNodeError` · 18—19行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py:18>)。未知或类型错误的精确节点查询异常。

输入/输出接口：类；共享配置/方法边界。

### `_unique` · 22—23行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py:22>)。保序去重节点ID。

输入/输出接口：`(values)`。

### `_same_exact_json_structure` · 26—39行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py:26>)。递归比较值及原生容器类型，防类型相容但协议不等价。

输入/输出接口：`(actual, expected)`。

### `GraphQueryService` · 42—189行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py:42>)。固定只读查询门面，初始化即验证全图与规范路径。

输入/输出接口：类；共享配置/方法边界。

### `GraphQueryService.__init__` · 45—139行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py:45>)。验证ready身份，独立重算路径、根/后果、解释引用与query_index，构建内存只读视图。

输入/输出接口：`(self, result: KnowledgeGraphResult)` → `None`。

### `GraphQueryService._node_copy` · 141—142行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py:141>)。深拷贝节点，调用者修改不污染服务。

输入/输出接口：`(self, node_id)`。

### `GraphQueryService._path_copies` · 144—145行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py:144>)。把路径协议转字典并深拷贝。

输入/输出接口：`(self, paths)`。

### `GraphQueryService.root_evidence` · 147—152行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py:147>)。按规范排序取去重根证据，limit必须为非负原生int。

输入/输出接口：`(self, limit=3)`。

### `GraphQueryService.paths_to_alert` · 154—160行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py:154>)。只返回结论节点为WarningState的支持路径。

输入/输出接口：`(self)`。

### `GraphQueryService.possible_consequences` · 162—163行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py:162>)。返回去重的RiskConsequence节点，不把ConfidenceState算市场后果。

输入/输出接口：`(self)`。

### `GraphQueryService.quality_limitations` · 165—171行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py:165>)。只返回终点ConfidenceState的质量链。

输入/输出接口：`(self)`。

### `GraphQueryService.inspect_node` · 173—176行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py:173>)。只接受当前事件图中存在的精确ID。

输入/输出接口：`(self, node_id)`。

### `GraphQueryService.paths_from_anomaly` · 178—189行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_queries.py:178>)。只接受当前图的Anomaly精确ID，返回含该异常的规范路径。

输入/输出接口：`(self, anomaly_id)`。

## 面试先讲清楚这一问

**问：为什么不直接相信query_index？**

答：外部JSON与缓存可能被篡改；服务按图重建索引再严格比较，不把一份自称一致的缓存当作证据。

继续学习：[[曲面观策项目学习与面试/02-循序学习/20 - Agent如何把一次请求变成可复核风险判断.md|20 - Agent如何把一次请求变成可复核风险判断]] → [[曲面观策项目学习与面试/02-循序学习/21 - 动态知识图谱的机制与推理边界.md|21 - 动态知识图谱的机制与推理边界]] → [[曲面观策项目学习与面试/02-循序学习/22 - 可追溯、防未来与运行身份.md|22 - 可追溯、防未来与运行身份]] → [[曲面观策项目学习与面试/02-循序学习/23 - 界面、真实案例与35品种验收.md|23 - 界面、真实案例与35品种验收]]。
