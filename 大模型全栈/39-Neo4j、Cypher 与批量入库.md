---
type: 学习笔记
course: 大模型全栈
order: 39
stage: 知识图谱
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/38-实体融合：名称、属性与相似度|38-实体融合：名称、属性与相似度]] · 下一篇：[[大模型全栈/40-Text2Cypher 与图谱问答|40-Text2Cypher 与图谱问答]]

> [!abstract] 学习目标
> 用图数据库保存、查询和约束关系数据。

## 核心理解

Neo4j 的属性图用节点、关系、标签与属性表达业务。Cypher 通过模式匹配查询，例如先指定实体，再沿某类关系取邻居，或按属性过滤。

CREATE 用于创建新记录；MERGE 根据给定模式匹配或创建。MERGE 并不自动解决所有重复问题，仍需选择稳定键、配置必要约束，并明确更新策略。

批量入库把多条记录送入一个事务或使用 UNWIND，减少逐条网络交互。课堂按批处理人物与关系，再用内置接口查看 Schema。节点入库与关系入库通常分阶段执行，避免端点不存在。

查询时要同时检查方向、关系类型、过滤条件与返回条数。只返回一个名字，往往不足以追溯该事实来自哪里。

## 课堂代码怎么读

先看课堂 Cypher 命令与练习，再读 Python driver 的事务函数、分批 yield 与 relationship 构造，最后看 Neo4jGraph 的 Schema 和 query 接口。

> [!warning] 易错点与资料边界
> 原例有写入与删除命令，属于学习材料，本轮没有连接或修改你的数据库。示例地址、账号和口令只是课堂配置，应按自己的环境管理，不能据此认定本地已有数据库。

## 复盘练习

为什么关系批量写入前先建立节点？

> [!question]- 参考思路
> 关系依赖两端节点身份。先稳定节点 ID 和约束，再 MATCH 两端写关系，可以减少重复节点与悬空匹配失败。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中015 %%

> [!quote]- 大模型全栈（中）.md · 部分命令
> 来源：原笔记第 617–639 行。
>
> **部分命令**
>
> ```cypher
> MATCH (p:Person)
> RETURN p.name AS 姓名, p.age AS 年龄
> ORDER BY p.age DESC
> SKIP 0 LIMIT 2;
>
> MATCH (p:Person)
> WHERE p.name =~ '张.*'
> RETURN p.name AS 姓名;
>
> MATCH (p:Person)
> WHERE p.age >= 25 AND p.age <= 35     
>   AND p.city IN ['北京', '上海']        
>   AND p.name STARTS WITH '张'           
>   AND p.name ENDS WITH '三'              
>   AND p.name CONTAINS '三'               
>   AND p.age IS NOT NULL                  
>   AND NOT (p.city = '广州')              
> RETURN p.name, p.age;
> ```
>

%% source-id: 中014 %%

> [!quote]- 大模型全栈（中）.md · 练习使用
> 来源：原笔记第 563–616 行。
>
> **练习使用**
>
> ```cypher
> // 清空原有数据
> MATCH (n) DETACH DELETE n;
>
> // 创建人物节点（全中文姓名）
> CREATE
> (:Person{name:"张三",age:29,city:"北京"}),
> (:Person{name:"李四",age:26,city:"上海"}),
> (:Person{name:"王五",age:34,city:"北京"}),
> (:Person{name:"赵六",age:31,city:"广州"}),
> (:Person{name:"孙七",age:24,city:"深圳"}),
> (:Person{name:"周八",age:36,city:"上海"}),
> (:Person{name:"吴九",age:28,city:"北京"}),
> (:Person{name:"郑十",age:33,city:"成都"}),
> (:Person{name:"陈十一",age:27,city:"杭州"}),
> (:Person{name:"林十二",age:38,city:"广州"});
>
> // 创建公司节点
> CREATE
> (:Company{name:"星辰科技",industry:"互联网"}),
> (:Company{name:"云海集团",industry:"金融"}),
> (:Company{name:"绿洲软件",industry:"互联网"});
>
> // 构建社交关系链（KNOWS），形成多跳路径
> // 张三 → 李四 → 周八 → 郑十 （4跳链路）
> MATCH (a:Person{name:"张三"}),(b:Person{name:"李四"}) MERGE (a)-[:KNOWS{since:2021}]->(b);
> MATCH (b:Person{name:"李四"}),(c:Person{name:"周八"}) MERGE (b)-[:KNOWS{since:2022}]->(c);
> MATCH (c:Person{name:"周八"}),(d:Person{name:"郑十"}) MERGE (c)-[:KNOWS{since:2023}]->(d); 
>
> // 张三直接认识王五、吴九
> MATCH (a:Person{name:"张三"}),(b:Person{name:"王五"}) MERGE (a)-[:KNOWS{since:2019}]->(b);
> MATCH (a:Person{name:"张三"}),(b:Person{name:"吴九"}) MERGE (a)-[:KNOWS{since:2020}]->(b);
>
> // 王五认识赵六、孙七
> MATCH (a:Person{name:"王五"}),(b:Person{name:"赵六"}) MERGE (a)-[:KNOWS{since:2021}]->(b);
> MATCH (a:Person{name:"王五"}),(b:Person{name:"孙七"}) MERGE (a)-[:KNOWS{since:2022}]->(b);
>
> // 赵六认识陈十一、林十二
> MATCH (a:Person{name:"赵六"}),(b:Person{name:"陈十一"}) MERGE (a)-[:KNOWS{since:2020}]->(b);
> MATCH (a:Person{name:"赵六"}),(b:Person{name:"林十二"}) MERGE (a)-[:KNOWS{since:2021}]->(b);
>
> // 构建就职关系（WORKS_AT）
> MATCH (p:Person{name:"张三"}),(c:Company{name:"星辰科技"}) MERGE (p)-[:WORKS_AT]->(c);
> MATCH (p:Person{name:"李四"}),(c:Company{name:"星辰科技"}) MERGE (p)-[:WORKS_AT]->(c);
> MATCH (p:Person{name:"王五"}),(c:Company{name:"云海集团"}) MERGE (p)-[:WORKS_AT]->(c);
> MATCH (p:Person{name:"吴九"}),(c:Company{name:"云海集团"}) MERGE (p)-[:WORKS_AT]->(c);
> MATCH (p:Person{name:"赵六"}),(c:Company{name:"绿洲软件"}) MERGE (p)-[:WORKS_AT]->(c);
> MATCH (p:Person{name:"孙七"}),(c:Company{name:"绿洲软件"}) MERGE (p)-[:WORKS_AT]->(c);
>
> // 周八、郑十、陈十一、林十二 不设置就职关系，用于测试空值匹配
> ```
>

