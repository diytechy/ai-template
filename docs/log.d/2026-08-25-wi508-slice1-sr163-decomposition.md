## 2026-08-25 — WI-508 slice 1: the row re-validated, the lane claimed, and `SR-163` decomposed

**Summary.** The architectural remapping program opens with the act its own
spec names first: the requirement the remap is the verification exercise FOR is
now traced. `SR-163` mints `LLR-203`/`TC-199` and `LLR-204`/`TC-200`, all four
`Drafted`, and leaves the orphan list — the debt is down to `SR-181` alone. The
row's two staleness warnings were READ rather than cleared by the touch, and
both re-validate: the cited requirement's only amendment is a lens, and its
SpecRef file's only change is four open items that do not retask this program.
**No purpose-coverage checker was built and no module or symbol was invented to
cite** — the honest state is that the mechanism is unbuilt, and both design rows
say so on the row rather than in this fragment.

Deferred open items: none — nothing here needed a ruling. `OI-63` was read for
context because it landed in this row's SpecRef file three days after the row
was minted, and it is explicitly NOT this row's to execute.

### The re-validation, and what it actually found

`check_trajectory --strict` carried three warnings naming `WI-508`. All three
are gone, and two of them by measurement rather than by touching the file:

| warning | what reading it found |
| --- | --- |
| cites `SR-163` amended after the row was last touched | The amendment is `hat_refs = ["MAINTAINER"]`, added by the perspective backfill. `requirement`, `rationale` and `acceptance_criteria` are **byte-identical** to the text the row was minted against. |
| its SpecRef `open-items.toml` changed after the row was last touched | `OI-58`'s own row last changed when it was ruled — **before** this row's last touch. The warning is file-level; what changed is `OI-60`…`OI-63` arriving. |
| `Title` over 120 characters (138) | Trimmed to 108 by dropping the trailing ruling citation, which `specref` and the spec's Context already carry. The filename is unchanged, so no link moved. |

fig: cmd="git log -L 779,791:docs/requirements/system-requirements.toml --max-count=2 ; git log --format='%h %ai' -1 e6dc86a0 e8e24459 ; git log -L 2185,2199:docs/requirements/open-items.toml --max-count=2" rev=3b2156dc

The amendment is not neutral for this program, which is why it is recorded
rather than dismissed. `MAINTAINER` asks *"can a reader two years from now tell
why this exists, and what would break if they deleted it?"* — the remap's own
question, asked of a module instead of a row. It sharpens the derivation brief;
it does not redirect it.

### The decomposition, and the discipline it follows

The shape is the one the stray-orphan decomposition established: **name the
real, already-delivered mechanism, and state plainly what does not exist** —
never a fabricated checker with a plausible-sounding symbol.

- **`LLR-203`** — *the shipped-file inventory and its declared exclusions,
  carrying no purpose reference.* `project-trajectory/scripts/bootstrap.py`,
  symbol `MAPPING`, `CMP-009`. Two of the parent's four finding classes are
  already delivered and already driven. The dogfood direction: the
  scaffold-coverage walk reports a declared destination this repository neither
  carries, serves in place out of the kit tree, nor declares as an absence, and
  its honesty half reports a declared absence that has since materialized, so
  the exclusion list can only shrink. The package direction, asked of a REAL
  scaffold because the kit's own `scripts/` holds every file: the copied helper
  package must be exactly the kit's module set, naming a missing or stale
  `MAPPING` row as the cause, and a shipped script importing a file the
  inventory omits is reported off the `MAPPING` literal read as an AST.
  `docs/declared-absences` is the recorded-exclusions carrier.
- **`TC-199`** — Integration / Full, verifying `SR-163` + `LLR-203`. Evidence
  is **5 EXISTING node ids**: `tests/test_dogfood_sync.py`'s walk, its
  stale-entry honesty half and its bite proof (remove one declared entry and
  its destination must reappear in the finding set), plus
  `tests/test_bootstrap.py`'s package-completeness and sibling-import-closure
  checks.
- **`LLR-204`** — *the purpose-reference grammar and its declared warn-to-gate
  dial, running the other direction.*
  `project-trajectory/scripts/gen_arch_map.py`, symbols
  `backlink_ids/scan_backlinks/read_backlink_min`, `CMP-006`. `backlink_ids` is
  the ONE definition of a purpose declaration in the source surface, shared by
  the map's column and the coverage percentage so the two cannot disagree; and
  the declared threshold delivers exactly the warning-to-gating shape the
  parent's fourth clause asks for — warn at exit zero, gate only on the strict
  arm the harness appends from the tests rung onward.
- **`TC-200`** — Integration / Full, verifying `SR-163` + `LLR-204`. Evidence
  is **2 EXISTING node ids** in `tests/test_gen_arch_map.py`: the grammar driven
  directly on the shared function, and the warn-then-gate exit contract driven
  through the real command line on a real scaffold.

**Every one of the seven cited node ids was collected before it was written
into a cell**, rather than trusted from a grep.

fig: cmd="python -m pytest -q --collect-only <the 7 node ids in TC-199 and TC-200>" rev=3b2156dc

### What the two rows say is NOT DISCHARGED — the load-bearing half

A design row that named only the delivered arms would read as though the
obligation were met, and the next reviser would have to re-derive the gaps by
inspection. So they are on the rows:

1. **No cell joins an inventoried file to a requirement id.** A `MAPPING` row is
   a source/destination pair plus a comment; the purpose is prose a reader
   interprets and no check resolves.
2. **Every delivered arm walks the inventory's declared DESTINATIONS, not the
   shipped tree** — so a kit file the inventory omits altogether is outside all
   of them.
3. **The installer's own exclusion is prose at its module**, not a row in the
   exclusion carrier — the one exclusion load-bearing for the distribution model
   is the one nobody can enumerate mechanically.
4. **The coverage report runs the INVERSE direction.** It asks whether each live
   design row is named by some source declaration; the parent asks whether each
   shipped file names a requirement. A full reading on one side is compatible
   with a tree in which no file declares anything.
5. **Its universe is the declared source paths** (`[paths] src =
   project-trajectory/scripts`), so the grammar never sees a template, registry
   seed, launcher, workflow or process document — the greater part of the
   inventory.

### Why the framing act comes first, stated so the next slice does not re-derive it

The blind agent is asked for the minimal set of modules that serves the declared
outputs. `SR-163` is the row that says every shipped file must be traceable to a
stakeholder outcome — so **the derivation's output IS evidence for that row**,
and gaps 4 and 5 above are precisely the missing side of a join the registry
already half-carries. Without the decomposition the remap would be a
free-standing opinion about layout; with it, the exercise has a requirement it
answers to.

### Counts

Orphans **4 → 2** (`SR-163`'s two are discharged; `SR-181`'s two remain, owned
elsewhere). `integrity=0` unchanged. Drafts **0 → 4** — the ordinary consequence
of a mint, and it moves no rung: `docs/stage` reads `DevStg-LLReqs` before and
after, per-phase byte-identical apart from the draft count and the fingerprint.
Watermarks `LLR` 202 → 204, `TC` 198 → 200.

fig: cmd="python project-trajectory/scripts/trace.py --root . --strict ; python project-trajectory/scripts/derive_stage.py --root . --check" rev=3b2156dc-dirty

### Gates

```
python -m pytest -q -n auto -m smoke        -> 1327 passed, 5 skipped in 54.59s  [cold, first run of the session]
python scripts/check_smoke_budget.py --mode enforce
                                            -> 1327 passed, 5 skipped in 22.76s
                                               23.2s vs 60s budget -> within     [warm]
python project-trajectory/scripts/check_docs.py --root . --stale
                                            -> OK, 0 broken links
python project-trajectory/scripts/check_trajectory.py --root . --strict
                                            -> clean (515 WIs, 491 done, graph acyclic); all three WI-508 warnings gone
python project-trajectory/scripts/trace.py --root . --strict
                                            -> integrity=0, orphans=2, drafts=4
```
fig: cmd="each command as written above, run in this order on this tree" rev=3b2156dc-dirty

**The full unfiltered suite is NOT claimed for this slice, and the reason is the
scope.** Nothing executable changed: the diff is registry TOML, the WI spec, the
working surface, this fragment, and the five regenerated artifacts that follow
from them. That is the same class the stray-orphan decomposition recorded when
it declined the full run for registry-only work. The smoke tier ran in full and
the four generated-artifact freshness gates were re-run to `--check` clean.

### Regenerated, because four rows changed the derived surfaces

`docs/requirements/components.derived.toml` (two new `Component` tags),
`docs/stage` (draft count + fingerprint), `PROJECT_STATE.html`,
`docs/status.md`'s generated block, `docs/open-items.html`, and
`docs/ratify/CURRENT.md` — the `approval-fresh` step caught that one, which is
the mechanism working: a mint puts a section on the owner's reading surface, and
the brief that is stale is one an owner could bless without having been shown
what they were blessing. The brief now carries **one section, `SR-163`**, with
the four new rows rendered in full because a `Drafted` row owes a first
approval rather than a re-attestation.

**OWNER-OWED, and deliberately not taken here:** blessing those four rows.
`intake.py snapshot` was NOT run and no `Status` cell was flipped — the last
commit to move one in a snapshotted registry is still the 2026-08-24 approval,
which the brief's own provenance line states.

### Deviations, and one thing deliberately left

- **`hat_refs` is EMPTY on both LLRs, deliberately.** A design row's own cell
  holds only what its OWN decomposition raised, never a copy of its parent's —
  the effective set derives `MAINTAINER` down from `SR-163` already. The one
  candidate considered and declined was `TEST-ENGINEER` ("an obligation with no
  enforcer"): these rows *record* a missing enforcer, they do not prevent one
  from being missing, and attributing on that reading would put a name in every
  cell that describes a gap.
- **`docs/status.md`'s "`drafted = 0`" sentence was corrected, not deleted.** It
  was a true statement about a dated approval act and is false as a present
  reading, so it now says the count *was taken to* zero; the four new drafts are
  named in the lane's own bullet, which is where a reader is told what happens
  next.
- **Pre-existing and NOT introduced here:** `check_docs` warns
  `docs/test/report.md` is a live orphan. It is gitignored generated output that
  exists only because `trace.py` ran in this session; it is a WARN, not part of
  the FAIL verdict, and no allow-file entry was added for it (editing a declared
  list to quiet a finding is accepting what it measures, and nothing here needs
  quieting).
