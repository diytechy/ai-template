+++
id = "WI-404"
title = "check_figures' placeholder proxy over-approximates (WI-392 REVIEW-A round-2 finding 4, minted trunk-side at intake per the R3 invariant). DRIVEN by the reviewer at f5a423ae: a DEFECTIVE marker whose cmd contains shell metacharacters — cmd of pytest -q piped to tail with rev MISSING — escapes both the census and the flagging because PLACEHOLDER_CHARS treats the angle bracket/pipe as example-grammar; and a REAL declaration whose command legitimately redirects (sort < in.txt) is silently uncounted. Both errors point the SILENT direction on a warn-first step, and zero live declarations hit the class today — which is why the finding rode the APPROVE as a bounded recorded gap (the enforcement-audit idiom) instead of a third round. THE FIX SHAPE: narrow the placeholder proxy so it excuses only genuine example grammar (the angle-bracket-wrapped whole-token placeholder shape the convention text uses) rather than any metacharacter anywhere; a metacharacter inside a quoted cmd value is legitimate command text and the marker must still be judged complete (cmd AND rev both carried). State the rule in the convention text (PROCESS_OPTIONS.md Signed measurements Grammar sentence) so the proxy is documented, not folklore. Tests: the reviewer's two fixtures both ways — the defective piped-cmd marker with missing rev must FLAG, the legitimate redirecting declaration must COUNT — plus the existing placeholder-prose exemptions staying exempt (the scaffold-tier test from f5a423ae must stay green). Scope: check_figures.py + its tests + the one Grammar sentence; no new rungs, rung 2 stays a declared absence."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

Shipped 2026-08-02, work commit 02331e1f. The proxy is narrowed to the rule
the reviewer ratified: a marker value is placeholder-shaped only when the
WHOLE value is the convention's own example grammar — an angle-bracket-wrapped
token (`<command>`; the bare rev= capture stops before the closing bracket, so
a whitespace-free token may arrive unclosed) or the bare ellipsis
(`PLACEHOLDER_VALUE`, a fullmatch per attribute value, replacing the any-char
`PLACEHOLDER_CHARS`). A metacharacter inside a longer value is command text
and the marker is judged on its attributes: the reviewer's defective
piped-cmd fixture (a cmd of `pytest -q 2>&1 | tail -1` with rev absent) now
FLAGS its missing rev=, and the legitimate redirecting declaration (a cmd of
`sort < in.txt | wc -l` with a full rev) now COUNTS. The rule is stated where
the convention lives — the PROCESS_OPTIONS.md "Signed measurements" *Grammar*
sentence, +115 bytes (169,010 → 169,125
<!-- fig: cmd="wc -c project-trajectory/PROCESS_OPTIONS.md" rev=02331e1f -->),
re-stamped with reason in all three byte-budget-guard copies — and in the
module docstring and judge_marker, no longer folklore.

Watched red first on the claim tree: the two new reviewer-fixture tests
failed exactly as convicted, 2 failed / 19 passed, "OK - no declared figures"
in both silent directions
<!-- fig: cmd="python -m pytest -q tests/test_check_figures.py" rev="90aefbb8 with the two new fixture tests staged, pre-fix" -->;
green after: 21 passed
<!-- fig: cmd="python -m pytest -q tests/test_check_figures.py" rev=02331e1f -->,
the scaffold-tier end-to-end test and every placeholder-prose exemption
staying green, live census unchanged at 28 declared rc=0
<!-- fig: cmd="python project-trajectory/scripts/check_figures.py --root . --strict" rev=02331e1f -->.
Full suite 1877 passed / 10 skipped in 0:04:38
<!-- fig: cmd="python -m pytest -q -n auto" rev=02331e1f -->;
smoke 618 passed / 6 skipped in 11.83s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=02331e1f -->.

DISCLOSED for the verdict round's adjudication (ratified-cell amendments, the
WI-392-rework/WI-402 precedent, no Modified flip — the requirement did not
move and SR-136's AcceptanceCriteria already name the narrow class): LLR-146
Detail now defines placeholder-shaped as the whole-token rule; TC-140 Method
adds the two new behaviors 1:1 with the new tests; SR-136 untouched. The
staged-spine amend-without-flip warn fired at the work commit as designed;
this disclosure is its answer. Full session record: the WI-404 entry in
docs/log.md (compiled from this branch's fragment).
