# AMA576 Algorithmic Trading 总整理

> [!info] 整理说明
> 这份笔记基于文件夹内 8 篇 Markdown 笔记重新整理。原笔记多来自课件/OCR，部分公式和表格存在识别噪声；这里按课程语义重构主线，尽量保留核心公式、策略逻辑、风险框架和复习重点。

## 1. 课程总主线

AMA576 这一组笔记可以看成一条完整的量化交易链路：

1. **市场如何运作**：连续双向拍卖、限价订单簿、报价、成交、盘口深度、价差、流动性。
2. **如何执行交易**：市价单、限价单、拆单/TWAP、参与率上限、实现成本、无前视偏差。
3. **如何寻找策略边际**：统计套利、波动率套利、做市、跨市场套利、订单流预测、价格行为识别。
4. **如何控制风险**：VaR/CVaR、尾部风险、Kelly 仓位、信用利差风险、FRTB、杠杆贷款风险。
5. **如何走向现代系统**：机器学习、深度学习、强化学习、Agent、RWA/能源资产代币化、AI 基础设施带来的能源市场变化。

一句话抓主线：

> **算法交易不是“找到一个信号”这么简单，而是把市场微观结构、交易成本、执行约束、风险资本、模型验证和合规要求全部放进同一个系统里。**

## 2. 原始笔记索引

| 原笔记                                                                                                      | 主题定位                                          | 建议阅读顺序 |
| -------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ------ |
| [[01 - Lecture 1-2 - Baseline Execution Simulator]]                                                      | 执行模拟器、CDA、LOB、三类基线执行、IS                       | 1      |
| [[02 - Lecture 3 - LOB Liquidity and Microstructure Signals]]                                            | 盘口流动性、microprice、order imbalance、impact proxy | 2      |
| [[03 - HFT Strategies Part 1 - Stat Arb Vol Arb and Market Making]]                                      | 合法 HFT 策略 Part 1：统计套利、Gamma Scalping、做市       | 3      |
| [[04 - HFT Strategies Part 2 - Cross-Venue Arb and Order Flow Prediction]]                               | 合法 HFT 策略 Part 2：跨市场套利、订单流机器学习                | 4      |
| [[05 - Quantitative Trading in Crypto Markets]]                                                          | 加密市场结构、永续合约、资金费率、Kelly、尾部风险、回测陷阱              | 5      |
| [[06 - Price Action and AI Pattern Recognition]]                                                         | 价格行为、K 线结构、交易管理、CNN/Metric Learning 图形识别      | 6      |
| [[07 - Fixed Income Pricing and Risk Analytics]]                                                         | 固定收益定价、债券风险、杠杆贷款、FRTB                         | 7      |
| [[08 - AI-Driven Quantitative Trading and Tokenized Energy Markets]]                                      | 深度学习量化、AI Agent、能源冲击、RWA/tokenized energy     | 8      |

## 3. 市场微观结构：从 CDA 到 LOB

### 3.1 连续双向拍卖 CDA

连续双向拍卖是现代交易所撮合机制的基础：

- 买方和卖方可以持续提交订单。
- 当买方愿意支付的价格不低于卖方报价时，交易立即发生。
- 限价订单提供流动性，市价/可成交订单消耗流动性。
- 撮合规则通常遵循 **价格优先、时间优先**：
  - 买单价格越高越优先；
  - 卖单价格越低越优先；
  - 同价位按先来先服务。

这解释了算法交易最核心的执行取舍：

> **想马上成交，就要付出价差和冲击成本；想要价格更好，就要承担不成交、排队和错过行情的风险。**

### 3.2 限价订单簿 LOB

订单簿的关键变量：

| 概念 | 含义 | 交易意义 |
|---|---|---|
| Best Bid | 当前最高买价 | 卖出时最容易成交的参考价 |
| Best Ask | 当前最低卖价 | 买入时最容易成交的参考价 |
| Spread | `Ask - Bid` | 即时成交成本，越大越贵 |
| Midprice | `(Ask + Bid) / 2` | 常用的“公平价格”近似 |
| Depth | 各价位挂单量 | 衡量大单是否会穿透盘口 |
| Queue Position | 排队位置 | 决定限价单成交概率 |

买入市价单通常吃 ask 端流动性，因此相对 mid 的即时成本约为：

$$
\text{cost vs mid}=a_t-m_t=\frac{s_t}{2}
$$

如果下单量超过最优 ask 的数量，就会继续吃更高价位的 ask，形成 **walking the book**，平均成交价随交易量上升。

