---
course: AMA572 Fixed-Income and Credit Risk
source: 01_Lecture2_原课件_或有索取权与Merton模型.pdf
pages: 9
created: "2026-10-15"
cssclasses:
  - ama-inline-translations
---

> [!info] 阅读方式
> 英文按原 PDF 页序完整转录，公式、表格和原文数值保留。点击「中文译文」显示对应段落的翻译；课堂截图已插入相应内容附近。
> [[AMA572 Fixed-Income and Credit Risk/Lecture 2/00 - Lecture 2 资料索引|资料索引]] · [[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/01_Lecture2_原课件_或有索取权与Merton模型.pdf|原课件 PDF]]

## PDF p.1

# AMA572 Lecture 2. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AMA572 第 2 讲。</span></details>

**Credit Risk (II): Contingent Claims** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">信用风险（二）：或有索取权。</span></details>

### 1 Contingent Claims <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1 或有索取权。</span></details>

Contingent claims are claims that can be made only if one or more specified outcomes occur. In other words, the payoffs of a contingent claim depend on the values of other assets or numerical indices. Obvious examples of contingent claims are: put and call options, warrants, futures contracts, and convertible bonds. In addition, as we will see in this section that the value of a firm’s debt and equity depends on the value of the firm’s assets, and even taxes paid to the government can be viewed as contingent claims. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">或有索取权是只有在一种或多种特定结果发生时才能行使的索取权。换言之，其收益取决于其他资产或数值指数的取值。典型例子包括看跌期权、看涨期权、认股权证、期货合约和可转换债券。本节还将看到，企业债务与股权的价值取决于企业资产价值，甚至向政府缴纳的税款也可以视为或有索取权。</span></details>

Suppose the firm’s asset value is $V(t)$. Assume that the firm has only two types of claims: equity and debt. More precisely, we assume that the firm issue a bond with face value $D$ with maturity $T$. Assume (i) there is no coupon payment; (ii) there is no tax credit to coupon payments; (iii) there is no bankruptcy cost. Also, for simplicity, we assume that at time $T$ the firm will liquidate the asset and deliver all the remaining asset, after paying the debt holders, to the equity holders. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设企业资产价值为 V(t)，企业只有股权和债务两类索取权。具体而言，假设企业发行一只面值为 D、到期日为 T 的债券，且（i）不支付票息；（ii）不存在票息支付的税收抵免；（iii）不存在破产成本。为简化分析，还假设企业在 T 时清算资产，向债权人偿付后，将全部剩余资产交付股东。</span></details>

Then the total payment to the debt holders at time $T$ is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则在时刻 T，向债权人支付的总金额为：</span></details>

$$
\min(V(T),D).
$$

Similarly the total payment to the equity holders at time $T$ is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">类似地，时刻 T 向股东支付的总金额为：</span></details>

$$
(V(T)-D)^+.
$$

Thus, both debt and equity can be viewed as contingent claims. In particular, the equity payoff is the same as that a call option with strike price $D$ and the underlying asset $V$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，债务与股权都可以视为或有索取权。特别地，股权收益等同于以 V 为标的资产、执行价为 D 的看涨期权收益。</span></details>

The above analysis can also be extended to subordinated bonds. More precisely, suppose there are two classes of debt, senior debt and junior debt. In the event of default the senior debt holders will collect the money first, and then the junior debt holders, and whatever left if any will finally go to the equity holders. Suppose the face values of the senior and junior debt are $D_S$ and $D_J$ respectively. Then we have the following payoff function. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">上述分析也可以推广到次级债券。假设债务分为优先债和次级债两类，违约时优先债权人首先受偿，然后是次级债权人；如有剩余，最后交给股东。设两类债务面值分别为 Dₛ 和 Dⱼ，则收益函数如下。</span></details>

