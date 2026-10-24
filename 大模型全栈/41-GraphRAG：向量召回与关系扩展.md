---
type: 学习笔记
course: 大模型全栈
order: 41
stage: 知识图谱
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/40-Text2Cypher 与图谱问答|40-Text2Cypher 与图谱问答]] · 下一篇：[[大模型全栈/42-工具调用：Schema、执行与结果回传|42-工具调用：Schema、执行与结果回传]]

> [!abstract] 学习目标
> 先找到相关实体，再沿关系补充上下文。

## 核心理解

课堂混合图 RAG 的路径是：为业务节点生成文本向量 → 建立 Neo4j 向量索引 → 用问题召回种子实体 → 扩展一到两跳关系 → 拼接三元组 → 生成回答。

它与 Text2Cypher 的入口不同：Text2Cypher 直接生成结构化查询，混合图 RAG 则先用语义相似度找起点。二者都需要图谱质量、明确 Schema 和可追踪的事实来源。

扩展跳数增加，能获得更多关联，也容易爆炸性引入无关节点。实际应限制关系类型、方向、节点数量与上下文预算，并按证据去重。

医疗数据在这里用于演示 Disease、Drug、Symptom 等实体与关系，不代表经过临床审核的知识库，也不应把课堂模型输出当成真实诊疗结论。

## 课堂代码怎么读

先读初始化图谱的数据与 APOC 导入，再看 `build_vector_index`、`semantic_recall`、`graph_expand`、`query`。核对用于生成向量的文本属性，以及种子实体如何映射到关系扩展。

> [!warning] 易错点与资料边界
> 初始化示例与现有图谱是否兼容必须先检查。原代码依赖 Neo4j、插件、本地 Embedding 和模型服务；“MedKG.zip”只有文件名记录，不能说已复现其完整项目。

## 复盘练习

为什么仅增加扩展跳数不一定改善回答？

> [!question]- 参考思路
> 多跳会增加噪声、歧义和重复关系，还会挤占关键证据。应让扩展受问题与 Schema 约束，并评估最终答案是否更可靠。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中006 %%

