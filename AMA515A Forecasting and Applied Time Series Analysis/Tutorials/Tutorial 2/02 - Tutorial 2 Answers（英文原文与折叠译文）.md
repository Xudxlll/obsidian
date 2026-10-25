---
course: "AMA515A Forecasting and Applied Time Series Analysis"
source: "Tutorial 2 Answers.pdf"
pages: 4
cssclasses: [ama-inline-translations]
---

# Tutorial 2 Answers

原始资料：[[附件/Tutorial 2 Answers.pdf|PDF 原件]] · [[00 - Tutorial 2 资料索引|资料索引]] · [[01 - Tutorial 2 题目（英文原文与折叠译文）|题目]]

本篇对应印刷答案。手写解答另见 [[03 - Ex 2 Q1（手写解答）]] 与 [[04 - Ex 2 Q2-Q4（手写解答）]]；不同版本的数值和结论分别保留。

## PDF p.1

Ans to Ex.2 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">练习 2 答案。</span></details>

1. (a) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1. (a) 趋势方程如下。</span></details>

$$
\hat y=22.955-1.832t+0.168t^2
$$

(b) DW=2.391, $d_L=0.812$, $d_U=1.579$, $4-d_L=3.188$, $4-d_U=2.421$, don't reject $H_0$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(b) DW=2.391，下界为 0.812、上界为 1.579，4 减下界为 3.188、4 减上界为 2.421；不拒绝原假设。</span></details>

(c) $b_1$ and $b_2$ are both significant, $R^2=0.72$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(c) b₁ 和 b₂ 均显著，决定系数为 0.72。</span></details>

(d) Theil's U=0.033 (good model), or 0.56 from another definition of U. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(d) Theil 的 U 为 0.033（模型良好）；若采用 U 的另一种定义，则为 0.56。</span></details>

(e) Model acceptable judging from (c) & (d) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(e) 根据 (c) 和 (d)，模型可以接受。</span></details>

(f) 27.591; interval= (22.54,32.63)=27.591 ± 1.5513(1.438)(2.262). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(f) 点预测为 27.591；区间为 (22.54, 32.63)，即 27.591 加减 1.5513×1.438×2.262。</span></details>

In the prediction interval, the correction factor is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">预测区间中的修正因子如下。</span></details>

$$
\left(1+x_0'(X'X)^{-1}x_0\right)^{1/2}=(1+1.0682)^{1/2}=1.438.
$$

Here $x_0'=(1\ 13\ 13^2)$ and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中，x₀ 的转置为 (1, 13, 13²)，设计矩阵 X 如下。</span></details>

$$
X=\begin{pmatrix}
1&1&1^2\\
1&2&2^2\\
\vdots&&\vdots\\
1&12&12^2
\end{pmatrix}.
$$

2. (a) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2. (a)</span></details>

$r=0.942$; t-statistics=7.9, reject $H_0$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">相关系数为 0.942；t 统计量为 7.9，拒绝原假设。</span></details>

Linear model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">线性模型。</span></details>

$$
\begin{aligned}
\mathrm{Sales}&=569.45+140.51*\mathrm{time}\\
&\quad(5.18)\qquad(7.94)
\end{aligned}
$$

$R_{\mathrm{adj}}^2=0.87$, F=63, DW=1.05(I), n=10 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">调整后的决定系数为 0.87，F=63，DW=1.05(I)，样本量为 10。</span></details>

Exponential model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">指数模型。</span></details>

$$
\begin{aligned}
\operatorname{Ln}(\mathrm{sales})&=6.56+0.11*\mathrm{time}\\
&\qquad\qquad(7.82)
\end{aligned}
$$

$R_{\mathrm{adj}}^2=0.87$, F=61.1, DW=1.12(I), n=10 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">调整后的决定系数为 0.87，F=61.1，DW=1.12(I)，样本量为 10。</span></details>

First difference model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">一阶差分模型。</span></details>

$$
\begin{aligned}
\mathrm{D(sales)}&=51.54+9.21*\mathrm{time}\\
&\qquad\qquad(0.42)
\end{aligned}
$$

$R_{\mathrm{adj}}^2=0.11$, F=0.18, DW=1.56(N), n=9 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">调整后的决定系数为 0.11，F=0.18，DW=1.56(N)，样本量为 9。</span></details>

Logistic model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">逻辑斯蒂模型（续下页）。</span></details>

