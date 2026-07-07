> [!info] 资料来源
> - 课件：`AMA564_Deep Learning_Lecture6.pdf`
> - 本笔记只依据 PDF 整理。
> - 本讲核心问题：如何把神经网络用于分类？为什么分类训练通常使用 Softmax 和 Cross Entropy？

# 一、本讲的整体地图

## 1. PDF 页码索引

| PDF 页码 | 内容 | 学习重点 |
|---|---|---|
| p.1-p.5 | Classification overview 与 binary classification | 分类目标是让预测标签与真实标签一致 |
| p.6-p.10 | Logistic Regression | 估计条件概率，线性决策边界 |
| p.11-p.18 | Support Vector Machine | 最大间隔、support vectors、kernel trick |
| p.19-p.28 | Neural network binary classification | 0-1 loss 难优化，需要 surrogate loss |
| p.29-p.36 | Multi-class preprocessing 与 Softmax | one-hot label，输出维度等于类别数，Softmax 转概率 |
| p.37-p.41 | Likelihood、negative log likelihood、cross entropy | 交叉熵来自最大似然 |
| p.42-p.44 | Multi-class extension | 多分类中 Cross Entropy 的一般形式 |
| p.45-p.56 | MNIST example | 下载、标准化、查看数据、构建 LeNet-5、训练测试 |

# 二、分类问题的基本形式

## 1. 分类与回归的区别

对应 PDF：p.2-p.5

分类（Classification）的输出是离散类别，而回归（Regression）的输出通常是连续数值。课件举例包括 spam email classification、detection and classification。

二分类（Binary Classification）中，数据为：

$$
(X_i,Y_i),\quad i=1,\ldots,n
$$

并且样本独立同分布（i.i.d.）来自某个总体分布。标签可以写成：

$$
Y_i\in\{1,0\}
$$

也可以写成：

$$
Y_i\in\{1,-1\}
$$

目标是找一个分类器：

$$
h:\mathcal{X}\rightarrow\{1,0\}
$$

或者：

$$
h:\mathcal{X}\rightarrow\{1,-1\}
$$

使分类正确概率最大：

$$
\mathbb{P}(h(X)=Y)
$$

等价于让错误概率最小：

$$
\mathbb{P}(h(X)\ne Y)
$$

## 2. 常见分类方法

对应 PDF：p.5

课件列出三类方法：

- 逻辑回归（Logistic Regression）
- 支持向量机（Support Vector Machine, SVM）
- 深度神经网络（Deep Neural Networks）

它们都在做分类，但学习目标和模型形式不同。Logistic Regression 估计条件概率；SVM 找最大间隔超平面；神经网络通过多层非线性学习复杂边界。

# 三、Logistic Regression

## 1. 最小二乘也能估计条件概率

对应 PDF：p.7

课件提醒：二分类中如果 $Y\in\{0,1\}$，最小二乘的目标是条件均值：

$$
\mathbb{E}[Y\mid X]
$$

而：

$$
\mathbb{E}[Y\mid X]
=
1\cdot \mathbb{P}(Y=1\mid X)
+
0\cdot \mathbb{P}(Y=0\mid X)
=
\mathbb{P}(Y=1\mid X)
$$

所以分类中估计条件均值其实就是估计 $Y=1$ 的条件概率。

## 2. Logistic model

对应 PDF：p.8-p.10

逻辑回归（Logistic Regression）直接建模条件概率：

$$
p(x)=\mathbb{P}(Y=1\mid X=x)
$$

具体形式为：

$$
\mathbb{P}(Y=1\mid X=x)
=
\frac{\exp(w^Tx+b)}
{1+\exp(w^Tx+b)}
$$

如果：

$$
\mathbb{P}(Y=1\mid X=x)>0.5
$$

则预测 $Y=1$；否则预测 $Y=0$。

## 3. Logistic Regression 的局限

对应 PDF：p.10-p.11

逻辑回归的决策边界是：

$$
\{x:w^Tx+b=0\}
$$

这是线性边界。因此对于非线性可分的数据，logistic regression 可能不合适。

这也是为什么后面要用 kernel SVM 或 deep neural networks：它们可以产生非线性边界。

# 四、Support Vector Machine

## 1. 最大间隔思想

对应 PDF：p.12-p.16

支持向量机（Support Vector Machine, SVM）的目标是找到一个超平面，把不同类别样本分开，并让两类样本到超平面的距离最大。

直观上，能够分开样本的超平面可能有很多，但最大间隔（Maximum Margin）的超平面通常泛化更好。

SVM 的最优超平面只依赖一部分样本，这些样本叫支持向量（Support Vectors）。它们是离边界最近、真正决定边界位置的点。

## 2. Kernel Trick

