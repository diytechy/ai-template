# Mechanized-loop contracts — the seams the program's slices share

**Status:** normative for the build. Terminology and rulings are
[mechanized-loop-decisions.md](mechanized-loop-decisions.md); the build order is
[the plan](stakeholder-needs-build-plan-2026-08-08.md). This file fixes the
**interfaces between slices** so they can be built in parallel and still compose.
It states each seam once; a slice's own module docstring links here rather than
restating it.

---

## 1. `docs/config.toml` — the single configuration authority

Adopter-owned. The kit ships `project-trajectory/config.toml.template`; a
re-sync never overwrites a filled file (SR-141). Read through
`config.load_config(root)`; never parsed ad hoc.

```toml
schema = 1

[attestation]
# Inclusive human checkpoints: 0=SN; 1=SN+SR; 2=SN+SR+LLR; 3=SN+SR+LLR+TC.
human_ratification_through = 1
final_full_spine_review = "never"        # never | always

[automation]
lanes = 1
session_timeout_seconds = 7200
blackout = ""                            # "HH:MM-HH:MM" UTC Mon-Fri, "" disables

[policy]
push = "human"                           # human | agent-iteration | agent
privacy_check = false
secrets_scan = true
review_rounds = 1                        # 0 | 1 | 2
guardrails = "off"
subagent_gate = "off"                    # off | ask | deny
live_status = false
status_lint = 120                        # int budget, or 0 to disable
trajectory_check = true
interfaces_check = true
components_check = true
okf_export = true

[harness]
# The declared toolchain. Mirrors docs/stack.ini's [paths]/[product]/[tiers]/
# [coverage]/[step:*]/[generated] sections. stack.ini STAYS THE LIVE SOURCE until
# the P13 cutover; nothing reads these keys yet.
#
# CORRECTION, ruled 2026-08-08: this comment previously claimed the two are
# "proved to agree by the parity tests". No such test exists — the review swept
# for it and found only a loader assertion against a literal fixture, plus a rung
# that deliberately leaves `harness.*` out of the mixed-source watch list. The
# claim is withdrawn rather than quietly kept: an unproved parity claim about a
# duplicated toolchain declaration is exactly the kind of green this kit refuses.
# P13 owes ONE of two things, and must say which it did: land the parity test, or
# delete these keys and read the toolchain from stack.ini alone. Until then, a
# divergence between the two is undetected — and this repo's own config already
# has one, which is how the review found it.
src = "project-trajectory/scripts"
tests = "tests"

[outcomes]
# Complete normally takes its verdict from the independent reviewer plus the
# composed-tree bar. A dedicated adjudicator runs only on these triggers.
complete_sampling_rate = 0.0             # 0.0..1.0
risk_safety_classes = ["spine", "gate", "attestation", "high-risk", "adjudication"]

[admission]
# Optional throttle only, never the independence criterion (plan §8).
max_batch_size = 0                       # 0 disables the throttle

[routing]
enabled = true                           # the consent surface docs/agents-enabled carried

[[routes]]
id = "ANTHROPIC-OPUS-STRONG"
family = "ANTHROPIC"
model = "opus"
strength = 3                             # 1=quick 2=medium 3=strong
argv = ["claude", "-p", "--model", "{model}", "--output-format", "stream-json",
        "--verbose", "--dangerously-skip-permissions"]
env = { CLAUDE_CODE_EFFORT_LEVEL = "medium" }
capabilities = ["text", "implementation", "review", "adjudication"]
notes = "install/sign-in hint echoed at preflight-missing, cooldown and the no-routable page"

[jobs.reviewer]
minimum_strength = 2
fallback = "same-or-higher"
prefer_cross_family = true
pool = [ { route = "ANTHROPIC-OPUS-STRONG", weight = 1 },
         { route = "OPENAI-SOL", weight = 1 } ]

[prompts.reviewer]
template = "prompts/reviewer.md"
required_slots = ["VERDICT"]
allowed_sources = ["registry", "diff", "harness"]
prohibited_sources = ["self-assessment"]
output_schema = "review-v1"
```