> [!quote]- 大模型全栈（中）.md · 医疗数据
> 来源：原笔记第 151–250 行。
>
> **医疗数据**
>
> ```python
> from neo4j import GraphDatabase
>
> # 医疗三元组数据：(头实体, 头类型, 关系, 尾实体, 尾类型, 关系属性)
> MEDICAL_TRIPLES = [
>     ("高血压", "Disease", "CAUSES", "头痛", "Symptom", {}),
>     ("高血压", "Disease", "CAUSES", "头晕", "Symptom", {}),
>     ("高血压", "Disease", "CAUSES", "心悸", "Symptom", {}),
>     ("高血压", "Disease", "COMPLICATES", "冠心病", "Disease", {}),
>     ("高血压", "Disease", "COMPLICATES", "脑卒中", "Disease", {}),
>     ("氨氯地平", "Drug", "TREATS", "高血压", "Disease", {"first_line": True}),
>     ("氨氯地平", "Drug", "SIDE_EFFECT", "水肿", "Symptom", {}),
>     ("氨氯地平", "Drug", "SIDE_EFFECT", "头痛", "Symptom", {}),
>     ("依那普利", "Drug", "TREATS", "高血压", "Disease", {"first_line": True}),
>     ("依那普利", "Drug", "TREATS", "2型糖尿病", "Disease", {"first_line": False}),
>     ("依那普利", "Drug", "CONTRAINDICATED_IN", "双侧肾动脉狭窄", "Disease", {}),
>     ("依那普利", "Drug", "SIDE_EFFECT", "干咳", "Symptom", {}),
>     ("2型糖尿病", "Disease", "CAUSES", "多饮", "Symptom", {}),
>     ("2型糖尿病", "Disease", "CAUSES", "多尿", "Symptom", {}),
>     ("2型糖尿病", "Disease", "COMPLICATES", "高血压", "Disease", {}),
>     ("二甲双胍", "Drug", "TREATS", "2型糖尿病", "Disease", {"first_line": True}),
>     ("二甲双胍", "Drug", "SIDE_EFFECT", "胃肠道反应", "Symptom", {}),
>     ("冠心病", "Disease", "CAUSES", "胸痛", "Symptom", {}),
>     ("冠心病", "Disease", "CAUSES", "胸闷", "Symptom", {}),
>     ("阿司匹林", "Drug", "TREATS", "冠心病", "Disease", {"first_line": True}),
>     ("阿司匹林", "Drug", "CONTRAINDICATED_IN", "胃溃疡", "Disease", {}),
>     ("阿司匹林", "Drug", "CONTRAINDICATED_IN", "出血性疾病", "Disease", {}),
>     ("阿司匹林", "Drug", "SIDE_EFFECT", "胃肠道出血", "Symptom", {}),
>     ("胃溃疡", "Disease", "CAUSES", "胃痛", "Symptom", {}),
> ]
>
> # 关系类型白名单
> ALLOWED_REL_TYPES = {"CAUSES", "TREATS", "SIDE_EFFECT", "CONTRAINDICATED_IN", "COMPLICATES"}
>
> def init_graph_apoc():
>     driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))
>     with driver.session() as s:
>         # 1.清空全库
>         s.run("MATCH (n) DETACH DELETE n")
>
>         # 2.创建唯一约束
>         for label in ["Disease", "Drug", "Symptom"]:
>             s.run(
>                 f"CREATE CONSTRAINT {label.lower()}_name IF NOT EXISTS "
>                 f"FOR (n:{label}) REQUIRE n.name IS UNIQUE"
>             )
>
>         # 组装实体列表，apoc.create.nodes 批量创建节点
>         entity_list = []
>         for head, head_type, rel, tail, tail_type, props in MEDICAL_TRIPLES:
>             entity_list.append({"name": head, "_label": head_type})
>             entity_list.append({"name": tail, "_label": tail_type})
>
>         # apoc.create.nodes(标签列表, 属性列表)，自动MERGE避免重复
>         s.run("""
>                     UNWIND $entity_list AS item
>                     WITH DISTINCT item.name AS name, item._label AS label
>                     CALL apoc.create.node([label], {name: name}) YIELD node
>                     RETURN node
>                 """, entity_list=entity_list)
>
>         # 组装关系数据，apoc.create.relationship批量创建关系
>         rel_input = []
>         for head, head_type, rel, tail, tail_type, props in MEDICAL_TRIPLES:
>             assert rel in ALLOWED_REL_TYPES, f"非法关系类型: {rel}"
>             rel_input.append({
>                 "head_name": head,
>                 "tail_name": tail,
>                 "rel_type": rel,
>                 "props": props
>             })
>
>         s.run("""
>             UNWIND $rel_input AS row
>             MATCH (h {name: row.head_name})
>             MATCH (t {name: row.tail_name})
>             CALL apoc.create.relationship(h, row.rel_type, row.props, t) YIELD rel
>             RETURN rel
>         """, rel_input=rel_input)
>
>         # 统计输出
>         stats = s.run("""
>             MATCH (n)
>             RETURN count(n) AS nodes,
>                    sum(CASE WHEN 'Disease' IN labels(n) THEN 1 ELSE 0 END) AS diseases,
>                    sum(CASE WHEN 'Drug' IN labels(n) THEN 1 ELSE 0 END) AS drugs,
>                    sum(CASE WHEN 'Symptom' IN labels(n) THEN 1 ELSE 0 END) AS symptoms
>         """).single()
>         rel_count = s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
>         print(f"【APOC版本】图谱初始化完成: {stats['nodes']} 个节点 "
>               f"(疾病{stats['diseases']}/药物{stats['drugs']}/症状{stats['symptoms']}), "
>               f"{rel_count} 条关系")
>
>     driver.close()
>
> init_graph_apoc()
> ```
>

%% source-id: 中005 %%