<details><summary>本页原图（核对用）</summary>

![[附件/tut2-answers-p01.png]]

</details>

## PDF p.2

$$
\begin{aligned}
\mathrm{Logistic(sales)}&=1.14-0.34*\mathrm{time}\\
&\qquad\qquad(-8.08)
\end{aligned}
$$

$R_{\mathrm{adj}}^2=0.88$, F=65.44, DW=0.95(I), n=10 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">调整后的决定系数为 0.88，F=65.44，DW=0.95(I)，样本量为 10。</span></details>

Note: The answer depends on the choice of L. I don’t know the choice of the author in this case. But it is a regression of Log((L/y_t)-1) on t (time). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意：答案取决于 L 的选取。我不知道原作者在此选择的 L。但这里进行的是 Log((L/yₜ)−1) 对 t（时间）的回归。</span></details>

Quadratic model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">二次模型。</span></details>

$$
\mathrm{Sales}=713.29+68.59*\mathrm{time}+6.54*\mathrm{time}^2
$$

$R_{\mathrm{adj}}^2=0.87$, F=31.37, DW=1.16(I), n=10 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">调整后的决定系数为 0.87，F=31.37，DW=1.16(I)，样本量为 10。</span></details>

Cubic model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">三次模型。</span></details>

$$
\begin{aligned}
\mathrm{Sales}&=1293.06-445.64*\mathrm{time}+118.03*\mathrm{time}^2-6.76*\mathrm{time}^3\\
&\qquad\qquad(-3.61)\qquad\qquad(4.63)\qquad\qquad(-4.42)
\end{aligned}
$$

$R_{\mathrm{adj}}^2=0.96$, F=82.95, DW=2.42(N), n=10 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">调整后的决定系数为 0.96，F=82.95，DW=2.42(N)，样本量为 10。</span></details>

The following table is based on fitted values. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">下表基于拟合值计算。</span></details>

| Model | $R_{\mathrm{adj}}^2$ | RMSE | MAE | MAPE | Th. U |
| --- | ---: | ---: | ---: | ---: | ---: |
| Linear | .873(3) | 143.8(4) | 127.6(4) | 11.03(4) | 0.051(4) |
| Exponential | .870(5) | 140.2(3) | 127.8(5) | 9.98(3) | 0.05(3) |
| Logistic | 0.877(2) | 159.6(5) | 118.5(2) | 11.43(5) | 0.056(5) |
| Quadratic | 0.871(4) | 135.7(2) | 122.8(3) | 9.78(2) | 0.048(2) |
| Cubic | 0.965(1) | 65.7(1) | 46.6(1) | 4.36(1) | 0.023(1) |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">模型依次为线性、指数、逻辑斯蒂、二次和三次。指标依次为调整后的决定系数、均方根误差、平均绝对误差、平均绝对百分比误差和 Theil 的 U；括号保留原表排名。</span></details>

Thus Cubic model is the best model according to the ranking in various criteria. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，根据各项标准的排名，三次模型是最佳模型。</span></details>

Forecasts & intervals (Cubic): <details class="translation-details"><summary>中文译文</summary><span class="translation-body">预测值与区间（三次模型）。</span></details>

| Year | low | forecast | up |
| ---: | ---: | ---: | ---: |
| 91 | 1225.7 | 1679.1 | 2132.6 |
| 92 | 482.5 | 1265.6 | 2048.8 |
| 93 | -672.8 | 601.67 | 1876.1 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头：年份、下限、预测值、上限。</span></details>

<details><summary>本页原图（核对用）</summary>

![[附件/tut2-answers-p02.png]]

</details>

## PDF p.3

2 (b) Fitting the individual models is similar to 2(a). We have the following table similar to 2(a). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2 (b) 各模型的拟合方法与 2(a) 类似。可得到下面这张与 2(a) 类似的表。</span></details>

$r=0.906$, t-stat=8.27, reject $H_0$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">相关系数为 0.906，t 统计量为 8.27，拒绝原假设。</span></details>