> **Two corrections to this sample, ruled 2026-08-08 after the P4 slice drove it.**
>
> `required_slots` for the reviewer is **`["VERDICT"]`**, not the four-slot brief
> the first draft showed. The reviewer prompt deliberately carries **no diff**:
> it tells the reviewer to run `git log` / `git diff` itself, and that is the
> prompt's redaction *by construction* — the implementer's account never enters
> the brief because the brief contains nothing but the verdict contract. Adding
> four slots would have been a rewrite of a reviewed prompt, not a move of it.
> The lesson generalises: a slot list is DERIVED from the template, and declaring
> one by hand is just a second place to be wrong. `prompt_render.py check`
> compares the two and refuses on a mismatch.
>
> `template` is **repo-relative and layout-specific**. A scaffold receives the
> templates at `prompts/`, so an adopter's converted config says `prompts/…`
> (shown above). This kit *is* the product, so its own instance says
> `project-trajectory/prompts/…`. The renderer resolves the declared path against
> the repo root and carries **no special case** for either layout — which is
> exactly why the two instances differ here, and only here.
>
> `allowed_sources` / `prohibited_sources` draw from `prompt_render`'s **closed**
> class vocabulary (`registry`, `spec`, `diff`, `harness`, `ledger`, `graph`,
> `rubric`, `owner-prompt`, `self-assessment`, `worker-rationale`, `rival-plan`,
> `provenance`). `worker-rationale` is the one that carries SR-156: it is the
> judged party's own account, and it is prohibited in every judging brief.

**Declared jobs:** `planner`, `critic`, `arbiter`, `implementer`, `reviewer`,
`adjudicator`. **Declared prompts:** the six jobs plus the four adjudicator
templates `adjudicate-amendment`, `adjudicate-disposition`,
`adjudicate-conflict`, `adjudicate-red-test`.

**Loader contract.**

- `config.load_config(root)` → `(Config, [Finding])`. A non-empty finding list
  means the caller refuses; the `Config` is still returned so a caller can report
  every problem at once rather than one per run.
- `Finding` is `(key, reason)`. `key` is the dotted path (`policy.review_rounds`,
  `routes[2].strength`).
- Unknown key, wrong type, out-of-range value and unsupported `schema` are each a
  finding. An absent file is **not** a finding — it yields `DEFAULTS`.
- `config.mixed_source_findings(root)` → findings for every canonical key whose
  retired declared-policy file is still present *and* whose canonical key is set.
- Values are read through typed accessors, never by dict-walking at call sites.

**Retired sources** (the converter's input, the mixed-source detector's watch
list): `docs/gate-policy`, `docs/push-policy`, `docs/review-policy`,
`docs/privacy-check`, `docs/privacy-review`, `docs/secrets-scan`,
`docs/guardrails-policy`, `docs/blackout`, `docs/live-status`,
`docs/subagent-gate`, `docs/status-lint`, `docs/trajectory-check`,
`docs/interfaces-check`, `docs/components-check`, `docs/okf-export`,
`docs/agents.csv`, `docs/agents-enabled`, and `docs/stack.ini`'s `[agent-loop]`
section. **Not retired** (state/consent/evidence, not configuration):
`docs/gate`, `docs/work/pause`, `docs/events/*`, the registries, the dashboards.

> **Corrections ruled 2026-08-08, after the P2 slice drove the list.**
> `docs/critique-policy` was listed here and **does not exist** in this kit — no
> template, no scaffolded file, no reader. Removed. `docs/privacy-review` (the
> `warn-unwired` reviewer opt-down that `pre-push` actually parses) was missing
> and is added, with the canonical key `policy.privacy_review`. And no hook has
> ever read `docs/review-policy` — `policy.review_rounds` therefore has no hook
> call site to convert; its readers are `agent_loop` and `integrate`, which the
> P13 cutover converts.
>
> `[routing] enabled` **defaults to `false`.** The sample above is a *filled*
> instance, not the default set. `docs/agents-enabled` carried consent by
> **presence** (decision D-5), so a default of `true` would switch managed
> routing on for every repo that never asked — the opposite of preserving the
> consent property. The converter writes an explicit `true` when an enable-list
> exists.
>
> A document that **omits** `schema` is a finding, not merely one that declares
> an unsupported value: a reader that cannot know which rules apply must stop
> rather than guess.
>
> `docs/agents.csv` has no capability column, so a converted route gets an empty
> `capabilities` list plus one unmapped-report entry. An adopter fills it before
> routing binds; a job whose pool has no capable route refuses.

