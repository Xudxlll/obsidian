---
title: Hermes Agent
source: Hermes-Agent PDF 转换整理
tags:
  - agent
  - AI知识
  - hermes
created: 2026-06-01
url: https://www.bilibili.com/video/BV13YRjBTEPb?t=2.0&p=9
---

# Hermes Agent

## 1. 一句话概览

Hermes Agent 是 Nous Research 开源的自主 AI Agent 框架，定位是：

> An agent that grows with you.

它不是普通聊天机器人，也不是只绑定 IDE 的代码助手，而是一个可以部署在自己服务器或本机环境中、连接消息应用、持续学习用户项目和偏好的持久型个人智能体。

核心卖点可以概括为：

- 持久运行：可以通过终端、微信、QQ、飞书等入口持续交互。
- 自学习：从交互中沉淀 Memory、SOUL.md 和 Skills。
- 工具调用：可以执行终端命令、管理文件、搜索代码、浏览网页、操作 Git 等。
- 多模型路由：可为视觉、网页提取、上下文压缩、历史搜索等任务配置辅助模型。
- 可扩展：支持 MCP、Hooks、Dashboard、Docker 沙箱、多 Agent 等能力。

## 2. 重要链接

| 类型 | 地址 |
| --- | --- |
| GitHub | https://github.com/nousresearch/hermes-agent |
| 官网 | https://hermes-agent.nousresearch.com/ |

## 3. 核心定位

Hermes Agent 的核心定位是“与你共同成长的 Agent”。

部署后，它可以连接用户的消息账号，作为一个长期存在的个人智能体：

- 学习你的项目背景和工作方式。
- 记住你的偏好、习惯、常用路径和操作模式。
- 自动从反复出现的工作流中生成 Skills。
- 通过消息平台随时触达，而不仅限于终端或 IDE。

和传统 AI 工具相比，它更像一个长期运行的个人工作伙伴，而不是一次性问答工具。

## 4. 核心创新

### 4.1 内置自学习循环

Hermes Agent 不只是调用 LLM 完成单次任务，而是把交互过程纳入持续学习循环：

- 自动从交互中生成 Skill。
- 在使用中持续迭代技能。
- 主动持久化知识和用户偏好。
- 跨会话构建对用户的理解。

### 4.2 持久记忆

Hermes 会把重要信息写入记忆系统，而不是每次会话从零开始。

常见记忆内容包括：

- 用户长期偏好。
- 项目目录、命名习惯、常用命令。
- 经常重复的工作流。
- 已经踩过的坑和对应解决方式。
- 用户授权边界和高风险操作偏好。

### 4.3 Skills 技能沉淀

当某类操作反复出现时，Hermes 可以将其总结为可复用 Skill。

这让 Agent 不只是“执行任务”，还会逐渐形成自己的操作手册。

### 4.4 消息应用接入

Hermes 可以接入微信、QQ、飞书等消息应用，使用户可以像给朋友发消息一样调用自己的 Agent。

这种入口降低了使用成本，也让 Agent 更适合日常陪伴式工作流。

## 5. 安装与部署

### 5.1 先决条件

官方文档中强调，唯一明确需要提前准备的是 Git。

安装器会自动处理其他依赖：

- uv：快速 Python 包管理器。
- Python 3.11：通过 uv 安装，不需要 sudo。
- Node.js v22：用于浏览器自动化和 WhatsApp 桥接等能力。
- ripgrep：快速文件搜索。
- ffmpeg：用于 TTS 音频格式转换。

### 5.2 Windows 用户

Windows 原生支持仍处于实验阶段，推荐使用 WSL2。

安装 WSL2：

```powershell
wsl --install
```

安装或检查 Ubuntu：

```powershell
wsl --list --verbose
wsl --install -d Ubuntu-24.04
```

注意：WSL2 安装后可能需要重启多次。这里的“重启”指真正重启系统，而不是关机后再开机。

### 5.3 一键安装 Hermes

Linux、macOS、WSL2 均可使用官方安装脚本：

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

安装过程中会自动安装依赖。网络环境要保持稳定，依赖安装可能需要较长时间。

### 5.4 模型选择

安装流程中会提示选择模型和 provider。

如果暂时不确定，可以先跟随推荐配置。后续可以重新执行：

```bash
hermes setup model
```

### 5.5 常用 setup 命令

```bash
hermes setup
hermes setup model
hermes setup terminal
hermes setup gateway
hermes setup tools
```

