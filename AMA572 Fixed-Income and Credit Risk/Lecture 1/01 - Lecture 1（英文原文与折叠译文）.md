---
course: AMA572 Fixed-Income and Credit Risk
source: 01_Lecture1_原课件_信用风险与违约概率.pdf
pages: 14
created: 2026-10-15
cssclasses:
  - ama-inline-translations
---

> [!info] 阅读方式
> 英文正文按 PDF 顺序转录，公式和表格保留原文数值。点击各段旁的「中文译文」查看翻译。PDF 排版中的换行与断词已合并，原文中的措辞及疑似笔误均保留。
> 原始文件：[[AMA572 Fixed-Income and Credit Risk/Lecture 1/附件/01_Lecture1_原课件_信用风险与违约概率.pdf|原课件 PDF]] · [[AMA572 Fixed-Income and Credit Risk/Lecture 1/02 - 课内练习解答（英文原文与折叠译文）|练习解答]] · [[AMA572 Fixed-Income and Credit Risk/Lecture 1/03 - Matrix Exponential Approximation（Notebook 原文代码）|配套 Notebook]]

## PDF p.1

# AMA572 Lecture 1. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AMA572 第 1 讲。</span></details>

**Credit Risk (I): Introduction and Default Probabilities** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">信用风险（一）：导论与违约概率。</span></details>

### 1 Introduction <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1 导论。</span></details>

Credit risk is the risk associated with default, which means that an obligor does not honor the payment obligations. As simple example, consider a defaultable bond which pays a face value (also called par value) \$1 at maturity $T$ and has a continuous coupon payment $\rho$. Let the default time be $\tau$. Assume the bond recovery value is $c(T,\tau)$; in other words upon default the bondholder can only get $c(T,\tau)$, which may be a random variable depending on the bond maturity $T$. Then the discounted total cash flow is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">信用风险是与违约有关的风险，违约是指债务人未履行付款义务。举一个简单的例子：一只存在违约风险的债券在到期日 T 支付面值（也称票面价值）1 美元，并连续支付票息 ρ。令违约时间为 τ，债券回收价值为 c(T, τ)。也就是说，违约时债券持有人只能获得 c(T, τ)，它可能是一个取决于债券到期日 T 的随机变量。全部现金流的折现值为：</span></details>

$$
e^{-rT}1_{\{\tau>T\}}+e^{-r\tau}c(T,\tau)1_{\{\tau\leq T\}}+\int_0^{\tau\wedge T}\rho e^{-rs}ds,
$$

where $r$ is the discount rate typically being the risk-free rate. The first term above is the discounted payoff if the default does not happen by time $T$, i.e. $\tau>T$. The second term is the payment upon default time $\tau$. The last term is the coupon payment from time 0 until either the default time or the maturity, whichever comes first. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 r 是贴现率，通常为无风险利率。第一项表示在 T 之前没有违约（即 τ &gt; T）时到期付款的折现值；第二项表示在违约时刻 τ 支付的回收款；最后一项表示从时间 0 开始，直到违约或到期中较早时刻为止的票息支付。</span></details>

The default time $\tau$ may be triggered by various events, including bankruptcy (or filing for bankruptcy protection), failure to pay, etc. In reality, the coupon payment may not be continuous, e.g. semi-annual payments. The default payment $c(T,\tau)$ may result from legal actions and/or contractual obligations. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">违约时间 τ 可能由破产（或申请破产保护）、未能付款等事件触发。现实中的票息不一定连续支付，例如可能半年支付一次。违约支付 c(T, τ) 可能由法律程序及／或合同义务决定。</span></details>

Credit risk is important for four reasons. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">信用风险的重要性主要体现在以下四个方面。</span></details>

**(1) Credit risk is relevant for defaultable bonds** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（1）信用风险与存在违约风险的债券有关。</span></details>

Defaultable bonds include corporate bonds, sovereign bonds (issued in currencies other than domestic currencies). Because of the default risk, the yield for defaultable bonds will be higher than otherwise identical default-free bonds. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">存在违约风险的债券包括公司债券，以及以本国货币以外的货币发行的主权债券。由于存在违约风险，它们的收益率会高于其他条件完全相同的无违约债券。</span></details>

The yield (or yield to maturity) $v(T)$ is defined to be the equivalent $T$-year rate matching the bond price $B(0,T)$, i.e. $v(T)$ solves the equation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">收益率（或到期收益率）v(T) 定义为与债券价格 B(0, T) 相匹配的等价 T 年期利率，即 v(T) 满足下列方程：</span></details>

$$
B(0,T)=e^{-v(T)T}+\int_0^T\rho e^{-v(T)s}ds.
$$

The first term above is related to the payment at maturity, and the second term is related to the coupon payment. Since the r.h.s. of the above equation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">上式第一项与到期付款有关，第二项与票息支付有关。由于上述方程的右侧……</span></details>

## PDF p.2

is a decreasing function of $v(T)$, it has a unique solution. Also note that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">……是 v(T) 的递减函数，因此该方程有唯一解。另外，注意到：</span></details>

$$
\int_0^T\rho e^{-v(T)s}ds=\frac{\rho}{v(T)}\left(1-e^{-v(T)T}\right),
$$

> [!note] 推导过程：连续票息现值积分
> **1. 明确积分变量与常数。** 积分变量是 $s$；对于一只到期日已经确定的债券，$T$ 固定，因此 $v(T)$ 虽然随到期日 $T$ 而变化，但不随积分变量 $s$ 变化，在这个积分中是常数。票息支付速率 $\rho$ 也是常数，所以可以提出积分号：
> $$
> \int_0^T\rho e^{-v(T)s}\,ds
> =\rho\int_0^T e^{-v(T)s}\,ds.
> $$
>
> **2. 求原函数。** 先假设 $v(T)\ne0$。根据链式法则：
> $$
> \frac{d}{ds}e^{-v(T)s}=-v(T)e^{-v(T)s}.
> $$
> 因此，要让求导后的系数变成 $1$，需要除以 $-v(T)$：
> $$
> \int e^{-v(T)s}\,ds=-\frac{1}{v(T)}e^{-v(T)s}+C.
> $$
>
> **3. 代入上下限，按“上限值减下限值”计算。**
> $$
> \begin{aligned}
> \int_0^T\rho e^{-v(T)s}\,ds
> &=\rho\left[-\frac{1}{v(T)}e^{-v(T)s}\right]_0^T\\
> &=\rho\left(-\frac{e^{-v(T)T}}{v(T)}+\frac{e^0}{v(T)}\right)\\
> &=\frac{\rho}{v(T)}\left(1-e^{-v(T)T}\right).
> \end{aligned}
> $$
> 这里 $e^0=1$；减去下限处的负数，就变成了正数，所以最后括号中是 $1-e^{-v(T)T}$。
>
> **4. 零收益率的特殊情况。** 若 $v(T)=0$，不能直接使用含除法的表达式，而应回到原积分：
> $$
> \int_0^T\rho e^{0}\,ds=\rho T.
> $$
> 这也等于上面结果在 $v(T)\to0$ 时的极限。直观上，收益率为零意味着无需折现，连续支付 $T$ 年的票息总额就是 $\rho T$。


