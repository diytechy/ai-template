## 2026-08-24 — WI-512: the interface `contract` stops restating its owner, and two new warn-first rules read what the old four could not

**Summary.** `OI-61`'s ruling executed in full: the 27 CLI-restatement `contract`
cells thinned to the typed crossing statement, the generated CLI reference
landed as (a)'s second step, (d)'s named-symbol tripwire folded in scoped to the
surviving prose, and the `VerifiedBy` seam-tier pointer sanctioned warn-first.
The number the ruling asked back for is below, and it is the input to whether
(b) runs across the other 108 rows and to whether (c) re-opens.

### The census, RE-MEASURED on the live registry

`WI-455` moved the schema under this brief between its writing and its
execution, so the census was re-run before anything was designed. **The row set
holds exactly; the row SHAPE moved.** 135 live rows, 27 carrying `CLI:`, the
same 27 ids, the same owner split (9 `SR-###` / 18 `LLR-###`), the same seven
`B-05` ties, the same four over-ceiling breaches (`IF-121` 587, `IF-015` 722,
`IF-044` 788, `IF-103` 800), the same length distribution (min 128, median 180,
mean 273.5, max 800). What changed: `direction` / `this_project` / `counterpart`
are gone, so "seven whose counterpart is `external:`" now reads as seven whose
`consumers` list is `external:downstream adopter`; and `provider` survives on
only 9 of the 27, the other 18 deriving it from a design-tier owner. The brief's
"26 of 27 open `<module>.py CLI:`" was not re-derivable as stated — 22 of 27
open on a literal `<module>.py CLI:`, the rest opening on a library-or-CLI
phrase — which changed nothing about the pass, since it was reviewed per row.

<!-- fig: cmd="python -c \"import tomllib,statistics; d=tomllib.load(open('docs/requirements/interfaces.toml','rb'))['interface']\"" rev=3cf43e2e -->

### THE NUMBER

The measurement the owner's *"let's see where it lands"* asks for, and the
condition (c)'s deferral is written against.

| | before | after |
|---|---|---|
| rows | 27 | 27 |
| total characters | **7,385** | **2,613** |
| min / median / mean / max | 128 / 180 / 273.5 / 800 | 54 / 70 / 96.8 / 220 |
| over the ruled 500-char ceiling | 4 | **0** |

**−4,772 characters, −64.6%.** Of the 2,613 that survive, **1,705 is the pure
crossing statement** and **908 characters over 11 rows is the IRREDUCIBLE
REMAINDER** — clauses carrying a typed fact the owner row does not state.
**Sixteen of the 27 rows thinned to the crossing statement with nothing left
over at all.**

Read as the owner's question — *how much of what those 27 cells said turns out
to be missed by any reader once it is gone* — the answer is **908 of 7,385
characters, 12.3%**. The other 87.7% was recoverable from the owner row, the
module, or the generated CLI reference, all three of which a check holds to the
code. That is the trial (a) was ruled to run, and it says (b) is worth running
across the other 108 rows — with the same per-row review, since one row in
seven carried something real.

<!-- fig: cmd="python project-trajectory/scripts/trace.py --root . --strict-integrity" rev=3cf43e2e -->

### The dossier — every row, reviewed, never regexed

`old` and `new` are `contract` characters. "Displaced content's home" names
where the deleted detail already lived; a **kept** row names the clause that
survived and why no other home states it.

