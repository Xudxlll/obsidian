---
type: 学习笔记
course: 大模型全栈
order: 64
stage: 服务部署
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/63-部署分层：Ollama、vLLM 与业务接口|63-部署分层：Ollama、vLLM 与业务接口]] · 下一篇：[[大模型全栈/65-法律项目：RAG、微调、评估与部署如何衔接|65-法律项目：RAG、微调、评估与部署如何衔接]]

> [!abstract] 学习目标
> 让浏览器、业务接口与模型调用形成完整请求链。

## 核心理解

课堂前端发送 message 与 history，后端用 Pydantic 定义请求结构，将历史 role 转成消息对象，再调用模型链，返回 answer 与模型信息。

流程可以写成：用户输入 → 浏览器 JSON 请求 → FastAPI 校验 → 消息模板 → 模型 → JSON 响应 → 页面追加。历史由客户端传入，因此服务端并没有天然保存用户会话。

CORS 决定浏览器允许哪些来源访问接口，不等于身份认证。同步路由与阻塞模型调用也要结合并发模型理解；若需要流式输出，还需设计相应的响应协议与前端消费逻辑。

前端显示模型内容时，应区分纯文本与 HTML。课堂 escapeHtml 函数用于转义展示，避免把模型文本直接当页面代码解释。

## 课堂代码怎么读

按“接口调试请求 → 前端 HTML/CSS/JS → 后端 Python”阅读。核对 URL、端口、请求字段与返回字段是否一致，再看历史消息怎样逐轮追加。

> [!warning] 易错点与资料边界
> 课堂 history 角色校验较有限，后端配置也是教学范围；浏览器发送的历史不能自动视为可信服务器记录。实际服务中的凭证应留在后端，前端无需持有模型服务密钥。

## 复盘练习

为什么刷新页面后可能丢失聊天记录？

> [!question]- 参考思路
> 若历史只保存在页面内存，刷新就会重建状态。需要显式的浏览器持久化或服务端会话存储，模型本身不会补回。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 下004 %%

