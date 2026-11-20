## 2026-11-19 — WI-1008: SR-033, SR-223 and SR-225 each cite an assumption stating the premise their own part rests on (DA-018, DA-019, DA-020, all Drafted)

Deferred open items: none.

Built on the maintenance branch `maint/wi-1008`, cut from `refactor_again` at
`84ca8c4f0`, outside the lane workflow at the operator's direction: no claim,
no lane review rounds, commit hooks on. The parent session reviews and merges.

- **The critique.** Gemini Argon's round 1 raised four findings, and all four
  were adopted. `planmode = "none"`, since the row adds no code path (S4). The
  Context states the delta: three registry rows, each landing on B-09, and no
  code (S5). The three premises land together, for one acceptance act (S1).
  SR-225's assumption names no page, so the row does not wait on WI-1009 (S6).
  S5 also found that `docs/open-items.html` renders no assumption. Measured
  further: a change to `da_refs` alone leaves the page byte-identical, because
  the cell is traced. So the second Done-when item now names where the new
  rows are shown today, and WI-1010 is the item that adds them to the page.
- **The rows.** DA-018: the person releasing works through the release
  checklist, checking each listed budget against a measurement of the release
  and each listed assumption for its falsifier. DA-019: a model in a guarded
  session acts on the guardrails payload chosen for it. DA-020: a delegated
  run's record lists every call it was told to record, as its work shows it,
  and the operator reads each entry listed as not yet seen. Each requirement
  cites its own in `da_refs`, a traced pointer, so all three stay `Accepted`
  and owe no re-accept. The three assumptions owe their first acceptance.
- **Where they land.** All on B-09, the operator's read crossing. B-05 (SR-223's
  crossing) is never a landing, and B-10 belongs to the model provider, which
  is no stakeholder's party. The reach check reports nothing for the three.
- **The gate's steps** (off, so advisories): `assumption-gate` 76 findings
  before and 79 after, the three new ones being "relies on assumption DA-0NN,
  which is not accepted (Status Drafted)". `crossing-allocation` 9 before and
  9 after, none of them these rows.
- **The review.** Gemini Argon read the rows and asked for two falsifier
  fixes, both applied. DA-018's falsifier also catches a budget item ticked
  with no measurement of the release. DA-020's gains an arm for the case where
  the operator reads nothing: an entry still listed as not yet seen after
  later integrated work has built on the call it records, as git history
  shows.
- **For the operator.** Both of DA-020's reading arms are already observed
  here. `coordinator-2026-10-04`'s 13 entries have no verdict, while an entry
  of `coordinator-2026-11-05` was confirmed on 2026-11-05. One of the 13,
  D-003, is the call to keep the WI-788 lane open, and the lane landed on it
  the same day. Across all records, 52 of 1,194 entries have a verdict. DA-018 and DA-019 have nothing to
  observe in this repository yet: it has made no release, and it vendors no
  guardrails payload.
