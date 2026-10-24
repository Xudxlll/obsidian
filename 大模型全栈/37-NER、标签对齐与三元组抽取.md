---
type: 学习笔记
course: 大模型全栈
order: 37
stage: 知识图谱
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/36-知识图谱：实体、关系与图结构|36-知识图谱：实体、关系与图结构]] · 下一篇：[[大模型全栈/38-实体融合：名称、属性与相似度|38-实体融合：名称、属性与相似度]]

> [!abstract] 学习目标
> 把自然语言中的实体与关系转成可校验的结构。

## 核心理解

NER 给 token 序列标注实体边界与类型，常见 BIO 中 B 表示实体起点、I 表示延续、O 表示非实体。模型分词可能把一个原始词拆成多个子词，因此原始标签必须与 tokenizer 输出对齐。

课堂利用 word_ids 映射标签，并给特殊 token 或不参与监督的位置使用 -100。评价时要排除这些位置，把预测编号还原成标签，再用实体级指标计算 precision、recall、F1。

关系抽取更进一步，形成 head、relation、tail 三元组。课堂另一段用 LLM 从文本生成 JSON 关系，省去部分标注流程，但结果仍需检查类型、实体是否出现在证据中，以及关系是否被文本支持。

NER 与 LLM 抽取可以组合：先识别候选实体，再推断关系，最后按 Schema 入库与合并。

## 课堂代码怎么读

NER 代码依赖磁盘数据集、本地 bert 与 seqeval；按 `tokenizer_labels → compute_metrics → Trainer` 阅读。LLM 片段则重点看 JSON 解析与三元组格式，不要把格式正确等同于抽取准确。

> [!warning] 易错点与资料边界
> 子词标签延续的处理要与所用 BIO 约定一致。训练/验证/测试的实体级分数不同于逐 token 准确率；大量 O 标签会使后者具有迷惑性。

## 复盘练习

为什么需要给特殊 token 的 label 设为 -100？

> [!question]- 参考思路
> 它们通常不属于原始标注实体；-100 用于在损失中忽略这些位置，评价时也应排除，避免污染训练与指标。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中019 %%

