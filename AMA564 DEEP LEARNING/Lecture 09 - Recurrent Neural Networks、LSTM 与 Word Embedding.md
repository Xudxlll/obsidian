# Lecture 09 - Recurrent Neural Networks、LSTM 与 Word Embedding

> [!info] 资料来源
> - 课件：`Lecture9.pdf`
> - 本笔记只依据 PDF 整理。
> - 本讲核心问题：如何处理序列数据？RNN 如何记住历史？为什么会有梯度消失，LSTM 如何缓解？

# 一、本讲的整体地图

## 1.1 PDF 页码索引

| PDF 页码 | 内容 | 学习重点 |
|---|---|---|
| p.1-p.2 | Overview | RNN、LSTM、word embedding |
| p.3-p.11 | Motivating examples | translation、speech-to-text、sentiment、video activity |
| p.12-p.23 | RNN 基本思想与类型 | sequence modeling、many-to-one、one-to-many、many-to-many |
| p.24-p.29 | Elman/Jordan network 与 unfolded RNN | hidden state、recurrent connection、dynamical system |
| p.30-p.37 | Backpropagation Through Time 与梯度问题 | 权重共享、递归导数、vanishing/exploding gradient |
| p.38-p.44 | LSTM 与 GRU | memory cell、gate 机制、长距离依赖 |
| p.45-p.57 | Word Embedding | one-hot、custom embedding、word similarity、linguistic relationships |
| p.58-p.71 | RNN 姓氏分类例子 | surname dataset、one-hot embedding、RNN forward、training loss、result |

# 二、为什么需要处理序列数据

## 2.1 Translation 中的上下文

对应 PDF：p.3-p.8

课件用翻译（Translation）引出序列建模。句子：

```text
He is eating a hot dog
```

和：

```text
He is a lucky dog
```

都包含单词 `dog`，但含义完全不同。第一个 `hot dog` 是食物，第二个 `dog` 是字面动物或习语中的词。模型必须根据前后文理解词义。

这说明自然语言不是一组独立 token 的集合，而是有顺序和上下文依赖的序列。

## 2.2 其他序列任务

对应 PDF：p.9-p.11

课件还列出：

- 语音转文本（Speech to Text）
- 情感分类（Sentiment Classification）
- 视频活动分类（Video Activity Classification）

这些任务有共同点：输入不是单个固定向量，而是随时间展开的序列：

$$
x_1,x_2,\ldots,x_T
$$

模型需要把历史信息传递到后续时间步。

# 三、RNN 的基本结构

## 3.1 RNN 处理 time-dependent / sequence-dependent data

对应 PDF：p.12-p.13

循环神经网络（Recurrent Neural Network, RNN）是处理时间依赖或序列依赖数据的标准结构之一。

传统神经网络通常是：

$$
\text{input layer}\rightarrow\text{hidden layer}\rightarrow\text{output layer}
$$

每个输入独立处理。而 RNN 在时间维度上共享参数，并维护隐藏状态（Hidden State）：

$$
h_t=f(W_xx_t+W_hh_{t-1}+b)
$$

输出可以写成：

$$
y_t=g(W_yh_t+c)
$$

$h_t$ 是当前时刻的记忆，它由当前输入 $x_t$ 和前一时刻隐藏状态 $h_{t-1}$ 共同决定。

## 3.2 意图识别例子

对应 PDF：p.14-p.19

课件用用户语音意图识别举例。假设输入句子由多个词组成，RNN 按顺序读入：

$$
x_1=\text{what},\quad x_2=\text{time},\quad \ldots
$$

每读一个词，隐藏状态更新一次。最后用最后一个 hidden state 判断用户意图，比如问天气、问时间、设置闹钟。

关键思想是：

> all previous inputs have an impact on the future output.

这就是 RNN 中 hidden state 的作用。

## 3.3 RNN 的输入输出类型

对应 PDF：p.20-p.23

RNN 可以有不同输入输出结构：

| 类型 | 例子 | 说明 |
|---|---|---|
| Many-to-one | sentiment classification | 多个输入 token，输出一个类别 |
| One-to-many | image captioning | 一个输入，输出一个序列 |
| Many-to-many | translation、sequence labeling | 输入序列到输出序列 |

这些结构本质上都依赖 hidden state 在时间上的传递。

