---
course: AMA572 Fixed-Income and Credit Risk
created: "2026-10-20"
source: "01_Lecture5_原课件_强度模型与信用衍生品.pdf"
pages: 7
cssclasses:
  - ama-inline-translations
---

> [!info] 阅读方式
> 英文按 PDF 实际页序完整转录；仅合并排版换行与断词。公式、数值、题号及原文疑似笔误保留，译文不替原文纠错。点击段末「中文译文」展开对应中文；各段之间保留留白。
> [[AMA572 Fixed-Income and Credit Risk/Lecture 5/00 - Lecture 5 资料索引|资料索引]] · [[AMA572 Fixed-Income and Credit Risk/Lecture 5/附件/01_Lecture5_原课件_强度模型与信用衍生品.pdf|原始 PDF]]

## PDF p.1

# AMA572 Lecture 5 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AMA572 第 5 讲。</span></details>

**Intensity Based Reduced Form Models and Introduction to Credit Derivatives** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">基于强度的简约式模型（intensity-based reduced-form models）与信用衍生品简介。</span></details>

Unlike previous structural models, such as Merton, Black-Cox, and Leland-Toft models, which assume that there is a fundamental asset value which triggers the default, reduced form models do not model default explicitly. More precisely, reduced form models assume that there is some exogenous processes, such as intensity processes, drive the defaults, and take the bond prices as given. After we calibrate the defaultable bond price to the market, then we can use the bonds prices to compute prices for other derivatives. This is similar to the Black-Scholes model, in which we use stock prices to compute option prices. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">之前的结构式模型（structural models），例如 Merton、Black–Cox 和 Leland–Toft，都假设某个基础资产价值会触发违约；简约式模型则不显式刻画违约机制。更准确地说，它假设某些外生过程，例如强度过程，驱动违约，并将债券价格视为给定。把可违约债券价格校准至市场后，就可以利用这些债券价格计算其他衍生品价格。这类似于 Black–Scholes 模型利用股票价格计算期权价格。</span></details>

Popular reduced form models include Duffie-Singleton model, which is based on intensities, and Jarrow-Turnbull model, which is based on credit rating migration. Here we shall focus on the first model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">常见简约式模型包括基于强度的 Duffie–Singleton 模型，以及基于信用评级迁移的 Jarrow–Turnbull 模型。这里重点讨论前者。</span></details>

### 1 Duffie-Singleton Reduced Form Model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1 Duffie–Singleton 简约式模型。</span></details>

Reduced-form models take the probability of default as given by the market, unlike the structural models (such as Merton, Black-Cox, Leland-Toft models). In this lecture we shall focus on one particular reduced-form model, Duffie-Singleton (1999) Model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">与 Merton、Black–Cox 和 Leland–Toft 等结构式模型不同，简约式模型将违约概率视为市场给定。本讲重点介绍 Duffie–Singleton（1999）模型。</span></details>

#### 1.1 Hazard Rate and Intensity <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.1 风险率（hazard rate）与强度（intensity）。</span></details>

The hazard rate $h(t,T)$ measures the conditional probability of defaulting between $T$ and $T+dt$, given all the information available at time $t$. More precisely, let the default time be $\tau$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">风险率 h(t，T) 衡量：给定 t 时刻所有可得信息，在 T 至 T＋dt 之间违约的条件概率。具体地，设违约时间为 τ：</span></details>

$$
\begin{gathered}
S(t,T)=P(\tau>T\mid\mathcal F_t),\\
f(t,T)=\frac{\partial S(t,T)}{\partial T},\\
h(t,T)=\frac{f(t,T)}{S(t,T)}=\frac1{S(t,T)}\frac{\partial S(t,T)}{\partial T}.
\end{gathered}
$$

Then, it can be shown that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">可以证明：</span></details>

$$
S(t,T)=\exp\left\{-\int_t^T h(t,s)ds\right\}.
$$

## PDF p.2

The intensity $\lambda(t)$ measures the instantaneous defaults rate. More precisely, there is a unique stochastic process $\lambda(t)$ such that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">强度 λ(t) 衡量瞬时违约率。更准确地说，存在唯一随机过程 λ(t)，使得：</span></details>

$$
N(t)-\int_0^t\lambda(s)ds
$$

is a martingale, and under suitable conditions <details class="translation-details"><summary>中文译文</summary><span class="translation-body">是一个鞅，并且在适当条件下：</span></details>

$$
\lambda(t)=h(t,t).
$$

