> [!info] 资料来源
> - 课件：`AMA564_Deep Learning_Lecture5.pdf`
> - 本笔记只依据 PDF 整理。
> - 本讲从 CNN 基本组件进入经典架构，并解释深层网络训练中的初始化与 Batch Normalization。

# 一、本讲的整体地图

## 1. PDF 页码索引

| PDF 页码 | 内容 | 学习重点 |
|---|---|---|
| p.1-p.9 | CNN recap | filter、activation map、CNN 序列、pooling |
| p.10-p.21 | LeNet-5 | 早期 CNN 架构，卷积、池化、全连接的组合 |
| p.22-p.30 | AlexNet | ReLU、overlapping pooling、data augmentation、dropout、ImageNet 突破 |
| p.31-p.35 | VGG | 用多个小卷积核替代大卷积核，深度提升性能但内存昂贵 |
| p.36-p.45 | ResNet | skip connection、residual block、bottleneck、训练策略 |
| p.46-p.51 | Weight initialization | 随机初始化问题、Xavier、He initialization |
| p.52-p.61 | Batch Normalization | 控制激活均值和方差，缓解梯度消失，训练和测试行为不同 |
| p.62-p.64 | DenseNet、GoogLeNet | 其他经典 CNN 架构 |

# 二、CNN Recap

## 1. Convolution layer 回顾

对应 PDF：p.2-p.8

输入图像可以表示为：

$$
32\times 32\times 3
$$

如果使用 $5\times 5\times 3$ 的 filter，它会覆盖输入的全部深度，并在空间维度上滑动。每个空间位置做一次点积：

$$
z=\sum_{u,v,c}W_{u,v,c}X_{u,v,c}+b
$$

一个 filter 产生一张 activation map。多个 filters 会产生多个 activation maps，并沿通道方向堆叠。例如 6 个 filters 得到：

$$
28\times 28\times 6
$$

CNN 是卷积层（Convolution Layers）和激活函数（Activation Functions）的序列：

$$
\text{CONV}\rightarrow\text{ReLU}\rightarrow\text{CONV}\rightarrow\text{ReLU}\rightarrow\cdots
$$

## 2. Pooling 回顾

对应 PDF：p.9

池化层（Pooling Layer）是下采样（Down Sampling）策略，主要作用是：

1. 构造更好的平移不变特征（Translationally Invariant Features）；
2. 学习更紧凑的特征（Compact Features）。

这为后面的经典架构做准备。LeNet、AlexNet 等模型都在不同程度上组合了 convolution、activation、pooling 和 fully connected layers。

# 三、LeNet-5

## 1. LeNet-5 的历史位置

对应 PDF：p.10-p.12

LeNet-5 是 Yann LeCun 等人在 1998 年提出的经典 CNN，用于文档识别和手写数字识别。课件总结它有 7 层，不计 input layer：

- 3 个卷积层：C1、C3、C5
- 2 个池化层：S2、S4
- 2 个全连接层：F6、Output

它使用 Sigmoid activation。今天常用 ReLU，但 LeNet 的重要性在于它展示了卷积、池化、全连接组合处理图像的完整路线。

## 2. LeNet-5 的层结构

对应 PDF：p.13-p.19

LeNet-5 的尺寸变化如下：

| 层 | 类型 | 输入 | 参数或操作 | 输出 |
|---|---|---|---|---|
| C1 | Convolution | $1\times 32\times 32$ | 6 个 $5\times 5$ kernels | $6\times 28\times 28$ |
| S2 | Max Pooling | $6\times 28\times 28$ | $2\times 2$ pooling | $6\times 14\times 14$ |
| C3 | Convolution | $6\times 14\times 14$ | 16 个 $5\times 5$ kernels | $16\times 10\times 10$ |
| S4 | Max Pooling | $16\times 10\times 10$ | $2\times 2$ pooling | $16\times 5\times 5$ |
| C5 | Convolution | $16\times 5\times 5$ | 120 个 $5\times 5$ kernels | $1\times 120$ |
| F6 | Fully Connected | $1\times 120$ | 全连接 | $1\times 84$ |
| Output | Fully Connected | $1\times 84$ | 分类输出 | $1\times 10$ |

