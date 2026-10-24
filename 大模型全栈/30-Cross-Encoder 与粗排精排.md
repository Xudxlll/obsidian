---
type: 学习笔记
course: 大模型全栈
order: 30
stage: 检索增强
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/29-BM25、向量检索与融合排序|29-BM25、向量检索与融合排序]] · 下一篇：[[大模型全栈/31-论文 RAG：从朴素检索到 Advanced RAG|31-论文 RAG：从朴素检索到 Advanced RAG]]

> [!abstract] 学习目标
> 用便宜的召回找候选，再用更细的匹配选证据。

## 核心理解

双编码器分别编码问题和文档，文档向量可以预计算，适合从大量数据快速召回。Cross-Encoder 将问题与候选文本一起输入，直接判断二者匹配程度，通常用于较小候选集的重排序。

课堂流程是 BM25 与向量召回 → RRF 粗排 → Cross-Encoder 精排 → 截取最终上下文。两个阶段的 K 不相同：先保留较多候选，再把有限上下文预算留给较相关的片段。

重排只能重评已经召回的候选；正确证据没进入候选集，重排无法凭空找回。因此调参时要同时看召回覆盖与最终 Top-K 精度。

证据过于重复也会浪费上下文。重排后仍可按来源、相邻片段或文本相似度去重，兼顾覆盖面与相关性。

## 课堂代码怎么读

看 `coarse_indices` 如何从融合排名产生，再看 `(question, document)` 成对送入 CrossEncoder。最后检查排序方向和最终选取数量。课堂只给出重排模型的本地路径线索，没有附该模型包。

> [!warning] 易错点与资料边界
> Cross-Encoder 分数的范围与含义取决于模型及配置，不必然是 0 到 1 的概率。候选增加会增加计算量，应把精排延迟计入端到端耗时。
>
> “交叉编码器”小节仅残留 +. 等内容，不能作为可执行实现；完整精排示例在后一份“粗排+精排”中。

## 复盘练习

增加最终 Top-K 是否一定提升回答？

> [!question]- 参考思路
> 不一定。可能补入噪声和重复片段，稀释关键条件，还可能挤占输出预算；应同时评估证据覆盖与生成质量。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中036 %%

> [!quote]- 大模型全栈（中）.md · 交叉编码器
> 来源：原笔记第 2917–2926 行。
>
> **交叉编码器**
>
> ```python
> """
> 交叉编码器-精排
> """
>
> +.
> ```
>

%% source-id: 中035 %%

