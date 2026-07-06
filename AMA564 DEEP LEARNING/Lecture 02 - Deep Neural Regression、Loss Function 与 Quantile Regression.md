# Lecture 02 - Deep Neural Regression、Loss Function 与 Quantile Regression

> [!info] 资料来源
> - 课件：`AMA564_Deep Learning_Lecture2.pdf`
> - 本笔记只依据 PDF 整理，不使用字幕内容。
> - 本讲核心问题：神经网络如何做回归？损失函数（Loss Function）不同，模型到底会学到什么目标？

# 一、本讲的整体地图

## 1.1 PDF 页码索引

| PDF 页码 | 内容 | 学习重点 |
|---|---|---|
| p.1-p.6 | Lecture 1 复习：MLP 与万能逼近 | 神经网络是一类可表达复杂函数的函数族 |
| p.7-p.11 | Deep Neural Regression | 从线性回归闭式解过渡到神经网络经验风险最小化 |
| p.12-p.14 | Loss surface、grid/random search | 高维参数空间中暴力搜索效率低 |
| p.15-p.27 | 梯度、数值梯度、解析梯度 | 负梯度方向是最陡下降方向，解析梯度更快 |
| p.28-p.33 | 梯度下降训练流程与问题 | 初始化、步长、梯度计算、大样本问题 |
| p.34-p.48 | General loss 与 robust regression | 异常值会影响 LS，稳健损失降低大残差影响 |
| p.49-p.60 | LAD、conditional median、quantile regression | 不同损失对应不同统计目标：均值、中位数、分位数 |
| p.61 | TensorFlow Playground | 可视化理解神经网络拟合 |
| p.62-p.66 | 参数回归 vs 非参数回归 | 已知函数形式用参数模型，未知非线性关系用非参数模型 |

# 二、复习：MLP 是一类函数

## 2.1 MLP 的函数复合形式

对应 PDF：p.2-p.6

课件先复习多层感知机（Multi-Layer Perceptron, MLP）：

$$
f_{\theta}(x)=\mathcal{A}_L\circ\sigma\circ\mathcal{A}_{L-1}\circ\sigma\circ\cdots\circ\sigma\circ\mathcal{A}_1(x),
\quad x\in\mathbb{R}^{d_0}
$$

其中：

$$
\mathcal{A}_i(x)=W_i x+b_i,\quad W_i\in\mathbb{R}^{d_i\times d_{i-1}},\quad b_i\in\mathbb{R}^{d_i}
$$

$\sigma$ 是激活函数（Activation Function），例如：

$$
\mathrm{ReLU}(x)=\max\{x,0\},\qquad
\mathrm{Sigmoid}(x)=\frac{1}{1+e^{-x}}
$$

这组公式要理解成：神经网络不是一个单独函数，而是一整个由参数 $\theta$ 控制的函数族（Function Class）。训练前 $\theta$ 未定，模型还只是一个候选函数集合；训练后 $\theta$ 被确定，模型才变成具体函数。

## 2.2 万能逼近定理解决的是表达能力问题

对应 PDF：p.3-p.6

课件复习万能逼近定理（Universal Approximation Theorem）：

- 任意宽度版本：浅层网络如果足够宽，可以逼近紧集上的任意连续函数。
- 任意深度版本：固定宽度网络如果足够深，也可以逼近紧集上的任意连续函数。

它回答的是“神经网络有没有能力表示复杂函数”。但 Lecture 2 的重点是另一个问题：

> 如果神经网络有表达能力，我们如何从数据中找到合适的参数 $\theta$？

这就引出了经验风险最小化（Empirical Risk Minimization）和优化算法（Optimization Algorithms）。

# 三、从线性回归到深度非参数回归

## 3.1 线性回归为什么有闭式解

对应 PDF：p.7-p.9

给定数据：

$$
(X_i,Y_i),\quad i=1,\ldots,n
$$

最小二乘线性回归（Least Squares Linear Regression）寻找：

$$
f(x;\alpha,\beta)=\beta^Tx+\alpha
$$

使平方误差最小：

$$
\min_{\alpha,\beta}\sum_{i=1}^n\left(Y_i-f(X_i;\alpha,\beta)\right)^2
$$

令：

$$
Z_i^T=(1,X_i^T),\qquad \theta^T=(\alpha,\beta^T)
$$

则预测可以写成 $Z_i^T\theta$，目标函数为：

$$
\min_{\theta}\|Y-Z\theta\|_2^2
$$

在 $Z^TZ$ 可逆时，闭式解（Closed-form Solution）是：

