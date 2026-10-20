---
course: AMA572 Fixed-Income and Credit Risk
created: "2026-10-20"
source: "01_Lecture3_原课件_首次穿越与Black-Cox模型_含应用补充.pdf"
pages: 12
cssclasses:
  - ama-inline-translations
---

> [!info] 阅读方式
> 英文按 PDF 实际页序完整转录；仅合并排版换行与断词。公式、数值、题号及原文疑似笔误保留，译文不替原文纠错。点击段末「中文译文」展开对应中文；各段之间保留留白。
> [[AMA572 Fixed-Income and Credit Risk/Lecture 3/00 - Lecture 3 资料索引|资料索引]] · [[AMA572 Fixed-Income and Credit Risk/Lecture 3/附件/01_Lecture3_原课件_首次穿越与Black-Cox模型_含应用补充.pdf|原始 PDF]]

> [!note] 页码说明
> PDF 第 8–12 页是文件自带的 Practical Implementation 补充部分，其印刷页码重新从 1 开始；本文仍按 PDF 阅读器页码编号。

## PDF p.1

# AMA572 Lecture 3. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AMA572 第 3 讲。</span></details>

**First Passage Times and Black-Cox Model** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">首次穿越时间（first passage times）与 Black–Cox 模型。</span></details>

### 1 Laplace Transforms of First Passage Times <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1 首次穿越时间的拉普拉斯变换（Laplace transform）。</span></details>

Instead of using the probability (Girsanov) transform, another way to compute the first passage times is to use Laplace transform via martingales. Consider the first passage time <details class="translation-details"><summary>中文译文</summary><span class="translation-body">除了采用概率变换（Girsanov transform），还可以借助鞅（martingale）使用拉普拉斯变换来计算首次穿越时间。考虑首次穿越时间：</span></details>

$$
\tau_b=\min\{t\geq0:W_{\mu,\sigma}(t)=b\},\quad b>0.
$$

Here, without loss of generality,we assume $b>0$, and $W_{\mu,\sigma}(t)$ is a Brownian motion with drift $\mu$ and volatility $\sigma$, i.e., $W_{\mu,\sigma}(t)=\mu t+\sigma W(t)$. Note that $W_{\mu,\sigma}(\tau_b)=b$ on the set $\tau_b<\infty$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这里不失一般性地假设 b＞0，Wμ,σ(t) 是漂移率为 μ、波动率为 σ 的布朗运动（Brownian motion），即 Wμ,σ(t)＝μt＋σW(t)。注意：在 τb＜∞ 的事件上，Wμ,σ(τb)＝b。</span></details>

**Theorem.** For any $s>0$, the Laplace transform of $\tau_b$ is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">定理：对任意 s＞0，τb 的拉普拉斯变换为：</span></details>

$$
E[e^{-s\tau_b}]=\exp\left\{-\frac b{\sigma^2}\left(\sqrt{\mu^2+2\sigma^2s}-\mu\right)\right\},\tag{1}
$$

$$
P(\tau_b<\infty)=\begin{cases}\exp(2\mu b/\sigma^2)<1,&\text{if }\mu b<0,\\1,&\text{otherwise.}\end{cases}\tag{2}
$$

**Proof.** Let $s=\theta\mu+\frac12\theta^2\sigma^2$, for any numbers $\theta>0$ and $s>0$. More precisely, since $\theta$ is a positive solution of a quadratic equation we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">证明：令 s＝θμ＋θ²σ²／2，其中 θ＞0、s＞0。更准确地说，θ 是该二次方程的正根，因此：</span></details>

$$
\theta=\frac1{\sigma^2}\left(\sqrt{\mu^2+2\sigma^2s}-\mu\right)>0.
$$

Thus, for any $s>0$, we can always define $\theta>0$ as above. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，对于任意 s＞0，总能按上式定义 θ＞0。</span></details>

It is easy to see that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">容易看出，</span></details>

$$
\exp\{\theta W_{\mu,\sigma}(t)-st\}
$$

is a martingale. Therefore, by the optional sampling theorem, for any $t>0$, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">是一个鞅。因此，根据可选抽样定理（optional sampling theorem），对任意 t＞0，</span></details>

$$
1=E[\exp\{\theta W_{\mu,\sigma}(t\wedge\tau_b)-s(\tau_b\wedge t)\}].\tag{3}
$$

Since $s>0$ and $\theta>0$, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于 s＞0 且 θ＞0，</span></details>

$$
\begin{aligned}
0&\leq\exp\{\theta W_{\mu,\sigma}(t\wedge\tau_b)-s(\tau_b\wedge t)\}\\
&\leq\exp\{\theta b-s(\tau_b\wedge t)\}\leq\exp\{\theta b\},
\end{aligned}
$$

