---
title: Codex 接入 DeepSeek：CCX + CC Switch 配置原理与排错
source_url: https://www.bilibili.com/video/BV1Xj5E65Euo/
created: 2026-06-01
tags:
  - Codex
  - DeepSeek
  - CCX
  - CC-Switch
  - bilibili
  - agent
  - AI知识
---

# Codex 接入 DeepSeek：CCX + CC Switch 配置原理与排错

> 整理来源：[[../Clippings/2026-06-01-deepseek接入codex，国内直连性价比之王！小白必学！|原视频剪辑笔记]] + 补充说明。

<iframe src="https://player.bilibili.com/player.html?aid=116549708942086&bvid=BV1Xj5E65Euo&cid=38236127856&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allow="fullscreen; picture-in-picture" allowfullscreen="true" style="height:100%;width:100%; aspect-ratio: 16 / 9;"> </iframe>

## 简介

这篇笔记的核心是：**Codex 本质上只是一个发起模型请求的客户端软件**。它并不是只能请求 OpenAI 官方模型；只要把 Codex 发出的 API 请求导向自己的代理网关，就可以把后端模型切换成 DeepSeek、Qwen 或其他兼容接口的模型。

本方案使用两个工具完成这件事：

- **CC Switch**：负责让 Codex 以为自己仍然在请求一个 OpenAI / ChatGPT 风格的 API 地址。它主要改的是 Codex 侧看到的 **Base URL** 和 **API Key**。
- **CCX**：负责真正接收请求、管理渠道，并把请求转发给 DeepSeek。它更关键的作用是处理 **请求格式兼容**：Codex 官方偏向 Responses / Codex 格式，而 DeepSeek 更适合走 OpenAI Chat Completions 风格的格式。

所以，新手最容易踩坑的地方不是“Codex 里模型名写成什么”，而是：**代理链路、API Key、Base URL、请求格式是否一致**。如果 CCX 渠道格式选错，例如选成 Codex / Responses，而不是 OpenAI Chat，就很容易出现兼容性报错。

## 核心原理

### 1. Codex 为什么可以接入 DeepSeek

Codex 的本质是一个普通桌面软件 / CLI 客户端：

1. 用户在 Codex 里输入任务；
2. Codex 通过本机网络请求模型服务；
3. 模型服务返回结果；
4. Codex 再把结果展示给用户或执行到本地文件。

因此，只要能在网络层或配置层把它的请求导向自己的网关，就可以控制它最终请求哪个模型。这个思路不只适用于 Codex，也适用于很多 CLI、API 客户端或桌面 App。

### 2. CC Switch 解决“请求到哪里去”的问题

Codex 如果直接使用 API 登录，默认会按照 OpenAI 官方的方式请求模型，也就是默认使用 OpenAI 的 Base URL 和 API Key 体系。

CC Switch 的作用，是把 Codex 侧的请求地址和密钥改成你自己的代理配置：

- Base URL 指向 CCX 提供的本地 / 代理 API 地址；
- API Key 使用 CCX 的访问密钥；
- Codex 内部原本显示什么模型名，并不是最关键的判断依据；真正打到哪个模型，取决于代理网关后面怎么转发。

换句话说，在这套链路里，Codex 发出的请求会被 CC Switch 导向 CCX，再由 CCX 转给 DeepSeek。

### 3. CCX 解决“请求格式是否兼容”的问题

模型请求不只有 Base URL 和 API Key，还有请求格式。

这里最关键：

- OpenAI 官方 Codex / Responses 格式：DeepSeek 不一定兼容；
- Qwen 等部分模型或服务可能兼容性更好；
- DeepSeek 更应该配置成 **OpenAI Chat / Chat Completions 风格**；
- 如果 CCX 里渠道类型选成 Codex / Responses，接入 DeepSeek 时大概率会报错；
- 很多“规范化 chat role”相关选项，只会出现在 OpenAI Chat 类型配置里，而不是 Codex 类型配置里。

所以，排错时要重点检查 `localhost:3000` 管理界面里的渠道配置：**服务类型不要选 Codex，要选 OpenAI Chat，并开启必要的规范化选项。**

## 配置流程

### 1. 安装基础环境

1. 打开 Node.js 官网；
2. 根据自己的系统下载对应安装包；
3. 安装时一路确认即可；
4. 再下载安装 Codex 桌面端。

视频以 Windows 为例演示，但核心逻辑在 macOS / Windows 上类似：先让 Codex 能正常打开，再配置代理链路。

### 2. 准备 CCX 和 CC Switch

下载并解压：

- CCX；
- CC Switch。

CCX 解压后一般会带有环境配置文件，里面包含访问管理后台的密钥。示例里使用过 `123456`，但实际使用时要以你本地 `.env` 或配置文件里的值为准。

### 3. 启动 CCX 并进入管理界面

1. 启动 CCX；
2. 找到它提供的管理界面地址；
3. 在浏览器打开管理地址，常见为 `localhost:3000`；
4. 输入访问密钥进入后台；
5. 可以先切换为简体中文界面，方便后续配置。

如果打不开或密码不对，优先检查 `.env` 是否存在、是否和可执行文件处在同级目录、访问密钥是否和 CC Switch / Codex 中填写的一致。

### 4. 在 CCX 中添加 DeepSeek 渠道

在 DeepSeek API 平台完成：

1. 登录 DeepSeek 开放平台；
2. 找到接口文档；
3. 复制 Base URL；
4. 创建 API Key；
5. 回到 CCX 管理界面添加渠道。