$$
\theta^*=(Z^TZ)^{-1}Z^TY
$$

这说明线性回归有两个特点：函数形式简单，目标函数通常容易优化。

## 3.2 神经网络回归为什么没有简单闭式解

对应 PDF：p.10-p.11

神经网络回归把线性函数换成：

$$
f(x;\theta)
$$

目标变成：

$$
\min_{\theta\in\mathbb{R}^s}\sum_{i=1}^n\left(Y_i-f(X_i;\theta)\right)^2
$$

或写成经验风险（Empirical Risk）：

$$
R_n(\theta)=R_n(f(\cdot,\theta))
=\frac{1}{n}\sum_{i=1}^{n}\left(Y_i-f(X_i;\theta)\right)^2
$$

目标是：

$$
\min_{\theta\in\mathbb{R}^s}R_n(\theta)
$$

这里的难点是 $f(X_i;\theta)$ 是多层线性变换和非线性激活函数复合而成的，目标函数通常非凸（Non-convex），没有像线性回归那样简单的解析解。因此需要搜索参数，最常用的是梯度下降（Gradient Descent）及其变体。

## 3.3 “loss surface” 的含义

对应 PDF：p.12

损失曲面（Loss Surface）就是把参数 $\theta$ 映射到损失值 $R_n(\theta)$ 的地形图：

$$
\theta \mapsto R_n(\theta)
$$

如果参数只有两个维度，可以想象成山谷和山峰；训练模型就是沿着地形往低处走。真实神经网络可能有百万甚至十亿级参数，无法画出完整地形，但这个比喻帮助理解优化算法：我们不是直接知道最低点在哪，而是根据当前位置的局部信息逐步下降。

# 四、为什么不用网格搜索或随机搜索

## 4.1 Grid search 与 random search 的问题

对应 PDF：p.13-p.14

网格搜索（Grid Search）和随机搜索（Random Search）的思路很直接：尝试很多组参数，计算损失，保留最好的参数。

课件给出的 toy example 可以概括为：

```python
bestloss = float("inf")
for num in range(1000):
    theta = np.random.randn(9876) * 0.0001
    loss = R(X_train, Y_train, theta)
    if loss < bestloss:
        bestloss = loss
        best_theta = theta
```

这个循环做了三件事：

1. 随机猜一组参数；
2. 计算它在训练集上的 loss；
3. 如果更好，就更新 best solution。

问题是神经网络参数空间维度极高。假设每个参数只试 10 个值，$s$ 维参数空间就有 $10^s$ 种组合。维度稍大就不可承受，这就是维度灾难（Curse of Dimensionality）。

所以深度学习不能靠暴力枚举参数，而要利用梯度。

# 五、梯度：沿着最陡下降方向走

## 5.1 多维梯度的几何意义

对应 PDF：p.15-p.16

在多维空间中，梯度（Gradient）是由各个方向偏导数组成的向量：

$$
\nabla R_n(\theta)=
\left(
\frac{\partial R_n}{\partial \theta_1},
\ldots,
\frac{\partial R_n}{\partial \theta_s}
\right)^T
$$

课件强调两点：

- 任意方向上的斜率可以由该方向与梯度的点积得到。
- 最陡上升方向是梯度方向，最陡下降方向是负梯度方向。

因此如果想让损失下降，最自然的更新是：

$$
\theta_{t+1}=\theta_t-\alpha_t\nabla R_n(\theta_t)
$$

其中 $\alpha_t$ 是步长（Step Size）或学习率（Learning Rate）。

## 5.2 数值梯度为什么慢

对应 PDF：p.17-p.24

课件用 $W$ 作为待优化参数，逐个维度观察 loss 如何变化，并计算偏导数。这其实是数值梯度（Numerical Gradient）的思想。

对第 $j$ 个参数，可以用差分近似：

$$
\frac{\partial R}{\partial \theta_j}
\approx
\frac{R(\theta+h e_j)-R(\theta)}{h}
$$

其中 $e_j$ 是第 $j$ 个坐标方向的单位向量。

如果有 $s$ 个参数，就要至少额外计算 $s$ 次 loss。神经网络参数量巨大时，这会非常慢。因此课件说 numerical gradient is slow。

数值梯度的优点是容易写、概念直观；缺点是近似、慢。它常用于梯度检查（Gradient Check），而不是正式训练。

## 5.3 解析梯度与链式法则

对应 PDF：p.25-p.27

解析梯度（Analytic Gradient）用微积分直接推导导数，速度快且精确。对平方损失：

