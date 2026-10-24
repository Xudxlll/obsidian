---
type: 学习笔记
course: 大模型全栈
order: 6
stage: 基础原理
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/05-RNN、LSTM、GRU 与 Seq2Seq|05-RNN、LSTM、GRU 与 Seq2Seq]] · 下一篇：[[大模型全栈/07-BERT、MLM 与 Transformer 家族|07-BERT、MLM 与 Transformer 家族]]

> [!abstract] 学习目标
> 把结构图连成一条能解释张量流向的计算路径。

## 核心理解

输入文字先转成 token ID，再查嵌入矩阵，并加入位置信息。原始 Transformer 使用正弦、余弦位置编码，例如：

$$
PE_{pos,2i}=\sin\left(pos/10000^{2i/d}\right),\quad
PE_{pos,2i+1}=\cos\left(pos/10000^{2i/d}\right)
$$

自注意力从同一输入投影得到 $Q=XW_Q$、$K=XW_K$、$V=XW_V$，计算：

$$
\operatorname{Attention}(Q,K,V)=\operatorname{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}+M\right)V
$$

$QK^\top$ 衡量位置之间的匹配程度，Softmax 沿候选 Key 的维度归一化，再对 Value 加权。多头注意力让不同投影子空间并行建模关系；各头拼接后再投影回模型维度。

残差连接要求相加两侧形状一致。LayerNorm 在每个 token 的特征维度上归一化；“横着/竖着”只是固定画法下的辅助说法。原始 Post-LN 与后来常见的 Pre-LN 顺序不同，读结构图时应确认位置。

## 课堂代码怎么读

原文先给位置编码与结构图，再讲 Q/K/V、多头、残差、LayerNorm 和 Decoder 掩码。阅读时选一个长度为 T、隐藏维度为 d 的输入，逐层标出 T×d、T×T 和 T×d；图中公式缺少可复制文本的地方，可用本篇公式对照 PDF。

> [!warning] 易错点与资料边界
> 课堂“随机初始化矩阵”描述的是参数的初始状态，训练后矩阵是学习得到的。LayerNorm 不是对整批样本统一计算统计量；Encoder 输出也不是必然压缩成一个单独句向量。

## 复盘练习

为什么注意力权重乘 V 后，输出仍可保留每个 token 的位置？

> [!question]- 参考思路
> 注意力矩阵的每一行对应一个 Query 位置。每行分别对各 Value 加权，所以输出仍有 T 行，而不是把整句话只平均成一行。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

上篇保留了网页公共缩进与不间断空格，执行前需在练习副本中核对输入类型、缩进与依赖。

%% source-id: 上000 %%

