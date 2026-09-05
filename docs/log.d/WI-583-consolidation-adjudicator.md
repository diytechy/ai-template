## 2026-09-04 — WI-583: the consolidation adjudicator

Plan §1 of `docs/plans/2026-09-02-backlog-restructure-and-consolidation.md`,
built out of band as a hand commit series on `contract_split` (owner direction
2026-09-04): the `consolidate` brief, the digest-guarded census that mints it,
and the close that absorbs several queued rows into one successor.

**What landed, plan section by section.**

- **§1.1–§1.2 — the brief.** `prompts/adjudicate-consolidate.template.md` plus
  `adjudicate_brief.VERDICT_GRAMMAR["consolidate"]`. `adjudicate-conflict` is
  RETIRED rather than left standing beside its replacement (Done-when 1's
  "otherwise retire it"): it had a template and a grammar and none of the three
  things that make a brief real — nothing minted such a row, no assembler filled
  its slots, and nothing read the `needs=` its grammar demanded. Its three
  questions survive verbatim in the new template; what is new is the CONSOLIDATE
  exit and the `{prior}` slot. Both verdict counters are required on every
  alternative, `-` being the honest "none": a counter that appears only on the
  alternative that uses it lets a session omit it and still parse.
- **§1.3 — the census and its guards.** `scripts/consolidate.py` (new). The
  pre-filter is `check_trajectory.queue_conflict_pairs` — the same three signals
  the validator has warned on since LLR-160, now produced at PAIR grain so the
  census reads edges instead of parsing the warn sentences — plus two signals a
  queue accumulates on its own: rows commissioned by one plan document or one
  open-item edge, and rows whose SR-Refs reach the same LLR `Module` or whose
  own Context/Done-when names the same file. Three guards, all on typed cells:
  no mint beside another judgement; no mint for a queue state a `consolidate`
  row already carries in its `Digests` cell (in ANY status, terminal included —
  that arm is what stops the census re-minting forever after its own close); and
  a row an earlier consolidation minted never seeds a cluster and may never be
  re-absorbed. Minted `priority = 9`, `buildtier = strong`, with typed
  `Adjudicates` and `Digests` cells.
- **§1.4 — the evidence assembler.** `adjudicate_brief.consolidate_values`,
  all-or-nothing like its four siblings, with two refusals only this brief needs:
  every row of the cluster or none (the verdict ABSORBS what it is shown, so a
  judge shown four of five drafts a `supersedes` that silently omits one), and
  the overlap must still exist at composition time. `{spine}` and `{prior}` have
  STATED literals rather than blanks.
- **§1.5 — the close.** A consolidation arm in `handback.close_adjudication`,
  reading a typed `## Consolidation` TOML block in the judging row's own spec.
  It writes the hard `needs` edge for QUEUE-WITH-EDGE (the reader the conflict
  brief promised and never got) and moves `queued/ -> draft/` with the finding
  quoted into Context for RETURN-TO-DRAFT. The absorbed rows' move into
  `docs/archive/work/restructured/` is `consolidate.archive_absorbed`, called
  from `intake._mint` — see the deviation below.
- **§1.6 — the fourth terminal word.** Already on trunk from the 2026-09-02
  out-of-band series; built on, not rebuilt.
- **§1.7 — what stays out.** Honoured as written: no structural-classifier
  producer for the `structural=` seam in `schedule.kind_of`, and no change to
  batch admission. Consolidation reads declared classes.

**Deviation from the plan, and why.** §1.5 and WI-583 Done-when 3 place the
absorbed rows' move to `restructured/` in `handback.close_adjudication`. It runs
at the MINT instead, and the ordering is forced from both ends: the absorbed
row's whole Deliverable is `Restructured into WI-<successor>.` and that id is
allocated by `intake._mint` at the row's MERGE, one commit after the close; and
`intake._supersedes_refusal`'s `absorbed_ids` arm refuses a draft continuing an
already-`restructured` row, so archiving at the close would make the mint refuse
its own successor. Everything the close CAN do at close time it does, including
the refuse-by-name guard Done-when 3 asks for. The rule has one home
(`consolidate.py`); `handback` and `intake` are its two call sites.