independent of $t$. Therefore, by the dominated convergence theorem, we can let $t\to\infty$ in (3) to get <details class="translation-details"><summary>中文译文</summary><span class="translation-body">上界与 t 无关。因此，根据控制收敛定理（dominated convergence theorem），在式（3）中令 t→∞，得到：</span></details>

$$
\begin{aligned}
1={}&E\left[\lim_{t\to\infty}(\exp\{\theta W_{\mu,\sigma}(t)-st\}I\{\tau_b=\infty\})\right]\\
&+E[\exp\{\theta W_{\mu,\sigma}(\tau_b)-s(\tau_b)\}\cdot I\{\tau_b<\infty\}]\\
={}&E[\exp\{\theta W_{\mu,\sigma}(\tau_b)-s\tau_b\}\cdot I\{\tau_b<\infty\}];
\end{aligned}
$$

## PDF p.2

note the first term is zero because $\limsup W(t)<b$ on the set $\tau_b=\infty$ and, again, $\theta>0$. Since $W_{\mu,\sigma}(\tau_b)=b$ on the set $\tau_b<\infty$, we further have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意第一项为零，因为在 τb＝∞ 的事件上有 limsup W(t)＜b，而且 θ＞0。由于在 τb＜∞ 的事件上 Wμ,σ(τb)＝b，进一步得到：</span></details>

$$
E[\exp\{\theta b-s\tau_b\}]=E[\exp\{\theta b-s\tau_b\}\cdot I\{\tau_b<\infty\}]=1.
$$

In summary, we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">综上，得到：</span></details>

$$
E[e^{-s\tau_b}]=e^{-\theta b}=\exp\left\{-\frac b{\sigma^2}\left(\sqrt{\mu^2+2\sigma^2s}-\mu\right)\right\}.
$$

As a by-product, we also have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">同时还可得到：</span></details>

$$
P(\tau_b<\infty)=\lim_{s\to0}E[e^{-s\tau_b}]=\exp\{-b(\sqrt{\mu^2}-\mu)/\sigma^2\}.
$$

Since $\sqrt{\mu^2}=|\mu|$, we get that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于 √μ²＝|μ|，可得：</span></details>

$$
P(\tau_b<\infty)=\begin{cases}\exp(2\mu b/\sigma^2)<1,&\text{if }\mu b<0;\\1,&\text{otherwise.}\end{cases}
$$

Generally speaking, one can only numerically invert the Laplace transform to compute the density function. However, in this special case, the Laplace transform can be inverted analytically. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">一般只能通过数值反演拉普拉斯变换来计算密度函数。不过，在这一特殊情况下可以进行解析反演。</span></details>

The Laplace inversion table (available in many handbooks of mathematical tables) gives the Laplace inversion of the function $\exp\{-a\sqrt s\}$, $a>0$, as <details class="translation-details"><summary>中文译文</summary><span class="translation-body">拉普拉斯反演表（许多数学手册均有收录）给出函数 exp{−a√s}（a＞0）的反演结果为：</span></details>

$$
\frac a{2\sqrt\pi}\frac1{x^{3/2}}\exp\left\{-\frac{a^2}{4x}\right\}.
$$

We can use this result to invert the Laplace transform in (1) to calculate the density of $\tau_b$ explicitely. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">可以利用这一结果反演式（1）的拉普拉斯变换，显式计算 τb 的密度。</span></details>

**Lemma.** The density of $\tau_b$ is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">引理：τb 的密度为：</span></details>

$$
f_{\tau_b}(x)=\frac b{\sigma\sqrt{2\pi x^3}}\exp\left\{-\frac{(b-x\mu)^2}{2x\sigma^2}\right\}.
$$

**Proof.** Using the Laplace inversion table, we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">证明：利用拉普拉斯反演表，有：</span></details>

$$
\int_0^\infty e^{-sx}\cdot\frac a{2\sqrt\pi}\frac1{x^{3/2}}\exp\left\{-\frac{a^2}{4x}\right\}dx=\exp\{-a\sqrt s\},\quad a>0.
$$

Thus, changing $s$ to $\mu^2+2\sigma^2s$, we get <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，将 s 替换为 μ²＋2σ²s，得到：</span></details>

$$
\begin{aligned}
&\int_0^\infty e^{-(\mu^2+2\sigma^2s)x}\cdot\frac a{2\sqrt\pi}\frac1{x^{3/2}}\exp\left\{-\frac{a^2}{4x}\right\}dx\\
&=\exp\{-a(\sqrt{\mu^2+2\sigma^2s})\},\quad a>0,
\end{aligned}
$$

## PDF p.3

