# Reasoning Bridge

[中文](#中文) · [English](#english)

## 中文

有些开发问题难的不是怎么写代码，而是该往哪个方向走。

Reasoning Bridge 让 Codex 把项目背景、已经确认的事实、尝试过的办法和真正需要决定的问题整理好，交给 ChatGPT 网页端做调研或判断。请求会像工程师写给另一位工程师的说明，而不是一段压缩过的状态数据。

Codex 继续负责读仓库、写代码、调试和验证。网页端更适合搜索资料、比较架构方案、规划长期工作，或者重新检查一个沿用了很久的前提。

使用时，在 Codex 中调用 `$reasoning-bridge`，然后直接说明你想解决的问题。插件会收集必要上下文，使用你指定的网页推理档位发送请求，并把完整回答带回原任务。如果你只想先看将要发送的内容，可以说“只预览，不发送”。

网页端的 Pro、`high`、`xhigh` 等档位是互斥选择。它们只影响这次网页对话，不会改变执行代码的 Codex 设置。

## English

Some development problems are difficult not because the code is hard to write, but because the right direction is unclear.

Reasoning Bridge helps Codex assemble the project background, confirmed facts, previous attempts, and the decision that still needs to be made, then asks a ChatGPT web chat to research or assess it. The request is written as an engineering brief, not as a compressed status dump.

Codex remains responsible for reading the repository, writing code, debugging, and validation. The web advisor is better suited to external research, architectural comparisons, long-term planning, and reconsidering assumptions that may no longer hold.

Invoke `$reasoning-bridge` in Codex and describe the problem. The plugin gathers the necessary context, sends the request using the web reasoning level you selected, and returns the complete answer to the original task. Say “preview only” if you want to review the request without sending it.

Web levels such as Pro, `high`, and `xhigh` are mutually exclusive. They apply only to the web conversation and do not change the Codex settings used for implementation.

## Installation

Install this repository as a Codex plugin, or copy `skills/reasoning-bridge` to `~/.codex/skills/` to use the skill directly.
