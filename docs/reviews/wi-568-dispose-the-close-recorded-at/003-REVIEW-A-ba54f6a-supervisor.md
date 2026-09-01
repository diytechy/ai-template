### REVIEW-A — WI-568 — Round 003 — 2026-09-01 — supervisor-drawn verification (independent Opus)

Tree: `/Users/diytechy/Documents/ai-template-drive/wi-568-dispose-the-close-recorded-at`
@ `ba54f6a5` (round-002 file committed at `49fcde88`). Python
`/Users/diytechy/Documents/ai-template/.venv/bin/python`. Every round-002
finding re-driven against the tree, plus a hostile pass over the corrections
themselves.

## What I verified

**BLOCKER 1 (misplaced block) — FIXED, mechanically.** `## Dispositions` now sits
in the spec after `## Context`; the verdict carries only a pointer.

```
intake.parse_dispositions(<WI-568 spec>) -> refusal: None ; n drafts: 1
keys: ['buildtier','kind','open_item','planmode','priority','supersedes','title','workstream']
title len: 111 ; kind: spine ; buildtier: strong ; planmode: single ; priority: 2 ; supersedes: WI-508
open_item len: 541 ; scope chars: 3027
intake.owes_successor(meta)        -> True
intake._mint_shape_refusal(draft)  -> None
draft['kind'] in schedule.SAFETY_CLASSES -> True
```

Every key is in `_DRAFT_KEYS`; `_draft_refusal` returned nothing; title is under
the 120-char `check_trajectory` bound. With `owes_successor` True AND a parsed
draft, `handback.close_adjudication` (handback.py:521) and
`intake._disposition_drafts` (intake.py:1184) both fall through — the refusal is
gone. `grep -c '^OUTCOME:'` on the verdict -> `1` (line 108,
`OUTCOME: PARTIAL successors=1`); the only other occurrence is the prose word at
line 9. So the first and only machine line still governs.

