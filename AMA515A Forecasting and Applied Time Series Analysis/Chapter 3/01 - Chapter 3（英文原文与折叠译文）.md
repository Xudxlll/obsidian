---
course: "AMA515A Forecasting and Applied Time Series Analysis"
chapter: 3
source: "Chapter 3 Notes.pdf"
pages: 15
cssclasses:
  - ama-inline-translations
---

# Chapter 3 — 英文原文与折叠中文译文

[本章资料索引](<00 - Chapter 3 资料索引.md>) · [原始 PDF](<附件/Chapter 3 Notes.pdf>)

英文按原 PDF 页序整理，逐段附默认折叠的中文译文。独立公式和图表另排；每页底部可展开原页核对。原有题目与解答分别保留，不另编解题分析。

## PDF p.1


**AMA515A Forecasting and applied time series analysis** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AMA515A 预测与应用时间序列分析。</span></details>


### Chapter 3 : Box-Jenkins (ARIMA ) models <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 3 章：Box–Jenkins（ARIMA）模型。</span></details>


**3.1 Stationarity** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.1 平稳性。</span></details>


If a discrete time stochastic process $\{X_t\}$ satisfy the following conditions: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">若离散时间随机过程满足以下条件：</span></details>

$$
\begin{aligned}
\text{(i)}\quad&E(X_t)=\mu\ \text{(constant) for all }t,\\
&\operatorname{Var}(X_t)=\sigma^2\ \text{(constant) for all }t,\\
\text{(ii)}\quad&\operatorname{Cov}(X_t,X_s)=\Gamma_{t-s}\ \text{(depend on t-s only !)}
\end{aligned}
$$

Then $\{X_t\}$ possesses second order stationarity. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则该过程具有二阶平稳性。</span></details>


In our following discussion we concentrate on process of this type. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">以下主要讨论这类过程。</span></details>


**3.2 Autocorrelation function of a stationary stochastic process** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.2 平稳随机过程的自相关函数。</span></details>


Recall for a stochastic process which is stationary, the autocovariance function is equal to <details class="translation-details"><summary>中文译文</summary><span class="translation-body">回顾：平稳随机过程的自协方差函数为：</span></details>

$$\gamma(k)=E(X_tX_{t+k})-E(X_t)E(X_{t+k}),\quad \gamma(0)=E(X_t^2)-E^2(X_t)=\operatorname{var}(X_t).$$

Note: $\gamma(k)$ is known as the autocovariance function. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意：γ(k) 称为自协方差函数。</span></details>


We then define the autocorrelation function $\rho(k)=\gamma(k)/\gamma(0)$, $k=0,\pm1,\pm2,\ldots$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">定义自相关函数为 γ(k)/γ(0)，k = 0、±1、±2、…。</span></details>


**3.3 Some simple stochastic models and their autocorrelation function** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.3 一些简单随机模型及其自相关函数。</span></details>


**3.3.1 White noise** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.3.1 白噪声。</span></details>


$X_t=Z_t$, $t=0,\pm1,\pm2,\ldots$, where $\{Z_t\}$ is a sequence of iid rv's with zero mean and constant variance. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Xₜ = Zₜ，其中 Zₜ 是均值为零、方差恒定的独立同分布随机变量序列。</span></details>


Then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则：</span></details>

$$\gamma(k)=E(X_tX_{t-k})=\begin{cases}\sigma^2,&k=0,\\0,&\text{o.w.}\end{cases}$$

and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">并且：</span></details>

$$\rho(k)=\begin{cases}1,&k=0,\\0,&k\ne0.\end{cases}$$

**3.3.2 First order Autoregressive Process** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.3.2 一阶自回归过程。</span></details>

$$X_t=\alpha X_{t-1}+Z_t,\qquad |\alpha|<1.\tag{3.1}$$

> [!example]- PDF 第 1 页原貌（含原有批注）
> ![PDF p.1](<附件/ch3-lecture-p01.png>)

## PDF p.2


and $\{Z_t\}$ is white noise; $Z_t$, $X_{t-k}$ are uncorrelated for $k\ne0$. Then assume $\{X_t\}$ is stationary, taking expectation in (3.1), <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 Zₜ 为白噪声；原文称，当 k ≠ 0 时，Zₜ 与 Xₜ₋ₖ 不相关。假设 Xₜ 平稳，对式（3.1）取期望：</span></details>

$$E(X_t)=\alpha E(X_{t-1})\Rightarrow\mu=\alpha\mu\Rightarrow\mu=0.$$

and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">并且：</span></details>

$$
\begin{aligned}
V(X_t)&=\alpha^2V(X_{t-1})+V(Z_t)+2\alpha\operatorname{Cov}(X_{t-1},Z_t)\\
\Rightarrow V(X_t)&=\alpha^2V(X_t)+\sigma^2\\
\Rightarrow V(X_t)&=\sigma^2/(1-\alpha^2).
\end{aligned}
$$

For autocorrelation, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对自相关，有：</span></details>

$$
\begin{aligned}
E(X_tX_{t-k})&=\alpha E(X_{t-1}X_{t-k})+E(Z_tX_{t-k})\\
\Rightarrow\rho(k)&=\alpha\rho(k-1)\\
\Rightarrow\rho(k)&=\alpha^k,\quad\text{as }\rho(0)=1.
\end{aligned}
$$

Thm 3.1 : For an AR(1) process, $X_t=\phi X_{t-1}+\varepsilon_t$, $|\phi|<1$ is a necessary and sufficient condition for stationarity. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">定理 3.1：对于 AR(1) 过程，|φ| &lt; 1 是平稳的充要条件。</span></details>