$$
\begin{aligned}
\Longrightarrow\quad&\int_0^\infty e^{-2\sigma^2sx}\cdot\frac a{2\sqrt\pi}\frac1{x^{3/2}}\exp\left\{-\frac{a^2}{4x}-\mu^2x\right\}dx\\
&=\exp\{-a(\sqrt{\mu^2+2\sigma^2s})\},\quad a>0.
\end{aligned}
$$

Changing the variable and letting $y=2\sigma^2x$ yield <details class="translation-details"><summary>中文译文</summary><span class="translation-body">作变量替换，令 y＝2σ²x，得到：</span></details>

$$
\begin{aligned}
&\int_0^\infty e^{-sy}\cdot\frac1{2\sigma^2}\frac a{2\sqrt\pi}\frac{2\sqrt2\sigma^3}{y^{3/2}}\exp\left\{-\frac{a^2\sigma^2}{2y}-\frac{\mu^2y}{2\sigma^2}\right\}dy\\
&=\exp\{-a(\sqrt{\mu^2+2\sigma^2s})\},\quad a>0,\\
\Longrightarrow\quad&\int_0^\infty e^{-sy}\cdot\frac a{\sqrt{2\pi y^3}}\sigma\exp\left\{-\frac{a^2\sigma^2}{2y}-\frac{\mu^2y}{2\sigma^2}\right\}dy\\
&=\exp\{-a(\sqrt{\mu^2+2\sigma^2s})\},\quad a>0.
\end{aligned}
$$

In summary, with $a=b/\sigma^2$ in the above equation and multiplying by the constant $\exp\{-\frac b{\sigma^2}(-\mu)\}$, we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">综上，在上式中取 a＝b／σ²，并乘上常数 exp{−(b／σ²)(−μ)}，得到：</span></details>

$$
\begin{aligned}
f_{\tau_b}(y)&=\frac b{\sigma\sqrt{2\pi y^3}}\exp\left\{-\frac{b^2}{2y\sigma^2}-\frac{\mu^2y}{2\sigma^2}\right\}\cdot\exp\left\{-\frac b{\sigma^2}(-\mu)\right\}\\
&=\frac b{\sigma\sqrt{2\pi y^3}}\exp\left\{-\frac{b^2+\mu^2y^2-2by\mu}{2y\sigma^2}\right\}\\
&=\frac b{\sigma\sqrt{2\pi y^3}}\exp\left\{-\frac{(b-y\mu)^2}{2y\sigma^2}\right\}.
\end{aligned}
$$

The derivation of the Laplace transform only relies on finding a martingale, applying the optional sampling theorem, and the fact $W_{\mu,\sigma}(\tau_b)=b$. This makes it more suitable to solve more complied first passage time problems. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">拉普拉斯变换的推导只依赖于找到一个鞅、应用可选抽样定理，以及 Wμ,σ(τb)＝b 这一事实。因此，这种方法更适合处理更复杂的首次穿越时间问题。</span></details>

### 2 Basic Setting of the Black-Cox Model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2 Black–Cox 模型的基本设定。</span></details>

Assume that the asset value of the firm $V_t$ follows a geometric Brownian motion under a risk-adjusted probability: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">假设在风险调整概率（risk-adjusted probability）下，企业资产价值 Vt 服从几何布朗运动（geometric Brownian motion）：</span></details>

$$
\frac{dV_t}{V_t}=(r-\delta)dt+\sigma dW_t,
$$

whose solution is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其解为：</span></details>

$$
V_t=V_0\exp\left\{\left(r-\delta-\frac12\sigma^2\right)t+\sigma W_t\right\},
$$

## PDF p.4

where $r$ is the risk-free interest rate, $\delta$ is the total payout rate the firm’s investors (including both bond and equity holders, as bond coupon and stock dividend payments). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 r 为无风险利率，δ 为向企业投资者的总支付率，包括向债权人支付的票息和向股东支付的股利。</span></details>

Now the firm issues a bond with par value 1, maturity $T$ and coupon rate $\rho$ with $\rho<\delta$. The default may happen at any time between 0 and $T$. In fact the default happens at the first time the process $V_t$ falls below $V_B$: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">企业现发行面值为 1、到期日为 T、票息率为 ρ 的债券，并假设 ρ＜δ。违约可以在 0 到 T 之间任何时刻发生，具体发生于资产价值过程 Vt 首次跌至边界 VB 时：</span></details>

$$
\tau=\min\{t\geq0:V_t\leq V_B\},\quad V_B<V_0.
$$

Upon default, the bondholder gets <details class="translation-details"><summary>中文译文</summary><span class="translation-body">违约时，债券持有人获得：</span></details>

$$
ce^{-r(T-\tau)},\quad0\leq c\leq1.
$$

