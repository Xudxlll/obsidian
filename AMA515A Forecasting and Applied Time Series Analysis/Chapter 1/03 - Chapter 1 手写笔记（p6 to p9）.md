---
course: AMA515A Forecasting and Applied Time Series Analysis
source: Chapter 1 notes p6 to p9.pdf
pages: 12
cssclasses:
  - ama-inline-translations
---

> [!info] 手写与混合页面的阅读方式
> 本篇按源 PDF 的 12 页顺序完整嵌入原图，保留黑、蓝、红笔批注。手写部分采用原页保留，并提供可确认的标题译文及对应讲义页；PDF p.5—p.6 的印刷 OLS 正文另作逐段转录和翻译。未将全部手写逐字转录，也不把不同版本改成一套答案。
> [资料索引](<00 - Chapter 1 资料索引.md>) · [原 PDF](<附件/Chapter 1 notes p6 to p9.pdf>) · [正式讲义](<01 - Chapter 1（英文原文与折叠译文）.md>) · [前半手写笔记](<02 - Chapter 1 手写笔记（p1 to p5）.md>)

## PDF p.1

**1.5.1 Trend (depends on time) and seasonality (p6)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.5.1 趋势（取决于时间）与季节性，见讲义第 6 页。</span></details>

**1.5.2 Stochastic Trend (the time element is statistically variate)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.5.2 随机趋势（时间成分按统计方式变化）。原页括号内措辞依手写保留。</span></details>

对应正式讲义 PDF p.6：趋势、季节性、随机游走展开，以及均值和方差的旁注计算。

![手写笔记后半 PDF p.1](<附件/notes-b-p01.png>)

## PDF p.2

**Differencing operation (p6 bottom)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">差分运算，见讲义第 6 页底部。</span></details>

对应正式讲义 PDF p.6底部—p.7顶部：一阶差分、季节差分及均值、方差计算。原图中的 NID 标记保留；有关独立性标记的疑点见正式讲义转录篇 PDF p.7 的核对备注。

![手写笔记后半 PDF p.2](<附件/notes-b-p02.png>)

## PDF p.3

**1.5.3 Causal model and regression over time (p7)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.5.3 因果模型与对时间的回归，见讲义第 7 页。</span></details>

**Durbin-Watson Test statistic** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Durbin–Watson 检验统计量。</span></details>

对应正式讲义 PDF p.7：线性模型、误差假设及 DW 与一阶残差相关系数的近似关系推导。

![手写笔记后半 PDF p.3](<附件/notes-b-p03.png>)

## PDF p.4

对应正式讲义 PDF p.7—p.8顶部：DW 检验的 dL、dU、4−dU、4−dL 分区。原图保留全部区间、判定文字和蓝笔不确定区标记。

**Reject H₀ — positive correlation; Don’t reject H₀ — No evidence of autocorrelation; Reject H₀ — negative correlation; Inconclusive** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">图中：拒绝 H₀——正相关；不拒绝 H₀——没有自相关的证据；拒绝 H₀——负相关；Inconclusive——无法得出确定结论。</span></details>

![手写笔记后半 PDF p.4](<附件/notes-b-p04.png>)

## PDF p.5

对应正式讲义 PDF p.8。以下转录本页印刷正文和印刷公式；左侧手写求导标注及底部蓝笔等价写法以本页原图保留。

**Ordinary Least Squares Method (OLS)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">普通最小二乘法（OLS）。</span></details>

We will find a line of ‘best fit’, we will minimize the Sum of Squares Errors (SSE): <details class="translation-details"><summary>中文译文</summary><span class="translation-body">我们要寻找一条“最佳拟合”直线，为此将误差平方和（SSE）最小化：</span></details>

$$
Y_i=\alpha+\beta X_i+\varepsilon_i
\quad\Rightarrow\quad
\varepsilon_i=Y_i-\alpha-\beta X_i
$$

$$
\mathrm{SSE}=\sum_{i=1}^n\varepsilon_i^2
=\sum_{i=1}^n(Y_i-\alpha-\beta X_i)^2.
$$

This is minimized with respect to $\alpha$ and $\beta$ when <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对于 α 和 β，当下列条件满足时，平方和达到最小：</span></details>

$$
\sum_{i=1}^n(Y_i-\hat\alpha-\hat\beta X_i)(1)=0
\quad\Rightarrow\quad
\sum_{i=1}^nY_i=n\hat\alpha+\hat\beta\sum_{i=1}^nX_i.\tag{a}
$$

$$
\sum_{i=1}^n(Y_i-\hat\alpha-\hat\beta X_i)(X_i)=0
\quad\Rightarrow\quad
\sum_{i=1}^nX_iY_i=\hat\alpha\sum_{i=1}^nX_i+\hat\beta\sum_{i=1}^nX_i^2.\tag{b}
$$

Dividing (a) by n, we get $\bar Y=\hat\alpha+\hat\beta\bar X$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">把式（a）除以 n，得到 Ȳ = α̂ + β̂X̄。</span></details>

Multiplying (a) by $\dfrac{\sum_{i=1}^nX_i}{n}$ and subtracting from (b), <details class="translation-details"><summary>中文译文</summary><span class="translation-body">将式（a）乘以 Xᵢ 总和除以 n，再从式（b）中减去，得到：</span></details>