so the equation can be rewritten as <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，该方程可以改写为：</span></details>

$$
B(0,T)=e^{-v(T)T}+\frac{\rho}{v(T)}\left(1-e^{-v(T)T}\right).
$$

Due to the default risk, the yield for defaultable bonds $v(T)$ will be bigger than the default-free rate $r$. The difference <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于存在违约风险，违约债券的收益率 v(T) 会高于无违约利率 r。二者之差为：</span></details>

$$
v(T)-r\geq0
$$

is called yield spread. Yield spreads may have variety shapes, upward, downward, humped. Many factors may influence yield spreads, e.g. credit ratings, interest rate, etc. The shapes of credit spreads will be discussed in Lectures 3 and 4. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这一差值称为收益率利差。收益率利差曲线可能呈上升、下降或驼峰形等多种形状。信用评级、利率等许多因素都可能影响收益率利差。信用利差的形状将在第 3、4 讲中讨论。</span></details>

**(2) Credit risk is relevant for the capital structure of a firm** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（2）信用风险与企业资本结构有关。</span></details>

Two ways for a firm to get capital are issuing bonds (or taking debts) or issuing stocks (or equity). The main differences between a bond and a stock are: (a) The equity holders control the firm. (b) Upon default the debt holders has the right to collect the money first, which means that the equity value is zero upon default. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">企业筹资的两种方式是发行债券（或举债）和发行股票（或股权融资）。债券与股票的主要区别是：（a）股东控制企业；（b）发生违约时，债权人享有优先受偿权，这意味着股权价值在违约时为零。</span></details>

One important corporate decision for a firm to make is to choose the debt equity ratio. In other words, if the firm needs money, the firm has to decide how much capital should be financed by issuing debt and how much capital should be financed by issuing equity. Credit risk plays an important role in deciding the capital structure. The higher probability of default, the more costly it is to issue debt, because of the potential bankruptcy costs. On the other hands, firms typically get tax benefits from the coupon payments of debts, as the coupon payments are tax deductible. Therefore, the choice of capital structure is a balance between the trade-off of the tax benefit and bankruptcy costs. The celebrated Modigliani-Miller theorem provides a framework to address this issue. We will discuss the capital structure in Lecture 2. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">企业的一项重要决策是选择债务与股权的比例。企业需要资金时，必须决定有多少通过发行债务筹集，有多少通过发行股权筹集。信用风险在资本结构决策中十分重要：违约概率越高，潜在破产成本越大，发行债务的成本也越高。另一方面，债务票息通常可以税前扣除，因此带来税收利益。资本结构的选择是在税收利益与破产成本之间进行权衡。著名的莫迪利安尼-米勒定理为研究这一问题提供了框架。第 2 讲将讨论资本结构。</span></details>

**(3) Credit risk is relevant for the equity prices** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（3）信用风险与股票价格有关。</span></details>

As we just mentioned that upon default the equity value is zero. Thus, the equity values is affected by the credit risk. This in turn will affect options on the equity values. For example, on Jan 18th, 2006, the GM stock is traded at about \$20. The Jan 2007 put option with the largest open interest is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">如前所述，违约时股权价值为零。因此，股权价值受到信用风险影响，进而影响以股权为标的的期权。例如，2006 年 1 月 18 日，通用汽车（GM）的股价约为 20 美元。2007 年 1 月到期、未平仓合约量最大的看跌期权……</span></details>

## PDF p.3

at the strike price 10, which is traded around \$2.10. This implies a quite significant default probability for GM. Indeed GM went into bankruptcy during the 2008 financial crisis. This will be discussed in Lecture 5. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">……执行价为 10 美元，交易价格约为 2.10 美元。这意味着市场认为 GM 存在相当显著的违约概率。此后，GM 在 2008 年金融危机期间陷入破产。这一内容将在第 5 讲中讨论。</span></details>

**(4) Credit risk is relevant for pricing credit derivatives** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（4）信用风险与信用衍生品定价有关。</span></details>

Credit derivatives are useful for transferring credit risk from one party to another. Some popular credit derivatives are <details class="translation-details"><summary>中文译文</summary><span class="translation-body">信用衍生品可用于将信用风险从一方转移给另一方。常见的信用衍生品包括：</span></details>

- Credit default swaps (CDS), which pay certain amount once the default event occurs. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">信用违约互换（CDS）：一旦发生违约事件，就支付一定金额。</span></details>
- Collateralized debt obligations (CDO), whose payoffs depend on the default events within a portfolio of bonds or debts. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">债务抵押证券（CDO）：其收益取决于债券或债务组合中的违约事件。</span></details>
- Credit spread options. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">信用利差期权。</span></details>

There are two basic modeling approaches to study credit risk. The first one is the structural approach, which attempts to first build models for the firm asset, and then study the implication of credit events to bond prices, equity values, options on bonds, and credit derivatives. The second one, reduced-form models, takes the bond prices (or more precisely the yield curves of bonds) as given in the market, and then try to study bond options and credit derivatives. In other words, the main difference between the two is that in the structural approach the bond prices are derived, while in the reduced-form approach the bond prices are taken from the market data. The structural models will be discussed in Lectures 2, 3, 4, 5, and the reduced-form models will be studies in Lectures 6 and 7. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">研究信用风险有两种基本建模方法。第一种是结构化方法：先对企业资产建立模型，再研究信用事件对债券价格、股权价值、债券期权和信用衍生品的影响。第二种是简约模型：将市场债券价格，更准确地说是债券收益率曲线，作为已知条件，再研究债券期权与信用衍生品。两者的主要区别是：结构化方法推导债券价格，简约方法从市场数据获得债券价格。结构模型将在第 2 至第 5 讲讨论，简约模型将在第 6、7 讲讨论。</span></details>

### 2 Basic Terminologies <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2 基本术语。</span></details>

