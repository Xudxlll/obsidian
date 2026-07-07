> [!info] 资料来源
> - 课件：`AMA564_Deep Learning_Lecture7.pdf`
> - 本笔记只依据 PDF 整理。
> - 本讲核心问题：生成模型如何学习数据分布？为什么普通 Autoencoder 不适合直接生成？VAE 如何让 latent space 可采样？

# 一、本讲的整体地图

## 1. PDF 页码索引

| PDF 页码 | 内容 | 学习重点 |
|---|---|---|
| p.1-p.8 | Generative Models overview | 生成模型学习数据分布并产生新样本，与 discriminative model 不同 |
| p.9-p.18 | Autoencoder 与 latent space regularity | AE 是压缩与重构，普通 latent space 可能不规则 |
| p.19-p.25 | Variational Autoencoder 与 KL divergence | VAE 编码分布而非单点，loss 有 reconstruction 和 regularization |
| p.26-p.33 | VAE neural implementation 与 reparameterization trick | encoder 输出 mean/covariance，采样会阻断反传，需要重参数化 |
| p.34-p.48 | MNIST 上 AE 与 VAE 示例 | 比较普通 AE 与 VAE 的 latent space 和 decoded space |
| p.49-p.56 | Conditional VAE | 加入 label 条件，实现按类别生成 |

# 二、Generative Models

## 1. 什么是生成模型

对应 PDF：p.2-p.3

生成模型（Generative Model）是一类机器学习模型，它学习数据集的概率分布（Probability Distribution），并生成与原始数据相似的新样本。

如果训练数据来自某个未知分布：

$$
x\sim p_{\text{data}}(x)
$$

生成模型希望学到一个模型分布：

$$
p_\theta(x)
$$

使得从 $p_\theta(x)$ 中采样的新样本看起来像真实数据。

它可以用于：

- 图像生成（Image Generation）
- 文本生成（Text Generation）
- 语音合成（Speech Synthesis）

## 2. 生成模型与判别模型

对应 PDF：p.4

判别模型（Discriminative Model）学习不同类别之间的决策边界。例如分类器学习：

$$
p(y\mid x)
$$

或直接学习：

$$
y=f_\theta(x)
$$

生成模型（Generative Model）则试图建模整个数据分布：

$$
p(x)
$$

有些生成模型还建模联合分布：

$$
p(x,y)
$$

区别可以这样记：

| 类型 | 学什么 | 典型问题 |
|---|---|---|
| Discriminative Model | 决策边界或条件概率 | 这张图属于哪一类 |
| Generative Model | 数据分布 | 如何生成一张像训练集的新图 |

## 3. 常见生成模型路线

对应 PDF：p.5-p.8

课件展示了不同生成路线：

- GAN 学习生成图像；
- VAE 学习生成图像；
- Denoising Diffusion Models 学习生成图像。

这些方法目标相似，都是生成新样本，但训练方式不同。第 7 讲重点放在 Variational Auto-Encoder（VAE）。

# 三、Autoencoder

## 1. Autoencoder 是自动学习的压缩与解压

对应 PDF：p.9-p.11

自动编码器（Autoencoder, AE）是一种数据压缩算法。它由两部分组成：

- 编码器（Encoder）：把输入 $x$ 压缩成 latent representation $z$；
- 解码器（Decoder）：把 $z$ 重构回 $\hat{x}$。

形式上：

$$
z=E_\phi(x)
$$

$$
\hat{x}=D_\theta(z)
$$

训练目标是让重构误差（Reconstruction Loss）尽量小：

$$
\mathcal{L}_{\text{rec}}(x,\hat{x})
$$

例如可用平方误差：

$$
\|x-\hat{x}\|^2
$$

课件强调 autoencoding 有三个特点：

1. data-specific；
2. lossy；
3. learned automatically from examples。

## 2. 普通 Autoencoder 的潜在问题

对应 PDF：p.12-p.16

课件指出：如果 encoder 能力无限强，它可能把 $N$ 个训练样本编码成 $1,2,\ldots,N$ 这样的离散编号，decoder 再把编号映射回原样本。这样 reconstruction loss 可以很低，但 latent space 没有可解释、可利用的结构。

这会带来一个问题：我们能否随机从 latent space 采样一个点，然后用 decoder 生成新数据？

普通 AE 不一定可以。因为 latent space 可能非常不规则（Irregular Latent Space）。某些区域 decoder 能生成合理样本，另一些区域可能完全没有意义。

## 3. Regular latent space 需要什么性质

对应 PDF：p.17

