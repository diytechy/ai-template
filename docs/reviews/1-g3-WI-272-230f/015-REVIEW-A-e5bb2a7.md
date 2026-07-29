# REVIEW-A — e5bb2a7

### REVIEW-A — G3 — Round 1 — 2026-07-23
Verdict: APPROVE

Scope: the docs-only disposition correction `e5bb2a7` (+ telemetry `bbd8a6e`),
which consumes the two MAJOR findings of `013-REVIEW-A-7ac3043.md` by making the
U5 closure order explicit, re-labelling the U5 successor as pending (not
durable/schedulable), and recording WI-272 as BLOCKED on an integration-owned
action (`Blocked-WI: WI-272` / `BlockRef:`).

Independently verified against the real tree and harness (main-repo `.venv`,
Python 3.11.9):
- Docs-only: `git show --stat e5bb2a7 bbd8a6e` touches only the two review `.md`
  files + one telemetry log — no code, registry cell, generated artifact, root
  status, or source palette changed (matches the record's closing claim).
- U5 is genuinely pre-existing, not introduced by WI-272: `STATUS_FILL["done"]`,
  `TIER_FILL["tc"]`, and `OKF_TYPE_FILL["Test Case"]` all map to `#047857`
  (gen_trajectory.py:506/220/2652); `git blame` dates the tc/Test-Case side to
  2026-07-14; WI-272's build diff (`a6abfb8`) added only `deferred #6b21a8` /
  `blocked #b91c1c` to `STATUS_FILL` (both unique) and never touched
  `TIER_FILL`/`OKF_TYPE_FILL`/`PHASE_ACCENTS`.
- No U5 successor row exists in `work-items.csv` (grep); the only `~WI-272` child
  is WI-273 — so "pending, no registry-authoritative successor" holds.
- `check_trajectory --root . --strict` reports `perceptual-stale
  SR-052;SR-053;SR-054` (last judged by top-level `112-CRITIQUE.md`);
  `_latest_critique_file` globs only top-level `docs/reviews/*-CRITIQUE.md`, so
  the train-scoped `009-CRITIQUE` is invisible and the gate is red by
  construction — the record's claim is accurate. Remaining reds are WI-275 root
  state (status.md forward-only + R-F SpecRef), integration-owned, not WI-272.
- `check_docs.py --root . --stale` → exit 0, 0 broken links (record's PASS).
- `pytest -q -n auto -m smoke` → **1 failed, 1086 passed, 3 skipped** (332s); the
  sole failure is `test_forward_only_unit_over_the_real_meta_repo`, and a direct
  `status_forward_only_findings(ROOT, wis)` call confirms its one item is WI-275's
  `done` id in status.md — unrelated to WI-272 (which appears in status.md only as
  an open build-order item). WI-272's own five fidelity tests pass (5/5).

The block is legitimate, not a dodge of in-scope work: WI-272 cites SR-053
(whole-dashboard `Verification=Critique`), the independent 009 critique returned
CHANGES-REQUESTED on U5, the critic routed U5 to `@owner`, and 013-REVIEW-A itself
required the successor's palette fix be integrated before the re-critique. A build
worker cannot self-adjudicate a Critique gate, file a registry row, or regenerate
the freshness-gated dashboard — the named next actions are genuinely
integration-owned. Both 013 MAJORs are faithfully consumed.

Findings (both MINOR, for-clarity, pre-existing, `@owner` — neither blocks):

- [MINOR] docs/reviews/1-g3-WI-272-230f/010-BUILD-DISPOSITION-c67e85b.md:21 -> for clarity: the disposition rests WI-272's closure basis on SR-Refs "SR-038;SR-053", but SR-038 is a superseded row (Title "Superseded: Offline project-state view"; SupersededBy SR-070;SR-071;SR-072; its own Requirement directs that active requirements "shall cite the replacement rows"), so WI-272 citing SR-038 is a stale reference the prose restates unflagged (pre-existing in the registry row a train worker cannot edit; SR-053 alone still carries the block) -> at integration, repoint WI-272's SR-Refs off superseded SR-038 to its live replacements (or drop it) so the closure basis names only live requirements -> @owner
- [MINOR] docs/reviews/1-g3-WI-272-230f/010-BUILD-DISPOSITION-c67e85b.md:134 -> for clarity: the disposition frames U5 as a net-new owner palette WI (the M-2->WI-272 pattern) yet omits that the U5 colour-vocabulary anchor is a recurring, previously-dispositioned defect — WI-144 shipped "the U5 palette de-collision (OI-12)" and WI-247 reworked a U5 regression (PHASE_ACCENTS byte-identical to STATUS_FILL/TIER_FILL) — so the successor is arguably a re-collision fix, not a first-time redesign -> cite the WI-144/WI-247 precedent in the successor filing so @owner scopes it as a regression, not fresh design -> @owner
VERDICT: APPROVE findings=2