Here $N(t)$ is a counting process <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 N(t) 为计数过程（counting process）：</span></details>

$$
N(t)=I\{\tau\leq t\}.
$$

#### 1.2 The Model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.2 模型。</span></details>

Consider a European contingent claim whose payoff is given by $g(T)$. This is a quite general framework. For example, for the zero coupon bond $g(T)=1$. Suppose the recovery value is a fraction, $\delta$, of the market value of the contingent claim right before the default. The key result of Duffie-Singleton model is that the value of the contingent claim at time $t$ is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑到期收益为 g(T) 的欧式或有索取权（European contingent claim）。这一框架相当一般，例如零息债券有 g(T)＝1。假设回收价值等于违约前一刻该索取权市场价值的比例 δ。Duffie–Singleton 模型的核心结果是，t 时刻该索取权的价值为：</span></details>

$$
g(t)=E^*\left[\exp\left\{-\int_t^T[r(s)+(1-\delta)\lambda(s)]ds\right\}\cdot g(T)\mid\mathcal F_t\right].\tag{1}
$$

**Remarks.** (1) In the above formula the risk-free rate $r(s)$ may be stochastic, and the default intensity may also be a stochastic process. (2) For zero-coupon bond we have at time 0 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">说明：（1）上式中的无风险利率 r(s) 可以随机，违约强度也可以是随机过程。（2）对于零息债券，零时刻有：</span></details>

$$
B(0,T)=E^*\left[\exp\left\{-\int_0^T[r(s)+(1-\delta)\lambda(s)]ds\right\}\right].
$$

(3) After we calibrate the default intensity $\lambda(t)$, then we can use $\lambda(t)$ to price other contingent claims. In other words, we view bond prices as given, and then use the bond prices to compute prices for other derivatives. This is similar to the Black-Scholes model, in which we use stock prices to compute option prices. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（3）校准违约强度 λ(t) 后，即可用其为其他或有索取权定价。换言之，将债券价格视为给定，再用它计算其他衍生品价格。这与 Black–Scholes 模型利用股票价格计算期权价格类似。</span></details>

#### 1.3 A Heuristic Derivation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.3 启发式推导（heuristic derivation）。</span></details>

We shall only give a heuristic explanation of (1). Consider a discrete time framework. We can think $h(t)dt$ as approximately the default probability in $(t,t+dt)$ and $r(t)$ as the approximate risk-free yield from $t$ to $t+dt$. Then the standard option pricing theory implies that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这里只对式（1）给出启发式解释。考虑离散时间框架，将 h(t)dt 视为 (t，t＋dt) 内违约概率的近似值，将 r(t) 视为从 t 到 t＋dt 的近似无风险收益率。标准期权定价理论给出：</span></details>

$$
g(t)=h(t)dt\cdot e^{-r(t)dt}E^*[\delta g(t+dt)\mid\mathcal F_t]+(1-h(t)dt)e^{-r(t)dt}E^*[g(t+dt)\mid\mathcal F_t],
$$

## PDF p.3

because the default payment is $\delta g(t+dt)$ and the non-default payment is $g(t+dt)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因为违约支付为 δg(t＋dt)，未违约支付为 g(t＋dt)。</span></details>

Introduce $R(t)$ such that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">引入 R(t)，使得：</span></details>

$$
\exp\{-R(t)\cdot dt\}=h(t)dt\cdot e^{-r(t)dt}\delta+(1-h(t)dt)e^{-r(t)dt}.\tag{2}
$$

Then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则：</span></details>

$$
g(t)=\exp\{-R(t)\cdot dt\}E^*[g(t+dt)\mid\mathcal F_t].
$$

Iterating the above expression yields <details class="translation-details"><summary>中文译文</summary><span class="translation-body">迭代上述表达式，得到：</span></details>

$$
g(t+dt)=\exp\{-R(t+dt)\cdot dt\}E^*[g(t+2dt)\mid\mathcal F_{t+dt}],
$$

and therefore <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，</span></details>

$$
\begin{aligned}
g(t)&=\exp\{-R(t)\cdot dt\}E^*[g(t+dt)\mid\mathcal F_t]\\
&=\exp\{-R(t)\cdot dt\}\cdot E^*\{\exp\{-R(t+dt)\cdot dt\}\cdot E^*[g(t+2dt)\mid\mathcal F_{t+dt}]\mid\mathcal F_t\}\\
&=E^*\{E^*[\exp\{-(R(t)+R(t+dt))\cdot dt\}\cdot g(t+2dt)\mid\mathcal F_{t+dt}]\mid\mathcal F_t\}\\
&=E^*[\exp\{-(R(t)+R(t+dt))\cdot dt\}\cdot g(t+2dt)\mid\mathcal F_t].
\end{aligned}
$$

