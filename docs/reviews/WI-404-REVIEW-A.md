# WI-404 — REVIEW-A (2026-08-02)

Verdict: APPROVE — I re-drove both reviewer fixtures red-then-green, ran a
23-case grammar-edge battery against the new `PLACEHOLDER_VALUE` fullmatch
(every defective shape flags loudly, every convention-prose shape stays
exempt), enumerated the live exempt population by hand, re-ran every
registered bar, and took the disclosed ratified-cell adjudication myself.
Two bounded residuals are recorded below; neither blocks. **This APPROVE
explicitly carries the adjudication judgment for the LLR-146 `Detail` and
TC-140 `Method` amendments — scope-not-moved** (the act is in full under
"Adjudication act").

Reviewed: branch `wi-404-placeholder-proxy-over-approximates` at `9cd6bb44`
(work `02331e1f` + close), trunk `ConcurrencyTrainRewrite` = `90aefbb8` (the
claim commit; the branch is exactly the two reviewed commits). All commands
run under `/Users/diytechy/Documents/ai-template/.venv/bin/python` from the
worktree; historical trees driven via detached temp worktrees. Per the brief,
`docs/log.d/` fragments were not read — the fragment's markers are counted
below only through `check_figures` itself.

## What I verified before hunting

**Watched red, reproduced.** Temp worktree at `90aefbb8` (old
`PLACEHOLDER_CHARS` proxy) with the branch's own `tests/test_check_figures.py`
copied in:

```
2 failed, 19 passed in 2.48s
E  AssertionError: check_figures: OK - no declared figures (the fig: marker
   is opt-in; unmarked figures are out of scope by design).
```