#### 2.1 Credit Ratings <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.1 信用评级。</span></details>

There are two major credit rating agencies in U.S., Moody’s and S&P, which provide ratings indicating the creditworthiness of corporate bonds and of sovereign countries. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">美国有两家主要信用评级机构：穆迪与标准普尔。它们为公司债券和主权国家提供评级，以反映其信用状况。</span></details>

In Moody’s system, the highest rating is Aaa, followed by Aa, A, Baa, Ba, B, and Caa. Bonds with ratings Baa or higher are called investment grade bonds, otherwise, junk bonds. The corresponding S&P ratings are AAA, AA, A, BBB, BB, B, and CCC. The finer ratings also exist. For example, for Moody’s there are three subcategories within Aa, namely Aa1, Aa2, and Aa3, with Aa1 being higher than the other two; for S&P the subcategories with AA are AA+, AA, AA-. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">穆迪评级体系的最高等级为 Aaa，之后依次是 Aa、A、Baa、Ba、B、Caa。评级为 Baa 或以上的债券称为投资级债券，其余称为垃圾债券。对应的标准普尔评级为 AAA、AA、A、BBB、BB、B、CCC。评级还可以细分：穆迪将 Aa 分为 Aa1、Aa2、Aa3，其中 Aa1 最高；标准普尔将 AA 分为 AA+、AA、AA-。</span></details>

## PDF p.4

Generally, the higher credit rating the lower probability of default. Below is the historical default probability from Moody’s. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">一般而言，信用评级越高，违约概率越低。下表为穆迪提供的历史违约概率。</span></details>

Average Cumulative Default Probability (in percent), 1970-2003. (From Moody’s) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1970—2003 年平均累计违约概率（单位：%，来源：穆迪）。Years 表示年数，评级符号保持原样。</span></details>

| Years | 1 | 2 | 3 | 4 | 5 | 7 | 10 | 15 | 20 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Aaa | 0.00 | 0.00 | 0.00 | 0.04 | 0.12 | 0.29 | 0.62 | 1.21 | 1.55 |
| Aa | 0.02 | 0.03 | 0.06 | 0.15 | 0.24 | 0.43 | 0.68 | 1.51 | 2.70 |
| A | 0.02 | 0.09 | 0.23 | 0.38 | 0.54 | 0.91 | 1.59 | 2.94 | 5.24 |
| Baa | 0.20 | 0.57 | 1.03 | 1.62 | 2.16 | 3.24 | 5.10 | 9.12 | 12.59 |
| Ba | 1.26 | 3.48 | 6.00 | 8.59 | 11.17 | 15.44 | 21.01 | 30.88 | 38.56 |
| B | 6.21 | 13.76 | 20.65 | 26.66 | 31.99 | 40.79 | 50.03 | 59.21 | 60.73 |
| Caa | 23.65 | 37.20 | 48.02 | 55.56 | 60.83 | 69.36 | 77.91 | 80.23 | 80.23 |

We can compute probabilities of default for a given year by using the above cumulative probabilities. For example, for Caa bonds, the average probability of default during year 2 is $0.3720-0.2365=0.1355$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">可以利用上述累计概率计算某一年的违约概率。例如，Caa 债券在第 2 年内的平均违约概率为 0.3720 − 0.2365 = 0.1355。</span></details>

One empirical observation is that for high grade bonds the default probability is a increasing function of time, while for low grade bonds the default probability decreases over time. For example, for A-rated bonds, the average default probabilities during years 1, 2, 3, 4, 5 are 0.02%, 0.07%, 0.14%, 0.15%, and 0.16%, respectively; while for Caa rated bonds, they are 23.65%, 13.55%, 10.82%, 7.54%, and 5.27%. The reason is mean-reverting, i.e. a firm with great creditworthiness now will likely be less financially healthy later, and a firm facing financial distress will likely to improve its credit rating if the firm can survive during the first one or two years. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">一个经验观察是，高评级债券的年度违约概率随时间上升，而低评级债券的年度违约概率随时间下降。例如，A 评级债券在第 1 至第 5 年内的平均违约概率分别为 0.02%、0.07%、0.14%、0.15%、0.16%；Caa 债券则分别为 23.65%、13.55%、10.82%、7.54%、5.27%。原因在于均值回归：现在信用状况很好的企业，日后的财务状况可能有所恶化；财务困难企业若能在最初一两年生存下来，信用评级往往有望改善。</span></details>

There are some connections between default probabilities and business cycles, especially for low-grade bonds. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">违约概率与经济周期存在一定联系，对低评级债券尤其如此。</span></details>

#### 2.2 Default Intensities <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.2 违约强度。</span></details>

The previous table reported unconditional probabilities of default. For our purpose it is more convenient to study conditional probability of defaults, which is also related to hazard rate or default intensity. This is also useful to give us an intuition about the generator of a transition matrix later when we discuss how to estimate transition matrices. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">前表报告的是无条件违约概率。后续分析中，研究条件违约概率更加方便；它与风险率或违约强度有关，也有助于直观理解后面估计迁移矩阵时使用的生成矩阵。</span></details>

The default intensity (or hazard rate) $\lambda(t)$ is defined to be <details class="translation-details"><summary>中文译文</summary><span class="translation-body">违约强度（或风险率）λ(t) 定义为：</span></details>

$$
\lambda(t)=\frac{f_\tau(t)}{P(\tau>t)},
$$

where $\tau$ is the default time, and $f_\tau(t)$ is the density function of $\tau$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 τ 为违约时间，fτ(t) 为 τ 的概率密度函数。</span></details>

## PDF p.5

To interpret $\lambda(t)$, consider the probability of default right after time $t$, given the default has not happened by time $t$, or more precisely $P(\tau\in(t,t+dt)\mid\tau>t)$. Now <details class="translation-details"><summary>中文译文</summary><span class="translation-body">为理解 λ(t)，考虑已知时间 t 之前没有违约时，紧接 t 之后违约的概率，更准确地说，就是已存活到 t 的条件下，在 (t, t+dt) 内违约的概率。于是：</span></details>

$$
P(\tau\in(t,t+dt)\mid\tau>t)
=\frac{P(\tau\in(t,t+dt))}{P(\tau>t)}
\approx\frac{f_\tau(t)dt}{P(\tau>t)}
=\lambda(t)dt.
$$

Thus, the default intensity gives the instantaneous conditional default probability. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，违约强度给出了瞬时条件违约概率。</span></details>

To get an explicit representation of the hazard rate, note that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">为得到风险率的显式表示，注意到：</span></details>

