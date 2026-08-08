# Plan — SN build-out for the fully mechanized loop (2026-08-08)

Owner-directed planning pass over the six new stakeholder needs (A–F) plus the
end-of-plan cleanup items. **Nothing here executes until reviewed.** Built from
five parallel exploration passes over the live machinery (handback, gate/
attestation, config surfaces, prompt templates, WI lifecycle); every claim below
names the file it was measured in.

Execution mode, per the owner's directive: because these changes rewrite the
loop's own machinery, the implementation **does not run through that machinery**
— one dedicated infra branch, no WI minting per change, the full unfiltered
suite (`pytest -q -n auto`) as the bar at each phase close. The spine rows this
plan mints are the *record* of the work, ratified at the end, not the vehicle
for it.

---

## 1. Where the new needs land on the current spine

Current spine: **SN-001..027, SR=136, LLR=137, TC=135**, derived gate **G2**
with **21 `Modified` SRs** — the 2026-08-07 cleanup (SN-011 amended, SN-025
narrowed, SN-026 multi-family routing + SN-027 parallel lanes minted) already
owes one re-attest sitting. That matters: several "new" needs below are
*amendments or children of rows already in flight*, so the honest move is **one
combined drafting-plus-re-attest sitting**, not two.

| Scratch item | Disposition on the spine | Why |
|---|---|---|
| SN A (single config file) | **New SN-028** | Not covered; SN-003's "declared once in `stack.ini`" covers the *stack*, not the ~14 scattered policy files |
| SN B (human attest level) | **New SN-029**, supersedes the `docs/gate-policy` contract inside SN-025/SN-004's orbit | Replaces the 3-enum `attended\|single-ratify\|autonomous` with a numeric level |
| SN C.1 (max-autonomy resume loop) | **New SN-030**, extending SN-006 + SN-025 | ~70% already built (see §4); the SN states the *loop order contract* |
| SN C.2 (lane self-judgment) | **New SN-031** — and it *is* the answer to the open [handback-contract.md](handback-contract.md) ruling | See §5; this closes the pause on WI-416/417/418 |
| SN C.3 (queue-conflict vetting) | **New SN-032** | Real gap: today only mechanical dedup (exact-title, duplicate id, exclusive keys) exists — no scope-overlap vetting |
| SN D (model/provider table) | **Amend SN-026**, no new SN | `docs/agents.csv` + `docs/agents-enabled` already carry family × model × tier, per-phase ratio weights (`PHASE=weight`), up-never-down fallback, cross-family review preference. Gaps are job-type vocabulary + adjudicator routing (§7) |
| SN E / SN F (placeholders) | **Reserve nothing** | A placeholder row is exactly what `-000` exemplars and `trace.py --no-placeholders` exist to keep out of a live registry; mint when real |
| Cleanup (dead functions / dead WIs) | Two small rows at the end | Findings in §9 — the remembered "unused functions WI" **does not exist** |

Drafting mechanics: new SNs go under a `## Draft needs` heading in
`stakeholder-needs.md` — `derive_gate.py`'s section-as-state rule then holds the
gate down honestly while they're worked (`sn_draft_ids`), and `ex-draft=` keeps
the window arithmetic honest. Expect the gate to read G0/G1 during the sitting;
that is the design working, not a regression.

---

## 2. SN A — one configuration file (and the owner's three questions)

### Why it is scattered today (the recollection, resolved)

There was never a "many files" ruling — the idiom accreted. The real constraint
the owner half-remembers as "grep could only return the first line" is the
**pure-sh parse in the git hooks**: `hooks/pre-commit:46`, `commit-msg:36`,
`pre-push:73,142` read `docs/privacy-check` / `docs/review-policy` with
`grep -v '^#' | head -n 1` because repo-review M-42 (2026-07-21) required a
**Python-less box to still fail closed** on a declared privacy policy. A
one-word-per-file format is the only thing that parse rule can read — that, plus
the old Python 3.8 floor's "no `tomllib`" rejection of TOML (Thread 30 Q2), is
the whole story. Everything else (launchers, CI, check.py) already parses config
in Python only.

### What 3.11 changes

