---
title: Vibe-Trading：你的个人交易智能体
url: https://github.com/HKUDS/Vibe-Trading/tree/main
日期: 2026-05-31
tags:
  - github
  - agent
  - AI知识
---

# Vibe-Trading 指南
## 这是什么

Vibe-Trading 是一个面向交易研究、行情分析、策略回测和多 Agent 协作的金融研究 Agent 平台。它既可以独立作为 CLI/Web 应用使用，也可以作为 MCP server 接入 Codex、Claude Desktop、Cursor 等智能体，让这些智能体调用它的行情、回测、文档读取和研究工具。

简单理解：

```text
Vibe-Trading 本体 = 金融研究 Agent / 回测平台
Vibe-Trading MCP = 给 Codex 等智能体使用的金融工具箱
Codex = 主控智能体，负责对话、代码分析、调工具和总结结果
```

## 本机安装位置

当前本地安装目录：

```bash
/Users/xuji/Documents/Vibe-Trading
```

核心文件和目录：

```text
/Users/xuji/Documents/Vibe-Trading/.venv                  Python 虚拟环境
/Users/xuji/Documents/Vibe-Trading/frontend               Web 前端源码
/Users/xuji/Documents/Vibe-Trading/agent/.env             Web/API 使用的配置
/Users/xuji/.vibe-trading/.env                            CLI 优先读取的配置
/Users/xuji/.codex/config.toml                            Codex MCP 配置
```

## 当前模型配置

当前 Vibe-Trading 本地和 MCP 使用的是 OpenAI Codex OAuth provider：

```bash
LANGCHAIN_PROVIDER=openai-codex
LANGCHAIN_MODEL_NAME=openai-codex/gpt-5.3-codex
OPENAI_CODEX_BASE_URL=https://chatgpt.com/backend-api/codex/responses
```

这个配置不使用 `OPENAI_API_KEY`，而是使用 ChatGPT/Codex OAuth 登录状态。

==ps：本地安装的在前端页面可以自由选择模型==

注意区分：

```text
Codex App 自己的模型 = 负责和你对话、写代码、决定调用工具
Vibe-Trading 的模型 = Vibe-Trading 内部 agent / swarm 任务需要推理时使用
```

普通 MCP 工具，例如获取行情、期权计算、读取文件、运行回测，不一定会用到 Vibe-Trading 的模型。只有当 Vibe-Trading 自己执行复杂研究、swarm、多 agent 报告等任务时，才会调用它配置的 LLM。

## Codex MCP 接入状态

Codex 中已配置 MCP server：

```toml
[mcp_servers.vibe_trading]
command = "/Users/xuji/Documents/Vibe-Trading/.venv/bin/vibe-trading-mcp"
startup_timeout_sec = 120
```

环境变量：

```toml
[mcp_servers.vibe_trading.env]
LANGCHAIN_PROVIDER = "openai-codex"
LANGCHAIN_MODEL_NAME = "openai-codex/gpt-5.3-codex"
OPENAI_CODEX_BASE_URL = "https://chatgpt.com/backend-api/codex/responses"
```

验证时 MCP 可以正常启动，并识别到 27 个工具。

当前会话如果没有出现 Vibe-Trading 工具，重启 Codex 或新开一个 Codex 会话即可加载最新 MCP 配置。

## 如何在 Codex 中使用 MCP

直接用自然语言要求 Codex 调用 Vibe-Trading 即可，例如：

```text
用 vibe_trading MCP 获取 BTC-USDT 最近 30 天日线数据，并总结走势。
```

```text
用 Vibe-Trading 回测 BTC-USDT 的 20/50 均线策略。
```

```text
用 Vibe-Trading 分析 AAPL.US 最近一年的行情，并给出技术面总结。
```

```text
用 vibe_trading MCP 读取这份交易流水，并分析我的交易行为。
```

Codex 会作为主控智能体：理解任务、决定调用哪些 MCP 工具、读取结果、再整理成你能看的结论。

## 常用 MCP 能力

常见工具包括：

```text
get_market_data        获取股票、港股、美股、加密货币等行情数据
backtest               运行策略回测
factor_analysis        因子分析
analyze_options        Black-Scholes 期权价格和 Greeks 计算
pattern_recognition    技术形态识别
web_search             金融资料搜索
read_url               读取网页内容
read_document          读取 PDF 文档
read_file              读取本地文件
write_file             写入回测相关文件
analyze_trade_journal  分析交易流水
extract_shadow_strategy 提取 Shadow Account 策略画像
run_shadow_backtest    运行 Shadow Account 回测
render_shadow_report   生成 Shadow Account 报告
list_swarm_presets     查看多 Agent 团队预设
run_swarm              运行多 Agent 研究团队
get_swarm_status       查看 swarm 运行状态
get_run_result         获取 swarm 结果
```

## 如何启动 Web UI

进入项目目录：

```bash
cd /Users/xuji/Documents/Vibe-Trading
source .venv/bin/activate
```