Proof: By repeated substitution from the model we get <details class="translation-details"><summary>中文译文</summary><span class="translation-body">证明：反复代入模型得到：</span></details>

$$X_t=\phi(\phi X_{t-2}+\varepsilon_{t-1})+\varepsilon_t=\sum_{j=0}^{\infty}\phi^j\varepsilon_{t-j}.\tag{3.2}$$

We then make use of the theory of linear difference equation. See for example, Wei, 1993. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">接着使用线性差分方程理论，例如参见 Wei（1993）。</span></details>


We first solve the homogenous equation $X_t-\phi X_{t-1}=0$ to give the complementary function $X_t=k\phi^t$ where k depends on the initial condition. The infinite moving average representation (3.2) is a particular solution to this difference equation. The general solution to the original AR(1) difference equation is then the sum of the complementary function and the particular solution, i.e. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">先解齐次方程，得到齐次解 kφᵗ，其中 k 取决于初始条件。无限阶移动平均表示（3.2）是特解。原 AR(1) 差分方程的通解为齐次解与特解之和：</span></details>

$$X_t=k\phi^t+\sum_{j=0}^{\infty}\phi^j\varepsilon_{t-j}.\tag{3.3}$$

When $|\phi|<1$ the complementary function tends to zero for large t, so only the second term of (3.3), the particular solution, remains and the mean of $X_t$ is independent of t. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">当 |φ| &lt; 1 且 t 很大时，齐次解趋于零，只留下特解，均值不依赖 t。</span></details>


> [!example]- PDF 第 2 页原貌（含原有批注）
> ![PDF p.2](<附件/ch3-lecture-p02.png>)

## PDF p.3


$E(X_t)=0$. In addition the variance of the second term of (5.3) converges for $|\phi|<1$, so the model is second order stationary. (Exercise : show that $E(X_tX_{t-k})=\gamma(k)=\sigma^2\phi^k/(1-\phi^2)$.) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">均值为零。此外，当 |φ| &lt; 1 时，式（5.3）第二项的方差收敛，所以模型二阶平稳。练习：证明所列自协方差公式。式号（5.3）沿用原文。</span></details>


Conversely from (3.2) it is clear that the variance of $X_t$ is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">反之，由式（3.2）可见 Xₜ 的方差为：</span></details>

$$\sigma^2\sum_{j=0}^{\infty}\phi^{2j}\quad\text{(assume variance of }\varepsilon_t\text{ is }\sigma^2\text{)},$$

and for this sum to be finite we need $|\phi|<1$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">该和有限要求 |φ| &lt; 1。</span></details>


**3.3.3 Finite order moving average process** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.3.3 有限阶移动平均过程。</span></details>


The process is defined by $X_t=\sum_{i=0}^m\beta_iZ_{t-i}$, where $\{Z_t\}$ is white noise and conventionally we set $\beta_0=1$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">过程定义为当前和前 m 期白噪声的线性组合，惯例设 β₀ = 1。</span></details>


Clearly <details class="translation-details"><summary>中文译文</summary><span class="translation-body">显然：</span></details>

$$E(X_t)=0,\quad\operatorname{Var}(X_t)=\sigma^2\sum_{i=0}^m\beta_i^2$$

and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">并且：</span></details>

$$
\begin{aligned}
\operatorname{Cov}(X_t,X_{t+k})&=E(X_tX_{t+k})=E\left[\sum_{i=0}^m\beta_iZ_{t-i}\sum_{j=0}^m\beta_jZ_{t-j+k}\right]\\
&=\sum_{i=0}^m\sum_{j=0}^m\beta_i\beta_jE(Z_{t-i}Z_{t-j+k})\\
&=\begin{cases}\sigma^2\sum_{i=0}^{m-k}\beta_i\beta_{i+k},&k=0,1,\ldots,m,\\0,&k>m.\end{cases}
\end{aligned}\tag{*}
$$

This is because $E(Z_{t-i}Z_{t-j+k})\ne0$ only when j=i+k. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这是因为只有 j = i + k 时，两个白噪声项乘积的期望才非零。</span></details>


So $\rho(k)=1$ if k=0 and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">所以 k = 0 时自相关为 1，而：</span></details>

$$\rho(k)=\begin{cases}\displaystyle\frac{\sum_{i=0}^{m-k}\beta_i\beta_{i+k}}{\sum_{i=0}^m\beta_i^2},&k=1,2,\ldots,m,\\0,&k>m.\end{cases}$$

i.e, a cut-off at lag m. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即在滞后 m 阶后截尾。</span></details>


> [!example]- PDF 第 3 页原貌（含原有批注）
> ![PDF p.3](<附件/ch3-lecture-p03.png>)

## PDF p.4


NB1. The following diagram is instructive <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意 1：下图有助于理解。</span></details>

![White-noise term alignment](<附件/ch3-lecture-p04-diagram.png>)

i / j <details class="translation-details"><summary>中文译文</summary><span class="translation-body">图中 i、j 对应两个求和指标；每列展示相应的白噪声项和系数，原表排列完整保留。</span></details>


NB2. In (\*), to evaluate $\sum_{i=0}^m\sum_{j=0}^m\beta_i\beta_jE(Z_{t-i}Z_{t-j+k})$, from the above table, we see that it will be simplified to the form <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意 2：式（&#42;）的双重求和，根据上表可以简化为：</span></details>

$$\sum_{i=0}^{m-k}\beta_i\beta_{i+k}E(Z_{t-i}Z_{t-(i+k)+k})=\sum_{i=0}^{m-k}\beta_i\beta_{i+k}\sigma^2.$$

