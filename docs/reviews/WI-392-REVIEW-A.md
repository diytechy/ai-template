# WI-392 — REVIEW-A (independent)

### REVIEWER — G3 — Round 1 — 2026-08-01

Reviewed at `cab612c3` (branch `wi-392-driven-figures-carry-their-command`;
trunk = `ConcurrencyTrainRewrite`). I did not write this work; I drove it to
break it. Requirement surface read: the spec of record
`docs/work/complete/WI-392-driven-figures-carry-their-command.md`, drain plan
row 6 (`docs/archive/history/backlog-plan-2026-08-01.md` — **rung 1 only**; rung 2
deliberately not built), the archived
`docs/archive/specs/WI-392.2026-08-01.md`, and `PROCESS_OPTIONS.md` "Signed
measurements". `docs/log.d/` fragments were not read.

Verdict: CHANGES-REQUESTED

## Findings

**1. MAJOR — the shipped convention text fails the shipped check: a fresh
scaffold that follows the check's own opt-in instruction is red before it
declares a single figure.** Reproduced end-to-end:
`python3 project-trajectory/scripts/bootstrap.py --dest <tmp>` then
`python3 <tmp>/scripts/check_figures.py --root <tmp> --strict` (the exact
opt-in the module docstring instructs) exits **1**:

```
check_figures: WARN - docs/process-options.md:1337: declared figure carries neither cmd="…" rev=… nor derived="…" — "3. **Declare the figure — the `fig:` marker (WI-392, rung 1).** A driven"
check_figures: WARN - docs/process-options.md:1354: declared figure carries neither cmd="…" rev=… nor derived="…" — "`[step:figures]`, warn-first, `--strict` gates) flags a `fig:` marker carrying"
check_figures: 2 declared figure(s) missing provenance of 4 declared.
```

Both flagged lines are the "Signed measurements" part-3 prose that *states*
the convention (shipped `PROCESS_OPTIONS.md:1337` and `:1355`; bootstrap
materializes it verbatim as `docs/process-options.md`). Under the
convention's own rule these are exactly the lines `fig-ok` exists for ("a
line carrying `fig-ok` is prose ABOUT the convention, never a declaration")
— only the line that happens to mention `fig-ok` literally (`:1347`)
self-exempts. The same class also *silently passes*: `:1339`
(`fig: cmd="<command>" rev=<revision>`) and `:1346` (the `derived=`
grammar) parse their placeholders as non-empty values and are **counted as
declared figures** — as are the grammar-prose lines in this repo's own
scanned record (`docs/work/complete/WI-392-…md:18,:20`,
`docs/enforcement-audit.md:58`), which is why the meta-repo's "17 declared
figure(s)" includes at least 5 lines that are prose, not figures. The kit's
own gate passes today only because this repo carries **no**
`docs/process-options.md` (verified absent) — the one surface that would
red its own `[step:figures] --strict` G3 step never enters its walk; every
downstream scaffold gets the file, and CLAUDE.md's copy-ready bar is the
principle broken. No shipped test drives `check_figures` over a scaffold, so
the suite could not see this. **Remedy:** apply the convention's own
exemption (`fig-ok`) or reword the literal-`fig:` prose lines in
`PROCESS_OPTIONS.md` part 3 (and re-stamp the byte budget); consider a
commented `[step:figures]` row in `stack.ini.template` beside the WI-308
precedent for `[step:doc-refs]`, and a scaffold-drive test so this class
stays caught. -> fix before merge -> @builder