$$
R_n(\theta)=\frac{1}{n}\sum_{i=1}^{n}\left(Y_i-f(X_i;\theta)\right)^2
$$

梯度为：

$$
\frac{d}{d\theta}R_n(\theta)
=-\frac{2}{n}\sum_{i=1}^{n}
\left(Y_i-f(X_i;\theta)\right)
\frac{d}{d\theta}f(X_i;\theta)
$$

这里最关键的是：

$$
\frac{d}{d\theta}f(X_i;\theta)
$$

因为神经网络 $f$ 是复合函数，所以要用链式法则（Chain Rule）。Lecture 3 会专门讲反向传播如何高效完成这个计算。

## 5.4 数值梯度与解析梯度的实际关系

对应 PDF：p.27

课件总结：

- 数值梯度（Numerical Gradient）：近似、慢、容易写。
- 解析梯度（Analytic Gradient）：精确、快、容易写错。

实践中通常使用解析梯度训练，但会用数值梯度做梯度检查（Gradient Check），确认实现没有错误。

# 六、梯度下降训练过程

## 6.1 标准训练迭代

对应 PDF：p.28-p.32

课件将训练过程写成：

1. 随机初始化参数：

$$
\theta_0\in\mathbb{R}^s
$$

2. 对 $t=1,\ldots,T$，计算梯度：

$$
\left.\frac{dR_n(\theta)}{d\theta}\right|_{\theta=\theta_{t-1}}
$$

3. 设置步长：

$$
\alpha_t>0
$$

4. 更新参数：

$$
\theta_t=\theta_{t-1}
-\alpha_t
\left.
\frac{dR_n(\theta)}{d\theta}
\right|_{\theta=\theta_{t-1}}
$$

迭代 $T$ 次后，希望得到一个使 $R_n(\theta_T)$ 较小的参数。

## 6.2 训练时观察什么

对应 PDF：p.29-p.32

课件提到可以观察：

- 风险 $R_n(\theta_t)$ 如何随迭代变化；
- 神经网络预测 $f(\cdot;\theta_t)$ 如何随迭代变化。

这非常重要。训练不是只看最后一个数字，而是观察模型如何逐渐从随机函数变成能贴近数据的函数。如果 loss 不下降，可能是学习率太大、太小、初始化不好、梯度计算错误，或模型结构不合适。

## 6.3 训练中自然出现的四个问题

对应 PDF：p.33

课件列出四个问题：

1. 如何初始化 $\theta_0\in\mathbb{R}^s$？
2. 如何选择步长 $\alpha_t>0$？
3. 如何计算梯度，尤其是如何精确计算 $\frac{d}{d\theta}f(X_i;\theta)$？
4. 样本量 $n$ 很大时怎么办？

这四个问题分别对应后续主题：

- 初始化（Initialization）
- 学习率策略（Learning Rate Schedule）
- 反向传播（Backpropagation）
- 随机梯度下降（Stochastic Gradient Descent, SGD）和 minibatch

# 七、一般损失函数与异常值问题

## 7.1 为什么 least squares 会被异常值影响

对应 PDF：p.34-p.40

回归问题可以不只使用平方损失。课件先讨论异常值（Outliers）：

如果某个观测 $Y_j$ 被污染，那么残差：

$$
\left|Y_j-f(X_j;\theta)\right|
$$

可能很大。平方损失会把它变成：

$$
\left(Y_j-f(X_j;\theta)\right)^2
$$

大残差被平方后会更大，可能支配整个经验风险：

$$
R_n(\theta)=\frac{1}{n}\sum_{i=1}^{n}\left(Y_i-f(X_i;\theta)\right)^2
$$

于是模型会优先拟合异常点，导致整体回归曲线被拉偏。

## 7.2 平方损失对应 conditional mean

对应 PDF：p.38

课件指出，如果总体风险为：

$$
R(f)=\mathbb{E}\left[(Y-f(X))^2\right]
$$

那么对每个 $x$，最优函数满足：

$$
f^*(x)=\mathbb{E}[Y\mid X=x]
$$

也就是说，最小二乘回归（Least Squares Regression）的目标是条件均值（Conditional Mean）。

为什么？固定 $X=x$，要最小化：

$$
\mathbb{E}\left[(Y-a)^2\mid X=x\right]
$$

对 $a$ 求导：

$$
\frac{d}{da}\mathbb{E}\left[(Y-a)^2\mid X=x\right]
=
-2\mathbb{E}[Y-a\mid X=x]
$$

令其为 0：

$$
a=\mathbb{E}[Y\mid X=x]
$$

