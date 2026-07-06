# Lecture 03 - Backpropagation 与 Optimization Algorithms

> [!info] 资料来源
> - 课件：`AMA564_Deep Learning_Lecture3.pdf`
> - 本笔记只依据 PDF 整理，不使用字幕内容。
> - 本讲核心问题：如何精确计算神经网络梯度？样本很多时如何训练？常见优化算法之间有什么关系？

# 一、本讲的整体地图

## 1.1 PDF 页码索引

| PDF 页码 | 内容 | 学习重点 |
|---|---|---|
| p.1-p.5 | 回顾 deep nonparametric regression 与梯度问题 | 训练就是初始化、算梯度、走一步、重复 |
| p.6-p.12 | Backpropagation 与 chain rule | 反向传播用链式法则高效计算复合函数梯度 |
| p.13-p.19 | One-layer perceptron example | 用单层感知机具体推导 loss 对权重的导数 |
| p.20-p.21 | 优化算法列表 | SGD、Momentum、AdaGrad、ADAM |
| p.22-p.27 | Gradient Descent 与 L-smooth | 固定步长、下降条件、收敛思路 |
| p.28-p.34 | 大样本瓶颈与 SGD | 用随机梯度估计全梯度，步长需要衰减 |
| p.35-p.39 | SGD 的不足与 Momentum | 慢、局部最优、鞍点，动量用于加速和平滑 |
| p.40-p.43 | AdaGrad、RMSProp、ADAM | 自适应学习率与动量结合 |
| p.44-p.47 | ADAM 的收敛故事 | ADAM 流行但理论曾有问题，后续论文修正理解 |
| p.48-p.50 | Minibatch、Epoch、动态学习率 | 实际训练通常用 minibatch 和学习率调度 |

# 二、从上一讲的问题出发

## 2.1 深度非参数回归的训练流程

对应 PDF：p.2-p.4

上一讲把神经网络回归写成经验风险最小化（Empirical Risk Minimization）：

$$
R_n(\theta)=\frac{1}{n}\sum_{i=1}^{n}
\left(Y_i-f(X_i;\theta)\right)^2
$$

更一般地，如果使用损失 $\phi$：

$$
R_n(\theta)=\frac{1}{n}\sum_{i=1}^{n}
\phi\left(Y_i-f(X_i;\theta)\right)
$$

训练步骤是：

1. 初始化参数 $\theta_0\in\mathbb{R}^s$；
2. 在当前参数 $\theta_t$ 处计算梯度；
3. 按步长 $\alpha_t$ 移动一步；
4. 重复直到停止。

平方损失下的梯度下降更新为：

$$
\theta_t=\theta_{t-1}
-\alpha_t
\left.
\frac{dR_n(\theta)}{d\theta}
\right|_{\theta=\theta_{t-1}}
$$

## 2.2 最核心的困难：网络输出对参数求导

对应 PDF：p.5

平方损失下：

$$
\frac{d}{d\theta}R_n(\theta)
=-\frac{2}{n}\sum_i
\left(Y_i-f(X_i;\theta)\right)
\frac{d}{d\theta}f(X_i;\theta)
$$

误差项 $Y_i-f(X_i;\theta)$ 容易计算，真正困难的是：

$$
\frac{d}{d\theta}f(X_i;\theta)
$$

因为 $f$ 是多层复合函数。反向传播（Backpropagation）就是为这个问题服务的：高效、系统地计算神经网络中所有参数对损失的梯度。

# 三、链式法则：反向传播的数学基础

## 3.1 简单链式法则

对应 PDF：p.6-p.9

如果：

$$
z=f(g(x))
$$

则：

$$
\frac{dz}{dx}=\frac{df}{dg}\frac{dg}{dx}
$$

课件用函数依赖箭头说明：如果 $z$ 依赖 $y$，$y$ 依赖 $x$，那么 $z$ 也间接依赖 $x$。例如：

$$
z(y)=2y^2
$$

则：

$$
\frac{\partial z}{\partial y}=4y
$$

神经网络是很多层复合函数，因此最早层参数对最终 loss 的影响必须通过链式法则一层层乘回来。

## 3.2 多路径链式法则

对应 PDF：p.10-p.11

如果：

$$
z(x)=z(y_1(x),y_2(x))
$$

则：

