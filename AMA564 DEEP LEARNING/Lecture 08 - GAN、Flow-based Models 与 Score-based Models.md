> [!info] 资料来源
> - 课件：`Lecture8.pdf`
> - 本笔记只依据 PDF 整理。
> - 本讲从 GAN 开始，扩展到 conditional GAN、CycleGAN、flow-based model 和 score-based model。

# 一、本讲的整体地图

## 1. PDF 页码索引

| PDF 页码 | 内容 | 学习重点 |
|---|---|---|
| p.1-p.4 | GAN demo | 生成模型可以产生逼真的人脸图像 |
| p.5-p.8 | 什么是 GAN 与基本架构 | generator 与 discriminator 的对抗博弈 |
| p.9-p.18 | Discriminator、Generator、value function 与训练 | 两个网络的目标函数与交替训练 |
| p.19-p.22 | GAN 理论与训练困难 | 理想平衡、non-convergence、mode collapse |
| p.23-p.32 | GAN 发展：Conditional GAN、Age Conditional GAN、CycleGAN | 条件生成与图像到图像转换 |
| p.33-p.40 | Flow-based models 与 Normalizing Flow | 可逆变换、显式密度、negative log-likelihood |
| p.41-p.53 | Score-based models | 直接学习 score function，用 Langevin dynamics 采样 |

# 二、GAN 的基本直觉

## 1. GAN 想解决什么问题

对应 PDF：p.2-p.4

生成对抗网络（Generative Adversarial Network, GAN）是一类生成模型（Generative Model）。它的目标不是判断一张图属于哪一类，而是学习如何生成看起来像真实数据的新样本。

课件用 photorealistic human faces 作为 demo。这里真正重要的不是“图像很逼真”，而是：模型并没有从训练集中复制一张已有图片，而是学习了真实人脸图像背后的数据分布。

如果真实数据来自：

$$
x\sim p_{\text{data}}(x)
$$

GAN 希望训练一个生成器：

$$
G(z)
$$

把噪声：

$$
z\sim p_z(z)
$$

映射成看起来像真实数据的样本。

## 2. 对抗的含义

对应 PDF：p.5-p.6

GAN 的核心是对抗（Adversarial）。课件引用原始论文的思想：生成模型与一个对手模型竞争，这个对手模型试图区分样本来自真实数据还是生成器。

可以把它想成两个角色：

- 生成器（Generator）：制造“假样本”，希望骗过判别器。
- 判别器（Discriminator）：判断输入是真实样本还是生成样本。

这种竞争会推动两个模型都变强。理想情况下，生成器生成的样本和真实样本无法区分。

# 三、GAN 的架构

## 1. Discriminator

对应 PDF：p.7-p.9

判别器（Discriminator）是一个神经网络：

$$
D(x)\in[0,1]
$$

它的目标是：

$$
D(x)=1
$$

如果 $x$ 来自真实数据；

$$
D(x)=0
$$

如果 $x$ 来自生成器。

也就是说，判别器本质上是一个二分类器（Binary Classifier）。它把输入图像映射成“真实概率”。

## 2. Generator

对应 PDF：p.10-p.11

生成器（Generator）也是一个神经网络：

$$
G(z)=x
$$

其中 $z$ 来自噪声分布，例如：

$$
z\sim \mathcal{N}(0,I)
$$

生成器不直接接收图像，而是接收随机噪声。它学习把简单噪声空间映射成复杂数据空间。

GAN 的 workflow 可以写成：

$$
z\rightarrow G(z)\rightarrow D(G(z))
$$

同时真实样本走：

$$
x\rightarrow D(x)
$$

# 四、GAN 的目标函数

## 1. Value function

对应 PDF：p.12-p.15

GAN 的经典目标函数是二人极小极大博弈（Two-player Minimax Game）：

$$
\min_G\max_D V(D,G)
$$

其中：

$$
V(D,G)
=
\mathbb{E}_{x\sim p_{\text{data}}}
\left[\log D(x)\right]
+
\mathbb{E}_{z\sim p_z}
\left[\log(1-D(G(z)))\right]
$$

判别器希望最大化这个目标：