| | $V_T<D_S$ | $D_S\leq V_T<D_S+D_J$ | $D_S+D_J\leq V_T$ |
|---|---|---|---|
| Senior | $V_T$ | $D_S$ | $D_S$ |
| Junior | $0$ | $V_T-D_S$ | $D_J$ |
| Equity | $0$ | $0$ | $V_T-(D_S+D_J)$ |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">行名依次为优先债、次级债、股权；三列分别对应资产不足以偿还优先债、只能完全偿还优先债，以及能够偿还全部债务的情况。</span></details>

> [!example] 课堂截图：股权收益与优先次级债表
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/01_第1页_股权收益与优先次级债表_截图09-10_1933.PNG]]

## PDF p.2

Therefore, the equity has a payoff $\{V_T-(D_S+D_J)\}^+$ that is identical to a call option with strike price $(D_S+D_J)$. The senior debt has a payoff <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，股权收益为 max{Vₜ − (Dₛ + Dⱼ), 0}，等同于执行价为 Dₛ + Dⱼ 的看涨期权。优先债收益为：</span></details>

$$
V_T-(V_T-D_s)^+,
$$

and the junior debt has a payoff <details class="translation-details"><summary>中文译文</summary><span class="translation-body">次级债收益为：</span></details>

$$
(V_T-D_s)^+-\{V_T-(D_S+D_J)\}^+.
$$

> [!example] 课堂截图：股权收益分情况解释
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/02_第1至2页_股权收益分情况解释_截图09-10_1938.PNG]]
> [!example] 课堂截图：优先债收益分情况解释
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/03_第1至2页_优先债收益分情况解释_截图09-10_2000.PNG]]
> [!example] 课堂截图：次级债收益情况一
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/04_第1至2页_次级债收益情况一_截图09-10_2003.PNG]]
> [!example] 课堂截图：次级债收益情况二
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/05_第1至2页_次级债收益情况二_截图09-10_2005.PNG]]
> [!example] 课堂截图：次级债收益情况三
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/06_第1至2页_次级债收益情况三_截图09-10_2009.PNG]]

### 2 Optimal Capital Structure and Modigliani-Miller Theorem <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2 最优资本结构与莫迪利安尼-米勒定理。</span></details>

The contingent claim approach to value debt and equity values is also useful to study corporate finance. One of the most famous results in corporate finance is Modigliani-Miller Theorem (MM theorem), which attempts to understand the optimal capital structure of a firm. The capital structure problem means that, when a firm needs capital, it has to decide how much of the capital should be financed by issuing debts and how much by issuing equity. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">用或有索取权方法评估债务和股权价值，也有助于研究公司金融。公司金融中最著名的结论之一是莫迪利安尼-米勒定理（MM 定理），它研究企业的最优资本结构。资本结构问题是指企业需要资金时，必须决定多少通过举债筹集、多少通过发行股权筹集。</span></details>

Here is a simplest possible version of the MM theorem. Assume the market is perfect and is in equilibrium. In this simple setting the decision of the capital structure becomes the choice of the face value of the debt $D$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">以下是 MM 定理的一个最简单版本。假设市场完美并处于均衡，在这一简单设定下，资本结构决策等价于选择债务面值 D。</span></details>

The total market value of equity is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">股权的总市场价值为：</span></details>

$$
S(0)=E^*[e^{-rT}(V(T)-D)^+],
$$

where the expectation $E^*$ is taken under some risk-adjusted probability $P^*$. Similarly the total market value of the debt will be <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中，期望 E* 在某个风险调整概率 P* 下计算。类似地，债务总市场价值为：</span></details>

$$
B(0)=E^*[e^{-rT}\min(V(T),D)].
$$

Thus, the total market value of firm, $M(0)$, which is defined to be the sum of the market values of debt and equity, is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">企业总市场价值 M(0) 定义为债务与股权市场价值之和，因此：</span></details>

