### REVIEW-A — WI-578 — Round 003 — 2026-09-03 — supervisor-drawn (independent Opus, hostile brief)

Rework round over `f51281cc`, lane worktree `wi-578-adjudicate-llr-158-llr-203`.
Scope: confirm round 002's two findings are actually fixed, and hunt for what
the fix broke. A rework of a drafted successor admits three failure classes —
a fix that does not parse, a fix that leaves a dangling reference to the thing
it removed, and a fix that removes the defect's SYMPTOM while leaving the row
declared for the actor that could not perform it. Hunted in that order.

## What I verified

**Diff since `c3ae6ba0` — exactly the two expected files, nothing else.**

```
$ git diff c3ae6ba0..HEAD --stat
 .../002-REVIEW-A-c3ae6ba-supervisor.md             | 196 +++++++++++++++++++++
 .../complete/WI-578-adjudicate-llr-158-llr-203.md  |  20 ++-
 2 files changed, 209 insertions(+), 7 deletions(-)

$ git diff c3ae6ba0..HEAD --name-only | grep -E 'docs/requirements/|docs/test/|last_approved|docs/archive'
  (none)
```

No registry, no `docs/archive/last_approved/`, no code file. Round 002's file
was committed at 196 lines, matching what I wrote. The absolute constraint
holds at this HEAD as it did at `c3ae6ba0`. Working tree clean.

**The draft still parses, and it is still exactly one draft.**

```
$ intake.parse_dispositions(text, "docs/work/complete/WI-578-...md")
n_drafts: 1   refusal: None
keys: ['bar','buildtier','kind','priority','scope','specref','title','workstream']
kind: spine   bar: DevStg-Impl   buildtier: medium   priority: 2
specref: docs/requirements/low-level-requirements.toml
valid safety class? True
```

No refusal string, no unknown key, `bar` still valid, `specref` still the kit's
own mint idiom. The rework touched prose inside the scope body and one TOML
string; it did not disturb the fence or the frontmatter.

**Finding 2 (title) — FIXED, and measured, not eyeballed.**

```
title: The snapshot's scoped writer and unscoped refusal disagree on registry scope
TITLE LEN: 76
```

76 characters, comfortably under `check_trajectory._TITLE_CONCISE_MAX` (120),
so the concise-title WARN will not fire when the row is minted and open. The
shortened title keeps the actual claim — a scoped writer and an unscoped
refusal disagreeing about registry scope — rather than degrading to a generic
label, and the full statement survives verbatim in the scope body's
"THE CONTRADICTION" paragraph. Nothing was lost by the trim.

**Finding 1 (misrouted approval act) — FIXED, at the right level.** The
replacement paragraph does not merely delete the offending step; it states the
CONSTRAINT and re-homes the act:

> THE ANCHOR IS NOT THIS ROW'S STEP (REVIEW-A round 002, finding 1). A `spine`
> row is a WORKER LANE, and `acceptance_record.lane_approval_refusal` refuses a
> lane that writes `SNAPSHOT_DIR` — by construction, at merge. So this row's
> whole scope is the ruling on (a)/(b), the `refresh_refusal` change it
> implies, and the test. The re-anchor ... is the SUCCESSOR CONDITION: once
> this row lands and the act is takeable, the trunk-side
> amendment-adjudication rung — the same rung that minted WI-578 — takes it.

That is the correct owner: the rung that minted WI-578 is the amendment
adjudication, which `integrate._adjudication_lane` classifies as the permitted
actor, and `merge_approval_refusal` routes to `adjudication_approval_refusal`
rather than the lane refusal. The blessability evidence (seven drifted Approved
rows, `LLR-206` excluded as a first approval) is preserved rather than dropped,
so the successor rung inherits the reading instead of re-deriving it.

**I re-read the WHOLE scope body for a dangling reference to the removed step,
and found none.** A token sweep of the parsed `scope` string:

```
SNAPSHOT_DIR            1     (only in the sentence saying the lane must NOT write it)
last_approved           0
snapshot --approves     0     (the CLI form appears only as the reproducible OBSERVABLE)
re-anchor               1     (only as the SUCCESSOR CONDITION)
Status                  1     (descriptive, quoting `_authorised_registries`)
flip                    3     (all "the flip-back arm does not apply" / descriptive)
```

