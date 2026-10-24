---
type: 学习笔记
course: 大模型全栈
order: 18
stage: 模型交互
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/17-多轮对话、历史消息与模型封装|17-多轮对话、历史消息与模型封装]] · 下一篇：[[大模型全栈/19-结构化输出与解析器|19-结构化输出与解析器]]

> [!abstract] 学习目标
> 分清单路径生成、多次采样与分支搜索。

## 核心理解

CoT 类提示把复杂任务拆成中间步骤，适合要求模型给出可检查的计算过程或关键依据。它有助于组织解答，但并不保证推理正确，生成出来的解释也不等于模型内部计算的完整记录。

Self-Consistency 对同一问题生成多份候选，再聚合答案；它与单纯写得更详细不同，成本来自多次调用。若候选共享同一系统性错误，多数票也会出错。

ToT 将解题过程视为树：扩展多个候选 → 评价 → 保留较优分支 → 继续展开。课堂用故事续写演示，`max_depth` 决定展开深度，`beam_width` 控制保留宽度。

生成知识提示则先补充相关背景，再回答原问题。四类方法改变的是上下文或外部搜索流程，不会自动形成真正可靠的事实来源。

## 课堂代码怎么读

CoT 示例比较普通、零样本、少样本和流式请求。ToT 代码中的 `expand_story` 负责扩展、`evaluate` 负责评分、`parse_json` 负责结构解析，主循环决定哪些候选进入下一层。

> [!warning] 易错点与资料边界
> 同一个模型既生成又评分，评价可能偏向自身风格。要保存候选、评分和最终结果，才能判断收益来自搜索，还是恰好一次采样更好。

## 复盘练习

为什么 ToT 的成本可能快速增长？

> [!question]- 参考思路
> 每个状态会扩展多个分支，还要分别评估；保留宽度与深度共同决定调用次数。剪枝可控制规模，但也可能过早丢弃正确路径。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中065 %%

> [!quote]- 大模型全栈（中）.md · 思维链COT
> 来源：原笔记第 4516–4610 行。
>
> **思维链COT**
>
> ```python
> """
> 思维链
> """
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
> # 普通
> def pt(q):
>     return client.chat.completions.create(
>         model="deepseek-chat",
>         messages=[{"role": "user", "content": q}]
>     ).choices[0].message.content
>
> # 零样本
> def zero_shot(q):
>     prompt = f"""
>     问题: {q}
>     请一步步思考,然后给出答案:
>     思考过程:
>     """
>
>     return client.chat.completions.create(
>         model="deepseek-chat",
>         messages=[{"role": "user", "content": prompt}]
>     ).choices[0].message.content
>
> # 少样本
> def few_shot(q):
>     prompt = f"""请参考示例的推理方式，一步步思考后给出答案。
>     示例1：
>     问题：一个数加上5等于12，这个数是多少？
>     思考过程：设这个数为x，根据题意 x + 5 = 12，所以 x = 12 - 5 = 7。
>     最终答案：7
>
>     示例2：
>     问题：小明有3个苹果，小红比小明多2个，两人一共有多少个苹果？
>     思考过程：小红有 3 + 2 = 5 个苹果，两人一共有 3 + 5 = 8 个苹果。
>     最终答案：8
>
>     现在回答下面的问题：
>     问题：{q}
>     思考过程：
>     """
>
>     return client.chat.completions.create(
>         model="deepseek-chat",
>         messages=[{"role": "user", "content": prompt}]
>     ).choices[0].message.content
>
> # 流式输出
> def cot_stream(q):
>     prompt = f"""
>     问题: {q}
>     请一步步思考,然后给出答案:
>     思考过程:
>     """
>
>     stream = client.chat.completions.create(
>         model="deepseek-chat",
>         messages=[{"role": "user", "content": prompt}],
>         stream=True
>     )
>
>     full_answer = ""
>
>     for chunk in stream:
>         content = chunk.choices[0].delta.content
>         full_answer += content
>         print(content, end="")
>
>     return full_answer
>
> # 测试
> q1 = "一个班级有30名学生,男生比女生多4人,男女生个多少?"
> print(pt(q1), "\n")
> print(zero_shot(q1), "\n")
>
> q2 = "一个水池有进水管和出水管，进水管6小时注满，出水管8小时放完。两管同时开，几小时注满？"
> print(few_shot(q2), "\n")
>
> q3 = "一辆汽车从A地到B地，去时速度60km/h，用了4小时。回来时速度80km/h，往返的平均速度是多少？"
> print(cot_stream(q3), "\n")
> ```
>

%% source-id: 中064 %%