$$
\frac{dz}{dx}
=
\frac{\partial z}{\partial y_1}
\frac{dy_1}{dx}
+
\frac{\partial z}{\partial y_2}
\frac{dy_2}{dx}
$$

更一般地：

$$
z(x)=z(y_1(x),y_2(x),\ldots,y_n(x))
$$

则：

$$
\frac{dz}{dx}
=
\sum_{j=1}^{n}
\frac{\partial z}{\partial y_j}
\frac{dy_j}{dx}
$$

这对应神经网络中一个参数通过多条路径影响最终损失的情况。反向传播会把这些路径上的影响累加起来。

## 3.3 Forward pass 与 backward pass

对应 PDF：p.12

反向传播包含两个方向：

前向传播（Forward Pass）：

$$
x \rightarrow h_1 \rightarrow h_2 \rightarrow \cdots \rightarrow \hat{y} \rightarrow L
$$

给定输入，逐层计算隐藏层、输出和损失。

反向传播（Backward Pass）：

$$
L \rightarrow \hat{y} \rightarrow h_2 \rightarrow h_1 \rightarrow \theta
$$

从损失出发，逐层计算每个权重和偏置对损失的影响。

要点是：前向传播保存中间值，反向传播利用这些中间值和链式法则计算梯度。

# 四、单层感知机例子

## 4.1 模型与损失函数

对应 PDF：p.13-p.16

课件用单层感知机（One-layer Perceptron）说明反向传播。

输入为：

$$
x=(x_1,\ldots,x_n)
$$

线性部分为：

$$
z(w)=w_0+\sum_{i=1}^{n}w_i x_i
$$

输出使用 sigmoid：

$$
o(w)=\mathrm{sigmoid}(z(w))
=\frac{1}{1+e^{-z(w)}}
$$

损失函数为：

$$
L(w)=\frac{1}{2}(o(w)-y)^2
$$

为了统一偏置项，课件记：

$$
x_0=1
$$

这样 $w_0$ 也可以被看成普通权重。

## 4.2 对权重求导的链式分解

对应 PDF：p.16

目标是计算：

$$
\frac{\partial L}{\partial w_i}
$$

由于：

$$
w_i \rightarrow z(w) \rightarrow o(w) \rightarrow L(w)
$$

链式法则给出：

$$
\frac{\partial L}{\partial w_i}
=
\frac{dL}{do}
\frac{do}{dz}
\frac{\partial z}{\partial w_i}
$$

分别计算：

$$
\frac{dL}{do}
=
\frac{d}{do}\frac{1}{2}(o-y)^2
=o-y
$$

Sigmoid 的导数：

$$
\frac{do}{dz}
=
\frac{d}{dz}\frac{1}{1+e^{-z}}
=o(1-o)
$$

线性部分对 $w_i$ 的导数：

$$
\frac{\partial z}{\partial w_i}
=
\frac{\partial}{\partial w_i}
\left(w_0+\sum_{j=1}^{n}w_jx_j\right)
=x_i
$$

所以：

$$
\frac{\partial L}{\partial w_i}
=(o-y)o(1-o)x_i
$$

这就是一个最简单的 backprop 例子：每个局部导数都不复杂，复杂的是把它们按计算图顺序连起来。

## 4.3 数值例子的作用

对应 PDF：p.17-p.19

课件后面给出具体权重、输入、sigmoid 输出和 loss 的数值。学习时不必死记这些小数，更重要的是看清楚每个数字在计算图中的位置：

- $w_i$ 与 $x_i$ 相乘后进入求和；
- 求和得到 $z(w)$；
- $z(w)$ 经过 sigmoid 得到 $o(w)$；
- $o(w)$ 与真实值 $y$ 形成损失；
- 反向时，梯度沿相反方向逐层乘回去。

这和多层神经网络完全同构，只是多层网络有更多节点、更多路径和更多矩阵。

# 五、优化算法总览

## 5.1 本讲后半部分的四类算法

对应 PDF：p.20-p.21

课件列出四类优化方法：

1. 随机梯度下降（Stochastic Gradient Descent, SGD）
2. 动量加速（Momentum Acceleration）
3. AdaGrad
4. ADAM

它们都围绕同一个基本问题：

> 如何用梯度信息更快、更稳定地找到较低的 loss？

# 六、Gradient Descent

## 6.1 基本更新公式

对应 PDF：p.22-p.24

