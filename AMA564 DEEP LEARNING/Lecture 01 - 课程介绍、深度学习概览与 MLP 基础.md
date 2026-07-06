# Lecture 01 - 课程介绍、深度学习概览与 MLP 基础

> [!info] 资料来源
> - 课件：`AMA564_Deep Learning_Lecture1.pdf`
> - 本笔记只依据 PDF 整理，不使用字幕内容。
> - 页码均指 PDF 页码。内容按“课件要点 -> 中文解释 -> 公式/概念理解 -> 复习抓手”整理。

# 一、本讲的整体地图

对应 PDF：p.1-p.14

Lecture 1 有两个层次：前半部分说明课程会学什么，后半部分用深度学习（Deep Learning）的历史、应用和多层感知机（Multi-Layer Perceptron, MLP）公式，把后续课程的入口搭起来。

## 1.1 PDF 页码索引

| PDF 页码 | 内容 | 学习时要抓住什么 |
|---|---|---|
| p.1-p.2 | 课程标题、授课信息 | 课程名称、教师、上课时间与地点 |
| p.3-p.5 | 课程主题与 learning outcomes | 网络结构、学习算法、任务类型、PyTorch 实践、LLM 训练 |
| p.6-p.8 | 先修知识、参考书、评分 | 线代、微积分、概率统计、Python 是后续公式和代码的基础 |
| p.9-p.14 | 编程工具、PyTorch、tutorial/project | 本课用 Python 与 PyTorch，project 是应用课程内容的主线 |
| p.15-p.18 | AI 与深度学习定义 | 深度学习属于机器学习，核心是人工神经网络和表示学习 |
| p.19-p.41 | 深度学习发展史 | 感知机、AI winter、backprop、LeNet、ImageNet、VAE/GAN、ChatGPT |
| p.42-p.63 | 深度学习为什么现在爆发、能做什么 | 计算力、数据、开源工具，以及回归、视觉、语言、音频、科学等应用 |
| p.64-p.66 | 从线性回归到神经网络回归 | 为什么需要更有表达力的非参数模型 |
| p.67-p.77 | MLP 的数学定义与结构 | 线性层、激活函数、深度、宽度、参数量、全连接 |
| p.78-p.89 | 从浅层到深层、表达能力与效率 | 大网络、万能逼近、参数效率、下一讲引入 deep regression |

# 二、课程主线：深度学习到底学什么

## 2.1 两条主线：网络结构与学习算法

对应 PDF：p.3-p.5

课件把课程内容分成两类：一类是深度神经网络（Deep Neural Networks）的结构，另一类是学习算法（Learning Algorithms）。

网络结构包括：

- 多层感知机（Multi-Layer Perceptron, MLP）
- 卷积神经网络（Convolutional Neural Network, CNN）
- 循环神经网络（Recurrent Neural Network, RNN）
- Transformer

学习算法和任务包括：

- 回归（Regression）
- 分类（Classification）
- 生成学习（Generative Learning）
- 反向传播（Backpropagation）
- 优化算法（Optimization）
- 大语言模型训练（Training LLMs）

可以这样理解：网络结构决定模型“长什么样”，学习算法决定模型“怎么从数据中学”。例如 CNN 不是单纯因为名字高级才适合图像，而是因为卷积结构更适合捕捉局部空间模式；Transformer 适合语言和序列任务，是因为注意力机制（Attention）能处理不同位置之间的依赖关系。

本课的核心目标不是背模型名字，而是建立一个统一框架：

$$
\text{data} \rightarrow \text{model } f_\theta \rightarrow \text{loss} \rightarrow \text{optimization} \rightarrow \text{trained model}
$$

其中 $\theta$ 表示模型参数（Parameters）。深度学习训练，本质上就是通过优化算法找到一组好的参数。

## 2.2 课程安排背后的知识依赖

对应 PDF：p.4

课程从 MLP 开始，而不是直接从 CNN、GAN 或 LLM 开始，是因为 MLP 是最基本的神经网络形式。只要理解了 MLP 的函数复合、参数、激活函数和训练方式，后面很多模型都可以看成是在这个框架上加入结构假设。

课程顺序可以理解为：

