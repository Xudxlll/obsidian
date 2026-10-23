---
course: "AMA515A Forecasting and Applied Time Series Analysis"
chapter: 2
source: "Chapter 2.pdf"
pages: 11
cssclasses:
  - ama-inline-translations
---

# Chapter 2 — 英文原文与折叠中文译文

[本章资料索引](<00 - Chapter 2 资料索引.md>) · [原始 PDF](<附件/Chapter 2.pdf>)

英文按原 PDF 页序整理，逐段附默认折叠的中文译文。独立公式和图表另排；每页底部可展开原页核对。原有题目与解答分别保留，不另编解题分析。

## PDF p.1


**AMA515A Forecasting and applied time series analysis** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AMA515A 预测与应用时间序列分析。</span></details>


### Ch.2 Stationarity and further exponential smoothing <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 2 章：平稳性与进一步的指数平滑。</span></details>


**2.1 Time series** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.1 时间序列。</span></details>


A stochastic process is a family of random variables $Z_t$, where t belongs to the set of integers $0,\pm1,\pm2,\ldots$. If t carries the meaning of time, then the process is called a time series. In most cases, we shall be dealing with non-negative time, namely, t = 0, 1, 2,…. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">随机过程是一族随机变量 Zₜ，其中 t 属于整数集 0、±1、±2、…。如果 t 表示时间，这个过程就称为时间序列。在大多数情况下，我们处理非负时间，即 t = 0、1、2、…。</span></details>


**2.1.1 Stationary time series** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.1.1 平稳时间序列。</span></details>


A strictly stationary series is one whose statistical properties remain constant in time. A proper definition for a time series $\{X_t,t=0,\pm1,\ldots\}$ is by the condition that $(X_1,\ldots,X_n)$ and $(X_{1+h},\ldots,X_{n+h})$ have the same joint distribution for all integers h and n > 0. A necessary condition for this is the absence of any deterministic or stochastic trend. Stationary series are amenable to formal analysis. Elimination of non-stationarity is a primary aim of preliminary, descriptive analysis. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">严格平稳序列的统计性质不随时间改变。正式定义要求：对所有整数 h 和正整数 n，两组变量 (X₁,…,Xₙ) 与 (X₁₊h,…,Xₙ₊h) 具有相同的联合分布。一个必要条件是不具有任何确定性或随机趋势。平稳序列便于正式分析；消除非平稳性是初步描述性分析的主要目标。</span></details>


**2.1.2 White noise** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.1.2 白噪声。</span></details>


If $X_t\sim\operatorname{IID}(0,\sigma^2),\ \forall t$, the process $\{X_t\}$ is said to be white noise. It’s a term coming from engineering. Thus white noise is the simplest kind of strictly stationary time series. Before attempting any analysis in terms of more complicated models, it is advisable to examine, either informally or by formal tests, whether data show any incompatibility with white noise. A standard tool is the autocorrelation coefficients in the next section. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">若各 Xₜ 独立同分布、均值为 0、方差为 σ²，该过程称为白噪声。这一术语来自工程学。白噪声是最简单的一类严格平稳序列。使用更复杂模型前，应通过直观观察或正式检验，检查数据是否表现出与白噪声不相容的特征。下一节的自相关系数是一种标准工具。</span></details>


**2.1.3 Weakly stationary TS** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.1.3 弱平稳时间序列。</span></details>


Strict stationarity is usually a too strong condition in applications. Let <details class="translation-details"><summary>中文译文</summary><span class="translation-body">实际应用中，严格平稳通常是过强的条件。设：</span></details>

$$
\mu_t=E(X_t),\quad\sigma_t^2=E(X_t-\mu_t)^2,\quad \operatorname{cov}(t,t+h)=\gamma(t,t+h).
$$

Here cov is the abbreviation of covariance. If <details class="translation-details"><summary>中文译文</summary><span class="translation-body">cov 是协方差的缩写。如果：</span></details>


(i) $\mu_t$ is independent of t, and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（i）均值 μₜ 不依赖 t；并且</span></details>


(ii) $\gamma(t,t+h)$ is independent of t for each h, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（ii）对每个 h，协方差 γ(t,t+h) 不依赖 t，</span></details>


