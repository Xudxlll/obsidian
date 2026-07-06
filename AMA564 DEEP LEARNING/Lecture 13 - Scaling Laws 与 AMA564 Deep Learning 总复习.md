# Lecture 13 - Scaling Laws 与 AMA564 Deep Learning 总复习

> [!info] 资料来源
> - 课件：`Lecture13.pdf`
> - 本笔记只依据 PDF 整理。
> - 第 13 讲有 230 页，是“Scaling Laws 新内容 + 全课程总复习”。本笔记按主题整合，并保留 PDF 页码范围，方便回到课件对照。

# 一、本讲的整体地图

## 1.1 PDF 页码索引

| PDF 页码 | 内容 | 学习重点 |
|---|---|---|
| p.1-p.12 | AI Scaling Laws | 规模、数据、计算和性能之间的可预测关系 |
| p.13-p.22 | 深度学习与 DNN 总复习 | 定义、历史、MLP、activation、universality、overfitting |
| p.23-p.35 | Deep regression 与 robust loss | 经验风险、优化、异常值、LS/LAD/Huber/Cauchy/Tukey |
| p.36-p.54 | Optimization | GD、SGD、Momentum、Nesterov、AdaGrad、Adam、noise reduction |
| p.55-p.59 | Backpropagation | chain rule、one-layer perceptron、sigmoid loss 梯度 |
| p.60-p.77 | CNN 基础 | convolution、padding、pooling、receptive field |
| p.78-p.95 | Classification loss | 0-1 loss、surrogate loss、Softmax、Cross Entropy |
| p.96-p.114 | CNN architectures 与训练技巧 | LeNet、AlexNet、VGG、ResNet、DenseNet、GoogLeNet、initialization、BN、dropout、augmentation |
| p.115-p.138 | Generative models | VAE、GAN、Normalizing Flow、Score-based Models |
| p.139-p.153 | RNN 与 LSTM | RNN、Elman/Jordan、BPTT、LSTM |
| p.154-p.176 | Word Embedding、Attention、Transformer | Word2Vec、self-attention、multi-head、Transformer |
| p.177-p.192 | LLM Pretraining 与 BERT | pretraining、tokenization、BPE、BERT masking、two-sentence task |
| p.193-p.209 | PEFT、LoRA、few-shot、prompting、CoT | 参数高效微调和 prompt-based 使用 |
| p.210-p.229 | Instruction fine-tuning、RLHF、DPO | 人类偏好、reward model、RLHF、DPO |

# 二、AI Scaling Laws

## 2.1 为什么 Scaling Laws 重要

对应 PDF：p.1-p.4

Scaling Laws 试图回答一个昂贵的问题：如果我们投入更多模型参数、更多训练数据和更多计算量，模型性能会怎样变化？

课件把这称为从 “Guess & Pray” 走向 predictable science。也就是说，大模型训练不再完全靠猜，而是可以通过小规模实验预测大规模训练结果。

## 2.2 规模和损失之间的近似直线

对应 PDF：p.5

课件提到 unexpected straight line。许多 scaling law 结果显示，在 log-log 坐标下，loss 与模型规模、数据规模、计算量之间可能近似呈线性关系。

典型形式可以写成：

$$
L(N)\approx aN^{-\alpha}+b
$$

其中 $N$ 可以代表参数量、数据量或计算量，$\alpha$ 是 scaling exponent。

在 log-log 坐标中：

$$
\log(L-b)\approx \log a-\alpha\log N
$$

因此会出现近似直线。

## 2.3 预训练规模的三个杠杆

对应 PDF：p.6-p.9

课件列出 pretraining scale 的三个杠杆：

1. 模型参数量（Model Size）；
2. 数据量（Dataset Size）；
3. 训练计算量（Compute）。

实际问题不是简单“越大越好”，而是在固定预算下如何分配。例如参数太大但数据不足会浪费模型容量；数据太多但模型太小也可能无法吸收。

这就是 optimal allocation problem。

## 2.4 Scaling Laws 的边界

对应 PDF：p.10-p.12

Scaling laws 可以预测未来趋势，但课件也提醒：not everything is a straight line。

原因包括：

- 数据质量变化；
- 架构变化；
- 优化策略变化；
- 训练稳定性；
- 评估任务不完全连续；
- emergent behavior 可能在某些规模附近突然出现。

所以 scaling laws 是指导工具，不是绝对定律。

# 三、深度学习与 DNN 总复习

## 3.1 什么是 Deep Learning

对应 PDF：p.13-p.16