| 阶段 | 主题 | 为什么放在这里 |
|---|---|---|
| Week 1-2 | MLP、回归、训练 | 先建立“神经网络是一类函数”的基本观念 |
| Week 3 | 反向传播与优化 | 训练神经网络必须会算梯度、会更新参数 |
| Week 4-5 | CNN 与计算机视觉 | 图像任务需要局部连接、卷积、池化等结构 |
| Week 6-7 | VAE、GAN 等生成模型 | 从预测任务进入生成任务 |
| Week 8-10 | RNN、Attention、Transformer、LLM | 从序列建模到现代大语言模型 |
| Week 12 | Fine-tuning 与 RLHF | 理解 LLM 如何适配任务和人类偏好 |
| Week 13 | Overall Review | 将模型、任务、训练算法串起来 |

这里有一个很重要的学习顺序：先知道模型能表示什么，再知道模型怎么训练，最后再看不同应用场景下为什么要换结构。

## 2.3 学完课程应具备的能力

对应 PDF：p.5

课件列出的 learning outcomes 可以拆成五种能力：

第一，能区分不同神经网络。看到 MLP、CNN、RNN、Transformer 时，要知道它们大致对应什么数据形态和任务。

第二，理解训练机制。最重要的是反向传播（Backpropagation）和优化技巧（Optimization Techniques）。如果不知道梯度怎么来，就很难真正理解模型为什么能学。

第三，能将模型用于不同任务：回归（Regression）、分类（Classification）、生成（Generation）、视觉（Vision）、自然语言处理（Natural Language Processing, NLP）。

第四，会用 Python 和 PyTorch 做实践。本课不是只讲数学定义，还要求能实现常规学习任务。

第五，知道构建大语言模型（Large Language Models, LLMs）的关键步骤。后续会接触 Transformer、预训练（Pretraining）、微调（Fine-tuning）、RLHF 等内容。

# 三、先修知识与工具

## 3.1 四个先修知识各自解决什么问题

对应 PDF：p.6

课件列出线性代数、微积分、概率统计和 Python。这四个基础分别对应深度学习的不同层面：

| 先修知识 | 在深度学习中的作用 |
|---|---|
| 线性代数（Linear Algebra） | 神经网络每一层通常是矩阵乘法和向量加法，例如 $Wx+b$ |
| 微积分（Calculus） | 梯度下降和反向传播依赖导数、偏导数、链式法则 |
| 概率统计（Probability and Statistics） | 风险、期望、条件均值、条件分位数、泛化误差都来自统计思想 |
| Python Basics | PyTorch、NumPy、数据处理和实验代码都依赖 Python |

可以这样记：

> 线性代数负责“算网络”，微积分负责“算梯度”，概率统计负责“定义学习目标”，Python 负责“把模型跑起来”。

## 3.2 参考书与课程评价

对应 PDF：p.7-p.8

参考书覆盖了四个方向：

- Goodfellow、Bengio、Courville 的 *Deep Learning*：偏深度学习理论与经典结构。
- Chollet 的 *Deep Learning with Python*：偏实践和 Keras/Python 视角。
- Mohri 等人的 *Foundations of Machine Learning*：偏机器学习理论基础。
- Hastie、Tibshirani、Friedman 的 *The Elements of Statistical Learning*：偏统计学习。
- Bubeck 的 *Convex Optimization: Algorithms and Complexity*：偏优化理论。

这也说明本课不是“只调包”，它同时涉及统计学习、优化算法和实际实现。

评分结构是：

| 项目 | 比例 |
|---|---|
| Assignments | 30% |
| Project | 20% |
| Examination | 50% |

从学习角度看，作业通常帮助理解公式和算法；project 负责把模型落到实际任务；考试检验概念、推导和方法选择。

## 3.3 Python 与 PyTorch

对应 PDF：p.9-p.14

课件明确说明本课使用 Python，并使用 PyTorch。PyTorch 的核心优势在于它适合写动态计算图（Dynamic Computational Graph）和自动求导（Automatic Differentiation），这对深度学习训练非常重要。

后续做深度学习项目时，通常会遇到这样的流程：

```python
import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(d_in, hidden),
    nn.ReLU(),
    nn.Linear(hidden, d_out),
)
```

这段代码背后的数学结构正是后面 p.68-p.77 讲的 MLP：线性变换、激活函数、再线性变换。