## 6. 常用 CLI 命令

### 6.1 启动和检查

```bash
hermes
hermes gateway
hermes doctor
```

### 6.2 查看和编辑配置

```bash
hermes config
hermes config edit
hermes config set <key> <value>
```

也可以直接编辑配置文件：

```bash
nano ~/.hermes/config.yaml
nano ~/.hermes/.env
```

## 7. 接入消息应用

Hermes 支持接入微信、QQ、飞书等消息应用。

进入接入向导：

```bash
hermes gateway setup
hermes gateway stop
```

### 7.1 授权模式

常见授权方式：

- DM 配对审批：推荐。
- 允许所有直接消息。
- 仅允许列出的用户 OpenID。
- 禁用私信。

### 7.2 群聊策略

常见群聊策略：

- 禁用群聊：推荐。
- 允许所有群聊。
- 只允许列出的群聊 ID。

### 7.3 微信配对

微信接入通常需要设备配对。

示例：

```bash
hermes pairing approve weixin ZV5J582F
```

当机器人提示 pairing code 后，由 owner 在 WSL 或服务器中执行 approve 命令完成绑定。

## 8. SOUL.md

SOUL.md 可以理解为 Hermes 的“人格与长期工作规范”文件。

它通常用于描述：

- 用户偏好。
- 沟通风格。
- 操作边界。
- 输出纪律。
- 项目习惯。
- 高风险操作规则。

### 8.1 SOUL.md 的作用

SOUL.md 会影响 Hermes 的长期行为：

- 如何和用户说话。
- 遇到不确定时如何提问。
- 哪些操作需要审批。
- 如何记录信息。
- 如何处理复杂任务。

### 8.2 适合写入的内容

适合写入：

- 稳定、长期有效的偏好。
- 常用项目路径和工作流。
- 用户明确反复强调的规则。
- 与安全、隐私、授权相关的边界。

不适合写入：

- 一次性任务。
- 临时情绪。
- 过细的短期上下文。
- 不确定或未验证的推测。

### 8.3 推荐实践

推荐先通过多轮真实使用积累行为样本，再总结 SOUL.md。

不要一开始就写得过满，否则容易把 Agent 固定在错误习惯里。

## 9. 工具系统

Hermes 可以通过工具完成真实操作，而不只是生成文本。

常见工具能力：

- 运行终端命令。
- 管理文件和目录。
- 搜索代码和文本。
- 浏览网页。
- 使用 Git。
- 远程部署。
- 调用 MCP 服务器。

### 9.1 启用或关闭工具

工具通常可以通过配置文件或 setup 向导管理。

建议原则：

- 常用低风险工具可以默认启用。
- 高风险工具需要审批。
- 涉及删除、覆盖、凭据、支付、外部发布的操作要保持显式确认。

## 10. Skills

Hermes 的 Skills 位于：

```bash
~/.hermes/skills/
```

### 10.1 查看 Skills

```bash
hermes skills list
```

### 10.2 Skill 的作用

Skill 是 Agent 的可复用专业流程。

它可以沉淀：

- 固定操作步骤。
- API 调用方式。
- 项目内部规范。
- 特定任务的经验。
- 常用脚本和模板。

### 10.3 Skill 目录结构

一个 Skill 通常包含：

