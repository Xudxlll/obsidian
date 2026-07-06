# Lecture 11 - Pretraining、BERT、PEFT、Prompting 与 RLHF

> [!info] 资料来源
> - 课件：`Lecture11.pdf`
> - 本笔记只依据 PDF 整理。
> - 本讲从 LLM training 的整体流程出发，讲 pretraining、BERT、PEFT、in-context learning、instruction fine-tuning 和 RLHF。

# 一、本讲的整体地图

## 1.1 PDF 页码索引

| PDF 页码 | 内容 | 学习重点 |
|---|---|---|
| p.1-p.6 | LLM training overview 与 pretraining revolution | 大规模数据、无标签数据、compute-aware scaling |
| p.7-p.10 | Tokenization 与 BPE | 子词切分解决 rare words 和词表规模问题 |
| p.11-p.15 | Past vs modern pretraining | 从随机初始化转向大规模预训练参数初始化 |
| p.16-p.25 | BERT | encoder-only、masking、two-sentence task、empirical results |
| p.26-p.32 | PEFT、Pruning、LoRA | 参数高效微调，低秩适配 |
| p.33-p.50 | Scale、few-shot learning、prompting、CoT | 大模型涌现能力，prompting 无需梯度更新但有上下文限制 |
| p.51-p.63 | Instruction fine-tuning | 让模型从语言模型变成多任务助手 |
| p.64-p.83 | RLHF 与 InstructGPT/ChatGPT | 人类偏好、reward model、policy gradient、RLHF pipeline |

# 二、LLM Training 的整体视角

## 2.1 Pretraining revolution 的三个关键

对应 PDF：p.3-p.6

大语言模型训练（LLM Training）通常不是从一个具体任务开始训练，而是先进行大规模预训练（Pretraining）。

课件列出 pretraining 的三个关键：

1. 模型必须能处理大规模、多样化数据；
2. 使用无标签数据（Unlabeled Data）；
3. 计算感知的扩展（Compute-aware Scaling）。

预训练的核心价值是：让模型先从海量文本中学习语言结构、事实知识、推理模式和世界模式，再通过 fine-tuning 或 prompting 适配具体任务。

## 2.2 为什么无标签数据重要

对应 PDF：p.6

监督学习需要人工标签，而互联网上大量文本没有人工任务标签。语言模型的预训练把文本本身变成监督信号，例如预测被遮住的词或预测下一个词。

这让模型可以利用远大于人工标注数据的数据规模。

# 三、Tokenization 与 BPE

## 3.1 为什么需要 tokenization

对应 PDF：p.7

分词（Tokenization）把原始文本转换成模型能处理的 token 序列。模型实际看到的不是完整字符串，而是 token id：

$$
\text{text}\rightarrow (t_1,t_2,\ldots,t_n)
$$

好的 tokenizer 要平衡：

- 词表不能太大；
- token 序列不能太长；
- rare words 也要能表示。

## 3.2 Byte Pair Encoding

对应 PDF：p.8-p.10

BPE（Byte Pair Encoding）是一种子词分词算法。它反复合并文本中最常见的相邻字符或子词对，直到达到指定词表规模。

常见词会成为完整 subword，稀有词会被拆成多个组件。课件总结：

> Common words end up being a part of the subword vocabulary, while rarer words are split into components.

例如一个罕见词不需要被当作 unknown token，而可以拆成可组合的 subword。

# 四、Pretraining Paradigm

## 4.1 过去的 pretraining 问题

对应 PDF：p.11

过去如果直接用下游任务数据训练模型，会遇到两个问题：

1. 下游任务数据可能不足以教会模型语言上下文；
2. 大部分网络参数随机初始化。

这意味着模型不仅要学任务，还要从小数据中学语言本身，难度很大。

## 4.2 Modern Pretraining

对应 PDF：p.12-p.15

现代预训练范式：

1. 几乎所有参数先通过 pretraining 初始化；
2. 预训练任务会隐藏输入的一部分，让模型重构；
3. 再用 fine-tuning 适配下游任务。

流程可以写成：

$$
\text{large unlabeled corpus}
\rightarrow
\text{pretrained model}
\rightarrow
\text{fine-tuned model}
$$

这就是 modern pretraining/fine-tuning paradigm。

# 五、BERT

## 5.1 BERT 的定位

对应 PDF：p.16-p.19

