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
  * `ladder`   — the eight-rung `DevStg-*` STAGE vocabulary: the rung labels in
                 ladder order, the derived rung count, the per-rung
                 descriptions, and `stage_ord`, the only legal comparison.
                 Pure data — it imports nothing at all.
  * `stage`    — the STAGE CARRIER, one rung above `ladder`: the declared
                 derivation inputs and their fingerprint, the `docs/stage`
                 format, the ordering that admits the per-phase sentinel, the
                 selection floor and the per-phase fold, and THE COMMON READER
                 every consumer of "what stage is this repo in" calls. It takes
                 the derivation as an ARGUMENT — the registry parse needs a
                 sibling this package may not import.
  * `spine`    — the spine ROW vocabulary, one tier over `ladder`: what a
                 `Status` word means (`Drafted`/`Approved`/`Founded`), which
                 `Verification` methods decompose to a TC but no LLR, what a
                 free-form `Phase` cell parses to, which `SN-###` ids a needs
                 registry mentions and which of them the SRs cite, plus the ref
                 split, the `-000` placeholder test and the registry CSV loader
                 those rules are written on.
  * `evidence` — the TEST-EVIDENCE record: the `docs/test/evidence` format and
                 the declared source surface a harness claim binds to, so the
                 top rung can be derived from a verdict instead of a cell.
  * `station`  — the lane-close TERMINAL-OUTCOME vocabulary: the three states a
                 lane can close into, the status directory each is declared by,
                 the bar-attestation trailer label, and the "exactly one
                 declared directory, or none" decision.

`station` arrived by a different route from the other three, and the difference
is worth stating because it is the shape the remaining slots should follow. The
first three were CONSOLIDATIONS — one behaviour with several copies, pulled into
one home. `station` was a DECOMPOSITION: the vocabulary had exactly one home
already, but that home was the merge coordinator, so every reader had to import a
module that claims lanes and moves specs in order to read a table. A view did
exactly that, which is how the render leaf became part of the runtime scripts'
strongly connected component. A shared home is not only for things that were
duplicated; it is also for things that were correctly single and wrongly PLACED.

`spine` (WI-448 slice 3) is the FIRST shape at its purest, and it is the case
the package was ruled into existence for: two modules that must never disagree —
`trace.py`, which ENFORCES the spine, and `spine_rules.py`, which DERIVES its
stage from the same rows — each carrying its own copy of nine POLICY decisions,
with nine equality pins standing in for one home. It got its own module rather
than joining `registry` because `registry` is the `docs/work/` SPEC-FOLDER
reader: a different registry, a different carrier, a different consumer set.
Folding the two together would have grown the package's largest module into
exactly the generic bucket the shape constraint above forbids.

`ladder` (WI-498 slice 0) is BOTH shapes at once, which is why it is the
clearest case in the package. It was DUPLICATED — the eight rung strings
restated in `agent_common`, the descriptions copied byte-for-byte into
`traj_status` — and it was also wrongly PLACED, because the one home it did have
was `spine_rules`, a derivation engine that parsed the registries and wrote
`docs/gate`. So a renderer needing eight sentences either loaded the engine or
kept a copy, and it kept a copy that nothing pinned.

`stage` (WI-498 slice 1) is a THIRD shape, and naming it keeps the roster
honest: it is NEW BEHAVIOUR placed here from the start rather than a copy pulled
in or a misplaced home moved. It belongs here on the same test the other two
pass — every consumer of the stage will call it, so a home inside any one
consumer would make the others import that consumer. Note what it is NOT
allowed to be: the derivation itself stays outside, because it needs the
registry carrier, and this package's one asserted rule is that it imports no
sibling. A module here that "just needed one import" would smuggle the whole
graph into the scaffolder.

One further theme slot is NAMED BY THE ADOPTED SHAPE AND DELIBERATELY NOT YET
CREATED, because an empty module is a worse statement than an absent one:
`views` (render helpers).

**Stdlib only, like every kit script**, and every module here must import
cleanly on a bare Python 3.11+ on Windows and POSIX.
"""