深度学习（Deep Learning）属于机器学习方法的一部分，基于人工神经网络（Artificial Neural Networks）和表示学习（Representation Learning）。

核心思想是：模型通过多层可学习函数，从数据中学习特征表示，而不是完全依赖人工特征工程。

## 3.2 MLP 的数学形式

对应 PDF：p.17-p.19

多层感知机（Multi-Layer Perceptron, MLP）：

$$
f_\theta(x)=
\mathcal{A}_L\circ\sigma\circ
\mathcal{A}_{L-1}\circ\sigma\circ\cdots\circ
\sigma\circ\mathcal{A}_1(x)
$$

其中：

$$
\mathcal{A}_i(x)=W_ix+b_i
$$

激活函数包括：

$$
\mathrm{ReLU}(x)=\max\{x,0\}
$$

$$
\mathrm{Sigmoid}(x)=\frac{1}{1+e^{-x}}
$$

激活函数的作用是引入非线性。没有 activation，多层线性变换仍等价于单层线性变换。

## 3.3 Universality 与深度

对应 PDF：p.20-p.22

万能逼近定理（Universal Approximation Theorem）说明神经网络可以逼近紧集上的连续函数。

任意宽度版本：浅层网络足够宽，可以逼近任意连续函数。

任意深度版本：宽度固定但足够深，也可以逼近任意连续函数。

但要注意：这只是表达能力结论，不保证训练算法一定找到最优网络，也不保证泛化。

# 四、Deep Regression 与 Robust Loss

## 4.1 Deep Nonparametric Regression

对应 PDF：p.23-p.27

神经网络回归写作：

$$
\min_{\theta}
\frac{1}{n}\sum_{i=1}^{n}
\left(Y_i-f(X_i;\theta)\right)^2
$$

或更一般：

$$
\min_{\theta}
\frac{1}{n}\sum_{i=1}^{n}
\phi(Y_i-f(X_i;\theta))
$$

优化过程是初始化、计算梯度、按步长更新、迭代停止。

## 4.2 异常值与 robust loss

对应 PDF：p.28-p.35

平方损失对异常值敏感，因为大残差会被平方放大：

$$
(Y_i-f(X_i;\theta))^2
$$

LS 对应条件均值：

$$
f^*(x)=\mathbb{E}[Y\mid X=x]
$$

LAD 对应条件中位数：

$$
f^*(x)=\mathrm{median}(Y\mid X=x)
$$

常见 robust loss：

$$
\phi_{\mathrm{LS}}(a)=a^2
$$

$$
\phi_{\mathrm{LAD}}(a)=|a|
$$

Huber loss：

$$
\phi(a)=
\begin{cases}
\frac{a^2}{2},& |a|<\tau\\
\tau |a|-\frac{\tau^2}{2},& |a|\ge\tau
\end{cases}
$$

robust loss 的直觉是降低大残差样本对训练目标的支配。

# 五、Optimization 总复习

## 5.1 Gradient Descent

对应 PDF：p.36-p.39

梯度下降（Gradient Descent, GD）：

$$
\theta^{k+1}
=
\theta^k-\alpha_k\nabla f(\theta^k)
$$

停止条件可以是：

$$
\|\nabla f(\theta^k)\|\le \epsilon
$$

对 $L$-smooth 函数，步长 $1/L$ 有理论意义。

## 5.2 Stochastic Gradient Descent

对应 PDF：p.40-p.43

当：

$$
f(\theta)=\frac{1}{n}\sum_{i=1}^{n}f_i(\theta)
$$

全梯度：

$$
\nabla f(\theta)=\frac{1}{n}\sum_{i=1}^{n}\nabla f_i(\theta)
$$

样本量很大时计算昂贵。SGD 用随机梯度估计：

$$
g(\theta,\xi)
$$

并更新：

$$
\theta^{k+1}
=
\theta^k-\alpha_k g(\theta^k,\xi_k)
$$

递减步长常满足：

$$
\sum_t\alpha_t=\infty,\qquad
\sum_t\alpha_t^2<\infty
$$

## 5.3 Momentum、Nesterov、AdaGrad、Adam

对应 PDF：p.44-p.51

SGD 问题包括收敛慢、局部最优、鞍点。

Momentum 引入速度：

$$
v_{k+1}=\gamma v_k+\alpha_k g_k
$$

$$
\theta^{k+1}=\theta^k-v_{k+1}
$$

AdaGrad 根据历史梯度调整每个坐标学习率；Adam 同时结合 momentum 和 adaptive learning rate。

