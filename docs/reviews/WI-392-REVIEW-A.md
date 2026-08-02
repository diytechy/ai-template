# WI-392 — REVIEW-A (independent)

### REVIEWER — G3 — Round 1 — 2026-08-01

Reviewed at `cab612c3` (branch `wi-392-driven-figures-carry-their-command`;
trunk = `ConcurrencyTrainRewrite`). I did not write this work; I drove it to
break it. Requirement surface read: the spec of record
`docs/work/complete/WI-392-driven-figures-carry-their-command.md`, drain plan
row 6 (`docs/backlog-plan-2026-08-01.md` — **rung 1 only**; rung 2
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

VERDICT: CHANGES-REQUESTED findings=3
