# Meta-Repo Status — Blackboard

The **working surface** for developing the kit itself — the same `status.md`
pattern the kit scaffolds downstream, self-applied. This file is
**forward-only**: only what must happen **next** lives here. Backward-looking
homes: [log.md](log.md) (sessions, verdicts, **Decisions**),
[open-items.html](open-items.html) (the generated **Open items** owner surface),
[docs/work/](work/) (the WI registry — status = directory; dashboard
[`PROJECT_STATE.html`](../PROJECT_STATE.html)), and
[archive/](archive/README.md) (design history, with per-file dispositions).

- **THE TARGET — ONE SITTING, and it is the owner's.** Everything mechanizable
  ahead of it is executed. The spine layer is **settled**; every act on it is
  **provisional and overturnable**; **nothing is signed, nothing is seeded**,
  and `docs/archive/last_approved/` deliberately does not exist yet. **Run the
  sitting from two documents, in this order:**
  [plans/2026-08-13-sitting-3-spine-verification.md](plans/2026-08-13-sitting-3-spine-verification.md)
  — its 2026-08-16 banner, then **§0.4, the desk** (§0.3 ledger, §2.1 window,
  §3 status-vocabulary sequence, §4 close mechanics) — and
  [plans/2026-08-15-review-package.md](plans/2026-08-15-review-package.md) §5,
  the procedure in order: read the regenerated brief
  ([ratify/2026-08-13-wi444.md](ratify/2026-08-13-wi444.md)) **plus the ten
  ex-`Planned` rows no brief lists**, rule the open calls, **sign**, **seed the
  snapshot in the same reviewed commit**, then step 7 arms.
- **What the sitting still has to RULE — exactly two items.** Everything else
  the list carried is ruled and countersign-only (narrative in [log.md](log.md)).
  1. **The mis-seeded `B`/`REL` watermarks.** `B-08`/`REL-004` were allocated
     and cut, the seeding probe could not see them, and raising the marks by
     hand is REFUSED by `trace.py`'s integrity rule now that both spaces carry a
     committed mark. **The owner rules the MECHANISM for correcting a
     mis-computed seed.** Interim protection: a SPENT IDS block in
     `external.toml`'s header.
  2. **`SR-040`'s resume-surface tripwire.** Investigated; no live carrier
     found, and the nearest look-alike was REFUSED as a substitute.
- **What the sitting has to DO, beyond those two.** The **attestation**: the
  re-attest window, the **LLR/TC draft ratifications** (same sequence), and the
  remainder of the status-vocabulary sequence — review-package §5 step 7: retire
  the transitional `Modified` so the enum lands at `{Drafted, Approved,
  Founded}` (drift = snapshot comparison), turn `intake`'s `!= "Modified"` guard
  into a refusal, arm the UNANCHORED rule as an ERROR. Registry-status
  unification §5B (D-9 steps 7–8) is POST-sign AND POST-seed — deliberately NOT
  done. The **amendment window closes at that sitting, not before**; §0.3's
  ledger is 9-of-9 RULED and §0.4's WORK OWED block is empty, so no pre-work is
  owed. Known-open, unrelated: the `trajectory` gating red, and the brief's
  freshness check (it re-reddens on every spine amendment).
- **The `wi455-architecture-retirement` lane owns what the sitting does not:**
  the crossing-ownership re-key onto each named owner, the five
  `external:`-marked IF rows with no tie-back, B-04's half realization, the D-3
  `direction`/`this_project` shed and the counterpart→consumers transform (v2
  ruled the direction, the lane executes), the one live derivability fire
  (`IF-128`), and the runtime flows' move to `docs/runtime-flows.md` — which
  re-lands `check_flows`'s obligation one last time.
- **Standing owner acts the loop will not make:** merge-to-main + push for
  `dualplan-routing-fix`, `guardrails-fable-method`, `ConcurrencyTrainRewrite`
  and this branch (`push = "human"`). Known residue, kept deliberately: the
  `wi416-parked-handback-contract` branch holds a 271-line pre-ruling draft
  that exists nowhere else (its rows are disposed; the handback ruling
  superseded it) — delete only after deciding the draft is not wanted.
- **STARTING COLD? Read in this order:** this block →
  [plans/2026-08-15-review-package.md](plans/2026-08-15-review-package.md) →
  sitting-3 §0.4 → [log.md](log.md)'s `2026-08-15*`/`2026-08-16*` Decisions.
  The standing constraint under all of it: **the depth-0 frame is LOCKED** —
  **4 entities · 4 crossings · 3 relationships**, ids of the cut rows spent and
  watermark-held; the repository is the system, the template is the deliverable.
  What the sitting owes a look at in
  [plans/2026-08-15-interface-rework-plan.md](plans/2026-08-15-interface-rework-plan.md):
  the 21 judgement owner picks, the `carried_by` prototype on `IF-102` and its
  provisional depth bound of 2, and the `IF-097`/`IF-080` calls.
