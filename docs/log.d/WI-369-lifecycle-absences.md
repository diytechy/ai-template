## 2026-07-30 — WI-369: LIFECYCLE declared absences may legally exist

The declared-absence honesty test failed on ANY entry that exists — but two
entries' own reasons say the path exists during a lifecycle state
(`docs/work/active/` while claims are open; `docs/work/pause` while
paused). With two claims outstanding, every composed tree the integrator
builds contains the other branch's claim dir, so every bar redded
`SCAFFOLD_OMISSIONS entries now materialized: docs/work/active` and no
branch could merge — a deadlock of exactly the §2.3 parallel-claims model
the queue serves. First hit 2026-07-30 with WI-366 + WI-368 claimed
concurrently; latent until now because prior sessions committed
attended-serial.

- **Deliverable:** the `LIFECYCLE:` reason marker in
  [declared-absences](../declared-absences) (documented in its header) +
  the marker-scoped exemption in tests/test_dogfood_sync.py
  (`_stale_declared_absences`); the two live rows tagged and their marker
  pinned by its own test; a synthetic bite test proves the exemption is the
  marker's in both directions. `check_doc_refs.py` untouched — reasons are
  opaque text consulted only when the path is absent. Spec archived:
  [WI-369](../work/archive/WI-369-lifecycle-absences-red-the-bar-while-claimed.md).
- **Deviations from spec:** none.
- **Suite:** full `pytest -q -n auto` (posix-shell gate satisfied):
  1669 passed / 11 skipped / 1 failed — the sole failure the standing
  WI-357 work-branch conditional (`test_this_repo_is_not_a_work_branch`),
  re-green on trunk; the omissions test passes WITH three claims
  outstanding. `check_trajectory.py --strict` exits 1 on this branch — NOT
  this WI's defect and not masked: R-E flags trunk's WI-368 intake row
  (open, no SpecRef; WI-369's own intake shares the gap on trunk). The
  intakes were filed against the warn-first floor without the direct
  strict run the standing habit demands — the debt is recorded at the
  drain sitting, and the claim rung owes a hardening (filed per
  change-intake).