# 四、Elman、Jordan 与 Unfolded RNN

## 4.1 Elman Network

对应 PDF：p.24-p.25

Elman Network 的 recurrent connection 来自 hidden state。也就是说：

$$
h_t=f(W_xx_t+W_hh_{t-1}+b)
$$

前一时刻的隐藏状态参与当前隐藏状态计算。

## 4.2 Jordan Network

对应 PDF：p.26-p.27

Jordan Network 的 recurrent connection 来自前一时刻输出。可以理解为：

$$
h_t=f(W_xx_t+W_yy_{t-1}+b)
$$

它把上一时刻输出反馈给当前时刻。

## 4.3 Unfolded over time

对应 PDF：p.28-p.29

RNN 可以展开成时间上的深层网络：

$$
h_1\rightarrow h_2\rightarrow \cdots \rightarrow h_T
$$

虽然图上看起来有 $T$ 个 cell，但它们共享同一组参数：

$$
W_x,\quad W_h,\quad W_y
$$

因此 RNN 是一个动态系统（Dynamical System）。它的状态随输入序列一步步演化。

# 五、Backpropagation Through Time

## 5.1 BPTT 的基本思想

对应 PDF：p.30-p.34

RNN 的训练使用时间反向传播（Backpropagation Through Time, BPTT）。把 RNN 在时间上展开后，就可以像普通深层网络一样从最后的 loss 向前反传。

RNN 定义为：

$$
h_t=\phi(W_xx_t+W_hh_{t-1}+b)
$$

由于同一个 recurrent weight $W_h$ 在所有时间步共享，loss 对 $W_h$ 的梯度要把每个时间步的贡献加起来：

$$
\frac{\partial L}{\partial W_h}
=
\sum_{t=1}^{T}
\frac{\partial L}{\partial h_t}
\frac{\partial h_t}{\partial W_h}
$$

而 $\frac{\partial L}{\partial h_t}$ 又会依赖后续时间步，因为 $h_t$ 会影响 $h_{t+1},h_{t+2},\ldots$。

## 5.2 Vanishing / Exploding Gradient

对应 PDF：p.35-p.37

课件指出：因为递归导数，我们需要重复乘上类似：

$$
\frac{\partial h_t}{\partial h_{t-1}}
$$

的项。如果这些项的范数长期小于 1，梯度会指数衰减，形成梯度消失（Vanishing Gradient）。如果长期大于 1，梯度会指数增长，形成梯度爆炸（Exploding Gradient）。

梯度消失的后果是：很早的输入对当前输出的影响难以被学习。RNN 会偏向短期依赖，难以捕捉长距离关系。

# 六、LSTM 与 GRU

## 6.1 LSTM 的直觉

对应 PDF：p.38-p.41

长短期记忆网络（Long Short-Term Memory, LSTM）的直觉是：创建一个额外模块，学习什么时候记住、什么时候忘记、什么时候输出信息。

除了 hidden state：

$$
h_t
$$

LSTM 还维护 memory cell：

$$
c_t
$$

memory cell 像一条相对稳定的信息通道，帮助长距离信息传播。

## 6.2 LSTM 的 gate 机制

对应 PDF：p.42-p.43

课件提到 forget gate。标准 LSTM 包含：

- 遗忘门（Forget Gate）$f_t$：决定旧记忆保留多少；
- 输入门（Input Gate）$i_t$：决定新信息写入多少；
- 输出门（Output Gate）$o_t$：决定记忆输出多少；
- 候选记忆（Candidate Cell）$\tilde{c}_t$。

常见公式为：

$$
f_t=\sigma(W_f[x_t,h_{t-1}]+b_f)
$$

$$
i_t=\sigma(W_i[x_t,h_{t-1}]+b_i)
$$

$$
\tilde{c}_t=\tanh(W_c[x_t,h_{t-1}]+b_c)
$$

$$
c_t=f_t\odot c_{t-1}+i_t\odot \tilde{c}_t
$$

$$
o_t=\sigma(W_o[x_t,h_{t-1}]+b_o)
$$

$$
h_t=o_t\odot\tanh(c_t)
$$

$\odot$ 表示逐元素乘法（Element-wise Multiplication）。

## 6.3 GRU

对应 PDF：p.44

门控循环单元（Gated Recurrent Unit, GRU）是 LSTM 的简化版本。它也使用 gate 控制信息流，但结构更少，计算更轻。

