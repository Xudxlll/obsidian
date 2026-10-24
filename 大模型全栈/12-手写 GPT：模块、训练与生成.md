---
type: 学习笔记
course: 大模型全栈
order: 12
stage: 基础原理
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/11-因果注意力与 Mask 可视化|11-因果注意力与 Mask 可视化]] · 下一篇：[[大模型全栈/13-推测解码：草稿、验证与接受率|13-推测解码：草稿、验证与接受率]]

> [!abstract] 学习目标
> 把模型结构真正落到可跟踪的模块中。

## 核心理解

课堂小 GPT 用字符级词表演示 Decoder-only 模型，主线是：字符编码 → token 与位置嵌入 → 多个 Transformer Block → 词表 logits → 下一字符损失。

单头模块计算 Q/K/V 和因果注意力；多头模块拼接不同头，再投影。Block 结合归一化、注意力、前馈网络与残差。最终线性层输出每个位置对整个词表的分数。

训练样本 $x$ 与目标 $y$ 错开一个字符，例如输入“我爱学”，目标“爱学习”。因此同一次前向就可以计算多个位置的交叉熵。`generate` 则反复截取最近的上下文，从最后位置抽样，再追加到序列。

本例的价值是解释张量、梯度和状态；字符级教学模型、训练数据规模和算力都不同于现成大模型，不能把它的输出当成通用问答能力。

## 课堂代码怎么读

按 `get_batch → Head → MultiHeadAttention → FeedForward → Block → GPT.forward → estimate_loss → generate` 阅读。特别核对 B、T、C 三个维度，以及 loss 前展平为什么不改变每个位置对应的目标。

> [!warning] 易错点与资料边界
> `estimate_loss` 中评估模式与训练模式需要切换；生成必须限制上下文长度。本例训练会读取语料并更新模型，本轮仅整理代码，没有启动训练。

## 复盘练习

为什么训练误差下降，生成仍可能混乱？

> [!question]- 参考思路
> 训练目标只是提高所见语料的下一字符预测；模型容量、语料范围、训练充分程度和采样设置都影响生成，低训练误差也可能来自记忆训练集。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中079 %%

