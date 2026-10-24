---
类型: 源码教学
源文件: "/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/decision.py"
阅读方式: 实际完整源码与函数核对
---

> [!info] 在项目里的职责
> 在已经计算好的历史压力上运行唯一正式策略。等级0/1/2/3是当前状态；alert_emitted是新通知脉冲。综合最大压力可用于关注，但正式警告/危险依赖较窄的核心市场风险和多市场信号条件。

源码入口：[src/option_risk/decision.py 第1行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/decision.py:1>)。本篇依据最终提交目录，源码保持只读；完整逐字源码由知识库档案区保存，本篇聚焦如何理解和讲解。

## 输入、输出和上下游

过去特征表 + DecisionPolicy + 所选时点 → 全时间状态表，或单时点DecisionResult。features提供数值，Agent/回测复用同一决策。

直接导入模块：`__future__`, `dataclasses`, `hashlib`, `json`, `numpy`, `pandas`, `.config`, `.contracts`, `.errors`。


## 三个分数/等级，必须拆开

设第 $j$ 项压力为 $p_{j,t}$。上游features计算所有指标；本模块定义的核心是：

$$
R_t=\max_j p_{j,t},\qquad C_t=\max(p_{\mathrm{ATM},t},p_{\mathrm{convexity},t}).
$$

$R_t$体现全部诊断证据的最大压力，包括质量；$C_t$只围绕赛题核心事件定义。市场多信号数为：

$$
M_t=\sum_{j\in\mathcal M}\mathbf 1\{p_{j,t}\ge1.00\},
$$

$\mathcal M$为九项市场指标，不含零成交、IV求解下限和覆盖缺口。“独立信号”是代码中不同列的计数，不是已经证明统计独立。

### 按代码顺序理解分支

- 未准备好：状态表标 `not_ready`；单时点评估直接抛历史/质量异常。
- 危险：$C_t\ge1.50$ 且 $M_t\ge3$，设3级。初次进入发通知；连续危险保持而不每bar通知。
- 否则只要 $C_t\ge0.98$：设2级。新进入正式状态即通知；之后仅当 $0.98\le C_t<1.00$ 且距上次通知至少6bar才再发通知。$C_t\ge1$持续时是warning_held，不能误读成必须小于1才有2级。
- 其余：$R_t\ge0.90$进入/维持1级关注。回落需至少保持2bar且 $R_t\le0.85$，或达到最长6bar且低于0.90才释放。0.85—0.90之间是迟滞区间。

参数的“固定”指分段压力比和时序策略固定；压力的分母是各时点过去历史的动态分位数。因此它仍是动态阈值策略。`from_diagnostics`不会根据某份测试成绩另选参数。

## 手算两个容易讲错的案例

案例A：某质量项压力4，ATM压力0.60、凸性压力0.70，其他市场项不足。$R=4,C=0.70$，最多可使系统关注，不能因此进入2/3级。

案例B：ATM压力1.60，只有两项市场压力达到1。$C\ge1.50$但 $M=2$，仍不满足3级；根据正式分支是2级。只有同时满足多信号条件才3级。

问：为什么把状态和通知分离？答：持续风险需要持续显示，但运营通知不能每15分钟重复轰炸；状态机加冷却和保持使两种职责分别可检验。

## 逐个类与函数查阅

每个锚点都指向当前源文件的实际定义。嵌套函数属于所在外层算法；`self`表示实例状态，不是额外业务输入。

### `DecisionPolicy` · 67—129行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/decision.py:67>)。冻结的正式策略参数集合：关注/释放/警告/危险、多信号、冷却、保持与版本。

输入/输出接口：类；字段：`attention_pressure`, `attention_release_pressure`, `warning_pressure`, `warning_upper_pressure`, `danger_pressure`, `danger_core_pressure`, `multi_signal_count`, `cooldown_bars`, `persistence_bars`, `max_watch_bars`, `policy_version`。

### `DecisionPolicy.from_diagnostics` · 81—117行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/decision.py:81>)。仅接受预注册策略版本、选择来源、参数值和匹配完整哈希，不能从摘要任意改策略。

输入/输出接口：`(cls, payload: dict[str, object] | None)` → `'DecisionPolicy'`。

### `DecisionPolicy.parameter_hash` · 120—129行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/decision.py:120>)。规范JSON编码除版本外所有策略参数后算SHA256。

输入/输出接口：`(self)` → `str`。

### `canonical_policy_diagnostics` · 132—143行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/decision.py:132>)。返回正式策略来源、版本、哈希和关键选定参数。

输入/输出接口：`()` → `dict[str, object]`。

### `DecisionResult` · 147—160行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/decision.py:147>)。单时点决策协议，带等级/通知/迁移原因/证据/解释原因。

输入/输出接口：类；字段：`timestamp`, `alert_level`, `alert_name`, `alert_emitted`, `risk_score`, `policy_version`, `policy_parameter_hash`, `transition_reason`, `trigger_reasons`, `feature_evidence`。

### `DecisionResult.to_dict` · 159—160行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/decision.py:159>)。把单时点决策转为JSON可用字典。

输入/输出接口：`(self)` → `dict[str, object]`。

### `_number` · 163—168行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/decision.py:163>)。转为有限float，失败/无穷返回None。

输入/输出接口：`(value: object)` → `float | None`。

### `_direction` · 171—178行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/decision.py:171>)。当前减上一值，用相对容差判断方向；变化率除以上一期绝对值。

输入/输出接口：`(current: float | None, previous: float | None)` → `tuple[str, float | None]`。

### `_severity` · 181—190行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/decision.py:181>)。单项证据严重度以0.90/0.98/1.50分段；它不等于总体危险条件。

输入/输出接口：`(pressure: float | None, policy: DecisionPolicy)` → `int`。

### `apply_decision_policy` · 193—342行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/decision.py:193>)。按时间重放past-only状态机，输出当前等级与稀疏通知脉冲。

输入/输出接口：`(features: pd.DataFrame, policy: DecisionPolicy | None=None, *, timestamp: pd.Timestamp | str | None=None)` → `pd.DataFrame`。

### `_evidence` · 345—395行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/decision.py:345>)。构造12项完整证据与按压力排序的前三触发原因。

输入/输出接口：`(history: pd.DataFrame, row: pd.Series, policy: DecisionPolicy)` → `tuple[list[FeatureEvidence], list[TriggerReason]]`。

### `assess_features` · 398—456行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/decision.py:398>)。严格定位所选时点，验证data/history ready，重放状态机并返回当前DecisionResult。

输入/输出接口：`(features: pd.DataFrame, timestamp: pd.Timestamp | str, policy: DecisionPolicy | None=None, config: PipelineConfig | None=None)` → `DecisionResult`。

## 面试先讲清楚这一问

**问：为什么风险分数4也可能只有2级？**

答：分数取12项最大值，3级另要求核心压力≥1.50且至少3个市场压力≥1；任何单项最大值都不能单独替代这个合取条件。

继续学习：[[曲面观策项目学习与面试/02-循序学习/20 - Agent如何把一次请求变成可复核风险判断.md|20 - Agent如何把一次请求变成可复核风险判断]] → [[曲面观策项目学习与面试/02-循序学习/21 - 动态知识图谱的机制与推理边界.md|21 - 动态知识图谱的机制与推理边界]] → [[曲面观策项目学习与面试/02-循序学习/22 - 可追溯、防未来与运行身份.md|22 - 可追溯、防未来与运行身份]] → [[曲面观策项目学习与面试/02-循序学习/23 - 界面、真实案例与35品种验收.md|23 - 界面、真实案例与35品种验收]]。
