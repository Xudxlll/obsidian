---
类型: 源码教学
源文件: "/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py"
阅读方式: 实际完整源码与函数核对
---

> [!info] 在项目里的职责
> 问题1验响应完整性，问题2进一步独立重算图、路径、索引、解释并与问题1逐项对照；部署验收逐品种选最新有效时点，再做确定性、无未来、措辞安全全局检查。

源码入口：[src/option_risk/validation.py 第1行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:1>)。本篇依据最终提交目录，源码保持只读；完整逐字源码由知识库档案区保存，本篇聚焦如何理解和讲解。

## 输入、输出和上下游

AgentResult或OptionRiskAgent → 审计字典或AssertionError；脚本据此写正式验收JSON。本次教学只读代码和已有结果，没有重跑35品种。

直接导入模块：`__future__`, `collections.abc`, `dataclasses`, `datetime`, `inspect`, `json`, `math`, `numbers`, `pathlib`, `tempfile`, `typing`, `numpy`, `pandas`, `.agent`, `.config`, `.contracts`, `.errors`, `.graph_explanation`, `.graph_queries`, `.graph_reasoner`, `.knowledge_graph`, `.knowledge_schema`。


## 逐品种验收的实际取样

`validate_knowledge_graph_deployment`对每个选定品种取 `timestamps[-1]`，只分析这个最新有效时点。它先验问题1契约，再验图谱契约，最后汇总。返回 `mode="full"`指这条部署流程的全量选品种运行，不能据此推断跑了每个历史时点。

保存的 `outputs/knowledge_graph_acceptance_full.json` 确有35/35 passed，三项global_checks的checked_count分别是35、36、44。本次教学没有重跑这项大验收，读取已有JSON与实现以解释其含义。

| 全局检查 | 计数来由 | 能支持的结论 |
|---|---|---|
| deterministic | 35份成功图各独立恢复并规范重建两次 | 这些图的图/路径/查询/解释可确定重现；不等于从全源文件做两遍冷启动 |
| no_future | 35份图的时间审计 + 1个追加未来月份fixture | 显式来源无未来，且受控真实Agent链在该fixture中不受新增未来记录影响 |
| content_safety | 35份解释 + 2安全 + 7不安全措辞fixture | 已生成文本和这些边界例满足有限语言检查 |

未来fixture使用临时合成数据，分别建新缓存，避免“只是命中旧缓存所以相同”的伪验证。这里“真实OptionRiskAgent”指真正调用生产代码，不表示fixture的行情是真实市场数据。

## 35/35之外还缺哪些证明

它不包含全历史泛化、每个风险等级充分样本、盈利能力、因果识别或人工解释平均≥4/5。`validate_public_agent_surface`只看包公开导出的Agent类名，不能证明算法本身是LLM或通用智能体。

真实案例来自保存的0/1/2级与质量受限截面；3级为synthetic_contract，只验证规则/查询/解释链，不能计入真实市场的危险识别率，也不构成35品种里的第36个真实样本。

## 一个应该被验收拒绝的例子

把图谱WarningState的alert_level从2改3，却保留AgentResult为2：即使节点ID也改成合法3级格式、图形仍可显示，正式验收还会对照问题1逐字段查出不一致。把某条path_id复制进解释但该路径不在当前规范图，也会在重发现/重渲染阶段失败。因此通过条件远强于“程序没有报错”或“图成功画出来”。

## 逐个类与函数查阅

每个锚点都指向当前源文件的实际定义。嵌套函数属于所在外层算法；`self`表示实例状态，不是额外业务输入。

### `_require_graph_contract` · 60—62行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:60>)。不满足条件即明确AssertionError。

输入/输出接口：`(condition: bool, message: str)` → `None`。

### `_strict_json_ready` · 65—119行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:65>)。递归允许指定数据类型，保留非有限数让JSON拒绝，避免规范化掩盖错误。

输入/输出接口：`(value: Any, active: set[int] | None=None)` → `Any`。

### `_strict_json_document` · 122—132行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:122>)。严格规范JSON；allow_nan=False，失败变验收断言。

输入/输出接口：`(value: Any, *, owner: str)` → `str`。

### `_same_exact_json_structure` · 135—156行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:135>)。比较数据值和精确类型，包含dataclass字段递归。

输入/输出接口：`(actual: Any, expected: Any)` → `bool`。

### `_finite_number` · 159—165行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:159>)。有限数转换，拒绝bool。

输入/输出接口：`(value: Any)` → `float | None`。

### `_require_builtin_string` · 168—169行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:168>)。要求原生str。

输入/输出接口：`(value: Any, owner: str)` → `None`。

