---
类型: 源码教学
模块: 核心链路
源文件: "src/option_risk/pipeline.py"
依据: 最终提交项目静态源码
---

> [!abstract] 一句话定位
> **一次离线运行生成训练对照、正式预警和可追溯报告**。这是实验总编排，和单时点Agent是并列工作流。

源文件：[src/option_risk/pipeline.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/pipeline.py:1>)。本文解释实际实现；逐字源码请结合知识库的源码档案阅读。

## 输入、输出与上下游

输入data_dir、独立output_dir与可选config；输出run_summary字典并写多种文件。必须有足够月份才能过ML划分，因此不是给任意单时点调用的轻量接口。上游io/quality/surfaces/features；中段labels/model/alerts；下游backtest/official_events/visualization/provenance与产物。

## 逐个理解核心对象与函数

### `_json_default`（34—41 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/pipeline.py:34>)

把numpy标量变Python标量，Timestamp/Period/Path变字符串，ndarray变list；其他未知类型报TypeError，防止悄悄写出无法解释的数据对象。

### `_write_json`（44—47 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/pipeline.py:44>)

使用UTF-8、ensure_ascii=False、缩进2把payload写到指定路径；序列化转换交_json_default。写入本身没有临时文件原子替换机制。

### `_identity_input_files`（50—60 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/pipeline.py:50>)

复制发现的Parquet路径列表，若存在官方事件CSV且不重复则加入，用于run身份。传入的是discover出的文件列表，不应仅凭docstring称每份都实际解析成功，read_option_files可能跳过分区或schema。

### `_attach_run_identity`（63—99 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/pipeline.py:63>)

要求正式策略诊断为dict，按DecisionPolicy.from_diagnostics恢复固定canonical政策并核对参数hash；将features、config、输入、源码根、校准/测试边界等交build_run_identity。再运行fixed_holdout_checks，任一失败删除身份并报错；身份缺失不能声称通过固定留出鉴证。

### `_rule_baseline`（102—114 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/pipeline.py:102>)

用risk_pressure生成简单分级0/.8/1/1.5并门控data_ready，以1−exp(−max(pressure−.5,0))映射展示分数，所有≥2行都发射。它是较粗基线，无正式状态机的稀疏通知/回滞，不是canonical正式规则。该risk_probability是规则映射分数，非学习概率。

### `_effective_labels_for_output`（117—127 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/pipeline.py:117>)

检查predictions包含原labels所有列、索引相同，返回模型划分purge之后的标签列，保证正式risk_labels保存的是边界清除过的有效性，而非最初未经purge的标签表。

### `run_pipeline`（130—271 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/pipeline.py:130>)

依次完成读取→清洗→节点→特征→原始标签→raw_only固定留出ML→验证选ML通知策略→固定正式规则→带标签派生列的ML消融→简单规则基线。分别算正式验证/测试、ML、简单基线、消融测试指标；只对正式alerts做CVaR与官方事件对照。写表/模型后挑最新数量合格时点生成IV/Greeks/时间轴与npz，汇总config/quality/surface/model/policy/metrics/outputs，绑定run_identity后写run_summary.json。中途失败可能已留下部分文件，不能仅凭文件存在判断整次成功。

## 关键推导、具体例子与真实边界

主要产物与真实含义：

| 文件 | 内容 | 容易说错的地方 |
|---|---|---|
|risk_features.parquet|全部时点特征、阈值和压力|不是只有12列|
|risk_labels.parquet|经split边界purge的标签可用性|末尾或边界处label值仍可能存在，但不可用|
|warning_predictions.parquet|正式规则状态、通知、split、标签及保留的ML概率|概率存在不代表正式状态由ML决定|
|ml_predictions_raw_only.parquet|raw_only逻辑回归及比较器通知|不同于主预警|
|ablation_predictions_with_label_derived.parquet|保留压力和阈值派生列的ML消融|不能替代保守口径|
|detected_events.csv|全序列事件起点|不随purge删除事件本身|
|warning_model.joblib|raw_only离线ML bundle|不包含正式状态机替代品|
|cvar_backtest_daily.parquet|多空基准/减仓日收益和敞口|单次减仓的简化实验|
|cvar_random_warning_baseline.parquet|随机日期对照|不是随机价格市场模拟|
|run_summary.json|配置、各口径指标与身份|应核验与当前源码和输入匹配|

链路中的完整IV拟合发生在210—219行最新快照展示阶段，而features在148行就已生成；因此“用SVI拟合所有时点再提特征训练”不符合这条代码路径。

## 面试怎么讲，追问怎么答

**问：你怎么确保结论可追溯？** 除文件和配置外，主策略有版本与参数hash，run身份将代码、数据、配置和测试边界绑定，并做固定留出检查；但我会验证具体产物身份后才引用数值。

**问：Pipeline能直接当网页请求处理吗？** 它会训练、评估、写大量文件且要求月份覆盖；网页走Agent单时点分析，其职责与延迟预算不同。

## 下一步学习

[[曲面观策项目学习与面试/02-循序学习/核心08-离线Pipeline与单时点Agent的完整关系.md|核心08-离线Pipeline与单时点Agent的完整关系]]