Thus, continuing this procedure, we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">继续这一过程，得到：</span></details>

$$
g(t)=E^*[\exp\{-(R(t)+R(t+dt)+\cdots+R(T))\cdot dt\}\cdot g(T)\mid\mathcal F_t].\tag{3}
$$

Now we need to have an approximation for $R(t)$. Using the approximation $e^x\approx1+x$, we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">现在需要对 R(t) 作近似。利用 eˣ≈1＋x，有：</span></details>

$$
\exp\{-R(t)\cdot dt\}\approx1-R(t)\cdot dt,
$$

$$
\lambda(t)dt\cdot e^{-r(t)dt}\delta+(1-\lambda(t)dt)e^{-r(t)dt}\approx\lambda(t)dt\cdot(1-r(t)dt)\delta+(1-\lambda(t)dt)(1-r(t)dt),
$$

and, therefore, we have from (2) that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因而由式（2）得：</span></details>

$$
1-R(t)\cdot dt\approx\lambda(t)dt\cdot(1-r(t)dt)\delta+(1-\lambda(t)dt)(1-r(t)dt).
$$

In summary, we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">综上，</span></details>

$$
1-R(t)\cdot dt\approx\lambda(t)\delta dt-\lambda(t)r(t)\delta(dt)^2+1-\lambda(t)dt-r(t)dt+\lambda(t)r(t)(dt)^2.
$$

Ignoring the term $(dt)^2$ we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">忽略 (dt)² 项，有：</span></details>

$$
-R(t)\cdot dt\approx\lambda(t)\delta dt-\lambda(t)dt-r(t)dt,
$$

or <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即：</span></details>

$$
R(t)\approx\lambda(t)(1-\delta)+r(t).
$$

This in conjunction with (3) gives, as $dt\to0$, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">将其与式（3）结合，并令 dt→0，得到：</span></details>

$$
\begin{aligned}
g(t)&=E^*\left[\exp\left\{-\int_t^T R(s)ds\right\}\cdot g(T)\mid\mathcal F_t\right]\\
&=E^*\left[\exp\left\{-\int_t^T[\lambda(s)(1-\delta)+r(s)]ds\right\}\cdot g(T)\mid\mathcal F_t\right],
\end{aligned}
$$

which shows the result. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即证。</span></details>

## PDF p.4

### 2 Credit Default Swaps <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2 信用违约互换（credit default swaps，CDS）。</span></details>

#### 2.1 Background <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.1 背景。</span></details>

A credit default swap (CDS) is a traded insurance contract that provides payments against the risk of default. The buyer of the CDS makes periodic payment to the seller until either the contract reaches maturity or a credit event occurs. In the credit event, the seller of the CDS will make certain payment. For example, a buyer may pay 90 basis point on a notation amount \$10M once per year (i.e. \$90K per year) for 5 years, in exchange for a protection payment of difference between the face value of the debt and the market value of the debt after the credit event. For example, if the face value of the debt is \$100, but the market value is \$40 after the credit event, and the seller of the CDS will pay \$6m to the buyer. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">信用违约互换是一种可交易的保险合约，在违约风险发生时提供支付。买方定期向卖方付费，直至合约到期或发生信用事件（credit event）；发生信用事件时卖方支付约定金额。例如，买方以 1,000 万美元名义本金、每年 90 个基点付费，即每年 9 万美元，持续 5 年，换取发生信用事件后债务面值与市值差额的保护支付。若债务面值为 100、事件后市值为 40，则按该名义本金，卖方向买方支付 600 万美元。</span></details>

Back in 2008, all CDS contracts are not traded in exchanges. Now CDS contracts are traded in several exchanges. Even individual investors can buy CDS contracts via, e.g., International Exchange (ICE) and Chicago Mercantile Exchange (CME). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">回看 2008 年，CDS 合约并不在交易所交易。讲义称，现在已有数家交易所交易 CDS，个人投资者也能通过例如 ICE 和芝加哥商品交易所（CME）购买 CDS 合约。</span></details>