### 3.3 Quotes vs Trades

- **Trades** 记录已经发生的成交：成交价、成交量、时间、主动买卖方向。
- **Quotes/LOB** 描述下一刻可以交易的流动性：bid/ask 价格、挂单量、盘口层级。

执行质量不能只看历史成交价，因为真实交易面对的是订单簿：

> 回测里看起来能在 mid 成交，不代表真实世界能在 mid 成交。

### 3.4 重要盘口信号

**Quoted spread 与 Effective spread**

$$
\text{Effective spread}=2\left|p_{\mathrm{trade}}-m_t\right|
$$

quoted spread 是“报价机会”，effective spread 是你实际成交付出的成本。

**Microprice**

$$
p_t^{\mathrm{micro}}
=\frac{a_t q_t^b+b_t q_t^a}{q_t^b+q_t^a}
$$

直觉：

- bid size 远大于 ask size：买方深度更强，microprice 更接近 ask，表示上行压力。
- ask size 远大于 bid size：卖方深度更强，microprice 更接近 bid，表示下行压力。

**Order Imbalance**

$$
\mathrm{OI}_t=\frac{q_t^b-q_t^a}{q_t^b+q_t^a}
$$

- `OI > 0`：买盘深度更强。
- `OI < 0`：卖盘深度更强。
- 对买入执行来说，强正 OI 往往意味着未来价格可能上移，应该更主动；强负 OI 可能允许更耐心地挂限价。

**Impact Proxy**

$$
\Delta p \approx \lambda \frac{q}{V}
$$

交易量 `q` 相对市场成交量/深度 `V` 越大，临时冲击越大。这就是参与率上限和拆单执行的基础。

## 4. 执行模拟器与评估纪律

### 4.1 三个执行基线

在买入 `Q = 1000` 的任务中，原笔记定义了三个 baseline：

| 方法 | 规则 | 优点 | 缺点 |
|---|---|---|---|
| Market All | 下一可行时刻全部市价买入 | 成交确定、速度快 | 支付 spread/slippage，冲击可能大 |
| Limit Single | 以 `P0 * (1 - δ)` 挂买入限价，在窗口 `W` 内等待 | 可能获得价格改善 | 可能不成交，且错过上涨 |
| Split/TWAP-like | 将 `Q` 拆成 `N` 份逐分钟执行 | 降低单次冲击 | 多次支付成本，暴露于市场漂移 |

限价单的基线成交规则：

$$
\begin{aligned}
L &= P_{t_0}(1-\delta),\\
\min_{t_0+1\le t\le t_0+W}\mathrm{Low}_t &\le L
\end{aligned}
$$

拆单平均成交价：

$$
\bar{p}_{\mathrm{exec}}
=\frac{1}{Q}\sum_i q_i P_{t_i}(1+\mathrm{slippage})
$$

### 4.2 Implementation Shortfall

实现成本是执行评估的核心：

$$
\mathrm{IS}=Q(\bar{p}_{\mathrm{exec}}-p_{\mathrm{arrival}})
$$

对于买单：

- `IS > 0`：平均成交价高于决策价，执行变贵。
- `IS < 0`：平均成交价低于决策价，执行更好。

直觉分解：

$$
IS \approx \mathrm{spread} + Impact + Drift
$$

- **Spread**：为即时性支付的价差。
- **Impact**：自己的交易推动价格。
- **Drift**：等待过程中市场本身移动。

### 4.3 无前视偏差

执行模拟器最重要的纪律：

> 在 `t` 时刻做决策，必须在 `t+1` 或之后成交，不能用 `t` 的 close 生成信号又在 `t` 的 close 成交。

正确回测应明确：

- 决策时间；
- 可用信息集合；
- 执行延迟；
- 成交规则；
- 未成交处理；
- 交易成本、滑点和市场冲击。

### 4.4 自适应执行作业的核心

课程作业要求构建一个 signal-driven adaptive execution policy：

- 至少使用两个 OHLCV 信号，例如 rolling volatility、volume z-score、trend proxy。
- 每分钟决定：
  - 市价单数量；
  - 限价单数量；
  - 限价激进程度 `α_t`。
- 约束：
  - 无前视；
  - 参与率上限 `q_t <= CAP * volume_t`；
  - 输出逐分钟 trade log；
  - 与 market all、split n10、limit single 对比。

## 5. 合法 HFT 策略版图

原 HFT 两篇笔记覆盖五类合法策略：

