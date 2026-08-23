# Spine restructure — SN-028..SN-032 build-out plan (2026-08-08)

**Status: PLAN, not ruled.** Nothing here executes until the owner answers §7.
A design doc in the shape of [`concurrency-restructure.md`](concurrency-restructure.md)
— not a working surface. The live surfaces stay [`status.md`](status.md), the
registries, and [`log.md`](log.md).

> **The owner waived the kit's own process mechanics for this implementation**
> ("those mechanics do NOT need to be followed... that will likely create more
> challenges working around a changing infrastructure"). §6 states exactly what
> that waiver does and does not switch off — the distinction is load-bearing and
> a session that gets it wrong will land a red.

Measured against the tree at `f1ba5fa0`. Gate **DevStg-Tests**; basis `SN=27 SR=136
LLR=137 TC=135 drafts=0 modified=21 uncovered=0`.
<!-- fig: cmd="cat docs/gate" rev=f1ba5fa0 -->

---

## 1 · What was already done in this session

**The mermaid skill is provisioned** — but not where you might expect, and the
reason is the kit's own rule.

[`EXTERNAL_SKILLS.md`](../project-trajectory/EXTERNAL_SKILLS.md) rule 1 is
**"Mine, don't install"**: a skill is instructions an agent will follow, so it is
a prompt-injection surface, and the kit vendors none. Independently,
`.claude/skills/` is a **byte-identical fan-out** of `project-trajectory/skills/`
policed by `gen_skills_index.py --check-agents` (pinned by
`tests/test_skills_sync.py`) — so a copy dropped there is drift by construction,
and adding it to the kit source would ship 620 KB of third-party docs to every
downstream adopter.

So it went to your **user** skills dir, where it is your tooling rather than a
kit dependency:

| | |
|---|---|
| Source | [`WH-2099/mermaid-skill`](https://github.com/WH-2099/mermaid-skill), MIT |
| Pinned | `50f13660453269d4ef8a7ca0ae5d945bdeb4ce44` |
| Installed to | `~/.claude/skills/mermaid/` (a `skills-dir` plugin) |
| Payload | 39 markdown files, **zero scripts, zero executables** — verified |

Its `references/` are re-synced verbatim from `mermaid-js/mermaid`'s own
`docs/syntax` + `docs/config` by a scheduled GitHub Action, so the payload is <!-- path-ok: proposed or upstream path -->
upstream documentation rather than someone's opinion. It **auto-loads next
session** (`claude plugin details` reporting `Skills (0)` is a display quirk — a
freshly scaffolded probe reports the same). A row recording all of this was added
to `EXTERNAL_SKILLS.md`.

---

## 2 · The diagram cross-comparison — no overlap, keep it where it is

The file in question is **`project-trajectory/PROCESS.md:587`** — the §5
**change-intake flowchart** (owner-confirmed). For the record, the other two
candidates were ruled out by inspection: `project-trajectory/README.md` has
**zero fenced code blocks of any kind**, and `PROJECT_STATE.html` has **zero
mermaid fences** (its one `mermaid` string is IF-029 *description text* inside a
JSON blob; the dashboard is 91 hand-built inline `<svg>` elements).

### The cross-comparison

| `PROCESS.md:587` draws | The dashboard's Process tab draws |
|---|---|
| **Change intake** — how an inbound *problem* routes INTO the spine: contradiction test → coverage gap vs requirement gap → scope (IF / CMP+PART / LLR) → WI → implement test-first → CMP `has-gap → verified` | **1 · Artifact lifecycle × gates** — Vision→SN→SR→LLR+arch→TC→code, each with its gate span and **live registry counts** |
| | **2 · The station cycle** — 10-node SVG (tick, claim, build, merged, cancelled, handback, refresh, slot, advance, intake); vocabulary **derived from `integrate.OUTCOME_DIRS` / `BAR_GREEN` / `schedule._KIND_CONCURRENCY`** |
| | **3 · Slices → phase → gates** — per-WI slice, commit bar, phase close, gate bar, CI |

**There is zero overlap.** Change-intake is *triage into* the spine; the three
panels are the *tiers*, the *concurrency model*, and the *cadence*. So there is
no duplication to remove — moving the diagram into the dashboard would mean
**building a new panel 4**, not consolidating anything.

### Recommendation: keep it in PROCESS.md. Do not move it.

Four reasons, in order of weight:

1. **The dashboard disclaims being the source.** Its own caption reads: *"A view
   — the process docs are the source of truth."* Every panel caption points
   *back* at `PROCESS.md` / `PROCESS_OPTIONS.md`. Moving the diagram out of
   PROCESS.md and into the HTML inverts the relationship the tab was built on.
2. **Downstream would lose it exactly when it's needed most.** `PROCESS.md`
   scaffolds to `docs/process.md` in every adopting repo. `PROJECT_STATE.html` is
   generated per-repo, and `process_panel()` **returns `None` when `docs/gate` is
   absent** — so a pre-DevStg-Reqs repo renders no Process tab at all. Change-intake is
   triage guidance; a young repo needs it before it has a gate.
3. **It would be the only panel with no data source.** Panels 1–3 are
   data-derived or derived-from-constants. Change-intake is 100% static, so it
   would break the tab's stated design principle and add a hand-maintained
   surface to a generated artifact.
4. **It would create a 2× sync problem rather than solve one.**

### The `\n` question — checked, and it is *not* a bug

`PROCESS.md:587` uses `\n` for in-node line breaks while **every other authored
diagram in the repo uses `<br/>`** (`architecture.md:1250,1329,1338,1340,1346`;
`concurrency-v2.md:57,61,68,72`). Upstream mermaid docs describe `<br>` as the
traditional-string idiom and newlines as the *markdown-string* idiom, which
suggested a latent rendering bug.

**Rendered both forms headlessly against mermaid 11 and compared pixels: they are
identical.** `\n` is handled correctly in traditional quoted strings. So this is a
**cosmetic inconsistency, not a defect** — worth normalizing to `<br/>` only if
someone is editing the block anyway.
<!-- fig: cmd="node render.mjs (mermaid 11 + pinned chromium; A=\\n form, B=<br/> form, screenshot compared)" rev=f1ba5fa0 -->

> This is why the check was worth running: the documentation-based inference said
> "broken", and the pixels said "fine". Judge rendered output, not source —
> the repo's own WI-189 doctrine.

### For the record — why the *other* direction is also closed

Had the ask been to build the dashboard's diagrams from mermaid, it crosses three
rulings at once, each independently blocking:

| Ruling | Where | Why it blocks |
|---|---|---|
| Offline-render principle | `PROCESS_OPTIONS.md:1460-1464` | a mermaid→SVG step makes the renderer a build dependency |
| Byte-stable freshness | `gen_trajectory.py:42-45` | `--check` is a byte-compare; any nondeterministic render breaks the DevStg-Impl gate |
| No CDN / no JS layout library | `gen_trajectory.py:16-19` (Thread 52 ruling A) | direct contradiction |

It would additionally need a `docs/dependencies.md` row — a ledger that declares
**zero `Kind=python` rows** today. And it would *lose* capability: the SVG derives
its vocabulary from shipped module constants (`traj_panels.py:513` iterates
`integrate.OUTCOME_DIRS`), and carries hrefs, `<title>` tooltips and
existence-probed links that mermaid cannot express. That is very likely what your
"limitations in the pure mermaid diagrams" aside is pointing at — and it is an
argument *for* the hand-built SVG, not against it.

**Stripping mermaid from the runtime-flow docs** is the mirror image: `PROCESS.md:272-275`
requires "always one [`sequenceDiagram`] for any concurrent / asynchronous /
non-blocking behavior", and the mermaid runtime-flow contract is backed by a full
approved chain **SN-010 → SR-013 → LLR-013 → TC-013** plus IF-003/IF-029, wired at
DevStg-Tests/DevStg-Impl as `check.py`'s `design-flows` step. Retiring that is a spine amendment
needing an approval window, not a doc edit.

### The real defect, which nobody filed

The **station cycle is drawn three times in three technologies with nothing
syncing them**:

| Home | Technology | Pinned to |
|---|---|---|
| `docs/runtime-flows.md` Flow 4 (measured at architecture.md:1316, pre-WI-455 move) | mermaid `sequenceDiagram` | registry ids, via `check_flows.ID_RE` |
| `docs/concurrency-v2.md:236` and `:464` | mermaid `flowchart TD` | nothing |
| `traj_panels._station_svg` | hand-built SVG | Python constants |

Nothing compares them. **Recommendation:** keep Flow 4 as the canonical id-citing
artifact; demote `concurrency-v2.md`'s two duplicates to pointers (keep `:55` — it
draws a different subject); add a participant comparator. The comparator ships
**WARN-first as its own flag that `check.py` does not wire** — *not* folded into
`--no-placeholders`, which is wired from DevStg-Tests for every adopter and would red
`tests/test_check_flows.py:34-39`'s fresh-scaffold assertion. Evaluate `tests/` as
its home first: the invariant is id-specific to *this* repo's Flow 4, and
CLAUDE.md draws that line explicitly.

### Separately — four rows describe a render that was deleted

`SR-050`, `LLR-051`, `TC-056` and `docs/status.md:152-155` all still describe the
**retired WI-250** render — "the resume loop", "two intersecting hoops … shared
`LLM_Agent` hub". WI-389 replaced it with the station cycle on 2026-08-02.
`LLM_Agent` appears in `PROJECT_STATE.html` only inside JSON registry text, never
as a rendered node. This is real drift and worth fixing regardless of which way
§7 Q1 lands.

---

## 3 · The needs

Six proposals. **Two are free-riding amendments, not new needs** — which matters,
because the timing in §5 turns on it.

> **Cost model, stated precisely.** "Live" means **non-superseded**. Amending an
> SN's acceptance intent flips **nothing mechanically** — `check_trajectory.SPINE_CSVS`
> covers only the three CSVs, so a changed need rides its SR chain only if a human
> also flips those rows. The costs below are therefore **rows a human would owe at
> the next sitting**, not harness state. (SN-029 exists precisely because that
> discipline leaks.)

Verified counts:

| SN | rows citing | **live** | superseded | live Status |
|---|---|---|---|---|
| SN-025 | 23 | **5** | 18 | all Modified |
| SN-026 | 4 | **4** | 0 | all Modified |
| SN-027 | 9 | **9** | 0 | all Modified |

<!-- fig: cmd="python3 -c \"import csv; rows=list(csv.DictReader(open('docs/requirements/system-requirements.csv'))); [print(sn, len([r for r in rows if sn in (r['SN-Refs'] or '')]), len([r for r in rows if sn in (r['SN-Refs'] or '') and not r['SupersededBy'].strip()])) for sn in ('SN-025','SN-026','SN-027')]\"" rev=f1ba5fa0 -->

All 18 live SRs across the three are **already Modified**, so the acceptance-intent
amendments add **zero rows** to the sitting that is already owed.

### A → **SN-028** (new) · one config file

*Not* an SN-003 amendment: SN-003's driver is stack-agnosticism, A's is the
adopter's config surface.

> **Need.** An adopter who wants to change how this process treats their work
> should find every such dial in one file they own, rather than discovering them
> one at a time across a directory of single-word files — and no dial's meaning
> should be carried by a file's *absence*, a state nothing displays and no `ls`
> distinguishes from "not yet considered". It matters because the kit's working
> agreement already states the principle (one fact, one home) and configuration
> is the one place the kit does not keep it.
>
> *Met when* a reader can answer "how is this repo's process configured?" from one
> adopter-owned file whose every dial is present and commented at its default,
> when no dial's meaning depends on absence, and when the kit never
> programmatically rewrites that file.

The need deliberately **does not enumerate the files** — that inventory's home is
`bootstrap.MAPPING`, and a need that lists them rots the moment it is met.

**Your grep hypothesis is half right, and stale.** The parse rule *was* chosen to
be shell-expressible — `tests/test_agent_loop_policy.py:257` says so outright
("the rule the git hooks (`head -n 1` of the non-comment lines) already
enforce"). But today **exactly one** policy value is read from shell:
`docs/privacy-check`, and not for a grep limitation — it is a deliberate
**bootstrap-order fail-closed guard** (`hooks/pre-commit:36-48`), because the hook
must decide whether a missing Python is fatal *before* it has a Python.
`docs/gate`, `gate-policy`, `push-policy`, `review-policy`, `guardrails-policy`,
`blackout` and every list/CSV/INI file have **zero** shell readers.

**The honest answer to "I do not recall why": there is no recorded why.**
`gate-policy` and `push-policy` landed 2026-07-04 at 16:18 and 16:42 — *hours
before* `stack.ini` existed (19:44) — justified only as "one word, tracked like
`docs/gate`". No commit, review doc, or archive doc states a reason for keeping the
later policies (`privacy-check` 07-06, `review-policy` 07-10, `blackout` 07-14) out
of the by-then-existing `stack.ini`. **The split is inheritance, not design.**

**Python-only core?** Already ~90% true. `agent-resume.sh` is 24 non-comment lines
— env slots, an interpreter probe, and `exec`. `check.sh`/`check.ps1` read no
configuration at all. The only substantial shell left is the three git hooks, and
that is git-protocol logic, not config parsing.

**Does 3.11 unlock it?** Partly. `tomllib` is stdlib at 3.11 and is *already* a
load-bearing kit dependency in five modules — but it is **read-only** (no
`dump`/`dumps`; the kit hand-rolled an emitter in `wi_convert.py:197` for exactly
this reason). And `configparser.write()` **destroys every comment** — verified by
round-trip. That matters enormously: the seven scalar policy files are 6,092 bytes
of which **92 lines are rationale and 7 are values**. The rationale *is* the file.

**Decision: `docs/policy.toml`, read-only to the kit, TOML via `tomllib`.** Because <!-- path-ok: proposed or upstream path -->
no kit script ever writes it, the read-only limitation costs nothing and the
comments survive every re-sync. Four things stay where they are — `docs/gate`
(machine-regenerated), `docs/privacy-check` (the M-42 fail-closed guard),
`docs/agents-enabled` (presence *is* consent), and every list/census file.

> ⚠ **`docs/privacy-check` is a deliberate second home for one fact.** The
> acceptance intent must say so, or SN-028 ships a criterion its own design
> violates. Pin the two values equal with a test.

**SRs** (one `shall` each — `trace_text.form_findings` counts them and gates under
`--strict`; `PROCESS.md:104`):

1. The coordinator, harness and hooks **shall** read every declared process dial from `docs/policy.toml`. <!-- path-ok: proposed or upstream path -->
2. `bootstrap.py` **shall** scaffold `docs/policy.toml` with every recognized dial present at its default. <!-- path-ok: proposed or upstream path -->
3. A dial reader **shall** fall back to the legacy per-file value when `policy.toml` omits the key.
4. A dial reader **shall** emit one warning naming the legacy path it fell back to. *(split from 3)*
5. No kit script **shall** write `docs/policy.toml`. <!-- path-ok: proposed or upstream path -->
6. `check_docs.py` **shall** read the status-lint budget by the same declared-value rule as every other dial reader.

SR 6 fixes a **latent defect found in passing**: `check_docs._status_lint_policy:700`
takes the **last** non-comment line while every other reader takes the **first**.
They coincide today only because all comments precede the value.

**Amends:** SR-031 ("Declared-policy readers agree", Verified) — 1 row.

### B → **SN-029** (new) · attestation depth

**Not** a replacement for `docs/gate-policy` — they are orthogonal axes and
"replace" would strand five consumers. `gate-policy` says *who may act without a
human*; the depth says *how far the human's signature reaches*.

**The collision you need to know about:** your 0–3 scale and the kit's DevStg-Reqs/DevStg-Tests/DevStg-Impl are
**not the same space**. `docs/gate` publishes what the artifacts have **met** —
the inverse of your question, which is how deep the human's signature has
**travelled**. They share inputs but answer opposite questions, so the depth must
be a **new field on the basis line**, not a reinterpretation of the gate value.

> **Need.** A human returning to this repo should see at a glance how deep their
> own signature currently reaches into the requirement chain — and that reading
> should be a consequence of the artifacts' actual state, not something a person
> remembered to update. When a need's *meaning* changes, everything decomposed
> beneath it is provisional again, and **nothing detects that today**: the needs
> file sits in no amendment seam anywhere in the kit. Separately, a human
> sometimes needs to demand a full end-to-end sitting regardless of what the
> artifacts say; that demand changes far more often and must not be confused with
> the depth.
>
> *Met when* the depth is derived from the same states the gate reads, when a
> change to an approved need's meaning drops it to its floor without human action,
> and when a demanded sitting is raised and cleared as its own auditable act.

**Your "level 4" question, answered:** it is a *volatile request*, not a
*persistent dial* — you said yourself it changes more often. So it does not belong
in `policy.toml` beside the stable dials. Give it its own presence-is-state file,
`docs/work/attest`, reusing the **declared-absences LIFECYCLE** pattern that <!-- path-ok: proposed or upstream path -->
`docs/work/active/` and `docs/work/pause` already use. Raising and clearing it are
each one reviewed commit — which is exactly the auditability a forced sitting
wants.

**The baseline-commit question, answered:** rows do not each need a git hash. The
comparison baseline is *the newest commit where the derived gate was at or above
1*, which `spine_rules.py` can find from history — and `intake.py:376` already does
`git show <rev>:docs/gate`, so the machinery exists.

**SRs:**

1. `spine_rules.py` **shall** compute an attestation depth on 0..3 from the same spine states it reads for the gate.
2. `spine_rules.py` **shall** record that depth in the `docs/gate` basis line. *(split from 1)*
3. `spine_rules.py` **shall** compute a depth of 0 when an approved need's content differs from its content at the baseline commit.
4. `check_trajectory.py` **shall** report an approved need whose approved cells changed while its downstream rows kept `Verified`.
5. `dispatch.py` **shall** drain its lanes and exit zero with a banner naming the requested review when `docs/work/attest` is present. <!-- path-ok: proposed or upstream path -->
6. `agent_common.py` **shall** read `docs/work/attest` as a declared request whose presence is its state. <!-- path-ok: proposed or upstream path -->

> **Corrected from the draft:** an earlier version put the numeric→tier mapping in
> `gate.template`. That is wrong — `gate.template` is a **one-line file containing
> `DevStg-Reqs`**, and `spine_rules.py:594` rewrites `docs/gate` **whole**, so anything
> placed there survives only until the scaffold's first run. The mapping's single
> home is `spine_rules`'s `HEADER` constant, which ships downstream and
> regenerates verbatim.

### C.1 → **amend SN-025** (free) · resume autonomy

SN-025 already carries the single-command autonomy claim; SN-006 already carries
"never blocks on a prompt and fails clearly". This is an **acceptance-intent
amendment plus new SRs**, not a new need.

> **Need (added clause).** A walk-away launch should get every unit of work the
> project's current stage actually permits, and when the machine can go no
> further, the human should return to a plain statement of *why*, naming the act
> only they can perform. The gap is the difference between "the loop ended" and
> "the loop finished everything it was allowed to do, and here is the one act
> only you can perform" — a stop a human cannot interpret is indistinguishable
> from a failure.

**Your six steps, dispositioned against what exists:**

| Step | State | Gap |
|---|---|---|
| 1 · adjudicator walks handbacks first, mints WIs, estimates model tier | **PARTIAL** | `intake._cmd_sweep` exists but is a **by-hand CLI**, not a tick-zero act |
| 2 · spawn adjudicator on spine prose change; meaning vs clarity | **MISSING** | this is SN-029's amendment detector — C.1 consumes it |
| 3 · exit with banner when depth == attest level | **PARTIAL** | it stops honestly, but the reason is a safety-class × authority cross a reader must reverse-engineer; banner is **print-only** |
| 4 · all spine WIs at the current level in one session | **MISSING** | no gate-aware admission predicate |
| 5 · non-spine items in parallel or series | **EXISTS** | `dispatch._lane_count` (CLI > `AGENT_LANES` > `stack.ini [agent-loop] lanes` > 1). **This repo declares no `lanes` key, so it runs serial.** Setting it is a config act, not a build — no work needed, but say so deliberately |
| 6 · mint a repair WI when TCs fail after a completion claim | **MISSING** | `_refresh_failed` has no repair-mint arm |

**SRs:**

1. `dispatch.py` **shall** admit no work item whose completion requires a human act the declared authority level withholds.
2. `dispatch.py` **shall** name that item and that act in its exit banner. *(split from 1)*
3. `dispatch.py` **shall** report, at every honest end state, both what it completed and the human act now owed.
4. `dispatch.py` **shall** walk every returned work item at the start of a run and mint a disposition for each return that has none.
5. `intake.py` **shall** mint a successor row rather than reopening a terminal work item.
6. `dispatch.py` **shall** mint a repair row when the declared bar fails on a branch that asserted completion.
7. `agent_loop.py` **shall** write its stop banner to a durable tracked surface.

> ⚠ **A known regression contradicts this need on day one.** `dispatch.py:388-411`
> records verbatim that a worker which merely hit its session ceiling
> (`EXIT_BUDGET`/`EXIT_STALL`) now hands back and gets a blockref, which the
> scheduler reads as *blocked* — so an unattended run can never resume it without
> a human. The code files it as "an owner call rather than a builder's". This is
> the handback change that fixed some things and broke others. **It must be ruled
> before C.1's SRs are written**, or they will be contradicted by the code they
> describe.

### C.2 → **amend SN-027** (free) · branch self-judgement

**Roughly 80% already ships** under SR-132/LLR-144 — a branch already moves its WI
spec into a terminal folder, and status **is** the directory (bijection, no
frontmatter status field). Only the **scope-immutability invariant** is genuinely
new, and it is exactly the thing you asked for.

> **Need (added clause).** A later reader should be able to trust that an item's
> **scope** is exactly what it was when the work was claimed, and that the only
> thing the branch decided was whether that scope was delivered. Today a branch
> can edit any part of its own work item — including what the item was *for* — so
> a disappointing outcome can be made to look like a success by narrowing the
> target after the fact, invisibly in every downstream artifact. A reader with
> authority should be able to overturn the branch's verdict, since a session
> judging its own work is the conflict the process already refuses elsewhere.

**SRs:**

1. The integrator **shall** refuse a merge whose branch changed a claimed work item's **scope** fields.
2. The integrator **shall** accept a branch's edits to a claimed work item's **outcome** fields.
3. `check_trajectory.py` **shall** report as an error any work item moved from a terminal state to an open state.
4. `intake.py` **shall** mint a successor work item citing the closed item when continuing work is judged necessary.
5. The adjudicating work item **shall** be able to set a merged branch's recorded outcome to a value other than the one the branch declared.

Cite **SN-024** for the override (it already states "never by the session that
authored the artifact") and **SN-008** for the scope-narrowing prohibition
("a green that hides an unmet criterion") — do not amend either; SN-024 would cost
15 rows and SN-008 eight.

> ⚠ **This edits the fail-closed waist.** `_minted_id_refusal` runs inside
> `integrate`'s four-rung ladder; a defect there does not fail one lane loudly, it
> fails the integrator **for every lane**. Full suite, not smoke. Rollback plan
> required. And the field split newly refuses merges adopters perform legally
> today — needs a warn-first window.

### C.3 → **SN-030** (new) · queue-admission conflict vetting

No existing SN reaches queue admission. Today an item is admitted if its id is
well-formed and unique and its predecessors resolve — nothing asks whether the
requirement it cites still means what it meant, or whether another queued item
aims at the same target.

> **Need.** Work should not enter the queue while it silently contradicts either
> the project's agreed scope or another item already waiting. The cost lands later
> and lands twice: two agents build overlapping work that collides at
> integration, or an item is built against a requirement whose meaning moved
> underneath it — and in both cases the waste is only discovered after the work
> exists. The queue is the one place a cheap question prevents an expensive
> answer.

**SRs:**

1. `intake.py` **shall** record, in each work item it mints, every other open item citing a requirement the new item also cites.
2. `check_trajectory.py` **shall** report as an error under strict verification any queued item citing a requirement amended after that item was last edited.
3. `intake.py` **shall** refuse to mint a work item whose cited requirements are all superseded.
4. `schedule.py` **shall** exclude from the ready frontier any queued item carrying an unresolved recorded overlap.

Slice one is cheap: `intake._context_block` **already computes a `siblings` set and
discards it**. Emit it.

**Free alternative, stated honestly:** fold C.3 into SN-027 instead (all 9 SRs
already Modified → zero cost). I recommend the new SN because SN-027's subject is
fan-out and serialized integration and queue admission is a different subject —
but the cheaper option is real and yours to take.

### D → **amend SN-026** (free) · model routing

**Most of D already ships.** `docs/agents.csv` (`Id,Family,Model,Version,Tier,
CmdTemplate,Env,Notes`) already carries providers, models, per-agent argv
templates, env, and a tier; `docs/agents-enabled` already carries ordered ids
**with optional per-phase weights**; fallback to same-strength-or-higher already
exists. SN-026 was minted 2026-08-07 and already names both files.

**The gap is narrower than the phrasing implies**: the routable job vocabulary is
narrower than the set of jobs that exist. The sessions that judge a returned
item's disposition and the session that breaks a tie between competing plans both
run on **whatever model was ambient** — so the two most consequential judgements
in the loop are the two least deliberately staffed.

> **Need (added clause).** Every kind of judgement this process asks a model to
> make should be routable to a model chosen for that judgement, with the mix
> across a run declared rather than incidental. The value of configuring several
> model families is that different judgements benefit from different strengths and
> different blind spots — a judgement staffed by accident is a judgement whose
> independence is unverified.

**SRs:**

1. `agent_route.py` **shall** resolve a model row for the adjudicating session from the declared registry.
2. `agent_route.py` **shall** accept a declared draw weight for every named job type.
3. `plan_runner.py` **shall** resolve the tie-breaking session's model from the declared registry.
4. `agent_route.py` **shall** record, in the launch log, the reason a selected model differs from the preferred one.

> ⚠ **"Ratio pool" is ambiguous and the two readings differ by an order of
> magnitude.** (a) *proportional single-selection* — weighted draw of one model per
> session; this **ships today** and D is a vocabulary widening. (b) *N concurrent
> sessions merged* — does not exist and is a major build. §7 Q2.

### E, F → **SN-031, SN-032 reserved**

Ids allocated, **no content invented**. Current high-water is SN-027 (SN-001..027,
no gaps), so SN-028..032 are free.

> ⚠ **Do not write the tokens `SN-031`/`SN-032` into
> `docs/requirements/stakeholder-needs.md`.** One draft or uncited SN token drops
> the derived gate **DevStg-Tests → DevStg-Reqs**, and at DevStg-Reqs the traceability, design-flows,
> trajectory `--strict` and approval-fresh steps all leave the required plan. The
> reservation's home is **this document plus the WI spec** until real content
> exists. A named step in §5 owns retiring it.

---

## 4 · Prompt reviewability — the ceiling on all of the above

You asked how this influences automation so far. **It is the ceiling, and the
ceiling is low.**

| Tier | Bytes | Reviewable? | Drives |
|---|---|---|---|
| 4 Python constants in `agent_loop.py` | 6,182 | ❌ code only | **100% of the default walk-away loop** |
| 3 markdown files in `prompts/` | 6,783 | ✅ prose | only the opt-in `--dual-plan` layer; **not scaffolded** |
| f-strings assembled at dispatch | ~1,083 | ❌ **no file contains the text** | worker/critique/context/repair |

**The prose that actually drives automation is the least reviewable prose in the
repository, and the prose that is reviewable drives almost nothing.**

There is **no prompt lint, no golden, no snapshot, and no `--print-prompt`** — a
human cannot read the composed text before it is sent. The only prompt evidence
surviving a run is the integer `prompt-chars` in the session-log header; the actual
text appears in **4 of 212** committed session logs, and only because the codex CLI
echoed its own stdin.

**The drift is not hypothetical.** `tests/test_agent_loop.py:763` still asserts a
`WORKER_PROMPT` opening sentence **that no longer exists**, passing only through an
`or` fallback. Four prose-vs-machinery contradictions are live, the sharpest being:
the arbiter prompt tells the model *"The plans are provenance-anonymized"* while
**only the A/B labels swap** — nothing strips provenance from the plan text, and
the instruction that would have told a human to anonymize sits in the dispatcher
block that `strip_dispatcher_block` **deletes before sending**.

**Why this is a prerequisite and not a follow-up:** every SN here pushes *more*
judgement into that surface — C.1 wants an adjudicator to judge returns, C.2 wants
a branch to self-judge and an adjudicator to override, C.3 wants conflict vetting,
D wants an Adjudicator job type. `docs/enforcement-audit.md` carries **zero rows for
prompt prose** across its 108 lines. So the strongest available enforcer for every
new judgement in this batch is **"Prose"** — the weakest tier the kit recognizes —
applied to text the kit does not review.

**Recommended first move** (~1 day, and it is step S3):

1. `agent_loop.py --print-prompt <phase>` — composes and prints without dispatching. Zero structural cost; `agent_loop.py` keeps its single-file-copyable property.
2. A golden per phase under `tests/golden/prompts/`, using the mechanism `tests/golden/{clean,offspine,orphan}.txt` already provides for `trace.py`. Turns prose drift from invisible into a red diff. <!-- path-ok: proposed or upstream path -->
3. One `enforcement-audit.md` row per prompt surface.

**The trade, stated honestly:** moving the four constants into files would cost
`agent_loop.py` its single-file-copyable property and force every adopter to carry
four more files; a renderer alone leaves prose diffs invisible in code review. The
renderer-plus-goldens combination gets both properties.

---

## 5 · Sequencing

**S0 · Unblock the launch trap — before anything else.** Re-create `docs/work/pause`
naming this restructure. The ready frontier's first row is WI-390 (spine, rank 0),
and a spine row dispatches at *every* gate-policy level; `docs/work/pause` was
deleted 2026-08-02. Also decide WI-416: its work is parked off trunk on
`wi416-parked-handback-contract` while its spec sits in `queued/` with **no
blockref**, so the scheduler reports it ready and a launch would redo the parked
work. *Blocks everything.*

**S1 · Correct the stale prose the SRs would otherwise be written against.**
(a) `status.md:276-281` claims a plain `agent-resume` launch "refuses with the map"
— the code sends it to `dispatch.run` (`agent_loop.py:2650`), and C.1's entire
premise is what resume does *today*. (b) `status.md:152-155` (the retired hoops
render). (c) `README.md:324` says gate "DevStg-Impl (derived)" while `docs/gate` reads DevStg-Tests.

**S2 · Land every needs-text edit inside the currently-open window — free ones
first.** `PROCESS.md:333-337` is explicit: *"Sequence requirement-text work INTO an
open window, not after it… Landing it after a re-attest flips freshly-blessed rows
straight back to Modified and buys a second sitting for the same reading."* Free
amendments: SN-025, SN-026, SN-027 acceptance intents. New: SN-028, SN-029, SN-030.
Cheap flips to absorb: SR-031, and SR-050 + LLR-051 + TC-056.

**S3 · Make the prompt surface reviewable** (§4). A prerequisite, not a follow-up.

**S4 · Build SN-028.** Write `policy.toml.template`; add `read_policy()` with
TOML-first/legacy fallback and a one-shot warning; migrate readers script by
script, re-fingerprinting the dupes census as the F5 copies change; fix the
last-line/first-line divergence; map in `bootstrap.py`. **Do not retire the legacy
path in this change.** Run **byte-budget-guard before and after** — `PROCESS.md`
(baseline 64,460) documents this surface; expect `PROCESS_OPTIONS.md` to absorb the
detail.

**S5 · Build SN-029.** Un-archive `docs/specs/derived-gate-model.md` first — 15 <!-- path-ok: proposed or upstream path -->
files cite that live path and it exists only under `docs/archive/`. Then
`attest-depth=N` on the basis line (+ mapping in `spine_rules`'s `HEADER`), with
`--check` tolerant of the field's absence **on the old side only**; extend
`check_trajectory`'s amendment seam to the needs markdown reusing
`_split_changed_cells`; add `docs/work/attest`. **Do not touch `gate-policy`'s <!-- path-ok: proposed or upstream path -->
three-word vocabulary.** Byte-budget-guard again.

**S6 · Owner ruling on the handback contract.** `docs/archive/history/handback-contract.md` states
*"Nothing here executes until ruled."* Its §10 lists five questions; none is
answered in the tree. Five mechanisms for return-event identity have been driven
and **all five leaked**; WI-413's merged design had to be reverted off trunk. This
is a human act. *Blocks C.1 step 1, C.2's never-revive clause, WI-390's close.*

**S7 · Build the behaviour SNs, in dependency order.** (a) D's vocabulary widening
— smallest; needs S3. (b) C.3 slice one — emit `siblings`; promote
`backlog_staleness_findings` to error-under-strict **only after measuring how many
findings it produces today**, and give adopters a warn-first window. (c) C.2 — the
scope/outcome field split; needs S6. (d) C.1 — the disposition walk,
successor-minting, the repair arm, the gate-aware predicate consuming S5's depth,
and a durable stop surface; needs S5 and S6.

**S8 · Cleanup, as its own commit** (§ below).

**S9 · Diagram consolidation** — sequenced late because it is lowest-confidence and
depends on §7 Q1.

**S10 · Close the window: one re-attest sitting.** Everything above is arranged so a
single sitting covers the original 21 Modified rows *plus* everything this
restructure touched. Generate with `trace.py --approve modified --out`. Also: retire
the SN-031/SN-032 reservation from this doc into real content or an explicit
carry-forward. **Do not close earlier.**

---

## 6 · What the waiver does and does not switch off

The waiver means **not running the full DevStg-Reqs/DevStg-Tests/DevStg-Impl approval ceremony** for each
step of a change to the infrastructure that implements those gates. It does **not**
stop:

- `spine_rules.py` recomputing the gate on every commit, and `--check` byte-comparing the basis line
- the **module-size ratchet** firing on any shrink below baseline (baselines are **exact, not ceilings**)
- the dupes census reddening on a changed fingerprint
- 30 test modules naming the config files by path
- `gen_trajectory --check` byte-comparing the dashboard

**State this boundary explicitly in the WI spec**, or a session will assume the
checks are off and land a red.

> ⚠ **The enforced floor is already reduced.** The advisory tier is active
> (`modified=21`), so format/lint/doc-refs/figures/dupes are non-gating **right
> now**. Do not widen that — it is the WI-333 hole where "regressions accumulate
> green".

> ⚠ **Do not name this plan's WI ids in `status.md` hand prose.**
> `integrate._status_prose_refusal` refuses the claim outright for any id appearing
> there — a plan written into `status.md` makes its own work items unclaimable.

---

## 7 · Owner decisions — the plan stalls without these

1. **The diagram question is RESOLVED** (§2): the file was `PROCESS.md:587`, it has **zero overlap** with the dashboard, and the recommendation is to **leave it alone**. What remains optional is the *separate* finding — the station-cycle 3× duplication and the four rows describing the deleted render. Take S9 or drop it; nothing else depends on it.
2. **"Ratio pool"** — proportional single-selection (ships today) or N concurrent sessions merged (major build)?
3. **The handback contract ruling** (S6) — five open questions, none answered. *Blocks C.1 step 1 and C.2.*
4. **Does "never revive" retire R3's approved re-queue outcome?** `check_trajectory`'s own remedy text currently *recommends* revival, and this repo has a revival precedent (`b5ea0647`). Downstream repos that have reopened a WI would red without a warn-first window.
5. **"Conflict" in C.3** takes one of three definitions, one of which reverses a standing ruling.
6. **Scope collision with WI-390** — `handback-contract.md` §11 says WI-390 will amend the same rows in the same window. Absorb it, or sequence into its sitting? Doing neither means two batches amending the same rows.

---

## 8 · Cleanup

**Two corrections to the premise, both verified:**

- **There is no existing dead-code work item.** A grep of every WI title across all five folders returns 40 rows, none scoping dead-symbol removal. The closest, WI-390, **explicitly forbids it** ("NOT a sweep-up-dead-code row, and must not be built as one"). File a new WI.
- **There are no dead work items.** `draft/` and `deferred/` each hold only a zero-byte `.gitkeep`. All 6 real queued rows have verified-live context.

**Confirmed dead** (~35 lines of function + ~20 of constants):

| Symbol | Site | Note |
|---|---|---|
| `_by_id(wis)` | `schedule.py:576` | born unused at WI-179 |
| `_norm_anchor(f)` | `score_reviews.py:230` | born unused |
| `_field_value` + `_ONELINE_LABEL_RE` + `_RECO_LABEL_RE` | `traj_status.py:120,111,114` | orphaned by WI-322. **`_OI_ID_RE` at :117 is still live** — do not delete |
| `prompt_text` | `bootstrap.py:713` | appears in the *generated* arch map — regenerate in the same commit |
| `SPEC_EXAMPLE` ×3 | `agent_common.py:687`, `schedule.py:263`, `check_trajectory.py:390` | changes an existing dupes fingerprint |
| `_NUL`, `SR_SURFACE_COLUMNS`, `SEVERITIES` | `check_vendored.py:93`, `plan_briefs.py:76`, `score_reviews.py:65` | siblings of each are live — the asymmetry is the tell |

**Explicitly NOT dead — do not touch:** `GraphGeom.__iter__` (invoked implicitly by
tuple unpacking) and `gen_arch_map.reference.ps1` (a deliberate PowerShell
reference port documented in two places — the honest finding is that it is
*untested*, not dead).

**`docs/archive/history/parallel-ready` is dead config** (zero readers) but is a **signed** audit
artifact (WI-208) — **archive it, do not delete**. The kit does not destroy signed
records.

**Same-commit obligations, non-negotiable:** re-stamp
`tests/test_module_size_ratchet.py` (`bootstrap.py` 2278, `agent_common.py` 1839,
`check_trajectory.py` 3531 are exact); re-fingerprint `docs/dupes-allow` (run
`check_dupes.py` **before and after** — do not guess); regenerate the arch map.

**Fold in the doc rot** — it becomes gating the moment the window closes.
`check_doc_refs --strict` reports 5 dangling refs, **two fresh regressions from the
last two commits** (WI-419 and WI-420 both cite `tests/test_stdlib_only.py`, which <!-- path-ok: proposed or upstream path -->
`0a487767` deleted).

**Out of scope, recorded as a decision:** nested functions, unused parameters,
unreachable branches, and dead code in `tests/`. Mechanizing those needs ruff
F401/ARG or vulture — and `docs/dependencies.md` declares **zero `Kind=python`
rows** today.

---

*Survey: 9 parallel agents + 3 adversarial critics, ~2M tokens. Every load-bearing
figure re-verified against the tree before inclusion; two critic findings were
themselves refuted and dropped.*
