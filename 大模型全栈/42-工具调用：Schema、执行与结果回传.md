---
type: 学习笔记
course: 大模型全栈
order: 42
stage: Agent 与协作
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/41-GraphRAG：向量召回与关系扩展|41-GraphRAG：向量召回与关系扩展]] · 下一篇：[[大模型全栈/43-Agent、ReAct 与 Self-Ask|43-Agent、ReAct 与 Self-Ask]]

> [!abstract] 学习目标
> 模型提出调用，应用程序执行，并将真实结果送回模型。

## 核心理解

工具调用不是模型在文本里写“我查了天气”，而是一套交互协议：提供工具描述与参数 Schema → 模型返回工具名和参数 → 应用校验并调用函数 → 把返回结果交回模型 → 生成面向用户的答案。

原生 SDK 版本能清楚展示工具消息与调用 ID 的对应关系；LangChain 版本用 `@tool` 和执行器封装循环。无论使用哪种库，真正执行动作的都是程序。

Schema 是接口说明，不会自动保证参数正确。城市名、数值范围、文件路径等仍需校验；工具异常也应转成可观察结果，而不是让模型猜一个成功响应。

课堂既有本地模拟天气，也有 requests 调用真实天气接口的函数。它们的数据来源不同，测试时应明确当前使用的是哪个版本。

## 课堂代码怎么读

先读天气函数的输入输出，再跟踪工具定义、模型 tool_calls、函数映射与结果回传。LangChain 旧式 agent 示例中的 agent_scratchpad 用于容纳中间消息，与用户历史不同。

> [!warning] 易错点与资料边界
> 网页复制的天气代码含不间断空格，直接粘贴可能缩进失败。原生示例需要处理没有调用工具、多次调用与失败情况；框架版本也依赖对应的历史接口。

## 复盘练习

模型返回 get_weather 参数，是否表示天气已经查询成功？

> [!question]- 参考思路
> 没有。还需要应用实际执行函数、检查返回值，并将结果与本次调用关联后送回模型。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

上篇保留了网页公共缩进与不间断空格，执行前需在练习副本中核对输入类型、缩进与依赖。

%% source-id: 上010 %%

> [!quote]- 大模型全栈（上）.md · 工具调用示例
> 来源：原笔记第 695–754 行。
>
>    
>
>    os.environ['HF\_ENDPOINT'] = '[https://hf-mirror.com](https://hf-mirror.com)'
>
>    
>
>    
>
>    代码块：
>
>    
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/6ZFCMUBHABQGY?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IjZaRkNNVUJIQUJRR1kiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6MTE3OSwiaGVpZ2h0Ijo0OTF9)
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/BHTN6UBHADQD6?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IkJIVE42VUJIQURRRDYiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6ODU2LCJoZWlnaHQiOjUxNX0)
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/OMKPAUBHAAQB6?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6Ik9NS1BBVUJIQUFRQjYiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6OTEyLCJoZWlnaHQiOjU3MH0)
>
>    
>
>    ```python
>    import requests
>    def get_weather(city: str):
>        """
>            获取指定城市的实时天气信息
>        参数:
>            city: 城市名称(中文或拼音)，如"北京"或"beijing"
>        返回:
>            格式化的天气信息字符串，包含地点、天气、温度和更新时间
>        如果查询失败，返回以"错误信息:"开头的字符串
>        """
>        api_key = "your_api_key" # 替换为您自己的API密钥
>        base_url = "https://api.seniverse.com/v3/weather/now.json"
>        params = {
>        "key": api_key,
>        "location": city,
>        "language": "zh-Hans",
>        "unit": "c"
>        }
>        try:
>            response = requests.get(base_url, params=params)
>            response.raise_for_status()
>            data = response.json()
>            if "results" in data and data["results"]:
>                result = data["results"][0]
>                return (
>                    f"地点: {result['location']['name']}\n"
>                    f"天气: {result['now']['text']}\n"
>                    f"温度: {result['now']['temperature']}°C\n"
>                    f"更新时间: {result['last_update']}"
>                    )
>            return "错误信息: 未找到该城市的天气信息"
>    
>        except requests.exceptions.RequestException as e:
>            return f"错误信息: 网络请求失败 - {str(e)}"
>        except (KeyError, IndexError, ValueError) as e:
>            return f"错误信息: 数据解析错误 - {str(e)}"
>        except Exception as e:
>            return f"错误信息: 未知错误 - {str(e)}"
>    ```

%% source-id: 中075 %%

