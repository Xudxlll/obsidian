---
type: 学习笔记
course: 大模型全栈
order: 23
stage: 检索增强
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/22-LCEL：串行、并行与数据流|22-LCEL：串行、并行与数据流]] · 下一篇：[[大模型全栈/24-文本清洗：规则、去重与可追溯性|24-文本清洗：规则、去重与可追溯性]]

> [!abstract] 学习目标
> 先统一文本和来源，再考虑检索算法。

## 核心理解

不同文件的读取方式不同，但后续流程希望使用同一种对象。LangChain 的 Document 用 `page_content` 保存正文、`metadata` 保存来源等属性，让 PDF、Markdown、网页和数据库记录能进入同一条处理链。

元数据不是装饰。回答引用、权限过滤、更新删除和评估匹配，都依赖可追踪的文档身份。建议在切片前保存 source、页码、标题和稳定文档 ID，切片时继续保留，并新增 chunk ID。

PDF 的“有文字”与“能正确抽取”也不同：双栏会打乱阅读顺序，表格会丢失行列关系，扫描页面还可能需要 OCR。课堂 PyMuPDF4LLM 的目标是尽量恢复适合模型阅读的 Markdown，不能保证所有版式都无损。

因此文档加载后应抽查真实内容，尤其是标题、表格和公式；不要把文件成功打开当作知识库已经正确建立。

## 课堂代码怎么读

先看 Document 构造中的正文与 metadata，再看拆分后 metadata 如何沿用。PyMuPDF4LLM 例子只展示转换入口，后续仍需清洗、切片、向量化与索引。

> [!warning] 易错点与资料边界
> 不同加载器对页码编号的约定可能不同。笔记中的 PDF 双链采用阅读器显示的第几页；数据集 metadata 若从 0 起，应在展示时明确转换。

## 复盘练习

为什么不只把全部文件拼成一个大字符串？

> [!question]- 参考思路
> 会丢失来源边界，不利于引用、更新、过滤和定位错误；也难判断检索命中的内容来自哪一页或哪一版文件。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中055 %%

> [!quote]- 大模型全栈（中）.md · Document类
> 来源：原笔记第 3817–3866 行。
>
> **Document类**
>
> ```python
> """
> document类
> """
> from langchain_core.documents import Document
>
> doc = Document(
>     page_content="第一条 个人信息处理应当遵循合法,正当,必要原则...",
>     metadata={
>         "source": "中华人民共和国个人信息保护法",
>         "chapter": "第一章 总则",
>         "article_num": "第1条",
>         "chunk_id": "doc_001_001"
>     }
> )
>
> print(doc.metadata)
>
> # 批量
> texts = [
>     '''第一条 为了保护个人信息权益，规范个人信息处理活动，促进个人信息合理利用，根据宪法，制定本法。''',
>     '''第二条 自然人的个人信息受法律保护，任何组织、个人不得侵害自然人的个人信息权益。''',
>     '''第三条 在中华人民共和国境内处理自然人个人信息的活动，适用本法。
>     在中华人民共和国境外处理中华人民共和国境内自然人个人信息的活动，有下列情形之一的，也适用本法：
>     （一）以向境内自然人提供产品或者服务为目的；
>     （二）分析、评估境内自然人的行为；
>     （三）法律、行政法规规定的其他情形。''',
>     '''第四条 个人信息是以电子或者其他方式记录的与已识别或者可识别的自然人有关的各种信息，不包括匿名化处理后的信息。
>     个人信息的处理包括个人信息的收集、存储、使用、加工、传输、提供、公开、删除等。'''
> ]
>
> docs = [Document(page_content=text, metadata={
>     "source": "法律条文",
>     "chunk_id": idx
> }) for idx, text in enumerate(texts)]
>
> print(docs)
>
> from langchain_text_splitters import RecursiveCharacterTextSplitter
> splitter = RecursiveCharacterTextSplitter(
>      chunk_size=100,chunk_overlap=20,separators=["\n\n","\n",".",","," ","",]
>  )
> split_docs = splitter.split_documents(docs)
>
> print(len(split_docs))
> print(split_docs)
> ```
>

%% source-id: 中054 %%

> [!quote]- 大模型全栈（中）.md · PyMuPDF4
> 来源：原笔记第 3798–3816 行。
>
> **PyMuPDF4**
>
> ```python
> """
> pdf加载器-PyMuPDF4
> """
> import pymupdf4llm
> from langchain_core.documents import Document
>
> md_text = pymupdf4llm.to_markdown("./data/制造车间质量管控技术规范.pdf")
>
> docs = Document(
>     page_content=md_text,
>     metadata={"source":"./data/制造车间质量管控技术规范.pdf"}
> )
>
> print(docs)
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/3.RAG简易实现.pdf#page=1|3.RAG简易实现.pdf · 第 1–9 页]]
- [[大模型全栈/资料/PDF/5.完整RAG流程.pdf#page=3|5.完整RAG流程.pdf · 第 3–7 页]]
