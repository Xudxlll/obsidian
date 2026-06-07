按“真实解释器”去重后，你电脑里我目前看到 **5 个 Python**：

1. `/opt/anaconda3/bin/python3.13`  
   Python `3.13.9`，Anaconda 的，当前 `python` / `python3` 优先用这个。

2. `/Library/Frameworks/Python.framework/Versions/3.9/bin/python3.9`  
   Python `3.9.13`，官网/框架版安装。

3. `/usr/bin/python3`  
   Python `3.9.6`，macOS 系统自带/命令行工具里的。

4. `/Users/xuji/.local/share/uv/python/cpython-3.11.15-macos-aarch64-none/bin/python3.11`  
   Python `3.11.15`，`uv` 安装的；Hermes 的虚拟环境也指向它，所以不算另一个真实 Python。

5. `/Users/xuji/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3.12`  
   Python `3.12.13`，Codex runtime 缓存里的。

所以简单说：**系统里至少 5 个真实 Python 解释器**。当前终端默认最先用的是 **Anaconda Python 3.13.9**。