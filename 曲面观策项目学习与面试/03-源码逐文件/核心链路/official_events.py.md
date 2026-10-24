---
类型: 源码教学
模块: 核心链路
源文件: "src/option_risk/official_events.py"
依据: 最终提交项目静态源码
---

> [!abstract] 一句话定位
> **把内部动态事件与官方事件日历分开验证**。官方事件是一条外部对照轴，没有拿来训练当前标签。

源文件：[src/option_risk/official_events.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/official_events.py:1>)。本文解释实际实现；逐字源码请结合知识库的源码档案阅读。

## 输入、输出与上下游

输入：extreme_event.csv、alerts、product配置。输出官方事件汇总与逐事件对照。pipeline先完成标签/模型/预警之后才调用；因此它不参与当前监督标签生成。

## 逐个理解核心对象与函数

### `find_official_event_file`（20—22 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/official_events.py:20>)

递归查找精确文件名extreme_event.csv并排序，只取第一份，没有检查多个版本是否内容一致。返回None时pipeline明确记录不可用。

### `load_official_events`（25—32 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/official_events.py:25>)

按GB18030读取，日期解析失败变NaT并删除缺开始/结束日期的行，再从1编号official_event_id；attrs保存来源路径。不是默认UTF-8，不要因乱码误判事件文本缺失。

### `evaluate_official_events`（35—104 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/official_events.py:35>)

用预定义品种板块映射对sectors_affected做精确isin过滤，再取与alerts日期范围重叠事件。每事件找到日历日期覆盖的全部市场bar，检查其首bar之前horizon根是否有通知、区间内是否通知；若多条前置通知取最早一条，记录bar数×15的lead。按事件起始第一市场bar所属split形成test子集。

## 关键推导、具体例子与真实边界

内部事件是核心压力首次越线；官方事件是宏观或板块事件的日期区间。两者不是同一个随机变量。例：官方事件从10月10日至12日，算法找数据中10日第一根bar；即使该事件实际于10日夜间才公开，本实现也以日期首bar为锚，所以无法据此证明对新闻发布时间的实时预测。

品种映射仅ag/au/cu/al/sc做专用板块，其他品种默认只认“全板块”。`sectors_affected`按完整字符串精确匹配，不会自动拆分任意逗号、做语义分类。事件期间预警与事件前预警分开统计，不能合称全部为提前预测。

源码summary内写明“源有17行而题目描述18事件”，这是代码中硬编码说明；实际当前CSV行数仍应以读取产物为证。日期区间和夜盘交易日口径也与backtest不同，本函数用timestamp.normalize的自然日。

## 面试怎么讲，追问怎么答

**问：官方事件召回高，是否说明训练标签可信？** 只能说明一定口径下对照相关，内部标签和外部事件定义、时间粒度与品种覆盖不同，应分别报告。

**问：为什么事件回测和官方事件lead不同？** evaluate_alerts给内部事件取最近的前置episode起点（不是段内最新任意通知）；本函数取窗口最早的原始alert_emitted通知，二者锚与匹配规则都不同。

## 下一步学习

[[曲面观策项目学习与面试/02-循序学习/核心08-离线Pipeline与单时点Agent的完整关系.md|核心08-离线Pipeline与单时点Agent的完整关系]]
