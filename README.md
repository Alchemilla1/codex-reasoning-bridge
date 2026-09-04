# Reasoning Bridge

[中文说明](README.zh-CN.md)

Reasoning Bridge is a local Codex skill for asking a signed-in ChatGPT web chat
to research or make a high-level decision for a remote Codex task.

The remote task continues to own the repository, commands, experiments, and
implementation. The local bridge reads that task, writes the advisor briefing,
uses the local Chrome/Edge extension, and sends the result back. No permanent
coordinator task or background watcher is required.

## Use it

Invoke the skill in a local Codex task and provide the unique remote thread ID:

```text
$reasoning-bridge
remote_thread_id: <remote-thread-id>
Reassess the architecture direction. Use xhigh and attach only relevant code if needed.
```

The bridge reads the remote thread itself. If current facts are missing, it
sends one focused request for facts, then reads the reply before writing the
briefing. After the web answer is complete, it sends the full response and a
short execution brief back to the same remote thread.

## Options

`reasoning_level` selects the ChatGPT web control: `instant`, `medium`, `high`,
`xhigh`, or `pro`.

`code_context` controls optional uploads:

- `none` (default): no files;
- `files`: a small explicit set of relevant files;
- `bundle`: a sanitized archive of selected remote code.

These options affect only the web advisor. They do not change the remote Codex
task's model or reasoning settings.

## Browser requirements

Use a signed-in ordinary Chrome or Edge profile with the Codex browser extension
enabled. Allow local file URLs when uploading code. The built-in `@Browser`
surface cannot automate local file selection.

## Local run state

Recoverable files are kept outside the repository at:

```text
$CODEX_HOME/reasoning-bridge/sessions/<remote-thread-id>/
```

The directory contains the request, response, execution brief, state, and any
revisioned attachments. It is temporary run state, not a persistent bridge
session.
