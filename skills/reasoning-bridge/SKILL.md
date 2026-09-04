---
name: reasoning-bridge
description: Bridge a coding task to a separate ChatGPT web chat for research, broad planning, or a high-level direction decision, then return the decision to execution. The web chat may use a user-selected reasoning level such as Pro or xhigh.
---

# Reasoning Bridge

Use a separate ChatGPT web chat as a deliberate direction setter. The web chat
may use the user's Pro access and selected reasoning level, such as `pro` or
`xhigh`.
The local bridge coordinator remains low-effort, and the original remote
execution chat keeps its existing effort. Remote hosts are execution targets,
not advisor-chat targets. Keep the execution chat responsible for repository
inspection, skill use, implementation, and validation.

## Operating boundary

- Use low reasoning effort for coordination. Collect facts, identify
  missing evidence, organize context, and route work without trying to replace
  the advisor's judgment. Never raise the coordinator's effort merely because
  the advisor was configured for `high` or `xhigh`.
- Do not invoke an advisor until the user either explicitly asks to send a
  prepared request or invokes the bridge in one-shot mode with a concrete task.
  A request only to prepare, accumulate, or preview context is not permission to
  send it.
- Do not block ordinary implementation while waiting for a possible advisor call.
  Continue safe in-scope work that does not depend on the unresolved direction.
- Use the web advisor primarily for external research, broad task planning,
  architectural or product direction, and consequential tradeoffs. Routine
  coding and debugging remain with the execution session. Escalate an unusually
  difficult bug only after collecting a minimal reproduction, relevant attempts,
  and concrete evidence.
- Do not insert a coordinator into every exchange. The coordinator is an
  asynchronous context collector and request writer, not a mandatory relay.

## Prepare the context

Accumulate context until the question is mature enough for a useful decision.
Prefer current repository files, loaded skills, actual runtime arguments, test
results, and original user constraints over inference.

Before marking an advisor request ready, establish as applicable:

- what the user is trying to accomplish and what is out of scope;
- why a high-level decision is needed now;
- the current system behavior and relevant project history or constraints;
- facts confirmed in the active local or remote environment;
- approaches already considered or attempted and what happened;
- the real alternatives, their consequences, and the current team's tentative
  leaning, if any;
- meaningful uncertainties or assumptions that the advisor should challenge;
- inherited premises that have shaped the work for a long time but may no
  longer be valid, including their origin, age, and current supporting evidence;
- the precise decision or research questions the advisor should answer.

Do not delay the request merely to make the packet exhaustive. It is ready when
additional low-cost repository inspection is unlikely to change the question.
If important evidence is still obtainable locally or from the active remote
execution host, gather it before invoking the web advisor.

## Write for a person

The final request must read like a thoughtful engineer briefing a senior
collaborator, not like serialized state, telemetry, a prompt template, or a
distilled model summary.

- Use natural paragraphs and descriptive headings when they help navigation.
- Explain the causal story: what is being built, what was discovered, why the
  decision matters, and why it is being raised now.
- Preserve important nuance, user priorities, uncertainty, failed attempts, and
  representative original evidence. Include small code or error excerpts when
  the advisor needs them to reason independently.
- Clearly distinguish confirmed facts, current interpretations, and unknowns.
- Describe alternatives fairly. Do not silently pre-decide the answer or reduce
  the problem to labels such as `option_a` and `option_b`.
- End with a small number of direct questions about direction, overlooked
  premises, implementation boundaries, and evidence that should trigger
  reconsideration.
- State that code or line-by-line debugging is not requested unless the user
  explicitly wants it.

Structure may be used internally, but do not expose YAML, JSON, revision fields,
host metadata, or machine-oriented status blocks in the advisor request unless a
specific field is genuinely relevant to the decision.

## Preview and send

When the material is ready, show the user the complete proposed request and a
brief note about any material context still missing. Do not send it yet.

Send it only after an explicit instruction or an unambiguous one-shot bridge
request. Use the selected ChatGPT web reasoning level. Do
not silently substitute another mode or effort.

After the advisor replies:

- preserve the original response rather than replacing it with a lossy summary;
- extract only the decisions and execution constraints needed by the active
  Codex task;
- record what new evidence would justify asking the advisor to reconsider;
- return implementation control to the active Codex session.

## Host behavior

Work against the environment that owns the active task. Repository facts,
skills, commands, and validation come from that local or remote host. A browser
session belongs to the host where it is configured; do not imply that an SSH
session can directly reuse another machine's signed-in browser.

When this skill is installed on multiple hosts, keep the workflow identical but
do not synchronize credentials, cookies, secrets, or browser profiles between
them.

## Exact operating protocol

Follow this protocol when the skill is invoked. Do not replace it with a search
for another workflow document.

### 1. Classify the request

Choose one mode:

- `collect`: gather material for a possible advisor request; never contact the
  ChatGPT web advisor.