In other words, we assume the recovery at the fraction of otherwise identical treasury bond value. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">换言之，假设违约回收金额等于其他条件相同的国债价值的一定比例。</span></details>

In this setting, the payoff to the bond consists of three parts, the par value at maturity if no default, the recovery value upon default, and the continuous coupon payment up to $\tau\wedge T$. Therefore, the bond price at time zero is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">在这一设定下，债券收益包含三部分：未违约时到期偿还的本金、违约时的回收价值，以及直到违约或到期（τ∧T）为止的连续票息。因此，零时刻债券价格为：</span></details>

$$
B(V;V_B,T)=E\left[e^{-rT}I\{\tau>T\}+e^{-r\tau}\cdot ce^{-r(T-\tau)}I\{\tau\leq T\}+\int_0^{\tau\wedge T}\rho e^{-rs}ds\right].
$$

### 3 Laplace Transform of the Bond Price <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3 债券价格的拉普拉斯变换。</span></details>

Let <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令：</span></details>

$$
\tau_b=\min\{t\geq0:W_{\mu,\sigma}(t)=b\},\quad b<0.
$$

It can be shown easily that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">容易证明：</span></details>

$$
E[e^{-s\tau_b}]=\exp\left\{\frac b{\sigma^2}\left(\sqrt{\mu^2+2\sigma^2s}+\mu\right)\right\},\quad b<0.
$$

Now in the Black-Cox setting, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">在 Black–Cox 模型设定下，</span></details>

$$
\begin{aligned}
\tau&=\min\{t\geq0:V_t\leq V_B\}\\
&=\min\left\{t\geq0:V_0\exp\{(r-\delta-\tfrac12\sigma^2)t+\sigma W_t\}\leq V_B\right\}\\
&=\min\left\{t\geq0:(r-\delta-\tfrac12\sigma^2)t+\sigma W_t\leq\log(V_B/V_0)\right\}.
\end{aligned}
$$

## PDF p.5

Thus, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，</span></details>

$$
\begin{aligned}
E[e^{-s\tau_b}]&=\exp\left\{\frac{\log(V_B/V_0)}{\sigma^2}\left(\sqrt{(r-\delta-\tfrac12\sigma^2)^2+2\sigma^2s}+(r-\delta-\tfrac12\sigma^2)\right)\right\}\\
&=\exp\left\{\log(V_B/V_0)\left(\sqrt{\left(\frac{r-\delta}{\sigma^2}-\frac12\right)^2+\frac2{\sigma^2}s}+\left(\frac{r-\delta}{\sigma^2}-\frac12\right)\right)\right\}\\
&=\exp\left\{\log(V_B/V_0)\left(\sqrt{\xi^2+\frac2{\sigma^2}s}+\xi\right)\right\},
\end{aligned}
$$

where the constant $\xi=\frac{r-\delta}{\sigma^2}-\frac12$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中常数 ξ＝(r−δ)／σ²−1／2。</span></details>

Thus, we have the Laplace transform for the bond price, except the recovery part, is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因而，除违约回收部分以外，债券价格的拉普拉斯变换为：</span></details>

$$
\begin{aligned}
&\int_0^\infty e^{-sT}E\left[e^{-rT}I\{\tau>T\}+\int_0^{\tau\wedge T}\rho e^{-rs}ds\right]dT\\
&=E\left\{\int_0^\infty e^{-sT}\left[e^{-rT}I\{\tau>T\}+\frac\rho r(1-e^{-r(\tau\wedge T)})\right]dT\right\}\\
&=E\left\{\int_0^\tau e^{-sT}e^{-rT}dT+\int_0^\tau e^{-sT}\frac\rho r(1-e^{-rT})dT+\int_\tau^\infty e^{-sT}\frac\rho r(1-e^{-r\tau})dT\right\}\\
&=E\left\{\left(1-\frac\rho r\right)\int_0^\tau e^{-(s+r)T}dT+\int_0^\infty e^{-sT}\frac\rho r dT-\frac\rho r e^{-r\tau}\int_\tau^\infty e^{-sT}dT\right\}\\
&=E\left\{\left(1-\frac\rho r\right)\frac{1-e^{-(s+r)\tau}}{s+r}+\frac\rho r\frac1s-\frac\rho r\frac{e^{-(s+r)\tau}}s\right\}\\
&=\frac{\rho+s}{s(r+s)}(1-E[e^{-(r+s)\tau}]),
\end{aligned}
$$

which the first equality follows by changing the order the integration. Now, we only need to compute the Laplace transform of the recovery part: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第一个等号由交换积分次序得到。接下来只需计算违约回收部分的拉普拉斯变换：</span></details>