这解释了为什么 LS 对异常值敏感：均值本来就容易被极端值影响。

## 7.3 一般损失函数形式

对应 PDF：p.41-p.45

一般回归问题可以写作：

$$
\min_{\theta\in\mathbb{R}^s}
\frac{1}{n}\sum_{i=1}^{n}
L(Y_i,f(X_i;\theta))
$$

特别地，若损失只依赖残差：

$$
L(a,b)=\phi(a-b)
$$

则目标为：

$$
R_n(\theta)=\frac{1}{n}\sum_{i=1}^{n}
\phi\left(Y_i-f(X_i;\theta)\right)
$$

梯度为：

$$
\frac{d}{d\theta}R_n(\theta)
=-\frac{1}{n}\sum_{i=1}^{n}
\phi'\left(Y_i-f(X_i;\theta)\right)
\frac{d}{d\theta}f(X_i;\theta)
$$

不同的 $\phi$ 会给大残差不同权重，因此决定模型的统计目标和鲁棒性。

# 八、常见 robust loss

## 8.1 损失函数列表

对应 PDF：p.43-p.47

课件列出多种损失：

最小二乘（Least Squares, LS）：

$$
\phi(a)=a^2
$$

最小绝对偏差（Least Absolute Deviation, LAD）：

$$
\phi(a)=|a|
$$

Huber loss：

$$
\phi(a)=
\begin{cases}
\frac{a^2}{2},& |a|<\tau\\
\tau |a|-\frac{\tau^2}{2},& |a|\ge \tau
\end{cases}
$$

Cauchy loss：

$$
\phi(a)=\log(1+\kappa^2a^2)
$$

Tukey loss：

$$
\phi(a)=
\begin{cases}
\frac{t^2}{6}\left[1-\left(1-\frac{a^2}{t^2}\right)^3\right],& |a|<t\\
\frac{t^2}{6},& \text{otherwise}
\end{cases}
$$

## 8.2 这些损失如何降低异常值影响

对应 PDF：p.40-p.48

平方损失会让残差越大、惩罚增长越快。稳健损失函数（Robust Loss Function）通常会让大残差的边际影响变小。

可以这样理解：

| 损失 | 大残差影响 | 学习目标直觉 |
|---|---|---|
| LS | 非常大，因为平方增长 | 条件均值 |
| LAD | 线性增长，比平方温和 | 条件中位数 |
| Huber | 小残差像 LS，大残差像 LAD | 折中 |
| Cauchy | 大残差增长更慢 | 更强鲁棒性 |
| Tukey | 大残差惩罚封顶 | 对极端异常值影响很小 |

课件数值实验设置中，样本量 $n=128$，数据生成模型为：

$$
Y=f_0(X)+\eta
$$

误差 $\eta$ 包括 Cauchy 分布和正态混合分布：

$$
\eta\sim 0.8N(0,1)+0.2N(0,10^4)
$$

这种混合分布会产生少量非常大的噪声，正适合比较 robust regression 的效果。

# 九、LAD 与条件中位数

## 9.1 LAD 的风险

对应 PDF：p.49-p.53

最小绝对偏差（Least Absolute Deviation, LAD）的经验风险为：

$$
R_n(\theta)=\frac{1}{n}\sum_{i=1}^{n}
\left|Y_i-f(X_i;\theta)\right|
$$

总体风险为：

$$
R(f)=\mathbb{E}|Y-f(X)|
$$

课件给出结论：在适当条件下，对每个 $x$，

$$
f^*(x)=\mathrm{median}(Y\mid X=x)
$$

也就是说，LAD regression 学的是条件中位数（Conditional Median）。

## 9.2 为什么绝对损失对应中位数

对应 PDF：p.52

固定 $X=x$，令 $a=f(x)$，考虑：

$$
\mathbb{E}\left[|Y-a|\mid X=x\right]
$$

用条件分布函数（Conditional CDF）$F_{Y|X=x}$ 写成：

$$
\int_{-\infty}^{a}(a-y)dF_{Y|X=x}(y)
+
\int_{a}^{+\infty}(y-a)dF_{Y|X=x}(y)
$$

对 $a$ 求导：

$$
F_{Y|X=x}(a)-[1-F_{Y|X=x}(a)]
$$

令导数为 0：

$$
F_{Y|X=x}(a)=\frac{1}{2}
$$

所以：

$$
a=F^{-1}_{Y|X=x}\left(\frac{1}{2}\right)
$$

这就是条件中位数。

# 十、Quantile Regression

