+++
id = "WI-420"
title = "TC-034's enforcer is now STRICTER than the requirement it verifies - retarget tests/test_stdlib_only.py onto the dependency ledger. WI-419 amended SR-034 from 'stdlib-only' to 'stdlib plus non-stdlib dependencies declared as a reviewed row in docs/dependencies.md' (owner RULING-3 2026-07-28, closing a prose-vs-ruling drift). test_stdlib_only.py still AST-scans every kit script and asserts each top-level import resolves to stdlib or a local sibling - full stop. Today that is harmless because no Kind=python ledger row exists, so the strict test and the wider requirement agree vacuously; the moment the first Python dependency is admitted through the reviewed ledger path the requirement permits it and TC-034 reds, which reads as a regression when it is the test disagreeing with its own parent. THE ASK: make TC-034 verify SR-034 as written - an import passes if it resolves to stdlib, a local sibling, OR a name declared Kind=python in docs/dependencies.md - reusing tests/test_dependency_ledger.py's ledger_declared() parser rather than growing a second one (that file already owns the ledger-table grammar and carries the mutation proof that the scanner CAN fail). Decide deliberately whether the two suites then overlap enough to merge: test_dependency_ledger.py already fails on an UNDECLARED import, so the retargeted TC-034 may be the same assertion from the other direction - if so, say which row each test verifies, or fold one into the other and re-point the TC registry. NOT a licence to weaken the bar: the shipped-tier stdlib-preferred rule (a dependency an adopter is forced to install needs an owner ruling) must still be enforced or explicitly recorded as prose-only in docs/enforcement-audit.md."
specref = ""
workstream = "tests"
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

Resolved by **deleting the duplicate and spending it on the unenforced clause** —
owner design call, taken after the discussion the spec asked for.

**The finding that decided it.** The two scans were the same test. Side by side:

- `test_stdlib_only.py`: `allowed = stdlib ∪ siblings`
- `test_dependency_ledger.py`: `allowed = stdlib ∪ siblings ∪ ledger(Kind=python)`

Same AST walk, same directory, differing by exactly one union term — and that
term is **empty** (the ledger declares zero `Kind=python` rows; only the `git` /
`gh` `system` substrates). So the two were *bit-identical in behavior*, and the
spec's own proposal — teach `test_stdlib_only.py` to read the ledger — would have
reproduced `test_dependency_ledger.py` verbatim: two homes for one rule, the
thing this kit tells downstream repos not to do.

**The gap that was actually open.** SN-011 and SR-034 both distinguish a
`coordinator` dependency (only this repo installs it) from a `shipped` one
(**every adopter** is forced to install it, so it needs an owner ruling and
stdlib stays *preferred*). **Nothing read the `Tier` column.**
`test_dependency_ledger.py` asks only *is it declared?* — so a coordinator-tier
or unruled package imported by `trace.py` would have shipped to every adopter
with a green suite.

**What landed**

- **Deleted** `tests/test_stdlib_only.py`; **TC-034 re-pointed** at
  `tests/test_dependency_ledger.py` with its Method restated to the ledger model
  (`Status=Modified` — it joins SR-034's open re-attest window rather than
  buying a second sitting).
- **`ledger_rows()` added to `tests/test_dependency_ledger.py`** — the ledger
  table grammar keeps **one** home; the new module imports it rather than
  growing a second parser. `ledger_declared()` is unchanged.
- **New `tests/test_shipped_tier.py`** (**TC-149**, minted `Verified` on real
  passing evidence): derives the adopter-facing set from `check.py`'s own
  `layer="process"` step tags — 15 steps, 11 entry scripts, read from the plan
  rather than hand-copied, so a step that changes layer cannot drift away from
  the bar — walks their **transitive** sibling imports, and requires every
  non-stdlib module in that closure to be a `Kind=python` row that is
  `Tier=shipped` **and** carries a non-empty `Ruled` cell. Transitive matters: a
  sibling's dependency ships just as surely as a direct one, and the failure
  message attributes it to the file that actually imports it.
- **Four mutation proofs in-file** (the standing vacuous-guard rule), since the
  real assertion is vacuously green today: coordinator-tier, unruled-shipped and
  undeclared imports are each driven through fixture trees and asserted
  **caught**; a properly ruled shipped row is asserted **allowed**, so the check
  can never be mistaken for the stdlib-only ban it replaced. Plus
  `test_the_process_layer_still_covers_the_kit_floor`, which fails if `trace.py`
  / `derive_gate.py` / `check_docs.py` stop being process-layer entry points —
  i.e. if the derivation itself goes blind.
- **`docs/enforcement-audit.md`** — the stale row (*"Kit scripts are stdlib-only
  → test_stdlib_only.py"*, describing the pre-amendment world) replaced by two
  rows, and audit finding 1 extended with the Inspection → Test → *right two
  tests* history.

## Evidence

- `pytest -q tests/test_shipped_tier.py tests/test_dependency_ledger.py`:
  **12 passed in 0.32s**.
  <!-- fig: .venv/bin/python -m pytest -q tests/test_shipped_tier.py tests/test_dependency_ledger.py @ WI-420 -->
- `trace.py --strict --strict-integrity`: `SN=27 SR=136 LLR=137 TC=135
  orphans=0 integrity=0`, exit 0.
  <!-- fig: python3 project-trajectory/scripts/trace.py --root . --strict --strict-integrity @ WI-420 -->

## Deviations from spec

- The spec's stated ask (teach the test to read the ledger) was **not**
  implemented — it would have created the duplicate described above. The spec's
  own second paragraph anticipated this ("decide deliberately whether the two
  suites then overlap enough to merge"); they did, completely.
- Its fallback ("or explicitly recorded as prose-only in
  `docs/enforcement-audit.md`") was **not** taken either: the shipped-tier bar is
  now mechanically enforced, so recording it as a prose gap would have understated
  the coverage.
- **TC-149 was minted directly as `Verified`** rather than `Draft`. Its evidence
  exists and passes, and a `Draft` TC reads G0 in the derived gate — it would
  have dropped the gate below the amendment window's G2 for a row that is not in
  fact unfinished. It rides SR-034's open window and appears in the re-attest
  brief, so it is not blessed silently.
