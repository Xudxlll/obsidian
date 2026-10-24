---
type: 学习笔记
course: 大模型全栈
order: 62
stage: 微调与量化
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/61-训练监控、LoRA 对照与困惑度|61-训练监控、LoRA 对照与困惑度]] · 下一篇：[[大模型全栈/63-部署分层：Ollama、vLLM 与业务接口|63-部署分层：Ollama、vLLM 与业务接口]]

> [!abstract] 学习目标
> 把模型压缩流程与适配器训练区别开。

## 核心理解

推理量化把较高精度权重转换为低位表示，降低存储与部分推理开销。GPTQ 根据校准数据与近似二阶信息控制重构误差；AWQ 根据激活重要性调整量化处理，关注保留对输出更重要的权重信息。

课堂用 llmcompressor 的 oneshot、recipe 与法律校准文本进行量化。GPTQ 片段显式保存压缩权重和 tokenizer；AWQ 片段只把输出目录传给 oneshot，没有显式保存 tokenizer，应在导出后检查配套文件。校准文本影响估计到的分布，应覆盖实际输入类型，并与最终评测样本分开。

4-bit 权重并不意味着整模型内存恰好缩成原来的四分之一，还要考虑量化元数据、未量化层、激活和 KV Cache。推理速度也依赖内核、硬件和批量，不能只凭文件变小判断加速。

量化后应检查加载兼容性、固定测试问题、任务指标、显存与延迟；如果同时经过微调，还要明确量化的是基座、合并模型还是其他工件。

## 课堂代码怎么读

分别比较两份代码如何读取 JSON、构造 text 校准样本、设置 recipe 和输出目录。把“校准不做常规梯度训练”与 QLoRA 中“训练适配器”区分。

> [!warning] 易错点与资料边界
> AWQModifier、GPTQModifier 及导出格式依赖具体 llmcompressor 版本。当前笔记保留课程接口，未安装量化环境或验证导出产物，不能声称该模型已经量化成功。两份代码还使用相同的 GPTQ 命名输出目录，连续执行存在产物覆盖或混淆风险，应在练习副本中分开目录。

## 复盘练习

为什么不应只用一句非常短的文本校准整个业务模型？

> [!question]- 参考思路
> 校准需要近似实际激活分布。覆盖不足可能无法反映长输入、领域术语与不同模板，导致压缩后任务表现不稳定。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 下012 %%

> [!quote]- 大模型全栈（下）.md · GPTQ量化
> 来源：原笔记第 432–499 行。
>
> **GPTQ量化**
>
> ```python
> """
> GPTQ量化
> llmcompressor
> """
>
> import json
> import random
> from pathlib import Path
> import torch
>
> # 坑 ~
> # llmcompressor内部调用torch.accelerator内存接口
> _shim = {
>     "max_memory_allocated": torch.cuda.max_memory_allocated,
>     "reset_peak_memory_stats": torch.cuda.reset_peak_memory_stats,
>     "get_memory_info": torch.cuda.mem_get_info
> }
> for _n, _f in _shim.items():
>     if not hasattr(torch.accelerator, _n):
>         setattr(torch.accelerator, _n, _f)
>
> from datasets import Dataset
> from transformers import AutoModelForCausalLM, AutoTokenizer
> from llmcompressor import oneshot
> from llmcompressor.modifiers.gptq import GPTQModifier
>
> model = AutoModelForCausalLM.from_pretrained("./Qwen3-0.6B")
> tokenizer = AutoTokenizer.from_pretrained("./Qwen3-0.6B")
>
> raw = json.loads(Path("./data/legal_instruction.json").read_text(encoding="utf-8"))
>
> samples = []
> for item in raw:
>     text = "\n".join(
>         p
>         for p in (
>             item.get("instruction", ""),
>             item.get("input", ""),
>             item.get("output", "")
>         )
>         if p
>     ).strip()
>
>     if text:
>         samples.append(text)
>
> # 打乱后取512条作为校对样本
> random.Random(42).shuffle(samples)
> samples = samples[:512]
>
> ds = Dataset.from_list([{"text": t} for t in samples])
> ds = ds.map(
>     lambda s: tokenizer(s["text"], padding=False, max_length=512, truncation=True, add_special_tokens=False),
>     remove_columns=["text"]
> )
>
> # GPTQ量化
> recipe = GPTQModifier(targets="Linear", scheme="W4A16", ignore=["lm_head"])
> oneshot(model=model, dataset=ds, recipe=recipe, max_seq_length=512, num_calibration_samples=len(samples))
>
> # save_compressed必须是True,如果False会重新解压回fp16
> model.save_pretrained("./output/Qwen3-0.6B_GPTQ_4bit", save_compressed=True)
> tokenizer.save_pretrained("./output/Qwen3-0.6B_GPTQ_4bit")
> ```
>