LSTM 和 GRU 都是为了解决普通 RNN 难以学习长距离依赖的问题。

# 七、Word Embedding

## 7.1 为什么需要词向量

对应 PDF：p.45-p.46

在自然语言处理（Natural Language Processing, NLP）中，词嵌入（Word Embedding）是单词的向量表示。

神经网络不能直接处理字符串，所以要把词变成向量：

$$
\text{word}\rightarrow \mathbb{R}^d
$$

## 7.2 One-hot embedding 的问题

对应 PDF：p.47-p.49

One-hot encoding 用一个很长的向量表示单词。如果词表大小是 $V$，每个词是 $V$ 维向量，只有一个位置为 1，其余为 0。

问题是：

1. 维度随词表线性增长；
2. 向量非常稀疏；
3. 无法表达词之间的相似性。

例如 `king` 和 `queen` 在 one-hot 中没有天然接近关系。

## 7.3 Custom embedding 与语义空间

对应 PDF：p.50-p.55

课件提到 custom embedding：手动选择对词汇有意义的维度。更一般地，模型可以自动学习 embedding。

好的词向量空间有两个性质：

- 相似词在空间中位置接近；
- 语言关系可以表现为向量关系。

例如词向量中可能出现：

$$
\mathrm{king}-\mathrm{man}+\mathrm{woman}\approx \mathrm{queen}
$$

课件还展示了 male-female、verb tense、country-capital 等关系。

## 7.4 常见算法

对应 PDF：p.56-p.57

课件列出 Word Embedding 相关算法，包括 Word2Vec、GloVe、FastText 等。Lecture 10 会继续讲 Word2Vec。

# 八、RNN 姓氏分类例子

## 8.1 任务设置

对应 PDF：p.58-p.60

例子使用来自 18 个国家的 surnames，目标是训练 RNN 分类器，把一个 surname 分到对应国家类别。

这是 many-to-one 任务：

$$
\text{character sequence}\rightarrow \text{country category}
$$

## 8.2 One-hot character embedding

对应 PDF：p.61-p.63

课件使用 one-hot embedding 表示字符。每个字符是一个 one-hot vector，姓氏是一串字符向量。

例如：

$$
x_1,x_2,\ldots,x_T
$$

其中 $T$ 是姓氏长度。

## 8.3 Build RNN 与 forward pass

对应 PDF：p.64-p.65

RNN 按字符顺序处理：

$$
h_t=f(W_xx_t+W_hh_{t-1}+b)
$$

最后 hidden state 用于分类：

$$
\hat{y}=\mathrm{Softmax}(W_yh_T+c)
$$

## 8.4 Training process 与 result

对应 PDF：p.66-p.71

训练时使用分类损失，例如 cross entropy。课件展示训练过程、training loss 和结果。

学习这个例子的重点是：RNN 可以处理长度不固定的输入序列，因为它逐步读取 token，并把历史信息压缩进 hidden state。

# 九、本讲复习抓手

## 9.1 必须掌握的概念

- 序列数据（Sequential Data）：具有顺序依赖的数据。
- RNN：用 hidden state 传递历史信息的神经网络。
- Hidden State：当前时刻对过去输入的压缩记忆。
- BPTT：把 RNN 沿时间展开后反向传播。
- Vanishing Gradient：长距离梯度逐渐消失。
- Exploding Gradient：长距离梯度逐渐爆炸。
- LSTM：使用 memory cell 和 gates 缓解长距离依赖问题。
- GRU：结构更简洁的 gated RNN。
- Word Embedding：词或字符的向量表示。

## 9.2 关键公式

RNN hidden state：

$$
h_t=\phi(W_xx_t+W_hh_{t-1}+b)
$$

RNN output：

$$
y_t=g(W_yh_t+c)
$$

LSTM memory update：

$$
c_t=f_t\odot c_{t-1}+i_t\odot \tilde{c}_t
$$

Many-to-one classification：

$$
\hat{y}=\mathrm{Softmax}(W_yh_T+c)
$$

## 9.3 本讲一句话

RNN 用 hidden state 处理序列，但普通 RNN 容易遇到长距离梯度问题；LSTM/GRU 通过门控机制改善信息保留，而 word embedding 则把离散词或字符变成神经网络可处理的向量。
