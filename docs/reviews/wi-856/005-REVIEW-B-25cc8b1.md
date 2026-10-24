Reviewed: 25cc8b13309cd24381cdf12a676ea8f896408d3e

Verified. Checkout confirmed at 25cc8b13309cd24381cdf12a676ea8f896408d3e. Worst failure classes this change admits, hunted first: (1) silent wrong content, meaning an inserted `needs` that does not parse as the ROOT key, or a rewrite of the wrong line that the close then reports as written; (2) fail-open, meaning an unreadable frontmatter that is edged when it should be refused; (3) the rest of the waiter's spec not being preserved. What I drove through the shipped `consolidate.edged_text`, and what I found right:
- The insert arm puts `needs = ["<blocker>"]` directly after the opening fence. That position is always top-level TOML, so a frontmatter that ends in a `[table]` still gains a root `needs`. A leading comment, blank lines and an empty frontmatter all give a root key that parses.
- The insert arm is idempotent, and it keeps the opening fence line's own line ending (tested for LF and CRLF).
- On the real close path, `_enact_plan` and `_apply_plan` read the file with universal newlines and write it back LF. This matches what the RESYNC entry states.
- These are refused: a missing fence, an unterminated `needs = [`, a multi-line root list (when no table follows it), and a one-line `needs` carrying a trailing comment. That last input is outside the declared set and fails closed, so it is a coverage-extension note, not a finding.
- The extension arm now searches only the frontmatter. The old whole-text search could rewrite a body line reading `needs = [...]` when the frontmatter list was multi-line. That is a side improvement.

Convergence stance, red-before evidence: I extracted the trees at the trunk base 3b9f2b44f and at the pre-fix lane commit 79be877e3, which inserted just before the closing fence. Into each I overlaid the tip's tests/test_consolidate.py, plus tests/test_consolidate_close.py at the base.
- At 3b9f2b44f, three tests FAIL: `test_the_edge_write_inserts_a_missing_needs_line[lf]`, `[crlf]` and `test_the_inserted_needs_line_is_top_level_before_any_table` (3 failed, 4 passed). `test_queue_with_edge_gives_a_waiter_with_no_needs_line_one` FAILS as well.
- At 79be877e3, the same three tests FAIL (3 failed, 4 passed). That confirms the table-position fix is pinned.

Done-when coverage:
- (1a) Insert holding just the blocker, Context and Deliverable byte-identical: covered by `test_the_edge_write_inserts_a_missing_needs_line` (LF and CRLF) and the close test `test_queue_with_edge_gives_a_waiter_with_no_needs_line_one`.
- (1b) A `needs` row extended as before, idempotence included: covered by `test_the_edge_write_is_surgical_and_idempotent`, which now does a full byte comparison.
- (1c) An unreadable frontmatter is refused: covered by `test_the_edge_write_refuses_a_frontmatter_it_cannot_read` and `test_a_refused_edge_leaves_the_lane_tree_byte_identical`. The second test now rewrites WI-404 on the lane to an unparseable frontmatter.
- (2) The three named tests: covered as above.
- (3) LLR-210's detail and TC-208 (and TC-254, which also verifies LLR-210) state the insertion. LLR-210 and the TC rows at the tip are byte-identical to those at 793f65cc3: `git diff 793f65cc3 25cc8b133 -- docs/requirements docs/test` is empty. The lane carries an adjudication record keyed to that commit. Under the convergence stance I did not read its content.
- (4) RESYNC_PACK entry: present, anchored `[since 3b9f2b44f]` at the trunk base, in the house format.

Other checks:
- SR-220 and LLR-312 are unchanged, and neither contradicts the new behaviour.
- No interface row covers the consolidate/handback seam.
- No Status flipped. The approved LLR-210, TC-208 and TC-254 change only where the spec grants it (K3).
- The `[smoke-budget]` re-stamp to 3410 is arithmetically honest: 5 cases at the test commit and 6 at the tip, so 3282, which is under 3410.

Commands:
- `git rev-parse HEAD` -> 25cc8b13309cd24381cdf12a676ea8f896408d3e
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-24a-leg17/g/opus/wi-856 tests/test_consolidate.py tests/test_consolidate_close.py` -> 119 passed in 240.84s
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (970 work item(s), 858 done (88%), 34 cancelled, graph acyclic).
- base tree 3b9f2b44f + tip tests: `pytest tests/test_consolidate.py -k "edge_write or inserted_needs"` -> 3 failed, 4 passed
- base tree 3b9f2b44f + tip tests: `pytest tests/test_consolidate_close.py -k "no_needs_line_one or refused_edge"` -> 2 failed. The refused-edge failure is the expected refusal-text change; the no-needs close test fails because the base refuses.
- tree 79be877e3 + tip tests: `pytest tests/test_consolidate.py -k "edge_write or inserted_needs"` -> 3 failed, 4 passed
- direct probe of `consolidate.edged_text` and `kitlib.registry.parse_spec_frontmatter` on constructed frontmatters (results cited in the findings)

Findings:
- [MINOR] project-trajectory/scripts/consolidate.py:1452 -> K1. The extension arm finds the line to rewrite with `_NEEDS_RE` over the whole frontmatter and never confirms that the matched line is the ROOT `needs` the parse just read. Probe, a frontmatter `parse_spec_frontmatter` accepts: `needs = [\n  "WI-1",\n]` followed by `[x]\nneeds = ["a"]`. `edged_text(..., "WI-401")` returns text with `[x].needs = ["WI-1", "WI-401"]` and the root `needs` unchanged. The close would then report the edge written while no edge exists. This also contradicts the lane's own LLR-210 sentence that a spec "whose `needs` list is not on one line is refused". It is contrived: no spec under docs/work has a table in its frontmatter, so it is MINOR. -> the concrete change: accept a rewrite only when the rewritten frontmatter re-parses to the expected root `needs`, which is the parse-verified rule `intake._replace_needs_value` already owns. Better, lift that writer into one shared kitlib home that both call (§3 "Consolidate, don't duplicate"; intake imports consolidate, so a direct import would be circular). That single owning boundary makes a wrong-line rewrite unrepresentable rather than guarded, the `antidote` skill's smallest change that makes this fix unnecessary. -> @owner
- [MINOR] project-trajectory/scripts/handback.py:816 -> K1, for clarity. The refusal now reads "has no frontmatter the edge can read" (and at :849, "no longer has a frontmatter the edge can read"). It is also emitted for a waiter whose frontmatter parses but whose root `needs` list spans several lines, which is LLR-210's third refusal. project-trajectory/RESYNC_PACK.md:9776 likewise lists only the missing-fence and non-parsing cases. -> name the multi-line case in both refusal strings, for example "has no frontmatter, or no one-line `needs` list, the edge can read", and in the RESYNC entry's refusal sentence. -> @owner

VERDICT: CHANGES-REQUESTED findings=2
