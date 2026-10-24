---
type: 学习笔记
course: 大模型全栈
order: 55
stage: Agent 与协作
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/54-工具权限、审计与代码执行边界|54-工具权限、审计与代码执行边界]] · 下一篇：[[大模型全栈/56-Context Engineering 与 Skill|56-Context Engineering 与 Skill]]

> [!abstract] 学习目标
> 理解协议如何把工具服务与调用方解耦。

## 核心理解

MCP 用统一协议描述并调用外部能力。Host 承载用户交互与模型流程，Client 负责连接 Server，Server 暴露工具等能力；它不是一个负责自动规划的语言模型。

课堂用 FastMCP 注册工具，再以 stdio 子进程连接。Client 先初始化，列出工具，再按名称和参数调用。天气服务器查询地理位置与气象接口，文件服务器在限定根目录内提供列目录、读取与写入。

stdio 的标准输出用于协议通信，普通调试文字若混入可能破坏消息解析；日志应使用合适的输出通道。客户端启动路径还决定实际运行哪个 Python 和服务器脚本。

MCP 统一接口，并不自动解决权限、数据可靠性或工具选择。应用仍要判断该调用什么，并处理远程错误与结果类型。

## 课堂代码怎么读

分别按客户端与服务器读，不要把它们拼为同一个脚本。比较 StdioServerParameters、ClientSession、list_tools、call_tool 与 `@mcp.tool()`；文件例子重点看 safe_path 的解析和越界检查。

> [!warning] 易错点与资料边界
> 原路径和解释器需要按自己的目录配置；天气结果是外部接口返回，不是模型知识。文件服务可写入内容，学习时要清楚允许根目录与覆盖行为。

## 复盘练习

为什么有 MCP Server 还需要 Agent 或业务程序？

> [!question]- 参考思路
> Server 只是提供能力和协议入口；谁决定用户目标、选择工具、组合结果与结束流程，仍由 Host 中的业务逻辑或 Agent 负责。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 下024 %%

> [!quote]- 大模型全栈（下）.md · 天气服务器
> 来源：原笔记第 1170–1171 行。
>
> **天气服务器**
>

%% source-id: 下025 %%