# 四、什么是深度学习

## 4.1 深度学习属于机器学习

对应 PDF：p.15-p.18

课件给出的定义是：深度学习（Deep Learning）是机器学习（Machine Learning）方法中的一个分支，基于人工神经网络（Artificial Neural Networks），并带有表示学习（Representation Learning）的思想。

这句话里有三个关键词：

1. 机器学习（Machine Learning）：模型不是由人手写规则，而是从数据中学习规律。
2. 人工神经网络（Artificial Neural Networks）：模型由很多简单计算单元连接而成。
3. 表示学习（Representation Learning）：模型不仅学习最终答案，还学习中间特征如何表示。

传统机器学习里，很多特征需要人工设计。例如图像分类时，人可能要先设计边缘、纹理、形状等特征。深度学习希望通过多层网络自动学出这些表示。

## 4.2 深度神经网络的直觉

对应 PDF：p.18

深度神经网络（Deep Neural Networks）可以理解为很多层可学习的函数叠在一起。前面的层学较低级的特征，后面的层学更抽象的特征。

例如在图像任务中：

- 前几层可能学边缘、颜色变化；
- 中间层可能学局部形状；
- 后面层可能学物体部件甚至整体类别。

这种“由低级到高级”的特征层次，是深度学习相对传统浅层模型的重要优势。

# 五、深度学习发展史

## 5.1 第一波：感知机与早期神经元

对应 PDF：p.19-p.25

课件把深度学习的发展称为三次浪潮。最早可以追溯到 1943 年的 McCulloch-Pitts 神经元（McCulloch-Pitts Neuron），它把神经元抽象成一个逻辑计算单元。

随后 Rosenblatt 提出了感知机（Perceptron）。感知机可以看成最简单的线性分类器：

$$
\hat{y}=\mathrm{sign}(w^Tx+b)
$$

如果数据能被一条直线或一个超平面分开，感知机就有机会学到分界面。但它的表达能力很有限。

课件特别提到 XOR 问题（XOR Problem）。XOR 的四个点无法用一条直线分开，因此线性分类器无法解决：

| 输入 $x_1$ | 输入 $x_2$ | XOR 输出 |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

这说明单层感知机只能处理线性可分（Linearly Separable）问题。Minsky 和 Papert 对感知机局限性的批评，导致神经网络研究进入第一次 AI winter。

## 5.2 第二波：反向传播重新点燃神经网络

对应 PDF：p.26-p.28

1986 年，Rumelhart、Hinton 和 Williams 发表关于通过反向传播误差学习表示的论文。课件称这一时期为 “The Backpropagandists Emerge”。

反向传播（Backpropagation）的意义不只是“会算导数”，而是让多层隐藏层的神经网络可以有效训练。多层网络可以学习非线性函数，而反向传播提供了更新每一层参数的实际方法。

核心直觉是：

1. 前向传播（Forward Pass）算出预测值和损失。
2. 从损失开始，利用链式法则（Chain Rule）逐层向前计算梯度。
3. 用梯度下降（Gradient Descent）更新权重。

所以 backprop 是从“模型有表达力”走向“模型可训练”的关键一步。

## 5.3 LeNet、第二次 AI winter 与 2006 年后的复兴

对应 PDF：p.29-p.31

1998 年，Yann LeCun 的 LeNet-5 用于 MNIST 手写数字识别，是卷积网络（Convolutional Network）的经典早期案例。它说明神经网络在特定任务上已经可以取得实用效果。

但 1990s 神经网络又遇到第二次 AI winter。课件指出原因之一是当时的网络方法无法很好扩展到更大问题，支持向量机（Support Vector Machine, SVM）等方法成为主流。

2006 年后，Hinton 等人通过深度信念网络（Deep Belief Nets）和无监督预训练（Unsupervised Pre-training）重新推动深层模型。这一阶段，“Deep Learning” 这个名称逐渐被广泛使用。

## 5.4 2012 ImageNet 突破与现代深度学习

对应 PDF：p.32-p.41

2012 年是深度学习爆发的标志性年份。ImageNet 数据集和 ILSVRC 比赛提供了大规模标注图像数据，GPU 计算让训练大模型变得可行。课件提到 2012 年 ImageNet 错误率出现明显下降，并且使用 GPU 的团队显著增加。

