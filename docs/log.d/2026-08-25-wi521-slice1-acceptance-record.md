## 2026-08-25 — WI-521 slice 1: the acceptance record leaves the checker

**Summary.** The standing decomposition-debt row takes its first slice, and it
pays down the axis the module-size ratchet actually measures. 677 lines came out
of `check_trajectory.py` VERBATIM into a new sibling,
`project-trajectory/scripts/acceptance_record.py` — the two-tree spine
comparison and the recorded-baseline mirror. The boundary, in one sentence:
**what compares two git trees cell by cell to answer whether attested text has
moved away from the copy recording its acceptance is in the new module; what
asks what the registries say today stayed.** `check_trajectory.py` re-exports
every moved name, so no caller moved and its CLI is byte-identical; `intake.py`
was re-pointed because all three of its executable uses were inside the block,
which deleted its import of a ~5,000-line validator outright.

Deferred open items: none — the slice needed no ruling, and the one finding it
banked (`LLR-178`'s attested rationale now locates the judge one indirection
from the code) is kept true by a multi-module traced cell rather than by an
edit to approved text.

### The evidence was re-derived first, and it corrected the row's own table

`WI-508`'s fusion table is this row's strongest asset, so it was re-derived from
the two blind returns' own forward-coverage tables rather than inherited.

fig: derived="pairs (x,y) of SRs where derivation A and derivation B each place x and y in different modules while the live SR->module join puts them in the same one; A and B read from their own `## Forward: every SR to exactly one owning module` tables, the live join reads LLR `module` cells through `sr_refs` and assigns each SR the module its rows name most often"

The three-way agreement reproduces **exactly** — A vs LIVE 94.6%, B vs LIVE
94.8%, A vs B 97.0% over the same 71 SRs and 2,485 pairs — which is the
strongest available check that the re-derivation is reading the same partitions.
The fusion counts do not: 45 pairs against the recorded 48, and `agent_loop`
reads **11**, not 14.

The reason is worth more than the correction. The live join's rule — *the module
an SR's own LLR rows name most often* — is **underdetermined for 13 of the 71
SRs**, whose top module is a tie. `SR-026` ties three ways between
`agent_session`, `agent_loop` and `dispatch`; break it toward `agent_loop` and
that module reads 14 and heads the table, break it any other way and it reads 11
and does not. Nothing recorded which way the original run broke it. So the head
of the table turns on one arbitrary tie-break — the table remains good evidence
about *which* modules fuse obligations and is not reliable about their order.
Recorded in the WI's own slice block rather than quietly patched.

### Why `check_trajectory`, with no argument

It reads 13 fused pairs under **both** tie-breaks; it was the largest of the four
fusion heads (4,963 lines against `agent_loop` 3,614, `bootstrap` 3,146,
`agent_common` 2,643); it holds the two most complex checker functions in the kit
(`main` 24, `interface_findings` 20); and unlike `agent_loop`, which `WI-483`
decomposed twice, nothing had ever come out of it. Its own ratchet stamps had
asked for this four separate times — each recording "whether `check_trajectory`
is still ONE checker" as a live question and declining to answer it.

Within the module, the acceptance record was the largest single reduction
available: 8 of the 13 fused pairs run through `SR-178`/`SR-179`, and **both**
blind derivations gave that subject a module of its own (A's `A2`, B's `M06`)
from the requirement text alone.

### The seam was found, not carved

The moved block's only non-builtin dependencies, out of everything
`check_trajectory.py` had in scope, were `spine_carrier` and one `git … or None`
primitive — no `argparse`, `csv`, `re`, `difflib`, `configparser` or `pathlib`.
`tests/test_acceptance_record.py` (8 tests) pins that as the boundary rather
than re-asserting rules already covered where they were: the import census, that
no rule calls `open()` or builds a `Path`, that the module never reaches back up
into the checker, that every shim is the same OBJECT rather than a copy, and
that `_git` resolves to one home in both modules.

### Byte-identical, measured that way

fig: cmd="drive 9 CLI paths (check_trajectory x5 incl. --staged and a non-root --root, trace --strict, three intake --help surfaces, baseline_snapshot --help) plus 56 in-process API probes over this repo, against a scripts tree rebuilt at HEAD, and diff" rev=c3bc6e07

The harness self-diffed **empty twice** against itself before it was trusted
(set/frozenset `repr` order varies per process, so the transcript normalizes
containers). HEAD vs the slice: **one intended difference and no others** —
`intake.py --help` prints its own docstring, which now names
`acceptance_record.staged_spine_amendments`.

### Ratchets

- `tests/test_module_size_ratchet.py`: `check_trajectory.py` **4,963 → 4,327**
  re-stamped DOWN (−636). `acceptance_record.py` is 758 lines, under
  `THRESHOLD`, so it opens no entry — the escape hatch working as documented.
  `bootstrap.py` **3,146 → 3,153** (+7), a reviewed bump: one MAPPING row and
  the six comment lines saying why the scaffold cannot skip it.
- `tests/test_complexity_ratchet.py`: `committed_snapshot_findings` (12)
  **RE-KEYED**, not re-stamped — the function is byte-identical and this file
  keys on (scripts-relative path, name), so a module move has to be spelled or
  the census reports the same 12 twice.
- `docs/stack.ini` `[smoke-budget] max-tests` **1367 → 1377**: the 8 new
  in-process boundary tests. The seconds budget is untouched at 60 and was not
  discussed — measured 22.9 s at the stamp.

### Spine, and the one approved cell that was not rewritten