$$
\lambda(t)=\frac{\frac{d}{dt}P(\tau\leq t)}{1-P(\tau\leq t)}.
$$

Integrating both sides gives <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对两边积分得到：</span></details>

$$
\begin{aligned}
\int_0^s\lambda(t)dt
&=\int_0^s\frac{\frac{d}{dt}P(\tau\leq t)}{1-P(\tau\leq t)}dt+C\\
&=\int_0^s\frac{dP(\tau\leq t)}{1-P(\tau\leq t)}+C
=-\ln(1-P(\tau\leq s))+C,
\end{aligned}
$$

or <details class="translation-details"><summary>中文译文</summary><span class="translation-body">或者：</span></details>

$$
P(\tau>s)=e^C\cdot\exp\left\{-\int_0^s\lambda(t)dt\right\}.
$$

Putting $s=0$ yields $1=e^C$, and therefore <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令 s = 0，得到 1 = eᶜ，因此：</span></details>

$$
P(\tau>s)=\exp\left\{-\int_0^s\lambda(t)dt\right\}.\tag{1}
$$

In terms of estimate the intensity from data, one can assume $\lambda(t)$ is piecewise constant, and replace $\frac{d}{dt}P(\tau\leq t)$ by $\{P(\tau\leq t+\Delta t)-P(\tau\leq t)\}/\Delta t$. For example, for the B-rated bond, the estimator for $\lambda(2)$ will be <details class="translation-details"><summary>中文译文</summary><span class="translation-body">根据数据估计强度时，可以假设 λ(t) 是分段常数，并以区间内累计违约概率的增量除以 Δt，替代累计违约概率关于时间的导数。例如，B 评级债券的 λ(2) 估计值为：</span></details>

$$
\frac{20.65-13.76}{100-13.76}=0.07989.
$$

### 3 Credit Transition Matrix <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3 信用评级迁移矩阵。</span></details>

Ratings at Year End <details class="translation-details"><summary>中文译文</summary><span class="translation-body">年末评级。下表 Initial Rating 表示初始评级，各列为年末评级；D 表示违约，数值单位为百分比。</span></details>

| Initial Rating | AAA | AA | A | BBB | BB | B | CCC | D |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| AAA | 93.06 | 6.29 | 0.45 | 0.14 | 0.06 | 0.00 | 0.00 | 0.00 |
| AA | 0.59 | 90.99 | 7.59 | 0.61 | 0.06 | 0.11 | 0.02 | 0.01 |
| A | 0.05 | 2.11 | 91.43 | 5.63 | 0.47 | 0.19 | 0.04 | 0.05 |
| BBB | 0.03 | 0.23 | 4.44 | 88.98 | 4.70 | 0.95 | 0.28 | 0.39 |
| BB | 0.04 | 0.09 | 0.44 | 6.07 | 82.73 | 7.89 | 1.22 | 1.53 |
| B | 0.00 | 0.08 | 0.29 | 0.41 | 5.32 | 82.06 | 4.90 | 6.95 |
| CCC | 0.00 | 0.00 | 0.31 | 0.63 | 1.57 | 9.97 | 55.82 | 31.58 |
| D | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100 |

## PDF p.6

The above table is the historical worldwide corporate average one-year transition probabilities from 1980 to 2002, reported by S&P. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">上表为标准普尔报告的 1980—2002 年全球公司历史平均一年期评级迁移概率。</span></details>

Clearly we can use the Markov chain method to analysis the above table. For example, (a) D is an absorbing state in the above Markov chain; (b) each row sum must equal to one; (c) if we denote the above matrix by $P=P(1)$ for the one-year transition matrix, then the two-year transition matrix is $P(2)=P^2$, by Chapman-Kolmogorov theorem. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">显然可以用马尔可夫链分析上表。例如：（a）D 是该马尔可夫链的吸收状态；（b）每行概率之和必须等于 1；（c）若将上述一年期迁移矩阵记为 P = P(1)，根据 Chapman-Kolmogorov 定理，两年期迁移矩阵为 P(2) = P²。</span></details>

### 4 Estimation of Credit Transition Matrix <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4 信用评级迁移矩阵的估计。</span></details>

There are at least three ways to do the estimation: empirical estimation, generator-based estimation, and intensity-based product estimation. Here are we discuss the first two methods. The last one is slightly more complicated and is valid for broader classes (e.g. non-homogeneous Markov chains with possible truncations in the observation). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">至少有三种估计方法：经验估计、基于生成矩阵的估计，以及基于强度的乘积估计。这里讨论前两种。最后一种稍复杂，但适用范围更广，例如观测可能存在截断的非齐次马尔可夫链。</span></details>

As a illustration, consider the following example. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">以下面的例子作说明。</span></details>

**Example.** (a) There are four credit classes, A, B, C, D. At the beginning, there are 10 firms in A, B, C, each. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例。（a）共有 A、B、C、D 四个信用等级。期初 A、B、C 各有 10 家企业。</span></details>

(b) In one month, one B rated firm migrates to C, and one B rated firm migrates to A, and both firms stay there for the rest of the year. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（b）第 1 个月，一家 B 评级企业迁移到 C，另一家 B 评级企业迁移到 A，两家企业此后在当年余下时间均保持新评级。</span></details>

(c) In two months, two A rated firms migrates to B, and stay there for the rest of the year. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（c）第 2 个月，两家 A 评级企业迁移到 B，此后当年内保持 B 评级。</span></details>

(d) In six months, one C rated firm migrates to B and stays there for the rest of the year. Furthermore, one C rate firm defaults. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（d）第 6 个月，一家 C 评级企业迁移到 B，此后当年内保持 B 评级。另外一家 C 评级企业违约。</span></details>

(e) Eight months later, a C rated firm defaults. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（e）第 8 个月，一家 C 评级企业违约。</span></details>

We can summarize the above transition in a table. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">上述迁移可以汇总为下表，Months 表示月份。</span></details>

| Months | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | | B,B | | | | | | | | | | |
| B | A,C | | | | | | | | | | | |
| C | | | | | | B,D | | D | | | | |
| D | | | | | | | | | | | | |

## PDF p.7

#### 4.1 Empirical Estimator <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4.1 经验估计量。</span></details>

