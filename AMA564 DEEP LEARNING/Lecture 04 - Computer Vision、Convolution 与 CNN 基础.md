# Lecture 04 - Computer Vision、Convolution 与 CNN 基础

> [!info] 资料来源
> - 课件：`AMA564_Deep Learning_Lecture4.pdf`
> - 本笔记只依据 PDF 整理。
> - 页码均指 PDF 页码。笔记目标是帮助你按课件逐页学习，而不是只看摘要。

# 一、本讲的整体地图

## 1.1 PDF 页码索引

| PDF 页码 | 内容 | 学习重点 |
|---|---|---|
| p.1-p.10 | MLP、regression、backprop 复习 | 从前几讲的函数学习和训练方法过渡到视觉任务 |
| p.11-p.20 | Computer Vision tasks 与 ImageNet | 图像分类、检测、分割、风格迁移、caption、VQA、generation |
| p.21-p.29 | 用 Fully Connected DNN 做图像分类 | 图像张量被拉直会丢失空间结构，并且容易 overfit |
| p.30-p.39 | Convolution 与 convolution layer | filter 滑动、局部点积、activation map、多个 filter 形成新 tensor |
| p.40-p.55 | Spatial dimension、stride、padding | 输出尺寸公式、stride 不整除问题、zero padding 保持空间尺寸 |
| p.56-p.60 | Feature extraction | 卷积核可以提取边缘等局部特征 |
| p.61-p.70 | CNN、1 x 1 convolution、activation | CNN 是 convolution layer 与 activation function 的序列 |
| p.71-p.76 | Pooling | down sampling、translation invariance、max pooling、average pooling |
| p.77-p.82 | Receptive field 与 CNN 可视化 | 多层卷积扩大感受野，形成层级特征 |

# 二、从前几讲过渡到 Computer Vision

## 2.1 为什么先复习 MLP

对应 PDF：p.2-p.8

课件先复习多层感知机（Multi-Layer Perceptron, MLP）：

$$
f_\theta(x)=\mathcal{A}_L\circ\sigma\circ\mathcal{A}_{L-1}\circ\sigma\circ\cdots\circ\sigma\circ\mathcal{A}_1(x)
$$

其中：

$$
\mathcal{A}_i(x)=W_i x+b_i
$$

这个复习的目的不是重新讲 MLP，而是强调一个连接点：不管是回归、分类还是图像任务，深度学习都可以被看成用参数化函数 $f_\theta$ 学习输入和输出之间的关系。

前几讲的 deep nonparametric regression 是：

$$
\min_{\theta\in\mathbb{R}^s}
\sum_{i=1}^n
\left(Y_i-f(X_i;\theta)\right)^2
$$

如果使用一般损失函数，则是：

$$
\min_{\theta\in\mathbb{R}^s}
\sum_{i=1}^n
\phi\left(Y_i-f(X_i;\theta)\right)
$$

训练步骤仍然是：

1. 初始化参数 $\theta_0$；
2. 在当前参数处计算梯度；
3. 按步长 $\alpha_t$ 更新；
4. 重复直到停止。

因此进入计算机视觉（Computer Vision）后，变化的不是“训练框架”，而是输入数据的形态和模型结构。

## 2.2 Backpropagation 仍然是训练基础

对应 PDF：p.9-p.10

课件再次出现 one-layer perceptron 的反向传播例子。它提醒我们：卷积神经网络（Convolutional Neural Network, CNN）虽然结构比 MLP 特殊，但仍然通过反向传播（Backpropagation）训练参数。

卷积层也有权重和偏置：

$$
\text{filter weights},\quad \text{bias}
$$

训练时 loss 对这些参数求梯度，然后用 SGD、Momentum、Adam 等优化算法更新。CNN 的新东西在于“怎么连接”和“怎么利用图像空间结构”，不是训练范式完全改变。

# 三、Computer Vision 任务类型

## 3.1 图像分类、检测与分割

对应 PDF：p.11-p.15

课件列出的前三类视觉任务是：

- 图像分类（Image Classification）
- 目标检测（Object Detection）
- 目标分割（Object Segmentation）

它们之间的区别非常重要。

图像分类只回答“这张图是什么”。例如输入一张图片，输出 cat、dog、car 等类别。

目标检测不仅要回答“有什么”，还要指出“在哪里”。通常输出 bounding boxes 和类别。

