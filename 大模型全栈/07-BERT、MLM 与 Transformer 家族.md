---
type: 学习笔记
course: 大模型全栈
order: 7
stage: 基础原理
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/06-Transformer：Embedding、注意力与归一化|06-Transformer：Embedding、注意力与归一化]] · 下一篇：[[大模型全栈/08-句向量、池化与 Embedding 接口|08-句向量、池化与 Embedding 接口]]

> [!abstract] 学习目标
> 区分 Encoder-only、Decoder-only 和 Encoder–Decoder 的信息可见性。

## 核心理解

三类结构共享 Attention 等组件，但目标不同。Encoder-only 常用于文本理解和表示；Decoder-only 用因果约束逐 token 预测；Encoder–Decoder 将输入编码与目标生成分开，适合条件生成。

BERT 通过双向上下文学习每个位置的表示。MLM 在训练时选取部分位置作为预测目标；`fill-mask` 管道是在已有预训练模型上做推理，不会因调用一次而重新训练 BERT。NSP 是原始 BERT 的另一预训练任务，后续家族并不都保留。

原笔记中的“深层、双向、动态”可分别理解为多层表征、左右上下文融合、输出随语境变化。需要补充的是：**BERT 不会在普通填空推理中自动修改参数**。它与静态词嵌入的差别主要体现在上下文表征。

T5 等 Encoder–Decoder 模型也属于这条主线；但原笔记只留下 `t5_translation.zip` 名称，完整项目目前没有导入。

## 课堂代码怎么读

`pipeline("fill-mask", model="bert-base-chinese")` 负责分词、模型前向和候选解码。一个与多个 `[MASK]` 的返回结构可能不同，课堂分别使用单层循环和嵌套循环读取 token 与 score；score 是该填空设置下的概率输出。

> [!warning] 易错点与资料边界
> 多个 MASK 的常见管道输出不等于对所有空位组合做完整联合搜索。原文把动态掩码笼统归于 BERT 特征，实际还要区分预训练数据构造策略和上下文动态表示。

## 复盘练习

为什么 BERT 可以看到右侧词，而 GPT 训练通常不可以？

> [!question]- 参考思路
> MLM 的目标是恢复被遮住的位置，双向上下文是任务条件；GPT 的目标是预测下一个 token，读取未来目标会造成信息泄露。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

上篇保留了网页公共缩进与不间断空格，执行前需在练习副本中核对输入类型、缩进与依赖。

%% source-id: 上001 %%

> [!quote]- 大模型全栈（上）.md · Transformer 家族与预训练
> 来源：原笔记第 120–183 行。
>
> 二、Transformer家族
>
> 1. Transformer家族包括三个系列：Decoder-Only，Encoder-Only，Encoder-Decoder
>
>    2、BERT架构详解
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/Y25Q4BZHACQGC?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IlkyNVE0QlpIQUNRR0MiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6MTU3MCwiaGVpZ2h0Ijo0ODF9)
>
>    BERT的特点简单来说：深层、双向、动态
>
>    **深层**
>
>    BERT 使用多层 Transformer 编码器（Base 12 层，Large 24 层）。每一层都在前一层的表示基础上进一步抽象和融合上下文信息。
>
>    -&gt; 层数越多，模型能捕捉的语法、语义、甚至语用信息就越抽象、越丰富。
>
>    **双向**
>
>    在每一层自注意力中，每个词都可以直接看到句子中**所有其他词**（左侧和右侧）。
>
>    -&gt; 与 ELMo 那种“两个独立单向 LSTM 再拼接”的浅双向不同，BERT 是**从第一层开始就让左右信息深度融合**。
>
>    **动态**
>
>    同一个词在不同句子中的向量表示不同，因为它会**根据当前上下文实时计算**，而不是查一个固定的词向量表。
>
>    -&gt; 这解决了一词多义问题（如“bank”在“河边”和“银行”中表示完全不同）。
>
>    
>
>    3、BERT与SKIP-GRAM生成时的区别
>
>    skip-gram 是静态模型，输出的时候，固定映射为一个向量，生成的向量里面会包含所有训练时的窗口信息，但是生成的时一个固定向量，不会根据上下文变动而改变向量
>
>    BERT  是动态模型，也叫上下文模型，生成向量时，会根据输入文本内容的不同，动态输出内容，比如输入“我吃苹果”和“我买了苹果手机”，两句话里面，苹果的向量时不同的。
>
>    
>
>    4、BERT的里程碑意义
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/DGNUQBZHADAC2?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IkRHTlVRQlpIQURBQzIiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6MTQxNCwiaGVpZ2h0Ijo2NTJ9)
>
>    第一：动态词嵌入，真正做到了语义消歧，可以动态表示不同的内容
>
>    第二，统一特征表示，让NLP从手工作坊时代进入到统一模型时代。
>
>    5、预训练的任务
>
>    任务一MLM，动态掩码
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/ZC7VKBZHABAFI?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IlpDN1ZLQlpIQUJBRkkiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6ODk5LCJoZWlnaHQiOjQxMX0)
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/CN7VMBZHACAFE?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IkNON1ZNQlpIQUNBRkUiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6MTQwOCwiaGVpZ2h0Ijo2MTJ9)
>
>    
>
> 2. 自回归生成
>
> 3. KV cache
>
> 4. GPT任务是把所有任务转换成文本生成任务
>
>    
>

%% source-id: 中089 %%

> [!quote]- 大模型全栈（中）.md · MASK掩码
> 来源：原笔记第 5909–5937 行。
>
> **MASK掩码**
>
> ```python
> """
> mask掩码
> pip install transformers
>
> 如果遇到国内下载内容时失败的可以尝试加入下方代码
>
> import os
> os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
>
> """
> from transformers import pipeline
>
> masker = pipeline("fill-mask", model="bert-base-chinese")
>
> res = masker("我是一名[MASK]序员")
> print(res)
> for r in res:
>     print(f"词: {r['token_str']}, 概率: {r['score']:.4f}")
>
> res = masker("我爱吃[MASK]果, [MASK]色的圆的,甜的")
> print(res)
> for lst in res:
>     for r in lst:
>         print(f"词: {r['token_str']}, 概率: {r['score']:.4f}")
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/预训练时代.pdf#page=21|预训练时代.pdf · 第 21–41 页]]
- [[大模型全栈/资料/PDF/NLP.pdf#page=155|NLP.pdf · 第 155–168 页]]
- 关联知识：[[大模型全栈/04-Word2Vec 与上下文词向量|04-Word2Vec 与上下文词向量]]、[[大模型全栈/08-句向量、池化与 Embedding 接口|08-句向量、池化与 Embedding 接口]]、[[大模型全栈/09-BERT 文本分类与监督微调|09-BERT 文本分类与监督微调]]、[[大模型全栈/10-GPT 自回归生成与采样策略|10-GPT 自回归生成与采样策略]]。

> [!example]- 本地讲义页预览
> ![[大模型全栈/资料/PDF/预训练时代.pdf#page=29]]