$$
\begin{aligned}
M(0)&=S(0)+B(0)\\
&=E^*[e^{-rT}(V(T)-D)^+]+E^*[e^{-rT}\min(V(T),D)]\\
&=E^*[e^{-rT}\{(V(T)-D)^++\min(V(T),D)\}]\\
&=E^*[e^{-rT}V(T)],
\end{aligned}
$$

which is independent of $D$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">该结果与 D 无关。</span></details>

In other words, since the total market value of the firm is independent of $D$, the firm’s capital structure is irrelevant for the market value of the firm! <details class="translation-details"><summary>中文译文</summary><span class="translation-body">换言之，企业总市场价值既然与 D 无关，企业资本结构就与其市场价值无关！</span></details>

> [!example] 课堂截图：MM定理与债股价值相加
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/07_第2页_MM定理与债股价值相加_截图09-10_2015.PNG]]

## PDF p.3

This is a simple yet very surprising conclusion, which leaded to a Nobel Prize for MM. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这是一个简单却十分惊人的结论，并使 MM 获得了诺贝尔奖。</span></details>

Note that in above argument, we never use the “risk-neutral” assumption; more precisely, we never assume that $E^*[e^{-rT}V(T)]=V(0)$. As long as we can pricing contingent claims by using a “risk-adjusted” probability, the argument works. For further details of how to derive the “risk-adjusted” probability from equilibrium argument, see Kou (2002, Management Science), in which the risk-adjusted probability is derived explicitly for a general model (including model with jumps). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">上述论证并未使用“风险中性”假设，更准确地说，没有假定 E*[e⁻ʳᵀV(T)] = V(0)。只要能在“风险调整”概率下为或有索取权定价，该论证就成立。关于如何通过均衡推导风险调整概率，可参见 Kou（2002，Management Science），该文为包括跳跃模型在内的一般模型明确推导了风险调整概率。</span></details>

Also, it worth to pointing out that in the original MM paper published in 1958, they used an arbitrage argument rather than the equilibrium argument as above. More precisely, they assumed that there are two identical firms (of course this is a big assumption), with one firm having only equity, and the other one having both debts and equity. Then it is very easy to see that arbitrage argument between the two firms will prove that the MM result. In fact, we can treat the all-equity firm as the underlying asset for the other firm and use the option pricing arbitrage argument. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1958 年的 MM 原始论文采用的是套利论证，而非上述均衡论证。他们假设存在两家完全相同的企业（一项很强的假设）：一家只有股权，另一家既有债务也有股权。通过两家企业之间的套利论证便可证明 MM 结论。实际上，可以将全股权企业视为另一家企业的标的资产，再采用期权定价中的套利论证。</span></details>

Of course, the empirical evidences suggest the totally opposite conclusion: the capital structure is relevant for firm’s finance decisions. More precisely, here are some main empirical findings. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">然而，实证证据给出了相反结论：资本结构与企业融资决策有关。主要经验发现如下。</span></details>

- Higher volatility leads to lower debt/equity ratio. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">波动率越高，债务／股权比率越低。</span></details>
- Higher recovery value leads to higher debt/equity ratio. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">回收价值越高，债务／股权比率越高。</span></details>
- More maturity companies tend to have higher debt/equity ratio. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">更成熟的企业往往具有更高的债务／股权比率。</span></details>
- High tech companies tend to have no debts. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">高科技企业往往没有债务。</span></details>

To explain these empirical facts, one can look at the trade-off between the bankruptcy costs and tax credit. Let us begin with a simple example. Suppose the bond pays no coupon, and the principle value of the debt is $D$ to be paid at maturity $T$, if there is no bankruptcy at time $T$, and the tax rate is $\kappa$. Thus, $\kappa D$ is the tax credit if there is no bankruptcy at time $T$. Note that for U.S. companies the debt payments (both the interests and principle payments) are tax deductible. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">为解释这些经验事实，可以研究破产成本与税收抵免之间的权衡。先看一个简单例子：债券不付息，若企业在到期时 T 未破产，则支付债务本金 D；税率为 κ。因此，若 T 时未破产，税收抵免为 κD。原文指出，对美国企业而言，债务支付（利息与本金）均可税前扣除。</span></details>