| 策略 | 核心机制 | 单笔利润 | 胜率 | 延迟要求 | 主要风险 |
|---|---|---:|---:|---|---|
| Statistical Arbitrage | 协整价差均值回复 | 5-50 bps | 55-65% | 中高 | regime/correlation breakdown |
| Volatility Arbitrage | IV 与 RV 差异，Gamma Scalping | 10-100 bps | 50-60% | 高 | theta decay、gap risk |
| Market Making | 双边报价赚 spread | 0.5-5 bps | 51-75% | 极高，常 <1μs | adverse selection、inventory risk |
| Cross-Venue Arbitrage | 跨交易所价格差 | 1-10 bps | 70-85% | 极高，μs 级 | execution risk、latency creep |
| Order Flow Prediction | L2 订单簿和订单流 ML 预测 | 2-20 bps | 52-58% | 100-500ms | overfitting、regime change |

### 5.1 统计套利：Pairs Trading

核心思想：

> 两个有经济联系且协整的资产，短期可能偏离，长期价差应回到均值。

流程：

1. 选择经济上相关的资产对。
2. 用 OLS 得到 hedge ratio。
3. 对残差做 ADF，确认 residual stationary。
4. 将 spread 建模为 OU 过程。
5. 用 z-score 触发入场/出场。

关键公式：

$$
\begin{aligned}
P_{B,t} &= \beta_0+\beta_1 P_{A,t}+u_t,\\
\mathrm{spread}_t &= P_{B,t}-(\beta_1P_{A,t}+\beta_0),\\
z_t &= \frac{\mathrm{spread}_t-\mu_{\mathrm{spread}}}{\sigma_{\mathrm{spread}}},\\
dS_t &= \lambda(\mu-S_t)\,dt+\sigma\,dW_t,\\
t_{1/2} &= -\frac{\ln 2}{\lambda}
\end{aligned}
$$

交易规则示例：

- `z > +2`：short spread，卖出相对高估腿、买入低估腿。
- `z < -2`：long spread，买入相对低估腿、卖出高估腿。
- `z ≈ 0`：平仓。
- `|z| > 3.5`：止损，防止关系失效。

重点风险：

- 协整关系永久失效；
- 压力期相关性崩溃；
- 策略拥挤导致 edge 消失；
- hedge ratio 需要 rolling re-estimation。

### 5.2 波动率套利：Gamma Scalping

核心思想：

> 当期权隐含波动率 IV 低于未来实现波动率 RV 时，买入期权并动态 delta hedge，靠标的波动赚 gamma，付出 theta。

核心 P&L：

$$
\text{Delta-hedged P\&L}
\approx \frac{1}{2}\Gamma(\Delta S)^2-\Theta\,\Delta t
$$

流程：

1. 筛选 `IV < expected RV` 的期权。
2. 买入 ATM straddle，初始 delta 约等于 0。
3. 当 `|Δ|` 超过阈值时调仓：
   - 标的上涨后卖出 underlying；
   - 标的下跌后买入 underlying。
4. 监控 gamma gain 是否覆盖 theta decay。
5. IV 回归、接近到期、触发止损时退出。

核心风险：

- RV 低于 IV，gamma 收益覆盖不了 theta；
- 临近到期 pin risk；
- 隔夜 gap 绕过 delta hedge；
- 交易频率过高会被成本吃掉。

### 5.3 做市：Market Making

做市的经济角色是提供双边报价、赚取买卖价差。策略成功依赖：

- 速度；
- 库存控制；
- 订单流识别；
- 规模和品种分散。

Avellaneda-Stoikov 模型核心：

$$
\begin{aligned}
r(s,q,t) &= s-q\gamma\sigma^2(T-t),\\
\delta &= \gamma\sigma^2(T-t)+\frac{2}{\gamma}\ln\left(1+\frac{\gamma}{\kappa}\right),\\
\mathrm{Ask} &= r+\delta,\\
\mathrm{Bid} &= r-\delta
\end{aligned}
$$

含义：

- `q > 0` 长库存时，reservation price 下移，报价整体偏低，鼓励卖出库存。
- `q < 0` 短库存时，reservation price 上移，报价整体偏高，鼓励买回库存。
- `κ` 表示订单到达强度，影响最佳价差。

关键风险：

- **Adverse Selection**：被 informed trader 打掉 stale quote。
- **Inventory Risk**：单边成交导致库存堆积。
- **Technology Failure**：系统故障可能在毫秒内造成灾难性损失。

