---
name: reasoning-bridge
description: Ask a separate ChatGPT web chat to research or make a high-level decision for an active coding task, then return the answer to the task that requested it. Use when the user explicitly invokes the bridge for research, planning, architecture, or a difficult direction choice.
---

# Reasoning Bridge

Use ChatGPT in the user's signed-in local browser as an outside advisor. The
active Codex task remains responsible for repository inspection, implementation,
debugging, and validation.

## Invocation

An invocation with a concrete question authorizes one complete run: gather the
needed context, ask the web advisor once, return its answer to the originating
task, and let that task continue. Do not ask for a second confirmation before
sending.

If the user selects `prepare` or clearly asks not to send, summarize the task's
progress so far and write the complete request that could be sent to the
advisor. Stop before submitting it.

Use the advisor for research, planning, architecture, consequential tradeoffs,
or an unusually difficult problem whose direction remains unclear after normal
investigation. Do not use it for routine coding or ordinary debugging.

## Bridge task

Keep advisor work in a separate local Codex task. Reuse the same bridge task for
follow-ups to the same logical problem so its web conversation and original
answers remain available.

Run this coordinator at low reasoning effort. Name it:

`RB · <execution-environment> · <project> · <topic>`

Place it in a local group named `Reasoning Bridge` when grouping is available.
Otherwise pin it and keep the `RB ·` prefix. Record the originating task ID,
host ID, project, working directory, branch, and commit so the answer returns to
the correct task even after a handoff.

Keep recoverable bridge artifacts under `$CODEX_HOME/reasoning-bridge/sessions/`
(on Windows, the configured Codex home directory), with one directory per
logical request. Use a stable slug plus the originating task ID, for example
`<project-slug>--<topic-slug>--<task-id>/`. Inside it use these fixed names:
`state.json`, `request.md`, `response.md`, `execution-brief.md`, and an
`attachments/` directory. Write new revisions to the same session directory,
and never overwrite an existing attachment; use a revision suffix when needed.
Do not put cookies, credentials, or browser profile data in this directory.

## Gather context

Ask the originating Codex task to supply current repository facts and relevant
evidence. Before contacting the advisor, know:

- what the user wants and what is out of scope;
- why a direction decision is needed now;
- how the project currently behaves;
- what has already been tried and what happened;
- the realistic alternatives and their tradeoffs;
- which assumptions may be accepted mainly because they are old or familiar;
- the exact questions the advisor should answer.

Gather missing facts that are cheap to obtain, but do not delay the request in
search of exhaustive context. Treat repository evidence from the originating
task as authoritative; do not turn guesses into facts.

Before sending, check whether an advisor with no access to the repository or
the Codex conversation could understand the problem and make the requested
decision. If not, obtain the missing material from the originating task. Ask
the user only when the missing information requires a real choice or cannot be
recovered from the task and repository.

## Write the web request

Write as an engineer briefing a senior collaborator. Keep it concise, but give
the advisor enough context to reason without access to the repository or the
earlier conversation. Use this order, omitting sections that truly do not apply:

1. **What we are trying to achieve** — the outcome and why the decision matters.
2. **Current situation** — how the system works now and the relevant project context.
3. **Evidence** — confirmed behavior, measurements, tests, or representative errors.
4. **What we tried** — the meaningful attempts and what each one showed.
5. **Choices and constraints** — realistic alternatives, tradeoffs, deadlines,
   resources, exclusions, and user priorities.
6. **Assumptions to challenge** — inherited beliefs that may be wrong or stale.
7. **Questions** — a small set of direct decisions the advisor should make.

Use natural paragraphs under these headings rather than terse fields. Include
short code or error excerpts only when they help the advisor reason independently.

Call out long-standing assumptions that deserve a fresh look. Make clear what
is confirmed, what is interpretation, and what is still unknown. End with a few
direct questions. Do not send JSON, YAML, routing metadata, token counts, or a
compressed status packet to the advisor.

## Use the browser

Use browser Use through the enabled Chrome/Edge extension on the local
coordinator host. Do not use the built-in `@Browser` for attachments, and never
copy cookies, credentials, profiles, or session tokens to an execution host.

Use this tested sequence; do not rediscover the upload or reasoning controls:

1. Read the current browser state and select the extension browser whose normal
   profile is signed in to ChatGPT. Browser IDs can change after the extension
   reloads. If a saved handle reports that the browser is unavailable, read the
   state again and bind the same extension/profile using its newly returned ID.
2. Reuse the conversation URL stored in `state.json`, or create a new
   `https://chatgpt.com/` tab for a new logical problem. Keep advisor tabs
   separate from unrelated user chats.
3. For attachments, click **Add files** and refresh the page state so **Upload
   from computer** is visible. Only then start a `filechooser` wait, click
   **Upload from computer**, await the chooser, and call `setFiles` with the
   absolute paths from the session `attachments/` directory. Start the chooser
   wait immediately before that upload click, not before opening the menu, and
   handle timeouts so an abandoned promise cannot reset the browser session.
4. Verify every attachment filename is visibly listed in the composer. A
   successful `setFiles` call alone is not proof of upload. If `setFiles`
   returns `Not allowed`, local-file access is still disabled for the extension;
   stop before sending and report that exact blocker.
5. Open the visible reasoning control. It is a five-position ability slider.
   Focus the text shaped like `<level>, item <n> of 5`, move one position at a
   time with the left or right arrow, refresh, and repeat until the selector
   button visibly names the requested level. The positions are 1 Instant, 2
   Medium, 3 High, 4 xhigh, and 5 Pro; visible labels may be localized. Do not
   assume an arrow changed the level unless the visible label changed.
6. Put the completed briefing in the ChatGPT composer and verify the request,
   attachment names, and reasoning label together. Submit exactly once.