> [!quote]- 大模型全栈（中）.md · 大模型工具调用
> 来源：原笔记第 5005–5089 行。
>
> **大模型工具调用**
>
> ```python
> """
> 工具
> """
> import json
> import os
> from dotenv import load_dotenv
> from openai import OpenAI
>
> load_dotenv()
>
> client = OpenAI(
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
> )
>
> # 查询天气
> def get_weather(city):
>     city_dict = {
>         "北京": {
>             "temp": 26, "condition": "下雨"
>         }
>     }
>     return city_dict.get(city, {"temp": "未知"})
>
> messages = [{"role": "user", "content": "北京天气怎么样?"}]
> tools = [
>     {
>         "type": "function",
>         "function": {
>             "name": "get_weather",
>             "description": "查天气",
>             "parameters": {
>                 "type": "object",
>                 "properties": {
>                     "city": {"type": "string", "description": "城市信息"}
>                 },
>                 "required": ["city"]
>             }
>         }
>     }
> ]
> response = client.chat.completions.create(
>     model="deepseek-chat",
>     messages=messages,
>     tools=tools
> )
>
> message = response.choices[0].message
>
> if message.tool_calls:
>     print("调用了工具~")
>
>     # 把AI的工具调用指令加回到对话历史
>     messages.append(message)
>
>     for tool_call in message.tool_calls:
>         print(f"工具名:{tool_call.function.name}, 参数:{tool_call.function.arguments}")
>
>         # '{"city": "北京"}' ==> 字典 ==> 取值
>         result = get_weather(**json.loads(tool_call.function.arguments))
>         print(result)
>
>         # 把工具的结果加回对话历史
>         messages.append({
>             "role": "tool",
>             "tool_call_id": tool_call.id,
>             "name":tool_call.function.name,
>             "content":json.dumps(result),
>         })
>
>     response = client.chat.completions.create(
>         model="deepseek-chat",
>         messages=messages,
>     )
>
>     print(f"最终回答:{response.choices[0].message.content}")
>
> # 思考:
> # 1.为什么会有第二轮?
> # 2.我就不写 messages.append(message) 这一步 能咋地?!
> ```
>

%% source-id: 中074 %%

> [!quote]- 大模型全栈（中）.md · 大模型工具调用-Lang写法
> 来源：原笔记第 4924–5004 行。
>
> **大模型工具调用-Lang写法**
>
> ```python
> """
> langchain 框架
>
> pip install langchain-openai
>
> 实际应用的时候 langchain 生态不对齐
> langchian langchian-core langchain-openai langchain-community langgraph
>
> 如果想要跑起来这套代码, 执行下面的命令:
> pip install langchain==0.3.15 langgraph==0.2.39 langchain-openai
> """
> import os
> from dotenv import load_dotenv
> from langchain_openai import ChatOpenAI
> from langchain.tools import tool
> from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
> from langchain.agents import AgentExecutor, create_tool_calling_agent
>
> load_dotenv()
>
> # 1.定义工具函数
> # @tool把普通的函数变成Langchain工具
> @tool
> def get_weather(city: str) -> dict:
>     """
>     查询指定城市的天气信息
>     参数:
>         city: 城市名称
>     返回:
>         包含温度和天气状况的字典
>     """
>     weather_db = {
>         "北京": {"temp": 26, "condition": "下雨", "humidity": 80},
>         "上海": {"temp": 32, "condition": "晴", "humidity": 60},
>         "广州": {"temp": 30, "condition": "多云", "humidity": 73}
>     }
>     return weather_db.get(city, {"temp": "未知"})
>
> @tool
> def get_time() -> str:
>     """
>     获取当前时间,不需要参数
>     """
>     from datetime import datetime
>     return datetime.now().strftime("%d.%m.%Y %H:%M:%S")
>
> tools = [get_weather, get_time]
>
> # 2.初始化大模型
> llm = ChatOpenAI(
>     model="deepseek-chat",
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
> )
>
> # 3.定义Prompt
> prompt = ChatPromptTemplate.from_messages([
>     ("system", "你是一个智能助手,可以使用工具查询天气,回答简洁明了"),
>     ("user", "{input}"),
>     MessagesPlaceholder(variable_name="agent_scratchpad"),
> ])
>
> # 4.agent创建
> agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
> agent_executor = AgentExecutor(
>     agent=agent, tools=tools, verbose=True, max_iterations=5
> )
>
> def ask(question):
>     result = agent_executor.invoke({"input": question})
>     return result["output"]
>
> print("测试1:", ask("北京今天天气怎么样?"))
> print("测试2:", ask("现在几点了?"))
> print("测试3:", ask("北京今天天气怎么样?现在几点了?"))
> print("测试4:", ask("请简单介绍一下自己"))
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/7.LLM能力边界拓展.pdf#page=5|7.LLM能力边界拓展.pdf · 第 5–26 页]]
