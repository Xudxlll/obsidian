---
类型: 源码教学
源文件: "/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py"
阅读方式: 实际完整源码与函数核对
---

> [!info] 在项目里的职责
> 给离线结果附上数据内容、源码、列模式、配置、策略参数、包版本和划分协议的指纹，并在验收时重新计算。它主要审计离线训练与评价身份，不是实时Agent本身的结果缓存算法。

源码入口：[src/option_risk/provenance.py 第1行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:1>)。本篇依据最终提交目录，源码保持只读；完整逐字源码由知识库档案区保存，本篇聚焦如何理解和讲解。

## 输入、输出和上下游

features/config/输入文件/策略/划分月份 → run_identity；已有summary与bundle → 布尔检查字典。pipeline生成，离线审计消费。

直接导入模块：`__future__`, `dataclasses`, `datetime`, `hashlib`, `importlib.metadata`, `json`, `math`, `pathlib`, `typing`, `numpy`, `pandas`, `.config`, `.decision`, `.features`。


## 两种“没有看未来”，对应两种风险

点时分析防未来要求 $X_t$ 只由不晚于 $t$ 的行情生成，动态历史阈值通过shift(1)只使用严格早于 $t$ 的特征行；逐列rolling按有效观测数量满足min_periods，代码没有先过滤data_ready=True快照。训练评价还须防止标签和测试期反向污染选模：校准结束早于测试月，测试标签不回流调参；若标签看未来 $H$ 个bar，靠近训练/验证和验证/测试边界的各 $H$ 行必须清除，保证标签窗口完全落在本划分内部。

例如训练最后一行在1月31日而标签用未来8bar，这些bar若已进入验证期，训练样本就带了验证期信息。仅按特征行时间划分仍会泄漏。`forward_label_boundary_purge`记录并核对两处各H行，而不是只写一句“按时间切分”。

## 为什么排除26列

12个pressure列依赖动态历史阈值，12个history_q95列是其参考，另有risk_pressure/core_risk_pressure两个合成分数。这26列与赛题事件定义联系很紧。正式模型要排除标签衍生捷径时，契约要求精确这26列，而不是只按某个前缀粗删。是否正确训练还要读model.py；本文件检查身份、列契约与诊断的一致。

## 指纹链如何帮助复查

相对文件路径+大小+内容SHA256 → 输入总指纹；源码相对路径+内容SHA256 → 源码树指纹；策略/配置用规范JSON哈希。搬整个项目不必因绝对路径改变身份，但文件内容、列顺序、参数任一变化可被检测。生成时间用UTC记录运行记录；它不应被当作市场数据的source_timestamp。

`fixed_holdout_checks`会检查诊断中的protocol字段和月份，避免主摘要写固定留出而消融/策略诊断仍在复用测试标签。应理解为可核对的审计约定，而不是只靠元数据便已证明所有历史代码没有违规。

## 逐个类与函数查阅

每个锚点都指向当前源文件的实际定义。嵌套函数属于所在外层算法；`self`表示实例状态，不是额外业务输入。

### `_json_value` · 43—60行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:43>)。规范化dataclass、集合、NumPy、路径和特殊浮点，形成稳定可哈希内容。

输入/输出接口：`(value: Any)` → `Any`。

### `_canonical_bytes` · 63—70行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:63>)。排序键、紧凑JSON、UTF-8生成规范字节串。

输入/输出接口：`(value: Any)` → `bytes`。

### `_sha256_json` · 73—74行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:73>)。对规范JSON字节计算SHA256。

输入/输出接口：`(value: Any)` → `str`。

### `_content_sha256` · 77—82行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:77>)。1MB分块读取文件算内容哈希，避免一次载入大文件。

输入/输出接口：`(path: Path)` → `str`。

### `_relative_name` · 85—97行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:85>)。要求输入位于声明根内，记录相对名以支持搬迁后身份比较。

输入/输出接口：`(path: Path, root: Path)` → `str`。

### `_input_file_identity` · 100—119行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:100>)。对相对路径、大小、内容哈希列表排序后形成输入总指纹。

输入/输出接口：`(input_files: Iterable[str | Path], input_root: str | Path)` → `dict[str, object]`。

### `_source_tree_identity` · 122—137行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:122>)。对源码树所有.py相对路径与内容哈希形成总指纹。

