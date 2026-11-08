+++
id = "WI-1000"
title = "SR-035's token scan is built: a test scans the shipped registry templates and ID vocabulary for language-specific tokens"
workstream = "process"
sr_refs = ["SR-035"]
specref = "docs/requirements/low-level-requirements.toml#LLR-171"
buildtier = "medium"
safety_class = "ordinary"
planmode = "none"
priority = 5
+++

## Context

Filed by hand on 2026-11-05 (attended), routed by OI-127's ruling. TC-165 has
two halves. Its scaffold half is driven by
`tests/test_profile.py::test_every_profile_permutation_scaffolds_green`, whose
`node` cases scaffold a non-Python profile and run `trace.py --strict`. That
covers integrity, but not `--strict-schema`, and the test carries no TC-165
tag. The token scan of the shipped registry templates and ID vocabulary has no
test. OI-129 was ruled (a) on 2026-11-08: an approved row is built unless
evidence shows substantial work, and none does.

Measured on 2026-11-08: a `--stack node` scaffold passes
`trace.py --strict --strict-schema` with exit 0. The contract below finds no
token on today's surface and exempts 37 kit-script names, 29 of them in
`registries/*.template.{toml,csv}` (e.g. `trace.py`, `scripts/hats.py`). The
other non-Python stacks take the same `NON_PYTHON_STACKS` branch in
`bootstrap.py` as `node`, so `node` stands for them.

## The scan contract (S3: closed)

**Surface.** The scan reads these files:

- every `project-trajectory/registries/*.template.toml` and
  `*.template.csv`. That is IF-039's declared set, 15 files today. It is
  globbed, so a new template joins the scan without an edit.
- `project-trajectory/work/WI-000.template.md`, the work-item registry's
  scaffold.
- `project-trajectory/id-watermark.template`.

**ID vocabulary.** The vocabulary has three declarations:

- `trace.WATERMARK_SPACES`, the declared set of every id space (20 today,
  pinned by `tests/test_id_watermark.py`);
- `PROCESS.md` §2 "Identifier scheme", from its heading to the next `## `;
- `INTERFACES.template.md` "ID scheme & columns", bounded the same way.

Each off-spine prefix is also declared by its template's row ids, which the
file scan covers. If a glob matches nothing or a heading is missing, the test
fails. It never skips.

**Token set.** The set is declared once, as two constants in the test module:

- `LANGUAGE_TOKENS`: python, pytest, pip, pyproject, conftest, unittest,
  mypy, ruff, virtualenv, javascript, typescript, nodejs, npm, rust, cargo,
  golang, java, kotlin, maven, gradle, junit, csharp, dotnet, nuget, ruby,
  rubygems, php, cmake, powershell.
- `SOURCE_EXTENSIONS`: py, pyi, ipynb, js, mjs, cjs, ts, tsx, jsx, rs, go,
  java, kt, cs, rb, php, c, cc, cpp, h, hpp, swift, ps1.

Words that are also ordinary English are left out: node, go, gem, composer,
yarn, swift, black. Today's templates use "node" and "composer" as English.

**Matching.** Matching is case-insensitive.

- A word matches only between non-`[A-Za-z0-9_]` boundaries.
- An extension matches as a file-name suffix: a name character before the
  dot and none after it.
- One exemption applies: a `.py` match that is exactly `<name>.py` or
  `scripts/<name>.py`, where `project-trajectory/scripts/<name>.py` exists. A
  kit script is the kit's own toolchain, which every adopter runs whatever
  its stack. Naming it names the delivered checks that SR-035 presupposes, not
  the adopter's language. `src/check.py` and `tests/*.py` are still reported.

A hit is reported as file, line and token.

**Outside the claim.**

- Any token not in the two constants.
- All other kit prose. This includes the rest of `PROCESS.md`, which carries
  marked Python reference examples by design.
- `registries/last-approved-README.template.md` and `specs/`, which are not
  registry templates.
- Restatements of the scheme, such as `KICKOFF_PROMPT.md` and
  `AGENTS.template.md`.
- The kit's scripts.

The test does not claim to detect arbitrary language-specific free text.

## Done-when

- [ ] A new in-process module, `tests/test_language_neutral_scheme.py`
      (tagged `Implements: TC-165`), declares the two constants and one scan
      function over the surface above. The shipped surface scans clean.
- [ ] Planted cases run against a temp copy of the surface:
      - `pytest` and `src/app.py` planted into a template copy are each
        reported with file and line;
      - `scripts/trace.py` is not reported;
      - `src/check.py` is reported;
      - a removed §2 heading fails the test.
- [ ] `test_every_profile_permutation_scaffolds_green` runs
      `trace.py --strict --strict-schema` (`--strict` includes the integrity
      tier) and carries the node-level tag `Implements: TC-165`.
- [ ] TC-165's `evidence` reads
      `tests/test_profile.py::test_every_profile_permutation_scaffolds_green; tests/test_language_neutral_scheme.py`,
      and `check_trajectory --strict` finds tags and evidence equal.
- [ ] No shipped file changes, so no RESYNC entry is owed.
- [ ] Review bar: A+B (REVIEW-A plus an independent REVIEW-B).

## Architectural delta

The row adds no mode class, no adopter-facing value domain and no boundary.

- The new output is a test result. It depends on the template bytes IF-039
  carries, on `trace.WATERMARK_SPACES`, on the two declared doc sections and
  on the token constants.
- This stays inside LLR-171 and CMP-009.
- The scaffold half changes one flag in an existing test.
- No IF row, component or flow changes.

## Critique dispositions

Round 1 (fresh Codex session, 2026-11-08): CHANGES-REQUESTED, one MAJOR and
two MINORs.

- **S3, the finite scan contract: adopted.** "The scan contract (S3: closed)"
  names the surface ("every `project-trajectory/registries/*.template.toml`
  and `*.template.csv` ..."), the ID vocabulary (`trace.WATERMARK_SPACES`,
  `PROCESS.md` §2, `INTERFACES.template.md` "ID scheme & columns"), the token
  set "declared once, as two constants in the test module", the matching
  rule, and what is outside the claim: "The test does not claim to detect
  arbitrary language-specific free text."
- **S4, the planning ruling: adopted as `planmode = "none"`.** With the
  contract closed, the Done-when fully specifies the diff:
  - one file-scan test with its planted cases;
  - one flag and one tag in an existing test;
  - one evidence cell.

  That is S4's cheap-test exception.
- **S5, the architectural delta: adopted.** "Architectural delta" states:
  "The row adds no mode class, no adopter-facing value domain and no
  boundary."