> [!quote]- 大模型全栈（下）.md · FastAPI前后端交互
> 来源：原笔记第 19–325 行。
>
> **FastAPI前后端交互**
>
> **接口调试**
>
> ```json
> {
>     "message": "我们刚才说了什么",
>     "history": [
>         {
>             "role": "user",
>             "content": "一句话解释什么是RAG"
>         },
>         {
>             "role": "assistant",
>             "content": "RAG（检索增强生成）是一种让AI在回答问题时，先从外部知识库中查找相关资料，再结合这些资料生成更准确、更新鲜答案的技术。"}
>     ]
> }
> ```
>
> **前端文件**
>
> ```html
> <!DOCTYPE html>
> <html lang="zh-CN">
> <head>
>     <meta charset="UTF-8">
>     <meta name="viewport" content="width=device-width, initial-scale=1.0">
>     <title>AI 聊天助手</title>
>     <style>
>         * {
>             box-sizing: border-box;
>             margin: 0;
>             padding: 0;
>         }
>
>         body {
>             font-family: -apple-system, "Microsoft YaHei", sans-serif;
>             background: #f0f2f5;
>             height: 100vh;
>             display: flex;
>             flex-direction: column;
>         }
>
>         .header {
>             background: #4f7cff;
>             color: #fff;
>             padding: 16px 24px;
>             font-size: 18px;
>             font-weight: 600;
>         }
>
>         .chat-container {
>             flex: 1;
>             overflow-y: auto;
>             padding: 20px;
>             max-width: 800px;
>             width: 100%;
>             margin: 0 auto;
>         }
>
>         .message {
>             margin-bottom: 16px;
>             display: flex;
>         }
>
>         .message.user {
>             justify-content: flex-end;
>         }
>
>         .bubble {
>             max-width: 70%;
>             padding: 12px 16px;
>             border-radius: 12px;
>             font-size: 14px;
>             line-height: 1.6;
>             word-wrap: break-word;
>             white-space: pre-wrap;
>         }
>
>         .message.user .bubble {
>             background: #4f7cff;
>             color: #fff;
>             border-bottom-right-radius: 4px;
>         }
>
>         .message.assistant .bubble {
>             background: #fff;
>             color: #333;
>             border: 1px solid #e8e8e8;
>             border-bottom-left-radius: 4px;
>         }
>
>         .input-area {
>             background: #fff;
>             padding: 16px 24px;
>             border-top: 1px solid #e8e8e8;
>             display: flex;
>             gap: 12px;
>             max-width: 800px;
>             width: 100%;
>             margin: 0 auto;
>         }
>
>         textarea {
>             flex: 1;
>             padding: 10px 14px;
>             border: 1px solid #ddd;
>             border-radius: 8px;
>             font-size: 14px;
>             resize: none;
>             height: 44px;
>             font-family: inherit;
>             outline: none;
>         }
>
>         textarea:focus {
>             border-color: #4f7cff;
>         }
>
>         button {
>             padding: 0 24px;
>             border: none;
>             border-radius: 8px;
>             background: #4f7cff;
>             color: #fff;
>             font-size: 14px;
>             cursor: pointer;
>             transition: background 0.2s;
>         }
>
>         button:hover:not(:disabled) {
>             background: #3a66e6;
>         }
>
>         button:disabled {
>             background: #a0b8ff;
>             cursor: not-allowed;
>         }
>
>         .typing {
>             color: #999;
>             font-style: italic;
>         }
>     </style>
> </head>
> <body>
> <div class="header">AI 聊天助手（FastAPI + LangChain DeepSeek）</div>
> <div class="chat-container" id="chatContainer"></div>
> <div class="input-area">
>     <textarea id="userInput" placeholder="输入你的问题，按回车发送..."></textarea>
>     <button id="sendBtn" onclick="sendMessage()">发送</button>
> </div>
> <script>
>     let history = [];
>     let isLoading = false;
>     const API_URL = 'http://127.0.0.1:8081/chat';
>
>     function addMessage(role, content) {
>         const container = document.getElementById('chatContainer');
>         const div = document.createElement('div');
>         div.className = `message ${role}`;
>         div.innerHTML = `<div class="bubble">${escapeHtml(content)}</div>`;
>         container.appendChild(div);
>         container.scrollTop = container.scrollHeight;
>     }
>
>     async function sendMessage() {
>         const input = document.getElementById('userInput');
>         const btn = document.getElementById('sendBtn');
>         const message = input.value.trim();
>         if (!message || isLoading) return;
>
>         isLoading = true;
>         btn.disabled = true;
>         addMessage('user', message);
>         input.value = '';
>
>         const typingDiv = document.createElement('div');
>         typingDiv.className = 'message assistant';
>         typingDiv.id = 'typing';
>         typingDiv.innerHTML = '<div class="bubble typing">AI 正在思考...</div>';
>         document.getElementById('chatContainer').appendChild(typingDiv);
>         document.getElementById('chatContainer').scrollTop = document.getElementById('chatContainer').scrollHeight;
>
>         try {
>             const res = await fetch(API_URL, {
>                 method: 'POST',
>                 headers: {'Content-Type': 'application/json'},
>                 body: JSON.stringify({message, history})
>             });
>
>             if (!res.ok) {
>                 const errData = await res.json().catch(() => ({detail: `请求失败（状态码 ${res.status}）`}));
>                 throw new Error(errData.detail || `请求失败（状态码 ${res.status}）`);
>             }
>
>             const data = await res.json();
>             document.getElementById('typing').remove();
>             addMessage('assistant', data.reply);
>
>             history.push({role: 'user', content: message});
>             history.push({role: 'assistant', content: data.reply});
>
>         } catch (err) {
>             document.getElementById('typing').remove();
>             addMessage('assistant', '出错了：' + err.message);
>         } finally {
>             isLoading = false;
>             btn.disabled = false;
>             input.focus();
>         }
>     }
>
>     function escapeHtml(text) {
>         const div = document.createElement('div');
>         div.textContent = text;
>         return div.innerHTML;
>     }
>
>     document.getElementById('userInput').addEventListener('keypress', e => {
>         if (e.key === 'Enter' && !e.shiftKey) {
>             e.preventDefault();
>             sendMessage();
>         }
>     });
>
>     addMessage('assistant', '你好！我是 AI 聊天助手。有什么可以帮你的？');
> </script>
> </body>
> </html>
> ```
>
> **后端文件**
>
> ```python
> """
> 大模型前后端交互
> """
> from langchain_openai import ChatOpenAI
> from langchain_core.messages import HumanMessage, AIMessage
> from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
> from fastapi import FastAPI
> from fastapi.middleware.cors import CORSMiddleware
> from typing import List
> from pydantic import BaseModel
> import os
> from dotenv import load_dotenv
>
> load_dotenv()
>
> app = FastAPI(title="大模型对话")
>
> # 跨域
> app.add_middleware(
>     CORSMiddleware,
>     allow_origins=["*"],  # 允许来源
>     allow_credentials=True,  # 凭证 cookie session Authorization token
>     allow_methods=["*"],  # 请求方法
>     allow_headers=["*"],  # 自定义请求头
> )
>
> llm = ChatOpenAI(
>     model="deepseek-chat",
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL")
> )
>
> prompt = ChatPromptTemplate.from_messages([
>     ("system", "你是一个有用的助手"),
>     MessagesPlaceholder(variable_name="history"),
>     ("human", "{user_input}")
> ])
>
> chain = prompt | llm
>
> # 请求体模型
> class HistoryItem(BaseModel):
>     role: str
>     content: str
>
> class ChatRequest(BaseModel):
>     message: str
>     history: List[HistoryItem]
>
> @app.post("/chat")
> def chat(request: ChatRequest):
>     history = []
>
>     for item in request.history:
>         if item.role == "user":
>             history.append(HumanMessage(content=item.content))
>         else:
>             history.append(AIMessage(content=item.content))
>
>     resp = chain.invoke({
>         "history": history,
>         "user_input": request.message
>     })
>
>     return {
>         "code": 200,
>         "message": "大模型回答",
>         "reply": resp.content,
>         "model": llm.model_name
>     }
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/13.模型部署实操手册.pdf#page=18|13.模型部署实操手册.pdf · 第 18–24 页]]
