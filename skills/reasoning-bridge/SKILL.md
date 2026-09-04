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

Control the signed-in ChatGPT browser on the local coordinator host. Never copy
cookies, credentials, browser profiles, or session tokens to an execution host.

Reuse the existing advisor chat for the same logical problem. Create a new web
chat only when no suitable conversation exists.

The bridge accepts one logical setting, `reasoning_level`. Values such as `pro`,
`xhigh`, and `high` are mutually exclusive. Select the exact level requested by
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

Before submitting, remove credentials, private keys, cookies, signed URLs,
personal identifiers, and unrelated private material while preserving the
technical meaning.

## Return the decision

Wait for the web response to finish. Preserve the complete response in the
bridge task, then send the originating task a concise brief containing:

- the recommended direction and reasoning;
- implementation boundaries and validation expectations;
- assumptions the advisor rejected or asked to retest;
- evidence that would justify reconsidering the decision.

Verify the recorded task, host, project, and branch before sending the brief.
Do not ask the advisor again unless the user requests it or new evidence meets a
stated reconsideration condition.
