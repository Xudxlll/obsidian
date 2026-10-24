---
type: 学习笔记
course: 大模型全栈
order: 15
stage: 模型交互
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/14-API 调用、Token 与生成参数|14-API 调用、Token 与生成参数]] · 下一篇：[[大模型全栈/16-Few-shot 与动态示例选择|16-Few-shot 与动态示例选择]]

> [!abstract] 学习目标
> 把可复用的任务说明与每次变化的数据分开。

## 核心理解

提示词模板把稳定结构与变量分离：任务要求、角色、输出格式通常保持稳定，问题或文章内容通过变量注入。`PromptTemplate` 常输出字符串；`ChatPromptTemplate` 则构造带角色的消息序列。

角色用于表达消息职责。system 提供总体行为说明，user 表达本次需求，assistant 表示先前回复；工具返回另有专门的消息表示。角色标签不应该被当作普通文本随意混用。

`.partial()` 可以预先绑定部分变量，适合固定角色、日期或风格，再在调用时提供剩余输入。模板里的 JSON 花括号若按字面出现，要注意与模板变量语法区分。

好的模板不只是“你是一位专家”，还应说明任务、可用资料、约束、输出结构和信息不足时怎样处理。后面的 RAG 与 Agent 都继续复用这一思路。

## 课堂代码怎么读

课堂依次使用 `from_template`、显式 `input_variables`、partial、Chat 模板及综合练习。观察 `.format()` 与 `.format_messages()` 的返回类型；不要只看打印出来的文字相似就认为可以互换。

> [!warning] 易错点与资料边界
> 普通变量替换不会自动获得完整条件逻辑。模板格式化成功只说明变量填齐，不保证指令清楚，也不保证输出符合业务约束。

## 复盘练习

为什么用户文章不应该被直接拼进系统规则里？

> [!question]- 参考思路
> 系统规则与待处理数据职责不同。保留边界有利于复用、追踪，也能减少把文章中的指令误当成系统要求的风险。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

上篇保留了网页公共缩进与不间断空格，执行前需在练习副本中核对输入类型、缩进与依赖。

%% source-id: 上003 %%

> [!quote]- 大模型全栈（上）.md · 提示词模板与角色
> 来源：原笔记第 314–337 行。
>
>    6.提示词模板：**PromptTemplate**
>
>    动态模板 PromptTemplate ，通过模板语法，让提示词结构化，支持：
>
>    变量替换（如 {question} ）
>
>    设置默认值
>
>    条件逻辑（可选参数）
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/AUWCUEZHADADW?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IkFVV0NVRVpIQURBRFciLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6MTE2MCwiaGVpZ2h0Ijo0MDV9)
>
>    
>
>    7.角色
>
>    对应API角色
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/VDUSUEZHAAABM?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IlZEVVNVRVpIQUFBQk0iLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6MTE0MywiaGVpZ2h0IjozNTF9)
>
>    对应的字段
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/JNMSWEZHADADW?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IkpOTVNXRVpIQURBRFciLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6MTE2MSwiaGVpZ2h0IjoyNjN9)
>

%% source-id: 中072 %%

> [!quote]- 大模型全栈（中）.md · PromptTemplate
> 来源：原笔记第 4871–4919 行。
>
> **PromptTemplate**
>
> ```python
> """
> 提示词模板
> """
> from langchain_core.prompts import PromptTemplate
>
> # 工厂
> template = "你是一个{role}专家,请用{style}风格,解释{topic}"
> prompt = PromptTemplate.from_template(template)
> print(prompt.input_variables)
>
> res = prompt.format(role="AI", style="幽默", topic="机器学习")
> print(res)
>
> # 构造
> prompt = PromptTemplate(
>     template="你是一个{role}专家,请用{style}风格,解释{topic}",
>     input_variables=["style", "role", "topic"],
>     template_format="f-string",
>     validate_template=True
> )
> res = prompt.format(role="AI", topic="机器学习", style="幽默")
> print(res)
>
> # 部分填充
> from datetime import datetime
>
> template = "当前日期{date},你是一个{role}助手,请回答:{question}"
> prompt = PromptTemplate.from_template(template)
> print(prompt.input_variables)
>
> prompt_partial = prompt.partial(
>     role="AI",
>     date=lambda: datetime.now().strftime("%Y%m%d")
> )
> res = prompt_partial.format(question="什么是装饰器")
> print(res)
> ```
>
> 来的早的安装下面的库和下载包, 模型包只保留1个星期! 及时下载!! 2026年8月15日01:52:08--
>
> ```text
> pip install langchain-huggingface
> ```
>
> bge-base-zh-v1.5.zip
>

%% source-id: 中071 %%

> [!quote]- 大模型全栈（中）.md · Chat
> 来源：原笔记第 4850–4870 行。
>
> **Chat**
>
> ```python
> """
> 聊天提示词模板
> """
> from langchain_core.prompts import ChatPromptTemplate
>
> prompt = ChatPromptTemplate.from_messages(
>     [
>         ("system", "你是一个{role}专家,回答问题需要代码示例"),
>         ("human", "请帮我写一个{task}排序")
>     ]
> )
>
> messages = prompt.format_messages(role="Python", task="冒泡")
>
> for msg in messages:
>     print(f"[{msg.type}]: {msg.content}")
> ```
>

%% source-id: 中067 %%

> [!quote]- 大模型全栈（中）.md · 综合练习
> 来源：原笔记第 4619–4677 行。
>
> **综合练习**
>
> ```python
> """
> 综合练习
> """
> import os
> from dotenv import load_dotenv
> from langchain_openai import ChatOpenAI
> from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
> from langchain_core.messages import HumanMessage, AIMessage
>
> load_dotenv()
>
> llm = ChatOpenAI(
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     model="deepseek-chat",
> )
>
> # 1.PromptTemplate
> prompt = PromptTemplate(
>     template="你是一个{role}专家,请用{style}的风格解释{topic},100个字",
>     input_variables=["role", "style", "topic"]
> )
> formatted = prompt.format(role="人工智能",style="简单通俗",topic="深度学习")
> res = llm.invoke(formatted).content
> print(f"PromptTemplate 回答: {res}\n")
>
> # 2.ChatPromptTemplate
> chat_prompt = ChatPromptTemplate.from_messages([
>     ("system","你是一个{role}专家,回答需要带上代码"),
>     ("human", "请写一个{task}排序"),
> ])
>
> messages = chat_prompt.format_messages(role="Python",task="快速")
> res = llm.invoke(messages).content
> print(f"ChatPromptTemplate 回答: {res}\n")
>
> # 3.MessagesPlaceholder
> msg_prompt = ChatPromptTemplate.from_messages([
>     ("system","你是一个会怼人的曼波"),
>     MessagesPlaceholder(variable_name="history"),
>     ("human", "{question}"),
> ])
>
> history = [
>     HumanMessage(content="我家有等离子电视"),
>     AIMessage(content="你什么档次和我用一样的电视")
> ]
>
> messages = msg_prompt.format_messages(
>     history=history,
>     question="我家有啥?",
> )
> res = llm.invoke(messages).content
> print(f"MessagesPlaceholder 回答: {res}")
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/1.从调用API开始.pdf#page=11|1.从调用API开始.pdf · 第 11–15 页]]
- [[大模型全栈/资料/PDF/2.Model+I+O.pdf#page=10|2.Model+I+O.pdf · 第 10–15 页]]