— both new fixtures fail in exactly the convicted silent direction ("OK - no
declared figures" both ways). On the branch: `21 passed in 1.16s`.

**Both reviewer fixtures, re-driven through `judge_marker` directly:**

```
reviewer fixture 1 (defective piped)   -> FLAGS: carries cmd= but no rev= —
                                          a figure is evidence only at the
                                          revision it was driven on
reviewer fixture 2 (redirecting)       -> COUNTS (complete declaration)
```

— the WI-392 REVIEW-A round-2 finding 4 fixtures verbatim (`cmd="pytest -q
2>&1 | tail -1"` rev-missing FLAGS; `cmd="sort < in.txt | wc -l" rev=abc123`
COUNTS), each also pinned end-to-end by the two new tests.

**Census, three ways.** Pre-close tree (`02331e1f`): **28 declared, rc=0**.
Claim tree under the OLD proxy (`90aefbb8`): **28 declared, rc=0** — the
narrowing changed zero live classifications, exactly as claimed. Close tree
(`9cd6bb44`): **40 declared, rc=0**, and I enumerated the composition:
28 prior + 6 markers in the WI-404 Deliverable + 6 in the (unread, counted
only) `docs/log.d/` fragment = 40. The grammar-exempt population is exactly
three lines — `docs/enforcement-audit.md:58` (`` `fig: cmd="…" rev=…` ``),
`docs/work/complete/WI-392-driven-figures-carry-their-command.md:18`
(`` fig: cmd="<command>" rev=<revision> ``) and `:20`
(`` fig: derived="<how, from which declared figures>" ``) — every one a
whole-token shape; **no live line depends on any looser reading**.

**The scaffold-tier test and prose exemptions.** Both in the green 21:
`test_a_fresh_scaffold_passes_its_own_docstring_opt_in` bootstraps a fresh
scaffold (whose `docs/process-options.md` now carries the amended Grammar
sentence) and passes `--strict`; `test_a_placeholder_grammar_example_
declares_nothing` drives all three convention shapes including the bare
`rev=<revision>` whose capture arrives unclosed (`<revision` — the REV
bare form excludes `>` and stops there), the case the unclosed
`<[^<>\s]*` alternative exists for. I confirmed that motivating shape on the
two live lines above.

## Grammar-edge battery (hunt 1)

23 cases driven through `marker_segments` + `judge_marker` on the branch;
the load-bearing rows:

```
token+trailing, rev ok                 -> COUNTS (complete declaration)
token+trailing, rev MISSING            -> FLAGS: ... no rev=
two tokens <a> <b>, rev MISSING        -> FLAGS: ... no rev=
empty cmd, no rev                      -> FLAGS: carries neither cmd="…" rev=… nor derived="…"
empty cmd, real rev                    -> FLAGS: ... no cmd=
whitespace-only cmd, real rev          -> FLAGS: ... no cmd=
convention line (part 1)               -> GRAMMAR (excused, uncounted)
convention line (derived)              -> GRAMMAR (excused, uncounted)
unclosed with space <a b, rev MISSING  -> FLAGS: ... no rev=
genuine redirect-first <in.txt wc -l   -> COUNTS (complete declaration)
embedded ellipsis, rev MISSING         -> FLAGS: ... no rev=
whitespace-free <in.txt cmd, real rev  -> GRAMMAR (excused, uncounted)   [finding 2]
MIXED: real cmd, placeholder rev       -> GRAMMAR (excused, uncounted)   [finding 1]
MIXED: placeholder cmd, real rev       -> GRAMMAR (excused, uncounted)   [finding 1]
```

Every value that is exactly a token plus trailing text, every multi-token
value, every empty/whitespace value and every unclosed-with-whitespace value
is judged as a real marker — the defective variants all flag **loudly**,
which is the honest direction on a warn-first step. The convention's own
shapes (closed token, spaced token like `<how, from which declared
figures>`, bare ellipsis, and the bare-capture unclosed token) all stay
exempt. The two residual excusals are findings 1 and 2.

## Adjudication act (hunt 3)

`staged_spine_amendments(".", "90aefbb8", "9cd6bb44")` returns **exactly two
records**: `docs/requirements/low-level-requirements.csv` LLR-146 with one
**ratified**-half cell (`Detail`) and `docs/test/test-cases.csv` TC-140 with
one **ratified**-half cell (`Method`). No SR-136 record, no traced-half
changes, no Status moves anywhere on the spine — the disclosed set, exactly.
The amend-without-flip warn is live for this shape (both records carry
ratified cells, so `staged_spine_findings` fires on them at the work commit,
as the Deliverable discloses).

**This APPROVE is the adjudication act.** Under `docs/gate-policy`
`autonomous`, a recorded independent reviewer verdict carries the
adjudication-class judgment below G-Final (the WI-402 precedent shape).
**The no-flip amendment of LLR-146 `Detail` and TC-140 `Method` at
`02331e1f` is hereby adjudicated as scope-not-moved.** Grounds, from the diff
and the record, not the lane's say-so:

- The attestation unit is the SR, and SR-136's row is byte-untouched. Its
  AcceptanceCriteria already name the class: "unmarked figure prose,
  **placeholder-grammar examples**, fig-ok lines, GENERATED blocks and
  docs/reviews/ records are ignored" — and the ratifying reviewer construed
  that class narrowly *in the same verdict that ratified it* (WI-392
  REVIEW-A round 2, finding 4: "The ratified class is 'placeholder-grammar
  examples' / 'placeholder-shaped (`<command>`, `…`)' — a real shell-redirect
  command is neither, so the implementation ignores markers the ratified text
  does not say it ignores"). The amendment conforms the implementation and
  its detail cells **to** the already-ratified reading — the truth-restoration
  shape, not a scope move.
- The amended cells are the traced-description halves of child rows: LLR-146
  `Detail` now states the whole-token rule the code ships, TC-140 `Method`
  adds the two new behaviors 1:1 with the two new tests. I re-verified both
  cells against my own runs (battery above, 21-green suite, census three
  ways).
- Flipping SR-136 to Modified would open a re-attest window for a
  requirement whose text did not change — the spurious-window shape the
  WI-402 act declined for the same reason.

Had the class actually moved — had SR-136's AC blessed the old any-char
reading — this would have been a MAJOR and a round. It did not: the old
implementation was the deviation, convicted as such by the ratifying
reviewer, and this WI closes it.

## Mechanical (hunt 4)

- `tests/test_check_figures.py`: **21 passed in 1.16s** (claimed 21). Red
  form reproduced as quoted above.
- Smoke, close tree: **622 passed, 2 skipped in 10.01s** (claimed 622/2;
  re-run with `-rs`: the 2 are the Windows-only job-object tests). Smoke,
  work tree: **618 passed, 6 skipped** — the Deliverable's 618/6 figure also
  reproduces exactly; the 4-test delta between the two trees is claim-state
  conditional skips, present before this WI, consistent totals (624 both).
- Full suite, close tree: **1881 passed, 6 skipped in 0:04:47** (total 1887 =
  the Deliverable's 1877+10 at the work commit, same 4-skip shift); full
  suite, work tree: **1877 passed, 10 skipped in 291.93s (0:04:51)** — the
  Deliverable figure verbatim.
- `check_figures --root . --strict` rc=0 (40 declared);
  `check_trajectory --strict` rc=0; `check_doc_refs --strict` rc=0;
  `ruff check .` and `ruff format --check .` clean. No WI-404-shaped warn on
  the non-strict trajectory surface (remaining SpecRef warns name
  WI-389/WI-390 — pre-existing).
- Byte re-stamp: `wc -c project-trajectory/PROCESS_OPTIONS.md` = **169,125**
  on the branch and **169,010** at `90aefbb8` (+115 exactly). All **three**
  tracked byte-budget-guard copies (`.agents/`, `.claude/`,
  `project-trajectory/skills/`) re-stamp "baseline **169,125** as of
  2026-08-02/WI-404 (+115 on the 169,010 stamp: the 'Signed measurements'
  *Grammar* sentence narrowed to whole-token placeholders …)" — delta,
  reason, and history chain intact in each.
- R-A: the Deliverable is dated (2026-08-02, work `02331e1f`) and every
  declared figure in it reproduced under my own runs (the six `fig:` markers:
  byte count, red 2f/19p, 21 passed, 28-census strict, 1877/10 full, 618/6
  smoke). R-F: the complete spec carries no `specref`; nothing archived;
  no WI-404 SpecRef warn.
- `docs/work` delta over `90aefbb8..9cd6bb44` is WI-404-only: one D
  (active spec) + one A (complete spec). Only historical mentions of
  `PLACEHOLDER_CHARS` remain (spec title/Deliverable — appropriate).

## Findings (severity-ordered)

**1. MINOR (recorded, non-blocking; follow-up owed) — a MIXED marker (one
real value beside one wholly-placeholder value) is still excused wholesale,
and the amended Grammar sentence does not state that semantics.** Driven:

```
<!-- fig: cmd="wc -c README.md" rev=<revision> -->  -> GRAMMAR (excused, uncounted)
<!-- fig: cmd="<command>" rev=abc1234 -->           -> GRAMMAR (excused, uncounted)
```

`judge_marker` excuses the whole marker when **any** value fullmatches
`PLACEHOLDER_VALUE` (`if any(PLACEHOLDER_VALUE.fullmatch(v.strip()) for v in
values)`), so a half-filled template — a real command typed, `rev=<revision>`
left unfilled — escapes both census and flagging: the same silent direction
as the parent finding, though strictly narrower (it now requires a visibly
unfilled `<token>` field beside the real value, where the old proxy excused
any metacharacter anywhere). The shipped convention sentence — the one home
this WI added so the proxy is "documented, not folklore" — reads
**all-values**: "a marker **whose values are wholly placeholder tokens**
(`<command>`, `…`) is the convention quoting itself"; the code implements
**any-value**. (LLR-146 `Detail` and the `judge_marker` docstring do state
the any-value rule — "a value that is wholly a placeholder token … makes the
marker grammar prose" — so the registry is honest; the convention sentence
and the module-docstring grammar bullet are the two homes that underspecify
it.) Bounded: zero live hits (the exempt population is the three
all-placeholder lines enumerated above), warn-first step, and the naive fix
is a trap — under judged-not-excused semantics `rev=<revision` carries word
characters and would *satisfy* `has_rev`, silently passing the half-filled
template as complete, which is worse. Follow-up owed: either state the
any-value excusal in the Grammar sentence, or judge mixed markers with a
placeholder value counting as *missing* — not as a revision.

**2. NOTE (recorded, no remedy owed) — the unclosed-token alternative
reaches quoted values its motivation does not cover.** `<[^<>\s]*` exists
because the *bare* `rev=` capture stops before `>` (driven on the live
convention lines), but it applies per-value everywhere, so a **quoted** cmd
whose whole value is a whitespace-free `<`-leading token is excused even
beside a full rev:

```
<!-- fig: cmd="<in.txt" rev=abc123 -->  -> GRAMMAR (excused, uncounted)
<!-- fig: cmd="<" rev=abc123 -->        -> GRAMMAR (excused, uncounted)
```

Silent-uncount direction, but bounded well below finding 1: no runnable
command is a single whitespace-free `<`-leading token, and the realistic
redirect-first shape counts correctly (`cmd="<in.txt wc -l" rev=abc123 ->
COUNTS`, driven). Recorded so the boundary is written down.

**3. NOTE (recorded, no remedy owed) — multi-token and token-plus-text
values are judged real, so hypothetical convention prose of that shape would
flag, loudly.** `cmd="<a> <b>"` and `cmd="<command> --strict"` fullmatch
nothing (the closed alternative forbids inner `<`/`>`; the unclosed one
forbids whitespace) and are judged as real markers. No live prose has such a
shape — the convention's own lines put each token in its own attribute — and
the failure direction is a loud false positive at authoring time, not
silence, which is the correct side of the WI-404 trade. Recorded for the
next prose author.

## Verdict

Both reviewer fixtures are driven both ways, the narrowing is exactly the
ratified whole-token class with zero live reclassification, every mechanical
claim in the Deliverable reproduced under my own runs, and the disclosed
LLR-146/TC-140 no-flip amendments are adjudicated scope-not-moved by this
verdict. The two residuals are recorded above in the bounded-gap idiom the
parent finding itself used.

VERDICT: APPROVE findings=3