> [!quote]- 大模型全栈（中）.md · 混合式图RAG
> 来源：原笔记第 37–150 行。
>
> **混合式图RAG**
>
> ```python
> """
> 向量相似度+图 混合式图RAG
> 向量索引创建->语义召回->图关系扩展->上下文拼接->答案生成
> """
> import os
> from neo4j import GraphDatabase
> from langchain_openai import ChatOpenAI
> from langchain_neo4j import Neo4jVector
> from langchain_huggingface import HuggingFaceEmbeddings
> from langchain_core.prompts import ChatPromptTemplate
> from langchain_core.output_parsers import StrOutputParser
> from dotenv import load_dotenv
>
> load_dotenv()
>
> class HybridGraphRAG:
>     def __init__(self):
>         self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))
>         self.llm = ChatOpenAI(
>             api_key=os.getenv("DEEPSEEK_API_KEY"),
>             base_url=os.getenv("DEEPSEEK_BASE_URL"),
>             model="deepseek-chat",
>             temperature=0
>         )
>         self.embeddings = HuggingFaceEmbeddings(
>             model_name="./bge-base-zh-v1.5",
>             model_kwargs={"device": "cpu"},
>             encode_kwargs={"normalize_embeddings": True}
>         )
>         self.vector_index = None
>
>     def build_vector_index(self):
>         # 先给业务节点打标签 自动生成词嵌入
>         with self.driver.session() as session:
>             for label in ["Disease", "Drug", "Symptom"]:
>                 session.run(f"MATCH (n:{label}) SET n:__Entity__")
>
>         # 自动读取节点,生成向量并建立内部Neo4j索引
>         self.vector_index = Neo4jVector.from_existing_graph(
>             embedding=self.embeddings,
>             url="bolt://localhost:7687",
>             username="neo4j",
>             password="12345678",
>             index_name="entity_embeddings",  # 内部的名字
>             node_label="__Entity__",
>             text_node_properties=["name"],
>             embedding_node_property="embedding",  # 计算出向量存在节点属性中
>             search_type="vector"
>         )
>         print("向量索引构建完成~")
>
>     def semantic_recall(self, question, top_k):
>         with self.driver.session() as session:
>             query_embedding = self.embeddings.embed_query(question)
>             records = session.run("""
>                 CALL db.index.vector.queryNodes('entity_embeddings', $top_k, $embedding)
>                 YIELD node, score
>                 RETURN node.name AS name, labels(node) AS labels, score
>                 ORDER BY score DESC
>             """, top_k=top_k, embedding=query_embedding)
>
>             return [dict(r) for r in records]  # [{"name:xx","labels:xx,"score":...},{},...]
>
>     def graph_expand(self, entity_names):
>         if not entity_names:
>             return {"nodes": [], "relationships": [], "triples_text": []}
>         # 召回实体为起点,遍历多跳邻居,收集子图中的节点和关系作为结构化上下文
>         # {"node":[....],"rel":[...],...}
>         with self.driver.session() as session:
>             # 查询1
>             nodes = session.run("""
>                 UNWIND $seeds AS seeds
>                 MATCH (seed_node {name:seed})
>                 MATCH path=(seed_node)-[*1..2]-(neighbor)
>                 UNWIND nodes(path) AS n
>                 RETURN DISTINCT n.name AS name, labels(n) AS labels
>                 LIMIT 20
>             """, seeds=entity_names)
>
>             # 查询2
>             # 取出路径中的全部关系,得到头尾实体+关系类型+关系属性
>             relationships = session.run("""
>                  UNWIND $seeds AS seeds
>                  MATCH (seed_node {name:seed})
>                  MATCH path = (seed_node)-[*1..2]-(neighbor)
>                  UNWIND relationships(path) AS r
>                  RETURN DISTINCT startNode(r).name AS head,
>                         type(r) AS rel,
>                         endNode(r).name AS tail,
>                         properties(r) AS props
>                  LIMIT 20
>             """, seeds=entity_names)
>
>         triples_lines = []
>         for r in relationships:
>             props_str = ""
>             if r["props"]:
>                 props_str = f"{{{','.join(f'{k}:{v}' for k, v in r['props'].items())}}}"
>
>             triples_lines.append(f" {r['head']} --{r['rel']}{props_str}--> {r['tail']}")
>
>         triples_text = "\n".join(triples_lines)
>         return {"nodes": nodes, "relationships": relationships, "triples_text": triples_text}
>
>     def query(self):
>         ...
>
>     def close(self):
>         ...
> ```
>

%% source-id: 中002 %%

> [!quote]- 大模型全栈（中）.md · 医疗项目
> 来源：原笔记第 25–28 行。
>
> **医疗项目**
>
> MedKG.zip
>

## 资料与关联

- [[大模型全栈/资料/PDF/知识图谱.pdf#page=1|知识图谱.pdf · 第 1–9 页]]
- [[大模型全栈/资料/PDF/知识图谱.pdf#page=25|知识图谱.pdf · 第 25–27 页]]
- 关联知识：[[大模型全栈/36-知识图谱：实体、关系与图结构|36-知识图谱：实体、关系与图结构]]、[[大模型全栈/37-NER、标签对齐与三元组抽取|37-NER、标签对齐与三元组抽取]]、[[大模型全栈/38-实体融合：名称、属性与相似度|38-实体融合：名称、属性与相似度]]、[[大模型全栈/39-Neo4j、Cypher 与批量入库|39-Neo4j、Cypher 与批量入库]]、[[大模型全栈/40-Text2Cypher 与图谱问答|40-Text2Cypher 与图谱问答]]。
