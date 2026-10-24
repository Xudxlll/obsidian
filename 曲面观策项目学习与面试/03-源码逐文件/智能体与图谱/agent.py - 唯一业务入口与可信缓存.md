---
类型: 源码教学
源文件: "/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py"
阅读方式: 实际完整源码与函数核对
---

> [!info] 在项目里的职责
> 把选品种、校验时点、读取过去数据、清洗、节点构建、特征、决策、五张曲面、图谱与离线评估组织成一个 AgentResult。这里的Agent是确定性的业务编排对象，没有大模型调用、提示词、工具自主规划或多智能体协作。

源码入口：[src/option_risk/agent.py 第1行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:1>)。本篇依据最终提交目录，源码保持只读；完整逐字源码由知识库档案区保存，本篇聚焦如何理解和讲解。

## 输入、输出和上下游

输入 product 与 timestamp，加 AgentConfig 指定的数据/缓存/离线结果目录；输出 AgentResult。上下游：dashboard/cli/Notebook → agent → catalog/io/quality/surfaces/features/decision → 图谱 → 缓存。

直接导入模块：`__future__`, `dataclasses`, `gzip`, `hashlib`, `json`, `math`, `os`, `pathlib`, `tempfile`, `numpy`, `pandas`, `.catalog`, `.config`, `.contracts`, `.decision`, `.errors`, `.features`, `.graph_explanation`, `.graph_queries`, `.graph_reasoner`, `.io`, `.knowledge_graph`, `.knowledge_schema`, `.quality`, `.surfaces`。


## 从一次点击追到每一步数据

阅读 `analyze`（1187—1283行），把每一步当作接口，而不是记住长文件：

1. 规范品种、Timestamp，并用目录验证合法请求。合法请求来自数据能力，不靠输入字符串格式就算合法。
2. 取预注册决策策略，计算结果缓存键。若缓存问题1仍可信，可复用昂贵的曲面；但离线回测摘要每次刷新，旧图谱也会重新校验或升级。
3. 未命中时，读所选时点往前的日历窗口，先按月份选文件，再用 `raw.datetime <= timestamp` 精确截断（1235行）。仅指定 `end_date` 不够，因为同一天仍可能存在更晚bar。
4. 清洗 → 合约汇成节点 → 提取特征 → `assess_features`重放历史状态。Agent本身不拟合分类器。
5. 对IV/Delta/Gamma/Vega/Theta生成曲面，期限从天数除365转年；曲面矩阵和坐标进入SurfacePayload。
6. 先创建问题1 `AgentResult`，其中价格来源明确是 `reconstructed_proxy`。再附图谱；最后通过强校验原子写缓存。

### 为什么前半文件几乎都在查缓存

缓存是外部持久化边界。JSON能解析不等于可信：`True`可能混成1、NaN可能掩盖缺失、旧规则可能留在新图里、同品种另一个时间可能混入。缓存前置函数分别核对原生类型、容器、证据顺序、曲面轴形状、触发文本、策略版本和时间轴重放。它们做的是一致性保护，不能证明原行情真实无误。

特别注意 `_timeline_replay_matches`：对最后512行的状态重放，需要考虑窗口开始之前已经进入关注/警告/危险的情况，因此枚举有限前缀。它没有原始完整历史，历史危险的独立信号由已记录状态推定；这是缓存自洽检查，强度不同于对原行情重新完整计算。当前时点的市场压力会再用真实FeatureEvidence核对。

## 能自己手工走的例子

假设现有ag目录允许 `2025-04-07 10:15`。Agent先过滤到该时刻及以前，输出2级、`warning_held`、`alert_emitted=False`。这表示仍处于警告状态，此bar没有新发通知。图谱里的 `WarningState` 必须逐项复制这三个字段，不能因为某条解释很严重就自行改成3级。

## 阅读后的检查题

- 如果结果缓存可用但刚新增离线回测文件，是否会返回旧的evaluation？不会：1201—1205行刷新离线视图。
- 图谱校验失败会不会删去曲面？已确认的问题1可继续保留，图谱单独重建或降级；不是把图谱失败伪装成0级。
- 结果缓存是否是内容哈希？缓存键依赖catalog的元数据源指纹；离线provenance另有逐文件内容哈希，两者不能混称。

## 逐个类与函数查阅

每个锚点都指向当前源文件的实际定义。嵌套函数属于所在外层算法；`self`表示实例状态，不是额外业务输入。

### `_graph_cache_identity` · 59—66行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:59>)。图谱schema/rule版本与决策参数哈希共同定义缓存身份，防止换规则继续用旧图。

输入/输出接口：`(policy: DecisionPolicy)` → `dict[str, str]`。

### `_is_finite_number` · 98—107行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:98>)。严格排除bool，接受有限Python/NumPy数值；用于审计结果缓存。