| Model | $R_{\mathrm{adj}}^2$ | RMSE | MAE | MAPE | Th. U |
| --- | ---: | ---: | ---: | ---: | ---: |
| Linear | .81(2.5) | 307.9(4) | 235.4(3) | 3.97(4) | .026(4) |
| Fir. Diff | 0.07(5) | 334.4(5) | 237.3(5) | 3.96(3) | 0.028(5) |
| Logistic | 0.79(4) | 292.5(3) | 229.7(1) | 3.86(1) | 0.025(3) |
| Quadratic | 0.82(1) | 289.1(2) | 232.6(2) | 3.9(2) | 0.024(1.5) |
| Cubic | 0.81(2.5) | 285.4(1) | 236.5(4) | 4.03(5) | 0.024(1.5) |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">模型依次为线性、一阶差分、逻辑斯蒂、二次和三次。指标依次为调整后的决定系数、均方根误差、平均绝对误差、平均绝对百分比误差和 Theil 的 U；括号保留原表排名。</span></details>

Thus according to average rank, quadratic is the best model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，按平均排名，二次模型最佳。</span></details>

Forecasts and intervals (quadratic) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">预测值与区间（二次模型）。</span></details>

| Year | low | Forecast | up |
| ---: | ---: | ---: | ---: |
| 89 | 5954.15 | 6838.85 | 7723.56 |
| 90 | 5900.67 | 6878.75 | 7856.83 |
| 91 | 5813.53 | 6908.73 | 8003.93 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头：年份、下限、预测值、上限。</span></details>

<details><summary>本页原图（核对用）</summary>

![[附件/tut2-answers-p03.png]]

</details>

## PDF p.4

3. (a), (b), and (c) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3. (a)、(b) 和 (c)。</span></details>

SSE(SES)=57557, SSE(MA3)=61635, hence SES is better. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">SES 的误差平方和为 57557，MA3 的误差平方和为 61635，因此 SES 更好。</span></details>

> [!note] 版本核对
> [[04 - Ex 2 Q2-Q4（手写解答）#PDF p.5|手写版本第 5 页]]的 SES 数值及红字批注与此处不同。两个版本分别保留，不将手写批注合并成印刷答案的勘误。

4. We know <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4. 已知：</span></details>

$$
\operatorname{E}(S_T)=\operatorname{E}(x_T)-\frac{1-\alpha}{\alpha}b_2.\tag{1}
$$

Now <details class="translation-details"><summary>中文译文</summary><span class="translation-body">现在：</span></details>

$$
\begin{aligned}
S_T^{[2]}&=\alpha S_T+(1-\alpha)S_{T-1}^{[2]}\\
&=\alpha S_T+(1-\alpha)\left[\alpha S_{T-1}+(1-\alpha)S_{T-2}^{[2]}\right]\\
&=\cdots\\
&=\alpha\sum_{j=1}^{T-1}(1-\alpha)^j S_{T-j}+(1-\alpha)^T S_0^{[2]}
\end{aligned}
$$

Thus as T → infinity, the second term vanishes. Take expectation on both sides of above equation, and by (1) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，当 T 趋于无穷时，第二项消失。对上式两边取期望，并利用式 (1)，得到：</span></details>

$$
\begin{aligned}
\operatorname{E}(S_T^{[2]})
&=\alpha\sum_{j=0}^{\infty}(1-\alpha)^j\left[\operatorname{E}(x_{T-j})-\frac{1-\alpha}{\alpha}b_2\right],\\
&=\alpha\sum_{j=0}^{\infty}(1-\alpha)^j\left[b_1+b_2(T-j)-\frac{1-\alpha}{\alpha}b_2\right],\\
&=b_1+\alpha\sum_{j=0}^{\infty}(1-\alpha)^j b_2(T-j)-\frac{1-\alpha}{\alpha}b_2\\
&=b_1+b_2T-\frac{1-\alpha}{\alpha}b_2-\frac{1-\alpha}{\alpha}b_2\\
&=\operatorname{E}(S_T)-\frac{1-\alpha}{\alpha}b_2.
\end{aligned}
$$

because $\operatorname{E}(x_T)=b_1+b_2T$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因为 xₜ 的期望为 b₁+b₂T（原文下标为大写 T；此说明在原页位于第二行等式之后）。</span></details>

> [!note] 原文公式核对
> 上方有限递推展开的求和下限按原 PDF 保留为 $j=1$；后续期望式则从 $j=0$ 开始。原式下限疑有笔误，未在转录中静默修改。原解还使用了 $T\to\infty$ 忽略初始项；其结论应结合这一处理阅读。

<details><summary>本页原图（核对用）</summary>

![[附件/tut2-answers-p04.png]]

</details>