### 5.4 跨市场套利：Cross-Venue Arbitrage

核心思想：

> 同一资产在两个 venue 出现价格差，低买高卖，在差价消失前完成两腿交易。

关键公式：

$$
\begin{aligned}
\delta(t) &= P_A(t)-P_B(t+\tau),\\
\pi_{\mathrm{net}} &= Q\left(\delta-c_A-c_B-\frac{s_A}{2}-\frac{s_B}{2}-I\right),\\
\delta(t) &= \delta_0 e^{-\lambda t},\\
t^* &= \frac{1}{\lambda}\ln\left(\frac{\delta_0}{C_{\mathrm{total}}}\right)
\end{aligned}
$$

交易可行条件：

$$
\begin{aligned}
\delta(t) &> C_{\mathrm{total}},\\
\tau_{\mathrm{total}} &< t^*
\end{aligned}
$$

要点：

- 微秒级 latency advantage 决定策略是否存在；
- co-location、DMA、FPGA、低延迟行情源是基础设施；
- 小差价经常被手续费、半价差、冲击和失败腿风险吃掉；
- 两腿必须尽可能原子化，否则会出现 directional exposure。

### 5.5 订单流预测：Order Flow ML

目标：

> 用 L2 order book、tick trades、VPIN、trade intensity、momentum 等特征，预测未来 10-500ms 的 mid-price 方向。

关键特征：

$$
\begin{aligned}
\mathrm{OBI}_t &= \frac{V_t^b-V_t^a}{V_t^b+V_t^a},\\
\mathrm{VPIN}_t &= \frac{|V_{\mathrm{buy},t}-V_{\mathrm{sell},t}|}{V_{\mathrm{total},t}},\\
\lambda(t) &= \mu+\sum_{t_i<t}\alpha e^{-\beta(t-t_i)},\\
\mathrm{Momentum}_t(k) &= \frac{P_t-P_{t-k}}{P_{t-k}}
\end{aligned}
$$

模型：

- Random Forest：解释性较好、推理快，适合作 baseline 和特征筛选。
- LSTM：能捕捉序列依赖，但训练慢、调参敏感。
- XGBoost：表格特征强、生产常用，但依赖特征工程。
- Ensemble：通常比单模型更稳健。

验证纪律：

- walk-forward validation；
- purging and embargo；
- 真实交易成本；
- 模型漂移监控；
- rolling retraining；
- OOS accuracy 不需要很高，53%-58% 在高频环境已可能有价值，但必须扣成本看 Sharpe。

## 6. Crypto Quant：加密市场的特殊性

### 6.1 Crypto 为什么适合 Quant

加密市场的特殊结构：

- 24/7 交易，没有传统收盘；
- retail-heavy order flow；
- CEX/DEX 流动性高度碎片化；
- 非平稳、厚尾、波动聚集；
- 永续合约和资金费率是核心机制；
- DeFi 引入 MEV、gas、智能合约风险。

### 6.2 CeFi 与 DeFi

| 维度 | CeFi | DeFi |
|---|---|---|
| 机制 | 中心化撮合 CLOB | AMM 或链上 CLOB |
| 优点 | 低延迟、高吞吐、API 成熟 | 透明、可审计、无托管 |
| 风险 | 交易所/托管/监管风险 | 智能合约、MEV、gas、链上延迟 |
| 策略关注 | LOB、maker/taker、跨所套利 | MEV、防夹、池子深度、链上流动性 |

### 6.3 Maker/Taker 与成本门槛

maker 提供流动性，可能获得 rebate，但承担 adverse selection。

taker 获得即时成交，但支付 taker fee 和 spread。对于高换手策略：

> gross alpha 必须超过 round-trip fee、spread、slippage 和 impact，才是真正有 edge。

### 6.4 永续合约与 Funding Rate

永续合约没有到期日，靠 funding rate 将 perp price 拉回 spot。

当 perp 高于 spot：

- longs pay shorts；
- arbitrageur 可以 short perp + long spot；
- 收 funding，并赌 basis 收敛。

Funding rate 可建模为 OU：

$$
\begin{aligned}
dr(t) = \kappa(\mu - r(t))dt + \sigmadW(t) \\
t_{1/2} = \ln(2) / \kappa
\end{aligned}
$$

实际限制：

- 保证金占用；
- 借贷成本；
- 交易费用；
- 跨所/链上结算延迟；
- 极端行情下 funding 与 basis 可持续偏离。