The floor is now 3.11 (WI-262), `tomllib` is stdlib and already used in four
modules (`wi_convert`, `schedule`, `agent_common`, `traj_status`). The 3.8
argument against TOML is dead. What remains true: **stdlib has no TOML writer**
(`wi_convert.toml_string` is hand-rolled) — fine, since config is hand-edited,
machine-read.

### Design: `docs/process.toml`, with three deliberate exceptions

One adopter-owned TOML file absorbing every *policy dial*:

```toml
# docs/process.toml — how items are processed. Hand-edited, machine-read.
[attestation]
# 0=SNs in process; 1=SNs ratified, SRs in process; 2=+LLRs; 3=+TCs in process
human-attest-level = 3        # replaces docs/gate-policy (see SN-029)
final-review = "always"       # "always" | "off" — the level-4 full-breakdown hold

[policies]
push = "human"                # was docs/push-policy
review-rounds = 1             # was docs/review-policy
privacy-check = false         # was docs/privacy-check
secrets-scan = true           # was docs/secrets-scan (absent=true today)
guardrails = "off"            # was docs/guardrails-policy
# blackout = "22:00-06:00"    # was docs/blackout
```

The three exceptions, each with a stated reason, documented in the file header:

1. **`docs/stack.ini` stays** (or becomes `[stack]` tables in the same TOML —
   see the option below). It is the *product toolchain*, adopter-owned across
   re-syncs, with five Python consumers and a working format.
2. **Presence-as-semantics files stay files**: `docs/work/pause` (delete-to-
   resume is the whole contract) and `docs/agents-enabled` (presence = consent
   to managed routing). A key in a shared file cannot express
   deletion-as-an-act or survive as a one-line reviewed diff.
3. **`docs/gate` stays** — it is a *generated cache*, not configuration.

**The sh-hook problem, solved without abandoning fail-closed:** keep the two
security-relevant keys greppable by convention — the TOML is written one
`key = value` per line, so the hook parse becomes
`grep -E '^privacy-check *= *true' docs/process.toml` (keyed match, not
first-line — which is precisely the limitation the owner remembered). Python
consumers read it with `tomllib` and *validate* that the greppable keys parse to
the same value (a cheap cross-parser agreement test, the same pattern WI-1.21
used when the four declared-file readers diverged). If the owner prefers zero sh
parsing, the fallback design is: hooks call `python -c` and **fail closed on a
missing interpreter** — stricter than today, and acceptable now that the floor
is enforced by `dev-setup`.

**"Convert the whole spine/trace layer to Python-only with cmd/sh starters?"**
— it effectively already is. `trace.py` reads no config at all;
`agent-resume.{cmd,sh,command}` parse nothing and exec Python; CI parses
nothing. The *only* shell config parsing in the toolchain is the two hook reads
above. So SN-028 is a consolidation of ~10 one-word files into one TOML plus a
reader shim, **not** a rewrite. `agent_common.read_declared` grows a
process.toml-first lookup with the legacy files as a deprecation fallback (one
release of dual-read, warn on the old file, so adopters migrate on resync).

Touched: `agent_common.py` (reader), `bootstrap.py` (scaffold + policy
appliers), the three hooks, `check_privacy.py`, `agent_loop.py`/`dispatch.py`/
`intake.py`/`integrate.py`/`agent_route.py`/`plan_round.py` call sites,
`process.toml.template`, ~12 test files. Downstream migration: resync note +
`downstream-resync` skill section — the dual-read window makes it non-breaking.

---

## 3. SN B — the human attest level

### The model

One integer, **in-process semantics** (what is being *developed*, not what is
ratified): `0` SNs in process → `3` TCs in process, plus the separate
`final-review` toggle for the "always show me the full breakdown at the end"
hold — split out precisely because the owner expects to flip it more often than
the level itself. Comment block above the value maps every number (see the TOML
sketch in §2). Enum-vs-int: **int**, as the owner leans — the comparison the
dispatcher makes is ordinal (`in-process level` vs `human-attest-level`), and an
enum would re-introduce string tokens into five consumers.

### What already exists (most of it)

