# Reasoning Bridge

[中文说明](README.zh-CN.md)

Reasoning Bridge lets Codex ask a signed-in ChatGPT web chat to research or assess a development problem, then return the answer to the task doing the work.

It is intended for architecture choices, external research, comparing approaches, long-term planning, and difficult problems whose direction remains unclear after ordinary investigation. The active Codex task still reads the repository, writes code, debugs, and validates the result.

## Requirements

The local coordinator uses a browser-control extension:

1. Install and enable the Chrome or Edge browser extension.
2. Sign in to ChatGPT with the ordinary browser profile used by the extension.
3. Allow the extension to access local file URLs when uploading code.
4. The built-in `@Browser` surface may view web pages but cannot automate local file uploads.

If uploads are unavailable, text-only requests can use `code_context=none`. A request with attachments stops before upload and reports the missing capability.

## Usage

Invoke `$reasoning-bridge` and describe the decision:

```text
$reasoning-bridge
Compare these three training plans. Focus on data cost, multi-machine scaling, and what can be completed in two weeks. Use xhigh.
```

The bridge gathers facts, writes a natural engineering brief, asks the signed-in web advisor, and returns the full answer plus an execution brief to the originating task.

## Options

### `reasoning_level`

Choose one level available in the ChatGPT web interface: `instant`, `medium`,
`high`, `xhigh`, or `pro`. These correspond to the five positions shown by the
web reasoning control; labels may be localized. If omitted, keep the level
selected in the current web chat. An unavailable requested level stops the run
rather than being replaced.

### `prepare`

Summarize progress and produce the complete advisor request without sending it.

```text
$reasoning-bridge
Prepare the request only. Decide whether this dependency upgrade is worth doing based on the evidence gathered so far. Use high and do not send it.
```

### `code_context`

`none` (default) sends no files; `files` uploads a small explicit set; `bundle` builds and uploads a sanitized archive of selected relevant code. Uploads occur only when `files` or `bundle` is explicitly selected.

```text
$reasoning-bridge
Use xhigh to assess this cross-module refactor. Set code_context to files and attach the entry point, interface definition, and two relevant implementations.
```

## Local state

Recoverable state lives under `$CODEX_HOME/reasoning-bridge/sessions/`. Each logical request has a directory combining project, topic, and originating task ID; request, response, execution brief, and revisioned attachments stay outside the repository.

## Installation

For local skill use, copy `skills/reasoning-bridge` to `~/.codex/skills/reasoning-bridge`. A packaged installation can be added through a configured Codex marketplace.
