# Reasoning Bridge

[中文](#中文) · [English](#english)

## 中文

Reasoning Bridge 让 Codex 把一个开发问题交给 ChatGPT 网页端调研或判断，再根据回答继续工作。

它适合用在架构选择、方案比较、外部调研、长期规划，以及普通调试无法解释的困难问题。发送给 ChatGPT 的内容会包含项目背景、现有证据、已经尝试过的办法和需要回答的问题。

### 使用方法

调用 `$reasoning-bridge`，然后直接描述问题：

```text
$reasoning-bridge
比较这三个训练方案，重点考虑数据成本、扩展到多机训练的难度，以及两周内能否完成。使用 xhigh。
```

Reasoning Bridge 会收集当前任务中的必要信息，在已登录的 ChatGPT 网页会话中提问，并把回答带回当前任务。

### 配置

#### `reasoning_level`

选择 ChatGPT 网页端使用的推理档位。

| 值 | 效果 |
| --- | --- |
| `pro` | 使用 Pro 模式 |
| `high` | 使用 high 档位 |
| `xhigh` | 使用 xhigh 档位 |
| 不指定 | 保留当前网页会话已选择的档位 |

一次只能选择一个档位。如果指定的档位在当前网页中不可用，请求不会发送。

#### `prepare`

总结当前进度，并生成一份此刻可以发送给顾问的完整请求；不发送消息。

```text
$reasoning-bridge
总结到目前为止的进度，只准备请求。判断这次依赖升级是否值得做，使用 high，不要发送。
```

#### `code_context`

控制是否把代码作为附件发给网页顾问。

| 值 | 效果 |
| --- | --- |
| `none` | 默认。不上传文件，只在请求中引用必要的短代码片段 |
| `files` | 上传少量关键源码或配置文件 |
| `bundle` | 生成并上传一个只包含相关代码的干净最小包 |

只有明确选择 `files` 或 `bundle` 时才会上传代码。附件不会包含凭据、环境文件、个人信息、数据集、日志、缓存、构建产物、模型权重或无关代码。
如果当前浏览器不支持文件上传，插件会停在上传前并保留已准备好的附件，等待你手动附加。

```text
$reasoning-bridge
用 xhigh 判断这次跨模块重构是否合理。code_context 使用 files，附上入口文件、接口定义和两个相关实现。
```

### 更多示例

使用 Pro 做一次外部调研：

```text
$reasoning-bridge
用 Pro 调研目前可用的开源实现，比较许可证、维护状态和迁移成本，然后给出建议。
```

重新判断一个困难问题：

```text
$reasoning-bridge
这个 bug 已经尝试过三种修复，但现象仍然解释不通。用 xhigh 检查我们是不是从一开始就采用了错误的假设。
```

继续之前的讨论：

```text
$reasoning-bridge
把刚得到的新实验结果补充给之前的顾问，再判断原方案是否还成立。
```

## English

Reasoning Bridge lets Codex ask a ChatGPT web chat to research or assess a development problem, then continue working with the answer.

It is useful for architecture choices, comparing approaches, external research, long-term planning, and difficult problems that ordinary debugging has not explained. The request includes the project background, available evidence, previous attempts, and the questions that need an answer.

### Usage

Invoke `$reasoning-bridge` and describe the problem:

```text
$reasoning-bridge
Compare these three training plans. Focus on data cost, the difficulty of scaling to multiple machines, and what can be completed in two weeks. Use xhigh.
```

Reasoning Bridge gathers the necessary context from the current task, asks the question in the signed-in ChatGPT web session, and brings the answer back.

### Configuration

#### `reasoning_level`

Select the reasoning level used in the ChatGPT web chat.

| Value | Effect |
| --- | --- |
| `pro` | Use Pro mode |
| `high` | Use the high level |
| `xhigh` | Use the xhigh level |
| Omitted | Keep the level currently selected in the web chat |

Choose one level per request. If the requested level is unavailable in the current web UI, the request is not sent.

#### `prepare`

Summarize the progress so far and prepare the complete request that could be sent to the advisor; do not send it.

```text
$reasoning-bridge
Summarize the progress so far and prepare the request only. Decide whether this dependency upgrade is worth doing. Use high and do not send it.
```

#### `code_context`

Control whether code is uploaded as context for the web advisor.

| Value | Effect |
| --- | --- |
| `none` | Default. Upload no files and quote only necessary short excerpts |
| `files` | Upload a small set of key source or configuration files |
| `bundle` | Build and upload a sanitized minimal package containing only relevant code |

Code is uploaded only when `files` or `bundle` is explicitly selected. Attachments exclude credentials, environment files, personal information, datasets, logs, caches, build outputs, model weights, and unrelated code.
If the connected browser cannot upload files, the bridge stops before upload and keeps the prepared attachment for you to add manually.

```text
$reasoning-bridge
Use xhigh to assess this cross-module refactor. Set code_context to files and attach the entry point, interface definition, and the two relevant implementations.
```

### More examples

Research available implementations with Pro:

```text
$reasoning-bridge
Use Pro to research the available open-source implementations. Compare their licenses, maintenance status, and migration cost, then recommend one.
```

Reconsider a difficult problem:

```text
$reasoning-bridge
We have tried three fixes for this bug, but the behavior still does not make sense. Use xhigh to check whether our original assumption was wrong.
```

Continue an earlier discussion:

```text
$reasoning-bridge
Add the new experiment results to the previous advisor conversation and decide whether the original plan still holds.
```

## Installation

For local use, copy `skills/reasoning-bridge` to `~/.codex/skills/`. To use the
full plugin package, install it from a configured Codex marketplace.