A simple way to estimate the one-year transition matrix is available by counting empirical transitions between states. For example, the empirical estimator for the transition probability from A to B is 2/10=0.2, as there are two A-rated firms migrate to B; similarly the empirical estimator for the transition probability from A to C and from A to D are all zero, as there is no such transition in the observation. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">估计一年期迁移矩阵的一种简单方法，是统计状态之间实际发生的迁移。由于两家 A 评级企业迁移到 B，A 到 B 的经验迁移概率为 2/10 = 0.2。类似地，由于没有观察到 A 到 C 或 A 到 D 的迁移，这两个迁移概率的经验估计均为零。</span></details>

In summary, we have the following empirical estimator for the one-year transition matrix <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，一年期迁移矩阵的经验估计为：</span></details>

$$
\widehat P_{\mathrm{empirical}}=
\begin{pmatrix}
0.8&0.2&0&0\\
0.1&0.8&0.1&0\\
0&0.1&0.7&0.2\\
0&0&0&1
\end{pmatrix}.
$$

However, this estimator is not very good for several reasons. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">不过，这个估计量存在以下不足。</span></details>

(1) The estimator does not fully use the available information. For example, for this estimator, it does not matter whether the two transitions from A to B happen in two months or four months, or one happens in one month and another in five month. In other words, the exact time points of the transition are ignored in the estimation. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（1）没有充分利用现有信息。两次 A 到 B 的迁移是发生在第 2 个月还是第 4 个月，或分别发生在第 1 和第 5 个月，对这个估计量没有影响。换言之，估计忽略了迁移发生的准确时间点。</span></details>

(2) The estimated matrix has too many zeros. For example, the estimated transition probability from A to C is zero. Since there is a positive probability from A to B (0.8) and a positive probability from B to C (0.1), we would like to have a positive probability from A to C. But since there is no observed transition from A to C, the estimator simply ignore this possibility. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（2）估计矩阵中的零元素过多。例如，A 到 C 的估计迁移概率为零。但 A 到 B 的概率为正（原文写为 0.8），B 到 C 的概率也为正（0.1），因此我们希望 A 到 C 也有正概率。然而，经验估计量由于未直接观测到 A 到 C 的迁移，就忽略了这种可能性。</span></details>

Better estimation can be obtained by using other methods. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">使用其他方法可以得到更好的估计。</span></details>

#### 4.2 Generator-Based Estimator <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4.2 基于生成矩阵的估计量。</span></details>

We have shown that there is a one-to-one correspondence between default probability and default intensity. Similarly, according to the theory of Markov chain, there is a generator matrix $\Lambda$ associated with the matrix $P$ of transition probabilities between states. More precisely, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">前面已经说明，违约概率与违约强度之间存在一一对应关系。类似地，根据马尔可夫链理论，状态迁移概率矩阵 P 对应一个生成矩阵 Λ。具体来说：</span></details>

$$
\Lambda=
\begin{pmatrix}
-\lambda_{1,1}&\lambda_{1,2}&\cdots&\lambda_{1,K}\\
\lambda_{2,1}&-\lambda_{2,2}&\cdots&\lambda_{2,K}\\
\vdots&\vdots&\ddots&\vdots\\
\lambda_{K,1}&\lambda_{K,2}&\cdots&-\lambda_{K,K}
\end{pmatrix}
$$

## PDF p.8

and the sum of each row is equal to zero, i.e. $\lambda_{1,1}=\lambda_{1,2}+\cdots+\lambda_{1,K}$, etc. The intuition behind the generator $\Lambda$ is that it gives the instantaneous transition matrix, just as what the hazard rate does for a random variable. Thus, it can be viewed as the hazard rate for the whole transition matrix. The element $\lambda_{i,j}$ measures the intensity from state $i$ to state $j$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">每行之和等于零，即 λ₁,₁ = λ₁,₂ + … + λ₁,ₖ，其余各行类似。生成矩阵 Λ 给出了瞬时迁移情况，作用类似于描述随机变量的风险率，因此可以把它看作整个迁移矩阵的风险率。λᵢ,ⱼ 衡量从状态 i 到状态 j 的迁移强度。</span></details>

Furthermore, similar to the relationship in (1) between a default probability and its intensity, the $n$-step transition matrix is simply the exponential of $\Lambda n$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">类似于公式（1）中违约概率与强度的关系，n 步迁移矩阵就是 Λn 的矩阵指数：</span></details>

$$
P(n)=P^n=\exp\{\Lambda n\},
$$

where for any matrix $A$ the exponential function is defined to be <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对任意矩阵 A，其指数函数定义为：</span></details>

$$
\exp\{A\}=\sum_{i=0}^{\infty}\frac{A^i}{i!}.
$$

Most of software package can compute the above exponential function easily. For example in Matlab the code is expm. Note that the exponential function for a matrix is not equal to exponentiate each cells inside the matrix. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">大多数软件包都能方便地计算上述矩阵指数，例如 Matlab 使用 expm。需要注意，矩阵指数不等于分别对矩阵中的每个元素取指数。</span></details>

> [!example] 配套代码
> [[AMA572 Fixed-Income and Credit Risk/Lecture 1/03 - Matrix Exponential Approximation（Notebook 原文代码）|查看 Notebook：SciPy 计算与 k = 3、5、10 的泰勒近似]]。代码和 Notebook 原有输出均按单元格顺序收录。

Since $\lambda_{i,j}$ measures the intensity from state $i$ to state $j$, we can estimate it by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于 λᵢ,ⱼ 衡量从状态 i 到状态 j 的强度，可以按下式估计：</span></details>

$$
\widehat\lambda_{i,j}=\frac{M_{i,j}}{N_i},
$$

where $M_{i,j}$ is the number of transitions from $i$ to $j$, and $N_i$ is the cumulative time units in state $i$ for all firms. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Mᵢ,ⱼ 表示从 i 到 j 的迁移次数，Nᵢ 表示所有企业在状态 i 停留时间的累计总和。</span></details>

For example, in our example <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例如，在本例中：</span></details>

$$
N_A=8*\frac{12}{12}+2*\frac{2}{12}+1*\frac{11}{12},
$$

as there are eight firms stay in state A the whole year, two firms stay in A for two months (then they move to B) and one firm stays in A for 11 months (as it moves from B to A after one month). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因为有 8 家企业全年保持 A 评级，两家企业在 A 停留 2 个月后迁移到 B，还有一家企业在第 1 个月从 B 迁移到 A，因此在 A 停留 11 个月。</span></details>

$$
M_{A,B}=2,
$$

as there are two transitions from A to B. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因为发生了两次 A 到 B 的迁移。</span></details>

In our example, the estimator becomes <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，本例中的估计量为：</span></details>

