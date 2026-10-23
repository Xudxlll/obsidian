---
类型: 源码教学
源文件: "/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/knowledge_schema.py"
阅读方式: 实际完整源码与函数核对
---

> [!info] 在项目里的职责
> 定义八种节点、九种关系与十二项特征的固定语义映射。规则决定某项数值证据可以被解释为什么异常、机制和非方向后果；这是一套人工登记知识，不是从市场数据学习出来的因果图。

源码入口：[src/option_risk/knowledge_schema.py 第1行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/knowledge_schema.py:1>)。本篇依据最终提交目录，源码保持只读；完整逐字源码由知识库档案区保存，本篇聚焦如何理解和讲解。

## 输入、输出和上下游

PRESSURE_SPECS → FEATURE_RULES；validate_schema在模块导入时执行，图构建与路径发现共享同一注册表。

直接导入模块：`__future__`, `dataclasses`, `enum`, `re`, `typing`, `.decision`。


## 十二项映射按经济意义分组记

前三项描述波动率整体、短时变化和近端压力；随后四项描述曲面局部/相对定价/期限一致性；Gamma和Vega集中描述敏感性可能被放大；后三项描述可观测性与反解可靠性。每项各有独立ASCII代码与版本化rule_id。

| 例子 | 登记的语义 | 必须保留的限制 |
|---|---|---|
| ATM IV高 | 波动率整体重定价→短期波动风险 | 不预测标的涨跌 |
| 凸性违反 | 定价一致性下降→估值一致性风险 | 不代表可执行套利 |
| Gamma HHI高 | 非线性敏感性集中→可能放大Gamma风险 | 不是买卖/仓位建议 |
| 覆盖缺口高 | 曲面分析可靠性受限→解释置信度降低 | 不支持2/3级市场风险升级 |

`validate_schema`把规则表与decision.PRESSURE_SPECS精确对齐，连顺序都检查。新增指标不仅是画一条边，还要更新数值特征、压力、证据协议、规则、查询预期与验收测试；否则很容易出现图说12项但决策已换列的版本漂移。

## 逐个类与函数查阅

每个锚点都指向当前源文件的实际定义。嵌套函数属于所在外层算法；`self`表示实例状态，不是额外业务输入。

### `NodeType` · 15—23行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/knowledge_schema.py:15>)。八类节点枚举：上下文、四层业务链与警告/置信结论。

输入/输出接口：类；共享配置/方法边界。

### `RelationType` · 26—35行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/knowledge_schema.py:26>)。九类允许关系枚举，避免任意字符串关系漂移。

输入/输出接口：类；共享配置/方法边界。

### `FeatureRule` · 39—57行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/knowledge_schema.py:39>)。单项证据语义协议：稳定顺序、ID、各层代码、文本、措辞边界与关系。

输入/输出接口：类；字段：`order`, `rule_id`, `feature_name`, `evidence_group`, `label`, `evidence_code`, `anomaly_code`, `anomaly`, `mechanism_code`, `mechanism`, `conclusion_code`, `conclusion`, `conclusion_type`, `boundary`, `evidence_relation_options`, `relation_types`。

### `_rule` · 60—111行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/knowledge_schema.py:60>)。复用PRESSURE_SPECS组名/标签，自动给质量和集中度选择正确末端关系。

输入/输出接口：`(order: int, feature_name: str, anomaly: str, mechanism: str, conclusion: str, conclusion_type: NodeType, boundary: str)` → `FeatureRule`。

### `_as_node_type` · 130—134行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/knowledge_schema.py:130>)。检查节点类型属于注册枚举。

输入/输出接口：`(value: object)` → `NodeType`。

### `_as_relation_type` · 137—141行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/knowledge_schema.py:137>)。检查关系类型属于注册枚举。

输入/输出接口：`(value: object)` → `RelationType`。

### `validate_schema` · 144—217行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/knowledge_schema.py:144>)。严格检查特征顺序与决策一致、代码/版本确定，质量末端只能降低置信度。

输入/输出接口：`(rules: Iterable[FeatureRule] | None=None)` → `None`。

## 面试先讲清楚这一问

**问：为什么质量结论不用RiskConsequence？**

答：质量退化首先限制我们对市场的观察与解释可信度，不应被当作价格波动风险已被证实。

继续学习：[[20 - Agent如何把一次请求变成可复核风险判断]] → [[21 - 动态知识图谱的机制与推理边界]] → [[22 - 可追溯、防未来与运行身份]] → [[23 - 界面、真实案例与35品种验收]]。