Assume that upon bankruptcy the firm losses $(1-\alpha)$ of its asset value. This is because the bankruptcy will incur legal costs (such as lawyer fees), financial costs (difficulty in borrowing money), operational costs (e.g. damage to the brand name, layoff employees). Note that the bankruptcy occurs whenever $V(T)$ is less than $D$. Now the debt and equity values are given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">假设破产时企业损失其资产价值的 1 − α。这是因为破产会产生法律成本（如律师费）、融资成本（借款困难）和经营成本（如品牌受损、裁员）。当 V(T) 小于 D 时发生破产。此时债务和股权价值为：</span></details>

$$
B(0)=E^*[e^{-rT}(D\cdot I\{V(T)\geq D\}+e^{-rT}\alpha V(T)\cdot I\{V(T)<D\}],
$$

## PDF p.4

$$
S(0)=E^*[e^{-rT}(V(T)-D+\kappa D)\cdot I\{V(T)\geq D\}].
$$

The tax credit is $A(0)$ is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">税收抵免 A(0) 为：</span></details>

$$
A(0)=E^*[e^{-rT}\kappa D\cdot I\{V(T)\geq D\}].\tag{1}
$$

The bankruptcy cost $C(0)$ is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">破产成本 C(0) 为：</span></details>

$$
C(0)=E^*[e^{-rT}(1-\alpha)V(T)\cdot I\{V(T)<D\}].\tag{2}
$$

Then it is easy to see that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">容易得到：</span></details>

$$
\begin{aligned}
M(0)&=B(0)+S(0)\\
&=E^*[e^{-rT}(V(T)+\kappa D)\cdot I\{V(T)\geq D\}]\\
&\quad+E^*[e^{-rT}\alpha V(T)\cdot I\{V(T)<D\}]\\
&=E^*[e^{-rT}V(T)]+E^*[e^{-rT}\kappa D\cdot I\{V(T)\geq D\}]\\
&\quad+E^*[e^{-rT}(\alpha-1)\cdot V(T)\cdot I\{V(T)<D\}]\\
&=E^*[e^{-rT}V(T)]+A(0)-C(0).
\end{aligned}
$$

More precisely, the total market value of the firm is the sum of the asset value of the firm and the tax credit minus the bankruptcy cost: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">更准确地说，企业总市场价值等于企业资产价值加上税收抵免，再减去破产成本：</span></details>

$$
M(0)=E^*[e^{-rT}V(T)]+A(0)-C(0).
$$

Although the above derivation is based on a simple example, the conclusion that total market value of the firm is the asset value plus the tax credit minus the bankruptcy cost holds for more general case, including coupon payments, bonds with various maturities etc. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">上述推导虽基于简单例子，但“企业总市场价值等于资产价值加税收抵免、减破产成本”的结论，也适用于支付票息、存在不同期限债券等更一般情形。</span></details>

Note that $A(0)$ is an increasing function of $D$ when $D$ is small, and a decreasing function of $D$ when $D$ is large (as the bankruptcy chances becomes higher when $D$ increases). $C(0)$ is an increasing function of $D$. In fact, it can be shown that $A(0)-C(0)$ increases in $D$ first, and then decreases. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">D 较小时，A(0) 随 D 增大而增加；D 较大时，A(0) 随 D 增大而减少，因为债务增加会提高破产概率。C(0) 则随 D 增大而增加。可以证明，A(0) − C(0) 关于 D 先升后降。</span></details>

Now, if we want to choose $D$ to optimize the total market value of the firm, i.e., maximizing $B(0)+S(0)$, then we realize that the optimal choice of $D$ (or the optimal capital structure) is a balance of the trade-off between the tax credit of issuing bonds and the bankruptcy cost of issuing bonds. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">如果希望通过选择 D 来最大化企业总市场价值，即最大化 B(0) + S(0)，最优债务面值（或最优资本结构）就是发行债券的税收抵免与破产成本之间权衡的结果。</span></details>

More advanced models such as the Leland-Toft model or jump model in Chen and Kou (2006) can give a better explanation of the empirically observed capital structure. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">更先进的模型，例如 Leland-Toft 模型或 Chen 与 Kou（2006）的跳跃模型，能够更好地解释实证观察到的资本结构。</span></details>

**Exercise 1.** Compute (1) and (2) under the Black-Scholes-Merton geometric Brownian motion model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">练习 1。在 Black-Scholes-Merton 几何布朗运动模型下，计算公式（1）与（2）。</span></details>

> [[AMA572 Fixed-Income and Credit Risk/Lecture 2/02 - 补充推导（Ito 等距版，英文原文与折叠译文）|补充推导：Itô 等距版]] · [[AMA572 Fixed-Income and Credit Risk/Lecture 2/03 - 补充推导（Ito 引理及手写批注版）|补充推导：Itô 引理及手写批注版]] · [[AMA572 Fixed-Income and Credit Risk/Lecture 2/04 - 手写讲解：税盾与违约概率|手写讲解]]

> [!example] 课堂截图：税盾与指示函数期望
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/08_第4页配套_税盾与指示函数期望_截图09-10_2035.PNG]]