Adam 推荐超参数：

$$
\alpha=0.001,\quad \beta_1=0.9,\quad \beta_2=0.999,\quad \epsilon=10^{-8}
$$

## 5.4 Noise Reduction 与 Dynamic Sample Size SGD

对应 PDF：p.52-p.54

SGD 的随机性可以用方差参数理解。课件提到 noise reduction methods，希望降低 Assumption 3.2 中的 $B$。

Dynamic Sample Size SGD 的直觉是：训练早期可以用较小 batch 快速探索，后期逐渐增加样本量，降低梯度噪声。

# 六、Backpropagation 总复习

## 6.1 Chain rule

对应 PDF：p.55-p.59

反向传播（Backpropagation）本质是链式法则（Chain Rule）。

单层感知机：

$$
z(w)=w_0+\sum_{i=1}^{n}w_ix_i
$$

$$
o(w)=\sigma(z(w))
$$

$$
L(w)=\frac{1}{2}(o(w)-y)^2
$$

对权重求导：

$$
\frac{\partial L}{\partial w_i}
=
\frac{dL}{do}
\frac{do}{dz}
\frac{\partial z}{\partial w_i}
$$

若 $\sigma$ 是 sigmoid：

$$
\frac{do}{dz}=o(1-o)
$$

所以：

$$
\frac{\partial L}{\partial w_i}
=(o-y)o(1-o)x_i
$$

# 七、CNN 总复习

## 7.1 Convolution Layer

对应 PDF：p.60-p.71

卷积层用 filter 在图像空间上滑动。对 $32\times 32\times 3$ 图像和 $5\times 5\times 3$ filter，每个位置做：

$$
5\times 5\times 3=75
$$

维点积加 bias。

输出尺寸公式：

$$
O=\frac{N+2P-F}{S}+1
$$

其中 $N$ 是输入尺寸，$F$ 是 kernel size，$S$ 是 stride，$P$ 是 padding。

## 7.2 Pooling 与 Receptive Field

对应 PDF：p.72-p.77

Pooling 是下采样策略，可以增强局部平移鲁棒性并压缩特征。

输入：

$$
D\times M\times N
$$

Pooling size $K$、stride $P$ 后：

$$
D\times
\left(\frac{M-K}{P}+1\right)
\times
\left(\frac{N-K}{P}+1\right)
$$

感受野（Receptive Field）表示输出元素依赖输入中的区域。多层卷积会扩大感受野。

# 八、Classification Loss 总复习

## 8.1 0-1 loss 与 surrogate loss

对应 PDF：p.78-p.85

分类的 0-1 loss：

$$
I(h(X_i)\ne Y_i)
$$

不连续、不光滑，难以直接优化。因此使用 surrogate loss：

$$
\min_\theta
\frac{1}{n}\sum_{i=1}^{n}
\phi(Y_if(X_i;\theta))
$$

常见替代损失：

$$
\phi_{\mathrm{exp}}(yf)=\exp(-yf)
$$

$$
\phi_{\mathrm{logistic}}(yf)=\log(1+\exp(-yf))
$$

$$
\phi_{\mathrm{hinge}}(yf)=\max\{1-yf,0\}
$$

## 8.2 Softmax 与 Cross Entropy

对应 PDF：p.86-p.95

多分类中，神经网络输出 logits：

$$
h(x;\theta)\in\mathbb{R}^{K}
$$

Softmax：

$$
\hat{p}_j=
\frac{\exp(h_j)}
{\sum_{k=1}^{K}\exp(h_k)}
$$

Cross Entropy：

$$
\mathrm{CE}(Y,\hat{p})
=
-\sum_{j=1}^{K}Y_j\log\hat{p}_j
$$

这来自 negative log likelihood。

# 九、CNN Architectures 与训练技巧

## 9.1 经典 CNN 架构

对应 PDF：p.96-p.105

LeNet-5：早期 CNN，Conv + Pooling + FC，用于手写数字识别。

AlexNet：使用 ReLU、data augmentation、dropout，在 ImageNet 上取得突破。

VGG：用多个小卷积核堆叠替代大卷积核，证明更深网络有效，但内存昂贵。

ResNet：使用 skip connection：

$$
H(x)=F(x)+x
$$

让深层网络更容易学习 identity mapping。

DenseNet：使用密集连接复用特征。

GoogLeNet：使用 Inception 模块处理多尺度特征。

## 9.2 Initialization、Normalization、Regularization

对应 PDF：p.106-p.114

