+++
id = "WI-393"
title = "Rehome the LINK-AWARE SPEC-ARCHIVAL RITUAL that Phase 5 deleted - spec archival is an unassisted `git mv` again, and both defects it once fixed are live. WI-288 built `_relink_archived_specs` (redirect every inbound link whose target RESOLVES to the moved spec, by path relative to the file holding it, keeping the link TEXT and carrying `#fragment`s) and WI-353 built its mirror `_rebase_moved_spec_links` (re-relativise the moved file's OWN relative targets against its new directory), plus the two primitives they shared, `_rewrite_md_links` and `_resolvable_link`. All four lived in `agent_dispatch.py` and were deleted with it at concurrency-restructure Phase 5 (31ad569d). They were never rehomed, and nothing replaced them: `integrate.py` owns the CLAIM move (`claim()`, the `git mv` into `active/<branch>/`) and reads the close from the spec landing in a terminal directory (`finished_branches`), but the SPEC-OF-RECORD archival - `docs/specs/WI-###.md` -> `docs/archive/specs/WI-###.<date>.md` - is done by the worker, by hand, in the closing commit, with no relinking of any kind. `check_trajectory`'s R-F only TELLS you to archive; it does not help you do it. DRIVEN EVIDENCE (WI-391 REVIEW-A, 2026-08-01, measured not argued): from a baseline of 4 broken links, adding a probe spec plus an inbound link to it left the count at 4; a bare `git mv` of that spec into `docs/archive/specs/` took it to 8 - of which 3 are WI-353's defect verbatim (the moved file sits one level deeper, so its own `../` targets resolve one directory short) and 1 is WI-288's (the inbound link still points at the vacated path). `docs/archive/` is exempt from the ORPHAN check only, not from the broken-link check, so these land in the bar. The failure surfaces at INTEGRATION on the composed tree, which is exactly the late-surfacing shape WI-288 existed to stop and which WI-281 and WI-274 paid for live. THIS IS CONSTRAINT-SHAPED, not another check: the deliverable is ONE INDIVISIBLE RITUAL - move, relink-inbound, relink-outbound as a single operation no caller can perform two thirds of, which is how WI-288 and WI-353 each wrote it and why their docstrings say so. It removes a way to be wrong rather than adding a detector for it, so concurrency-v2 §0's constraints-over-checks argument REACHES this row, and the enforcement-layer-maintaining-enforcement-layer objection does not: the cost is paid once and retires a recurring manual step, where the objection bites recurring machinery built to police a one-time move. Contrast WI-391, handed back the same day: that row proposed navigation with no driving necessity, and this one has a live, reproduced defect. SCOPE: pick the surviving host (the close path `integrate.py` already owns is the candidate; the builder judges), restore the two rewriters and their two primitives with the discipline the originals carried - link text untouched, only the target redirected, `#fragment`s carried, external/protocol-relative/bare-anchor targets left alone, root-relative targets excused only in the rebase half, and line endings preserved via `newline=''` so a CRLF checkout is not silently relaid to LF (the WI-234/WI-337 lesson) - and restore the MUTATION-TWIN guard shape: archive a fixture carrying a link at each depth through the REAL function and assert the REAL check_docs passes, beside a twin that moves it WITHOUT the rebase and asserts check_docs FAILS, so the guard demonstrably reproduces the defect it fixes. Watch the same complexity ratchet WI-288 hit (C901 at 11) - split the per-link decision out rather than baselining it."
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

The ritual is rehomed as the new kit sibling
`project-trajectory/scripts/spec_move.py` (under the size-ratchet THRESHOLD;
the extraction escape, since `integrate.py` sits at its exact baseline as a
named decomposition target): `move_spec` performs move + outbound rebase
(`_rebase_moved_spec_links`) + inbound redirect (`_relink_inbound_links`, the
restored `_relink_archived_specs` generalised to any spec move) + staging as
ONE operation over the two restored primitives (`_resolvable_link`,
`_rewrite_md_links` with its pure `rewrite_text` core), with the original
discipline verbatim - link text untouched, `#fragment`s carried,
external/protocol-relative/bare-anchor targets left alone, root-relative
excused only in the rebase half, CRLF preserved via `newline=''`, and the
per-link decisions (`_redirected_link_target`/`_rebased_link_target`) split
out of the traversals per this spec's C901 warning. A CLI (`SRC DEST`, or
`--archive [--date]` for the dated `docs/archive/specs/` move) serves the
worker's by-hand close and archival moves.

Wired at every live move site, which the drain plan widened beyond this spec's
archival scope (claim owed too, driven 2026-08-01): `integrate.claim` replaces
its bare `git mv`, so the claim commit carries the relinks;
`handback.hand_back` returns specs through `move_spec(new_text=...)`; and
`integrate._abandoned_claim`'s content fact widens by ORACLE only
(`_relinked_exactly` against `spec_move.expected_relink` over the commit's own
move pair; `_claim_delta` is the C901 extraction) so a crashed relinked claim
still re-cuts while any other `.md` edit convicts.

Tests: `tests/test_spec_move.py` (16, smoke tier) restores the guard shape
including the MUTATION TWIN - the archived fixture passes the REAL
`check_docs` while the same move without the rebase fails it - plus claim
wiring and conviction both ways in `tests/test_integrate.py` and the return
ritual in `tests/test_handback.py`. Registration: kit README + bootstrap rows,
LLR-145 + TC-139 (CMP-004, under SR-132), dupes census (cli 86; `link-rebase`
class returns), size stamps (integrate 1890->1946 reviewed, bootstrap
2250->2257), arch map/gate/dashboard regenerated. Watched: full suite 1822
passed / 10 skipped (0:04:42); smoke 594/6; trace, check_trajectory and
check_doc_refs all rc=0 under --strict.