> [!quote]- 大模型全栈（中）.md · 手动实现GPT
> 来源：原笔记第 5258–5497 行。
>
> **手动实现GPT**
>
> ```python
> """
> 从0实现GPT
> #   - 因果掩码（Causal Mask）
> #   - 多头自注意力（Multi-Head Self-Attention）
> #   - 前馈网络（Feed-Forward Network）
> #   - 残差连接 + LayerNorm（Pre-LN）
> #   - 词嵌入 + 可学习位置编码
> #   - 语言建模头 + 自回归生成
> """
>
> import torch
> import torch.nn as nn
> import torch.nn.functional as F
> import urllib.request
> import os
>
> # 超参数
> batch_size = 32  # 每批32个序列
> block_size = 128  # 上下文窗口，数据量大了可以调大
> n_layer = 6  # 6层Decoder
> n_head = 8  # 12个注意力头
> n_embd = 256  # 隐藏维度256
> dropout = 0.1  # dropout比例，训练时设0.1防过拟合
> learning_rate = 3e-4  # 学习率
> max_iters = 10000  # 训练迭代次数，数据量大了可以多训
> eval_interval = 500  # 每500步评估一次
> eval_iters = 100  # 评估时跑100批取平均
> device = "cuda" if torch.cuda.is_available() else "cpu"
>
> # 1.准备数据（完整莎士比亚全集，约100万字符，字符级语言模型）
> data_path = "shakespeare_full.txt"
> # 如果本地没有就自动下载
> if not os.path.exists(data_path):
>     print("正在下载莎士比亚全集...")
>     url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
>     urllib.request.urlretrieve(url, data_path)
>     print("下载完成！")
>
> with open(data_path, "r", encoding="utf-8") as f:
>     text = f.read()  # 读取完整文本
>
> chars = sorted(list(set(text)))  # 所有出现过的字符，排序
> vocab_size = len(chars)  # 词表大小（字符数）
> print(f"词表大小（字符数）: {vocab_size}")
> print(f"文本总长度: {len(text)} 字符")
>
> # 字符和编号的映射
> stoi = {ch: i for i, ch in enumerate(chars)}  # 字符 -> 编号
> itos = {i: ch for i, ch in enumerate(chars)}  # 编号 -> 字符
> encode = lambda s: [stoi[c] for c in s]  # 编码函数：字符串转编号列表
> decode = lambda l: "".join([itos[i] for i in l])  # 解码函数：编号列表转字符串
>
> # 全部文本转成张量
> data = torch.tensor(encode(text), dtype=torch.long)  # 形状 [总长度]
> n = int(0.9 * len(data))  # 90%训练集
> train_data = data[:n]  # 训练集
> val_data = data[n:]  # 验证集
>
> print(f"训练集长度: {len(train_data)}, 验证集长度: {len(val_data)}")
> print(f"block_size: {block_size}, 验证集够不够: {len(val_data) > block_size}")
>
> # 取一批数据的函数
> def get_batch(split):
>     data = train_data if split == "train" else val_data  # 选训练或验证
>     ix = torch.randint(len(data) - block_size, (batch_size,))  # 随机选batch_size个起始位置
>     x = torch.stack([data[i:i + block_size] for i in ix])  # 输入：每个起始位置开始的block_size个字符
>     y = torch.stack([data[i + 1:i + block_size + 1] for i in ix])  # 目标：输入右移一位（预测下一个字符）
>     x, y = x.to(device), y.to(device)  # 移到设备
>     return x, y
>
> # 2.定义模型组件
> # 组件1：因果自注意力头
> class Head(nn.Module):
>     def __init__(self, head_size):
>         super().__init__()
>         self.head_size = head_size  # 保存head_size，forward里缩放用
>         self.key = nn.Linear(n_embd, head_size, bias=False)  # Key投影矩阵，无偏置
>         self.query = nn.Linear(n_embd, head_size, bias=False)  # Query投影矩阵
>         self.value = nn.Linear(n_embd, head_size, bias=False)  # Value投影矩阵
>         # 注册因果掩码为buffer（不是参数，但随模型保存和移动设备）
>         self.register_buffer("tril", torch.tril(torch.ones(block_size, block_size)))
>         self.dropout = nn.Dropout(dropout)  # dropout层
>
>     def forward(self, x):
>         B, T, C = x.shape  # B=batch, T=序列长度, C=通道维度
>         k = self.key(x)  # [B, T, head_size]，每个位置的Key
>         q = self.query(x)  # [B, T, head_size]，每个位置的Query
>         # 计算注意力分数：Q·K^T / sqrt(head_size)
>         wei = q @ k.transpose(-2, -1) * (self.head_size ** -0.5)  # [B, T, T]，缩放点积
>         # 应用因果掩码：把上三角设为-inf，这样Softmax后为0
>         wei = wei.masked_fill(self.tril[:T, :T] == 0, float("-inf"))
>         wei = F.softmax(wei, dim=-1)  # Softmax归一化，每行和为1
>         wei = self.dropout(wei)  # dropout随机丢弃
>         v = self.value(x)  # [B, T, head_size]，每个位置的Value
>         out = wei @ v  # [B, T, head_size]，加权求和Value
>         return out
>
> # 组件2：多头注意力（把多个头拼起来）
> class MultiHeadAttention(nn.Module):
>     def __init__(self, num_heads, head_size):
>         super().__init__()
>         # 创建num_heads个独立的注意力头
>         self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
>         self.proj = nn.Linear(n_embd, n_embd)  # 输出投影矩阵W^O
>         self.dropout = nn.Dropout(dropout)
>
>     def forward(self, x):
>         # 每个头独立计算，然后在特征维度拼接
>         out = torch.cat([h(x) for h in self.heads], dim=-1)  # [B, T, num_heads*head_size] = [B, T, n_embd]
>         out = self.proj(out)  # 输出投影
>         out = self.dropout(out)
>         return out
>
> # 组件3：前馈网络（FFN）
> class FeedForward(nn.Module):
>     def __init__(self, n_embd):
>         super().__init__()
>         # GPT用4倍升维，GELU激活
>         self.net = nn.Sequential(
>             nn.Linear(n_embd, 4 * n_embd),  # 升维4倍：128 -> 512
>             nn.GELU(),  # GELU激活（GPT用GELU不用ReLU）
>             nn.Linear(4 * n_embd, n_embd),  # 降维回来：512 -> 128
>             nn.Dropout(dropout),
>         )
>
>     def forward(self, x):
>         return self.net(x)
>
> # 组件4：Transformer Block（一层Decoder）
> class Block(nn.Module):
>     def __init__(self, n_embd, n_head):
>         super().__init__()
>         head_size = n_embd // n_head  # 每个头的维度 = 总维度 / 头数
>         self.sa = MultiHeadAttention(n_head, head_size)  # 多头自注意力
>         self.ffwd = FeedForward(n_embd)  # 前馈网络
>         self.ln1 = nn.LayerNorm(n_embd)  # 第一个LayerNorm（Pre-LN）
>         self.ln2 = nn.LayerNorm(n_embd)  # 第二个LayerNorm（Pre-LN）
>
>     def forward(self, x):
>         # Pre-LN结构：先LayerNorm，再注意力，再加残差
>         x = x + self.sa(self.ln1(x))  # 残差连接：x + 注意力(LayerNorm(x))
>         x = x + self.ffwd(self.ln2(x))  # 残差连接：x + FFN(LayerNorm(x))
>         return x
>
> # 3.定义完整 GPT 模型
> class GPT(nn.Module):
>     def __init__(self):
>         super().__init__()
>         # 词嵌入表：每个字符对应一个n_embd维向量
>         self.token_embedding_table = nn.Embedding(vocab_size, n_embd)
>         # 位置编码：每个位置对应一个n_embd维向量（可学习，不是正弦）
>         self.position_embedding_table = nn.Embedding(block_size, n_embd)
>         # 堆叠n_layer个Transformer Block
>         self.blocks = nn.Sequential(*[Block(n_embd, n_head) for _ in range(n_layer)])
>         # 最后一层的LayerNorm（GPT-2在最后加了额外的LN）
>         self.ln_f = nn.LayerNorm(n_embd)
>         # 语言建模头：把n_embd维映射到vocab_size维，预测下一个字符
>         self.lm_head = nn.Linear(n_embd, vocab_size)
>
>     def forward(self, idx, targets=None):
>         B, T = idx.shape  # B=batch, T=序列长度
>         # token嵌入 + 位置嵌入
>         tok_emb = self.token_embedding_table(idx)  # [B, T, n_embd]
>         pos_emb = self.position_embedding_table(torch.arange(T, device=device))  # [T, n_embd]
>         x = tok_emb + pos_emb  # 逐元素相加，[B, T, n_embd]
>         # 过所有Transformer Block
>         x = self.blocks(x)  # [B, T, n_embd]
>         x = self.ln_f(x)  # 最后的LayerNorm
>         logits = self.lm_head(x)  # [B, T, vocab_size]，每个位置预测下一个字符的分数
>
>         if targets is None:
>             loss = None  # 推理时不需要计算损失
>         else:
>             B, T, C = logits.shape
>             logits = logits.view(B * T, C)  # 展平成 [B*T, vocab_size]
>             targets = targets.view(B * T)  # 展平成 [B*T]
>             loss = F.cross_entropy(logits, targets)  # 交叉熵损失
>
>         return logits, loss
>
>     # 自回归生成函数
>     def generate(self, idx, max_new_tokens, temperature=0.7):
>         for _ in range(max_new_tokens):  # 循环生成每个token
>             idx_cond = idx[:, -block_size:]  # 只取最后block_size个token（截断上下文）
>             logits, loss = self(idx_cond)  # 前向传播
>             logits = logits[:, -1, :]  # 取最后一个位置的logits，[B, vocab_size]
>             logits = logits / temperature
>             probs = F.softmax(logits, dim=-1)  # Softmax转概率
>             idx_next = torch.multinomial(probs, num_samples=1)  # 按概率采样1个token
>             idx = torch.cat([idx, idx_next], dim=1)  # 拼到序列末尾
>         return idx
>
> # 4.训练模型
> print("开始训练~~~")
> model = GPT()  # 创建模型
> model = model.to(device)  # 移到设备
> print(f"模型参数量: {sum(p.numel() for p in model.parameters()) / 1e3:.1f}K")
>
> optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
>
> # 评估函数：在训练集和验证集上算平均损失
> @torch.no_grad()  # 不计算梯度
> def estimate_loss():
>     out = {}
>     model.eval()  # 评估模式
>     for split in ["train", "val"]:
>         losses = torch.zeros(eval_iters)
>         for k in range(eval_iters):
>             X, Y = get_batch(split)
>             logits, loss = model(X, Y)
>             losses[k] = loss.item()
>         out[split] = losses.mean()
>     model.train()  # 切回训练模式
>     return out
>
> # 训练循环
> for iter in range(max_iters):
>     # 定期评估
>     if iter % eval_interval == 0:
>         losses = estimate_loss()
>         print(f"step {iter:4d}: train_loss={losses['train']:.4f}, val_loss={losses['val']:.4f}")
>
>     xb, yb = get_batch("train")  # 取一批训练数据
>     logits, loss = model(xb, yb)  # 前向传播，算损失
>     optimizer.zero_grad(set_to_none=True)  # 清空梯度
>     loss.backward()  # 反向传播，算梯度
>     optimizer.step()  # 更新参数
>
> # 第五步：生成文本
> print("训练完成! 生成文本~~")
>
> context = torch.zeros((1, 1), dtype=torch.long, device=device)  # 起始输入：一个0（换行符）
> generated = model.generate(context, max_new_tokens=500)  # 生成500个字符
> generated_text = decode(generated[0].tolist())  # 解码成字符串
> print(generated_text)
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/预训练时代.pdf#page=7|预训练时代.pdf · 第 7–20 页]]