> [!quote]- 大模型全栈（下）.md · 客户端
> 来源：原笔记第 1172–1338 行。
>
> **客户端**
>
> ```python
> import asyncio
> import sys
> from pathlib import Path
>
> from mcp.client.stdio import stdio_client, StdioServerParameters
> from mcp.client.session import ClientSession
>
> SERVER_PYTHON = sys.executable
> SERVER_SCRIPT = str(Path(__file__).resolve().parent / "02_weather_server.py")
>
> def text_of(result):
>     """从 CallToolResult 里把所有文本块拼成字符串"""
>     return "\n".join(
>         b.text for b in result.content if getattr(b, "type", None) == "text"
>     )
>
> async def main():
>     params = StdioServerParameters(command=SERVER_PYTHON, args=[SERVER_SCRIPT])
>     async with stdio_client(params) as (read, write):
>         async with ClientSession(read, write) as session:
>             await session.initialize()
>
>             # 列出 server 提供的工具
>             print("可用工具:", [t.name for t in (await session.list_tools()).tools])
>
>             # 上海当前天气（中文城市名）
>             print(
>                 "\n[get_current_weather 上海] ->\n"
>                 + text_of(await session.call_tool("get_current_weather", {"city": "上海"}))
>             )
>
>             # 北京未来3天预报
>             print(
>                 "\n[get_forecast Beijing 3天] ->\n"
>                 + text_of(await session.call_tool("get_forecast", {"city": "Beijing", "days": 3}))
>             )
>
>             # 不存在的城市，验证错误处理
>             print(
>                 "\n[get_current_weather 不存在的城市] ->\n"
>                 + text_of(await session.call_tool("get_current_weather", {"city": "不存在的城市xyz"}))
>             )
>
> if __name__ == "__main__":
>     asyncio.run(main())
> ```
>
> **服务器**
>
> ```python
> import requests
> from mcp.server.fastmcp import FastMCP
>
> GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
> FC_URL = "https://api.open-meteo.com/v1/forecast"
>
> # WMO 天气代码 -> 中文描述
> WMO = {
>     0: "晴", 1: "大致晴朗", 2: "部分多云", 3: "阴",
>     45: "雾", 48: "雾凇",
>     51: "小毛毛雨", 53: "毛毛雨", 55: "大毛毛雨",
>     56: "冻毛毛雨", 57: "强冻毛毛雨",
>     61: "小雨", 63: "中雨", 65: "大雨",
>     66: "冻雨", 67: "强冻雨",
>     71: "小雪", 73: "中雪", 75: "大雪", 77: "雪粒",
>     80: "阵雨", 81: "阵雨", 82: "强阵雨",
>     85: "阵雪", 86: "强阵雪",
>     95: "雷雨", 96: "雷雨伴小冰雹", 99: "雷雨伴大冰雹",
> }
>
> mcp = FastMCP("weather-service")
>
> def geocode(city):
>     """城市名 -> (纬度, 经度, 显示名)；找不到返回 None。"""
>     resp = requests.get(
>         GEO_URL,
>         params={"name": city, "count": 1, "language": "zh", "format": "json"},
>         timeout=10,
>     )
>     resp.raise_for_status()
>     results = resp.json().get("results")
>     if not results:
>         return None
>     r = results[0]
>     return r["latitude"], r["longitude"], r.get("name", city)
>
> def wmo(code):
>     return WMO.get(int(code), f"未知天气(代码{code})")
>
> @mcp.tool()
> def get_current_weather(city, units="metric"):
>     """查询指定城市的当前天气（免费接口，无需 API Key）。
>     Args:
>         city: 城市名称，支持中英文（如 "Beijing"、"上海"）。
>         units: 温度单位，metric 为摄氏度，imperial 为华氏度。默认 metric。
>     """
>     try:
>         geo = geocode(city)
>         if not geo:
>             return f"错误：找不到城市 '{city}'，请检查拼写"
>         lat, lon, name = geo
>         temp_unit = "°C" if units == "metric" else "°F"
>         params = {
>             "latitude": lat,
>             "longitude": lon,
>             "current": "temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m",
>             "temperature_unit": "celsius" if units == "metric" else "fahrenheit",
>             "wind_speed_unit": "ms" if units == "metric" else "mph",
>             "timezone": "auto",
>         }
>         resp = requests.get(FC_URL, params=params, timeout=10)
>         resp.raise_for_status()
>         cur = resp.json()["current"]
>         return (
>             f"城市：{name}\n"
>             f"天气：{wmo(cur['weather_code'])}\n"
>             f"温度：{cur['temperature_2m']}{temp_unit}（体感 {cur['apparent_temperature']}{temp_unit}）\n"
>             f"湿度：{cur['relative_humidity_2m']}%\n"
>             f"风速：{cur['wind_speed_10m']} {'m/s' if units == 'metric' else 'mph'}"
>         )
>     except requests.exceptions.Timeout:
>         return "错误：请求超时，请检查网络连接"
>     except requests.exceptions.RequestException as e:
>         return f"请求失败：{e}"
>
> @mcp.tool()
> def get_forecast(city, days= 5):
>     """查询指定城市未来几天的天气预报（免费接口，无需 API Key）。
>
>     Args:
>         city: 城市名称。
>         days: 预报天数，最大 7 天。默认 5。
>     """
>     days = min(max(days, 1), 7)
>     try:
>         geo = geocode(city)
>         if not geo:
>             return f"错误：找不到城市 '{city}'，请检查拼写"
>         lat, lon, name = geo
>         params = {
>             "latitude": lat,
>             "longitude": lon,
>             "daily": "weather_code,temperature_2m_max,temperature_2m_min",
>             "forecast_days": days,
>             "timezone": "auto",
>         }
>         resp = requests.get(FC_URL, params=params, timeout=10)
>         resp.raise_for_status()
>         d = resp.json()["daily"]
>         lines = [f"{name} 未来 {days} 天预报："]
>         for date, code, tmax, tmin in zip(
>                 d["time"], d["weather_code"], d["temperature_2m_max"], d["temperature_2m_min"]
>         ):
>             lines.append(f"{date}：{wmo(code)}，{tmin:.0f}~{tmax:.0f}°C")
>         return "\n".join(lines)
>     except requests.exceptions.Timeout:
>         return "错误：请求超时，请检查网络连接"
>     except requests.exceptions.RequestException as e:
>         return f"查询失败：{e}"
>
> if __name__ == "__main__":
>     mcp.run()
> ```
>