输入/输出接口：`(value: object)` → `bool`。

### `_is_finite_number_or_none` · 110—111行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:110>)。在有限数之外允许None，表达证据不可用。

输入/输出接口：`(value: object)` → `bool`。

### `_is_strict_json_value` · 114—139行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:114>)。递归只允许标准内置JSON类型、有限float、字符串键与≤64层深度。

输入/输出接口：`(value: object, *, depth: int=0)` → `bool`。

### `_reject_json_constant` · 142—143行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:142>)。拒绝JSON中的NaN/Infinity特殊常量，不默默修复。

输入/输出接口：`(value: str)` → `object`。

### `_parse_finite_json_float` · 146—150行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:146>)。浮点字符串解析后再查有限性，挡住溢出成Infinity。

输入/输出接口：`(value: str)` → `float`。

### `_cache_payload_has_expected_shapes` · 153—195行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:153>)。from_dict之前预检容器形状，防止宽松恢复隐藏错误。

输入/输出接口：`(payload: object)` → `bool`。

### `_allowed_directions_from_evidence` · 198—235行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:198>)。由当前值与变化率反推允许方向，处理上期零值/缺失的歧义。

输入/输出接口：`(row: FeatureEvidence)` → `frozenset[str]`。

### `_trigger_reasons_are_canonical` · 238—304行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:238>)。根据压力重新排序前三触发原因，核对数值、方向、严重度与模板全文。

输入/输出接口：`(result: AgentResult, policy: DecisionPolicy)` → `bool`。

### `_is_valid_analytical_timeline_value` · 307—317行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:307>)。时间轴数值可缺失/NaN，但禁止bool与Infinity。

输入/输出接口：`(value: object)` → `bool`。

### `_current_cross_layer_facts_are_valid` · 320—368行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:320>)。把当前12项证据的最大/核心压力和危险条件与时间轴末行、顶层结果互相核对。

输入/输出接口：`(timeline: pd.DataFrame, result: AgentResult, policy: DecisionPolicy)` → `bool`。

### `_timeline_transition_sequence_is_valid` · 371—513行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:371>)。逐行查迁移原因、级别、通知、关注保持、冷却和释放是否有合法顺序。

输入/输出接口：`(timeline: pd.DataFrame, policy: DecisionPolicy)` → `bool`。

### `_timeline_replay_matches` · 516—610行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:516>)。利用时间轴重放状态机，枚举窗口之前可能存在的关注/警告/危险前缀，验证截尾时间轴可解释。

输入/输出接口：`(timeline: pd.DataFrame, result: AgentResult, policy: DecisionPolicy)` → `bool`。

### `_timeline_replay_matches.seed_row` · 559—570行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:559>)。嵌套辅助函数，构造状态机前缀的压力/ready行，不是追加市场训练样本。

输入/输出接口：`(core: float, risk: float, *, danger: bool=False)` → `dict[str, object]`。

### `_timeline_is_current` · 613—686行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:613>)。核对固定11列、唯一递增索引、末时点、策略哈希、迁移序列及重放结果。

输入/输出接口：`(timeline: object, result: AgentResult, *, timestamp: pd.Timestamp, policy: DecisionPolicy)` → `bool`。

### `OptionRiskAgent` · 689—1283行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:689>)。唯一公开业务Agent，职责见前述编排主线；以下逐个拆方法。

输入/输出接口：类；共享配置/方法边界。

### `OptionRiskAgent.__init__` · 694—697行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:694>)。保存AgentConfig，确保输出目录，创建数据目录服务。

输入/输出接口：`(self, config: AgentConfig)`。

### `OptionRiskAgent.list_products` · 699—700行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:699>)。委托catalog扫描真实品种。

输入/输出接口：`(self)` → `list[ProductOption]`。

### `OptionRiskAgent.list_timestamps` · 702—703行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:702>)。委托catalog返回可分析时点目录。

输入/输出接口：`(self, product: str)` → `pd.DatetimeIndex`。

### `OptionRiskAgent._validate_timestamp` · 705—708行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:705>)。确认请求时点属于该品种的有效下拉选项。

输入/输出接口：`(self, product: str, timestamp: pd.Timestamp)` → `None`。

### `OptionRiskAgent._result_cache_path` · 710—733行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:710>)。把源指纹、时点、窗口、管线配置、策略和图谱版本编码后哈希，生成gzip JSON位置。

输入/输出接口：`(self, product: str, timestamp: pd.Timestamp, policy: DecisionPolicy | None=None)` → `Path`。

### `OptionRiskAgent._timeline` · 736—758行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:736>)。先对完整过去视图重放状态机，之后才截最后512行，保留真实状态记忆。

输入/输出接口：`(features: pd.DataFrame, timestamp: pd.Timestamp, policy: DecisionPolicy)` → `pd.DataFrame`。