No sentence instructs this row to flip a `Status`, write the snapshot, or take
any approval act. The "IN SCOPE" section's (a)/(b) ruling and its acceptance
shape are untouched and remain coherent with the narrowed scope — they were
always the mechanism half. The "OUT OF SCOPE" paragraph still correctly
excludes the three rows' text and the SR/TC drift, and it does not contradict
the new paragraph (one is about registry CELLS, the other about the snapshot
ACT).

**The (a) acceptance test cannot re-introduce the defect through the back
door.** I checked this specifically, because "a test that a scoped, authorised,
single-registry approval COMPLETES" is a test that CALLS `copy_live`, which
writes `SNAPSHOT_DIR` — if it ran against the repo root it would put the
snapshot into the lane's own delta and re-trip `lane_approval_refusal`. It
will not: every existing caller in the suite takes a scaffold root, never the
repo (`tests/test_baseline_snapshot.py:61,69,153,188`, `SNAP.copy_live(root,
seed=True)` on a `tmp_path` fixture; `tests/test_adjudicate_brief.py:642,678,
768,862` likewise on `repo`). The row's acceptance therefore sits inside the
convention that already keeps the act out of the delta.

**Harness — unchanged, nothing regressed.**

```
$ .venv/bin/python project-trajectory/scripts/trace.py --strict-integrity | tail -1
Traceability: SN=27 SR=76 LLR=188 TC=187 orphans=2 integrity=0 verified-mechanized=72 verified-demonstrated=3 verified-attested=0 drafts=9 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=162 interface-findings=0 provenance-findings=1 paraphrase-advisories=3. Report -> docs/test/report.md

$ .venv/bin/python project-trajectory/scripts/check_trajectory.py --strict 2>&1 | grep ERROR
check_trajectory: ERROR - cross-component import scripts/schedule (CMP-008) -> scripts/trace (CMP-006) has no declared IF-### seam ...
```

`integrity=0`, byte-identical counters to round 002, and the same single
INHERITED component-seam ERROR — still not caused here, since the diff since
`c3ae6ba0` contains no Python.

**One thing the rework DID unsettle, and I am flagging it because it was my own
round-002 reasoning that it invalidated.** In round 002 I examined
`safety_class = "spine"` and blessed it — but on the ground that
`refresh_ledger` is a whole-tree comparison whose outcome shifts if a
concurrent lane amends a registry mid-ACT, so the row needed
`CONCURRENCY_EXCLUSIVE`. The rework removed the act. What remains is a ruling,
a `refresh_refusal` change and a test — work that authors no spine cell text,
takes no approval act, and on the literal "spine authoring under approval"
reading would be `ordinary`. The declaration is still VALID and still errs in
the conservative direction (`schedule._KIND_CONCURRENCY["spine"]` = exclusive,
`_KIND_RANK` = 0; `ordinary` would be parallel and later), and the kit shares
that bias — `dispatch._branch_exclusive` "fails toward exclusivity, never
toward sharing the station", and the class carries no human-approval hold
(`human_holds` reads the RUNG, not the safety class). So this is not unsafe and
does not block. But the row no longer says why it is `spine`, which is finding
1 below.

## Findings

- [MINOR, for clarity] docs/work/complete/WI-578-adjudicate-llr-158-llr-203.md:38 -> `safety_class = "spine"` now has no stated justification in the row: the rework correctly removed the approval act, which was the only part of the scope that needed a spine-class lane, and what remains (a ruling, a `refresh_refusal` edit, a test) authors no spine cell text and would read as `ordinary` on the literal definition — the declaration is valid and conservative (exclusive + rank 0, the direction `dispatch._branch_exclusive` itself fails toward), so nothing is unsafe, but the next reader meets a class the row's own text now argues against when it says "A `spine` row is a WORKER LANE" purely to explain a constraint -> add one clause to the scope body naming the reason to KEEP it — that the row changes `refresh_refusal`, the gate every approval act consults, so it runs alone and first — or change the declaration to `ordinary`; either is fine, leaving it unexplained is what is not -> @owner

Both round-002 findings are properly fixed: the title is measured at 76 chars,
and the approval act is re-homed to the actor that may take it with the reason
cited in the row. The rework introduced no dangling reference, no parse
regression and no harness change. The one finding above is a wording gap, not a
defect, and does not withhold approval.

VERDICT: APPROVE findings=1