后续重要节点包括：

- 2013 年：变分自编码器（Variational Auto-encoder, VAE）。
- 2014 年：生成对抗网络（Generative Adversarial Networks, GAN）。
- 2018 年：Bengio、Hinton、LeCun 获得图灵奖。
- 2022 年：OpenAI ChatGPT 推动大语言模型进入大众视野。
- 2024 年：Nobel Prize 与深度学习相关主题被课件列入时间线。
- 2025 年：Turing Award 被列入时间线。

这段历史要抓住一个主线：深度学习不是突然出现的，而是经历了“早期想法 -> 表达能力受限 -> 训练方法突破 -> 数据和算力到位 -> 大规模应用爆发”的过程。

# 六、为什么深度学习现在变得重要

## 6.1 三个条件：算力、数据、开源工具

对应 PDF：p.42

课件把深度学习当下发展的原因概括为三点：

- 计算能力（Computing Power）：GPU、TPU 等硬件可以并行处理大量矩阵运算。
- 大数据（Big Data）：模型参数越多，通常越需要大量数据支撑。
- 开源工具（Open Source Tools）：PyTorch、TensorFlow 等工具降低了实现门槛。

深度学习模型通常包含大量矩阵乘法，GPU 擅长并行计算，因此硬件是关键推动力。仅有算法不够，如果没有大数据和计算资源，很多深层模型很难训练。

## 6.2 深度学习能做什么

对应 PDF：p.43-p.63

课件列了很多应用，可以按任务类型整理：

| 任务类型 | PDF 中的例子 | 核心理解 |
|---|---|---|
| 回归（Regression） | least squares、quantile、robust regression | 用模型预测连续数值 |
| 图像识别（Image Recognition） | vision、image recognition | 判断图像中有什么 |
| 生成模型（Generative Models） | sampled celebrities、StackGAN | 学习数据分布并生成新样本 |
| 图像翻译（Image Translation） | Liu et al. 2017 | 从一种图像域转换到另一种图像域 |
| 语音转文本（Speech to Text） | speech recognition | 将音频信号转成文字 |
| 自然语言处理（NLP） | ChatGPT | 理解、生成和变换语言 |
| 音频生成（Audio Generation） | WaveNet、Tacotron 2 | 生成语音或音乐信号 |
| 视觉 + 语言 | GPT-3、DALL-E | 连接图像与文本 |
| 基因组学（Genomics） | AlphaFold | 用深度模型处理生命科学问题 |
| 化学与物理 | 3D CNN 加速有限元模拟 | 用神经网络近似复杂科学计算 |
| 强化学习/AI | AlphaGo/Zero | 结合树搜索、深度强化学习、自我博弈 |
| 数据智能体 | LAMBDA | 将大模型用于数据分析和自动化 |

复习时不要只背例子，而要看它们的共同点：深度学习擅长从复杂、高维、非结构化数据中学习表示。

# 七、从线性回归走向神经网络回归

## 7.1 线性回归的表达能力

对应 PDF：p.64-p.65

课件用最小二乘回归（Least Squares Regression）引出深度非参数回归（Deep Nonparametric Regression）。

线性回归模型写作：

$$
f(x;\alpha,\beta)=\beta^Tx+\alpha
$$

给定数据 $(X_i,Y_i)$，目标是最小化平方误差：

$$
\min_{\alpha,\beta}\sum_{i=1}^n\left(Y_i-f(X_i;\alpha,\beta)\right)^2
$$

线性模型的优点是简单、高效、容易计算；缺点是表达能力有限，尤其面对非线性数据时，线性函数可能无法捕捉真实关系。

## 7.2 神经网络回归的表达能力

对应 PDF：p.66

如果用神经网络表示回归函数：

$$
f(x;\theta)
$$

训练目标变成：

$$
\min_{\theta}\sum_{i=1}^n\left(Y_i-f(X_i;\theta)\right)^2
$$

这里 $\theta$ 是所有网络参数。与线性回归相比，神经网络的函数形式不是预先写死的直线或多项式，而是通过层与层之间的组合来学习复杂函数。因此它更适合高维、非线性数据。

但代价是：参数很多，没有简单闭式解，需要训练。

# 八、MLP 的数学定义