- 对真实数据 $x$，让 $D(x)$ 接近 1；
- 对生成数据 $G(z)$，让 $D(G(z))$ 接近 0。

生成器希望最小化这个目标，尤其希望让：

$$
D(G(z))\rightarrow 1
$$

也就是让判别器误以为生成样本是真实样本。

## 2. Discriminator 的训练目标

对应 PDF：p.13-p.16

固定生成器 $G$ 时，训练判别器就是一个二分类问题：

$$
\max_D
\mathbb{E}_{x\sim p_{\text{data}}}
\left[\log D(x)\right]
+
\mathbb{E}_{z\sim p_z}
\left[\log(1-D(G(z)))\right]
$$

这和 cross entropy 的思想一致：真实样本标签为 1，生成样本标签为 0。

## 3. Generator 的训练目标

对应 PDF：p.14-p.17

固定判别器 $D$ 时，生成器希望让生成样本被判别为真实。经典 minimax 写法中，生成器最小化：

$$
\mathbb{E}_{z\sim p_z}
\left[\log(1-D(G(z)))\right]
$$

实践中常用 non-saturating version，让生成器最大化：

$$
\mathbb{E}_{z\sim p_z}
\left[\log D(G(z))\right]
$$

直观上就是：生成器越能骗过判别器，loss 越低。

## 4. GAN 的交替训练

对应 PDF：p.18-p.20

GAN 不是一次性同时求出 $G$ 和 $D$。通常交替训练：

1. 固定 $G$，用真实样本和生成样本训练 $D$；
2. 固定 $D$，更新 $G$，让 $G(z)$ 更像真实样本；
3. 重复以上步骤。

这种训练像一个动态博弈。判别器太强会让生成器梯度很差；生成器太强或训练不稳定也会导致判别器失去有效信号。

# 五、GAN 的理论平衡与训练困难

## 1. 理想平衡

对应 PDF：p.19

课件给出 GAN 的理论状态：

$$
G^*(Z)\sim X
$$

即生成器产生的数据分布与真实数据分布相同。

此时判别器无法区分真假，所以：

$$
D^*(x)=\frac{1}{2}
$$

对所有 $x$ 都成立。

这不是说判别器“失败了”，而是生成器已经达到理想效果，真假样本不可区分。

## 2. Non-convergence

对应 PDF：p.21

GAN 的第一个训练困难是模型不收敛（Non-convergence）。由于 $G$ 和 $D$ 的目标互相依赖，训练过程可能震荡，而不是稳定下降到一个固定点。

普通监督学习通常最小化一个固定 loss；GAN 中判别器在变，生成器面对的目标也在变。

## 3. Mode collapse

对应 PDF：p.22

第二个困难是模式崩塌（Mode Collapse）。真实数据分布可能有很多模式，例如数字 0-9、人脸不同姿态、不同背景。生成器可能只学会生成其中少数几种模式，以骗过判别器。

例如训练集有 10 类数字，但生成器只生成 1 和 7。这些样本可能很逼真，但缺乏多样性。

# 六、GAN 的发展

## 1. 2014 年原始 GAN

对应 PDF：p.23-p.25

课件提到 2014 年 GAN 的数据集包括 MNIST、Toronto Face Database 和 CIFAR-10。早期 GAN 已经展示了生成样本的潜力，后续出现了大量变体和应用。

## 2. Conditional GAN

对应 PDF：p.26-p.27

条件 GAN（Conditional GAN, cGAN）在生成器和判别器中加入条件变量 $y$。

普通 GAN：

$$
G(z)
$$

Conditional GAN：

$$
G(z,y)
$$

判别器也可以写成：

$$
D(x,y)
$$

这样就能控制生成结果。例如指定类别标签，让模型生成某一类图像。

## 3. Age Conditional GAN

对应 PDF：p.28

Age Conditional GAN 是条件生成的一个应用：给定年龄条件，让模型生成不同年龄阶段的人脸。它说明条件变量不一定只是类别，也可以是年龄、属性、文本描述等。

## 4. CycleGAN

对应 PDF：p.29-p.32

CycleGAN 用于 unpaired image-to-image translation。课件例子包括：

- Monet paintings $\rightarrow$ photos；
- object transfiguration；
- season transfer。