## PDF p.5

### 3 Merton’s Credit Model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3 Merton 信用风险模型。</span></details>

#### 3.1 Bond Price <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.1 债券价格。</span></details>

In Merton’s model an equity value is a call option on the corresponding asset value. There is no bankruptcy costs (i.e., $\alpha=1$) and there is no tax credit (i.e., $\kappa=0$). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">在 Merton 模型中，股权价值等于以相应企业资产价值为标的的看涨期权价值。模型没有破产成本（α = 1），也没有税收抵免（κ = 0）。</span></details>

We have the Black-Scholes formula <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由 Black-Scholes 公式：</span></details>

$$
S(t)=V_t\Phi(d_1)-De^{-r(T-t)}\Phi(d_2),\tag{3}
$$

where <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中：</span></details>

$$
d_1=\frac{\log(V_t/D)+(r+\sigma_V^2/2)(T-t)}{\sigma\sqrt{T-t}},
\qquad d_2=d_1-\sigma_V\sqrt{T-t}\tag{4}
$$

with $\sigma_V$ is the volatility of the asset value. Therefore, in Merton’s model, the bond value at time $t$ is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">σᵥ 为资产价值的波动率。因此，在 Merton 模型中，时刻 t 的债券价值为：</span></details>

$$
\begin{aligned}
B(t,T)&=V_t-C^{BS}(V_t,D,T-t,\sigma_V,r)\\
&=V_t-V_t\Phi(d_1)+D\exp(-r(T-t))\Phi(d_2)\\
&=V_t\Phi(-d_1)+D\exp(-r(T-t))\Phi(d_2),
\end{aligned}
$$

where $C^{BS}(V_t,D,T-t,\sigma_V,r)$ denotes the Black-Scholes formula for the call option. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Cᴮˢ(Vₜ, D, T−t, σᵥ, r) 表示看涨期权的 Black-Scholes 定价公式。</span></details>

Since under $P^*$, we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">在 P* 下，有：</span></details>

$$
V(T)=V(t)\exp\left\{\left(r-\frac12\sigma^2\right)(T-t)+\sigma(W_T-W_t)\right\}.
$$

Also, note that at time $t$ the risk-adjusted default probability is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">另外，时刻 t 的风险调整违约概率为：</span></details>