> [!quote]- 大模型全栈（中）.md · 中文NER
> 来源：原笔记第 785–921 行。
>
> **中文NER**
>
> ```python
> """
> 使用BERT完成NER
> 原始标注数据集 --> 分词 + 标签对齐 --> 加载模型 --> 设置参数 --> 循环训练  --> 验证集 + 测试评估 --> 保存模型和分词器
>
> """
> import numpy as np
> from datasets import load_from_disk
> from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer, \
>     DataCollatorForTokenClassification
> import evaluate
>
> # 数据集
> dataset = load_from_disk("./data/ner_dataset")
> tokenizer = AutoTokenizer.from_pretrained("./bert-base-chinese")
>
> '''
> 样本
> data_train = [
>     {"token":["张","三","去","北","京"],"ner_tags":[1,2,0,8,10]},
>     {"token":["马","云","阿","里","巴","巴"],"ner_tags":[1,2,0,3,4,4]},
> ]
> '''
>
> # 分词 子词标签对齐
> def tokenizer_labels(examples):
>     # tokens = ["张","三"] ner_tags = [1,2]
>     # 张 --> B-PER(1) 三 --> i-PER(2)
>     tokenized_inputs = tokenizer(
>         examples["tokens"],
>         truncation=True,
>         max_length=128,
>         is_split_into_words=True,
>     )
>
>     all_labels = []
>
>     for batch_idx, label in enumerate(examples["ner_tags"]):
>         # 每个原始词对应下标
>         word_ids = tokenized_inputs.word_ids(batch_index=batch_idx)
>         prev_word_idx = None
>         label_ids = []
>         for word_idx in word_ids:
>             if word_idx is None:
>                 label_ids.append(-100)
>             elif word_idx != prev_word_idx:
>                 label_ids.append(label[word_idx])  # [None,0,1,None]
>             else:
>                 label_ids.append(-100)
>
>             prev_word_idx = word_idx
>         all_labels.append(label_ids)
>     tokenized_inputs["labels"] = all_labels
>
>     return tokenized_inputs
>
> # 转换
> tokenized_ds = dataset.map(tokenizer_labels, batched=True)
>
> # 模型
> model = AutoModelForTokenClassification.from_pretrained(
>     "./bert-base-chinese",
>     num_labels=7,
>     id2label={0: "O", 1: "B-PER", 2: "I-PER", 3: "B-ORG", 4: "I-ORG", 5: "B-LOC", 6: "I-LOC"},
>     label2id={"O": 0, "B-PER": 1, "I-PER": 2, "B-ORG": 3, "I-ORG": 4, "B-LOC": 5, "I-LOC": 6}
> )
> seqeval_metric = evaluate.load("seqeval")  # 加载 seqeval 指标 (没有库就下载)
>
> # 训练
> training_args = TrainingArguments(
>     output_dir="./ner_output",  # 输出目录，存放checkpoint
>     learning_rate=2e-5,  # 学习率，bert微调常用2e‑5
>     per_device_train_batch_size=16,  # 训练每卡batch大小16
>     per_device_eval_batch_size=16,  # 验证每卡batch大小16
>     num_train_epochs=3,  # 训练轮数3轮
>     weight_decay=0.01,  # 权重衰减，防止过拟合
>     eval_strategy="epoch",  # 每训练完1轮做一次验证评估
>     save_strategy="epoch",  # 每训练完1轮保存checkpoint
>     logging_strategy="epoch",  # 每轮输出日志
>     load_best_model_at_end=True,  # 训练结束自动加载验证集指标最优的模型
>     metric_for_best_model="f1",  # 使用f1判断哪个模型最优
>     report_to="none",  # 关闭wandb等第三方日志上报
>     fp16=False  # 关闭半精度混合训练
> )
> data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)
>
> # 评估函数 eval_pred=(模型的输出logits,真实标签)
> def compute_metrics(eval_pred):
>     predictions, labels = eval_pred
>     predictions = np.argmax(predictions, axis=2)
>
>     # 预测
>     true_preds = [
>         [{0: "O", 1: "B-PER", 2: "I-PER", 3: "B-ORG", 4: "I-ORG", 5: "B-LOC", 6: "I-LOC"}[p] for p, l in zip(pred, label) if l != -100]
>         for pred, label in zip(predictions, labels)
>     ]
>
>     # 真实
>     true_labels = [
>         [{0: "O", 1: "B-PER", 2: "I-PER", 3: "B-ORG", 4: "I-ORG", 5: "B-LOC", 6: "I-LOC"}[l] for p, l in zip(pred, label) if l != -100]
>         for pred, label in zip(predictions, labels)
>     ]
>
>     result = seqeval_metric.compute(predictions=true_preds, references=true_labels)
>     return {
>         "precision": result["overall_precision"],
>         "recall": result["overall_recall"],
>         "f1": result["overall_f1"],
>         "accuracy": result["overall_accuracy"],
>     }
>
> trainer = Trainer(
>     model=model,
>     args=training_args,
>     train_dataset=tokenized_ds["train"],
>     eval_dataset=tokenized_ds["validation"],
>     data_collator=data_collator,
>     compute_metrics=compute_metrics,
> )
>
> if __name__ == "__main__":
>     trainer.train()
>     eval_result = trainer.evaluate()
>
>     for k,v in eval_result.items():
>         print(f"{k}: {v}")
>
>     test_result = trainer.evaluate(tokenized_ds['test'])
>     for k,v in test_result.items():
>         print(f"{k}: {v}")
>
>     model.save_pretrained("./ner_output/best_model")
>     tokenizer.save_pretrained("./ner_output/best_model") 
> ```
>

%% source-id: 中018 %%

> [!quote]- 大模型全栈（中）.md · 大模型三元组抽取
> 来源：原笔记第 734–784 行。
>
> **大模型三元组抽取**
>
> ```python
> """
> 基于大模型做三元组
> """
> import os
> import re
> import json
> from dotenv import load_dotenv
> from langchain_openai import ChatOpenAI
>
> load_dotenv()
>
> # 大模型
> llm = ChatOpenAI(
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     model="deepseek-chat",
>     temperature=0
> )
>
> # 提示词
> # 文本
> text = "阿里巴巴集团由马云于1999年在杭州创立，旗下拥有淘宝、天猫等电商平台。2014年，阿里巴巴在纽约证券交易所上市。"
> # 关系
> relation_types = ["创始人", "成立年份", "总部位于", "旗下拥有", "上市地点", "上市年份"]
>
> prompt = f"""你是一个专业的知识图谱构建助手。请从以下文本中提取所有的三元组（头实体, 关系, 尾实体）。
> 关系类型限定为：{', '.join(relation_types)}
> 如果文本中没有这些关系，请返回空列表。
> 要求：
> 1. 实体必须是文本中出现的具体名称，不要泛化
> 2. 关系必须从给定的关系类型中选择
> 3. 输出严格的JSON数组格式，不要有其他文字说明
> 4. 每个三元组格式：{{"head": "头实体", "relation": "关系", "tail": "尾实体"}}
> 文本：
> {text}
> 输出："""
>
> # 结果
> response = llm.invoke([{"role": "user", "content": prompt}])
> res = response.content.strip()
>
> res = re.sub(r"^```josn\s*", "", res)
> res = re.sub(r"\s*```$", "", res)
>
> triples = json.loads(res)
> print(json.dumps(triples, ensure_ascii=False, indent=4))
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/知识图谱.pdf#page=14|知识图谱.pdf · 第 14–22 页]]