- "A meaning-change forces the level back down" **is built**: a ratified-cell
  edit without a same-commit `Modified` flip warns at stage
  (`check_trajectory.staged_spine_findings`, WI-316), the flip pulls the derived
  gate down (`derive_gate.sr_gate` — `Modified` reads G2, `Draft` reads G0), and
  every merge-slot ratified-cell diff **deterministically mints an adjudication
  WI** with before/after in its body (`intake.py` trigger (a)).
- "Which comparison baseline?" — answered, and **without a per-row hash
  column**: `trace._attested_baseline` derives each row's last-attested commit
  from git history (sound under the enforced amend+flip-same-commit regime), and
  the rendered surfaces stamp the baseline sha (`open-items.html`
  `attestation-baseline` comment; ratify briefs' `_Baseline`). Recommendation:
  **keep it derived** — a hand-carried hash column is exactly the mutable-proxy
  pattern that failed five times in the handback saga (§5). Record this as the
  SN's acceptance note so the question stays answered.

### What changes

`docs/gate-policy` (`attended|single-ratify|autonomous`) retires in favor of the
level. The mapping the consumers need:

| Consumer | Today | Under SN-029 |
|---|---|---|
| `dispatch._kind_action` (§A8 admission) | attestation/gate rows "surface" under attended, dispatch under autonomous | attestation rows at or below the human level **surface**; above it, dispatch |
| `intake.reattest_flip` | mechanical `Modified→Verified` allowed under autonomous | allowed only for spine levels **above** the human level; at/below, it writes the brief and waits |
| `agent_route.failure_action` | 3-way page/keep/redesign | derived from whether the failing row's level is human-held |
| `_surface_banner` exit | "N ratifications waiting in open-items.html" | same, plus prints the level comparison that caused the hold |

The adjudicator's **meaning-vs-clarity** judgment (scratch C.1 step 2) is the
one genuinely new piece: today the autonomous flip is mechanical (no-scope-moved
only). Add a prompt template (`prompts/adjudicate-amendment.template.md`, §8)
that shows the adjudicator the per-cell before/after from `trace.reattest_model`
and asks exactly one question — *changed meaning, or changed clarity?* —
clarity ⇒ row stays `Verified` (flip restored), meaning ⇒ stays `Modified` and
the derived level follows automatically. The human-attest-level then decides
whether that verdict is final or itself surfaces for override.

---

## 4. SN C.1 — the resume-loop contract, mapped rung by rung

The dispatcher's actual tick order today (`dispatch.run`): pause → dirty-trunk →
poll lanes → admit from frontier under the §A8 table → idle-exit ladder
(gap-census mint → surface banner → honest drain). The six numbered steps land
on it as follows — **most of the loop exists; the deltas are ordering, three
templates, and one estimator**:

| Scratch step | Exists today | Delta |
|---|---|---|
| 1. Dispose handbacks first; adjudicator checks disposition, files gap WIs, estimates model level; closed WIs never revived | Intake mints the disposition row at merge; adjudication rows are `exclusive` rank-1; no-revival is convention + R-A hard error; `buildtier`/`planmode` frontmatter already carries the model-level estimate | **Ordering rung**: admission prefers `adjudication`-kind rows over all other ready work (one-line frontier sort key). **Estimator**: the disposition template (§8) must *output* `buildtier`/`planmode` for any successor row it drafts — today intake mints with defaults |
| 2. Prose change ⇒ spawn meaning-vs-clarity adjudicator | Mechanical detection built end-to-end (WI-316 + intake trigger (a)); baseline derivation built | The template + wiring per §3 — no new detection machinery |
| 3. No handbacks + level at human-attest + all queued work above it ⇒ EXIT with banner; needs surface in open-items.html | Built (`_surface_banner`, `gen_open_items.py`, the WI-381 three-surfaces-agree rule) | Re-key the comparison from gate-policy enum to the numeric level (§3 table) |
| 4. Spine WIs at current level batch into one session | Built — `spine` kind is an exclusive **batch** (one branch, one re-attest window, §A4) | **Component-scoped batching** at levels 2/3: allow the batch to split by `Component` (the LLR/TC registries already carry it) when the whole-spine batch exceeds a size threshold. Design note, opt-in dial, not default |
| 5. Else non-spine work, parallel or serial as required | Built — SN-027 lanes, `exclusive|parallel` × rank axes | None |
| 6. TCs red after implementation claimed ⇒ adjudicator estimates effort, drafts a fix-to-green WI | Half-built: the idle-time `gap_census` (reuses `trace.analyze`) already mints rows for unverified SRs | Extend the census to classify *failing-Evidence* TCs distinctly and route them through the estimator template rather than a default-tier mint |

SN-030's text should state the **priority order as the contract** (dispositions
→ amendment adjudication → surface-or-dispatch by level → spine batch →
non-spine → red-TC intake), so the order is ratified prose the tests pin, not
an emergent property of the tick loop.

