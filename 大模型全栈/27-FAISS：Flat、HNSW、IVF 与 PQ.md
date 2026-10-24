---
type: 学习笔记
course: 大模型全栈
order: 27
stage: 检索增强
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/26-最小 RAG：检索、上下文与生成|26-最小 RAG：检索、上下文与生成]] · 下一篇：[[大模型全栈/28-查询改写与多查询召回|28-查询改写与多查询召回]]

> [!abstract] 学习目标
> 理解近似检索如何在速度、内存和召回之间取舍。

## 核心理解

Flat 逐一比较全部向量，适合基准与较小数据；HNSW 用分层近邻图加速搜索；IVF 先聚类，查询只访问部分簇；PQ 把向量分块压缩，减少存储与距离计算开销。

| 索引 | 主要思路 | 重点参数与代价 |
| --- | --- | --- |
| Flat | 全量精确比较 | 内存与查询量随数据增长 |
| HNSW | 图搜索 | M、efSearch；速度与召回取舍 |
| IVF | 先粗分簇 | nlist、nprobe；需要训练 |
| IVF-PQ | 分簇并压缩 | 子空间数、编码位数与精度 |

课堂用 Flat 的近邻作为 ground truth，比较其他索引的 Top-K 重合比例。这测量的是近似索引相对精确向量搜索的召回，不是业务问答正确率。

距离定义也要一致。FAISS 的 L2 通常返回平方欧氏距离，越小越近；内积越大越近。文档与查询都归一化后，最大内积才可对应余弦相似度。

## 课堂代码怎么读

先看 FAQ 的 `IndexFlatIP` 与归一化，再看 HNSW、IVF 训练、IVF-PQ 压缩，最后读统一比较函数。把建库、训练、搜索耗时分开观察。

> [!warning] 易错点与资料边界
> 随机向量实验不能替代真实语料评估。维度要满足 PQ 分块配置，训练数据量也应支持聚类；相似度阈值的方向不能与距离阈值混用。
>
> 课堂 HNSW 输出行末尾混入“吧”，会触发语法错误；这是复制文本中的杂字，原代码仍按原文保留。

## 复盘练习

把 nprobe 调到覆盖全部簇会怎样？

> [!question]- 参考思路
> 通常提高 IVF 对精确搜索的接近程度，但查询开销也增加；压缩索引仍可能存在量化误差。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中043 %%

> [!quote]- 大模型全栈（中）.md · 暴力索引
> 来源：原笔记第 3260–3318 行。
>
> **暴力索引**
>
> ```python
> """
> 暴力索引
> """
> import os
> import faiss
> from sentence_transformers import SentenceTransformer
>
> # 数据
> faq_data = [
>     {"q": "年假有多少天？", "a": "入职满1年享5天年假，满10年享10天，满20年享15天。"},
>     {"q": "社保基数怎么算？", "a": "以上年度月平均工资为基数，最低不低于当地最低工资的60%。"},
>     {"q": "离职需要提前多久？", "a": "正式员工需提前30天书面通知，试用期提前3天。"},
>     {"q": "公积金提取条件是什么？", "a": "购房、租房、离职、退休等情况均可申请提取。"},
>     {"q": "加班费怎么计算？", "a": "工作日加班1.5倍，休息日2倍，法定节假日3倍。"}
> ]
>
> # 向量化
> model = SentenceTransformer('./bge-base-zh-v1.5')
>
> faq_questions = [item['q'] for item in faq_data]
> faq_vec = model.encode(faq_questions, convert_to_numpy=True).astype("float32")
>
> # 构建索引
> faiss.normalize_L2(faq_vec)
>
> # 空的索引对象(暴力检索,使用内积度量)
> index = faiss.IndexFlatIP(faq_vec.shape[1])
>
> # 添加
> index.add(faq_vec)
>
> # 提问
> user_questions = [
>     "我能休几天年假?",
>     "RAG是什么?",
>     "我想辞职能提前说嘛?"
> ]
>
> for q in user_questions:
>     q_vec = model.encode([q], convert_to_numpy=True).astype("float32")
>
>     faiss.normalize_L2(q_vec)
>
>     scores, indices = index.search(q_vec, 1)
>
>     best_idx = indices[0][0]
>     best_scores = scores[0][0]
>
>     if best_scores >= 0.6:
>         print(f"提问:{q}")
>         print(f"匹配问题:{faq_data[best_idx]['q']},相似度:{best_scores}")
>         print(f"回答:{faq_data[best_idx]['a']}")
>     else:
>         print(f"相似度:{best_scores},低于阈值0.6")
> ```
>

%% source-id: 中042 %%

> [!quote]- 大模型全栈（中）.md · HNSW索引
> 来源：原笔记第 3216–3259 行。
>
> **HNSW索引**
>
> ```python
> """
> 分层导航小世界图
> """
> import numpy as np
> import faiss
> import time
>
> np.random.seed(42)
> N = 100000
> d = 768
> K = 5
>
> # 数据
> database_vec = np.random.randn(N, d).astype("float32")
> faiss.normalize_L2(database_vec)
>
> # 问题
> query_vec = np.random.randn(1, d).astype("float32")
> faiss.normalize_L2(query_vec)
>
> # 构建
> index_hnsw = faiss.IndexHNSWFlat(d, 32)
> index_hnsw.hnsw.efConstruction = 200
>
> start = time.time()
> index_hnsw.add(database_vec)
> build_time = time.time() - start
> print(f"HNSW构建时间:{build_time}")
> print(f"HNSW层数:{index_hnsw.hnsw.max_level}")
>
> # 查询
> index_hnsw.hnsw.efSearch = 100  # 平衡速度和召回率
> start = time.time()
> distances, indices = index_hnsw.search(query_vec, K)
> query_time = time.time() - start
> print(f"HNSW查询耗时:{query_time * 1000}ms")
>
> for i in range(K):
>     print(f" 排名{i + 1},索引={indices[0][i]},距离={distances[0][i]}")    吧 
> ```
>