### 6.5 Crypto 风险管理

Crypto 不适合简单高斯 VaR：

- excess kurtosis 高；
- crash skew 明显；
- volatility clustering；
- 压力期相关性失效。

更合适的工具：

- CVaR / Expected Shortfall；
- Extreme Value Theory；
- power-law tail；
- stress testing；
- fractional Kelly。

Kelly 连续近似：

$$
f^*= \mu / \sigma^2
$$

实务中常用 Half-Kelly，因为参数估计误差会放大过度下注风险。

### 6.6 回测红旗

原 crypto 笔记强调：回测默认会骗人。需要警惕：

- in-sample Sharpe > 3 且无合理解释；
- 没有 walk-forward；
- 没有交易成本；
- 参数网格过大；
- survivorship bias；
- look-ahead bias；
- 多重检验没有修正；
- mid-price fill 假设过度乐观。

## 7. Price Action 与 AI 图形识别

### 7.1 基本分析 vs 技术分析

| 方法 | 回答的问题 | 关注点 |
|---|---|---|
| Fundamental Analysis | 该不该交易这个资产 | 宏观、行业、公司/资产、估值情景 |
| Technical Analysis | 什么时候交易 | 趋势、结构、动量、均值回复、量能、波动 |

交易工作流：

1. 定义目标和时间周期。
2. 理解交易标的和流动性。
3. 形成交易假设。
4. 预设入场、目标、失效点。
5. 决定风险和仓位。
6. 执行。
7. 按规则管理。
8. 退出并复盘。

### 7.2 Price Action 的核心观点

Price Action 不只是背 K 线形态，而是读市场参与者在压力下的行为：

- 最新价格代表最新供需共识；
- OHLC K 线比单个 close 信息密度更高；
- 影线显示拒绝和波动；
- 趋势、通道、支撑阻力、突破失败比孤立的“十字星/锤子线”更重要；
- 单个 candlestick pattern 大多接近 coin flip，不能单独作为交易系统。

### 7.3 常见结构

| 结构 | 含义 | 交易思路 |
|---|---|---|
| Trading Range | 市场认为区间内价格大致公平 | 低买高卖，突破失败后回到区间 |
| Always In | 强趋势、紧通道、少回调 | 顺势，即使小仓位也不要逆势硬打 |
| Trend | HH/HL 或 LH/LL 持续 | 顺势做 pullback |
| Breakout | 突破支撑/阻力 | 未确认前警惕失败，确认后顺突破方向 |
| Channel | 两条平行线约束价格 | 观察 overshoot/undershoot 和回测 |
| Support/Resistance | 买方/卖方可能增强的位置 | 支撑买、阻力卖，但要结合 context |
| Measured Move | Leg1 ≈ Leg2 | 在目标附近止盈或反向 scalp |
| Double Top/Bottom | 测试前高/前低失败 | 反向交易 |
| Triangle | 三次推升/下压后的横盘 | breakout mode，等待方向 |
| Rounded Top/Bottom | 逐渐减速的反转 | 本质仍要看 wedge、pullback、climax 等结构 |

### 7.4 Trader's Equation

任何交易都应满足数学期望：

$$
P(\mathrm{win}) \cdot \mathrm{Reward} > P(\mathrm{loss}) \cdot \mathrm{Risk}
$$

重点：

- 早入场：风险小、盈亏比好，但胜率低。
- 晚入场：胜率高，但价格更差、盈亏比下降。
- 没有完美形态，所有 pattern 都可能失败。
- stop 不是心理价位，应该真实放入市场。

### 7.5 Trade Management

交易管理的三件事：

- 为什么进场：必须有正期望理由；
- 目标在哪里：profit target；
- 错了怎么办：protective stop。

课程中特别强调：

> Stop protects you from yourself.

没有 stop 时，交易者容易因为情绪让亏损扩大。所谓 “other people's money” 也不应改变风控逻辑：进入账户后就是自己的风险资本，必须根据当前 price action 管理。

### 7.6 AI Pattern Recognition

AI 图形识别的三类应用：

1. 实时监控价格图，出现目标形态时报警。
2. 分析历史形态，判断 continuation/reversal，并研究后续走势。
3. 股票/品种筛选，找到与某类结构相似的标的。

CNN 的优势：

- 卷积核可学习局部 K 线片段；
- 深层网络可组合成更复杂形态；
- 可用灰度 K 线图或多通道输入，如时间周期、成交量、指标。

训练注意：

