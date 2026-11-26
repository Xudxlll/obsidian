---
course: "AMA515A Forecasting and Applied Time Series Analysis"
chapter: 6
source: "AMA515A Chapter 6 Scanned Notes.pdf"
pages: 16
cssclasses:
  - ama-inline-translations
---

# Chapter 6 讲义、Exercise 6 与答案（英文原文、折叠译文与教师批注）

> [!info] 阅读方式与资料结构
> 本篇按 [AMA515A Chapter 6 Scanned Notes.pdf](<附件/AMA515A Chapter 6 Scanned Notes.pdf>)（共 16 页）原页序完整转录印刷英文原文、公式、表格与全部教师红笔／黑笔手写批注，逐段提供默认折叠的中文译文。原文印刷笔误与原手写算式笔误均照录并单独注明疑点；含软件时间序列图（Fig. 1–3）的页面及每页扫描原貌均保留原图供核对。
> [本章资料索引](<00 - Chapter 6 资料索引.md>) · [原始 PDF（16 页）](<附件/AMA515A Chapter 6 Scanned Notes.pdf>) · [Week 10 字幕重点](<02 - Chapter 6 Week 10 字幕重点.md>)

## 内容导航

- **第一部分：Chapter 6 GARCH Modelling 讲义正文**（[[#PDF p.1|PDF pp. 1–10]]）
- **第二部分：AMA 515 Exercise 6 题目**（[[#PDF p.11|PDF pp. 11–12]]）
- **第三部分：Outline Solution to Ex.6 参考解答**（[[#PDF p.13|PDF pp. 13–16]]）

---

## PDF p.1

**AMA515A Forecasting and applied time series analysis** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AMA515A 预测与应用时间序列分析。</span></details>

**Chapter 6 GARCH Modelling** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 6 章 GARCH 建模。</span></details>

### 6.1 Introduction <details class="translation-details"><summary>中文译文</summary><span class="translation-body">6.1 引言。</span></details>

It has been known to financial researchers for a long time that financial time series exhibit the behavior of volatility clustering. Engle (1982), however, was the first model that has paved the way for modeling this phenomenon. This is often referred to as conditional heteroscedascity model since it is assumed that overall the series is stationary but the conditional variance may be time-dependent. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">金融研究人员很早就注意到金融时间序列呈现波动率聚集（volatility clustering）特征。不过，Engle (1982) 是首个为刻画这一现象铺平道路的模型。这类模型常被称为条件异方差（conditional heteroscedasticity）模型，因为它假设序列整体上是平稳的，但条件方差可能随时间变化。（注：原文拼作 heteroscedascity，教师红笔补插 ti 改为 heteroscedasticity。）</span></details>

Many different time series models have been suggested for modeling time-varying volatility. The most popular ARCH/GARCH family will be studied in this course. The ARCH/GARCH is not available in standard statistical software systems such as minitab or SPSS. But it is available in econometric software such as RATS and GAUSS. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">学界提出了许多刻画时变波动率的时间序列模型，本课程将学习最常用的 ARCH/GARCH 族模型。标准统计软件（如 Minitab 或 SPSS）中并不提供 ARCH/GARCH，但在计量经济软件（如 RATS 和 GAUSS）中可以使用。</span></details>

Engle (1982) first suggested the ARCH model. An example is like below: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Engle (1982) 首次提出了 ARCH 模型。示例如下：</span></details>

$$
\begin{aligned}
y_t &= \mu + \phi_1 x_t + \phi_2 y_{t-1} + a_t \\
a_t &= \varepsilon_t \sigma_t, \quad \varepsilon_t \sim NID(0, 1) \\
\sigma_t^2 &= \omega + \alpha_1 a_{t-1}^2 + \dots + \alpha_p a_{t-p}^2 \qquad (*\ \text{volatility equation})
\end{aligned}
$$

Here $\mu, \phi_1, \phi_2$ are unknown parameters, $x_t$ is an explanatory variable, and $y_{t-1}$ is an lagged variable of $y_t$. (*) is called the conditional variance equation or volatility equation. In general the variable $y_t$ can have structure in both the mean and the variance. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 μ、φ₁、φ₂ 为未知参数，x_t 为解释变量，y_{t−1} 为 y_t 的滞后变量（注：原文 "an lagged"，教师红笔划去 n 改为 "a lagged"）。(*) 称为条件方差方程或波动率方程。一般而言，变量 y_t 在均值与方差两方面都可能具有结构。</span></details>

For ease of exposition, let us consider the following simple example: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">为便于阐述，先考虑如下简单例子：</span></details>

$$
\begin{aligned}
y_t &= a_t \\
a_t &= \varepsilon_t \sigma_t, \quad \varepsilon_t \sim NID(0, 1) \\
\sigma_t^2 &= \omega + \alpha_1 a_{t-1}^2 + \dots + \alpha_p a_{t-p}^2 \qquad (*)
\end{aligned}
$$

where <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中：</span></details>

$\omega > 0$ *and* $\alpha_i \ge 0, i = 1, \dots, p.$ *The conditions* $\omega > 0$ *and* $\alpha_i \ge 0, i = 1, \dots, p$ are sufficient to ensure that $\sigma_t > 0$. (*) is called the conditional variance equation or <details class="translation-details"><summary>中文译文</summary><span class="translation-body">ω &gt; 0 且 α_i ≥ 0（i = 1, …, p）。这些条件足以保证 σ_t &gt; 0。(*) 称为条件方差方程或……</span></details>

> [!tip] 本页教师手写批注（PDF p.1）
> - 红笔补正拼写：`heteroscedascity` → `heteroscedasticity`；划去 `an lagged` 中的 `n` → `a lagged`。

> [!example]- PDF 第 1 页原貌（含原有批注）
> ![[Chapter 6/附件/ch6-annotated-p01.png]]

---

## PDF p.2

volatility equation. This is because $\sigma_t^2 = E(a_t^2 \mid F_{t-1})$, where $F_{t-1}$ is the information set up to time $t-1$. That means $\sigma_t^2$ is the conditional variance of $a_t$ given $F_{t-1}$. In this example we assume the mean equation of the time series $\{y_t\}$ has no structure. Structure does exist in the conditional variance of $y_t$. ARCH is actually the acronym for Autoregressive Conditional Heteroscedasticity. The ARCH model is stationary. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">……波动率方程。这是因为 σ_t² = E(a_t² | F_{t−1})，其中 F_{t−1} 是截至 t−1 时刻的信息集，也就是说 σ_t² 是给定 F_{t−1} 时 a_t 的条件方差。在这个例子中我们假设序列 {y_t} 的均值方程没有结构，结构仅存在于 y_t 的条件方差中。ARCH 实际上是“自回归条件异方差”（Autoregressive Conditional Heteroscedasticity）的缩写。ARCH 模型是平稳的。</span></details>

Often $\varepsilon_t$ is assumed to be $t$-distributed or following some other symmetric fat tailed distribution. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">实际中常假设 ε_t 服从 t 分布或其他对称厚尾分布（fat-tailed distribution）。</span></details>

### 6.2 Properties of unconditional moments <details class="translation-details"><summary>中文译文</summary><span class="translation-body">6.2 无条件矩的性质。</span></details>

- **Mean** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">均值。</span></details>

Let $F_{t-1}$ be the information set up to time $t-1$. You can imagine that means everything related to the data up to time $t-1$ is known to the modeler. Then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设 F_{t−1} 为截至 t−1 时刻的信息集，可以将其理解为建模者已知截至 t−1 时刻与数据相关的一切信息。于是：</span></details>

$$
E(a_t) = E(\varepsilon_t \sigma_t) = E\big(E(\varepsilon_t \sigma_t \mid F_{t-1})\big) = E\big(\sigma_t E(\varepsilon_t \mid F_{t-1})\big) = E(\sigma_t \cdot 0) = 0
$$

- **Variance** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">方差（注：原印刷第 3 行误将 α_p 印作 α_q，教师红笔已更正为 p，此处照录原文）。</span></details>

$$
\begin{aligned}
\sigma_a^2 &= E(a_t^2) = E\big(E(a_t^2 \mid F_{t-1})\big) \\
&= E\big(\omega + \alpha_1 a_{t-1}^2 + \cdots + \alpha_p a_{t-p}^2\big) \\
&= \omega + \alpha_1 E(a_{t-1}^2) + \alpha_q E(a_{t-p}^2) \\
&= \omega + (\alpha_1 + \cdots + \alpha_p)\sigma_a^2.
\end{aligned}
$$

Hence, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此：</span></details>

$$
\sigma_a^2 = \frac{\omega}{1 - \alpha_1 - \dots - \alpha_p}.
$$

So in order for $\sigma_a^2 > 0$, $\alpha_1 + \dots + \alpha_p < 1$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此为使 σ_a² &gt; 0，需要 α₁ + … + α_p &lt; 1。</span></details>

- **Kurtosis** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">峰度（Kurtosis；教师红笔旁注“峰態／态 (4th moment)”）。</span></details>

Additional restrictions on $\alpha$'s are required to ensure the existence of higher-order moments. Taking <details class="translation-details"><summary>中文译文</summary><span class="translation-body">需要对系数 α 施加额外约束以保证高阶矩存在。取……</span></details>

> [!tip] 本页教师手写批注（PDF p.2）
> - 方差第 3 行红笔把误印的 $\alpha_q$ 圈改为 $\alpha_p$；右侧红笔展开完整移项过程：
>   $$
>   \sigma_a^2 = \omega + \alpha_1 E(a_{t-1}^2) + \alpha_2 E(a_{t-2}^2) + \cdots + \alpha_p E(a_{t-p}^2) = \omega + (\alpha_1 + \alpha_2 + \cdots + \alpha_p)\sigma_a^2
>   $$
>   $$
>   \Rightarrow \sigma_a^2 - (\alpha_1 + \alpha_2 + \cdots + \alpha_p)\sigma_a^2 = \omega \Rightarrow (1 - \alpha_1 - \alpha_2 - \cdots - \alpha_p)\sigma_a^2 = \omega
>   $$
> - 在 `Kurtosis` 旁红笔注记：`峰態 态 (4th moment)`。

> [!example]- PDF 第 2 页原貌（含原有批注）
> ![[Chapter 6/附件/ch6-annotated-p02.png]]

---

## PDF p.3

$\varepsilon_t \sim \text{NID}(0, 1)$ and assuming for simplicity $p = 1$ and that $m_4 = E(a_t^4)$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">……ε_t ~ NID(0, 1)，为简化设 p = 1 且 m₄ = E(a_t⁴)：</span></details>

$$
\begin{aligned}
m_4 &= E(a_t^4) \\
&= E E(a_t^4 \mid F_{t-1}) \\
&= E E(\varepsilon_t^4 \sigma_t^4 \mid F_{t-1}) = 3E\big((\omega + \alpha_1 a_{t-1}^2)^2\big) \\
&= 3E\big(\omega^2 + 2\alpha_1 \omega a_{t-1}^2 + \alpha_1^2 a_{t-1}^4\big) \\
&= 3\omega^2\left(1 + \frac{2\alpha_1}{1 - \alpha_1}\right) + 3\alpha_1^2 m_4
\end{aligned}
$$

Solving for $m_4$, We get <details class="translation-details"><summary>中文译文</summary><span class="translation-body">解出 m₄，得到：</span></details>

$$
m_4 = \frac{3\omega^2(1 + \alpha_1)}{(1 - \alpha_1)(1 - 3\alpha_1^2)}
$$

Hence for the fourth moment to exist we need, $0 \le \alpha_1^2 < 1/3$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，为使四阶矩存在，需要 0 ≤ α₁² &lt; 1/3。</span></details>

The standardized kurtosis, $k = m_4 / m_2^2 - 3$, and it can be shown $k > 0$, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">标准化峰度（超额峰度）为 k = m₄ / m₂² − 3，且可证明 k &gt; 0，</span></details>

which implies that $a_t$ has thicker tails than the normal distribution ($k = 0$). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这意味着 a_t 比正态分布（k = 0）具有更厚的尾部（thicker tails）。</span></details>

This fits the fact that financial time series usually have thick tails and outliers. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这契合金融时间序列通常呈现厚尾（thick tails）与异常值（outliers）的经验事实。</span></details>

### 6.3 AR Representation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">6.3 自回归（AR）表示。</span></details>

Setting $v_t = a_t^2 - \sigma_t^2$ then $v_t$ is white noise, that is, $E(v_t) = 0$ and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令 v_t = a_t² − σ_t²，则 v_t 为白噪声，即 E(v_t) = 0 且：</span></details>

$$
\operatorname{Cov}(v_t, v_s) = 0, \quad \text{if } t \ne s.
$$

Putting $a_t^2 = \sigma_t^2 + v_t$, obtain, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">将 σ_t² = a_t² − v_t（原文写作 Putting a_t² = σ_t² + v_t）代入，得（注：原印刷末项误将 α_p 印作 α_q，教师红笔已圈改为 p，照录原文）：</span></details>

$$
a_t^2 = \omega + \alpha_1 a_{t-1}^2 + \dots + \alpha_q a_{t-p}^2 + v_t
$$

> [!tip] 本页教师手写批注（PDF p.3）
> - 右侧红笔完整补写 $m_4$ 化简步骤：
>   $$
>   \begin{aligned}
>   m_4 &= 3\left[\omega^2 + 2\alpha_1 \omega \sigma_a^2 + \alpha_1^2 m_4\right] = 3\left[\omega^2 + 2\alpha_1 \omega \cdot \frac{\omega}{1 - \alpha_1} + \alpha_1^2 m_4\right] \\
>   &= 3\left(\omega^2 + 2\alpha_1 \frac{\omega^2}{1 - \alpha_1}\right) + 3\alpha_1^2 m_4 \\
>   \Rightarrow\quad m_4 - 3\alpha_1^2 m_4 &= 3\omega^2\left(1 + \frac{2\alpha_1}{1 - \alpha_1}\right) \\
>   m_4 &= \frac{3\omega^2\left(\frac{1 - \alpha_1 + 2\alpha_1}{1 - \alpha_1}\right)}{1 - 3\alpha_1^2} = \frac{3\omega^2(1 + \alpha_1)}{(1 - \alpha_1)(1 - 3\alpha_1^2)}
>   \end{aligned}
>   $$
> - 红笔注明四阶矩存在条件来自 $1 - 3\alpha_1^2 > 0 \text{ and } 1 - \alpha_1 > 0$；在峰度处补注 $m_2 = \sigma^2$，并红线下划 `thick tails and outliers.`。
> - 底部公式红笔将 $\alpha_q$ 改为 $\alpha_p$，并用方括号与箭头将 $\alpha_1 a_{t-1}^2 + \dots + \alpha_p a_{t-p}^2$ 移向左侧 $a_t^2$（引出下一页的 $\alpha(B)a_t^2 = \omega + v_t$）。

> [!example]- PDF 第 3 页原貌（含原有批注）
> ![[Chapter 6/附件/ch6-annotated-p03.png]]

---

## PDF p.4

or in operator notation, $\alpha(B) = 1 - a_1 B - \dots - \alpha_p B^p$ *and* $\alpha(B)a_t^2 = \omega + v_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">或者用滞后算子记号写为 α(B) = 1 − α₁B − … − α_p B^p 且 α(B)a_t² = ω + v_t。（注：原文首项系数误印为 a₁，教师红笔圈改为 α₁ 并展开 −α₂B² − α₃B³ −，此处照录原 PDF。）</span></details>

Hence we can summarize that if $a_t \sim ARCH(p)$ *then* $a_t^2 \sim AR(p)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由此可总结：若 a_t ~ ARCH(p)，则平方序列 a_t² ~ AR(p)。</span></details>

- **Remark** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注（Remark）。</span></details>

A necessary condition for $a_t^2$ to be stationary is that all roots of $\alpha(B) = 0$ are outside the unit circle. But this always holds when $\alpha_i \ge 0, i = 1, \dots, p$ *and* $\alpha_1 + \dots + \alpha_p < 1$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">a_t² 平稳的必要条件是特征方程 α(B) = 0 的所有根都在单位圆外；而当 α_i ≥ 0（i = 1, …, p）且 α₁ + … + α_p &lt; 1 时，该条件恒成立。</span></details>

### 6.4 Estimation and diagnostic checking <details class="translation-details"><summary>中文译文</summary><span class="translation-body">6.4 参数估计与诊断检验。</span></details>

- **LS estimates** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">最小二乘（LS，least square）估计。</span></details>

We can obtain LS estimates by fitting an $AR(p)$ to the squares of the series, $a_t^2$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">可以通过对平方序列 a_t² 拟合 AR(p) 模型来得到最小二乘估计。</span></details>

- **Maximum Likelihood Estimate** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">极大似然估计（Maximum Likelihood Estimate）。</span></details>

Let $X_{t-1} = \{a_0, a_1, \dots, a_{t-1}\}$. Then the joint density function can be written as, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设 X_{t−1} = {a₀, a₁, …, a_{t−1}}，则联合密度函数可写作：</span></details>

$$
f(a_1, \dots, a_t) = f(a_t \mid X_{t-1}) f(a_{t-1} \mid X_{t-2}) \dots f(a_1 \mid X_0) f(a_0)
$$

Given data $a_1, \dots, a_n$ the loglikelihood <details class="translation-details"><summary>中文译文</summary><span class="translation-body">给定观测数据 a₁, …, a_n，对数似然函数为：</span></details>

$$
L = \sum_{k=0}^{n-1} \log f(a_{n-k} \mid X_{n-k-1})
$$

can be evaluated using the model volatility equation for any assumed distribution for the $\varepsilon_t$. Then $L$ can be maximized numerically to obtain the MLE. Let $\theta = (\omega, \alpha_1, \dots, \alpha_p)$ denote the parameters. Then $\sqrt{n}(\hat{\theta} - \theta)$ converges in distribution to $N(0, I^{-1})$, where $I$ is the Fisher information matrix. But the method can be extended to more general cases. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对于 ε_t 的任意假定分布，均可利用模型的波动率方程计算该对数似然，再通过数值最优化极大化 L 得到极大似然估计（MLE）。记参数向量 θ = (ω, α₁, …, α_p)，则 √n(θ̂ − θ) 依分布收敛于 N(0, I⁻¹)，其中 I 为 Fisher 信息矩阵。该方法还可推广到更一般的情形。</span></details>

Example: ARCH(1) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例：ARCH(1)。</span></details>

> [!tip] 本页教师手写批注（PDF p.4）
> - 红笔圈改首行印刷笔误 $a_1$ 为 $\alpha_1 B - \alpha_2 B^2 - \alpha_3 B^3 -$；
> - `LS estimates` 旁红笔注明 `least square`；
> - 对数似然右侧红笔改写为自然对数记号：$=\sum_{k=0}^{n-1} \ln f(a_{n-k} \mid X_{n-k-1})$。

> [!example]- PDF 第 4 页原貌（含原有批注）
> ![[Chapter 6/附件/ch6-annotated-p04.png]]

---

## PDF p.5

$$
\begin{aligned}
X_t &= \phi X_{t-1} + a_t, \quad t = 1, \dots, n \\
E(a_t^2 \mid F_{t-1}) &= h_t = \sigma_t^2 = \omega + \alpha a_{t-1}^2 \qquad (*\ \text{volatility equation})
\end{aligned}
$$

Let $\theta = (\phi, \omega, \alpha)'$. Note here $\theta$ is a vector. Then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设 θ = (φ, ω, α)'（注意此处 θ 为列向量）。于是：</span></details>

$$
L(\theta) = \prod_{t=2}^{n} \frac{1}{\sqrt{2\pi h_t}} \exp\left\{-\frac{(x_t - \phi x_{t-1})^2}{2h_t}\right\},
$$

and in finding maximum likelihood, constants do not matter. So we consider <details class="translation-details"><summary>中文译文</summary><span class="translation-body">而在求极大似然时常数项不起作用，因此考虑如下对数似然（注：原印刷式漏写了求和号括号及分数分母中的 2；教师红笔已在分母补入 2，实际完整形式应为 −½ ∑_{t=2}^n (log h_t + (x_t − φ x_{t−1})² / h_t)，此处照录原 PDF）：</span></details>

$$
l = l(\theta) \propto -\frac{1}{2}\sum_{t=2}^{n} \log h_t + \frac{(x_t - \phi x_{t-1})^2}{h_t},
$$

and proceed as usual using Newton-Raphson's method. Namely, use the recursion <details class="translation-details"><summary>中文译文</summary><span class="translation-body">并按常规采用 Newton–Raphson 方法求解，即使用如下迭代公式：</span></details>

$$
\theta_{n+1} = \theta_n - \left.\left(\frac{\partial^2 l}{\partial \theta \partial \theta'}\right)^{-1} \frac{\partial l}{\partial \theta}\right|_{\theta_n}.
$$

Obtain value of $\theta_{n+1}$ from value of $\theta_n$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由 θ_n 的取值迭代求得 θ_{n+1}。</span></details>

Note here $\dfrac{\partial l}{\partial \theta}$ is vector. $\dfrac{\partial l}{\partial \theta} = \begin{pmatrix} \partial l / \partial \phi \\ \partial l / \partial \omega \\ \partial l / \partial \alpha \end{pmatrix}$ and similarly $\dfrac{\partial^2 l}{\partial \theta \partial \theta'}$ is a matrix. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意这里 ∂l/∂θ 是列向量，类似地 ∂²l/(∂θ∂θ') 是矩阵（Hessian 矩阵）。</span></details>

- **Diagnostic Checking** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">诊断检验（Diagnostic Checking）。</span></details>

Test the standardized residuals for autocorrelation, $\tilde{a}_t = \hat{a}_t / \hat{\sigma}_t$ as well as the squared values. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">检验标准化残差 ã_t = â_t / σ̂_t 及其平方序列是否存在自相关。</span></details>

### 6.5 GARCH Models <details class="translation-details"><summary>中文译文</summary><span class="translation-body">6.5 GARCH 模型。</span></details>

Often ARCH(p) models require a large number of parameters. To reduce the number of parameters the GARCH(p, q) was introduced (Bollerslev, 1986). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">ARCH(p) 模型往往需要大量参数；为减少参数个数，Bollerslev (1986) 引入了 GARCH(p, q) 模型：</span></details>

$$
\begin{aligned}
a_t &= \varepsilon_t \sigma_t, \quad \varepsilon_t \sim NID(0, 1) \\
\sigma_t^2 &= \omega + \alpha_1 a_{t-1}^2 + \alpha_p a_{t-p}^2 + \beta_1 \sigma_{t-1}^2 + \dots + \beta_q \sigma_{t-q}^2
\end{aligned}
$$

*(注：原印刷式漏印 $\alpha_1 a_{t-1}^2$ 与 $\alpha_p a_{t-p}^2$ 之间的 `+ \dots`，教师红笔已补插。)*

> [!tip] 本页教师手写批注（PDF p.5）
> - 左上红笔标明 $\theta$ 为 `Column vector` $\begin{pmatrix}\phi \\ \omega \\ \alpha\end{pmatrix}$；
> - 对数似然分母 $h_t$ 前红笔补入 `2`（变为 $2h_t$）；
> - 诊断检验左侧红笔重写 $\tilde{a}_t$；
> - 底部 GARCH 方程中红笔用插入符 `^` 补上 `+ \dots`。

> [!example]- PDF 第 5 页原貌（含原有批注）
> ![[Chapter 6/附件/ch6-annotated-p05.png]]

---

## PDF p.6

Sufficient conditions for positive $\sigma_t^2$ are $\omega > 0$, and $\alpha_i$'s and $\beta_i$'s all nonnegative. Other distributions such as the $t$-distribution are often used for $\varepsilon_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">保证 σ_t² 为正的充分条件是 ω &gt; 0 且所有 α_i 与 β_i 均非负。实际中也常对 ε_t 采用 t 分布等其他分布。</span></details>

#### 6.5.1 Properties of unconditional moments <details class="translation-details"><summary>中文译文</summary><span class="translation-body">6.5.1 无条件矩的性质。</span></details>

- **Variance** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">方差。</span></details>

Assuming $\sigma_a^2 = E(a_t^2)$ exists, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">假设 σ_a² = E(a_t²) 存在（注：原印刷第 2–3 行存在多处下标与符号笔误，如 β_{t−1}² 应为 a_{t−1}²、α_q 应为 α_p、β_p 应为 β_q，教师红笔已逐一更正，此处照录原 PDF）：</span></details>

$$
\begin{aligned}
E(a_t^2) &= E\big(E(a_t^2 \mid F_{t-1})\big) \\
&= E\big(E(\varepsilon_t^2(\omega + \alpha_1 \beta_{t-1}^2 + \cdots + \alpha_q a_{t-p}^2 + \beta_1 \sigma_{t-1}^2 + \beta_p \sigma_{t-q}^2) \mid F_{t-1})\big) \\
&= E\big(\omega + \alpha_1 a_{t-1}^2 + \cdots + \alpha_q a_{t-p}^2 + \beta_1 \sigma_{t-1}^2 + \cdots + \beta_p \sigma_{t-q}^2\big) \\
&= \omega + (\alpha_1 + \cdots + \alpha_p)\sigma_a^2 + (\beta_1 + \cdots + \beta_q)\sigma_a^2
\end{aligned}
$$

So <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此：</span></details>

$$
\sigma_a^2 = \frac{\omega}{1 - \alpha_1 - \dots - \alpha_p - \beta_1 - \dots - \beta_q}
$$

So in order for the variance, $\sigma_a^2$, to exist we need <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此为使方差 σ_a² 存在（且为正），需要：</span></details>

$$
\alpha_1 + \dots + \alpha_p + \beta_1 + \dots + \beta_q < 1
$$

- **Kurtosis** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">峰度。</span></details>

For GARCH (1,1), <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对于 GARCH(1, 1)：</span></details>

$$
m_4 = E(a_t^4) = \frac{3\omega^2(1 + \alpha_1 + \beta_1)}{(1 - \alpha_1 - \beta_1)(1 - \beta_1^2 - 2\alpha_1 \beta_1 - 3\alpha_1^2)}
$$

So $m_4$ exists only if $\beta_1^2 + 2\alpha_1 \beta_1 + 3\alpha_1^2 < 1$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此 m₄ 存在的条件为 β₁² + 2α₁β₁ + 3α₁² &lt; 1。</span></details>

And if may be shown that $k = m_4 / (m_2^2) - 3 > 0$, where $m_2 = \sigma_a^2$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">并且可以证明 k = m₄ / (m₂²) − 3 &gt; 0，其中 m₂ = σ_a²。（注：原文 "if" 疑似 "it" 笔误，教师红笔已划改为 "it"。）</span></details>

#### 6.5.2 Conditional Variance as Sum of Past Squared Innovations <details class="translation-details"><summary>中文译文</summary><span class="translation-body">6.5.2 条件方差表示为过去平方冲击之和。</span></details>

In operator notation, with $\beta(B) = 1 - \beta_1 B - \dots - \beta_q B^q$ and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">用算子记号表示，令 β(B) = 1 − β₁B − … − β_q B^q 以及……</span></details>

> [!tip] 本页教师手写批注（PDF p.6）
> - 顶部红笔补充下标范围：$\alpha_i \ge 0\ (i=1,2,\dots,p)$、$\beta_i \ge 0\ (i=1,2,\dots,q)$。
> - 方差推导红笔纠错与补充：将第 2 行 $\beta_{t-1}^2 \to a_{t-1}^2$、在 $\beta_1\sigma_{t-1}^2$ 后补入 $+\beta_2\sigma_{t-2}^2 + \cdots +$、将第 2–3 行的 $\alpha_q \to \alpha_p$ 与 $\beta_p \to \beta_q$；右侧注 `[for E(\varepsilon_t^2) = 1]`；下方补出移项 $\Rightarrow \sigma_a^2(1 - \alpha_1 - \alpha_2 - \cdots - \alpha_p - \beta_1 - \beta_2 - \cdots - \beta_q) = \omega$，以及特例：`For GARCH(1, 1), then` $\sigma_a^2 = \dfrac{\omega}{1 - \alpha_1 - \beta_1}$。
> - `Kurtosis` 段红笔将 `if` 改为 `it`；底部 $\beta(B)$ 下方红笔标注 `MA(q)`。

> [!example]- PDF 第 6 页原貌（含原有批注）
> ![[Chapter 6/附件/ch6-annotated-p06.png]]

---

## PDF p.7

$$
\begin{aligned}
\alpha(B) &= \alpha_1 B + \dots + \alpha_q B^p \\
\beta(B)\sigma_t^2 &= \omega + \alpha(B)a_t^2
\end{aligned}
$$

*(注：第一行原印刷误将 $\alpha_p$ 印作 $\alpha_q$，教师红笔已改为 $p$。)*

So $\sigma_t^2 = \omega + \psi(B)a_t^2$, where $\psi(B) = \alpha(B) / \beta(B)$. Provided $\beta(B)$ is invertible. So <details class="translation-details"><summary>中文译文</summary><span class="translation-body">于是 σ_t² = ω + ψ(B)a_t²（严格常数项应为 ω/β(1)），其中 ψ(B) = α(B)/β(B)，前提是 β(B) 可逆。于是（注：原印刷求和下限误印为 i−1，教师红笔圈改为 i=1，此处照录原 PDF）：</span></details>

$$
\sigma_t^2 = \omega + \sum_{i-1}^{\infty} \psi_i a_{t-i}^2
$$

#### 6.5.3 ARMA Representation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">6.5.3 ARMA 表示。</span></details>

Setting $v_t = a_t^2 - \sigma_t^2$ then $v_t$ is white noise, that is, $E(v_t) = 0$ and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令 v_t = a_t² − σ_t²，则 v_t 为白噪声，即 E(v_t) = 0 且：</span></details>

$$
\operatorname{Cov}(v_t, v_s) = 0, \quad t \ne s.
$$

Substituting $\sigma_t^2 = a_t^2 - v_t$, in the model equation, obtain, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">将 σ_t² = a_t² − v_t 代入模型方程，得：</span></details>

$$
a_t^2 = \omega + \alpha_1 a_{t-1}^2 + \dots + \alpha_p a_{t-p}^2 + \beta_1(a_{t-1}^2 - v_{t-1}) + \dots + \beta_q(a_{t-q}^2 - v_{t-q}) + v_t
$$

So the GARCH(p, q) can be represented as an ARMA(p', q), where $p' = \max(p, q)$, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此 GARCH(p, q) 可以表示为 ARMA(p', q)，其中 p' = max(p, q)：</span></details>

$$
a_t^2 = \omega + \sum_{i=1}^{p'} (\alpha_i + \beta_i)a_{t-i}^2 + v_t - \sum_{i=1}^{q} \beta_i v_{t-i}
$$

where $\alpha_i = 0$ for $i > p$ and $\beta_i = 0$ for $i > q$. in other words, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中当 i &gt; p 时 α_i = 0，当 i &gt; q 时 β_i = 0。换言之（注：原文末行 "GRACH" 拼写笔误，教师红笔已标记对调为 GARCH，照录原文）：</span></details>

$a_t \sim \text{GRACH}(p, q)$ then $a_t^2 \sim \text{ARMA}(p', q)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">若 a_t ~ GARCH(p, q)，则 a_t² ~ ARMA(p', q)。</span></details>

> [!tip] 本页教师手写批注（PDF p.7）
> - 顶部红笔在 $\alpha(B)$ 处补写 $+\alpha_2 B^2 + \alpha_3 B^3 + \cdots$、将 $\alpha_q$ 圈改为 $\alpha_p$，右侧标注 `AR(p)`；
> - 中右红笔概念对照：`For stationary is AR(p)` / `invertible is MA(q)`；
> - 求和下限红笔圈改 $i-1 \to i=1$；末行红笔标正 `GRACH` → `GARCH`。

> [!example]- PDF 第 7 页原貌（含原有批注）
> ![[Chapter 6/附件/ch6-annotated-p07.png]]

---

## PDF p.8

#### 6.5.4 GARCH(1,1) Model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">6.5.4 GARCH(1, 1) 模型。</span></details>

The GARCH(1,1) is the most important GARCH model. Higher-order GARCH models tend to be overcomplicated and are rarely used in practice. So in the GARCH(1,1) case, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">GARCH(1, 1) 是最重要的 GARCH 模型。高阶 GARCH 模型往往过于复杂，实践中很少使用。因此对于 GARCH(1, 1)：</span></details>

$$
\begin{aligned}
a_t &= \varepsilon_t \sigma_t, \quad \varepsilon_t \sim \text{NID}(0, 1) \\
\sigma_t^2 &= \omega + \alpha_1 a_{t-1}^2 + \beta_1 \sigma_{t-1}^2
\end{aligned}
$$

where $\omega > 0$ and $\alpha_1, \beta_1 \ge 0.$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 ω &gt; 0 且 α₁, β₁ ≥ 0（教师红笔展开强调：α₁ ≥ 0 and β₁ ≥ 0）。</span></details>

**Example:** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">示例：</span></details>

The following plots are the SP500 and the Sydney All Ordinary (AO) indices during the period January 1993 to June 1997. There are 1136 observations for each series. The two series are of different magnitude, with the mean of AO series about 3.5 times that of SP500. So we multiply the SP500 series by 3.5 and plot it with SP500 in Fig. 1. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">下图为 1993 年 1 月至 1997 年 6 月期间标普 500（SP500）与悉尼普通股综合指数（Sydney All Ordinary，AO）的走势图，每条序列各有 1136 个观测值。两条序列量级不同，AO 序列的均值约为 SP500 的 3.5 倍，因此我们将 SP500 乘以 3.5 后与 AO 同绘于图 1 中。（注：原文末句误写为 "with SP500"，意为 "with AO"，照录。）</span></details>

**Fig.1 Time plot of SP500 (transformed) and All Ordinary series** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">图 1 变换后的 SP500 序列与 All Ordinary 序列时间序列图（横轴 Index 0–1136，纵轴 Data 1500–3000，详见下方原页扫描图）。</span></details>

> [!tip] 本页教师手写批注（PDF p.8）
> - 红箭头指向 GARCH(1, 1) 方程；红圈圈出 $\alpha_1, \beta_1 \ge 0$ 并在右侧展开写明 $\alpha_1 \ge 0 \text{ and } \beta_1 \ge 0$。

![[Chapter 6/附件/ch6-annotated-p08.png]]

---

## PDF p.9

**Fig. 2 Time plot of first differences of SP500 series** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">图 2 SP500 序列一阶差分时间序列图（纵轴 sp-diff 约 −20 至 20，横轴 Index 0–1136，详见下方原页扫描图）。</span></details>

**Fig. 3 Time plot of first differences of All Ord. series** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">图 3 All Ordinary 序列一阶差分时间序列图（纵轴 allo-diff 约 −50 至 50，横轴 Index 0–1136，详见下方原页扫描图）。</span></details>

The first differences of the two raw data series are shown in Figs 2 and 3 respectively. From the graph, it can be said that SP500 shows more conditional heteroscedasticity than AO. The SP graph shows small fluctuations at the beginning and larger deviations near the end. We then fit a GARCH(1,1) model to the individual return series, i.e. first difference of logs times by 100. Let $Z_t$ be the return series. We find $Z_t = a_t$ and $a_t$ is white noise. Let <details class="translation-details"><summary>中文译文</summary><span class="translation-body">两条原始数据序列的一阶差分分别如图 2 和图 3 所示。从图形可以看出，SP500 比 AO 表现出更明显的条件异方差性：SP500 图形前期波动较小，临近末尾处偏离幅度明显增大。接着我们对各自的收益率序列（即对数一阶差分乘以 100）拟合 GARCH(1, 1) 模型。设 Z_t 为收益率序列，我们发现 Z_t = a_t 且 a_t 为白噪声。令（注：下式原印刷漏印 a_t 上的平方，实应为 E(a_t² | F_{t−1}) = h_t = α₀ + α₁ a_{t−1}² + β₁ h_{t−1}，照录原文）：</span></details>

$$
E(a_t \mid F_{t-1}) = \alpha_0 + \alpha_1 a_{t-1}^2 + \beta_1 h_{t-1},
$$

*(本页无教师手写批注。)*

![[Chapter 6/附件/ch6-annotated-p09.png]]

---

## PDF p.10

and the estimation results using MLE for the two series are summarized in the table below, with values in brackets being standard errors. MLE method is used. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">两条序列采用极大似然估计（MLE）的结果汇总于下表，括号内数值为标准误（standard errors）。</span></details>

For convenience, $\alpha_1\ \&\ \beta_1$ will called ARCH and GARCH coefficients. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">为方便起见，α₁ 与 β₁ 分别称为 ARCH 系数与 GARCH 系数。（注：原文漏写 "be"，教师红笔已补插 "be"。）</span></details>

| | $\alpha_0$ | $\alpha_1$ | $\beta_1$ |
| :--- | :--- | :--- | :--- |
| SP500 | 0.009(0.0046) | 0.0483(0.012) | 0.9329(0.0177) |
| AO | 0.1875(0.167) | 0.0716(0.0299) | 0.5991(0.2875) |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头：系数 α₀、α₁、β₁；行名：SP500 与 AO（括号内为对应估计值的标准误）。</span></details>

- **Stationarity** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">平稳性（Stationarity）。</span></details>

In the normal case, $a_1 + \beta_1 < 1$ is sufficient for convariance stationary process. In the case of non-normal distributions, the condition is $\beta_1 + \alpha_1 \operatorname{Var}(\varepsilon_t) < 1$, where $\varepsilon_t$ are IID with mean zero and finite variance. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">在正态分布情形下，α₁ + β₁ &lt; 1 是协方差平稳过程的充分条件（注：原文误印作 a₁ 与 convariance，教师红笔已分别改为 α₁ 与 covariance）。在非正态分布情形下，该条件为 β₁ + α₁ Var(ε_t) &lt; 1，其中 ε_t 为零均值、有限方差的独立同分布（IID）序列。</span></details>

- **Volatility Forecasting** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">波动率预测（Volatility Forecasting）。</span></details>

Let $\sigma_t^2(l)$ denote the MMSW forecast of $\sigma_{t+l}^2$ given all the information up to and including time $t$. Then, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设 σ_t²(l) 表示在给定截至并包含时刻 t 的全部信息下，对 σ_{t+l}² 的最小均方误差（MMSE；原文拼作 MMSW，照录）预测。则：</span></details>

$$
\begin{aligned}
\sigma_t^2(1) &= \omega + \alpha_1 a_t^2 + \beta_1 \sigma_t^2 \\
\sigma_t^2(l) &= \omega + (\alpha_1 + \beta_1)\sigma_t^2(l-1).
\end{aligned}
$$

> [!tip] 本页教师手写批注（PDF p.10）
> - 红笔补正 3 处印刷笔误：`will called` → `will be called`；`a_1` → `α_1`；划去 `convariance` 中的 `n` → `covariance`。

> [!example]- PDF 第 10 页原貌（含原有批注）
> ![[Chapter 6/附件/ch6-annotated-p10.png]]

---

## PDF p.11

# AMA 515 Exercise 6 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AMA 515 练习 6（题目部分，PDF pp. 11–12；本页与第 12 页均无手写批注）。</span></details>

**1.** Let $X$ and $Y$ be two *rvs* with $E(Y) = \mu$ and $E(Y^2) < \infty$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1. 设 X 与 Y 为两个随机变量，满足 E(Y) = μ 且 E(Y²) &lt; ∞。</span></details>

- **(a)** Show that the constant $C$ that minimizes $E(Y - C)^2$ is $C = \mu$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(a) 证明使 E(Y − C)² 最小的常数 C 为 C = μ。</span></details>
- **(b)** Deduce that the *rv* $f(X)$ that minimizes $E\Big[(Y - f(X))^2 \mid X\Big]$ is $f(X) = E(Y \mid X)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(b) 由此推出使条件期望 E[(Y − f(X))² | X] 最小的随机变量 f(X) 为 f(X) = E(Y | X)。</span></details>
- **(c)** Deduce that the *rv* $f(X)$ that minimizes $E(Y - f(X))^2$ is also $f(X) = E(Y \mid X)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(c) 由此推出使无条件期望 E(Y − f(X))² 最小的随机变量 f(X) 同样是 f(X) = E(Y | X)。</span></details>

**2.** Let $\{Z_t\}$ be a stationary solution of the $ARCH(1)$ process. Namely the process <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2. 设 {Z_t} 是 ARCH(1) 过程的平稳解，即如下过程：</span></details>

$$
\begin{aligned}
Z_t &= \sigma_t e_t, \qquad \{e_t\} \sim NID(0, 1) \\
\sigma_t^2 &= E\big(Z_t^2 \mid F_{t-1}\big) = \alpha_0 + \alpha_1 Z_{t-1}^2,
\end{aligned}
$$

where $F_{t-1}$ is the information set up to time $t-1$. Let $Y_t = Z_t^2 / \alpha_0$. Show that $Y_t$ satisfies the equation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 F_{t−1} 为截至 t−1 时刻的信息集。令 Y_t = Z_t² / α₀，证明 Y_t 满足方程：</span></details>

$$
Y_t = e_t^2(1 + \alpha_1 Y_{t-1}).
$$

**3.** Let $a_t$ be the $GARCH(1, 1)$ process. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3. 设 a_t 为 GARCH(1, 1) 过程：</span></details>

$$
\begin{aligned}
a_t &= \sqrt{h_t}\,\varepsilon_t, \quad \varepsilon_t \sim NID(0, 1). \\
h_t &= \omega + \alpha_1 a_{t-1}^2 + \beta_1 h_{t-1}.
\end{aligned}
$$

Show that $m_4 = \mathrm{E}(a_t^4) = \dfrac{3\omega^2(1 + \alpha_1 + \beta_1)}{(1 - \alpha_1 - \beta_1)(1 - \beta_1^2 - 2\alpha_1 \beta_1 - 3\alpha_1^2)}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">证明四阶矩 m₄ = E(a_t⁴) 等于上式右端表达式。</span></details>

**4.** Find the daily closing price of Hang Seng Index in 1980. Let the time series be $\{Y_t\}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4. 查找 1980 年恒生指数（Hang Seng Index）的每日收盘价，记该时间序列为 {Y_t}。</span></details>

- **(a)** Explain why $R_t = \log Y_t - \log Y_{t-1}$ can be regarded as the return of the stock index on day $t$ over day $t-1$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(a) 解释为什么 R_t = log Y_t − log Y_{t−1} 可视为第 t 日相对于第 t−1 日的股指收益率。</span></details>
- **(b)** Fit an appropriate $ARCH(p)$ model to the return series. (Hint: $p$ is not small) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(b) 对该收益率序列拟合一个合适的 ARCH(p) 模型。（提示：p 并不小。）</span></details>

**5.** Write down the maximum likelihood estimation equations for an $AR(2) - GARCH(1, 1)$ model, i.e. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">5. 写出 AR(2)–GARCH(1, 1) 模型的极大似然估计方程，即：</span></details>

$$
\begin{aligned}
Y_t &= \phi_1 Y_{t-1} + \phi_2 Y_{t-2} + a_t, \\
a_t &= \sigma_t e_t, \quad e_t \sim NID(0, 1), \\
\sigma_t^2 &= \omega + \alpha a_{t-1}^2 + \beta \sigma_{t-1}^2.
\end{aligned}
$$

> [!example]- PDF 第 11 页原貌（Exercise 6 第 1 页）
> ![[Chapter 6/附件/ch6-annotated-p11.png]]

---

## PDF p.12

**6.** For the $ARCH(1)$ process, $a_t = \sigma_t \varepsilon_t$, $\varepsilon_t \sim NID(0, 1)$, let $m_2$ and $m_4$ be the variance and kurtosis of $a_t$ respectively. Show that the standardized kurtosis $k = \dfrac{m_4}{m_2^2} - 3$ is greater than zero. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">6. 对于 ARCH(1) 过程 a_t = σ_t ε_t（ε_t ~ NID(0, 1)），设 m₂ 和 m₄ 分别为 a_t 的方差和四阶矩（原文称 kurtosis）。证明标准化峰度 k = m₄/m₂² − 3 大于零。</span></details>

**7.** For the model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">7. 对于如下模型：</span></details>

$$
Y_t - \mu = \phi(Y_{t-1} - \mu) + a_t, \quad a_t \sim wn(0, \sigma^2)
$$

Show that $\operatorname{var}(e_t(L)) = \sigma^2 \left(\dfrac{1 - \phi^{2L}}{1 - \phi^2}\right)$. Here $e_t(L)$ is the forecast error of the L-step ahead forecast. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">证明 var(e_t(L)) = σ² (1 − φ^(2L)) / (1 − φ²)，其中 e_t(L) 为向前 L 步预测的预测误差。</span></details>

**8.** Consider the stationary AR(1) model $X_t = \alpha X_{t-1} + a_t,\; a_t \sim wn(0, \sigma^2)$. Without using the GLP (general linear process) representation, show that the variance of the 2-step ahead forecast error of the time series is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">8. 考虑平稳 AR(1) 模型 X_t = α X_{t−1} + a_t（a_t ~ wn(0, σ²)）。不使用一般线性过程（GLP）表示，证明该时间序列向前 2 步预测误差的方差为：</span></details>

$$
\operatorname{var}\left(X_{t+2} - \hat{X}_t(2)\right) = (1 + \alpha^2)\sigma^2.
$$

**9.** Consider the ARCH(1) model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">9. 考虑如下 ARCH(1) 模型（注：原印刷题干存在两处笔误：ε_t ~ NID(0, σ²) 应为 NID(0, 1)，且 h_t = ω + α h_{t−1} 应为 ω + α r_{t−1}²；照录原文）：</span></details>

$$
r_t = \sqrt{h_t}\,\varepsilon_t, \quad \varepsilon_t \sim NID(0, \sigma^2), \quad h_t = \omega + \alpha h_{t-1}, \quad h_t = E(r_t^2 \mid F_{t-1}).
$$

Let $n_t = r_t^2 - h_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令 n_t = r_t² − h_t。</span></details>

- **(a)** Show that $n_t$ is a serially uncorrelated sequence. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(a) 证明 n_t 为序列不相关序列（serially uncorrelated sequence）。</span></details>
- **(b)** Show that $\operatorname{corr}(n_t, r_{t-k}^2) = 0$ for $k > 0$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(b) 证明对所有 k &gt; 0，corr(n_t, r_{t−k}²) = 0。</span></details>

> [!example]- PDF 第 12 页原貌（Exercise 6 第 2 页）
> ![[Chapter 6/附件/ch6-annotated-p12.png]]

---

## PDF p.13

# Outline Solution to Ex.6 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">练习 6 简要参考解答（PDF pp. 13–16）。</span></details>

**1.**
- **(a)**
  $$
  \begin{aligned}
  f(C) &= E(Y - C)^2 \\
  f'(C) &= -2E(Y - C) = 0 \\
  &\Rightarrow C = E(Y) = \mu
  \end{aligned}
  $$
- **(b)** Consider $E\Big[(Y - f(X))^2 \mid X = x\Big] = \omega$. Now we consider the conditional distribution $Y \mid x$. Thus from (a), the minimum of $\omega$ occurs at $E(Y \mid x)$. Thus the *rv* that minimizes $E\Big[(Y - f(X))^2 \mid X\Big]$ is $E(Y \mid X)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(b) 考虑 E[(Y − f(X))² | X = x] = ω。现考虑条件分布 Y | x，由 (a) 可知 ω 的最小值在 E(Y | x) 处取得。因此使 E[(Y − f(X))² | X] 最小的随机变量是 E(Y | X)。</span></details>
- **(c)**
  $$
  E\Big[(Y - E(Y \mid X))^2 \mid X = x\Big] \le E\Big[(Y - f(X))^2 \mid X = x\Big] \quad \text{for all } x \text{ by (b).}
  $$
  Thus, $E\Big[(Y - E(Y \mid X))^2 \mid X\Big] \le E\Big[(Y - f(X))^2 \mid X\Big]$. which implies $E(Y \mid X) = f(X)$ minimizes $E\big[Y - f(X)\big]^2$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由 (b)，对所有 x 均有上述不等式成立，从而 E[(Y − E(Y | X))² | X] ≤ E[(Y − f(X))² | X]（两边再取期望），即 f(X) = E(Y | X) 使 E[Y − f(X)]² 最小。</span></details>

**2.**
$$
\begin{aligned}
Z_t^2 &= e_t^2 \sigma_t^2 \\
&= e_t^2(\alpha_0 + \alpha_1 Z_{t-1}^2) \\
&\Leftrightarrow \alpha_0 Y_t = e_t^2(\alpha_0 + \alpha_0 \alpha_1 Y_{t-1}) \\
&\Leftrightarrow Y_t = e_t^2(1 + \alpha_1 Y_{t-1})
\end{aligned}
$$

**3.** Let $\sqrt{h_t} = \sigma_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3. 令 √h_t = σ_t：</span></details>

$$
\begin{aligned}
&\therefore a_t = \sigma_t \varepsilon_t, \quad \& \quad \varepsilon_t \sim N(0, 1) \\
&\therefore E(a_t^2) = E(\sigma_t^2) \\
&\& \quad E(a_t^4) = m_4 = 3E(\sigma_t^4).
\end{aligned}
$$

So <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此：</span></details>

$$
\begin{aligned}
m_4 &= E\,E(\varepsilon_t^4 \sigma_t^4 \mid F_{t-1}) \\
&= 3E\big[\omega + \alpha_1 a_{t-1}^2 + \beta_1 \sigma_{t-1}^2\big]^2 \\
&= 3E\big[\omega^2 + \alpha_1^2 a_{t-1}^4 + \beta_1^2 \sigma_{t-1}^4 + 2\omega \alpha_1 a_{t-1}^2 + 2\omega \beta_1 \sigma_{t-1}^2 + 2\alpha_1 \beta_1 a_{t-1}^2 \sigma_{t-1}^2\big] \\
&= 3\left[\omega^2 + \alpha_1^2 m_4 + \frac{\beta_1^2 m_4}{3} + \frac{2\omega^2 \alpha_1}{1 - \alpha_1 - \beta_1} + \frac{2\omega^2 \beta_1}{1 - \alpha_1 - \beta_1} + \frac{2\alpha_1 \beta_1 m_4}{3}\right]
\end{aligned}
$$

and result follows. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">整理求解 m₄ 即得结论。</span></details>

> [!tip] 本页教师手写批注（PDF p.13，红笔）
> - 1.(a)：在 `= 0` 上方写 `set`，右侧补写 `=> E(Y) - C = 0 => E(Y) = C`；
> - 2.：右侧补注 $Y_t = Z_t^2/\alpha_0$、$Y_{t-1} = Z_{t-1}^2/\alpha_0$；
> - 3.：右侧补注 $\sqrt{h_{t-1}} = \sigma_{t-1}, h_t = \sigma_t^2, h_t^2 = \sigma_t^4, h_{t-1} = \sigma_{t-1}^2$；在 $E(a_t^2)=E(\sigma_t^2)$ 旁顺手写了 $E(\varepsilon_t^4)=1$（**手写笔误**，此处应为 $E(\varepsilon_t^2)=1$，下一行求四阶矩才用 $E(\varepsilon_t^4)=3$）；底部补注代换关系 $E(\sigma_{t-1}^4) = m_4/3$ 与 $E(a_{t-1}^2) = E(\sigma_{t-1}^2) = \dfrac{\omega}{1 - \alpha_1 - \beta_1}$。

> [!example]- PDF 第 13 页原貌（含原有批注）
> ![[Chapter 6/附件/ch6-annotated-p13.png]]

---

## PDF p.14

**4.** (a) $\log(1 + x) \approx x$ and put $x = \dfrac{Y_t - Y_{t-1}}{Y_{t-1}}$. *(原答案未提供 4(b) 解答。)* <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4. (a) 利用近似 log(1 + x) ≈ x，令 x = (Y_t − Y_{t−1}) / Y_{t−1} 即可。</span></details>

**5.** Let $\underset{\sim}{\theta} = (\phi_1, \phi_2, \omega, \alpha, \beta)'$. And contribution to likelihood at time $t$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">5. 设参数向量 θ = (φ₁, φ₂, ω, α, β)'，时刻 t 对似然函数的贡献为：</span></details>

$$
\begin{aligned}
L_t &= \frac{1}{\sqrt{2\pi \sigma_t^2}} \exp\left\{\frac{-(y_t - \phi_1 y_{t-1} - \phi_2 y_{t-2})^2}{2\sigma_t^2}\right\} \\
&= \frac{1}{\sqrt{2\pi h_t}} \exp\left\{\frac{-(y_t - \phi_1 y_{t-1} - \phi_2 y_{t-2})^2}{2h_t}\right\}
\end{aligned}
$$

if we put $h_t = \sigma_t^2$, $\varepsilon_t = y_t - \phi_1 y_{t-1} - \phi_2 y_{t-2}$. Then $\log L_t = \ell_t \propto -\dfrac{1}{2}\log h_t - \dfrac{1}{2}\dfrac{\varepsilon_t^2}{h_t}$. Then apart from a constant, $\sum \ell_t = \ell = -\dfrac{1}{2}\sum \log h_t + \dfrac{\varepsilon_t^2}{h_t}$. Use Newton's method by applying <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令 h_t = σ_t²、ε_t = y_t − φ₁ y_{t−1} − φ₂ y_{t−2}，则 log L_t = ℓ_t（略去常数）为 −½ log h_t − ½ ε_t²/h_t。略去常数后总对数似然为 ℓ = −½ ∑(log h_t + ε_t²/h_t)（注：原印刷式漏了括号，此处照录）。应用牛顿法迭代：</span></details>

$$
\underset{\sim}{\theta}_{n+1} = \underset{\sim}{\theta}_n - \left\{\frac{\partial^2 \ell}{\partial \underset{\sim}{\theta}\,\partial \underset{\sim}{\theta}'}^{-1} \cdot \frac{\partial \ell}{\partial \underset{\sim}{\theta}}\right\}_{\underset{\sim}{\theta}_n}.
$$

Note here $\dfrac{\partial^2 \ell}{\partial \underset{\sim}{\theta}\,\partial \underset{\sim}{\theta}'}^{-1}$ is a matrix. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意此处逆 Hessian（原文省去外括号）是一个矩阵。</span></details>

**6.** Note $m_4 = \dfrac{3\omega^2(1 + \alpha_1)}{(1 - \alpha_1)(1 - 3\alpha_1^2)}$ and $m_2 = \dfrac{\omega}{1 - \alpha_1}$. Then result follows by direct calculation. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">6. 注意 m₄ = 3ω²(1 + α₁) / [(1 − α₁)(1 − 3α₁²)] 且 m₂ = ω / (1 − α₁)，直接代入计算即得结论。</span></details>

> [!warning] 本页教师手写批注与算式疑点（PDF p.14）
> - **4.(a) 旁手写（深蓝/黑笔）**：写了 $e^{\ln(1+x)} = 1 + x \simeq x$（笔误：应为 $\ln(1+x)\approx x$），以及 $1 + x = 1 + \frac{Y_t - Y_{t-1}}{Y_{t-1}} = \frac{Y_t}{Y_{t-1}} = R_t$ 并标注 `rate of return`（严格而言 $Y_t/Y_{t-1} = 1+x$，而对数收益率 $R_t = \log(Y_t/Y_{t-1}) = \log(1+x) \approx x$）。
> - **6. 右侧手写（红笔+黑笔）**：手写代算 $\frac{m_4}{m_2^2} - 3$ 时**漏掉了分母 $m_2$ 的平方**（写成了除以 $\frac{\omega}{1-\alpha_1}$ 而得到 $\frac{3\omega(1+\alpha_1)}{1-3\alpha_1^2} - 3 > 0$ 及红框 $\frac{\omega(1+\alpha_1)}{1-3\alpha_1^2} > 1$，右侧扫描边缘有被裁切的 `since \omega >` / `and |\alpha_1| <`）。正确代入 $m_2^2 = \frac{\omega^2}{(1-\alpha_1)^2}$ 时 $\omega^2$ 恰好消去：$\frac{m_4}{m_2^2} - 3 = \frac{3(1-\alpha_1^2)}{1-3\alpha_1^2} - 3 = \frac{6\alpha_1^2}{1-3\alpha_1^2} > 0$。

> [!example]- PDF 第 14 页原貌（含原有批注）
> ![[Chapter 6/附件/ch6-annotated-p14.png]]

---

## PDF p.15

**7.** Let $X_t = Y_t - \mu$. Since the two random variables $X_t$ and $Y_t$ differ by only a constant, they have the same variances and covariances. Consider $X_t = \phi X_{t-1} + a_t$. Using the GLP (general linear process) representation $X_t = a_t + \phi a_{t-1} + \phi^2 a_{t-2} + \dots$, then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">7. 令 X_t = Y_t − μ。由于 X_t 与 Y_t 仅相差一个常数，二者具有相同的方差与协方差。考虑 X_t = φ X_{t−1} + a_t，利用一般线性过程（GLP）表示 X_t = a_t + φ a_{t−1} + φ² a_{t−2} + …，可得（注：原印刷式右端时间下标平移了 L，实应为 a_{t+L} + φ a_{t+L−1} + … + φ^(L−1) a_{t+1}，方差结论不变，照录原文）：</span></details>

$$
\begin{aligned}
X_{t+L} - \hat{X}_t(L) &= a_t + \phi a_{t-1} + \dots + \phi^{L-1} a_{t-(L-1)} \\
\operatorname{var}\left(X_{t+L} - \hat{X}_t(L)\right) &= \left(1 + \phi^2 + \phi^4 + \dots + \phi^{2L-2}\right)\sigma^2 = \sigma^2 \left(\frac{1 - \phi^{2L}}{1 - \phi^2}\right).
\end{aligned}
$$

**8.** $X_t = \alpha X_{t-1} + a_t$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">8. 原题第 12 页问的是向前 2 步预测误差方差 var(X_{t+2} − X̂_t(2)) = (1 + α²)σ²，但本页参考答案印成了向前 3 步预测误差方差（方法相同，将 3 换为 2 即得原题结果）；此处按原卷照录：</span></details>

$$
\begin{aligned}
\hat{X}_t(3) &= \alpha^3 X_t, \qquad \therefore X_{t+3} - \hat{X}_t(3) = X_{t+3} - \alpha^3 X_t. \\
\operatorname{Var}\left(X_{t+3} - \hat{X}_t(3)\right) &= \operatorname{var}(X_{t+3}) + \alpha^6 \operatorname{var}(X_t) - 2\alpha^3 \operatorname{cov}(X_{t+3}, X_t) \\
&= \operatorname{var} X_t (1 + \alpha^6) - 2\alpha^3 \alpha^3 \operatorname{var} X_t, \quad \text{by stationarity.} \\
&= \operatorname{var} X_t (1 - \alpha^6) \\
&= \frac{\sigma^2}{1 - \alpha^2}(1 - \alpha^6) \\
&= \sigma^2(1 + \alpha^2 + \alpha^4).
\end{aligned}
$$

*(本页无教师手写批注。)*

> [!example]- PDF 第 15 页原貌（Exercise 6 答案第 3 页）
> ![[Chapter 6/附件/ch6-annotated-p15.png]]

---

## PDF p.16

**9. (a)** $n_t = r_t^2 - h_t$. It is easy to see $E(n_t) = 0$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">9. (a) n_t = r_t² − h_t，易见 E(n_t) = 0。</span></details>

Thus $\operatorname{cov}(n_t, n_{t-k}) = E(n_t n_{t-k})$. Here we assume $k \ge 1$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">于是 cov(n_t, n_{t−k}) = E(n_t n_{t−k})。这里假定 k ≥ 1：</span></details>

$$
E(n_t n_{t-k}) = E\big[E(n_t n_{t-k} \mid F_{t-1})\big] = E\big[n_{t-k} E(n_t \mid F_{t-1})\big] \quad \text{as } k \ge 1.
$$

But $E(n_t \mid F_{t-1}) = 0$. Thus $E(n_t n_{t-k}) = 0$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">但 E(n_t | F_{t−1}) = 0，因此 E(n_t n_{t−k}) = 0。</span></details>

**(b)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(b) 由于 k &gt; 0 时 r_{t−k}² 关于信息集 F_{t−1} 可测，故可提出条件期望号，从而协方差与相关系数均为 0：</span></details>

$$
\begin{aligned}
\operatorname{cov}(n_t, r_{t-k}^2) &= E(n_t r_{t-k}^2) \\
&= E\big[E(n_t r_{t-k}^2 \mid F_{t-1})\big] \\
&= E\big[r_{t-k}^2 E(n_t \mid F_{t-1})\big], \quad \text{as } r_{t-k}^2 = h_{t-k} \varepsilon_{t-k}^2 \\
&= 0.
\end{aligned}
$$

*(本页无教师手写批注。)*

> [!example]- PDF 第 16 页原貌（Exercise 6 答案第 4 页）
> ![[Chapter 6/附件/ch6-annotated-p16.png]]
