## 2026-10-09 — WI-870: the review files the strict VERDICT reader no longer reads

The migration inventory WI-870's Done-when asks for: every file under
`docs/reviews/` whose merge-gate reading changed between the pre-change reader
(`score_reviews.parse_verdict` at `c5076d62`, the last matching VERDICT line,
loosely) and the one strict reader (`kitlib.sitting.review_line`). None is
rewritten (wi-870.toml D-002). Each now reads as no verdict, which the gate
treats fail-closed; the gate reads only open lanes' rounds, so a closed lane's
file changes nothing but its generated rollup. Computed at the lane tip by a
coordinator probe over every `*.md` under `docs/reviews/`.

**87 files.** Before is the old reading (`?` = no count on the line);
after is the strict reader's refusal.

| File | Before | After (refusal) |
|---|---|---|
| `docs/reviews/012-REVIEW-A.md` | CHANGES-REQUESTED findings=2 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/014-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/017-REVIEW-A.md` | CHANGES-REQUESTED findings=1 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/019-REVIEW-A.md` | CHANGES-REQUESTED findings=1 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/023-REVIEW-A.md` | CHANGES-REQUESTED findings=1 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/036-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/077-CRITIQUE.md` | APPROVE findings=0 | no verdict: it carries the VERDICT line `VERDICT: APPROVE findings=0 (1 non-blocking observation recorded)`, which is not exactly `VERDICT: <APPROVE\|CHANGES-REQUESTED> findings=<digits>` |
| `docs/reviews/1-g3-WI-272-230f/011-REVIEW-A-057c5fb.md` | CHANGES-REQUESTED findings=2 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/1-g3-WI-272-230f/015-REVIEW-A-e5bb2a7.md` | APPROVE findings=2 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/101-GROUNDING.md` | APPROVE findings=? | no verdict: it says `VERDICT: APPROVE` but omits findings |
| `docs/reviews/130-REVIEW-A.md` | CHANGES-REQUESTED findings=? | no verdict: it says `VERDICT: CHANGES-REQUESTED` but omits findings |
| `docs/reviews/2026-09-27-wave5/sol-tc055.md` | CHANGES-REQUESTED findings=1 | no verdict: it carries the VERDICT line `VERDICT: CHANGES-REQUESTED findings=1 anchors=T2,T4,T5,T8`, which is not exactly `VERDICT: <APPROVE\|CHANGES-REQUESTED> findings=<digits>` |
| `docs/reviews/retier-v2/ROUND-2-SOL-TERRA.md` | CHANGES-REQUESTED findings=? | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-277-REVIEW-A.md` | APPROVE findings=3 | no verdict: it carries 6 VERDICT lines, not exactly one |
| `docs/reviews/WI-280-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 8 VERDICT lines, not exactly one |
| `docs/reviews/WI-346-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-355-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-366-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-367-REVIEW-A.md` | APPROVE findings=3 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-368-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-369-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-370-REVIEW-A.md` | APPROVE findings=1 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-371-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-372-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 6 VERDICT lines, not exactly one |
| `docs/reviews/WI-373-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-374-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 8 VERDICT lines, not exactly one |
| `docs/reviews/WI-375-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 4 VERDICT lines, not exactly one |
| `docs/reviews/WI-376-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 3 VERDICT lines, not exactly one |
| `docs/reviews/WI-377-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 3 VERDICT lines, not exactly one |
| `docs/reviews/WI-378-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 6 VERDICT lines, not exactly one |
| `docs/reviews/WI-379-REVIEW-A.md` | APPROVE findings=1 | no verdict: it carries 4 VERDICT lines, not exactly one |
| `docs/reviews/WI-380-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 6 VERDICT lines, not exactly one |
| `docs/reviews/WI-381-REVIEW-A.md` | APPROVE findings=4 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-383-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 12 VERDICT lines, not exactly one |
| `docs/reviews/WI-384-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 10 VERDICT lines, not exactly one |
| `docs/reviews/WI-386-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 10 VERDICT lines, not exactly one |
| `docs/reviews/WI-387-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 12 VERDICT lines, not exactly one |
| `docs/reviews/WI-388-REVIEW-A.md` | APPROVE findings=6 | no verdict: it carries 3 VERDICT lines, not exactly one |
| `docs/reviews/WI-389-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 3 VERDICT lines, not exactly one |
| `docs/reviews/WI-391-REVIEW-A.md` | APPROVE findings=1 | no verdict: it carries 12 VERDICT lines, not exactly one |
| `docs/reviews/WI-392-REVIEW-A.md` | APPROVE findings=4 | no verdict: it carries 3 VERDICT lines, not exactly one |
| `docs/reviews/WI-393-REVIEW-A.md` | APPROVE findings=5 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-394-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-395-REVIEW-A.md` | APPROVE findings=3 | no verdict: it carries 6 VERDICT lines, not exactly one |
| `docs/reviews/WI-396-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-397-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-398-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-401-REVIEW-A.md` | APPROVE findings=5 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-402-REVIEW-A.md` | APPROVE findings=3 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-403-REVIEW-A.md` | APPROVE findings=4 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-404-REVIEW-A.md` | APPROVE findings=3 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-405-REVIEW-A.md` | APPROVE findings=1 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-406-REVIEW-A.md` | APPROVE findings=1 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-409-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-410-REVIEW-A.md` | APPROVE findings=1 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-411-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 3 VERDICT lines, not exactly one |
| `docs/reviews/WI-412-REVIEW-A.md` | APPROVE findings=? | no verdict: it says `VERDICT: APPROVE` but omits findings |
| `docs/reviews/WI-414-REVIEW-A.md` | APPROVE findings=? | no verdict: it carries 3 VERDICT lines, not exactly one |
| `docs/reviews/WI-442-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 4 VERDICT lines, not exactly one |
| `docs/reviews/WI-453-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 3 VERDICT lines, not exactly one |
| `docs/reviews/WI-454-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 4 VERDICT lines, not exactly one |
| `docs/reviews/WI-535-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 3 VERDICT lines, not exactly one |
| `docs/reviews/WI-538-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 7 VERDICT lines, not exactly one |
| `docs/reviews/WI-543-REVIEW-A.md` | APPROVE findings=1 | no verdict: it carries 3 VERDICT lines, not exactly one |
| `docs/reviews/WI-547-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 5 VERDICT lines, not exactly one |
| `docs/reviews/WI-548-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 6 VERDICT lines, not exactly one |
| `docs/reviews/WI-549-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-550-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 3 VERDICT lines, not exactly one |
| `docs/reviews/WI-552-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 4 VERDICT lines, not exactly one |
| `docs/reviews/WI-553-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-555-REVIEW-A.md` | APPROVE findings=5 | no verdict: it carries 4 VERDICT lines, not exactly one |
| `docs/reviews/WI-563-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-566-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-568-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 5 VERDICT lines, not exactly one |
| `docs/reviews/WI-569-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 3 VERDICT lines, not exactly one |
| `docs/reviews/WI-571-REVIEW-A.md` | APPROVE findings=2 | no verdict: it carries 3 VERDICT lines, not exactly one |
| `docs/reviews/WI-573-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/WI-575-REVIEW-A.md` | APPROVE findings=0 | no verdict: it carries 3 VERDICT lines, not exactly one |
| `docs/reviews/wi-579-the-verdict-carrier-and-the-ad/022-REVIEW-A-6684422.md` | CHANGES-REQUESTED findings=2 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/wi-579-the-verdict-carrier-and-the-ad/036-REVIEW-A-eb4ee91.md` | CHANGES-REQUESTED findings=1 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/wi-586-adjudicate-llr-207-llr-208/010-REVIEW-A-397d4b1.md` | CHANGES-REQUESTED findings=1 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/wi-589-two-verified-defects-around-th/011-REVIEW-A-6f27419.md` | APPROVE findings=0 | no verdict: it carries 2 VERDICT lines, not exactly one |
| `docs/reviews/wi-685-re-judge-tc-055-no-result-rec/001-ADJUDICATE-fe96ec6.md` | APPROVE findings=0 | no verdict: it carries the VERDICT line `VERDICT: APPROVE findings=0 anchors=T2,T4,T5,T8`, which is not exactly `VERDICT: <APPROVE\|CHANGES-REQUESTED> findings=<digits>` |
| `docs/reviews/wi-765-re-judge-tc-055-declared-inpu/001-REJUDGE-51c48d6e.md` | APPROVE findings=? | no verdict: it says `VERDICT: APPROVE` but omits findings |
| `docs/reviews/wi-777-re-judge-tc-055-declared-trig/001-REJUDGE-2e46707c.md` | APPROVE findings=? | no verdict: it says `VERDICT: APPROVE` but omits findings |
| `docs/reviews/wi-796-re-judge-tc-055-declared-trig/001-REJUDGE-5fb0fc7.md` | CHANGES-REQUESTED findings=2 | no verdict: it carries the VERDICT line `VERDICT: CHANGES-REQUESTED findings=2 ? ANCHORS: T2=fail T4=pass T5=fail T8=pass`, which is not exactly `VERDICT: <APPROVE\|CHANGES-REQUESTED> findings=<digits>` |
| `docs/reviews/wi451-retier/ROUND-2-SOL.md` | CHANGES-REQUESTED findings=? | no verdict: it says `VERDICT: CHANGES-REQUESTED` but omits findings |