C5 很值得注意。因为输入空间尺寸是 $5\times 5$，kernel 也是 $5\times 5$，所以输出空间尺寸变成 $1\times 1$，再加 120 个输出通道，就得到 $1\times 120$。这说明卷积层也可以把 tensor 转换为 vector。

## 3. LeNet-5 的意义

对应 PDF：p.20-p.21

课件总结 LeNet-5 是 simple CNN architecture。它的学习价值在于：

1. 让我们看到 CNN 的基本 pipeline；
2. 展示卷积层、池化层和全连接层如何衔接；
3. 说明分类任务最后通常需要输出类别数，例如 MNIST 为 10 类。

# 四、AlexNet

## 1. AlexNet 的突破

对应 PDF：p.22-p.30

AlexNet 是 2012 年 ImageNet 分类任务的标志性模型。课件给出结果：

| 模型 | Top-1 Error | Top-5 Error |
|---|---:|---:|
| Before AlexNet | 47.1% | 28.2% |
| AlexNet | 37.5% | 17% |

这个提升说明深度 CNN 在大规模图像分类中有巨大潜力。

## 2. Feature 1：ReLU Activation

对应 PDF：p.23

AlexNet 使用 ReLU（Rectified Linear Unit）：

$$
\mathrm{ReLU}(x)=\max\{x,0\}
$$

课件指出，使用 ReLU 的 CNN 在 CIFAR-10 上达到 25% error rate 的速度比使用 tanh 快 6 倍。

原因是 tanh 在两端会饱和，导数接近 0，容易导致梯度消失（Vanishing Gradient）。ReLU 在正半轴导数为 1，深层网络更容易训练。

## 3. Feature 2：Overlapping Pooling

对应 PDF：p.24

AlexNet 使用 $3\times 3$ max pooling，stride 为 2。这叫 overlapping pooling，因为 pooling window 之间有重叠。

普通 $2\times 2$ pooling with stride 2 没有重叠；$3\times 3$ with stride 2 会让相邻池化区域共享一部分输入。这样可以让下采样更平滑，也可能提升泛化能力。

## 4. Overfitting 与 Data Augmentation

对应 PDF：p.25-p.28

课件指出：复杂模型不一定过拟合，前提是：

1. 有大而复杂的数据集；
2. 大量模型参数为零或被正则化控制。

AlexNet 使用数据增强（Data Augmentation）降低过拟合风险。课件展示了 rotation。数据增强的思想是：通过对训练图像做合理变换，构造更多等价样本。

常见图像增强包括：

- rotation；
- crop；
- flip；
- color jitter；
- translation。

这些操作让模型不要过度依赖某个具体位置、角度或颜色分布。

## 5. Dropout

对应 PDF：p.29

Dropout layer 会以给定概率随机把输入元素置为 0。AlexNet 使用 dropout probability $0.5$。

直观理解：每次训练时随机关闭一部分神经元，迫使模型不要过度依赖少数特征。它相当于训练许多共享参数的子网络，从而起到正则化作用。

# 五、VGG

## 1. VGG 的核心思想

对应 PDF：p.31-p.34

VGG 的关键是：用多个小卷积核替代一个大卷积核。课件例子是用两个 $3\times 3$ filters 替代一个 $5\times 5$ filter。

两个连续的 $3\times 3$ 卷积在感受野上可以覆盖 $5\times 5$ 区域，同时引入两次非线性激活。因此它可能比单个 $5\times 5$ 卷积更有表达能力。

参数量也可能更低。若输入输出通道近似相同为 $C$：

单个 $5\times 5$ 卷积参数约为：

$$
25C^2
$$

两个 $3\times 3$ 卷积参数约为：

$$
2\times 9C^2=18C^2
$$

所以小卷积核堆叠可以同时增加深度、增加非线性，并控制参数量。

## 2. VGG 的优缺点

对应 PDF：p.34-p.35

课件给出 VGG 的优点：

1. 更简洁、更容易泛化；
2. 小 filter 可以达到比大 filter 更好的性能；
3. 展示增加深度可以提升表现。

缺点是内存昂贵（Memory Expensive）。VGG 有大量卷积层和参数，训练与推理成本都较高。