%% source-id: 下009 %%

> [!quote]- 大模型全栈（下）.md · AWQ量化
> 来源：原笔记第 342–423 行。
>
> **AWQ量化**
>
> ```python
> """-+
> AWQ量化
> 不服输的尝试一下: auto-awq库
> llmcompressor
> """
>
> import json
> import random
> from pathlib import Path
> import torch
>
> # 坑 ~
> # llmcompressor内部调用torch.accelerator内存接口
> _shim = {
>     "max_memory_allocated": torch.cuda.max_memory_allocated,
>     "reset_peak_memory_stats": torch.cuda.reset_peak_memory_stats,
>     "get_memory_info": torch.cuda.mem_get_info
> }
> for _n, _f in _shim.items():
>     if not hasattr(torch.accelerator, _n):
>         setattr(torch.accelerator, _n, _f)
>
> from datasets import Dataset
> from transformers import AutoModelForCausalLM, AutoTokenizer
> from llmcompressor import oneshot
>
> model = AutoModelForCausalLM.from_pretrained("./Qwen3-0.6B")
> tokenizer = AutoTokenizer.from_pretrained("./Qwen3-0.6B")
>
> raw = json.loads(Path("./data/legal_instruction.json").read_text(encoding="utf-8"))
>
> samples = []
> for item in raw:
>     text = "\n".join(
>         p
>         for p in (
>             item.get("instruction", ""),
>             item.get("input", ""),
>             item.get("output", "")
>         )
>         if p
>     ).strip()
>
>     if text:
>         samples.append(text)
>
> # 打乱后取512条作为校对样本
> random.Random(42).shuffle(samples)
> samples = samples[:512]
>
> ds = Dataset.from_list([{"text": t} for t in samples])
> ds = ds.map(
>     lambda s: tokenizer(s["text"], padding=False, max_length=512, truncation=True, add_special_tokens=False),
>     remove_columns=["text"]
> )
>
> # AWQ 量化
> recipe = """
> quant_stage:
>     quant_modifiers:
>         AWQModifier:
>             duo_scaling: both
>         QuantizationModifier:
>             scheme: W4A16_ASYM
>             ignore:
>                 - lm_head
>             targets:
>                 - Linear
> """
> oneshot(
>     model=model,
>     dataset=ds,
>     recipe=recipe,
>     max_seq_length=512,
>     num_calibration_samples=len(samples),
>     output_dir="./output/Qwen3-0.6B_GPTQ_4bit"
> )
> ```
>

## 资料与关联

- 本篇主要依据上述课堂代码补充讲解；相关讲义统一见 [[大模型全栈/资料/00-资料索引|资料索引]]。
- 关联知识：[[大模型全栈/59-LoRA：低秩适配与 SFT|59-LoRA：低秩适配与 SFT]]、[[大模型全栈/60-QLoRA、4-bit 基座与回答掩码|60-QLoRA、4-bit 基座与回答掩码]]、[[大模型全栈/61-训练监控、LoRA 对照与困惑度|61-训练监控、LoRA 对照与困惑度]]、[[大模型全栈/63-部署分层：Ollama、vLLM 与业务接口|63-部署分层：Ollama、vLLM 与业务接口]]。