---

## 5. SN C.2 — lane self-judgment with adjudicator override (the handback ruling)

This is the open ruling in [handback-contract.md](handback-contract.md), and the
owner's direction *modifies its §5*: the contract doc recommended the lane never
judge (single `returned/` state); the owner now wants the lane to judge —
**Complete / Cancelled / Partial** — with the adjudicator empowered to review
and override. The synthesis that keeps both truths:

> **The lane's folder move is a *claim*, not a verdict. The adjudicator's
> review makes it authoritative — by minting, never by mutating.**

Design, answering the contract doc's §10 questions directly:

1. **Per-return document: YES** — generalized to a **per-close report** for
   every non-merged-clean outcome. The lane writes one immutable file per
   event under `docs/handbacks/` (outside `docs/work/`, honoring the §8
   `spec_files` rglob trap): lane name, claimed outcome, reason, commit range,
   what-was/wasn't delivered. The document *is* the event identity — this is
   what dissolves F1/F2/F4/F7, the root of all five failed dedup mechanisms
   (every one tried to reconstruct the return event from a mutable proxy).
2. **Lane chooses the folder**: `complete/`, `cancelled/`, or the **new
   `partial/`** directory (added to `SPEC_STATUS_DIRS` in all F5-synced copies,
   `_TERMINAL_DISPOSITION`, loaders, dashboard views). `partial/` is terminal —
   nothing re-claims it, so nothing strands — replacing today's
   handback-into-`queued/`+`blockref` shape entirely. `blockref` survives as
   the *general* blocked-row mechanism it always was (47 sites, predates
   handback).
3. **R3's re-queue outcome retires.** Continuing partial work = the adjudicator
   drafts a **successor WI** (drafts-not-mints, minted at its merge), carrying
   explicit lineage (`supersedes = "WI-nnn"` frontmatter key) so partial work
   keeps its thread across the id change. This satisfies the owner's "closed
   WIs are never revived; scope definitions never change — only whether they
   were fully delivered": the spec is immutable in the branch (only trunk edits
   definitions, and after this change trunk only edits *open* ones), and the
   outcome folder + report record delivery, not scope drift.
4. **Adjudicator review scope**: every `partial/` and `cancelled/` close gets a
   disposition row (as handbacks do today — intake's trigger (b) re-keys from
   "`## Handback` section merged" to "report document merged", which *simplifies*
   dedup to file-existence vs disposition-existence). `complete/` closes are
   **spot-checked, not gated**: the merge slot already runs the declared bar on
   the composed tree, and the review-round machinery already judges the work
   itself; a mandatory adjudication of every green close would rebuild the
   verdict gate under a new name. Override = mint a corrective successor and
   record the overridden claim in the disposition — the original folder move is
   never reversed (history stays honest).
5. **WI-413** defers (its brief targets the old contract; the new contract
   dissolves its defect class), **WI-416** is re-decided against this ruling
   with its review re-run, **WI-417** mostly dissolves — the reason string stops
   carrying disposition (`NEEDS-HUMAN`) because the *claimed outcome field* in
   the report now carries it, typed; the tier-selection half of WI-417 moves
   into the report schema (an explicit `suggested_tier` field replacing the
   magic substring at `intake.py:151`). **WI-418** (anchoring) is addressed
   structurally by §8's template rules.

Also fixed in passing, because it bit live on 2026-08-03 (`08e6c08a`): a green
handback merges rejected code onto trunk as-is. Under the new contract a
`partial/` close **must state in its report which commits are keep vs discard**,
and the integrator gains a rung that refuses a `partial/` close whose report
omits that split — the revert decision becomes the adjudicator's explicit call
instead of a hand cleanup.