- `preview`: write the complete human-readable request and show it to the user.
- `send`: contact the ChatGPT web advisor because the user authorized sending.
- `resume`: apply an existing advisor decision to the active execution task.

There is also a one-shot mode. When the user invokes this skill with a concrete
task and asks the bridge to handle it, treat that invocation as authorization for
one complete bridge run: create or resume the bridge session, collect the needed
context, send one mature request to the ChatGPT web advisor, apply the answer,
and continue remote execution. Do not pause for a second send confirmation. The
one-shot run still must not contact the advisor before the maturity gate.

If the user asks only to prepare, accumulate, or preview, use `collect` or
`preview` and do not contact the advisor. If the user's wording is ambiguous, prefer
`preview` rather than sending.

### 2. Create or resume the bridge session

Always keep bridge work separate from the implementation session. Create or
resume a dedicated Codex bridge task on the local coordinator host, even when
the implementation task is also local. In one-shot mode this is part of the
single invocation and happens without another question.

Keep all bridge tasks in one local session group named `Reasoning Bridge`.
If the current Codex surface exposes named task sections or groups, create or
reuse that exact group and place every bridge task inside it. If grouping is not
available through the current tools, use the `RB ·` title prefix and pin active
bridge tasks so they remain equally retrievable; do not pretend that a group was
created.

Run the bridge task at low reasoning effort by default. It is a lightweight
coordinator, not a second implementation agent. Give it the original objective
and acceptance criteria, active execution host and repository identity, context
revision, confirmed facts, assumptions, constraints, attempts, evidence,
current decision question, requested `reasoning_level`, request
status, the untouched advisor response, and
conditions for reconsideration.

At creation, record the exact return route to the implementation task: task or
thread ID, host ID, project identity, working directory, branch, and latest
known commit. A human-readable title is not sufficient for routing a decision
back. Refresh the route after a host handoff.

Use exactly one bridge task for each logical user task. Name it:

`RB · <host-label> · <project> · <decision-topic>`

Use a short label that identifies the active execution environment without
including credentials or sensitive infrastructure details. Keep the title short
enough to scan while preserving the project and decision identity. When the
execution host changes, update the existing title instead of creating a new bridge task.

Resolve an existing bridge task by stable task identity first, then by its exact
title and project. Resume it for follow-ups and retain its full advisor conversation.
Do not reuse a bridge task for a different logical task merely because the
project or topic looks similar.

Treat repeated invocations for the same task and context revision as idempotent.
If an advisor request is already in progress, wait for or resume that request instead
of submitting a duplicate. If the repository facts changed after submission,
mark the response as based on stale context and compare the changed facts before
applying it.

After creation or resumption, send it the latest execution findings and continue
collecting there asynchronously. The implementation task may continue work that
does not depend on the pending advisor decision.

### 3. Select the execution host

Use the environment that owns the active task, or the remote target explicitly
named by the user. Never select a different host merely because it appears more
capable. If the requested target is unavailable, report it and keep the bridge
session waiting.

Record the resolved host, project directory, branch, and commit when available
before using that host's findings in an advisor request.

### 4. Collect execution-side facts

Ask the active Codex execution session to inspect the relevant repository and
load the applicable skills:

1. Read project instructions and relevant skill instructions.
2. Locate the implementation entry points and configuration governing the
   question.
3. Run the smallest safe inspection, reproduction, or targeted test that can
   disprove the current understanding.
4. Record attempted approaches, concrete outcomes, and representative errors.
5. State what remains unknown and whether it can still be answered locally.
6. Identify inherited premises: architecture choices, configurations, earlier
   conclusions, workarounds, dataset assumptions, or operating habits that the
   current task has treated as fixed mainly because they are longstanding.

For every inherited premise that could affect the direction, record:

- where it came from and whether that source is still available;
- when it was last independently checked;
- what current evidence supports or contradicts it;
- what work has already been built on top of it;
- the cost and consequence of keeping, retesting, or rejecting it.

Longevity, prior investment, repeated mention, and presence in the current
session are not evidence that a premise is correct. Do not silently preserve a
premise merely to avoid invalidating completed work.

The execution session remains authoritative for repository facts. The bridge
must not invent behavior or convert an unverified interpretation into a fact.

### 5. Decide whether the request is mature

Keep collecting while the question can be answered cheaply by the execution
session. Mark it mature only when the unresolved issue is a consequential
direction or tradeoff, relevant local evidence exists, user priorities and
exclusions are known, alternatives can be explained fairly, and the questions
for the advisor are specific enough to answer.

Do not call the advisor because a command is slow, a log is long, or a routine bug needs
ordinary debugging.

### 6. Use the browser correctly

For the ChatGPT web advisor browser:

1. Use the browser on the host where the signed-in ChatGPT web session exists,
   normally the local coordinator host.