$$
\begin{aligned}
&\int_0^\infty e^{-sT}E[e^{-r\tau}\cdot ce^{-r(T-\tau)}I\{\tau\leq T\}]dT\\
&=c\int_0^\infty e^{-(s+r)T}E[I\{\tau\leq T\}]dT\\
&=cE\left\{\int_0^\infty e^{-(s+r)T}I\{\tau\leq T\}dT\right\}\\
&=cE\left\{\int_\tau^\infty e^{-(s+r)T}dT\right\}=\frac c{s+r}E[e^{-(s+r)\tau}].
\end{aligned}
$$

## PDF p.6

In summary, the Laplace transform of the bond price is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">综上，债券价格的拉普拉斯变换为：</span></details>

$$
\begin{aligned}
&\int_0^\infty e^{-sT}B(V;V_B,T)dT\\
&=\frac{\rho+s}{s(r+s)}(1-E[e^{-(r+s)\tau}])+\frac c{s+r}E[e^{-(s+r)\tau}]\\
&=\frac{\rho+s}{s(r+s)}+\left(\frac c{s+r}-\frac{\rho+s}{s(r+s)}\right)E[e^{-(s+r)\tau}]\\
&=\frac{\rho+s}{s(r+s)}-\left(\frac\rho r\frac1s+\left(1-\frac\rho r-c\right)\frac1{r+s}\right)\\
&\qquad\times\exp\left\{\log(V_B/V_0)\left(\sqrt{\xi^2+\frac2{\sigma^2}(s+r)}+\xi\right)\right\}.
\end{aligned}
$$

Fortunately, the above Laplace transform can be inverted analytically; see a hwk problem. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">上述拉普拉斯变换可以解析反演，参见课后练习。</span></details>

The equity price $E$ can be obtained simply by using the fact that the equity value plus the bond value minus the bankruptcy cost is equal to the asset value of the firm, as there is no tax in this model. We will have a more general model includes tax later when we discuss Leland’s model. So we skip the equity value here. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于本模型没有税收，可利用“股权价值加债券价值减破产成本等于企业资产价值”这一关系得到股权价格 E。后面讨论 Leland 模型时会引入包含税收的更一般模型，因此这里略去股权价值的计算。</span></details>

Empirically, the Black-Cox model leads to better possibilities of credit spreads than Merton’s model. For example, it generates better spreads with humped shapes, partly because the default can happen any time between 0 and $T$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">从实证表现看，Black–Cox 模型比 Merton 模型能产生更合理的信用利差（credit spread）。例如，它能更好地产生驼峰形利差曲线，部分原因在于违约可在 0 到 T 之间任意时刻发生。</span></details>

However, several main issues remain, such as the model cannot produce non-zero credit spreads observed in practice for short maturity bonds, and cannot generate flexible credit spread curves for speculative bonds. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">不过仍有一些主要问题：例如，模型不能产生实践中短期限债券所观察到的非零信用利差，也不能为投机级债券生成足够灵活的利差曲线。</span></details>

### 4 Practical Implementation of Black-Cox Model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4 Black–Cox 模型的实际应用。</span></details>

See the menu by CreditGrades. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">参见 CreditGrades 的说明手册。</span></details>

**HWK.** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">课后练习。</span></details>

Invert the Laplace transform to get a formula for the bond price $B(V;V_B,T)$. Use the following Laplace inversion table: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">反演拉普拉斯变换，得到债券价格 B(V；VB，T) 的公式。使用下列拉普拉斯反演表：</span></details>

The Laplace inversion of $\frac{\rho+s}{s(r+s)}$ is $\frac{r-\rho}{r}e^{-rT}+\frac\rho r$, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(ρ＋s)／[s(r＋s)] 的拉普拉斯反演为 ((r−ρ)／r)e^(−rT)＋ρ／r，</span></details>

the Laplace inversion of $\frac1{s-\beta}\exp\{-\sqrt{\alpha s}\}$, $\beta>0$, $\alpha>0$, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">而 exp{−√(αs)}／(s−β)（β＞0、α＞0）的拉普拉斯反演，</span></details>

## PDF p.7

is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">为：</span></details>

$$
e^{\beta T}\left\{e^{\sqrt{\alpha\beta}}\Phi\left(-\sqrt{\frac\alpha{2T}}-\sqrt{2\beta T}\right)+e^{-\sqrt{\alpha\beta}}\Phi\left(-\sqrt{\frac\alpha{2T}}+\sqrt{2\beta T}\right)\right\}.
$$

## PDF p.8

### 1 Practical Implementation of the Black-Cox Model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1 Black–Cox 模型的实际应用。</span></details>

Under the risk-neutral measure, the firm value follows the geometric Brownian motion <details class="translation-details"><summary>中文译文</summary><span class="translation-body">在风险中性测度（risk-neutral measure）下，企业价值服从几何布朗运动：</span></details>

