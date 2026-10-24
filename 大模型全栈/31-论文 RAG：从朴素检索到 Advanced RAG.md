---
type: 学习笔记
course: 大模型全栈
order: 31
stage: 检索增强
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/30-Cross-Encoder 与粗排精排|30-Cross-Encoder 与粗排精排]] · 下一篇：[[大模型全栈/32-RAG 评估：检索指标与生成指标|32-RAG 评估：检索指标与生成指标]]

> [!abstract] 学习目标
> 把前面的组件组合成一个可解释的论文问答系统。

## 核心理解

课堂以 arXiv 元信息与摘要构建 Document，元数据保留题名、作者、日期与链接，再完成切片、向量入库、检索和生成。这里检索的是代码实际收集的内容，不能笼统称为已阅读全文。

朴素版本使用单路向量检索；进阶版本引入多查询、BM25、RRF 和 Cross-Encoder。原笔记包含一个较早的 Advanced 入库片段与后续完整版本，本篇按功能演进顺序保留。

离线阶段应稳定保存语料快照、chunk ID 与索引配置。在线阶段才处理当前问题，并记录查询改写、候选、重排与引用。这样更容易判断改进来自哪个模块。

读项目时不要从第一行机械背到最后一行。先画出数据流，再逐个核对每个模块的输入输出与缓存文件：语料、向量库和 BM25 缓存必须对应同一版本。

## 课堂代码怎么读

按“朴素完整示例 → Advanced 早期入库片段 → Advanced 完整示例”阅读。关注加载已有 Chroma 的分支、BM25 与 chunk 的顺序对齐、去重方式，以及答案引用如何与 metadata 对应。

> [!warning] 易错点与资料边界
> 课堂从在线 arXiv 获取数据，重跑得到的语料可能不同。只检索摘要不能支持论文正文中的全部细节；若知识不足，应明确检索范围，而不是凭模型补全。

## 复盘练习

为什么更换切片规则后，不能直接复用旧 BM25 缓存？

> [!question]- 参考思路
> 缓存中的词项、顺序和文档身份属于旧切片；新向量库若不一致，融合时可能把一个片段的分数配到另一个片段。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中034 %%