%% source-id: 中013 %%

> [!quote]- 大模型全栈（中）.md · 练习命令
> 来源：原笔记第 543–562 行。
>
> **练习命令**
>
> ```cypher
> MATCH (a:Person {name:'张三'})-[:KNOWS*1..3]->(远房朋友)
> RETURN DISTINCT 远房朋友.name;
>
> MATCH (a:Person {name:'张三'})-[:KNOWS*2]->(朋友的朋友)
> RETURN DISTINCT 朋友的朋友.name;
>
> MATCH    
> (a:Person {name:'张三'}),    
> (b:Person {name:'陈十一'}),    
> 路径= shortestPath((a)-[:KNOWS*]-(b))
> RETURN 路径, length(路径) AS 跳数;
>
> MATCH 
> (a:Person {name:'张三'})-[:KNOWS|WORKS_AT]->(目标)
> RETURN a.name AS 主体, 目标.name AS 关联对象;
> ```
>

%% source-id: 中011 %%

> [!quote]- 大模型全栈（中）.md · 批量插入
> 来源：原笔记第 470–538 行。
>
> **批量插入**
>
> ```python
> """
> 批量插入
> """
> from neo4j import GraphDatabase
>
> driver = GraphDatabase.driver(
>     "bolt://localhost:7687",
>     auth=("neo4j", "12345678"),
> )
>
> driver.verify_connectivity()
>
> # 批量创建节点
> def batch_persons(tx, persons):
>     tx.run("""
>         UNWIND $persons AS person
>         MERGE (p:Person {name: person.name})
>         ON CREATE SET p.age = person.age,p.city=person.city
>         ON MATCH SET p.age=person.age,p.city=person.city
>     """, persons=persons)
>
> persons_data = [
>     {"name": f"用户{i:03d}", "age": 18 + i % 30, "city": ["北京", "上海", "广州", "深圳"][i % 4]}
>     for i in range(100)
> ]
>
> with driver.session() as session:
>     session.execute_write(batch_persons, persons_data)
>     print("添加完成")
>
> '''
> # 生成器写法,批量大数据
> def batch_chunks(data):
>     for i in range(0, len(data), 2000):
>         yield data[i:i + 2000]
>
> persons_data = [
>     {"name": f"用户{i:05d}", "age": 18 + i % 40, "city": ["北京", "上海", "广州", "深圳"][i % 4]}
>     for i in range(10000)
> ]
>
> with driver.session() as session:
>     for idx, chunk in enumerate(batch_chunks(persons_data)):
>         session.execute_write(batch_persons, chunk)
>         print("添加完成")
> '''
>
> # 创建关系
> def batch_relations(tx, relations):
>     tx.run("""
>         UNWIND $relations AS rel
>         MATCH (a:Person {name: rel.source_name})
>         MATCH (b:Person {name: rel.target_name})
>         MERGE (a)-[r:KNOWS {since:rel.since}]->(b)
>     """, relations=relations)
>
> relations_data = [
>     {"source_name": "用户001", "target_name": "用户002", "since": "2002"},
>     {"source_name": "用户001", "target_name": "用户003", "since": "2125"},
>     {"source_name": "用户002", "target_name": "用户004", "since": "2022"}
> ]
> with driver.session() as session:
>     session.execute_write(batch_relations, relations_data)
>     print("succ")
> ```
>

%% source-id: 中009 %%

> [!quote]- 大模型全栈（中）.md · 内置方法
> 来源：原笔记第 434–465 行。
>
> **内置方法**
>
> ```python
> """
> 使用内置类实现
> """
> from langchain_neo4j import Neo4jGraph
>
> graph = Neo4jGraph(
>     url="bolt://localhost:7687",
>     username="neo4j",
>     password="12345678",
>     database="neo4j"
> )
>
> # 获取图谱
> schema = graph.schema
> print(schema)
>
> # 结构化
> structured = graph.get_structured_schema
> print("节点标签:",list(structured["node_props"].keys()))
>
> rel_type = [r["type"] for r in structured["relationships"]]
> print("关系类型:",rel_type)
>
> # 查询
> res = graph.query("MATCH (p:Person) RETURN p.name as 姓名,p.age as 年龄 LIMIT 10")
> for record in res:
>     print(record)
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/知识图谱.pdf#page=3|知识图谱.pdf · 第 3–9 页]]