**Not wired into `dispatch._admit`.** `intake.mint_consolidation(root, busy)` is
the arm; the call site is four lines at the top of a tick and belongs to another
lane's module. Nothing else mints a `consolidate` row, so the machinery is inert
until it is called — which is the honest state to leave it in rather than
editing a file this session does not own.

**Two spine rows the plan did not name, authored because a HARD test demanded
them.** `tests/test_traj_views.py::test_meta_component_top_view_smoke` asserts
`uncontained == []` over this repo's own arch map — deliberately, so that any
module landing ahead of its spine rows reds rather than needing a renewed
allowance — and it caught `project-trajectory/scripts/consolidate.py` in the full suite after every
smoke-tier run was green. So `LLR-210` (module `consolidate.py`, parent SR-157,
`Component = CMP-008`) and its covering `TC-208` are authored **Drafted**, and
no `Status` was flipped: authoring is not approving, and the first approval is
an adjudication session's act on the trunk side. `trace.py --bump-ids` raised
LLR 209 -> 210 and TC 207 -> 208; the strict-integrity pass reads
`orphans=0 integrity=0`, drafts 11 -> 13.

**Known residue, reported rather than absorbed.** No `IF-###` row names
`project-trajectory/scripts/consolidate.py`, so `check_trajectory` still warns `connectivity
undeclared` for it — warn-only, and declaring the seam is an interface-authoring
act this row does not scope. The census is also not called from
`dispatch._admit`; see above.

**Measurements.**

- Smoke tier, `python -m pytest -q -n auto -m smoke`: 1581 passed, 8 skipped in
  40.67s; budget check `within` (50.9s vs 60s). The tier's membership ceiling
  was re-stamped 1560 -> 1626 (1564 collected at the re-stamp, ~4% headroom) for
  `tests/test_consolidate.py` and three call-site pins — all pure functions over
  hand-built rows, none bootstrapping a scaffold. THE SECONDS BUDGET WAS NOT
  MOVED: this box read 70.4s on the UNCHANGED tree before any of this work began
  and 96-185s during it under concurrent sessions, which is an environmental
  reading and not a tier that grew.
  fig: cmd="python -m pytest -q -n auto -m smoke" rev=7f8a4a7a
- Full suite, `python -m pytest -q -n auto`: 3447 passed, 25 skipped
  in 735.69s (0:12:15), on the tree this close commits. An EARLIER full run on
  the same code tip reported `1 failed, 3446 passed, 25 skipped` -
  `test_meta_component_top_view_smoke`, the uncontained-module assertion that
  bought the two spine rows above. It is recorded because a green that replaced
  a red is a different fact from a green that was always green.
  fig: cmd="python -m pytest -q -n auto" rev=d63feaf3+close

**Reviewed ratchet bumps**, each with its reason in the baseline entry:
`bootstrap.py` +1 (one MAPPING row), `check_trajectory.py` +4 (the
accumulate-and-pair shape; the naive 3-tuple literal cost +14 to ruff-format
expansion alone), `intake.py` +14 then +2 (call sites only — the archival cost
+25 written into `intake` and +2 written where it belongs, measured both ways).
One complexity row RE-KEYED, not bumped: `queue_conflict_findings` -> 
`queue_conflict_pairs` at the same 21.