$$
\begin{aligned}
&P^*(V(T)<D)\\
&=P^*\left\{
\frac{\log(V(T)/V(t))-(r-\frac12\sigma^2)(T-t)}{\sigma\sqrt{T-t}}
<
\frac{\log(D/V(t))-(r-\frac12\sigma^2)(T-t)}{\sigma\sqrt{T-t}}
\right\}\\
&=P^*\left\{
\frac{\log(V(T)/V(t))-(r-\frac12\sigma^2)(T-t)}{\sigma\sqrt{T-t}}<-d_2
\right\}\\
&=\Phi(-d_2).
\end{aligned}
$$

## PDF p.6

#### 3.2 Credit Spread <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.2 信用利差。</span></details>

Hence the yield of the bond at time $t$ is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，时刻 t 的债券收益率为：</span></details>

$$
\begin{aligned}
y(t,T)&=\frac1{T-t}\log\frac{D}{B(t,T)}\\
&=\frac1{T-t}\log\frac{D}{V_t\Phi(-d_1)+D\exp(-r(T-t))\Phi(d_2)}
\end{aligned}
$$

and the credit spread in Merton’s model is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Merton 模型中的信用利差为：</span></details>

$$
\begin{aligned}
s(t,T)&=y(t,T)-r\\
&=\frac1{T-t}\log\frac{D}{V_t\Phi(-d_1)+D\exp(-r(T-t))\Phi(d_2)}-r,
\end{aligned}
$$

where $d_1$ and $d_2$ are defined in equation (4). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">d₁、d₂ 由公式（4）定义。</span></details>

In terms of the shape of the credit spread $s(t,T)$, meaning the curve of the credit spread the model cannot generate flexible credit spread similar to market observations. More precisely, there are only two shapes available for the credit spread under Merton’s model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">就信用利差 s(t, T) 的曲线形状而言，该模型无法灵活产生与市场观察相似的信用利差曲线。更准确地说，Merton 模型只能产生以下两类形状。</span></details>

(i) When $D<V(0)$ Merton’s model generates humped curve with the initial credit spread at zero being 0. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（i）当 D &lt; V(0) 时，模型产生驼峰形曲线，期限趋近零时的信用利差为 0。</span></details>

(ii) When $D>V(0)$, the model leads to monotonically decreasing credit spreads with the credit spread at zero being $\infty$. ($D>V(0)$ is possible especially if the bond investor believe that the asset price will go up significantly so that the firm will have enough money to cover the debt obligation at the bond maturity). Of course, by making the maximum point of the humped curve sufficiently large, we can see a monotonically increasing credit spreads within a range of maturities typically observed. However, in practice, we see all three kinds of credit spreads, humped, increasing, decreasing for both investment grade bonds and speculative grade bonds. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（ii）当 D &gt; V(0) 时，模型产生单调下降的信用利差，期限为零处的信用利差为无穷大。债券投资者若相信资产价格将显著上涨，使企业到期时有足够资金履行债务，则 D &gt; V(0) 也有可能。当然，若将驼峰曲线最高点对应的期限设得足够大，在通常观察的期限范围内可以看到单调上升的利差。但现实中，无论投资级还是投机级债券，都能观察到驼峰形、上升形和下降形三类信用利差。</span></details>

#### 3.3 Empirical Fitting <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.3 实证拟合。</span></details>

Empirically Merton’s model does not fit the data well. From modelling perspective, there are several issues with the model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">从实证看，Merton 模型对数据的拟合不佳。从建模角度看，存在以下问题。</span></details>

(i) In terms of the shape of the credit spreads, the model cannot generate flexible credit spreads similar to market observations. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（i）模型不能灵活生成与市场观察相似的信用利差形状。</span></details>

(ii) The model does not have coupon payments. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（ii）模型不包含票息支付。</span></details>

(iii) The model assumes that the default can only happen at the maturity of the bond. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（iii）模型假设违约只能发生在债券到期时。</span></details>

## PDF p.7