Xavier initialization 目标是保持输入输出方差：

$$
\mathrm{Var}(W)=\frac{1}{n_{\text{in}}}
$$

He initialization 适合 ReLU：

$$
\mathrm{Var}(W)=\frac{2}{n_{\text{in}}}
$$

Batch Normalization：

$$
\hat{x}_j^i=
\frac{x_j^i-\mu_j}{\sqrt{\sigma_j^2+\epsilon}}
$$

带可学习参数：

$$
y_j^i=\gamma_j\hat{x}_j^i+\beta_j
$$

Dropout 随机把输入元素置零，data augmentation 通过旋转等变换增加数据多样性。

# 十、Generative Models 总复习

## 10.1 VAE

对应 PDF：p.115-p.123

VAE 让 encoder 输出 latent distribution：

$$
q_\phi(z\mid x)=\mathcal{N}(\mu_\phi(x),\Sigma_\phi(x))
$$

loss 包含 reconstruction term 和 KL regularization：

$$
\mathcal{L}(x)
=
-\mathbb{E}_{q_\phi(z\mid x)}
[\log p_\theta(x\mid z)]
+
D_{\mathrm{KL}}(q_\phi(z\mid x)\|p(z))
$$

重参数化：

$$
z=\mu_x+\sigma_x\odot\epsilon,\quad \epsilon\sim\mathcal{N}(0,I)
$$

## 10.2 GAN

对应 PDF：p.124-p.131

GAN 的 value function：

$$
\min_G\max_D
\mathbb{E}_{x\sim p_{\text{data}}}
[\log D(x)]
+
\mathbb{E}_{z\sim p_z}
[\log(1-D(G(z)))]
$$

训练困难包括 non-convergence 和 mode collapse。

## 10.3 Normalizing Flow 与 Score-based Model

对应 PDF：p.132-p.138

Normalizing Flow 使用可逆变换，并用 negative log-likelihood 训练。

Score-based model 学习：

$$
s(x)=\nabla_x\log p(x)
$$

并通过 Langevin dynamics 或 denoising 过程采样。

# 十一、RNN、LSTM 与 Word Embedding

## 11.1 RNN 与 BPTT

对应 PDF：p.139-p.150

RNN：

$$
h_t=\phi(W_xx_t+W_hh_{t-1}+b)
$$

时间反向传播（BPTT）把 RNN 沿时间展开。由于递归导数，可能出现 vanishing/exploding gradient。

## 11.2 LSTM

对应 PDF：p.151-p.153

LSTM 维护 hidden state 和 memory cell：

$$
h_t,\quad c_t
$$

核心更新：

$$
c_t=f_t\odot c_{t-1}+i_t\odot\tilde{c}_t
$$

gate 机制决定遗忘、写入和输出。

## 11.3 Word Embedding

对应 PDF：p.154-p.161

Word embedding 把词变成向量。Word2Vec 包括：

- Skip-gram：中心词预测上下文；
- CBOW：上下文预测中心词。

词向量可以表达相似性和语言关系。

# 十二、Attention 与 Transformer

## 12.1 Self-Attention

对应 PDF：p.162-p.172

给定：

$$
Q=XW^Q,\quad K=XW^K,\quad V=XW^V
$$

Self-attention：

$$
\mathrm{Attention}(Q,K,V)
=
\mathrm{Softmax}
\left(
\frac{QK^T}{\sqrt{d_k}}
\right)V
$$

它让序列中每个位置直接关注其他位置。

## 12.2 Transformer

对应 PDF：p.173-p.176

Transformer block 由 multi-head attention、feed-forward network、residual connection、normalization 构成。

Decoder 生成词时使用 masked self-attention，不能看到未来 token。

# 十三、LLM Pretraining、BERT、PEFT 与 Prompting

## 13.1 Pretraining 与 BERT

对应 PDF：p.177-p.192

LLM training 的基本流程：

$$
\text{large corpus}
\rightarrow
\text{pretrained model}
\rightarrow
\text{fine-tuning / prompting}
$$

BPE 用 subword tokenization 处理 rare words。

BERT 使用 masked language modeling：

$$
p_\theta(x\mid \tilde{x})
$$

并使用 two-sentence task 学习句间关系。

## 13.2 PEFT 与 LoRA

对应 PDF：p.193-p.200

PEFT 只训练少量参数。LoRA 把参数更新写成低秩形式：

$$
\Delta W=BA
$$

其中 $r$ 很小：

