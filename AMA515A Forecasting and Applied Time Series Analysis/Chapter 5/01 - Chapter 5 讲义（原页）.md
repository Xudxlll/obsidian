---
course: "AMA515A Forecasting and Applied Time Series Analysis"
chapter: 5
source: "tsf5_ama515A.pdf"
pages: 9
cssclasses:
  - ama-inline-translations
---

# Chapter 5 — 英文原文与折叠中文译文

> [!info] 阅读方式
> 本篇按 [tsf5_ama515A.pdf](<附件/tsf5_ama515A.pdf>)（共 9 页）原页序完整转录英文正文、公式、表格与例题，每段附默认折叠的中文译文；原文疑似笔误照录并注明疑点。每页末尾可展开对应印刷原页核对，带教师手写批注的扫描版逐页补充见 [02 - Chapter 5 带批注讲义（原页）](<02 - Chapter 5 带批注讲义（原页）.md>)。
> [本章资料索引](<05 - Chapter 5 资料索引.md>) · [原始 PDF](<附件/tsf5_ama515A.pdf>) · [带批注讲义](<02 - Chapter 5 带批注讲义（原页）.md>) · [手写课堂笔记](<03 - Chapter 5 手写课堂笔记.md>)

## PDF p.1

**AMA515A Forecasting and applied time series analysis** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AMA515A 预测与应用时间序列分析。</span></details>

**Chapter 5 Forecasting with BJ models (ARMA models)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 5 章 使用 Box–Jenkins 模型（ARMA 模型）进行预测。</span></details>

### 5.1 Introduction & general theory <details class="translation-details"><summary>中文译文</summary><span class="translation-body">5.1 引言与一般理论。</span></details>

Recall an ARMA model in general expressed in the form <details class="translation-details"><summary>中文译文</summary><span class="translation-body">回顾一般形式的 ARMA 模型可写为：</span></details>

$$
\Phi(B)X_t = \theta(B)a_t, \quad \text{where } \{a_t\} \text{ denotes white noise}
$$

and thus <details class="translation-details"><summary>中文译文</summary><span class="translation-body">从而：</span></details>

$$
X_t = \Phi(B)^{-1}\theta(B)a_t
$$

i.e. $X_t$ always has a random-shock representation in general <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即 X_t 一般总具有随机冲击表示（random-shock representation）：</span></details>

$$
X_t = a_t + \psi_1 a_{t-1} + \psi_2 a_{t-2} + \cdots.
$$

Let $X_i(\ell)$ denote the forecast at $i$ for $\ell$ period ahead <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设 X_i(ℓ) 表示在时刻 i 向前 ℓ 期的预测值（原图此处配有时间轴示意图：横轴 t 上依次标出 i（下方箭头标注 present“当前”）与 ℓ + i）。</span></details>

Suppose $\hat{X}_i(\ell) = \psi_\ell^* a_i + \psi_{\ell+1}^* a_{i-1} + \cdots$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">假设 X̂_i(ℓ) = ψ_ℓ* a_i + ψ_{ℓ+1}* a_{i−1} + …</span></details>

where the $\psi^*$ wts are to be determined. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中权重 ψ* 待确定。</span></details>

According to random shock representation, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">根据随机冲击表示：</span></details>

$$
\begin{aligned}
X_{i+\ell} &= a_{i+\ell} + \psi_1 a_{i+\ell-1} + \psi_2 a_{i+\ell-2} + \cdots \\
&\quad + \psi_{\ell-1} a_{i+1} + (\psi_\ell a_i + \psi_{\ell+1} a_{i-1} + \cdots)
\end{aligned}
$$

So <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此：</span></details>

$$
\begin{aligned}
E\left[\left\{X_{i+\ell} - \hat{X}_i(\ell)\right\}^2\right]
&= \left(1 + \psi_1^2 + \cdots + \psi_{\ell-1}^2\right)\sigma_a^2 + \sum_{j=\ell}^{\infty}\left(\psi_j - \psi_j^*\right)^2 \sigma_a^2.
\end{aligned}
$$

Thus mean square forecast error is a minimum when <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由此可见，均方预测误差（mean square forecast error）达到最小，当且仅当……</span></details>