**BLOCKER 2 (owner-owed by omission) — FIXED.** The `open_item` cell poses one
question with two named branches ("STAND at the wi508 branch's 2026-08-30
bytes … or … RESTORED to the pre-merge `6d3d9db4` bytes"), which is rulable as
written. `intake._inject_open_item` mints a `pending` OI and appends its id to
the successor's `needs`; `schedule._waiting_reasons` (schedule.py:686) then emits
`waiting:open-item-pending:<id>`, so the parking claim is real, not asserted.
The verdict's Findings section now carries it as a [MAJOR] naming the omission.

**MAJOR (decision-9 miscitation) — FIXED and the replacement is accurate.** The
new Basis bullet states the measurement was "on the lane, against the lane's own
pre-measure live state … predates the merge", matching
`docs/decisions-for-review-2026-08-31.md:203`, and quotes 2269 / 14 / 4 vs
16 / 0 / 0. Re-measured independently: `diff docs/requirements/<f>.toml
docs/archive/last_approved/docs/requirements/<f>.toml` -> 16 / 0 / 0 for
interfaces / external / components; the same diff at `6d3d9db4` -> 2269 / 14 / 4.
Correct.

**MAJOR (unexecutable successor) — FIXED.** Captured `scope` is 3027 chars, and
it names, checked line by line: the four rows (`LLR-203`, `LLR-204`, `TC-199`,
`TC-200`) with their live statuses; the KEEP decision on the `580df781`
`Drafted` -> `Approved` flips as "a named keep decision, not a defaulted one",
with `TC-199`/`TC-200` held `Drafted`; BOTH ruling-conditional baseline branches
with the command (`python project-trajectory/scripts/intake.py --root . snapshot`
in the row's own approval commit) for "stand" and the `6d3d9db4` re-copy plus
`docs/ratify/CURRENT.md` regeneration for "restore"; `OI-72` inheritance ("owned
and discharged by the re-scoped `WI-543`; do not re-open the `SR-163` shape");
and the two `010-REVIEW-A-5175065` BLOCKERs routed with their file:line and a
required Deliverable ruling (annotate-as-caveat or file a sterile re-run row).
It also states an EXPLICITLY NOT IN SCOPE clause. A worker can execute this.

**MINOR (tier) — FIXED.** `buildtier = "strong"` in the block, and the verdict
carries the reasoning as a fourth finding.

**MINOR (round-10 claim) — FIXED and correct.** The Basis now reads "The lane's
STANDING verdict is round 019 CHANGES-REQUESTED, not an APPROVE", with
`899352b7` (05:47, APPROVE) → `209773cf` (08:46, findings=1) → `fa3c99c4`
(08:59, findings=3) and the surviving row-level claim resting on the diff. All
three commits and verdict counts re-checked; correct.

**MINOR (unrouted BLOCKERs) — FIXED by routing**, and the Basis states honestly
that they fall outside the range and were on no queue.

**Corrections that could themselves misstate — checked.** `77270030` is
`integrate: merge wi-555-wi508-partial-close (WI-555)` ✔. `13593db9` is the
2026-08-24 sitting ✔. `git merge-base --is-ancestor 6ba2711078 HEAD` -> yes ✔.
`docs/test/test-cases.toml` TC-199 `verifies = ["LLR-203"]`, `status = "Drafted"`;
TC-200 `verifies = ["LLR-204"]` ✔. `agent_common.APPROVAL_RUNGS` maps
external/interfaces/components to DevStg-Boundary/Arch/Arch, above
`human_approval_through = "DevStg-Needs"`, so "loop-legal" ✔. No
immutability convention on `docs/reviews/` exists in `check.py` or `PROCESS.md`,
and `docs/reviews/WI-566-REVIEW-A.md` is the cited precedent ✔.

**The fragment.** `gen_open_items.py --root . --check` -> `open-items view up to
date.` (exit 0). Driven directly:

```
fragment_declarations -> [{'file':'docs/log.d/WI-568-…md','line':3,'ids':[],
                           'none':True,'scope':None}]
deferral_findings        -> 0 findings
fragment_scope_findings  -> 0 findings
```

`scope: None` confirms the line is FILE-LEVEL (line 3, above the first `### `),
which is exactly what `fragment_scope_findings` asks for on a multi-section
fragment. All four relative links resolve from `docs/log.d/`. `check_trajectory.py`
exits 0, "clean (565 work item(s) … graph acyclic)"; its only WI-568 WARN is the
expected active-row trailer reconcile prompt.

## Findings

- [MINOR] docs/work/active/wi-568-dispose-the-close-recorded-at/WI-568-dispose-the-close-recorded-at.md:36 -> the `open_item` question attaches interfaces.toml's census figures to all three registries it names, and drops components.toml's own attribution -> `git show 6d3d9db4:docs/ratify/CURRENT.md` renders the pre-merge off-spine census as two lines, not one: "`docs/requirements/interfaces.toml` — 132 changed, 30 added, 3 removed … ruling(s): OI-64, OI-65, OI-67, WI-522, WI-528, WI-530, WI-531, WI-533, WI-534, WI-553" and "`docs/requirements/components.toml` — 1 changed, 0 added, 0 removed … ruling(s): WI-520"; `external.toml` carries no census row at all (its 14 diff lines were not row-level changes). The cell as written reads as though 132/30/3 spans "interfaces.toml, external.toml, components.toml", and `WI-520` — the one ruling behind the components change the reseal also absorbs — is named nowhere in the question the owner will rule on -> split the figures in the cell: "interfaces.toml 132 changed / 30 added / 3 removed (OI-64, OI-65, OI-67, WI-522, WI-528, WI-530, WI-531, WI-533, WI-534, WI-553) and components.toml 1 changed / 0 added / 0 removed (WI-520)"; this is not mechanizable — the cell is free text posing a human question, and no check can bind its prose to the generated census it paraphrases, which is exactly why the figures must be copied rather than summarised -> @worker

VERDICT: APPROVE findings=1