课件给出两个直觉：

连续性（Continuity）：

> latent space 中相近的点，解码后不应变成完全不同的内容。

完备性（Completeness）：

> 从 chosen distribution 中采样的 latent point，解码后应产生有意义的内容。

普通 AE 只优化 reconstruction loss，没有明确约束 latent space 的形状，所以不保证满足这两个性质。

# 四、Variational Autoencoder

## 1. VAE 的核心动机

对应 PDF：p.18

变分自动编码器（Variational Autoencoder, VAE）的目标是让 autoencoder 能用于生成。为此，它在训练中加入显式正则化（Regularisation），避免 latent space 过度不规则，并让 latent space 具有良好性质。

课件定义：VAE 是一种 regularised autoencoder，用来避免 overfitting，并保证 latent space 具有支持 generative process 的性质。

## 2. VAE 编码的是分布，不是单点

对应 PDF：p.19

普通 AE 编码：

$$
x \rightarrow z
$$

VAE 编码：

$$
x \rightarrow q_\phi(z\mid x)
$$

也就是说，encoder 不输出一个固定点，而是输出 latent space 上的分布。课件说 latent distribution $p(z|x)$ 是 normal distribution。更常见的写法是近似后验：

$$
q_\phi(z\mid x)=\mathcal{N}(\mu_\phi(x),\Sigma_\phi(x))
$$

其中 encoder 输出：

$$
\mu_\phi(x),\quad \Sigma_\phi(x)
$$

或在对角协方差情况下输出：

$$
\mu_\phi(x),\quad \log\sigma_\phi^2(x)
$$

## 3. VAE loss 的两部分

对应 PDF：p.20-p.25

VAE 的损失函数由两部分组成：

1. 重构项（Reconstruction Term）：让 $\hat{x}$ 接近原始 $x$；
2. 正则化项（Regularisation Term）：让 encoder 输出的 latent distribution 接近预设分布。

通常选择标准正态先验：

$$
p(z)=\mathcal{N}(0,I)
$$

VAE loss 可以写成：

$$
\mathcal{L}
=
\mathcal{L}_{\text{rec}}
+
\mathcal{L}_{\text{reg}}
$$

常见形式为：

$$
\mathcal{L}(x)
=
-\mathbb{E}_{q_\phi(z\mid x)}
\left[\log p_\theta(x\mid z)\right]
+
D_{\mathrm{KL}}\left(q_\phi(z\mid x)\|p(z)\right)
$$

第一项要求 reconstruction 好，第二项要求 latent distribution 规则。

# 五、KL Divergence

## 1. KL divergence 的含义

对应 PDF：p.21-p.22

KL 散度（Kullback-Leibler Divergence, KL Divergence）用于衡量两个分布 $p$ 和 $q$ 的差异：

$$
D_{\mathrm{KL}}(p\|q)
=
\int p(z)\log\frac{p(z)}{q(z)}\,dz
$$

离散情形：

$$
D_{\mathrm{KL}}(p\|q)
=
\sum_z p(z)\log\frac{p(z)}{q(z)}
$$

课件强调两个性质：

1. KL divergence 非负；
2. KL divergence 为 0 当且仅当 $p=q$。

需要注意：KL divergence 不是对称距离，通常：

$$
D_{\mathrm{KL}}(p\|q)\ne D_{\mathrm{KL}}(q\|p)
$$

## 2. KL 在 VAE 中的作用

对应 PDF：p.23-p.25

VAE 用 KL 项把每个输入对应的 latent distribution 拉向标准正态：

$$
D_{\mathrm{KL}}\left(q_\phi(z\mid x)\|\mathcal{N}(0,I)\right)
$$

这样做的效果是：latent space 被组织得更连续、更完整。课件说 regularisation tends to create a “gradient” over the information encoded in the latent space。

通俗理解：普通 AE 的 latent space 可能到处是空洞；VAE 用 KL regularization 把编码分布整理到一个更可采样的空间里。

# 六、VAE 的神经网络实现

## 1. Encoder 输出 mean 和 covariance

对应 PDF：p.26-p.29

VAE 的 encoder neural network 输出 mean 和 covariance：

$$
\mu_x,\quad \Sigma_x
$$

然后从这个分布采样 latent variable：

$$
z\sim \mathcal{N}(\mu_x,\Sigma_x)
$$

decoder 接收 $z$，输出 reconstruction：

$$
\hat{x}=D_\theta(z)
$$

整个流程是：