**2. MINOR — line-grammar edges in `judge_line`/`REV`, one of them a hole in
SR-136's own "(or carrying only empty values)" clause.** Driven on fixture
files (all outputs verbatim):
(a) *an empty `rev=` flush against the comment close passes* —
`flush rev: 12 things <!-- fig: cmd="ls | wc -l" rev=-->` produced **no
finding** (declared and passed): `REV = r"\brev=([^\s>\"']+)"` captures the
`--` of `-->` as the revision. The shipped test covers `rev= -->` (space
form, flagged) but not the no-space form, so an author's flush typo records
no revision yet passes — the exact clause "carrying only empty values counts
as missing" is defeated in this corner.
(b) *two half-carrying markers on one line cross-satisfy* —
`x 5 <!-- fig: cmd="a" --> y 6 <!-- fig: rev=b -->` passes as one declared
figure: `judge_line` searches the whole line, so figure x's missing `rev=`
is satisfied by figure y's, and vice versa.
(c) fail-closed, cosmetic: a *quoted* revision flags —
`quoted rev: 9 things <!-- fig: cmd="ls" rev="abc123" -->` → `WARN … carries
cmd= but no rev=` — natural authoring (the `cmd` value is quoted) is
convicted; worth either accepting quotes or saying "unquoted" in the
convention text. (a) and (b) are contrived and warn-first, so MINOR, but (a)
should be closed (e.g. require a `\w` start or exclude `-`-only captures)
because it dents the SR's AcceptanceCriteria as written. -> fix or narrow
the AC wording -> @builder

**3. MINOR — `docs/gate`'s regenerated stamp cites a revision that history
no longer contains.** The branch's `docs/gate` reads
`# computed 2026-08-01 (as-of db211dd7)`; `db211dd7` resolves only in the
reflog ("WI-392: declared figures carry their command and revision (rung
1)" — an amended/superseded twin of the build commit `83ebd450`) and
`git merge-base --is-ancestor db211dd7 HEAD` fails; no branch contains it.
Trunk's previous stamp (`as-of 7946a2ba`) *is* reachable, so this is the
branch's anomaly, not a pre-existing pattern. It is informational only —
`derive_gate.py --root . --check` rc=0 ("docs/gate up to date (G3)"), the
basis numbers are right (re-counted: SR=136 LLR=129 TC=126), and the trunk
regen at merge re-stamps it — but a WI whose whole subject is "a figure is
evidence only at the revision it was driven on" ships a gate cache whose
own rev pointer names an unreachable commit. Record-only. -> self-heals at
trunk regen; no code owed -> @owner

## Verified (hunted, held — no remedy owed)