%% source-id: 中041 %%

> [!quote]- 大模型全栈（中）.md · IVF-PQ
> 来源：原笔记第 3177–3215 行。
>
> **IVF-PQ**
>
> ```python
> """
> 倒排索引+乘积量化
> """
> import faiss
> import numpy as np
>
> np.random.seed(0)
>
> N = 100000
> dim = 128
>
> query = np.random.randn(10, dim).astype(np.float32)
> database = np.random.randn(N, dim).astype(np.float32)
>
> # IVF-Flat
> quantizer = faiss.IndexFlatL2(dim)
> # 向量库官方: nlist = 4 * sqrt(N)
> index = faiss.IndexIVFFlat(quantizer, dim, 256)
> index.train(database)
> index.add(database)
> index.nprobe = 16
>
> # IVF-PQ
> index_pq = faiss.IndexIVFPQ(quantizer, dim, 256, 8, 8)
> index_pq.train(database)
> index_pq.add(database)
> index_pq.nprobe = 16
>
> # 内存占比
> men_flat = N * dim * 4
> men_pq = N * dim * 1
>
> print(f"FLAT:{men_flat / 1024 / 1024}MB")
> print(f"PQ:{men_pq / 1024 / 1024}MB")
> ```
>

%% source-id: 中040 %%

> [!quote]- 大模型全栈（中）.md · 四种索引算法对比
> 来源：原笔记第 3088–3176 行。
>
> **四种索引算法对比**
>
> ```python
> """
> 不同算法的索引对比
> """
> import numpy as np
> import faiss
> import time
>
> np.random.seed(42)
> N = 100000
> d = 768
> K = 10
>
> database_vectors = np.random.randn(N, d).astype("float32")
> faiss.normalize_L2(database_vectors)
> query_vectors = np.random.randn(100, d).astype("float32")  # 100个查询取平均
> faiss.normalize_L2(query_vectors)
>
> # Ground Truth
> index_flat_gt = faiss.IndexFlatL2(d)
> index_flat_gt.add(database_vectors)
> _, gt_indices = index_flat_gt.search(query_vectors, K)
>
> def evaluate_index(index, name, train_data=None):
>     # 训练（如果需要）
>     if train_data is not None and not index.is_trained:
>         start = time.time()
>         index.train(train_data)
>         train_t = time.time() - start
>     else:
>         train_t = 0
>
>     # 构建
>     start = time.time()
>     index.add(database_vectors)
>     build_t = time.time() - start
>
>     # 查询
>     start = time.time()
>     _, pred_indices = index.search(query_vectors, K)
>     query_t = (time.time() - start) * 1000 / len(query_vectors)
>
>     # 召回率
>     recalls = []
>     for i in range(len(query_vectors)):
>         recall = len(set(gt_indices[i]) & set(pred_indices[i])) / K
>         recalls.append(recall)
>     avg_recall = np.mean(recalls)
>
>     return {
>         "name": name,
>         "train_time": train_t,
>         "build_time": build_t,
>         "query_time_ms": query_t,
>         "recall": avg_recall,
>     }
>
> # 测试四种索引
> results = []
>
> # 1. Flat
> results.append(evaluate_index(faiss.IndexFlatL2(d), "Flat"))
>
> # 2. HNSW
> idx = faiss.IndexHNSWFlat(d, 32)
> idx.hnsw.efConstruction = 200
> idx.hnsw.efSearch = 100
> results.append(evaluate_index(idx, "HNSW(M=32,ef=100)"))
>
> # 3. IVF
> quantizer = faiss.IndexFlatL2(d)
> idx = faiss.IndexIVFFlat(quantizer, d, 256)
> idx.nprobe = 16
> results.append(evaluate_index(idx, "IVF(nlist=256,nprobe=16)", database_vectors))
>
> # 4. LSH
> idx = faiss.IndexLSH(d, 128)
> results.append(evaluate_index(idx, "LSH(128bit)", database_vectors))
>
> # 打印对比
> print(f"{'算法':<25} {'训练(s)':<10} {'构建(s)':<10} {'查询(ms)':<12} {'召回率@10':<12}")
> print("-" * 70)
> for r in results:
>     print(f"{r['name']:<25} {r['train_time']:<10.2f} {r['build_time']:<10.2f} "
>           f"{r['query_time_ms']:<12.2f} {r['recall']:<12.2%}")
> ```
>

## 资料与关联

- 本篇主要依据上述课堂代码补充讲解；相关讲义统一见 [[大模型全栈/资料/00-资料索引|资料索引]]。
- [FAISS 官方说明：距离与余弦相似度](https://github.com/facebookresearch/faiss/wiki/MetricType-and-distances)：查询与文档共同归一化后，可以用内积检索余弦相似度。（补充核对日期：2026-10-25）
- 关联知识：[[大模型全栈/08-句向量、池化与 Embedding 接口|08-句向量、池化与 Embedding 接口]]、[[大模型全栈/26-最小 RAG：检索、上下文与生成|26-最小 RAG：检索、上下文与生成]]、[[大模型全栈/34-RAG 超参数搜索与评估偏差|34-RAG 超参数搜索与评估偏差]]。