Because t-i = t-j+k implies j= i+k. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因为 t − i = t − j + k 意味着 j = i + k。</span></details>


NB3. i+k is at most m, thus i is at most m-k, so we have $\sigma^2\sum_{i=0}^{m-k}\beta_i\beta_{i+k}$, k = 0,1,...,m. Moreover, j=i+k and both i and j are at most m, thus k is at most m in (\*) for the existence of non-zero terms. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意 3：i+k 最大为 m，所以 i 最大为 m−k，得到所列求和。又因为 i、j 均不超过 m，所以要存在非零项，k 最大为 m。</span></details>


Example: For MA(2), we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例：对于 MA(2)，有：</span></details>

$$\rho(1)=\frac{\beta_1+\beta_1\beta_2}{1+\beta_1^2+\beta_2^2},\quad\rho(2)=\frac{\beta_2}{1+\beta_1^2+\beta_2^2}.$$

> [!example]- PDF 第 4 页原貌（含原有批注）
> ![PDF p.4](<附件/ch3-lecture-p04.png>)

## PDF p.5

![Theoretical correlogram](<附件/ch3-lecture-p05-chart.png>)

The above diagram is the theoretical correlogram of an MA(2) process. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">上图为 MA(2) 过程的理论相关图。</span></details>


Example: For an invertible MA(2) process <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例：对于可逆 MA(2) 过程：</span></details>

$$y_t=\varepsilon_t-0.2\varepsilon_{t-1}+\theta_2\varepsilon_{t-2},$$

you are given that $\rho_1=-0.1$. Determine $\rho_2$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">已知一阶自相关为 −0.1，求二阶自相关。</span></details>


Solution: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">解：</span></details>

$$-0.1=\rho_1=\frac{\theta_1+\theta_1\theta_2}{1+\theta_1^2+\theta_2^2}\Rightarrow-0.1=\frac{-0.2-0.2\theta_2}{1+0.04+\theta_2^2}.$$

Solving the last equation, we get $\theta_2$ = -0.4 or 2.4. To satisfy the invertibility condition, $\theta_2$ = -0.4. Then $\rho_2=-1/3$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">解得 θ₂ 为 −0.4 或 2.4。为满足可逆性，取 −0.4，此时二阶自相关为 −1/3。</span></details>


**3.3.4 Random Walk** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.3.4 随机游走。</span></details>


Consider $X_t=X_{t-1}+Z_t$, where $\{Z_t\}$ is white noise, $Z_t$ and $X_{t-k}$ are uncorrelated for k>0. Then it is easy to see $X_t$ is mean stationary, but <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑随机游走，Zₜ 为白噪声，k &gt; 0 时 Zₜ 与 Xₜ₋ₖ 不相关。容易看出均值平稳，但：</span></details>

$$\operatorname{Var}(X_t)=\operatorname{Var}(X_{t-1})+\sigma^2=\operatorname{Var}(X_{t-2})+2\sigma^2$$

> [!example]- PDF 第 5 页原貌（含原有批注）
> ![PDF p.5](<附件/ch3-lecture-p05.png>)

## PDF p.6

$$=\cdots=\operatorname{Var}(X_0)+t\sigma^2.$$

Therefore the process is not stationary. However, $Y_t=\nabla X_t=X_t-X_{t-1}=Z_t$ is stationary. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此该过程不平稳，但其一阶差分等于 Zₜ，是平稳的。</span></details>


**3.4 A general class of linear process** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.4 一般线性过程。</span></details>


To extend our discussion, it is convenient to introduce 2 operators, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">为扩展讨论，引入两个算子：</span></details>


(i) Backward shift $BX_t=X_{t-1}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（i）后移算子。</span></details>


(ii) Differecnce $\nabla X_t=X_t-X_{t-1}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（ii）差分算子。Differecnce 按原文拼写保留。</span></details>


These operators obey simple algebraic rules, e.g. $B^2X_t=B(BX_t)=B(X_{t-1})=X_{t-2}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这些算子遵循简单代数规则，例如两次后移等于移到 t−2 期。</span></details>


Also $\nabla\equiv1-B$, so $\nabla^2=(1-B)^2=1-2B+B^2$, which implies $\nabla^2X_t=X_t-2X_{t-1}+X_{t-2}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">又有差分算子等于 1−B，其平方展开给出二阶差分。</span></details>


This agrees with <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这与以下结果一致：</span></details>

$$\begin{aligned}\nabla^2X_t&=\nabla(\nabla X_t)=\nabla(X_t-X_{t-1})\\&=X_t-X_{t-1}-(X_{t-1}-X_{t-2})\\&=X_t-2X_{t-1}+X_{t-2}.\end{aligned}$$

Also expression like $(1-\alpha B)^{-1}X_t$ can be regarded as $(1+\alpha B+\alpha^2B^2+\cdots)X_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">形如 (1−αB)⁻¹Xₜ 的表达式可视为所列幂级数。</span></details>


Examples: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例：</span></details>


(i) $X_t=\alpha X_{t-1}+Z_t$ is eq. to $(1-\alpha B)X_t=Z_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（i）AR(1) 的等价算子表示。</span></details>


(ii) $X_t=\sum_{i=0}^m\beta_iZ_{t-i}$ is equal to $X_t=\Theta(B)Z_t$, where $\Theta(B)$ is a polynomial in B. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（ii）有限阶 MA 可写成 B 的多项式作用于白噪声。</span></details>


(iii) $X_t=X_{t-1}+Z_t$ is equal to $\nabla X_t=Z_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（iii）随机游走等价于差分等于白噪声。</span></details>