## 8.1 MLP 是复合函数

对应 PDF：p.67-p.69

多层感知机（Multi-Layer Perceptron, MLP）的形式是：

$$
f_\theta(x)=\mathcal{A}_L\circ\sigma\circ\mathcal{A}_{L-1}\circ\sigma\circ\cdots\circ\sigma\circ\mathcal{A}_1(x),
\quad x\in\mathbb{R}^{d_0}
$$

其中每一层线性变换为：

$$
\mathcal{A}_i(x)=W_i x+b_i,\quad x\in\mathbb{R}^{d_{i-1}}
$$

参数维度为：

$$
W_i\in\mathbb{R}^{d_i\times d_{i-1}},\quad b_i\in\mathbb{R}^{d_i}
$$

激活函数（Activation Function）记为 $\sigma$，例如：

$$
\mathrm{ReLU}(x)=\max\{x,0\}
$$

$$
\mathrm{Sigmoid}(x)=\frac{1}{1+e^{-x}}
$$

这个公式的读法是：先用 $\mathcal{A}_1$ 做线性变换，再用 $\sigma$ 加入非线性；然后继续下一层。没有激活函数的话，多层线性变换仍然等价于一个线性变换，模型不会真正变深。

## 8.2 深度、宽度、参数量

对应 PDF：p.69

课件定义：

- 输入层是第 0 层（0-th layer）。
- 输出层是最后一层。
- 中间层是隐藏层（Hidden Layers）。
- 网络深度（Depth）通常与隐藏层数量有关。
- 第 $i$ 层宽度（Width）是 $d_i$。
- 网络宽度可以取隐藏层宽度的最大值：

$$
\max\{d_1,\ldots,d_{L-1}\}
$$

所有参数收集为：

$$
\theta=(W_1,b_1,\ldots,W_L,b_L)
$$

网络大小（Size）就是参数个数。对于每一层，参数数目是：

$$
d_i d_{i-1}+d_i
$$

其中 $d_i d_{i-1}$ 来自权重矩阵，$d_i$ 来自偏置向量。

## 8.3 激活函数与非饱和性

对应 PDF：p.70-p.71

课件区分饱和非线性（Saturated Nonlinearity）和非饱和非线性（Non-saturated Nonlinearity）。

饱和激活函数包括 Sigmoid 和 Tanh。它们在输入很大或很小时会变得很平，导数接近 0，训练深层网络时容易出现梯度消失（Vanishing Gradient）。

非饱和激活函数包括 ReLU 和 Leaky ReLU。ReLU 在正半轴导数为 1，训练中通常更稳定，因此课件说 ReLU 是多数问题的好默认选择。

$$
\mathrm{ReLU}(x)=
\begin{cases}
x,&x>0\\
0,&x\le 0
\end{cases}
$$

## 8.4 全连接与神经元类比

对应 PDF：p.71-p.73

课件用生物神经元和网络中的神经元作类比，但要注意：人工神经网络只是数学模型，不是对大脑的完整模拟。

MLP 中的层是全连接（Fully Connected）的：上一层的每个输出都连接到下一层的每个神经元。因此一层线性变换可以写成矩阵乘法：

$$
z^{(i)}=W_i h^{(i-1)}+b_i
$$

再经过激活函数：

$$
h^{(i)}=\sigma(z^{(i)})
$$

全连接结构表达能力强，但参数量也可能很大。后续 CNN 会通过局部连接和权重共享减少参数。

## 8.5 随机连接网络也可能有效

对应 PDF：p.74

课件提到 randomly wired neural networks：用 Watts-Strogatz 模型生成的随机连接网络，在 ImageNet 上也能达到接近 ResNet-50 的准确率。

这个例子说明：神经网络结构设计不只有“人工精心设计”一种可能。网络连接方式本身也可以被搜索、随机化或自动设计。这与后来的神经架构搜索（Neural Architecture Search, NAS）思想有关。

## 8.6 MLP 参数量例子

对应 PDF：p.75-p.77

课件给出一个 2-layer MLP：

- 输入维度：$4$
- 隐藏层宽度：$6$
- 输出维度：$2$

第一层参数：

$$
W_1\in\mathbb{R}^{6\times 4},\quad b_1\in\mathbb{R}^{6}
$$