then $X_t$ is said to be weakly stationary time series. In this course we mainly focus on this type of stationarity. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则称 Xₜ 为弱平稳时间序列。本课程主要关注这种平稳性。</span></details>


> [!example]- PDF 第 1 页原貌（含原有批注）
> ![PDF p.1](<附件/ch2-lecture-p01.png>)

## PDF p.2


**2.2 Further discussion on weak stationarity** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.2 进一步讨论弱平稳性。</span></details>


Recall if a discrete time stochastic process $\{X_t\}$ satisfy the following conditions: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">回顾：若离散时间随机过程满足下列条件：</span></details>

$$
\begin{aligned}
\text{(i)}\quad&E(X_t)=\mu\ \text{(constant) for all }t,\\
&\operatorname{var}(X_t)=\sigma^2\ \text{(constant) for all }t,\\
\text{(ii)}\quad&\operatorname{cov}(X_t,X_s)=\Gamma_{t-s}\ \text{(depend on t-s only !)}
\end{aligned}
$$

Then $\{X_t\}$ is said to possess second order stationarity. Some authors also say $\{X_t\}$ is weakly stationary or covariance-stationary. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则称该过程具有二阶平稳性。有些作者也称它为弱平稳或协方差平稳。</span></details>


**2.2.1 Autocorrelation function of a stationary stochastic process** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.2.1 平稳随机过程的自相关函数。</span></details>


The autocovariance function of a time series $X_t$ is defined by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">时间序列的自协方差函数定义为：</span></details>

$$
\gamma(k)=E(X_tX_{t+k})-E(X_t)E(X_{t+k}),\qquad
\rho(k)=\frac{\gamma(k)}{[\operatorname{var}(X_t)\operatorname{var}(X_{t+k})]^{1/2}}.
$$

Here $k=0,\pm1,\pm2,\ldots$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 k = 0、±1、±2、…。</span></details>


For a stochastic process which is stationary, then the autocovariance function is simplified to <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对于平稳随机过程，自协方差函数简化为：</span></details>

$$
\gamma(k)=E(X_tX_{t+k})-E(X_t)^2,\qquad \gamma(0)=\operatorname{var}(X_t).
$$

In this case, the autocorrelation function $\rho(k)=\gamma(k)/\gamma(0)$, $k=0,\pm1,\pm2,\ldots$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">此时，自相关函数等于 γ(k)/γ(0)，滞后阶数 k 可取 0、±1、±2、…。</span></details>


Remark 1 : It can be shown that $|\rho(k)|\leq1$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">备注 1：可以证明自相关系数的绝对值不超过 1。</span></details>


Remark 2: Some algebraic simplicity can be obtained if $E(X_t)=0$, because then $\gamma(k)=E(X_tX_{t+k})$ and $\gamma(0)=\operatorname{var}(X_t)=E(X_t^2)$. But remember this is a special case. In general $E(X_t)\neq0$ and we have to use the full form above. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">备注 2：若均值为 0，代数计算可以简化，此时自协方差等于乘积的期望，方差等于二阶矩。但这只是特殊情况，一般均值不为 0，必须使用上面的完整公式。</span></details>


**Example 1:** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 1：</span></details>


Let $\{a_t\}$ be zero-mean white noise and $\operatorname{var}(a_t)=\sigma^2$. A time series is formed by the following process: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设 aₜ 为零均值白噪声，方差为 σ²。构造下列时间序列：</span></details>

$$Z_t=a_t+0.5a_{t-1}.$$

Show that $Z_t$ is stationary by finding its autocovariance function. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">通过求自协方差函数，证明 Zₜ 平稳。</span></details>


Solution: $E(Z_t)=0$, $\operatorname{var}(Z_t)=\sigma'^2$ (constant). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">解：Zₜ 均值为 0，方差为常数 σ′²。</span></details>


Observe <details class="translation-details"><summary>中文译文</summary><span class="translation-body">观察：</span></details>

$$
\begin{aligned}
E(Z_tZ_{t-k})&=E(a_t+0.5a_{t-1})(a_{t-k}+0.5a_{t-k-1})\\
&=E(a_ta_{t-k}+0.5a_{t-1}a_{t-k}+0.5a_ta_{t-k-1}+0.25a_{t-1}a_{t-k-1})
\end{aligned}
$$

