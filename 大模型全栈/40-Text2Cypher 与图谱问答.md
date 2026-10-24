---
type: 学习笔记
course: 大模型全栈
order: 40
stage: 知识图谱
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/39-Neo4j、Cypher 与批量入库|39-Neo4j、Cypher 与批量入库]] · 下一篇：[[大模型全栈/41-GraphRAG：向量召回与关系扩展|41-GraphRAG：向量召回与关系扩展]]

> [!abstract] 学习目标
> 把自然语言问题转成结构化查询，再基于结果回答。

## 核心理解

Text2Cypher 先将图谱 Schema 与问题交给模型生成查询，再执行查询，最后把结构化结果组织成自然语言。它适合包含实体、关系、过滤与聚合的问题。

内置 GraphCypherQAChain 封装主要步骤；课堂自定义版本则展示提示词、代码围栏清理、错误反馈与重试。理解自定义版本后，更容易知道封装类内部需要哪些输入。

Schema 决定模型能引用哪些标签、属性与关系；错误或过时 Schema 会让查询反复失败。空结果也有不同原因：图谱没有事实、实体没对齐、查询方向错，或限制条件不符合。

回答应保留查询与实际结果，避免在空结果时把模型常识混作图谱事实。

## 课堂代码怎么读

并排跟踪两份代码的 Schema 注入、生成 Cypher、执行与答案链。自定义版本对写入关键词进行拦截并反馈异常，展示了控制层与生成层的分工。

> [!warning] 易错点与资料边界
> 关键词黑名单不足以构成数据库权限边界；应优先用只读账号和受限查询能力。内置链中允许危险请求的配置不是安全保证。PDF 仅提供知识图谱前置概念，具体实现依据课堂代码。

## 复盘练习

模型生成的查询能执行，但回答仍错，可能原因是什么？

> [!question]- 参考思路
> 查询语义可能偏离问题，例如关系方向、时间条件或聚合单位错；语法成功不等于业务语义正确，应保留查询与结果共同检查。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中008 %%

> [!quote]- 大模型全栈（中）.md · GraphCypherQAChain
> 来源：原笔记第 385–433 行。
>
> **GraphCypherQAChain**
>
> ```python
> """
> GraphCypherQAChain
> """
> from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
> from langchain_openai import ChatOpenAI
> import os
> from dotenv import load_dotenv
>
> load_dotenv()
>
> graph = Neo4jGraph(
>     url="bolt://localhost:7687",
>     username="neo4j",
>     password="12345678",
>     database="neo4j"
> )
>
> llm = ChatOpenAI(
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     model="deepseek-chat",
>     temperature=0
> )
>
> # 构建链路: 自然语言输入->LLM生成Cypher语句->执行查询->整理结果
> chain = GraphCypherQAChain.from_llm(
>     llm=llm,
>     graph=graph,
>     verbose=True,
>     allow_dangerous_requests=True,
>     return_intermediate_steps=True
> )
>
> question = "北京和深圳有多少人?"
> response = chain.invoke({"query": question})
>
> print(response["result"],"\n")
>
> # 中间步骤
> for step in response["intermediate_steps"]:
>     if "query" in step:
>         print(f"哈?step:{step['query']}")
>     if "context" in step:
>         print(f"结果:{step['context']}")
> ```
>

%% source-id: 中007 %%

