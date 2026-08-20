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
- **What the sitting still has to RULE.** The one below, **plus the three
  pending briefs projected below** — the rest is ruled, countersign-only
  ([log.md](log.md)). Note the item below is itself an open ruling that carries
  no `OI` row, which is `OI-41`'s subject.
  1. **The mis-seeded `B`/`REL` watermarks.** `B-08`/`REL-004` were allocated
     and cut, the seeding probe could not see them, and raising the marks by
     hand is REFUSED by `trace.py`'s integrity rule now that both spaces carry a
     committed mark. **The owner rules the MECHANISM for correcting a
     mis-computed seed.** Interim protection: a SPENT IDS block in
     `external.toml`'s header.
- **What the sitting has to DO, beyond that one.** The **attestation**: the
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
  **Countersign-only, added 2026-08-18k:** fifteen SN `acceptance` cells reworded
  from instrument voice to condition voice under the owner's artifact-voice
  directive — a wording sweep, no `status` cell moved, per-row before/after in
  [log.d/2026-08-18-sn-artifact-voice.md](log.d/2026-08-18-sn-artifact-voice.md).
  **Also countersign-only:** `SN-006` relaxed on the owner's ruling (the
  unattended layer moves forward as far as it can and surfaces only when it
  cannot proceed; the human-held override stays, the absolute goes) — a
  provisional amendment, before/after in
  [log.d/2026-08-18-owner-rulings.md](log.d/2026-08-18-owner-rulings.md).
- **The `wi455-architecture-retirement` lane owns what the sitting does not:**
  the crossing-ownership re-key onto each named owner, the five
  `external:`-marked IF rows with no tie-back, B-04's half realization, the D-3
  `direction`/`this_project` shed and the counterpart→consumers transform (v2
  ruled the direction, the lane executes), and the one live derivability fire
  (`IF-128`). Its `Contract`-cell half now also carries **the 49 held provenance
  citations** (`OI-36` ruled 2026-08-19) — the hold and its `WI-469` blocker are
  recorded in [provenance-allow](provenance-allow)'s header, which is the surface
  to re-open if that chain outlives the lane.
- **Owed by a ruling, not yet built:** `WI-472` — mint the SR/LLR/TC for the
  `CodeSymbol` anchor obligation and re-point `IF-117` (`OI-39` ruled (a) MINT,
  2026-08-19). The binding constraint is **language-agnosticism**: state the
  obligation so an adopter whose implementation units are not Python files can
  satisfy it, never `.py` and never `check_doc_refs`. No back-link obligation is
  minted there — that direction is `OI-42`'s.
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
- **Spine:** **SN=27 SR=72 LLR=161 TC=157** (74 drafts) · 125 seams · 4 components.
- **Open items** _(pending rows of [requirements/open-items.toml](requirements/open-items.toml); each item's blast radius, options and recommendation render in [open-items.html](open-items.html), the generated owner surface):_
  - **OI-32** — RE-POINTED 2026-08-18 by the owner's direction (NOT a ruling): they are considering a GENERATED approach - one living source of what a component does, derived as a list of the SRs and LLRs tied to that component rather than a hand-maintained document. Rule between the hand-maintained home, the generated view, and retirement
  - **OI-41** — rule what mechanism reinforces that EVERY deferred-to-the-owner decision reaches open-items.toml - the owner's own question, raised because the ten briefs of 2026-08-18 only appeared when they asked; today the generated view can report itself up to date while carrying zero pending rows and ten genuine decisions sit on other surfaces; recommendation AMENDED 2026-08-19 to (e) - three arms that are each a FIELD or a COUNT rather than a phrase match (the allow-file grammar gains a required OI-###; the session log declares what it deferred; a vacuity check names the contradicting entry), because the owner's objection is that a phrase matcher grabs items that are not applicable and a matcher's precision cannot be bounded before it ships
  - **OI-42** — rule the CODE-to-REGISTRY direction that OI-39 is NOT about - two SHIPPED documents require Implements: SR-/LLR- on every public symbol, the kit's own scripts carry it on 2 of 781, nothing checks it, and gen_arch_map.implements() fills the map's back-link column 97% from undeclared prose (SR-9, SR-10, LLR-1 harvested out of sorting examples); recommendation is (b) SOFTEN THE GUIDE AND TIGHTEN THE HARVESTER, with (e)'s reverse-coverage measurement as the second arm in place of (a) - (e) is the owner's 2026-08-19 proposal, it is the only option that measures adherence rather than policing the links that exist, and unlike (a) it needs no history-marker convention first, but it must ship at a report-only default because measured coverage is 1 of 161 LLRs
  - **OI-43** — rule the assurance posture for interface contract tests - PROCESS.md and README state every interface is backed by an SR and a contract/fixture test, while PROCESS_OPTIONS.md and check_trajectory.py DELIBERATELY keep IF-to-TC coverage warn-only at every bar and the measured gap is 115 of 125 seams (verified 2026-08-19); the recommendation is (a) PROMOTE AT DevStg-Tests WITH A MIGRATION ALLOWLIST, sequenced behind the wi455/WI-469 contract re-authoring so tests pin re-authored contracts, with (b) the prose soften executed by WI-477 only if the ruling refuses promotion
  - **OI-44** — rule the publication/identity posture before wider distribution - docs/process.toml sets privacy_check = false (the secrets floor is separately ON and clean), and git history carries author/committer identities on personal email-provider domains (verified 2026-08-19 by domain census only; identities deliberately not copied here); the recommendation is (a)/(c) - record acceptance or defer-to-publication-event - because (b)'s history rewrite is uniquely expensive in THIS repo, whose working method cites commit SHAs pervasively (fig: rev= markers, RESYNC landing SHAs, log entries), and a fresh-history EXPORT is the cheap honest alternative if the identities must not publish
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-448** `P3` — OI-16 execution (inversion confirmed by the owner 2026-08-13): the common-module program
  - **WI-455** `P3` — The docs/architecture.md RETIREMENT program (owner-ruled 2026-08-13u, sitting-2 decision…
  - **WI-469** `P3` — Consumes rows that name the MEDIUM, not whom the medium serves
  - **WI-473** `P3` — Gate scheduling loses every established product check when one draft row lands: design an…
  - **WI-474** `P3` — Declare or re-partition the hats -> spine_carrier seam: the one live strict-architecture…
  - **WI-464** `P2` — Re-tier v2
  - **WI-472** `P2` — Mint the SR that states the CodeSymbol-anchor obligation, plus its LLR and TC, and re-poi…
  - **WI-482** `P2` — Repair the three verified-stale LLR CodeSymbol anchors (LLR-087, LLR-088, LLR-112)
  - **WI-483** `P2` — Successor decomposition program: break the seven-module import cycle behind typed read mo…
  - **WI-390** — PROGRAM CLOSE for concurrency-v2 (docs/concurrency-v2.md §A9 deletion ledger). NOT a swee…
  - **WI-452** `P3` — Resurface LLR-165's carrier converter as the downstream-resync helper it now is (owner-ru…
  - **WI-465** `P3` — Pin core.autocrlf in every git-initing test fixture (or one shared builder): the CRLF-con…
  - _(+10 more ready — see the dashboard)_
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