目标分割进一步要求对每个像素分类。语义分割（Semantic Segmentation）关心每个像素属于什么类别；实例分割（Instance Segmentation）还要区分同一类别中的不同对象。

可以这样记：

| 任务 | 输出 | 需要的空间精度 |
|---|---|---|
| Image Classification | 一个或多个类别标签 | 低 |
| Object Detection | 类别 + 框 | 中 |
| Object Segmentation | 每个像素的类别或实例 | 高 |

## 3.2 更复杂的视觉任务

对应 PDF：p.16-p.19

课件还列出：

- 艺术风格迁移（Art Style Transformation）
- 图像描述（Image Captioning）
- 视觉问答（Visual Question Answering, VQA）
- 图像生成（Image Generation）

这些任务说明计算机视觉不只是分类。视觉模型可以和语言模型、生成模型结合。例如 image captioning 要把图像信息转成自然语言；VQA 要同时理解图像和问题；image generation 则要从噪声、文本或其他条件生成图像。

## 3.3 ImageNet 为什么重要

对应 PDF：p.20

课件把 ImageNet 称为 computer vision 的 oil。意思是：大规模标注数据是现代视觉模型发展的燃料。

深度学习模型参数多，若没有足够数据，很容易只记住训练集。ImageNet 提供了大规模图像和标签，使更大的 CNN 可以被训练和比较，也推动了 AlexNet、VGG、ResNet 等经典架构出现。

# 四、直接用 Fully Connected DNN 做图像分类的问题

## 4.1 彩色图像是三维张量

对应 PDF：p.21-p.25

彩色图像通常可以表示为三维张量（Tensor）：

$$
H\times W\times C
$$

其中：

- $H$ 是高度（Height）；
- $W$ 是宽度（Width）；
- $C$ 是通道数（Channels），RGB 图像通常 $C=3$。

例如 CIFAR-10 图像常见尺寸是：

$$
32\times 32\times 3
$$

如果用 fully connected DNN，需要先把图像拉直：

$$
32\times 32\times 3=3072
$$

于是输入变成一个长度为 3072 的向量。

## 4.2 拉直图像会丢失空间结构

对应 PDF：p.24-p.29

Fully Connected DNN 的做法是：

$$
x_{\text{image}}\in\mathbb{R}^{H\times W\times C}
\quad \rightarrow \quad
x_{\text{flat}}\in\mathbb{R}^{HWC}
$$

问题在于：图像中相邻像素的空间关系非常重要。比如边缘、纹理、角点都是局部空间结构。如果直接 flatten，模型虽然仍然可以学习，但它没有显式利用“相邻像素更相关”这个先验。

第二个问题是参数量大。若第一层 hidden units 为 512，对 CIFAR-10 输入 $3072$ 维，则第一层权重矩阵大小为：

$$
512\times 3072
$$

仅第一层就有大量参数。参数多而没有合适结构时，课件 p.29 指出会出现过拟合（Overfitting）。

因此需要 CNN：它用局部连接（Local Connectivity）和权重共享（Weight Sharing）保留空间结构，同时减少参数量。

# 五、Convolution 的基本思想

## 5.1 卷积的优势：保留空间信息

对应 PDF：p.30-p.32

卷积（Convolution）的关键优势是包含空间信息（Contain Spatial Information）。卷积不是新概念，课件提到 Sobel operator，它就是经典边缘检测滤波器。

图像中的局部模式通常具有平移性。例如同一个边缘出现在左上角或右下角，仍然是同一种模式。卷积核（Kernel 或 Filter）可以在图像上滑动，检测不同位置是否出现某种局部模式。

## 5.2 Filter 的形状

对应 PDF：p.33-p.35

对一张 $32\times 32\times 3$ 的图像，若使用 $5\times 5$ 的 filter，那么 filter 实际维度是：

$$
5\times 5\times 3
$$

课件强调：filters always extend the full depth of the input volume。也就是说，filter 的空间大小是 $5\times 5$，但深度必须覆盖所有输入通道。

一个局部区域也是：

$$
5\times 5\times 3
$$

卷积操作在这个局部区域和 filter 之间做点积，再加 bias：

$$
z = \sum_{u=1}^{5}\sum_{v=1}^{5}\sum_{c=1}^{3}
W_{u,v,c}X_{u,v,c}+b
$$

这就是课件中说的 $5\times 5\times 3=75$ dimensional dot product + bias。

## 5.3 Activation map

对应 PDF：p.36-p.39