$$
x
\rightarrow
(\mu_x,\Sigma_x)
\rightarrow
z
\rightarrow
\hat{x}
$$

## 2. 为什么采样会阻断 backpropagation

对应 PDF：p.30

如果直接写：

$$
z\sim \mathcal{N}(\mu_x,\Sigma_x)
$$

采样操作本身含有随机性，梯度难以直接从 decoder 的 loss 反传到 encoder 的 $\mu_x,\Sigma_x$。

问题不是不能采样，而是要让采样过程写成一个可微函数加外部噪声。

## 3. Reparameterization trick

对应 PDF：p.31

重参数化技巧（Reparameterization Trick）把采样写成：

$$
z=\mu_x+\sigma_x\odot \zeta,\qquad
\zeta\sim\mathcal{N}(0,I)
$$

课件写作：

$$
z=\sigma_x\zeta+\mu_x,\qquad \zeta\sim N(0,I)
$$

这样随机性来自 $\zeta$，而 $z$ 对 $\mu_x$ 和 $\sigma_x$ 是可微的：

$$
\frac{\partial z}{\partial \mu_x}=1
$$

$$
\frac{\partial z}{\partial \sigma_x}=\zeta
$$

因此 backpropagation 可以继续训练 encoder。

## 4. VAE 小结

对应 PDF：p.32-p.33

课件总结：

1. VAE 解决普通 AE latent space irregularity 的问题；
2. VAE 让 encoder 返回 latent space 上的 distribution，而不是单点；
3. VAE loss 包含 regularisation term，用来组织 latent space。

一句话：VAE 用概率分布和 KL regularization，让 autoencoder 的 decoder 可以作为生成器使用。

# 七、MNIST 上的 AE 与 VAE 示例

## 1. 普通 Autoencoder 示例

对应 PDF：p.34-p.41

课件用 MNIST 作为例子。MNIST 图像是：

$$
28\times 28
$$

普通 AE 的步骤是：

1. Train an Autoencoder on MNIST；
2. Define the encoder；
3. Define the decoder；
4. Define the auto-encoder；
5. Train the auto-encoder；
6. Visualize 2D latent space；
7. Visualize decoded 2D latent space。

观察重点不是代码细节，而是 latent space 的质量。如果普通 AE 的 latent space 不规则，那么在二维平面上随机取点解码时，某些区域可能生成不清楚或无意义的数字。

## 2. VAE 示例

对应 PDF：p.42-p.48

VAE 的步骤是：

1. Train a VAE on MNIST；
2. Define the variational encoder；
3. Define the variational auto-encoder；
4. Train the VAE；
5. Visualize 2D latent space；
6. Visualize decoded 2D latent space；
7. 使用 VAE Latent Space Explorer。

VAE 的 latent space 通常更连续。二维 latent space 中从一个点移动到另一个点，decoded image 会逐渐变化，而不是突然跳变。

这体现了前面说的 continuity 和 completeness。

# 八、Conditional VAE

## 1. 为什么需要 CVAE

对应 PDF：p.49-p.50

普通 VAE 可以生成新图像，但不能指定生成“某个数字”。例如你从 latent space 随机采样，decoder 可能生成 3，也可能生成 8，无法直接控制类别。

因此需要条件变分自动编码器（Conditional Variational Autoencoder, CVAE）。

## 2. CVAE 的结构

对应 PDF：p.51-p.53

CVAE 在 encoder 和 decoder 中都加入额外输入，通常是 label：

$$
y
$$

训练时，图像标签被提供给 encoder 和 decoder。标签用 one-hot vector 表示：

$$
\text{digit 3}=(0,0,0,1,0,0,0,0,0,0)
$$

VAE：

$$
q_\phi(z\mid x),\qquad p_\theta(x\mid z)
$$

CVAE：

$$
q_\phi(z\mid x,y),\qquad p_\theta(x\mid z,y)
$$

也就是说，decoder 不只看 latent variable $z$，还看条件 $y$。

## 3. 按类别生成

对应 PDF：p.54-p.56

CVAE 可以根据给定 label 生成对应类别的图像。例如指定 $y=7$，再采样：

$$
z\sim \mathcal{N}(0,I)
$$

输入 decoder：

$$
\hat{x}=D_\theta(z,y)
$$

就可以生成更接近数字 7 的图像。

这说明条件生成（Conditional Generation）的核心是：在生成过程中不仅提供随机 latent variable，还提供控制变量。

# 九、本讲复习抓手

## 1. 必须掌握的概念