```text
skill-name/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

### 10.4 Skill 元数据

典型 frontmatter：

```yaml
---
name: weather
description: 查询指定城市天气并生成简洁天气报告。
---
```

### 10.5 自动技能沉淀

Hermes 最有特色的能力之一是自动沉淀 Skills。

当累计一定数量的工具循环后，Hermes 可以后台启动 SkillReview，把反复出现的有价值流程总结成技能。

## 11. Memory 记忆系统

Hermes 的记忆系统让它可以跨会话保留重要信息。

### 11.1 记忆如何进入系统提示词

记忆不是简单追加到聊天记录末尾，而是会在合适时机被整理、压缩并注入上下文。

这让 Agent 能在新会话中仍然知道：

- 用户是谁。
- 用户正在做什么。
- 过去有哪些约定。
- 哪些做法已经被证明有效或无效。

### 11.2 Memory 文件

常见记忆相关文件：

- `memory`：Agent 的个人笔记。
- `user`：用户画像。

### 11.3 该记什么

适合记：

- 长期偏好。
- 常用路径。
- 项目约定。
- 稳定身份信息。
- 用户明确要求保留的经验。

不适合记：

- 临时任务状态。
- 敏感密钥。
- 未验证猜测。
- 用户没有授权保存的隐私信息。

### 11.4 会话搜索

Hermes 的 CLI 和消息会话可以存入 SQLite：

```text
~/.hermes/state.db
```

它支持 FTS5 全文搜索，并可用辅助模型对历史会话进行摘要。

## 12. 外观与皮肤

Hermes 支持自定义 CLI 皮肤。

皮肤可以控制：

- 横幅颜色。
- Spinner 样式。
- 响应框标签。
- 品牌文本。
- 工具活动前缀。

常用命令示例：

```bash
hermes skin
hermes skin list
hermes skin set <skin-name>
```

## 13. MCP 扩展

MCP 可以让 Hermes 调用更多外部工具和服务。

### 13.1 两类 MCP 服务器

| 类型 | 说明 | 适合场景 |
| --- | --- | --- |
| 本地 MCP 服务器 | 运行在本机或服务器上 | 文件系统、数据库、本地工具 |
| HTTP MCP 服务器 | 远程服务提供接口 | 云服务、团队共享服务 |

### 13.2 配置步骤

一般流程：

1. 编辑 Hermes 配置文件。
2. 添加 MCP server 配置。
3. 准备所需 token 或环境变量。
4. 使用 Hermes 验证工具是否可用。

### 13.3 常见 MCP 服务器

| MCP 服务器 | 功能 | 安装命令 |
| --- | --- | --- |
| `server-github` | GitHub 仓库操作 | `npx @modelcontextprotocol/server-github` |
| `server-postgres` | PostgreSQL 查询 | `npx @modelcontextprotocol/server-postgres` |
| `server-sqlite` | SQLite 操作 | `npx @modelcontextprotocol/server-sqlite` |
| `server-filesystem` | 文件系统操作 | `npx @modelcontextprotocol/server-filesystem` |
| `server-brave-search` | Brave 搜索 | `npx @modelcontextprotocol/server-brave-search` |
| `playwright-mcp` | 浏览器自动化 | `npx @playwright/mcp@latest` |

## 14. 自动化与定时任务

Hermes 支持自然语言创建定时任务，也支持从独立 CLI 管理。

### 14.1 调度格式

常见格式：

- 相对延迟：例如“30 分钟后提醒我”。
- 间隔重复：例如“每 2 小时检查一次”。
- Cron 表达式：适合精确周期任务。

### 14.2 BlogWatcher 示例

BlogWatcher 用于监控博客和 RSS/Atom 订阅源更新。

它可以帮助用户：

- 管理订阅源。
- 扫描更新。
- 标记文章状态。
- 持续跟踪关注的博客内容。

## 15. Web Dashboard

Hermes Agent Web Dashboard 是一个浏览器管理界面。

它适合用来：

- 管理 Hermes 安装。
- 配置设置。
- 管理 API 密钥。
- 查看和监控会话。
- 避免手动编辑 YAML 文件。

启动：

```bash
hermes dashboard
```

常见选项：

```bash
hermes dashboard --no-open
```

## 16. 高级配置

### 16.1 Camofox 防爬浏览器

Camofox 可用于更稳健的网页浏览、抓取和自动化场景。

适合任务：

- 搜索资料。
- 打开复杂网页。
- 抓取网页内容。
- 需要浏览器环境的自动化。

### 16.2 Auxiliary 副驾模型路由

Auxiliary 是 Hermes 的辅助模型路由中心。

设计理念：

- 主模型专注复杂推理。
- 辅助模型承担便宜、专用、重复的任务。
- 降低成本，提高效率。

常见辅助模型任务：

| 辅助模型任务 | 用途 |
| --- | --- |
| `vision` | 截图、验证码、图片分析 |
| `web_extract` | 网页内容抓取与提炼 |
| `compression` | 上下文压缩摘要，节省 token |
| `session_search` | 历史会话搜索与摘要 |
| `approval` | 高危命令审批决策 |
| `skills_hub` | 技能市场搜索与安装 |
| `mcp` | MCP 服务调用辅助 |
| `flush_memories` | 记忆系统清理与重组 |

## 17. Hooks 与审计

Hermes 可以通过 Hooks 或插件系统扩展生命周期行为。

常见用途：

- 记录终端命令。
- 审计高风险操作。
- 在任务开始或结束时执行检查。
- 将重要操作写入日志。

建议把高风险命令审计作为长期配置：

- 删除文件。
- 修改系统配置。
- 写入生产环境。
- 推送代码或发布版本。
- 暴露 token 或隐私数据。

## 18. Docker 沙箱

Docker 沙箱用于隔离高风险或实验性任务。

适合场景：

- 执行不可信代码。
- 运行有副作用的命令。
- 测试安装脚本。
- 让 worker agent 在隔离环境里探索。

基本思路：

1. 创建使用 Docker 沙箱的 worker profile。
2. 给 worker 配置较便宜模型。
3. 将高风险任务交给 sandbox worker。
4. 验证沙箱不会破坏宿主机环境。

## 19. 多 Agent 模式

Hermes 支持多 Agent 工作模式。

常见形态：

- 主 Agent：负责理解用户目标、拆解任务、汇总结果。
- Worker Agent：负责独立执行子任务。
- Sandbox Agent：在隔离环境里尝试高风险操作。
- Messaging Agent：通过消息应用接入日常任务。

多 Agent 的价值：

- 并行探索。
- 隔离风险。
- 将复杂任务拆成多个专业角色。
- 减少主 Agent 上下文负担。

## 20. 备份体系

Hermes 的长期价值在于配置、记忆和技能沉淀，因此需要备份。

建议备份三类内容：

| 类型 | 内容 |
| --- | --- |
| 核心配置 | `~/.hermes/config.yaml`、`~/.hermes/.env` |
| 记忆与状态 | `~/.hermes/state.db`、Memory 文件 |
| Skills | `~/.hermes/skills/` |

建议策略：

- 定期本地备份。
- 重要配置加入私有仓库或加密同步。
- 密钥文件单独处理，不要明文提交。
- 重大升级前先备份。

## 21. 使用建议

### 21.1 适合 Hermes 的任务

- 长期项目管理。
- 自动化工作流沉淀。
- 多工具组合任务。
- 消息入口触发的日常任务。
- 需要跨会话记忆的个人助理场景。
- 需要终端、浏览器、文件系统协同的任务。

### 21.2 不适合直接交给 Hermes 的任务

- 未经授权的生产环境操作。
- 涉及高敏感数据的外部调用。
- 无审计机制的删除或覆盖操作。
- 需要严格人工判断的法律、医疗、金融决策。

### 21.3 推荐落地路径

1. 先本地安装并完成基础配置。
2. 连接一个低风险消息入口。
3. 明确授权策略和群聊策略。
4. 使用 SOUL.md 固化长期偏好。
5. 逐步开放工具权限。
6. 将重复任务沉淀成 Skills。
7. 配置 MCP、Hooks、Dashboard。
8. 对高风险任务使用 Docker 沙箱和 worker profile。
9. 建立备份体系。

## 22. 八大亮点总结

| # | 亮点 | 说明 |
| --- | --- | --- |
| 1 | 智能授权 | 自动识别高危指令，说明意图后请求授权 |
| 2 | 会话感知 | 通过历史会话搜索理解上下文 |
| 3 | 多模型路由 | Auxiliary 可为不同任务分配独立模型 |
| 4 | 配置解耦 | 密钥与配置分离，YAML 修改直观 |
| 5 | 工具透明 | 消息或终端界面可展示 tool 调用过程 |
| 6 | 多 Profile | 可区分主力、沙箱、消息入口等配置 |
| 7 | 自动技能沉淀 | 将高价值流程总结成可复用 Skill |
| 8 | 消息不丢失 | 通过会话存储和搜索降低上下文丢失风险 |

## 23. 快速命令索引

```bash
# 安装
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 启动聊天
hermes

# 启动消息网关
hermes gateway

# 重新配置
hermes setup
hermes setup model
hermes setup gateway
hermes setup tools

# 查看配置
hermes config
hermes config edit

# 健康检查
hermes doctor

# 启动 Dashboard
hermes dashboard

# 查看 Skills
hermes skills list
```

## 24. 个人理解

Hermes Agent 的价值不只是“能调用工具”，而是把工具调用、长期记忆、消息入口、技能沉淀和多模型路由组合成一个持续运行的个人智能体系统。

如果只把它当成聊天机器人，会低估它的能力；如果一上来就给它过高权限，又容易带来风险。更合理的方式是从低风险任务开始，把常用流程逐步变成 Skills，再通过 SOUL.md、Memory、MCP 和 Hooks 建立稳定边界。

最终目标不是让 Agent 一次性完成所有任务，而是让它越来越理解你的工作方式，并把重复劳动变成可复用能力。
