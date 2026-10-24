---
type: 学习笔记
course: 大模型全栈
order: 33
stage: 检索增强
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/32-RAG 评估：检索指标与生成指标|32-RAG 评估：检索指标与生成指标]] · 下一篇：[[大模型全栈/34-RAG 超参数搜索与评估偏差|34-RAG 超参数搜索与评估偏差]]

> [!abstract] 学习目标
> 让测试数据和评分过程成为可检查的实验材料。

## 核心理解

课堂流水线从知识片段生成问答对，再用模型过滤，检索相关上下文，划分数据，最后接入 RAGAS。需要特别注意：原代码把合成 QA 的参考答案直接填入 answer，没有另行调用待测 RAG 生成回答；因此它主要演示测试集与评价接线，不能据此衡量实际生成链质量。

合成问答能提高覆盖，但存在偏差：问题可能过度贴近原句，同一模型生成与过滤会保留共同盲点，相邻或重叠片段还可能泄漏到不同集合。正式评价应加入人工核验，并按文档或来源分组隔离。

每条样本应保存问题、参考答案、证据出处、参考片段身份、实际检索上下文和最终输出。保留模型版本、提示词、随机种子与异常状态，才能解释分数变化。

过滤掉失败请求会让剩余平均分看起来更好。更完整的报告需要同时展示成功率、失败数、耗时和评价分布，而不仅是平均分。

## 课堂代码怎么读

追踪生成链与过滤链，检查 qa_pairs 怎样落盘；再看同一问题如何得到检索片段、把 qa["answer"] 同时作为 answer 与 reference 写入 Dataset。区分构建测试集所用资料与检索语料的关系。

> [!warning] 易错点与资料边界
> 少量教学知识与模型自动生成标签仅适合验证流程，不能直接宣传为真实业务准确率。测试集应在调参前冻结，评价失败也应记录。

## 复盘练习

为什么随机切分 QA 对，未必能阻止泄漏？

> [!question]- 参考思路
> 同一源文档或相邻重叠片段生成的问题可能同时落入训练/验证/测试；需要按来源分组，检查文本与证据重叠。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中025 %%

