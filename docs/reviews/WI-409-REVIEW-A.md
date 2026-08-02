# WI-409 — REVIEW-A (2026-08-02)

Verdict: APPROVE — I convicted the reviewer's named trap myself by
counterfactual (a naive all-values flip WITHOUT the placeholder-counts-as-
absent rule certifies the mixed fixture as a complete declaration), ran a
19-case grammar-edge battery shipped-vs-naive, proved zero live
reclassification at per-line granularity, re-ran every registered bar in my
tier, and took the disclosed ratified-cell adjudication myself. Two bounded
notes are recorded below; neither blocks. **This APPROVE explicitly carries
the adjudication judgment for the LLR-146 `Detail` and TC-140 `Method`
amendments — scope-not-moved** (the act is in full under "Adjudication act").

Reviewed: branch `wi-409-mixed-marker-any-value-excusal` at `be3f8f36`
(work `9895a654` + close), trunk `ConcurrencyTrainRewrite`; claim commit
`f67d6c70` is the branch base state. All commands run under
`/Users/diytechy/Documents/ai-template/.venv/bin/python` from the worktree;
historical trees driven via detached temp worktrees. Per the brief,
`docs/log.d/` fragments were not read — the fragment's markers are counted
below only as a `grep -c` total and through `check_figures` itself. The full
unfiltered suite is outside this review's tier and was not re-driven; the
Deliverable's 1891/10 figure is taken as the builder's watched claim.

## Hunt 1 — the trap, convicted by counterfactual

I hacked a scratch copy of the branch's `check_figures.py` that KEEPS the
all-values excusal (`values and all(_placeholder(v) for v in values)`)
but REMOVES the absent rule — `has_cmd`/`has_rev`/`derived` restored to
their pre-WI-409 forms (`has_rev = bool(rev_val and WORD.search(rev_val))`
etc.). Driven through `judge_marker`:

```
mixed: real cmd, placeholder rev (cmd="wc -c README.md" rev=<revision>)
  shipped    -> FLAGS: carries cmd= but no rev= — a figure is evidence only at the revision …
  naive flip -> COMPLETE (counts, silent-pass)
mixed: placeholder cmd, real rev (cmd="<command>" rev=abc1234)
  shipped    -> FLAGS: carries rev= but no cmd= — name the command that produced it
  naive flip -> COMPLETE (counts, silent-pass)
```

The mechanism is exactly the one the WI-404 reviewer named: the bare `rev=`
capture (`[^\s>\"'`]+`) stops before `>`, so `rev=<revision>` arrives as the
unclosed `<revision`, whose word characters satisfy `WORD.search` — and the
naive flip is silently wrong in BOTH directions (any non-empty `<command>`
satisfies the naive `has_cmd` too). End-to-end, on a temp worktree at the
close tree with the naive-flip module swapped in, the branch's own two new
tests fail with:

```
check_figures: OK - 1 declared figure(s), every one carrying its command and revision (or derivation).
2 failed, 21 passed
```

— the naive flip doesn't just stay silent, it CERTIFIES the half-filled
template as carrying full provenance. The same assertions on the pre-fix
tree (`f67d6c70` + the branch's tests copied in) fail as:

```
E  AssertionError: check_figures: OK - no declared figures (the fig: marker
   is opt-in; unmarked figures are out of scope by design).
