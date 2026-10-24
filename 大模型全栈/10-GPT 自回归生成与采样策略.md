---
type: 学习笔记
course: 大模型全栈
order: 10
stage: 基础原理
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/09-BERT 文本分类与监督微调|09-BERT 文本分类与监督微调]] · 下一篇：[[大模型全栈/11-因果注意力与 Mask 可视化|11-因果注意力与 Mask 可视化]]

> [!abstract] 学习目标
> 理解下一 token 分布如何变成一段文字。

## 核心理解

自回归语言模型把序列概率分解为：

$$
p(x_1,\ldots,x_T)=\prod_{t=1}^{T}p(x_t\mid x_{<t})
$$

每一步取最后位置的 logits，变成概率，选择下一 token，再拼回输入。贪心选择概率最大项；Beam Search 保留多条候选序列；采样则按调整后的分布随机抽取。

温度通过 $p_i=\exp(z_i/\tau)/\sum_j\exp(z_j/\tau)$ 改变分布的尖锐程度。Top-k 固定候选数量，Top-p 根据累计概率选择候选集合。它们改变生成分布，不能保证事实正确。

课堂 GPT-2 代码把手动循环与 `model.generate()` 放在一起，适合对照接口封装。`max_new_tokens` 限制新生成数量；与某些接口中同时计入输入长度的 `max_length` 应区别理解。

## 课堂代码怎么读

先看 ModelScope 下载线索与本地 `./gpt2` 路径，再读手动生成的最后位置 logits、拼接和解码。随后比较 greedy、beam、top-k、top-p 与混合参数，不要只比较最终文本是否“好看”。

> [!warning] 易错点与资料边界
> 随机生成要记录种子、温度、长度和设备。课堂选择 CUDA 或 CPU，并未自动覆盖所有 Mac 加速路径。模型包和 T5 ZIP 的文件名只是依赖线索。

## 复盘练习

温度很低是否就不会产生幻觉？

> [!question]- 参考思路
> 不会。温度主要影响抽样随机性；如果最高概率答案本身错误，低温只会更稳定地输出这个错误。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中082 %%

> [!quote]- 大模型全栈（中）.md · 阿里魔塔下载
> 来源：原笔记第 5753–5761 行。
>
> **阿里魔塔下载**
>
> ```python
> #模型下载
> from modelscope import snapshot_download
> model_dir = snapshot_download('openai-community/gpt2')
> model_dir = snapshot_download('distilbert/distilgpt2')
> ```
>

%% source-id: 中083 %%

> [!quote]- 大模型全栈（中）.md · 下载好的模型
> 来源：原笔记第 5762–5765 行。
>
> **下载好的模型**
>
> distilgpt2.zip
>

%% source-id: 中081 %%