> [!quote]- 大模型全栈（中）.md · 测试框架
> 来源：原笔记第 1945–2166 行。
>
> **测试框架**
>
> ```python
> """
> LLM 自动生成测试集
> """
> import os
> import json
> import random
> from langchain_core.documents import Document
> from langchain_text_splitters import RecursiveCharacterTextSplitter
> from langchain_openai import ChatOpenAI
> from langchain_core.prompts import ChatPromptTemplate
> from langchain_core.output_parsers import JsonOutputParser
> from langchain_community.embeddings import HuggingFaceEmbeddings
> from langchain_community.vectorstores import Chroma
> from datasets import Dataset
> from ragas import evaluate
> from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
> from ragas.llms import LangchainLLMWrapper
> from ragas.embeddings import LangchainEmbeddingsWrapper
> from dotenv import load_dotenv
>
> load_dotenv()
>
> # 1.知识库
> knowledge_docs = [
>     Document(
>         page_content="检索增强生成（RAG）是一种结合信息检索和大语言模型的技术。RAG由Facebook AI研究院于2020年提出，核心思想是在生成回答前先从外部知识库检索相关文档，然后将检索结果融入Prompt，从而减少LLM的幻觉问题。RAG系统通常包括离线索引阶段（文档加载、清洗、切片、向量化、存储）和在线查询阶段（查询向量化、检索、Prompt构建、生成）。"),
>     Document(
>         page_content="Python是一种高级编程语言，以简洁的语法和丰富的库生态著称。Python广泛应用于数据分析、机器学习、Web开发和自动化运维。Python的核心特点包括：动态类型、自动内存管理、支持多种编程范式。"),
>     Document(
>         page_content="向量数据库是专门用于存储和检索高维向量的数据库。与传统关系型数据库不同，向量数据库支持近似最近邻（ANN）搜索，能够在毫秒级内从数十亿向量中找到最相似的结果。常见的向量数据库包括Chroma、FAISS、Milvus、Pinecone和Weaviate。向量数据库的核心索引算法包括Flat、IVF、HNSW和PQ。"),
>     Document(
>         page_content="红烧肉是一道经典的中式菜肴，以五花肉为主料。制作步骤包括：切块焯水、炒糖色、炖煮收汁。关键技巧是火候控制和调料比例，好的红烧肉应该肥而不腻、入口即化。"),
>     Document(
>         page_content="混合检索结合了关键词检索（如BM25）和向量检索的优势。BM25擅长精确匹配（如专有名词、产品编号），向量检索擅长语义匹配（如同义表达、概念关联）。混合检索通过融合策略（如RRF倒数排名融合、加权线性组合）将两种检索结果合并，通常能显著提升Recall和NDCG。重排序是在混合检索的候选集基础上，用Cross-Encoder模型重新计算相关性，进一步提升Top-K精度。"),
>     Document(
>         page_content="北京是中国的首都，拥有丰富的历史文化遗产。著名景点包括故宫、天安门、长城、颐和园和天坛。最佳旅游季节是春秋两季，气候宜人，适合户外活动。"),
>     Document(
>         page_content="RAG系统的评估包括检索端评估和生成端评估。检索端评估指标包括Precision@K、Recall@K、MRR、MAP和NDCG@K。生成端评估通常使用RAGAS框架，核心指标有Faithfulness、Answer Relevance、Context Precision和Context Recall。评估的前提是构建高质量的测试集。"),
>     Document(
>         page_content="篮球是一项全球性的团队运动，每队5人上场。比赛目标是将球投入对方篮筐得分，三分线外投中得3分。NBA是世界最高水平的职业篮球联赛，汇聚了全球顶尖球员。"),
>     Document(
>         page_content="Embedding模型负责将文本转换为高维向量表示。常用的中文Embedding模型包括bge系列、m3e、text2vec和GTE。选择Embedding模型时需要考虑维度、推理速度、中文支持能力和向量空间质量。相似度计算通常使用余弦相似度，也可以使用点积或欧氏距离。Embedding模型的质量直接影响检索的Recall和Precision。"),
>     Document(
>         page_content="每天保证7-8小时睡眠对身体健康至关重要。均衡饮食应包含蛋白质、碳水化合物、脂肪、维生素和矿物质。适量运动可以增强心肺功能，建议每周至少150分钟中等强度运动。"),
>     Document(
>         page_content="Prompt工程是RAG系统中提升生成质量的关键环节。常见的Prompt策略包括：角色设定、少样本示例、思维链（CoT）、以及自我修正。好的Prompt可以显著提升答案的准确性、相关性和格式规范性。"),
>     Document(
>         page_content="React是一个用于构建用户界面的JavaScript库。React采用组件化开发模式，通过虚拟DOM提升渲染性能。Hooks是React 16.8引入的特性，让函数组件也能使用状态和生命周期。"),
>     Document(
>         page_content="咖啡是世界上最受欢迎的饮品之一，源自埃塞俄比亚。常见的咖啡种类包括美式、拿铁、卡布奇诺、摩卡和浓缩咖啡。咖啡豆的烘焙程度影响风味，浅烘偏酸，深烘偏苦。"),
>     Document(
>         page_content="日本是一个位于东亚的岛国，由四个主要岛屿组成。东京是日本的首都和最大城市，也是全球重要的经济中心。日本文化融合了传统与现代，樱花、富士山和新干线是其标志性符号。"),
> ]
> print(f"[知识库] {len(knowledge_docs)} 篇文档")
>
> # 2.切片
> splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
> all_chunks = splitter.split_documents(knowledge_docs)
> print(f"[切片总数] {len(all_chunks)} ")
>
> # 3.生成问答对(不同类型)
> llm = ChatOpenAI(
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     model="deepseek-chat",
>     temperature=0.7
> )
>
> # 问答对生成
> generate_prompt = ChatPromptTemplate.from_template("""你是一个专业的测试集构建专家。请基于以下文档片段，生成 {count} 个高质量问答对。
>
> 【要求】
> 1. 问题必须能从文档片段中找到答案（不能编造）
> 2. 问题类型多样化，覆盖以下类型：
>    - 事实型：问具体事实（如"RAG由谁提出？"）
>    - 推理型：需要推理或综合（如"为什么RAG能减少幻觉？"）
>    - 对比型：比较两个概念（如"向量数据库和传统数据库有什么区别？"）
>    - 总结型：需要概括总结（如"RAG系统包括哪些阶段？"）
> 3. 答案必须基于文档片段内容，简洁准确
> 4. 标注答案在文档片段中的依据（关键句子原文）
> 5. 以JSON数组输出，不要输出解释
>
> 【输出格式】
> [
>   {{
>     "question": "问题内容",
>     "answer": "答案内容",
>     "question_type": "事实型|推理型|对比型|总结型",
>     "evidence": "文档片段中的关键依据句子"
>   }}
> ]
>
> 【文档片段】
> {context}
>
> 【生成的问答对】""")
> generate_chain = generate_prompt | llm | JsonOutputParser()
>
> # 问答对质量过滤
> filter_prompt = ChatPromptTemplate.from_template("""请判断以下问答对是否合格。合格标准：
> 1. 问题能从文档片段中找到答案
> 2. 答案准确且基于文档内容
> 3. 问题表述清晰，不是太简单或太宽泛
>
> 只回答"合格"或"不合格"，不要解释。
>
> 问题：{question}
> 答案：{answer}
> 文档片段：{context}
> """)
> filter_chain = filter_prompt | llm
>
> # 批量生成+过滤
> random.seed(42)
> all_qa = []
> for i, chunk in enumerate(all_chunks):
>     try:
>         qa_pairs = generate_chain.invoke({"context": chunk.page_content, "count": 5})
>         for qa in qa_pairs:
>             filter_result = filter_chain.invoke({"context": chunk.page_content,
>                                                  "question": qa["question"],
>                                                  "answer": qa["answer"]
>                                                  })
>
>             # 不合格 ==> 合格  误判
>             if "合格" in filter_result.content and "不合格" not in filter_result.content:
>                 qa["source_chunk"] = chunk.page_content
>                 qa["chunk_id"] = i
>                 all_qa.append(qa)
>         print(f"[片段] {i + 1}/{len(all_chunks)} --> 累计合格: {len(all_qa)} 个")
>     except Exception as e:
>         print(f"片段 {i + 1} 生成失败")
>
> # 去重(问题)+统计
> seen = set()
> unique_qa = []
> for qa in all_qa:
>     q_key = qa["question"]
>     if q_key not in seen:
>         seen.add(q_key)
>         unique_qa.append(qa)
> type_dict = {}
> for qa in unique_qa:
>     t = qa.get("question_type", "未知")
>     type_dict[t] = type_dict.get(t, 0) + 1
> print(
>     f"[统计] 生成总数:{len(all_qa)}个,去重后:{len(unique_qa)}个, 类型分布:{json.dumps(type_dict, ensure_ascii=False)}")
>
> # 构建索引
> embeddings = HuggingFaceEmbeddings(
>     model_name="./bge-base-zh-v1.5",
>     model_kwargs={"device": "cpu"},
>     encode_kwargs={"normalize_embeddings": True}
> )
> vectorstore = Chroma.from_documents(
>     documents=all_chunks,
>     embedding=embeddings,
>     persist_directory="./chroma_db_test",
>     collection_name="test_ragas"
> )
>
> # 执行检索
> ragas_samples = []
> for qa in unique_qa:
>     search_results = vectorstore.similarity_search(qa["question"], k=4)
>     contexts = [doc.page_content for doc in search_results]
>
>     ragas_samples.append({
>         "question": qa["question"],
>         "answer": qa["answer"],
>         "contexts": contexts,
>         "reference": qa["answer"],
>         "question_type": qa["question_type"],
>         "evidence": qa["evidence"],
>
>     })
>
> # 划分测试集,验证集,训练集 16:40继续
> random.shuffle(ragas_samples)
> n = len(ragas_samples)
> testset = {
>     "train": ragas_samples[:int(n * 0.2)],
>     "val": ragas_samples[int(n * 0.2): int(n * 0.5)],
>     "test": ragas_samples[int(n * 0.5):],
> }
> with open("./ragas_testset.json", "w", encoding="utf-8") as f:
>     json.dump(testset, f, ensure_ascii=False, indent=2)
> print(f"[划分信息] 训练集:{len(testset['train'])} 条, 验证集:{len(testset['val'])} 条,测试集:{len(testset['test'])} 条")
>
> # 进行评估
> test_data = testset["test"]
> eval_dataset = Dataset.from_dict({
>     "question": [x["question"] for x in test_data],
>     "answer": [x["answer"] for x in test_data],
>     "contexts": [x["contexts"] for x in test_data],
>     "reference": [x["reference"] for x in test_data],
> })
>
> eval_llm = LangchainLLMWrapper(
>     ChatOpenAI(
>         api_key=os.getenv("DEEPSEEK_API_KEY"),
>         base_url=os.getenv("DEEPSEEK_BASE_URL"),
>         model="deepseek-chat",
>         temperature=0
>     ),
>     bypass_n = True
> )
> eval_emb = LangchainEmbeddingsWrapper(embeddings)
>
> result = evaluate(
>     eval_dataset,
>     metrics=[faithfulness,answer_relevancy,context_precision,context_recall],
>     llm=eval_llm,
>     embeddings=eval_emb,
>     raise_exceptions=False
> )
> print(result)
> ```
>

## 资料与关联

- 本篇主要依据上述课堂代码补充讲解；相关讲义统一见 [[大模型全栈/资料/00-资料索引|资料索引]]。
