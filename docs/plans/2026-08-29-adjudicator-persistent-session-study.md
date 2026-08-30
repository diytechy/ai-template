<!-- Copied verbatim on 2026-08-30 from C:/Projects/ai-template-plans/adjudicator-persistent-session/PLAN.md — the plan of record for the rows that cite it; its companions there (the source reports, the prototype, the drafts, the review transcripts) stay outside the repo. -->

# Persistent adjudicator session — investigation synthesis and plan

Date: 2026-08-29. Repo: `ai-template` @ `contract_split` (read-only during this study; nothing
in the repo was changed). Four opus agents produced the source reports in this folder:

| # | Report | What it settles |
|---|---|---|
| 01 | `01-repo-adjudicator-mechanics.md` | How the adjudicator is launched/briefed/torn down today; every integration point; the rule-3 constraint |
| 02 | `02-claude-code-session-primitives.md` | Claude Code 2.1.201 measured on this box: keep-alive protocol, `/context`, `--resume` cost, compaction dials, hooks |
| 03 | `03-oss-persistent-session-patterns.md` | Reusable OSS designs; Anthropic guidance; the judge-anchoring evidence |
| 04 | `04-codex-opencode-session-capabilities.md` | codex 0.144.4 + opencode 1.18.15 measured: resume, process-alive protocols, telemetry, compaction, Windows |

---

## 1. The answer in one paragraph

Every CLI family the kit routes (claude, codex, opencode) can keep an adjudicator alive across
many adjudications **and** report enough to rotate it at a context threshold — that part is
verified, not assumed (§3). But the premise "one judge that remembers prior work items and
cross-sections their feedback in its own context" collides head-on with the kit's own rule
(`prompts/README.md` rule 3: no prior verdict / no self-assessment as premise) and with the
measured evidence behind it: a 192k-evaluation study found Claude models are the *most*
anchor-susceptible of eight tested (−0.7 points, −22pp acceptance from randomly sampled prior
scores; "ignore prior scores" instructions recover ~7%; chain-of-thought makes it 48% worse).
The design that gets the benefit without the bias is to **persist knowledge, not verdicts**:
the long-lived session per family IS the adjudicator — it retains vision, spine breakdown,
implementation impact and handback/integration patterns (domain knowledge, no measured bias)
and writes depersonalized cross-item findings to an append-only ledger. Each ruling is issued
from a *forked* child (`--fork-session` / `thread/fork` / `/fork`) that inherits everything the
parent knows plus the brief `adjudicate_brief.compose` assembles; the parent gets back only the
typed ledger row, never the verdict prose. The parent is the process that "stays open until
context passes N%"; the fork is what keeps the judge honest. (Owner Q2, §9, settled this
wording; earlier drafts called the parent a "librarian".)

A cheaper first step exists and is worth pricing before anything else (§5, step 0): on the
one measurement taken (a ~40k sonnet session — **not yet at realistic 100k–700k prefixes on the
judge models**, Sol #12) the "re-learning" cost is *process spawn + transcript replay*, not
tokens — Claude Code's 1-hour prompt cache already makes a resumed request cost the same as an
in-process turn (measured $0.013–0.018 vs $0.012–0.018). Resume-per-request keeps every
existing invariant (closed stdin, per-session timeout, tree kill, per-session telemetry) and
loses only ~4.5 s per request.

---

## 2. What exists today (from report 01)

- Launch: `agent-resume.*` → `agent_loop.run_iteration` → `agent_session.run_session:375`
  `Popen`s the family's `cmd_template`, pipes the brief on stdin, **closes stdin** (SN-016
  no-wedge), waits ≤ 7200 s, kills the tree. Telemetry is parsed post-hoc from the final
  `type: result` event (`session_meta:2722`).
- **No** `--resume`, `--continue`, `--session-id`, or session-id capture anywhere.
- Four adjudication classes selected by the WI row's typed `Brief` cell (`amendment`,
  `disposition`, `red-tc` routed; `conflict` held). `adjudicate_brief.compose` is all-or-nothing
  and reads only registries / git ranges / immutable handback reports — the redaction seam.
- Adjudications are already **globally serialized** (`schedule.py:159/177`: exclusive, rank 1),
  so one global adjudicator introduces no new bottleneck — that is the only placement
  compatible with §A1 exclusivity and `_lane_close`'s durability contract.
