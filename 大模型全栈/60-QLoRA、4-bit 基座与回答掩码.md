---
type: 学习笔记
course: 大模型全栈
order: 60
stage: 微调与量化
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/59-LoRA：低秩适配与 SFT|59-LoRA：低秩适配与 SFT]] · 下一篇：[[大模型全栈/61-训练监控、LoRA 对照与困惑度|61-训练监控、LoRA 对照与困惑度]]

> [!abstract] 学习目标
> 分清存储精度、计算精度与参与优化的参数。

## 核心理解

QLoRA 将基础模型以低位形式加载并冻结，再训练 LoRA 适配器。权重存储为 4-bit，不表示全部运算都使用 4-bit；课堂还指定 FP16 计算精度、NF4 和双重量化。

`prepare_model_for_kbit_training` 为量化模型的训练进行准备，再添加 LoRA。梯度主要更新适配器，基础权重保留量化表示；这与把整模型所有参数都进行 4-bit 梯度更新不同。

课堂预处理分别构造完整对话和不含回答的 prompt，给 prompt 部分 labels 设为 -100，只监督回答区域。attention_mask 控制注意力中的有效 token，labels 的 -100 控制损失，两者职责不同。

截断后还要确认留下了有效回答 token；过长 prompt 应过滤或重新设计，而不是保留一条全部不参与 loss 的样本。

## 课堂代码怎么读

按 BitsAndBytesConfig、量化加载、prepare、LoraConfig、preprocess_function、动态 padding 和 Trainer 阅读。重点核对 full_ids 与 prompt_ids 的前缀是否真的一致。

> [!warning] 易错点与资料边界
> 原代码使用 `examples.get("inputs", ...)`，而前一版数据字段是 `input`，可能静默丢掉补充输入。模板前缀与角色标记也需验证；不同硬件后端的低位支持不能直接由课堂设置推断。

## 复盘练习

为什么 attention_mask=1 的位置，label 仍可为 -100？

> [!question]- 参考思路
> 该位置可以作为模型理解后文的上下文，但不要求模型在该位置承担监督预测损失，例如用户提示部分。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 下017 %%

