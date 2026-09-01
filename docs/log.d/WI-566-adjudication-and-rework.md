## 2026-09-01 — WI-566: the WI-553 amendment adjudication, corrected by review

**What the row is.** WI-566 is the amendment-brief adjudication minted at
WI-553's merge (§A5.2): six approved/routed spine cells moved on merged trunk
`a024e76..fa92323`, and this row judges, per row, whether the amendment changed
the requirement's MEANING or only its CLARITY.

**The original verdict (session `…-001`, commit `5550bd96`).** The verdict file
[`../reviews/wi-566-adjudicate-llr-058-llr-144/001-ADJUDICATE-05fb6a3.md`](../reviews/wi-566-adjudicate-llr-058-llr-144/001-ADJUDICATE-05fb6a3.md)
ruled every row, then closed with `VERDICT: MEANING rows=23`. The row was closed
mechanically at its DONE (`825fc966`).

**The supervisor round.** No mechanized review round exists for adjudication
lanes (WI-559), so the supervising session drew one through an independent Opus
reviewer at `61ad8b8f`:
[`../reviews/wi-566-adjudicate-llr-058-llr-144/002-REVIEW-A-61ad8b8-supervisor.md`](../reviews/wi-566-adjudicate-llr-058-llr-144/002-REVIEW-A-61ad8b8-supervisor.md)
— `VERDICT: CHANGES-REQUESTED findings=5`. It re-derived every classification
from the raw cell diffs and confirmed the six in-scope calls and the close
mechanics, but reds the verdict's census and its disposition record.

**The corrected census: `rows=6`.** Seventeen of the twenty-three lines were SR
rows WI-547 had already adjudicated and CLOSED (`VERDICT: CLARITY rows=17`, the
same id set); the SR registry is untouched in this row's range (`git diff
a024e766 fa923231 -- docs/requirements/system-requirements.toml` is empty) and
the spec's generated `## Context` lists only six rows. `rows=23` overstated the
adjudicated population by seventeen and silently re-imported a closed row's
verdict. The verdict file is **re-issued in place** with
`VERDICT: MEANING rows=6` over LLR-058, LLR-144, LLR-198, TC-138, TC-147,
TC-194; the seventeen SR lines are retained verbatim under a section marking
them as the WI-547 restatement and excluding them from the counter, and a
correction note at the top says what changed and why.

*Why edited rather than appended.* Checked what machine-reads an ADJUDICATE
verdict line: only `adjudicate_brief.verdict_refusal` (its grammar table at
`adjudicate_brief.py:148` — `("VERDICT", ("MEANING","CLARITY"), ("rows",))`),
called from `agent_loop.adjudication_bookkeeping` *during the session*, to
decide whether the judge actually ruled. Nothing reads it after close:
`check_trajectory` parses only `*-CRITIQUE.md` with the APPROVE/CHANGES-REQUESTED
vocabulary, `score_reviews` the same, and `check_figures`/`check_vocab` skip
`docs/reviews/`. No immutability convention covers `docs/reviews/` (the
immutable per-close record is the handback report, not a verdict). And the
parser uses `re.search`, which takes the FIRST `VERDICT:` line — so an appended
correction would have left the WRONG line governing on any re-read. In-place
re-issue with one verdict line is the safe form here; the file's own correction
note keeps the history.

**Where the re-attestation obligation lives.** Nowhere new. The six rows are all
MEANING, so §A5.2's flip-back-to-Approved arm does not apply — but no successor
WI is owed either: WI-553 already moved the code to match the amended text, and
the human act the amendment owes is a re-attestation carried by snapshot drift
against `docs/archive/last_approved/`. Verified in this worktree: `trace.py
--approve modified` renders all six rows into the owner's brief (LLR-144/TC-138
under SR-144, LLR-058 under SR-148, LLR-198/TC-194 under SR-168, TC-147 under
SR-174). Six of six.
<!-- fig: cmd="python project-trajectory/scripts/trace.py --approve modified | grep -cE '^### (LLR|TC) (LLR-058|LLR-144|LLR-198|TC-138|TC-147|TC-194)$'" rev=520ca00a -->
That obligation persists in the generated brief until the owner blesses the rows
and re-snapshots in the same commit (PROCESS.md §7) — it is a human signature on
a generated surface, not schedulable work, so minting a WI for it would create a
lane that can only wait.

The closed spec's machine-inserted Deliverable had asserted "Its `##
Dispositions` successors mint at this row's own merge" while carrying no such
section — a record promising successors that cannot exist. That sentence is
replaced with the reasoning above, on the record. **No `## Dispositions` section
was added on purpose:** `intake.parse_dispositions` REFUSES a section carrying
no fenced `toml` block ("nothing minted"), so a prose-only "none owed" section
would halt the merge sweep. The kit has no shape for "adjudicated, no successor
owed"; this Deliverable is the only honest home for it today.

**Left for other rows, deliberately (both are review findings, neither is this
row's scope):** REVIEW-A finding 3 — `handback.close_adjudication` /
`intake.owes_successor` key on the `dispose:` title prefix, so an `amendment`
brief that rules MEANING and drafts nothing passes both refusal invariants
untouched; that is a kit gap owed a future row, and widening a refusal invariant
is not an adjudication-scoped edit. REVIEW-A finding 5 — the wi508 claim
directory with no matching local branch (`check_trajectory.py --strict` ERROR,
the hold-by-rename pattern) is pre-existing and rides the already-queued wi508
partial-close row.

**Deviations from spec.** None on the adjudication itself; the six
classifications stand as originally ruled and were independently re-derived by
the reviewer. The correction is to the census and the disposition record.

**Deferred open items: none** — the only outstanding act is the owner's
re-attestation of the six MEANING rows, and that is already carried by the
`trace.py --approve modified` brief (drift against
`docs/archive/last_approved/`), which is a standing generated surface, not a
deferred OI. Nothing here needs an owner ruling to proceed.