CCX 里要重点设置：

- Base URL：填写 DeepSeek 的 API 地址；
- API Key：填写 DeepSeek 平台创建的 Key；
- 服务类型：选择 **OpenAI Chat**；
- 规范化 chat role：开启；
- 不要把 DeepSeek 渠道配置成 Codex / Responses 格式。

### 5. 在 CC Switch 中添加供应商

打开 CC Switch 后：

1. 选择 ChatGPT / OpenAI 类配置；
2. 添加自定义供应商；
3. 供应商名称随便起，方便识别即可；
4. API Key 填 CCX 的访问密钥；
5. API 请求地址填 CCX 提供的 API 地址；
6. 点击获取模型列表；
7. 如果能看到 DeepSeek 相关模型，说明 CC Switch 到 CCX 的链路基本打通；
8. 根据需要开启较大的上下文窗口选项。

### 6. 重启 Codex 并测试

1. 关闭并重新打开 Codex；
2. 选择使用 API Key 登录；
3. 输入 CCX / CC Switch 对应的访问密钥；
4. 进入 Codex 后发起普通文本对话；
5. 如果能正常回复，说明 Codex 已经通过代理链路接入 DeepSeek。

如果想验证后端是不是 DeepSeek，可以用模型能力差异做判断：例如 DeepSeek 如果不支持某些多模态图片输入，那么上传图片可能会报错。这个现象可以辅助判断，但日常排错更推荐直接看 CCX 请求日志和渠道命中情况。

## 常见问题与排错

### 问题 1：`localhost:3000` 渠道格式选错

最常见错误是只填了 Base URL 和 API Key，却忽略请求格式。

排查重点：

- 不要把 DeepSeek 渠道设置成 Codex / Responses；
- 要设置成 OpenAI Chat / Chat Completions；
- 找不到“规范化 chat role”时，多半是服务类型选错了。

### 问题 2：`.env` 看不到、创建不了或不生效

macOS 访达默认隐藏以 `.` 开头的文件，所以 `.env` 看不到不代表不存在。

可在终端里检查：

```bash
ls -la
```

创建 `.env` 可以用：

```bash
touch .env
```

编辑可以用：

```bash
nano .env
```

也可以用 VS Code、Cursor 等编辑器打开目录后编辑。关键是：`.env` 要放在程序能读取到的位置，里面的访问密钥要和 CCX / CC Switch / Codex 中填写的值保持一致。

### 问题 3：默认密码或访问密钥不一致

有些包默认示例可能写 `123456`，有些文档或配置会写 `your-proxy-access-key`。

处理原则：

- 不要只记视频里的示例值；
- 以你本地 `.env` 或配置文件里实际设置的值为准；
- CCX 后台登录密码、CC Switch API Key、Codex API Key 要保持同一套链路一致；
- 如果没有自定义 `.env`，就检查程序默认值到底是什么；
- 不要把真实 DeepSeek API Key 发给别人或提交到 Git 仓库。

### 问题 4：macOS 可执行文件打不开

Mac 常见有两类芯片架构：

- Apple Silicon：M1 / M2 / M3 / M4 等，通常选择 `darwin-arm64`；
- Intel Mac：通常选择 `darwin-amd64` 或 `x64`。

如果下载错架构，可能无法运行。若文件没有执行权限，可先授权：

```bash
chmod +x ./ccx-darwin-arm64
./ccx-darwin-arm64
```

如果被 macOS 安全机制隔离，可解除 quarantine 标记：

```bash
xattr -d com.apple.quarantine /path/to/ccx-darwin-arm64
```

然后再运行。这个命令的作用是解除 macOS 对该下载文件的安全隔离，避免每次都需要到系统设置里手动放行。

## 最小可行配置检查清单

- [ ] Node.js 已安装；
- [ ] Codex 桌面端能正常打开；
- [ ] CCX 能启动；
- [ ] `localhost:3000` 管理后台能打开；
- [ ] CCX 访问密钥已确认；
- [ ] DeepSeek Base URL 已填写；
- [ ] DeepSeek API Key 已填写；
- [ ] CCX 渠道类型是 OpenAI Chat，不是 Codex / Responses；
- [ ] 规范化 chat role 已开启；
- [ ] CC Switch 的 API 地址指向 CCX；
- [ ] CC Switch 的 API Key 使用 CCX 访问密钥；
- [ ] Codex 里输入的 API Key 与 CCX / CC Switch 链路一致；
- [ ] 能获取 DeepSeek 模型列表；
- [ ] Codex 普通文本对话能成功返回。

## Skills 安装补充

视频最后还提到一个 Codex 使用技巧：可以让 Codex 帮你安装 Skills。

基本方法是：

1. 在网页上找到想要安装的 Skill 或 GitHub 仓库；
2. 复制仓库链接；
3. 把链接发给 Codex，让它根据仓库内容安装；
4. 安装完成后，后续任务触发对应场景时，Codex 会自动调用该 Skill。

例如制作 PPT 时，如果已安装对应的 presentation / PPT skill，Codex 就可以按该技能的规范生成更稳定的演示文稿。

## 一句话总结

**CC Switch 负责把 Codex 的请求导向本地代理，CCX 负责把请求按 DeepSeek 能理解的 OpenAI Chat 格式转发出去。接入失败时，优先检查 CCX 渠道格式、访问密钥、Base URL 和 `.env` 位置，而不是纠结 Codex 界面里显示的模型名。**