Two popular indices for CDS are: 5 year and 10 year CDX NA IG index which tracks 125 investment grade North American companies; 5 year and 10 year iTraxx Europe index which tracks 125 investment grade European companies. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">两种常见 CDS 指数为：5 年期和 10 年期 CDX NA IG，跟踪 125 家北美投资级企业；以及 5 年期和 10 年期 iTraxx Europe，跟踪 125 家欧洲投资级企业。</span></details>

In September 2009 US government bailed American International Group (AIG) out, mainly because AIG had been excessively selling CDS protection without hedging against the possibility that the reference entities, especially on Lehman, might decline in value, which exposed the insurance giant to potential losses over \$100 billion. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">原文称，美国政府于 2009 年 9 月救助美国国际集团（AIG），主要原因是 AIG 过度出售 CDS 保护，却没有对冲参考实体（尤其是雷曼）价值下跌的可能性，使这家保险巨头面临超过 1,000 亿美元的潜在损失。</span></details>

In April 2012, the market in credit default swaps was possibly being affected by the activities of Bruno Iksil, a trader for J.P. Morgan Chase & Co., referred to as ”the London whale” in reference to the huge positions he was taking. Heavy opposing bets to his positions were made by traders, including another branch of J.P. Morgan, who purchased the derivatives offered by J.P. Morgan in such high volume. \$2 billion losses were reported by the firm in May, 2012 in relationship to these trades. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2012 年 4 月，摩根大通交易员 Bruno Iksil 的交易活动可能影响了 CDS 市场。他因持仓规模庞大而被称为“伦敦鲸”（London whale）。包括摩根大通另一分支在内的交易者大量买入摩根大通提供的衍生品，对其仓位进行反向押注。该公司于 2012 年 5 月报告了与这些交易有关的 20 亿美元损失。</span></details>

#### 2.2 Valuation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.2 估值。</span></details>

We will illustrate the valuation of 5 year CDS via an example. In this example, we shall find out the break-even CDS spread $s$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">以下通过例子说明 5 年期 CDS 的估值，计算盈亏平衡利差（break-even spread）s。</span></details>

## PDF p.5

Assume: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">假设：</span></details>

1. The default intensity during any year is 0.02. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1. 每年的违约强度为 0.02。</span></details>

2. The risk-free rate is 5% <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2. 无风险利率为 5%。</span></details>

3. The recovery rate is 40%. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3. 回收率为 40%。</span></details>

4. Default can only happen at year 0.5, 1.5, 2.5, 3.5, 4.5. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4. 违约只可能发生在第 0.5、1.5、2.5、3.5、4.5 年。</span></details>

Since the payment from the buyer is typically in arrear (e.g. at year 1, 2, ..., 5), the calculation relies on computation of 3 payments. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于买方通常在期末付款（如第 1、2、……、5 年），需要计算三项支付。</span></details>

1. Regular payments by the buyer. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1. 买方的定期支付。</span></details>

2. Accrual payment by the buyer after the credit event. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2. 信用事件发生后买方支付的应计保费（accrual payment）。</span></details>

3. The payment from the seller to the buyer after the credit event. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3. 信用事件后卖方向买方支付的赔偿。</span></details>

The following table details item 1, with $s$ being the CDS spread. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">下表列出第 1 项，其中 s 为 CDS 利差。</span></details>

| Time (Years) | Prob. of Survival | Expected Payments | Discount Factor | PV of Exp Payment |
|---|---|---|---|---|
| 1 | 0.9800 | 0.9800 $s$ | 0.9512 | 0.9322 $s$ |
| 2 | 0.9604 | 0.9604 $s$ | 0.9048 | 0.8690 $s$ |
| 3 | 0.9412 | 0.9412 $s$ | 0.8607 | 0.8101 $s$ |
| 4 | 0.9224 | 0.9224 $s$ | 0.8187 | 0.7552 $s$ |
| 5 | 0.9039 | 0.9039 $s$ | 0.7788 | 0.7040 $s$ |
| Total | | | | 4.0704 $s$ |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头依次为：时间（年）、存续概率、预期支付、贴现因子、预期支付现值；Total 表示合计。本表列示买方常规保费。</span></details>


For example, in Year 3, the survival probability is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例如，第 3 年的存续概率为：</span></details>

$$
(1-0.02)^3=0.9412;
$$

the discounted factor is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">贴现因子为：</span></details>

$$
e^{-0.05*3}=0.8607;
$$

and the PV of expected payment is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">预期支付现值为：</span></details>

$$
0.9412s*0.8607=0.8101s.
$$