> [!quote]- 大模型全栈（中）.md · 粗排+精排
> 来源：原笔记第 2821–2916 行。
>
> **粗排+精排**
>
> ```python
> """
> 先粗排后精排
> """
> from rank_bm25 import BM25Okapi
> import jieba
> from sentence_transformers import SentenceTransformer, CrossEncoder
> import numpy as np
>
> # 文档
> documents = [
>     "RAG通过检索外部知识库增强大语言模型，结合重排序可以显著提高最终检索准确率。",
>     "查询改写技术通过优化用户提问表达方式，使检索系统更容易命中相关文档。",
>     "对召回结果进行Cross-Encoder精排是提升RAG系统Top-K准确率的关键步骤。",
>     "通过多路召回融合策略，可以综合不同检索算法的优势，提高整体检索效果。",
>     "动态调整文档切片粒度，能够使检索结果更精准地匹配用户查询意图。",
>     "RAG并不能提高检索准确率，外部知识库的噪声反而会降低检索质量。",
>     "增加检索返回数量不会提高准确率，只会引入更多无关文档。",
>     "在医学影像检索系统中，RAG技术用于辅助医生快速定位相似病例。",
>     "法律文书检索中，BM25算法是最常用的基线方法之一。",
>     "电商商品检索系统通过向量召回提高商品匹配准确率。",
>     "对初筛候选集进行二次打分排序，可以有效过滤噪声并提升最终结果质量。",
>     "Embedding模型的语义理解能力直接决定了向量检索的上限和准确率。",
>     "通过相关性反馈机制迭代优化检索策略，是提升准确率的有效途径。",
>     "RAG系统架构通常包括文档加载、切片、向量化、检索和生成五个模块。",
>     "Chroma是一个轻量级向量数据库，支持持久化存储和相似度查询。",
>     "FAISS通过近似最近邻算法实现亿级向量的毫秒级检索。",
>     "递归字符切片是RAG系统中最常用的文档切分方法。",
>     "Python是一种高级编程语言，支持面向对象和函数式编程范式。",
>     "PyTorch是深度学习框架，提供动态计算图和自动微分功能。",
>     "Transformer架构由编码器和解码器组成，核心是自注意力机制。",
>     "MySQL是关系型数据库，支持事务和ACID特性。",
>     "Redis是内存数据库，常用于缓存和会话存储。",
>     "Docker容器化技术可以实现应用的快速部署和隔离运行。",
>     "Kubernetes用于容器编排，支持自动扩缩容和服务发现。",
>     "Git是分布式版本控制系统，支持分支管理和合并。",
>     "Linux操作系统由内核、shell和文件系统组成。",
>     "TCP协议通过三次握手建立可靠连接。",
>     "React是前端框架，采用虚拟DOM和组件化开发。",
>     "混合检索将BM25关键词匹配与向量语义检索结合，有效提升召回率和准确率。",
>     "微服务架构将单体应用拆分为多个独立服务。",
>     "Elasticsearch是分布式搜索引擎，基于倒排索引。",
>     "Nginx是高性能Web服务器和反向代理。",
>     "梯度下降是机器学习中最常用的优化算法。",
>     "卷积神经网络CNN擅长处理图像数据。",
>     "BERT通过掩码语言模型预训练获取上下文表示。",
>     "知识图谱用三元组表示实体和关系。",
>     "强化学习通过奖励信号指导智能体决策。",
>     "LoRA通过低秩矩阵实现大模型的高效微调。",
>     "量化技术将FP32权重压缩为INT8，减少显存占用。",
>     "扩散模型通过逐步去噪生成高质量图像。",
> ]
>
> query = "RAG如何提高检索准确率？"
>
> # 第一阶段:粗排
> # BM25检索
> tokenized_docs = [list(jieba.cut(doc)) for doc in documents]
> bm25 = BM25Okapi(tokenized_docs, k1=1.5, b=0.75)
> tokenized_query = list(jieba.cut(query))
> bm_scores = bm25.get_scores(tokenized_query)
> bm25_rank = np.argsort(bm_scores)[::-1]  # 降序
>
> # 向量检索
> model = SentenceTransformer("./bge-base-zh-v1.5")
> query_vec = model.encode([query], normalize_embeddings=True)
> doc_vec = model.encode(documents, normalize_embeddings=True)
> vec_scores = np.dot(doc_vec, query_vec.T).flatten()
> vec_rank = np.argsort(vec_scores)[::-1]
>
> # RRF融合
> rrf_scores = np.zeros(len(documents))
> for rank, doc_idx in enumerate(bm25_rank):
>     rrf_scores[doc_idx] += 1 / (60 + rank + 1)
>
> for rank, doc_idx in enumerate(vec_rank):
>     rrf_scores[doc_idx] += 1 / (60 + rank + 1)
>
> rrf_rank = np.argsort(rrf_scores)[::-1]
> coarse_indices = rrf_rank[:25]
> coarse_docs = [documents[i] for i in coarse_indices]
> print(f"粗排完成:召回TOP25~ {coarse_docs}")
>
> # 第二阶段:精排
> model = CrossEncoder("./bge-reranker-v2-m3")
> pairs = [[query, doc] for doc in coarse_docs]
> rerank_scores = model.predict(pairs)
> rerank_rank = np.argsort(rerank_scores)[::-1]
> final_top5 = [(coarse_indices[i], rerank_scores[i]) for i in rerank_rank[:5]]
>
> for i, (idx, score) in enumerate(final_top5, 1):
>     print(f"{i}: {score},{documents[i]}")
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/6.RAG综合项目.pdf#page=11|6.RAG综合项目.pdf · 第 11–18 页]]