启动后端和 Web：

```bash
vibe-trading serve --port 8899
```

浏览器打开：

```text
http://localhost:8899
```

API 文档地址：

```text
http://localhost:8899/docs
```

## 前端开发模式

如果要修改前端源码，使用 Vite 开发服务器：

```bash
cd /Users/xuji/Documents/Vibe-Trading
source .venv/bin/activate
vibe-trading serve --port 8899
```

另开一个终端：

```bash
cd /Users/xuji/Documents/Vibe-Trading/frontend
npm run dev
```

打开：

```text
http://localhost:5899
```

前端开发服务器会把 API 请求代理到 `localhost:8899`。

## CLI 用法

进入项目目录并激活环境：

```bash
cd /Users/xuji/Documents/Vibe-Trading
source .venv/bin/activate
```

查看版本：

```bash
vibe-trading --version
```

直接运行一个研究任务：

```bash
vibe-trading -p "分析 BTC-USDT 最近 6 个月走势，并给出一个均线回测思路"
```

启动交互式 TUI：

```bash
vibe-trading
```

查看可用 swarm preset：

```bash
vibe-trading --swarm-presets
```

## MCP 手动启动方式

一般不需要手动启动，Codex 会自动按配置拉起 MCP server。

如果要手动测试：

```bash
cd /Users/xuji/Documents/Vibe-Trading
source .venv/bin/activate
vibe-trading-mcp
```

stdio 模式用于 MCP 客户端自动通信，手动运行时终端看起来可能像是在等待输入，这是正常的。

SSE 模式：

```bash
vibe-trading-mcp --transport sse --port 8001
```

## 数据源说明

很多行情能力可以不配置行情 API key：

```text
yfinance   港股 / 美股
OKX        加密货币
mootdx     A 股免 token fallback
AKShare    A 股、美股、港股、期货、外汇等兜底
```

Tushare token 是可选项。如果需要更完整或更稳定的 A 股数据，可以在配置中加入：

```bash
TUSHARE_TOKEN=你的 token
```

可写入：

```bash
/Users/xuji/.vibe-trading/.env
/Users/xuji/Documents/Vibe-Trading/agent/.env
```

## 三种使用入口的区别

```text
Web UI
适合人眼浏览、点页面、看图表、管理设置。

CLI
适合开发、调试、脚本化运行、快速执行自然语言任务。

MCP
适合让 Codex/Claude/Cursor 等主智能体调用 Vibe-Trading 的金融工具。
```

推荐日常工作流：

```text
简单行情 / 回测 / 文件分析：直接在 Codex 里说“用 Vibe-Trading MCP ...”
需要看图表或管理设置：启动 Web UI
需要改源码或调试工具：进入 /Users/xuji/Documents/Vibe-Trading 用 CLI 和编辑器
```

## 什么时候会用到模型

不会总是用模型。

不太依赖模型的任务：

```text
拉行情
算期权 Greeks
读文件
跑已有策略回测
列工具 / 列技能
```

会依赖模型的任务：

```text
自然语言研究分析
复杂报告生成
多 Agent swarm
让 Vibe-Trading 自己规划并调用内部工具
```

因此，Vibe-Trading MCP 的模型配置主要是给它内部 agent 用的，不是每次工具调用都会消耗 LLM。

## 维护命令

更新项目代码：

```bash
cd /Users/xuji/Documents/Vibe-Trading
git pull
```

更新 Python 依赖：

```bash
cd /Users/xuji/Documents/Vibe-Trading
uv pip install --python .venv/bin/python -e .
```

更新前端依赖：

```bash
cd /Users/xuji/Documents/Vibe-Trading/frontend
npm install
```

重新构建前端：

```bash
cd /Users/xuji/Documents/Vibe-Trading/frontend
npm run build
```

检查 Codex MCP 配置：

```bash
/Applications/Codex.app/Contents/Resources/codex mcp list
```

## 注意事项

1. 修改 `~/.codex/config.toml` 后，通常需要重启 Codex 或新开会话，MCP 工具才会重新加载。
2. 如果 Web UI 启不来，先确认端口 `8899` 没被占用。
3. 如果 Vibe-Trading agent 报模型未登录，运行：

```bash
cd /Users/xuji/Documents/Vibe-Trading
source .venv/bin/activate
vibe-trading provider login openai-codex
```

4. 如果只是行情、回测、计算类任务，通常不需要 LLM API key。
5. 实盘交易、经纪商授权、自动下单等能力需要额外谨慎配置，不建议在未充分理解风险前开启。

## 快速测试句

在 Codex 新会话中可以这样测试：

```text
用 vibe_trading MCP 获取 BTC-USDT 最近 30 天日线数据，并总结走势。
```

或者：

```text
用 vibe_trading MCP 对 AAPL.US 最近一年做一个简单技术面分析。
```

如果工具正常，Codex 会自动调用 Vibe-Trading MCP，并返回行情数据摘要或分析结果。
