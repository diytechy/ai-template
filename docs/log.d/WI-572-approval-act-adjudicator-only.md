## 2026-09-01 — WI-572: the approval act is the adjudicator's, on trunk

**Spec of record:** `../plans/2026-09-01-approval-act-adjudicator-only.md`
(the owner's ruling, 2026-09-01, recorded in
`../log.md` from `2026-09-01-owner-ruling-approval-act.md`). Serialized behind
WI-571 (the copy-scope row); both touch `intake.py` / `baseline_snapshot.py`.

**In one line:** a worker lane may author `Drafted` spine rows and amend cell
text, but the approval act — the `Status` flip into `Approved`/`Founded` and
the `docs/archive/last_approved/` copy that anchors it — is the adjudicator's,
performed on the serial trunk side.

### The baseline this row is measured against

Every commit that moved an `"Approved"` string in a spine registry before the
ruling, classified by where it happened:

- **1 worker-lane flip** — `580df781` (WI-508 slice 6), whose next review round
  returned CHANGES-REQUESTED against exactly those flips.
- **4 lanes minted rows born `Approved`**, skipping the brief entirely —
  `8848f6fb` (WI-483), `ad2222df` (WI-500), `69e4a854` (WI-501), `0cfb2e6f`
  (WI-507).
- The rest were trunk sittings or the pre-ladder rename.

fig: 17 commits, classified by subject; `git log --format='%h|%s'
-S'"Approved"' fd86e47f -- docs/requirements/system-requirements.toml
docs/requirements/low-level-requirements.toml docs/test/test-cases.toml
docs/requirements/system-requirements.csv
docs/requirements/low-level-requirements.csv docs/test/test-cases.csv`
at `fd86e47f`.

### Deliverables

(in progress — this fragment is kept current as the session runs)

Deferred open items: none — the ruling this row executes is already recorded;
nothing here is owed back to the owner.
