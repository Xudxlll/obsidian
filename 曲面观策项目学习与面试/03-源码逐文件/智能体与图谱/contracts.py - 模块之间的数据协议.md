---
类型: 源码教学
源文件: "/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py"
阅读方式: 实际完整源码与函数核对
---

> [!info] 在项目里的职责
> 一组冻结dataclass规定业务模块交接的字段和类型。数据协议把“某个函数返回一个字典”变成可审计的明确对象；它不计算波动率，也不证明输入数值真实。

源码入口：[src/option_risk/contracts.py 第1行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:1>)。本篇依据最终提交目录，源码保持只读；完整逐字源码由知识库档案区保存，本篇聚焦如何理解和讲解。

## 输入、输出和上下游

Python对象 ↔ JSON可序列化字典；AgentResult包住曲面、证据、原因、时间轴、评估和KnowledgeGraphResult。

直接导入模块：`__future__`, `dataclasses`, `pathlib`, `typing`, `numpy`, `pandas`。


## 最关键的三层协议

| 层 | 交接对象 | 读者应能解释的字段 |
|---|---|---|
| 数值与决策 | FeatureEvidence / TriggerReason / SurfacePayload | 当前值和历史参考不是同一个数；严重度、最终等级、通知脉冲不同；矩阵行对应期限列对应log-moneyness |
| 图谱内部解释 | RiskPath / ExplanationSection | 路径存精确节点与边ID；段落存引用path_ids，确保文字能回到数值证据 |
| 业务总输出 | AgentResult / KnowledgeGraphResult | status表示是否可用；alert_level表示风险；evaluation.available表示是否有离线结果，三者语义不能混用 |

`AgentResult.from_dict`会做 `bool(...)`、`int(...)`、`str(...)`转换，因此不能直接作为外部数据的严格验证器。例如字符串 `"false"` 转bool会得到True。Agent先查原始JSON形状和类型，图谱序列化恢复还进行独立预检，正式验证也直接检查冻结对象而不依赖可能“修复”数据的 `to_dict`。

`_json_ready`将非有限值转None有利于图表空白与标准JSON输出；与之不同，图谱/验收审计宁可抛错，也不允许先规范化后掩盖坏数值。理解这两个边界比背dataclass语法更重要。

## 一个协议样例

某证据 `current_value=0.30`、`reference_value=0.25`、`pressure_ratio=1.20`，`change_rate=-0.02`。它表示相对历史参考仍偏高，但比上一时点下降2%。“异常”和“正在上升”是两回事，面试时不要把超过阈值说成一定继续上升。

## 逐个类与函数查阅

每个锚点都指向当前源文件的实际定义。嵌套函数属于所在外层算法；`self`表示实例状态，不是额外业务输入。

### `_json_ready` · 11—31行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:11>)。统一Timestamp/NumPy/数组/时间轴/Path格式；非有限浮点转None，适合展示导出，不能代替严格审计。

输入/输出接口：`(value: Any)` → `Any`。

### `ProductOption` · 35—39行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:35>)。目录下拉数据：code,label与可选覆盖月份。

输入/输出接口：类；字段：`code`, `label`, `start`, `end`。

### `TriggerReason` · 43—51行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:43>)。前三触发说明：指标、当前/参考/压力、方向、严重度与消息。

输入/输出接口：类；字段：`feature_name`, `label`, `current_value`, `reference_value`, `pressure_ratio`, `change_direction`, `severity`, `message`。

### `FeatureEvidence` · 55—63行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:55>)。完整证据：组名、指标、当前/参考/压力/变化率/状态。

输入/输出接口：类；字段：`group`, `feature_name`, `label`, `current_value`, `reference_value`, `pressure_ratio`, `change_rate`, `status`。

### `SurfacePayload` · 67—85行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:67>)。一张曲面的轴和矩阵；values形状为(期限数,log-moneyness数)。

输入/输出接口：类；字段：`metric`, `timestamp`, `log_moneyness`, `time_to_expiry`, `values`。

### `SurfacePayload.to_dict` · 74—75行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:74>)。asdict后按_json_ready做递归JSON导出。

输入/输出接口：`(self)` → `dict[str, Any]`。

### `SurfacePayload.from_dict` · 78—85行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:78>)。从字典重建相应dataclass/数组/Timestamp；会强制转换部分类型，严格入口须先预检。

输入/输出接口：`(cls, payload: dict[str, Any])` → `'SurfacePayload'`。

### `EvaluationResult` · 89—100行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:89>)。available/status/metrics区分是否已有离线回测。

输入/输出接口：类；字段：`available`, `status`, `metrics`。

### `EvaluationResult.from_dict` · 95—100行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:95>)。从字典重建相应dataclass/数组/Timestamp；会强制转换部分类型，严格入口须先预检。

输入/输出接口：`(cls, payload: dict[str, Any])` → `'EvaluationResult'`。

### `GraphNodeRecord` · 104—120行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:104>)。通用节点记录协议：ID、类型、标签和属性。

输入/输出接口：类；字段：`node_id`, `node_type`, `label`, `properties`。

### `GraphNodeRecord.to_dict` · 110—111行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:110>)。asdict后按_json_ready做递归JSON导出。

输入/输出接口：`(self)` → `dict[str, Any]`。