给定目标函数 $f(\theta)$，梯度下降（Gradient Descent, GD）从某个初始点 $\theta^0\in\mathbb{R}^s$ 出发，迭代：

$$
\theta^{k+1}=\theta^k-\alpha_k\nabla f(\theta^k)
$$

直到梯度范数足够小：

$$
\|\nabla f(\theta^{k+1})\|\le \epsilon
$$

其中 $\epsilon>0$ 是容忍度（Tolerance）。

两个关键点：

1. 计算当前梯度 $\nabla f(\theta^k)$；
2. 选择步长 $\alpha_k>0$，希望满足：

$$
f(\theta^{k+1})<f(\theta^k)
$$

## 6.2 L-smooth 条件

对应 PDF：p.25

课件引入 $L$-smooth function。若 $f$ 连续可微，且梯度满足 Lipschitz 连续：

$$
\|\nabla f(x)-\nabla f(y)\|\le L\|x-y\|
$$

则称 $f$ 是 $L$-smooth。

直观理解：$L$ 控制函数曲面的“弯曲程度”。$L$ 越大，函数变化越陡，步长越需要谨慎。

课件给出引理：

$$
f(y)\le f(x)+\nabla f(x)^T(y-x)+\frac{L}{2}\|y-x\|^2
$$

这个不等式提供了函数在 $x$ 附近的二次上界。

如果令：

$$
y=x-\alpha\nabla f(x)
$$

并选择：

$$
\alpha=\frac{1}{L}
$$

通常可以得到稳定下降。这就是为什么 $1/L$ 常被看作理论上的固定步长选择。

## 6.3 收敛证明思路

对应 PDF：p.26-p.27

课件给出 Gradient Descent 的收敛定理，并把证明留作 Assignment 1。提示包括：

1. 在第 $k$ 步应用 Lemma 3.1；
2. 对 $k=0,1,\ldots,T$ 求和；
3. 利用 $f$ 有下界（bounded from below）。

这个证明思路很典型：每一步都能让函数值下降一点，把所有下降量累加起来，如果函数不可能无限下降，就能推出梯度在某种意义上会变小。

# 七、大样本瓶颈与随机梯度

## 7.1 全梯度为什么昂贵

对应 PDF：p.28

经验风险通常是：

$$
f(\theta)=\frac{1}{n}\sum_{i=1}^{n} f_i(\theta)
$$

全梯度为：

$$
\nabla f(\theta)=\frac{1}{n}\sum_{i=1}^{n}\nabla f_i(\theta)
$$

如果样本量 $n$ 很大，每一步 GD 都要遍历全部样本，计算非常昂贵。

课件的问题是：如何克服？提示是：如何估计随机变量的期望。

## 7.2 随机梯度的思想

对应 PDF：p.29-p.30

随机梯度（Stochastic Gradient）用一个随机估计代替全梯度。最常见做法是随机抽一个样本索引 $\xi$：

$$
\xi\sim \mathrm{Uniform}\{1,\ldots,n\}
$$

然后用：

$$
g(\theta,\xi)=\nabla f_\xi(\theta)
$$

作为全梯度的估计。它满足无偏性：

$$
\mathbb{E}_\xi[g(\theta,\xi)]=\nabla f(\theta)
$$

直觉上，每一步不看全部数据，只看一个随机样本或一小批样本。单步方向有噪声，但计算便宜，可以走更多步。

## 7.3 SGD 更新公式

对应 PDF：p.31-p.34

随机梯度下降（Stochastic Gradient Descent, SGD）更新为：

$$
\theta^{k+1}=\theta^k-\alpha_k g(\theta^k,\xi_k)
$$

关键点：

1. 如何采样来计算 $g(\theta^k,\xi_k)$；
2. 如何选择步长 $\alpha_k$；
3. 如何评估解的质量。

课件提到常用质量指标是随机梯度范数的期望，例如：

$$
\mathbb{E}_\xi\|g(\theta^k,\xi)\|
$$

## 7.4 为什么 SGD 需要递减步长

对应 PDF：p.32-p.34

课件的 implication 是：固定步长会让估计停在一个误差球内，因此需要递减步长。

经典条件是：

$$
\sum_{t=0}^{\infty}\alpha_t=\infty,
\qquad
\sum_{t=0}^{\infty}\alpha_t^2<\infty
$$

例如：

$$
\alpha_t=\frac{1}{t+1}
$$

