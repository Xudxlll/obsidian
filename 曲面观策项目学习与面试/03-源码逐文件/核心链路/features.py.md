---
类型: 源码教学
模块: 核心链路
源文件: "src/option_risk/features.py"
依据: 最终提交项目静态源码
---

> [!abstract] 一句话定位
> **把报价与节点变成12类可解释压力证据**。“12项证据”不等于表里只有12列，更不等于12个统计独立预测因子。

源文件：[src/option_risk/features.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/features.py:1>)。本文解释实际实现；逐字源码请结合知识库的源码档案阅读。

## 输入、输出与上下游

输入：同品种多时点 cleaned、nodes、config。输出：datetime为索引、每行一个市场时点的风险特征表，包含原始形状、期限、几何、Greeks、质量、变化量、历史阈值与标准化压力。上游不需要先生成所有正式拟合网格；下游 labels、规则状态机与可选ML复用这张表。

## 逐个理解核心对象与函数

### `_safe_divide`（30—31 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/features.py:30>)

把分母0替换为NaN后相除，避免无意义无限值。缺失不等于0；后续是否可用要看历史门槛与模型填补。

### `_term_features`（34—65 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/features.py:34>)

每时点按DTE排序，少于2期限返回期限特征NaN；对ATM IV与T=DTE/365拟合直线取斜率；近远差取最短减最长，term_inversion=max(差,0)。只关注倒挂的正向压力。

### `_geometry_features`（68—97 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/features.py:68>)

按时间、标的、期权类型、执行价、合约排序，再在各条价格曲线上计算相邻执行价差、价格差、斜率及斜率变化。call价格上升/put价格下降是单调违反；斜率下降是凸性违反。比率分母是可比较相邻差或二阶差数量，并非全部报价数。价格并未加bid-ask、成交时效或交易费用，因此指标是异常诊断。

### `_put_call_parity_features`（100—127 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/features.py:100>)

同时间/标的/DTE/K用中位close配对call和put；从重建underlying_price分组中位数取F代理，算贴现期货期权平价残差并除以F。输出有效配对数、中位/95分位/最大误差。若整个数据缺一侧，则返回仅索引的空特征表；extract后续时间特征要求对应列存在，极端输入不一定能平稳降级。

### `_calendar_variance_features`（130—151 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/features.py:130>)

将k四舍五入到小数点后2位分桶，算w=IV²T，在同时间同k桶内按DTE排后做相邻差。差小于-1e-10为违反，汇总违反比例和最大下降幅度。不同期货月份、分桶误差、同桶同DTE重复节点会影响解释，因此不是严格套利证书。

### `_surface_roughness`（154—165 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/features.py:154>)

按时间/DTE/k排序，计算相邻IV绝对跳变和二阶差绝对值，输出最大局部跳变与二阶差中位数。没有除以k间距，所以不等于数学上严格的一阶/二阶导数，也受执行价间距变化影响。

### `_hhi`（168—171 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/features.py:168>)

根据一组非负风险权重计算每时点“权重平方和/总权重平方”，等价于风险份额平方和。全零权重分母变NaN。该HHI是合约层的集中，不是机构集中度或净头寸集中。

### `extract_risk_features`（174—262 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/features.py:174>)

依次聚合报价数量、IV分位、成交持仓和地板/零成交率；在ATM/翼部带提取IV中位数构成偏斜和曲率；join期限、几何、平价、粗糙度与日历特征；以|Gamma|×非负OI、|Vega|×非负OI算HHI，再算近月/平值Gamma占比。每时点从最近DTE重建标的中位价，做pct_change。coverage按报价数/(期限数×预计每期限报价12)截上限1，data_ready检查≥20报价、≥2期限且ATM IV非缺失。最后排序并交add_temporal_features。

### `add_temporal_features`（265—322 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/features.py:265>)

对13个指标加1根和short_change_bars根差分；对全部传入特征行逐信号clip下限0，再用严格更早的最多640个特征行、最少96个该信号非缺失观测的95%分位数，并以shift(1)排除当前值。这里没有先按data_ready=True筛历史；不足20报价或不足2期限的时点，只要该信号有值，也可能贡献历史分位数。压力=当前正值/历史阈值，分母下限1e-12，压力截到25，历史缺失则压力NaN。risk_pressure为12项最大值；core_risk_pressure只取ATM IV与凸性违反率压力最大值；history_ready要求至少4项压力非空。

## 分清输入样本、历史窗口与可决策门槛

