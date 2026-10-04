# Chapter 2: sessions, routing and accounts (including U1)

Part of WI-788's half-1 design note ([README.md](README.md)). Lane `wi-788`, base `c3be7be0`, written
2026-10-04; code cites are repo-relative `path:line` at the base (`scripts/`
means `project-trajectory/scripts/`).

**Siblings.** [1](1-state-evidence-recovery.md) owns `lane_state`, [3](3-planning-tiering.md)
the plan protocol, and [4](4-adjudication-mint-landing.md) the station authority,
mint and landing check.

**This chapter owns** `ask(kind, ...)`, the session families, the session store,
accounts and homes, the routes, and U1.

## 1. What the probes settled (this box, 2026-10-04)

| Question | Finding | Consequence |
|---|---|---|
| claude 2.1.289: resume by id from another directory | Works. The answer is remembered, the id is kept, and the turn runs in the new `cwd`. The transcript stays in the first directory's `projects/<slug>/` file. | A retained claude session needs no fixed directory. LS10's expectation is refuted for this version. |
| codex 0.160.0: `exec resume <id>` from another directory | Works. The rollout records both `cwd`s. `--last` filters by cwd; resuming by id does not. `resume` takes no `-s`. | Resume by id only. |
| opencode 1.18.30: `run --session <id>` from another directory | **Hangs.** The turn runs in the session's own directory, but stdout stays empty and the process never exits (exit 124, twice). It works from the same directory, and with `--dir <that directory>`. | An opencode session is bound to its directory. Its retention resets when the call's directory differs (§2). |
| A custom endpoint through a scratch `OPENCODE_CONFIG` | `opencode models freellmapi` lists `freellmapi/auto`. Without the config it fails with `Provider not found`. A run fails at the connection to `127.0.0.1:3001`, not at config. | The per-route config mechanism is verified. The end-to-end FreeLLMAPI call is **UNVERIFIED**: there is no endpoint or key on this box. |
| opencode account isolation | `XDG_DATA_HOME` moves `auth.json`, the session database and the logs (`opencode debug paths`). | opencode's home variable is `XDG_DATA_HOME`, plus `OPENCODE_CONFIG`. |
| Usage after a hard kill | `opencode export <id>` gives the directory and per-message `tokens`. The claude transcript and the codex rollout carry per-request usage. | Usage is recoverable by session id (§6). |

## 2. Session families and reset terms

A **session family** is a class of calls that share one retention slot and one
independence rule. **Reset terms** are the declared conditions under which the
next call starts a fresh session. "Every call" is a value of the terms, not a
second path.

Every retained family keeps today's terms:
- crest of the dial, then drain and retire at a clear point;
- a governing-input change;
- a CLI version change;
- an unusable session;
- a lease that expired unreleased.

These rules are at `scripts/session_keep.py:365-383`, `:475-513` and `:673-675`.