- 将 K 线序列切成固定尺寸图像；
- 每类经典 pattern 需要足够样本；
- 需要归一化价格尺度；
- 增强时避免破坏 K 线语义的几何变换；
- 数据集可按 `70/20/10` 切分 train/validation/test。

两类学习方式：

- **Supervised Learning**：学习输入到固定 pattern label 的映射，适合经典形态分类。
- **Metric Learning**：学习相似度空间，适合用户自定义、不断演化的形态搜索。

## 8. 固定收益定价与风险分析

### 8.1 Quant Finance 在资本市场中的位置

固定收益笔记补充了算法交易之外的定价与风险视角：

- Asset Pricing；
- Risk Management；
- Portfolio Management；
- Model Validation；
- Compliance；
- Low-latency System；
- Market Risk、Credit Risk、Liquidity Risk、IRRBB、xVA。

这说明量化能力不只服务于交易信号，也服务于估值、风险资本和监管报告。

### 8.2 利率期限结构

零息债定价：

$$
\begin{aligned}
\text{Continuous compounding:}\quad
B(t,T) &= e^{-r(t,T)(T-t)},\\
\text{Simple compounding:}\quad
B(t,T) &= \frac{1}{1+R(t,T)(T-t)}
\end{aligned}
$$

期限结构 `r(0, T_i)` 或 discount factor curve `B(0, T_i)` 可用于：

- 折现固定现金流；
- 估值浮动现金流；
- 债券、swap、结构化产品定价；
- 风险敏感度计算。

曲线构建：

- Money market、Eurodollar futures、swaps；
- RFR futures、RFR swaps；
- Par bond；
- bootstrapping + interpolation；
- 也可用 global fitting。

### 8.3 债券估值与敏感度

债券风险指标：

- yield；
- duration；
- modified duration；
- convexity；
- Z-spread；
- asset swap spread；
- PV01/DV01；
- CS01。

价值变化可按 Taylor expansion 理解：

$$
\begin{aligned}
\Delta V \approx\;&
\Theta\,\Delta t
\;+\;\Delta_{\mathrm{IR}}\Delta \mathrm{IR}
\;+\;\Delta_{\mathrm{CS}}\Delta \mathrm{CS}\\
&+\frac{1}{2}\Gamma\text{-terms}
\;+\;\text{cross-gamma terms}
\end{aligned}
$$

风险报告通常包括：

- market value；
- DV01 / CS01；
- one-day 99% VaR；
- 10-day stressed VaR；
- stress scenarios，如 2008 crisis、liquidity stress。

### 8.4 Leveraged Loan

杠杆贷款特征：

- 发行人通常低于投资级；
- senior secured；
- floating rate，如 LIBOR/SOFR + spread；
- covenants；
- callable；
- settlement 较慢，带来 counterparty/PFE 风险；
- 是 CLO 的主要抵押资产。

风险关注：

- rating；
- yield to maturity；
- weighted average life；
- historical VaR；
- PFE；
- default risk captured by CDR；
- prepayment/call captured by CPR；
- CLO 估值依赖资产现金流生成。

### 8.5 FRTB 与信用利差风险

FRTB 是交易账簿监管资本框架，SA 包括：

- Sensitivities-based Method；
- Default Risk Charge；
- Residual Risk Add-on。

非证券化信用利差风险 CSR 的 delta sensitivity 可理解为：

$$
CS01 = [V(cs + 1bp) - V(cs)] / 0.0001
$$

风险暴露要按 credit quality、sector、bucket 分组，并在监管公式下聚合资本。

## 9. AI-Driven Quant、能源市场与 RWA

### 9.1 深度学习在期权定价和波动预测中的角色

笔记中的关键观点：

- MLP 可在非线性期权定价中大幅降低相对 Black-Scholes 的误差。
- LSTM 从历史窗口学习 volatility dynamics，尤其适合较长期权和时间依赖结构。
- CNN-LSTM 可同时捕捉局部 LOB 特征和序列依赖。
- LSTM-HIT 结合：
  - high-frequency realized volatility；
  - technical indicators；
  - GARCH/HAR 等传统模型参数。
- LSTM-HIT-EVT 将 EVT 引入尾部风险，改善 VaR 预测。
- Transformer、GNN、multi-task learning、RL 分别对应长依赖、跨资产关系、多目标预测和动态执行/对冲。

### 9.2 Autonomous AI Trading Systems

Agent 架构一般包括：