- Heterogeneity rule (`route_intent:988-996`): the judge's family must differ from the last
  implementer's. A single pinned session cannot satisfy this → the design needs one standing
  session **per family** (or a Claude-only declaration with a one-shot fallback).
- Prior ruling to argue against explicitly: `docs/archive/AGENT_ROLES.md:123-131`
  (owner-confirmed 2026-07-09) dropped the persistent/self-rebooting actor as unnecessary.
  WI-506 (2026-08-23) then found the ~66% restart trigger "not implementable on real context
  accounting for any provider" — **that finding is now superseded** by the measurements in §3.

---

## 3. Capability matrix — verified on this machine

| Capability | claude 2.1.201 | codex 0.144.4 | opencode 1.18.15 |
|---|---|---|---|
| Resume by id, prompt on stdin | ✅ `--session-id <uuid>` (orchestrator mints) / `--resume` / `--fork-session` (measured: memory preserved, $0.013/req) | ✅ `codex exec resume <uuid>` — **rejects `-C`**, set OS cwd | ✅ `opencode run --session <id>` / `--fork` |
| Keep-process-alive protocol | ✅ `-p --input-format stream-json --output-format stream-json --verbose` — idles on stdin, one `session_id`, queued msgs run sequentially, exit 0 on stdin close | ✅ `codex app-server --stdio` JSON-RPC (`initialize` → `thread/start` → `turn/start`…), 2 turns in one process, no approval prompt with `approvalPolicy:"never"` | ✅ `opencode serve` + synchronous `POST /session/{id}/message` (returns text + tokens + cost). **`run --attach` is broken for capture** |
| Per-turn usage | ✅ `result.usage` per turn; `modelUsage[model]` cumulative + `contextWindow` | ⚠️ `exec --json` usage is **cumulative per thread** (diff consecutive values); per-turn `last` + window only in app-server `thread/tokenUsage/updated` or rollout JSONL `token_count` | ✅ `step_finish.tokens{total,input,output,reasoning,cache}` per turn |
| Context-window size | ✅ `modelUsage[<model>].contextWindow` (1,000,000 for sonnet-5; **verify opus on this plan**) | ✅ `modelContextWindow` = 258,400 (default model) | ✅ `GET /config/providers` → `limit.context` (kimi-k3 1,048,576; grok-4.**6** 500,000 — grok-4.5 no longer exists on this install; `docs/agents.toml` slug is stale) |
| Direct "context %" probe | ✅ send `/context` as a user message: 0.6 s, zero tokens, returns `**Tokens:** 39.4k / 967k (4%)` — denominator already net of the 33k autocompact buffer | ❌ compute | ❌ compute (`/api/session/{id}/context` is a message list, not a %) |
| Auto-compaction control | ⚠️ cannot reliably disable; `CLAUDE_CODE_AUTO_COMPACT_WINDOW=<n>` **works** (measured); `PreCompact` hook `deny` is the veto; `--autocompact` flag absent on this build | ⚠️ `model_auto_compact_token_limit` real (strict-config verified) but **capped at 90%, no off switch** | ✅ `compaction.auto=false` fully disables (`autoCompact` does not exist) |
| Bypass on resume | ✅ `--dangerously-skip-permissions` per invocation | ✅ flag re-applied on resume; app-server `sandbox:"danger-full-access"` | ✅ `--auto` per run; **`serve` has no `--auto`** — use `"tools":{"*":false}` on the POST (also cuts prompt 6842→2129 tokens) or `permission:"allow"` in config |
| Cache on re-spawn | 1-hour TTL cache; resume #2 read 40,588 / wrote 33 | ~94% cached on resume | ~98% cached, cost 8× lower on turn 2 |
| Windows | native binary; `newline="\n"`, `encoding="utf-8"`, no `start_new_session` | `codex.cmd` → node shim (two hops) → `taskkill /T /F`; harmless stderr line at startup | `opencode.cmd` → native exe (one hop) |