BERT（Bidirectional Encoder Representations from Transformers）是基于 Transformer encoder 的预训练模型。

课件强调：BERT 使用 encoder-only architecture。Encoder 能获得双向上下文（Bidirectional Context），这对理解任务很强。

但因为 encoder 能看到左右两边，所以不能直接做普通自回归语言建模：

$$
p(x_t\mid x_1,\ldots,x_{t-1})
$$

因此 BERT 使用 masked language modeling。

## 5.2 Masked Language Modeling

对应 PDF：p.20-p.21

BERT 随机 mask 15% 的词，并训练模型预测这些词。

在被选中的 15% 中：

- 80% 替换成 `[MASK]`；
- 10% 替换成随机 token；
- 10% 保持不变，但仍然预测。

如果 $\tilde{x}$ 是 masked version of $x$，训练目标是：

$$
p_\theta(x\mid \tilde{x})
$$

这种任务允许模型利用左右上下文预测被遮住的 token。

## 5.3 Two Sentences Task

对应 PDF：p.22-p.23

为了让 BERT 更好处理句子间关系，预训练还包含两句子任务：给定句子 A 和 B，判断 B 是否可能是 A 的后续句子。

这个任务帮助模型学习 sentence-level relationship，适用于问答、自然语言推断等任务。

## 5.4 BERT 架构和结果

对应 PDF：p.24-p.25

BERT 的核心是多层 Transformer encoder。输入包括 token embedding、segment embedding 和 positional embedding。

课件提到 empirical results，说明 BERT 在多种 NLP 任务上取得了强效果。它的重要意义是：预训练 encoder 可以成为通用语言理解基础。

# 六、Parameter-Efficient Fine-Tuning

## 6.1 为什么需要 PEFT

对应 PDF：p.26-p.29

大模型参数量巨大，如果每个任务都 full fine-tuning，成本很高，也需要保存完整模型副本。

参数高效微调（Parameter-Efficient Fine-Tuning, PEFT）希望只更新少量参数，让大部分预训练参数保持冻结。

## 6.2 Pruning 与 Lottery Ticket

对应 PDF：p.27-p.28

Pruning 关注哪些参数结构真正有用。课件引用 Lottery Ticket Hypothesis，核心直觉是：大网络中可能存在稀疏子网络，只要初始化合适，也能训练出好性能。

这提醒我们：不是所有参数都同等重要。

## 6.3 LoRA

对应 PDF：p.31-p.32

LoRA（Low-Rank Adaptation）通过低秩矩阵近似参数更新。原本 full fine-tuning 会学习一个完整更新：

$$
\Delta W\in\mathbb{R}^{d\times k}
$$

LoRA 假设这个更新可以低秩分解：

$$
\Delta W=BA
$$

其中：

$$
B\in\mathbb{R}^{d\times r},\quad
A\in\mathbb{R}^{r\times k},\quad r\ll \min(d,k)
$$

训练时冻结原始权重 $W$，只训练 $A,B$：

$$
Wx+\Delta Wx = Wx+BAx
$$

这样显著减少可训练参数。

# 七、Scale、Few-shot Learning 与 Prompting

## 7.1 Scale 的祝福

对应 PDF：p.33-p.38

课件进入 few-shot learner、in-context learning、instruction fine-tuning、RLHF。先强调 scale 的作用：随着模型规模、数据规模和训练计算增加，语言模型出现新的能力，例如 planning、math problems、coding problems。

GPT-3 展示了 emergent few-shot learning：模型可以从 prompt 中的几个例子学习任务格式，而不需要梯度更新。

## 7.2 In-context Learning

对应 PDF：p.39-p.43

In-context learning 指模型在上下文中看到示例，然后按示例完成新任务。它不更新参数，只改变输入 prompt。

形式上：

```text
Example 1
Example 2
Example 3
New input -> ?
```

模型根据上下文模式生成答案。

## 7.3 Prompt Engineering 与 CoT

对应 PDF：p.44-p.49

Prompting 的局限是：模型表现可能对 prompt 很敏感。课件说 solution: change the prompt。

链式思维提示（Chain-of-Thought Prompting, CoT）通过让模型写出中间推理步骤，提升复杂推理任务表现。

Zero-shot CoT 则用类似：

```text
Let's think step by step.
```

这样的提示，让模型在没有示例的情况下产生推理过程。

## 7.4 Prompting 的优缺点

对应 PDF：p.50

