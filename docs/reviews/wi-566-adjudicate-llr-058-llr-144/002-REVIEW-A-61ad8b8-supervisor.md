# WI-566 REVIEW-A (supervisor-drawn) — adjudication of the WI-553 spine amendments

No mechanized round exists for adjudication lanes (WI-559); drawn by the
supervising session through an independent Opus reviewer, read-only, at HEAD
`61ad8b8f` (adjudication commit `5550bd96`, mechanical close `825fc966`,
base `05fb6a34`). The reviewer re-derived every classification from the raw
cell diffs (`git diff a024e766..fa923231` over the two registries), read the
verdict-line contract (`adjudicate_brief.py:148`) and
`handback.close_adjudication`'s refusal invariant, and ran
`check_trajectory.py --strict`, `trace.py --approve modified`, and
`gen_open_items.py --check`.

The six in-scope rows (LLR-058, LLR-144, LLR-198, TC-138, TC-147, TC-194 —
eight cells) are all correctly called MEANING; no in-scope row was
under-called CLARITY, and the re-attestation obligation is genuinely carried
by the snapshot-drift machinery (`docs/archive/last_approved/` still holds
the old text; `--approve modified` renders all six rows). Close mechanics
sound. But the verdict's census and its disposition record both fail.

## Findings

- [MAJOR] docs/reviews/wi-566-adjudicate-llr-058-llr-144/001-ADJUDICATE-05fb6a3.md:1 -> seventeen of the verdict's twenty-three lines (SR-024, 033, 043, 052, 053, 054, 111, 112, 129, 144, 146, 147, 149, 167, 175, 176, 177) were already adjudicated and CLOSED by WI-547 ("VERDICT: CLARITY rows=17", the id set matching byte for byte); the SR registry is untouched in this row's range (`git diff a024e766 fa923231 -- docs/requirements/system-requirements.toml` is EMPTY) and the spec's generated Context lists only the six LLR/TC rows. `rows=23` overstates the adjudicated population by 17 and silently re-imports a closed row's verdict -> re-issue the verdict over the six in-scope rows only (`VERDICT: MEANING rows=6`), or keep the SR lines explicitly marked as WI-547 restatement and excluded from the counter -> @owner
- [MAJOR] docs/work/complete/WI-566-adjudicate-llr-058-llr-144.md:13 -> the row's Context demands either the no-scope-moved recommendation or drafted rows in a `## Dispositions` section, and six MEANING rows were found — yet the closed spec has NO `## Dispositions` section while its machine-inserted Deliverable asserts "Its `## Dispositions` successors mint at this row's own merge": a record promising successors that cannot exist. There may genuinely be no work owed (WI-553 already moved the code; the drift brief carries the re-attestation) but that reasoning appears nowhere -> add a `## Dispositions` section, or state on the record why the six MEANING rows owe no successor beyond the owner's signature on the `--approve modified` brief -> @owner
- [MINOR] project-trajectory/scripts/handback.py:519 -> nothing guarded this close: `intake.owes_successor` keys on the `dispose:` title prefix, but this row's title begins `adjudicate:` and its brief is `amendment`, so an amendment-brief adjudication that rules MEANING and drafts no successor passes both refusal invariants untouched -> extend the invariant (or a warn) to an `amendment` brief whose verdict is MEANING and whose spec carries no `## Dispositions` section -> @owner
- [MINOR] docs/log.d/ -> the lane wrote no session log fragment and so no `Deferred open items:` declaration (`gen_open_items.fragment_declarations` returns `[]`), which PROCESS.md §5 and the session-protocol skill require of every session; the only narrative record is the commit message -> write the fragment with its declaration (`none — <why>`) -> @owner
- [MINOR] docs/work/active/wi508-architectural-remap/ -> `check_trajectory.py --strict` carries a SECOND ERROR beyond the named WI-552/WI-564 seam: the wi508 claim directory has no matching local branch (only `origin/...-HELD-for-owner-verdict` exists) — the hold-by-rename pattern WI-553's own new detector targets, so the hold-ban check is RED on trunk. Pre-existing and not this lane's (its diff is six unrelated files); the sanctioned disposal is the queued wi508 partial-close row -> close the wi508 lane through the handback path on its own row -> @owner

VERDICT: CHANGES-REQUESTED findings=5