Two measurement caveats the reports disagree on, resolved:
- **`/context` vs usage-sum.** Report 03 cites claude-code#28167 (`/context` input-only). Report
  02 measured on 2.1.201 that `/context` (39.4k) tracked the usage-sum (40,645) within 3% — on
  ONE ~40k toy session; not resolved for tool-heavy turns or 700k [Sol #7]. Interim rule: record
  both raw components, use `/context` as the Claude probe, cross-check with
  `usage.input + cache_read + cache_creation + output` **against the same absolute budget**, and
  rotate on whichever is higher; enable automatic rotation only after the §6 checks.
- **Threshold.** 70% on the `/context` denominator (already net of the compaction buffer);
  60% if only the arithmetic is available (it runs high). Pair the trigger with a **target**
  (Cline's two-number budget): the successor's seed pack must land ≤ 25% of window or the
  rotation re-fires immediately.

---

## 4. Recommended architecture

### 4.1 Split knowledge from verdict (the load-bearing decision)

```
                 ┌───────────────────────────── per family (ANTHROPIC / OPENAI / OPENCODE) ──┐
                 │  LIBRARIAN session (long-lived, rotates at ctx ≥ 70%)                      │
  rank-1 queue   │   • holds codebase context, conventions, recurring smells                  │
  (schedule.py)  │   • NEVER emits a verdict, never sees a lane's self-assessment             │
      │          │   • appends depersonalized findings → docs/adjudication-ledger.jsonl       │
      │          └───────────────────────────────────────────────────────────────────────────┘
      ▼                                        │ read-only slice (GROUP BY evidence_ref / claim)
  adjudicate_brief.compose(row)  ──────────────┼──►  VERDICT child (fresh or --fork-session)
   (unchanged: registry/git/report-only)       │      rubric + artifact + ledger slice, nothing else
                                               │      → docs/reviews/<n>-ADJUDICATE-<sha7>.md
                                               │      → verdict_refusal / adjudication_bookkeeping
```

- The **librarian** is the "session that stays open until context passes N%". Its context can
  grow freely and rotate lazily because nothing in it is a verdict.
- The **verdict child** is a fork: `--fork-session` (claude) / `thread/fork` (codex) / `POST
  /session/{id}/fork` (opencode) **copies the parent's transcript into a new id**, so the child
  sees everything the parent knows (that is the retention) and shares its cache prefix; what the
  fork buys is that **the parent never sees the child's output**. Fork semantics were verified
  only as flag/endpoint presence (reports 02/04) — the canary test in §6 must prove them before
  this is relied on. [Sol review #1]
- **How the parent learns without re-importing outcomes** [Sol #5]: the child emits two
  artifacts — the verdict (to the orchestrator only) and a *knowledge note* in a schema that has
  no outcome fields (no verdict, severity, WI lineage, disposition), validated by script. The
  orchestrator — never the model — appends it to the knowledge store and feeds it to the parent
  on its next turn. Persisted knowledge is limited to provenance-bearing, as-of-commit facts
  (architecture, conventions, spine structure); lane-specific "recurring smells" are treated as
  potentially anchoring until measured otherwise [Sol #2]. The store is family-neutral and
  authoritative; the three per-family sessions are disposable caches of it [Sol #21].
- **Cross-item feedback** lives in TWO append-only stores, not chat history [Sol #3 — the
  earlier single ledger with a `verdict` column would have fed every verdict back to the parent]:
  1. **Outcome log** (`id, wi, ts, judge_session, rubric_version, outcome, evidence_ref`) —
     orchestrator-only; never read by the parent or a child except through the typed
     `{prior_verdicts}` brief slot when a multi-round brief explicitly asks for it (WI-506).
  2. **Knowledge store** (`id, ts, as_of_commit, kind, claim, evidence_ref, cross_refs[]`) —
     no verdict, severity, WI lineage or disposition fields; what the parent and children read.
  The orchestrator is the only writer (deterministic ids, lock + fsync, one JSONL line per
  record, never rewritten) [Sol #19]; a *derived* cross-cutting view is regenerated by script
  from explicit normalized keys — matching the repo's derived-not-hand-maintained idiom.
- The WI-506 banked idea — a typed `{prior_verdicts}` slot for multi-round rows — is the
  sanctioned door for the one case where history is *wanted*; it stays an explicit assembled
  field, never implicit carry-over.

### 4.2 Transport: LCD baseline + one adapter

**Baseline (all three families, ~120 lines stdlib):** re-spawn per request, resume by session
id, prompt on stdin, orchestrator-side token accounting. Keeps every current invariant. Costs
~4.5 s/request on claude, comparable elsewhere.

| | claude | codex | opencode |
|---|---|---|---|
| seed | `claude -p --session-id <uuid> …` | `codex exec --json … -o <f>` → capture `thread.started.thread_id` | `opencode run --format json …` → capture `sessionID` |
| next | `claude -p --resume <id> --output-format stream-json --verbose --dangerously-skip-permissions` | `codex exec resume <id> --json --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox -o <f>` (cwd = repo, **no `-C`**, **no `--ephemeral`**) | `opencode run --session <id> -m <model> --auto --format json --dir <abs>` |
| used | max(`/context`, usage-sum) | `usage.input_tokens[n] − [n−1]`, or rollout `token_count.info.last_token_usage.total_tokens` | `step_finish.tokens.total` |
| window | `modelUsage[init.model].contextWindow` | rollout `model_context_window` | `GET /config/providers` `limit.context` |

**Process-alive upgrade (latency only), build in this order if the baseline's spawn cost
matters:** (1) opencode `serve` — HTTP+JSON via `urllib`, ~30 lines, clearly better than its
own re-spawn — launched with a random `OPENCODE_SERVER_PASSWORD` and a random loopback port
(report 04 observed it unsecured by default) [Sol #14]; (2) claude bidirectional stream-json — a `Session` object beside (not replacing)
`run_session`, since IF-064's declared contract is "stdin fed then closed"; (3) codex
`app-server` — best telemetry, but a JSON-RPC client to write; do last or skip.

Define the five-verb interface once (`prompt`, `wait`, `context`, `compact`, `interrupt` —
opencode's API is the reference) with three adapters behind it.

Isolation note: session state is global per home — `CODEX_HOME` (codex), `CLAUDE_CONFIG_DIR`
(claude), opencode's equivalent unverified — give the orchestrator a dedicated home per family,
private permissions, and a retention/size policy for transcripts (forks multiply them) [Sol #16].
codex specifically: Give the orchestrator a
dedicated `CODEX_HOME` so `exec resume --last`, `thread/list` and the rollout-file telemetry
cannot collide with an owner's interactive codex sessions on the same box (observed during the
study: an unrelated `codex exec -m gpt-5.6-sol` shared the default home with the probes).

### 4.3 Rotation policy (the librarian)

Define **one absolute token budget per detected window** (`modelUsage[...].contextWindow`,
codex `modelContextWindow`, opencode `limit.context`) and derive everything from it: rotate at
0.70 × budget, set the provider's compaction point at ≥ 0.90 × budget. (Setting
`CLAUDE_CODE_AUTO_COMPACT_WINDOW` changes `/context`'s denominator — report 02 — so "70% of
`/context`" with an 800k window meant 560k, not 700k.) [Sol #6]

Rotate when **any** of:
- occupancy ≥ 0.70 × budget;
- `system/init.claude_code_version` ≠ `claude --version` (auto-updater replaced the binary);
- the **hash of the governing inputs** changed — CLAUDE.md, AGENTS.md, the skills the judge
  loads, `docs/process.toml`, the rubric templates. NOT `HEAD`: HEAD moves on every merge, so
  rotate-on-HEAD would fire once per adjudication and delete the persistence [Sol #10].
  Knowledge facts carry an `as_of_commit` and are invalidated selectively;
- (claude) NOT idle time — keep the cache warm instead: a trivial API ping every ~50 min costs
  ~0.1× prefix, a cold 1h-cache rewrite ~2× prefix (≈ 20 pings). Worker gaps > 1 h are normal,
  and the session's memory survives any gap — only the next request's price changes;
- any `result.is_error` / `terminal_reason ≠ "completed"`; a `PreCompact` hook fired;
- the 12:00–19:00 UTC blackout: do not **start** a turn within one worst-case turn duration of
  12:00; whether an in-flight turn may overrun or is interrupted (with the row's HOLD report
  written) is an owner ruling [Sol #17].

Rotation is **graceful and appended**, driven by a durable per-family generation record with
lock/CAS transitions `active → draining → retired → successor-active`, so a heartbeat, a
version watch and a timeout cannot each mint a successor [Sol #18]: mark draining → finish the
in-flight turn → close stdin (exit 0) → write a `rotation` record (reason, session_id,
predecessor link, occupancy) → start the successor. **The successor re-warms only the static
prefix** (system prompt + CLAUDE.md, ~30–40k); its seed pack is a cold cache write — budget
that cost and latency rather than assuming full reuse [Sol #11]. Keep the predecessor
transcript; the seed pack is a derived artifact (Anthropic keep/discard list: keep decisions and
open threads, drop raw tool output) built in tiers (rubric + architecture first, open threads
next, patterns last) so an overshoot of the 25% target prunes deterministically and only a
below-minimum pack raises a per-row HOLD, never an unbounded rotation loop [Sol #23].

Provider compaction is set so the kit's policy always fires first: claude
`CLAUDE_CODE_AUTO_COMPACT_WINDOW=800000` + `PreCompact` deny hook; codex
`model_auto_compact_token_limit` ≈ 90%; opencode `compaction.auto=false`.

### 4.4 Invariants the design must re-establish (from report 01 §c)

| Today | Persistent form |
|---|---|
| SN-016 no-wedge: stdin fed then closed | per-**turn** timeout on the result queue + liveness probe + tree kill; baseline transport keeps the original |
| `--session-timeout 7200` per session | per-turn bound **and** an absolute process bound |
| one fresh `docs/reviews/<n>-ADJUDICATE-<sha7>.md` per session | one per **adjudication** (planted-verdict defence) |
| `adjudication_bookkeeping` at process exit | after every verdict |
| `session_meta` per process | synthesized per-turn rows (or a new grouping in `regenerate_index`) |
| HOLD → `EXIT_NEEDS_HUMAN` → `_lane_close` report + blockref | per row, not per process; an abandoned row on rotation still gets its report |
| `tests/test_prompts.py:185` pins the brief template | a canary test: plant prior verdicts / self-assessments in every channel (transcript, ledger, files) and prove they are absent from the child's request (carried history is invisible to a template test) [Sol #20] |
| brief-level redaction; the model can still read `docs/reviews/*`, handbacks, iteration logs (**pre-existing** in the one-shot design) | narrow the tool surface: opencode `tools:{"*":false}`, claude `--disallowedTools` / a staged read-only evidence dir; deny transcript/review/outcome-log paths [Sol #4] |
| session writes and commits its own verdict (the `adjudicate-*` templates require it) | owner ruling: keep, or have the orchestrator write/commit so the judge needs no write or shell access during a multi-hour bypass session [Sol #15] |
| — | request journaling before submit, idempotent verdict paths and finding ids, reconcile transcript vs journal on restart — a crash after model completion but before verdict write / bookkeeping must not duplicate or lose a ruling [Sol #9] |

---

## 5. Sequenced plan

> **Superseded 2026-08-29 by owner decision — see `PLAN-OPTIN-LAYER.md`.** The layer ships
> as a `docs/process.toml` dial (`[adjudicator] context_reset_pct`, `0` = today's behaviour)
> using resume-by-id per adjudication (no persistent process), resetting the session ahead
> of provider compaction. The A/B gate (3b) is dropped; the owner's earlier extreme-usage run
> is the evidence. The steps below remain the reference for the hardening path.

Each step is a separate WI/OI candidate; none is started while `docs/work/pause` exists.

0. **Measure before building (no code).** From `docs/iteration/*.log` ADJUDICATE rows, read
   `cache-read` vs `cache-create` and `wall-secs − api-secs`. If cache hits are already high,
   the observed "re-learning" is spawn/replay latency and step 1 alone may be enough.
1. **Capture session ids + context telemetry in the existing one-shot path** (smallest change,
   independently useful): `session_meta` gains `session_id`, `context_used`, `context_window`,
   `context_pct` per family (formulas in §3/§4.2). Fix the stale `opencode-go/grok-4.5` slug
   in `docs/agents.toml` (install has grok-4.6). Adds columns to the iteration index.
2. **Owner rulings needed (OI):** (a) reverse the 2026-07-09 "no persistent actor" ruling *with
   this evidence*; (b) consent model for a multi-hour `--dangerously-skip-permissions` process;
   (c) rotation threshold as a `docs/process.toml` dial; (d) Claude-first vs three-family from
   day one; (e) are the outcome log / knowledge store new registries (schema, trace) or
   log-shaped surfaces? Added after the Sol review [#24]: (f) blackout overrun policy; (g) may
   the judge execute tools / write files, or does the orchestrator write and commit verdicts;
   (h) what knowledge is safe to persist (stable facts only vs lane patterns); (i) transcript
   retention/privacy; (j) acceptable p95 latency and cost per adjudication; (k) queue owner and
   coordinator-lock lifetime for a standing session.
3. **Ledger + derived view** (`docs/adjudication-ledger.jsonl` + `gen_*` derived TOML/dashboard
   section) — the cross-item mechanism, usable even with zero persistent sessions. The
   `{prior_verdicts}` slot (WI-506 banked) is built here as an explicit assembled field.
3b. **Gate before any persistence [Sol #22]:** A/B on real adjudication rows — (fresh
   child + knowledge-store pack) vs (forked child of a standing parent) — measuring verdict
   agreement with owner rulings, p50/p95 wall time, billed tokens, cache reads/writes at
   realistic prefix sizes. If the fresh-child arm is not materially worse, **stop at step 3**:
   the knowledge store alone delivers the retention and there is no session to keep open.
4. **Baseline transport** (only if 3b favours persistence): resume-by-id adapters for the three families as a sibling of
   `run_session` (IF-064 unchanged), driven by a `context_pct` rotation rule; librarian/verdict
   split via `--fork-session` / `thread/fork` / `/fork`. New interface row(s) in
   `docs/requirements/interfaces.toml`; tests listed in report 01 §7 extended, not rewritten.
5. **Process-alive adapters** only if step 0/4 show spawn latency matters: opencode `serve`
   first, claude stream-json second, codex app-server last.
6. **Contamination canary + bias test**: plant prior verdicts and self-assessments in each
   channel (parent transcript, outcome log, files) and prove by request inspection that the
   child's input lacks them [Sol #20]; separately, a 100–300 case set run twice with order
   swapped for position bias.

---

## 6. Verify empirically before trusting the threshold (from reports 02/04)

1. Behaviour at the ceiling: `CLAUDE_CODE_AUTO_COMPACT_WINDOW=100000`, drive past it, confirm a
   `PreCompact` deny actually blocks on 2.1.201 and what `/context` reads afterwards — **the
   single most important untested assumption**.
2. `modelUsage["claude-opus-5"].contextWindow == 1000000` on this account (Opus 1M is
   plan-gated; a silent 200k would make 70% fire 3.5× late). All Claude measurements used sonnet.
3. A real adjudication (not a PONG) — how many tokens one consumes sizes the headroom above 70%.
4. Idle > 1 h → next request's `cache_creation_input_tokens` (prices the rewrite the ~50-min ping avoids); same test on codex/opencode to learn their real TTLs.
5. Rotation under load: successor's first turn hits the warm cache.
6. codex/opencode cache TTLs (minutes, unstated) — same idle test per family.
7. **Fork semantics per family** [Sol #1]: plant a canary in the parent, fork, confirm the child
   reproduces it (retention) and that the child's turns never appear in the parent's transcript
   or requests (isolation).
8. Telemetry on long tool-using turns (many steps), after compaction, after resume and after a
   fork — confirm the "last step = occupancy" rule holds [Sol #8].
9. Realistic-prefix benchmark (100k–700k, opus/kimi/sol): resume replay time, fork cost, TTFT,
   cache writes, rate-limit incidence, p50/p95 [Sol #12].

---

## 7. Reuse shortlist (from report 03)

1. usage-sum meter + ccstatusline window resolution (MIT) — ~30 lines stdlib, build first.
2. OpenHands condenser contract (`keep_first` / `max_size` / `attention_window`; rotation
   recorded as an *event*, view derived by applying it).
3. Cline's two-number budget (`triggerTokens` + `targetTokens`).
4. CodeRabbit "Learnings" as the ledger model (scoped, retrieved-not-accumulated).
5. opencode's five-verb session API as the adapter interface.

Deliberately not reused: `claude-agent-sdk` (PyPI dep + asyncio foot-guns), claude-code-router
(routing, not lifetime), claude-squad (AGPL), Letta (heavy runtime), claude-code-parser (1★,
stale — read its protocol doc only).

---

## 8. Honest tensions to keep in view

- Anthropic's own long-running-agent guidance reaches for `claude-progress.txt` + fresh contexts,
  not long-lived sessions; Ralph-style loops treat fresh context as a feature. The kit's current
  one-shot adjudicator *is* that design. A persistent session is an **optimization that can be
  switched off**, not a correctness dependency — the ledger must carry the memory.
- The strongest evidence in the study cuts against the original premise: a judge that remembers
  its verdicts judges worse, and prompting cannot fix it. The librarian/verdict split is what
  makes the persistent session compatible with the kit's own rule 3.

---

## 9a. Adversarial review (gpt-5.6-sol, medium) — 2026-08-29

`review-sol-medium.md` (24 findings) and `review-sol-medium.response.md` (per-finding
confirm/partial/refute with the edits made). Confirmed and folded in: the single ledger leaked
verdicts back to the parent (#3, now two stores); rotate-on-HEAD would have fired every merge
(#10); the successor does not re-warm its seed pack (#11); fork wording (#1); Opus pricing (#13);
opencode serve password (#14); absolute token budget (#6); blackout/rotation state machine
(#17/#18); an A/B gate before building persistence (#22). Refuted: #8's specific claim. Sol's
overall verdict — prove the fresh-session + knowledge-store baseline first — is adopted as §5 3b.

## 9. Owner questions, 2026-08-29

**Q1 — Is the prompt cache per session? Does a new CLI call open a new session? Must we ping?**
Two things share the word: the Claude Code *session* (transcript + id) and the API *prompt cache*
(server-side, keyed on the exact request prefix, org-scoped — not per process or session). A new
`claude -p --resume <id>` (or `--session-id <uuid>` minted on the first call) is a new process that
replays the chosen transcript, so the prefix matches and the cache hits (measured: resume #2 read
40,588 / wrote 33). codex `exec resume <id>` and opencode `run --session <id>` behave the same.
The cache breaks only when the prefix changes — an edit to CLAUDE.md/settings/tools between calls
→ near-full rewrite; hence the rotate-on-HEAD-moved rule. TTL 1 h, refreshed on every API hit;
`/context` is local and does NOT refresh. Pinging works mechanically on all three families (resume
by id + a trivial message); whether it PAYS depends on TTL. claude: ping ≈ 0.1× prefix, cold
1h-cache rewrite ≈ 2× prefix → one rewrite ≈ 20 pings, so ping every ~50 min through any gap up to
~20 h (Opus 5 at $5 in / $10 1h-write / $0.50 cache-read per MTok: a 300k-prefix rewrite ≈ $3 vs
≈ $0.15/ping — corrected from Fable prices, Sol #13). codex/OpenAI and opencode-go caches
live minutes, with cached reads at 0.1× and no write surcharge — keeping them warm would need a
ping every ~5 min (≈1.2× prefix/hour > one 1× rewrite), so don't ping; accept one uncached read
after a long gap (kimi-k3 200k prefix ≈ $0.60). OpenAI's 24 h `prompt_cache_retention` option is
NOT verified as exposed by codex — check `codex features list` / config. In every family the
adjudicator's memory survives a gap of any length (the transcript is on disk; resume replays it);
a worker gap > 1 h changes only the price of the next request, never what the judge knows.

**Q2 — The adjudicator should retain integration/handback context (the arbiter handles conflicts).**
Agreed. The split in §4.1 is restated: the long-lived session IS the adjudicator, holding vision,
spine breakdown, implementation impact and handback patterns — *domain knowledge*, which carries no
measured bias. The narrow hazard is its *own prior verdicts* and the judged lane's self-assessment
(the disposition → successor chain; WI-418). So each ruling is issued from a `--fork-session` child
(codex `thread/fork`, opencode `/fork`) that inherits everything the parent knows + the brief; the
parent receives back only the typed ledger row (the WI-506 `{prior_verdicts}` slot), never the
verdict prose. Role, visibility and the arbiter/adjudicator division are unchanged. Fallback
without forks: partition by artifact — rotate to a fresh session before any row whose WI or
predecessor chain has a verdict in this session's history (simpler, more rotations, leakier).