### `GraphNodeRecord.from_dict` · 114—120行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:114>)。从字典重建相应dataclass/数组/Timestamp；会强制转换部分类型，严格入口须先预检。

输入/输出接口：`(cls, payload: dict[str, Any])` → `'GraphNodeRecord'`。

### `GraphEdgeRecord` · 124—142行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:124>)。通用边记录协议：端点、关系、ID与属性。

输入/输出接口：类；字段：`edge_id`, `source_node_id`, `target_node_id`, `relation_type`, `properties`。

### `GraphEdgeRecord.to_dict` · 131—132行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:131>)。asdict后按_json_ready做递归JSON导出。

输入/输出接口：`(self)` → `dict[str, Any]`。

### `GraphEdgeRecord.from_dict` · 135—142行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:135>)。从字典重建相应dataclass/数组/Timestamp；会强制转换部分类型，严格入口须先预检。

输入/输出接口：`(cls, payload: dict[str, Any])` → `'GraphEdgeRecord'`。

### `RiskPath` · 146—182行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:146>)。活动四层路径的节点ID、三条边、压力、严重度、关系语义、规则和时间。

输入/输出接口：类；字段：`path_id`, `evidence_node_id`, `anomaly_node_id`, `mechanism_node_id`, `conclusion_node_id`, `edge_ids`, `pressure_ratio`, `severity`, `relation_semantics`, `rule_ids`, `timestamp`。

### `RiskPath.to_dict` · 159—160行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:159>)。asdict后按_json_ready做递归JSON导出。

输入/输出接口：`(self)` → `dict[str, Any]`。

### `RiskPath.from_dict` · 163—182行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:163>)。从字典重建相应dataclass/数组/Timestamp；会强制转换部分类型，严格入口须先预检。

输入/输出接口：`(cls, payload: dict[str, Any])` → `'RiskPath'`。

### `ExplanationSection` · 186—202行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:186>)。固定解释段落的ID、标题、正文与被引用的path_ids。

输入/输出接口：类；字段：`section_id`, `title`, `content`, `path_ids`。

### `ExplanationSection.to_dict` · 192—193行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:192>)。asdict后按_json_ready做递归JSON导出。

输入/输出接口：`(self)` → `dict[str, Any]`。

### `ExplanationSection.from_dict` · 196—202行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:196>)。从字典重建相应dataclass/数组/Timestamp；会强制转换部分类型，严格入口须先预检。

输入/输出接口：`(cls, payload: dict[str, Any])` → `'ExplanationSection'`。

### `KnowledgeGraphResult` · 206—296行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:206>)。图谱结果信封，包含图、路径、索引、五段解释、缺证据及错误状态。

输入/输出接口：类；字段：`status`, `schema_version`, `rule_version`, `product`, `timestamp`, `graph_json`, `node_count`, `edge_count`, `active_path_count`, `active_paths`, `root_evidence`, `possible_consequences`, `explanation_sections`, `explanation_text`, `explanation_confidence`, `missing_evidence`, `query_index`, `error_type`, `error_message`。

### `KnowledgeGraphResult.to_dict` · 227—228行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:227>)。asdict后按_json_ready做递归JSON导出。

输入/输出接口：`(self)` → `dict[str, Any]`。

### `KnowledgeGraphResult.from_dict` · 231—269行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:231>)。从字典重建相应dataclass/数组/Timestamp；会强制转换部分类型，严格入口须先预检。

输入/输出接口：`(cls, payload: dict[str, Any])` → `'KnowledgeGraphResult'`。

### `KnowledgeGraphResult.unavailable` · 272—296行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:272>)。构造有品种、时点和错误原因的图谱降级结果，不伪造空图成功。

输入/输出接口：`(cls, *, product: str, timestamp: pd.Timestamp | str, error_type: str | None=None, error_message: str | None=None, schema_version: str='kg-schema-v1', rule_version: str='kg-rule-v1')` → `'KnowledgeGraphResult'`。

### `AgentResult` · 300—383行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:300>)。总结果信封，既带问题1证据/曲面，也可附问题2图谱和离线评估。

输入/输出接口：类；字段：`product`, `timestamp`, `status`, `alert_level`, `alert_name`, `alert_emitted`, `risk_score`, `price_source`, `data_quality`, `surfaces`, `feature_evidence`, `trigger_reasons`, `timeline`, `evaluation`, `policy_version`, `policy_parameter_hash`, `transition_reason`, `knowledge_graph`。

### `AgentResult.to_dict` · 320—322行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:320>)。asdict后按_json_ready做递归JSON导出。

输入/输出接口：`(self)` → `dict[str, Any]`。

### `AgentResult.from_dict` · 325—383行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py:325>)。从字典重建相应dataclass/数组/Timestamp；会强制转换部分类型，严格入口须先预检。

输入/输出接口：`(cls, payload: dict[str, Any])` → `'AgentResult'`。

## 面试先讲清楚这一问

**问：frozen=True是否彻底不可变？**

答：仅阻止字段重新赋值；字段里的dict、list、ndarray仍可被改，查询服务用deepcopy保护返回副本。

继续学习：[[20 - Agent如何把一次请求变成可复核风险判断]] → [[21 - 动态知识图谱的机制与推理边界]] → [[22 - 可追溯、防未来与运行身份]] → [[23 - 界面、真实案例与35品种验收]]。