**3.4.1 Infinite and finite order moving average process** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.4.1 无限阶与有限阶移动平均过程。</span></details>


**Infinite order** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">无限阶。</span></details>


Let Z be white noise. Consider $X_t=\alpha X_{t-1}+Z_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设 Z 为白噪声，考虑 AR(1) 过程。</span></details>


> [!example]- PDF 第 6 页原貌（含原有批注）
> ![PDF p.6](<附件/ch3-lecture-p06.png>)

## PDF p.7


Write $(1-\alpha B)X_t=Z_t$, which suggests <details class="translation-details"><summary>中文译文</summary><span class="translation-body">写成算子形式，提示：</span></details>

$$X_t=(1-\alpha B)^{-1}Z_t=\sum_{i=0}^{\infty}\alpha^iB^iZ_t=\sum_{i=0}^{\infty}\alpha^iZ_{t-i}.$$

Check: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">核对：</span></details>

$$\begin{aligned}X_t&=\alpha X_{t-1}+Z_t=\alpha(\alpha X_{t-2}+Z_{t-1})+Z_t\\&=\alpha^2X_{t-2}+\alpha Z_{t-1}+Z_t\\&=\alpha^3X_{t-3}+\alpha^2Z_{t-2}+\alpha Z_{t-1}+Z_t=\cdots.\end{aligned}$$

This shows that an AR(1) process can be represented as an infinite order moving average process. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这表明 AR(1) 可以表示为无限阶移动平均过程。</span></details>


**Finite order** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">有限阶。</span></details>

$$X_t=\Theta(B)Z_t=(\beta_0+\beta_1B+\beta_2B^2+\cdots+\beta_mB^m)Z_t=\sum_{i=0}^m\beta_iZ_{t-i}.$$

An important concept related to moving average (MA) process is invertibility. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">与移动平均过程有关的重要概念是可逆性。</span></details>


For an MA(1) process, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对于 MA(1)：</span></details>

$$X_t=Z_t+\beta Z_{t-1},\qquad|\beta|<1.\tag{3.4}$$

It is easy to see that $\rho(0)=1$, $\rho(1)=\beta/(1+\beta^2)$, $\rho(k)=0$ for k>1. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">容易求得零阶自相关为 1，一阶为 β/(1+β²)，更高阶为 0。</span></details>


Now consider the following process, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">再考虑：</span></details>

$$X_t=Z_t+\frac1\beta Z_{t-1}.\tag{3.5}$$

Then clearly it has the same ACF(autocorrelation function) as the previous process. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">它与前一个过程具有相同的自相关函数。</span></details>


So there is an indeterminacy problem. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因而存在不确定性问题。</span></details>


And for (3.4), observe $X_t=(1+\beta B)Z_t$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对式（3.4），观察其算子形式：</span></details>

$$Z_t=(1+\beta B)^{-1}X_t=X_t-\beta X_{t-1}+\beta^2X_{t-2}-\cdots,$$

> [!example]- PDF 第 7 页原貌（含原有批注）
> ![PDF p.7](<附件/ch3-lecture-p07.png>)

## PDF p.8


whence the coefficients on the RHS is decaying and convergent. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">右侧系数衰减且收敛。</span></details>


For (3.5), <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对式（3.5）：</span></details>

$$Z_t=X_t-\frac1\beta X_{t-1}+\frac1{\beta^2}X_{t-2}-\cdots,$$

The coefficients on the RHS are not decaying and not convergent. The representation is not meaningful as that suggests the error’s dependence on X increases as we go back in time. In general, for MA process $X_t=\Theta(B)Z_t$, if the representation $Z_t=\Theta(B)^{-1}X_t$ has this behavior, then the time series $X_t$ is not invertible. Intuitively, a non-invertible time series may have problem in statistical estimation. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">右侧系数不衰减也不收敛，意味着越早的 X 对误差影响越大，这种表示没有意义。一般地，若 MA 的逆表示具有这种性质，则序列不可逆；直观上，不可逆序列的统计估计可能有问题。</span></details>


For the MA(1), restricting |β|<1 will resolve both the indeterminacy and convergency problem. For general MA(q) process, we have the following theorem. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对 MA(1)，限制 |β| &lt; 1 可以解决不确定性与收敛问题。对一般 MA(q)，有以下定理。</span></details>


Thm.: A necessary and sufficient condition for a finite order MA process to be invertible is that all the roots of the polynomial $\Theta(B)$ lie outside the unit circle. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">定理：有限阶 MA 可逆的充要条件，是 MA 多项式的所有根均位于单位圆外。</span></details>


**3.4.2 Finite order autoregressive processes** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.4.2 有限阶自回归过程。</span></details>


Consider <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑：</span></details>

$$X_t=\alpha_1X_{t-1}+\alpha_2X_{t-2}+\cdots+\alpha_mX_{t-m}+Z_t.\tag{3.6}$$

In operator form, $\Phi(B)X_t=Z_t$, where $\Phi(.)$ is a polynomial of degree m. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">算子形式为 Φ(B)Xₜ = Zₜ，其中 Φ 是 m 次多项式。</span></details>


Temporarily assume stationarity, then $E(X_t)=0$, so multiply (5.4) by $X_{t-k}$ and take expectation gives <details class="translation-details"><summary>中文译文</summary><span class="translation-body">暂时假定平稳，此时均值为 0；将式（5.4）乘以 Xₜ₋ₖ 并取期望得到（式号依原文）：</span></details>

$$\gamma(k)=\alpha_1\gamma(k-1)+\alpha_2\gamma(k-2)+\cdots+\alpha_m\gamma(k-m),\quad k=1,2,\ldots.$$