CycleGAN 的关键意义是：不需要一一配对的训练样本。比如不需要同一场景的夏天和冬天照片配对，也可以学习季节转换。

核心思想是循环一致性（Cycle Consistency）：

$$
x\rightarrow G(x)\rightarrow F(G(x))\approx x
$$

如果从域 A 转到域 B，再从域 B 转回域 A，应该接近原图。

# 七、Flow-based Models

## 1. Flow-based model 的基本思想

对应 PDF：p.33-p.35

Flow-based generative model 通过一系列可逆变换（Invertible Transformations）构造生成模型。

从简单分布开始：

$$
z\sim \pi(z)
$$

经过可逆函数：

$$
x=f(z)
$$

如果 $f$ 可逆，则：

$$
z=f^{-1}(x)
$$

这样就可以显式计算 $x$ 的概率密度。

## 2. 为什么要求可逆

对应 PDF：p.35-p.36

可逆性让我们可以用 change of variables 公式：

$$
p_X(x)=p_Z(f^{-1}(x))
\left|
\det
\frac{\partial f^{-1}(x)}{\partial x}
\right|
$$

因此 flow-based model 与 GAN/VAE 不同，它可以显式估计 likelihood。

课件列出 transformation function $f$ 的要求：

1. 容易求逆；
2. Jacobian determinant 容易计算；
3. 有足够表达能力。

## 3. Normalizing Flow

对应 PDF：p.37-p.40

Normalizing Flow 把简单分布通过一系列可逆变换变成复杂分布：

$$
z_0\rightarrow z_1\rightarrow \cdots \rightarrow z_K=x
$$

每一步：

$$
z_k=f_k(z_{k-1})
$$

最终得到复杂数据分布。

训练准则是负对数似然（Negative Log-likelihood, NLL）：

$$
\mathcal{L}
=
-\sum_{x\in D}\log p_\theta(x)
$$

课件提到实现方法包括 NICE、RealNVP、Glow 等。

# 八、Score-based Models

## 1. 从密度函数到 score function

对应 PDF：p.41-p.43

Likelihood-based models 直接建模概率密度：

$$
p_\theta(x)
$$

Score-based models 不直接建模 $p(x)$，而是建模它的梯度：

$$
\nabla_x\log p(x)
$$

这个量叫 score function。

score function 指向“让概率密度上升最快”的方向。学习 score function 后，可以通过迭代采样过程生成数据。

## 2. Fisher divergence 与 Langevin dynamics

对应 PDF：p.44-p.46

课件提到用 Fisher divergence 训练 score-based model，使模型：

$$
s_\theta(x)\approx \nabla_x\log p(x)
$$

训练好后，可以用 Langevin dynamics 采样。一个典型更新形式是：

$$
x_{t+1}
=
x_t+\frac{\epsilon}{2}s_\theta(x_t)+\sqrt{\epsilon}\eta_t,
\quad
\eta_t\sim\mathcal{N}(0,I)
$$

直觉是：沿着 score 指向的高密度区域移动，同时加入随机噪声保持采样多样性。

## 3. 为什么要加噪声训练

对应 PDF：p.47-p.48

课件指出问题：估计的 scores 只在高密度区域准确。低密度区域数据少，score 估计差，采样可能不稳定。

解决方法是：给数据加噪声，在 noisy data points 上训练 score-based model。这样模型能学会从噪声扰动的数据逐渐回到真实数据流形。

这与后来的扩散模型（Diffusion Models）关系很紧密。

## 4. NCSN 与生成样本

对应 PDF：p.49-p.53

课件展示 Annealed Langevin Dynamics for Noise Conditional Score Network（NCSN）以及 FFHQ、LSUN bedroom、CelebA-HQ 等样本。

这里的重点是：score-based model 可以通过逐步去噪生成高质量图像。第 8 讲虽然没有深入 diffusion 的全部数学，但已经给出核心思想：学习分布的 score，再用迭代过程采样。

# 九、本讲复习抓手

## 1. 生成模型对比