> [!example]- PDF 第 2 页原貌（含原有批注）
> ![PDF p.2](<附件/ch2-lecture-p02.png>)

## PDF p.3

$$
=\begin{cases}1.25\sigma^2,&\text{if }k=0,\\0.5\sigma^2,&\text{if }k=1,\end{cases}
$$

and zero otherwise. Thus the autocovariance function does not depend on t and the time series is stationary. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其他情况下为 0。因此自协方差函数不依赖 t，时间序列平稳。</span></details>


Data set of $Z_t$: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Zₜ 的数据集：</span></details>

```text
[1] 0.000000000 1.199029059 0.937211975 0.377127620 -0.924223292
2.220568702 0.527257800
[8] 0.142674172 -1.834390395 -1.528993473 -0.085945082
0.416225614 0.121972651 -1.782135004
[15] 0.534948229 0.679576935 -0.996696720 1.069333629
1.490594600 -0.191680799 -1.015607750
[22] -0.966119524 0.982169064 -0.364061477 0.126410622
1.595840358 1.842386935 0.222502768
[29] 1.366782692 1.375200233 1.194991685 0.657327092
0.808684808 1.714032542 -0.057458359
[36] -1.788004908 -1.247961109 -0.868670219 -2.173200872 -0.159922316 -0.341009101 -0.628610581
[43] -1.175171658 -1.555893585 -0.182386914 0.802749687 -0.626516274 -1.091144944 -0.779253637
[50] -0.490859319 0.583532012 -1.170744961 0.334446867
0.182804797 -0.784265916 -0.549941369
[57] -0.916257097 -0.943788382 -1.109368599 -0.878730597 -0.001349007 -1.007794331 -0.661527550
[64] 1.296500949 1.296215840 -0.786050349 0.544770321
1.968043939 1.741360250 1.167194140
[71] -1.589614677 0.205395416 0.961343896 1.050667001
0.252366853 0.320838385 0.427223073
[78] 2.643445289 1.190330743 0.200806139 -0.536378755 -0.180027191 0.479469412 0.389866555
[85] -0.591259974 -0.549441985 0.348061201 0.094776612
1.323005303 0.612284727 -0.125294291
[92] -1.558313190 -1.467395135 -1.027625129 -1.118878250
1.055524758 2.680406656 2.186709476
[99] 1.233137154 -1.285679126
```

> [!example]- PDF 第 3 页原貌（含原有批注）
> ![PDF p.3](<附件/ch2-lecture-p03.png>)

## PDF p.4

![Plot of MA process zt=0.5a_(t-1)+a_t](<附件/ch2-lecture-p04-chart.png>)

**Plot of MA process zt=0.5a_(t-1)+a_t** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">移动平均过程 zₜ = 0.5aₜ₋₁ + aₜ 的图；横轴 Index 为时间序号。</span></details>


**Example 2:** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 2：</span></details>


Suppose $Y_t=5+2t+X_t$, where $X_t$ is a zero-mean stationary series with autocovariance function $\gamma_k$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设 Yₜ = 5 + 2t + Xₜ，其中 Xₜ 是零均值平稳序列，自协方差函数为 γₖ。</span></details>


(a) Find the mean function for $Y_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（a）求 Yₜ 的均值函数。</span></details>


Solution: $E(Y_t)=5+2t$ as $X_t$ has mean zero. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">解：由于 Xₜ 均值为 0，Yₜ 的均值为 5 + 2t。</span></details>


(b) Find the autocovariance function for $Y_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（b）求 Yₜ 的自协方差函数。</span></details>


Solution: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">解：</span></details>

$$
\begin{aligned}
&E[(Y_t-E(Y_t))(Y_{t-k}-E(Y_{t-k}))]\\
={}&E[(5+2t+X_t-5-2t)(5+2(t-k)+X_{t-k}-5-2(t-k))]\\
={}&E(X_tX_{t-k})=\gamma_k,
\end{aligned}
$$

the same autocovariance function as $X_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">与 Xₜ 的自协方差函数相同。</span></details>


(c) Is $Y_t$ stationary? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（c）Yₜ 是否平稳？</span></details>


**Example 3:** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 3：</span></details>