### `OptionRiskAgent._summary_payload` · 760—776行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:760>)。搜索run_summary.json并按品种过滤；找不到返回None。

输入/输出接口：`(self, product: str)` → `dict[str, object] | None`。

### `OptionRiskAgent._decision_policy` · 778—782行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:778>)。忽略品种参数，始终返回代码预注册的DecisionPolicy，不用测试标签选策略。

输入/输出接口：`(self, product: str)` → `DecisionPolicy`。

### `OptionRiskAgent._load_evaluation` · 784—800行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:784>)。把已有离线摘要包装成EvaluationResult，不现场训练或回测。

输入/输出接口：`(self, product: str)` → `EvaluationResult | None`。

### `OptionRiskAgent.get_evaluation` · 802—812行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:802>)。先验证品种，再返回离线结果或available=False。

输入/输出接口：`(self, product: str)` → `EvaluationResult`。

### `OptionRiskAgent._missing_graph_evidence` · 815—831行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:815>)。按注册表查哪些特征缺少有限当前值。

输入/输出接口：`(graph)` → `tuple[str, ...]`。

### `OptionRiskAgent._build_knowledge_graph_result` · 833—869行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:833>)。问题1→图→路径→解释→结果→查询复验；图或措辞错误降级为unavailable。

输入/输出接口：`(self, base_result: AgentResult, policy: DecisionPolicy)` → `KnowledgeGraphResult`。

### `OptionRiskAgent._graph_from_problem_one` · 872—890行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:872>)。逐字段把原等级、证据、策略、质量和价格来源送入构图器。

输入/输出接口：`(base_result: AgentResult, policy: DecisionPolicy)`。

### `OptionRiskAgent._attach_knowledge_graph` · 892—898行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:892>)。dataclasses.replace只附加knowledge_graph，不回写原决策。

输入/输出接口：`(self, base_result: AgentResult, policy: DecisionPolicy)` → `AgentResult`。

### `OptionRiskAgent._is_current_problem_one_cache` · 901—1025行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:901>)。严查类型、12项证据顺序、五曲面形状坐标、时间轴及规范原因。

输入/输出接口：`(result: object, *, product: str, timestamp: pd.Timestamp, policy: DecisionPolicy)` → `bool`。

### `OptionRiskAgent._validate_ready_graph_cache` · 1027—1076行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:1027>)。恢复缓存图，与当前问题1重新构图比较，再重算路径、解释和缺证据清单。

输入/输出接口：`(self, result: AgentResult, policy: DecisionPolicy, *, compare_problem_one: bool=True)` → `None`。

### `OptionRiskAgent._validate_publishable_result` · 1078—1114行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:1078>)。发布前验问题1身份；图谱ready需强校验，unavailable也需正确事件身份和错误字段。

输入/输出接口：`(self, result: AgentResult, *, product: str, timestamp: pd.Timestamp, policy: DecisionPolicy, compare_ready_to_problem_one: bool=True)` → `None`。

### `OptionRiskAgent._load_cached_result` · 1117—1139行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:1117>)。安全读取gzip JSON并恢复协议，坏缓存作为miss返回None。

输入/输出接口：`(cache_path: Path)` → `AgentResult | None`。

### `OptionRiskAgent._publish_result` · 1141—1185行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:1141>)。写同目录唯一临时文件，再os.replace原子发布；竞争权限异常时只接受可复验的已发布结果。

输入/输出接口：`(self, cache_path: Path, result: AgentResult, *, product: str, timestamp: pd.Timestamp, policy: DecisionPolicy)` → `AgentResult`。

### `OptionRiskAgent.analyze` · 1187—1283行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py:1187>)。业务总流程：校验请求→可信缓存→截断原始过去数据→清洗/节点/特征/决策/曲面→图谱→发布。

输入/输出接口：`(self, product: str, timestamp: pd.Timestamp | str)` → `AgentResult`。

## 面试先讲清楚这一问

**问：如果把图谱拿掉，预警会改变吗？**

答：不会。先生成问题1的正式结果，再用 replace 附加知识图谱；图谱失败时可返回 unavailable，问题1仍保留。

继续学习：[[曲面观策项目学习与面试/02-循序学习/20 - Agent如何把一次请求变成可复核风险判断.md|20 - Agent如何把一次请求变成可复核风险判断]] → [[曲面观策项目学习与面试/02-循序学习/21 - 动态知识图谱的机制与推理边界.md|21 - 动态知识图谱的机制与推理边界]] → [[曲面观策项目学习与面试/02-循序学习/22 - 可追溯、防未来与运行身份.md|22 - 可追溯、防未来与运行身份]] → [[曲面观策项目学习与面试/02-循序学习/23 - 界面、真实案例与35品种验收.md|23 - 界面、真实案例与35品种验收]]。