| row | old | new | displaced content's new home |
|---|---|---|---|
| `IF-001` | 219 | 85 | `SR-157` (the gating rule) + `trace.py` argparse. **KEPT (37):** *writes `docs/test/report.md`* — a written artifact is a crossing, and no owner cell names it. |
| `IF-002` | 143 | 57 | `LLR-012` `detail` states `--stale` and all three failure classes verbatim. |
| `IF-003` | 140 | 58 | `LLR-013` `detail` + `check_flows.py` argparse. |
| `IF-004` | 133 | 57 | `LLR-014` `detail` states the tolerance/block-level rule. |
| `IF-005` | 142 | 151 | `SR-017`. **KEPT (95):** the always-on floor vs the `docs/privacy-check`-gated identity/PII classes — SR-017 names the `secrets_scan` dial, not the gating file. (The one row that grew: the SR states the floor, not the two-tier split.) |
| `IF-006` | 128 | 58 | `LLR-016` `detail`. |
| `IF-008` | 155 | 61 | `LLR-038` `detail` (a strict superset, down to `--strict`). |
| `IF-009` | 164 | 163 | `SR-157`. **KEPT (104):** the R-A-always / R-B..R-E-under-`--strict` / connectivity-never split — a severity ladder no owner cell carries. |
| `IF-010` | 329 | 220 | `LLR-023` `detail` (the splice + drift half). **KEPT (151):** the LIBRARY seam — `scan_inventory()` as the one AST harvest its readers consume. Not a CLI restatement at all. |
| `IF-011` | 142 | 114 | `SR-070`. **KEPT (57):** the git as-of line's exclusion from the byte compare — an exclusion in a comparison, stated nowhere else. |
| `IF-012` | 133 | 54 | `LLR-039` `detail` (states `--check`'s three trips AND the dial that silences it). |
| `IF-013` | 203 | 65 | `SR-006` — the row's own `notes` already recorded that the contract *"restates SR-006's own requirement text almost verbatim"*. |
| `IF-014` | 180 | 129 | `SR-010`. **KEPT (67):** idempotence without `--force`, and the kit-version stamp. |
| `IF-015` | 722 | 189 | `SR-026` + `agent_loop.py` argparse (the four role flags and their help). **KEPT (118):** the plain-launch drive cycle, *never pushes*, and the per-checkout lock's refusal — two fail-loud guarantees. |
| `IF-016` | 131 | 105 | `LLR-022` `detail`. **KEPT (29):** network-gated, warn-first — a posture the terse owner cell omits. |
| `IF-017` | 135 | 70 | `LLR-024` `detail` (the grammar) + the `--spec` help string. |
| `IF-018` | 147 | 82 | `LLR-033` `detail`. |
| `IF-019` | 133 | 63 | `LLR-025` `detail`. |
| `IF-044` | 788 | 156 | `SR-154` + the module's own public surface (the derived architecture's inventory). **KEPT (90):** selection is PURE and returns its reason as data, the coordinator owning every launch. |
| `IF-046` | 296 | 72 | `LLR-046` `detail`. |
| `IF-048` | 260 | 69 | `LLR-047` `detail` — a verbatim superset, exit-code passthrough included. |
| `IF-053` | 421 | 159 | `SR-148` (the selection order). **KEPT (95):** pure and side-effect-free. **ROT REMOVED:** the old cell named *"the dispatcher (Slice D)"*, deleted at concurrency-restructure Phase 5. |
| `IF-069` | 219 | 61 | `LLR-098` `detail`. |
| `IF-086` | 306 | 60 | `LLR-146` `detail` (a superset, `--strict` ladder included). |
| `IF-103` | 800 | 124 | `LLR-165` `detail`. **KEPT (65):** a lossy conversion refuses to write with or without `--check` — the CLI's refusal, where the owner states only that the caller decides. |
| `IF-121` | 587 | 62 | `LLR-170` `detail` (a superset, the wiring-without-`--strict` note included). |
| `IF-139` | 229 | 61 | `LLR-199` `detail`. |

**Fourteen `signal_note` cells were re-typed by hand in the same pass**, and
that was forced rather than opportunistic: each carried the boilerplate
*"DERIVED, NOT HAND-TYPED … re-type it by hand when this row is next touched"*,
and the derivation named prose this pass deleted — leaving it would have left a
cell asserting something demonstrably false. Every one stays `variable`; each
now says WHAT unbounded thing crosses.

### (a) step two — the generated CLI reference LANDED

The ruling's staging puts it on this row (*"the GENERATED CLI reference derived
from each module's argparse rides along as (a)'s second step … not as a separate
row"*), so it is built, not deferred.

`gen_arch_map.py` gains **`--cli-doc FILE`** (repeatable, honours `--check`): an
AST read of every scanned module's `argparse` tree — never an import, so
documenting a shipped script does not run it — rendered as a per-module summary,
its declared `Contracts: IF-###` line and a flag/help table, spliced into a
`<!-- BEGIN GENERATED CLI REFERENCE -->` pair. It is its own mode, returning
before `main()`'s `--doc`/MODULE MAP contract, and that is the load-bearing
design decision: the committed module map RETIRED at `WI-455`, so a target that
demanded one would force a repo to re-commit the artifact a ruling deleted.

It landed with the four things a generated artifact owes, in one change:
`docs/cli-reference.md` (the doc), the `[generated]` row of kind `cli`,
`check.py`'s `cli-reference` step (in `BUILTIN_STEP_NAMES`, in the pre-commit
floor, and in `_TRUNK_FRESHNESS_STEPS`), and `trunk_step.py --regen`'s table.
The last two go together deliberately: standing a step down on a work branch is
only honest when the trunk can regenerate it, which is the rule `skills-index`
and `prompt-catalog` fail and stay out for.

The `Contracts:` line is what makes it a REFERENCE for the registry rather than
a second document beside it — a cell that now says only *"SR-006's obligation
delivered as a CLI at check.py"* is one generated hop from the flags.

### (d)'s tripwire — and it caught the exhibit unplanted

A fifth rule in `trace.if_contract_advisories`, warn-first, reusing
`gen_arch_map.implements_report` (the one AST walk, per `WI-486`): a
`SCHED_*` / `Foo.bar` / `CONSTANT_NAME` token must resolve in the declared
source surface, and a path whose first segment is a real directory must exist.

**The acceptance case passed against the live tree, not a fixture:** the first
run reported `IF IF-055 Contract names SCHED_* — no such symbol exists in the
declared source surface`. It is also driven both ways on a planted tree
(`tests/test_trace_rules.py`), because a rule that only ever fires on one live
row is a rule nobody has shown can go quiet.

**Initial live count: 7 findings over 5 rows** (none of them among the 27 this
pass rewrote):