---

## 2. `docs/events/` — the append-only ledgers

One JSONL file per kind, one JSON object per line, newest last, never rewritten.
Outside `docs/work/` so `agent_common.spec_files`' `rglob("WI-*.md")` cannot see
them (decision D-3).

| Path | Kind | Owner |
|---|---|---|
| `docs/events/attestation.jsonl` | `attestation` | `attest.py` |
| `docs/events/review-requests.jsonl` | `review-request`, `review-decision` | `attest.py` |
| `docs/events/outcomes.jsonl` | `outcome`, `disposition` | `outcome.py` / `adjudicate.py` |
| `docs/events/failures.jsonl` | `bar-failure` | `outcome.py` |
| `docs/events/admissions.jsonl` | `admission` | `admit.py` |

**The envelope, identical in every ledger:**

```json
{"schema": 1, "kind": "outcome", "id": "<16 hex>", "ts": "2026-08-08T00:00:00Z", ...}
```

**`id` is derived, not random: the first 16 hex of the SHA-256 of the canonical
payload with `id` and `ts` removed** (`json.dumps(payload, sort_keys=True,
separators=(",", ":"), ensure_ascii=False)`). Three properties follow, and all
three are load-bearing:

1. **Duplicate detection is free** — a second write of the same facts produces
   the same id and is refused. This is what removes the derived-dedup-token
   problem outright rather than tokenizing it. *(Precedence, ruled after the P3
   slice drove it: in a **chained** ledger — attestation — `parent` is part of
   the digested payload and must equal the current head, so a second write of
   the same facts is refused by the **stale-parent** rung first and never
   reaches the id check. The id guard still earns its place: it catches a ledger
   repaired or appended to out of band. The "duplicate detection is free" claim
   is load-bearing for the **unchained** ledgers — outcomes, failures,
   admissions.)*
2. **Exactly-once remediation is free** — a bar failure keyed by tree, step and
   fingerprint has one id however many cycles observe it.
3. **The id is reproducible by anyone holding the payload**, so a reader can
   verify the ledger rather than trusting it.

