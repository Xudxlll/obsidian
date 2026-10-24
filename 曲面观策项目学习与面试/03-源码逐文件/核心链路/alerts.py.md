---
类型: 源码教学
模块: 核心链路
源文件: "src/option_risk/alerts.py"
依据: 最终提交项目静态源码
---

> [!abstract] 一句话定位
> **分清正式状态机、ML对照与评估口径**。同一个文件服务三种预警，并不意味着它们是同一模型。

源文件：[src/option_risk/alerts.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/alerts.py:1>)。本文解释实际实现；逐字源码请结合知识库的源码档案阅读。

## 输入、输出与上下游

输入features、模型predictions和bundle/config；输出附风险状态、稀疏通知、解释、策略诊断的表。正式路径tune_predictive_rule→assign_predictive_rule_alerts→decision.apply_decision_policy；ML路径assign_walk_forward_alerts→assign_alert_levels；共同评价函数evaluate_alerts。

## 逐个理解核心对象与函数

### `_explain_row`（36—46 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/alerts.py:36>)

遍历12项压力中文标签，将有值者按压力倒序，取最多3项且≥0.8生成简短解释；无触发则写压力较低。它只是离线解释文本，不决定alert_level；阈值0.8也不是正式DecisionPolicy的0.9。

### `assign_alert_levels`（49—114 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/alerts.py:49>)

ML比较器先join概率、数据准备状态和12项压力。概率到attention给1级；概率到warning且达到min_signals（默认2）的压力数连续满足persistence（默认2）才2级；再满足danger概率、至少3证据和总体pressure≥1.5为3级。数据未ready强制0；连续风险状态不受冷却更改，另每隔event_cooldown_bars产生alert_emitted。

### `_policy_grid`（117—128 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/alerts.py:117>)

枚举ML比较器证据门槛1/2/3、连续1/2/3根与冷却4/6/8/10/12/16/24，共63组配置；用dataclasses.replace保留其他配置。

### `_tune_policy_for_month`（131—173 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/alerts.py:131>)

每组在全序列产生候选状态，把指定月标calibration，再用该月事件指标评估；可行目标为事件precision≥.5、recall≥.6、平均lead≥30，按F1等选策略。无可行仍选最优并报告。它不应使用test来选策略。

### `assign_walk_forward_alerts`（176—196 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/alerts.py:176>)

名称保留历史叫法，实际只在bundle.validation_end那个月选一次ML比较器策略，然后同一策略覆盖validation和fixed test。没有逐测试月重训或重调。

### `assign_predictive_rule_alerts`（199—245 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/alerts.py:199>)

从features挑正式证据并joinpredictions的split/label；用lower、upper、cooldown实例化DecisionPolicy，再把apply_decision_policy输出逐列写入结果。核心决策不读取risk_probability，尽管结果表里保留该概率列。decision_source标正式规则版本。

### `tune_predictive_rule`（248—311 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/alerts.py:248>)

先使用固定DecisionPolicy构造正式alerts并算验证指标；再跑lower .94—.99步长.005、upper 1/1.05/∞、cooldown六档的网格，仅作为validation-only sensitivity_analysis。返回的alerts始终是固定canonical政策，最优敏感性候选不替换正式策略。

### `evaluate_alerts`（314—389 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/alerts.py:314>)

先取split匹配且label_available行；点级precision/recall把稀疏alert_emitted与label比较。再把相邻发射位置间距≤2行的通知连成episode，仅保留每段首个发射位置episode_starts。用每段起点未来0—horizon内有事件计算事件precision，用事件前1—horizon内存在段起点计算事件recall，并取其中最近的前置段起点算lead×15分钟；不是取最近任意一条通知。分别输出当前风险状态行数、通知数、episode数、事件数与目标是否达到。

## 关键推导、具体例子与真实边界

一个警告持续5根，而只在第一根alert_emitted=True，当前风险状态始终应显示警告；不能为减少通知把后4根改成“无预警”。状态是市场判断，通知是操作动作。

举例事件在位置10，且相关通知各自是独立episode的起点：起点10可算事件Precision命中，却不能计入该事件Recall的“前置段起点”；起点9可算Recall，lead=15分钟，但不是labels.py定义的2—8根正标签。position2—8的通知才符合本事件的严格30—120分钟标签窗口。这就是必须并列报告点级、事件级和lead分布的原因。

$$
Precision_{event}=\frac{\text{0到8根内有事件的通知episode}}{\text{全部通知episode}},\qquad Recall_{event}=\frac{\text{前1到8根有通知的事件}}{\text{全部事件}}.
$$

评估先过滤可用行再按位置计数，窗口是在筛后的frame上定义；跨purge空档、数据未ready间隔或拆分边缘会被压缩。它不是一对一匹配：同一episode起点可能落入多个事件窗口，多个episode也可指向同一事件，代码不会把已匹配对象移除。若通知在7/8/9、事件在10，三条通知合成一个episode起点7，lead=(10−7)×15=45分钟，而不是取通知9算15分钟。输出键`correct_alerts_with_event_in_0_to_8_bars`名称写死8，但实际计算读config.horizon_bars。

正式Policy的2级状态是core≥.98，允许从下方接近阈值和越线后的警告；不是只有[.98,1)才警告。区间上界主要影响冷却后重复通知。

## 面试怎么讲，追问怎么答

**问：为什么你的最终表既有risk_probability又说主系统是规则？** 表保留ML比较器的概率供研究，主alert_level/alert_emitted被正式状态机覆写；应按决策实际依赖讲解。

**问：Precision达50%、Recall达60%就等于提前30分钟成功？** 否，事件命中容许更短甚至同时点通知，必须同时检查lead，而且平均≥30也不意味着每个事件≥30。

## 下一步学习

[[曲面观策项目学习与面试/02-循序学习/核心06-预警状态通知与评价怎样避免混淆.md|核心06-预警状态通知与评价怎样避免混淆]]
