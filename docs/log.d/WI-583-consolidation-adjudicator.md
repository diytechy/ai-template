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
allowance — and it caught `scripts/consolidate` in the full suite after every
smoke-tier run was green. So `LLR-210` (module `consolidate.py`, parent SR-157,
`Component = CMP-008`) and its covering `TC-208` are authored **Drafted**, and
no `Status` was flipped: authoring is not approving, and the first approval is
an adjudication session's act on the trunk side. `trace.py --bump-ids` raised
LLR 209 -> 210 and TC 207 -> 208; the strict-integrity pass reads
`orphans=0 integrity=0`, drafts 11 -> 13.

**Known residue, reported rather than absorbed.** No `IF-###` row names
`scripts/consolidate`, so `check_trajectory` still warns `connectivity
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
