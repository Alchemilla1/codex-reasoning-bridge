---
name: reasoning-bridge
description: "Run a one-time local bridge for a remote Codex task: read its thread, ask a signed-in ChatGPT web advisor for research or a high-level decision, and send the result back."
---

# Reasoning Bridge

This skill runs in a local Codex task and requires the unique ID of the remote
Codex task. It does not create a permanent coordinator, watcher, relay, or
remote browser session.

## Invocation

Use `$reasoning-bridge` with the remote task ID and a concrete decision:

```text
$reasoning-bridge
remote_thread_id: <remote-thread-id>
请重新判断当前架构方向。使用 xhigh，必要时附上关键代码文件。
```

A concrete explicit invocation is the user's instruction to complete the whole
run: read the remote task, send one request to the selected ChatGPT web advisor,
and return the answer to the same remote task. Do not introduce a skill-level
preview, approval gate, or "shall I send it?" question after preparing the
briefing. Proceed directly to submission wherever the active product policy
allows it. File upload is authorized only when `code_context` is explicitly
`files` or `bundle`.

Optional settings are `reasoning_level` (`instant`, `medium`, `high`, `xhigh`,
or `pro`) and `code_context` (`none`, `files`, or `bundle`). They apply only
to the ChatGPT web advisor, never to the remote Codex task.

## Responsibility boundary

The remote task is the execution side. It reads the repository, runs commands,
checks experiments or services, produces current facts, and continues the work
after receiving the answer. If asked for more context, it supplies facts and
evidence only; it does not write the advisor briefing or choose the direction.

The local bridge is the reasoning side. It reads the remote thread and task
metadata, decides which context is current and relevant, challenges stale
assumptions, writes the human engineering briefing, selects the web reasoning
level and code attachments, operates the local browser, preserves the complete
advisor response, writes the execution brief, and sends the result back.

The remote task identifies relevant source paths and explains why they matter.
The local bridge copies only those explicit files into its local run directory,
checks them, and builds any requested bundle locally with the installed helper.
Never send a remote path directly to a browser file chooser.

## One-time workflow

1. Parse `remote_thread_id`; ask for it if missing.
2. Use local Codex app tools to find and verify the exact remote thread. Read its
   title, host ID, project, working directory, status, and recent history with
   `list_threads` and `read_thread`.
3. Read the thread yourself. Extract the goal, current implementation, confirmed
   evidence, failed attempts, constraints, open decisions, and the user's exact
   question. Do not ask the remote task to summarize unless facts are missing.
4. If facts are missing, send one focused request to the verified remote thread:

   ```text
   请只补充当前实现、已验证证据、失败尝试和未决问题。不要写顾问 briefing，不要做方向判断。
   ```

   Wait for that turn, then read the new message. Do not send repeated reminders.
5. Create a temporary local run directory at
   `$CODEX_HOME/reasoning-bridge/sessions/<remote-thread-id>/`. Keep
   `state.json`, `request.md`, `response.md`, `execution-brief.md`, and
   revisioned attachments there. This is recoverable run state, not a permanent
   bridge session. Never store credentials, cookies, or browser profiles.
6. Write `request.md` locally as a natural briefing for a senior engineer. Use
   these sections when relevant: outcome, current situation, evidence, attempts,
   choices and constraints, assumptions to challenge, and direct questions.
   Distinguish confirmed facts from interpretation. Do not send JSON, routing
   metadata, token counts, or a mechanical transcript to the web advisor.
7. For `code_context = files` or `bundle`, ask the remote task for the smallest
   relevant path list when the thread does not already identify it. Copy those
   files into the local run directory, inspect them, and use the installed
   helper for a bundle:

   ```bash
   python3 scripts/build_code_bundle.py --root <local-copy-root> --include <path> --output <session>/attachments/context-r<revision>.zip
   ```

   Exclude credentials, private keys, environment files, datasets, logs, caches,
   generated outputs, weights, binaries, and unrelated private code.
8. On the local machine, use the signed-in Chrome/Edge extension. Do not use
   the built-in `@Browser` for local file upload and do not open ChatGPT from
   the remote host. Submit the completed briefing exactly once.
9. Save the stable ChatGPT `/c/<conversation-id>` URL immediately. If the
   response is still generating after a short foreground check, persist phase
   `waiting`, keep the browser tab available, and create one temporary local
   heartbeat that checks this exact conversation every 10 minutes. End the
   current turn instead of repeatedly polling. The heartbeat must read only the
   saved state and exact conversation until generation finishes; it must not
   reread the remote thread or rebuild the briefing on every check. Stay silent
   while the response is incomplete. When complete, save the response verbatim
   to `response.md`, write `execution-brief.md`, continue with return routing,
   then pause the heartbeat.
10. Verify the original remote thread identity again. Use the local Codex app
    tool `send_message_to_thread` to send the complete response and execution
    brief to that remote task. This is the only return-routing action.
11. Mark the run `delivered`. If delivery fails, keep it `returned`, preserve
    the files, and report the concrete error without automatically duplicating
    the message.

## Browser procedure

Use the local browser-control extension:

1. Read browser state and select the enabled Chrome/Edge extension browser whose
   ordinary profile is signed in to ChatGPT. Browser IDs can change after an
   extension reload; if a saved handle is unavailable, read state again and bind
   the same profile using its current ID.
2. Reuse the conversation URL in `state.json`, or open a new `https://chatgpt.com/`
   tab for this request.
3. For attachments, open **Add files**, refresh until **Upload from computer**
   is visible, start the `filechooser` wait immediately before clicking it, and
   call `chooser.setFiles` with absolute local paths.
4. Verify each filename is visibly listed. A successful `setFiles` call alone
   is not proof of upload. If upload is denied or absent, stop before sending
   and preserve the prepared request.
5. Set the five-position reasoning control to the requested level: 1 Instant,
   2 Medium, 3 High, 4 xhigh, 5 Pro. Confirm the visible label after movement.
6. Confirm the briefing, attachments, and reasoning label, then submit once.
7. After submission, confirm the user message is visible and record the stable
   `/c/<conversation-id>` URL. Use a short foreground wait only for fast
   responses. For a long-running Pro response, do not hold the Codex turn open
   with repeated browser polling. Switch to the temporary 10-minute heartbeat
   described above. Completion requires the stop button to be absent and the
   complete assistant response plus response actions to be visible.

## State and recovery

Use this shape, adding fields only when necessary:

```json
{
  "schema_version": 2,
  "remote_thread_id": "...",
  "remote_host_id": "...",
  "phase": "collecting",
  "request_id": "<remote-thread-id>:r1",
  "context_revision": 1,
  "reasoning_level": "xhigh",
  "code_context": "none",
  "web": {"conversation_url": null, "conversation_id": null},
  "send_attempted": false,
  "last_error": null
}
```

Legal phases are `collecting -> ready -> submitting -> waiting -> returned ->
delivered`; any non-terminal phase may enter `blocked` with a concrete error.
Update `state.json` atomically before and after external actions. Never retry a
browser submission after an uncertain outcome: reopen the recorded conversation
and search for the exact request before deciding whether it was sent.

The run is complete only after the full response and execution brief have been
sent to the verified remote thread. A local answer without remote delivery is
`returned`, not `delivered`. A waiting heartbeat is temporary run machinery,
not a permanent coordinator or watcher, and must be paused after delivery or a
terminal error.

## Boundaries

- This skill runs only in a local Codex task.
- The remote task never controls the local browser or creates a local task.
- The local bridge may send one context request and one final result message.
- Browser login state and local files remain on the local machine.
- Do not silently change the requested reasoning level or upload unauthorized files.