> [!quote]- 大模型全栈（中）.md · 自定义实现
> 来源：原笔记第 251–384 行。
>
> **自定义实现**
>
> ```python
> """
> 自定义实现
> """
> from langchain_neo4j import Neo4jGraph
> from langchain_openai import ChatOpenAI
> import os
> import re
> from langchain_core.prompts import PromptTemplate
> from langchain_core.output_parsers import StrOutputParser
> from dotenv import load_dotenv
>
> load_dotenv()
>
> graph = Neo4jGraph(
>     url="bolt://localhost:7687",
>     username="neo4j",
>     password="12345678",
>     database="neo4j"
> )
>
> llm = ChatOpenAI(
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     model="deepseek-chat",
>     temperature=0
> )
>
> # 自定义 Cypher Prompt
> CYPHER_GENERATION = """
> 你是一个 Neo4j Cypher 查询专家。根据用户的自然语言问题和图谱 Schema，生成正确的 Cypher 查询语句。
> 【图谱 Schema】
> {schema}
> 【规则】
> 1. 只生成只读查询（MATCH/WITH/RETURN），禁止生成 CREATE/SET/DELETE/MERGE 等写操作
> 2. 使用正确的标签、关系类型和属性名，必须与 Schema 完全一致
> 3. 字符串匹配使用 CONTAINS 或 =，不要使用 LIKE
> 4. 分页使用 SKIP 和 LIMIT
> 5. 不要在 Cypher 中使用注释
> 6. 如果问题无法用当前 Schema 回答，返回 "无法回答"
> 7. 只返回 Cypher 语句本身，不要包含任何解释或 Markdown 代码块标记
> 【用户问题】
> {question}
> 【生成的 Cypher】
> """
> cypher_prompt = PromptTemplate(
>     input_variable=["schema", "question"],
>     template=CYPHER_GENERATION,
> )
>
> cypher_chain = cypher_prompt | llm | StrOutputParser()
>
> # 自定义问答
> def ask(question):
>     print(f"问题:{question}")
>     # 生成 cypher
>     cypher = cypher_chain.invoke({
>         "schema": graph.schema,
>         "question": question
>     })
>     cypher = re.sub(r"```cypher\s*", "", cypher)
>     cypher = re.sub(r"```\s*", "", cypher)
>     print(f"生成 cypher:{cypher}")
>     if "无法回答" in cypher:
>         return {
>             "answer": "抱歉,当前知识图谱无法回答这个问题",
>             "cypher": None, "result": None
>         }
>
>     # 出错自动重试
>     max_retries = 2
>     res_cypher = None
>     for attempt in range(max_retries + 1):
>         try:
>             # 安全执行
>             dangerous_keywords = ["CREATE", "SET", "DELETE", "MERGE", "DROP", "ALTER", "CALL", "REMOVE"]
>             cypher_upper = cypher.upper()
>             for kw in dangerous_keywords:
>                 if kw == "CALL" and "DB." in cypher_upper:
>                     continue
>                 if kw in cypher_upper:
>                     raise ValueError(f"安全拦截:禁止执行包含 {kw} 的查询")
>             res_cypher = graph.query(cypher)
>             print(f"查询结果:{res_cypher}")
>             break
>         except Exception as e:
>             print(f"执行失败(尝试{attempt + 1}/{max_retries + 1}):{e}")
>             if attempt < max_retries:
>                 # 把报错信息附加到问题,让LLM修正cypher
>                 cypher = cypher_chain.invoke({
>                     "schema": graph.schema,
>                     "question": f"{question}\n\n之前生成的 Cypher 执行报错:{e}\n请修正后重新生成"
>                 })
>                 cypher = re.sub(r"```cypher\s*", "", cypher).replace("```", "").strip()
>             else:
>                 return {"answer": f"查询失败:{e}", "cypher": None, "result": None}
>
>     # 生成答案
>     answer_prompt = PromptTemplate(
>         input_variable=["question", "cypher", "result"],
>         template="""你是一个知识图谱问答助手。根据用户问题、执行的 Cypher 和查询结果，生成简洁准确的自然语言回答。
> 【用户问题】{question}
> 【执行的 Cypher】{cypher}
> 【查询结果】{result}
> 【要求】
> 1. 直接回答问题，不要提及 Cypher 或查询过程
> 2. 如果结果为空，说明未找到相关信息
> 3. 数据要准确，不要编造结果中没有的信息
> 4. 回答简洁明了
> 【回答】
>         """)
>     answer_chain = answer_prompt | llm | StrOutputParser()
>     answer = answer_chain.invoke({
>         "question": question,
>         "cypher": cypher,
>         "result": str(res_cypher)
>     })
>
>     return {"answer": answer, "cypher": cypher, "result": res_cypher}
>
> # 测试
> questions = [
>     "北京和成都现在有多少人?",
>     "年龄最大的三个人是谁?",
>     "张三认识哪些人?",
>     "上海和北京哪个城市的人多?",
>     "有几家公司?每家公司分别有多少人?"
> ]
> for q in questions:
>     print(ask(q), "\n")
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/知识图谱.pdf#page=25|知识图谱.pdf · 第 25–27 页]]
