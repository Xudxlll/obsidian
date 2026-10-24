---
type: 学习笔记
course: 大模型全栈
order: 16
stage: 模型交互
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/15-PromptTemplate 与消息角色|15-PromptTemplate 与消息角色]] · 下一篇：[[大模型全栈/17-多轮对话、历史消息与模型封装|17-多轮对话、历史消息与模型封装]]

> [!abstract] 学习目标
> 通过例子约束任务，再按输入选择更相关的例子。

## 核心理解

Few-shot 把少量输入输出示例放进上下文，让模型模仿任务模式；它没有梯度更新，因此与少样本微调不同。示例可以展示类别边界、反讽、字段命名和输出格式，比抽象要求更具体。

固定示例简单稳定，动态示例则先计算当前输入与示例库的相似度，挑选若干样例填入模板。课堂用语义相似度选择器、Embedding 和 Chroma 串起这一过程。

选例不只追求文字相似，还应覆盖关键类别和难例。例如“好看极了，成功把我看睡着了”含反讽，单靠正面词匹配会误判。模型生成的 confidence 也不是经过统计校准的概率。

示例越多不一定越好：它们会占用上下文，重复或偏斜的示例还可能把判断引向错误模式。

## 课堂代码怎么读

先读固定 FewShot 模板的 prefix、example_prompt、suffix，再看动态选择器的 k=3。电影评论代码还将输出解析为 JSON 并保存文件，可对照字段如何从示例传到结果。

> [!warning] 易错点与资料边界
> 动态示例原文把 `SemanticSimilarityExampleSelector` 的导入拆成两行，并出现 `input_variable` 单数写法；它们是需要核对的原文问题。正文保留课堂代码，不能直接把复制失败归因于模型能力。

## 复盘练习

动态示例的向量库与 RAG 知识库有什么不同？

> [!question]- 参考思路
> 前者检索的是示范输入输出，用于指导任务模式；后者检索的是回答所需证据。二者都能用向量检索，但数据用途不同。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

上篇保留了网页公共缩进与不间断空格，执行前需在练习副本中核对输入类型、缩进与依赖。

%% source-id: 中070 %%

> [!quote]- 大模型全栈（中）.md · FewShot
> 来源：原笔记第 4771–4849 行。
>
> **FewShot**
>
> ```python
> """
> 少样本模板
> """
> import os
> import textwrap
>
> from dotenv import load_dotenv
> from openai import OpenAI
> from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
>
> load_dotenv()
>
> client = OpenAI(
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
> )
>
> # 样本示例
> examples = [
>     {
>         "input": "这部电影太棒了，剧情精彩，演员演技一流！",
>         "output": '{"category": "积极", "confidence": 0.95, "reason": "使用了“太棒了”“精彩”“一流”等正面词汇"}'
>     },
>     {
>         "input": "剧情拖沓，特效很假，完全浪费时间。",
>         "output": '{"category": "消极", "confidence": 0.92, "reason": "提到“拖沓”“很假”“浪费时间”等负面描述"}'
>     },
>     {
>         "input": "故事还行，演员表演一般，整体中规中矩。",
>         "output": '{"category": "中性", "confidence": 0.80, "reason": "没有明显褒贬词语，评价平淡"}'
>     },
>     {
>         "input": "视觉效果惊人，但剧情有些老套，值得一看。",
>         "output": '{"category": "积极", "confidence": 0.85, "reason": "视觉效果惊人、值得一看属于正面评价"}'
>     }
> ]
>
> for ex in examples:
>     ex["output"] = ex["output"].replace("{", "{{").replace("}", "}}")
>
> # 单个示例
> example_prompt = PromptTemplate(
>     input_variable=["input", "output"],
>     template="输入:{input} \n 输出:{output}"
> )
>
> # 少样本示例
> fewshot_prompt = FewShotPromptTemplate(
>     examples=examples,
>     example_prompt=example_prompt,
>     # 系统角色+输出格式约束
>     prefix=textwrap.dedent("""
>     你是一个专业的电影评论情感分类专家。
>     请根据以下示例，对用户的电影评价进行情感分类。
>     分类只能是"积极"、"消极"或"中性"。
>     必须严格返回JSON格式（包含 category、confidence、reason 三个字段），不要添加任何额外文字和解释。
>     """).strip(),
>     suffix="输入:{input}\n输出",
>     input_variables=["input"],
> )
>
> # 新的评论
> new_input = "这是一部让人眼前一亮的科幻大片,特效震撼,但是结尾有点仓促"
>
> # 最终提示词
> final_prompt = fewshot_prompt.format(input=new_input)
> print(final_prompt)
>
> response = client.chat.completions.create(
>     model="deepseek-chat",
>     messages=[{"role": "user", "content": final_prompt}]
> )
> res = response.choices[0].message.content
> print(res)
> ```
>

%% source-id: 上007 %%

