---
type: 学习笔记
course: 大模型全栈
order: 9
stage: 基础原理
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/08-句向量、池化与 Embedding 接口|08-句向量、池化与 Embedding 接口]] · 下一篇：[[大模型全栈/10-GPT 自回归生成与采样策略|10-GPT 自回归生成与采样策略]]

> [!abstract] 学习目标
> 从预训练表征走到有标签的具体任务。

## 核心理解

BERT 分类微调在编码器上接一个分类头。输入仍是 token ID 与 mask，输出则是每个类别的 logits。交叉熵让正确标签对应的概率上升，梯度可以同时更新分类头和未冻结的编码器参数。

课堂用少量正负面评论演示完整训练接口：`Dataset.from_dict` 建数据集，tokenizer 统一编码，`BertForSequenceClassification(num_labels=2)` 加载任务模型，Trainer 执行训练，再用 `argmax` 得到类别编号。

这里应把“流程跑通”与“模型有效”分开。少量样本适合教学，却不足以估计泛化能力。正式实验要明确标签映射，分离训练、验证和测试数据，并检查类别比例与重复评论。

如果只是想拿句向量，不应误用分类 logits 作为语义嵌入；若目标是分类，也不能把句子余弦相似度直接当成已训练分类器。

## 课堂代码怎么读

逐步追踪 `text` 如何变成 `input_ids`，`label` 如何进入 loss，再检查 `predict` 中 0/1 与中文类别的对应关系。课堂 ZIP 项目名称原样保留，但 ZIP 内文件没有在本轮补造。

> [!warning] 易错点与资料边界
> 课堂未展示完整独立验证流程；训练结束后的单句预测只能说明推理链路工作。预测时应确认评估模式、设备一致，并关闭不必要的梯度记录。

## 复盘练习

分类头最初是随机初始化的，这为什么正常？

> [!question]- 参考思路
> 预训练检查点通常不包含当前任务的二分类头。新增任务头需要用有标签数据学习；提示权重新初始化不等于编码器预训练失败。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中086 %%

> [!quote]- 大模型全栈（中）.md · BERT微调
> 来源：原笔记第 5774–5842 行。
>
> **BERT微调**
>
> ```python
> --"""
> 微调(仅做举例教学,效果不太好)
> pip install datasets
> """
>
> import torch
> from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
> from datasets import Dataset
>
> # 1.微调数据(实际上很多!)
> data = {
>     "text": [
>         "这个手机真好用，速度很快",
>         "电池很耐用，满意",
>         "屏幕清晰，拍照好看",
>         "质量太差了，用了一天就坏了",
>         "发货慢，客服态度差",
>         "卡顿严重，不推荐购买"
>     ],
>     "label": [1, 1, 1, 0, 0, 0]  # 1=正面, 0=负面
> }
>
> datasets = Dataset.from_dict(data)
> tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
> model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=2)
>
> def tokenize_fun(text):
>     return tokenizer(text["text"], padding="max_length", truncation=True, max_length=64)
>
> tokenized_dataset = datasets.map(tokenize_fun, batched=True)
>
> # 训练
> training_args = TrainingArguments(
>     output_dir='./model',
>     num_train_epochs=3,
>     per_device_train_batch_size=4,
>     learning_rate=2e-5,
>     logging_steps=1,
>     save_strategy='epoch',  # no epoch steps
> )
> trainer = Trainer(
>     model=model,
>     args=training_args,
>     train_dataset=tokenized_dataset
> )
>
> trainer.train()
>
> # 测试
> def predict(text):
>     inputs = tokenizer(text, return_tensors="pt", padding="max_length", truncation=True, max_length=64)
>
>     device = next(model.parameters()).device
>     inputs = {k: v.to(device) for k, v in inputs.items()}
>
>     with torch.no_grad():
>         outputs = model(**inputs)
>
>     pred = torch.argmax(outputs.logits, dim=1).item()
>     return "正面" if pred == 1 else "负面"
>
> # 结果可能不太好,不符合预期,因为数据量太少了
> print(predict("这个产品还不错,推荐购买"))
> print(predict("耳机的音质太差了,和破罗一样,续航非常短,不推荐购买"))
> ```
>

%% source-id: 中085 %%

> [!quote]- 大模型全栈（中）.md · BERT项目
> 来源：原笔记第 5770–5773 行。
>
> **BERT项目**
>
> Bert_finetune.zip
>

## 资料与关联

- [[大模型全栈/资料/PDF/NLP.pdf#page=165|NLP.pdf · 第 165–168 页]]