$$
B\in\mathbb{R}^{d\times r},\quad A\in\mathbb{R}^{r\times k}
$$

## 13.3 Few-shot、Prompting 与 CoT

对应 PDF：p.201-p.209

大模型出现 in-context few-shot learning，可以在 prompt 中通过示例完成任务。

Chain-of-Thought Prompting 通过中间推理步骤提升复杂推理表现。

Zero-shot CoT 使用简单提示触发推理：

```text
Let's think step by step.
```

# 十四、Instruction Fine-tuning、RLHF 与 DPO

## 14.1 Instruction Fine-tuning

对应 PDF：p.210-p.216

预训练模型不天然会遵循用户指令。Instruction fine-tuning 用指令数据训练：

$$
\text{instruction}\rightarrow \text{response}
$$

让模型更像多任务助手。

## 14.2 RLHF

对应 PDF：p.217-p.225

RLHF 使用人类偏好训练 reward model，再优化 policy：

$$
\pi_\theta(y\mid x)
$$

目标是提高人类偏好 response 的概率。

基本流程：

1. SFT；
2. 收集偏好数据；
3. 训练 reward model；
4. 用 RL 优化 policy。

## 14.3 DPO

对应 PDF：p.226-p.229

DPO（Direct Preference Optimization）直接用偏好对优化模型，不显式训练 reward model 或运行传统 RL loop。

常见 loss：

$$
\mathcal{L}_{\mathrm{DPO}}
=
-\mathbb{E}
\left[
\log\sigma
\left(
\beta\log
\frac{\pi_\theta(y_w\mid x)}
{\pi_{\mathrm{ref}}(y_w\mid x)}
-
\beta\log
\frac{\pi_\theta(y_l\mid x)}
{\pi_{\mathrm{ref}}(y_l\mid x)}
\right)
\right]
$$

其中 $y_w$ 是 preferred response，$y_l$ 是 rejected response。

# 十五、总复习框架

## 15.1 整门课的主线

本课程可以用一条线串起来：

$$
\text{model architecture}
\rightarrow
\text{loss function}
\rightarrow
\text{optimization}
\rightarrow
\text{application domain}
\rightarrow
\text{scaling and alignment}
$$

前半学期重点是基本结构和训练：

- MLP
- regression
- loss function
- backpropagation
- optimization
- CNN
- classification

中后段进入更复杂的模型：

- VAE
- GAN
- Flow
- Score-based models
- RNN/LSTM
- Word embedding
- Attention/Transformer

最后进入现代 LLM：

- pretraining
- BERT
- PEFT/LoRA
- prompting
- instruction fine-tuning
- RLHF
- DPO
- scaling laws

## 15.2 考前最应该抓的公式

MLP：

$$
f_\theta(x)=\mathcal{A}_L\circ\sigma\circ\cdots\circ\sigma\circ\mathcal{A}_1(x)
$$

GD：

$$
\theta^{k+1}=\theta^k-\alpha_k\nabla f(\theta^k)
$$

SGD：

$$
\theta^{k+1}=\theta^k-\alpha_k g(\theta^k,\xi_k)
$$

Convolution output：

$$
O=\frac{N+2P-F}{S}+1
$$

Softmax：

$$
\hat{p}_j=\frac{\exp(h_j)}{\sum_k\exp(h_k)}
$$

Cross Entropy：

$$
\mathrm{CE}=-\sum_jY_j\log\hat{p}_j
$$

VAE：

$$
\mathcal{L}
=
-\mathbb{E}_{q_\phi(z\mid x)}[\log p_\theta(x\mid z)]
+
D_{\mathrm{KL}}(q_\phi(z\mid x)\|p(z))
$$

GAN：

$$
\min_G\max_D
\mathbb{E}_{x\sim p_{\text{data}}}[\log D(x)]
+
\mathbb{E}_{z\sim p_z}[\log(1-D(G(z)))]
$$

Self-attention：

$$
\mathrm{Attention}(Q,K,V)
=
\mathrm{Softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

LoRA：

$$
\Delta W=BA
$$

DPO：

$$
\mathcal{L}_{\mathrm{DPO}}
=
-\mathbb{E}\left[\log\sigma(\text{preferred log-ratio} - \text{rejected log-ratio})\right]
$$

## 15.3 本讲一句话

Lecture 13 把深度学习从基础函数逼近、优化、视觉、生成、序列建模、Transformer，一直串到 LLM 的预训练、对齐和 scaling laws：模型越来越大，但核心仍然是结构、损失、优化、数据和计算之间的配合。
