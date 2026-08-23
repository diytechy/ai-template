+++
id = "WI-344"
title = "Extract check_trajectory.py's staged-close scan (docs/dupes-allow: staged-close-scan 4, spec-scan 1 = 5 sanctioned blocks). The 104-token block is the largest same-file duplication in the census: staged-name diff -> `show HEAD:<work-items.csv>` -> status map -> the newly-closed-WI comparison, run independently by the shared-SR follow-up guard and the critique-close guard, so the definition of \"closed in THIS commit\" lives in two places. The specs/*.md scan that skips README.md and the inert `-000` example states a policy twice the same way. Triaged under WI-340."
workstream = "scripts"
needs = ["WI-340"]
buildtier = "medium"
priority = 0
safety_class = "ordinary"
order = 341
+++

## Deliverable

DONE 2026-07-28, forced early by WI-352 and completed rather than left half-done. Adding a fourth copy of the staged-close preamble made check_dupes RED, and the standing rule (WI-343) is that the F5 sanction buys cross-SCRIPT copy-ability so it never covers a SAME-FILE copy: extract, do not sanction. All five sanctioned blocks are gone and their census entries REMOVED after proving each fingerprint is absent from the live census - a sanction whose block no longer exists is the stale-census drift WI-337 was about. _staged_wi_registry(root) returns (staged_names, cur_map, head_map) or None, folding the three no-op cases (no git context, no registry change staged, no HEAD copy) into one answer so a caller degrades silently off-git without restating the reason; _newly_closed() states the queued->done transition all three close-time ratchets key off; _chain_untouched() states the shared tail - a close that touches neither the TC registry nor the tests dir landed the fix in the code and not in what judges it - with *extra_dirs for the one way the two sites differed (the critique ratchet also accepts a rubric anchor), so the shared rule lives once and the difference stays visible at the call. _armed_specs(root) states the which-files-are-real-specs POLICY (skip README, skip the inert -000 example) that both spec walks had spelled out. Net effect beyond the census: critique_ratchet_findings (C901 11) and staged_findings (12) both dropped BELOW the limit and were DELETED from the complexity baseline rather than bumped - the direction that ratchet exists to hold. Bar shared with WI-352's commit: check_dupes OK, no duplicate blocks in 37 files.
