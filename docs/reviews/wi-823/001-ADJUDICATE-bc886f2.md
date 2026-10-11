# ADJUDICATE — WI-823 @ bc886f2: TC-055 Method amendment

Question: did the amendment change the row's MEANING or only its CLARITY? Judged
on the before/after cells against the 2026-10-10 anchor (`docs/archive/last_approved`,
b6766302e), read with the rubric, judge-brief and shot-matrix diff `fe30b0a4..HEAD`.

- [MEANING] TC-055 Method -> before: the CRITIQUE judge is given the rubric, the SN/SR intent and the shoot.mjs PNG matrix, and returns a VERDICT citing numbered anchors; nothing constrains the run or the matrix the verdict stands on -> after: the judge is ALSO given the scope lines and TC ids of every test-bound row behind a live anchor, and no judgment may be made on a failed shot run or an incomplete matrix -> not the same: two obligations were added. A brief that was correct under the old text (rubric + intent + shots, no test-bound scope lines) fails the new one, and a verdict the old text allowed on a run that exited non-zero or missed a rendered tab (today: Retired, absent from the old TABS) is forbidden by the new one. Both changes sit in this one cell.

Re-attestation judgement (the TC rung is RELEASED, so this is the adjudicator's to make): I would bless the new text.
- Upward: it serves SR-054's stated limit — only the clause no test holds rests on a judgement — and LLR-055's "keeps ONLY what a test cannot pin". Handing the judge the scope lines of the tests that own each anchor's core is the mechanism that keeps a verdict from re-ruling a tested clause, which TC-055's own Expected cell already requires ("a clause a test now holds is verified through the LLR/TC chain ... not by a verdict").
- Closed obligation: "every test-bound row behind a live anchor" is determined by the rubric, which Expected names as the single home of the live anchor set; "incomplete matrix" is measured against the tabs the page renders, which shoot.mjs reports (`NOT shot`). Both are observable in the recorded brief and run output.
- Not submitted, noted for the coordinator: LLR-055's detail names only the T2/T3/T1 child rows, while the rubric now also binds T4 (LLR-119), T5 (LLR-105, LLR-285) and T8 (LLR-120, LLR-292). The new Method does not depend on that list (it reads the set from the rubric), so the gap does not block this row; it predates this lane.

VERDICT: MEANING rows=1