2 failed, 21 passed in 1.65s
```

— the Deliverable's watched red, reproduced verbatim (2 failed / 21 passed,
"OK - no declared figures" in both silent directions). One assertion set
convicts the old excusal AND the naive flip; the shipped rule dodges both.
The trap was real.

## Hunt 2 — grammar edges and census

19-case battery through the shipped `judge_marker` (shipped vs naive-flip
side by side; full table driven, extract here):

```
bare fig: (no attributes)                -> FLAGS: carries neither cmd="…" rev=… nor derived="…"
all-placeholder 2-attr (convention line) -> GRAMMAR          (quoted-rev and derived= forms too)
bare ellipsis cmd="…"                    -> GRAMMAR
mixed both directions [finding 1]        -> FLAGS the absent half (each way, quoted above)
note-2 named: cmd="<in.txt" rev=abc123   -> FLAGS: carries rev= but no cmd=
residual: lone cmd="<in.txt"             -> GRAMMAR (excused)  [see finding 1]
WI-404: sort < in.txt + full rev         -> COMPLETE   (kept)
WI-404: piped cmd, rev missing           -> FLAGS no rev= (kept)
WI-404: cmd="<a> <b>", cmd="<command> --strict" -> judged real (kept)
flush rev=--> (wordless)                 -> FLAGS no rev= (kept)
empty cmd beside placeholder rev         -> FLAGS (louder than old: any-value would have excused it)
mixed: placeholder derived + real rev    -> FLAGS no cmd= (naive flip: COMPLETE — a fourth silent arm)
```

The `values and` guard holds (bare marker flags), every convention-prose
shape stays exempt, every WI-404 fixture keeps its classification, and the
note-2 named shape now flags via the mixed rule itself, exactly as the
Deliverable claims.

**Census, three ways, plus a per-line diff.** Claim tree `f67d6c70` under
its own OLD code: **45 declared, rc=0**. The NEW code over the same claim
tree: **45 declared, rc=0**. I then dumped every marker judgment
(file:line:classification) under both codes over the claim tree: **48
judgments each (45 complete + 3 grammar), per-line diff NONE — identical**.
The grammar-exempt population is exactly the three all-placeholder lines
(`docs/enforcement-audit.md:58`, `WI-392-…md:18`, `:20`) — zero live
reclassification, at line granularity, not just totals. Close tree
(`be3f8f36`): **57 declared, rc=0**, and the arithmetic closes: 45 + 6
markers in the WI-409 Deliverable (grepped) + 6 in the unread `docs/log.d/`
fragment (`grep -c` count only) = 57.

## Adjudication act (hunt 3)

`staged_spine_amendments(".", "f67d6c70", "be3f8f36")` returns **exactly
two records**: `docs/requirements/low-level-requirements.csv` LLR-146 with
one **ratified**-half cell (`Detail`) and `docs/test/test-cases.csv` TC-140
with one **ratified**-half cell (`Method`). No traced-half changes, no
SR-136 record (`git diff f67d6c70..be3f8f36 -- system-requirements.csv` is
**0 lines**), and both rows read `Verified` on both sides of the raw CSV
diff — no Status flip anywhere on the spine. The disclosed set, exactly.
The amend-without-flip warn's arming condition (`staged_spine_findings`
fires per amendment carrying ratified cells; index-vs-HEAD at the staged
moment) is satisfied by both records — consistent with the Deliverable's
"the warn fired at the work commit as designed; this disclosure is its
answer".

**This APPROVE is the adjudication act.** Under `docs/gate-policy`
`autonomous`, a recorded independent reviewer verdict carries the
adjudication-class judgment below G-Final (the WI-402/WI-404 precedent
shape). **The no-flip amendment of LLR-146 `Detail` and TC-140 `Method` at
`9895a654` is hereby adjudicated as scope-not-moved.** Grounds, from the
diff and my own runs, not the lane's say-so:

- The attestation unit is the SR, and SR-136's row is byte-untouched. Its
  AcceptanceCriteria already name the class ("unmarked figure prose,
  **placeholder-grammar examples**, fig-ok lines, GENERATED blocks and
  docs/reviews/ records are ignored"), and the ratified Grammar sentence
  that defines that class reads all-values — a construal the ratifying
  reviewer put on record in the very finding this WI closes (WI-404
  REVIEW-A finding 1: "The shipped convention sentence … reads
  **all-values** … the code implements **any-value**"). The amendment
  conforms the child detail cells and the code **to** the already-ratified
  reading — the truth-restoration shape, not a scope move.
- The amended cells are the traced-description halves of child rows:
  LLR-146 `Detail` now states the all-values excusal and the
  placeholder-counts-as-absent judgment ("in a judged marker a
  placeholder-shaped value counts as absent, never as satisfying (an
  unfilled rev=<revision> names no revision)") — verified 1:1 against my
  battery; TC-140 `Method` adds "a mixed marker … flagging the missing half
  both ways" — verified 1:1 against the two new tests.
- Flipping SR-136 to Modified would open a re-attest window for a
  requirement whose text did not change — the spurious-window shape both
  prior acts declined for the same reason.

## The PROCESS_OPTIONS non-edit (hunt 4)

Byte-identical everywhere: `git rev-parse <rev>:project-trajectory/
PROCESS_OPTIONS.md` returns one blob SHA (`dac1684d…`) at `f67d6c70`,
`9895a654`, `be3f8f36`, trunk `ConcurrencyTrainRewrite`, and the working
tree; **169,125 bytes** — no edit, no re-stamp owed, correctly. I read the
ratified sentence (line ~1361): "*Grammar:* a marker **whose values are
wholly placeholder tokens** (`<command>`, `…`) is the convention quoting
itself and declares nothing". The bare-plural predication is universal on
its plain reading (a marker "whose values are placeholder tokens" = all of
them; "wholly" does the per-value whole-token work from WI-404), and the
ratifying reviewer's own construal in the parent finding reads it the same
way. The code moved to the sentence's plain, ratified reading; **no
clarifying word is owed**. Residual recorded as finding 2.

## Mechanical (hunt 5)

- `tests/test_check_figures.py`: **23 passed in 1.23s** on the close tree
  and **23 passed in 1.24s** on the work-commit tree (claimed 23). Red form
  reproduced as quoted above (2 failed / 21 passed).
- Smoke, close tree: **629 passed, 2 skipped in 10.41s** (claimed 629/2 in
  10.42s). The work-tree 625/6 figure is the same 631-total under
  claim-state conditional skips — the WI-404-review-verified shape.
- `check_figures --root . --strict` rc=0 (57 declared);
  `check_trajectory --strict` rc=0 (remaining warns pre-existing:
  connectivity/IF rows and the WI-389/WI-390 SpecRef pair — none name
  WI-409); `check_doc_refs --strict` rc=0; `derive_gate --check` rc=0
  (docs/gate up to date, G3); `ruff check .` and `ruff format --check .`
  clean (152 files).
- Census at the work commit: **45 declared, rc=0** — the Deliverable's
  figure, reproduced on its own tree.
- R-A: the Deliverable is dated (2026-08-02, work `9895a654`) and five of
  its six declared figures reproduced under my own runs (red 2f/21p, 23
  passed, 45-census strict, smoke 629/2, wc -c 169,125); the full-suite
  1891/10 figure is outside my tier, not re-driven. R-F: the complete spec
  carries no `specref` (grep rc=1); no WI-409 SpecRef warn on the
  trajectory surface.
- `docs/work` delta over `f67d6c70^..be3f8f36` is WI-409-only: one D
  (queued spec) + one A (complete spec). Outside docs/work + docs/log.d the
  range touches only the five named product files plus `docs/gate`'s as-of
  comment line (`fc3c74da` -> `4e47d4cb`, basis line unchanged, G3) — the
  claim commit's designed regen, not product change.

## Findings (severity-ordered)

**1. NOTE (recorded, no remedy owed) — the lone-all-placeholder
unclosed-token residual stands, and the docstring records it honestly.**
Driven: `cmd="<in.txt"` alone -> GRAMMAR (excused, uncounted), while the
parent shape `cmd="<in.txt" rev=abc123` — WI-404 REVIEW-A note 2's named
fixture — now FLAGS "no cmd=" via the mixed rule. The module docstring's
"Recorded corner" bullet states exactly this boundary ("a marker ALL of
whose values are whitespace-free `<`-leading tokens (a lone `cmd="<in.txt"`)
is excused — no runnable command has that shape"). The rider's one-line arm
was taken as specified; the unclosed alternative was not re-bounded, and the
residual is bounded well below the parent finding (silent-uncount only for
a shape no runnable command has; the realistic redirect-first
`cmd="<in.txt wc -l" rev=abc123` COUNTS, driven).

**2. NOTE (recorded, no remedy owed) — the ratified Grammar sentence states
the excusal class (all-values) but not the judged-marker completeness
semantics.** The placeholder-counts-as-absent rule lives in LLR-146
`Detail`, the module docstring, and the two tests — not in the
byte-budgeted sentence, whose plain universal reading ("whose values are
wholly placeholder tokens") the code now implements. A reader could stretch
"wholly" to per-value-only and try an existential reading of "values", but
that reading is strained, contradicts the ratifying reviewer's on-record
construal, and would cost budgeted bytes to foreclose. Recorded so the next
editor knows the sentence defines the CLASS and the registries define the
JUDGMENT; no clarifying word owed today.

## Verdict

The trap conviction is mine, driven by counterfactual in both directions
and end-to-end through the branch's own assertions; the grammar edges hold
with zero live reclassification at per-line granularity and honest census
arithmetic (45 + 6 + 6 = 57); the disclosed LLR-146/TC-140 no-flip
amendments are adjudicated scope-not-moved by this verdict; the
PROCESS_OPTIONS non-edit is byte-verified and the right call; every
mechanical bar in my tier reproduced. Two notes recorded above in the
bounded-gap idiom.

VERDICT: APPROVE findings=2