Migration: measured at **one file** (WI-413 is the only spec carrying
`## Handback`). Amendments: §A3's outcome table in `concurrency-v2.md`, R3's
outcome list, `SPEC_STATUS_DIRS` ×3, `handback.py` (becomes the report writer),
`intake.py` trigger (b), `schedule._disposition`, `integrate.branch_outcomes`,
~27 named tests.

---

## 6. SN C.3 — queue-conflict vetting

New rung at the two places a row *becomes* `queued`: intake's mint arms and any
`draft/ → queued/` promotion. Two tiers:

- **Mechanical pre-filter** (cheap, always on): duplicate/near-duplicate title,
  overlapping `sr_refs` with an open row, shared `exclusive` key, `specref`
  pointing at a file another queued row's specref claims. Warn-first, in
  `check_trajectory.py` (its natural home — it already owns registry findings).
- **Adjudicator judgment** (template, §8) for what mechanics can't see: does
  this row's scope contradict the current spine or another queued row's scope?
  Runs inside the disposition/mint session that created the row — not a new
  session class. Output: queue as-is / queue with a `needs` edge / return to
  draft with the conflict named.

---

## 7. SN D — the model/provider table (mostly: verify, document, extend)

What the scratch note asks for vs what `agent_route.py` + `docs/agents.csv` +
`docs/agents-enabled` already do:

| Asked | Status |
|---|---|
| Table of providers/models/arguments | **Exists** — `agents.csv`: `Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes` |
| Which job types each model performs | **Exists as phases** (`PLAN`, `BUILD`, `REVIEW-A/B`, `CRITIQUE`, `DUALPLAN-*`) via per-phase weights in `agents-enabled` and `DEFAULT_PHASE_TIER` |
| Ratio pool per job type | **Exists** — `PHASE=weight` annotations drive weighted draws |
| Unavailable ⇒ fall back same strength or higher | **Exists** — cooldown + escalate **up, never down** |
| Planner/Reviewer/Implementer/Adjudicator/Arbiter vocabulary | **Gap** — Arbiter exists only inside dual-plan (`DUALPLAN-ARBITER` hat); **Adjudicator is not a routed phase at all** (adjudication rows route as ordinary builds today) |

Deltas: add an `ADJUDICATE` phase key (tier default: strong; cross-family
preference **on** — the adjudicator judging a lane's claim should not share the
implementer's family, same reasoning as reviewers), document the job-type ↔
phase mapping in one table inside `agents.template.csv`'s header comments, and
fold the whole selection surface into `docs/process.toml` *references* (the CSV
stays a CSV — tables in TOML are worse to hand-edit; the TOML names the file).
SN-026's acceptance text amends to name the adjudicator draw — it is already
`Modified` from 2026-08-07, so this rides the same sitting at zero extra
ceremony.

---

## 8. Prompt templates — reviewable prose, and how prose has steered automation

The owner asked for this inside the plan so the review can see how template
prose is already influencing the loop.

**Current state (measured):** the dual-plan hats are the good pattern — three
standalone files under `project-trajectory/prompts/` with strict `{{SLOT}}`
fill (unknown/unfilled raises), allowlist redaction, a stripped
`<!-- DISPATCHER NOTES -->` block, and preflight failure on a missing file. But
the three highest-traffic prompts — **worker, reviewer, critique — are Python
string constants inside `agent_loop.py`** (lines 259/299/347), reviewable only
by reading source. Tests do grep the *as-launched* prompt text (fake-CLI
`prompts.txt` capture), which is the right assertion layer and survives the
move.

**How prose has already shaped outcomes:** (a) WI-418 is an open finding that
derived prose injected at claim-time *anchored* the agent — the WI-416 judge's
brief opened with the defendant's clipped verdict; (b) the reviewer prompt's
redaction-by-construction (diff + requirements only, never the implementer's
self-assessment) exists because leaked self-assessment collapses review to
corroboration — and there's a test pinning the exact adversarial clause; (c)
the `NEEDS-HUMAN` magic substring (a prose token doing a config job) silently
selects review tier and typos downgrade it (WI-417). The pattern across all
three: **prose that carries control flow must be a typed field; prose that
briefs a judge must not contain the claim under judgment.**

**Plan:** move WORKER/REVIEWER/CRITIQUE into
`prompts/{worker,reviewer,critique}.template.md` under the existing hat
machinery (loader, strict slots, preflight, `--prompt-map` override unchanged);
author the four new adjudicator templates as files from day one —
`adjudicate-amendment` (meaning vs clarity, §3), `adjudicate-disposition`
(handback/partial review + successor drafting + tier estimate, §5),
`adjudicate-conflict` (queue vetting, §6), `adjudicate-red-tc` (effort
estimate, §4 step 6). Template authoring rules, stated in `prompts/README.md`
and pinned by tests: every slot's content is named and bounded (clip lines
declared), verdict/outcome lines are machine-typed (`VERDICT:` /
`OUTCOME:` + enum), and a judge's brief never includes the judged party's
self-assessment (the WI-418 rule, generalized). Each template ships with a
fake-CLI test asserting the launched prompt carries its load-bearing clauses —
prompt prose becomes diffable, reviewable text with a regression net.