# 六、ResNet

## 1. 深度为什么不一定容易优化

对应 PDF：p.36-p.38

直觉上，深层模型应该至少不比浅层模型差。因为深层模型理论上可以让新增层学习 identity mapping：

$$
f(x)=x
$$

这样深层网络就可以退化成浅层网络。

但实践中，普通深层网络很难优化。层数越深，梯度传播、初始化和函数学习都会变难。因此 ResNet 的核心问题是：怎样让深层网络更容易学习 identity mapping。

## 2. Skip connection 与 residual mapping

对应 PDF：p.39-p.41

ResNet 的核心是跳跃连接（Skip Connection）。普通网络直接学习：

$$
H(x)
$$

ResNet 让网络块学习残差：

$$
F(x)=H(x)-x
$$

输出为：

$$
H(x)=F(x)+x
$$

如果目标就是 identity mapping，那么只需要让：

$$
F(x)=0
$$

这比直接学习 $H(x)=x$ 更容易。

## 3. Residual block

对应 PDF：p.42-p.44

课件提到 ResNet 使用 residual blocks，并列出不同 stage 的卷积通道数：

- Stage 1：$3\times 3$ convolution filters with 64 channels；
- Stage 2：$3\times 3$ convolution filters with 128 channels；
- Stage 3：$3\times 3$ convolution filters with 512 channels。

课件还指出 ResNet 在输出前没有传统的大型 fully connected layers。这意味着深层卷积结构承担了主要特征提取工作。

对 50 层以上的 very deep networks，可以使用 bottleneck building blocks 提高效率。Bottleneck 常见形式是：

$$
1\times 1 \rightarrow 3\times 3 \rightarrow 1\times 1
$$

第一个 $1\times 1$ 降维，中间 $3\times 3$ 做空间特征提取，最后 $1\times 1$ 升维。

## 4. ResNet 的训练实践

对应 PDF：p.45

课件列出训练 ResNet 的实践要点：

- 使用 He 的 Xavier initialization；
- 每个 convolution layer 后使用 Batch Normalization；
- 使用 SGD + Momentum，其中 momentum 为 0.9；
- 使用动态学习率调度（Dynamic Learning Rate Scheduling）；
- He 的 ResNet 论文中没有使用 dropout。

这说明好架构还需要配合好的训练策略。ResNet 成功不是只因为 skip connection，也和 initialization、BN、optimizer、learning rate schedule 一起有关。

# 七、Weight Initialization

## 1. 随机初始化为什么可能失败

对应 PDF：p.46-p.47

课件讨论 10-layer DNN with tanh activation。

如果权重初始化为：

$$
W\sim N(0,0.01)
$$

后几层输出几乎变成 0。信号在层间传播时被压小。

如果权重初始化为：

$$
W\sim N(0,1)
$$

输出接近 $-1$ 或 $1$，tanh 进入饱和区，梯度很小。

这说明初始化不是随便给随机数。好的初始化要让信号在前向传播和反向传播时保持合适尺度。

## 2. Xavier Initialization

对应 PDF：p.48-p.49

Xavier Initialization 的动机是保持输入和输出方差一致。

考虑：

$$
y=w_1x_1+w_2x_2+\cdots+w_nx_n
$$

假设 $w_i$ 和 $x_i$ 独立同分布，均值为 0，则：

$$
\mathrm{Var}(w_ix_i)=\mathrm{Var}(w_i)\mathrm{Var}(x_i)
$$

因此：

$$
\mathrm{Var}(y)
=
\sum_{i=1}^{n}\mathrm{Var}(w_ix_i)
=
n\mathrm{Var}(w)\mathrm{Var}(x)
$$

为了让：

$$
\mathrm{Var}(y)=\mathrm{Var}(x)
$$

需要：

$$
\mathrm{Var}(w)=\frac{1}{n}
$$

所以可以初始化为：

$$
W\sim \frac{N(0,1)}{\sqrt{n_{\text{in}}}}
$$

这就是 Xavier 的核心直觉。

## 3. He Initialization for ReLU

对应 PDF：p.50-p.51