However, Merton’s model seems to predict the relative ranks of (both historical and implied) default probabilities reasonably well. That is why Moody uses Merton’s model and monotone transforms to get historical default probabilities, and CreditGrades use the model and monotone transforms to get implied default probabilities. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">不过，Merton 模型似乎能够较合理地预测违约概率（历史及隐含违约概率）的相对排序。因此，穆迪用该模型结合单调变换估计历史违约概率，CreditGrades 则用该模型结合单调变换估计隐含违约概率。</span></details>

The main advantage of Merton’s model is its simplicity. More precisely, as long as one can price European call/put options, one can use the model. That is why it is widely used in practice. Other models, such as the first-passage-time models, are more complicated than Merton’s model. But they can incorporate more empirical features. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Merton 模型的主要优点是简单：只要能对欧式看涨／看跌期权定价，就能使用该模型，因此它在实践中应用广泛。其他模型，例如首次通过时间模型，比 Merton 模型复杂，但能纳入更多经验特征。</span></details>

### 4 Short Term Credit Spreads <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4 短期信用利差。</span></details>

One important empirical observation is that even for very short maturity bonds the credit spreads is still significant. This non-zero credit spreads for short maturity bonds cannot be produced easily by using models only based on diffusion stochastic processes with continuous sample paths, such as Brownian motion. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">一个重要的经验现象是，即使债券期限很短，信用利差仍然显著。仅以布朗运动等具有连续样本路径的扩散随机过程为基础的模型，很难产生这种非零的短期信用利差。</span></details>

To understand this difficulty, note that for a diffusion process $X_t$ with continuous sample path we must have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">为理解这一困难，注意到具有连续样本路径的扩散过程 Xₜ 满足：</span></details>

$$
\frac{P(|X_{t+h}-X_t|\geq\varepsilon)}{h}\to0.\tag{5}
$$

Note that the bond price is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">债券价格为：</span></details>

$$
\begin{aligned}
B(0,T)&=E^*[De^{-rT}I\{V(T)\geq D\}]
+E^*[\alpha V(T)e^{-rT}I\{V(T)<D\}]\\
&=De^{-rT}P^*\{V(T)\geq D\}
+e^{-rT}E^*[\alpha V(T)I\{V(T)<D\}],
\end{aligned}
$$

where the recovery rate $0\leq\alpha<1$. Therefore, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中回收率满足 0 ≤ α &lt; 1。因此：</span></details>

$$
De^{-rT}\geq B(0,T)\geq De^{-rT}P^*\{V(T)\geq D\}.
$$

Thus, we have the following inequalities for the yield <details class="translation-details"><summary>中文译文</summary><span class="translation-body">所以，收益率满足以下不等式：</span></details>

$$
y(0,T)=\frac1T\log\frac D{B(0,T)}
\geq\frac1T\log\frac D{De^{-rT}}=r,
$$

and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">并且：</span></details>

$$
\begin{aligned}
y(0,T)&=\frac1T\log\frac D{B(0,T)}\\
&\leq\frac1T\log\frac D{De^{-rT}P^*\{V(T)\geq D\}}\\
&=-\frac1T\log(P^*\{V(T)\geq D\})+r,
\end{aligned}
$$

## PDF p.8

the credit spread $s(0,T)$ is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">信用利差 s(0, T) 满足：</span></details>

$$
0\leq s(0,T)=y(0,T)-r
\leq-\frac1T\log(P^*\{V(T)\geq D\}).
$$

Thus, letting $T\to0$ leads to <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，令 T 趋于 0，得到：</span></details>

$$
\begin{aligned}
\lim_{T\to0}s(0,T)
&\leq\lim_{T\to0}-\frac1T\log(P^*\{V(T)\geq D\})\\
&=\lim_{T\to0}-\frac1T\log(1-P^*\{V(T)<D\})\\
&\leq\lim_{T\to0}-\frac1T\log(1-P^*\{|V(T)-V(0)|>V(0)-D\})=0,
\end{aligned}
$$

