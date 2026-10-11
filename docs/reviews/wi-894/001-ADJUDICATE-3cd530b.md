# ADJUDICATE — WI-894 @ 3cd530b: disposition of WI-828's partial close

Judged on the per-close report `docs/handbacks/WI-828-wi-828.md` (a claim),
WI-828's spec in `docs/work/partial/`, and the commit facts: the report's range
`24a3ff4f38..24a3ff4f38` (empty), the lane branch `wi-828` (one commit past it,
`580a39e84`, the report plus the spec's move), and the squash landing
`e925bebb8`. I also read the rows the coordinator filed by hand in `a722ab7f5`
(D-015): WI-893 (queued), WI-892 (active) and OI-113 (pending).

**1. The claimed outcome is right: PARTIAL.** WI-828 delivered none of its
Done-when. The lane branch adds only the handback and the spec move. The squash
`e925bebb8` adds bookkeeping: the generated state, `status.md`, the needs of
WI-833/WI-850/WI-851 re-pointed, and WI-892's spec widened. No code and no spine
row changed. COMPLETE would be wrong. CANCELLED would also be wrong: the ask
still stands and waits on an owner ruling (OI-113), and the lane did not decide
it should never ship. The one route that would retire it, OI-113 option (d),
is the owner's to choose and is not chosen.

**2. The keep/discard split is honest.** Both lists are empty, and the range is
empty, so nothing of the lane's work stays on trunk. The round-1 diff is
outside the repository (`C:/Projects/ai-template.wt/wi-828-round1-parked.patch`,
25,450 bytes, present). It is neither a keep nor a discard left on trunk. It is
an off-record artifact that two queued specs cite (the last finding below).

**3. The successor already exists, and the existing rows carry the substance.**
WI-893 is queued with `needs = ["OI-113", "WI-892"]` and
`specref = "docs/requirements/open-items.toml#OI-113"`. That is the placeholder
shape an `[open_item]` mint would have produced. OI-113 is `pending` and carries
all four cells (`one_line`, `blast_radius`, `options` (a)–(d) and
`recommendation` (a)). That is the owner card I would have written: the trunk
identity the walk needs is a design choice with adopter-facing cost, so it is
the owner's. No queued row still `needs` WI-828; the squash re-pointed
WI-833/WI-850/WI-851 to WI-892 by hand. So the edge re-point a mint would make
is already done. Drafting a `## Dispositions` block here would mint a second
queued row for the same scope, both behind OI-113 and both answering SR-140.
That duplicate is worse than every gap below, so I drafted none.

One part of the substance is missing: lineage. WI-893 carries no `supersedes`,
so nothing joins WI-828 to its continuation across the id change.

**4. WI-828's ask continues in two rows, not one.** The report's "Not
delivered" says the whole Done-when goes to WI-893. The squash's own message
and diff say otherwise. Done-when bullet 1's shared walk ("the hook's one
lane-commit walk ... so later per-commit checks ride the same walk") went to
WI-892: its title and Done-when gained "one lane-commit walk with a rider
tuple". Only the hand-merge path (`HEAD..MERGE_HEAD`) went to WI-893. The report
is immutable, so this verdict is where the corrected thread is recorded.

- [MAJOR] WI-893 lacks `supersedes` -> a disposition's successor must carry it so partial work keeps its thread across the id change, and without it nothing links WI-828 to the row continuing its hand-merge ask -> add the top-level frontmatter line `supersedes = "WI-828"` (a bare string) to the `+++` block of `docs/work/queued/WI-893-hand-merge-walk-per-oi-113.md`; `supersedes` is a registry column (`kitlib/registry.py`), and for a `partial` predecessor the lineage check (`check_trajectory.py` `_restructured_lineage_findings`) asks nothing back of WI-828, so WI-828 stays byte-identical -> @owner
- [MAJOR] this row's mechanical close will be REFUSED -> `handback.py` (the `owes_successor` guard near line 870) refuses a disposition row whose `## Dispositions` holds no TOML draft and stops the run for a human; no draft key names an EXISTING queued row (`intake._DRAFT_KEYS` mints a new row only) -> close WI-894 by hand, citing this verdict and naming WI-893 as the successor once it carries `supersedes`; separately, file the missing arm as its own WI (for example a draft that adopts an existing queued row by id, so a hand-filed successor discharges a disposition without a duplicate). This is a gap in the machinery, not a defect of this lane -> @owner
- [MINOR] the report attributes the whole unfinished Done-when to WI-893 -> the shared lane-commit walk with its text-then-act rider is now WI-892's scope (e925bebb8), so a reader following only the report misses half the thread -> no edit to the report (it is immutable); WI-892's lane may add `supersedes = "WI-828"` beside WI-893's when it next touches its spec, since it continues Done-when bullet 1, and both successors may name the same predecessor -> @owner
- [MINOR] WI-893 and WI-892 cite a round-1 diff held only on one machine -> `C:/Projects/ai-template.wt/wi-828-round1-parked.patch` is outside version control and review, and it sits in the worktrees directory, where worktree cleanup can delete it -> both builders should treat it as a non-authoritative sketch and re-derive from WI-828's spec and OI-113's ruling; once WI-892 lands, the patch's shared-walk half is superseded and can be dropped -> @owner

No `## Dispositions` block was drafted (see the second finding above): WI-893 is the successor,
filed by hand before this row was minted, and OI-113 is its owner gate.

OUTCOME: PARTIAL successors=0