In particular, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">特别地：</span></details>

$$\rho(k)=\alpha_1\rho(k-1)+\alpha_2\rho(k-2)+\cdots+\alpha_m\rho(k-m),\quad k=1,2,\ldots.\tag{3.7}$$

(3.7) are known as Yule-Walker equations. In principle, they can be solved to give $\rho(k)$, in terms of given $\alpha_i$, and vice versa. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">式（3.7）称为 Yule–Walker 方程。原则上可以根据已知参数求自相关，反之亦然。</span></details>


Write (3.7) as <details class="translation-details"><summary>中文译文</summary><span class="translation-body">将式（3.7）写成：</span></details>


> [!example]- PDF 第 8 页原貌（含原有批注）
> ![PDF p.8](<附件/ch3-lecture-p08.png>)

## PDF p.9

$$
\begin{pmatrix}\rho(1)\\\vdots\\\rho(m)\end{pmatrix}
=\begin{pmatrix}1&\rho(1)&\cdots&\rho(m-1)\\\rho(1)&1&\cdots&\rho(m-2)\\\vdots&\vdots&\ddots&\vdots\\\rho(m-1)&\cdots&\cdots&1\end{pmatrix}
\begin{pmatrix}\alpha_1\\\vdots\\\alpha_m\end{pmatrix}.
$$

Because $\rho(k)=\rho(-k)$ for stationary $\{X_t\}$, i.e., $\boldsymbol\rho=R\boldsymbol\alpha$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因为平稳过程的自相关函数对称，所以矩阵形式为 ρ = Rα。</span></details>


and provided $R^{-1}$ is defined, we have $\boldsymbol\alpha=R^{-1}\boldsymbol\rho$, i.e., given the 1st m autocorrelations, or estimates of the corr. parameters, the mth order autoregresssive process may be obtained, or estimated. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">若逆矩阵存在，即可由前 m 阶自相关或其估计获得、估计 m 阶自回归过程。</span></details>


Thm. A necessary and sufficient condition for the stationarity of the autoregressive process $\Phi(B)X_t=Z_t$, where $\Phi(B)$ is a polynomial in B of order m, is that the roots of the equation $\Phi(B)=0$ should all lie outside the unit circle. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">定理：自回归过程平稳的充要条件，是其 AR 多项式的全部根都位于单位圆外。</span></details>


Proof: We first show the AR(2) case, i.e., $X_t=\phi_1X_{t-1}+\phi_2X_{t-2}+\varepsilon_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">证明：先证明 AR(2) 情况。</span></details>


The solution to the homogenous difference equation $X_t-\phi_1X_{t-1}-\phi_2X_{t-2}=0$ depends on the roots $r_1,r_2$ of the equation $1-\phi_1z-\phi_2z^2=0$ (See Wei, 1993) which we shall assume are distinct although they may be complex. The complementary function is of the form $X_t=k_1(1/r_1)^t+k_2(1/r_2)^t$, where $k_1$ and $k_2$ are constants depending on initial conditions. The particular solution is the infinite MA representation $X_t=\phi^{-1}(B)\varepsilon_t=\psi(B)\varepsilon_t$. The general solution to the AR difference equation is therefore <details class="translation-details"><summary>中文译文</summary><span class="translation-body">齐次差分方程的解取决于特征多项式的两个根，假定它们相异，允许为复数。齐次解中的两个常数取决于初始条件。无限阶 MA 表示给出特解，因此通解为：</span></details>

$$k_1(1/r_1)^t+k_2(1/r_2)^t+\sum_{j=0}^{\infty}\psi_j\varepsilon_{t-j}.$$

For the model to have a constant mean, the complementary function must decay for large t, so we require $|1/r_1|<1$ and $|1/r_2|<1$. Moreover, the AR polynomial takes the form <details class="translation-details"><summary>中文译文</summary><span class="translation-body">为保持恒定均值，齐次解必须在 t 很大时衰减，即两根倒数的模小于 1。此外，AR 多项式可写为：</span></details>

$$\phi(B)=\left(1-\frac1{r_1}B\right)\left(1-\frac1{r_2}B\right).$$

where $r_1,r_2$ are its roots. A particular solution is $X_t=\psi(B)\varepsilon_t=\phi^{-1}(B)\varepsilon_t$, so using partial fractions we can write <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 r₁、r₂ 为多项式的根。特解如上，利用部分分式分解可写成下页形式。</span></details>


> [!example]- PDF 第 9 页原貌（含原有批注）
> ![PDF p.9](<附件/ch3-lecture-p09.png>)

## PDF p.10

$$\phi^{-1}(B)=\frac{a}{1-B/r_1}+\frac{b}{1-B/r_2}$$

where a and b are constants. Each of the terms in $\phi^{-1}(B)$ can be expanded - for instance, the first is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">a、b 为常数，每一项可以展开，例如第一项为：</span></details>

$$a\left[1+\frac1{r_1}B+\left(\frac1{r_1}B\right)^2+\cdots\right],$$

so if the variance of $X_t=\psi(B)\varepsilon_t=\phi^{-1}(B)\varepsilon_t$ is to converge we require that $1/|r_1|<1$ and $1/|r_2|<1$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">要使该过程方差收敛，要求两根模的倒数均小于 1。</span></details>


Hence the condition for an AR(2) model to be stationary is that both the roots $r_1$ and $r_2$ of the AR polynomial are outside the unit circle. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此 AR(2) 平稳要求两个根都在单位圆外。</span></details>


