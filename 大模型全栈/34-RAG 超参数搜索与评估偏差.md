---
type: 学习笔记
course: 大模型全栈
order: 34
stage: 检索增强
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/33-测试集构建与 RAGAS 评估流水线|33-测试集构建与 RAGAS 评估流水线]] · 下一篇：[[大模型全栈/35-论文系统：检索与生成的联合评测|35-论文系统：检索与生成的联合评测]]

> [!abstract] 学习目标
> 学习搜索流程，同时识别会让最优分数失真的标注方法。

## 核心理解

课堂网格遍历 chunk_size、overlap 与 top_k，以 NDCG@5 选择配置，再保存全部结果。一般而言，参数会同时改变语义完整性、候选覆盖、运行时间和上下文成本。

本例有一个关键评估问题：相关性只在当前返回候选里通过证据关键词重叠生成；如果没有相关文档，还把第一条结果强制标成相关。这样评价标准随系统输出变化，可能让坏结果也得到正分。

正确比较需要独立于候选建立的参考标准。若更改切片，应保留稳定源文档与证据范围，再映射到新切片；不能只给已经返回的结果打标签，把未召回的相关内容排除在 Recall 分母之外。

选参使用验证集，最终只在未参与选择的测试集上报告一次。代码从 val 缺省回退 test 的写法有助于演示，却不适合作为正式实验的默认策略。

## 课堂代码怎么读

先读 `evaluate_config`，特别检查 qrels 构造位置与“兜底”逻辑，再读网格循环。注意 `top_k=3` 却汇总 @5 时实际可返回数量不同，比较前应统一定义。

> [!warning] 易错点与资料边界
> 本篇保留原始课堂算法，不把其 best_score 当作可信性能结论。建议先修正固定标注、集合隔离与候选不足问题，再比较配置。

## 复盘练习

为什么把第一条结果兜底标为相关会抬高 MRR？

> [!question]- 参考思路
> 只要有返回结果，第一条就被人为赋予相关性，MRR 可因此获得很高甚至满分，评分失去了判断检索质量的独立依据。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中024 %%