$$
\widehat\lambda_{A,B}
=\frac{2}{8*\frac{12}{12}+2*\frac{2}{12}+1*\frac{11}{12}}
=0.21622,
$$

$$
\widehat\lambda_{B,A}
=\frac{1}{8*\frac{12}{12}+2*\frac{1}{12}+2*\frac{10}{12}+1*\frac{6}{12}}
=0.09677,
$$

$$
\widehat\lambda_{B,C}
=\frac{1}{8*\frac{12}{12}+2*\frac{1}{12}+2*\frac{10}{12}+1*\frac{6}{12}}
=0.09677,
$$

## PDF p.9

$$
\widehat\lambda_{C,B}
=\frac{1}{7*\frac{12}{12}+1*\frac{11}{12}+2*\frac{6}{12}+1*\frac{8}{12}}
=0.10435,
$$

$$
\widehat\lambda_{C,D}
=\frac{2}{7*\frac{12}{12}+1*\frac{11}{12}+2*\frac{6}{12}+1*\frac{8}{12}}
=0.20870,
$$

$$
\widehat\lambda_{A,C}=\widehat\lambda_{A,D}=\widehat\lambda_{B,D}=\widehat\lambda_{C,A}=0.
$$

Thus, the estimator of the generator matrix is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，生成矩阵估计为：</span></details>

$$
\widehat\Lambda=
\begin{pmatrix}
-0.21622&0.21622&0&0\\
0.09677&-0.19354&0.09677&0\\
0&0.10435&-0.31305&0.20870\\
0&0&0&0
\end{pmatrix}.
$$

Therefore, the one-year transition matrix is estimated by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，一年期迁移矩阵估计为：</span></details>

$$
\widehat P_{\mathrm{generator}}=\exp(\widehat\Lambda)=
\begin{pmatrix}
0.81407&0.17707&0.00825&0.00061\\
0.07925&0.83663&0.07556&0.00857\\
0.00398&0.08148&0.73507&0.17948\\
0&0&0&1
\end{pmatrix}
$$

The generator-based estimator uses the available information and leads to nonzero transition probabilities. Therefore, in this sense, it is better than the empirical estimator. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">基于生成矩阵的估计量利用了现有信息，并给出非零迁移概率。从这一意义上说，它优于经验估计量。</span></details>

**Exercise 1.** Compute the empirical and generator-based estimators of one-year transition matrix for the following data.(a) There are four credit classes, A, B, C, D. At the beginning, there are 20 firms in A, B, C, each. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">练习 1。根据下列数据，计算一年期迁移矩阵的经验估计量及基于生成矩阵的估计量。（a）共有 A、B、C、D 四个信用等级。期初 A、B、C 各有 20 家企业。</span></details>

(b) In one month, one B rated firm migrates to C, and two B rated firms migrate to A, and both firms stay there for the rest of the year. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（b）第 1 个月，一家 B 评级企业迁移到 C，两家 B 评级企业迁移到 A；这些企业此后当年内保持新评级。</span></details>

(c) In three months, one A rated firm migrates to B, and stays there for the rest of the year. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（c）第 3 个月，一家 A 评级企业迁移到 B，此后当年内保持 B 评级。</span></details>

(d) In seven months, two C rated firms migrate to B and stay there for the rest of the year. Furthermore, one C rate firm defaults. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（d）第 7 个月，两家 C 评级企业迁移到 B，此后当年内保持 B 评级；另有一家 C 评级企业违约。</span></details>

(e) Ten months later, two C rated firms default. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（e）第 10 个月，两家 C 评级企业违约。</span></details>

