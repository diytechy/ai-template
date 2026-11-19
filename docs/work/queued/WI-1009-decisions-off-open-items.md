+++
id = "WI-1009"
title = "docs/open-items.html stops listing delegated decisions one by one; the listing moves to a surface of its own"
workstream = "process"
sr_refs = ["SR-225", "SR-049"]
specref = "docs/plans/2026-11-11-test-tiers/HANDOFF.md#126-progress-log"
buildtier = "medium"
safety_class = "spine"
priority = 3
+++

## Context

Filed by hand on 2026-11-18 at the operator's direction: the "Decisions to
review" section is too much for `docs/open-items.html`. On 2026-11-18 it held
1,144 cards, 110 of them high-risk, almost all from coordinator sessions of
October. They crowd out the page's purpose: the pending decisions and the
acceptance act.

The entries already have a home. Each delegated run writes its own record,
`docs/decisions/<run>.toml` (132 files on 2026-11-18). The page only renders
them, through `pending.decisions_to_review`. Taking them off the page loses no
data.

SR-225 still requires a listing of each entry the operator has not yet seen,
and of each overruled entry beside the open work that carries it. So the
listing moves; it is not dropped. The scope critique picks where:

- (a) **Recommended:** its own generated page, `docs/decisions.html`, from the
  renderer that draws the section today. `docs/open-items.html` keeps one line
  with the counts and a link. SR-225 stays as written; only the rows that name
  the page change.
- (b) A listing printed in the terminal (`pending.py`), with no page.
- (c) Amend SR-225 so that the record files are the listing. This changes the
  requirement's meaning, so it needs the operator's ruling.

Whether the October backlog should be marked seen in bulk is a separate
question for the operator. It is not part of this item.

Text that names the section and will change with it: IF-074's contract (in
`gen_open_items.py` and `interfaces.toml`); LLR-118 and LLR-283; TC-123 and
TC-293's methods and evidence; the `Decisions to review` line `traj_status.py`
writes into `docs/status.md`, which links the page's anchor; and the header of
`project-trajectory/decisions.template.toml`, which ships.

## Done-when

- [ ] `docs/open-items.html` renders no card for a delegated-decisions entry.
      It shows at most the counts of unseen, high-risk and overruled entries,
      and where to read them.
- [ ] The listing SR-225 requires is on the surface the scope critique chose,
      high-risk first, with overruled entries beside the open work that carries
      them.
- [ ] The rows, the shipped template header and the status line name the new
      surface. The amended accepted rows are listed for the operator's
      re-accept, and a RESYNC entry covers the shipped change.
- [ ] `gen_open_items.py --check`, `trace.py --strict`,
      `check_trajectory.py --strict` and the touched test modules pass.