## 10.1 从中位数推广到任意分位数

对应 PDF：p.54-p.55

LAD 让最优解满足：

$$
F_{Y|X=x}(f^*(x))=\frac{1}{2}
$$

课件接着问：能否构造一个损失函数，让最优解满足：

$$
F_{Y|X=x}(f^*(x))=\tau,\quad \tau\in(0,1)
$$

答案是可以。此时：

$$
f^*(x)=F^{-1}_{Y|X=x}(\tau)
$$

这就是条件 $\tau$ 分位数（Conditional $\tau$-th Quantile）。

## 10.2 Check loss

对应 PDF：p.56-p.57

分位数回归使用 check loss：

$$
\rho_\tau(a)=\left(\tau-I(a<0)\right)a
$$

分段写法为：

$$
\rho_\tau(a)=
\begin{cases}
\tau a,& a>0\\
(1-\tau)(-a),& a\le 0
\end{cases}
$$

当 $\tau=0.5$ 时，正负残差权重相同，它等价于绝对损失的一半比例；当 $\tau=0.75$ 时，正残差和负残差的惩罚不对称，模型会学习更高分位数。

## 10.3 Deep Quantile Regression

对应 PDF：p.58-p.60

深度分位数回归（Deep Quantile Regression）将函数类设为神经网络：

$$
\mathcal{F}=\{f:f(x;\theta)\text{ is a neural network parameterized by }\theta\in\mathbb{R}^s\}
$$

给定 $\tau\in(0,1)$，训练目标为：

$$
\min_{\theta\in\mathbb{R}^s}
\frac{1}{n}\sum_{i=1}^{n}
\rho_\tau\left(Y_i-f(X_i;\theta)\right)
$$

总体风险为：

$$
R(f)=\mathbb{E}\rho_\tau(Y-f(X))
$$

课件结论是：最优函数 $f^*(x)$ 是 $Y|X=x$ 的条件 $\tau$ 分位数。

这说明一个很关键的思想：

> 神经网络提供函数表达能力，损失函数决定模型在统计意义上要学什么。

# 十一、参数回归与非参数回归

## 11.1 参数回归

对应 PDF：p.62-p.65

参数回归（Parametric Regression）预先假设函数形式，例如线性模型、广义线性模型、多项式回归或某些非线性模型。此时学习问题主要是估计有限维参数。

优点：

- 模型简单；
- 可解释性较强；
- 推断（Inference）较方便；
- 数据量较小时可能更稳定。

缺点：

- 如果函数形式设错（Model Misspecification），预测会很差。

## 11.2 非参数回归

对应 PDF：p.62-p.66

非参数回归（Nonparametric Regression）不预先固定具体函数形式，而是让函数形状由数据调整。神经网络回归就是一种灵活的数据驱动方法。

适用场景：

- 自变量与响应变量关系未知；
- 关系明显非线性；
- 数据维度高；
- 人工指定函数形式很困难。

但非参数模型通常需要更多数据、更复杂的训练，并且可解释性较弱。

# 十二、本讲复习抓手

## 12.1 一句话串联本讲

神经网络可以表达复杂函数；训练时要最小化经验风险；不同损失函数不仅影响鲁棒性，还决定模型学习的是条件均值、中位数还是分位数。

## 12.2 必须会区分的概念

- 经验风险（Empirical Risk）：训练样本上的平均损失。
- 损失曲面（Loss Surface）：参数到损失值的映射。
- 梯度（Gradient）：损失函数对参数的偏导向量。
- 数值梯度（Numerical Gradient）：用差分近似导数，慢但直观。
- 解析梯度（Analytic Gradient）：用微积分推导，快但容易实现错误。
- 稳健回归（Robust Regression）：通过损失函数降低异常值影响。
- 条件均值（Conditional Mean）：平方损失对应目标。
- 条件中位数（Conditional Median）：LAD 对应目标。
- 条件分位数（Conditional Quantile）：check loss 对应目标。

## 12.3 损失函数与目标速查

| 损失函数 | 公式 | 统计目标 |
|---|---|---|
| LS | $\phi(a)=a^2$ | $\mathbb{E}[Y\mid X=x]$ |
| LAD | $\phi(a)=|a|$ | $\mathrm{median}(Y\mid X=x)$ |
| Check loss | $\rho_\tau(a)=(\tau-I(a<0))a$ | $F^{-1}_{Y|X=x}(\tau)$ |
| Huber | 小残差平方，大残差线性 | 稳健折中 |
| Cauchy/Tukey | 大残差影响更小 | 更强鲁棒性 |
