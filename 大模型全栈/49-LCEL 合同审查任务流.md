---
type: 学习笔记
course: 大模型全栈
order: 49
stage: Agent 与协作
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/48-CrewAI 金融分析项目与系统评估|48-CrewAI 金融分析项目与系统评估]] · 下一篇：[[大模型全栈/50-LangGraph：状态、条件分支与循环|50-LangGraph：状态、条件分支与循环]]

> [!abstract] 学习目标
> 把读取、条款识别、评分与报告编排成可追踪链。

## 核心理解

课堂合同工作流先读取文件，用规则拆出条款，按关键词给分，再根据高风险条款数量选择快速或深度审查，最后生成 Markdown 报告。

这是一条预定义的数据流：模型主要参与深度分析与报告表达，分支依据来自程序中显式的评分规则。它说明复杂应用不一定都需要自主 Agent。

读中间字典时，关注 text、clauses、level、score、deep_analysis 等字段何时产生。某一步漏写字段，通常会在后续模板格式化时才暴露，因此保留中间输出很重要。

关键词评分只是演示启发式；真正风险识别还需要结合合同上下文、适用规则和事实。教学流程产出的风险标签不应当作实际法律意见。

## 课堂代码怎么读

按 `read_contract → ext_clauses → score_all → review_branch → format_report → report_chain` 阅读。检查快速分支与深度分支是否最终产生报告所需的相同字段。

> [!warning] 易错点与资料边界
> 原代码依赖 ./data/test.txt，且条款切分与关键词评分覆盖有限。PDF 是 LCEL 编排参考；复杂合同项目的多 Agent 方案在另一份资料中，不要混作同一实现。

## 复盘练习

为什么分支两端最好返回相同结构？

> [!question]- 参考思路
> 这样后续步骤才能用统一接口接收结果，避免只有某条路径运行成功，另一条在报告阶段缺字段。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 下049 %%