Deferred open items: none — every question this row raised was answerable from
the plan or from the machinery, and the one place the plan and the machinery
disagreed (§1.5's ordering) is recorded above as a deviation rather than left
for a ruling.


## 2026-09-04 (later) — WI-583 rework: two adversarial rounds

The close as first landed was reviewed hostilely twice, independently: Sol (via
codex) returned 11 findings, an Opus session on a scratch clone returned 9, and
the two BLOCKERs agreed. Every finding was RE-DRIVEN on the merged tree before
it was believed; every one held. This entry records what they found, because the
pattern is worth more than the patches.

**One shape, six times.** The close called itself all-or-nothing and was not.
Each hole was a rung that had been *stated* — in a docstring, in the row's own
Context, in the shipped brief — and not *built*:

| Stated where | What actually happened |
|---|---|
| `_context`: "judge those rows and no others"; brief line 15; plan §1.3 | a draft superseding ANY queued row closed, merged and archived it |
| `Digests`' whole reason for existing | a forged pair enacted a verdict against a moved queue |
| `archive_absorbed`: "all or nothing" | a claimed row was skipped silently, one line missing out of three |
| `_consolidation_close`: "a half-enacted verdict is not a state this can reach" | the mint-side lineage refusal fired one commit after the close committed, wedging the queue permanently |
| the brief template: "the two cannot disagree" | nothing compared the machine line with the typed block |
| plan §1.2: the session drafts ONE successor | two drafts closed cleanly and split the scope |

Plus the one that was a promise rather than a claim: plan §1.5 / Done-when 4,
the absorbed rows' Done-when blocks quoted verbatim into the successor. The
template promises it in so many words, so a judge who followed the brief wrote a
boundary sentence and nothing else — and the successor a lane then built carried
no acceptance criteria at all. That is the finding worth remembering: a
DOCUMENTED behaviour with no implementation is worse than an undocumented gap,
because the document makes everyone downstream act as though it is there.

**The census is wired** (`dispatch._admit`), which closes Done-when 2 and makes
plan §4's acceptance path reachable from a run at all.

**Wiring it found a defect neither reviewer did**, and that is the argument for
wiring over describing. The minted row's SpecRef was a literal
`docs/work/README.md`; `integrate.claim` REFUSES a SpecRef that does not resolve
(R-E, WI-370). On a repo without that file the census minted a judgement that
could never be claimed, `_judgement_first` put it at the head of the frontier,
and the run exited 1 on every tick afterwards — the queue wedged by the census
meant to unblock it. It is an ordered existence probe now, and the census
DECLINES rather than minting an unclaimable row.

**The suite's own blind spot, named.** Both text transforms used `str.partition`
on `\n+++\n` / `\n## Context\n`, which finds nothing on a CRLF checkout — so on
Windows every absorbed row would have been skipped silently. The suite could not
see it because every fixture calls `conftest.pin_autocrlf`, which is exactly
why that regression test builds its CRLF bytes by hand instead of checking them
out.

**Mutation-verified, nine for nine.** Each new guard was removed in turn and the
test written for it went red: the scope bound, the digest drift, the one-draft
rule, the pre-close lineage refusal, the all-or-nothing archival, the Done-when
quoting, the machine-line reconciliation, the collection type/uniqueness rules,
and the CRLF-agnostic transforms. A tenth check found the first version of the
type/uniqueness test VACUOUS (it passed with the guard removed, because a later
rung caught the same input with a worse message) and it was rewritten until it
bit.

**A regression the existing suite caught that no reviewer did:** scoping. The
first cut archived off the whole mint lineage, which refused every ORDINARY
disposition mint by name — a disposition successor supersedes an
already-terminal row. The archival now keys on a `consolidated` flag set from
the judging row's declared brief.

**Corrections to the record.** `LLR-167`'s Approved `detail` claimed `conflict`
and `amendment` are "deliberately unrouted" — both falsified by the change that
fixed the module header. Amended in-lane per the re-pointing rule, no `Status`
flipped and no snapshot run, so it rides as snapshot drift to the next sitting
(the two warns on the close commit are that, working). `docs/declared-absences`
lost the entry naming the DELETED conflict template, which was masking exactly
the references an adopter would need to fix, and its sibling now reads as
shipped. `check_doc_refs` is back to its trunk count of 2 dangling.

**Measurements.**

- Merge: `contract_split` at `503d0e7e`, three conflicts (RESYNC_PACK — both
  sides' entries kept; `test_intake.py` — both additive blocks; the `intake.py`
  ratchet row — re-stamped at the MEASURED merge-result value, 1379, which
  happens to equal 1357+16+6 and the entry says so rather than letting the
  arithmetic pass for a measurement). Smoke straight after the merge, before
  anything else was touched: 1594 passed, 8 skipped in 72.56s.
- Smoke at the rework tip: 1615 passed, 8 skipped in 52.48s; budget 63.2 s vs
  60 s, this box under load and not a tier that grew (it read 49.6 s quiet on
  the same tier yesterday).
  fig: cmd="python -m pytest -q -n auto -m smoke" rev=7febfcfe
- Full suite at the rework tip: 3504 passed, 25 skipped in
  1056.43s (0:17:36), on the tree the rework commit carries.
  fig: cmd="python -m pytest -q -n auto" rev=7febfcfe

Ratchet: `intake.py` 1379 -> 1397 (reason in the entry); `_disposition_drafts`
complexity RE-STAMPED DOWN 25 -> 20 in the same commit, the extraction paying
for itself; `close_refusal` measured 21 and was decomposed OUTWARD into five
ordered rungs rather than bumped.

Deferred open items: none — every finding either landed or is stated above as
warn-only residue with the reason it is not this row's to close.


## 2026-09-04 (round 3) — WI-583: what a second look at a fixed thing finds

The rework above was reviewed hostilely again, on the range it produced. All 20
earlier findings re-drove as closed and all nine mutation tests re-drove as real
detectors — and six more findings came back, three of them MAJOR. That result is
the entry worth keeping: **a round that confirms the last round's fixes is not a
round that finds nothing.** Two of the six were the previous round's own fixes,
one layer down.

**The half-fix pattern, twice.**

- The close was made all-or-nothing across its ARCHIVAL and left one-at-a-time
  across its EDGES and RETURNS. A two-edge verdict whose second waiter had no
  readable `needs` line refused after the first waiter's spec was rewritten and
  STAGED — the exact class the round before had raised, surviving in the loops
  nobody re-read because the docstring above them now said the property held.
  Fixed by giving both loops the preflight the archival already had.
- `reconcile_refusal` shipped as a hard refusal and the BRIEF that instructs the
  session was not amended, so a verdict written to the shipped grammar was
  refused with no way to write a passing one: the machine line spelled
  `needs=<id or ->` singular while `edges` had always been a list. The
  enforcement half of a fix landed alone, which is the same shape as a
  documented behaviour with no implementation — just pointed the other way.

**And the sharpest finding of the previous round, reintroduced one heading-shape
down.** `_done_when_block` matched only the exact `## Done-when`, while the kit's
own `check_trajectory._DONE_WHEN_RE` has always accepted `Done when`, any
heading level and numbered or suffixed forms. Measured over this repo: 22
`## Done-when`, 5 `## Done when`, 2 `### Done when`, 1 `### Done-when` — so 8 of
30 live headings were dropped, and the successor's Context then ASSERTED that the
absorbed row "declared no `## Done-when` section". Writing a new narrow reader
beside an existing tolerant one is how the 0→A→B rule gets broken in practice:
not by copying the code, but by not looking for it. `HEADING_RE`,
`DONE_WHEN_RE` and `done_when_section` now live in `kitlib.registry`, which owns
the spec body's shape; `check_trajectory` re-exports them under the private names
its own rules use, so no call site moved.

**One vacuous test, caught by the sweep and not by review.** The CRLF
normalization test passed with the guard removed: a single-line Done-when block
is scrubbed by the trailing `.strip()` whatever the reader does. Rewritten to a
two-line block, where an interior `\r` survives. The mutation sweep is worth
running even when the tests were written deliberately.

**Record corrections.** The RESYNC entry anchored `[since 1c258508]` described
wiring that landed at `7febfcfe`, 26 commits later — and the pack's own rule is
that the anchor is where the change LANDED, with the `downstream-resync` skill
applying only entries a range contains. An adopter stamped inside that window
would never have been told the census is now called. Item 4 now says plainly
that nothing calls it at that commit, and a second entry carries the wiring, the
SpecRef probe, the transaction and the checked counters. `docs/declared-absences`
also lost a section heading (`# --- A proposed artifact, not yet written ---`)
that had gone false for its only row.

**Measurements.**

- Five new guards, mutation-verified five for five: the edge/return preflight
  (both e2e drives), the tolerant heading, the sibling-heading section end, the
  CR normalization, and the brief-teaches-the-grammar pin.
- Touched modules unfiltered: 426 passed.
- Smoke: 1628 passed, 8 skipped in 65.29s; wall budget 58.6s vs 60s, WITHIN.
  `max-tests` re-stamped 1626 → 1702 (1636 collected, ~4% headroom): ten
  pure-function regressions; the two lane-tree drives are slow-tiered.
  fig: cmd="python -m pytest -q -n auto -m smoke" rev=dd7bc7fd
- Full suite at the round-3 tip: 3517 passed, 25 skipped in 743.61s (0:12:23).
  fig: cmd="python -m pytest -q -n auto" rev=dd7bc7fd

No complexity or module-size bump: the close's new preflight is two sibling
functions, and the Done-when reader moved out rather than growing in place.

Deferred open items: none.
