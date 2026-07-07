> [!info] 资料来源
> - 课件：`Lecture10.pdf`
> - 本笔记只依据 PDF 整理。
> - 本讲从 Word2Vec 进入 Attention，再完整解释 Self-Attention、Multi-head Attention、Positional Encoding 和 Transformer。

# 一、本讲的整体地图

## 1. PDF 页码索引

| PDF 页码 | 内容 | 学习重点 |
|---|---|---|
| p.1-p.8 | Word Embedding 复习 | 词向量、相似性、语言关系、Word2Vec/GloVe/FastText |
| p.9-p.17 | Word2Vec：Skip-gram 与 CBOW | 用上下文预测目标或用目标预测上下文 |
| p.18-p.23 | Hierarchical Softmax 与 Negative Sampling | 大词表下 Softmax 计算太贵，需要近似技巧 |
| p.24-p.33 | Attention 高层直觉 | encoder-decoder 中 attention 帮助模型关注相关输入 |
| p.34-p.47 | Self-Attention 细节 | Q/K/V、相似度、缩放、Softmax、加权求和、矩阵形式 |
| p.48-p.60 | Transformer | multi-head attention、positional encoding、residual connection、attention block |
| p.61-p.66 | Decoder 与训练设置 | masked self-attention、输出词预测、WMT 数据、Adam 与 regularization |
| p.67-p.70 | 应用：BERT、GPT-3 | Transformer 架构成为现代 NLP 和 LLM 基础 |

# 二、Word Embedding 回顾

## 1. 词向量的目标

对应 PDF：p.3-p.8

词嵌入（Word Embedding）把单词表示为向量：

$$
\text{word}\rightarrow \mathbb{R}^d
$$

好的 embedding 应该让语义相近的词在向量空间中接近，并能表达一些语言关系。例如：

$$
\mathrm{king}-\mathrm{man}+\mathrm{woman}\approx\mathrm{queen}
$$

课件列出常见算法：

- Word2Vec
- GloVe
- FastText

本讲重点是 Word2Vec 和 Attention。

# 三、Word2Vec

## 1. Skip-gram Model

对应 PDF：p.9-p.13

Skip-gram 的目标是：给定中心词，预测它前后窗口中的上下文词。

例如句子：

```text
The wide road shimmered in the hot sun.
```

如果中心词是 `road`，窗口大小为 2，则上下文可能包括 `The`、`wide`、`shimmered`、`in`。

输入词先用 one-hot 向量表示：

$$
x\in\mathbb{R}^{V}
$$

其中 $V$ 是词表大小。通过 embedding matrix：

$$
W\in\mathbb{R}^{V\times d}
$$

得到词向量：

$$
v=W^Tx
$$

课件强调：embedding matrix $W$ 的每一行就是一个词的 embedding。

## 2. CBOW Model

对应 PDF：p.14-p.16

连续词袋模型（Continuous Bag-of-Words, CBOW）方向相反：给定上下文词，预测中心词。

例如句子：

```text
The quick brown fox jumps over the lazy dog.
```

窗口大小为 2 时，可以用中心词左右的词来预测中心词。

Skip-gram：

$$
\text{center word}\rightarrow\text{context words}
$$

CBOW：

$$
\text{context words}\rightarrow\text{center word}
$$

## 3. 大词表问题

对应 PDF：p.18

如果词表非常大，完整 Softmax 的分母需要对所有词求和：

$$
\sum_{j=1}^{V}\exp(s_j)
$$

$V$ 很大时，每次训练都计算完整分母非常昂贵。

因此 Word2Vec 使用一些技巧降低计算成本。

## 4. Hierarchical Softmax 与 Negative Sampling

对应 PDF：p.19-p.23

层次 Softmax（Hierarchical Softmax）用树结构替代完整 Softmax，使预测一个词变成沿树路径做一系列二分类。

负采样（Negative Sampling）则把多分类问题转成若干二分类：真实上下文词是正样本，从噪声分布抽取一些词作为负样本。

直觉上，模型不需要每次都区分所有词，只需要把真实词和少量负样本区分开。

# 四、Attention 的高层直觉

## 1. Translation task 中的问题

对应 PDF：p.24-p.28

机器翻译通常使用 encoder-decoder 结构：

$$
\text{source sentence}\rightarrow \text{encoder}\rightarrow \text{representation}
\rightarrow \text{decoder}\rightarrow \text{target sentence}
$$

如果只用一个固定向量压缩整句信息，长句子会丢失细节。Attention 的思想是：decoder 生成每个词时，不必只依赖一个固定向量，而是可以关注 source sentence 中相关部分。

## 2. Attention layer 的作用

对应 PDF：p.29-p.33

课件说 attention layer helps the model focus on the right parts of the data。

概念上，attention 会给每个输入词的 embedding 一个权重：

