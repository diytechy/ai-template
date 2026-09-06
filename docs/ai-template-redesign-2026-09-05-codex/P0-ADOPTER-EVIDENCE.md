# P0a populated adopter evidence

**Raw source base:** `83f2c7aa990a757729e7847816d40a8cdc2afcc7`
(`docs: Anchor baseline-repair resync instructions to the source commit`). The
adopter starts from the existing archived-kit pin
`fd5916b976dc3d77ff11a2d2d6bc4a7fa924641d` (2026-07-22).

This is no longer an exact base-`83f2c7aa` execution: the live checkout now has
a P0 fix to `bootstrap.py` that ships `gen_prompt_catalog.py` and generates its
required catalogue, while concurrent plan work changed `ADOPTING.md` and
`RESYNC_PACK.md`. The oracle takes the live checkout's script and template
bytes. It records the raw base so a future rerun can distinguish that source
from this corrected, dirty source state.

## Fixture and supported steps

`tests/test_old_kit_resync.py::test_node_adopter_upgrade_preserves_populated_owner_content`
builds an old scaffold, then fills it with an owner-controlled Node incident
timeline: README vision, custom `DATA-PROVENANCE` hat, `package.json`, Node
source and `node:test` test, a Node `docs/stack.ini`, legacy `SN-701`/`SR-701`,
a project-owned migration note, an unfinished `WI-701` draft, and a dated
source-confidence decision in `docs/log.md`. It commits that populated state to
a temporary Git repository.

The first target run declares `--stack node`, regenerates only the documented
process docs, and runs `--sync`. SHA-256 equality proves the owner files,
legacy carriers, work record, and log were unchanged; the old `pytest.ini`
deliberately remains after this add-only phase.

A separate copy then follows the complete current kit overwrite:

1. run `bootstrap.py --force --stack node`, replacing the declared kit-owned
   scripts, prompts, stubs, process docs, and registries as one coherent set;
2. explicitly merge back the owner README, hats, stack configuration, Node
   application/test, legacy SN/SR source, unfinished work, log, and custom note;
3. run `migrate_carrier.py --check`, then write mode, and stage deletion of
   every source carrier the converter reports plus obsolete `pytest.ini`;
4. add an old `docs/review-policy`, run `bootstrap.py --migrate-config`, and
   preserve `review_rounds = 2` in `docs/process.toml`; and
5. run `trace.py --bump-ids`, regenerate the prompt catalogue, and commit the
   converted tree.

This is not a recommendation to run `--force` blindly on an adopter. The
overwrite refreshes kit-owned material; preserving the owner records and
reviewing their live-reference merge are required parts of this evidence.

The companion [adopter-revalidation review record](P0-ADOPTER-REVALIDATION-REVIEW.md)
uses this populated fixture to distinguish a no-change upgrade, a changed-purpose
hat review, a missing-SN proposal, a hat-derived SR proposal, and an
implementation-only repair. Those fictional review outcomes are not live
adopter approvals.

The custom note initially links to
`requirements/system-requirements.csv`. The operator merge changes only that
live reference to `requirements/system-requirements.toml` after conversion. This
is the deliberately reviewed project-owned change that `check_docs.py` requires;
the fixture does not add an allow-list entry or a generic link migrator.

The oracle reads the target TOML rather than comparing altered carrier bytes:
`SN-701` remains `Approved` with its owner text, while `SR-701` still cites it
and remains `Drafted`. README, hats, Node code/test, package metadata, stack
configuration, unfinished work, and log remain byte-identical. The initial
commit is an ancestor of the migration commit, and `git show` still retrieves
the original vision and source-confidence decision.

## Measured results

The focused fresh-Node and populated-upgrade tests passed on 2026-09-06:

```
.venv/bin/python -m pytest -q \
  tests/test_old_kit_resync.py::test_fresh_node_scaffold_generates_its_required_prompt_catalog \
  tests/test_old_kit_resync.py::test_node_adopter_upgrade_preserves_populated_owner_content
# 2 passed in 7.80s
```