The following table details item 2, with $s$ being the CDS spread. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">下表列出第 2 项，其中 s 为 CDS 利差。</span></details>

## PDF p.6

| Time (Years) | Prob. of Default | Expected Payments | Discount Factor | PV of Exp Payment |
|---|---|---|---|---|
| 0.5 | 0.0200 | 0.0100 $s$ | 0.9753 | 0.0097 $s$ |
| 1.5 | 0.0196 | 0.0098 $s$ | 0.9277 | 0.0091 $s$ |
| 2.5 | 0.0192 | 0.0096 $s$ | 0.8825 | 0.0085 $s$ |
| 3.5 | 0.0188 | 0.0094 $s$ | 0.8395 | 0.0079 $s$ |
| 4.5 | 0.0184 | 0.0092 $s$ | 0.7985 | 0.0074 $s$ |
| Total | | | | 0.0426 $s$ |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头依次为：时间（年）、违约概率、预期支付、贴现因子、预期支付现值；Total 表示合计。本表列示买方在违约时支付的应计保费。</span></details>


For example, the default probability during the third year (which is assumed to happen exactly at time 2.5 year) is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例如，第 3 年违约（假定恰在第 2.5 年发生）的概率为：</span></details>

$$
0.02*(1-0.02)^2=0.0192;
$$

and the corresponding arrear payment is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">相应的期后支付为：</span></details>

$$
(2.5-2)*0.0192s=0.0096s.
$$

The discount factor is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">贴现因子为：</span></details>

$$
e^{-0.05*2.5}=0.88250.
$$

The following table details item 3, with $s$ being the CDS spread. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">下表列出第 3 项，其中 s 为 CDS 利差。</span></details>

| Time (Years) | Prob. of Default | Expected Payments | Discount Factor | PV of Exp Payment |
|---|---|---|---|---|
| 0.5 | 0.0200 | 0.0120 | 0.9753 | 0.0117 |
| 1.5 | 0.0196 | 0.0118 | 0.9277 | 0.0109 |
| 2.5 | 0.0192 | 0.0115 | 0.8825 | 0.0102 |
| 3.5 | 0.0188 | 0.0113 | 0.8395 | 0.0095 |
| 4.5 | 0.0184 | 0.0111 | 0.7985 | 0.0088 |
| Total | | | | 0.0511 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头依次为：时间（年）、违约概率、预期支付、贴现因子、预期支付现值；Total 表示合计。本表列示卖方的违约保护支付。</span></details>


For example, in the above table, if the default happens at time 2.5, then the expected payment is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例如，在上表中，若违约发生于第 2.5 年，预期支付为：</span></details>

$$
0.0192*(1-0.4)=0.0115.
$$

The break-even CDS spread is solved by matching the payments between the buyer and seller, i.e., <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令买卖双方支付相匹配即可求得盈亏平衡 CDS 利差，即：</span></details>

$$
4.0704s+0.0426s=0.0511,
$$

which yields <details class="translation-details"><summary>中文译文</summary><span class="translation-body">解得：</span></details>

$$
s=1.24\%,
$$

## PDF p.7

or 124 basis points per year, i.e. \$124,000 per year on the \$10M contact. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即每年 124 个基点，对应 1,000 万美元合约每年支付 124,000 美元。</span></details>

Note (i) Market CDS spread may be different from the break-even CDS spread, which may due to the different default intensities being used. In this case, traders may want to enter a trade, either on the long or short side of CDS. (2) Even if the traders agree on the initial CDS spread at time 0, at time $t$, the CDS spread may be considerably different from the spread at time 0, resulting in a profit/loss for one party. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意：（i）市场 CDS 利差可能不同于盈亏平衡利差，原因可能是采用了不同违约强度。此时交易者可能选择做多或做空 CDS。（2）即使双方在零时刻约定初始 CDS 利差，t 时刻的利差仍可能已发生较大变化，使一方产生盈利或亏损。</span></details>

**HWK:** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">课后练习：</span></details>

1. Suppose that the risk-free rate is at 7% per year with continuous compounding and that defaults can occur half way through each year in a new 5-year credit default swap. Suppose that the recovery rate is 30% and the default intensity each year is 3%. What is the break-even spread for the credit default swap? Assume payments are made annually. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1. 假设连续复利无风险年利率为 7%，一份新签订的 5 年期 CDS 只能在每年的年中违约。回收率为 30%，每年违约强度为 3%。若每年付费一次，盈亏平衡 CDS 利差是多少？</span></details>