> [!quote]- 大模型全栈（中）.md · 基于朴素RAG的论文检索
> 来源：原笔记第 2678–2820 行。
>
> **基于朴素RAG的论文检索**
>
> ```python
> """
> 基于Naive RAG实现论文检索系统
> """
> import os
> import arxiv
> from langchain_core.documents import Document
> from langchain_text_splitters import RecursiveCharacterTextSplitter
> from langchain_chroma import Chroma
> from langchain_huggingface import HuggingFaceEmbeddings
> from langchain_openai import ChatOpenAI
> from langchain_core.prompts import ChatPromptTemplate
> from langchain_core.output_parsers import StrOutputParser
> from langchain_core.runnables import RunnablePassthrough, RunnableLambda
> from dotenv import load_dotenv
>
> load_dotenv()
>
> # 1.从arXiv下载论文
> client = arxiv.Client()
> search = arxiv.Search(
>     query="cat:cs.AI AND (retrieval augmented generation OR RAG)",
>     max_results=50,
>     sort_by=arxiv.SortCriterion.Relevance
> )
> documents = []
> for paper in client.results(search):
>     content = (
>         f"标题: {paper.title}\n"
>         f"作者: {','.join(a.name for a in paper.authors)}\n"
>         f"发布日期: {paper.published.strftime('%Y-%m-%d')}\n"
>         f"摘要: {paper.summary}\n"
>         f"分类: {','.join(paper.categories)}\n"
>         f"链接: {paper.entry_id}"
>     )
>     documents.append(Document(
>         page_content=content,
>         metadata={
>             "title": paper.title,
>             "authors": ','.join(a.name for a in paper.authors),
>             "published": paper.published.strftime('%Y-%m-%d'),
>             "arxiv_id": paper.get_short_id(),
>             "url": paper.entry_id,
>             "source": "arxiv"
>         }
>     ))
> print(f"[数据加载]: 获取 {len(documents)} 篇论文")
>
> # 2.切片
> splitter = RecursiveCharacterTextSplitter(
>     chunk_size=500,
>     chunk_overlap=50,
>     separators=["\n\n", "\n", "。", "！", "？", " ", ""],
> )
> chunks = splitter.split_documents(documents)
> print(f"[切片] {len(documents)} 篇 --> {len(chunks)}个切片")
>
> # 3.构建Chroma索引
> embeddings = HuggingFaceEmbeddings(
>     model_name="./bge-base-zh-v1.5",
>     model_kwargs={"device": "cpu"},
>     encode_kwargs={"normalize_embeddings": True}
> )
>
> if not os.path.exists("./chroma_db_naive"):
>     vectorstore = Chroma.from_documents(
>         documents=chunks,
>         embedding=embeddings,
>         persist_directory="./chroma_db_naive",
>         collection_name="arxiv_naive"
>     )
>     print("[索引:] 向量库已保存")
> else:
>     vectorstore = Chroma(
>         persist_directory="./chroma_db_naive",
>         embedding_function=embeddings,
>         collection_name="arxiv_naive"
>     )
>     print("[索引:] 加载已有的向量库")
>
> # 4.构建 LCEL RAG链
> def format_doc(docs):
>     parts = []
>     for i, doc in enumerate(docs, 1):
>         parts.append(
>             f"[{i}] 标题: {doc.metadata['title']}\n"
>             f"  作者: {doc.metadata['authors']}\n"
>             f"  日期: {doc.metadata['published']}\n"
>             f"  内容: {doc.page_content}"
>         )
>     return "\n\n".join(parts)
>
> retriever = vectorstore.as_retriever(
>     search_type="similarity_score_threshold",
>     search_kwargs={"k": 5, "score_threshold": 0.5},
> )
>
> prompt = ChatPromptTemplate.from_template("""你是一个 AI 论文研究助手。请基于以下参考论文回答用户问题。
> 【核心规则】
> 1. 仅基于参考论文回答，不要使用外部知识
> 2. 每个事实性陈述必须标注来源编号，如[1][2]
> 3. 如果参考论文中没有相关信息，明确回答"根据现有论文无法回答"
> 4. 回答结构：先给直接结论，再给详细解释，最后列出引用论文
> 参考论文：
> {context}
> 用户问题：{question}
> 你的回答：""")
>
> llm = ChatOpenAI(
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     model="deepseek-chat",
>     temperature=0.3
> )
>
> rag_chain = (
>         {
>             "context": retriever | RunnableLambda(format_doc),
>             "question": RunnablePassthrough()
>         } | prompt | llm | StrOutputParser()
> )
> print("[RAG链] 构建完成")
>
> # 5.问答
> print(" axXiv 论文问答系统")
> while True:
>     question = input("你: ").strip()
>     if question.lower() == "q":
>         break
>
>     if not question:
>         continue
>
>     source_docs = retriever.invoke(question)
>     anwser = rag_chain.invoke(question)
>     print(f"AI回复: {anwser}\n")
>     for i, doc in enumerate(source_docs, 1):
>         print(
>             f" [{i}] {doc.metadata['title']} {doc.metadata['authors']} {doc.metadata['published']} {doc.metadata['arxiv_id']} {doc.metadata['url']}")
> ```
>

%% source-id: 中033 %%