Consider the TS $Z_t=A\sin(\omega t+\theta)$, where A is rv with a zero mean and unit variance and $\theta$ is rv with a uniform distribution on the interval $[-\pi,\pi]$ independent of A. Then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑时间序列 Zₜ = A sin(ωt+θ)，其中 A 是均值为 0、方差为 1 的随机变量；θ 是与 A 独立、在 [−π,π] 上均匀分布的随机变量。则：</span></details>

$$E(Z_t)=E(A)E[\sin(\omega t+\theta)]=0.$$

> [!example]- PDF 第 4 页原貌（含原有批注）
> ![PDF p.4](<附件/ch2-lecture-p04.png>)

## PDF p.5

$$
\begin{aligned}
E(Z_tZ_{t+k})&=E[A^2\sin(\omega t+\theta)\sin(\omega(t+k)+\theta)]\\
&=E(A^2)E\left\{\frac12[\cos(\omega k)-\cos(\omega(2t+k)+2\theta)]\right\}\\
&=\frac12\cos(\omega k)-\frac12E\{\cos(\omega(2t+k)+2\theta)\}\\
&=\frac12\cos(\omega k)-\frac12\int_{-\pi}^{\pi}\cos(\omega(2t+k)+2\theta)\frac1{2\pi}\,d\theta\\
&=\frac12\cos(\omega k)-0=\frac12\cos(\omega k).
\end{aligned}
$$

Thus $Z_t$ is stationary. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此 Zₜ 平稳。</span></details>


**2.2.2 Sample Autocorrelation** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.2.2 样本自相关。</span></details>


For a series $\{X_t:t=1,\ldots,n\}$, define <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对序列 X₁,…,Xₙ，定义：</span></details>

$$C_k=\sum_{t=k+1}^nX_tX_{t-k}-(n-k)\bar X^2,\quad k=0,1,\ldots.$$

Then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则：</span></details>

$$r_k=C_k/C_0$$

is the kth sample autocorrelation coefficient of $\{X_t\}$. A plot of $r_k$ vs k is called the correlogram of $\{X_t\}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">rₖ 是该序列第 k 阶样本自相关系数。rₖ 关于 k 的图称为相关图。</span></details>


Notes: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">备注：</span></details>


i) Limits $\pm2/\sqrt n$ are conventionally used to assess significantly non-zero $r_k$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">i）通常用 ±2/√n 作为判断 rₖ 是否显著非零的界限。</span></details>


ii) Slowing decaying $r_k$, especially with $r_1\approx1$, is indicative of non-stationarity in $\{X_t\}$. May need to eliminate trend. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">ii）rₖ 缓慢衰减，尤其 r₁ 接近 1，提示序列非平稳，可能需要消除趋势。</span></details>


iii) Sudden peaks in $r_k$ suggest seasonal effects, again eliminate wherever possible. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">iii）rₖ 突然出现峰值提示季节效应，同样应尽可能消除。</span></details>


iv) Removal of trend or seasonal effect can induce autocorrelation pattern in the residual series. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">iv）去除趋势或季节效应可能使残差序列出现自相关结构。</span></details>


v) Let $X_t$ be a time series, then the autocovariance function of $X_t$ is defined as <details class="translation-details"><summary>中文译文</summary><span class="translation-body">v）时间序列 Xₜ 的自协方差函数定义为：</span></details>

$$\operatorname{Cov}(X_t,X_{t-k})=E[(X_t-E(X_t))(X_{t-k}-E(X_{t-k}))].$$

The autocorrelation function of $X_t$ is defined as <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Xₜ 的自相关函数定义为：</span></details>

$$\operatorname{Corr}(X_t,X_{t-k})=\frac{\operatorname{Cov}(X_t,X_{t-k})}{[\operatorname{var}X_t\operatorname{var}X_{t-k}]^{1/2}}.$$

> [!example]- PDF 第 5 页原貌（含原有批注）
> ![PDF p.5](<附件/ch2-lecture-p05.png>)

## PDF p.6


**Example 4:** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 4：</span></details>


Consider the MA1 process $Z_t$ of Example 1, then its sample autocorrelations is shown below. Notice the theoretical lag-1 autocorrelation coefficient is 0.4, while the sample autocorrelation coefficient is slightly larger than 0.4 as shown in the plot. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑例 1 的 MA1 过程 Zₜ，其样本自相关如下图。注意理论一阶自相关为 0.4，而图中的样本一阶自相关略大于 0.4。</span></details>

