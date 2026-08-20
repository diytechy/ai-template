"""The kit's small SHIPPED helper package — one home per shared behaviour.

WHY THIS EXISTS, AND WHAT IT REPLACES (owner ruling D-8, `OI-16`, ruled
2026-08-12 and its inversion confirmed 2026-08-13; executed WI-448).

The kit used to run the **F5 rule**: a shared `_kitcommon.py` was REJECTED so
every script stayed a stdlib-only, independently-copyable drop-in, and small
helpers were duplicated on purpose. That rule bounded nothing. A 2026-08-12
census found one behaviour with FIVE homes (the declared-line reader, carrying
a prose claim of equivalence that was false), one with THREE (`is_example`, one
copy crashing on `None`), and a 270-line spec-folder reader copied verbatim into
three modules — a claim that had itself already drifted by the time this package
landed. D-8 replaced F5: shared helpers live HERE, once.

**The inversion, and why the package ships.** D-8's literal step 2 was "import
from `bootstrap.py`", which is unbuildable: `bootstrap.py` is deliberately NOT
in its own `MAPPING`, so a shipped script importing it would raise
`ModuleNotFoundError` on a fresh scaffold while passing in this repo, where the
kit folder holds every file. That is the exact failure the repo has shipped once
(`MAPPING` omitted `schedule.py` and every fresh scaffold died on its first
claim). So the direction inverts: this package ships like any other sibling, and
`bootstrap.py` imports FROM it.

**The rule that replaces F5's, and it is asserted, not merely written here:**
`bootstrap.py` imports this package and no other sibling
(`tests/test_bootstrap.py::test_bootstrap_imports_only_the_common_package`).
Every module here must therefore stay import-clean of the rest of `scripts/` —
a sibling import from inside `kitlib` would smuggle the whole graph into the
scaffolder.

**THEMED MODULES, NEVER ONE GENERIC `common.py`** (the shape constraint adopted
from the 2026-08-19 repository review, H-09; it is also D-8's smallest-total-code
direction read at the right grain). A generic bucket is how a shared module
becomes a second junk drawer nobody can decompose later. Each module owns one
theme and says so in its own docstring:

  * `config`   — declared-policy files and console encoding: the one-line
                 declared reader all five former copies applied, and the
                 UTF-8 console guard.
  * `registry` — the `docs/work/` spec-folder work-item reader: the row shape,
                 the frontmatter/status/body parse, and the ordered read.
  * `git`      — the best-effort-off-git subprocess pattern.

Two further theme slots are NAMED BY THE ADOPTED SHAPE AND DELIBERATELY NOT YET
CREATED, because an empty module is a worse statement than an absent one:
`station` (trunk/integration mechanics) and `views` (render helpers). They land
as the consolidation program continues; `WI-483`'s successor decomposition
builds on this topology.

**Stdlib only, like every kit script**, and every module here must import
cleanly on a bare Python 3.11+ on Windows and POSIX.
"""