---

## 9. Cleanup findings (the "at the end" items)

- **"There is likely already a WI for unused functions" — there is not.** The
  queued set is WI-000 (exemplar), 390, 413, 415, 416, 417, 418. WI-390
  explicitly *forbids* being built as a dead-code sweep. So: one new row,
  scoped as a measured sweep (`gen_arch_map` symbol inventory × grep of call
  sites; the module-size ratchet already catches growth, nothing catches
  orphaned symbols). Cheap, end-of-program.
- **Dead WIs with no context: none found.** Every queued row carries live
  context. The one superseded-in-motion row is WI-413, and §5 disposes it
  (defer) as part of the ruling rather than a separate sweep.

---

## 10. Sequencing

Ordered so each phase leaves the loop runnable, with the ruling first because
three queued rows and the paused grind wait on it:

| Phase | Contents | Depends on |
|---|---|---|
| **P0 — Sitting** | Owner ratifies: this plan's §5 as the handback ruling (contract §10 answered); drafts SN-028..032 under `## Draft needs`; combines with the owed 21-row re-attest. Dispositions: WI-413 defer, WI-416 re-decide, WI-417 fold, WI-418 fold into §8 rules | — |
| **P1 — Foundations** | SN-028 config consolidation (dual-read window); prompt externalization + `prompts/README.md` rules (§8, existing three templates only) | P0 |
| **P2 — Outcome model** | SN-031: `partial/` state, per-close report docs, intake re-key, keep/discard split at the integrator, adjudicator-override-by-minting, `supersedes` lineage | P0 (ruling), P1 (report schema lives beside process.toml conventions) |
| **P3 — Attest level** | SN-029: numeric level replaces gate-policy across the five consumers; `final-review` toggle; `adjudicate-amendment` template wired into the flip arm | P1 (the key lives in process.toml) |
| **P4 — Loop order** | SN-030: admission priority (dispositions first), red-TC census extension + estimator, component-scoped spine batching dial; SN-032 conflict vetting | P2, P3 |
| **P5 — Routing + close** | SN-026 amendments (ADJUDICATE phase, job-type table); dead-function sweep row; SR/LLR/TC decomposition of SN-028..032 ratified; full-suite + `check.py` at derived gate; downstream resync notes | P1–P4 |

Risk notes for the reviewer: P2 is the largest blast radius (~27 named tests +
the §A3/R3 prose amendments, but a one-file data migration); P3 is wide but
shallow (enum→ordinal at five call sites, each already isolated behind
`read_declared`); P1's dual-read window is what keeps downstream adopters
unbroken. Everything in P4 composes from parts P1–P3 built, which is why it
sits late despite being the headline need.

---

## 11. Addendum (2026-08-08) — reconciliation with the independent second plan

A second, independently authored plan ("Sol's plan") was cross-reviewed against
this one. The two agree on the core architecture (one TOML config; per-event
immutable outcome documents; lane claims + adjudicator override-by-minting;
`partial/` as a terminal state; SN E/F stay unminted; prompt externalization on
the dual-plan pattern; dedicated-branch execution outside the live loop). The
following points from that plan are **adopted here**, superseding this doc
where they conflict:

