# Reasoning Bridge

[English](README.md)

Reasoning Bridge 让 Codex 把需要调研或高层判断的开发问题交给已登录的 ChatGPT 网页会话，再把回答送回正在执行工作的任务。

它适合架构选择、外部调研、方案比较、长期规划，以及普通调查后方向仍不清楚的困难问题。读取仓库、写代码、调试和验证仍由原 Codex 任务完成。

## 运行要求

本地协调任务使用浏览器控制扩展：

1. 安装并启用 Chrome 或 Edge 浏览器扩展；
2. 使用扩展对应的普通浏览器 profile 登录 ChatGPT；
3. 需要上传代码时，允许扩展访问本地文件 URL；
4. 内置 `@Browser` 可以查看网页，但不能自动上传本地文件。

没有上传能力时，纯文本请求仍可使用 `code_context=none`。如果请求包含附件，桥接器会在上传前停下并说明缺少的能力。

## 使用方法

调用 `$reasoning-bridge`，直接描述需要判断的问题：

```text
$reasoning-bridge
比较这三个训练方案，重点考虑数据成本、多机扩展难度，以及两周内能完成什么。使用 xhigh。
```

桥接器收集事实，写成自然的工程问题说明，通过已登录的 ChatGPT 网页会话提问，再把完整回答和执行摘要送回原任务。

## 配置

### `reasoning_level`

从 ChatGPT 网页的五档推理强度中选择一个：`instant`、`medium`、`high`、
`xhigh` 或 `pro`。网页可能显示本地化名称，例如“即时”“中”“高”“极高”。
不指定时保留当前网页会话的档位；指定档位不可用时会停止，不会自行替换。

### `prepare`

总结当前进度并生成完整请求，但不发送。

```text
$reasoning-bridge
只准备请求。根据目前证据判断这次依赖升级是否值得做。使用 high，不要发送。
```

### `code_context`

`none`（默认）不上传文件；`files` 上传少量明确选择的文件；`bundle` 生成并上传只包含相关代码的干净压缩包。只有明确选择 `files` 或 `bundle` 才会上传。

```text
$reasoning-bridge
使用 xhigh 判断这次跨模块重构是否合理。code_context 使用 files，附上入口文件、接口定义和两个相关实现。
```

## 本地状态

可恢复状态保存在 `$CODEX_HOME/reasoning-bridge/sessions/`。每个逻辑请求的目录名由项目、主题和原任务 ID 组成；请求、回答、执行摘要和带 revision 的附件都与项目仓库分开保存。

## 安装

单独使用 skill 时，将 `skills/reasoning-bridge` 复制到 `~/.codex/skills/reasoning-bridge`。完整插件包可以通过已配置的 Codex marketplace 安装。