![Series zt ACF](<附件/ch2-lecture-p06-acf.png>)

**Series zt — ACF / Lag** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">序列 zₜ；纵轴为自相关函数，横轴为滞后阶数。</span></details>


**2.3 General Linear Process** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.3 一般线性过程。</span></details>


A general linear process (GLP) $\{Y_t\}$ is one that can be represented by a linear combination of present and past white noise terms, namely <details class="translation-details"><summary>中文译文</summary><span class="translation-body">一般线性过程可表示为当期与历史白噪声项的线性组合，即：</span></details>

$$Y_t=\psi_0e_t+\psi_1e_{t-1}+\cdots=\sum_{i=0}^{\infty}\psi_i e_{t-i}.$$

Without loss of generality, $\psi_0$ is usually set to be 1. For the right hand side of the series to be convergent, we need conditions on the $\psi_i$ terms. For our purpose, we impose the condition $\sum_{i=1}^{\infty}\psi_i^2<\infty$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">不失一般性，通常设 ψ₀ = 1。为使右侧级数收敛，需要对系数施加条件。这里要求系数平方和有限。</span></details>


Theorem: A general linear process with condition $\sum_{i=1}^{\infty}\psi_i^2<\infty$ is stationary. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">定理：系数平方和有限的一般线性过程是平稳的。</span></details>


Proof: By direct calculation, $E(Y_t)=0$, and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">证明：直接计算得均值为 0，并且：</span></details>

$$\operatorname{var}(Y_t)=E(Y_t^2)=\sigma_e^2\sum_{i=0}^{\infty}\psi_i^2<\infty,$$

free of t. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">不依赖 t。</span></details>


Finally <details class="translation-details"><summary>中文译文</summary><span class="translation-body">最后：</span></details>

$$
\begin{aligned}
\operatorname{cov}(X_t,X_{t+k})&=E(X_tX_{t+k})\\
&=E\left(\sum_{i=0}^{\infty}\psi_i e_{t-i}\sum_{j=0}^{\infty}\psi_j e_{t+k-j}\right)\\
&=\left(\sum_{i=0}^{\infty}\psi_i\psi_{i+k}\right)\sigma_e^2,
\end{aligned}
$$

which does not depend on t. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">此式也不依赖 t。</span></details>

> [!note] 原文核对
> 原文最后一式将 Y 写为 X，此处照录，不混改符号。

> [!example]- PDF 第 6 页原貌（含原有批注）
> ![PDF p.6](<附件/ch2-lecture-p06.png>)

## PDF p.7


**2.4 Exponential smoothing for a linear trend process** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.4 线性趋势过程的指数平滑。</span></details>


Suppose our process is of the form <details class="translation-details"><summary>中文译文</summary><span class="translation-body">假设过程具有下列形式：</span></details>

$$x_t=b_1+b_2t+\varepsilon_t,\qquad \varepsilon_t\sim\operatorname{NID}(0,\sigma^2),$$

if we use simple exponential smoothing, then recall <details class="translation-details"><summary>中文译文</summary><span class="translation-body">若使用简单指数平滑，回顾：</span></details>

$$
S_T=\alpha\sum_{k=0}^{T-1}\beta^k x_{T-k}+\beta^TS_0,\qquad\beta=1-\alpha.
$$
$$
\begin{aligned}
E(S_T)&=\alpha\sum_{k=0}^{T-1}\beta^kE(x_{T-k})+\beta^TS_0\\
&=\alpha\sum_{k=0}^{T-1}\beta^k[b_1+b_2(T-k)]+\beta^TS_0.
\end{aligned}
$$

As T goes to $\infty$, we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">当 T 趋于无穷时，有：</span></details>

$$
\begin{aligned}
E(S_T)&=(b_1+b_2T)\alpha\sum_{k=0}^{\infty}\beta^k-b_2\alpha\sum_{k=0}^{\infty}k\beta^k\\
&=b_1+b_2T-(\beta/\alpha)b_2=E(x_T)-(\beta/\alpha)b_2.
\end{aligned}\tag{2.4.1}
$$