- News Agent：处理财报、公告、监管文件、社交媒体情绪。
- Strategy Agent：结合监督学习、历史 pattern 和 RL 生成交易建议。
- Risk Manager：控制仓位、敞口、止损和合规。
- Backtest Agent：批量测试策略变体。

Quantamental 框架是把：

- 价格
- 订单簿
- 新闻叙事
- 情绪
- 链上数据
- 波动状态

整合成统一信号，并根据 regime 调整仓位。

### 9.3 AI 与能源市场

AI 基础设施推动能源需求：

- 数据中心单位面积能耗显著高于普通商业建筑；
- GPU/rack 级别能耗与冷却需求高；
- 数据中心可能向能源丰富区域迁移；
- 电力、核能、可再生、储能、输电基础设施成为 AI 产业瓶颈。

能源冲击案例：

| 事件 | 市场性质 | 策略含义 |
|---|---|---|
| Iraq War 2003 | 短期风险溢价，均值回复 | 可考虑短期波动/mean reversion |
| Russia-Ukraine War | 供应链和地缘结构重塑，永久性 regime shift | 需要趋势、重估相关性、模型重训和压力测试 |

### 9.4 Tokenized Energy / RWA

能源资产代币化的核心：

- 用 token 表示物理原油、天然气、电力、可再生能源证书、碳信用、能源基础设施收益权；
- 分割所有权，降低参与门槛；
- 24/7 交易和即时结算；
- smart contract 自动处理 KYC/AML、分红、赎回、合规限制；
- oracle 和 Proof of Reserve 验证实物资产支持；
- institutional custody、cross-chain bridge 和合规框架是基础设施。

对量化交易的启发：

- tokenized liquidity 可能带来新的跨市场套利；
- oracle price 与传统市场价格之间会形成基差和延迟；
- RWA 交易结合了传统商品基本面、链上机制和市场微观结构；
- 合规和资产托管风险与模型风险同等重要。

## 10. 关键公式速查

| 模块 | 公式 | 含义 |
|---|---|---|
| Spread | $s_t=a_t-b_t$ | 最优卖价与买价差 |
| Midprice | $m_t=\frac{a_t+b_t}{2}$ | 盘口中间价 |
| Effective Spread | $2\lvert p_{\mathrm{trade}}-m_t\rvert$ | 实际成交成本 |
| Microprice | $p_t^{\mathrm{micro}}=\frac{a_tq_t^b+b_tq_t^a}{q_t^b+q_t^a}$ | 深度加权价格压力 |
| Order Imbalance | $\mathrm{OI}_t=\frac{q_t^b-q_t^a}{q_t^b+q_t^a}$ | 买卖盘深度偏斜 |
| Impact Proxy | $\Delta p\approx\lambda\frac{q}{V}$ | 交易参与率导致的价格冲击 |
| IS | $\mathrm{IS}=Q(\bar p_{\mathrm{exec}}-p_{\mathrm{arrival}})$ | 实现成本 |
| OU | $dS_t=\lambda(\mu-S_t)\,dt+\sigma\,dW_t$ | 均值回复过程 |
| Half-life | $t_{1/2}=-\frac{\ln 2}{\lambda}$ 或 $t_{1/2}=\frac{\ln 2}{\kappa}$ | 均值回复速度 |
| Z-score | $z_t=\frac{\mathrm{spread}_t-\mu_{\mathrm{spread}}}{\sigma_{\mathrm{spread}}}$ | 统计套利入场信号 |
| Gamma P&L | $\frac{1}{2}\Gamma(\Delta S)^2-\Theta\,\Delta t$ | Gamma scalping 收益分解 |
| A-S Reservation Price | $r(s,q,t)=s-q\gamma\sigma^2(T-t)$ | 库存调整后的做市中心价 |
| Cross-Venue Profit | $\pi_{\mathrm{net}}=Q(\delta-C_{\mathrm{cost}}-I)$ | 跨市场套利净利润 |
| Signal Decay | $\delta(t)=\delta_0e^{-\lambda t}$ | 套利窗口衰减 |
| OBI | $\mathrm{OBI}_t=\frac{V_t^b-V_t^a}{V_t^b+V_t^a}$ | 订单流 ML 特征 |
| VPIN | $\mathrm{VPIN}_t=\frac{\lvert V_{\mathrm{buy},t}-V_{\mathrm{sell},t}\rvert}{V_{\mathrm{total},t}}$ | informed trading proxy |
| Kelly | $f^*=\frac{\mu}{\sigma^2}$ | 理论最优仓位比例 |
| Bond DF | $B(t,T)=e^{-r(t,T)(T-t)}$ | 零息债折现因子 |
| CS01 | $\mathrm{CS01}=\frac{V(cs+1\mathrm{bp})-V(cs)}{0.0001}$ | 信用利差敏感度 |
| Trader's Equation | $P(\mathrm{win})\cdot\mathrm{Reward}>P(\mathrm{loss})\cdot\mathrm{Risk}$ | 交易正期望条件 |