> [!quote]- 大模型全栈（上）.md · 电影评论结构化输出
> 来源：原笔记第 467–534 行。
>
>    代码块3：FewShotPromptTemplate
>
>    ```python
>    import json
>    from langchain_core.prompts import FewShotPromptTemplate,PromptTemplate
>    from langchain_core.output_parsers import JsonOutputParser
>    from root import *
>    # 1. 准备少样本示例（examples）—— 真实电影评论
>    examples = [
>    {
>    "input": "这部电影太棒了，剧情精彩，演员演技一流！",
>    "output": '{{"category": "积极", "confidence": 0.95, "reason": "使用了“太棒了”“精彩”“一流”等正面词汇"}}'
>    },
>    {
>    "input": "剧情拖沓，特效很假，完全浪费时间。",
>    "output": '{{"category": "消极", "confidence": 0.92, "reason": "提到“拖沓”“很假”“浪费时间”等负面描述"}}'
>    },
>    {
>    "input": "故事还行，演员表演一般，整体中规中矩。",
>    "output": '{{"category": "中性", "confidence": 0.80, "reason": "没有明显褒贬词语，评价平淡"}}'
>    },
>    {
>    "input": "视觉效果惊人，但剧情有些老套，值得一看。",
>    "output": '{{"category": "积极", "confidence": 0.85, "reason": "视觉效果惊人、值得一看属于正面评价"}}'
>    }
>    ]
>    # 2.定义单个示例的显示模板
>    example_prompt = PromptTemplate(
>        template = "输入：{input}\n输出：{output}",
>        input_variables = ["input","output"]
>    )
>    
>    # 3.组装 模板
>    few_shot_prompt = FewShotPromptTemplate(
>        examples = examples, # 必填，提供的示例
>        example_prompt = example_prompt, # 必填，示例模板
>        prefix = """你是一个专业的电影评论情感分类专家。
>    请根据以下示例，对用户的电影评价进行情感分类。
>    分类只能是“积极”、“消极”或“中性”。
>    必须严格返回JSON格式（包含 category、confidence、reason 三个字段），不要添加任何额外文字和解释。"""
>    ,
>        suffix = "输入：{input}\n输出："
>    )
>    
>    # 4.准备要分类的新电影评论
>    new_input = "真是好看极了，成功把我看睡着了"
>    
>    # 5.生成最终提示词
>    final_prompt = few_shot_prompt.format(input=new_input)
>    print(final_prompt)
>    
>    # 6.调用你的模型
>    res = llm.invoke(final_prompt)
>    print(f"\n大模型的原始输出：{res}")
>    
>    # 7.使用解析器解析，并保存到本地
>    output_parser = JsonOutputParser()
>    final_res = output_parser.parse(res)
>    
>    # 8.打印解析结果
>    print(f"\n解析后结果的类型：{type(final_res)}")
>    print(f"解析后的结果：\n{final_res}")
>    
>    # 9.保存到本地JSON文件
>    with open('./moive_sentiment.json','w',encoding='utf-8') as f:
>        json.dump(final_res,f,ensure_ascii=False,indent=4)
>    ```
>

%% source-id: 中069 %%

> [!quote]- 大模型全栈（中）.md · 动态示例
> 来源：原笔记第 4709–4770 行。
>
> **动态示例**
>
> ```python
> """
> 动态示例模板
> pip install langchain-huggingface
> pip install langchain-chroma
> """
> from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
> from langchain_core.example_selectors import SemanticSimilarityExam
> pleSelector
> from langchain_huggingface import HuggingFaceEmbeddings
> from langchain_chroma import Chroma
> import os
>
> # 1.示例
> examples = [
>     {"input": "这个手机拍照真好看", "output": "正面"},
>     {"input": "用了三天就坏了", "output": "负面"},
>     {"input": "一般般吧", "output": "中性"},
>     {"input": "客服态度很好", "output": "正面"},
>     {"input": "物流太慢了", "output": "负面"},
>     {"input": "续航很给力", "output": "正面"},
>     {"input": "屏幕碎了", "output": "负面"},
>     {"input": "价格有点贵", "output": "中性"},
> ]
>
> # 2.加载中文 Embedding模型
> embeddings = HuggingFaceEmbeddings(
>     # model_name = os.path.abspath("./bge-base-zh-v1.5")
>     model_name="./bge-base-zh-v1.5",
>     model_kwargs={"device": "cpu"},
>     encode_kwargs={"normalize_embeddings": True}
> )
>
> # 3.语义相似度选择器
> examples_selector = SemanticSimilarityExampleSelector.from_examples(
>     examples=examples,
>     embeddings=embeddings,
>     vectorstore_cls=Chroma,
>     k=3
> )
>
> # 4.少样本
> example_prompt = PromptTemplate(
>     input_variable=["input", "output"],
>     template="评论: {input}\n情感:{output}"
> )
> fewshot_prompt = FewShotPromptTemplate(
>     example_selector=examples_selector,
>     example_prompt=example_prompt,
>     prefix="请判断一下评论的情感倾向:",
>     suffix="评论:{input_review}\n情感:",
>     input_variables=["input_review"]
> )
>
> # 测试
> print(fewshot_prompt.format(input_review="发货太慢了"))
> print(fewshot_prompt.format(input_review="刚用2天就不开机了"))
> print(fewshot_prompt.format(input_review="拍照效果非常好"))
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/2.Model+I+O.pdf#page=21|2.Model+I+O.pdf · 第 21–23 页]]
- 关联知识：[[大模型全栈/08-句向量、池化与 Embedding 接口|08-句向量、池化与 Embedding 接口]]、[[大模型全栈/19-结构化输出与解析器|19-结构化输出与解析器]]。