$$
\begin{aligned}
\sum_{i=1}^nX_iY_i
&=\hat\alpha\sum_{i=1}^nX_i+\hat\beta\sum_{i=1}^nX_i^2,\\
\frac{\left(\sum_{i=1}^nX_i\right)\left(\sum_{i=1}^nY_i\right)}{n}
&=\hat\alpha\sum_{i=1}^nX_i+\hat\beta\frac{\left(\sum_{i=1}^nX_i\right)^2}{n},\\
\sum_{i=1}^nX_iY_i-\frac{\left(\sum_{i=1}^nX_i\right)\left(\sum_{i=1}^nY_i\right)}{n}
&=\hat\beta\left[\sum_{i=1}^nX_i^2-\frac{\left(\sum_{i=1}^nX_i\right)^2}{n}\right].
\end{aligned}
$$

Therefore an estimator of $\beta$, the slope of the regression line, is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，回归线斜率 β 的一个估计量为：</span></details>

$$
\hat\beta=
\frac{\displaystyle\sum_{i=1}^nX_iY_i-\frac{\left(\sum_{i=1}^nX_i\right)\left(\sum_{i=1}^nY_i\right)}n}
{\displaystyle\sum_{i=1}^nX_i^2-\frac{\left(\sum_{i=1}^nX_i\right)^2}n}
=\frac{\sum_{i=1}^n(X_i-\bar X)(Y_i-\bar Y)}{\sum_{i=1}^n(X_i-\bar X)^2}.
$$

![手写笔记后半 PDF p.5 OLS 印刷正文与手写批注](<附件/notes-b-p05.png>)

## PDF p.6

接续前页。以下两段与回归方程为本页印刷正文；下方关于估计方差、t 检验和时间趋势的手写内容完整保留在原图中。

and an estimator of $\alpha$, the y-intercept, is $\hat\alpha=\bar Y-\hat\beta\bar X$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">纵轴截距 α 的一个估计量为 α̂ = Ȳ − β̂X̄。</span></details>

Hence the best-fit line (the regression of Y on X) is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，最佳拟合直线（Y 对 X 的回归）为：</span></details>

$$
\hat Y_i=\hat\alpha+\hat\beta X_i,\quad i=1,2,\ldots,n.
$$

**For the trend model, we have** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对于趋势模型，有以下结果（手写部分见原图）。</span></details>

对应正式讲义 PDF p.8：一般回归中的 X 替换为时间 t，以及斜率检验和 n−2 自由度的相关公式。

![手写笔记后半 PDF p.6](<附件/notes-b-p06.png>)

## PDF p.7

**Forecasting with linear trend (p.8)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">利用线性趋势预测，见讲义第 8 页。</span></details>

对应正式讲义 PDF p.8：点预测及拟合均值方差推导。红笔补充和底部关于方差估计的批注都保留原貌。

![手写笔记后半 PDF p.7](<附件/notes-b-p07.png>)

## PDF p.8

**In time series analysis, we need to forecast future values, hence prediction for Y is useful. (p.8)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">在时间序列分析中，我们需要预测未来值，因此对 Y 进行预测很有用。见讲义第 8 页。</span></details>

对应正式讲义 PDF p.8：未来观察值的预测误差方差，以及从一般因果回归替换为时间趋势模型的手写推导。

![手写笔记后半 PDF p.8](<附件/notes-b-p08.png>)

## PDF p.9

**(B) Curvilinear model — Tools for detection of nonlinearity (pg 8)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（B）曲线模型——识别非线性的工具，见讲义第 8 页。</span></details>

对应正式讲义 PDF p.8底部—p.9顶部：时间序列图、DW 检验、一阶差分图，以及二次趋势差分的展开。

![手写笔记后半 PDF p.9](<附件/notes-b-p09.png>)

## PDF p.10

**Other Model types: (pg 9) — (I) Polynomial** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其他模型类型（讲义第 9 页）——（I）多项式模型。</span></details>

对应正式讲义 PDF p.9：多项式模型的矩阵表示、参数向量、误差向量和设计矩阵。

![手写笔记后半 PDF p.10](<附件/notes-b-p10.png>)

## PDF p.11

**We are going to minimise S with respect to β. In matrix notation** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">我们要对 β 最小化 S，以下用矩阵表示。原页 S 的具体定义见图内公式。</span></details>

**(II) Exponential: Loglinear models** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（II）指数模型：对数线性模型。</span></details>

对应正式讲义 PDF p.9：最小二乘矩阵推导，以及指数模型的两种写法。保留红笔“see Lemma 2.2”的原始交叉引用，不额外推定其来源。

![手写笔记后半 PDF p.11](<附件/notes-b-p11.png>)

## PDF p.12

**(III) Logistic models** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（III）Logistic 模型。</span></details>

对应正式讲义 PDF p.9：先接续上一页的第三种对数线性形式，再给出 Logistic 模型和预测式。上下两部分的编号、正态分布标注及参数写法均按原图保留。

![手写笔记后半 PDF p.12](<附件/notes-b-p12.png>)
