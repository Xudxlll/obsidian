---
type: 原始源码副本
---

来源：`pyproject.toml`。未修改原内容。

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "Myagents"
version = "1.4.0"
description = "multi-agent AI system"
readme = "README.md"
requires-python = ">=3.10,<3.14"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "python-multipart>=0.0.6",
    "motor>=3.3.0",
    "pymongo>=4.0.0",
    "redis>=5.0.0",
    "PyJWT>=2.0.0",
    "bcrypt>=4.0.0",
    "apscheduler>=3.10.0",
    "aiofiles>=0.8.0",
    "httpx>=0.24.0",
    "sse-starlette>=1.0.0",
    "concurrent-log-handler>=0.9.24",
    "akshare>=1.18.0",
    "baostock>=0.8.8",
    "finnhub-python>=2.4.23",
    "tushare>=1.4.21",
    "yfinance>=0.2.63",
    "chromadb>=1.0.12",
    "dashscope>=1.20.0",
    "anthropic>=0.40.0",
    "mcp>=2.0.0,<3.0.0",
    "openai>=1.0.0,<2.0.0",
    "pandas>=2.3.0",
    "curl-cffi>=0.6.0",
    "requests>=2.32.4",
    "markdown>=3.4.0",
    "pypandoc>=1.11",
    "python-docx>=0.8.11",
    "pdfkit>=1.0.0",
    "psutil>=6.1.0",
    "python-dotenv>=1.0.0",
    "pytz>=2025.2",
    "rich>=14.0.0",
    "setuptools>=80.9.0",
    "toml>=0.10.2",
    "tqdm>=4.67.1",
    "typing-extensions>=4.14.0",
]

[project.optional-dependencies]
qianfan = ["qianfan>=0.4.12.3"]

[project.scripts]
zhenshabi = "scripts.examples.run_analysis:main"

[tool.setuptools.packages.find]
include = ["app*", "scripts*"]
exclude = ["tests*", "docs*", "data*", "logs*", "reports*", "results*", "eval_results*", "upstream_contribution*", "frontend*"]

[dependency-groups]
dev = [
    "httpx>=0.28.1",
    "pytest>=9.0.3",
    "pytest-asyncio>=1.3.0",
    "pytest-timeout>=2.3.1",
    "ruff>=0.15",
    "import-linter>=2.0",
]

[tool.ruff]
target-version = "py312"
line-length = 120

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "TID251"]

[tool.ruff.lint.flake8-tidy-imports.banned-api]
"app.engine.config.config_manager".msg = "config_manager 已移除；使用 app/core/config.py 配置体系"

[tool.ruff.lint.per-file-ignores]
"scripts/*" = ["E402"]
"tests/*" = ["E402", "E731", "F841"]

[tool.importlinter]
root_packages = ["app"]

[[tool.importlinter.contracts]]
name = "Routers must not import data layer internals"
type = "forbidden"
source_modules = ["app.routers"]
forbidden_modules = [
    "app.data.storage",
    "app.data.sources",
]
allow_indirect_imports = true

[[tool.importlinter.contracts]]
name = "Engine must not import data storage internals"
type = "forbidden"
source_modules = ["app.engine"]
forbidden_modules = ["app.data.storage"]
allow_indirect_imports = true

[tool.pytest.ini_options]
markers = [
    "asyncio: async test",
    "slow: slow test",
    "integration: integration test",
    "requires_db: requires real MongoDB/Redis",
    "ai: requires AI API key",
]
asyncio_mode = "auto"

```
