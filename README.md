# Reasoning Bridge

[中文](#中文) · [English](#english)

## 中文

Reasoning Bridge 是一个给 Codex 使用的网页顾问桥接器。当一个开发问题需要查资料、比较方案，或者重新判断整体方向时，它把必要背景交给 ChatGPT 网页端，再把完整回答带回原来的 Codex 任务。

Codex 继续负责读代码、改代码、调试和验证；网页顾问负责需要更大范围信息或判断的问题。发送给网页顾问的内容会写成一段正常的工程说明，包含背景、证据、已经尝试过的办法和需要回答的问题。

### 默认行为

直接调用 `$reasoning-bridge` 并描述一个具体问题，插件会：

1. 找到或恢复这个问题对应的桥接任务；
2. 收集当前任务已经确认的事实和限制；
3. 在本地登录的 ChatGPT 网页会话中发送一次请求；
4. 把顾问的完整回答和可执行结论交回原任务。

如果只想检查请求内容而不发送，明确说“只预览”或 `preview`。

### 可选配置

#### `reasoning_level`

网页端推理档位。可用值取决于当前 ChatGPT 网页界面，例如 `pro`、`high` 或 `xhigh`。一次只能选一个。

- 指定 `pro`：网页端切换到 Pro 模式；
- 指定 `xhigh`：网页端使用 xhigh 档位；
- 不指定：保留当前网页会话已经显示的档位；
- 指定档位不可用：停止发送并报告，不自动降级。

#### `preview`

只生成请求，不联系网页顾问，也不改变执行任务。

#### 执行环境

可以在请求中说明要让哪个执行任务继续。桥接器会把回答交回发起问题的任务；它不会把网页登录信息复制到执行环境。

### 示例

```text
$reasoning-bridge
帮我比较这个训练方案的三种架构，重点看数据成本、可扩展性和两周内能否完成。用网页端 xhigh，结论交回当前任务。
```

```text
$reasoning-bridge
只预览。请判断这个依赖升级是否值得做，网页端使用 high，不要发送。
```

```text
$reasoning-bridge
这个 bug 已经尝试过三种修复仍然没有解释清楚。请用网页端 Pro 重新审视问题的整体方向，然后把建议交回原任务。
```

### 适合与不适合

适合：外部调研、架构选择、长期规划、重要前提的复核，以及普通调试无法解决的方向性问题。

不适合：简单改名、常规代码实现、已有明确答案的局部修复。此时直接让 Codex 执行更快。

## English

Reasoning Bridge connects an active Codex task to a ChatGPT web advisor when the problem needs research, architectural comparison, or a broader direction decision. It brings the complete answer back to the task that asked the question.

Codex remains responsible for reading and changing code, debugging, and validation. The web advisor handles questions that benefit from wider information or a second look at the overall direction. The request is written as a normal engineering brief with context, evidence, previous attempts, and specific questions.

### Default behavior

Invoke `$reasoning-bridge` with a concrete question. The plugin finds or resumes the bridge task, gathers the relevant facts, sends one request in the signed-in ChatGPT web session, and returns the complete answer and actionable constraints to the original task.

Say “preview only” or `preview` when you want to inspect the request without sending it.

### Options

#### `reasoning_level`

The reasoning level used by the web chat. Available values depend on the current ChatGPT UI, for example `pro`, `high`, or `xhigh`. Choose one value per request.

- `pro`: use Pro mode in the web chat;
- `xhigh`: use the xhigh level in the web chat;
- omitted: keep the level currently shown in that chat;
- unavailable: stop and report it instead of silently downgrading.

#### `preview`

Draft the request without contacting the web advisor or changing the execution task.

#### Execution target

You may say which execution task should continue. The bridge returns the answer to the task that raised the question and never copies browser credentials into the execution environment.

### Examples

```text
$reasoning-bridge
Compare the three architectures for this training plan, focusing on data cost, scalability, and what we can finish in two weeks. Use xhigh in the web chat and return the decision to the current task.
```

```text
$reasoning-bridge
Preview only. Assess whether this dependency upgrade is worth doing. Use high, but do not send the request.
```

```text
$reasoning-bridge
Three attempted fixes have not explained this bug. Use Pro mode to reconsider the overall direction, then return the recommendation to the original task.
```

### Good fit

Use it for external research, architecture decisions, long-term planning, premise checks, and unusually difficult direction problems.

For routine implementation, straightforward debugging, or a small local edit, ask Codex directly.

## Installation

Install this repository as a Codex plugin, or copy `skills/reasoning-bridge` to `~/.codex/skills/` to use the self-contained skill directly.
