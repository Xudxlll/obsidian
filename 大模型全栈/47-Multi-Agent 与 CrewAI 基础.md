---
type: 学习笔记
course: 大模型全栈
order: 47
stage: Agent 与协作
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/46-对话记忆：缓冲、摘要与向量检索|46-对话记忆：缓冲、摘要与向量检索]] · 下一篇：[[大模型全栈/48-CrewAI 金融分析项目与系统评估|48-CrewAI 金融分析项目与系统评估]]

> [!abstract] 学习目标
> 用角色、任务与依赖组织协作，控制额外沟通成本。

## 核心理解

多 Agent 将任务分给不同角色，但“多个角色”不自动产生更好答案。收益来自明确分工、适当工具权限、独立检查和结果整合；成本则包括更多调用、上下文传递和协调失败。

CrewAI 的 Agent 定义角色、目标、工具等；Task 定义具体任务与预期输出；Crew 组织人员与任务；Process 说明执行组织方式。顺序流程适合稳定依赖，层级流程由管理角色协调。

课堂三个小例子从单个研究任务，到作者与审阅者，再到开发与测试，逐步增加协作。前序 Task 输出通过 context 等机制传给后续任务，与所有 Agent 自动共享全部记忆不同。

任务说明应有可验收产物，例如“返回可执行代码与测试结果”，而不是仅写“认真思考”。审阅者还需要独立标准，避免只把前一角色的话改写一遍。

## 课堂代码怎么读

按三个例子比较 Agent、Task、Crew、Process 与 kickoff 的职责。观察两个任务间的 context，以及模型对象是否明确传入所需角色。

> [!warning] 易错点与资料边界
> 框架版本决定具体参数是否可用。任务之间的文字传递可能放大错误；多 Agent 的质量应与相同预算下的单 Agent 或固定流程比较。

## 复盘练习

为什么审阅 Agent 和作者使用同一模型仍可能有价值，也可能无效？

> [!question]- 参考思路
> 角色和任务不同可引导独立检查，但两者也可能共享盲点。必须给审阅者证据与明确检查项，并用真实错误样本验证收益。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 下042 %%

> [!quote]- 大模型全栈（下）.md · CrewAI-1
> 来源：原笔记第 3405–3444 行。
>
> **CrewAI-1**
>
> ```python
> """
> agent + task + crew
> CREWAI_TRACING_ENABLED=true
> """
> import os
> from dotenv import load_dotenv
> from crewai import Agent, Task, Crew, Process
>
> load_dotenv()
>
> os.environ['OPENAI_API_KEY'] = os.getenv("DEEPSEEK_API_KEY")
> os.environ['OPENAI_API_BASE'] = os.getenv("DEEPSEEK_BASE_URL")
> os.environ['OPENAI_MODEL_NAME'] = "deepseek-chat"
>
> researcher = Agent(
>     role="行业分析师",
>     goal="基于公开的信息,产生行业分析",
>     backstory="你拥有15年工作经验,擅长从数据中挖掘行业趋势",
>     verbose=True
> )
>
> research_task = Task(
>     description="调研2024年中国大模型行业市场规模和主要商场份额",
>     agent=researcher,
>     expected_output="一份包含市场规模数值,Top3厂商份额占比的简要分析报告,300字以内",
> )
>
> crew = Crew(
>     agents=[researcher],
>     tasks=[research_task],
>     process=Process.sequential,
>     verbose=True
> )
> res = crew.kickoff()
> print(res)
> ```
>

%% source-id: 下041 %%

> [!quote]- 大模型全栈（下）.md · CrewAI-2
> 来源：原笔记第 3359–3404 行。
>
> **CrewAI-2**
>
> ```python
> """
> process
> """
> import os
> from dotenv import load_dotenv
> from crewai import Agent, Task, Crew, Process
>
> load_dotenv()
>
> os.environ['OPENAI_API_KEY'] = os.getenv("DEEPSEEK_API_KEY")
> os.environ['OPENAI_API_BASE'] = os.getenv("DEEPSEEK_BASE_URL")
> os.environ['OPENAI_MODEL_NAME'] = "deepseek-chat"
>
> writer = Agent(
>     role="文案撰写人", goal="擅长写小红书文案",
>     backstory="你拥有15年文案经验", verbose=True
> )
> reviewer = Agent(
>     role="文案审核人", goal="审核并优化文案",
>     backstory="你拥有15年文案经验,擅长科技产品", verbose=True
> )
>
> writer_task = Task(
>     description="撰写一份200字的智能手表产品宣传文案",
>     agent=writer,
>     expected_output="200字以内的文案",
> )
> review_task = Task(
>     description="审核并优化上一步产出的文案,修改语病,剔除极限词,提高营销感",
>     agent=reviewer,
>     expected_output="最终优化后的文案",
> )
>
> crew = Crew(
>     agents=[writer, reviewer],
>     tasks=[writer_task, review_task],
>     process=Process.sequential,
>     verbose=True
> )
> res = crew.kickoff()
> print(res)
> ```
>

%% source-id: 下040 %%

> [!quote]- 大模型全栈（下）.md · CrewAI-3
> 来源：原笔记第 3307–3358 行。
>
> **CrewAI-3**
>
> ```python
> """
> 层级模式
> """
> import os
> from dotenv import load_dotenv
> from crewai import Agent, Task, Crew, Process, LLM
>
> load_dotenv()
>
> os.environ['OPENAI_API_KEY'] = os.getenv("DEEPSEEK_API_KEY")
> os.environ['OPENAI_API_BASE'] = os.getenv("DEEPSEEK_BASE_URL")
> os.environ['OPENAI_MODEL_NAME'] = "deepseek-chat"
>
> dev_agent = Agent(
>     role="开发工程师", goal="编写功能代码",
>     backstory="擅长后端开发,代码规范", verbose=True
> )
> test_agent = Agent(
>     role="测试工程师", goal="执行功能测试并输出报告",
>     backstory="细致的测试专家", verbose=True
> )
>
> dev_task = Task(
>     description="编写Python快速排序函数",
>     agent=dev_agent,
>     expected_output="带有注释的排序代码",
> )
> test_task = Task(
>     description="对排序代码编写测试用例,并验证确定性",
>     agent=test_agent,
>     expected_output="测试用例+测试结果",
> )
>
> llm = LLM(
>     model="deepseek-chat",
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
> )
> crew = Crew(
>     agents=[dev_agent, test_agent],
>     tasks=[dev_task, test_task],
>     process=Process.hierarchical,  # 自动创建manager rAgent
>     manager_llm=llm,
>     verbose=True
> )
> res = crew.kickoff()
> print(res)
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/10.MultiAgent.pdf#page=4|10.MultiAgent.pdf · 第 4–21 页]]
- 关联知识：[[大模型全栈/46-对话记忆：缓冲、摘要与向量检索|46-对话记忆：缓冲、摘要与向量检索]]、[[大模型全栈/48-CrewAI 金融分析项目与系统评估|48-CrewAI 金融分析项目与系统评估]]、[[大模型全栈/53-AutoML 多 Agent：模块与数据流程|53-AutoML 多 Agent：模块与数据流程]]。