对应 PDF：p.17-p.18

课件指出 SVM 本质上也是线性分类器，但可以通过核技巧（Kernel Trick）在变换后的特征空间中找线性超平面。

在高维特征空间中是线性的分类器，映射回原始输入空间后可能是非线性的边界。

可以这样理解：

$$
x \rightarrow \phi(x)
$$

在 $\phi(x)$ 空间中学习：

$$
w^T\phi(x)+b=0
$$

对应原空间中可能是一条曲线或更复杂边界。

# 五、神经网络做二分类

## 1. 0-1 loss 的困难

对应 PDF：p.19-p.22

二分类中，经验风险最小化可以写成：

$$
\min_{h\in\mathcal{H}}
\frac{1}{n}\sum_{i=1}^{n}
I(h(X_i)\ne Y_i)
$$

其中 $I(\cdot)$ 是指示函数（Indicator Function），也叫 0-1 loss：

$$
I(h(X_i)\ne Y_i)=
\begin{cases}
1,&h(X_i)\ne Y_i\\
0,&h(X_i)=Y_i
\end{cases}
$$

问题是 0-1 loss 不连续、不光滑，分类器 $h$ 也不是普通平滑函数。课件说这种 optimization problem is extremely hard。

神经网络训练需要梯度，而 0-1 loss 几乎无法直接用于梯度下降。

## 2. 用连续输出函数替代直接分类器

对应 PDF：p.23-p.25

神经网络先输出连续值：

$$
f(x;\theta)\in\mathbb{R}
$$

再通过阈值变成分类器：

$$
h(x;\theta)=\mathrm{sign}(f(x;\theta))
$$

规则是：

$$
f(x;\theta)>0 \Rightarrow \hat{Y}=+1
$$

$$
f(x;\theta)<0 \Rightarrow \hat{Y}=-1
$$

这样做的好处是：$f$ 是连续可微的神经网络输出，可以用 gradient descent 训练。

## 3. Surrogate loss

对应 PDF：p.26-p.28

为了替代 0-1 loss，使用替代损失（Surrogate Loss）。目标写成：

$$
\min_{\theta}
\frac{1}{n}\sum_{i=1}^{n}
\phi\left(Y_i f(X_i;\theta)\right)
$$

其中 $\phi$ 通常连续且递减。

为什么看 $Y_i f(X_i;\theta)$？因为若标签 $Y_i=+1$，希望 $f(X_i;\theta)$ 越大越好；若标签 $Y_i=-1$，希望 $f(X_i;\theta)$ 越小越好。二者都可以统一成希望 margin：

$$
Y_i f(X_i;\theta)
$$

越大越好。

课件列出几种 loss：

0-1 loss：

$$
\phi(yf)=I(yf<0)
$$

Exponential loss：

$$
\phi(yf)=\exp(-yf)
$$

Logistic loss：

$$
\phi(yf)=\log(1+\exp(-yf))
$$

Hinge loss：

$$
\phi(yf)=\max\{1-yf,0\}
$$

合适的 surrogate loss 可以导向一致分类器（Consistent Classifier）。

# 六、多分类的数据预处理

## 1. 为什么不能直接用类别数字大小

对应 PDF：p.29-p.30

多分类中，如果类别写成：

$$
Y\in\{0,1,2,3,\ldots\}
$$

数字大小可能引入虚假的顺序关系。比如 dog、cat、frog 没有天然大小顺序，但用 0、1、2 表示时，模型可能误以为 2 比 1 大。

因此多分类常用 one-hot encoding。

## 2. One-hot label

对应 PDF：p.31-p.32

二分类时，可以把 dog/cat 写成：

$$
\text{Dog}: (1,0),\qquad
\text{Cat}: (0,1)
$$

多分类 $K$ 类时，标签属于：

$$
Y_i\in\{0,1\}^{K}
$$

例如：

$$
\text{Dog}: (1,0,0,\ldots,0)
$$

$$
\text{Cat}: (0,1,0,\ldots,0)
$$

$$
\text{Tiger}: (0,0,\ldots,0,1)
$$

one-hot 的核心是：只有真实类别对应的位置为 1，其余为 0。

# 七、Softmax 输出概率

## 1. 神经网络输出维度

对应 PDF：p.33-p.34

如果有 $K$ 个类别，神经网络最后一层通常输出 $K$ 个实数：

$$
h(x;\theta)=(p_1,\ldots,p_K)\in\mathbb{R}^K
$$

但这些原始输出不一定在 $[0,1]$，也不一定加起来为 1。因此不能直接当概率。

## 2. Softmax function

对应 PDF：p.35-p.36

Softmax 把任意实数向量变成概率向量：