%% source-id: 下026 %%

> [!quote]- 大模型全栈（下）.md · 文件服务器
> 来源：原笔记第 1339–1460 行。
>
> **文件服务器**
>
> **客户端**
>
> ```python
> """
> 客户端
> """
> import asyncio
> import sys
> from pathlib import Path
> from mcp.client.stdio import stdio_client, StdioServerParameters
> from mcp.client.session import ClientSession
>
> SERVER_PYTHON = sys.executable
> SERVER_SCRIPT = str(Path(__file__).resolve().parent / "01_file_server.py")
>
> def text_of(result):
>     return "\n".join(
>         b.text for b in result.content if getattr(b, "type", None) == "text"
>     )
>
> async def main():
>     params = StdioServerParameters(command=SERVER_PYTHON, args=[SERVER_SCRIPT])
>     async with stdio_client(params) as (read, write):
>         async with ClientSession(read, write) as session:
>             await  session.initialize()
>
>             tools = await session.list_tools()
>             print("可用工具:", [t.name for t in tools.tools])
>
>             wr = await session.call_tool(
>                 "write_file",
>                 {
>                     "path": "demo/hello.txt",
>                     "content": "你好, MCP"
>                 }
>             )
>             print("\n[write_file]- ->", text_of(wr))
>
>             rd = await session.call_tool("read_file", {"path": "demo/hello.txt"})
>             print("\n[read_file]- ->", text_of(rd))
>
>             ls = await session.call_tool("list_dir", {"path": "."})
>             print("\n[list_dir]- ->", text_of(ls))
>
> asyncio.run(main())
> ```
>
> **服务器**
>
> ```python
> """
> 文件MCP服务器
> 如果mcp报错 需要单独安装 pip install mcp
> """
> import pathlib
> from mcp.server.fastmcp import FastMCP
>
> ALLOW_ROOT = (pathlib.Path(__file__).resolve().parent / "workspace").resolve()
>
> mcp = FastMCP("local-filesystem")
>
> # 路径校验
> def safe_path(user_path):
>     path = pathlib.Path(user_path)
>     if not path.is_absolute():
>         path = ALLOW_ROOT / path
>
>     resolved = path.resolve()
>
>     if not str(resolved).startswith(str(ALLOW_ROOT)):
>         raise PermissionError(f"路径越界! 不允许的工作路径")
>     return resolved
>
> # MCP工具函数
> @mcp.tool()
> def list_dir(path="."):
>     try:
>         target = safe_path(path)
>         if not target.is_dir():
>             return f"{target} is not a directory"
>         entries = sorted(
>             target.iterdir(),
>             key=lambda x: (not x.is_dir(), x.name.lower())
>         )
>         # 遍历
>         lines = []
>         for entry in entries:
>             kind = "[DIR]" if entry.is_dir() else "[FILE]"
>             size = f"{entry.stat().st_size}B" if entry.is_file() else " -"
>             lines.append(f"{kind} {size} {entry.name}")
>
>         return "\n".join(lines) if lines else "目录为空"
>     except Exception as e:
>         return f"操作失败:{e}"
>
> @mcp.tool()
> def read_file(path):
>     try:
>         target = safe_path(path)
>         if not target.is_file():
>             return f"{target} is not a file"
>         content = target.read_text(encoding="utf-8", errors="replace")
>         return content
>     except Exception as e:
>         return f"读取失败:{e}"
>
> @mcp.tool()
> def write_file(path, content):
>     try:
>         target = safe_path(path)
>         target.parent.mkdir(parents=True, exist_ok=True)
>         target.write_text(content, encoding="utf-8")
>         return f"已经写入文件~"
>     except Exception as e:
>         return f"写入失败:{e}"
>
> if __name__ == "__main__":
>     mcp.run()
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/12.高阶Agent.pdf#page=1|12.高阶Agent.pdf · 第 1–9 页]]
- 关联知识：[[大模型全栈/42-工具调用：Schema、执行与结果回传|42-工具调用：Schema、执行与结果回传]]、[[大模型全栈/54-工具权限、审计与代码执行边界|54-工具权限、审计与代码执行边界]]、[[大模型全栈/56-Context Engineering 与 Skill|56-Context Engineering 与 Skill]]。

> [!example]- 本地讲义页预览
> ![[大模型全栈/资料/PDF/12.高阶Agent.pdf#page=4]]