满足：

$$
\sum_{t=1}^{\infty}\frac{1}{t}=\infty
$$

以及：

$$
\sum_{t=1}^{\infty}\frac{1}{t^2}=\frac{\pi^2}{6}<\infty
$$

直觉是：早期步长要足够大，保证能持续探索；后期步长要变小，减少随机噪声带来的震荡。

# 八、SGD 的不足与 Momentum

## 8.1 SGD 的三个问题

对应 PDF：p.35-p.36

课件列出 SGD 的不足：

1. 收敛慢（Slow Convergence）。
2. 可能收敛到局部最优（Local Optimal Solution）。
3. 可能停在鞍点（Saddle Points）。

在深度学习中，损失曲面高维且非凸，梯度可能在某些方向很小、某些方向很大。普通 SGD 容易震荡或前进缓慢。

## 8.2 Momentum 的思想

对应 PDF：p.37-p.38

动量法（Momentum）引入速度变量 $v_k$，常见形式为：

$$
v_{k+1}=\gamma v_k+\alpha_k g(\theta^k,\xi_k)
$$

$$
\theta^{k+1}=\theta^k-v_{k+1}
$$

其中 $\gamma$ 是动量系数，课件指出实践中常用：

$$
\gamma=0.9
$$

Momentum 的直觉像“带惯性的下降”：如果连续几步梯度方向相似，速度会累积，从而加速；如果梯度方向来回震荡，动量会起到平滑作用。

## 8.3 Nesterov Momentum

对应 PDF：p.39

Nesterov Momentum 的核心区别是先“往前看一步”，再计算梯度。它的优势是可以减少 overshoot，也就是避免因为惯性太大冲过低点。

简单理解：

- 普通 Momentum：先看当前位置梯度，再按动量更新。
- Nesterov Momentum：先根据动量预估下一位置，再在预估位置看梯度。

# 九、自适应学习率：AdaGrad、RMSProp、ADAM

## 9.1 AdaGrad

对应 PDF：p.40

AdaGrad 的核心思想是：每个坐标根据历史梯度大小调整自己的学习率。

如果某个参数过去梯度一直很大，就降低它的学习率；如果某个参数梯度较小，就保留较大学习率。直觉上是对不同参数坐标做自适应缩放。

简化写法：

$$
G_k=G_{k-1}+g_k\odot g_k
$$

$$
\theta_{k+1}
=
\theta_k-\frac{\alpha}{\sqrt{G_k}+\epsilon}\odot g_k
$$

问题是 $G_k$ 会不断累积，导致学习率很快趋近于 0。

## 9.2 RMSProp

对应 PDF：p.41

RMSProp 可以看成 Leaky AdaGrad。它不把所有历史梯度等权累加，而是使用指数衰减平均：

$$
G_k=\beta G_{k-1}+(1-\beta)g_k\odot g_k
$$

这样旧梯度影响会逐渐衰减，学习率不至于像 AdaGrad 那样快速变成接近 0。

## 9.3 ADAM

对应 PDF：p.42-p.43

ADAM 的核心是把动量（Momentum）和自适应学习率（Adaptive Learning Rate）结合起来。

它维护一阶矩估计：

$$
m_k=\beta_1m_{k-1}+(1-\beta_1)g_k
$$

和二阶矩估计：

$$
v_k=\beta_2v_{k-1}+(1-\beta_2)g_k\odot g_k
$$

再用它们调整更新方向和步长。

原始 ADAM 论文推荐超参数：

$$
\alpha=0.001,\quad
\beta_1=0.9,\quad
\beta_2=0.999,\quad
\epsilon=10^{-8}
$$

这些也是很多深度学习代码中的默认值。

## 9.4 ADAM 的理论故事

对应 PDF：p.44-p.47

课件指出 ADAM 是训练深度神经网络时非常流行的优化算法，但原始论文的收敛分析存在问题，ADAM 在某些设置下可能不收敛。

相关后续工作包括：

- Reddi、Kale、Kumar, *On the convergence of adam and beyond*, ICLR 2018。
- Shi、Li、Hong、Sun, *RMSprop converges with proper hyper-parameter*, ICLR 2020。
- Zhang、Chen、Shi、Sun、Luo, *Adam Can Converge Without Any Modification on Update Rules*, NeurIPS 2022。

这部分的学习意义是：算法在实践中好用，不代表理论分析简单；深度学习优化同时是工程问题和数学问题。