Thus the smoothed statistic is a biased forecast for a linear trend process. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，对线性趋势过程而言，平滑统计量是有偏预测。</span></details>


**2.5 Double exponential smoothing (for linear trend process)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.5 双重指数平滑（适用于线性趋势过程）。</span></details>


Recall simple exponential smoothing, i.e., $S_T=\alpha x_T+(1-\alpha)S_{T-1}$, is a biased forecast for linear trend process. Now if we let <details class="translation-details"><summary>中文译文</summary><span class="translation-body">回顾：简单指数平滑对线性趋势过程产生有偏预测。现在令：</span></details>

$$S_T^{[2]}=\alpha S_T+(1-\alpha)S_{T-1}^{[2]}\tag{2.5.1}$$

it can be shown that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">可以证明：</span></details>

$$E(S_T^{[2]})=E(S_T)-\frac\beta\alpha b_2\tag{2.5.2}$$

thus <details class="translation-details"><summary>中文译文</summary><span class="translation-body">所以：</span></details>

$$b_2=(\alpha/\beta)[E(S_T)-E(S_T^{[2]})].\tag{2.5.3}$$

A logical estimate of $b_2$ at the end of time T is thus <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，在时点 T 结束时，b₂ 的一个合理估计是：</span></details>

$$\hat b_2(T)=\frac\alpha\beta(S_T-S_T^{[2]}).\tag{2.5.4}$$

Using (2.4.1) and (2.5.3), we observe <details class="translation-details"><summary>中文译文</summary><span class="translation-body">使用式（2.4.1）与（2.5.3），可见：</span></details>

$$
\begin{aligned}
E(x_T)&=E(S_T)+\frac\beta\alpha\frac\alpha\beta[E(S_T)-E(S_T^{[2]})]\\
&=2E(S_T)-E(S_T^{[2]}).
\end{aligned}\tag{2.5.5}
$$

Hence a reasonable estimate for $x_T$ at the end of time T is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">所以，T 期末对 xT 的合理估计为：</span></details>

$$\hat x_T=2S_T-S_T^{[2]}.\tag{2.5.6}$$

> [!example]- PDF 第 7 页原貌（含原有批注）
> ![PDF p.7](<附件/ch2-lecture-p07.png>)

## PDF p.8


Now <details class="translation-details"><summary>中文译文</summary><span class="translation-body">现在：</span></details>

$$
\hat b_1(T)+\hat b_2(T)\cdot T=\hat x_T
\quad\Rightarrow\quad
\hat b_1(T)=2S_T-S_T^{[2]}-T\frac\alpha\beta(S_T-S_T^{[2]}).\tag{2.5.7}
$$

Initial estimates satisfy <details class="translation-details"><summary>中文译文</summary><span class="translation-body">初始估计满足：</span></details>

$$S_0=\hat b_1(0)-\frac\beta\alpha\hat b_2(0),\qquad S_0^{[2]}=\hat b_1(0)-2\frac\beta\alpha\hat b_2(0),$$

where $\hat b_1(0)$ and $\hat b_2(0)$ are usually obtained by regression analysis on historical data. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">初始截距、斜率通常通过历史数据回归得到。</span></details>


**Forecasting** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">预测。</span></details>


If we always use a 'current origin approach', then we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">若始终采用“当前原点方法”，则有：</span></details>

$$\hat x_T(\tau)=\hat a_1(T)+\hat b_2(T)\tau,$$

where $\hat a_1(T)=\hat x_T=2S_T-S_T^{[2]}$, by (2.5.5). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">根据式（2.5.5），当前水平估计为 2ST − ST⁽²⁾。</span></details>

$$
\begin{aligned}
\because x_{T+\tau}&=b_1+b_2(T+\tau)\\
&=b_1+b_2T+b_2\tau\\
&=E(x_T)+b_2\tau.
\end{aligned}
$$

Rem 1: Rationale behind d. exp. smoothing is that $S_T$ lags behind $x_T$ by the 'same' amount that $S_T^{[2]}$ lags behind $S_T$. Thus we add back to $S_T$ the amount $S_T-S_T^{[2]}$, i.e. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">备注 1：双重指数平滑的思想是，ST 相对于 xT 的滞后量，与二次平滑相对于 ST 的滞后量“相同”。因此，把二者之差加回 ST，即：</span></details>