> [!quote]- 大模型全栈（中）.md · 超参数调优
> 来源：原笔记第 1781–1944 行。
>
> **超参数调优**
>
> ```python
> """
> 超参数
> chunk_size chunk_overlap top_k similarity_score_threshold nprobe efSearch 权重
> 重排序候选  
> """
>
> import json
> import numpy as np
> from rank_bm25 import BM25Okapi
> import jieba
> from langchain_core.documents import Document
> from langchain_text_splitters import RecursiveCharacterTextSplitter
> from langchain_community.vectorstores import Chroma
> from langchain_community.embeddings import HuggingFaceEmbeddings
> from ranx import Qrels, Run, evaluate
>
> # 1. 准备测试集和知识库
> with open("./rag_testset.json", "r", encoding="utf-8") as f:
>     testset = json.load(f)
> val_data = testset.get("val", testset.get("test", []))
> print(f"验证集: {len(val_data)} 条")
>
> # 模拟知识库
> knowledge_docs = [
>     Document(page_content="检索增强生成（RAG）是一种结合信息检索和大语言模型的技术，由Facebook AI研究院于2020年提出。"),
>     Document(page_content="向量数据库专门存储高维向量，支持近似最近邻搜索。常见的有Chroma、FAISS、Milvus。"),
>     Document(page_content="混合检索结合BM25和向量检索，通过RRF融合策略合并结果，提升Recall和NDCG。"),
>     Document(page_content="重排序用Cross-Encoder模型重新计算候选文档的相关性，提升Top-K精度。"),
>     Document(page_content="RAG评估包括检索端（Precision/Recall/NDCG）和生成端（Faithfulness/Answer Relevance）。"),
> ]
>
> embeddings = HuggingFaceEmbeddings(
>     model_name="./bge-base-zh-v1.5",
>     model_kwargs={"device": "cpu"},
>     encode_kwargs={"normalize_embeddings": True},
> )
>
> # 2. 定义评估函数
> def evaluate_config(chunk_size, chunk_overlap, top_k):
>     """评估一组超参数配置的检索质量"""
>     splitter = RecursiveCharacterTextSplitter(
>         chunk_size=chunk_size, chunk_overlap=chunk_overlap,
>         separators=["\n\n", "\n", "。", "！", "？", " ", ""],
>     )
>     chunks = splitter.split_documents(knowledge_docs)
>     if len(chunks) == 0:
>         return {"recall@5": 0, "ndcg@5": 0, "mrr": 0}
>
>     vectorstore = Chroma.from_documents(chunks, embeddings)
>
>     tokenized = [list(jieba.cut(c.page_content)) for c in chunks]
>     bm25 = BM25Okapi(tokenized, k1=1.5, b=0.75)
>
>     qrels_dict, run_dict = {}, {}
>     for i, item in enumerate(val_data):
>         qid = f"q{i}"
>         question = item["question"]
>         evidence = item.get("evidence", "")
>
>         vec_results = vectorstore.similarity_search_with_score(question, k=top_k)
>         bm25_scores = bm25.get_scores(list(jieba.cut(question)))
>         bm25_top = np.argsort(bm25_scores)[::-1][:top_k]
>
>         vec_ranking = []
>         for doc,_ in vec_results:
>             for idx,c in enumerate(chunks):
>                 if c.page_content == doc.page_content:
>                     vec_ranking.append(idx)
>                     break
>
>         bm25_ranking = list(bm25_top)
>         fused = {}
>         for ranking in [vec_ranking, bm25_ranking]:
>             for rank, idx in enumerate(ranking):
>                 fused[idx] = fused.get(idx, 0) + 1 / (60 + rank + 1)
>
>         run_dict[qid] = {}
>         qrels_dict[qid] = {}
>
>         # 用 jieba 分词提取 evidence 关键词，过滤单字停用词
>         ev_tokens = set(jieba.cut(evidence)) if evidence else set()
>         ev_tokens = {t for t in ev_tokens if len(t) > 1 and t.strip()}
>
>         for rank, (idx, score) in enumerate(sorted(fused.items(), key=lambda x: x[1], reverse=True)[:top_k]):
>             if idx < len(chunks):
>                 doc_id = f"d_{idx}"
>                 run_dict[qid][doc_id] = float(score)
>                 content = chunks[idx].page_content
>
>                 # 用重叠比例而非精确匹配判断相关性
>                 if ev_tokens:
>                     content_tokens = set(jieba.cut(content))
>                     content_tokens = {t for t in content_tokens if len(t) > 1 and t.strip()}
>                     overlap = len(ev_tokens & content_tokens)
>                     overlap_ratio = overlap / len(ev_tokens)
>                     rel = (3 if overlap_ratio >= 0.7 else
>                            2 if overlap_ratio >= 0.4 else
>                            1 if overlap_ratio >= 0.15 else 0)
>                 else:
>                     rel = 0
>
>                 if rel > 0:
>                     qrels_dict[qid][doc_id] = rel
>
>         # 兜底，确保每个 query 至少有一个相关文档，避免 ranx 报错==
>         if not qrels_dict[qid] and run_dict[qid]:
>             first_doc = list(run_dict[qid].keys())[0]
>             qrels_dict[qid][first_doc] = 1
>
>     # 过滤掉 run 为空的 query
>     valid_qids = [qid for qid in run_dict if run_dict[qid]]
>     qrels_dict = {qid: qrels_dict[qid] for qid in valid_qids}
>     run_dict = {qid: run_dict[qid] for qid in valid_qids}
>
>     if not qrels_dict or not run_dict:
>         return {"recall@5": 0, "ndcg@5": 0, "mrr": 0}
>
>     qrels = Qrels(qrels_dict)
>     run = Run(run_dict)
>     results = evaluate(qrels, run, ["recall@5", "ndcg@5", "mrr"])
>     return {k: float(v) for k, v in results.items()}
>
> # 3. 网格搜索
> param_grid = {
>     "chunk_size": [200, 500, 1000],
>     "chunk_overlap": [20, 50, 100],
>     "top_k": [3, 5, 10],
> }
>
> print("\n开始网格搜索")
> best_score = -1
> best_params = None
> all_results = []
>
> for cs in param_grid["chunk_size"]:
>     for co in param_grid["chunk_overlap"]:
>         if co >= cs:  # overlap不能大于等于chunk_size
>             continue
>         for tk in param_grid["top_k"]:
>             metrics = evaluate_config(cs, co, tk)
>             score = metrics["ndcg@5"]  # 用NDCG@5作为优化目标
>             all_results.append({
>                 "chunk_size": cs, "chunk_overlap": co, "top_k": tk,
>                 **metrics,
>             })
>             print(f"  chunk_size={cs:<5} overlap={co:<4} top_k={tk:<3} | "
>                   f"Recall@5={metrics['recall@5']:.4f} NDCG@5={metrics['ndcg@5']:.4f} MRR={metrics['mrr']:.4f}")
>             if score > best_score:
>                 best_score = score
>                 best_params = {"chunk_size": cs, "chunk_overlap": co, "top_k": tk}
>
> print(f"\n最优配置")
> print(f"  chunk_size={best_params['chunk_size']}, overlap={best_params['chunk_overlap']}, top_k={best_params['top_k']}")
> print(f"  NDCG@5 = {best_score:.4f}")
>
> # 保存所有结果
> with open("./hyperparam_search.json", "w", encoding="utf-8") as f:
>     json.dump({"best": best_params, "best_score": best_score, "all": all_results}, f, ensure_ascii=False, indent=2)
> print("\n搜索结果已保存到 hyperparam_search.json")
> ```
>

## 资料与关联

- 本篇主要依据上述课堂代码补充讲解；相关讲义统一见 [[大模型全栈/资料/00-资料索引|资料索引]]。