The fresh Node scaffold has `scripts/gen_prompt_catalog.py`, generates
`prompts/CATALOG.md`, and passes the Needs-stage prompt-catalog harness step.
The populated copy passes `migrate_carrier.py --check`,
`trace.py --strict-integrity`, `check_docs.py --root .`, and
`check.py --stage DevStg-Needs --tier smoke`. Node `v24.18.0` and npm `11.16.0`
were already available; `npm test` runs the preserved application test without
installing packages.

## Fresh scaffold footprint

These measurements precede the P2a dependency-writer change and final resync
guidance edits; they describe that captured scaffold state, not final release
bytes or an operating-efficiency comparison.

Fresh scaffolds were built in `/tmp` with the documented command shape
`python project-trajectory/scripts/bootstrap.py --dest <temp> --stack <node|python>
--agents none`. The raw comparison archives
`83f2c7aa990a757729e7847816d40a8cdc2afcc7`'s `project-trajectory/`; the current
run uses this checkout's dirty source, including the prompt-catalog fix. Both
measurements exclude `__pycache__` and `.pyc`. Python SLOC is the sum of
`check_complexity.module_sloc` over shipped `scripts/**/*.py` files.

| Source | Profile | Files | Bytes | Shipped Python | Python SLOC | Generated outputs |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| raw `83f2c7aa` | Node | 166 | 4,087,187 | 77 files / 3,434,422 bytes | 37,013 | kit stamps, trace report, open-items HTML |
| current dirty source | Node | 168 | 4,100,991 | 78 files / 3,444,635 bytes | 37,180 | same, plus `prompts/CATALOG.md` |
| raw `83f2c7aa` | Python | 167 | 4,086,220 | 77 files / 3,434,422 bytes | 37,013 | kit stamps, trace report, open-items HTML |
| current dirty source | Python | 169 | 4,100,024 | 78 files / 3,444,635 bytes | 37,180 | same, plus `prompts/CATALOG.md` |

Node copies record `stack=node`, `omit=` and omit `pytest.ini`. They still seed
the Python-reference `docs/stack.ini` product commands (`{py} -m ruff format`,
`{py} -m ruff check`, `{py} -m pytest -q`), while adding the Node rewiring
checklist and `[arch-map] mode = files`. Python copies record `stack=python`,
`omit=`, and include `pytest.ini`; their product commands are the same reference
commands. Thus `--stack node` is a supported structural profile and preservation
path, not a core-only scaffold or a dependency-free Node toolchain; an adopter
must intentionally replace the product commands with its own Node tooling. The
physical footprint also includes the reusable runtime, coordinator, hooks,
prompts, and HTML/process machinery; this measurement makes no
operational-efficiency claim.

This is a POSIX measurement. The test's archive, Git, and subprocess operations
are stdlib-based and can run in Windows CI, but no Windows execution or live
downstream adopter was exercised. It ran on Darwin 25.5.0 arm64 with Python
3.13.14, 6 logical CPUs, and 8 GiB memory. The raw archive is not itself a Git
checkout, so its bootstrap stamp is `unknown`; the current scaffold correctly
warns that its source checkout is dirty. If Node or npm is absent, pytest marks
the populated test skipped before its final commit/harness checks; that
environment has no passing populated-upgrade result. The separate fresh-scaffold
test still exercises the mandatory catalog without Node.

## Committed implementation recheck

The complete upgrade/catalog module passed against clean source
`77612fb217b1b0d18b420d7460b394e7398d7d0f`: `.venv/bin/python -m pytest -q tests/test_old_kit_resync.py`
reported `8 passed in 9.51s`. No provider or live adopter was involved.

Fresh scaffolds were remeasured at that same committed source using the command
and exclusions above. Both stamps read `77612fb2 2026-09-06`. SLOC calls
`check_complexity.module_sloc(path.read_text())`, not the path object.

| Profile | Files | Bytes | Shipped Python files | Python bytes | Python SLOC |
|---|---:|---:|---:|---:|---:|
| node | 168 | 4,105,090 | 78 | 3,447,623 | 37,236 |
| python | 169 | 4,104,121 | 78 | 3,447,623 | 37,236 |

These are whole-profile footprints, not a physically isolated core or measured
operating savings. The earlier dirty-tree measurements remain historical.
