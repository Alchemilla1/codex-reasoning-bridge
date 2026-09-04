# Reasoning Bridge

[中文说明](#中文说明) · [English](#english)

## 中文说明

Reasoning Bridge 帮助 Codex 在软件任务遇到需要外部调研、总体规划或高层取舍时，准备一份清晰、完整、像工程师写给资深合作者的请求，交给 ChatGPT 网页端高层顾问判断。

当前工作的 Codex session 仍然负责读取仓库、加载 skill、编写代码和验证。ChatGPT 网页端顾问主要用于架构方向、外部方案比较、长期任务规划，以及新证据推翻原有前提后的重新判断。网页端可以选择 Pro、`high`、`xhigh` 等可用的互斥推理档位；这些设置不会改变 Codex session。

加载插件后，你可以只发送一次具体任务。插件会创建或恢复桥接 session，让 Codex 收集事实，等待上下文达到决策条件，再通过已登录的 ChatGPT 浏览器提交自然语言请求。得到回答后，它会把方向与边界送回原任务并继续执行。如果你只想看草稿，可以明确使用预览模式，此时不会联系网页端顾问。

桥接会保留同一任务的上下文，让顾问的意见能够回到原来的执行任务中。浏览器登录信息不会写入仓库，也不会随代码传递。

安装后，在 Codex 中使用 `$reasoning-bridge` 并描述任务即可启动完整闭环。日常实现不会频繁调用 ChatGPT 网页端；只有高层问题成熟后才会提交一次完整请求。

## English

Reasoning Bridge helps Codex prepare a clear, complete request for a selected ChatGPT web chat when a software task needs outside research, broad planning, or a consequential direction decision.

The active Codex session remains responsible for inspecting the repository, loading skills, writing code, and validating changes. The ChatGPT web advisor is reserved for architecture, external comparisons, long-horizon planning, and reconsidering an old premise when new evidence challenges it. The web chat may use an available reasoning level such as Pro, `high`, or `xhigh`; these choices are mutually exclusive and do not change the Codex session.

After loading the plugin, you can send one concrete task. It gathers evidence, waits until the decision question is mature, submits a natural engineering brief in the existing signed-in ChatGPT browser, and returns the decision to the execution task. Use preview-only mode when you want to inspect the draft without contacting the advisor.

The bridge keeps one task's context together so the advisor's decision can return to the execution task that raised the question. Browser credentials stay outside the repository and are never transported with the code.

Install the plugin, invoke `$reasoning-bridge`, and describe the task to run the complete bridge.

## Installation / 安装

Install the repository as a Codex plugin, or copy `skills/reasoning-bridge` into `~/.codex/skills/` to use the self-contained skill directly.
