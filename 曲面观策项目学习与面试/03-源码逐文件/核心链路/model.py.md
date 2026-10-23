---
类型: 源码教学
模块: 核心链路
源文件: "src/option_risk/model.py"
依据: 最终提交项目静态源码
---

> [!abstract] 一句话定位
> **建立时间先后的逻辑回归离线对照**。主预警来自透明规则，这里是可检验的ML比较器和消融，不能把主系统口述为逻辑回归在线推断。

源文件：[src/option_risk/model.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/model.py:1>)。本文解释实际实现；逐字源码请结合知识库的源码档案阅读。

## 输入、输出与上下游

输入features与labels；输出ModelBundle、含所有行概率和split的predictions、diagnostics。默认raw_only排除label定义相关的压力与历史阈值列。pipeline另运行with_label_derived作对照。持久化warning_model.joblib供留档；Agent当前分析接口不加载它来决定预警。

## 逐个理解核心对象与函数

### `ModelBundle`（20—33 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/model.py:20>)

把估计器、按序特征名、关注/警告/危险概率门槛、训练/验证/测试边界与特征政策打包。只有这些一起保存，才知道预测概率对应怎样的数据列与校准期。

### `ModelBundle.save`（32—33 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/model.py:32>)

joblib.dump持久化整个bundle。它不生成评估报告，不证明反序列化文件安全，也不自动注册为运行时决策器。

### `chronological_month_split`（36—48 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/model.py:36>)

取索引中实际存在的不同月份排序；至少需要validation_months+test_months+2个月，默认至少6个月。末3个观测月份起为test，之前一月为validation_start，更早为train。若原始月份有缺口，“实际存在的末3月”不自动证明日历上连续。

### `_candidate_columns`（51—63 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/model.py:51>)

选数值与bool列，排除data_ready/history_ready。raw_only再排risk_pressure/core_risk_pressure以及pressure__/history_q95__前缀；其他数值列（包括当前ATM IV、报价数、变化量与underlying_return_1）可进入。字符串product不进入。raw_only并非没有任何与标签相关的经济信息，它只是隔离标签工程派生列。

### `_tune_warning_threshold`（66—100 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/model.py:66>)

在约0.001—0.999的非均匀概率网格上算点级Precision/Recall/F1，先优先选Precision≥0.5且Recall≥0.6的候选，再按F1、Recall、Precision排序；无可行候选仍选最优并显式feasible_target_found=False。它在验证集校准概率门槛，目标不等于正式规则事件指标。

### `_fit_estimator`（103—119 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/model.py:103>)

训练只有单类别时用DummyClassifier(strategy=prior)，避免逻辑回归无法拟合；正常路径为训练集median填补+缺失指示、RobustScaler、LogisticRegression(C=.25,max_iter=2000,class_weight=balanced,random_state=42)。所有预处理只fit训练集，之后transform验证/测试。

### `_positive_probability`（122—131 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/model.py:122>)

统一调用predict_proba并按classes_定位标签1的列；Dummy路径先fillna(0)。若训练从未有类别1，返回全0概率；不会误将唯一类别0的概率列当风险概率。

### `fit_warning_model`（134—227 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/model.py:134>)

划月份、构建split、purge跨边界标签，以有效标记选训练/验证/测试。默认训练截止train_end固定拟合一次；计算全序列及验证概率，验证集调warning，attention=max(.0001,.6×warning)，danger=min(.98,max(warning+.15,验证概率90分位))。输出各行split、标签、有效性和概率阈值，并记录样本量、正例率、排除列数、阈值诊断。walk_forward_folds为空，不是滚动重训。

## 关键推导、具体例子与真实边界

逻辑回归：

$$
\widehat p_t=\frac1{1+\exp[-(\beta_0+\boldsymbol\beta^\top\widetilde{\boldsymbol x}_t)]}.
$$

$\boldsymbol x_t$ 是此时已知特征，$\widetilde{\boldsymbol x}_t$ 是训练期填补和稳健缩放后的特征；$\beta$ 是训练标签学出的系数。$C=0.25$ 控制正则强度，越小通常约束越强；balanced重加权帮助少数类，但概率不能直接当已校准的真实事件频率。

假设月份为1—8月，默认test为6—8月、validation为5月、train到4月；模型在1—4月fit，5月只调阈值，6—8月不回流调整参数。全序列predictions也含训练期概率，它们是样本内结果，不能从里面挑最好的段宣称测试表现。

> [!warning] 可明确说明的限制
> `validation_months>1` 时实现仍只取等于validation_start的一个月，其他中间月可能标gap；不是通用多月验证器。危险门槛上限.98在warning>.98时甚至可能低于warning，需结合实际诊断检查，不能预设门槛永远严格递增。阈值可行性是结果字段，不是训练后自动达标保证。

## 面试怎么讲，追问怎么答

**问：为什么不用随机划分？** 相邻bar和同事件前多个正标签高度相关，随机划分会把时间上相似样本分给训练测试，并破坏部署先后顺序。

**问：带pressure消融一定是未来泄漏吗？** 这些pressure由过去阈值与当前值构成，未必含未来；问题是与内部标签定义高度同源、可能形成标签代理，因此作为敏感性对照，raw_only作为更保守ML口径。

**问：用了walk-forward吗？** 当前固定留出，诊断fold列表为空。函数或字段名不能代替真实协议。

## 下一步学习

[[02-循序学习/核心05-规则预警与机器学习对照到底各做什么]]