$$
\mathrm{Softmax}(p)_j
=
\frac{\exp(p_j)}
{\sum_{k=1}^{K}\exp(p_k)}
$$

输出满足：

$$
\mathrm{Softmax}(p)_j\in[0,1]
$$

且：

$$
\sum_{j=1}^{K}\mathrm{Softmax}(p)_j=1
$$

因此可以解释为每个类别的预测概率：

$$
\hat{b}_j\approx \mathbb{P}(Y=j\mid X=x)
$$

# 八、Cross Entropy 来自最大似然

## 1. Likelihood

对应 PDF：p.37-p.39

以二分类 one-hot 为例，标签：

$$
Y_i=(Y_{i1},Y_{i2})
$$

预测概率：

$$
\hat{b}=(\hat{b}_1,\hat{b}_2)
$$

对于一个样本，其 likelihood 可以写成：

$$
\hat{b}_1^{Y_{i1}}\hat{b}_2^{Y_{i2}}
$$

如果真实类别是第 1 类，则 $Y_{i1}=1,Y_{i2}=0$，likelihood 就是 $\hat{b}_1$；如果真实类别是第 2 类，则 likelihood 就是 $\hat{b}_2$。

log likelihood 为：

$$
Y_{i1}\log\hat{b}_1+Y_{i2}\log\hat{b}_2
$$

最大化 log likelihood 等价于最小化 negative log likelihood：

$$
-Y_{i1}\log\hat{b}_1-Y_{i2}\log\hat{b}_2
$$

## 2. Cross Entropy loss

对应 PDF：p.40-p.41

多分类的交叉熵（Cross Entropy）为：

$$
\mathrm{CELoss}(\hat{b},Y)
=
-\sum_{j=1}^{K}Y_j\log \hat{b}_j
$$

如果 $\hat{b}$ 来自 Softmax：

$$
\hat{b}_j=
\frac{\exp(h_j(x;\theta))}
{\sum_{k=1}^{K}\exp(h_k(x;\theta))}
$$

则经验风险为：

$$
\min_{\theta}
\frac{1}{n}\sum_{i=1}^{n}
\left(
-\sum_{j=1}^{K}Y_{ij}
\log
\frac{\exp(h_j(X_i;\theta))}
{\sum_{k=1}^{K}\exp(h_k(X_i;\theta))}
\right)
$$

Cross Entropy 的直觉：真实类别位置 $Y_j=1$，loss 就惩罚模型给真实类别的概率不够高。

## 3. 多分类扩展

对应 PDF：p.42-p.44

多分类中，输出大小就是类别数量。若有 $K$ 个类别，最后一层输出 $K$ 个 logits，Softmax 生成 $K$ 个概率，Cross Entropy 比较 one-hot label 和预测概率。

流程是：

$$
x \rightarrow h(x;\theta)\in\mathbb{R}^K
\rightarrow \mathrm{Softmax}(h)
\rightarrow \mathrm{CrossEntropy}
$$

# 九、MNIST 例子

## 1. 数据集与任务

对应 PDF：p.45-p.47

MNIST 是 $28\times 28$ 黑白手写数字图像数据集，标签为 0 到 9。

课件任务是：

- 使用 60,000 个 training data 训练分类器；
- 使用 10,000 个 testing data 测试分类器。

这是典型的 10-class image classification。

## 2. 数据预处理与查看

对应 PDF：p.48-p.52

课件提到下载 MNIST 并 normalize。标准化的目的是让输入数值范围更稳定，帮助网络训练。

对于黑白图像，输入可以写成：

$$
1\times 28\times 28
$$

如果 batch size 为 $B$，输入 batch 形状通常是：

$$
B\times 1\times 28\times 28
$$

## 3. 用 LeNet-5 做 MNIST 分类

对应 PDF：p.53-p.56

课件最后进入 Build the LeNet-5、Cross entropy loss function、Train and test the LeNet-5 on MNIST dataset。

典型训练流程是：

1. 定义 LeNet-5 模型；
2. 定义 Cross Entropy loss；
3. 选择 optimizer；
4. 在 training data 上迭代训练；
5. 在 testing data 上计算 accuracy。

PyTorch 中通常直接使用：

```python
loss_fn = torch.nn.CrossEntropyLoss()
```

需要注意：PyTorch 的 `CrossEntropyLoss` 通常接收 raw logits，不需要你手动先做 Softmax，因为它内部结合了 `LogSoftmax` 和 negative log likelihood。

# 十、本讲复习抓手

## 1. 必须掌握的概念