- 生成模型（Generative Model）：学习数据分布并生成新样本。
- 判别模型（Discriminative Model）：学习类别边界或条件概率。
- 自动编码器（Autoencoder, AE）：encoder 压缩，decoder 重构。
- 潜在空间（Latent Space）：压缩后的表示空间。
- 重构误差（Reconstruction Loss）：衡量 $\hat{x}$ 和 $x$ 的差距。
- 规则潜在空间（Regular Latent Space）：具有 continuity 和 completeness。
- 变分自动编码器（Variational Autoencoder, VAE）：encoder 输出分布，并用 KL regularization 整理 latent space。
- KL 散度（KL Divergence）：衡量两个分布差异。
- 重参数化技巧（Reparameterization Trick）：让随机采样可反向传播。
- 条件 VAE（Conditional VAE, CVAE）：加入 label 等条件，实现可控生成。

## 2. 关键公式

Autoencoder：

$$
z=E_\phi(x),\qquad \hat{x}=D_\theta(z)
$$

VAE encoder：

$$
q_\phi(z\mid x)=\mathcal{N}(\mu_\phi(x),\Sigma_\phi(x))
$$

VAE loss：

$$
\mathcal{L}(x)
=
-\mathbb{E}_{q_\phi(z\mid x)}
\left[\log p_\theta(x\mid z)\right]
+
D_{\mathrm{KL}}\left(q_\phi(z\mid x)\|p(z)\right)
$$

KL divergence：

$$
D_{\mathrm{KL}}(p\|q)
=
\int p(z)\log\frac{p(z)}{q(z)}\,dz
$$

Reparameterization trick：

$$
z=\mu_x+\sigma_x\odot\zeta,\qquad \zeta\sim\mathcal{N}(0,I)
$$

CVAE：

$$
q_\phi(z\mid x,y),\qquad p_\theta(x\mid z,y)
$$

## 3. 本讲一句话

普通 Autoencoder 能压缩和重构，但 latent space 不一定适合随机采样；VAE 通过输出分布、KL regularization 和 reparameterization trick，把 autoencoder 改造成可以生成新样本的概率模型。

# 十、补充学习注释与复习路线

## 1. 本讲怎么读

这一讲对应 PDF：p.1-p.56。它从判别式任务转向生成模型（Generative Models），核心问题变成：模型不只预测标签，还要学习数据分布并生成新样本。

推荐读法：

1. p.1-p.8：先区分生成模型和判别模型（Discriminative Model）。
2. p.9-p.18：理解 Autoencoder 为什么能压缩和重构，但普通 latent space 不一定适合采样。
3. p.19-p.33：重点读 VAE、KL divergence 和 reparameterization trick。
4. p.34-p.56：用 MNIST 和 Conditional VAE 看生成效果如何被控制。

Autoencoder（AE）的结构是：

$$
x \xrightarrow{encoder} z \xrightarrow{decoder} \hat{x}
$$

训练目标通常是让重构误差变小：

$$
\ell(x,\hat{x})=\|x-\hat{x}\|^2
$$

但普通 AE 的 $z$ 是确定性编码，latent space 可能出现空洞或不连续区域。这样从 latent space 随机采样时，decoder 未必能生成合理样本。

VAE 的关键改变是：encoder 输出的不是一个点，而是一个分布。常见写法是：

$$
q_\phi(z|x)=\mathcal{N}(\mu_\phi(x),\sigma_\phi^2(x))
$$

VAE loss 可以理解成两部分：

$$
\mathcal{L}=\text{Reconstruction Loss}+\text{KL Regularization}
$$

重构项要求生成样本像原输入；KL 项要求 $q_\phi(z|x)$ 不要离先验分布 $p(z)$ 太远。常见先验是标准正态分布：

$$
p(z)=\mathcal{N}(0,I)
$$

对应 p.26-p.33 的重参数化技巧（Reparameterization Trick）要重点理解：直接从 $\mathcal{N}(\mu,\sigma^2)$ 采样会让梯度难以通过随机节点传回 encoder，所以改写成：

$$
z=\mu+\sigma\odot\epsilon,\quad \epsilon\sim\mathcal{N}(0,I)
$$

这样随机性来自 $\epsilon$，而 $\mu$ 和 $\sigma$ 仍是可微的网络输出。

Conditional VAE 对应 p.49-p.56。它把条件 $y$ 加入 encoder 和 decoder：

$$
q_\phi(z|x,y),\quad p_\theta(x|z,y)
$$

直观上，普通 VAE 是“随便生成一张像训练集的图片”，CVAE 是“在指定类别条件下生成图片”。

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