1. **Detection-gap correction (fact, verified in source).** §3's claim that
   meaning-change detection is "built end-to-end" was too strong:
   `staged_spine_amendments` deliberately ignores any row whose Status moved in
   the same commit (`check_trajectory.py:2884` — "a deliberate call this does
   not second-guess"), so the *sanctioned* amend+flip path never reaches
   intake's adjudication mint. The meaning-vs-clarity adjudicator therefore
   cannot key off the commit-local diff alone; it must compare current
   normative text against the last **accepted anchor** (next item).
2. **Append-only attestation ledger** (artifact id + normative-text digest +
   accepted commit + decision `ratified|clarity|meaning|override`), replacing
   §3's "keep deriving the baseline from git log". This is the same medicine
   §5 prescribes for handbacks — an immutable event record instead of a
   reconstructed proxy — applied to attestation. It also fixes item 1 (ledger
   digest vs current text catches amend+flip) and gives **SN prose** an anchor
   it structurally lacks today (SNs have no Status cell). No per-row hash
   columns, as both plans agree.
3. **Two derived axes instead of one.** The owner's 0–3 scale separates LLRs
   (2) from TCs (3); the current `G0–G3` arithmetic cannot express that (G2
   conflates "LLRs and TCs exist" and also doubles as the Modified pull). So:
   `spine_stage` 0–4 (workflow/admission input, the axis the human boundary
   compares against) derived separately from `verification_gate` G1–G3 (the
   unchanged `check.py` harness contract), with a declared mapping function.
   §3's "compare the level against the existing derived gate" is superseded.
4. **Naming**: `human_ratification_through` (cumulative, "through" this tier)
   instead of "human-attest-level" — `Attest` already names a Verification
   method in the SR vocabulary, and the collision would be permanent.
5. **Queue admission as one trunk-side transaction** (every `→ queued/` move
   through one API; mechanical overlap graph + adjudicator verdict recorded
   with the scope/spine digests it judged; `--strict` rejects a queued spec
   whose verdict is absent or stale). Stronger than §6's warn-first rung, and
   the digest-freshness requirement is what keeps a verdict from rotting.
6. **Adjudicator override moves the byte-identical spec** to the corrected
   terminal folder (folder stays the single truth of final status), rather
   than §5's "never reverse the move" — history is preserved by the outcome
   events, so both goals hold.
7. **argv arrays** for new route declarations instead of shell `CmdTemplate`
   strings, and **template + rendered-prompt hashes recorded per session**
   plus a generated prompt catalog (extends §8).
8. **Hard mixed-config refusal** (preflight fails naming the conflicting keys
   when old and new sources are both live) instead of §2's silent dual-read
   precedence — provided bootstrap/resync runs the legacy converter
   automatically, so a downstream adopter never meets the refusal un-aided.
9. **WI dispositions**: WI-413 *and* WI-416 cancel as superseded (this doc had
   defer / re-decide); WI-390's still-valid spine-close content is absorbed
   into the P0 sitting rather than executed against the contract this program
   replaces.

Points this doc **retains against** the second plan, for the owner to weigh:

- **The M-42 hook constraint is real and unaddressed there.** The git hooks
  parse `privacy-check`/`review-policy` in pure sh so a Python-less box fails
  closed (repo-review 2026-07-21 M-42; `hooks/pre-commit:46`). The
  consolidation must either keep those two keys keyed-greppable
  (`grep -E '^privacy-check *= *true'`) with a cross-parser agreement test, or
  explicitly rule that hooks fail closed on a missing interpreter. "The
  convention, not grep, is why files stayed one-value" is only half the
  history.
- **Adjudicating every `complete/` close** matches the owner's stated intent
  but prices a strong-tier session onto every green close, on top of the
  review rounds that already judged the work. Recommendation: make review
  depth a config dial — always adjudicate `partial`/`cancelled`; `complete`
  at a declared tier/sampling rate — rather than fixing it in the SN text.
- **`stack.ini`'s adopter-owned never-clobber property** must carry over to
  whatever absorbs it; the second plan folds it into `config.toml` without
  stating that resync contract.
