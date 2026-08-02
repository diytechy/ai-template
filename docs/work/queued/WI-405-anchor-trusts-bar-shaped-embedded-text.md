+++
id = "WI-405"
title = "The refusal anchor trusts bar-shaped text embedded in step output (WI-398 REVIEW-A finding 1, minted trunk-side at intake per the R3 invariant). DRIVEN by the reviewer: three constructed shapes — a quoted FAIL row, a quoted mock banner, and a nested scaffold bar naming a different step, each printed INSIDE a step's own captured output — silently hijack _own_step_window onto a passing step's text; realistic here because failing tests print captured stub-bar stdout. THE REMEDY IS SCOPED SMALL, per the reviewer's own words and WI-398's scope guard (no parsing machinery, no log-management layer): a one-clause known-limit in _own_step_window's docstring naming the class and pointing at the kept full log (out/run-logs/refresh-refused-<branch>.log) as the backstop for the refresh path — plus, ONLY if it stays inside the existing shape, preferring the outermost banner when line-anchored matches nest (judge; do not build a parser). Tests: the reviewer's three shapes in docs/reviews/WI-398-REVIEW-A.md finding 1 are the fixture recipes — pin whichever behavior is chosen (documented limit or outermost-banner preference) so the choice is explicit, never folklore. Scope: agent_common.py docstring/one clause + tests; nothing else."
workstream = "scripts"
specref = "docs/reviews/WI-398-REVIEW-A.md"
buildtier = "quick"
safety_class = "ordinary"
+++
