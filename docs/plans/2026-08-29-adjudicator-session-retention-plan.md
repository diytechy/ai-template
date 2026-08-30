<!-- Copied verbatim on 2026-08-30 from C:/Projects/ai-template-plans/adjudicator-persistent-session/PLAN-OPTIN-LAYER.md — the plan of record for the rows that cite it; its companions there (the source reports, the prototype, the drafts, the review transcripts) stay outside the repo. -->

# Adjudicator session retention — the opt-in layer

Date: 2026-08-29. Owner decision (this date): design it as an **opt-in layer** with a single
dial, `0` = today's behaviour byte-for-byte. Motivation recorded from the owner: in a prior run
the adjudicator was spun up for every small work item, relearned and reloaded the spine and the
surrounding items each time, and usage was extreme; when a session *was* kept, its context
filled quickly (it needs the full spine plus neighbouring items) and the choice was compaction
(poor quality) or a full reload (the same tokens again). The layer must protect against both:
**retain context that would otherwise be reloaded, and reset the session ourselves before the
provider compacts.** Online guidance places session degradation past ~60%; the dial lets the
owner sit below that.

Supersedes the sequencing in `PLAN.md` §5 (the A/B gate is dropped by owner decision; the
mechanics, matrix and Sol-review corrections in `PLAN.md` still apply and are referenced).

---

## 1. Shape in one paragraph

Every adjudication is still **one bounded headless process** exactly as today — same
`run_session`, same closed stdin, same 7200 s timeout, same tree kill, same per-session
telemetry. The only difference when the dial is on: the process is launched with the family's
*resume* form (`claude -p --resume <id>` / `codex exec resume <id>` / `opencode run --session
<id>`) against a session the orchestrator minted earlier, so the model arrives already holding
the spine and the prior work items. After each adjudication the orchestrator reads that
family's occupancy from the process's own telemetry; when `occupancy ≥ dial` the session is
marked draining and is retired at the next **clear point** (idle, waiting on workers, no chain
of its own in flight) — the adjudication after that starts a fresh session, which is precisely
today's path. No long-lived process, no open stdin, no heartbeat process, no new consent
proposition: the invariants SN-016 (no-wedge), the walk-away timeout and IF-064's contract are
untouched. The dial sits below the provider's compaction point so the reset normally fires
first; if a long chain crosses it anyway, compaction is the backstop and is logged, not fought.

---

## 2. The dial

`docs/process.toml` (process policy, per `process.toml:1-20`; `stack.ini [agent-loop]` is
toolchain):

```toml
[adjudicator]
# Percent of the model's context window at which the retained adjudicator session is
# RESET (a fresh session replaces it). 0 = off: every adjudication is a fresh session,
# today's behaviour. Owner's reference point: degradation reported past ~60%.
context_reset_pct = 0            # e.g. 55

# Retain the session across these adjudication classes only (Brief cell values).
# Rows minted with no brief (clean-close spot checks) follow the same rule.
retain_for = ["disposition", "amendment", "red-tc"]

# ANTHROPIC only: keep the 1-hour prompt cache warm while the rank-1 queue is non-empty
# or a lane is active. Minutes between keep-warm calls; 0 = off. (Other families' caches
# live minutes — never pinged; they pay one uncached read after a long gap.)
keepwarm_minutes = 0             # e.g. 50

# Rule-3 guard: reset before judging a row whose WI, or whose predecessor chain, already
# received a verdict in the retained session ("partition by artifact"). Default false —
# the owner's stated purpose for the layer is continuity across a worker round-trip on the
# SAME item (judge -> worker acts -> worker returns -> judge again), which this guard would
# defeat. true restores the strict rule-3 posture at the cost of that continuity.
reset_on_same_artifact = false
```

**Cresting is not closing.** Reaching `context_reset_pct` marks the session `draining`; the
reset itself happens only at a **clear point** — when the adjudicator is idle waiting on
workers, not mid-way through a chain of feedback (owner clarification 2026-08-29; §3.4).

