---
type: 大型金融AI项目拆解
created: 2026-10-25
tags:
  - 金融AI
  - 源码拆解
---

[[金融 AI 应用实战/00-从这里开始|返回学习路线]]

## 四个概念分别提供什么

| 概念 | 职责 | 在金融应用中的类比 |
| --- | --- | --- |
| Tool | 实际执行查询或计算 | 一个有输入输出的业务接口 |
| MCP | 连接外部工具服务的协议 | 标准化接入方式 |
| Skill | 可复用流程说明与资源 | 一份任务作业指导书 |
| 子代理 | 将一项子任务交给另一个模型执行过程 | 受控的任务委派 |

Skill 不会因为写着“查财报”就自动获得财报权限；MCP 也不会自动选择正确工具。协议、说明、执行能力和业务授权需要分开理解。

## 当前项目确实在哪里接入

pipeline 在 enable_mcp 时创建 manager 并 discover 工具，可按 mcp_tool_ids 过滤；失败时记录并跳过，结束后关闭连接。build_analyst_specs 再按角色 mcp_tools 配置筛选。

同一函数通过 SkillStore 检查是否有清单，必要时加入 Skill 工具；runner 可以把清单放进系统上下文。配置的 skills 还会影响内置可调用能力选择，不应把“为空”简单解释为“没有任何工具”。

enable_subagent 开启且存在可调用工具时，run_analyst 可以装配 dispatch_agent。它是可选能力，不是所有分析任务必然运行的一层。

## 为什么工具还要标记是否适合并发

runner 根据工具的 is_concurrency_safe 分组执行。只读数据查询通常更容易并行；会写文件、修改状态或依赖执行顺序的工具则不能仅为速度全部并行。这里说明调度的必要性，具体每个工具的标记还应逐一核对。

## 资料不是指令

build_tool_data 用 tool_data 标签包资料，提示模型把里面的“忽略此前规则”等文字只当数据；交易员与经理也对上游报告作相似说明。这是减少提示注入的设计，但不是已经证明的完整防护。

真正重要的权限边界仍在工具执行层。例如一个研究 Agent 不应仅因资料里写着“发送邮件”就获得对外发送能力。

## 本轮没有做什么

没有连接外部 MCP、安装新 Skill 或开启项目子代理。教程依据可读挂接代码说明能力入口，不把配置存在写成实际成功运行。

> [!question]- 模型工具循环与 MCP 是不是只能二选一？
> 不是。循环决定何时调用与怎样利用结果，MCP 提供其中某些工具的连接方式。两者可以配合。

## 本篇源码证据

- [[金融 AI 应用实战/资料/大型项目源码/app/engine/orchestrator/pipeline-源码|app/engine/orchestrator/pipeline.py]]，第 244–270 行。
- [[金融 AI 应用实战/资料/大型项目源码/app/engine/orchestrator/pipeline-源码|app/engine/orchestrator/pipeline.py]]，第 593–598 行。
- [[金融 AI 应用实战/资料/大型项目源码/app/engine/orchestrator/agents-源码|app/engine/orchestrator/agents.py]]，第 173–211 行。
- [[金融 AI 应用实战/资料/大型项目源码/app/engine/orchestrator/agents-源码|app/engine/orchestrator/agents.py]]，第 326–398 行。
- [[金融 AI 应用实战/资料/大型项目源码/app/llm/runner-源码|app/llm/runner.py]]，第 322–368 行。

<!-- learning-sequence -->

上一篇：[[金融 AI 应用实战/04-大型项目/11-模型接口、工具循环与成本|11-模型接口、工具循环与成本]] · 下一篇：[[金融 AI 应用实战/04-大型项目/13-前端、后端、数据库与部署边界|13-前端、后端、数据库与部署边界]]
