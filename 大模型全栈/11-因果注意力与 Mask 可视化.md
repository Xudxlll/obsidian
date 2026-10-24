---
type: 学习笔记
course: 大模型全栈
order: 11
stage: 基础原理
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/10-GPT 自回归生成与采样策略|10-GPT 自回归生成与采样策略]] · 下一篇：[[大模型全栈/12-手写 GPT：模块、训练与生成|12-手写 GPT：模块、训练与生成]]

> [!abstract] 学习目标
> 用矩阵检查模型有没有偷看未来。

## 核心理解

因果掩码规定位置 $i$ 只能关注 $j\le i$。因此通常保留下三角和对角线，把上三角分数设为负无穷；加到 Attention logits 后，Softmax 会将这些未来位置的权重变成零。

Padding Mask 与 Causal Mask 解决不同问题：前者排除补齐位置，后者限制时间方向。它们可以同时存在。Attention 图的行是 Query 位置，列是 Key 位置，看图时要先确认坐标方向。

课堂用 GPT-2 的真实 attention 权重，再手动构造上三角遮罩进行对比。真实模型不同层、不同头的关注模式可以不同；热力图显示的是一次前向的权重，不是某个词对最终答案的完整因果解释。

训练可以一次输入完整目标序列并行计算各位置，但仍通过掩码保证每个位置只能用过去信息。生成阶段则必须逐步产生新 token。

## 课堂代码怎么读

观察 `torch.triu(..., diagonal=1)` 为什么不遮住对角线，再检查 `masked_fill` 如何分别填入负无穷与零。对照图中的行列 token，选一个中间位置验证未来列是否为零。

> [!warning] 易错点与资料边界
> 具体模型和 attention 后端是否返回可视化权重取决于所用配置。不能看到一张下三角图，就认定全部训练与标签对齐都正确。

## 复盘练习

为什么通常允许位置 i 读取自身？

> [!question]- 参考思路
> 训练时位置 i 的隐藏状态通常用于预测后一个 token；它读取当前位置输入不等于读取目标的未来信息。需要结合标签右移规则理解。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中080 %%