$$
\alpha_1,\alpha_2,\ldots,\alpha_T
$$

然后加权求和：

$$
c=\sum_{t=1}^{T}\alpha_t v_t
$$

权重越大，表示当前输出更应该关注那个输入位置。

# 五、Self-Attention

## 1. 为什么需要 Self-Attention

对应 PDF：p.34-p.36

Self-attention 让序列中每个位置都可以直接关注序列中其他位置。

课件例句：

```text
The animal didn't cross the street because it was too tired.
```

这里 `it` 指代 `animal` 还是 `street`？模型需要利用上下文判断。Self-attention 可以让 `it` 直接与其他词建立联系。

与 LSTM 相比，self-attention 不需要一步一步把信息传过去；任意两个位置可以通过 attention 直接交互。

## 2. Q、K、V

对应 PDF：p.37-p.38

给定输入 embedding $x$，self-attention 为每个位置计算：

- Query vector：$q$
- Key vector：$k$
- Value vector：$v$

它们由可学习矩阵得到：

$$
q=xW^Q,\quad k=xW^K,\quad v=xW^V
$$

可以这样理解：

- Query 表示“我想找什么信息”；
- Key 表示“我有什么特征可被匹配”；
- Value 表示“如果被关注，我实际提供什么内容”。

## 3. Attention score

对应 PDF：p.39-p.41

一个位置的 query 与其他位置的 keys 做点积，得到相似度：

$$
\mathrm{score}_{ij}=q_i^Tk_j
$$

为了控制数值尺度，除以：

$$
\sqrt{d_k}
$$

其中 $d_k$ 是 key 的维度。

然后使用 Softmax 得到权重：

$$
\alpha_{ij}
=
\frac{\exp(q_i^Tk_j/\sqrt{d_k})}
{\sum_{\ell}\exp(q_i^Tk_\ell/\sqrt{d_k})}
$$

## 4. 加权 Value 得到输出

对应 PDF：p.42-p.43

用 attention weights 加权 value vectors：

$$
o_i=\sum_j \alpha_{ij}v_j
$$

这就是位置 $i$ 的 self-attention 输出。它整合了整个序列中与当前位置相关的信息。

## 5. 矩阵形式

对应 PDF：p.44-p.46

把所有位置堆成矩阵：

$$
Q=XW^Q,\quad K=XW^K,\quad V=XW^V
$$

Scaled dot-product attention 为：

$$
\mathrm{Attention}(Q,K,V)
=
\mathrm{Softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

这是 Transformer 中最核心的公式。

# 六、Transformer

## 1. 从一个 attention 到 multi-head attention

对应 PDF：p.48-p.54

多头注意力（Multi-head Attention）的动机：

1. 增强模型关注不同位置的能力；
2. 让不同 head 学习不同关系；
3. 增加表示子空间的多样性。

每个 head 都有自己的：

$$
W_i^Q,\quad W_i^K,\quad W_i^V
$$

计算：

$$
\mathrm{head}_i
=
\mathrm{Attention}(XW_i^Q,XW_i^K,XW_i^V)
$$

然后拼接并投影：

$$
\mathrm{MultiHead}(X)
=
\mathrm{Concat}(\mathrm{head}_1,\ldots,\mathrm{head}_h)W^O
$$

## 2. Positional Encoding

对应 PDF：p.54-p.57

Self-attention 本身不包含顺序信息。如果打乱输入位置，attention 公式本身无法知道词的顺序。因此需要位置编码（Positional Encoding）。

课件说：创建一个与 embedding 同维度的额外向量，帮助模型确定每个词的位置或词之间的距离。

经典 Transformer 使用正弦/余弦位置编码：

$$
PE_{(pos,2i)}
=
\sin\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)
$$

$$
PE_{(pos,2i+1)}
=
\cos\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)
$$

输入变为：

$$
X_{\text{input}}=X_{\text{embedding}}+PE
$$

## 3. Residual connection 与 attention block

对应 PDF：p.58-p.60

Transformer encoder block 通常包括：

1. Multi-head self-attention；
2. Residual connection；
3. Layer normalization；
4. Feed-forward network；
5. Residual connection；
6. Layer normalization。

课件特别展示 residual connection。它与 ResNet 中的思想类似，用来帮助深层网络训练：

$$
y=x+F(x)
$$

# 七、Decoder 与训练

## 1. Decoder 的 masked self-attention

对应 PDF：p.61-p.63

Transformer decoder 中的 self-attention 只能关注当前位置之前的 tokens，不能看到未来。课件称之为 masking future positions。

这是因为生成任务中，预测第 $t$ 个词时只能依赖：

$$
y_1,\ldots,y_{t-1}
$$

不能偷看：

$$
y_{t+1},y_{t+2},\ldots
$$

## 2. 输出词预测

对应 PDF：p.63-p.64