### `_require_optional_builtin_float` · 172—176行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:172>)。要求None或有限原生float。

输入/输出接口：`(value: Any, owner: str)` → `None`。

### `_require_string_tuple` · 179—184行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:179>)。要求tuple内每个ID为原生str。

输入/输出接口：`(value: Any, owner: str)` → `None`。

### `_require_feature_evidence_contract` · 187—207行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:187>)。检查FeatureEvidence精确类、文本/数值类型和严格JSON。

输入/输出接口：`(row: Any)` → `None`。

### `_require_risk_path_contract` · 210—236行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:210>)。检查RiskPath类、ID、三类元组、压力及Timestamp类型。

输入/输出接口：`(path: Any)` → `None`。

### `_require_explanation_section_contract` · 239—253行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:239>)。检查解释段类、正文、ID元组与JSON。

输入/输出接口：`(section: Any)` → `None`。

### `_one_graph_node` · 256—266行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:256>)。找唯一类型节点，缺失或多个失败。

输入/输出接口：`(graph, node_type: NodeType)` → `tuple[str, dict[str, Any]]`。

### `validate_knowledge_graph_result` · 269—748行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:269>)。480行独立审计：原始类型、图、时间、计数、路径、索引、问题1证据/警告、规范五段与六查询。

输入/输出接口：`(result: AgentResult, requested_product: str, requested_timestamp: pd.Timestamp)` → `dict[str, Any]`。

### `validate_public_agent_surface` · 751—764行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:751>)。检查包公开的以Agent结尾类恰为OptionRiskAgent；不是扫描所有内部类或证明不存在其他算法。

输入/输出接口：`()` → `dict[str, Any]`。

### `validate_agent_result` · 767—856行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:767>)。核请求身份、五曲面、五组证据、等级、原因、时间轴末行与策略一致性。

输入/输出接口：`(result: AgentResult, requested_product: str, requested_timestamp: pd.Timestamp)` → `dict[str, Any]`。

### `_canonical_graph_audit_document` · 859—911行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:859>)。恢复图重新推理/解释/六查询，做完整规范文档供确定性比较。

输入/输出接口：`(result: AgentResult)` → `str`。

### `_result_has_no_future_graph_data` · 914—938行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:914>)。审计节点边来源≤请求时点，Evidence和path必须等于时点。

输入/输出接口：`(result: AgentResult)` → `bool`。

### `_future_fixture_rows` · 941—1005行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:941>)。生成受控合成期权数据，仅用于防未来回归fixture。

输入/输出接口：`(product: str, timestamps: pd.DatetimeIndex, *, first_bar: int)` → `pd.DataFrame`。

### `_write_future_fixture_partition` · 1008—1027行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:1008>)。在临时根按赛题分区写fixture Parquet。

输入/输出接口：`(source: Path, product: str, frame: pd.DataFrame, month: pd.Timestamp)` → `Path`。

### `_future_append_rejection_fixture` · 1030—1110行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:1030>)。合成120个过去bar，真实Agent分析；再追加未来月份，用新缓存重算同旧时点，要求完整图谱与规范审计完全相同。

输入/输出接口：`()` → `bool`。

### `_executed_global_graph_checks` · 1113—1198行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:1113>)。逐成功品种检查确定性/未来/语言，再加一个未来fixture和九个措辞fixture，记录次数和范围。

输入/输出接口：`(successful_results: list[tuple[str, AgentResult]], *, total_products: int)` → `dict[str, dict[str, Any]]`。

### `validate_knowledge_graph_deployment` · 1201—1297行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:1201>)。每品种最新有效时点验问题1+2，再做强制全局检查；任一不通过总体失败。

输入/输出接口：`(agent: OptionRiskAgent, *, product_codes: list[str] | None=None, progress: Callable[[str], None] | None=None)` → `dict[str, Any]`。

### `validate_deployment` · 1300—1354行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py:1300>)。可只审目录或每品种最新时点验问题1，返回独立部署摘要。

输入/输出接口：`(agent: OptionRiskAgent, *, analyze: bool=True, product_codes: list[str] | None=None, progress: Callable[[str], None] | None=None)` → `dict[str, Any]`。

## 面试先讲清楚这一问

**问：35/35意味着预测成功率100%吗？**

答：不是。它表示被选择的35个品种最新有效时点通过响应/图谱契约检查，另有全局检查；不等于全历史、每级覆盖、收益证明或人工解释评分通过。

继续学习：[[20 - Agent如何把一次请求变成可复核风险判断]] → [[21 - 动态知识图谱的机制与推理边界]] → [[22 - 可追溯、防未来与运行身份]] → [[23 - 界面、真实案例与35品种验收]]。