参数个数为：

$$
6\times 4+6=30
$$

第二层参数：

$$
W_2\in\mathbb{R}^{2\times 6},\quad b_2\in\mathbb{R}^{2}
$$

参数个数为：

$$
2\times 6+2=14
$$

总参数量：

$$
30+14=44
$$

这个例子很重要，因为以后看 PyTorch 模型时，参数量就是按这个方式一层层加起来。

# 九、从浅层到深层：表达能力与效率

## 9.1 大网络是否一定过拟合

对应 PDF：p.78-p.80

课件从 shallow neural network 过渡到 deep neural networks，并提出问题：大的神经网络是否一定会过拟合（Overfit）？

直觉上，参数多的模型更容易把训练数据记住；但深度学习中，大模型在大数据上往往表现更好。关键不是“模型大不大”，而是：

- 数据量是否足够；
- 正则化和训练策略是否合适；
- 模型结构是否适合任务；
- 优化是否成功。

课件 p.80 的意思是：在更大规模数据上，更大的神经网络可能表现更好。

## 9.2 神经网络为什么有表达能力

对应 PDF：p.81-p.85

课件总结三句话：

1. 神经网络是复合函数（Composited Functions）。
2. 神经网络可以逼近其他函数。
3. 神经网络具有表达能力（Expressive）。

万能逼近定理（Universal Approximation Theorem）可以分成两个版本理解。

任意宽度版本（Arbitrary-width case）：

> 对定义在紧集（Compact Set）上的连续函数，只要浅层神经网络足够宽，就可以任意精度逼近它。

任意深度版本（Arbitrary-depth case）：

> 对定义在紧集上的连续函数，如果网络宽度固定但深度可以增加，也可以任意精度逼近它。

这里要注意：万能逼近定理只说明“存在某个网络能逼近”，不保证训练算法一定能找到它，也不说明需要多少数据和参数。

## 9.3 参数效率与网络架构

对应 PDF：p.86-p.88

课件引用了 accuracy、operations、parameter size 等指标。这里想表达的是：模型好不好不能只看准确率，也要看计算量和参数量。

参数效率（Parameter Efficiency）可以理解为：每个参数带来了多少有效性能提升。有些模型参数很多但利用不充分，有些架构能用更少参数达到更高准确率。

这为后续 CNN、ResNet、GoogLeNet 等结构埋下伏笔：深度学习不仅是“堆更多层”，更是设计更合适的结构，让参数以更有效的方式工作。

## 9.4 下一讲的入口

对应 PDF：p.89

本讲最后预告：下一讲会回答如何用深度神经网络做回归（Deep Neural Regression）。

因此 Lecture 1 的结论可以压缩成一句话：

> 深度学习用多层可训练函数来表示复杂关系；但要真正使用它，必须定义损失函数并用优化算法训练参数。

# 十、本讲复习抓手

## 10.1 必须会解释的概念

- 深度学习（Deep Learning）：基于人工神经网络和表示学习的机器学习分支。
- 表示学习（Representation Learning）：模型自动学习中间特征，而不完全依赖人工特征工程。
- 多层感知机（Multi-Layer Perceptron, MLP）：由线性变换和激活函数复合而成的前馈神经网络。
- 激活函数（Activation Function）：引入非线性，使多层网络不退化为单层线性模型。
- 深度（Depth）：网络层数或隐藏层数量。
- 宽度（Width）：某一层神经元个数。
- 参数（Parameters）：权重和偏置的集合。
- 万能逼近定理（Universal Approximation Theorem）：说明神经网络有逼近连续函数的表达能力。

## 10.2 关键公式

MLP：

$$
f_\theta(x)=\mathcal{A}_L\circ\sigma\circ\mathcal{A}_{L-1}\circ\sigma\circ\cdots\circ\sigma\circ\mathcal{A}_1(x)
$$

线性层：

$$
\mathcal{A}_i(x)=W_i x+b_i
$$

ReLU：

$$
\mathrm{ReLU}(x)=\max\{x,0\}
$$

Sigmoid：

$$
\mathrm{Sigmoid}(x)=\frac{1}{1+e^{-x}}
$$

参数量：

$$
\#\theta=\sum_{i=1}^{L}(d_i d_{i-1}+d_i)
$$