Similar logic can be applied to the general AR(p) model. Assuming that the roots of the corresponding AR polynomial $\phi(z)=1-\phi_1z-\cdots-\phi_pz^p$ are dintinct and denoting these $r_1,\ldots,r_p$ the complementary function is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">类似逻辑适用于一般 AR(p)。假定对应 AR 多项式的根相异，记为 r₁ 至 rₚ，则齐次解为：</span></details>

$$k_1(1/r_1)^t+k_2(1/r_2)^t+\cdots+k_p(1/r_p)^t.$$

Thus similar to the AR(2) argument if the roots are all outside the unit circle the complementary function will decay to zero for large t and the model will be stationary. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">与 AR(2) 同理，如果所有根都在单位圆外，齐次解随时间趋于零，模型平稳。</span></details>


Conversely, i.e. , the model is stationary and thus has finite variance. Let $\lambda_i=1/r_i$, then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">反之，若模型平稳，则具有有限方差。令 λᵢ = 1/rᵢ，则：</span></details>

$$X_t=\phi^{-1}(B)\varepsilon_t=\left[\prod_{i=1}^p(1-\lambda_iB)\right]^{-1}\varepsilon_t.$$

Assume again the roots are distinct, then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">再假定各根相异，则：</span></details>

$$X_t=\left\{\sum_{i=1}^p\frac{a_i}{1-\lambda_iB}\right\}\varepsilon_t,$$

for suitable $a_i$'s. Therefore, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 aᵢ 为适当常数。因此：</span></details>

$$X_t=\sum_{i=1}^p\sum_{j=0}^{\infty}a_i(\lambda_iB)^j\varepsilon_t$$

> [!example]- PDF 第 10 页原貌（含原有批注）
> ![PDF p.10](<附件/ch3-lecture-p10.png>)

## PDF p.11

$$=\sum_{i=1}^p\sum_{j=0}^{\infty}a_i\lambda_i^j\varepsilon_{t-j}.$$

So <details class="translation-details"><summary>中文译文</summary><span class="translation-body">所以：</span></details>

$$\operatorname{Var}(X_t)=\sigma^2\sum_{i=1}^p\sum_{j=0}^{\infty}a_i^2\lambda_i^{2j}=\sigma^2\sum_{i=1}^pa_i^2\sum_{j=0}^{\infty}\lambda_i^{2j}.$$

$\operatorname{Var}(X_t)$ is finite implies the absolute values of all $\lambda_i$'s are less than one. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">方差有限意味着全部 λᵢ 的绝对值小于 1。</span></details>

> [!note] 原文核对
> 本页方差展开照录；不同 i 项共享同一组误差，交叉项的处理存在疑点。原 PDF 及批注版本均保留，不直接更正证明。

**Example: An AR(2) process** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例：AR(2) 过程。</span></details>


Let $X_t=0.7X_{t-1}-0.1X_{t-2}+Z_t$, $\{Z_t\}\sim\operatorname{NID}(0,\sigma^2)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设给定的 AR(2) 过程，扰动独立正态分布，均值为零、方差为 σ²。</span></details>


Then $(1-0.7B+0.1B^2)X_t=Z_t$. The roots of the backshift polynomial in B, i.e., $1-0.7B+0.1B^2=0$, are 2 and 5. Thus the AR(2) process is stationary. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">后移多项式的根为 2 和 5，所以过程平稳。</span></details>


**3.4.3 Mixed processes(ARMA processes)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.4.3 混合过程（ARMA 过程）。</span></details>


The equation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">方程：</span></details>

$$\alpha_0X_t-\alpha_1X_{t-1}-\cdots-\alpha_pX_{t-p}=Z_t+\beta_1Z_{t-1}+\cdots+\beta_qZ_{t-q}.$$

Where $\{Z_t\}$ is white noise and conventionally $\alpha_0=1$ defines a mixed autoregressive moving average process of order (p,q), ARMA(p,q). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 Zₜ 为白噪声，惯例设 α₀ = 1。该方程定义 (p,q) 阶自回归移动平均混合过程，记作 ARMA(p,q)。</span></details>


In operator notation, we have $\Phi(B)X_t=\Theta(B)Z_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">算子表示为 Φ(B)Xₜ = Θ(B)Zₜ。</span></details>


Autocorrelation functions are available in principle via the equation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">原则上可通过下式获得自相关函数：</span></details>

$$X_t=\frac{\Theta(B)}{\Phi(B)}Z_t,$$

which expresses $X_t$ as a MA($\infty$) process. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">该式把 Xₜ 表示为无限阶 MA。</span></details>


**Example: An ARMA(2,1) process** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例：ARMA(2,1) 过程。</span></details>


Consider the process $X_t-0.75X_{t-1}+0.5625X_{t-2}=Z_t+1.25Z_{t-1}$, $\{Z_t\}\sim\operatorname{NID}(0,\sigma^2)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑给定过程，扰动为独立正态白噪声。</span></details>


The AR polynomial $\phi(B)=1-0.75B+0.5625B^2$ has zeros at $B=2(1\pm i\sqrt3)/3$, which lie outside the unit circle. The process is stationary. On the other hand, the MA polynomial $\theta(B)$ has a zero at b=-0.8 and hence the process is not invertible. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AR 多项式的根在单位圆外，因此平稳；MA 多项式的根为 −0.8，因此不可逆。</span></details>


**Parsimony** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">简约性。</span></details>


> [!example]- PDF 第 11 页原貌（含原有批注）
> ![PDF p.11](<附件/ch3-lecture-p11.png>)

## PDF p.12