> [!quote]- 大模型全栈（中）.md · GPT2-文本生成
> 来源：原笔记第 5618–5752 行。
>
> **GPT2-文本生成**
>
> ```python
> """
> 文本生成 - 理解自回归生成过程
> """
> import torch
> from transformers import GPT2Tokenizer, GPT2LMHeadModel
>
> # 1.加载模型和分词器
> device = "cuda" if torch.cuda.is_available() else "cpu"
> print(f"使用设备: {device}")
>
> # 加载 GPT-2 分词器，词表 50257
> tokenizer = GPT2Tokenizer.from_pretrained("./gpt2")
> model = GPT2LMHeadModel.from_pretrained("./gpt2")
> model = model.to(device)
> model.eval()
>
> print(f"模型参数量: {sum(p.numel() for p in model.parameters()) / 1e6:.1f}M")
>
> # 2.准备输入
> prompt = "Artificial intelligence is"  # 提示文本，让 GPT-2 接着往下写
> # 文本转 token，return_tensors="pt" 表示返回 PyTorch 张量
> inputs = tokenizer(prompt, return_tensors="pt")
> # input_ids 形状 [1, seq_len]，移到设备
> input_ids = inputs["input_ids"].to(device)
> # attention_mask 标记哪些位置是真实 token 哪些是 padding
> attention_mask = inputs["attention_mask"].to(device)
>
> print(f"输入文本: {prompt}")
> print(f"输入 token IDs: {input_ids[0].tolist()}")
> print(f"输入 token 数: {input_ids.shape[1]}")
>
> # 3. 自回归生成
> print("自回归生成...")
>
> generated = input_ids.clone()  # 复制输入，作为生成的起始序列
> max_new_tokens = 200
>
> with torch.no_grad():
>     for step in range(max_new_tokens):
>         outputs = model(input_ids=generated, attention_mask=torch.ones_like(generated))
>         # 取最后一个位置的 logits，形状 [1, 50257]，这就是下一个 token 的预测分数
>         next_token_logits = outputs.logits[:, -1, :]
>         next_token_id = torch.argmax(next_token_logits, dim=-1, keepdim=True)
>         # 把新 token 拼到序列末尾，形状 [1, seq_len+1]
>         generated = torch.cat([generated, next_token_id], dim=-1)
>
>         # 实时打印生成过程
>         # 把新 token 的数字转回文本
>         new_token_text = tokenizer.decode(next_token_id[0])
>         print(f"Step {step + 1:2d}: 预测 token_id={next_token_id.item():5d} -> 文本='{new_token_text}'")
>
> # 把整个序列的 token 转回文本
> generated_text = tokenizer.decode(generated[0])
> print(f"最终生成: {generated_text}")
>
> # 4.对比不同解码策略
> print("不同解码策略对比...")
>
> # 策略1：Greedy Search（贪心，每次选概率最高的）
> output_greedy = model.generate(
>     input_ids,  # 输入 token
>     max_new_tokens=200,  # 最多生成30个新token
>     do_sample=False,  # 不采样，就是贪心
>     attention_mask=attention_mask,  # 注意力掩码
>     pad_token_id=tokenizer.eos_token_id,  # padding 用 eos 填充，避免警告
> )
> print(f"\n[Greedy 贪心]   {tokenizer.decode(output_greedy[0], skip_special_tokens=True)}")
>
> # 策略2：Beam Search（束搜索，保留多个候选路径）
> output_beam = model.generate(
>     input_ids,
>     max_new_tokens=200,
>     num_beams=5,  # 保留5条候选路径
>     do_sample=False,
>     attention_mask=attention_mask,
>     pad_token_id=tokenizer.eos_token_id,
> )
> print(f"[Beam 束搜索]   {tokenizer.decode(output_beam[0], skip_special_tokens=True)}")
>
> # 策略3：Top-K 采样（只在概率最高的 K 个 token 中随机采样）
> output_topk = model.generate(
>     input_ids,
>     max_new_tokens=200,
>     do_sample=True,  # 开启采样
>     top_k=50,  # 只考虑概率最高的50个token
>     temperature=0.7,  # 温度，小于1更确定，大于1更随机
>     attention_mask=attention_mask,
>     pad_token_id=tokenizer.eos_token_id,
> )
> print(f"[Top-K 采样]    {tokenizer.decode(output_topk[0], skip_special_tokens=True)}")
>
> # 策略4：Top-P (Nucleus) 采样（在累积概率达到 P 的最小 token 集合中采样）
> output_topp = model.generate(
>     input_ids,
>     max_new_tokens=200,
>     do_sample=True,
>     top_p=0.9,  # 累积概率达到0.9的最小集合
>     temperature=0.7,
>     attention_mask=attention_mask,
>     pad_token_id=tokenizer.eos_token_id,
> )
> print(f"[Top-P 采样]    {tokenizer.decode(output_topp[0], skip_special_tokens=True)}")
>
> # 5.混合策略 topk topp 重复惩罚 禁止3-gram重复
> output_mix = model.generate(
>     input_ids,
>     max_new_tokens=200,
>     do_sample=True,
>     top_p=0.9,
>     top_k=50,
>     repetition_penalty=2.5,
>     no_repeat_ngram_size=3,
>     temperature=0.7,
>     attention_mask=attention_mask,
>     pad_token_id=tokenizer.eos_token_id,
> )
> print(f"[混合策略 ]    {tokenizer.decode(output_topp[0], skip_special_tokens=True)}")
>
> # 6.理解 logits 和概率分布
> print("最后一个位置的概率分布 Top-10")
>
> with torch.no_grad():
>     outputs = model(input_ids=input_ids)
>     last_logits = outputs.logits[0, -1, :]
>     probs = torch.softmax(last_logits, dim=-1)
>     top10_probs, top10_ids = torch.topk(probs, k=10)
>
>     for i, (pid, p) in enumerate(zip(top10_ids, top10_probs)):
>         token_text = tokenizer.decode([pid.item()])
>         print(f"  Top-{i + 1:2d}: token='{token_text:15s}' 概率={p.item():.4f} ({p.item() * 100:.1f}%)")
> ```
>

%% source-id: 中077 %%

> [!quote]- 大模型全栈（中）.md · T5 项目
> 来源：原笔记第 5094–5097 行。
>
> **T5 项目**
>
> t5_translation.zip
>

## 资料与关联

- [[大模型全栈/资料/PDF/NLP.pdf#page=169|NLP.pdf · 第 169–183 页]]