> [!quote]- 大模型全栈（中）.md · 基于Advanced RAG的论文检索
> 来源：原笔记第 2575–2677 行。
>
> **基于Advanced RAG的论文检索**
>
> ```python
> """
> 基于Avanced  RAG实现论文检索系统
> 混合检索 + 查询改写 + 精排
> """
> import os
> import arxiv
> import json
> import pickle
> import jieba
> import numpy as np
> from rank_bm25 import BM25Okapi
> from sentence_transformers import CrossEncoder
> from langchain_core.documents import Document
> from langchain_text_splitters import RecursiveCharacterTextSplitter
> from langchain_huggingface import HuggingFaceEmbeddings
> from langchain_chroma import Chroma
> from langchain_openai import ChatOpenAI
> from langchain_core.prompts import ChatPromptTemplate
> from langchain_core.output_parsers import StrOutputParser
> from dotenv import load_dotenv
>
> load_dotenv()
>
> # 1.从arXiv下载论文
> client = arxiv.Client()
> search = arxiv.Search(
>     query="cat:cs.AI AND (retrieval augmented generation OR RAG)",
>     max_results=100,
>     sort_by=arxiv.SortCriterion.Relevance
> )
> documents = []
> for paper in client.results(search):
>     content = (
>         f"标题: {paper.title}\n"
>         f"作者: {','.join(a.name for a in paper.authors)}\n"
>         f"发布日期: {paper.published.strftime('%Y-%m-%d')}\n"
>         f"摘要: {paper.summary}\n"
>         f"分类: {','.join(paper.categories)}\n"
>         f"链接: {paper.entry_id}"
>     )
>     documents.append(Document(
>         page_content=content,
>         metadata={
>             "title": paper.title,
>             "authors": ','.join(a.name for a in paper.authors),
>             "published": paper.published.strftime('%Y-%m-%d'),
>             "arxiv_id": paper.get_short_id(),
>             "url": paper.entry_id,
>             "source": "arxiv"
>         }
>     ))
> print(f"[数据加载]: 获取 {len(documents)} 篇论文")
>
> # 2.切片
> splitter = RecursiveCharacterTextSplitter(
>     chunk_size=500,
>     chunk_overlap=50,
>     separators=["\n\n", "\n", "。", "！", "？", " ", ""],
> )
> chunks = splitter.split_documents(documents)
> print(f"[切片] {len(documents)} 篇 --> {len(chunks)}个切片")
>
> # 3.构建双向索引
> embeddings = HuggingFaceEmbeddings(
>     model_name="./bge-base-zh-v1.5",
>     model_kwargs={"device": "cpu"},
>     encode_kwargs={"normalize_embeddings": True}
> )
>
> if not os.path.exists("./chroma_db_advanced"):
>     vectorstore = Chroma.from_documents(
>         documents=chunks,
>         embedding=embeddings,
>         persist_directory="./chroma_db_advanced",
>         collection_name="arxiv_advanced"
>     )
>     tokenized_chunks = [list(jieba.cut(c.page_content)) for c in chunks]
>     bm25 = BM25Okapi(tokenized_chunks, k1=1.5, b=0.75)
>     with open("./chroma_db_advanced/bm25_index.pkl", "wb") as f:
>         pickle.dump({"bm25": bm25, "chunks": chunks}, f)
>
>     print("[双索引] 构建完成")
> else:
>     vectorstore = Chroma(
>         persist_directory="./chroma_db_advanced",
>         embedding_function=embeddings,
>         collection_name="arxiv_advanced"
>     )
>     with open("./chroma_db_advanced/bm25_index.pkl", "wb") as f:
>         data = pickle.load(f)
>         bm25 = data["bm25"]
>         chunks = data["chunks"]
>     print("[双索引] 加载已有索引")
>
> # 4.查询改写链
> # 5.答案生成链
> # 6.交互问答
> # 未完待续~~
> ```
>

%% source-id: 中031 %%