- 二分类（Binary Classification）：只有两个类别。
- 多分类（Multi-class Classification）：类别数大于 2。
- 0-1 loss：直接衡量分类错误，但不连续、不光滑，难以优化。
- 替代损失（Surrogate Loss）：用连续可优化的 loss 替代 0-1 loss。
- One-hot encoding：用长度为类别数的 0/1 向量表示类别。
- Softmax：把 logits 转成概率分布。
- Cross Entropy：分类中常用损失，来自 negative log likelihood。
- MNIST：手写数字分类基准数据集。

## 2. 关键公式

Logistic Regression：

$$
\mathbb{P}(Y=1\mid X=x)
=
\frac{\exp(w^Tx+b)}
{1+\exp(w^Tx+b)}
$$

Softmax：

$$
\hat{b}_j=
\frac{\exp(p_j)}
{\sum_{k=1}^{K}\exp(p_k)}
$$

Cross Entropy：

$$
\mathrm{CE}(Y,\hat{b})
=
-\sum_{j=1}^{K}Y_j\log \hat{b}_j
$$

Surrogate loss ERM：

$$
\min_{\theta}
\frac{1}{n}\sum_{i=1}^{n}
\phi\left(Y_i f(X_i;\theta)\right)
$$

## 3. 本讲一句话

分类不能直接靠 0-1 loss 做梯度训练，所以神经网络先输出连续 logits，再用 Softmax 转成概率，并用 Cross Entropy 作为可优化的分类损失。

# 十一、补充学习注释与复习路线

## 1. 本讲怎么读

这一讲对应 PDF：p.1-p.56。它把前面的回归问题转到分类问题（Classification），核心变化是：模型输出不再只是一个连续数值，而是要表示类别概率或类别决策。

建议按下面顺序读：

1. p.1-p.18：先理解二分类、Logistic Regression 和 SVM。
2. p.19-p.28：再看为什么神经网络分类不能直接优化 0-1 loss，而要用 surrogate loss。
3. p.29-p.44：重点读 one-hot、Softmax、likelihood 和 cross entropy 的关系。
4. p.45-p.56：用 MNIST 例子把数据预处理、模型输出和 loss 连起来。

分类里最重要的区分是“分数（Logit）”和“概率（Probability）”。神经网络最后一层通常先输出 logits：

$$
z=(z_1,\ldots,z_K)
$$

Softmax 把它们转成概率：

$$
p_k=\frac{e^{z_k}}{\sum_{j=1}^K e^{z_j}}
$$

这里每个 $p_k$ 都是正数，并且总和为 1，所以可以解释成模型认为样本属于第 $k$ 类的概率。

p.37-p.44 的 cross entropy 要和最大似然（Maximum Likelihood）一起理解。若真实标签是 one-hot 向量 $y$，预测概率是 $p$，多分类交叉熵为：

$$
\ell(y,p)=-\sum_{k=1}^K y_k\log p_k
$$

因为 one-hot 里只有真实类别位置为 1，所以它等价于：

$$
\ell=-\log p_{\text{true class}}
$$

也就是说，模型给真实类别的概率越小，惩罚越大。这个形式比 0-1 loss 更适合梯度优化，因为它不仅告诉模型“错了”，还告诉模型“错得有多不自信”。

本讲容易混淆三个概念：

- **Logistic Regression**：二分类概率模型，通常输出 $P(Y=1|X)$。
- **Softmax Regression**：多分类概率模型，是 Logistic Regression 的多类扩展。
- **Neural Network Classifier**：用深层网络产生 logits，再接 Softmax 和 Cross Entropy。

MNIST 例子对应 p.45-p.56。复习时要能把流程说完整：图像输入经过标准化（Normalization），CNN 提取特征，最后输出 10 个 logits，对应数字 0 到 9，再用 cross entropy 与真实 one-hot/类别标签比较。

## 2. 做题和复习时的检查清单

- 能不能用自己的话解释本讲的核心问题，而不是只背模型名称。
- 看到公式时，能不能说清每个符号代表什么、输入输出是什么、优化目标是什么。
- 能不能把本讲内容和前后讲联系起来：它继承了什么问题，又为下一讲解决什么问题。
- 能不能分清概念、公式、训练流程和应用场景四个层次。
- 遇到 PDF 中的图或代码时，先判断它是在说明结构、说明训练，还是说明实验结果。

## 3. 结构层级示例

下面这个小节专门用于统一结构编号：在 Obsidian 阅读时，一级结构用中文编号，二级结构用阿拉伯编号，三级结构用层级编号。后续如果继续扩写某个二级标题，可以使用类似 `1.1.1` 的形式继续细分。

### 1.1.1 如何继续扩展本讲

- 如果扩展概念解释，可以放在对应二级标题下面，先写直观含义，再写公式或例子。
- 如果扩展公式推导，先说明目标，再逐步解释每一步变形。
- 如果扩展复习题，可以把题目、解题思路、常见错误分开放，避免把结论堆在一起。
