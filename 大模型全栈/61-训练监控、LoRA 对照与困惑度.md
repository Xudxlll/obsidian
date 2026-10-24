---
type: 学习笔记
course: 大模型全栈
order: 61
stage: 微调与量化
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/60-QLoRA、4-bit 基座与回答掩码|60-QLoRA、4-bit 基座与回答掩码]] · 下一篇：[[大模型全栈/62-GPTQ 与 AWQ：校准、量化与导出|62-GPTQ 与 AWQ：校准、量化与导出]]

> [!abstract] 学习目标
> 同时检查训练稳定性、任务表现与语言模型损失。

## 核心理解

训练监控观察 loss、学习率、梯度与运行状态，帮助识别发散、无效样本和资源问题；它不等于最终任务验收。课堂增加 TensorBoard 配置，并比较启用或禁用同一 LoRA 适配器的输出。

困惑度定义为平均负对数似然的指数：

$$
\operatorname{PPL}=\exp\left(-\frac{1}{N}\sum_{t=1}^N\log p(x_t\mid x_{<t})\right)
$$

它衡量模型对给定文本的预测难度，比较时要保持 tokenizer、文本、截断与目标位置一致。PPL 下降不直接保证事实性、法律正确性或指令遵循改善。

基座与 LoRA 对照应使用相同问题与生成参数，保存原始回答，再按明确标准评价。代码虽然导入 ROUGE 工具，但所保留验证片段没有实际计算完整 ROUGE 结果。

## 课堂代码怎么读

先读监控 Dataset 与日志配置，再看 disable_adapter 如何得到基座输出。PPL 部分重点检查 padding 掩码、shift 后的有效目标数和加权平均；适配器路径还要与实际保存目录一致。

> [!warning] 易错点与资料边界
> 原 PPL 代码按 attention_mask 总数加权，没有精确排除因果移位后的首个位置，严格实现应按有效目标数计算。只有两段文本的演示不构成稳健评估；evaluation.zip 只保留名称，未导入结果。

## 复盘练习

为什么不能把训练 loss 最低的检查点直接认作最好？

> [!question]- 参考思路
> 它可能过拟合训练语料。应查看独立验证目标与任务测试，并在同一评价口径下决定检查点。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 下014 %%

> [!quote]- 大模型全栈（下）.md · 训练监控
> 来源：原笔记第 566–652 行。
>
> **训练监控**
>
> ```python
> """
> LoRA + SFT + 训练监控
> """
> import torch
> from torch.utils.data import Dataset
> from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, \
>     DataCollatorForLanguageModeling
> from peft import LoraConfig, get_peft_model
>
> MODEL = "./Qwen3-0.6B"
> OUTPUT_DIR = "./output/LoRA_SFT_Qwen3"
>
> # 数据
> texts = [           
>             "民事主体在民事活动中的法律地位一律平等。",
>             "民事主体从事民事活动,应当遵循自愿原则。",
>             "民事主体从事民事活动,应当遵循诚信原则,秉持诚实,恪守承诺。",
>             "自然人从出生时起到死亡时止,具有民事权利能力。",
>         ] * 20
>
> class LegalDataset(Dataset):
>     def __init__(self, texts, tokenizer):
>         self.enc = tokenizer(texts, padding="max_length", truncation=True, return_tensors="pt", max_length=50)
>
>     def __len__(self):
>         return len(self.enc["input_ids"])
>
>     def __getitem__(self, idx):
>         return {
>             "input_ids": self.enc["input_ids"][idx],
>             "attention_mask": self.enc["attention_mask"][idx],
>             "labels": self.enc["input_ids"][idx].clone(),
>         }
>
> # 加载模型
> tokenizer = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)
> tokenizer.pad_token = tokenizer.eos_token
>
> model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.bfloat16, trust_remote_code=True)
>
> # LoRA微调
> model = get_peft_model(
>     model,
>     LoraConfig(
>         r=8,
>         lora_alpha=16,
>         # PEFT 我要在哪几个线性层上挂上LoRA的A和B小矩阵
>         target_modules=["q_proj", "v_proj"],
>         lora_dropout=.1,
>         task_type="CAUSAL_LM",
>     )
> )
> model.print_trainable_parameters()
>
> train_ds = LegalDataset(texts, tokenizer)
> collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
>
> # 微调
> args = TrainingArguments(
>     output_dir=OUTPUT_DIR,
>     per_device_train_batch_size=2,
>     gradient_accumulation_steps=2,
>     num_train_epochs=3,
>     learning_rate=2e-4,
>     warmup_steps=20,
>     bf16=True,
>     gradient_checkpointing=True,
>     max_grad_norm=1,
>     logging_steps=1,
>     logging_first_step=True,
>     report_to="tensorboard",
>     save_strategy="no",
> )
> trainer = Trainer(
>     model=model,
>     args=args,
>     train_dataset=train_ds,
>     data_collator=collator,
> )
>
> trainer.train()
> model.save_pretrained(f"{OUTPUT_DIR}/runs")
> ```
>

%% source-id: 下016 %%