if $V(0)>D$, because equation (5) implies <details class="translation-details"><summary>中文译文</summary><span class="translation-body">此处假设 V(0) &gt; D，因为公式（5）意味着：</span></details>

$$
\lim_{T\to0}\frac1T P^*\{|V(T)-V(0)|>V(0)-D\}=0,
$$

and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">并且：</span></details>

$$
\lim_{x\to0}\frac{\log(1-x)}{-x}=1.
$$

In summary, the short credit spread may approach to zero. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，短期信用利差可能趋于零。</span></details>

### 5 Using Merton’s Model to Estimate Implied Default Probabilities from Equity Values <details class="translation-details"><summary>中文译文</summary><span class="translation-body">5 利用 Merton 模型，根据股权价值估计隐含违约概率。</span></details>

In the above equation (3), we have two unknowns, $V(0)$ and $\sigma_V$. To calibrate the model to market data, we need another equation in addition to (3). By Ito formula, since $S(t)=C(V(t),D,\sigma_V,r,T-t)$, we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">公式（3）中有 V(0) 和 σᵥ 两个未知数。要用市场数据校准模型，除了（3）还需要一个方程。由于 S(t) = C(V(t), D, σᵥ, r, T−t)，由伊藤公式可得：</span></details>

$$
dS(t)=(\cdots)dt+\frac{\partial S}{\partial V}\cdot\sigma_V\cdot V(t)\cdot dW(t).
$$

In particular, at time 0, the volatility $\sigma_S$ of the return of $S(t)$ and the volatility of the asset return $\sigma_V$ must satisfy <details class="translation-details"><summary>中文译文</summary><span class="translation-body">特别地，在时刻 0，股票收益波动率 σₛ 与资产收益波动率 σᵥ 必须满足：</span></details>

$$
\sigma_S=\frac{\partial S}{\partial V}\cdot\sigma_V\frac{V(0)}{S(0)}.
$$

Since $\frac{\partial S}{\partial V}$ is nothing but the delta in the Black-Scholes formula, we also have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于 ∂S/∂V 就是 Black-Scholes 公式中的 Delta，因此：</span></details>

$$
\frac{\partial S}{\partial V}=\Phi(d_1).\tag{6}
$$

In summary, we have two equations for two unknowns $V(0)$ and $\sigma_V$, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">于是，关于未知数 V(0) 和 σᵥ，得到两个方程：</span></details>

$$
S(0)=V(0)\Phi(d_1)-De^{-rT}\Phi(d_2),
$$

$$
\sigma_S=\Phi(d_1)\sigma_V\frac{V(0)}{S(0)}.
$$

## PDF p.9

After solving $V(0)$ and $\sigma_V$, the implied (risk-neutral) default probability is simply <details class="translation-details"><summary>中文译文</summary><span class="translation-body">解出 V(0) 与 σᵥ 后，隐含的风险中性违约概率就是：</span></details>

$$
P^*(V(T)\leq D)=\Phi(-d_2).\tag{7}
$$

**Example.** Suppose the equity value is \$3 million, and the equity return volatility $\sigma_S=80\%$. The only debt has a maturity 1 year with par value \$10 million with no coupon payment. Assume $r=5\%$. Then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例。假设股权价值为 300 万美元，股票收益波动率为 80%；唯一一笔债务期限为 1 年、面值为 1,000 万美元，不支付票息。设 r = 5%，则：</span></details>

$$
S(0)=3,\quad\sigma_s=0.8,\quad r=0.05,\quad T=1,\quad D=10.
$$

Solving the two equations yields <details class="translation-details"><summary>中文译文</summary><span class="translation-body">解上述两个方程得到：</span></details>

$$
V(0)=12.4,\quad\sigma_V=0.2123.
$$

Thus, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此：</span></details>

$$
d_2=1.1408,
$$

and the implied risk-neutral default probability is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">隐含风险中性违约概率为：</span></details>

$$
\Phi(-1.1408)=0.127.
$$
