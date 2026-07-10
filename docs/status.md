# Meta-Repo Status — Blackboard

The **working surface** for developing the kit itself — the same `status.md`
pattern the kit scaffolds downstream, self-applied. Only what happens **next**
lives here; the spec/backlog and per-thread design history live in
[IMPROVEMENT_PLAN.md](../IMPROVEMENT_PLAN.md) (its thread `Status:` blocks and
WI-1.x log). The **gate-walk** record for the kit's self-adoption (Thread 47 —
sign-offs, verdicts) is [log.md](log.md).

- **Process (kit source):** [PROCESS.md](../project-trajectory/PROCESS.md) ·
  [PROCESS_OPTIONS.md](../project-trajectory/PROCESS_OPTIONS.md) — this repo
  has no scaffolded `docs/process.md`; the masters are the reference.
- **Working rules:** [CLAUDE.md](../CLAUDE.md) + the `session-protocol` skill.

---

## Current State

- **Bar:** `python -m pytest -q` and
  `python project-trajectory/scripts/check_docs.py --root . --stale` green
  before every commit — this repo's standing gate. **The kit's own
  `SN→SR→LLR→TC` spine is self-adopted** (Thread 47): `docs/gate` is at **G3**
  — `check.py --gate G3` (12 steps; the `okf` freshness step joined 2026-07-10)
  is the full bar and CI's `gate` job runs it, on **real data** (the meta-repo
  dogfoods its own trajectory + OKF layers). Design history: the plan threads;
  gate-walk record: [log.md](log.md).
- **Plan state:** meta-repo at **G3**, spine **SN=22 SR=42 LLR=39 TC=42, 0
  orphans**, 42/42 SRs mechanized. **The 2026-07-10 grind landed the entire
  queued backlog** (owner-authorized, review deferred): WI-1.47 `Evidence`
  column (Thread 51) · WI-1.48 `check_dupes` (Thread 53) · WI-1.49 the
  dynamic layer (`AGENT_CMD_MAP` + `docs/review-policy` + size guard) ·
  WI-1.50 `check_doc_refs` (Thread 49) · WI-1.51 OKF export (Thread 48) ·
  WI-1.52 root `PROJECT_STATE.html` (WI-039). Details: the WI-1.x log in
  [IMPROVEMENT_PLAN.md](../IMPROVEMENT_PLAN.md); spine change:
  [log.md](log.md) 2026-07-10. Dogfood registry: **42 WIs, 41 done + WI-033
  active**; the dashboard is now the root
  [`PROJECT_STATE.html`](../PROJECT_STATE.html).
- **Open items:**
  - **Needs <human> (the run is paused on these):**
    1. **G3 re-attestation over the 2026-07-10 spine change** — SR-039…042
       added, SR-038/LLR-035/TC-038 extended, and the B1 SN-Refs correction
       ([log.md](log.md); *mandatory*: a Verified SR's text changed). The three
       adversarial reviews are **fully triaged** — all 20 findings fixed
       (WI-1.53), so re-attestation now covers a reviewed, corrected spine.
    2. **Push decision** — `MultiRepoSupport` is local-only (~40 commits).
    3. **F3 data-pass** on the 44-WI DAG edges (demote narrative edges to
       `~`) — owner's mapping call, unchanged.
  - **In flight:** _(none)_ — the queue is empty. The three
    [`REVIEW_GRIND_*.md`](../REVIEW_GRIND_A.md) reports (7 method/risk +
    4 process/trace + 9 full-repo; **no HIGH**) are all RESOLVED in **WI-1.53**
    — spine SN-Refs (B1) + the OKF count (B2), text-boundary/encoding
    hardening, per-script correctness, harness shadow-guard + `KIT_SCRIPTS_DIR`
    in every hook + parser-drift reconcile, and the docs/nits.
  - **Recently landed:** **OKF Layer B2** (process docs as `Process Guide`
    concepts — WI-1.54, 2026-07-10; extended SR-042 + LLR-039, rides the
    re-attestation).
  - **Deferred (backlog):** **WI-1.27** coordinator stash/rollback
    (owner-deferred 2026-07-05); OKF **Layer B1** (intrusive doc-frontmatter,
    behind a future flag); the **Q1 rider ruling** (a warn-first `--untraced`
    tier — recommendation recorded in WI-1.50's entry); the committed-composites
    freshness design (deferred with reasoning, WI-1.50).
- **Next action:** **owner sitting** — read the three `REVIEW_GRIND_*.md`
  reports, triage their findings (file/fix/dismiss), re-attest G3 per
  [log.md](log.md), and rule on push. After that the frontier is genuinely
  open: G-Release walk, the F3 edge data-pass, or new scope (which needs a
  plan/WI entry first).

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.8+.
- **Non-goals (self-application boundary):** no `run.*` product launchers (the
  kit's "product" is `project-trajectory/` + `tests/` — nothing to double-click
  launch); no scaffolded `docs/process.md` (the masters live in
  `project-trajectory/`). *(The SN-spine non-goal was **lifted by Thread 47** —
  the kit now traces itself; its registries live in `docs/requirements/` +
  `docs/test/`, distinct from the shipped `project-trajectory/registries/`
  templates.)*