In practice, may sets of data can reasonably be modelled by either a high order MA process or a lower order AR process. If so, we positively refer the version with fewer parameters. Similarly, an ARMA(p,q) process of lower order can often be made to fit data as either high order AR or MA process. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">实践中，许多数据既可用高阶 MA 也可用较低阶 AR 合理建模，应优先采用参数较少的版本。同样，较低阶 ARMA 常能拟合需要高阶 AR 或 MA 才能描述的数据。原文 may、refer 的措辞保留。</span></details>


**3.4.4 Low order models** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.4.4 低阶模型。</span></details>


Experience suggest that ARMA(p,q) process with $p+q\leq2$ constitute an extremely useful class of parsimonious models for stationary time series data. We can summarize main features of AR(2), MA(2), and ARMA(1,1) processes. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">经验表明，p+q 不超过 2 的 ARMA 是平稳数据中非常有用的简约模型。以下概括 AR(2)、MA(2) 与 ARMA(1,1) 的主要特征。</span></details>


**AR(2)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">二阶自回归。</span></details>

$$X_t=\alpha_1X_{t-1}+\alpha_2X_{t-2}+Z_t$$
$$\Rightarrow\Phi(B)X_t=Z_t,\quad\Phi(B)=1-\alpha_1B-\alpha_2B^2.$$

and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">并且：</span></details>

$$\Phi(B)=0\Leftrightarrow B=\frac{\alpha_1\pm\sqrt{\alpha_1^2+4\alpha_2}}{-2\alpha_2}.$$

For stationarity, require $|B|>1$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">平稳性要求根的模大于 1。</span></details>


The Yule-Walker equations become <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Yule–Walker 方程变为：</span></details>

$$\rho(k)=\alpha_1\rho(k-1)+\alpha_2\rho(k-2),\quad k\geq0.\tag{3.8}$$

In principle, can solve recursively from initial values $\rho(0)=1$, $\rho(1)=\alpha_1/(1-\alpha_2)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">原则上可由这两个初始值递推求解。</span></details>


Thus $\rho(2)=\alpha_1^2/(1-\alpha_2)+\alpha_2$, …etc. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因而二阶自相关如所列公式，其他阶类似。</span></details>


Note that constraints on $\alpha_1,\alpha_2$ implie constraints on $\rho(1)$ & $\rho(2)$. Alternatively, since (3.8) is a linear , 2nd order difference equation, it can be solved explicitly. In fact, for (3.8), i.e. $\rho(k)=\alpha_1\rho(k-1)+\alpha_2\rho(k-2)$, $k\geq0$, the general solution is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">参数约束也约束前两阶自相关。式（3.8）为线性二阶差分方程，可以显式求解，通解为：</span></details>

$$\rho(k)=A_1\lambda_1^k+A_2\lambda_2^k,$$

where $\lambda_1,\lambda_2$ are roots of $\lambda^2-\alpha_1\lambda-\alpha_2=0$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">λ₁、λ₂ 是所列特征方程的根。</span></details>


Values of $A_1,A_2$ can be obtained from using the initial values of $\rho(0)$ & $\rho(1)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">两个常数可以通过零阶和一阶自相关初值确定。</span></details>


Three distinct forms of solution: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">解有三种不同形式：</span></details>


> [!example]- PDF 第 12 页原貌（含原有批注）
> ![PDF p.12](<附件/ch3-lecture-p12.png>)

## PDF p.13


(i) $\alpha_1^2+4\alpha_2>0$ ⇒ mixtures of two exponentially decaying function for $\rho(k)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（i）判别式大于 0：自相关是两个指数衰减函数的混合。</span></details>


(ii) $\alpha_1^2+4\alpha_2<0$ ⇒ $\lambda=ae^{\pm i\theta}$, $\rho(k)$ is a damped harmonic. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（ii）判别式小于 0：复根使自相关呈阻尼振荡。</span></details>


(iii) $\alpha_1^2+4\alpha_2=0$ ⇒ $\rho(k)=(A_1+A_2k)\lambda^k$, an exponential decay. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（iii）判别式等于 0：重根情况下如式所示，呈指数衰减。</span></details>


**MA(2) Process** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">MA(2) 过程。</span></details>

$$X_t=Z_t+\beta_1Z_{t-1}+\beta_2Z_{t-2},\quad\text{equivalently }X_t=\Theta(B)Z_t.$$

For invertibility, require roots of $1+\beta_1B+\beta_2B^2=0$ to be outside the unit circle, i.e., <details class="translation-details"><summary>中文译文</summary><span class="translation-body">可逆性要求 MA 多项式的根位于单位圆外，即：</span></details>

$$\left|\frac{-\beta_1\pm\sqrt{\beta_1^2-4\beta_2}}{2\beta_2}\right|>1$$

which implies the same restriction on $(-\beta_1,-\beta_2)$ as for $(\alpha_1,\alpha_2)$ in AR(2) process. Again restrictions on $-\beta_1,\beta_2$ implies restrictions on $\rho(1)$ and $\rho(2)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对负的 MA 参数的限制，与 AR(2) 参数限制相同。参数限制又会约束前两阶自相关。第二句负号依原文照录。</span></details>


**ARMA(1,1)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">一阶自回归移动平均。</span></details>

$$X_t-\alpha X_{t-1}=Z_t+\beta Z_{t-1}\Rightarrow\left\{\frac{1+\beta B}{1-\alpha B}\right\}Z_t.$$

Thus |α|<1, |β|<1 are together sufficient to give a stationary , invertible process $\{X_t\}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">两个参数绝对值均小于 1，足以保证过程平稳且可逆。</span></details>


Consider the infinite order moving average representation, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑无限阶移动平均表示：</span></details>