> [[AMA572 Fixed-Income and Credit Risk/Lecture 1/02 - 课内练习解答（英文原文与折叠译文）#PDF p.1|查看原练习解答 PDF 第 1—2 页的转录]]

## PDF p.10

### 5 Differences between Historical Default Probabilities and Implied Risk-Adjusted Default Probabilities <details class="translation-details"><summary>中文译文</summary><span class="translation-body">5 历史违约概率与隐含风险调整违约概率的区别。</span></details>

Just like in the option pricing theory, one can get implied volatility from call/put options, i.e. implied risk-neutral volatility, or one can estimate historical volatility from historical stock returns. If (i) the market follows exactly geometric Brownian motion (ii) if the market is perfect (meaning no transaction costs, no borrowing and short-selling constraints, etc.) (iii) if one can trade the underlying asset continuously, then in theory the two approaches should give the same answer. However, in practice, none of the above conditions holds. Therefore, there is a significant difference between the historical volatility and implied risk-neutral volatility, mainly because if the model has any additional risk components (e.g. jump risk, or stochastic volatility), or any imperfection, or if the continuous trading is impossible, then the Black-Scholes theory will not be true. More general theories will tell us that in equilibrium the option prices should be computed under a risk-adjusted probability[^1]. Therefore, all the implied parameters from options will be risk-adjusted parameters, not the original physical parameters. Hence, the historical volatility will be quite different from implied volatility, as the latter may depend on investor’s utility functions and other equilibrium parameters. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">与期权定价理论类似，可以从看涨／看跌期权推导隐含波动率，即隐含风险中性波动率；也可以用历史股票收益率估计历史波动率。如果（i）市场严格服从几何布朗运动；（ii）市场完美，即无交易成本、借贷与卖空约束等；（iii）标的资产可以连续交易，那么理论上两种方法应得到相同结果。然而，现实中这些条件都不完全成立。若模型存在跳跃风险、随机波动率等额外风险成分，市场存在不完美，或无法连续交易，Black-Scholes 理论就不再成立，因此历史波动率与隐含风险中性波动率会有显著差异。更一般的理论指出，均衡下的期权价格应在风险调整概率下计算。因此，从期权反推的参数都是风险调整参数，而非原始的物理参数。隐含波动率可能取决于投资者效用函数及其他均衡参数，因而可能与历史波动率大不相同。</span></details>

When should we use implied parameters and when should we use historical parameters? If we want to compute derivative prices, then we should use appropriate implied parameters. If we want to calculate the present values of expected future cash flows or carry out scenario analysis to calculate potential future loss from defaults, then we should choose historical parameters. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">什么时候用隐含参数，什么时候用历史参数？计算衍生品价格时，应采用适当的隐含参数；计算预期未来现金流的现值，或通过情景分析计算未来违约可能造成的损失时，应选择历史参数。</span></details>

Note that one advantage of using implied default probabilities is that you can get the values from market security prices frequently, unless historical default probabilities, which, for example, are reported by rating agencies a few times per year. However, one main disadvantage of using implied default probabilities is that different securities give different implied default probabilities; one has to figure out which one to use. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">隐含违约概率的一个优点，是可以频繁地从市场证券价格获取；历史违约概率则可能一年只由评级机构发布几次。但其主要缺点是，不同证券会给出不同的隐含违约概率，需要判断应采用哪一个。</span></details>

As we shall see implied default probabilities are in general much bigger than corresponding historical default probabilities. The following table is a typical example, with the historical default intensities computed from Moody’s historical default data as given previously, and implied default intensity computed from bond prices from Merrill Lych. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">一般来说，隐含违约概率远高于对应的历史违约概率。下表是典型例子：历史违约强度由前述穆迪历史违约数据计算，隐含违约强度则由美林的债券价格计算。</span></details>

[^1]: In general, there will not be a unique risk-neutral probability. The risk-adjusted probability will be a particular risk-neutral probability.
<details class="translation-details"><summary>中文译文</summary><span class="translation-body">原文脚注 1：一般而言，风险中性概率未必唯一；风险调整概率是某一个特定的风险中性概率。</span></details>

## PDF p.11

| Rating | 7-year Average Historical Default Intensity (%) | 7-year Implied Default Intensity (%) | Ratio |
|---|---:|---:|---:|
| Aaa | 0.04 | 0.67 | 16.8 |
| Aa | 0.06 | 0.78 | 13 |
| A | 0.13 | 1.28 | 9.8 |
| Baa | 0.47 | 2.38 | 5.1 |
| Ba | 2.47 | 5.07 | 2.1 |
| B | 7.69 | 9.02 | 1.2 |
| Caa | 16.90 | 21.30 | 1.3 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头依次为：评级、7 年平均历史违约强度（%）、7 年隐含违约强度（%）、二者比率。</span></details>

For example, for the A-rate class, it follows from the table of Section 2.1 that we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例如，依据第 2.1 节的表，A 评级有：</span></details>

$$
P(\tau<7)=0.91\%.
$$

Then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此：</span></details>

$$
P(\tau\geq7)=1-P(\tau<7)=1-0.0091.
$$

So, the computation for the historical default intensity is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">所以，历史违约强度计算为：</span></details>

$$
-\frac{1}{7}\ln(1-0.0091)=0.13\%,
$$

by estimating the average hazard rate $\bar\lambda(t)$ in <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这里估计的是下式中的平均风险率 λ̄(t)：</span></details>

$$
P(\tau\geq t)=\exp\left\{-\int_0^t\lambda(s)ds\right\}
=:\exp\{-\bar\lambda(t)t\}.
$$

There are several reasons for the big difference. (1) Since default probabilities are related to corporate/foreign bonds, investors demand extra returns for liquidity, as corporate/foreign bonds are relatively illiquid comparing to default-free bonds, e.g. U.S. treasury bonds. (2) Historical default probabilities are estimated within a given time periods. Bond holders may want to allow for extra rooms for the range outside the given time periods. (3) Unlike stocks, bond portfolios are in general not as diversified as stock portfolios, whence investors may demand extra returns for bearing undiversified risk. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">两种强度差异很大，原因可能有：（1）公司债／外国债相较于美国国债等无违约债券流动性较差，投资者要求额外流动性补偿；（2）历史违约概率只由特定样本期估计，持有人可能希望为样本期以外的情况留出额外安全余量；（3）债券组合通常不如股票组合充分分散，投资者可能要求额外回报，以承担未分散的风险。</span></details>

### 6 Estimating Risk-Adjusted Default Probabilities from Bond Prices <details class="translation-details"><summary>中文译文</summary><span class="translation-body">6 根据债券价格估计风险调整违约概率。</span></details>

To estimate default probabilities from bond prices, one needs to make assumptions about recovery rates. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">根据债券价格估计违约概率，需要对回收率作出假设。</span></details>

## PDF p.12

#### 6.1 Recovery <details class="translation-details"><summary>中文译文</summary><span class="translation-body">6.1 回收。</span></details>

How much the debt holders can recover once a default occurs is matter of arts rather than science, as the whole recovery process involves complicated legal and financial issues. However, there are some well-established empirical evidences. For example, for high-tech companies (such as internet and biotech companies), the recovery values are generally low, as they have few tangible assets; while for asset-rich (e.g. such as airlines and utility) industries, the recovery values are generally high. There are also some empirical evidences supporting that the higher historical default probabilities the lower recovery rates. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">违约后债权人能收回多少，更依赖经验判断，因为回收过程涉及复杂的法律和财务问题。不过，已有一些较明确的经验证据。例如，互联网、生物科技等高科技企业有形资产较少，回收价值通常较低；航空、公用事业等资产丰富的行业，回收价值通常较高。还有证据表明，历史违约概率越高，回收率往往越低。</span></details>

In terms of modelling, there are three popular recovery assumptions. The first is the recovery at a fraction of par value. (For example, if a bond promises to pay \$1 at maturity, then the par value is \$1.) The second is recovery at a fraction of the market value of the bond just before default. The third is recovery at a fraction of the value of otherwise identical default-free bond. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">建模时有三种常用回收假设：第一，按面值的一定比例回收（例如，债券承诺到期支付 1 美元，其面值就是 1 美元）；第二，按债券违约前市场价值的一定比例回收；第三，按其他条件相同的无违约债券价值的一定比例回收。</span></details>

The first one is probably the mostly observed in practice, although the other two are also quite common. The last two approaches may lead to better analytical tractability. We shall use all of the three assumptions in this course. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第一种假设可能在实践中最常见，另外两种也相当常用。后两种方法可能更便于数学分析。本课程将使用全部三种假设。</span></details>

The recovery values also depend on the seniority of the debt. Assuming recovery at a fractional par value, the historical recovery rates from 1982 to 2003 computed by Moody’s are given in the following table. One observation from the table is that the default cost is quite high. Even for senior secured debts, the loss is almost 50%. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">回收价值也取决于债务偿付优先级。假设按面值比例回收，穆迪根据 1982—2003 年数据计算的历史回收率如下。表中可见违约成本很高：即使高级有抵押债务，损失也接近 50%。</span></details>

| Class | Average Recovery Rate (%) |
|---|---:|
| Senior secured | 51.6 |
| Senior unsecured | 36.1 |
| Senior subordinated | 32.5 |
| Subordinated | 31.1 |
| Junior subordinated | 24.5 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头为债务类别、平均回收率（%）。各行依次为高级有抵押债务、高级无抵押债务、高级次级债务、次级债务、初级次级债务。</span></details>

Of course the above table only gives the average recovery rates. For two firms, one being asset rich and the other not, the senior secured debts of the two firms will have different recovery rate, although the debts belongs to the same class. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">上表只提供平均回收率。两家企业如果一家资产丰富、另一家并非如此，即使债务属于相同类别，两者高级有抵押债务的回收率也会不同。</span></details>

## PDF p.13

#### 6.2 Implied Default Probabilities from Bond Prices <details class="translation-details"><summary>中文译文</summary><span class="translation-body">6.2 根据债券价格计算隐含违约概率。</span></details>

To illustrate the method, consider a corporate bond with maturity 5 years, and a coupon payment 6% (paid semiannually), with the par value \$100. Assume that the current yield of the bond is 7% per year (with continuous compounding), while the current yield on the otherwise identical risk-free bond is 5% (with continuous compounding). Furthermore, assume the recovery is 40% at the par value. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">为说明这种方法，考虑一只 5 年期公司债券，票息率为 6%，每半年付息，面值为 100 美元。假设当前连续复利年收益率为 7%，其他条件相同的无风险债券连续复利收益率为 5%，回收金额为面值的 40%。</span></details>

Then we have the following table, assuming the default can only happen at times 0.5, 1.5, 2.5, 3.5, 4.5 years, and the one-year default probabilities are the same. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">假设违约仅发生在第 0.5、1.5、2.5、3.5、4.5 年，且每年违约概率相同，可得下表。</span></details>

| Time (Years) | Default Intensity (per year) | Recovery Value (\$) | Risk-Free Value (\$) | Loss Given Default (\$) | Discount Factor | PV of Expected Loss (\$) |
|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | $P$ | 40 | 106.73 | 66.73 | 0.9753 | $65.08P$ |
| 1.5 | $P$ | 40 | 105.97 | 65.97 | 0.9277 | $61.20P$ |
| 2.5 | $P$ | 40 | 105.17 | 65.17 | 0.8825 | $57.52P$ |
| 3.5 | $P$ | 40 | 104.34 | 64.34 | 0.8395 | $54.01P$ |
| 4.5 | $P$ | 40 | 103.46 | 63.36 | 0.7985 | $50.67P$ |
| | | | | | Total: | $288.48P$ |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头依次为：时间（年）、年度违约强度、回收价值、无风险价值、违约损失、贴现因子、预期损失现值；金额单位均为美元。Total 表示合计。</span></details>

For example, the calculation for 3.5 is as follows. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例如，第 3.5 年的计算如下。</span></details>

(1) The risk-free value of the future cash flow at year 3.5 is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（1）在第 3.5 年，未来现金流的无风险价值为：</span></details>

$$
3+3e^{-0.05*0.5}+3e^{-0.05*1}+103e^{-0.05*1.5}=104.34,
$$

as the payments at 3.5, 4, 4.5, 5 years are 3, 3, 3, 103, respectively. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因为第 3.5、4、4.5、5 年的支付金额分别为 3、3、3、103。</span></details>

> [!example] 课堂手写截图 1：预期违约损失表与现金流
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 1/附件/01_第13页_预期违约损失表与现金流_截图09-10_1900.PNG]]