Three LLR `Module` cells re-point and **no new spine row is minted** — a module
move re-points TRACED cells only (`WI-483` slice 2/3), and re-pointing already
contains the new module, so a mint would have added `Drafted` rows to the
owner's approval surface for nothing. `LLR-158` and `LLR-202` name
`acceptance_record.py` alone. **`LLR-178` names both**, on cause: its attested
rationale places the mirror invariant in `check_trajectory` "rather than in
`baseline_snapshot` because the writer must not also be the judge of its own
writes", and its detail says it joins the failure set at `check_trajectory`'s
main aggregation. Both stay literally true through the re-export, and rewriting
an `Approved` cell to tidy a diff is not a session's act.

`IF-091` (owner `LLR-158`, consumer `scripts/intake`) follows its owner and now
declares `acceptance_record -> intake`, which is the live edge. Verified live
through `check_trajectory.py --root . --strict`, which reported the containment
error before the re-point and the `intake -> check_trajectory` seam error before
`intake` was moved, and is **clean (exit 0, zero errors)** after both.

### One consolidation act inside a decomposition slice

`check_trajectory._git` was a **fourth** copy of `kitlib.git.git_out` that the
D-8/`OI-16` consolidation missed — the same body plus an optional `stdin`, which
is exactly why it was missed: the extra argument made it look like a different
function. `stdin` is now a parameter on `git_out` (default `None`, so every
existing two-argument call is byte-for-byte unaffected) and both modules alias
the one home, the idiom `check.py` already used. Taken here rather than filed
because the cut needed it: both halves of the split use it, and a private copy
in each would have been the duplication this kit forbids.

### M-06 rides nothing here, measured rather than assumed

The moved tier's tests live in `tests/test_trajectory_staged.py` (1,301) and
`tests/test_baseline_snapshot.py` (966) — neither is one of M-06's four
monoliths, and both drive the tier through the CLI or the re-exported API, so
neither needed to move. The four are re-measured for the record:
`test_integrate.py` **3,520**, `test_trace.py` **2,099**,
`test_trajectory_arch.py` **1,993** (1,927 at the `WI-483` close — it has grown
again, with nothing watching), `test_agent_loop.py` **1,640**. The sensor gap
stays CARRIED, not executed, per the row's §3.

fig: cmd="python -c \"import pathlib; [print(len(p.read_text(encoding='utf-8').splitlines()), p.name) for p in sorted(pathlib.Path('tests').rglob('*.py'))]\"" rev=c3bc6e07

### Deviations, and one accident

- **`intake.py` was re-pointed, which the slice did not originally plan.** The
  first design kept every caller on the shims. `check_trajectory --strict` then
  reported `intake (CMP-008) -> check_trajectory (CMP-006)` as an undeclared
  seam: `IF-091` had been covering that module pair, and it follows its owner
  `LLR-158` to the new module. Reading `intake` showed all three of its
  EXECUTABLE uses were inside the moved block (the two other mentions are
  docstrings), so re-pointing removed the edge rather than needing a new seam
  row. The better outcome, reached by the check rather than by planning.
- **An accident, recorded because a session that hides one teaches nothing.**
  The byte-identical harness drove `intake.py census` as if it were a read. It
  is not: it minted `WI-522`/`WI-523` and COMMITTED the whole working tree.
  Recovered with `git reset --mixed`, the two minted specs deleted, and
  `docs/id-watermark`, `docs/stage`, `docs/status.md`, `PROJECT_STATE.html` and
  `docs/requirements/components.derived.toml` restored to `c3bc6e07`. The
  watermark reads `WI = 521` again and no id was spent. The harness now drives
  `--help` on the subcommands, with the reason written at the site.
- **A pre-existing hole in the BATCHED full-suite protocol, found and not
  fixed here.** `tests/test_phase_rule.py` and `tests/test_pre_commit_hook.py`
  import `kitlib` at module scope and rely on another test module having put
  `project-trajectory/scripts` on `sys.path` first. Under a file-restricted
  `-n auto` batch that ordering is not guaranteed, and both error at import.
  Reproduced with those two files alone **at HEAD in a clean worktree**, so it
  is not this slice's doing; they pass in their own invocation (32 passed).
  Left as a finding rather than fixed inline.
- No byte-budgeted file was touched (`AGENTS.template.md`, `PROCESS.md`,
  `PROCESS_OPTIONS.md` all unchanged).

### Bar

Commit bar: `pytest -q -n auto -m smoke` **1363 passed, 6 skipped** in 19.8 s;
`check_smoke_budget.py --mode enforce` **24.6 s vs 60 s → within**;
`check_docs.py --root . --stale` OK (1094 docs, 1437 links, 0 broken).

Full unfiltered suite, batched at the smoke/slow boundary and summed against
`--collect-only` (3,073 = 1,369 smoke + 1,704 not-smoke):

| batch | result | wall |
| --- | --- | --- |
| `-m smoke` (1,369) | 1363 passed, 6 skipped | 19.8 s |
| `-m "not smoke"`, files 1–33 (905) | 902 passed, 3 skipped | 209.8 s |
| `-m "not smoke"`, files 34–66 (767) | 761 passed, 6 skipped | 357.6 s |
| the two `sys.path`-ordering modules (32) | 32 passed | 122.1 s |

`check_trajectory.py --root . --strict`: clean, exit 0.

### What remains on the row

The three other fusion heads (`agent_loop`, `agent_common`, `bootstrap`), the
rest of `check_trajectory` (4,327 lines, 5 fused pairs left, `main` still at
complexity 24), M-06's four monoliths, and the sensor gap. **The row stays
ACTIVE** — it is a standing debt owner, and the module-size ratchet's pointer
still names it.
