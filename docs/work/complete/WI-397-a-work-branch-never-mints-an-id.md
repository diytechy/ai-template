+++
id = "WI-397"
title = "RULED 2026-08-01 (owner, R1 in docs/archive/history/backlog-plan-2026-08-01.md): a WORK BRANCH NEVER MINTS A NEW WORK-ITEM ID - minting is a serial trunk-side act only (claim bookkeeping, the adjudication mint when that row lands, a human trunk commit). THE DRIVEN CASE: on 2026-08-01 two lanes independently minted WI-392 because a lane can only see its own tree, and three further rows existed only on the wi-391 branch until it merged - during which trunk's max id (394) sat BELOW the branch's ids (395/396), so any trunk mint in that window would have re-collided. THE CONSTRAINT: one refusal rung at the merge slot - a finished branch whose docs/work/ delta ADDS a spec file carrying an id outside its claimed set is refused, the _claim_refusal shape applied at the other end of the lane's life. Allowed and unchanged: state moves and content edits of the branch's OWN claimed rows (the terminal-outcome moves), the handback artefacts, and every trunk-side bookkeeping commit. This makes the id collision UNREPRESENTABLE rather than coordinated around, and it DELETES the id-reservation question from the dispatcher row's scope before that row is built - net less code, which is why the ruling chose it over a reservation table (enforcement-layer growth of the audited shape) and over lane-namespaced ids (two id grammars plus a renumbering rewrite of cross-references). Lane-discovered findings are recorded as PROSE (spec body, log fragment, review record) and receive their id at or after merge - the handoff-2026-08-01.md §6 findings from the Part 1 integrations are the worked example of the discipline. DONE-WHEN, driven not asserted: the rung refuses a constructed branch that adds a foreign id; admits the same branch with the foreign spec removed; admits a branch performing only its own terminal-outcome move and a handback's queued/ return; and the R1 ruling is recorded in log.md's Decisions with this row named as its executor. SCOPE GUARD: keep it ONE rung - do not grow a general docs/work/ diff-policy engine around it, and do not touch the trunk-side minting paths, which stay exactly as free as they are today."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

`integrate._minted_id_refusal` — one rung at the merge slot. A finished branch
whose `docs/work/` delta, read from `merge-base(trunk, branch)` to its tip,
**ADDS** a spec file carrying an id outside its claimed set is refused by name:
the foreign id(s), the path(s) that carry them, the claimed set they were judged
against, and the rule. The claimed set is trunk's own `active/<branch>/` read
(`_claimed_wi_ids`) — the reader that was already there, not a second one.

Trunk-side minting is untouched, and by construction rather than by exemption:
whatever trunk did sits in the merge **base**, so it is not in the branch's
delta at all. The claim's bookkeeping commit, WI-388's mechanical adjudication
mint and a human trunk commit are all exactly as free as they were.

Three shapes stay admitted, each driven rather than argued: a terminal-outcome
move into `complete/` or `cancelled/` (which re-ADDS a file whose id the branch
already holds claimed), a handback's return to `queued/` with its bar-inert
`docs/work/handback/<branch>.patch` (which carries no spec filename), and any
content edit of a claimed row (an `M`, never an `A`).

The delta is read `--no-renames`, and that is load-bearing rather than tidy:
with rename detection on, git pairs the minted spec with the DELETE side of the
branch's own close — spec files are short and near-identical — and the mint
arrives as one `R` record with **no add left to see**. That trap is measured in
`tests/test_integrate.py`, not asserted.

Three deduplications the repo's other ratchets asked for on the way, none of
them new surface: `_spec_id` (one filename→id read, shared with `_claimed_specs`
so the rung's "is this id in that set" question cannot be answered by two
parsers that disagree), `_name_status` (one `--name-status` parse, replacing the
copy `check_dupes` convicted in `_abandoned_claim`), and `_merge_refusal` (the
slot's whole ladder lifted out of `integrate_one`, which the new rung had pushed
to C901 11 — extraction over a bigger number, the `_drop_abandoned` precedent).

The ruling itself is recorded in [log.md](../../log.md)'s Decisions naming this
row as its executor. That entry is written **on the trunk**, not by this branch:
`## Decisions log` is one of `trunk_step.RESERVED_HEADINGS`, so a log fragment
may not claim it — the log's shape is not a work branch's to redefine, and every
prior ruling in that section arrived the same way.