## 11. 从研究到上线：统一检查清单

### 11.1 数据

- 数据是否包含 survivorship bias？
- 时间戳是否统一？
- quotes 和 trades 是否同步？
- 是否有 L1/L2 深度？
- 是否能区分 maker/taker 成本？
- 是否有 corporate action、funding、borrow cost、fee schedule？

### 11.2 信号

- 信号是否有经济解释？
- 是否在扣成本后仍有 edge？
- 信号 horizon 是否与执行速度匹配？
- 是否存在 crowding？
- 是否会在 regime shift 下失效？

### 11.3 回测

- 决策时间和执行时间是否分离？
- 是否显式加入 lag？
- 是否有 slippage、spread、impact？
- 是否使用 walk-forward？
- 是否做 OOS？
- 是否控制 multiple testing？
- 是否用 Deflated Sharpe 或类似方法检验过拟合？

### 11.4 执行

- 市价、限价、拆单规则是否明确？
- fill assumption 是否保守？
- 是否有 participation cap？
- 是否考虑 partial fill？
- 是否输出 trade log？
- 是否能从 IS、fill rate、completion time 三个维度比较策略？

### 11.5 风险

- 是否设置 hard stop 和 kill switch？
- 是否监控 VaR/CVaR/stress loss？
- 是否控制库存、杠杆、集中度和流动性？
- 是否监控模型漂移？
- 是否建立合规日志与时间戳记录？

## 12. 复习路线

建议按下面方式复习：

1. **先建立市场结构**：读 Lecture 1-3，画出 CDA、LOB、spread、depth、microprice、OI 的关系。
2. **再看执行评估**：重点掌握 IS、无前视、三类 baseline、participation cap。
3. **再看策略家族**：把五类 HFT 策略用“edge 来源、成本来源、风险来源”三列重写一遍。
4. **再看加密市场**：理解 CEX/DEX、perp funding、碎片化流动性、厚尾风险。
5. **再看风险资本**：固定收益笔记中的 DV01/CS01/VaR/FRTB 是风险管理视角，不是孤立内容。
6. **最后看 AI/RWA**：把深度学习、Agent、tokenized energy 作为“未来市场结构变化”来理解。

## 13. 最容易混淆的点

- **Correlation 不是 Cointegration**：相关性高不代表价差会均值回复。
- **Backtest PnL 不是 Tradable PnL**：必须扣 spread、fee、slippage、impact。
- **Accuracy 不是 Profitability**：订单流预测 57% accuracy 可能赚钱，也可能被成本吃掉。
- **Pattern 不是 Edge**：K 线形态只有结合概率、盈亏比、止损和 context 才可能成为策略。
- **VaR 不是最大损失**：厚尾市场中，VaR 之外的损失需要 CVaR/EVT/stress test。
- **Latency Edge 不是永恒**：交易所规则、竞争基础设施、speed bump 都可能关闭套利窗口。
- **AI 模型不是免检**：非平稳、过拟合、数据泄漏和模型漂移仍然是核心风险。

## 14. 一页总复盘

> [!summary] 总结
> - **市场结构**：CDA 和 LOB 决定 spread、depth、queue、fill probability，也决定执行成本。
> - **执行核心**：Market/Limit/Split 是所有复杂执行算法的基线；评估必须看 IS、fill rate、completion time。
> - **策略核心**：合法 HFT 不是操纵市场，而是利用真实低维 inefficiency：均值回复、vol mispricing、spread capture、venue fragmentation、order flow predictability。
> - **风险核心**：每个 edge 都对应一个失败模式。Stat arb 怕 regime break，Gamma scalping 怕 theta/gap，MM 怕 adverse selection，cross-venue 怕 latency/execution，ML 怕 overfitting。
> - **现代扩展**：Crypto、AI Agent、tokenized energy/RWA 把交易从传统交易所扩展到 24/7、多链、多资产、多数据源环境，但执行成本、风险和合规没有消失，只是换了形态。