输入/输出接口：`(source_root: str | Path | None=None)` → `dict[str, object]`。

### `_package_version` · 140—149行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:140>)。优先安装元数据，再读pyproject版本。

输入/输出接口：`()` → `str`。

### `_feature_schema` · 152—165行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:152>)。记录有序特征列、12压力列、12历史列和26个标签衍生排除列。

输入/输出接口：`(features: pd.DataFrame)` → `dict[str, object]`。

### `_feature_contract_status` · 168—178行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:168>)。检查12+12+2契约精确存在且无重复。

输入/输出接口：`(features: pd.DataFrame)` → `tuple[bool, bool, bool]`。

### `decision_policy_parameter_sha256` · 181—187行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:181>)。优先复用DecisionPolicy.parameter_hash，否则规范化参数计算。

输入/输出接口：`(policy: DecisionPolicy)` → `str`。

### `_decision_policy_identity` · 190—200行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:190>)。记录预注册来源、版本、完整参数和哈希。

输入/输出接口：`(policy: DecisionPolicy)` → `dict[str, object]`。

### `pipeline_config_sha256` · 203—204行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:203>)。对PipelineConfig所有参数加类型标签后哈希。

输入/输出接口：`(config: PipelineConfig)` → `str`。

### `_forward_label_boundary_purge_contract` · 207—214行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:207>)。记录向前标签跨训练/验证和验证/测试边界的各horizon条清除约定。

输入/输出接口：`(horizon_bars: int)` → `dict[str, object]`。

### `build_run_identity` · 217—261行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:217>)。先验列契约与固定主策略，再建立数据/源码/配置/策略/划分/UTC时间完整身份。

输入/输出接口：`(*, features: pd.DataFrame, config: PipelineConfig, input_files: Iterable[str | Path], input_root: str | Path, policy: DecisionPolicy, calibration_end: str, test_start: str, test_end: str, fixed_holdout_no_test_label_reuse: bool, source_root: str | Path | None=None)` → `dict[str, object]`。

### `_is_utc_timestamp` · 264—269行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:264>)。确认生成时间明确带UTC时区。

输入/输出接口：`(value: object)` → `bool`。

### `run_identity_checks` · 272—368行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:272>)。重新算当前源码、输入和配置各身份，与既有离线artifact逐项比对。

输入/输出接口：`(identity: Mapping[str, object] | None, *, features: pd.DataFrame, config: PipelineConfig, input_files: Iterable[str | Path], input_root: str | Path, policy: DecisionPolicy, source_root: str | Path | None=None)` → `dict[str, bool]`。

### `replay_decision_policy_checks` · 371—418行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:371>)。重放正式策略，精确比索引、等级、通知、版本与哈希。

输入/输出接口：`(features: pd.DataFrame, warnings: pd.DataFrame, policy: DecisionPolicy)` → `dict[str, bool]`。

### `_month` · 421—427行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:421>)。把月份字符串转换Period，不合法返回None。

输入/输出接口：`(value: object)` → `pd.Period | None`。

### `_diagnostic_protocol_checks` · 430—441行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:430>)。检查每个诊断都声明固定留出且校准月早于测试开始。

输入/输出接口：`(diagnostics: object, test_start: pd.Period | None)` → `tuple[bool, bool]`。

### `_boundary_purge_matches_horizon` · 444—454行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:444>)。三个划分诊断中的清除策略/行数必须与horizon一致。

输入/输出接口：`(diagnostics: Mapping[str, object], horizon: int)` → `bool`。

### `fixed_holdout_checks` · 457—561行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py:457>)。交叉比summary和model bundle，确认前置校准、主策略身份、无测试标签复用与边界清除。

输入/输出接口：`(summary: Mapping[str, object], bundle: object)` → `dict[str, bool]`。

## 面试先讲清楚这一问

**问：哈希证明策略有效吗？**

答：哈希证明被比较对象身份一致；有效性仍需恰当标签、严格样本外评价及真实市场检验。

继续学习：[[20 - Agent如何把一次请求变成可复核风险判断]] → [[21 - 动态知识图谱的机制与推理边界]] → [[22 - 可追溯、防未来与运行身份]] → [[23 - 界面、真实案例与35品种验收]]。