| Family | Kinds | Retained | Slot | Added reset terms | Independence |
|---|---|---|---|---|---|
| [plan and build] | plan, build | Capability built. Shipped default: every call. This repo: every call. | per lane (per drafter in a dual round, [chapter 3 §4.3](3-planning-tiering.md#4-design)) | The lane is archived, or the work item changes. | None of its own: it is the author that others are judged against. |
| [adjudicate] | adjudicate, author | **Shipped: retained** at `context_reset_pct = 55`. This repo: stays 0. | station | The same-artifact guard, default off (OI-69 (b)). | Never judges a scope its own session authored. The exception is the final pass (OI-101 Q1, B10): it approves only if it changed nothing. |
| [adjudication review] | author-review, the post-act final review | Retained, at the same dial. | station | As [adjudicate]. | Never the adjudicator's session, and preferably another family. Never reviews a range it authored. |
| [review] | review (REVIEW-A/B, CRITIQUE), plan-critique | No: every call, fixed. | none | none | Never a recorded author of the scope. REVIEW-B's family differs from REVIEW-A's where the pool allows. The relaxed draw stays SR-154's recorded degraded case. |
| [judge] | judge (observation re-judge, DESIGN-CHECK); arbitrate only if the owner rules option (b) ([README Q-5](README.md#questions-for-the-owner-at-the-checkpoint)) | No: every call, fixed. | none | none | Never the session that recorded the observation, or that authored a plan it selects among. |

**Per brief kind** (second pass, gap 2):
- All five adjudication briefs are retained: amendment, first-approval,
  disposition, consolidate and red-tc. Each judges against the whole spine,
  which is the reload the layer removes.
- Because nothing is excluded, `retain_for` retires.
- `rejudge` moves to [judge]. **Reason:** an observation judgment must not
  anchor on the same session's earlier verdicts on that case. The move also
  matches the glossary's "judge (an observation re-judge)".

**No occupancy reported (risk 4).** Retention requires a reported `used`.
- opencode reports `used` (`scripts/session_adapters.py:728-752`) but no
  window, so its route row declares `window`. The same percentage rule then runs.
- A route that reports no `used` is reset every call: Gemini until it is
  recorded, and the plain adapter.
- So is a router alias such as FreeLLMAPI `auto`. Its model, and with it the
  window and the family, can change between calls.
- Directory-bound runners add the term "the directory differs from the
  session's". That covers opencode as probed, and Gemini, whose sessions are
  stored per project.

**Where the terms are declared.** Today's `[adjudicator]` table becomes
`[sessions.<family>]`, with `context_reset_pct` (0 = every call).
- [adjudicate] keeps `keepwarm_minutes` and `reset_on_same_artifact`.
- [review] and [judge] are fixed in code.
- The template sets both adjudication families to 55 and [plan and build]
  to 0.
- The RESYNC entry moves the keys (risk 9).

**Ruling changes:**
- **S10's "reviewers never"** is narrowed: the adjudication reviewer is
  retained, and code reviewers stay unretained.
- **OI-69's "turning the dial on is the owner's act"** changes for adopters: the
  template ships it on. In this repo it stays the owner's edit.
- **S11 §4.6's "fresh cross-family review of the act"** changes: the final
  review is the retained adjudication reviewer, independent per scope and
  cross-family where the pool allows. S11 Q4 ("always owed") stands.
- **OI-69 (e1)** changes as set out in §4.

## 3. The one entry point

```python
ask(kind, *, root, lane, prompt, subject, escalation=None, attached=False,
    on_line=None) -> Answer
```

**Parameters:**
- `kind` is one of build, review, judge, adjudicate, author, author-review, plan
  or plan-critique (plus arbitrate, only under Q-5 option (b); chapter 3 §4.4
  recommends none). Probe and keep-warm are internal.
- `lane` is the worktree the call runs in, or None for internal calls only.
- `prompt` is the composed brief. Composition stays in `agent_brief`,
  `adjudicate_brief` and the plan templates.
- `subject` gives the `wi`, the judged `scope` (`base..head`), the adjudication
  `brief` and the `rows`.
- `escalation` is `swap` or `tier-up`, never a family.

**Result.** `Answer` carries `text` (the final message), `code`, `outcome`,
`log`, `route`, `account`, `session_id` and `resumed`. A caller never names a
family, model, route or account.

**Steps, in order:**
1. **Label to tier.** The phase default (`agent_brief.phase_tier`), the
   BuildTier pin, `tier-up`, and OI-103 Q5's planned-build dial. The planner
   tier comes from chapter 3's plan record.
2. **Exclusion from recorded authors** (risk 2, B10). (Amended, [README A1](README.md#the-owners-checkpoint-ruling-2026-10-04): the kind's eligible families come first; every family exclusion in the table below, `plan-critique`'s and `author`'s included, is a ranked preference within that set; and a preference the declared table makes impossible is logged, not recorded for review.) Read the lane's committed
   session logs whose `commits` range meets the call's **judged scope**, for every
   authoring kind: build, plan, author, author-review, and adjudicate where it
   wrote beyond its verdict. Each kind's judged scope and exclusions are exact:

   | Kind | Judged scope | Excluded |
   |---|---|---|
   | review (REVIEW-A/B, CRITIQUE) | build and plan ranges | their authors' sessions; families ranked (see "A lane built by both families" below); REVIEW-B also REVIEW-A's family where the pool allows |
   | plan-critique | the critiqued plan's drafting range | its drafter's family |
   | judge | the observation's range and the build it observes | their authors' sessions; families ranked, as for review |
   | author | builder text it adopts | builder families |
   | author-review | the adjudicator's `author` ranges, and the builder text they adopt | the adjudicator's session always; then two ranked preferences, the adjudicator's family first and the builders' families second, a preference dropped only when the pool cannot meet it and the unmet one recorded per call (the owner's "preferably another family", stated against "the adjudicator it checks") |
   | adjudicate (RESOLVE, JUDGE, the final pass) | build, plan and author-review ranges | every build, plan and author-review session; builder and planner families ranked, as for review. Its own `author` ranges are **not** excluded: B10's one exception, admitted only when an author-review range by another session follows each and the pass changes no byte |
   | final review ([adjudication review]) | the adjudicator's ADJUDICATE and MINT ranges only | every session that authored any range in this sitting; the adjudicator's family where the pool allows |

   **With today's two-family pool** (builder family X, the other Y): review Y,
   adjudicate Y, author-review an X session (the builder-family preference
   unmet, recorded), final review a fresh X session that authored nothing in
   the sitting. Every approved byte is then read by another family before the
   act: the builder's by the adjudicator, the adjudicator's drafts by the
   author-review, the author-review's edits by the adjudicator's unchanged
   pass. Every kind has an eligible draw for a lane built by one family.

   **A lane built by both families** (today's implementer swap,
   `agent_loop.py:618-621`, which chapter 3 §4.7 keeps). Its build ranges carry
   X and then Y, so excluding every author's family would leave `review` and
   `adjudicate` no draw in a two-family pool. The rows above are therefore read
   with dispute 2's one rule (the 2026-10-04 adjudication): **sessions are
   excluded hard; families are ranked preferences**, dropped only when the
   pool cannot meet them, the unmet one recorded per call. For `review`,
   `judge` and `adjudicate` the ranking is:
   1. not the family of the latest authoring range in the judged scope (the
      bytes being judged as they now stand);
   2. not the family of any earlier authoring range.

   After a swap (X built, Y reviewed twice, Y rebuilt): review X, adjudicate X,
   each with preference 2 unmet and recorded. Every byte still has a
   cross-family read before the act: X's earlier ranges were read by Y as
   reviewer and as swapped builder; Y's ranges by the X reviewer and the X
   adjudicator. With one family enabled, both preferences are unmet: that is
   SR-154's documented same-family mode, the same rule with a smaller pool, not
   a second path. The set of eligible sessions is never empty, because a fresh
   session is always eligible, so the entry point never stops for this. An
   unmet preference is owner-visible without stopping anything: `ask` writes it
   in the session log's `exclusion-unmet` field and as an entry in the lane's
   decisions record, which feeds WI-790's "Decisions to review" (LS9's rule:
   advice the owner may simply take is a decision entry, not an open item).
   - A commit in scope that no log covers is attributed by its own
     `Co-Authored-By:` trailer when that names a registered model. Otherwise
     it counts as a person's commit, logged as `unattributed`.
   - **Why this is not a marker convention.** The trailer is read from the
     judged commit itself, inside the scope under judgement, never from
     history beyond it. The kit asks no one to write it: it is the harness's
     own attribution line. It can only add an exclusion, never remove one, so a
     wrong or absent trailer fails toward today's behaviour. Once hand
     sittings run through `ask.py` it covers only a person's own editing
     session. The owner rules on keeping it
     ([README Q-10](README.md#questions-for-the-owner-at-the-checkpoint)).
   - Review kinds also exclude the round's earlier reviewers.
   - `swap` excludes the latest build author.
   - This **replaces** `last_impl_family` (`scripts/agent_loop.py:462`,
     `:506-547`) and `last_build_family` (`:3049-3067`). Neither is kept
     beside it.
3. **Retention before the ratio** (risk 3). If the family is retained and its
   slot holds an active session, use that session's route and account, unless a
   reset term is met, or step 2 excludes that session or its family for this
   judged scope. An excluded retained session is not reset: the call runs a
   fresh, non-replacing session (logged, never stored), and the slot keeps its
   session for the next eligible call. The `docs/agents-enabled` ratio applies
   only at (re)initialization.
   - **The router-before-service split moves here.** The store is read
     before `agent_route.select`. Today `plan_keep` runs on a route already
     drawn (`agent_loop.py:2587-2614`).
4. **Availability and ratio.** (Amended, [README A1-A2](README.md#the-owners-checkpoint-ruling-2026-10-04): the family by its per-kind weight, then the account by weekly pace.) `agent_route.select` keeps its rules. Cooldowns
   move from loop memory (`agent_loop.py:454`) into the store, keyed by
   `route@account`, so every lane and the coordinator share them.
5. **The session lease** (risk 5, B4).
   - A retained slot is leased for the call. The caller waits up to 1200 s
     (today 120 s, `session_keep.py:544`), in its own process and never on the
     dispatcher's tick, and **never while holding the station authority**
     (OI-103 Q2).
   - Past that, the call runs a fresh session that **does not replace** the
     retained one: it is logged, never stored. `keep_for` already returns
     None, at `:591-598`.
   - **How it composes with the authority** (chapter 4 §2's order): a sitting
     takes its leases first, waiting holding nothing, then tries the authority
     once without waiting; if the authority is held it releases the leases and
     tries again on a later tick. Under the authority every lease acquisition
     is one non-blocking try, and a busy lease (a keep-warm ping) gives that call
     a fresh, non-replacing session at once
     ([README](README.md#how-the-locks-and-the-lease-compose)).
6. **Durable invocation** (B9). Before launch, an invocation record is written
   to the store: the id, kind, wi, lane, route, account, cwd, pid and start time.
   The session id comes from:
   - claude: minted up front with `--session-id`, on every claude call;
   - codex and opencode: written as the stream shows it (`on_line`).

   **Conditional resume.** A session resumes only when its id is recorded, its
   lease is ours and its terms are unmet. A launch that raises:
   - **before** the runner starts: releases the lease and leaves the session
     active;
   - **after** it starts: retires it. Today's rule at
     `scripts/session_service.py:238-243` applies only to this case.
7. **Record.** One session log per call, with a `commits` range for every kind
   (HEAD in `lane`, before and after). Today a plain call records none
   (`session_service.py:342-351`). New columns: `kind`, `account`, `resumed`.
   The invocation record is removed when the log is written.
8. **The decisions note.** `kitlib.decisions.session_note(mode, branch)`
   (`scripts/kitlib/decisions.py:167-196`) is appended for every kind except
   those whose range a mechanical rule confines to their verdict file.
   - **That rule is S9's.** Today it covers REVIEW-A/B only, in two parts: the
     phase set `REVIEW_PHASES` (`kitlib/verdict.py:189`, read at `:944`; the
     live arm runs only for a review, `agent_loop.py:2460-2463`) and the
     verdict-file identity (`scope_offenders` through `round_file`, whose
     `ROUND_FILE_RE` admits only `REVIEW-[A-Z]` names, `kitlib/verdict.py:219-222`,
     `:822-842`). S788-ask gives S9 its own phase set and leaves
     `REVIEW_PHASES` alone (it also drives `is_review`, `agent_loop.py:2866`,
     and the owed review phases, `kitlib/verdict.py:1174`). Each added kind's
     verdict file is stated:
     - **CRITIQUE** commits only its verdict
       (`prompts/critique.template.md:24-46`), named `<n>-CRITIQUE-<sha7>.md`
       (`agent_loop.py:1703-1705`); S9 admits exactly that file, in both arms.
     - **plan-critique**, and arbitrate under Q-5 (b), end in one block and
       commit nothing (`prompts/dual-plan-critic.template.md:65-77`,
       `prompts/dual-plan-arbiter.template.md:78-80`); the runner writes the
       block (`plan_runner.py:490-492`), so S9 admits an empty range.

     Those kinds then skip the note, because their calls are recorded by their
     verdicts.
   - **Every other kind gets it**, judge included: an observation re-judge
     commits an observation record beside its verdict
     (`prompts/adjudicate-rejudge.template.md:43-56`), so it can owe a record.
   - The note moves from `agent_loop.session_body` (`agent_loop.py:387`,
     `:398`) into `ask`, so a coordinator's sitting gets it too.
   - Chapter 4 owns the landing check and the gap measurement.

**The B11 split.** `ask` owns model and session calls, the store and the ledger
rows. `lane_state` owns the lifecycle effects. At `ARCHIVE` it retires the
lane's [plan and build] slot through one store call.

**Callers.** These move onto `ask`:
- `agent_loop.route_session` and `launch_session` (`agent_loop.py:1588-1700`,
  `:2617-2650`);
- `plan_runner._dp_routes` and `_dp_session` (`scripts/plan_runner.py:102-155`,
  `:173`): its `planner_pair` draw stops being a bypass;
- `KeepWarmer` (`session_service.py:451-590`);
- the route probes.

`session_service.Call`, `act` and `record` become `ask`'s internals (IF-246,
amended).

**The coordinator calls the same `ask`** (risk 8, LS10):
- The command is `python project-trajectory/scripts/ask.py <kind> --lane <path>
  --wi WI-n --scope base..head --prompt-file <f>`.
- The prompt reaches the runner on stdin, as every route already does.
- Results arrive as the files the brief names in the lane, plus the captured
  final message: the claude `result` event, codex `-o`, or opencode's last
  `text` event. It is printed and kept in the log.
- Continuity comes from the store and each CLI's own resume form. Agent-tool
  subagents and `SendMessage` retire for model work.
- The person's tool permissions must allow `ask.py`. A classifier refusal of a
  route's flags is surfaced to the owner, never worked around (LS9).

## 4. One session store, accounts and homes (risk 1, B12)

**The store.** `out/sessions/store.toml` under the primary checkout, by the
existing `store_dir` rule (`session_keep.py:165-175`).
- **Properties:** untracked and machine-local; read with `tomllib` and written
  whole by the kit's writer, under the existing store lock.
- **What it absorbs:** today's per-route JSON files and tombstones in
  `out/adjudicator/`, which the RESYNC entry deletes. A dropped session costs
  one reload.
- **Tables:**
  - `[slot."adjudicate"]`, `[slot."adjudication-review"]` and
    `[slot."plan-and-build/<lane>"]`, each with IF-247's fields plus
    `route`, `account` and `cwd`;
  - `[cooldown."<route>@<account>"]`;
  - `[invocation."<id>"]`.
- **Keys.** A slot is keyed by family and scope, never by route, so a retained
  session keeps one identity across route draws. The slot *records* the
  `route@account` its session runs on; only cooldowns are keyed by it.

**Accounts.** Today IF-045 says "a second account or router is a second pair
row" (`docs/agents.toml:16`). For codex that means three duplicated rows per
account.
- **Proposed:** `[account.<ID>]` tables in `docs/agents.toml`, holding `cli`,
  `notes` and an optional `env`.
- An enable-list line may qualify a route: `OPENAI-SOL@WORK`. Unqualified means
  the person's own ambient login, exactly as today.
- Cooldowns key on `route@account`, because rate limits are per account. A
  slot records its session's `route@account` but is not keyed by it.
- **Where a home lives:** `<user config dir>/project-trajectory/accounts/<ID>/`
  (`%APPDATA%` on Windows, `$XDG_CONFIG_HOME` or `~/.config` on POSIX). It is
  outside every checkout and shared by every repo on the box.
- **Who fills it:** a person provisions the credentials, for example
  `CODEX_HOME=<home> codex login`. The kit never reads them.

**Home variables** are an adapter fact (IF-245, amended):

| CLI | Home variables |
|---|---|
| claude | `CLAUDE_CONFIG_DIR` |
| codex | `CODEX_HOME` |
| opencode | `XDG_DATA_HOME=<home>/data` and `OPENCODE_CONFIG=<home>/opencode.json` |
| gemini | `GEMINI_CLI_HOME` |

**Changes OI-69 (e1).** Today there is one home per family while retention is
on (`session_keep.py:102-107`, `:316-328`), laid over the route's env
(`session_service.py:164-171`).
- **Proposed:** a call runs under its account's home whether or not it is
  retained, and the per-family home retires.
- **Reason (a):** two retained accounts of one provider currently share one
  home, and a route's own `CLAUDE_CONFIG_DIR` or `CODEX_HOME` is silently
  overridden. This is the OI-101 fact.
- **Reason (b):** "retention changes the home" is a second path (risk 7).
- **Reason (c):** with retention shipped on, the family home would start every
  adopter's adjudicator with no credentials.
- **What e1 protected:** a person's sessions mixing with the orchestrator's. That
  mattered only for `resume --last`, which the kit never uses. A person who
  wants the separation declares an account.
- **Build order:** homes come first (B12).

## 5. Providers and routes

| Provider | Headless CLI | Auth and account | Home variable | Free plan | Stream: usage, occupancy, id |
|---|---|---|---|---|---|
| Anthropic | `claude -p`, 2.1.289 (probed) | Login, `ANTHROPIC_API_KEY` (always used under `-p`), or `CLAUDE_CODE_OAUTH_TOKEN` | `CLAUDE_CONFIG_DIR` (referenced in the docs, not tabled) | UNVERIFIED | stream-json `result`: `usage`, `modelUsage.<m>.contextWindow`, `session_id`. Adapter exists. |
| OpenAI | `codex exec`, 0.160.0 (probed) | ChatGPT login or API key | `CODEX_HOME` | UNVERIFIED | `--json`: `thread.started.thread_id`, and `turn.completed.usage`, which is cumulative per thread (15,033 then 30,222). The rollout's `token_count` gives the per-request figure. Adapter exists. |
| xAI Grok, through OpenCode only (OI-101 Q3) | `opencode run -m opencode-go/grok-4.6`, 1.18.30 (probed: 10,822 tokens, $0.021576) | OpenCode Go gateway login, or an xAI key as an opencode provider | `XDG_DATA_HOME`, `OPENCODE_CONFIG` | No permanent free API tier. Promotional credits are reported by secondary sources (UNVERIFIED). SuperGrok is a consumer plan with no headless route. | `--format json`: `step_finish.part.tokens` and `cost`, `sessionID` on every event. The row declares the window (500,000 per the 2026-08-29 study). |
| FreeLLMAPI, through OpenCode | `opencode run -m freellmapi/<model>` | A local server at `http://127.0.0.1:3001/v1`, with one bearer key `freellmapi-<key>` | the opencode account home | The aggregated free tiers of its upstream providers; limits are per upstream key | As opencode. `auto` fails over, and the serving model appears only in an HTTP header (`X-Routed-Via`). |
| Google | `gemini` (npm latest 0.62.0; not installed; docs only, OI-101 Q4) | Google login, `GEMINI_API_KEY`, or Vertex | `GEMINI_CLI_HOME` | 1,000 requests/day on a Google account; 250/day on a free API key | stream-json `init` (session id, model) and `result` (per-model stats; field names UNVERIFIED). Exits 0/1/42/53. Resume with `-r <id>`. |

**FreeLLMAPI as an OpenCode custom provider:**
- **Where its config lives.** The account home's `opencode.json`, copied from a
  kit-shipped `project-trajectory/opencode-freellmapi.template.json`. It
  declares:
  - `"npm": "@ai-sdk/openai-compatible"`;
  - `options.baseURL`;
  - `options.apiKey: "{file:./key}"`;
  - one `models.<id>` per pinned model, each with a `limit`.

  OpenCode merges this file over the global config. It does not replace it.
- **Where the key lives.** In the home's `key` file, untracked, provisioned by
  the person and never read by the kit.
- **The route row:** model `freellmapi/<model>`, `account = "FREELLMAPI"`, and
  `family` set to the model's trainer, so independence stays true.
- **No `auto` row:** its family and window are unknowable, and it fails over
  mid-session.
- **A pinned model can fail over too.** The README says the router "retries the
  next model in your chain on 429/5xx", and every response names the server in
  an `X-Routed-Via` header, which OpenCode does not surface. **Contract:** a
  FreeLLMAPI row ships only for a pinned id whose chain, declared in the
  account home's FreeLLMAPI configuration, holds that one model, so the family
  is the row's. If FreeLLMAPI cannot declare a one-model chain per id
  (UNVERIFIED), no FreeLLMAPI row ships: a row whose family is unknowable would
  break every exclusion.
- **OpenCode's own `opencode/*-free` models get no row:**
  - they proved unreliable in OI-101's probe;
  - they are not what the owner meant;
  - the routing pack advises against vendoring a catalogue with no consumer.

**Corrections.**
- **Families.** The OpenCode rows' `family = "OPENCODE"` (`docs/agents.toml:84-98`)
  breaks IF-045's rule that the family is who trained the model. Grok is `XAI`,
  Kimi `MOONSHOT`.
- **Untested is visible.** Every row gains `verified = "<date> <cli version>"`,
  and an empty value means untested.
  - Preflight prints each enabled untested route.
  - The shipped defaults enable none of them.
- **The Gemini row** moves from `-p {prompt}`, which a Windows `.cmd` shim
  refuses (`project-trajectory/agents.template.toml:34-40`), to stdin.
- **The Gemini adapter** is built from the documented schema, with a fixture
  labelled synthetic.

**Contracts from documentation, and the live checks still owed.** Builders
implement the left column; nothing in it is guessed. The right column is
exactly what remains, which row owes it, and whether it costs model spend.

| Item | Contract (source, read 2026-10-04) | Live check still owed |
|---|---|---|
| Claude Code plans | No Free-plan access; Pro, Max, Team premium seat or API billing (secondary sources: eesel.ai, costbench.com) | none: provisioning is the person's |
| Codex plans | ChatGPT Free includes limited Codex access; CLI, web and IDE share one quota with a 5-hour window and a weekly cap (secondary: eesel.ai, developersdigest.tech) | none |
| claude account isolation | `CLAUDE_CONFIG_DIR` moves "your settings, session history, and plugins" (code.claude.com/docs/en/settings). The docs do not say whether `~/.claude.json`, which holds the sign-in session, moves with it | S788-accounts, no model spend: two homes on Windows show two logins. Until it passes, a claude account other than the ambient login keeps `verified = ""` |
| Gemini stream | `init` carries `session_id` and `model`; `result` carries `status` and `stats` (`total_tokens`, `input_tokens`, `output_tokens`, `duration_ms`, `tool_calls`) (geminicli.com headless docs; field names from secondary parsers). No cache split, no context window. Headless runs when stdin is not a TTY or with `-p`; prompt-on-stdin is not documented | S788-routes builds on a synthetic fixture: usage from `stats`, no occupancy, so every-call reset (§2). The row stays untested; a recording needs the owner's authorization, which OI-101 Q4 does not give |
| FreeLLMAPI | as above: one-model chain, or no row | S788-routes, one live call once the owner names the endpoint (README Q-4): the served model equals the pinned one |
| opencode directory binding | probed (§1) | none |

## 6. U1, the usage ledger

**The carrier.** `docs/usage-ledger.csv`: append-only, generated, one row per
session log, keyed by `invocation-id`.

**Columns:** date, wi, lane, kind, phase, route, account, provider, CLI, model,
the five `gen_ai.usage.*` counts, fresh input, cost (where reported), wall
seconds, outcome, session id, `resumed`, `usage-status`
(known/partial/unavailable/recovered), and the log path.

**It replaces `docs/iteration_index.md`.** Confirmed against the code:
- `agent_common.regenerate_index` (`scripts/agent_common.py:1600-1648`) has no
  caller;
- the tests assert the index is never written (`tests/test_agent_loop.py:288`,
  `:1298`, `:1326`);
- yet the stop banner still names the index (`agent_common.py:2060`).

The index and its writer retire. A backfill appends every existing log, keyed
`log:<name>` where a log predates `invocation-id`.

**Appending, under OI-103 Q1.** `trunk_step` appends the unseen rows at the
final evidence's regeneration ([chapter 4 §5](4-adjudication-mint-landing.md#5-final-evidence-b5-and-authorization-b6)),
inside chapter 4's station authority, and the squash lands them. Lanes never write the ledger in between, so it is conflict-free, like
`log.md`.

**The spool.** Some sessions have no lane commit to ride:
- keep-warm pings, which today commit to trunk (`session_service.py:451-590`;
  OI-103 Q1 moves them);
- probes;
- a discarded lane's logs, harvested by chapter 1's discard before the worktree
  goes (OI-103 Q6).

Their logs go to `out/sessions/spool/`. The next landing's final regeneration
copies them into `docs/iteration/` and appends their rows. A spooled entry is deleted only once
trunk's tree holds its log (a squash leaves no ancestry to test), so a
rejected lane loses nothing. Rows are keyed by invocation id, never by session
id, because a retained session spans many invocations.

**Usage per invocation, not per session.** A retained session is resumed by
many invocations, and some CLIs report usage for the whole session: codex's
`turn.completed.usage` is cumulative over the thread
(`session_adapters.py:480`, scope `thread`). Keying rows by invocation id stops
duplicate rows, not double counting. So:
- each adapter declares its usage scope, `call` or `thread` (codex already
  does);
- for a `thread`-scope adapter, the invocation record stores the session's
  cumulative counters at launch (the previous invocation's final counters, kept
  in the slot), and the row is the end counters minus that baseline;
- claude's `result.usage` is taken as `call` scope; whether that holds for a
  resumed session is UNVERIFIED, and S788-session-store's resumed-call fixture
  pins it either way.

**A hard kill with no log.**
- The invocation record outlives the process. At launch it also stores a
  **cursor** into the CLI's own record: the claude transcript's line count, the
  codex rollout's line count, or opencode's message count.
- The next `ask`, or the harvest, finds a record whose pid is dead and recovers
  usage by session id, counting **only entries after the cursor**: the claude
  transcript `projects/*/<id>.jsonl` in the account home, the codex rollout
  `sessions/**/rollout-*-<id>.jsonl`, or `opencode export <id>`. Earlier
  invocations of the same session are never counted again.
- It writes a `KILLED` log marked `recovered`, or `unavailable` when no id was
  seen. It never claims a finished session (B9).

**What this repo cannot cover:** the coordinator's own Claude Code sittings, and
reviews launched by hand outside `ask.py`.

## 7. Dual paths in this area (risk 7)

| Dual path | Disposition |
|---|---|
| The CSV registry reader beside TOML (`scripts/agent_route.py:233`) | Retire; RESYNC converts. Built in S788-retire-legacy-config-and-carriers (chapter 1 D6). |
| The legacy `Provider` column and the `weak` tier (IF-045) | Retire; RESYNC rewrites. Same row (chapter 1 D5). |
| No enable-list means the single-model `AGENT_CMD` path (IF-162) | Fold: an implicit one-route registry. |
| The per-family retention home | Retire (§4). |
| `KeepWarmer`'s own record and commit | Fold into `ask` and the spool. |
| `iteration_index.md` | Retire into U1. |
| `last_impl_family` / `last_build_family` | Retire into step 2. |

## 8. Matrix rows

| item | kind | amend / preserve / retire | why | successor |
|---|---|---|---|---|
| SR-222 | row | amend | One usage record = log + ledger row; recovered kills | S788-session-store |
| SR-227 | row | amend | Per-family retention and terms; template on; conditional resume; account homes | S788-session-families |
| SR-154 | row | amend | Independence from all recorded authors; one entry for every caller | S788-ask |
| SR-225 | row | amend | The note is handed by `ask` on every path (landing: chapter 4) | S788-ask |
| SR-155, LLR-076 (amend); LLR-072 (retire) | row | chapter 3 | Plan kinds through `ask` | S788-plan-kinds, S788-dual-pickup |
| LLR-266, LLR-267, LLR-268 | row | amend | Gemini adapter; home variables; directory binding; declared window | S788-routes, S788-accounts |
| LLR-269 | row | amend | Service internal to `ask`; `commits` for every kind | S788-ask |
| LLR-270 | row | amend | One store; slots; 1200 s wait; launch-raised narrowed | S788-session-store |
| LLR-044, LLR-081 | row | amend | Cooldowns in the store; escalation as a label | S788-ask |
| LLR-283, LLR-290 | row | preserve | Unchanged; only the note's caller moves | — |
| new LLRs: `ask`, ledger, accounts | row | add | §3, §6, §4 | S788-ask, S788-session-store, S788-accounts |
| TC-262..265 | row | amend | kind, account, commits; Gemini synthetic fixture | S788-ask, S788-routes |
| TC-266, TC-267, TC-268, TC-303 | row | amend | Store, families, template default, conditional resume | S788-session-store, S788-session-families |
| TC-046, TC-084 | row | amend | Author-derived exclusion; shared cooldowns | S788-ask |
| TC-293 | row | preserve | — | — |
| IF-045 | contract | amend | Accounts, `verified`, `window`, family = trainer; retires "second account = second row" | S788-accounts, S788-routes |
| IF-162 | contract | amend | `@account`; weights by kind; single-model fold | S788-accounts |
| IF-245 | contract | amend | Home variables, directory binding, Gemini | S788-accounts, S788-routes |
| IF-246 | contract | amend; new IF for `ask`/`ask.py` | `Call` internal | S788-ask |
| IF-247, IF-248 | contract | amend | One TOML store; keep keyed by slot | S788-session-store |
| IF-081, IF-155 | contract | amend | `trunk_step` appends the ledger | S788-session-store |
| IF-064, IF-266 | contract | preserve | — | — |
| `docs/agents.toml`, `agents.template.toml` | carrier | amend | Accounts, `verified`, family fixes, new rows | S788-accounts, S788-routes |
| `docs/agents-enabled` | carrier | amend | `@account`, kind weights | S788-accounts |
| `[adjudicator]` in `docs/process.toml` / `process.toml.template` | carrier | amend to `[sessions.*]` | Families; template 55 | S788-session-families |
| `out/adjudicator/` | carrier | retire into `out/sessions/` | Risk 1 | S788-session-store |
| `docs/iteration_index.md`, `regenerate_index` | carrier, module | retire | Uncalled; replaced by U1 | S788-session-store |
| `docs/usage-ledger.csv` | carrier | add | U1 | S788-session-store |
| `session_service`, `session_keep`, `session_adapters`, `agent_route`, `trunk_step` | module | amend | §3-§6 | as above |
| `agent_loop` (route_session, launch_session, route_intent, last_build_family, adjudication_keep, the note) | module | amend | Callers of `ask` | S788-ask |
| `ask.py` | module | add | The coordinator's CLI | S788-ask |
| PROCESS_OPTIONS.md "Unattended operation"; registry-machinery-reference; enforcement-audit; cli-reference | doc | amend | Families, `ask`, accounts, ledger | each slice |
| `session-protocol` skill; the S11 hand recipe (SendMessage) | prompt | amend | Coordinator uses `ask.py` | S788-ask |
| RESYNC_PACK.md | doc | amend | One entry per slice | each slice |

## 9. Proposed successor rows

Order: `S788-glossary` → **S788-accounts** → **S788-session-store** →
**S788-ask** → **S788-session-families** → **S788-routes**. S788-plan-kinds
needs S788-ask. S788-landing needs S788-ask; S788-sitting and
S788-spine-authoring need S788-session-families. The full graph is the
[README's](README.md#the-dependency-graph-of-successor-rows). Every row carries a RESYNC entry. The test bar for
each is its affected modules plus the smoke tier at `-n 2`.

- **S788-accounts: account tables and per-account homes.**
  - **Scope:**
    - `[account.<ID>]` tables and the `@account` qualifier;
    - adapter home variables;
    - retire the family home.
  - **Done-when:**
    - two accounts of one CLI run under two homes;
    - a route's env is never overridden;
    - unqualified entries behave as today;
    - cooldowns key on `route@account`;
    - a scaffold bootstrap passes.
  - **needs:** S788-glossary. **BuildTier:** strong.
- **S788-session-store: one store, durable invocations and the usage ledger.**
  - **Scope:**
    - `out/sessions/store.toml` with slots, cooldowns and invocations;
    - recovery after a kill;
    - the ledger, the spool and the harvest;
    - retire `iteration_index.md`.
  - **Done-when:**
    - a mid-call kill is recovered into a `KILLED` log, from per-CLI fixtures,
      counting only usage after the invocation's cursor;
    - a resumed `thread`-scope session's row is end minus baseline, and the
      claude resumed-call fixture pins its scope;
    - `trunk_step`'s append is idempotent;
    - spooled logs land exactly once;
    - the backfill covers every existing log;
    - keep-warm commits nothing to trunk.
  - **needs:** S788-accounts, and S788-lane-state-provider (`harvest` at
    discard). **BuildTier:** strong.
- **S788-ask: one labelled entry point carrying today's kinds.**
  - **Scope:**
    - `ask` and `ask.py`;
    - today's phases moved on unchanged, except author-derived exclusion and
      [README A1](README.md#the-owners-checkpoint-ruling-2026-10-04)'s per-kind
      table, ordering rule and swap rule, which this row builds;
    - `commits` recorded for every kind;
    - the note handed by `ask`.
  - **Done-when:**
    - only `ask` launches or draws a route;
    - the loop-memory family fields are deleted;
    - a WI-688-shaped test passes: a build run outside the loop excludes its
      family from the judge;
    - an `ask.py` call writes a log and carries the note;
    - S9's reader covers CRITIQUE and plan-critique, and every kind outside it
      (judge included) receives the note;
    - each kind's judged scope and exclusions match step 2's table, and an
      excluded retained session yields a fresh, non-replacing call;
    - one live `ask.py` call has run, if the owner authorizes it.
  - **needs:** S788-session-store. **BuildTier:** strong.
- **S788-session-families: session families with declared reset terms.**
  - **Scope:**
    - `[sessions.<family>]`, migrated from `[adjudicator]`;
    - the retained adjudication reviewer;
    - builder retention, at every call;
    - `rejudge` moved to [judge];
    - the directory term;
    - the 1200 s wait.
  - **Done-when:**
    - the template retains both adjudication families at 55;
    - this repo's values are unchanged;
    - each family's terms are pinned by tests, including the opencode
      directory term and the no-`used` rule;
    - a spawn failure leaves the session active.
  - **needs:** S788-ask. **BuildTier:** strong.
- **S788-routes: FreeLLMAPI and Grok through OpenCode, Gemini untested.**
  - **Scope:**
    - the `verified` field and its preflight line;
    - family fixes;
    - the FreeLLMAPI account template and row, and the Grok row;
    - the Gemini row on stdin, with its adapter on a synthetic fixture.
  - **Done-when:**
    - untested rows are visibly unverified and enabled nowhere by default;
    - `opencode models freellmapi` resolves under the account home;
    - a FreeLLMAPI row exists only with a declared one-model chain (§5);
    - one live FreeLLMAPI call is recorded once the owner's endpoint exists;
    - no adopter is forced to install a CLI.
  - **needs:** S788-accounts, S788-ask. **BuildTier:** medium.

## 10. Questions for the owner

Consolidated in the [README](README.md#questions-for-the-owner-at-the-checkpoint).
After the fix round: question 1 is decided (a) as a design call (an
implementation location, no owner input needed); question 2's option (b) is
withdrawn, because OI-101 Q4 already rules Gemini documentation-only; Q-3 asks
only for spend authorization; question 3 is Q-4.

1. **Where do account homes live?**
   - (a) The user config directory, shared by every repo on the box.
   - (b) Each clone's `out/accounts/`.

   **Recommend (a):** credentials stay out of every tree, and one login serves
   every repo.
2. **Gemini evidence.**
   - (a) A docs-only adapter with a synthetic fixture, marked unverified.
   - (b) Authorize one install and one free-tier recording.

   **Recommend (a)** under OI-101 Q4, then (b) when a Google account is wanted.
3. **FreeLLMAPI.** Name the endpoint (a local install at `:3001`, or hosted) and
   the models to pin, so S788-routes can record one live call.

## 11. Research record

**Probes.** Run in scratch directories `C:/Projects/ai-template.wt/review-tmp/wi788-probe/{a,b}`.
Versions: claude 2.1.289, codex-cli 0.160.0, opencode 1.18.30. No `gemini` or
`grok` is on PATH. `curl http://127.0.0.1:3001/v1/models` exited 7.

| # | Where | Command | Result |
|---|---|---|---|
| 1 | a | `claude -p "Reply with exactly: ONE" --output-format json` | exit 0; `session_id 35c6119f-dcfd-4bd5-bfb7-2524d16e9814`, `result "ONE"`, `contextWindow 1000000` |
| 2 | b | `claude -p --resume 35c6119f-... "What did you reply? One word." --output-format json` | exit 0; same id, `"ONE"`. The transcript is only under `projects/C--...-probe-a/`, recording cwd a ×16 and b ×4. |
| 3 | a | `echo "Reply with exactly: ONE" \| codex exec -m gpt-5.6-terra -c model_reasoning_effort="low" --skip-git-repo-check -s read-only --json -` | exit 0; `thread_id 01a105bc-8196-7a03-969a-c779a495d1b4`, `ONE`, `input_tokens 15033` |
| 4 | b | `echo "What did you reply? One word." \| codex exec resume 01a105bc-... -m gpt-5.6-terra -c model_reasoning_effort="low" --skip-git-repo-check --json -` | exit 0; `ONE`, `input_tokens 30222`; the rollout records both cwds |
| 5 | a | `opencode run -m opencode-go/grok-4.6 "Reply with exactly: ONE" --format json` | exit 0; `ses_efa4328c2ffePrNgc25LeFVLln`, `ONE`, total 10822, cost 0.021576 |
| 6 | b | `timeout 180 opencode run --session ses_efa... -m opencode-go/grok-4.6 "What did you reply? One word." --format json` (again with `</dev/null`, `timeout 100`) | exit 124 both times, empty stdout |
| 7 | a | the same as 6, `</dev/null` | exit 0, `ONE` |
| 8 | b | the same as 6 with `--dir <a>` | exit 0, `ONE` |
| 9 | b | 6 with `--print-logs --log-level INFO` | The instance switches to directory `a`, streams `grok-4.6` and reaches `exiting loop`; stdout stays empty until the timeout |
| 10 | a | `OPENCODE_CONFIG=<probe>/freellmapi.opencode.json FREELLMAPI_BASE_URL=http://127.0.0.1:3001/v1 FREELLMAPI_API_KEY=freellmapi-probe opencode models freellmapi` | exit 0, `freellmapi/auto`. Without the config: exit 1, `Provider not found: freellmapi` |
| 11 | a | the same env, `opencode run -m freellmapi/auto "Reply with exactly: ONE" --format json` | exit 1; `APIError: Cannot connect to API ... url http://127.0.0.1:3001/v1/chat/completions` |
| 12 | — | `XDG_DATA_HOME=<probe>/xdg opencode debug paths` | data, log and repos move under `<probe>/xdg/opencode` |
| 13 | a | `opencode export ses_efa...` | `info.directory` = a; 12 messages with per-message `tokens`. Probe 6's runs had still executed their turns. |

**Sources** (read 2026-10-04):
- github.com/tashfeenahmed/freellmapi (README, the raw `opencode.json`; MIT,
  pushed 2026-10-04);
- opencode.ai/docs/providers and /docs/config;
- code.claude.com/docs/en/env-vars and /docs/en/settings (`CLAUDE_CONFIG_DIR`,
  `~/.claude.json`);
- geminicli.com/docs/cli/headless and secondary stream parsers (littlebearapps.com
  Gemini stream-json cheatsheet), for the `init`/`result` field names;
- Codex and Claude Code plan access, secondary sources only (eesel.ai,
  developersdigest.tech, costbench.com);
- the google-gemini/gemini-cli `main` docs: `cli/headless.md`,
  `cli/session-management.md`, `cli/cli-reference.md`,
  `reference/configuration.md`, `resources/quota-and-pricing.md`;
- registry.npmjs.org `@google/gemini-cli`;
- xAI pricing, from secondary sources only (mem0.ai, eesel.ai, costbench.com).

**UNVERIFIED** (each with its owed check in §5's contracts table):
- the FreeLLMAPI end-to-end call, opencode's usage events for it, and whether
  a one-model chain per pinned id can be declared;
- Gemini's per-model and cache stats, its stdin delivery, and resume across
  directories;
- xAI's free credits;
- whether `~/.claude.json` follows `CLAUDE_CONFIG_DIR` on Windows;
- claude's `result.usage` scope on a resumed session.