# 十、实际训练技巧

## 10.1 Minibatch

对应 PDF：p.48-p.49

实践中很少每次只用一个样本，也很少每次都用全部样本，而是使用小批量（Minibatch）。

如果 batch size 为 $p$，则随机抽取：

$$
\xi_{k,1},\ldots,\xi_{k,p}
$$

用平均梯度更新：

$$
g_k=
\frac{1}{p}\sum_{j=1}^{p}
g(\theta^k,\xi_{k,j})
$$

$$
\theta^{k+1}=\theta^k-\alpha_k g_k
$$

Minibatch 的好处：

- 比单样本 SGD 方差更小；
- 比 full batch GD 计算更便宜；
- 适合 GPU 并行计算。

## 10.2 Epoch

对应 PDF：p.49

一个 epoch 表示训练过程大致看完整个训练集一次。如果样本量为 $n$，batch size 为 $p$，则每个 epoch 的更新次数通常为：

$$
n_E=\mathrm{ceil}(n/p)
$$

例如 $n=10000$，$p=128$，则每个 epoch 大约有：

$$
\mathrm{ceil}(10000/128)=79
$$

次参数更新。

## 10.3 动态学习率调整

对应 PDF：p.50

课件列出两种动态步长策略：

第一，按周期衰减：每 $K$ 个 epoch 将学习率乘以某个比例 $\gamma$：

$$
\alpha \leftarrow \gamma\alpha,\quad 0<\gamma<1
$$

第二，epoch doubling strategy：先用步长 $\alpha$ 跑 $K$ 个 epoch，再用 $\alpha/2$ 跑 $2K$ 个 epoch，之后继续延长训练并减小步长。

这些策略的共同目的：前期让模型快速下降，后期降低步长使训练更稳定。

# 十一、本讲复习抓手

## 11.1 一句话串联本讲

反向传播解决“如何精确高效算梯度”，SGD 和各种优化算法解决“如何在大数据和复杂损失曲面上更新参数”。

## 11.2 必须掌握的公式

平方损失梯度：

$$
\frac{d}{d\theta}R_n(\theta)
=-\frac{2}{n}\sum_i
\left(Y_i-f(X_i;\theta)\right)
\frac{d}{d\theta}f(X_i;\theta)
$$

链式法则：

$$
\frac{dz}{dx}=\frac{dz}{dy}\frac{dy}{dx}
$$

GD：

$$
\theta^{k+1}=\theta^k-\alpha_k\nabla f(\theta^k)
$$

SGD：

$$
\theta^{k+1}=\theta^k-\alpha_k g(\theta^k,\xi_k)
$$

Minibatch gradient：

$$
g_k=
\frac{1}{p}\sum_{j=1}^{p}
g(\theta^k,\xi_{k,j})
$$

ADAM 推荐超参数：

$$
\alpha=0.001,\quad
\beta_1=0.9,\quad
\beta_2=0.999,\quad
\epsilon=10^{-8}
$$

## 11.3 算法对比

| 算法 | 核心思想 | 优点 | 问题 |
|---|---|---|---|
| GD | 用全数据计算全梯度 | 方向稳定 | 大样本计算贵 |
| SGD | 用随机样本估计梯度 | 单步便宜 | 噪声大、可能震荡 |
| Momentum | 累积历史方向 | 加速、平滑震荡 | 可能 overshoot |
| Nesterov | 先预判再算梯度 | 减少 overshoot | 实现稍复杂 |
| AdaGrad | 每个坐标自适应学习率 | 适合稀疏梯度 | 学习率快速变小 |
| RMSProp | 对历史梯度做衰减平均 | 缓解 AdaGrad 学习率消失 | 需调超参数 |
| ADAM | Momentum + adaptive learning rate | 实践常用、收敛快 | 理论分析更复杂 |

## 11.4 易混点

反向传播（Backpropagation）不是一种优化算法，它只是计算梯度的方法。梯度算出来之后，还要用 GD、SGD、ADAM 等优化算法更新参数。

学习率（Learning Rate）不是越大越好。太大可能震荡或发散，太小训练太慢。

SGD 的“随机”不是随便乱走，而是用随机样本构造全梯度的无偏估计。

Minibatch 不是一个新的优化思想，而是实践中平衡计算效率和梯度稳定性的训练方式。
