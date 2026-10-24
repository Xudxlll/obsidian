---
type: 学习笔记
course: 大模型全栈
order: 59
stage: 微调与量化
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/58-领域续训与全参数微调|58-领域续训与全参数微调]] · 下一篇：[[大模型全栈/60-QLoRA、4-bit 基座与回答掩码|60-QLoRA、4-bit 基座与回答掩码]]

> [!abstract] 学习目标
> 理解参数高效微调究竟训练了什么。

## 核心理解

LoRA 冻结基础权重，以低秩矩阵表达更新：

$$
W'=W+\frac{\alpha}{r}BA
$$

若 $W\in\mathbb R^{d_{out}\times d_{in}}$，则 $A\in\mathbb R^{r\times d_{in}}$、$B\in\mathbb R^{d_{out}\times r}$。当 r 较小时，可训练参数显著少于整个 W。

课堂将 LoRA 挂在 q_proj、v_proj，配置 r、alpha 与 dropout，再把法律指令转成聊天模板训练。r 控制更新容量，target_modules 决定影响哪些层；它们没有跨任务通用的最优值。

适配器保存的是增量权重与配置，推理仍需匹配基础模型。保存 tokenizer、训练数据版本和模板同样重要，否则换环境后可能无法一致加载或生成。

本例用语言模型 collator 训练整段对话；它与下一篇只监督回答区域的 label-mask 方案并不相同。

## 课堂代码怎么读

重点读 to_text 如何拼接指令、input 与 output，再看 get_peft_model 和可训练参数打印。最后确认输出目录保存了哪些文件，推理加载路径是否一致。

> [!warning] 易错点与资料边界
> 原文同样误写 `user_cache`。当 PAD 与 EOS 相同，collator 的掩码行为需要检查；训练时的模板、长度与目标区域会影响结果，不能只看 LoRA 参数少。

## 复盘练习

为什么只拿 adapter 文件无法单独构成完整模型？

> [!question]- 参考思路
> 适配器通常只包含相对基础模型的更新；实际前向仍需要基础结构、原始权重和匹配 tokenizer。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 下018 %%

> [!quote]- 大模型全栈（下）.md · LoRA+SFT
> 来源：原笔记第 879–957 行。
>
> **LoRA+SFT**
>
> ```python
> """
> LoRA + SFT
> """
> import torch
> from datasets import load_dataset
> from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, \
>     DataCollatorForLanguageModeling
> from peft import LoraConfig, get_peft_model
>
> MODEL = "./Qwen3-0.6B"
> OUTPUT_DIR = "./output/LoRA_SFT_Qwen3"
>
> # 分词器
> tokenizer = AutoTokenizer.from_pretrained(MODEL)
> if tokenizer.pad_token is None:
>     tokenizer.pad_token = tokenizer.eos_token
>
> # 读文本
> raw = load_dataset(
>     "json", split="train",
>     data_files="./data/legal_train.json"
> )
>
> def to_text(e):
>     user = e["instruction"] + ("\n" + e["input"] if e.get("input") else "")
>     e["text"] = tokenizer.apply_chat_template([
>         {"role": "user", "content": user},
>         {"role": "assistant", "content": e["output"]},
>     ], tokenize=False, add_generation_prompt=False)
>
>     return e
>
> raw = raw.map(to_text)
> ds = raw.map(lambda e: tokenizer(e["text"], truncation=True, max_length=256), batched=True)
>
> # 加载因果大模型
> model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.bfloat16, device_map="auto")
> model.config.user_cache = False
>
> # LoRA微调
> model = get_peft_model(
>     model,
>     LoraConfig(
>         r=8,
>         lora_alpha=16,
>         target_modules=["q_proj", "v_proj"],
>         lora_dropout=.1,
>         task_type="CAUSAL_LM",
>     )
> )
> model.print_trainable_parameters()
>
> # 微调
> args = TrainingArguments(
>     output_dir=OUTPUT_DIR,
>     per_device_train_batch_size=2,
>     gradient_accumulation_steps=4,
>     num_train_epochs=3,
>     learning_rate=2e-5,
>     bf16=True,
>     gradient_checkpointing=True,
>     logging_steps=5,
>     report_to="none",
>     save_strategy="no",
> )
> trainer = Trainer(
>     model=model,
>     args=args,
>     train_dataset=ds,
>     data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
> )
>
> trainer.train()
> model.save_pretrained(OUTPUT_DIR)
> ```
>

## 资料与关联

- 本篇主要依据上述课堂代码补充讲解；相关讲义统一见 [[大模型全栈/资料/00-资料索引|资料索引]]。
- [PEFT 官方量化训练说明](https://huggingface.co/docs/peft/developer_guides/quantization)：可将 LoRA 与量化基座组合，具体支持需匹配模型与环境。（补充核对日期：2026-10-25）
- 关联知识：[[大模型全栈/58-领域续训与全参数微调|58-领域续训与全参数微调]]、[[大模型全栈/60-QLoRA、4-bit 基座与回答掩码|60-QLoRA、4-bit 基座与回答掩码]]、[[大模型全栈/61-训练监控、LoRA 对照与困惑度|61-训练监控、LoRA 对照与困惑度]]。
