

> [!info] 整理说明
> 这份笔记基于此前的 8 篇 Markdown 笔记重新整理。原笔记多来自课件/OCR；下方索引保留来源主题，这些原始 Markdown 文件目前不在本文件夹中，可在课程资料目录查阅对应课件。

## 1. 课程总主线

AMA576 这一组笔记可以看成一条完整的量化交易链路：

1. **市场如何运作**：连续双向拍卖、限价订单簿、报价、成交、盘口深度、价差、流动性。
2. **如何执行交易**：市价单、限价单、拆单/TWAP、参与率上限、实现成本、无前视偏差。
3. **如何寻找策略边际**：统计套利、波动率套利、做市、跨市场套利、订单流预测、价格行为识别。
4. **如何控制风险**：VaR/CVaR、尾部风险、Kelly 仓位、信用利差风险、FRTB、杠杆贷款风险。
5. **如何走向现代系统**：机器学习、深度学习、强化学习、Agent、RWA/能源资产代币化、AI 基础设施带来的能源市场变化。

一句话抓主线：

> **算法交易不是“找到一个信号”这么简单，而是把市场微观结构、交易成本、执行约束、风险资本、模型验证和合规要求全部放进同一个系统里。**

> [!info] 课堂代码位置
> 两份课堂 Notebook 的原始代码已直接收录在本文：[[#3.5 Lecture 3–4：订单簿与执行信号课堂代码|订单簿与执行信号]]，以及 [[#4.5 Lecture 1–2：课堂执行模拟代码|执行模拟器]]。单元按各自原文件顺序排列，并在代码旁说明已发现的问题。

## 2. 原始笔记索引

| 原笔记                                                                                                      | 主题定位                                          | 建议阅读顺序 |
| -------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ------ |
| 01 - Lecture 1-2 - Baseline Execution Simulator                                                      | 执行模拟器、CDA、LOB、三类基线执行、IS                       | 1      |
| 02 - Lecture 3 - LOB Liquidity and Microstructure Signals                                            | 盘口流动性、microprice、order imbalance、impact proxy | 2      |
| 03 - HFT Strategies Part 1 - Stat Arb Vol Arb and Market Making                                      | 合法 HFT 策略 Part 1：统计套利、Gamma Scalping、做市       | 3      |
| 04 - HFT Strategies Part 2 - Cross-Venue Arb and Order Flow Prediction                               | 合法 HFT 策略 Part 2：跨市场套利、订单流机器学习                | 4      |
| 05 - Quantitative Trading in Crypto Markets                                                          | 加密市场结构、永续合约、资金费率、Kelly、尾部风险、回测陷阱              | 5      |
| 06 - Price Action and AI Pattern Recognition                                                         | 价格行为、K 线结构、交易管理、CNN/Metric Learning 图形识别      | 6      |
| 07 - Fixed Income Pricing and Risk Analytics                                                         | 固定收益定价、债券风险、杠杆贷款、FRTB                         | 7      |
| 08 - AI-Driven Quantitative Trading and Tokenized Energy Markets                                      | 深度学习量化、AI Agent、能源冲击、RWA/tokenized energy     | 8      |

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

quoted spread 是成交前可见的最优买卖价差；上式是相对成交前 mid 的双边价差，单边价格偏离为其一半。$m_t$ 应使用成交前可观察的同期中间价；绝对值写法假设主动单成交在报价对应的一侧。

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

### 3.5 Lecture 3–4：订单簿与执行信号课堂代码

> [!info] 来源与阅读方式
> 来源：`/Users/xuji/Documents/qfft/sem 2/AMA576 Algorithmic Trading/上半学期/AMA576_Lecture3_Classdemo.ipynb`。以下按 Notebook 单元顺序呈现，编号从 1 开始；课堂原文和代码保留，中文提示补充含义与限制。原 Notebook 输出未复制；运行需安装相关库、可访问行情接口，且实时快照每次可能不同。

> [!tip] 这一讲的主线
> 先抓取订单簿快照，提取 spread、订单不平衡和 microprice，再用下一次快照中间价变化做初步分析，最后建立一个简化的单步执行模拟器。示例不是已验证的实时交易系统。

#### 原 Notebook 单元 1 · 课程说明

##### AMA576 Advanced Topics in Algorithmic Trading 
##### Lecture 3-4: Limit Order Books, Liquidity, and Microstructure Signals  
**Lecturer:** Selena QIAN 

**Goal today:** move from OHLCV-only baselines to **LOB-informed features** (spread, depth, imbalance, microprice) and connect them to execution decisions.

#### 原 Notebook 单元 2 · 课程说明

##### What we will do (in class)
1. Fetch **real-time** order book snapshots (public API).
2. Build a clean feature table: spread, depth, imbalance, microprice.
3. Quick predictive check: does imbalance relate to the next mid-price move?
4. Extend the baseline execution idea with a **LOB-informed aggressiveness rule**.

#### 原 Notebook 单元 3 · 代码

> [!note] 中文说明
> 依赖 `numpy`、`pandas`、`matplotlib` 和 `requests`。`np.random.seed(42)` 只影响随机数，不会固定外部盘口快照。

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime, timezone
np.random.seed(42)
```

#### 原 Notebook 单元 4 · 课程说明

##### Step 1 — Fetch a LOB snapshot (real-time) with a safe fallback
If the request fails (network / rate limit), we fall back to a synthetic snapshot so the notebook still runs.

#### 原 Notebook 单元 5 · 代码

> [!note] 中文说明
> 原说明提到网络失败时使用模拟盘口，但此函数没有异常捕获或合成数据回退；访问失败、超时或触及限流时会报错。参数默认值以函数定义 `limit=500` 为准，文档字符串中的 `default=100` 与定义不一致。此代码调用公开行情接口，不发送订单；请求权重和限制以 [Binance 官方说明](https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#order-book) 为准。

```python
BASE_VISION = 'https://data-api.binance.vision'

def fetch_order_book(symbol='BTCUSDT', limit=500):
    """
    Fetches the order book data from Binance API for a given trading pair.
    
    Parameters:
    -----------
    symbol : str, default='BTCUSDT'
        The trading pair symbol (e.g., 'BTCUSDT', 'ETHUSDT')
    limit : int, default=100
        Maximum number of bid/ask entries to retrieve
        
    Returns:
    --------
    dict
        JSON response containing order book data with 'bids' and 'asks' lists
    """
    url = f"{BASE_VISION}/api/v3/depth"
    params = {'symbol':symbol,'limit':limit}
    r = requests.get(url,params,timeout=15)
    r.raise_for_status()  # Raises an exception for HTTP errors
    return r.json()

ob = fetch_order_book(symbol='BTCUSDT', limit=500)
ob
```

#### 原 Notebook 单元 6 · 课程说明

##### Step 2 — Parse the snapshot into numeric arrays
Binance returns strings in JSON; we convert to floats for calculations.

#### 原 Notebook 单元 7 · 代码

> [!note] 中文说明
> 先将报价字符串转换成数值，然后分别按买价降序和卖价升序排列；如果一侧为空，后续读取第 0 档会失败。

```python
def parse_ob(ob):

    # Build a bids DataFrame from ob['bids'] with columns ['price','qty'], then convert string values to float.
    bids = pd.DataFrame(ob['bids'],columns=['price','qty']).astype(float)

    # Build an asks DataFrame from ob['asks'] with columns ['price','qty'], then convert string values to float.
    asks = pd.DataFrame(ob['asks'],columns=['price','qty']).astype(float)

    # Sort bids by price descending so the first row is the best bid; reset index to 0..n-1.
    bids = bids.sort_values('price',ascending=False).reset_index(drop=True)

    # Sort asks by price ascending so the first row is the best ask; reset index to 0..n-1.
    asks = asks.sort_values('price',ascending=True).reset_index(drop=True)

    # Return the processed bid and ask DataFrames.
    return bids, asks

# Run the parsing function on the raw order book dictionary `ob`.
bids, asks = parse_ob(ob)

# Show the top 5 rows of bids and asks (best levels first).
bids.head(), asks.head()
```

#### 原 Notebook 单元 8 · 课程说明

##### Step 3 — Compute top-of-book features: spread, mid, imbalance, microprice

#### 原 Notebook 单元 9 · 代码

> [!note] 中文说明
> 买一／卖一深度之和必须大于 0，否则不平衡度和 microprice 的分母会为 0。Microprice 是按对侧价格加权的盘口指标，是可研究的代理信号，并不保证未来价格或成交。

```python
def top_of_book_features(bids, asks):

    # Read the best bid price (highest bid)
    b = bids.loc[0,'price']

    # Read the best ask price (lowest ask)
    a = asks.loc[0,'price']

    # Read the quantity available at the best bid level.
    qb = bids.loc[0,'qty']

    # Read the quantity available at the best ask level.
    qa = asks.loc[0,'qty']

    # Compute the bid-ask spread.
    spread = a - b

    # Compute the mid price.
    mid = 0.5 * (a + b)

    # Compute order imbalance at the top level.
    oi = (qb - qa) / (qb + qa)

    # Compute microprice.
    micro = (qb/(qa+qb)) * a + (qa/(qa+qb)) * b

    # Return all features in a dictionary for easy access.
    return dict(best_bid=b, best_ask=a, q_bid=qb, q_ask=qa, spread=spread, mid=mid, oi=oi, microprice=micro)

# Calculate the top-of-book features using the current bids and asks snapshots.
feat0 = top_of_book_features(bids, asks)

# Display the resulting feature dictionary.
feat0
```

#### 原 Notebook 单元 10 · 课程说明

##### Step 4 — Plot cumulative depth

#### 原 Notebook 单元 11 · 代码

> [!note] 中文说明
> 深度图按档位累计数量；函数画中线时引用外部变量 `feat0`，因此若之后换用新盘口而不更新 `feat0`，图中的中线会失配。

```python
# Define a function called 'plot_depth' to plot the cumulative depth of the order book
def plot_depth(bids, asks, levels=30):
    # Take the top N levels from the bid and ask dataframes
    bb = bids.head(levels).copy()
    aa = asks.head(levels).copy()
    # Calculate cumulative quantity for bids
    bb['cum_qty'] = bb['qty'].cumsum()
    # Calculate cumulative quantity for asks
    aa['cum_qty'] = aa['qty'].cumsum()
    
    plt.figure(figsize=(9,4.5))
    plt.step(bb['price'], bb['cum_qty'], where='post', label='Bids (cum depth)')
    plt.step(aa['price'], aa['cum_qty'], where='post', label='Asks (cum depth)') 
    plt.axvline(feat0['mid'], linestyle='--', linewidth=1, label='Mid')
    plt.title('Order Book Cumulative Depth (Top Levels)') 
    plt.xlabel('Price')
    plt.ylabel('Cumulative Quantity')
    plt.legend()
    plt.tight_layout ()
    plt.show()
    
plot_depth(bids, asks, levels=30)
```

#### 原 Notebook 单元 12 · 课程说明

##### Step 5 — Collect a short time series of snapshots
We need a time series to test whether imbalance relates to the next mid move.

#### 原 Notebook 单元 13 · 代码

> [!note] 中文说明
> 本地 UTC 时间在请求开始前记录，不是交易所事件时间或实际响应时间；实际快照间隔包含网络延迟，样本数量少且不等间距。反复请求依赖网络、接口可用性与限流，不应据此推断完整盘口事件流。

```python
def collect_lob_series(symbol='BTCUSDT', n=25, sleep_s=0.6, limit=25):
    """
    Collects a time series of limit order book (LOB) data for a given symbol.
    
    Parameters:
    -----------
    symbol : str, default='BTCUSDT'
        The trading pair symbol to collect order book data for
    n : int, default=25
        Number of samples to collect
    sleep_s : float, default=0.6
        Sleep time in seconds between consecutive data collections
    limit : int, default=25
        Number of price levels to fetch from the order book
        
    Returns:
    --------
    pd.DataFrame
        DataFrame containing order book features with timestamps
    """
    import time
    rows = []  # List to store collected data points
    
    for i in range(n):
        # Record current timestamp in UTC
        ts = datetime.now(timezone.utc)
        
        ob = fetch_order_book(symbol, limit=limit)
        
        # Parse order book into bids and asks
        bids, asks = parse_ob(ob)
        
        # Extract features from the top of the order book
        f = top_of_book_features(bids, asks)
        
        # Add metadata to features
        f['ts'] = ts
        
        # Add this data point to our collection
        rows.append(f)
        
        # Wait before collecting the next sample
        time.sleep(sleep_s)
    
    # Convert collected data to DataFrame, sort by timestamp, and reset index
    return pd.DataFrame(rows).sort_values(by='ts').reset_index(drop=True)

lob = collect_lob_series(n=50, sleep_s=1, limit=25)

lob
```

#### 原 Notebook 单元 14 · 课程说明

##### Step 6 — No look-ahead target: next-step mid change
Features at time t, outcome is mid(t+1) - mid(t).

#### 原 Notebook 单元 15 · 代码

> [!note] 中文说明
> `shift(-1)` 将下一次快照的中间价放在当前行，作为事后标签；这一步的特征／标签方向是向前预测，但训练、标准化或参考值若使用测试期信息仍会产生前视。最后一行没有下一次快照，因此被丢弃。

```python
# Calculate the next mid price by shifting the 'mid' column values one position up
lob['mid_next'] = lob['mid'].shift(-1)

# Calculate the change in mid price between current and next time step
lob['dmid_1'] = lob['mid_next'] - lob['mid']

# Remove rows with NaN values (created by the shift operation) and reset the index
lob = lob.dropna().reset_index(drop=True)

# Display the first 5 rows of selected columns for inspection
lob[['ts','mid','oi','spread','dmid_1']].head()
```

#### 原 Notebook 单元 16 · 课程说明

##### Step 7 — Quick predictive check: OI vs next dMid
We do:
1) correlation
2) binned average plot

#### 原 Notebook 单元 17 · 代码

> [!note] 中文说明
> 相关性和按分位数分组是小样本描述性检查。`qcut` 用整段样本确定分箱边界，不能将同一段数据上的结果直接当成样本外预测能力；重复值过多时分箱数可能减少。

```python
#print the correlation of OI and next_dMid, round to 4 decimal places
print("Corr(OI, next dMid):", round(lob['oi'].corr(lob['dmid_1']),4))

# Create a new column 'oi_bin' by dividing 'oi' values into 5 equal-sized bins
lob['oi_bin'] = pd.qcut(lob['oi'], q=5, duplicates='drop')

# Group the data by the 'oi_bin' categories, calculate the mean of 'dmid_1' for each bin, convert the result back to a DataFrame with reset_index()
grp = lob.groupby('oi_bin',observed=True)['dmid_1'].mean().reset_index()

grp
```

#### 原 Notebook 单元 18 · 代码

```python
# visualization
```

#### 原 Notebook 单元 19 · 代码

> [!note] 中文说明
> 此单元将上一单元的分箱结果画成柱状图；横轴为 OI 分箱、纵轴为下一次采样的平均中间价变化，不能作为扣费后交易收益。

```python
plt.figure(figsize=(10, 6))
grp['oi_bin_str'] = grp['oi_bin'].astype(str)
x_labels = grp['oi_bin_str']
y_values = grp['dmid_1']
bars = plt.bar(range(len(x_labels)), y_values)
plt.xticks(range(len(x_labels)), x_labels, rotation=45, ha='right', fontsize=10)
plt.show()
```

#### 原 Notebook 单元 20 · 课程说明

##### Step 8 — A simple aggressiveness rule (market fraction)
Higher OI -> more aggressive; wider spread -> less aggressive.

#### 原 Notebook 单元 21 · 代码

> [!note] 中文说明
> 这是一条买入执行的演示性规则，并非经过校准的最优执行政策。`spread_ref` 使用整段 `lob` 的中位数；若模拟逐时实时决策，则当前时刻会提前使用未来样本信息，应只采用当时已知的历史参考值或训练集参考值。

```python
# Define a function that calculates market aggressiveness based on order imbalance and spread
def aggressiveness_rule(oi, spread, spread_ref):
    # Normalize the spread by dividing by reference spread (with small epsilon to avoid division by zero)
    s = spread/max(1e-9,spread_ref)
    
    # Calculate a score based on order imbalance (oi) and normalized spread
    x = 0.8 * oi - 0.6 * (s - 1.0)
    
    # Apply sigmoid function to transform score to range (0,1)
    frac = 1/(1 + np.exp(-3 * x))
    
    # Ensure the result is within [0,1] and convert to float
    return float(np.clip(frac, 0.0, 1.0))

# Calculate the median spread as reference value
spread_ref = lob['spread'].median()

# Apply the aggressiveness rule to each row in the dataframe
# Creates a new column 'mkt_frac' representing market aggressiveness
lob['mkt_frac'] = lob.apply(lambda r: aggressiveness_rule(r['oi'], r['spread'], spread_ref), axis=1)

lob[['oi','spread','mkt_frac']]
```

#### 原 Notebook 单元 22 · 课程说明

Simple intuition you can remember

✅ High positive oi (strong buy-side) → more aggressive → mkt_frac goes up

✅ Wide spread → more expensive to trade now → less aggressive → mkt_frac goes down

#### 原 Notebook 单元 23 · 课程说明

##### Step 9 — LOB-informed one-step policy simulator (demo)
This is a teaching proxy:
- volume proxy = q_bid + q_ask
- market exec proxy = mid + gamma*spread （gamma controls how expensive a market order is in your execution price model）
- limit price = mid - alpha*spread, filled if microprice <= L

#### 原 Notebook 单元 24 · 代码

> [!note] 中文说明
> 这里模拟买单：`q_bid+q_ask` 是买一卖一的可见挂单量，不是成交量或市场总成交量；`CAP` 是模型约束，不能等同于真实成交量参与率。默认 `gamma=0.08` 时假设市价买入价格为 `mid+0.08×spread`，低于正常盘口的卖一价 `mid+0.5×spread`，不是一般可执行的市价单价格。限价单是否成交仅由当前 microprice 与限价比较，缺少未来逐笔成交、队列位置与部分成交建模；这些输出只是教学代理。若成交量为零，`cash/filled_qty` 可能除零。

```python
def simulate_one_step_policy(row, Q_remain, CAP=0.30, alpha=0.25, gamma=0.08):
    """
    Simulates a single step of a trading policy that combines market and limit orders.
    
    Parameters:
    - row: DataFrame row containing market data (bid/ask quantities, mid price, spread, etc.)
    - Q_remain: Remaining quantity to be executed
    - CAP: Volume participation cap as a fraction of total market volume
    - alpha: Parameter controlling limit order price placement relative to mid price
    - gamma: Parameter controlling market order slippage as a fraction of spread
    
    Returns:
    - Dictionary containing execution details
    """
    # Calculate total visible volume in the order book
    V = row['q_bid'] + row['q_ask']
    
    # Calculate maximum quantity to trade based on participation cap
    q_cap = CAP * V
    
    # Determine actual trade quantity (limited by remaining quantity)
    q_trade = min(Q_remain, q_cap)

    # Split order between market and limit components based on market fraction
    q_mkt = q_trade * row['mkt_frac']
    q_lmt = q_trade - q_mkt

    # Calculate market order execution price with slippage
    slip = gamma * row['spread']
    exec_mkt = row['mid'] + slip

    # Calculate limit order price and determine if it would be filled
    L = row['mid'] - alpha * row['spread']
    filled = row['microprice']<=L
    exec_lmt = L if filled else np.nan

    # Calculate total filled quantity and execution statistics
    filled_qty = q_mkt + (q_lmt if filled else 0.0)
    cash = q_mkt * exec_mkt + (q_lmt * exec_lmt if filled else 0.0)
    avg_px = cash/filled_qty

    # Return execution details as a dictionary with proper type conversion
    return {'q_mkt': float(q_mkt), 'q_lmt': float(q_lmt), 'filled_lmt': bool(filled),
            'filled_qty': float(filled_qty), 'avg_px': float(avg_px) if np.isfinite(avg_px) else np.nan}

# Initialize total quantity to execute
Q_total = 100
Q_remain = Q_total

# Create empty list to store execution logs
log = []

# Store initial mid price for reference
p0 = lob.loc[0,'mid']

# Simulate trading strategy for up to 15 steps or until we run out of data
for i in range(min(15, len(lob))):
    # Execute one step of the trading policy
    out = simulate_one_step_policy(lob.loc[i], Q_remain, CAP=0.30, alpha=0.25, gamma=0.08)
    
    # Add index and market data to the output
    out.update({'i': i, 'oi': float(lob.loc[i,'oi']), 'spread': float(lob.loc[i,'spread'])})
    
    # Store execution results
    log.append(out)
    
    # Update remaining quantity
    Q_remain -= out['filled_qty']
    
    # Exit loop if we've executed (almost) all quantity
    if Q_remain <= 1e-9:
        break

# Convert execution log to DataFrame for analysis
trade = pd.DataFrame(log)

trade
```

#### 原 Notebook 单元 25 · 课程说明

##### Step 10 — Plot policy behavior (clean plots)

#### 原 Notebook 单元 26 · 代码

> [!note] 中文说明
> 这一单元只有绘图注释，没有实际生成图片的代码。

```python
# plot policy allocation per step
```

#### 原 Notebook 单元 27 · 代码

> [!note] 中文说明
> 本地未找到 `policy allocation.png`；此单元依赖当前工作目录下的同名图片，缺失时会报错。原 Notebook 没有在前一个代码单元实际生成该图。

```python
from IPython.display import Image, display
img_path = "policy allocation.png"
display(Image(filename=img_path))
```

## 4. 执行模拟器与评估纪律

### 4.1 三个执行基线

在买入 `Q = 1000` 的任务中，原笔记定义了三个 baseline：

| 方法 | 规则 | 优点 | 缺点 |
|---|---|---|---|
| Market All | 下一可行时刻全部市价买入 | 优先追求快速成交 | 支付 spread/slippage、冲击可能大，成交仍受盘口和交易限制 |
| Limit Single | 以 `P0 * (1 - δ)` 挂买入限价，在窗口 `W` 内等待 | 可能获得价格改善 | 可能不成交，且错过上涨 |
| Split/TWAP-like | 将 `Q` 拆成 `N` 份逐分钟执行 | 降低单次冲击 | 多次支付成本，暴露于市场漂移 |

限价单的基线成交规则（仅为简化回测假设）：

$$
\begin{aligned}
L &= P_{t_0}(1-\delta),\\
\min_{t_0+1\le t\le t_0+W}\mathrm{Low}_t &\le L
\end{aligned}
$$

低价触及限价并不保证实际成交：排队、盘口深度、部分成交及订单到达时间都可能使订单无法完成。

拆单平均成交价：

$$
\bar{p}_{\mathrm{exec}}
=\frac{1}{Q}\sum_i q_i P_{t_i}(1+\mathrm{slippage})
$$

### 4.2 Implementation Shortfall

对于完全成交的买单、暂不计手续费，实现成本可写成：

$$
\mathrm{IS}=Q(\bar{p}_{\mathrm{exec}}-p_{\mathrm{arrival}})
$$

对于买单：

- `IS > 0`：平均成交价高于决策价，执行变贵。
- `IS < 0`：平均成交价低于决策价，执行更好。

如果只成交 $q<Q$，通常还要将未成交数量按评估终点价格计入机会成本，并加入费用：

$$
\mathrm{IS}_{\mathrm{buy}}=\sum_i q_i(p_i-p_{\mathrm{arrival}})+(Q-q)(p_{\mathrm{end}}-p_{\mathrm{arrival}})+\mathrm{fees}.
$$

卖单方向相反；公式中的到达价和终点价必须在比较时统一。

直觉分解：

$$
IS \approx \mathrm{spread\ cost} + \mathrm{impact\ cost} + \mathrm{drift\ cost}
$$

- **Spread**：为即时性支付的价差。
- **Impact**：自己的交易推动价格。
- **Drift**：等待过程中市场本身移动。

各项必须使用一致单位；若按每股分解，再乘以成交数量，未成交机会成本和手续费还须另计。

### 4.3 无前视偏差

执行模拟器最重要的纪律：

> 成交时间不能早于信号实际可获得和订单到达市场的时间。例如，若用第 $t$ 根 K 线收盘后才确定的 close 生成信号，通常不能再假设以该收盘价成交；若使用此前已知的信息并在收盘竞价截止前提交订单，则应按相应市场机制建模。

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
  - 参与率上限 `q_t <= CAP * volume_t`；若以整分钟最终成交量决定该分钟开始时的订单，会产生前视，须改用当时可观测量/预测量或在分钟内逐笔约束；
  - 输出逐分钟 trade log；
  - 与 market all、split n10、limit single 对比。

### 4.5 Lecture 1–2：课堂执行模拟代码

> [!info] 文件与阅读方式
> 原文件：`/Users/xuji/Documents/qfft/sem 2/AMA576 Algorithmic Trading/上半学期/AMA576_Lecture1_Classdemo.ipynb`。以下按原 Notebook 单元顺序保留课堂原文与代码，单元编号从 1 开始；中文提示为补充解释。图片输出未复制，原始 Notebook 保持不变。
>
> 学习主线：获取 BTCUSDT 分钟 K 线 → 数据清洗 → 市价单、限价单与拆单的简化执行模拟 → 比较实现缺口和成交情况。

> [!warning] 模拟的适用边界
> 这是一份教学示例，并非实盘成交记录。下一根 K 线的完整 high-low 只能事后观察；限价规则还会用到这一未来区间，涉及前视。触价成交、订单数量、交易费用与未成交机会成本均需按实际执行规则重新建模，不能直接把示例结果解释为可交易策略表现。

#### 单元 1 · 课件说明

##### AMA576 — Advanced Topics in Algorithmic Trading  
##### Lecture 1-2 — Baseline Execution Simulator  
**Lecturer: Selena QIAN**

##### Today’s goal
We will build a **baseline execution simulator** using **real intraday BITCOIN data**:

1. Fetch *raw* kline data from Binance (see exactly what the API returns).
2. Convert to a clean DataFrame (and verify types).
3. Define a simple, explicit execution model:
   - **Market** (buy now; proxy price = next-bar open + slippage proxy)
   - **Limit** (buy only if price touches a limit; risk of non-fill)
   - **Splitting** (slice a big order into smaller pieces)

#### 单元 2 · 课件说明

##### 0) Import libraries

#### 单元 3 · 代码

> [!note] 中文讲解
> 导入数组、表格、绘图、HTTP 请求和时间处理工具。`np.random.seed(42)` 固定随机数种子；`warnings.filterwarnings` 会隐藏警告，排错时应留意。

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from datetime import datetime, timedelta, timezone
import warnings
warnings.filterwarnings('ignore')
np.random.seed(42)
```

#### 单元 4 · 课件说明

##### 1) Fetch raw data from Binance
**Purpose:** show that the API returns a **list of lists** (JSON → Python).

Each row has 12 fields:
`['open_time','open','high','low','close','volume','close_time','qav','n','tbb','tbq','ignore']`

#### 单元 5 · 代码

> [!note] 中文讲解
> 数据来自 Binance 的 BTCUSDT 现货 1 分钟 K 线，时间使用 UTC；区间由运行时的当前时刻决定，结果无法固定复现。网络不可用、API 限制或返回空列表时，后面的 `data[0]` 会报错。最新一根 K 线可能尚未收盘，实际研究中应明确处理。

```python
base = 'https://data-api.binance.vision/api/v3/klines'

# Demo window (UTC)
end = datetime.now(timezone.utc).replace(second=0,microsecond=0)


# Set the start time to 8 hours before the end time
start = end-timedelta(hours=8)


# Define parameters for the Binance API request
params = {
    'symbol':'BTCUSDT',     
    'interval':'1m',            
    'startTime': int(start.timestamp() * 1000),  # Convert to milliseconds timestamp
    'endTime': int(end.timestamp() * 1000),      # Convert to milliseconds timestamp
    'limit':1000              
}


# Send GET request to Binance API
r=requests.get(base,params=params,timeout=30)


# Raise an exception if the request was unsuccessful
r.raise_for_status()


# Parse the JSON response into a Python object
data = r.json()


print('Type:', type(data))
print('Rows:', len(data))
print('Row length:', len(data[0]) if len(data)>0 else None)


#check your first row
data[0]
```

#### 单元 6 · 课件说明

##### 2) Label one raw row
**Purpose:** make the raw structure readable.

#### 单元 7 · 代码

```python
# Define column names for the data structure
cols = ['open_time','open','high','low','close','volume','close_time','qav','n','tbb','tbq','ignore']

# Loop through each column name and corresponding value in the first row of data and print each pair with the column name right-aligned to width 10
for k, v in zip(cols, data[0]):
    print(f'{k:>10}: {v}')
```

#### 单元 8 · 课件说明

##### 3) Convert to DataFrame (no type conversion yet)
**Purpose:** table view first, then check dtypes.

#### 单元 9 · 代码

```python
# Create a pandas DataFrame from the 'data' variable using the column names specified in 'cols'
df_raw = pd.DataFrame(data,columns=cols)

# Display the first 5 rows of the DataFrame to inspect the data structure
df_raw.head()
```

#### 单元 10 · 课件说明

##### 4) Check dtypes
**Purpose:** numeric fields often arrive as strings in JSON.

#### 单元 11 · 代码

```python
# Check the data types of each column in the df_raw DataFrame
df_raw.dtypes
```

#### 单元 12 · 课件说明

##### 5) Convert timestamps to datetime (UTC)
**Purpose:** build a clean time axis.

#### 单元 13 · 代码

> [!note] 中文讲解
> 时间戳以毫秒转为 UTC；此单元只转换 `open_time`，`close_time` 转换行仍是注释。

```python
# Create a copy of the raw dataframe
df1 = df_raw.copy()


# Convert 'open_time' from milliseconds timestamp to datetime format with UTC timezone
df1['open_time'] = pd.to_datetime(df1['open_time'],unit='ms',utc=True)
# df1['close_time'] = pd.to_datetime(df1['close_time'],unit='ms',utc=True)


# Display the first few rows of the time columns to verify the conversion
df1[['open_time','close_time']].head()
```

#### 单元 14 · 课件说明

##### 6) Convert OHLCV to floats
**Purpose:** ensure computations work correctly.

#### 单元 15 · 代码

> [!note] 中文讲解
> 这里把 OHLCV 五列转成浮点数；其他成交量、成交笔数等字段仍保持原始类型。

```python
# Create a copy of the d1 to avoid modifying it
df2 = df1.copy()


# Define a list of columns that contain numerical data
num_cols = ['open','high','low','close','volume']


# Convert the specified columns to float data type
df2[num_cols] = df2[num_cols].astype(float)


# Display the first few rows of the numerical columns to verify the conversion
df2[num_cols].head()
```

#### 单元 16 · 课件说明

##### 7) Keep the clean OHLCV dataset
**Purpose:** minimal baseline dataset for execution simulation.

#### 单元 17 · 代码

> [!note] 中文讲解
> 排序、按开盘时间去重并重置索引，方便后续使用 `.loc`；尚未检查 K 线缺失、停牌或异常值。

```python
# Select specific columns from df2 and create a new dataframe, sort by open_time and drop duplicates if there is any, reset index
df = df2[['open_time','open','high','low','close','volume']].sort_values('open_time').drop_duplicates('open_time').reset_index(drop=True)

# Print the shape (rows, columns) of the dataframe
print('Shape:', df.shape)
# Print the minimum timestamp in the dataset
print('time min:', df['open_time'].min())
# Print the maximum timestamp in the dataset
print('time max:', df['open_time'].max())
# Display the first 5 rows of the dataframe
df.head()
```

#### 单元 18 · 课件说明

##### 8) Sanity plots (quick)

#### 单元 19 · 代码

```python
#visualized close price
plt.figure(figsize=(12,6))
plt.plot(df['open_time'],df['close'],label='BTCUSDT')
plt.title('Close Price Over Time') # 设置图表标题
plt.xlabel('Time (UTC)')             # 设置 X 轴标签
plt.ylabel('Price')                  
plt.legend() 
```

#### 单元 20 · 代码

```python
#visualize volume
plt.figure(figsize=(12,6)) # Typically, volume charts are shorter vertically than price charts
plt.bar(df['open_time'], df['volume'], label='BTCUSDT Volume', width=0.0005)
plt.title('Trading Volume Over Time') # 设置图表标题
plt.xlabel('Time (UTC)')             # 设置 X 轴标签
plt.ylabel('Volume')
plt.legend()
plt.tight_layout() # Adjust layout to prevent labels overlapping
plt.show() # Display the plot
```

#### 单元 21 · 课件说明

##### Part B — Baseline execution simulator (Market / Limit / Splitting)

##### 9) Define baseline objects (avoid look-ahead)
**Timing rule:** decide at time *t*, execute at *t+1*.

Baseline proxies (with OHLCV only):
- Arrival price: `p0 = close[t]`
- Market execution price: `next_open[t] + slip[t]` 
- Slippage proxy: `slip[t] = GAMMA * (high[t+1] - low[t+1])`

#### 单元 22 · 代码

> [!note] 中文讲解
> `shift(-1)` 将下一根 K 线放到当前行，方便事后模拟。下一根完整 K 线的最高价和最低价在其开盘时尚不可知；用该区间计算滑点属于事后成本代理，不能当作开盘时已知的信号或真实可执行报价。`Q_TOTAL=1000` 是假设数量，未考虑订单容量。

```python
# Total quantity to trade
Q_TOTAL = 1000


# Price impact factor
GAMMA = 0.10


# Maximum waiting time in periods
MAX_WAIT = 30 


# Calculate next period's price data by shifting current data forward
df['next_open'] = df['open'].shift(-1)
df['next_high'] = df['high'].shift(-1)
df['next_low']  = df['low'].shift(-1)


# Calculate the price range for the next period (high minus low)
df['range_next'] = df['next_high'] - df['next_low']


# Set the arrival price as the current closing price
df['arrival_price'] = df['close']


# Calculate price slippage as a fraction (GAMMA) of the next period's price range
df['slip'] = GAMMA * df['range_next']

# Display the first few rows of relevant columns
df[['open_time','close','next_open','range_next','slip']].head()
df
```

#### 单元 23 · 课件说明

##### 10) Strategy 1 — Market (all at once)

#### 单元 24 · 课件说明

Write a function simulate_market_all(df, t0_idx, Q) that simulates a buy market order.

- decision at time t0_idx

- execution at t0_idx + 1 (next bar)

- compute implementation shortfall

- return a dictionary of results

#### 单元 25 · 代码

> [!note] 中文讲解
> 买入实现缺口以 `(成交均价 − 到达价) × 已成交数量` 衡量，本例假设全部立即成交；没有单独纳入手续费、订单簿深度、冲击和未成交机会成本，`slip` 为未来一整根 K 线区间的事后代理。

```python
def simulate_market_all(df, t0_idx, Q=1000):
    """Buy Q via market order at decision time t0 (exec at t0+1).
    
    Parameters:
    -----------
    df : DataFrame
        DataFrame containing price data with columns like 'arrival_price', 'next_open', 'slip', 'open_time'
    t0_idx : int
        Index in the DataFrame representing the decision time
    Q : float, default=1000
        Quantity to be executed
        
    Returns:
    --------
    dict
        Dictionary containing execution details including method, execution time, prices, and costs
    """
    # Get the arrival price at decision time
    p0 = df.loc[t0_idx,'arrival_price']
    
    # Calculate execution price (next open price plus slippage)
    exec_px = df.loc[t0_idx,'next_open'] + df.loc[t0_idx,'slip']
    
    # Get the timestamp when the order is executed (t0+1)
    exec_time = df.loc[t0_idx+1,'open_time']
    
    # Calculate implementation shortfall cost
    is_cost = (exec_px - p0) * Q
    
    # Return execution details as a dictionary
    return {
        'method': 'market_all',
        't0_idx': int(t0_idx),
        'exec_time': exec_time,
        'Q': float(Q),
        'p0': float(p0),
        'avg_exec_px': float(exec_px),
        'IS': float(is_cost),
        'filled_qty': float(Q),
        'minutes_to_complete': 1
    }

# Set t0 to the middle of the DataFrame
t0 = len(df) // 2
# t0 = 150

# Simulate a market order execution at time t0 with quantity Q_TOTAL
results_all = simulate_market_all(df, t0, Q_TOTAL)
results_all
```

#### 单元 26 · 课件说明

##### 11) Strategy 2 — Limit (single limit with max wait)
In our baseline simulator, a buy limit order is considered filled if the market price ever trades down to your limit price during the next bar.

Baseline fill rule (touch-to-fill): filled if `low <= L`.

Limit price definition (baseline):
$L = next\_open - \alpha \cdot range\_{next} $

**For a buy:**

We place the limit below the next bar’s open.

𝛼 controls how far below we place it

#### 单元 27 · 代码

> [!note] 中文讲解
> 限价 `L` 使用下一根完整 K 线的 high-low，在当下尚未知晓，因此作为提前提交的订单价存在前视。触及最低价不保证排队成交，也未模拟部分成交。未成交时 `IS` 为 NaN，不包含未成交机会成本。此单元将限价结果赋给 `results_all`，覆盖了前面的市价结果。

```python
def simulate_limit_single(df, t0_idx, Q=1000, alpha=0.25, max_wait=30):
    """Place one buy limit; filled if low <= L within max_wait minutes."""
    p0 = df.loc[t0_idx,'arrival_price']
    L = df.loc[t0_idx,'next_open'] - alpha * df.loc[t0_idx,'range_next']

    # Initialize execution variables
    filled = 0.0
    fill_idx = None

    # Loop through subsequent time periods up to max_wait
    for i in range(1, max_wait + 1):
        current_idx = t0_idx + i

    
        # Break if we reach the end of the dataframe
        if current_idx >= len(df):
            break
    
        # Check if price drops below our limit price
        if df.loc[current_idx, 'low'] <= L:
            filled = Q
            fill_idx = current_idx
            break
    

    # Calculate execution metrics if order was filled
    if filled > 0:
        # Execution price is the limit price
        exec_px = float(L)
        
        # Time of execution
        exec_time = df.loc[fill_idx, 'open_time']

        # Implementation shortfall cost
        is_cost = (exec_px - p0) * Q

        # Time to execution
        minutes = int(fill_idx - t0_idx)
        
    else:
        # Order wasn't filled, set appropriate values
        exec_px = np.nan
        exec_time = pd.NaT
        is_cost = np.nan
        minutes = int(max_wait)  # Used full waiting time

    return {
            'method': f'limit_a{alpha:.2f}',
            't0_idx': int(t0_idx),
            'exec_time': exec_time,
            'Q': float(Q),
            'p0': float(p0),
            'avg_exec_px': exec_px,
            'IS': is_cost,
            'filled_qty': filled,
            'minutes_to_complete': minutes
    }

# Set t0 to the middle of the DataFrame
t0 = len(df) // 2
# t0 = 150

# Simulate a market order execution at time t0 with quantity Q_TOTAL
results_all = simulate_limit_single(df, t0, Q=1000, alpha=0.25, max_wait=30)
results_all
```

#### 单元 28 · 代码

> [!note] 中文讲解
> 此单元再次定义同名函数，会覆盖上一版本；`exec_time` 取 `fill_idx+1` 的开盘时间而不是触及那根 K 线的时间，最后一根触及时还可能越界。由于只有 K 线，触及发生在该分钟内的准确时点无法确定。

```python
def simulate_limit_single(df, t0_idx, Q=1000, alpha=0.25, max_wait=30):
    """Place one buy limit; filled if low <= L within max_wait minutes."""
    p0 = df.loc[t0_idx, 'arrival_price']
    L = df.loc[t0_idx, 'next_open'] - alpha * df.loc[t0_idx, 'range_next']

    filled = 0.0
    fill_idx = None
    
    for i in range(1, max_wait+1):
        current_idx = t0_idx + i
        if current_idx >= len(df):
            break
        if df.loc[current_idx, 'low'] <= L:
            filled = Q
            fill_idx = current_idx
            break
    
    if filled > 0:
        exec_px = L
        exec_time = df.loc[fill_idx+1, 'open_time']
        is_cost = (exec_px - p0) * Q
        minutes = int(fill_idx - t0_idx)
    else:
        exec_px = np.nan
        exec_time = pd.NaT
        is_cost = np.nan
        minutes = int(max_wait)
    
    return {
        'method': f'limit_a{alpha:.2f}',
        't0_idx': int(t0_idx),
        'exec_time': exec_time,
        'Q': float(Q),
        'p0': float(p0),
        'avg_exec_px': exec_px,
        'IS': is_cost,
        'filled_qty': filled,
        'minutes_to_complete': minutes
    }


t0 = len(df) // 2 

results_limit = simulate_limit_single(df, t0, Q=1000, alpha=0.25, max_wait=30)
results_limit
```

#### 单元 29 · 课件说明

##### 12) Strategy 3 — Splitting (market slices)

#### 单元 30 · 课件说明

Split Q into n slices; execute one market slice per minute (each slice uses next_open+slip)

#### 单元 31 · 代码

> [!note] 中文讲解
> 按等量切分，并以每根 K 线的下一开盘加区间滑点模拟成交。若样本结束会部分成交；计算的 IS 仅覆盖已成交部分，不计未成交机会成本。`minutes_to_complete` 实际是成交片数，只有 K 线连续且每片一分钟时才等于经过分钟数。

```python
def simulate_market_splitting(df, t0_idx, Q=1000, n_slices=10):
    """Split Q into n slices; execute one market slice per minute (each slice uses next_open+slip)."""
    # Get the initial price at the arrival time
    p0 = df.loc[t0_idx,'arrival_price']
    
    # Calculate the quantity for each slice
    slice_q = Q / n_slices

    # Initialize lists to store execution prices and times
    exec_prices = []
    exec_times = []

    # Loop through each slice
    for j in range(n_slices):
        # Calculate the index for the current slice
        current_idx = t0_idx + j
        
        # Check if we've reached the end of the dataframe
        if current_idx >= len(df) - 1:
            break
        
        # Calculate execution price as next open price plus slippage
        px = df.loc[current_idx,'next_open'] + df.loc[current_idx,'slip']
        
        # Store the execution price
        exec_prices.append(px)
        
        # Store the execution time (open time of the next minute)
        exec_times.append(df.loc[current_idx+1,'open_time'])


    # Calculate how many slices were actually filled
    filled_slices = len(exec_prices)
    
    # Calculate the total quantity filled
    filled_qty = filled_slices * slice_q

    # Handle the case where no slices were filled
    if filled_slices == 0:
        return {
            'method': f'split_n{n_slices}',
            't0_idx': int(t0_idx),
            'exec_time': pd.NaT,  # Not a Time (no execution)
            'Q': float(Q),
            'p0': float(p0),
            'avg_exec_px': np.nan,  # No execution price
            'IS': np.nan,  # No implementation shortfall
            'filled_qty': 0.0,
            'minutes_to_complete': 0
        }

    # Calculate the weighted average execution price
    avg_exec_px = np.sum(exec_prices) / filled_slices
    
    # Calculate implementation shortfall cost (difference between execution and arrival price)
    is_cost = (avg_exec_px - p0) * filled_qty
    
    # Number of minutes to complete the order equals the number of filled slices
    minutes = int(filled_slices)
    

    # Return the execution summary
    return {
        'method': f'split_n{n_slices}',
        't0_idx': int(t0_idx),
        'exec_time': exec_times[-1],  # Time of the last execution
        'Q': float(Q),
        'p0': float(p0),
        'avg_exec_px': avg_exec_px,
        'IS': is_cost,
        'filled_qty': float(filled_qty),
        'minutes_to_complete': minutes,
        'time': exec_times,
        
    }

# Simulate a market splitting order execution
t0 = len(df) // 2 
# t0 = 160

results_split = simulate_market_splitting(df, t0, Q=1000, n_slices=10)
results_split
```

#### 单元 32 · 课件说明

##### 13) Compare three mothods in one table at the same decision time

#### 单元 33 · 代码

> [!note] 中文讲解
> 这里的 `results_all` 已被前面限价单元覆盖，因此此表可能出现两条限价结果而没有市价单结果。应重新调用市价函数再比较；保留原代码以便对应课件。

```python
results_list = []
results_list.append(results_all)
results_list.append(results_limit)
results_list.append(results_split)
comparison_table = pd.DataFrame(results_list)
comparison_table
```

#### 单元 34 · 课件说明

##### 14) Sweep over many decision times
What changes when we move the decision time earlier or later—across all three strategies?
   - Starts at index 30 (avoiding the beginning of the dataset)
   - Stops 60 indices before the end of the dataframe (avoiding the end)
   - Takes every 10th index (step size of 10)

#### 单元 35 · 代码

> [!note] 中文讲解
> 遍历多个起始时点，将三个方法结果拼接；区间不足时列表可能为空，`pd.concat` 会报错。不同方法可能成交数量不同，直接比较原始 IS 有偏，需同时查看成交率并对未成交数量约定处理。

```python
start_idx = 30
end_idx = len(df) - 61
step_size = 10

t0_index_test = list(range(start_idx, end_idx, step_size))

all_comparison_results_for_sweep = []

for t0 in t0_index_test:
    results_all = simulate_market_all(df, t0, Q=1000)
    results_limit = simulate_limit_single(df, t0, Q=1000, alpha=0.25, max_wait=30)
    results_split = simulate_market_splitting(df, t0, Q=1000, n_slices=10)
    results_list = []
    results_list.append(results_all)
    results_list.append(results_limit)
    results_list.append(results_split)
    comparison_table = pd.DataFrame(results_list)
    comparison_table['original_t0_idx'] = t0
    all_comparison_results_for_sweep.append(comparison_table)

final_swept_results_df = pd.concat(all_comparison_results_for_sweep, ignore_index=True)
df0 = final_swept_results_df
df0 = df0[df0['method'] == 'split_n10']
df0
```

#### 单元 36 · 课件说明

##### 15) Plot 1 — IS distribution by method based on step 14

#### 单元 37 · 代码

> [!note] 中文讲解
> 绘制前会删掉 IS 缺失的观测；未成交限价单因此不在箱线图里，不能据此断言限价单整体执行成本更低。

```python
plot_data = final_swept_results_df[['method', 'IS']].copy()
plot_data.dropna(subset=['IS'], inplace=True)
plt.figure(figsize=(12, 8))
sns.boxplot(x='method', y='IS', data=plot_data, palette='viridis')

plt.title('Distribution of Implementation Shortfall (IS) by Trading Strategy Method', fontsize=16)
plt.xlabel('Trading Strategy Method', fontsize=12)
plt.ylabel('Implementation Shortfall (IS) [Currency]', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45, ha='right')
plt.tight_layout() 
plt.show()
```

#### 单元 38 · 代码

> [!note] 中文讲解
> 从当前工作目录读取已有图片文件，代码未在前面的图表步骤中保存该文件；若图片不存在会报错。

```python
from IPython.display import Image, display
img_path = "IS_distribution.png"
display(Image(filename=img_path))
```

#### 单元 39 · 课件说明

##### 16) Plot 2 — Splitting trade-off
Instead of writing text on every point (which overlaps), we:
- plot points in order of `n_slices`
- connect them with a line
- label using the x-axis `n_slices` (separate plot)

#### 单元 40 · 代码

> [!note] 中文讲解
> 该单元只有注释，没有实际实现切片数量敏感性分析。

```python
# Prepare splitting sweep results
```

#### 单元 41 · 代码

> [!note] 中文讲解
> 依赖本地 `Splitting sensitivity.png`，原 Notebook 中未在此之前生成或保存该文件；路径不存在时会报错。

```python
img_path = "Splitting sensitivity.png"
display(Image(filename=img_path))
```

#### 单元 42 · 代码

> [!note] 中文讲解
> 该单元只有注释，后续可作为练习补充；原 Notebook 没有绘图实现。

```python
# Plot n_slices vs Avg IS
```

## 5. 合法 HFT 策略版图

原 HFT 两篇笔记覆盖五类合法策略：

| 策略 | 核心机制 | 单笔利润 | 胜率 | 延迟要求 | 主要风险 |
|---|---|---:|---:|---|---|
| Statistical Arbitrage | 协整价差均值回复 | 5-50 bps | 55-65% | 中高 | regime/correlation breakdown |
| Volatility Arbitrage | IV 与 RV 差异，Gamma Scalping | 10-100 bps | 50-60% | 高 | theta decay、gap risk |
| Market Making | 双边报价赚 spread | 0.5-5 bps | 51-75% | 极高，常 <1μs | adverse selection、inventory risk |
| Cross-Venue Arbitrage | 跨交易所价格差 | 1-10 bps | 70-85% | 极高，μs 级 | execution risk、latency creep |
| Order Flow Prediction | L2 订单簿和订单流 ML 预测 | 2-20 bps | 52-58% | 100-500ms | overfitting、regime change |

表中收益、胜率与延迟是课件中的示意范围，缺少统一样本及成本口径，不能当成可复现业绩或策略保证。

### 5.1 统计套利：Pairs Trading

核心思想：

> 两个有经济联系且协整的资产，短期可能偏离，历史价差在统计上表现出均值回复；未来关系仍可能失效。

流程：

1. 选择经济上相关的资产对。
2. 用 OLS 得到 hedge ratio。
3. 对估计残差做 Engle–Granger 协整检验，使用适合估计残差的临界值；拒绝单位根原假设可支持协整，但不能保证关系在未来持续。
4. 将 spread 建模为 OU 过程。
5. 用 z-score 触发入场/出场。

关键公式：

$$
\begin{aligned}
P_{B,t} &= \beta_0+\beta_1 P_{A,t}+u_t,\\
\mathrm{spread}_t &= P_{B,t}-(\beta_1P_{A,t}+\beta_0),\\
z_t &= \frac{\mathrm{spread}_t-\mu_{\mathrm{spread}}}{\sigma_{\mathrm{spread}}},\\
dS_t &= \lambda(\mu-S_t)\,dt+\sigma\,dW_t,\\
t_{1/2} &= \frac{\ln 2}{\lambda}\quad(\lambda>0)
\end{aligned}
$$

依据 $e^{-\lambda t_{1/2}}=1/2$ 可得正的半衰期。课件 `Legal_HFT_Strategies.pdf` 第 5 页误写为负号，这里按其给出的 $\lambda>0$ 和 OU 过程修正。

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

核心 P&L（将 $\Theta_{\rm decay}=-\partial V/\partial t$ 定义为正的时间衰减成本）：

$$
\text{Delta-hedged P\&L}
\approx \frac{1}{2}\Gamma(\Delta S)^2-\Theta_{\rm decay}\,\Delta t
$$

若采用常见定义 $\Theta=\partial V/\partial t$，同一项应写作 $+\Theta\Delta t$。上式忽略利率、分红、隐含波动率变化及交易成本；实现波动率高于买入时的隐含波动率也不保证获利。

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
\mathrm{Ask} &= r+\delta/2,\\
\mathrm{Bid} &= r-\delta/2
\end{aligned}
$$

含义：

- `q > 0` 长库存时，reservation price 下移，报价整体偏低，鼓励卖出库存。
- `q < 0` 短库存时，reservation price 上移，报价整体偏高，鼓励买回库存。
- 这里 $\delta$ 是完整买卖价差，因此距中心价的半价差为 $\delta/2$；$\kappa$ 表示订单到达强度对报价距离的衰减参数，而非到达强度本身。原课件 `Legal_HFT_Strategies.pdf` 第 17 页同时把 $\delta$ 写成全价差并用于两边，存在因子 2 不一致。

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
\delta_{\mathrm{obs}}(t) &= m_A(t)-m_B(t),\\
\delta_{\mathrm{exec}}(t,\tau) &= m_A(t+\tau)-m_B(t+\tau),\\
\pi_{\mathrm{net}} &= Q\left(\delta_{\mathrm{exec}}-c_A-c_B-\frac{s_A}{2}-\frac{s_B}{2}-I\right),\\
\delta(t) &= \delta_0 e^{-\lambda t},\\
t^* &= \frac{1}{\lambda}\ln\left(\frac{\delta_0}{C_{\mathrm{total}}}\right)
\end{aligned}
$$

交易可行条件：

$$
\begin{aligned}
\delta_{\mathrm{obs}}(t) &> C_{\mathrm{total}},\\
\tau_{\mathrm{total}} &< t^*
\end{aligned}
$$

这里假设 $m_A>m_B$，在 A 卖出、B 买入，费用及冲击都按每单位计；实际成交时刻的价差是事后结果，不能用于 $t$ 时刻的交易决策。指数衰减只是简化模型，且 $t^*$ 公式要求 $\lambda>0$、$\delta_0>C_{\mathrm{total}}>0$；执行价差、两腿成交时点和费用应按实际市场条件计算。

要点：

- 延迟优势会影响套利能否实现，所需速度取决于交易场所及策略；
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
\mathrm{VPIN}_t &= \frac{1}{N}\sum_{j=t-N+1}^{t}\frac{|V_j^{\mathrm{buy}}-V_j^{\mathrm{sell}}|}{V},\\
\lambda(t) &= \mu+\sum_{t_i<t}\alpha e^{-\beta(t-t_i)},\\
\mathrm{Momentum}_t(k) &= \frac{P_t-P_{t-k}}{P_{t-k}}
\end{aligned}
$$

这里 VPIN 使用最近 $N$ 个等成交量桶，每桶总量为 $V$；单个桶的买卖量差只是其组成部分，并不等同于通常滚动平均的 VPIN。该指标是订单流不平衡代理，不是可直接观测或保证准确的知情交易概率。

模型：

- Random Forest：解释性较好、推理快，适合作 baseline 和特征筛选。
- LSTM：能捕捉序列依赖，但训练慢、调参敏感。
- XGBoost：表格特征强、生产常用，但依赖特征工程。
- Ensemble：可组合不同模型，但是否更稳健需要样本外和成本后验证。

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

在常见资金费率机制下，当 funding 为正：

- longs pay shorts；
- arbitrageur 可以 short perp + long spot；
- 可能收取 funding，并承担 basis 变化风险；perp 高于 spot 并不必然保证 funding 为正，各交易所规则和费率会变化。

Funding rate 可建模为 OU：

$$
\begin{aligned}
dr(t) = \kappa(\mu - r(t))dt + \sigma\,dW(t) \\
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

在连续时间几何布朗运动、无交易成本、对数效用和可持续再平衡的简化模型中，Kelly 风险资产比例为：

$$
f^*= (\mu-r) / \sigma^2
$$

这里 $\mu$ 是风险资产预期收益率、$r$ 是无风险利率，二者需使用与 $\sigma$ 一致的时间单位。实务中有时采用 Half-Kelly，以降低参数估计误差造成的过度下注风险。

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
| Triangle | 上下边界逐渐收敛的整理形态 | breakout mode，等待方向；三次推升或下压更常用于描述 wedge |
| Rounded Top/Bottom | 逐渐减速的反转 | 本质仍要看 wedge、pullback、climax 等结构 |

### 7.4 Trader's Equation

以胜负两类结果概括、且 Reward 和 Risk 分别代表对应的平均盈利与平均亏损时，交易扣费后的正期望条件为：

$$
P(\mathrm{win}) \cdot \mathrm{Reward} > P(\mathrm{loss}) \cdot \mathrm{Risk}+\mathbb E[\mathrm{cost}]
$$

重点：

- 早入场可能带来较好的盈亏比，但胜率也可能较低；这是课件中的经验性权衡，并非普遍规律。
- 晚入场可能获得更多确认，但也可能面临更差的价格和盈亏比。
- 没有完美形态，所有 pattern 都可能失败。
- 可以预先设置保护性止损或其他退出机制；止损触发后的成交价并不保证等于止损价，跳空和流动性不足时尤其如此。

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
- 可以按时间先后切分 train/validation/test（例如 `70/20/10`）；重叠窗口、标签期限和标准化必须防止跨集合信息泄漏，并保留真正未参与调参的测试集。

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
\mathrm{CS01}_{\mathrm{change}}=V(cs+0.0001)-V(cs)
$$

这里是利差上升 1 bp 的价值变化，通常为负；有的报告以其负值表示正的损失额。若再除以 $0.0001$，得到每单位利差的导数近似，而不是每 1 bp 的价值变化。FRTB 的监管敏感度及聚合口径应按对应规则具体计算。风险暴露按 credit quality、sector、bucket 分组。

## 9. AI-Driven Quant、能源市场与 RWA

### 9.1 深度学习在期权定价和波动预测中的角色

笔记中的关键观点：

- 课件引用的特定研究中，MLP 在相应数据与实验设置下较 Black–Scholes 有更低定价误差；不能据此断言所有市场和样本均如此。
- LSTM 可以从历史窗口学习波动率动态；课件报告其在特定较长期权实验中表现较好，泛化能力仍需独立检验。
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
| Iraq War 2003 | 课件将其作为短期风险溢价回落的例子 | 可研究短期波动与均值回复，但需结合历史样本验证 |
| Russia-Ukraine War | 课件强调供应链与地缘结构调整 | 关注可能持续的结构变化，重估相关性并做压力测试 |

### 9.4 Tokenized Energy / RWA

能源资产代币化的核心：

- 用 token 表示物理原油、天然气、电力、可再生能源证书、碳信用、能源基础设施收益权；
- 分割所有权，降低参与门槛；
- 某些平台支持 24/7 交易和更快结算，实际可用性取决于平台、链及托管安排；
- smart contract 自动处理 KYC/AML、分红、赎回、合规限制；
- oracle 和储备证明有助于提供资产信息，但不能单独保证实物存在、法律权属或赎回；仍须核查审计和托管安排；
- institutional custody、cross-chain bridge 和合规框架是基础设施。

对量化交易的启发：

- tokenized liquidity 可能带来新的跨市场套利；
- oracle price 与传统市场价格之间会形成基差和延迟；
- RWA 交易结合了传统商品基本面、链上机制和市场微观结构；
- 合规和资产托管风险与模型风险同等重要。

> [!note] 资料核对说明
> 市场微观结构、执行和 HFT 内容可对照课程目录的 Lecture 1–3、`Legal_HFT_Strategies.pdf` 和 `HFT_Strategies_Part_2.pdf`。其中部分数字是课件给出的示意，依赖特定样本与口径。AI 与能源课件为图像型 PDF，已通过图像文字识别对照主题和主要表述；具体论文数据与案例归因仍应回到课件引用的原始研究核实。

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
| Half-life | $t_{1/2}=\frac{\ln 2}{\lambda}$，$\lambda>0$ | OU 偏离均值的条件期望衰减一半所需时间 |
| Z-score | $z_t=\frac{\mathrm{spread}_t-\mu_{\mathrm{spread}}}{\sigma_{\mathrm{spread}}}$ | 统计套利入场信号 |
| Gamma P&L | $\frac{1}{2}\Gamma(\Delta S)^2-\Theta_{\rm decay}\,\Delta t$ | 忽略其他因素的近似；衰减成本采用正号定义 |
| A-S Reservation Price | $r(s,q,t)=s-q\gamma\sigma^2(T-t)$ | 库存调整后的做市中心价 |
| Cross-Venue Profit | $\pi_{\mathrm{net}}=Q(\delta-C_{\mathrm{cost}}-I)$ | 跨市场套利净利润 |
| Signal Decay | $\delta(t)=\delta_0e^{-\lambda t}$ | 套利窗口衰减 |
| OBI | $\mathrm{OBI}_t=\frac{V_t^b-V_t^a}{V_t^b+V_t^a}$ | 订单流 ML 特征 |
| VPIN | $\mathrm{VPIN}_t=\frac{1}{N}\sum_{j=t-N+1}^t\frac{\lvert V_j^{\mathrm{buy}}-V_j^{\mathrm{sell}}\rvert}{V}$ | 等成交量桶的滚动不平衡指标 |
| Kelly | $f^*=\frac{\mu-r}{\sigma^2}$ | 简化连续时间模型中的风险资产比例 |
| Bond DF | $B(t,T)=e^{-r(t,T)(T-t)}$ | 零息债折现因子 |
| CS01 | $\Delta V_{1\mathrm{bp}}=V(cs+0.0001)-V(cs)$ | 利差上升 1 bp 的价值变化；符号口径因报告而异 |
| Trader's Equation | $P(\mathrm{win})\cdot\mathrm{Reward}>P(\mathrm{loss})\cdot\mathrm{Risk}+\mathbb E[\mathrm{cost}]$ | 扣除交易成本后的正期望条件 |

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