$$
\frac{dV_t}{V_t}=(r-\delta)\,dt+\sigma\,dW_t,
$$

with solution <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其解为：</span></details>

$$
V_t=V_0\exp\left\{\left(r-\delta-\frac12\sigma^2\right)t+\sigma W_t\right\}.
$$

The firm defaults when its asset value first hits a lower default barrier $V_B$, where <details class="translation-details"><summary>中文译文</summary><span class="translation-body">当资产价值首次触及下方违约边界（default barrier）VB 时，企业违约，其中：</span></details>

$$
0<V_B<V_0.
$$

Thus the default time is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此违约时间为：</span></details>

$$
\tau=\inf\{t\geq0:V_t\leq V_B\}.
$$

Taking logarithms, default occurs when <details class="translation-details"><summary>中文译文</summary><span class="translation-body">取对数后，违约发生的条件是：</span></details>

$$
\left(r-\delta-\frac12\sigma^2\right)t+\sigma W_t\leq\log\left(\frac{V_B}{V_0}\right).
$$

Since $V_B<V_0$, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于 VB＜V0，</span></details>

$$
\log\left(\frac{V_B}{V_0}\right)<0.
$$

Therefore, the Black-Cox default time is a first downward passage time of a Brownian motion with drift. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，Black–Cox 模型中的违约时间是带漂移布朗运动的首次向下穿越时间。</span></details>

Define <details class="translation-details"><summary>中文译文</summary><span class="translation-body">定义：</span></details>

$$
\xi=\frac{r-\delta}{\sigma^2}-\frac12.
$$

Then the Laplace transform of the default time is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则违约时间的拉普拉斯变换为：</span></details>

$$
E[e^{-s\tau}]=\exp\left\{\log\left(\frac{V_B}{V_0}\right)\left[\sqrt{\xi^2+\frac{2s}{\sigma^2}}+\xi\right]\right\}.
$$

#### 1.1 Bond Payoff <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.1 债券收益。</span></details>

Consider a bond with face value 1, maturity $T$, continuous coupon rate $\rho$, and recovery parameter $c\in[0,1]$. The bond payoff has three components: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑一只面值为 1、到期日为 T、连续票息率为 ρ、回收参数 c∈[0，1] 的债券。债券收益包含三个组成部分：</span></details>

$$
e^{-rT}\mathbf1_{\{\tau>T\}},
$$

which is the discounted par payment if no default occurs before maturity; <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这是到期前未违约时支付本金的贴现值；</span></details>

$$
e^{-r\tau}ce^{-r(T-\tau)}\mathbf1_{\{\tau\leq T\}},
$$

## PDF p.9

which is the discounted recovery payment if default occurs before maturity; and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这是到期前违约时回收支付的贴现值；以及：</span></details>

$$
\int_0^{\tau\wedge T}\rho e^{-rs}\,ds,
$$

which is the discounted continuous coupon payment until default or maturity. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这是直到违约或到期为止连续票息支付的贴现值。</span></details>

Hence the time-zero bond price is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，零时刻债券价格为：</span></details>

$$
B(V_0;V_B,T)=E\left[e^{-rT}\mathbf1_{\{\tau>T\}}+e^{-r\tau}ce^{-r(T-\tau)}\mathbf1_{\{\tau\leq T\}}+\int_0^{\tau\wedge T}\rho e^{-rs}\,ds\right].
$$

#### 1.2 Why the Laplace Transform Is Useful <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.2 为什么拉普拉斯变换有用。</span></details>

The direct valuation of the bond requires the distribution of the first-passage time $\tau$. Instead of working directly with the density of $\tau$, we use its Laplace transform: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">直接估值债券需要首次穿越时间 τ 的分布。这里不直接处理 τ 的密度，而是使用其拉普拉斯变换：</span></details>

$$
E[e^{-s\tau}].
$$

This is useful because the first-passage-time Laplace transform has a closed-form expression, while the direct maturity-dependent pricing formula is more difficult to derive. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这样做的好处在于，首次穿越时间的拉普拉斯变换具有闭式表达式（closed form），而直接推导依赖到期日的定价公式则更困难。</span></details>

Taking the Laplace transform of the bond price with respect to maturity $T$, define <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对债券价格关于到期时间 T 作拉普拉斯变换，定义：</span></details>

$$
\widehat B(s)=\int_0^\infty e^{-sT}B(V_0;V_B,T)\,dT.
$$

The Black-Cox model gives <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Black–Cox 模型给出：</span></details>