`ts` is excluded from the digest precisely so that observing the same fact twice
is not two events. Every module writes through its own small append helper (the
kit's F5 independently-copyable rule); the helpers are pinned equal by a sync
test rather than extracted.

**Append rule.** Write with `newline="\n"`, UTF-8, one line, `os.replace`-free
plain append. A malformed line is a hard read error naming the file and line
number — never a silently skipped record.

---

## 3. Module and symbol map (the LLR contract)

| Module | Symbols | Slice |
|---|---|---|
| `config.py` | `load_config`, `DEFAULTS`, `SCHEMA`, `mixed_source_findings`, `Config` | P2 |
| `config_query.py` | `main` | P2 |
| `config_migrate.py` | `convert`, `LEGACY_MAP` | P2 |
| `attest.py` | `normative_digest`, `NORMATIVE_CELLS`, `append_event`, `accepted_anchor`, `requires_human`, `tier_routing`, `ratification_projection`, `review_requests`, `detect_candidates` | P3/P9 |
| `derive_gate.py` | `spine_stage`, `verification_gate_for`, `STAGE_GATE` | P3 |
| `outcome.py` | `write_outcome`, `scope_digest`, `classify_groups`, `failure_event`, `OUTCOMES` | P6 |
| `adjudicate.py` | `adjudicate`, `draft_successor`, `needs_adjudication` | P7 |
| `admit.py` | `admit`, `overlap_graph`, `admission_verdict` | P8 |
| `prompt_render.py` | `render`, `check_sources`, `provenance`, `catalog` | P4 |
| `resume_plan.py` | `plan`, `snapshot`, `spine_components`, `Decision` | P11 |

**Every module is stdlib-only** (SN-011) and runs on a clean Python 3.11+ on
Windows and POSIX. Each carries a `Contracts:` docstring line naming its
declared `IF-###` seams once its interface row exists (P13).

---

## 4. Normative cells and canonicalisation (P3, consumed by P10)

The cell lists are decisions §4. Canonicalisation, applied to each cell before
digesting, in this order:

1. Unicode NFC.
2. CRLF and CR to LF.
3. Every run of spaces and tabs to one space.
4. Strip leading and trailing whitespace from each line, then from the whole.

The digest input is `"attest-v1\n" + kind + "\n" + id + "\n"` followed by
`cell_name + "\x1f" + canonical_value + "\x1e"` for each declared cell in the
declared order. The `attest-v1` prefix is the schema version: changing the rule
changes the prefix, so old anchors are recognisably old rather than silently
wrong.

**The boundary, ruled 2026-08-08 after the P3 slice drove it.** Step 3 collapses
runs of *spaces and tabs*, **not newlines**. So inserting a hard line break
inside a cell — a re-wrap of a long requirement — *does* change the digest and
*does* raise a candidate. That is deliberate, and the asymmetry is the reason:

- **over-detection costs one adjudication.** The candidate is raised, an
  adjudicator reads the before/after, records `clarity`, and the anchor advances
  to the new digest. Nothing is blocked and nothing is lost.
- **under-detection is a hole.** A rule that collapsed every whitespace run
  would also collapse the difference between a list rendered as one line and as
  four, and there are cells where that genuinely changes obligation.

A cheap false positive beats a silent miss on the artifact the whole gate rests
on. If this is ever widened, the `attest-v1` prefix must change with it so old
anchors read as old rather than as agreeing.

**SN cells come from the markdown table row**, parsed with the same
`\|\s*(SN-\d+)\s*\|` shape the dashboard and the knowledge export already use.
`stakeholder-needs.md` carries **two tables with different shapes**, and the
digest declares both rather than assuming the first:

| Table | Heading | Cells |
|---|---|---|
| Core needs | `## Core needs` | need, why, priority, acceptance |
| Edge-case expectations | `## Edge-case expectations` | lifecycle, scenario, expected |

Reading the second table with the first's cell names was the shape the P3 slice
found: the digest stayed stable and total (every cell still binds), but the
anchor recorded `Lifecycle` under the name `need`, which would mislead anyone
reading a diff. The cell *names* are part of the record, so they are declared
per table.

---

## 5. Refusal conventions

Every refusal in this program is a **string naming the offending thing**, never a
bare boolean, and every entry point returns a non-zero exit on refusal. The
message form is:

```
<module>: REFUSED - <what> (<why>)
```

matching `spec_move.py`'s existing `spec_move: REFUSED - ...`. A finding list is
printed one per line, all of them, before the exit — a caller fixing a config
learns every problem in one run.

---

## 6. What each slice may NOT touch

To keep the parallel slices composable:

- **P2** owns `config*.py`, `project-trajectory/config.toml.template`,
  `docs/config.toml`, the three hooks, and its own tests. It does **not** change
  any existing runtime reader — the cutover is P13.
- **P3** owns `attest.py`, `derive_gate.py`, `docs/events/attestation.jsonl`,
  `docs/events/review-requests.jsonl` and its own tests.
- **P6** owns `outcome.py`, `docs/work/partial/`, the `SPEC_STATUS_DIRS` copies,
  `integrate.py`'s scope-at-claim record, `docs/events/outcomes.jsonl`,
  `docs/events/failures.jsonl` and its own tests.

A slice that needs a symbol from another slice imports it lazily inside the
function that uses it (the kit's existing deferred-import convention), so an
unbuilt sibling never breaks an import chain.