> [!quote]- 大模型全栈（下）.md · 合同审查任务流
> 来源：原笔记第 4039–4202 行。
>
> **合同审查任务流**
>
> test.txt
>
> ```python
> """
> 合同审查任务流
> 读取->提取->评分->分支审查->报告
> """
> import os
> import re
> import logging
> from dotenv import load_dotenv
> from langchain_openai import ChatOpenAI
> from langchain_core.prompts import ChatPromptTemplate
> from langchain_core.output_parsers import StrOutputParser
> from langchain_core.runnables import RunnableLambda, RunnableBranch
>
> load_dotenv()
>
> # 大模型
> llm = ChatOpenAI(
>     model="deepseek-chat",
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     temperature=0,
> )
>
> # 读文本
> def read_contract(input_data):
>     file_path = input_data.get("file_path")
>     with open(file_path, "r", encoding="utf-8") as f:
>         text = f.read()
>
>     print("读取文本~")
>     return {"text": text, "file_path": file_path}
>
> # 提取条款
> def ext_clauses(data):
>     text = data["text"]
>     parts = re.split(r"\n(?=第[一二三四五六七八九十百\d]+条)", text)
>
>     clauses = []
>     for part in parts:
>         if part and len(part) > 5:
>             first_line = part.split("\n")[0]
>             clauses.append({"title": first_line, "content": part})
>
>     data["clauses"] = clauses
>     print("条款提取完毕~")
>     return data
>
> # 风险评分
> RISK_KW = {
>     "高": ["无限责任", "200%", "随时终止", "不予退还", "全部赔偿"],
>     "中": ["赔偿损失", "永久保密", "违约金", "仲裁"]
> }
>
> def score_clause(clause):
>     content = clause["content"]
>     score = 0
>     risks = []
>     for word in RISK_KW["高"]:
>         if word in content:
>             score += 30
>             risks.append(f"[高] 关键词 {word}")
>
>     for word in RISK_KW["中"]:
>         if word in content:
>             score += 15
>             risks.append(f"[中] 关键词 {word}")
>
>     score = min(score, 100)
>     clause["score"] = score
>     clause["level"] = "高" if score >= 60 else ("中" if score >= 30 else "低")
>     clause["risks"] = risks if risks else ["未发现明显风险"]
>     return clause
>
> def score_all(data):
>     data["clauses"] = [score_clause(c) for c in data["clauses"]]
>     high_count = sum(1 for c in data["clauses"] if c["level"] == "高")
>     data["high_count"] = high_count
>     print(f"评分完成:{high_count} 条高风险")
>     return data
>
> # 分支审查
> # 深度审查
> deep_prompt = ChatPromptTemplate.from_template(
>     "你是一位资深合同法律专家。请对以下高风险条款进行深度分析，"
>     "指出具体风险点、可能造成的损失、修改建议（用中文，分条列出）：\n\n"
>     "条款标题：{title}\n条款内容：{content}\n"
>     "初步风险标记：{risks}"
> )
> deep_chain = deep_prompt | llm | StrOutputParser()
>
> def deep_review(data):
>     for clause in data["clauses"]:
>         if clause["level"] == "高":
>             clause["deep_analysis"] = deep_chain.invoke({
>                 "title": clause["title"],
>                 "content": clause["content"],
>                 "risks": ";".join(clause["risks"]),
>             })
>     data["review_mode"] = "深度审查"
>     return data
>
> # 快速审查
> def quick_review(data):
>     for clause in data["clauses"]:
>         clause["deep_analysis"] = "低风险条款,无需深度分析"
>     data["review_mode"] = "快速审查"
>     return data
>
> review_branch = RunnableBranch(
>     (lambda data: data["high_count"] > 0,
>      RunnableLambda(deep_review)),
>     RunnableLambda(quick_review),
> )
>
> # 报告
> report_prompt = ChatPromptTemplate.from_template(
>     "请根据以下合同审查结果生成一份结构化审查报告（Markdown 格式）：\n\n"
>     "文件：{file_path}\n审查模式：{review_mode}\n"
>     "条款总数：{total}，高风险：{high}，中风险：{medium}，低风险：{low}\n\n"
>     "各条款详情：\n{clauses_detail}\n\n"
>     "报告要求：\n"
>     "1. 总体评价（2-3句）\n"
>     "2. 高风险条款逐条列出（含分析和建议）\n"
>     "3. 中风险条款简要列出\n"
>     "4. 审查结论与建议"
> )
>
> def format_report(data):
>     detail_lines = []
>     for i, clause in enumerate(data["clauses"], 1):
>         detail_lines.append(f"{i}. [{clause['level']}风险|{clause['score']}分] {clause['title']}")
>         detail_lines.append(f"   风险点:{';'.join(clause['risks'])}")
>         if clause.get("deep_analysis"):
>             detail_lines.append(f"   深度分析:{clause['deep_analysis'][:100]}")
>
>     data["clauses_detail"] = "\n".join(detail_lines)
>     data["total"] = len(data["clauses"])
>     data["high"] = data["high_count"]
>     data["medium"] = sum(1 for c in data["clauses"] if c["level"] == "中")
>     data["low"] = data["total"] - data["high"] - data["medium"]
>
>     return data
>
> report_chain = report_prompt | llm | StrOutputParser()
>
> # 测试运行
> contract_chain = (
>         RunnableLambda(read_contract)
>         | RunnableLambda(ext_clauses)
>         | RunnableLambda(score_all)
>         | review_branch
>         | RunnableLambda(format_report)
>         | report_chain
> )
>
> print("LCEL 合同审查任务开始~")
> report = contract_chain.invoke({"file_path": "./data/test.txt"})
> print(report)
> ```

## 资料与关联

- [[大模型全栈/资料/PDF/9.LCEL高阶.pdf#page=6|9.LCEL高阶.pdf · 第 6–18 页]]
- 关联知识：[[大模型全栈/22-LCEL：串行、并行与数据流|22-LCEL：串行、并行与数据流]]、[[大模型全栈/50-LangGraph：状态、条件分支与循环|50-LangGraph：状态、条件分支与循环]]、[[大模型全栈/52-GraphRAG 合同审查综合案例|52-GraphRAG 合同审查综合案例]]。
