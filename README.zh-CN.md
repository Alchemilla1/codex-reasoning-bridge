# Reasoning Bridge

[English](README.md)

Reasoning Bridge 是一个只在本地 Codex 中运行的 skill，用来读取远端 Codex
任务，把需要调研或高层判断的问题交给已登录的 ChatGPT 网页会话，再把结果
送回原远端任务。

远端任务继续负责仓库、命令、实验和代码实现。本地桥接器负责读取远端任务、
筛选有效上下文、写给顾问的 briefing、操作本地 Chrome/Edge 扩展，并把回答发回。
不需要永久协调任务，也不需要后台 watcher。

## 使用

在本地 Codex 中调用 skill，并提供唯一的远端 thread ID：

```text
$reasoning-bridge
remote_thread_id: <remote-thread-id>
请重新判断当前架构方向。使用 xhigh，必要时只附上相关代码。
```

桥接器自己读取远端任务历史。如果事实不足，只会向远端发送一次针对缺失事实
的补充请求，然后重新读取回复并写 briefing。网页顾问回答完成后，桥接器会把
完整回答和执行摘要发回同一个远端任务。

## 配置

`reasoning_level` 对应 ChatGPT 网页端的推理档位：`instant`、`medium`、`high`、
`xhigh` 或 `pro`。

`code_context` 控制是否上传代码：

- `none`（默认）：不上传文件；
- `files`：上传少量明确相关的文件；
- `bundle`：生成只包含选定远端代码的清理后压缩包。

这些设置只作用于网页顾问，不改变远端 Codex 任务的模型或思考强度。

## 浏览器要求

使用已登录 ChatGPT 的普通 Chrome 或 Edge profile，并启用 Codex 浏览器扩展。
需要上传代码时，允许扩展访问本地文件 URL。内置 `@Browser` 不能自动选择本地文件。

## 本地运行状态

可恢复文件保存在仓库之外：

```text
$CODEX_HOME/reasoning-bridge/sessions/<remote-thread-id>/
```

其中包含请求、回答、执行摘要、状态和带 revision 的附件。这是一次运行的临时
状态，不是永久桥接会话。
