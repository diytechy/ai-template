## 2026-08-01 — WI-395: the `blocked` bullet stops promising a self-release

**Summary.** The R3 wording fix, built exactly as the 2026-08-01 amendment
narrowed it: the two byte-identical exemplar paragraphs
(`docs/work/queued/WI-000-example.md` + `project-trajectory/work/WI-000.template.md`,
the `blocked` bullet) no longer say "readiness is the scheduler's to derive" —
the sentence WI-391's park measured as a false promise. The bullet now states
the mechanism as built (the scheduler reads the `blockref` key's **presence**,
never the blocker's state) and names the actual release paths: the
dispatcher's handback-intake arm (mints the disposition row when a handback
merge lands — loop machinery, never another work item; R3, log Decisions
2026-08-01), or a reviewed edit deleting the `blockref`.

- **Deliverables:** the paired bullet rewrite, both copies edited together.
- **Deviations from spec:** none. Option A (the cross-registry subscription)
  not built, per the ruling; no human sweep named as mechanism, per the
  amendment.
- **Verification:** `python -m pytest -q tests/test_dogfood_sync.py` — 25
  passed in 0.14s (the pair-sync test that reds when the copies diverge).