(2) The loss if the default happens between year 3.5 and 4.5 is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（2）若违约发生于第 3.5 年与第 4.5 年之间，损失为：</span></details>

$$
104.34-40=64.34.
$$

(3) The discount factor is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（3）贴现因子为：</span></details>

$$
e^{-3.5*0.05}=0.8395.
$$

(4) The discounted loss if the default happens between year 3.5 and 4.5 is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（4）若违约发生在第 3.5 年与第 4.5 年之间，折现后的损失为：</span></details>

$$
64.34*0.8395=54.01.
$$

Now since the yield is 7% the corporate bond price is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">公司债券收益率为 7%，因此其价格为：</span></details>

$$
\begin{aligned}
&3e^{-0.07*0.5}+3e^{-0.07*1}+3e^{-0.07*1.5}+3e^{-0.07*2}+3e^{-0.07*2.5}\\
&+3e^{-0.07*3}+3e^{-0.07*3.5}+3e^{-0.07*4}+3e^{-0.07*4.5}+103e^{-0.07*5}=95.34.
\end{aligned}
$$

> [!example] 课堂手写截图 2：违约损失折现与公司债价格
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 1/附件/02_第13页_违约损失折现与公司债价格_截图09-10_1905.PNG]]

## PDF p.14

Similarly, the default-free bond price is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">类似地，无违约债券价格为：</span></details>

$$
3e^{-0.05*0.5}+\cdots+103e^{-0.05*5}=104.09.
$$

Setting the difference between the corporate bond and default-free bond equal to the PV of the expected loss yields <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令公司债券与无违约债券之间的价格差等于预期损失现值，可得：</span></details>

$$
104.09-95.34=288.48P,
$$

i.e. the implied default intensity (or implied one-year default probability given no default yet) is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即隐含违约强度（或已知此前尚未违约时的一年期隐含违约概率）为：</span></details>

$$
P=3.03\%.
$$

The above approach can be easily generalized to the case of different default probabilities for a given year, and with default happens more frequently than a year. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">上述方法可以推广到不同年份具有不同违约概率的情形，也可推广到违约发生频率高于每年一次的情形。</span></details>

**Exercise 2.** A company has issued 3- and 5-year bonds with a coupon payment of 4% per year payable annually. The yields on the bonds (in terms of continuous compounding) are 4.5% and 4.75%, respectively. Assume the risk-free rate is 3.5% for all maturities, and the recovery value is 40% of the par value. Also assume default can only take place halfway through each year, i.e. at year 0.5, 1.5, 2.5, etc. Compute $P_1$ and $P_2$, which are the implied default intensities per year for years 1 to 3 and for years 4 and 5, respectively. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">练习 2。一家公司发行了 3 年期和 5 年期债券，年票息率为 4%，每年付息一次。两只债券的连续复利收益率分别为 4.5% 和 4.75%。假设所有期限的无风险利率均为 3.5%，回收价值为面值的 40%。违约仅可能发生于每年年中，即第 0.5、1.5、2.5 年等时点。计算 P₁ 和 P₂，分别表示第 1 至第 3 年以及第 4、5 年的年度隐含违约强度。</span></details>

> [[AMA572 Fixed-Income and Credit Risk/Lecture 1/02 - 课内练习解答（英文原文与折叠译文）#PDF p.3|查看原练习解答 PDF 第 3—4 页的转录及手写批注]]