7. Verify that ChatGPT created a conversation URL, then wait until the stop
   button disappears and a complete assistant response with response actions is
   visible. Store the final stable `/c/<conversation-id>` URL, not an interim
   `WEB:` URL. Preserve the response verbatim before writing the execution brief.

At startup, verify the extension is enabled, the ordinary browser profile is
signed in, and local-file URL access is enabled when attachments are requested.
A text-only request can continue with `code_context = none`; an attachment run
must stop before sending if upload cannot be visibly verified.

Reuse the existing advisor chat for the same logical problem. Create a new web
chat only when no suitable conversation exists.

The bridge accepts one logical setting, `reasoning_level`: `instant`, `medium`,
`high`, `xhigh`, or `pro`. These five values are mutually exclusive. Select the exact level requested by
the user and verify it in the visible web UI before sending. If the user does
not specify a level, keep the level already selected in that chat. If the exact
level is unavailable, stop and report it rather than silently substituting one.
Never pass `reasoning_level` to the Codex execution task.

The optional `code_context` setting controls code attachments:

- `none` (default): send no files; use concise excerpts in the written request;
- `files`: attach the smallest useful set of source or configuration files;
- `bundle`: create and attach a minimal sanitized code bundle when the decision
  genuinely depends on relationships across many files.

Only upload code when the user explicitly selects `files` or `bundle`. That
selection authorizes uploading the prepared material to the chosen ChatGPT web
chat. For `files`, prefer files named by the user; otherwise select only files
whose contents are needed for the decision. For `bundle`, include a short
README that identifies the entry points and explains why each included area is
relevant. Do not include the whole repository by default.

Exclude `.git`, credentials, environment files, private keys, personal data,
datasets, logs, caches, generated outputs, model weights, binaries, and
unrelated proprietary code. Inspect the final attachment set before upload and
mention the attachments in the written request so the advisor knows how to use
them.

If the connected browser cannot upload files, do not claim that an attachment
was sent. Keep the prepared bundle available, report the limitation, and ask the
user to attach it manually or continue with `code_context = none`.

Before submitting, remove credentials, private keys, cookies, signed URLs,
personal identifiers, and unrelated private material while preserving the
technical meaning.

For `code_context = bundle`, build the attachment with
`scripts/build_code_bundle.py --root <repo> --include <path> --output
<session>/attachments/context-r<revision>.zip`. Repeat `--include` for each
selected file or directory. The script is allowlist-based and refuses paths
outside the repository, sensitive content, binaries, oversized files, and
overwrites.

## Wait, wake, and recovery

The bridge task owns `state.json`. Update it atomically before and after every
external action. Use this minimal state shape:

```json
{
  "schema_version": 1,
  "session_id": "<project>--<topic>--<origin-task-id>",
  "phase": "collecting",
  "mode": "send",
  "context_revision": 1,
  "request_id": "<session-id>:r1",
  "origin": {
    "task_id": "...", "host_id": "...", "project": "...",
    "working_directory": "...", "branch": "...", "commit": "..."
  },
  "bridge_task_id": "...",
  "reasoning_level": "xhigh",
  "code_context": "none",
  "attachments": [],
  "web": {"conversation_url": null, "conversation_id": null},
  "send_attempted": false,
  "message_visible": false,
  "last_error": null
}
```

The phases and legal transitions are:

- `collecting -> ready`: the briefing is complete and every requested
  attachment has been built and inspected;
- `collecting -> prepared`: `prepare` mode wrote `request.md` and intentionally
  stops without browser submission;
- `ready -> submitting`: write `send_attempted = true` immediately before the
  single browser submit action;
- `submitting -> waiting`: the user message is visibly present in ChatGPT;
  store the conversation URL and set `message_visible = true`;
- `waiting -> returned`: the complete response is visible and saved verbatim to
  `response.md`, then `execution-brief.md` is written;
- `returned -> delivered`: the full response and execution brief were sent to
  the recorded originating task;
- any non-terminal phase may enter `blocked` with a concrete `last_error` and
  the previous phase recorded; after the blocker is resolved, resume that phase;
- a requested follow-up from `delivered` increments `context_revision`, assigns
  a new `request_id`, and returns to `collecting` in the same session.

Never automatically retry from `submitting`. If execution stopped after the
submit action but before the message was verified, mark the run `blocked` with
`send_outcome_unknown`, reopen the recorded ChatGPT conversation, and search
for the exact request text and attachment names. Move to `waiting` if it is visible;
return to `ready` only after confirming it was not sent. This is the duplicate
submission guard.

The originating task sends its context revision to the bridge task. If its work
is blocked on the decision, it waits on that bridge task with `wait_threads`;
otherwise it may continue unrelated safe work. The bridge uses `wait_threads`
only when it requested missing facts from another Codex task. Browser responses
are awaited by observing the ChatGPT page, not by `wait_threads`.

Once the web answer is complete, the bridge sends the untouched response plus
the execution brief with `send_message_to_thread` to the recorded originating
task. That message is the wake-up signal. Verify the origin identity before
sending. If the originating task moved or ended, retain the answer in phase
`returned` and ask where to resume rather than routing it elsewhere.

## Return the decision

Wait for the web response to finish. Preserve the complete response in the
bridge task, then send the originating task a concise brief containing:

- the recommended direction and reasoning;
- implementation boundaries and validation expectations;
- assumptions the advisor rejected or asked to retest;
- evidence that would justify reconsidering the decision.

Verify the recorded task, host, project, and branch before sending the brief.
Include the complete untouched advisor response in the bridge task and in the
message sent to the originating task; the brief is an index for execution, not
a replacement for the source answer.
Do not ask the advisor again unless the user requests it or new evidence meets a
stated reconsideration condition.