> [!quote]- 大模型全栈（中）.md · 因果注意力可视化
> 来源：原笔记第 5498–5617 行。
>
> **因果注意力可视化**
>
> ```python
> """
> 因果注意力可视化
> """
> import torch
> from transformers import GPT2Tokenizer, GPT2Model
> import matplotlib.pyplot as plt
>
> # 1.加载模型
> device = "cuda" if torch.cuda.is_available() else "cpu"  # 选择设备
> tokenizer = GPT2Tokenizer.from_pretrained("./gpt2")  # 加载分词器
> model = GPT2Model.from_pretrained("./gpt2", output_attentions=True)
> model = model.to(device)
> model.eval()
>
> # 2.准备输入
> text = "The cat sat on the mat"  # 测试句子
> inputs = tokenizer(text, return_tensors="pt")  # 文本转 token
> input_ids = inputs["input_ids"].to(device)  # input_ids 形状 [1, 6]
> tokens = [tokenizer.decode([t]) for t in input_ids[0]]  # 每个 token 转回文本，用于坐标轴标签
>
> print(f"输入句子: {text}")
> print(f"Token 列表: {tokens}")
> print(f"Token 数量: {len(tokens)}")
>
> # 3.前向传播获取注意力权重
> with torch.no_grad():
>     outputs = model(input_ids=input_ids)
>     # attentions 是一个元组，12层，每层形状 [batch, 12头, seq, seq]
>     attentions = outputs.attentions
>
> print(f"注意力权重结构：{len(attentions)} 层，每层形状 {attentions[0].shape}")
> print(f"  解释：[batch_size=1, num_heads=12, seq_len={len(tokens)}, seq_len={len(tokens)}]")
>
> # 4.验证因果掩码（下三角结构）
> print("验证因果掩码：第1层第1头的注意力矩阵（应该是下三角）")
>
> # 取第1层第1头，形状 [6, 6]，移到CPU转numpy
> layer0_head0 = attentions[0][0, 0].cpu().numpy()
>
> print(f"{'':>12s}", end="")
> for t in tokens:
>     print(f"{t:>8s}", end="")  # 每列标题是 token
> print()
>
> for i, row_token in enumerate(tokens):  # 遍历每行
>     print(f"{row_token:>12s}", end="")  # 行标题
>     for j in range(len(tokens)):  # 遍历每列
>         val = layer0_head0[i, j]
>         if val < 0.001:  # 接近0说明被掩码遮住了
>             print(f"{'✗':>8s}", end="")  # 用 ✗ 标记被掩码的位置
>         else:
>             print(f"{val:8.3f}", end="")  # 打印注意力权重
>     print()
>
> # 5.可视化多个头的注意力模式
> print("可视化：第1层的12个注意力头，每个头关注模式不同")
>
> fig, axes = plt.subplots(3, 4, figsize=(16, 12))  # 3行4列子图，共12个头
> fig.suptitle("GPT-2 Layer 1 - All 12 Attention Heads", fontsize=16)
>
> for head_idx in range(12):  # 遍历12个头
>     row = head_idx // 4  # 子图行号
>     col = head_idx % 4  # 子图列号
>     ax = axes[row, col]  # 获取子图
>
>     attn = attentions[0][0, head_idx].cpu().numpy()  # 取第1层第head_idx个头
>     im = ax.imshow(attn, cmap="YlOrRd", vmin=0, vmax=1)  # 画热力图，黄到红，0到1
>
>     ax.set_title(f"Head {head_idx}", fontsize=10)  # 子图标题
>     ax.set_xticks(range(len(tokens)))  # x轴刻度
>     ax.set_yticks(range(len(tokens)))  # y轴刻度
>     ax.set_xticklabels(tokens, rotation=45, ha="right", fontsize=8)  # x轴标签
>     ax.set_yticklabels(tokens, fontsize=8)  # y轴标签
>
> plt.tight_layout()  # 自动调整布局
> plt.savefig("gpt2_layer1_heads.png", dpi=150, bbox_inches="tight") 
>
> # 6.对比不同层的注意力
> print("对比不同层：第1层 vs 第6层 vs 第12层（取第0头）")
>
> fig, axes = plt.subplots(1, 3, figsize=(15, 5))  # 1行3列
> layer_indices = [0, 5, 11]  # 第1、6、12层（索引从0开始）
>
> for idx, layer_idx in enumerate(layer_indices):
>     ax = axes[idx]
>     attn = attentions[layer_idx][0, 0].cpu().numpy()  # 取指定层第0头
>     im = ax.imshow(attn, cmap="YlOrRd", vmin=0, vmax=1)
>     ax.set_title(f"Layer {layer_idx + 1}, Head 0", fontsize=12)
>     ax.set_xticks(range(len(tokens)))
>     ax.set_yticks(range(len(tokens)))
>     ax.set_xticklabels(tokens, rotation=45, ha="right", fontsize=9)
>     ax.set_yticklabels(tokens, fontsize=9)
>
> plt.tight_layout()
> plt.savefig("gpt2_layers_compare.png", dpi=150, bbox_inches="tight")
>
> # 7.手动构造因果掩码，理解原理
> print("手动构造因果掩码，理解 GPT 如何实现'看不到未来'")
>
> seq_len = len(tokens)  # 序列长度6
> # 方法1：用 torch.triu 构造上三角为1的矩阵，然后取反
> mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1)  # 上三角（不含对角线）为1
> mask = mask.masked_fill(mask == 1, float("-inf"))  # 上三角填 -inf，Softmax 后变成0
> mask = mask.masked_fill(mask == 0, float(0.0))  # 下三角（含对角线）填0，不影响
>
> # 验证：模拟一次注意力计算
> Q = torch.randn(seq_len, 64)  # 随机 Query，64维
> K = torch.randn(seq_len, 64)  # 随机 Key，64维
> scores = Q @ K.T / (64 ** 0.5)  # 注意力分数 = QK^T / sqrt(d_k)
> scores_masked = scores + mask  # 加因果掩码
> weights = torch.softmax(scores_masked, dim=-1)  # Softmax 归一化
>
> print("加掩码后的注意力权重（上三角应该全是0）：")
> print(weights.numpy().round(3))
> print(f"每行和（应该都是1）: {weights.sum(dim=-1).numpy().round(3)}")
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/传统NLP.pdf#page=148|传统NLP.pdf · 第 148–150 页]]
- [[大模型全栈/资料/PDF/预训练时代.pdf#page=13|预训练时代.pdf · 第 13–17 页]]

> [!example]- 本地讲义页预览
> ![[大模型全栈/资料/PDF/传统NLP.pdf#page=149]]