2. Reuse the user's selected ChatGPT chat when available.
3. Select the requested ChatGPT reasoning level in that web chat when
   the UI exposes those controls. The selected effort belongs to the web chat,
   not to the remote Codex execution session.
4. Never ask an SSH execution session to control that local browser.
5. Never copy cookies, browser profiles, passwords, or session tokens to a
   remote host.
6. Before explicit send authorization, browser actions may open the selected
   chat and prepare text, but must not submit it.
7. After explicit authorization, submit exactly the reviewed request and
   capture the complete response in the bridge session.
8. Before submission, remove credentials, tokens, cookies, private keys, signed
   URLs, personal identifiers, and unrelated proprietary material. Replace them
   with a description that preserves the technical meaning. Do not weaken the
   decision context merely to avoid stating that something was redacted.

Interpret advisor settings from natural language. Examples:

- `$reasoning-bridge 用网页端 xhigh 判断这个训练方案，然后让执行任务继续。`
- `$reasoning-bridge 用当前 ChatGPT Pro 模式调研，再把结论交回原任务。`
- `$reasoning-bridge 只预览，网页端使用 high，不要发送。`

Use one logical web-chat setting, `reasoning_level`. Its values are mutually
exclusive and may be named `pro`, `xhigh`, `high`, or another visible label.
The current ChatGPT UI may expose ordinary levels through the composer selector
and Pro through a separate “use Pro mode” action, but the bridge must not model
them as two values that can be requested together. When the user says “use
Pro”, record `reasoning_level = pro`; when they say “use xhigh”, record
`reasoning_level = xhigh`.

If the user omits the level, preserve the currently visible level in the chosen
ChatGPT web chat. Before submitting, verify that the UI visibly shows the exact
requested level. If that level is unavailable, stop at the advisor gate and
report it; do not silently downgrade, switch to Codex, or change the remote
execution chat's effort. Never pass `reasoning_level` to remote Codex.

For a project execution browser:

1. Use it only when the active execution host has its own configured browser,
   extension, or browser tool.
2. Treat it as part of that project environment, not as the ChatGPT web advisor
   channel.
3. If the remote host lacks browser capability, continue with repository and
   shell work or report the concrete blocker. Do not tunnel into the local
   browser implicitly.

### 7. Draft the request

Write the web-advisor request in this order:

1. what we are building or trying to change;
2. why the question is being raised now;
3. what the project actually does today;
4. important confirmed facts and representative evidence;
5. what has been tried and what happened;
6. remaining alternatives and their tradeoffs;
7. inherited premises that may deserve revalidation, including why the team has
   relied on them and what would change if they are wrong;
8. user priorities, constraints, and exclusions;
9. the specific judgment requested from the advisor, including which premises should be
   retained, retested, or discarded;
10. evidence that should trigger reconsideration later.

Use natural paragraphs and useful headings. Preserve necessary code and error
excerpts. Do not expose bridge IDs, serialized state, host-routing metadata,
token counts, or phrases such as "context distillation" unless the user asks
for operational details.

### 8. Preview and wait

In `preview` mode, show the entire proposed request and identify material gaps.
Stop there. Do not send it, create a new advisor chat, or act on an unapproved
direction.

In one-shot mode, do not stop at the preview. Keep the draft internally, proceed
to step 9 once the maturity gate passes, and report the final advisor decision and
execution outcome at the end. If the maturity gate does not pass, continue
low-cost local or remote fact gathering; pause only for a genuine user decision
or a missing permission.

### 9. Send only on explicit instruction

In `send` mode, and in one-shot mode after the maturity gate:

1. verify that the user explicitly requested sending, either directly or by
   invoking one-shot mode with a concrete task;
2. reuse the selected ChatGPT web chat;
3. create a dedicated reasoning bridge chat only when no suitable chat exists and the
   user explicitly asks for a new one;
4. submit the reviewed human-language request;
5. wait until the advisor has finished its response; partial streaming text is not a
   completed decision;
6. retain the untouched completed advisor response and the context revision it
   answered;
7. extract the decision, constraints, and reconsideration conditions for the
   execution session.

If browser control disconnects, ChatGPT requests login, or the response cannot be
verified as complete, preserve the bridge task and report the concrete blocker.
Do not fabricate a response, submit the request in another account, or silently
fall back to a different model.

Do not request code or line-by-line debugging unless the user explicitly expands
the advisor's role.

### 10. Resume execution

Give the execution session a concise implementation brief containing the chosen
direction, boundaries, validation requirements, and invalidation conditions.
The execution session then loads its local skills, implements, and validates
continuously.

Send the brief through the exact recorded return route. Verify that the target
task, host, project, and branch still match before delivery. If the original task
no longer exists or moved without a resolvable handoff, keep the answer in the
local bridge task and ask the user where it should continue.

Return to the web advisor only when an invalidation condition occurs or the user explicitly
requests another decision round. Preserve the bridge history so the next request
can explain what changed instead of restarting from scratch.