$$
\begin{aligned}
\hat x_T(\tau)&=b_1+b_2(T+\tau)\quad\text{theoretically}\\
&=E(x_T)+b_2\tau\\
&\approx S_T+(S_T-S_T^{[2]})+\hat b_2(T)\tau\quad\text{by (2.5.6)}\\
&=2S_T-S_T^{[2]}+\tau\frac\alpha\beta(S_T-S_T^{[2]})\\
&=S_T+\left(1+\tau\frac\alpha\beta\right)(S_T-S_T^{[2]}).
\end{aligned}\tag{2.5.8}
$$

Thus $E(\hat x_T(\tau))=b_1+b_2(T+\tau)$, showing the forecast is unbiased. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此预测的期望等于 b₁ + b₂(T+τ)，说明预测无偏。</span></details>


Note: I use the symbol $\hat x_T(\tau)$ to denote the $\tau$-step ahead forecast made at time T. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意：用 x̂T(τ) 表示在时点 T 作出的向前 τ 期预测。</span></details>


> [!example]- PDF 第 8 页原貌（含原有批注）
> ![PDF p.8](<附件/ch2-lecture-p08.png>)

## PDF p.9


**Choice of smoothing constant** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">平滑常数的选择。</span></details>


The smoothing constant controls the number of past realizations of the TS that influence the forecast. Small values of the smoothing constant give weights to many prior observations and result in a slow response to changes to the TS. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">平滑常数控制有多少历史观测会影响预测。常数较小时，较多历史值获得权重，因而对序列变化的响应较慢。</span></details>


However, large smoothing constant respond more rapidly to the change in the TS, it may cause the system to respond to random variations, when actually the system (TS) does not change. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">平滑常数较大时响应较快，但可能在序列本身没有改变时，对偶然波动作出反应。</span></details>


Some authors suggest the rule that we choose between 0.01 and 0.3 for a constant process. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">有些作者建议，恒定水平过程的平滑常数取 0.01 至 0.3。</span></details>


A quantitative method is to carry out a sequence of trials on a set of historical data using several different values for the smoothing constant, and then to select an $\alpha$ that optimizes some measure of effectiveness. One approach is using Least Squares. We consider <details class="translation-details"><summary>中文译文</summary><span class="translation-body">一种定量方法是在历史数据上试用若干平滑常数，选择使某种效果指标最优的 α。可以使用最小二乘法，考虑：</span></details>

$$f(\alpha)=\sum_{t=m}^{m+k}\left\{x_{t+1}-\alpha\sum_{j=0}^{m-1}(1-\alpha)^jx_{t-j}\right\}^2$$

and minimize $f(\alpha)$ numerically to find $\alpha$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">通过数值最小化 f(α) 来确定 α。</span></details>


**2.6 Higher order smoothing (General polynomial)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.6 高阶平滑（一般多项式）。</span></details>


The d. exp. Smoothing method can be extended easily to higher order. For example, if the model is : <details class="translation-details"><summary>中文译文</summary><span class="translation-body">双重指数平滑可以推广到更高阶。例如，模型为：</span></details>

$$x_t=b_1+b_2t+(1/2)b_3t^2+\varepsilon_t,$$

with current origin forecasting equation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">当前原点预测方程为：</span></details>

$$\hat x_{T+\tau}(T)=\hat a_1(T)+\hat a_2(T)\tau+(1/2)\hat a_3(T)\tau^2,$$

then it can be shown <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则可证明：</span></details>

$$
\begin{aligned}
\hat a_1(T)&=3S_T-3S_T^{[2]}+S_T^{[3]},\\
\hat a_2(T)&=\frac\alpha{2\beta^2}[(6-5\alpha)S_T-2(5-4\alpha)S_T^{[2]}+(4-3\alpha)S_T^{[3]}],\\
\hat a_3(T)&=\left(\frac\alpha\beta\right)^2(S_T-2S_T^{[2]}+S_T^{[3]}).
\end{aligned}
$$

where <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中：</span></details>

