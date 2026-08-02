## 2026-08-02 — WI-404: the figure placeholder proxy narrowed to whole-token grammar

**Summary.** WI-392 REVIEW-A round-2 finding 4 (the recorded bounded gap that
rode the APPROVE): `check_figures`' placeholder proxy treated ANY `<`, `>` or
`…` anywhere in a marker value as example grammar, so a DEFECTIVE marker
whose cmd embeds shell metacharacters (a cmd of `pytest -q 2>&1 | tail -1`
with rev absent) escaped both census and flagging, and a REAL redirecting
declaration (a cmd of `sort < in.txt | wc -l` with a full rev) was silently
uncounted — both errors the silent direction on a warn-first step. The proxy
now excuses only genuine example grammar: a value is placeholder-shaped only
when the WHOLE value is an angle-bracket-wrapped token (`<command>`; the bare
rev= capture stops before the closing bracket, so a whitespace-free token may
arrive unclosed) or the bare ellipsis — `PLACEHOLDER_VALUE`, a fullmatch per
attribute value, replacing the any-char `PLACEHOLDER_CHARS`. A metacharacter
inside a longer value is command text and the marker is judged on its own
attributes.

**Deliverables.**

- `project-trajectory/scripts/check_figures.py`: `PLACEHOLDER_VALUE` replaces
  `PLACEHOLDER_CHARS`; the docstring grammar bullet and `judge_marker` state
  the whole-token rule and the command-text consequence.
- The convention home: the PROCESS_OPTIONS.md "Signed measurements" *Grammar*
  sentence now states the rule where the convention lives (documented, not
  folklore), with the `sort < in.txt` command-text example.
- `tests/test_check_figures.py`: the reviewer's two fixtures both ways — the
  defective piped-cmd marker FLAGS its missing rev= (strict rc=1), the
  legitimate redirecting declaration COUNTS (strict rc=0, 1 declared); the
  placeholder-prose exemptions and the scaffold-tier end-to-end test stay
  green untouched.

**Judgment calls / deviations.** (1) Registration judged internal to
SR-136/LLR-146/TC-140 — no new rows: the round-2 reviewer ratified the narrow
class in the requirement text and convicted only the implementation. LLR-146
`Detail` and TC-140 `Method` amended to the built truth, DISCLOSED for the
verdict round's adjudication (the WI-392-rework/WI-402 precedent; no
`Modified` flip — the requirement did not move, SR-136 untouched). The
staged-spine amend-without-flip warn fired at the work commit as designed;
the disclosure in the work-commit body and the Deliverable is its answer.
(2) The provenance rule convicted WI-404 tokens in the first draft of the
amended cells; reworded — a spine row states the system, not its history
(the exact WI-402 lesson, relearned verbatim). (3) `docs/status.md` line 173
still names WI-404 in its queue listing — a worker branch never edits
status.md; the trunk-lane scrub at integrate owns it (the forward-only sharp
edge).

**Byte deltas:** AGENTS.template.md 9,991 and PROCESS.md 64,460 both
untouched; PROCESS_OPTIONS.md 169,010 → 169,125
<!-- fig: cmd="wc -c project-trajectory/PROCESS_OPTIONS.md" rev=02331e1f -->
(+115: the *Grammar* sentence's whole-token narrowing with its
command-text-vs-grammar example), baseline re-stamped with reason in all
three tracked byte-budget-guard skill copies in the work commit.

**Watched, measured on the work commit 02331e1f (clean tree):** red first —
2 failed / 19 passed on the claim tree, both fixtures erring silent exactly
as convicted
<!-- fig: cmd="python -m pytest -q tests/test_check_figures.py" rev="90aefbb8 with the two new fixture tests staged, pre-fix" -->;
then green — 21 passed in 1.15s
<!-- fig: cmd="python -m pytest -q tests/test_check_figures.py" rev=02331e1f -->.
Smoke 618 passed / 6 skipped in 11.83s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=02331e1f -->;
full suite 1877 passed / 10 skipped in 0:04:38
<!-- fig: cmd="python -m pytest -q -n auto" rev=02331e1f -->;
live census unchanged at 28 declared, rc=0 — the three genuine grammar-prose
lines stay exempt under the narrowed rule
<!-- fig: cmd="python project-trajectory/scripts/check_figures.py --root . --strict" rev=02331e1f -->;
`check_trajectory` / `check_doc_refs` `--strict` rc=0, the trace G3 bar
(`--strict --no-placeholders --require-verified --strict-schema`) rc=0,
`derive_gate --check` rc=0; `check_docs --stale` stays at the pre-existing
trunk red of 4 broken links (the same WI-070/WI-173/WI-288 record lines,
none added by this branch).