$$
\widehat B(s)=\frac{\rho+s}{s(r+s)}-\left[\frac\rho r\frac1s+\left(1-\frac\rho r-c\right)\frac1{r+s}\right]E[e^{-(s+r)\tau}].
$$

Substituting the default-time transform, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">代入违约时间的变换：</span></details>

$$
E[e^{-(s+r)\tau}]=\exp\left\{\log\left(\frac{V_B}{V_0}\right)\left[\sqrt{\xi^2+\frac{2(s+r)}{\sigma^2}}+\xi\right]\right\}.
$$

Let <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令：</span></details>

$$
q=\frac{V_B}{V_0}\in(0,1),\quad L=\log\left(\frac{V_0}{V_B}\right)>0.
$$

Then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则：</span></details>

$$
\log q=-L.
$$

Therefore, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，</span></details>

$$
E[e^{-(s+r)\tau}]=q^\xi\exp\left\{-L\sqrt{\xi^2+\frac{2(s+r)}{\sigma^2}}\right\}.
$$

## PDF p.10

Now, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">现在，</span></details>

$$
\xi^2+\frac{2(s+r)}{\sigma^2}=\frac2{\sigma^2}\left(s+r+\frac12\sigma^2\xi^2\right).
$$

Define <details class="translation-details"><summary>中文译文</summary><span class="translation-body">定义：</span></details>

$$
\lambda=r+\frac12\sigma^2\xi^2,
$$

and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">以及：</span></details>

$$
\alpha=\frac{2L^2}{\sigma^2}.
$$

Then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则：</span></details>

$$
L\sqrt{\xi^2+\frac{2(s+r)}{\sigma^2}}=\sqrt{\alpha(s+\lambda)}.
$$

Hence <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因而：</span></details>

$$
E[e^{-(s+r)\tau}]=q^\xi\exp\{-\sqrt{\alpha(s+\lambda)}\}.
$$

Thus, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，</span></details>

$$
\widehat B(s)=\frac{\rho+s}{s(r+s)}-q^\xi\left[\frac\rho r\frac1s+\left(1-\frac\rho r-c\right)\frac1{r+s}\right]\exp\{-\sqrt{\alpha(s+\lambda)}\}.
$$

#### 1.3 Laplace Inversion <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.3 拉普拉斯反演。</span></details>

The first term has inverse <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第一项的反演为：</span></details>

$$
\mathcal L^{-1}\left[\frac{\rho+s}{s(r+s)}\right](T)=\frac{r-\rho}{r}e^{-rT}+\frac\rho r.
$$

This is the default-free continuous-coupon bond price: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这就是无违约风险的连续付息债券价格：</span></details>

$$
B_{\mathrm{rf}}(T)=e^{-rT}+\int_0^T\rho e^{-rt}\,dt=\frac\rho r+\frac{r-\rho}r e^{-rT}.
$$

Next, define <details class="translation-details"><summary>中文译文</summary><span class="translation-body">接下来定义：</span></details>

$$
G_a(T)=\mathcal L^{-1}\left[\frac1{s+a}\exp\{-\sqrt{\alpha(s+\lambda)}\}\right](T).
$$

Set <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设：</span></details>

$$
u=s+\lambda.
$$

Then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则：</span></details>

$$
s+a=u-(\lambda-a).
$$

Define <details class="translation-details"><summary>中文译文</summary><span class="translation-body">定义：</span></details>

$$
\beta_a=\lambda-a.
$$

## PDF p.11

Therefore, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，</span></details>

$$
\frac1{s+a}\exp\{-\sqrt{\alpha(s+\lambda)}\}=\frac1{u-\beta_a}\exp\{-\sqrt{\alpha u}\}.
$$

Using the Laplace inversion formula, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">使用拉普拉斯反演公式：</span></details>

$$
\mathcal L^{-1}\left[\frac1{s-\beta}\exp\{-\sqrt{\alpha s}\}\right](T)=e^{\beta T}\left[e^{\sqrt{\alpha\beta}}\Phi\left(-\sqrt{\frac\alpha{2T}}-\sqrt{2\beta T}\right)+e^{-\sqrt{\alpha\beta}}\Phi\left(-\sqrt{\frac\alpha{2T}}+\sqrt{2\beta T}\right)\right],
$$

we obtain the shifted inverse <details class="translation-details"><summary>中文译文</summary><span class="translation-body">可得移位后的反演：</span></details>

$$
G_a(T)=e^{-aT}\left[e^{\sqrt{\alpha(\lambda-a)}}\Phi\left(-\sqrt{\frac\alpha{2T}}-\sqrt{2(\lambda-a)T}\right)+e^{-\sqrt{\alpha(\lambda-a)}}\Phi\left(-\sqrt{\frac\alpha{2T}}+\sqrt{2(\lambda-a)T}\right)\right].
$$

