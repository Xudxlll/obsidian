---
类型: 源码教学
模块: 核心链路
源文件: "src/option_risk/quality.py"
依据: 最终提交项目静态源码
---

> [!abstract] 一句话定位
> **确定性清洗并保留数据质量证据**。“删除坏行”与“保留可疑行供诊断”被有意分开。

源文件：[src/option_risk/quality.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/quality.py:1>)。本文解释实际实现；逐字源码请结合知识库的源码档案阅读。

## 输入、输出与上下游

输入：io.py 已加 datetime/product/source_file 的报价表与 PipelineConfig；输出：按 datetime、underlying、strike、option_type 排序的 cleaned 和质量 profile。cleaned 供报价级几何/流动性特征使用；其中 surface_eligible 且不是求解下限的子集才进入 surface_nodes。

## 逐个理解核心对象与函数

### `clean_and_profile`（29—146 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/quality.py:29>)

先复制输入并重算品种，按 `(datetime, contract)` 保留第一行去重，然后对价格、成交、持仓、IV、Greeks、DTE等做数值转换，失败变 NaN。核心字段任一缺失、错误品种、非 call/put、停牌标记非0、价格关系不合法、IV/Delta/Gamma/Vega/DTE/moneyness越界共同构成 quality_exclusion。求解下限单独用 np.isclose(atol=1e-8,rtol=0) 标记，不直接排除。保留行统一类型，计算 log_moneyness、年化期限、重建标的价格，建立 surface_eligible。profile 报告去重数、保留率、求解下限率与各排除原因的重叠前计数。

## 关键推导、具体例子与真实边界

核心字段在10—26行；排除规则在64—101行：$K>0$、$C\ge0$、$H\ge L$、$L\le O,C\le H$；$0.0005\le IV\le5$，$-1.0001\le\Delta\le1.0001$、$\Gamma\ge0$、$Vega\ge0$；DTE 2—180；moneyness 0.7—1.3。上下界使用闭区间。Theta没有经济范围筛选；volume/amount/OI负值也没有被统一排除。

设输入 moneyness 定义为 $m=K/F$，则：

$$
k=\ln m,\qquad T=\frac{DTE}{365},\qquad \widehat F=\frac K m.
$$

$K$ 是执行价，$F$ 是标的期货价格代理，$T$ 是以年计的到期时间。例：$K=6000,m=1.02$，重建 $\widehat F=5882.35$，$k\approx0.01980$，属于 ATM 带。这个重建依赖数据中 moneyness 定义，不能独立证明真实可交易价格。

虚值筛选：$|k|\le0.03$ 保留看涨看跌两侧；$k<-0.03$ 仅选 put；$k>0.03$ 仅选 call。深度实值报价仍可保留在 cleaned 供特征使用，只是不组成节点。IV 等于求解器地板的记录可合法通过 IV 区间，但之后建曲面时排除，同时 floor_share 仍衡量其占比。

> [!warning] 真实边界
> 去重保留 first，没有按来源可信度选择；原因计数可重叠，不能相加求总删除数；OHLC不全在 CORE_REQUIRED，OHLC 的 NaN 比较可能全为 False。此函数没有检查每一字段有限性、每个 bid-ask、合约乘数或全部交易所微观约束。

## 面试怎么讲，追问怎么答

**问：为什么不把求解下限记录全部删掉？** 若删掉，丢失的是可疑程度本身；当前设计让它们参与质量与流动性证据，但不污染拟合节点。

**问：清洗后一定无套利吗？** 否。清洗保证基本范围与关系；凸性、平价、日历一致性在特征层做诊断，IV拟合另有质量检查。

## 下一步学习

[[曲面观策项目学习与面试/02-循序学习/核心01-从一条期权报价到可分析的干净样本.md|核心01-从一条期权报价到可分析的干净样本]]


## 上游数据生成假设的原始证据

[官方数据说明PDF](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/数据说明.pdf>)物理第2页字段表：IV为年化，Theta每日衰减，Vega按波动率每变化1个百分点的价格变化；物理第3页：IV由BS模型、固定3%利率、二分法反推，Greeks用解析解，期权与标的最邻近对齐允许误差≤15分钟。可定位[字段单位摘录](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/学习拆解工作区/官方数据说明-PDF全文.txt:69>)与[生成方法摘录](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/学习拆解工作区/官方数据说明-PDF全文.txt:85>)。

项目config.py默认2%用于当前平价诊断，不是重新将所有输入IV/Greeks按2%估计。上游的最邻近对齐也意味着部分平价/凸性异常可能受时间错配影响。说明中moneyness数值定义为K/标的价格可用于坐标，附带“虚值<1/实值>1”文字不能同时适用于call和put；本项目按option_type与k方向自行选择OTM侧，不依赖该笼统文字。