- **Unfiled follow-ups** (no ids yet, so listed as topics): the stage-ladder
  program's deferred codex review round; the SN-036 per-decomposition coverage
  record (re-derive it — the basis line now reads `uncovered=0`); the two
  findings in the archived
  [2026-08-01 handoff §6](archive/history/handoff-2026-08-01.md); and the three
  unruled residues + §8 dead-symbol table in
  [spine-restructure-2026-08-08.md](spine-restructure-2026-08-08.md) (its §7
  items 2/4/5 need a destination before that file can archive).
- **Conventions:** spec-of-record [specs/README.md](specs/README.md) · rubrics
  [rubrics/README.md](rubrics/README.md) · partial-close reports
  [handbacks/](handbacks/README.md).

## Current State

<!-- BEGIN GENERATED STATUS -->
_Derived facts — regenerated by `python project-trajectory/scripts/gen_trajectory.py --status`; do not hand-edit (the forward-only intent below is hand-authored)._

- **In stage:** **DevStg-Boundary** (stage 1 of 8, system boundary interfaces in work) · **next to clear: DevStg-Reqs** (per-phase `1=DevStg-Below;3=DevStg-Tests;4=DevStg-Below;5=DevStg-Below`, derived current **phase=5**) — one vocabulary, and the VERB says which reading: a repo is IN a stage and CLEARS a stage. [`derive_gate.py`](../project-trajectory/scripts/derive_gate.py) derives both, cached to [`docs/gate`](gate).
- **Spine:** **SN=27 SR=72 LLR=161 TC=157** (74 drafts) · 123 seams · 4 components.
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-448** `P3` — OI-16 execution (inversion confirmed by the owner 2026-08-13): the common-module program
  - **WI-455** `P3` — The docs/architecture.md RETIREMENT program (owner-ruled 2026-08-13u, sitting-2 decision…
  - **WI-469** `P3` — Consumes rows that name the MEDIUM, not whom the medium serves
  - **WI-464** `P2` — Re-tier v2
  - **WI-390** — PROGRAM CLOSE for concurrency-v2 (docs/concurrency-v2.md §A9 deletion ledger). NOT a swee…
  - **WI-452** `P3` — Resurface LLR-165's carrier converter as the downstream-resync helper it now is (owner-ru…
  - **WI-465** `P3` — Pin core.autocrlf in every git-initing test fixture (or one shared builder): the CRLF-con…
  - **WI-466** `P3` — trace.py's summary line hides the whole verified-mechanized/demonstrated/attested triple…
  - **WI-470** `P3` — SR-052 coverage: bring gen_open_items.py inside the mechanized A3 no-colour-alone closure…
  - **WI-467** `P2` — Blind re-derivation validation exercise (owner-approved 2026-08-16): two independent agen…
<!-- END GENERATED STATUS -->

- **Bar (per commit):** `python -m pytest -q -n auto -m smoke` +
  `python project-trajectory/scripts/check_docs.py --root . --ignore docs/test/report.md --ignore "docs/work/*" --stale`,
  both green. At slice/phase close: the full unfiltered suite (`pytest -q -n
  auto`) and `check.py` at the derived gate. Also run
  `check_trajectory.py --strict` directly, unfiltered, before claiming
  anything done — the DEFAULTED pre-commit floor stays warn-first by design,
  so the floor's output is never the strict bar.
- **Standing rules with no other home (do not delete without relocating):**
  - **An id named in this file's hand-authored prose CANNOT BE CLAIMED**
    (`integrate._status_prose_refusal` refuses it at claim time; generated
    blocks are exempt). Point at [work/queued/](work/queued/) and let the
    generated frontier name ids.
  - **Never revert a real fix, or sanction a check, to green a step** —
    editing a declared list (a coverage floor, an orphan glob, a ratchet
    baseline) to clear a finding IS accepting what it measures.
  - **Signed claims + one-machine humility:** the recurring review-era defect
    was signed CLAIMS that pass every test ("Signed measurements",
    process-options.md), and **one machine is one data point for OS-behavior
    claims** — state the condition, not the universal.
  - **Measure on a tree whose line endings match the index** — before
    trusting any byte count or hash, `git ls-files --eol | grep 'w/crlf'`
    (only `*.ps1`/`*.cmd`/`*.bat` should appear).
- **Claiming runs through the integrator** (`integrate.py claim`; merges are
  its serial fail-closed queue; a pause is a tracked `docs/work/pause`).
  Probe providers before planning a critique dispatch, and route by PROVIDER,
  not gateway.
- **External follow-up** *(not this repo's work)*: guardrails content
  enrichment lives in `TheColliny/FableClaudeMDForOpus` (vendored downstream).
- **Process (kit source):** [PROCESS.md](../project-trajectory/PROCESS.md) ·
  [PROCESS_OPTIONS.md](../project-trajectory/PROCESS_OPTIONS.md) · working
  rules [CLAUDE.md](../CLAUDE.md) + the `session-protocol` skill · still-owed
  lock items [repo-lock.md](repo-lock.md) (its §1 now defers to the generated
  surfaces).

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.11+.
- **Non-goals (self-application boundary):** no product **launch** — the
  kit's "product" is `project-trajectory/` + `tests/`, a meta-repo has no
  product to launch, and an actions-menu launcher is in scope; no scaffolded
  `docs/process.md` (the masters live in `project-trajectory/`).