Semantics the tests must pin:
- `context_reset_pct = 0` → the whole layer is inert: no session ids minted, no resume argv,
  no occupancy computed beyond today's telemetry columns. `tests/test_dogfood_sync.py`
  structure parity: the template ships the table with `0`.
- `context_reset_pct` is kept **below the provider's compaction point** so that, in the
  normal case, the kit's reset fires first: claude — `CLAUDE_CODE_AUTO_COMPACT_WINDOW` left at
  the model window (compaction ~967k, far above any sane dial); codex — its own
  `model_auto_compact_token_limit` (≤ 90% cap) is the backstop, so a dial above 85 is clamped
  to 85 with a logged warning; opencode — `compaction.auto` left ON as the backstop (setting it
  false would turn an oversized turn into a hard overflow error instead). **No `PreCompact`
  deny hook and no reset-on-compaction** (owner, 2026-08-29): if a turn genuinely needs more
  context than remains, compaction is inevitable and a forced reset would only replay the same
  cost to reach the same place; if something else caused it, a reset doesn't fix that either.
  A compaction is *logged* (`compacted = true` on the session row, from the stream's
  `compact_boundary` / codex `thread/compacted` / opencode summarize event) so the owner can
  see how often the backstop is hit and lower the dial if it is.
- The dial is a **percent of an absolute budget** per detected window (Sol #6): claude
  `modelUsage[<init.model>].contextWindow`, codex `model_context_window` from the rollout /
  app-server, opencode `limit.context` from `/config/providers`; a config table is the
  fallback and a mismatch (e.g. opus reporting 200k on this plan) is logged, never guessed.

---

## 3. Mechanics

### 3.1 Session store (runtime state, untracked)

`out/adjudicator/<FAMILY>.json` (location for the WI to settle; must be gitignored and
per-checkout, like `ctx.raw_dir`):

```json
{"family":"ANTHROPIC","route_id":"ANTHROPIC-OPUS-STRONG","session_id":"<uuid>",
 "generation":3,"started":"2026-08-29T18:02:11Z","governing_hash":"<sha>",
 "window":1000000,"occupancy":412345,"pct":41,
 "judged":["WI-530","WI-531"],"last_used":"…","state":"active"}
```

`state` ∈ `active | draining | retired`; transitions are written atomically (write-temp +
`os.replace`) under the existing coordinator lock, so a keep-warm tick and an adjudication
cannot both mint a successor (Sol #18).

### 3.2 Launch — the per-family resume form

The one-shot templates in `docs/agents.toml` stay untouched. A small adapter keyed on
`family` derives the resume argv from the row's `cmd_template` (no schema change, so no
downstream migration):

| family | first use (mint) | subsequent (resume) | prompt |
|---|---|---|---|
| ANTHROPIC | append `--session-id <uuid4>` | replace with `--resume <id>` | stdin (unchanged) |
| OPENAI | unchanged; capture `thread.started.thread_id` (`--json`) | `codex exec resume <id> --json …` — **no `-C`** (cwd = repo), **no `--ephemeral`** | stdin |
| OPENCODE | add `--format json`; capture `sessionID` | add `--session <id>` | stdin |

`build_argv` keeps its `(argv, stdin_input)` contract (IF-064); the adapter runs *before* it,
rewriting the template string. Session-id capture is a new `session_id` column in
`session_meta` (also useful with the dial off — step 1 in `PLAN.md` §5).

### 3.3 Occupancy after each adjudication (from the process's own output)

| family | occupancy | source |
|---|---|---|
| ANTHROPIC | `usage.input + cache_read + cache_creation + output` of the final `result` | already parsed by `session_meta` |
| OPENAI | `token_count.info.last_token_usage.total_tokens` — last such event in `~/.codex/sessions/**/rollout-*-<id>.jsonl` (`exec --json` usage is cumulative; diff it as the fallback) | rollout file under the orchestrator's `CODEX_HOME` |
| OPENCODE | last `step_finish.part.tokens.total` | `--format json` stream |

`pct = occupancy / window`. Optional claude cross-check: a `claude -p --resume <id>` call
whose stdin is `/context` (zero tokens, ~5 s) — use the higher of the two (Sol #7). Verify the
"last step = occupancy" rule on long tool-using turns before trusting automatic reset (Sol #8).

### 3.4 Drain and reset (evaluated after every adjudication and before every launch)

Two steps, because the owner wants the adjudicator to close **at a clear point**, not the
moment it crests:

**Mark `draining`** when any of:
1. `pct ≥ context_reset_pct`;
2. the governing-inputs hash changed (CLAUDE.md, AGENTS.md, loaded skills,
   `docs/process.toml`, the `adjudicate-*` templates) — **not `HEAD`** (Sol #10);
3. CLI version drift (`system/init.claude_code_version` ≠ `claude --version`; `--version`
   for the others).

**Retire** a `draining` session — i.e. the next launch is fresh — at the first **clear
point**: no adjudication row in the rank-1 queue belongs to a chain this session is already
inside (a successor / handback of a row it judged), and no active lane is out on work whose
close will mint such a row. In practice: *the adjudicator is waiting for workers, with nothing
of its own pending.* Until then a draining session keeps being resumed for the rows that
continue its chains, so a review → worker → return → review loop is never cut mid-way. The
provider's own compaction is the backstop if a chain runs long past the dial (§2); that is
logged, not fought.

**Retire immediately** (no drain) when the session is unusable rather than merely full:
4. `result.is_error` / `terminal_reason ≠ "completed"` / timeout — corrupt or lost;
5. `reset_on_same_artifact = true` and the next row's WI or predecessor chain ∈ `judged`.

A route change (the heterogeneity rule drew a different family/model) is a lookup miss —
sessions are per `route_id` — not a reset.

The reset is **just "next launch is fresh"** — today's behaviour. No seed pack in this layer:
CLAUDE.md, AGENTS.md and the skills reload automatically, the brief is assembled fresh as
always, and the ~30–40k static prefix is served from the prompt cache. (A derived seed pack is
a later enhancement; `PLAN.md` §4.3 has the tiered design if wanted.)

### 3.5 Keep-warm (ANTHROPIC only, `keepwarm_minutes > 0`)

A scheduled tick in the dispatcher loop: if the family's session is `active`, the rank-1
queue is non-empty or any lane is active, and `now − last_used ≥ keepwarm_minutes`, run
`claude -p --resume <id> --max-turns 1` with stdin `ack` (a real API call: ~0.1× prefix, e.g.
≈ $0.15 on a 300k opus-5 prefix vs ≈ $3 for the 1-hour-cache rewrite it avoids — `PLAN.md`
§9). It is a bounded process like any other; its result updates `occupancy` and `last_used`.
Skipped inside the blackout unless the owner rules otherwise (Sol #17).

### 3.6 Rule 3 in this layer

The owner's purpose for this layer is continuity across a worker round-trip on the **same**
item, so `reset_on_same_artifact` defaults to `false` and the retained session *will* hold its
prior verdict on the artifact it judges next — the disposition → successor chain WI-418
measured and the anchoring study (`PLAN.md` §1) quantified. This is the owner's accepted
residual, taken with eyes open; `reset_on_same_artifact = true` restores the strict posture
per adopter. The brief-level redaction (rule 3 on the assembled brief) is unchanged either way. The fork-per-verdict + outcome-log/knowledge-store design in `PLAN.md`
§4.1 remains the hardening path if that residual ever shows up in review quality; it layers on
top of this without changing the dial.

---

## 4. Integration points (each maps to `PLAN.md` §4.4 / report 01 §b)

| Where | Change |
|---|---|
| `docs/process.toml` + `project-trajectory/process.template.toml` | the `[adjudicator]` table (values may differ, structure must not) |
| `agent_common` config reader | parse + validate the table; clamp per family; `0` short-circuits |
| new `adjudicator_session.py` (stdlib) | session store, resume-argv adapter, occupancy readers, reset rule, keep-warm tick |
| `agent_loop.route_session` | for `adjudicating(row)`, ask the adapter for the argv (mint or resume) and env (`CLAUDE_CODE_AUTO_COMPACT_WINDOW`, `CODEX_HOME`, `OPENCODE_CONFIG`) |
| `agent_loop.session_meta` / `write_session_log` / iteration index | new columns: `session_id`, `context_used`, `context_window`, `context_pct`, `session_gen`, `reset_reason` |
| `agent_loop.session_bookkeeping` | after `adjudication_bookkeeping`: update store, evaluate reset rule |
| `dispatch.py` tick | keep-warm scheduling; blackout awareness |
| `agent_session.run_session` | **unchanged** (IF-064 holds) |
| `adjudicate_brief.compose` / `session_body` | **unchanged** (the redaction seam) |
| `docs/requirements/interfaces.toml` | one new IF row for the session store + adapter; `docs/registry-machinery-reference.md` and `docs/enforcement-audit.md` rows |
| `RESYNC_PACK.md` | entry: new optional table, default off — no adopter migration |
| `.gitignore` | `out/adjudicator/` |

Tests: extend, not rewrite — `tests/test_session_stdin.py` (build_argv contract untouched;
adapter tested separately), `tests/test_agent_loop.py` telemetry columns, new
`tests/test_adjudicator_session.py` (dial 0 inert; clamps; reset rule table; same-artifact
guard; store atomicity; per-family occupancy parsing from captured fixtures),
`tests/test_dogfood_sync.py` template parity, `tests/test_prompts.py` unchanged.

---

## 5. Sequenced work (each a WI; none starts while `docs/work/pause` exists)

1. **Telemetry first, dial off** — session-id capture + occupancy/window/pct columns per
   family; fix the stale `opencode-go/grok-4.5` slug (install has grok-4.6). Independently
   useful: it shows how full today's one-shot adjudications already get.
2. **Owner rulings (one OI):** (a) reversal of the 2026-07-09 "no persistent actor" ruling on
   the strength of the owner's own usage experience — note this layer needs no persistent
   *process*, only a retained *session*; (b) confirm the rule-3 residual in §3.6 (`reset_on_same_artifact = false` by default,
   continuity over independence on the same item) — or require the fork hardening from day one; (c) blackout behaviour for keep-warm; (d) dial home confirmed
   as `process.toml`; (e) dedicated homes (`CODEX_HOME`, `CLAUDE_CONFIG_DIR`) for the
   orchestrator.
3. **The layer** — `adjudicator_session.py` + config + route_session hook + tests, shipped
   with `context_reset_pct = 0`.
4. **Verify on this box before flipping the dial** (from `PLAN.md` §6): opus window on this
   plan (200k vs 1M); behaviour at the compaction ceiling with `AUTO_COMPACT_WINDOW` low and
   the `PreCompact` deny hook; occupancy on a real multi-step adjudication; codex/opencode
   cache TTLs; resume replay time at 100k–700k.
5. **Enable** — owner sets the dial (e.g. 55) in `docs/process.toml`; watch `context_pct` and
   `reset_reason` in the iteration index for a week; the memory of the earlier extreme-usage
   run is the baseline to compare `tokens`/`cost-usd` per adjudication against.
6. Later, optional: seed pack on reset (`PLAN.md` §4.3), fork-per-verdict (`PLAN.md` §4.1),
   process-alive adapters if the ~4.5 s spawn ever matters.

---

## 6. What this layer does NOT do (deliberately)

- No long-lived process, no open stdin, no HTTP server — so no new consent question, no
  wedge risk, no rotation state machine beyond the store's three states.
- No fight with compaction: the dial sits below the provider's compaction point so the reset
  normally wins; when a long chain crosses it anyway, compaction is the backstop and is
  logged, never answered with a forced reset (which would only replay the same cost).
- No mid-chain cuts: cresting marks `draining`; retirement waits for a clear point (§3.4).
- No cross-family shared memory: sessions are per `route_id`; the family drawn by the
  heterogeneity rule gets its own retained session.
- No change to which evidence a judge is briefed with.