$$
\begin{aligned}
S_T&=\alpha x_T+(1-\alpha)S_{T-1},\\
S_T^{[2]}&=\alpha S_T+(1-\alpha)S_{T-1}^{[2]},\\
S_T^{[3]}&=\alpha S_T^{[2]}+(1-\alpha)S_{T-1}^{[3]}.
\end{aligned}
$$

> [!example]- PDF 第 9 页原貌（含原有批注）
> ![PDF p.9](<附件/ch2-lecture-p09.png>)

## PDF p.10


The above procedure is known as triple exponential smoothing. Result can be generalized to nth degree polynomial directly. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">上述方法称为三重指数平滑。其结果可直接推广到 n 次多项式。</span></details>


> [!example]- PDF 第 10 页原貌（含原有批注）
> ![PDF p.10](<附件/ch2-lecture-p10.png>)

## PDF p.11


**An Example** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">一个例子。</span></details>


Four years of monthly data (1995-1998) for the sales of a kind of filter are available. We'll use it to illustrate the calculations of the D. Exponential Smoothing method. We use the first two years (1995, 1996) data to find the initial estimates (Regression method), and show the forecasting for the year 1997. The table below gives the results: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">现有某种过滤器 1995—1998 年四年的月销量数据，用以演示双重指数平滑计算。用前两年（1995、1996）的数据通过回归确定初始估计，再展示 1997 年的预测结果：</span></details>

| Month of 1997 | Period | Actual sales | $S_T$ | $S_T^{[2]}$ | $\hat x_{T-1}(1)$ |
| --- | ---: | ---: | ---: | ---: | ---: |
| Jan | 1 | 538 | 446.28 | 352.22 | 541 |
| Feb | 2 | 570 | 458.65 | 362.86 | 551 |
| March | 3 | 600 | 472.79 | 373.85 | 565 |
| Apr | 4 | 565 | 482.01 | 384.67 | 583 |
| May | 5 | 485 | 482.31 | 394.43 | 590 |
| June | 6 | 604 | 494.48 | 404.44 | 580 |


Month of 1997 / Period / Actual sales <details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头：1997 年月份、期数、实际销量；其余列为一次平滑、二次平滑和在上一期作出的本期预测。</span></details>


Note : $\hat x_{T-1}(1)$ is the one-step ahead forecast for time T made at T-1. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意：x̂T₋₁(1) 是在 T−1 时点作出的、对 T 期的向前一期预测。</span></details>


**Calculations :** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">计算：</span></details>


Assume $S_0$ and $S_0^{[2]}$ are known from the regression based on 1995 and 1996. Let $S_0$ and $S_0^{[2]}$ be 436.09 and 341.77, and let the smoothing constant $\alpha$ be 0.1. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">假设通过 1995—1996 年数据回归已知两个初始平滑值，分别取 436.09 和 341.77，平滑常数为 0.1。</span></details>


Recall the forecasting equation, (2.5.8), we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">回顾预测方程（2.5.8），有：</span></details>

$$\hat x_0(\tau)=S_0+\left(1+\tau\frac\alpha\beta\right)(S_0-S_0^{[2]}),$$

thus the 1-step ahead forecast at time 0 (Dec. 1996) is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">所以，在时点 0（1996 年 12 月）作出的向前一期预测为：</span></details>

$$436.09+\left(1+\frac{0.1}{0.9}\right)(436.09-341.77)=540.89\approx541.$$

At the end of Jan. 1997, we know the sales for that month is 538 units. To calculate the forecast for Feb., we have to find $S_1$ and $S_1^{[2]}$ first, they are <details class="translation-details"><summary>中文译文</summary><span class="translation-body">到 1997 年 1 月末，知道当月销量为 538。为预测 2 月，需要先求一次和二次平滑值：</span></details>

$$S_1=0.1(538)+(1-0.1)436.09=446.28,$$
$$S_1^{[2]}=0.1(446.28)+(1-0.1)(341.77)=352.22.$$

Thus $\hat x_1(1)=550.79\approx551$, by (2.5.8) again. The other forecasts are obtained in a similar fashion. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">再次使用式（2.5.8）得到 2 月预测为 550.79，约为 551。其他预测依同样方法计算。</span></details>


> [!example]- PDF 第 11 页原貌（含原有批注）
> ![PDF p.11](<附件/ch2-lecture-p11.png>)