> [!example]- PDF 第 1 页原图 · [[02 - Chapter 5 带批注讲义（原页）#PDF p.1|查看本页教师批注]]
> ![[Chapter 5/附件/ch5-print-p01.png]]

---

## PDF p.2

$$
\psi_j^* = \psi_j, \quad \text{for} \quad j = \ell, \ell+1, \dots
$$

So <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此：</span></details>

$$
\hat{X}_i(\ell) = \psi_\ell a_i + \psi_{\ell+1} a_{i-1} + \cdots \tag{5.1}
$$

The forecast error at $i$ for lead $\ell$ is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">在时刻 i 对提前期（lead）ℓ 的预测误差为：</span></details>

$$
\begin{aligned}
e_i(\ell) &= X_{i+\ell} - \hat{X}_i(\ell) \\
&= a_{i+\ell} + \psi_1 a_{i+\ell-1} + \cdots + \psi_{\ell-1} a_{i+1}.
\end{aligned} \tag{5.2}
$$

**Conditional Expectation** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">条件期望（Conditional Expectation）。</span></details>

Let $\underset{i}{E}$ denote the conditional expectation operator, which gives a value 'the expected value at time $i$ of a certain r.v.' <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设 E_i 表示条件期望算子，它给出“某个随机变量在时刻 i 的期望值”。</span></details>

Then clearly <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则显然有：</span></details>

$$
\underset{i}{E}[a_{i+\ell}] = \begin{cases} 0, & \ell > 0 \\ a_{i+\ell}, & \ell \le 0 \end{cases}.
$$

So eqn (5.1) gives <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此式 (5.1) 给出：</span></details>

$$
\underset{i}{E}\left[\hat{X}_i(\ell)\right] = \hat{X}_i(\ell), \quad \ell > 0
$$

& eqn (5.2) gives <details class="translation-details"><summary>中文译文</summary><span class="translation-body">且式 (5.2) 给出：</span></details>

$$
\underset{i}{E}\left[e_i(\ell)\right] = 0, \quad \ell > 0 \tag{5.3}
$$

$$
\underset{i}{E}\left[X_{i+\ell}\right] = \hat{X}_i(\ell), \quad \ell > 0. \tag{5.4}
$$

Also clearly $\underset{i}{E}\left[X_{i+\ell}\right] = X_{i+\ell}, \quad \ell < 0.$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">同样显然，当 ℓ &lt; 0（含 ℓ ≤ 0）时，E_i[X_{i+ℓ}] = X_{i+ℓ}。（注：原文写作 ℓ &lt; 0，照录。）</span></details>

Eqn. (5.3) shows that the forecast error has zero expected value <details class="translation-details"><summary>中文译文</summary><span class="translation-body">式 (5.3) 表明预测误差的期望为零。</span></details>

Eqn. (5.4) shows that the forecasts are unbiased <details class="translation-details"><summary>中文译文</summary><span class="translation-body">式 (5.4) 表明该预测是无偏的（unbiased）。</span></details>

Eqn. (5.2) shows that the variance of the forecast error at lead $\ell$ is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">式 (5.2) 表明提前期 ℓ 处预测误差的方差为：</span></details>

$$
\operatorname{Var}(e_i(\ell)) = \left(1 + \psi_1^2 + \cdots + \psi_{\ell-1}^2\right)\sigma_a^2 \tag{5.5}
$$

> [!example]- PDF 第 2 页原图 · [[02 - Chapter 5 带批注讲义（原页）#PDF p.2|查看本页教师批注]]
> ![[Chapter 5/附件/ch5-print-p02.png]]

---

## PDF p.3

which is finite for all stationary processes and hence $(100-\alpha)\%$ confidence intervals for the forecasts are obtained as <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对所有平稳过程该方差均为有限值，由此可得预测的 (100−α)% 置信区间（注：带批注版中老师红笔补正为 100(1−α)%）：</span></details>

$$
\hat{X}_i(\ell) \pm k_\alpha \left\{\left(\sum_{j=0}^{\ell-1}\psi_j^2\right)\sigma_a^2\right\}^{\frac{1}{2}} \tag{5.5a}
$$

where $k_\alpha$ is the $\left(100 - \frac{\alpha}{2}\right)\%$ point of the standard normal variate. For large series, we can replace $\sigma_a^2$ by its estimate. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 k_α 为标准正态随机变量的 (100 − α/2)% 分位数。对于大样本序列，可用 σ_a² 的估计值替代 σ_a²。</span></details>

### 5.2 Forecasting Procedure <details class="translation-details"><summary>中文译文</summary><span class="translation-body">5.2 预测步骤。</span></details>

The difference eqn. form of an ARMA $(p, q)$ process is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">ARMA(p, q) 过程的差分方程形式为：</span></details>

$$
\begin{aligned}
X_{i+\ell} &= \phi_1 X_{i+\ell-1} + \cdots + \phi_p X_{i+\ell-p} + a_{i+\ell} \\
&\quad + \theta_1 a_{i+\ell-1} + \cdots + \theta_q a_{i+\ell-q}.
\end{aligned}
$$

So, taking conditional expectation at time $i$, for $\ell > 0$, the optimal forecast function can be written as <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，对 ℓ &gt; 0 在时刻 i 取条件期望，最优预测函数可写作（注：原印刷式 (5.6) 末尾误将 θ_q 印为 θ_p，教师在带批注版中已红笔更正为 θ_q，此处照录原 PDF）：</span></details>

$$
\begin{aligned}
\hat{X}_i(\ell) &= \phi_1 \underset{i}{E}[X_{i+\ell-1}] + \cdots + \phi_p \underset{i}{E}[X_{i+\ell-p}] \\
&\quad + 0 + \theta_1 \underset{i}{E}[a_{i+\ell-1}] + \cdots + \theta_p \underset{i}{E}[a_{i+\ell-q}]
\end{aligned} \tag{5.6}
$$

Thus for $1 < \ell < p, q$ say, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">于是，例如当 1 &lt; ℓ &lt; p, q 时（以下右侧 `← obs. value` 意为已知观测值）：</span></details>

$$
\begin{aligned}
\hat{X}_i(\ell) &= \phi_1 \hat{X}_i(\ell-1) + \cdots + \phi_{\ell-1} \hat{X}_i(1) \\
&\quad + \phi_\ell X_i + \cdots + \phi_p X_{i+\ell-p} && \leftarrow \text{obs. value} \\
&\quad + \theta_\ell a_i + \cdots + \theta_q a_{i+\ell-q} && \leftarrow \text{obs. value}
\end{aligned} \tag{5.6*}
$$

Eqn. (5.6) & the above eqn. are the most convenient form to use in practice. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">式 (5.6) 与上式 (5.6*) 是实际应用中最便于使用的形式。</span></details>

> [!example]- PDF 第 3 页原图 · [[02 - Chapter 5 带批注讲义（原页）#PDF p.3|查看本页教师批注]]
> ![[Chapter 5/附件/ch5-print-p03.png]]

---

## PDF p.4

**Updating ARIMA FORECASTS** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">更新 ARIMA 预测（Updating ARIMA Forecasts）。</span></details>

Starting with an observed series of length $N$ for which forecasts are required for leads up to $L$, we calculate the $\hat{X}_N(\ell), \ell = 1, 2, \dots, L$ recursively to fill up line (A) of Table 5.1, where if necessary some initial unknown $a$'s need to be set to zero. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">从长度为 N 的已观测序列出发，需要计算提前期直至 L 的预测值；我们递推计算 X̂_N(ℓ)（ℓ = 1, 2, …, L）以填满表 5.1 的第 (A) 行，必要时将若干初始未知的随机冲击 a 设为零。</span></details>

When $X_{N+1}$ becomes available we obtain, using eqn (5.2) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">当新观测值 X_{N+1} 到来时，利用式 (5.2) 可得：</span></details>

$$
a_{N+1} = X_{N+1} - \hat{X}_N(1) \tag{5.7}
$$

and then can easily update the forecasts for leads $1, \dots,$ by writing <details class="translation-details"><summary>中文译文</summary><span class="translation-body">接着便可方便地按如下公式更新提前期 1, … 的预测（注：原印刷漏印编号 `(5.8)`，下文提及 eqn. (5.8) 即指此式，教师在带批注版中已蓝笔补标）：</span></details>

$$
\hat{X}_{N+1}(\ell) = \hat{X}_N(\ell+1) + \psi_\ell a_{N+1}
$$

This follows since eqn. (5.1) yields <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这是因为由式 (5.1) 可得：</span></details>

$$
\hat{X}_{N+1}(\ell) = \psi_\ell a_{N+1} + \psi_{\ell+1} a_N + \psi_{\ell+2} a_{N-1} + \cdots
$$

and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">以及：</span></details>

$$
\hat{X}_N(\ell+1) = \psi_{\ell+1} a_N + \psi_{\ell+2} a_{N-1} + \cdots
$$

which on subtraction gives eqn. (5.8). Since we do not have $\hat{X}_N(L+1)$, we can proceed up to $\hat{X}_{N+1}(L-1)$. However $\hat{X}_{N+1}(L)$ is easily found then on reapplying eqn. (5.6*). Line (B) of Table 5.1 is thus obtained, and so on indefinitely. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">两式相减即得式 (5.8)。由于我们没有 X̂_N(L+1)，按此法只能更新到 X̂_{N+1}(L−1)；不过随后重新应用式 (5.6*) 即可轻松求出 X̂_{N+1}(L)。由此得到表 5.1 的第 (B) 行，此后可无限递推下去。</span></details>

*Example:* <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例：</span></details>

$$
\hat{X}_{N+1}(1) = \hat{X}_N(2) + \psi_1 a_{N+1}; \quad \hat{X}_{N+1}(2) \quad \text{from (5.6*)}
$$

i.e. updating one-step ahead forecasts & two-step ahead forecasts. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即更新一步提前预测与两步提前预测。</span></details>

*Table 5.1*

| $i$ | $X_i$ | $a_i$ | Lead $\ell$: $1$ | $2$ | $\dots$ | $L - 1$ | $L$ | |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $N$ | $X_N$ | | $\hat{X}_N(1)$ | $\hat{X}_N(2)$ | | $\hat{X}_N(L-1)$ | $\hat{X}_N(L)$ | (A) |
| $N+1$ | $X_{N+1}$ | $a_{N+1}$ | $\hat{X}_{N+1}(1)$ | $\hat{X}_{N+1}(2)$ | | $X_{N+1}(L-1)$ | $\hat{X}_{N+1}(L)$ | (B) |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表 5.1：表头为时刻 i、观测值 X_i、冲击 a_i 及提前期 Lead ℓ = 1, 2, …, L−1, L。原表中第 (A) 行向第 (B) 行画有左下斜箭头（如 X̂_N(2) → X̂_{N+1}(1)、X̂_N(L) → X_{N+1}(L−1)），且右下角 X̂_{N+1}(L) 带虚线框（需由 (5.6*) 另算）；原印刷中第 (A) 行 a_i 格为空、第 (B) 行 X_{N+1}(L−1) 漏印帽子符号，此处照录。</span></details>

> [!example]- PDF 第 4 页原图 · [[02 - Chapter 5 带批注讲义（原页）#PDF p.4|查看本页教师批注]]
> ![[Chapter 5/附件/ch5-print-p04.png]]

---

## PDF p.5

### 5.3 Examples <details class="translation-details"><summary>中文译文</summary><span class="translation-body">5.3 例题。</span></details>

Ex. 1 Recall the unemployment example of Ch.4. An AR(2) model is fitted to the data, i.e., $X_t - \mu = \phi_1(X_{t-1} - \mu) + \phi_2(X_{t-2} - \mu) + a_t$, which is equal to <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 1 回顾第 4 章的失业率例题。对数据拟合了一个 AR(2) 模型，即 X_t − μ = φ₁(X_{t−1} − μ) + φ₂(X_{t−2} − μ) + a_t，等价于：</span></details>

$$
X_t = \mu(1 - \phi_1 - \phi_2) + \phi_1 X_{t-1} + \phi_2 X_{t-2} + a_t = \theta_0 + \phi_1 X_{t-1} + \phi_2 X_{t-2} + a_t
$$

Corresponding to the printout, $\mu$ is the mean, and $\theta_0 = \mu(1 - \phi_1 - \phi_2)$ is the constant. So from Ch. 4, we have $\hat{\phi}_1 = 1.548, \hat{\phi}_2 = -0.645, \theta_0 = 0.493, \mu = 5.082$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对应软件输出，μ 为均值，θ₀ = μ(1 − φ₁ − φ₂) 为常数项。因此由第 4 章可得 φ̂₁ = 1.548、φ̂₂ = −0.645、θ₀ = 0.493、μ = 5.082。</span></details>

Thus at t=121 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此在 t = 121 处：</span></details>

$$
\hat{X}_t(1) = \hat{\theta}_0 + \hat{\phi}_1 X_t + \hat{\phi}_2 X_{t-1} = 5.81
$$

And <details class="translation-details"><summary>中文译文</summary><span class="translation-body">并且：</span></details>

$$
\hat{X}_t(2) = \hat{\theta}_0 + \hat{\phi}_1 \hat{X}_t(1) + \hat{\phi}_2 X_t = 5.488
$$

Ex. 2 (Cont from Ex. 1) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 2（续例 1）。</span></details>

Now recall the estimated prediction interval is $\hat{X}_t(\ell) \pm k_\alpha \left\{\left(\sum_{j=0}^{\ell-1}\psi_j^2\right)\sigma_a^2\right\}^{\frac{1}{2}}$ (see (5.5a)), and from the example in Ch.4, we have $\hat{\sigma}_a^2 = 0.1318$, and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">回顾估计的预测区间为式 (5.5a)，由第 4 章的例题有 σ̂_a² = 0.1318，并且：</span></details>

$$
\begin{aligned}
\hat{\psi}_1 &= \hat{\phi}_1 = 1.548 \\
\hat{\psi}_2 &= \hat{\phi}_1 \hat{\psi}_1 + \hat{\phi}_2 = 1.751 \\
\hat{\psi}_3 &= \hat{\phi}_1 \hat{\psi}_2 + \hat{\phi}_2 \hat{\psi}_1 = 1.71
\end{aligned}
$$

(Note: Why are the above equations true?) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（注：以上三个等式为何成立？）</span></details>

Hence prediction limits for the forecasts can be found. For instance, a 95% prediction limit for $\hat{X}_t(2)$ is $5.488 \pm 1.96\sqrt{0.1318}(1 + 1.548^2)^{1/2}$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由此可求出各预测值的预测限。例如，X̂_t(2) 的 95% 预测限为 5.488 ± 1.96√0.1318·(1 + 1.548²)^(1/2)。</span></details>

Ex. 3 ARMA (1,1) Process <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 3 ARMA(1, 1) 过程。</span></details>

Suppose process is $(1 - \phi B)X_t = (1 - \theta B)a_t$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设过程为 (1 − φB)X_t = (1 − θB)a_t，则：</span></details>

$$
\Rightarrow \quad X_{t+\ell} = \phi X_{t+\ell-1} + a_{t+\ell} - \theta a_{t+\ell-1}
$$

Forecasts are <details class="translation-details"><summary>中文译文</summary><span class="translation-body">预测值为：</span></details>

$$
\begin{aligned}
\hat{X}_t(1) &= \phi X_t - \theta a_t, && \text{for } \ell = 1 \\
\hat{X}_t(\ell) &= \phi \hat{X}_t(\ell-1), && \text{for } \ell \ge 2
\end{aligned}
$$

> [!example]- PDF 第 5 页原图 · [[02 - Chapter 5 带批注讲义（原页）#PDF p.5|查看本页教师批注]]
> ![[Chapter 5/附件/ch5-print-p05.png]]

---

## PDF p.6

The forecasts decay geometrically to the mean, as in an AR1 process, but with a lead-one forecast modified by a factor depending on $a_t = X_t - \hat{X}_{t-1}(1)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">预测值像 AR(1) 过程一样按几何速率衰减至均值，只是提前一步预测会受到一个依赖于 a_t = X_t − X̂_{t−1}(1) 的因子修正。</span></details>

Ex. 4 ARIMA (1, 1, 0) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 4 ARIMA(1, 1, 0)。</span></details>

Suppose process is $(1 - 0.8B)(1 - B)X_{t+\ell} = a_{t+\ell}$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设过程为 (1 − 0.8B)(1 − B)X_{t+ℓ} = a_{t+ℓ}，即：</span></details>

i.e.

$$
\begin{aligned}
&\left(1 - 1.8B + 0.8B^2\right)X_{t+\ell} = a_{t+\ell} \\
\Rightarrow \quad &X_{t+\ell} = 1.8X_{t+\ell-1} - 0.8X_{t+\ell-2} + a_{t+\ell}
\end{aligned}
$$

Thus forecast at origin $t$ are given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此以 t 为起点的预测为：</span></details>

$$
\begin{aligned}
\hat{X}_t(1) &= 1.8X_t - 0.8X_{t-1} \\
\hat{X}_t(2) &= 1.8\hat{X}_t(1) - 0.8X_t \\
\hat{X}_t(\ell) &= 1.8\hat{X}_t(\ell-1) - 0.8\hat{X}_t(\ell-2), \quad \ell = 3, 4, \dots.
\end{aligned}
$$

Ex.5 IMA (0, 1, 1) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 5 IMA(0, 1, 1)。</span></details>

$$
X_t - X_{t-1} = a_t + \theta_1 a_{t-1}.
$$

Thus $X_t = X_{t-1} + a_t + \theta_1 a_{t-1}$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">从而 X_t = X_{t−1} + a_t + θ₁ a_{t−1}，且：</span></details>

$$
\begin{aligned}
\& \quad \hat{X}_t(1) &= X_t + \theta_1 a_t \\
\& \quad \hat{X}_t(\ell) &= \hat{X}_t(\ell-1) \quad \text{for } \ell > 1
\end{aligned}
$$

Ex.6 IMA (0, 1, 1) with constant <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 6 带常数项的 IMA(0, 1, 1)。</span></details>

If a constant is present in the process, say $\mu$ then we have a slightly different picture <details class="translation-details"><summary>中文译文</summary><span class="translation-body">如果过程中包含一个常数项（比如 μ），情况就会略有不同：</span></details>

> [!example]- PDF 第 6 页原图 · [[02 - Chapter 5 带批注讲义（原页）#PDF p.6|查看本页教师批注]]
> ![[Chapter 5/附件/ch5-print-p06.png]]

---

## PDF p.7

$$
\begin{aligned}
&X_{t+\ell} = \mu + X_{t+\ell-1} + a_{t+\ell} + \theta_1 a_{t+\ell-1} \\
\Rightarrow \quad &\hat{X}_t(1) = \mu + X_t + \theta_1 a_t \\
&\hat{X}_t(l) = \mu + \hat{X}_t(\ell-1) \\
&\phantom{\hat{X}_t(l)} = \hat{X}_t(1) + (\ell-1)\mu \quad \text{for } \ell > 1.
\end{aligned}
$$

Ex.7 Seasonal time series model $(1, 0, 0)(0, 1, 1)_{12}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 7 季节时间序列模型 (1, 0, 0)(0, 1, 1)_{12}。</span></details>

Model: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">模型（注：第 4 行印刷存在三处符号笔误：X_{t−l−12}、X_{t+l−−13}、a_{t+l−−12}，教师在带批注版中已红笔更正为 X_{t+l−12}、X_{t+l−13}、a_{t+l−12}，此处照录原 PDF）：</span></details>

$$
\begin{aligned}
&(1 - \alpha B)(1 - B^{12})X_t = (1 - \theta B^{12})a_t \\
\therefore \quad &X_t - \alpha X_{t-1} - X_{t-12} + \alpha X_{t-13} = a_t - \theta a_{t-12} \\[6pt]
\Rightarrow \quad &X_t = \alpha X_{t-1} + X_{t-12} - \alpha X_{t-13} - \theta a_{t-12} + a_t \\
\Rightarrow \quad &X_{t+l} = \alpha X_{t+l-1} + X_{t-l-12} - \alpha X_{t+l--13} - \theta a_{t+l--12} + a_{t+l} \\[6pt]
\therefore \quad &\underset{t}{E}(X_{t+1}) = \hat{X}_t(1) \\
&\phantom{\underset{t}{E}(X_{t+1})} = \alpha X_t + X_{t-11} - \alpha X_{t-12} - \theta a_{t-11} \\[6pt]
&\underset{t}{E}(X_{t+2}) = \hat{X}_t(2) \\
&\phantom{\underset{t}{E}(X_{t+2})} = \alpha \hat{X}_t(1) + X_{t-10} - \alpha X_{t-11} - \theta a_{t-10} \\
&\phantom{\underset{t}{E}(X_{t+2})} = \alpha^2(X_t - X_{t-12}) + X_{t-10} - \theta \alpha a_{t-11} - \theta a_{t-10} \\
&\vdots
\end{aligned}
$$

Higher order forecast can be obtained similarly. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">更高步数的预测可类似求得。</span></details>

Ex. 8 A time series of 100 observations satisfies the following model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 8 一个含 100 个观测值的时间序列满足如下模型：</span></details>

$$
X_t = 20.62 + 0.777 X_{t-1} - 0.492 X_{t-2} + a_t.
$$

Its last 5 observation's are shown below: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其最后 5 个观测值如下表所示（注：原文 "observation's" 照录）：</span></details>

| $t$ | 96 | 97 | 98 | 99 | 100 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $X_t$ | 31.68 | 29.10 | 23.15 | 26.74 | 32.44 |

Forecast its $101^{\text{th}}$ observation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">试预测第 101 个观测值。（注：原文印作 101th，教师在带批注版中改标为 101st，此处照录。）</span></details>

> [!example]- PDF 第 7 页原图 · [[02 - Chapter 5 带批注讲义（原页）#PDF p.7|查看本页教师批注]]
> ![[Chapter 5/附件/ch5-print-p07.png]]

---

## PDF p.8

Soln: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">解：</span></details>

$$
\begin{aligned}
&X_{t+1} = 20.62 + 0.777 X_t - 0.492 X_{t-1} + a_{t+1} \\
\Rightarrow \quad &\hat{X}_t(1) = 20.62 + 0.777 X_t - 0.492 X_{t-1} \\
&\phantom{\hat{X}_t(1)} = 20.62 + 0.777(32.44) - 0.492(26.74) \\
&\phantom{\hat{X}_t(1)} = 32.67.
\end{aligned}
$$

Ex. 9 For the model $(1 - B)(1 - 0.2B)X_t = (1 - 0.5B)a_t,\; a_t \sim N(0, 1)$, find its forecast for one & two steps ahead. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 9 对于模型 (1 − B)(1 − 0.2B)X_t = (1 − 0.5B)a_t，其中 a_t ~ N(0, 1)，求其向前一步与向前两步的预测。</span></details>

(a) If $a_t = 1, X_t = 4, X_{t-1} = 3$, show that $\hat{X}_t(2) = 3.64$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(a) 若 a_t = 1、X_t = 4、X_{t−1} = 3，证明 X̂_t(2) = 3.64。</span></details>

(b) Find the 95% prediction limit for your forecast in (a). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(b) 求你在 (a) 中所得预测值的 95% 预测区间。</span></details>

Ans: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">答：</span></details>

(a)

$$
\begin{aligned}
&(1 - 1.2B + 0.2B^2)X_t = a_t - 0.5a_{t-1} \\
&X_t = 1.2X_{t-1} - 0.2X_{t-2} - 0.5a_{t-1} + a_t \\
\text{Thus } &X_{t+1} = 1.2X_t - 0.2X_{t-1} - 0.5a_t + a_{t+1} \\
&\hat{X}_t(1) = 1.2X_t - 0.2X_{t-1} - 0.5a_t = 3.7 \\
&\hat{X}_t(2) = 1.2\hat{X}_t(1) - 0.2X_t \tag{*}
\end{aligned}
$$

Then by direct calculation, we have $\hat{X}_t(2) = 3.64$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">直接代入计算即得 X̂_t(2) = 3.64。</span></details>

(b) (i) Method 1, direct method: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(b) (i) 方法 1（直接法）：</span></details>

$$
\begin{aligned}
\text{Forecast error} = f(t) &= X_{t+2} - \hat{X}_t(2) \\
&= X_{t+2} - \left(1.2\hat{X}_t(1) - 0.2X_t\right), \quad \text{from (*)} \\
&= 1.2X_{t+1} - 0.2X_t - 0.5a_{t+1} + a_{t+2} - \left(1.2\hat{X}_t(1) - 0.2X_t\right) \\
&= 1.2\left(X_{t+1} - \hat{X}_t(1)\right) - 0.5a_{t+1} + a_{t+2}
\end{aligned}
$$

By direct calculation it can be shown $X_{t+1} - \hat{X}_t(1) = a_{t+1}$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">经直接计算可证 X_{t+1} − X̂_t(1) = a_{t+1}。</span></details>

Note $\sigma_a^2 = 1$. Thus $f(t) = 1.2a_{t+1} - 0.5a_{t+1} + a_{t+2} = 0.7a_{t+1} + a_{t+2}$, and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意 σ_a² = 1，故 f(t) = 1.2a_{t+1} − 0.5a_{t+1} + a_{t+2} = 0.7a_{t+1} + a_{t+2}，且：</span></details>

$$
\operatorname{var}(f(t)) = (1 + 0.7^2)\sigma_a^2 = 1 + 0.7^2 \tag{**}
$$

Hence 95% prediction interval = $3.64 \pm 1.96(\sqrt{1 + 0.7^2})$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此 95% 预测区间为 3.64 ± 1.96√(1 + 0.7²)。</span></details>

> [!example]- PDF 第 8 页原图 · [[02 - Chapter 5 带批注讲义（原页）#PDF p.8|查看本页教师批注]]
> ![[Chapter 5/附件/ch5-print-p08.png]]

---

## PDF p.9

(ii) Method 2 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(ii) 方法 2。</span></details>

Following Section 5.1, the 95% prediction interval for 2-step ahead forecast is $\hat{X}_t(2) \pm 1.96\sqrt{(1 + \psi_1^2)\sigma_a^2}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">根据第 5.1 节，向前两步预测的 95% 预测区间为 X̂_t(2) ± 1.96√((1 + ψ₁²)σ_a²)。</span></details>

Here we assume $X_t = a_t + \psi_1 a_{t-1} + \psi_2 a_{t-2} + \dots$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这里我们设 X_t = a_t + ψ₁ a_{t−1} + ψ₂ a_{t−2} + …</span></details>

That means <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这意味着：</span></details>

$$
\operatorname{var}\left(X_{t+2} - \hat{X}_t(2)\right) = (1 + \psi_1^2)\sigma_a^2.
$$

To find $\psi_1$, we note that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">为求 ψ₁，注意到：</span></details>

$$
\begin{aligned}
X_t &= (1 - B)^{-1}(1 - 0.2B)^{-1}(1 - 0.5B)a_t \\
&= (1 + B + B^2 + \dots)(1 + 0.2B + 0.04B^2 + \dots)(1 - 0.5B)a_t \\
&= (1 + (1 + 0.2 - 0.5)B + \dots)a_t
\end{aligned}
$$

Thus $\psi_1 = 0.7$ and $\operatorname{var}(X_{t+2} - \hat{X}_t(2)) = 1 + 0.7^2$. Compare with (**) above. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此 ψ₁ = 0.7，且 var(X_{t+2} − X̂_t(2)) = 1 + 0.7²，与前文 (**) 式一致。</span></details>

Finally we have 95% prediction interval = $3.64 \pm 1.96(\sqrt{1 + 0.7^2}) = (1.248,\; 6.032)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">最终得到 95% 预测区间为 3.64 ± 1.96√(1 + 0.7²) = (1.248, 6.032)。</span></details>

Note: This example illustrates that the computation of forecast and prediction limits for stationary and nonstationary models are the same. The proof is, however, not straightforward. You can look at Chapter 9 of Cryer and Chan (2008) for mathematical details if you are interested. Notice that for nonstationary models the prediction limits may grow without bound for large step ahead forecasts as $\psi_i$'s do not form a convergent series, in contrast with the stationary case. This agrees with the nature of nonstationary models. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注：本例说明，平稳模型与非平稳模型的点预测和预测限计算方式相同，但其严格证明并不平凡；如有兴趣可参阅 Cryer and Chan (2008) 第 9 章的数学细节。注意，与平稳情形不同，对于非平稳模型，由于 ψ_i 并不构成收敛级数，随着预测步数增大，预测区间宽度可能无界增长；这正符合非平稳模型的本质特征。</span></details>

> [!example]- PDF 第 9 页原图 · [[02 - Chapter 5 带批注讲义（原页）#PDF p.9|查看本页扫描原貌]]
> ![[Chapter 5/附件/ch5-print-p09.png]]