当一个 filter 在整张图像的所有空间位置上滑动时，每个位置产生一个数。所有位置的输出排成一个二维矩阵，这就是激活图（Activation Map 或 Feature Map）。

如果输入是：

$$
32\times 32\times 3
$$

使用 $5\times 5\times 3$ filter，stride 为 1，且不加 padding，则输出空间尺寸为：

$$
28\times 28
$$

如果有 6 个 filters，每个 filter 产生一张 $28\times 28$ activation map，堆叠后得到：

$$
28\times 28\times 6
$$

所以卷积层的输出仍然是一个 tensor，可以继续送入下一层卷积。

# 六、卷积输出尺寸、Stride 与 Padding

## 6.1 输出尺寸公式

对应 PDF：p.40-p.51

假设输入空间尺寸为 $N\times N$，filter 大小为 $F\times F$，stride 为 $S$，无 padding，则输出尺寸为：

$$
\frac{N-F}{S}+1
$$

例如：

$$
N=7,\quad F=3
$$

若 $S=1$：

$$
\frac{7-3}{1}+1=5
$$

输出是 $5\times 5$。

若 $S=2$：

$$
\frac{7-3}{2}+1=3
$$

输出是 $3\times 3$。

若 $S=3$：

$$
\frac{7-3}{3}+1=2.33
$$

输出尺寸不是整数，说明 filter 滑动时无法完整覆盖输入，课件说 “doesn't fit”。

## 6.2 Padding 的作用

对应 PDF：p.52-p.54

Padding 是在输入边界补零。若输入为 $7\times 7$，filter 为 $3\times 3$，stride 为 1，不 padding 输出是 $5\times 5$。如果在边界 pad 1 pixel，输入有效空间变成 $9\times 9$：

$$
\frac{9-3}{1}+1=7
$$

输出保持为 $7\times 7$。

一般地，如果 stride 为 1，filter 大小为 $F\times F$，为了保持空间尺寸不变，常用 padding：

$$
P=\frac{F-1}{2}
$$

例如：

| Filter size | Padding |
|---|---|
| $3\times 3$ | 1 |
| $5\times 5$ | 2 |
| $7\times 7$ | 3 |

## 6.3 带 padding 的通用公式

对应 PDF：p.52-p.55

若 padding 为 $P$，输出尺寸为：

$$
\frac{N+2P-F}{S}+1
$$

这个公式是 CNN 中最常用的尺寸计算公式。以后看 PyTorch 的 `Conv2d` 时，对应参数就是 kernel size、stride、padding。

# 七、Feature Extraction 与 CNN

## 7.1 卷积核可以提取特征

对应 PDF：p.56-p.60

课件用 edge detector kernel 展示卷积可以提取边缘。直观上，一个 filter 就像一个局部模式探测器。如果某个图像局部区域和 filter 很匹配，点积输出就大；如果不匹配，输出就小。

在 CNN 中，filter 不是人手工指定，而是通过训练学出来。浅层 filter 可能学边缘和颜色变化，深层 filter 可能学形状、部件甚至语义概念。

## 7.2 CNN 的基本结构

对应 PDF：p.61-p.63

卷积神经网络（Convolutional Neural Network, CNN）可以理解为：

$$
\text{CONV} \rightarrow \text{Activation} \rightarrow \text{CONV} \rightarrow \text{Activation} \rightarrow \cdots
$$

课件说 CNN is a sequence of convolution layers, interspersed with activation functions。

例如：

1. 输入 $32\times 32\times 3$；
2. 使用 6 个 $5\times 5\times 3$ filters；
3. 得到 $28\times 28\times 6$；
4. 再使用 10 个 $5\times 5\times 6$ filters；
5. 得到新的 feature maps。

每一层都把低层特征组合成更高层特征。

## 7.3 1 x 1 Convolution

对应 PDF：p.64-p.65

$1\times 1$ convolution 看起来只看一个像素位置，但它仍然有意义，因为它会在通道维度上做点积。

若输入某位置有 $C$ 个通道：

$$
x_{i,j}\in\mathbb{R}^{C}
$$

一个 $1\times 1$ filter 等价于：

$$
z_{i,j}=w^Tx_{i,j}+b
$$

它不混合空间邻域，但会混合通道。常用于改变通道数、降低计算量或增强非线性表达。

## 7.4 PyTorch 中的卷积层

对应 PDF：p.66

课件提到 Code Convolution Layer in PyTorch。对应常见写法是：