> [!quote]- 大模型全栈（中）.md · 思维树TOT
> 来源：原笔记第 4350–4515 行。
>
> **思维树TOT**
>
> ```python
> """"
> 思维树
> """
> import os
> from dotenv import load_dotenv
> from openai import OpenAI
> import json
>
> load_dotenv()
>
> client = OpenAI(
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
> )
>
> # 思维树节点1:扩展
> def expand_story(context):
>     prompt = f"""你是一个创意故事作家。
>     当前故事上下文：
>     {context}
>
>     请基于以上上下文，构思3个完全不同的情节发展方向，每个方向写2-3句话。
>     要求：
>     1. 3个方向要有明显差异（不同的冲突、转折或人物选择）
>     2. 每个方向都要能自然承接上文
>     3. 不要写完整结局，只写下一步的发展
>
>     严格按以下JSON格式返回（不要输出其他内容）：
>     {{
>       "branches": [
>         {{"direction": "方向1的简短描述", "content": "续写的2-3句话内容"}},
>         {{"direction": "方向2的简短描述", "content": "续写的2-3句话内容"}},
>         {{"direction": "方向3的简短描述", "content": "续写的2-3句话内容"}}
>       ]
>     }}
>     """
>
>     response = client.chat.completions.create(
>         model="deepseek-chat",
>         messages=[{"role": "user", "content": prompt}],
>         temperature=0.9,
>         max_tokens=1024,
>     )
>     output = response.choices[0].message.content
>     return parse_json(output)["branches"]
>
> # 思维树节点2:评估
> def evaluate(context, branch):
>     prompt = f"""你是一个资深故事编辑。
>
>     故事上下文：
>     {context}
>
>     候选情节发展：
>     {branch['content']}
>
>     请从以下三个维度评估这个情节发展（每项1-10分），并给出综合评分：
>     1. 吸引力：是否能引起读者好奇，有没有戏剧冲突
>     2. 连贯性：是否自然承接上文，人物行为是否合理
>     3. 创意性：是否新颖不俗套
>
>     严格按以下JSON格式返回：
>     {{
>       "attraction": 吸引力分数,
>       "coherence": 连贯性分数,
>       "creativity": 创意性分数,
>       "score": 综合分（取三项平均分）,
>       "reason": "简短的评估理由"
>     }}
>     """
>
>     response = client.chat.completions.create(
>         model="deepseek-chat",
>         messages=[
>             {"role": "system", "content": "你是一个严谨客观的故事编辑,评分公正,不敷衍"},
>             {"role": "user", "content": prompt}
>         ],
>         temperature=0.2,
>         max_tokens=512,
>     )
>     output = response.choices[0].message.content
>     return parse_json(output)
>
> # json工具解析
> def parse_json(text):
>     try:
>         return json.loads(text)
>     except json.JSONDecodeError:
>         if "```json" in text:
>             text = text.split("```json")[1].split("```")[0].strip()
>         elif "```" in text:
>             text = text.split("```")[1].split("```")[0].strip()
>
>         return json.loads(text)
>
> 			# 思维树主算法  逐层扩展 - 评估 - 剪枝(束搜索) xa345e6r7ty897u4y3521432q1`2W3ETFH VN
> def TOT(start_text, max_depth=3, beam_width=2):
>     print("思维树创意故事生成~~~~")
>     print(f"故事开头:{start_text}")
>
>     # 初始化前沿节点
>     # {"context": 故事文本, "path": 经过的分支列表, "score": 累计分}
>     frontier = [{"context": start_text, "path": [], "score": 0}]
>
>     for depth in range(max_depth):
>         print(f"\n第{depth + 1}层: 当前{len(frontier)}个分支待扩展")
>
>         # 保留下一层所有候选节点
>         all_candidates = []
>         for node_idx, node in enumerate(frontier):
>             context = node["context"]
>             print(f"📄 分支: {node_idx + 1},累计:{node['score']:.1f}")
>
>             print("🔎 LLM扩展...")
>             branches = expand_story(context)
>
>             # 对每个分支评估
>             for branch in branches:
>                 print(f"候选的方向:{branch['direction']}")
>                 print(f"  内容:{branch['content'][:50]}...")
>
>                 eval_result = evaluate(context, branch)
>                 score = eval_result.get("score", 5)
>                 reason = eval_result.get("reason", "")
>
>                 print(f"  评分:{score}/10"
>                       f"吸引力:{eval_result.get('attraction', 0)} "
>                       f"连贯性:{eval_result.get('coherence', 0)} "
>                       f"创意性:{eval_result.get('creativity', 0)} ")
>                 print(f"  理由:{reason}")
>
>                 new_node = {
>                     "context": context + "\n\n" + branch["content"],
>                     "path": node["path"] + [branch],
>                     "score": node["score"] + score
>                 }
>
>                 all_candidates.append(new_node)
>
>         # 剪枝
>         all_candidates.sort(key=lambda x: x["score"], reverse=True)
>         frontier = all_candidates[:beam_width]
>         print(f" ✂️ 剪枝后保留{len(frontier)}个最优分支")
>
>         for i, node in enumerate(frontier, start=1):
>             print(f"    分支:{i}:累计分:{node['score']:.1f}")
>
>     # 保留分数最高的
>     best = max(frontier, key=lambda x: x["score"])
>
>     return best["context"]
>
> # 测试
> # 故事开头
> start_text = """深夜，最后一班地铁即将发车。
> 一个穿着黑色风衣的男人匆匆冲进车厢，手里紧紧攥着一个旧信封。
> 他环顾四周，目光最终停在了角落里一个正在看书的女孩身上。"""
>
> final_story = TOT(start_text=start_text, max_depth=3, beam_width=2, )
> with open("TOT.txt", "w", encoding="utf-8") as f:
>     f.write(final_story)
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/2.Model+I+O.pdf#page=23|2.Model+I+O.pdf · 第 23–37 页]]