> [!quote]- 大模型全栈（上）.md · Transformer 结构
> 来源：原笔记第 1–119 行。
>
>
> Transformer 内容梳理
>
> 1.Positional Encoding热力图
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/RZG7OAJHACQGI?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IlJaRzdPQUpIQUNRR0kiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6MTc3OSwiaGVpZ2h0Ijo5NDV9)
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/2Y3KMAZHABQEE?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IjJZM0tNQVpIQUJRRUUiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6NTM2LCJoZWlnaHQiOjExOH0)
>
>
>
> **嵌入层（Embedding Layer）：**
>
> **词嵌入（Word Embedding）**：每个分词ID通过嵌入矩阵转换为固定维度的向量（如512维），捕捉语义信息。
>
> **位置编码（Positional Encoding）**：为每个分词添加位置编码向量，弥补Transformer自注意力机制无
>
> 法捕捉序列顺序的缺陷。位置编码公式为：
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/32DQAARHAAAAI?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IjMyRFFBQVJIQUFBQUkiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6ODI2LCJoZWlnaHQiOjkwfQ)
>
>
>
> 为分词位置， 为向量维度索引， 为嵌入维度。
>
> 为了做先后位置的区别
>
> 2.模型架构
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/3652MAZHABQBU?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IjM2NTJNQVpIQUJRQlUiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6NDI2LCJoZWlnaHQiOjU2MH0)
>
> 3.Encoder 中注意力的计算
>
> 3.1 自注意力
>
> 自注意力机制的核心思想是让模型在处理序列中的每个词时，都能够考虑到整个序列中的其他词，从而捕捉到序
>
> 列内部的关联性和特征。为了实现这一点，模型会为序列中的每个词计算出三个不同的向量：Query向量（Q）、Key
>
> 向量（K）和Value向量（V）。
>
> 这些向量是通过将词的嵌入向量与一个随机初始化的矩阵相乘得到的。
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/I3SQ2ARHAAQDW?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IkkzU1EyQVJIQUFRRFciLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6NTUyLCJoZWlnaHQiOjQxNX0)
>
> 3.2 自注意力的计算
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/LUDBSARHADACS?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IkxVREJTQVJIQURBQ1MiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6NjU5LCJoZWlnaHQiOjY3NH0)
>
> 这里面的z1,z2相当于 Q = q1,q2 时候，获得的查询结果。
>
> 4.多头注意力的计算
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/HGRAOARHACAFS?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IkhHUkFPQVJIQUNBRlMiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6ODgxLCJoZWlnaHQiOjM5NH0)
>
> 5.全流程
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/DJLNIARHABQCC?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IkRKTE5JQVJIQUJRQ0MiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6MTE3NywiaGVpZ2h0Ijo2MjV9)
>
>
>
> 6.残差相加
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/JZUDUARHAAAES?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IkpaVURVQVJIQUFBRVMiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6NTU1LCJoZWlnaHQiOjM1N30)
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/KLADWARHACAEU?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IktMQURXQVJIQUNBRVUiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6NzgyLCJoZWlnaHQiOjEwN30)
>
> 注意保持输入和多头注意力输出内容的shape一致
>
>
>
> 7.LayerNorm
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/ZJNUAARHADQEC?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IlpKTlVBQVJIQURRRUMiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6NzkwLCJoZWlnaHQiOjUyNX0)
>
> 机器学习阶段，我们会对所有的样本，统一进行归一化。
>
> 深度学习阶段，由于数据量比较大，我们一般对批次数据，对的所有样本的单个特征通道进行归一化。
>
> transformer里面，进行层归一化，对单个样本的所有特征进行归一化。
>
>
>
> 简单来说一句话总结，竖着归一化叫做Batch Norm，横着归一化叫做 Layer Norm
>
>
>
> 8.Decoder 端 Masked 矩阵
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/ICMOIARHACAF6?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IklDTU9JQVJIQUNBRjYiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6OTQyLCJoZWlnaHQiOjM2OX0)
>
> 这里可以看到，对于任意一行（即任意一个query）而言，能够影响最终权重的只有该query及之前的信息
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/OKZ6OARHAAAG4?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6Ik9LWjZPQVJIQUFBRzQiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6MTUxOCwiaGVpZ2h0Ijo3MzV9)
>
> 如果左侧输入是中文，则右侧输入是英文，示例：
>
> 输入（Source）： 我 喜欢 自然语言处理 ， 我 爱 学习
>
> 目标（Target）： I like NLP , I love learning 
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/FDQOSARHACQFU?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IkZEUU9TQVJIQUNRRlUiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6NTgxLCJoZWlnaHQiOjc5Mn0)
>
> 如果N = 12，在Encoder端，数据会依次进入12 个Encoder层，可以获得高度压缩的输入文本信息向量。
>
> 从Encoder端输出的向量，会依次进入Decoder端的所有层，保证不会影响Encoder端的输出。
>
> 9.transformer家族
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/U4ER2AZHADQBU?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IlU0RVIyQVpIQURRQlUiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6MTQ0OSwiaGVpZ2h0Ijo2OTN9)
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/P6ISMAZHABACM?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IlA2SVNNQVpIQUJBQ00iLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6ODgyLCJoZWlnaHQiOjI3OH0)
>
> 10.需要安装的包
>
> [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/XLIW4AZHACQGW?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IlhMSVc0QVpIQUNRR1ciLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6NTk3LCJoZWlnaHQiOjQ3Nn0)
>
>
>

## 资料与关联

- [[大模型全栈/资料/PDF/预训练时代.pdf#page=1|预训练时代.pdf · 第 1–20 页]]
- [[大模型全栈/资料/PDF/传统NLP.pdf#page=132|传统NLP.pdf · 第 132–153 页]]
- 关联知识：[[大模型全栈/07-BERT、MLM 与 Transformer 家族|07-BERT、MLM 与 Transformer 家族]]、[[大模型全栈/11-因果注意力与 Mask 可视化|11-因果注意力与 Mask 可视化]]、[[大模型全栈/12-手写 GPT：模块、训练与生成|12-手写 GPT：模块、训练与生成]]。

> [!example]- 本地讲义页预览
> ![[大模型全栈/资料/PDF/预训练时代.pdf#page=7]]