优点：

- 不需要 fine-tuning；
- prompt engineering 例如 CoT 可以提升表现。

缺点：

- 上下文长度有限；
- 复杂任务可能仍然需要梯度更新。

# 八、Instruction Fine-tuning

## 8.1 为什么 LLM 不能直接作为助手

对应 PDF：p.51-p.53

预训练语言模型只是学习下一个 token 或 masked token 的分布，不天然知道“如何遵循用户指令”。因此课件说 LLMs cannot assist users directly。

要让模型变成助手，需要 instruction fine-tuning。

## 8.2 Instruction fine-tuning 的目标

对应 PDF：p.54-p.63

Instruction fine-tuning 使用大量指令-回答数据，让模型学习：

$$
\text{instruction}\rightarrow \text{helpful response}
$$

课件提到 scaling it up、instruction pretraining、new benchmark、MMLU progress、huge diversity of data、you do not need many samples。

这里的核心是：高质量、多样化任务数据能让模型更好地泛化到新指令。

# 九、RLHF 与 InstructGPT

## 9.1 Instruction fine-tuning 的局限

对应 PDF：p.64-p.66

Instruction fine-tuning 能让模型学会遵循指令，但不一定保证输出符合人类偏好。比如回答可能不够 helpful、harmless、honest，或风格不符合用户需求。

因此需要优化人类偏好（Human Preferences）。

## 9.2 RLHF Pipeline

对应 PDF：p.67-p.70

RLHF（Reinforcement Learning with Human Feedback）的基本流程：

1. 先有预训练模型；
2. 用 instruction data 做 supervised fine-tuning；
3. 收集人类偏好比较数据；
4. 训练 reward model；
5. 用强化学习优化 policy model。

## 9.3 Policy Gradient 的直觉

对应 PDF：p.71-p.75

强化学习中，模型是 policy：

$$
\pi_\theta(y\mid x)
$$

它给定 prompt $x$，生成 response $y$。reward model 给出：

$$
r(x,y)
$$

目标是最大化期望奖励：

$$
\mathbb{E}_{y\sim\pi_\theta(\cdot\mid x)}[r(x,y)]
$$

Policy gradient 的核心是：如果某个输出获得高 reward，就提高生成它的概率；低 reward 则降低概率。

## 9.4 Reward Model 与 RLHF

对应 PDF：p.76-p.78

课件强调 make your reward model work first。Reward model 是 RLHF 的关键，因为后续强化学习优化的是它给出的偏好信号。

如果 reward model 学错，人类偏好优化就会偏离目标。

## 9.5 InstructGPT 与 ChatGPT

对应 PDF：p.79-p.83

InstructGPT 使用约 30K tasks，并通过 instruction fine-tuning + RLHF 让模型更擅长遵循指令。

ChatGPT 可以理解为面向对话智能体的 instruction fine-tuning + RLHF。它不仅要回答问题，还要维持对话上下文、遵循用户意图，并生成符合人类偏好的回复。

# 十、本讲复习抓手

## 10.1 关键概念

- 预训练（Pretraining）：在大规模无标签数据上学习通用表示。
- Tokenization：把文本切成 token。
- BPE：通过频繁 pair 合并学习 subword vocabulary。
- BERT：encoder-only、bidirectional、masked language modeling。
- PEFT：只更新少量参数完成任务适配。
- LoRA：用低秩矩阵表示参数更新。
- In-context Learning：不更新参数，在上下文中学习任务。
- CoT：让模型输出中间推理步骤。
- Instruction Fine-tuning：用指令数据训练模型遵循任务。
- RLHF：用人类偏好训练 reward model，再优化模型输出。

## 10.2 关键公式

BERT masked LM：

$$
p_\theta(x\mid \tilde{x})
$$

LoRA：

$$
\Delta W=BA,\quad r\ll \min(d,k)
$$

Policy：

$$
\pi_\theta(y\mid x)
$$

RLHF reward objective：

$$
\max_\theta
\mathbb{E}_{y\sim\pi_\theta(\cdot\mid x)}
[r(x,y)]
$$

## 10.3 本讲一句话

现代 LLM 先通过大规模预训练获得通用能力，再通过 BERT-style masking、PEFT/LoRA、prompting、instruction fine-tuning 和 RLHF 等方法，把语言模型逐步变成能理解任务、遵循指令并贴近人类偏好的助手。