```python
import torch.nn as nn

conv = nn.Conv2d(
    in_channels=3,
    out_channels=6,
    kernel_size=5,
    stride=1,
    padding=0,
)
```

这里：

- `in_channels=3` 对应 RGB 输入通道；
- `out_channels=6` 对应 6 个 filters；
- `kernel_size=5` 对应 $5\times 5$；
- `stride` 控制滑动步长；
- `padding` 控制边界补零。

## 7.5 Activation 的作用

对应 PDF：p.67-p.70

卷积层后通常接非线性激活函数（Non-linear Activation），例如 ReLU：

$$
\mathrm{ReLU}(x)=\max\{x,0\}
$$

课件强调 ReLU 会把负输入变成 0。这样做的意义是给模型引入非线性。如果只有卷积和线性组合，没有非线性，多层结构仍然可以退化为一个线性映射。

# 八、Pooling

## 8.1 Pooling 是下采样

对应 PDF：p.71-p.72

池化层（Pooling Layer）是一种下采样（Down Sampling）策略。课件给出两个目的：

1. 构造更好的平移不变特征（Translationally Invariant Features）；
2. 学到更紧凑的特征（Compact Features）。

平移不变性的意思是：如果图像中的某个模式稍微移动一点，模型仍然能识别它。

## 8.2 Max pooling 与 average pooling

对应 PDF：p.73-p.74

Max pooling 在局部窗口中取最大值。例如 $2\times 2$ window、stride 2，会把每个 $2\times 2$ 区域压缩成一个数。

最大池化（Max Pooling）常被推荐，因为它能保留局部最强响应，对小扰动更鲁棒。

Average pooling 则取平均值，保留局部整体强度，但可能弱化最显著的激活。

## 8.3 Pooling 输出尺寸

对应 PDF：p.75-p.76

给定输入 tensor：

$$
D\times M\times N
$$

如果 pooling operator 大小为 $K\times K$，stride 为 $P$，输出尺寸为：

$$
D\times
\left(\frac{M-K}{P}+1\right)
\times
\left(\frac{N-K}{P}+1\right)
$$

注意 pooling 通常不改变通道数 $D$，只改变空间尺寸。

PyTorch 中常见写法：

```python
pool = nn.MaxPool2d(kernel_size=2, stride=2)
```

# 九、Receptive Field

## 9.1 单层卷积的感受野

对应 PDF：p.77-p.78

感受野（Receptive Field）指输出中某个元素依赖输入中的哪一片区域。

若卷积核大小为 $K\times K$，那么单层卷积输出的每个元素依赖输入中的一个 $K\times K$ 区域。

## 9.2 多层卷积会扩大感受野

对应 PDF：p.79-p.82

课件指出：每一层卷积的输出又来自前一层多个区域。因此堆叠多层卷积时，深层神经元在原图上的感受野会变大。

这解释了 CNN 的层级学习：

- 浅层看局部边缘；
- 中层看纹理和局部形状；
- 深层看更大范围的物体部件。

因此 CNN 不是一次性理解整张图，而是通过多层局部计算逐渐扩大视觉范围。

# 十、本讲复习抓手

## 10.1 必须掌握的概念

- 计算机视觉（Computer Vision）：让模型处理和理解图像、视频等视觉数据。
- 图像分类（Image Classification）：预测整张图的类别。
- 目标检测（Object Detection）：预测类别和位置框。
- 目标分割（Object Segmentation）：预测像素级类别或实例。
- 卷积（Convolution）：用 filter 在空间上滑动并做局部点积。
- 激活图（Activation Map）：一个 filter 在所有空间位置上的响应。
- 步长（Stride）：filter 每次滑动的距离。
- 填充（Padding）：在边界补零以控制输出尺寸。
- 池化（Pooling）：下采样并增强局部鲁棒性。
- 感受野（Receptive Field）：输出元素在输入图像中依赖的区域。

## 10.2 尺寸公式速查

无 padding：

$$
O=\frac{N-F}{S}+1
$$

有 padding：

$$
O=\frac{N+2P-F}{S}+1
$$

Pooling：

$$
D\times M\times N
\rightarrow
D\times
\left(\frac{M-K}{P}+1\right)
\times
\left(\frac{N-K}{P}+1\right)
$$

## 10.3 本讲一句话

CNN 的核心不是“多了一个卷积操作”这么简单，而是用局部连接、权重共享、padding、activation、pooling 和 receptive field，把图像的空间结构变成可以训练的层级特征。