> [!quote]- 大模型全栈（中）.md · 基于Advanced RAG的论文检索
> 来源：原笔记第 2349–2570 行。
>
> **基于Advanced RAG的论文检索**
>
> ```python
> """
> 基于Avanced  RAG实现论文检索系统
> 混合检索 + 查询改写 + 精排
> """
> import os
> import arxiv
> import json
> import pickle
> import jieba
> import numpy as np
> from rank_bm25 import BM25Okapi
> from sentence_transformers import CrossEncoder
> from langchain_core.documents import Document
> from langchain_text_splitters import RecursiveCharacterTextSplitter
> from langchain_huggingface import HuggingFaceEmbeddings
> from langchain_chroma import Chroma
> from langchain_openai import ChatOpenAI
> from langchain_core.prompts import ChatPromptTemplate
> from langchain_core.output_parsers import StrOutputParser
> from dotenv import load_dotenv
>
> load_dotenv()
>
> # 1.从arXiv下载论文
> client = arxiv.Client(
>     page_size=5,
>     delay_seconds=5,
>     num_retries=5
> )
>
> search = arxiv.Search(
>     query="cat:cs.AI AND (retrieval augmented generation OR RAG)",
>     max_results=30,
>     sort_by=arxiv.SortCriterion.Relevance
> )
> documents = []
> for paper in client.results(search):
>     content = (
>         f"标题: {paper.title}\n"
>         f"作者: {','.join(a.name for a in paper.authors)}\n"
>         f"发布日期: {paper.published.strftime('%Y-%m-%d')}\n"
>         f"摘要: {paper.summary}\n"
>         f"分类: {','.join(paper.categories)}\n"
>         f"链接: {paper.entry_id}"
>     )
>     documents.append(Document(
>         page_content=content,
>         metadata={
>             "title": paper.title,
>             "authors": ','.join(a.name for a in paper.authors),
>             "published": paper.published.strftime('%Y-%m-%d'),
>             "arxiv_id": paper.get_short_id(),
>             "url": paper.entry_id,
>             "source": "arxiv"
>         }
>     ))
> print(f"[数据加载]: 获取 {len(documents)} 篇论文")
>
> # 2.切片
> splitter = RecursiveCharacterTextSplitter(
>     chunk_size=500,
>     chunk_overlap=50,
>     separators=["\n\n", "\n", "。", "！", "？", " ", ""],
> )
> chunks = splitter.split_documents(documents)
> print(f"[切片] {len(documents)} 篇 --> {len(chunks)}个切片")
>
> # 3.构建双向索引
> embeddings = HuggingFaceEmbeddings(
>     model_name="./bge-base-zh-v1.5",
>     model_kwargs={"device": "cpu"},
>     encode_kwargs={"normalize_embeddings": True}
> )
>
> if not os.path.exists("./chroma_db_advanced"):
>     vectorstore = Chroma.from_documents(
>         documents=chunks,
>         embedding=embeddings,
>         persist_directory="./chroma_db_advanced",
>         collection_name="arxiv_advanced"
>     )
>     tokenized_chunks = [list(jieba.cut(c.page_content)) for c in chunks]
>     bm25 = BM25Okapi(tokenized_chunks, k1=1.5, b=0.75)
>     with open("./chroma_db_advanced/bm25_index.pkl", "wb") as f:
>         pickle.dump({"bm25": bm25, "chunks": chunks}, f)
>
>     print("[双索引] 构建完成")
> else:
>     vectorstore = Chroma(
>         persist_directory="./chroma_db_advanced",
>         embedding_function=embeddings,
>         collection_name="arxiv_advanced"
>     )
>     with open("./chroma_db_advanced/bm25_index.pkl", "rb") as f:
>         data = pickle.load(f)
>         bm25 = data["bm25"]
>         chunks = data["chunks"]
>     print("[双索引] 加载已有索引")
>
> # 4.查询改写链
> multi_query_prompt = ChatPromptTemplate.from_template("""你是一个学术检索查询改写专家。
> 请针对用户的研究问题，从 {count} 个不同的语义角度生成 {count} 个检索查询。
> 要求：
> 1. 每个查询从不同角度切入（方法角度、应用角度、对比角度等）
> 2. 查询应包含核心英文术语（RAG、retrieval、dense retrieval等）
> 3. 以JSON数组格式输出，如 ["query1", "query2", "query3"]
> 4. 不要输出解释，只输出JSON
> 原始问题：{question}
> 生成的查询：""")
>
> llm = ChatOpenAI(
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     model="deepseek-chat",
>     temperature=0.3
> )
>
> multi_query_chain = multi_query_prompt | llm | StrOutputParser()
>
> # 5.答案生成链
> answer_prompt = ChatPromptTemplate.from_template("""你是一个资深 AI 论文研究助手。请基于以下经过重排序的论文片段回答用户问题。
> 【核心规则】
> 1. 仅基于参考论文回答，禁止使用外部知识
> 2. 每个事实必须标注来源编号 [1][2]，并优先引用相关度高的来源
> 3. 如果论文之间有矛盾，指出矛盾并分别陈述
> 4. 如果参考论文不足以回答，明确说明"现有论文不足以回答该问题"
> 5. 回答结构：直接结论 → 详细分析 → 引用论文列表
> 参考论文（按相关度排序）：
> {context}
> 研究问题：{question}
> 回答：""")
> answer_chain = answer_prompt | llm | StrOutputParser()
>
> # 6.交互问答
> print(" axXiv 论文问答系统")
> while True:
>     question = input("你: ").strip()
>     if question.lower() == "q":
>         break
>
>     if not question:
>         continue
>
>     raw = multi_query_chain.invoke({"question": question, "count": 3})
>     try:
>         queries = json.loads(raw)
>         if len(queries) == 0 or not isinstance(queries, list):
>             queries = [question]
>     except Exception as e:
>         queries = [question]
>
>     if question not in queries:
>         queries.insert(0, question)
>
>     # 对每个查询做混合检索,合并信息
>     all_candidates = {}
>     for q in queries:
>         # 向量检索
>         vec_results = vectorstore.similarity_search_with_score(q, k=25)
>         vec_ranking = []
>         # 遍历检索的结果,得到doc对象,找到该doc在全局chunks切片列表里的下标索引
>         for doc, _ in vec_results:
>             for i, c in enumerate(chunks):
>                 if c.page_content == doc.page_content:
>                     vec_ranking.append(i)
>                     break
>         # BM检索
>         bm25_scores = bm25.get_scores(list(jieba.cut(q)))
>         bm25_rank = list(np.argsort(bm25_scores)[::-1][:25])
>
>         # RRF融合
>         fused = {}
>         for ranking in [vec_ranking, bm25_rank]:
>             for rank, idx in enumerate(ranking):
>                 fused[idx] = fused.get(idx, 0) + 1 / (60 + rank + 1)
>
>         # 多查询合并候选集,去重
>         for idx, score in fused.items():
>             # key 文本 value元组 (文档对象,累计总分数)
>             key = chunks[idx].page_content
>             if key not in all_candidates:
>                 all_candidates[key] = (chunks[idx], 0)
>
>             all_candidates[key] = (chunks[idx], all_candidates[key][1] + score)
>     candidates = sorted(all_candidates.values(), key=lambda x: x[1], reverse=True)
>     print(f"[混合检索] 多查询合并后,共 {len(candidates)} 个唯一候选")
>
>     # 重排序
>     pairs = [[question, chunk.page_content] for chunk, _ in candidates]
>     reranker = CrossEncoder("./bge-reranker-v2-m3")
>     rerank_scores = reranker.predict(pairs)
>     # 粗排+精排的格式: 文档元组 重排分数  ((chunk,rrf_score),rerank_scores) ((Doc,0.85),0.93)
>     ranked = sorted(zip(candidates, rerank_scores), key=lambda x: x[1], reverse=True)[:5]
>     # 精排后的格式: (chunk, rerank_scores)  (Doc,0.93)
>     reranked = [(chunk, float(s)) for (chunk, _), s in ranked]
>     print(f"[重排序] {len(candidates)} 个候选")
>
>     # 构建上下文+生成回答
>     context_parts = []
>     for i, (doc, score) in enumerate(reranked, 1):
>         context_parts.append(
>             f"[{i}] [相关度: {score}]"
>             f"标题:{doc.metadata['title']}"
>             f"日期:{doc.metadata['published']}"
>             f"内容:{doc.page_content}"
>         )
>
>     context = "\n\n".join(context_parts)
>     answer = answer_chain.invoke({"context": context, "question": question})
>     print(f"\n {answer} \n")
>     for i, (doc, score) in enumerate(reranked, 1):
>         print(
>             f"[{i}] [相关度: {score}]"
>             f"标题:{doc.metadata['title']}"
>             f"日期:{doc.metadata['published']}"
>             f"内容:{doc.page_content}"
>         )
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/6.RAG综合项目.pdf#page=1|6.RAG综合项目.pdf · 第 1–21 页]]
- 关联知识：[[大模型全栈/25-文本切片：固定、递归、结构与语义|25-文本切片：固定、递归、结构与语义]]、[[大模型全栈/28-查询改写与多查询召回|28-查询改写与多查询召回]]、[[大模型全栈/29-BM25、向量检索与融合排序|29-BM25、向量检索与融合排序]]、[[大模型全栈/30-Cross-Encoder 与粗排精排|30-Cross-Encoder 与粗排精排]]、[[大模型全栈/35-论文系统：检索与生成的联合评测|35-论文系统：检索与生成的联合评测]]。
