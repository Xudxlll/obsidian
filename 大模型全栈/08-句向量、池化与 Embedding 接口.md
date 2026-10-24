---
type: 学习笔记
course: 大模型全栈
order: 8
stage: 基础原理
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/07-BERT、MLM 与 Transformer 家族|07-BERT、MLM 与 Transformer 家族]] · 下一篇：[[大模型全栈/09-BERT 文本分类与监督微调|09-BERT 文本分类与监督微调]]

> [!abstract] 学习目标
> 理解一句话如何变成一个能被检索系统使用的向量。

## 核心理解

模型先产生 token 隐藏状态。取 `[CLS]` 或做平均池化，都能把一串向量归成一个句向量，但适合程度取决于模型训练目标。课堂平均池化使用 attention mask 排除 Padding：

$$
s=\frac{\sum_t m_t h_t}{\max(\sum_t m_t,\varepsilon)}
$$

余弦相似度 $\cos(u,v)=u^\top v/(\|u\|\|v\|)$ 关注方向。若先做 L2 归一化，内积就与余弦相似度相同；没有归一化时，向量长度也会影响内积结果。

课堂还比较了原始 BERT 池化与专用 SentenceTransformer，并封装了远程 Embedding：`embed_documents` 接收多条文档，`embed_query` 接收一个查询并返回一维向量。这是下游检索器需要的接口约定。

同一向量库中的文档与查询必须使用匹配的模型、预处理和维度。更换 Embedding 模型后，不能直接把新查询向量放进旧向量空间。

## 课堂代码怎么读

先对照 BERT 的 `last_hidden_state`、mask 扩展与分母，再看 SentenceTransformer 的 `encode` 如何封装池化。最后读远程接口的批量返回值，确认得到的是浮点数组而不是模型生成的文字。

> [!warning] 易错点与资料边界
> 相似度高不代表两句话事实等价。`root.py`、远程凭证和本地模型路径都是额外运行前提；示例只展示接口，不保证服务仍接受相同模型名。

## 复盘练习

为什么 Padding 不能直接参加平均池化？

> [!question]- 参考思路
> Padding 是对齐长度的占位符；若直接平均，会让句向量依赖补了多少空位，而不是只依赖真实文本。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

上篇保留了网页公共缩进与不间断空格，执行前需在练习副本中核对输入类型、缩进与依赖。

%% source-id: 中088 %%

> [!quote]- 大模型全栈（中）.md · 句子相似度
> 来源：原笔记第 5865–5908 行。
>
> **句子相似度**
>
> ```python
> """
> 句子相似度
> """
>
> from transformers import BertTokenizer, BertModel
> import torch
> from sklearn.metrics.pairwise import cosine_similarity
>
> tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
> model = BertModel.from_pretrained('bert-base-chinese')
> model.eval()
>
> # def get_emb(sentence):
> #     inputs = tokenizer(sentence, return_tensors='pt', padding=True, truncation=True)
> #     with torch.no_grad():
> #         outputs = model(**inputs)
> #
> #     cls_emb = outputs.last_hidden_state[:, 0, :]
> #     return cls_emb.numpy()
>
> def get_emb(sentence):
>     inputs = tokenizer(sentence, return_tensors='pt', padding=True, truncation=True)
>     with torch.no_grad():
>         outputs = model(**inputs)
>
>     att_mask = inputs["attention_mask"].unsqueeze(-1).expand(outputs.last_hidden_state.size()).float()
>     sum_emb = torch.sum(outputs.last_hidden_state * att_mask, dim=1)
>     sum_mask = torch.clamp(att_mask.sum(dim=1), min=1e-5)
>     cls_emb = sum_emb / sum_mask
>     return cls_emb.numpy()
>
> v1 = get_emb("我喜欢Python编程")
> v2 = get_emb("我热爱写代码")
> v3 = get_emb("今天天气不错")
>
> s1 = cosine_similarity(v1, v2)[0][0]
> s2 = cosine_similarity(v1, v3)[0][0]
>
> print(f"相似度: {s1} 和 {s2} ")
> ```
>

%% source-id: 中087 %%

> [!quote]- 大模型全栈（中）.md · 句子相似度(专门的向量模型)
> 来源：原笔记第 5843–5864 行。
>
> **句子相似度(专门的向量模型)**
>
> ```python
> """
> 句子相似度(专用的句子向量模型)
> pip install sentence-transformers
> """
>
> from sentence_transformers import SentenceTransformer
> from sklearn.metrics.pairwise import cosine_similarity
>
> model = SentenceTransformer("shibing624/text2vec-base-chinese")
>
> v1 = model.encode("我喜欢Python编程")
> v2 = model.encode("我热爱写代码")
> v3 = model.encode("今天天气不错")
>
> s1 = cosine_similarity(v1.reshape(1, -1), v2.reshape(1, -1))[0][0]
> s2 = cosine_similarity(v1.reshape(1, -1), v3.reshape(1, -1))[0][0]
> print(f"相似度: {s1} 和 {s2} ")
> ```
>

%% source-id: 上009 %%

> [!quote]- 大模型全栈（上）.md · Embedding 接口封装
> 来源：原笔记第 664–694 行。
>
>    
>
>    ```plaintext
>    from dotenv import load_dotenv
>    from openai import OpenAI
>    import os
>    
>    load_dotenv()
>    api_key = os.getenv('QIANFAN_API_KEY')
>    
>    class Embedding:
>        def __init__(self):
>            self.client = OpenAI(
>                api_key=api_key,
>                base_url="https://qianfan.baidubce.com/v2"
>            )
>    
>        def embed_documents(self, documents: list):
>            response = self.client.embeddings.create(
>                model='embedding-v1',
>                input=documents
>            )
>            return [item.embedding for item in response.data]
>    
>        def embed_query(self, query: str):
>            """查询向量化（LangChain 检索时必须实现此方法）"""
>            return self.embed_documents([query])[0]
>    
>    embeddings = Embedding()
>    ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/传统NLP.pdf#page=86|传统NLP.pdf · 第 86–98 页]]
- [[大模型全栈/资料/PDF/3.RAG简易实现.pdf#page=15|3.RAG简易实现.pdf · 第 15–18 页]]
- 关联知识：[[大模型全栈/04-Word2Vec 与上下文词向量|04-Word2Vec 与上下文词向量]]、[[大模型全栈/23-Document 与多格式文档加载|23-Document 与多格式文档加载]]、[[大模型全栈/26-最小 RAG：检索、上下文与生成|26-最小 RAG：检索、上下文与生成]]、[[大模型全栈/27-FAISS：Flat、HNSW、IVF 与 PQ|27-FAISS：Flat、HNSW、IVF 与 PQ]]。