In particular, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">特别地，</span></details>

$$
\beta_0=\lambda=r+\frac12\sigma^2\xi^2,
$$

and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">以及：</span></details>

$$
\beta_r=\lambda-r=\frac12\sigma^2\xi^2.
$$

#### 1.4 Closed-Form Bond Price <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.4 债券价格的闭式解。</span></details>

Combining the terms, the Black-Cox bond price is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">合并各项，Black–Cox 债券价格为：</span></details>

$$
B(V_0;V_B,T)=B_{\mathrm{rf}}(T)-q^\xi\left[\frac\rho rG_0(T)+\left(1-\frac\rho r-c\right)G_r(T)\right],
$$

where <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中：</span></details>

$$
\begin{gathered}
B_{\mathrm{rf}}(T)=\frac\rho r+\frac{r-\rho}r e^{-rT},\\
q=\frac{V_B}{V_0},\quad\xi=\frac{r-\delta}{\sigma^2}-\frac12,\\
L=\log\left(\frac{V_0}{V_B}\right),\quad\alpha=\frac{2L^2}{\sigma^2},
\end{gathered}
$$

and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">以及：</span></details>

$$
\lambda=r+\frac12\sigma^2\xi^2.
$$

The function $G_a(T)$ is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">函数 Ga(T) 为：</span></details>

$$
G_a(T)=e^{-aT}\left[e^{\sqrt{\alpha(\lambda-a)}}\Phi\left(-\sqrt{\frac\alpha{2T}}-\sqrt{2(\lambda-a)T}\right)+e^{-\sqrt{\alpha(\lambda-a)}}\Phi\left(-\sqrt{\frac\alpha{2T}}+\sqrt{2(\lambda-a)T}\right)\right].
$$

## PDF p.12

#### 1.5 Credit Spread <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.5 信用利差。</span></details>

Given the risky bond price $B(V_0;V_B,T)$, the risky yield $y$ is defined implicitly by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">给定风险债券价格 B(V0；VB，T)，风险收益率 y 由下式隐式定义：</span></details>

$$
B(V_0;V_B,T)=e^{-yT}+\int_0^T\rho e^{-yt}\,dt.
$$

Equivalently, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">等价地，</span></details>

$$
B(V_0;V_B,T)=e^{-yT}+\frac\rho y(1-e^{-yT}).
$$

The credit spread is then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">信用利差为：</span></details>

$$
CS(T)=y-r.
$$

For a zero-coupon bond, if the risky price is $B_Z(T)$, then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对于零息债券（zero-coupon bond），若风险价格为 BZ(T)，则：</span></details>

$$
B_Z(T)=e^{-(r+CS(T))T},
$$

so <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因而：</span></details>

$$
CS(T)=-\frac1T\log B_Z(T)-r.
$$

#### 1.6 Interpretation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.6 解释。</span></details>

The Black-Cox bond price has the form <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Black–Cox 债券价格可以写成：</span></details>

$$
B_{\mathrm{risky}}=B_{\mathrm{riskfree}}-\text{default adjustment}.
$$

The default-free component is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中，无违约风险部分为：</span></details>

$$
B_{\mathrm{rf}}(T)=\frac\rho r+\frac{r-\rho}r e^{-rT}.
$$

The default adjustment depends on the distance to default, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">违约调整取决于违约距离（distance to default），</span></details>

$$
q=\frac{V_B}{V_0},
$$

the asset volatility $\sigma$, the payout rate $\delta$, the recovery rate $c$, and the coupon rate $\rho$. A larger distance between $V_0$ and $V_B$ reduces default risk, while a larger asset volatility $\sigma$ increases the probability of hitting the default barrier. A higher recovery rate $c$ increases the risky bond price. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">以及资产波动率 σ、支付率 δ、回收率 c 和票息率 ρ。V0 与 VB 之间的距离越大，违约风险越低；资产波动率 σ 越大，触及违约边界的概率越高。回收率 c 越高，风险债券价格越高。</span></details>

In practice, one must calibrate or estimate <details class="translation-details"><summary>中文译文</summary><span class="translation-body">实务中需要校准（calibrate）或估计：</span></details>

$$
V_0,\ V_B,\ \sigma,\ r,\ \delta,\ c,\ \rho,\ T.
$$

A typical implementation uses equity market data to infer $V_0$ and $\sigma$, debt structure to estimate the default barrier $V_B$, and observed bond prices or CDS spreads to calibrate recovery and barrier parameters. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">典型实施方法是：利用股票市场数据推断 V0 和 σ，利用债务结构估计违约边界 VB，再利用实际观察到的债券价格或信用违约互换利差（CDS spread）校准回收率和边界参数。</span></details>