| 对象或步骤 | 实际使用范围 | 不能替换成的口径 |
|---|---|---|
|HHI、Gamma近月/平值占比|cleaned的合约行，用每份合约的Greek与OI|不是ATM/OTM合并后nodes的Greek与OI|
|零成交占比、地板占比|cleaned的合约报价行|不是nodes的行数或曲面网格缺失率|
|价格几何、Put-Call平价|cleaned报价，保留可配对两侧|不是拟合后平滑曲面|
|局部IV跳变、日历总方差|经过OTM/ATM筛选、去地板、聚合后的nodes|不是全部cleaned合约|
|历史分位阈值|全部传入features行中各信号的严格过去值，NaN/min_periods逐信号约束|不是仅data_ready历史行，也不是catalog可选时间目录|
|后续正式决策|当前data_ready与history_ready及core非缺失等门槛|这些门槛不会倒推删除先前参与rolling的值|

例如某过去时点只有18条报价，因此data_ready=False，但atm_iv=.20非缺失；该.20仍可进入后续ATM阈值的rolling。另一时点有20条报价但ATM缺失，它的atm_iv不会计入该信号的96个有效观测，却可能为其他信号提供有效历史。`history_ready`是在12项压力算完后计非缺失项数得到，不能拿它作为本轮阈值计算之前的历史过滤条件。

证据：[cleaned与nodes分工](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/features.py:179>)、[HHI输入](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/features.py:225>)、[先标data_ready再交全部features](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/features.py:255>)、[逐信号rolling未筛ready](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/features.py:293>)。

## 关键推导、具体例子与真实边界

`RISK_SIGNALS` 在14—27行完整列出12项。经济含义、计算实例与公式见 [[曲面观策项目学习与面试/02-循序学习/核心03-12项风险证据逐项算给你看.md|核心03-12项风险证据逐项算给你看]]。

这里最关键的因果式是：

$$
q_{j,t}=Q_{0.95}(x^+_{j,t-W},\ldots,x^+_{j,t-1}),\quad p_{j,t}=\min\left(25,\frac{x^+_{j,t}}{\max(q_{j,t},10^{-12})}\right),
$$

其中 $x^+=\max(x,0)$；$j$ 表示证据种类；$W=640$ 为最大历史bar数。历史门槛在至少96个有效值后才有意义。若ATM IV当前0.294、过去95%阈值0.30，压力0.98，接近正式警告边界；若阈值为0而当前是0.001，分母保护会使压力饱和25，表示“从零基线出现”，不表示精确风险增加25倍。

`surface_coverage` 实际用cleaned报价数而不是 nodes 数；由于OTM筛选、ATM合并、地板排除，它并不直接等于拟合节点覆盖率。`reference_underlying_price` 每时点选最近DTE；合约更换会造成代理价格跳跃。`underlying_return_1` 在完整features排序后使用，读者仍应注意合约滚动、非连续时间与缺bar。

> [!warning] 面试不能省略的区别
> 12个压力不是相互统计独立，代码变量 independent_pressure_signal_count 只计达到阈值的不同证据列。HHI、ATM水平和其变化、质量缺口可能相关。核心事件仅用两项，不是12项全部越线定义标签。

## 面试怎么讲，追问怎么答

**问：为什么历史分位数要shift(1)？** 如果把当前值放进阈值，异常会参与定义衡量自身的门槛；当前实现只用过去数据，更适合实时复现。

**问：Greeks数据从哪里来？** 本文件消费原始列，只做聚合、持仓加权和差分；没有在此重新使用Black模型求Greeks。

**问：全部特征都来自拟合曲面吗？** 否。几何和平价来自cleaned报价，局部跳变和日历来自nodes，正式IV拟合在展示/诊断链执行。

## 下一步学习

[[曲面观策项目学习与面试/02-循序学习/核心03-12项风险证据逐项算给你看.md|核心03-12项风险证据逐项算给你看]]


## 上游数据生成假设的原始证据

[官方数据说明PDF](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/数据说明.pdf>)物理第2页字段表：IV为年化，Theta每日衰减，Vega按波动率每变化1个百分点的价格变化；物理第3页：IV由BS模型、固定3%利率、二分法反推，Greeks用解析解，期权与标的最邻近对齐允许误差≤15分钟。可定位[字段单位摘录](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/学习拆解工作区/官方数据说明-PDF全文.txt:69>)与[生成方法摘录](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/学习拆解工作区/官方数据说明-PDF全文.txt:85>)。

项目config.py默认2%用于当前平价诊断，不是重新将所有输入IV/Greeks按2%估计。上游的最邻近对齐也意味着部分平价/凸性异常可能受时间错配影响。说明中moneyness数值定义为K/标的价格可用于坐标，附带“虚值<1/实值>1”文字不能同时适用于call和put；本项目按option_type与k方向自行选择OTM侧，不依赖该笼统文字。