| row | token | reading |
|---|---|---|
| `IF-055` | `SCHED_*` | **REAL ROT** — the exhibit the rule was ruled for. |
| `IF-038` | `SUBAGENT_GATE` | an ENV VAR name, not a symbol — a judgement call for whoever next touches the row. |
| `IF-072` | `SCAFFOLD_OMISSIONS` | a name that lives in `tests/`, outside the declared source surface. |
| `IF-061` | `docs/plans/DP-NNN-` | a template pattern, not a path. |
| `IF-132` | `registries/source` | names nothing in the tree. |
| `IF-143` | `scripts/x`, `project-trajectory/scripts/x.py` | placeholder paths in a worked example. |

They are left standing on purpose: re-authoring rows outside the CLI family is
(b)'s pass, deliberately deferred, and this row was ruled not to run it.

**The narrowing is the design, and it was measured.** The un-narrowed rule
reported **39** findings; four false-positive classes were then declined
outright — another library's symbols (`csv.DictReader`, `sys.executable`), the
registry's own column notation (`TC.Evidence`, `LLR.Module`), English slashes
(`identity/PII`, `claim/work/merge`) and a filename read as an attribute
(`trace.py`) — plus `docs/declared-absences` honoured for paths. **39 → 7, and
`SCHED_*` survived every narrowing.** Vacuous — silent — where there is no
surface to read, because an empty surface would report every name in the
registry as dead.

### `VerifiedBy` — sanctioned, shipped, unclaimed

The optional IF cell taking a `TC-###` or an `LLR-###`; **empty means "verified
in its own right"**, which is the ordinary case. Warn-first that the pointer
resolves, and nothing more: whether the named test really exercises the seam is
a judgement no grammar reads. It is the smallest honest mechanism for a position
that was previously UNSAYABLE — `Verification`'s one exemption is LLR-exemption
on an SR, `PROCESS.md` says every SR needs a TC regardless of method, and an IF
row carries no `Verification` cell at all.

**No live row here claims it, and that is deliberate**: filling one would be
inventing a per-row judgement this row was not asked to make. The mechanism
ships documented (template, `INTERFACES.template.md`, `PROCESS.md` §8,
`EXAMPLE.md`) with the example row demonstrating it, so an adopter can say the
true thing on day one.

### Deviations from spec

- **The `signal_note` re-typing** (14 cells) is not in `WI-512`'s spec. It is
  forced by the pass rather than added to it — see the dossier's note.
- **The census's "26 of 27" figure was refuted** (22 of 27) and recorded rather
  than repeated.
- **`IF-005` GREW** by 9 characters. The rule is "state the crossing and stop",
  not "make every cell shorter"; the two-tier floor/gated split is a typed fact
  the SR does not carry.
- **`trace.py` took a reviewed +229-line bump rather than a decomposition**, and
  the alternative considered (moving the pure token grammar to `trace_text.py`)
  is written into the ratchet entry with the reason it was declined.
- **`gen_arch_map.py` crossed the 1,500-line monolith threshold** and earns its
  first baseline entry.

### Gates

- `python -m pytest -q -n auto -m smoke` → **1317 passed, 5 skipped in 17.92s**;
  `check_smoke_budget.py --mode enforce` → **21.9s vs 60s budget → within**.
- `trace.py --strict-integrity` → `integrity=0 interface-findings=0`,
  `interfaces=135`.
- `check_trajectory.py --root . --strict` → clean (509 work items, graph acyclic).
- `check_docs.py --root . --stale` → 1052 docs, 1365 links, **0 broken**.
- `python -m pytest -q -n auto --basetemp=D:\pytest-tmp-w512` → **3004 passed,
  14 skipped in 1020.58s (0:17:00)**. The run before it caught one real defect
  this close introduced — the ruling fragment's link to the WI spec, broken by
  moving the spec to its terminal folder — re-pointed and re-driven green.
- `check_vocab.py --root . --strict` → clean (433 live authored files);
  `ruff format --check` → 215 files already formatted.

<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=3cf43e2e -->
<!-- fig: cmd="python -m pytest -q -n auto" rev=3cf43e2e -->

### Byte deltas on budgeted files

- `project-trajectory/PROCESS.md` **watched**: 85,984 → 86,676 (**+692**) — §8
  gains the `VerifiedBy` clause, the fifth `Contract` rule and the
  no-restatement instruction. Flagged; the skill's row is re-stamped.
- `AGENTS.template.md` (capped 10,000) and `CLAUDE.md`: unchanged.

Deferred open items: none — the ruling this row executes is already ruled, and
nothing here owes the owner a fresh decision.

**Option (c) is NOT re-raised here, and the condition is now
partly met rather than fully:** (a) has landed and (d) is reporting, but the
third clause — *a residual rot class demonstrated that neither reached* — needs
(d)'s findings to be triaged before it can be claimed. `IF-080`'s class (a
true-looking English phrase naming nothing symbolic) is still the standing
candidate and is still live and still unreached by anything shipped here; that
is a demonstration waiting for whoever runs (b), not a claim this row is
entitled to make.