- **SR-136 / LLR-146 / TC-140, reviewed as a ratification** (under
  `docs/gate-policy` `autonomous` this verdict would be the ratification act
  below G-Final): the row is real and measurable — the Requirement states one
  obligation (flag an opted-in `fig:` line missing `cmd=`+`rev=` or a
  non-empty `derived=`; presence, never truth; unmarked out of scope by
  design), the Rationale is the three driven 2026-08-01 cases plus the argued
  opt-in and the argued rung-2 decline, and the AcceptanceCriteria are
  testable and (modulo finding 2a's corner) shipped. SN links `SN-008;SN-010`
  are **byte-identical to the closest sibling SR-041** (check_doc_refs), as
  are every dial: Priority=S, Verification=Test, Status=Verified, Phase=1,
  Area="Doc currency" — Status-at-close per the LLR-143..145 convention.
  Traced cells resolve: Module/CodeSymbol (`findings_for`/`judge_line`)
  exist, TC-140's Evidence `tests/test_check_figures.py` exists, its Method
  maps 1:1 onto the 13 tests, and `check_doc_refs.py --root . --strict`
  rc=0 over the registries. IF-086/IF-087 leave Component empty like 59 of
  the 82 prior rows; Status=Stable is the registry's universal value.
  **Because this round is CHANGES-REQUESTED the ratification act is NOT
  taken here; it rides the re-review APPROVE** — nothing in the row itself
  blocks it, but finding 2a should either be fixed or the AC's empty-values
  clause narrowed so the ratified text is exactly true.
- **The IF seams resolve both directions once trunk regenerates.** On the
  branch `check_trajectory --strict` warns `IF IF-086/IF-087 … no script
  declares it via a Contracts: docstring line` (new vs trunk's baseline
  warnings) — but that harvest reads the generated arch-map, which is
  trunk-lane (SR-133). I regenerated `docs/architecture.md` in place
  (`gen_arch_map.py --strict-parse --src project-trajectory/scripts --doc
  docs/architecture.md`), re-ran the check — **both warnings clear**, and the
  map renders `m_scripts_check_figures -. IF-086 .-> m_scripts_check` and
  `m_scripts_check_doc_refs -. IF-087 .-> m_scripts_check_figures` — then
  restored the file (`git status --short` clean). Transient branch state, as
  designed.
- **Fail-open/grammar hunting that held** (all driven, outputs read): a bare
  `<!-- fig: -->` flags; a well-formed marker on a *false* figure passes —
  and the docstring, README row, PROCESS_OPTIONS closing paragraph,
  enforcement-audit row and stack.ini note all state presence-never-truth
  honestly, with rung 2 recorded as a declared absence in each home (and
  `docs/declared-absences` is the right non-home — it registers absent
  *paths*, not absent features). Both **wrapped/multiline marker** classes
  fail closed — `<!-- fig:` with attributes on the next line → `carries
  neither…`, and `cmd=` on the marker line with `rev=` wrapped → `carries
  cmd= but no rev=` (the class the builder's own close record was convicted
  for reproduces as a conviction, not a pass). A CRLF file flags and its
  well-formed CRLF marker passes. A GENERATED marker block with a bare
  marker inside is exempt; `fig-ok` exemption is **per-line only** (other
  lines in the same file still flagged); `docs/stack.ini` is scanned
  (`docs/stack.ini:1` finding reproduced in the suite's fixture);
  `config:`/`reconfig:` never match (`(?<![\w-])fig:`).
- **The three fixtures are the real recorded instances**: "2 failed, 7
  passed" (`docs/log.md:20643`), "two false positives" (`docs/log.md:21063`)
  and all three verbatim at `docs/log.md:21493-21494` — matching the
  archived spec's table — and
  `test_the_three_false_figures_each_flag_under_a_bare_marker` asserts each
  string appears flagged in stderr, warn-first (rc=0) then gating
  (`--strict` rc=1).
- **Registration honesty**: CMP-003 is the right component and its
  description now names check_figures in the checker list; bootstrap MAPPING
  + docstring listing + `tests/test_bootstrap.py` file list + kit README row
  all consistent, and the scaffold spot-check **materializes
  `scripts/check_figures.py`** (8,150 bytes, runs); module-size ratchet
  2257→2258 argued in place; dupes census **86→90 is honest** — exactly the
  four new F5 pair rows (`b87ed5851f33`, `74572e51bafc`, `da3bd5e9dd3e`,
  `f9a751e72b81`) with the substance walk genuinely *lifted* into
  `check_doc_refs.authored_lines` (the IF-087 seam), not copied;
  `check_dupes.py --src project-trajectory/scripts` rc=0. The
  PROCESS_OPTIONS re-stamp **166,314→167,884 (+1,570) is argued, not
  silent** — the byte-budget-guard row carries the delta + reason per its own
  "growth is allowed but must be flagged" rule, re-stamped in all three skill
  copies (`project-trajectory/skills`, `.claude/skills`, `.agents/skills`),
  and `wc -c` re-measures **167,884 exactly**; the +1,570 derived figure is
  itself declared with a `fig: derived=` marker (the fifth-case bar, honored
  in the row's own record).
- **Mechanical / R-A re-driven at `cab612c3`**:
  `tests/test_check_figures.py` → **13 passed in 0.43s**; smoke →
  **611 passed, 2 skipped in 9.52s** (membership 613, matching the
  deliverable's stamped 613; its 607/6 at `83ebd450` differs only in
  env-gated skips); `check_figures.py --root . --strict` rc=0 (**17
  declared** — but see finding 1 for what 5 of them are);
  `check_doc_refs.py --root . --strict` rc=0; `check_trajectory.py --root .
  --strict` rc=0 (clean, 401 WIs, graph acyclic); `trace.py` rc=0;
  `ruff format --check` on the three touched Python files — already
  formatted. **R-F**: the active spec's `specref = "docs/specs/WI-392.md"`
  is cleared in the complete spec's frontmatter; the spec of record is
  archived at the dated path with the R-F header. **docs/work delta**: WI-392's
  own complete/active/log-fragment files plus **one** line in
  `docs/work/complete/WI-378-…md` — a `path-ok` annotation on the backticked
  `docs/specs/WI-392.md` token the archival vacated (a prose token
  `spec_move` cannot relink; without it the composed tree reds
  `[step:doc-refs] --strict`); precedent `WI-394-…md:38`, honest text naming
  the destination, and it *adds no spec id* so the WI-397 merge rung is not
  in play. **log.md**: exactly one line changed — the link target redirected
  to `archive/specs/WI-392.2026-08-01.md` with the link text untouched,
  `spec_move`'s sanctioned shape (LLR-145). The deliverable's figures are
  dated, rev-stamped at `83ebd450`, and practice the convention they ship;
  the "watched RED first" claim is marked historical (its tree no longer
  exists), which is the honest form.

Findings: 1 MAJOR, 2 MINOR. The core is sound — the check is fail-closed on
every wrapped/half/empty class I could author but one, the fixtures are the
genuine incidents, rung 2 is a recorded absence everywhere it could have
been implied, and the registration is honest to the row. But the shipped
convention text convicting itself on every fresh scaffold is exactly the
class this WI exists to make cheap, and it must be fixed where the
convention lives, not waved through.

Round 1 verdict: CHANGES-REQUESTED findings=3 — superseded by Round 2 below.

---

### REVIEWER — G3 — Round 2 (remedy) — 2026-08-01

Judging only the remedy, `f5a423ae` ("rework: WI-392 scaffold-tier fig-ok +
parser grammar"), per the finding lifecycle: fixes verified by re-driving the
round-1 attacks, plus the one new surface the fix itself introduced (the
placeholder-grammar rule). Note for the record: `f5a423ae` also commits this
review file (round 1, verbatim — the crashed builder agent committed it with
the rework); the on-disk file matched the committed bytes before this append.

Verdict: APPROVE

**Finding 1 (MAJOR) — FIXED, verified at the class.** Re-drove the exact
round-1 attack: `bootstrap.py --dest <tmp>` then the docstring's own opt-in
`check_figures.py --root <tmp> --strict` → **rc=0**, `OK - no declared
figures`. The fix is three-layered as claimed and I drove each layer: (i)
the convention text carries `fig-ok` at source (part-3 heading and the
closing paragraph — read in the diff, inherited by the scaffold); (ii) the
parser reclassifies placeholder-shaped values as grammar prose
(`GRAMMAR_EXAMPLE` — neither flags nor counts); (iii) the missing test tier
exists — `test_a_fresh_scaffold_passes_its_own_docstring_opt_in` bootstraps
into tmp and runs the shipped check end-to-end, and I **mutation-drove its
red**: with `cab612c3`'s pre-fix `PROCESS_OPTIONS.md` swapped into the tree
the test **FAILED** (`tests/test_check_figures.py:178: AssertionError`),
restored clean after (`git status --short` empty). The fourth class member
(a verdict record quoting defective markers convicts the quoter — this very
file) is handled by `SKIP_PREFIXES = ("docs/reviews/",)` with the reasoning
in place, the **log deliberately not exempt** (stated in the code comment
and LLR-146), covered by
`test_a_review_record_quoting_defective_markers_is_out_of_scope` — and
proven live: the repo's `--strict` run is rc=0 *with this
bare-marker-quoting review committed*.

**Finding 2 (MINOR) — FIXED, all three edges re-driven on the round-1
fixtures.** (a) flush `rev=-->` now refuses: `WARN … carries cmd= but no
rev=` on both fixture files (the wordful-value rule, `WORD` +
`judge_marker`); (b) two half-carrying markers no longer cross-satisfy —
the same line now yields **two** findings (`no rev=` and `no cmd=`,
`marker_segments` per-marker ownership); (c) quoted rev **decided as
accepted** — `rev="83ebd450"` passes (`REV` takes bare or quoted), and the
convention text states the whole grammar where the convention lives
(PROCESS_OPTIONS part 3 *Grammar:* sentence: placeholder values declare
nothing, per-marker attribute ownership, bare-or-quoted `rev=`). Six new
tests cover all of it; suite **19 passed in 1.05s**.

**Finding 3 (INFO) — acknowledged as asked.** The fragment names
`db211dd7` (targeted grep, count 1 — the fragment was not otherwise read);
left to self-heal at the trunk-lane regen, which is the right disposition.

**Census 17→16 — verified to be exactly the class I convicted.** Re-ran the
census through the new parser: **16 declared, all passing, rc=0**; the 5
reclassified grammar-prose lines are precisely round 1's list
(`docs/work/complete/WI-392-…md:18,:20`, `docs/enforcement-audit.md:58`,
plus the fragment's two grammar lines), and the 4 additions are the rework
record's own markers (deliverable + fragment, 2 each). 17 − 5 + 4 = 16,
derivation declared in the Deliverable with its own `fig: derived=` marker.
Observed, acceptable: the rework's self-measurement rides
`rev=this-rework-commit` — a commit cannot carry its own hash, and the
record's landing commit identifies the revision; noted, not a finding.

**4. MINOR (new, in the fix; recorded, non-blocking) — the placeholder
proxy over-approximates its class, and the over-approximation is unstated.**
Driven: `Stderr cmd, rev MISSING: 9 tests <!-- fig: cmd="pytest -q 2>&1 |
tail -1" -->` → `OK - no declared figures` — a *defective* marker (rev
absent) escapes both census and flagging because `>` in the cmd value trips
`PLACEHOLDER_CHARS`; likewise a fully-provenanced `cmd="sort < in.txt |
wc -l" rev=abc123` declaration is silently uncounted. The ratified class is
"placeholder-grammar examples" / "placeholder-shaped (`<command>`, `…`)" —
a real shell-redirect command is neither, so the implementation ignores
markers the ratified text does not say it ignores. Bounded: requires `<`,
`>` or `…` *inside a quoted value*; zero of the repo's 16 live declarations
hit it; failure direction is silence (uncounted), never false conviction;
same stance-precedent as check_doc_refs' `{placeholder}` skip; warn-first
opt-in step. -> follow-up owed: narrow the proxy (e.g. treat placeholder
chars as grammar only when no other attribute is complete, or match
`<word>` bracket-pairs rather than bare chars) or state the
over-approximation in the convention/docstring where the stance lives, the
enforcement-audit bounded-gap idiom -> @owner

**Registries re-read after the amendment** (the AC changed in the rework,
so I re-read all three rows): SR-136's AcceptanceCriteria now says exactly
what ships — marker-level judgment ("each marker on a line judged on its
own attributes"), "empty or wordless values", "rev= (bare or quoted)", and
the ignore list naming placeholder-grammar examples and `docs/reviews/`
records; Requirement/Rationale/SN links/dials unchanged from the row I
verified in round 1. LLR-146's CodeSymbol tracks the real symbols
(`findings_for/judge_marker/marker_segments` — all exist) and its Detail
matches the shipped behavior including the reviews skip and the
deliberately-unskipped log; TC-140's Method adds the six new behaviors and
they map 1:1 onto the six new tests. `check_doc_refs --strict` rc=0 over
the registries.

**Mechanical, re-driven at `f5a423ae`**: `tests/test_check_figures.py` →
**19 passed in 1.05s**; smoke → **617 passed, 2 skipped in 9.69s**;
`check_figures --root . --strict` rc=0 (**16 declared**);
`check_trajectory --strict` rc=0 (clean, 401 WIs, acyclic);
`check_doc_refs --strict` rc=0; `check_dupes` rc=0; `ruff format --check`
clean; `wc -c PROCESS_OPTIONS.md` = **168,222** exactly as re-stamped, the
+338 argued with its reason in the byte-budget-guard row and re-stamped in
all three skill copy homes. Worktree clean before and after (the one
mutation probe restored from `f5a423ae`).

**RATIFICATION ACT (SR-136).** Under `docs/gate-policy` `autonomous`, a
recorded independent reviewer verdict carries ratification authority below
G-Final. **This APPROVE is that act: SR-136 — with LLR-146 and TC-140 as
amended at `f5a423ae` — is hereby ratified** as a row of record: the
requirement is real and one obligation, the SN links (SN-008;SN-010) are
honest and sibling-consistent, the amended AcceptanceCriteria state what I
measured the shipped check to do, the traced cells resolve, and Status
`Verified` is earned by the 19-green suite and the strict runs above.
Finding 4 is recorded beside the act as a bounded implementation residue
(the enforcement-audit idiom: written down, never implied covered) — it
narrows nothing in the ratified requirement text and owes a follow-up, not
a round.

Findings this round: 1 new (MINOR, finding 4, follow-up owed). Rounds 1–2
total: 1 MAJOR (fixed, verified), 2 MINOR (one fixed and verified, one INFO
self-healing), 1 MINOR residual recorded. I re-attacked the remedy and it
held everywhere the round-1 attacks broke it.

VERDICT: APPROVE findings=4