> [!quote]- 大模型全栈（下）.md · LoRA验证
> 来源：原笔记第 657–711 行。
>
> **LoRA验证**
>
> ```python
> """
> 验证
> 基座 VS LoRA
> """
> import re
> import json
> import torch
> import jieba
> from rouge_score import rouge_scorer
> from transformers import AutoTokenizer, AutoModelForCausalLM
> from peft import PeftModel
>
> tokenizer = AutoTokenizer.from_pretrained('./Qwen3-0.6B')
> base = AutoModelForCausalLM.from_pretrained('./Qwen3-0.6B', dtype=torch.bfloat16, device_map='auto').eval()
>
> # lora注入到base模型 ==> 修改 ==> 得到base效果后面会关掉lora分支
> lora = PeftModel.from_pretrained(base, './output/LoRA_SFT_Qwen3').eval()
>
> def answer(question):
>     prompt = tokenizer.apply_chat_template([
>         {"role": "user", "content": question},
>     ], tokenize=False, add_generation_prompt=True, enable_thinking=False
>     )
>
>     inputs = tokenizer(prompt, return_tensors='pt').to(lora.device)
>     with torch.no_grad():
>         out = lora.generate(**inputs, max_new_tokens=128, do_sample=False)
>         text = tokenizer.decode(
>             out[0][len(inputs['input_ids'][0]):],
>             skip_special_tokens=True
>         )
>
>         # ...思考块 纯回答文本 + ROUGE打分
>         return re.sub(r"<think>.*?</think>", "", text, flags=re.S)
>
> questions = [
>     "违约金太高怎么办?",
>     "试用期最长可与约定多久?",
>     "网购收到假货怎么维权?",
>     "公司拖欠工资,劳动者怎么处理?"
> ]
>
> for q in questions:
>     with lora.disable_adapter():
>         base_ans = answer(q)
>
>     lora_ans = answer(q)
>     print(f"问:{q}")
>     print(f"  基座:{base_ans}")
>     print(f"  LoRA:{lora_ans}")
> ```
>

%% source-id: 下013 %%

> [!quote]- 大模型全栈（下）.md · 困惑度
> 来源：原笔记第 500–565 行。
>
> **困惑度**
>
> ```python
>  """
> 困惑度
> """
> import torch
> from transformers import AutoTokenizer, AutoModelForCausalLM
> from peft import PeftModel
>
> def calculate_per(model, tokenizer, texts, batch_size=4):
>     # 验证集计算
>     model.eval()
>     total_loss = 0
>     total_tokens = 0
>
>     with torch.no_grad():
>         for i in range(0, len(texts), batch_size):
>             batch_texts = texts[i:i + batch_size]
>             encodings = tokenizer(
>                 batch_texts,
>                 return_tensors='pt',
>                 padding=True,
>                 max_length=128,
>                 truncation=True,
>                 return_token_type_ids=False
>             )
>
>             input_ids = encodings['input_ids'].to(model.device)
>             attention_mask = encodings['attention_mask'].to(model.device)
>
>             labels = input_ids.clone()
>             labels[attention_mask == 0] = -100
>
>             outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
>
>             # 真实token数量
>             num_valid_tokens = attention_mask.sum().item()
>             total_loss += num_valid_tokens * outputs.loss.item()
>             total_tokens += num_valid_tokens
>
>     # 总损失 / 全部有效token = 全局平均loss
>     avg_loss = total_loss / total_tokens
>     perplexity = torch.exp(torch.tensor(avg_loss)).item()
>
>     return perplexity
>
> # 使用
> base_model = AutoModelForCausalLM.from_pretrained('./Qwen3-0.6B', torch_dtype=torch.bfloat16, device_map='cuda')
> tokenizer = AutoTokenizer.from_pretrained('./Qwen3-0.6B')
>
> val_texts = [
>     "根据《民法典》第143条，具备下列条件的民事法律行为有效：（一）行为人具有相应的民事行为能力；（二）意思表示真实；（三）不违反法律、行政法规的强制性规定，不违背公序良俗。",
>     "《劳动合同法》第39条规定，劳动者有下列情形之一的，用人单位可以解除劳动合同：（一）在试用期间被证明不符合录用条件的；（二）严重违反用人单位的规章制度的；（三）严重失职，营私舞弊，给用人单位造成重大损害的。"
> ]
>
> # 先看基座模型
> base_ppl = calculate_per(base_model, tokenizer, val_texts)
> print(f"base_ppl:{base_ppl}")
>
> # 再看微调后模型
> finetuned_model = PeftModel.from_pretrained(base_model, "./output/LoRA_SFT_Qwen3/runs")
> finetuned_ppl = calculate_per(finetuned_model, tokenizer, val_texts)
> print(f"finetuned_ppl:{finetuned_ppl}")
> ```
>

%% source-id: 下008 %%

> [!quote]- 大模型全栈（下）.md · 评估结果(少样本 Fast快速脚本 结果)
> 来源：原笔记第 338–341 行。
>
> **评估结果(少样本 Fast快速脚本 结果)**
>
> evaluation.zip
>

## 资料与关联

- 本篇主要依据上述课堂代码补充讲解；相关讲义统一见 [[大模型全栈/资料/00-资料索引|资料索引]]。