decoder 输出经过 linear layer 和 Softmax，转换成词表上的概率分布：

$$
p(y_t\mid y_{<t},x)
$$

训练时最大化真实目标句子的 likelihood，或最小化 cross entropy。

## 3. Transformer 训练设置

对应 PDF：p.65-p.66

课件提到 WMT 2014 English-German 数据集，约 4.5M sentence pairs，vocabulary token size 为 37000。

优化器使用 Adam：

$$
\beta_1=0.9,\quad \beta_2=0.98,\quad \epsilon=10^{-9}
$$

并配合学习率调度和 regularization。

# 八、应用：BERT 与 GPT-3

## 1. BERT

对应 PDF：p.67-p.69

BERT 是基于 Transformer encoder 的预训练模型，强调双向上下文（Bidirectional Context）。它适合理解类任务，例如文本分类、问答、句子关系判断。

## 2. GPT-3

对应 PDF：p.70

GPT-3 是大规模自回归语言模型（Autoregressive Language Model），使用 Transformer decoder 结构，通过预测下一个 token 学习语言建模。

Lecture 10 的结尾把课程自然引向 LLM training：Transformer 已经成为现代大语言模型的核心架构。

# 九、本讲复习抓手

## 1. 必须掌握的概念

- Word2Vec：用上下文学习词向量。
- Skip-gram：中心词预测上下文。
- CBOW：上下文预测中心词。
- Negative Sampling：用少量负样本近似大词表训练。
- Attention：为不同输入位置分配权重。
- Self-Attention：序列内部位置互相关注。
- Query/Key/Value：attention 中的匹配与信息载体。
- Multi-head Attention：多个 attention head 并行关注不同关系。
- Positional Encoding：补充序列顺序信息。
- Masked Self-Attention：decoder 中禁止关注未来 token。

## 2. 关键公式

Scaled dot-product attention：

$$
\mathrm{Attention}(Q,K,V)
=
\mathrm{Softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

Multi-head attention：

$$
\mathrm{MultiHead}(X)
=
\mathrm{Concat}(\mathrm{head}_1,\ldots,\mathrm{head}_h)W^O
$$

Positional encoding：

$$
PE_{(pos,2i)}
=
\sin\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)
$$

$$
PE_{(pos,2i+1)}
=
\cos\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)
$$

## 3. 本讲一句话

Word embedding 让词变成向量，attention 让模型动态选择相关信息，Transformer 则用 self-attention、multi-head、positional encoding 和 residual block 组成现代 NLP 与 LLM 的基础架构。

# 十、补充学习注释与复习路线

## 1. 本讲怎么读

这一讲对应 PDF：p.1-p.70。它从 Word2Vec 过渡到 Attention 和 Transformer，是理解现代 NLP 与大语言模型（Large Language Models, LLMs）的关键桥梁。

推荐按四层读：

1. p.1-p.23：Word2Vec 说明词向量如何从上下文预测任务中学出来。
2. p.24-p.33：Attention 解决 encoder-decoder 中“所有信息挤进一个向量”的问题。
3. p.34-p.47：Self-Attention 给出 Q/K/V 的具体计算。
4. p.48-p.70：Transformer 把 multi-head attention、positional encoding、residual connection 组合成可扩展架构。

Word2Vec 的 Skip-gram 任务是：

$$
\text{center word}\rightarrow \text{context words}
$$

CBOW 则相反：

$$
\text{context words}\rightarrow \text{center word}
$$

这两个任务的共同点是：通过预测上下文，让模型把语义相近、上下文相似的词放到相近向量空间里。p.18-p.23 的 negative sampling 要看成计算近似：完整 Softmax 太贵，所以每次只让模型区分真实词和少量负样本。

Self-Attention 对应 p.34-p.47。给定输入表示 $X$，先线性变换成：

$$
Q=XW_Q,\quad K=XW_K,\quad V=XW_V
$$

然后计算注意力：

$$
\mathrm{Attention}(Q,K,V)
=\mathrm{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

可以这样理解：

- Query（Q）：当前位置想找什么信息；
- Key（K）：每个位置提供什么索引；
- Value（V）：真正被加权汇总的信息内容。

$QK^T$ 衡量位置之间的相关性，Softmax 把相关性变成权重，乘以 $V$ 得到上下文加权表示。

Transformer 对应 p.48-p.70。Multi-head Attention 不是重复计算同一件事，而是让不同 head 学不同关系，例如语法依赖、长距离指代、局部搭配等。Positional Encoding 则弥补 self-attention 本身不含顺序信息的问题。Residual connection 和 Layer Normalization 让深层堆叠更稳定。

复习本讲时，可以用一句话检查自己是否理解：**Transformer 的核心不是简单替代 RNN，而是用 self-attention 让序列中任意两个位置直接交互，并通过并行计算提升可扩展性。**

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
