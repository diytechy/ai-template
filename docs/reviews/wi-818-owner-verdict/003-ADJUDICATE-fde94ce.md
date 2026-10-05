# 003: ADJUDICATE (independent, Claude Opus), TC-319 and TC-320 at `fde94ce9`

Adjudicator: an independent Claude Opus session, the author of
`dispute-1-ruling.md`, `001-ADJUDICATE-be8633c.md` and
`002-ADJUDICATE-be8633c.md`. I wrote none of WI-818's code or rows. This is the
fresh ruling 001 called for, on the two `method` cells it returned.

## Basis (probed, not trusted)

- **One spine commit since 001 and 002.** `git diff --stat b454ba1a..HEAD`
  touches only `docs/test/test-cases.toml`: 2 lines, the `method` line of
  TC-319 and the `method` line of TC-320. No script and no test moved, and
  trunk is still `c0caea09`.
- **The landed text is 001's, byte for byte.** I parsed the registry at `HEAD`
  with tomllib. TC-319 `method` and TC-320 `method` each equal the matching
  fenced block of `001-ADJUDICATE-be8633c.md`, which a regex pulled out of the
  committed file.
- **No other cell moved.** I compared every row and every key of the
  test-case, low-level-requirement, system-requirement and interface
  registries at `b454ba1a` and at `HEAD`. The only cells that differ are
  TC-319 `method` and TC-320 `method`. The ten rows of 001 and 002 are
  otherwise as I judged them. LLR-303, LLR-304, TC-319 and TC-320 still read
  `Drafted`.
- **The code is the code 001 judged**, so 001's mutant results stand: every
  clause of the two new cells is held by a node in the row's unchanged
  `evidence`.

## Verdicts

- [APPROVE] TC-319 -> drive the overrule coupling through every case its
  evidence names, now stating the unparseable record beside another record's
  cited overrule, the `-000` example, and the listed blob the store cannot read
  -> the cell is 001's text, true of the code and held by its cited nodes ->
  ready.
- [APPROVE] TC-320 -> drive the migrator through every case its evidence
  names, each new case with its expected result -> the cell is 001's text, true
  of the code and held by its cited nodes -> ready.

With 001's [APPROVE] of LLR-303 and LLR-304 standing, all four first-approval
rows are approved.

OUTCOME: APPROVE rows=2

## Aftermath (the act, in the lane, uncommitted, for the coordinator to commit)

- Flip `Status` from `Drafted` to `Approved` on LLR-303, LLR-304, TC-319 and
  TC-320 only.
- Re-attest the six MEANING rows 002 blessed, whose cells have not moved.
- One snapshot does both:

`python project-trajectory/scripts/intake.py snapshot --approves "docs/requirements/low-level-requirements.toml=WI-818;docs/test/test-cases.toml=WI-818" --reattests SR-225,LLR-283,LLR-284,TC-293,TC-294,TC-313`
