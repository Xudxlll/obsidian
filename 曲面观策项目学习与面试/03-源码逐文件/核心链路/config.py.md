---
类型: 源码教学
模块: 核心链路
源文件: "src/option_risk/config.py"
依据: 最终提交项目静态源码
---

> [!abstract] 一句话定位
> **把经济假设集中为可审计配置**。修改一个数字会同时改变清洗、历史阈值、标签或对照模型，先学清这些含义，再谈调参。

源文件：[src/option_risk/config.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/config.py:1>)。本文解释实际实现；逐字源码请结合知识库的源码档案阅读。

## 输入、输出与上下游

上游是 CLI 或部署传入的品种、日期、路径；下游几乎所有分析模块都读取这些配置。`PipelineConfig` 描述分析假设，`PipelinePaths` 管输出目录，`AgentConfig` 管部署路径和回看范围。它们不是训练出的参数，也不是让用户在网页中任意修改的策略。

## 逐个理解核心对象与函数

### `PipelineConfig`（8—62 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/config.py:8>)

用带 `slots=True` 的 dataclass 保存默认参数。清洗默认保留 DTE 2—180 天、价内外程度 0.70—1.30、IV 0.0005—5.0；ATM 带为 $|\ln(K/F)|\le0.03$，翼部为对数价内外程度绝对值 0.05—0.15。历史为 20×32=640 个观测，最少 96 个；短变化 4 根，提前 2 根到未来 8 根，事件起点冷却 8 根。验证 1 月、测试末 3 月。这里的“根”是已排序观测行，不是补齐后的自然时间网格。

### `PipelineConfig.historical_window_bars`（49—50 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/config.py:49>)

把每交易日预计 bar 数乘历史日数，返回 640；实际 rolling 仍按全部传入特征行的行数计算，夜盘和缺失 bar 不会自动补成等间隔；并未先过滤data_ready历史行，min_history_bars是每个信号有效观测的最少数量。

### `PipelineConfig.to_dict`（52—53 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/config.py:52>)

用 `asdict` 导出完整配置，给 run_summary 和身份记录使用；这样读结果的人能知道结果对应哪套假设。

### `PipelineConfig.from_paths`（56—62 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/config.py:56>)

名字带 paths，但实际只构造品种小写、开始日期和结束日期，不读取文件、不查目录；其他参数使用 dataclass 默认值。

### `PipelinePaths`（66—72 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/config.py:66>)

只存原始数据与输出目录。不会自动检查二者是否重合，所以执行者应明确把实验输出放到独立目录。

### `PipelinePaths.ensure`（70—72 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/config.py:70>)

递归创建输出目录及 figures 子目录，是文件系统写操作，尚不意味着数据已处理成功。

### `AgentConfig`（76—110 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/config.py:76>)

默认缓存 data/agent_cache，回看 45 个日历日；这是在线式单时点分析需要的部署资源配置，与离线按全序列训练的配置不同。

### `AgentConfig.__post_init__`（86—97 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/config.py:86>)

将路径解析为绝对路径。无 data_source 时指向 cache/archive_source，无 output_dir 时指向 cache/outputs；archive_path 可为空。路径解析不证明文件存在或归档已解压。

### `AgentConfig.ensure_directories`（99—102 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/config.py:99>)

创建缓存和输出目录，并断言 output_dir 已由初始化补齐。

### `AgentConfig.pipeline_config`（104—110 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/config.py:104>)

把品种与日期交给 PipelineConfig.from_paths，复用同一套清洗和特征默认值；并不从 warning_model.joblib 恢复模型。

## 关键推导、具体例子与真实边界

例如历史日数由 20 改 10，窗口由 640 变 320，但最低历史仍是 96；不能把“窗口缩短”和“首次可用时间提前一半”画等号。`timezone` 只是配置字段，io.py 的 `pd.to_datetime` 没有据此本地化时区。默认策略里有两种冷却：标签事件的 `event_cooldown_bars=8`，正式 DecisionPolicy 的 `cooldown_bars=6`，属于不同对象，不能混为一个参数。

> [!warning] 假设与证据
> bars_per_trading_day=32 是窗口换算假设；不能据此声称每个商品的真实交易日都有 32 根。要验证实际覆盖，应从目录、时间戳和质量报告取证。

## 面试怎么讲，追问怎么答

**问：配置是超参数吗？** 有些是（如历史窗口），有些是业务约束（如 DTE）或基础设施路径。正式策略参数与可选 ML 参数还属于不同层次。

**问：修改验证月数就能做任意多月验证吗？** 当前 model.py 只用 `periods == validation_start` 选择一个月；把 validation_months 改大可能产生 gap 月，不能宣称自动支持多月验证。

## 下一步学习

[[02-循序学习/核心01-从一条期权报价到可分析的干净样本]]
