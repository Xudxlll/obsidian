---
类型: 源码教学
源文件: "/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_visualization.py"
阅读方式: 实际完整源码与函数核对
---

> [!info] 在项目里的职责
> 用Plotly将已排序活动路径画在Evidence/Anomaly/Mechanism/Conclusion四列，最多取1—3条。节点可选中回到精确ID，hover保留完整审计属性；它不重新计算风险。

源码入口：[src/option_risk/graph_visualization.py 第1行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_visualization.py:1>)。本篇依据最终提交目录，源码保持只读；完整逐字源码由知识库档案区保存，本篇聚焦如何理解和讲解。

## 输入、输出和上下游

ready KnowledgeGraphResult + max_paths → go.Figure；dashboard消费，完整路径仍在结果与查询中。

直接导入模块：`__future__`, `collections.abc`, `plotly.graph_objects`, `.contracts`, `.graph_queries`, `.knowledge_graph`, `.knowledge_schema`。


## 最小阅读方法

顺着入口语句看调用方与被调用方；本文件只提供公开边界，不另设业务算法。

## 一组路径怎样变成主图

假设规范排序是ATM后果链、ATM预警链、期限倒挂后果链、覆盖缺口置信链。默认max_paths=3就画前三条：ATM证据/异常/机制会共享节点，覆盖质量链这次不在主图。root_evidence仍可查询更多去重证据，quality_limitations仍可返回覆盖链；主图是否画到不改变底层结论。Plotly节点customdata保存精确ID，点击后界面用GraphQueryService查当前事件，不靠显示标签猜测。

## 逐个类与函数查阅

每个锚点都指向当前源文件的实际定义。嵌套函数属于所在外层算法；`self`表示实例状态，不是额外业务输入。

### `_strict_path_cap` · 31—36行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_visualization.py:31>)。只允许原生int的1/2/3，True不算1。

输入/输出接口：`(max_paths: int)` → `int`。

### `_path_node_ids` · 39—45行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_visualization.py:39>)。取得四层节点ID顺序。

输入/输出接口：`(path: RiskPath)` → `tuple[str, str, str, str]`。

### `_node_hover` · 48—68行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_visualization.py:48>)。给证据保留数值、阈值、压力、来源时间和规则的完整hover。

输入/输出接口：`(record: dict[str, object])` → `str`。

### `_display_label` · 71—74行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_visualization.py:71>)。每7字符换行适配窄屏，hover原文不变。

输入/输出接口：`(value: object)` → `str`。

### `_path_edges` · 77—83行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_visualization.py:77>)。对前三路径边ID保序去重，避免重复画共享边。

输入/输出接口：`(paths: Iterable[RiskPath])` → `list[str]`。

### `knowledge_graph_figure` · 86—226行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_visualization.py:86>)。先构造查询服务复验，再放到固定四列，生成可选择节点和带关系文字箭头。

输入/输出接口：`(result: KnowledgeGraphResult, max_paths: int=3)` → `go.Figure`。

## 面试先讲清楚这一问

**问：只画三条是否丢失其他风险？**

答：主图限制展示密度；全部路径仍可审计。且前三条是路径，不保证是三个不同证据，同一市场证据可能占后果链和预警链两条。

继续学习：[[20 - Agent如何把一次请求变成可复核风险判断]] → [[21 - 动态知识图谱的机制与推理边界]] → [[22 - 可追溯、防未来与运行身份]] → [[23 - 界面、真实案例与35品种验收]]。
