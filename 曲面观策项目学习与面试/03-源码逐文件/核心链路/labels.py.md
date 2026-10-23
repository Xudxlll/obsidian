---
类型: 源码教学
模块: 核心链路
源文件: "src/option_risk/labels.py"
依据: 最终提交项目静态源码
---

> [!abstract] 一句话定位
> **用未来新事件构建监督标签，并隔离跨集合窗口**。未来信息可以定义训练目标，不能倒流到预测特征或集合选择。

源文件：[src/option_risk/labels.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/labels.py:1>)。本文解释实际实现；逐字源码请结合知识库的源码档案阅读。

## 输入、输出与上下游

输入：按时序排序的features。输出labels含breach、event_start、label、future_severity、label_available；purge函数接收同索引split序列，输出有效标签与边界清除统计。event_table生成事件CSV所需表。

## 逐个理解核心对象与函数

### `build_forward_labels`（9—43 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/labels.py:9>)

优先用core_risk_pressure（列不存在才退回risk_pressure），压力≥1且数据/历史ready才是breach；只将False→True且距离上次事件起点≥8行记event_start。标签为未来第2—8行任一event_start出现；future_severity取同窗口压力最大值。label_available要求当前ready，长度≥horizon时再将末8行标为不可用。注意代码逐行索引，没有按墙钟时间查未来30—120分钟。

### `purge_split_boundary_labels`（46—89 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/labels.py:46>)

先检查horizon非负、索引完全一致、有label_available。找split变化边界，只针对train→validation和validation→test，把边界前horizon_bars行的可用性设False。它保留标签值及event_start，只改变可用于拟合/校准/评估的标记，并报告各边界清除行数及去重总数。不会泛化处理任意gap或test→train跳转。

### `event_table`（92—96 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/labels.py:92>)

只取event_start为True的行及对应future_severity，将索引名改event_time，给事件按序从1编号再reset_index。这里severity仍是该事件起点之后2—8行最大压力，不是事件起点当下压力，也不是完整事件持续期最大压力。

## 关键推导、具体例子与真实边界

设第8行是事件起点，则能提前2—8行预测它的行是0—6行；第7行距事件仅1行，不是正标签，第8行发生当下也不是针对该事件的正标签。多次连续breach只算第一个起点；一次False间隔后重越线，若距上次起点不足8行仍不记新事件。

$$
y_t=\mathbf1\left\{\exists h\in\{2,3,\ldots,8\}:e_{t+h}=1\right\}.
$$

$e_t$ 是“新恶化事件开始”，$y_t$ 是“现在预警是否能覆盖未来目标事件”。同一事件前有最多7个正标签，因此点级Recall与事件Recall不同。

假设验证集第一行位置1000。若训练行995的标签查看未来997—1003，它已借用验证期的事件定义；purge将992—999共8行的label_available设False，防止这种边界穿越。特征历史使用训练期过去数据进入验证期是允许的，删除标签边界不要求把滚动历史清零。

> [!warning] 已有实现边界
> 只有len(labels)≥8时才屏蔽末8行，少于8行的极短输入没有同样保护；完整离线链通常还会被历史和月份门槛阻挡，但不能据此忽略函数局部边界。缺bar和午休跨夜会让“2根=30分钟”仅是交易序列等效时长。

## 面试怎么讲，追问怎么答

**问：用了shift(-h)就是泄漏吗？** 在标签里合理，在预测时可用特征里不合理。关键是数据在哪个角色、何时可见、怎样隔离。

**问：官方极端事件CSV是训练标签吗？** 不是。这里是动态核心压力定义的内部事件，官方CSV另用于事后对照。

## 下一步学习

[[02-循序学习/核心04-标签如何定义未来以及怎样防止泄漏]]