> [!quote]- 大模型全栈（下）.md · QLoRA+SFT
> 来源：原笔记第 712–878 行。
>
> **QLoRA+SFT**
>
> ```python
> """
> QLoRA + SFT
> """
> import torch
> from datasets import load_dataset
> from transformers import (
>     AutoTokenizer,
>     AutoModelForCausalLM,
>     TrainingArguments,
>     Trainer,
>     DataCollatorForSeq2Seq,
>     BitsAndBytesConfig
> )
> from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, TaskType
>
> MODEL = "./Qwen3-0.6B"
> OUTPUT_DIR = "./output/QLoRA_SFT_Qwen3"
>
> # 分词器
> tokenizer = AutoTokenizer.from_pretrained(MODEL)
> if tokenizer.pad_token is None:
>     tokenizer.pad_token = tokenizer.eos_token
>
> # QLoRA:4bit 量化基座
> model = AutoModelForCausalLM.from_pretrained(
>     MODEL,
>     # 存储时是4bit的量化格式,先前计算权重会临时反量化
>     quantization_config=BitsAndBytesConfig(
>         load_in_4bit=True,
>         bnb_4bit_quant_type="nf4",  # 归一化4bit浮点数
>         bnb_4bit_compute_dtype=torch.float16,  # Turing架构用fp16而不是bf16
>         bnb_4bit_use_double_quant=True
>     ),
>     device_map="auto"
> )
> model = prepare_model_for_kbit_training(model)
>
> # 挂LoRA适配器
> model = get_peft_model(
>     model,
>     LoraConfig(
>         r=16,
>         lora_alpha=32,
>         # PEFT 我要在哪几个线性层上挂上LoRA的A和B小矩阵
>         target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
>         lora_dropout=.05,
>         bias="none",
>         task_type=TaskType.CAUSAL_LM,
>     )
> )
> model.print_trainable_parameters()
>
> # 数据预处理
> def preprocess_function(examples):
>     instructions = examples["instruction"]
>     inputs = examples.get("inputs", [""] * len(instructions))
>     outputs = examples["output"]
>
>     out_ids, out_mask, out_labels = [], [], []
>     for instr, inp, ans in zip(instructions, inputs, outputs):
>         user_content = f"{instr}" + (f"\n\n{inp}" if inp else "")
>
>         # 构建完整的对话
>         full_ids = tokenizer(
>             tokenizer.apply_chat_template(
>                 [
>                     {"role": "system",
>                      "content": "你是一个专业的中国法律助理,请根据中国法律,准确,严谨的回答用户的问题"},
>                     {"role": "user", "content": user_content},
>                     {"role": "assistant", "content": ans},
>                 ],
>                 tokenize=False,
>                 add_special_tokens=True,
>                 enable_thinking=False
>             ),
>             add_special_tokens=False
>         )["input_ids"]
>
>         # 构建提示词
>         prompt_ids = tokenizer(
>             tokenizer.apply_chat_template(
>                 [
>                     {"role": "system",
>                      "content": "你是一个专业的中国法律助理,请根据中国法律,准确,严谨的回答用户的问题"},
>                     {"role": "user", "content": user_content}
>                 ],
>                 tokenize=False,
>                 add_generation_prompt=True,  # 推理模板
>                 enable_thinking=False
>             ),
>             add_special_tokens=False
>         )["input_ids"]
>
>         if len(prompt_ids) >= 1024:
>             continue
>
>         # label-mask
>         labels = [-100] * len(prompt_ids) + full_ids[len(prompt_ids):]
>         # 截断
>         full_ids = full_ids[:1024]
>         labels = labels[:1024]
>
>         out_ids.append(full_ids)
>         out_mask.append([1] * len(full_ids))  # 参与注意力计算
>         out_labels.append(labels)
>
>     return {
>         "input_ids": out_ids,
>         "attention_mask": out_mask,
>         "labels": out_labels
>     }
>
> # 加载数据
> datasets = load_dataset("json", split="train", data_files="./data/legal_train.json")
> tokenized = datasets.map(preprocess_function, batched=True, remove_columns=datasets.column_names)
> tokenized = tokenized.filter(lambda x: len(x["input_ids"]) > 0)
> data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, padding=True, label_pad_token_id=-100)
>
> # 微调
> eff_batch = 2 * 8
> steps_per_epoch = max(1, len(tokenized) // eff_batch)
> total_steps = steps_per_epoch * 3
> warmup_steps = max(1, int(0.03 * total_steps))
>
> args = TrainingArguments(
>     output_dir=OUTPUT_DIR,
>     per_device_train_batch_size=2,
>     gradient_accumulation_steps=8,
>     num_train_epochs=3,
>     learning_rate=2e-4,
>     warmup_steps=warmup_steps,
>     lr_scheduler_type="cosine",
>     weight_decay=0.01,
>     max_grad_norm=1.0,
>     gradient_checkpointing=True,
>     gradient_checkpointing_kwargs={"use_reentrant": False},
>     # optim="paged_adamw_8bit",
>     optim="adamw_torch",
>     logging_steps=10,
>     save_steps=200,
>     save_total_limit=3,
>     # save_strategy="no",
>     report_to="none",
>     ddp_find_unused_parameters=False,
>     bf16=False,
>     fp16=True,
> )
> trainer = Trainer(
>     model=model,
>     args=args,
>     train_dataset=tokenized,
>     data_collator=data_collator,
> )
>
> trainer.train()
>
> # 单卡下等价 多卡时可能会被DDP包装
> # model.save_pretrained(OUTPUT_DIR)
> # 只保存 LoRA适配器 不保存基座大模型权重 推理时重新加载基座模型,再load LoRA适配器
> trainer.model.save_pretrained(OUTPUT_DIR)
> # 分词器全部文件
> tokenizer.save_pretrained(OUTPUT_DIR)
> ```
>

## 资料与关联

- 本篇主要依据上述课堂代码补充讲解；相关讲义统一见 [[大模型全栈/资料/00-资料索引|资料索引]]。
- [PEFT 官方量化训练说明](https://huggingface.co/docs/peft/developer_guides/quantization)：说明低位加载、prepare_model_for_kbit_training 与 LoRA 的衔接。（补充核对日期：2026-10-25）