$$
\begin{aligned}
X_t&=(1+\beta B)\sum_{i=0}^{\infty}\alpha^iB^iZ_t\\
&=\left\{1+\sum_{i=1}^{\infty}\alpha^{i-1}(\alpha+\beta)B^i\right\}Z_t\\
&=\sum_{i=0}^{\infty}b_iZ_{t-i},
\end{aligned}
$$

where $b_i$ to be determined. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">系数 bᵢ 待定。</span></details>


By direct calculation, $b_0=1$, $b_1=\alpha+\beta$, …, $b_i=\alpha^{i-1}(\beta+\alpha)$, for $i\geq1$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">直接计算得到所列系数。</span></details>


> [!example]- PDF 第 13 页原貌（含原有批注）
> ![PDF p.13](<附件/ch3-lecture-p13.png>)

## PDF p.14


then using results of section 3.3.3, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">使用第 3.3.3 节的结果：</span></details>

$$\rho(k)=\frac{\sum_{i=0}^{\infty}b_ib_{i+k}}{\sum_{i=0}^{\infty}b_i^2}$$

and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">并且：</span></details>

$$\sum b_i^2=1+(\alpha+\beta)^2\sum_{i=1}^{\infty}\alpha^{2i-2}=1+\frac{(\alpha+\beta)^2}{1-\alpha^2},$$
$$\sum_{i=0}^{\infty}b_ib_{i+k}=\alpha^{k-1}(\alpha+\beta)+\frac{\alpha^k(\alpha+\beta)^2}{1-\alpha^2},$$

and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">并且：</span></details>

$$\rho(k)=\frac{\alpha^{k-1}(\alpha+\beta)(1+\alpha\beta)}{1+2\alpha\beta+\beta^2},\quad k\geq1.$$

i.e. exponential decay, $\rho(k)=\alpha\rho(k-1)$, for $k\geq2$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即指数衰减，从二阶起满足所列递推关系。</span></details>


**Example: For an ARMA(2,1) process** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例：ARMA(2,1) 过程。</span></details>

$$y_t=0.3y_{t-1}+0.2y_{t-2}+\varepsilon_t+\theta\varepsilon_{t-1}$$

You are given $\rho_1=0.8$, $\rho_2=0.44$. Find $\rho_4$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">已知前两阶自相关为 0.8 和 0.44，求四阶自相关。</span></details>


Solution: Use the Yule-Walker equations. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">解：使用 Yule–Walker 方程。</span></details>

$$\rho_4=0.3\rho_3+0.2\rho_2=0.3\rho_3+0.088,\quad\rho_3=0.3\rho_2+0.2\rho_1=0.292,$$

hence $\rho_4=0.1756$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此四阶自相关为 0.1756。</span></details>


**3.5 Integrated process** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.5 单整过程。</span></details>


Recall the Markov process $X_t=X_{t-1}+Z_t$, which is nonstationary but can be transformed to a stationary process by differencing. More generally, consider the process <details class="translation-details"><summary>中文译文</summary><span class="translation-body">回顾非平稳的随机游走，它可通过差分转为平稳过程。更一般地，考虑：</span></details>

$$\Omega(B)X_t=\Theta(B)Z_t\tag{3.9}$$

where $\{Z_t\}$ is white noise, and $\Omega(B)=\Phi(B)(1-B)^d$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 Zₜ 为白噪声，Ω(B) 可分解为 Φ(B)(1−B)ᵈ。</span></details>


$\Phi(B)$, $\Theta(B)$ are polynomials of degree p,q respectively, all of their roots outside unit circle. Note that , so we can write (3.9) as <details class="translation-details"><summary>中文译文</summary><span class="translation-body">两个多项式次数分别为 p、q，所有根均在单位圆外。因此式（3.9）可写为下页形式。原文“Note that ,”中缺失的内容不猜补。</span></details>


> [!example]- PDF 第 14 页原貌（含原有批注）
> ![PDF p.14](<附件/ch3-lecture-p14.png>)

## PDF p.15

$$\Phi(B)\{\nabla^dX_t\}=\Theta(B)Z_t$$

i.e. the dth difference of $\{X_t\}$ is ARMA(p,q), we call (3.9) an autoregressive integrated moving average process or $\{X_t\}$ is an ARIMA(p,d,q) process. $\{X_t\}$ is nonstationary, so $\rho(k)$ does not exist. However, $\hat\rho(k)$ can be useful in identifying ARIMA process. Typically slow decay from $\hat\rho(1)\approx1$ suggest an integrated process a plausible model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即序列的 d 阶差分是 ARMA(p,q)，原序列称为 ARIMA(p,d,q)。原文指出原序列非平稳，平稳意义下的理论自相关函数不存在，但样本自相关有助于识别模型；从接近 1 的一阶自相关开始缓慢衰减，提示单整过程可能合适。</span></details>


Warning : over difference an already stationary series will often produce an undesirable increase in variability. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">警告：对已经平稳的序列过度差分，往往使波动不必要地增加。</span></details>


**3.6 Seasonal models** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.6 季节模型。</span></details>


The seasonal difference operator $\nabla_sX_t=X_t-X_{t-s}=(1-B^s)X_t$ can be used to eliminate seasonal nonstationarity. Formally, consider seasonal ARIMA models of the form <details class="translation-details"><summary>中文译文</summary><span class="translation-body">季节差分可消除季节性非平稳。正式地，考虑下列季节 ARIMA 模型：</span></details>

$$\Phi(B)(1-B)^{d_1}(1-B^s)^{d_2}X_t=\Theta(B)Z_t.$$

> [!example]- PDF 第 15 页原貌（含原有批注）
> ![PDF p.15](<附件/ch3-lecture-p15.png>)