对于 ReLU activation，Xavier 不一定最合适。因为 ReLU 会让大约一半神经元输出为 0。

He initialization 的动机是：假设每层只有一半神经元被激活，因此需要更大的方差来补偿。课件写作：

$$
W\sim \frac{N(0,1)}{\sqrt{n_{\text{in}}/2}}
$$

等价于：

$$
\mathrm{Var}(W)=\frac{2}{n_{\text{in}}}
$$

这也是为什么 ReLU 网络中经常使用 Kaiming/He initialization。

# 八、Batch Normalization

## 1. BN 的动机

对应 PDF：p.52-p.57

课件用线性层输出：

$$
y=Wx
$$

说明如果输入 $x$ 的均值不为 0 或方差很大，会让训练变难：

$$
\mathbb{E}[x]\ne 0
$$

或：

$$
\mathrm{Var}(x)\text{ is large}
$$

Batch Normalization（BN）希望让每一维激活满足：

$$
\mathbb{E}[x]=0,\qquad \mathrm{Var}(x)=1
$$

也就是把激活标准化。

## 2. BN 的计算

对应 PDF：p.58

给定 batch：

$$
x^1,\ldots,x^N\in\mathbb{R}^d
$$

对第 $j$ 个维度计算 batch mean：

$$
\mu_j=\frac{1}{N}\sum_{i=1}^{N}x_j^i
$$

和 batch variance：

$$
\sigma_j^2=\frac{1}{N}\sum_{i=1}^{N}(x_j^i-\mu_j)^2
$$

然后标准化：

$$
\hat{x}_j^i=
\frac{x_j^i-\mu_j}{\sqrt{\sigma_j^2+\epsilon}}
$$

$\epsilon$ 是为了避免除以 0 的小常数。

## 3. Learnable scale and shift

对应 PDF：p.59

如果只做标准化，可能会限制模型表达能力。因此 BN 加入可学习参数 $\gamma_j$ 和 $\beta_j$：

$$
y_j^i=\gamma_j\hat{x}_j^i+\beta_j
$$

这表示模型可以自己决定标准化后是否要缩放或平移。BN 不是简单把所有分布固定死，而是先稳定训练，再允许模型学习合适尺度。

## 4. BN 在测试阶段的行为

对应 PDF：p.60

训练时 BN 使用当前 batch 的均值和方差；测试时不能依赖 batch 的随机统计量，通常使用训练过程中累计的 running mean 和 running variance：

$$
\mu_j^{\text{test}}=\mathbb{E}[\mu_j]
$$

$$
(\sigma_j^2)^{\text{test}}=\mathbb{E}[\sigma_j^2]
$$

测试时：

$$
\hat{x}_j^i=
\frac{x_j^i-\mu_j^{\text{test}}}
{\sqrt{(\sigma_j^2)^{\text{test}}+\epsilon}}
$$

再使用：

$$
y_j^i=\gamma_j\hat{x}_j^i+\beta_j
$$

课件指出：测试阶段 BN 是一个 linear operator。

## 5. BN 可以放在哪里

对应 PDF：p.61

课件展示 BN 可以集成到 DNN 中，例如放在 Conv 或 FC 后、activation 前后。常见结构是：

$$
\text{Conv} \rightarrow \text{BN} \rightarrow \text{ReLU}
$$

BN 的作用不是替代 activation，也不是替代 optimizer，而是让中间激活分布更稳定，从而缓解训练深层网络时的梯度问题。

# 九、其他 CNN 架构

## 1. DenseNet

对应 PDF：p.62-p.63

DenseNet（Densely Connected Convolutional Networks）通过密集连接让后续层可以直接访问前面所有层的特征。它和 ResNet 都关注信息流和梯度流，但连接方式不同。

ResNet 使用加法：

$$
x_{l+1}=F_l(x_l)+x_l
$$

DenseNet 更强调特征拼接：

$$
x_l=H_l([x_0,x_1,\ldots,x_{l-1}])
$$

## 2. GoogLeNet

对应 PDF：p.64

GoogLeNet 的代表性组件是 Inception module。它的思想是在同一层中并行使用不同尺度的卷积，例如 $1\times 1$、$3\times 3$、$5\times 5$，再把结果组合起来。

