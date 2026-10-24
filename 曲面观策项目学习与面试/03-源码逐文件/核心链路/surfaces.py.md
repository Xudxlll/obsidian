---
类型: 源码教学
模块: 核心链路
源文件: "src/option_risk/surfaces.py"
依据: 最终提交项目静态源码
---

> [!abstract] 一句话定位
> **先形成同一时刻的经济坐标节点，再得到展示网格**。IV走总方差拟合诊断接口，Greeks走各期限内的有限支撑插值。

源文件：[src/option_risk/surfaces.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surfaces.py:1>)。本文解释实际实现；逐字源码请结合知识库的源码档案阅读。

## 输入、输出与上下游

输入：cleaned 报价。输出一是逐时点的 nodes，二是单个 timestamp/metric 的 SurfaceGrid。上游 quality.py 提供经济坐标和资格标记；下游 features.py 使用 nodes，visualization/interactive/Agent 展示 grid。重要顺序：正式风控特征直接来自 cleaned/nodes，并没有统一地先在 IV拟合网格上提取。

## 逐个理解核心对象与函数

### `SurfaceGrid`（13—19 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surfaces.py:13>)

结构包含时间戳、指标名、log_moneyness横轴、DTE纵轴、二维values，另可附 fit_diagnostics。矩阵每行对应期限、每列对应横轴节点；NaN表示无支持或无法构建，不能理解成零风险。

### `build_surface_nodes`（22—46 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surfaces.py:22>)

只取 surface_eligible 且非 iv_at_solver_floor 的行；空则报错。按 datetime/product/underlying/dte/strike 分组，坐标、IV和Greeks取中位数，volume和OI求和，quote_sides计类型数。这样ATM两侧在同执行价合为一个节点，OTM通常只有一侧。最后按时点、DTE、k排序，避免依赖物理行序。

### `_total_variance_iv_grid`（49—153 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surfaces.py:49>)

仅允许快照内一个product，抽出拟合输入，把forward_price设NaN、forward_source设 underlying_price_proxy，交由 surface_fit_diagnostics.diagnose_timestamp 和默认 FitPolicy。只有SurfaceGridStatus.AVAILABLE才能出网格；收集每次尝试和每期限的方法、成功/可用状态、节点数、总方差和IV误差、各检查状态、失败代码。函数本身不实现拟合算法，算法细节应继续读 total_variance_fit 等模块笔记。

### `surface_grid`（156—200 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surfaces.py:156>)

验证 metric 为 IV/Delta/Gamma/Vega/Theta，未指定时间取节点最大时间。IV直接调用专用拟合链，传入的x_min/x_max/x_points不会控制它的正式网格。Greeks使用默认k∈[-0.2,0.2]的33点；每个已观测DTE内按k中位聚合，少于3个节点整行保留NaN，仅在原有最小最大k内np.interp。既不跨期限插值，也不向翼部外推。

### `choose_latest_complete_snapshot`（203—212 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surfaces.py:203>)

按时点统计不同DTE数和节点数，只留下至少2期限、20节点（或调用者传入门槛）的时点，取最新；无候选报错。它只检查数量，不检查拟合成功、翼部覆盖、完整Greeks网格，所以“complete”应解释成满足数量门槛。

## 关键推导、具体例子与真实边界

同一时间 $t$，一张曲面写作：

$$
\sigma_t(k,T),\qquad k=\ln(K/F),\qquad w_t(k,T)=\sigma_t(k,T)^2T.
$$

$k$ 让不同期货月份的执行价可相对比较，$T$ 是该期货对应期权剩余期限，$w$ 是该期限累计总方差。把不同时间的数据拼为一张静态曲面会把时间变化误认为空间形状；正确做法是每个 $t$ 单独建截面，多个截面再形成动态序列。

例：30天期货 $F=6000,K=6000$ 与90天期货 $F=6200,K=6200$ 都是 $k=0$；直接把执行价当横轴会把两个平值点错开。ATM call 的delta=0.51、put=-0.49，中位合并为0.01，这只是节点聚合值，不能说它是某一实际期权的Delta。Greeks也没有合约持仓方向信息，图上Gamma不是投资组合净Gamma。

> [!warning] 不要过度解释
> 多期货月份不是同一个期货合约的连续到期序列；正式日历无套利结论有模型条件。这里由诊断接口给拟合状态，不能仅凭“3D很平滑”证明无套利、可交易、预测准确或所有期限完整。

## 面试怎么讲，追问怎么答

**问：为什么IV不用np.interp？** 当前IV已接入总方差拟合与降级诊断接口，Greeks仍是展示型插值。两种算法不能合称为同一个SVI模型。

**问：某期限没有可支持的翼部怎么办？** 保留NaN，图层不连空白；比用外推伪造信息更符合已有数据证据。

## 下一步学习

[[曲面观策项目学习与面试/02-循序学习/核心02-同一时间怎样从微笑走到曲面.md|核心02-同一时间怎样从微笑走到曲面]]