| 模型 | 是否显式建模密度 | 训练目标 | 主要优势 | 主要困难 |
|---|---|---|---|---|
| GAN | 否 | adversarial minimax | 样本锐利、生成质量高 | 训练不稳定、mode collapse |
| VAE | 近似 likelihood / ELBO | reconstruction + KL | latent space 可解释、可采样 | 样本可能模糊 |
| Flow-based | 是 | negative log-likelihood | 精确 likelihood，可逆生成 | 可逆结构限制表达 |
| Score-based | 不直接建模密度，建模 score | Fisher divergence / denoising score matching | 高质量生成，可与 diffusion 连接 | 采样迭代成本高 |

## 2. 关键公式

GAN value function：

$$
\min_G\max_D
\mathbb{E}_{x\sim p_{\text{data}}}
[\log D(x)]
+
\mathbb{E}_{z\sim p_z}
[\log(1-D(G(z)))]
$$

理想判别器：

$$
D^*(x)=\frac{1}{2}
$$

Normalizing Flow change of variables：

$$
p_X(x)=p_Z(f^{-1}(x))
\left|
\det
\frac{\partial f^{-1}(x)}{\partial x}
\right|
$$

Score function：

$$
s(x)=\nabla_x\log p(x)
$$

Langevin dynamics：

$$
x_{t+1}=x_t+\frac{\epsilon}{2}s_\theta(x_t)+\sqrt{\epsilon}\eta_t
$$

## 3. 本讲一句话

GAN 用两个网络对抗学习生成分布，flow-based model 用可逆变换显式计算密度，score-based model 学习数据分布的梯度方向并通过迭代采样生成数据。

# 十、补充学习注释与复习路线

## 1. 本讲怎么读

这一讲对应 PDF：p.1-p.53。它继续生成模型主题，但从 VAE 转到 GAN、Flow-based Models 和 Score-based Models。复习时要抓住三类生成模型的差别：是否显式建模密度、是否容易采样、训练是否稳定。

推荐按三段读：

1. p.1-p.22：GAN 的 generator、discriminator、value function 和训练困难。
2. p.23-p.32：Conditional GAN、Age Conditional GAN、CycleGAN 说明如何控制生成或做 domain translation。
3. p.33-p.53：Flow-based 和 Score-based Models 展示另一类基于概率密度或 score 的生成思路。

GAN 的核心是两个网络的博弈：

- 生成器（Generator）$G(z)$：把随机噪声 $z$ 变成假样本；
- 判别器（Discriminator）$D(x)$：判断输入是真样本还是假样本。

经典 value function 是：

$$
\min_G\max_D V(D,G)
=\mathbb{E}_{x\sim p_{data}}[\log D(x)]
+\mathbb{E}_{z\sim p_z}[\log(1-D(G(z)))]
$$

直观上，$D$ 想把真样本判成 1、假样本判成 0；$G$ 想让 $D(G(z))$ 接近 1。GAN 强在采样质量，难在训练稳定性。p.19-p.22 的 mode collapse 要特别记：生成器可能只生成少数几类样本来欺骗判别器，导致多样性不足。

Flow-based Models 对应 p.33-p.40，重点是可逆变换（Invertible Transformation）。若：

$$
x=f(z)
$$

且 $f$ 可逆，则可以用 change-of-variables 公式计算密度：

$$
p_X(x)=p_Z(f^{-1}(x))\left|\det \frac{\partial f^{-1}}{\partial x}\right|
$$

这类模型的优点是显式 likelihood，缺点是结构受可逆性限制。

Score-based Models 对应 p.41-p.53。它不直接学 $p(x)$，而是学 score function：

$$
s_\theta(x)\approx \nabla_x\log p(x)
$$

score 可以理解成“往数据高密度区域移动的方向”。采样时用 Langevin dynamics 逐步把噪声推向数据分布。它和后来的 diffusion model 思想关系很近：通过噪声水平和逐步去噪来生成样本。

三类模型可以这样对比：

| 模型 | 密度是否显式 | 采样 | 主要困难 |
|---|---|---|---|
| GAN | 通常不显式 | 快 | 不稳定、mode collapse |
| Flow | 显式 | 快且可逆 | 架构受限制 |
| Score-based | 学 score 而非直接密度 | 多步采样 | 采样成本和训练设计 |

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