这体现了 CNN 架构设计的一个方向：不仅要更深，还要让网络在同一层捕捉不同尺度的信息。

# 十、本讲复习抓手

## 1. 架构对比

| 架构 | 核心贡献 | 学习重点 |
|---|---|---|
| LeNet-5 | 早期 CNN pipeline | Conv + Pooling + FC |
| AlexNet | ImageNet 突破 | ReLU、data augmentation、dropout |
| VGG | 小卷积核堆叠 | 深度增加、结构简洁、内存昂贵 |
| ResNet | Skip connection | 学 residual mapping，解决深层优化难题 |
| DenseNet | Dense connection | 特征复用与梯度流 |
| GoogLeNet | Inception | 多尺度卷积并行 |

## 2. 训练技巧速查

- Xavier Initialization：适合 tanh 等对称激活，目标是保持方差。
- He Initialization：适合 ReLU，考虑一半神经元不激活。
- Batch Normalization：标准化 batch 激活，再用 $\gamma,\beta$ 学习缩放和平移。
- Dropout：随机置零，减少过拟合。
- Data Augmentation：通过合理变换增加训练样本多样性。
- Dynamic Learning Rate Scheduling：训练中逐步调整学习率。

## 3. 本讲一句话

第 4 讲告诉我们 CNN 的零件是什么；第 5 讲告诉我们这些零件如何组成经典架构，以及为什么深层 CNN 必须配合初始化、BN、正则化和学习率策略才能稳定训练。

# 十一、补充学习注释与复习路线

## 1. 本讲怎么读

这一讲对应 PDF：p.1-p.64。它不是简单罗列 CNN 名字，而是在回答一个训练深层 CNN 的核心问题：**怎样把网络做深、做宽，同时还能训练稳定并提升泛化能力？**

推荐按“架构演化 + 训练技巧”两条线读：

1. p.10-p.45：LeNet、AlexNet、VGG、ResNet 展示 CNN 架构如何逐渐变深。
2. p.46-p.61：初始化（Initialization）和批归一化（Batch Normalization）解释深层网络为什么需要训练稳定化技巧。
3. p.62-p.64：DenseNet、GoogLeNet 展示更多连接方式和模块化设计。

LeNet-5 对应 p.10-p.21，可以看成 CNN 的基本范式：卷积提取局部特征，池化降低空间尺寸，最后用全连接层做分类。AlexNet 对应 p.22-p.30，它的重要性不只是 ImageNet 获胜，还在于把 ReLU、数据增强（Data Augmentation）、dropout 和 GPU 训练组合起来，证明深层 CNN 可以在大规模视觉任务上有效。

VGG 对应 p.31-p.35，核心思想是用多个小卷积核叠加替代大卷积核。两个 $3\times3$ 卷积的感受野接近一个 $5\times5$，但参数更少、非线性更多。这个思想说明：**深度不只是层数增加，也是在增加中间非线性变换的机会。**

ResNet 对应 p.36-p.45，是本讲最关键的架构。残差块（Residual Block）写成：

$$
y=F(x)+x
$$

这里 $x$ 是 skip connection 直接传过来的输入，$F(x)$ 是若干卷积层学习到的残差。直观上，网络不必从零学习完整映射，只需要学习“在输入基础上应该改多少”。这让非常深的网络更容易优化。

p.46-p.51 的初始化要和梯度传播联系起来。Xavier initialization 适合 tanh/sigmoid 一类激活，He initialization 更适合 ReLU。目标都是让前向传播的激活方差、反向传播的梯度方差不要随着层数快速爆炸或消失。

p.52-p.61 的 Batch Normalization 可以理解为在训练时对 mini-batch 的激活做标准化：

$$
\hat{x}=\frac{x-\mu_B}{\sqrt{\sigma_B^2+\epsilon}}
$$

然后再学习缩放和平移：

$$
y=\gamma \hat{x}+\beta
$$

注意 BN 不是简单“把数据标准化一次”。它发生在网络中间层，而且训练阶段使用 mini-batch 统计量，测试阶段使用运行平均统计量（Running Statistics）。这一点是理解 BN 代码和考试概念题的关键。

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
