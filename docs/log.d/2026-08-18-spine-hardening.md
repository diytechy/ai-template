## 2026-08-18h — Two silent-green spine defects closed, and the `interfaces.csv` sweep the previous lane filed

**Why.** The scripts sweep (`docs/log.d/2026-08-18-scripts-sweep.md`) filed three
findings it deliberately did not act on, and a read of the enum floor while
discharging them turned up two live defects of the same class: a rule that is
*declared* but reads nothing, and a predicate whose unrecognized-value branch
returns the **unsafe** answer instead of reporting. Neither fails loudly. Both
make a surface a human is expected to trust say the wrong thing quietly.

**Defect 1 — the SN tier was outside the always-on enum floor.**
`trace.ENUM_FIELDS["SN"]["Status"]` was added on 2026-08-17k, but `analyze()`
built `raw = {"SR": …, "LLR": …, "TC": …}` and folded `enum_integrity_findings`
over *that* dict only. The need tier was never in it, so `status = "Bananas"` on
a stakeholder need produced **no finding at any bar** — the same
declared-and-read-by-nothing shape the LLR tier's own comment records one level
down, arriving again one level up.

- `load_registries` now projects the needs into the `SN-ID` / `Status` shape the
  other tiers carry (`reg.raw_sns`), and `analyze()` folds SN in beside `raw`.
  Deliberately *beside* and not *into*: `raw` also feeds the id-integrity and
  placeholder sweeps, and the need tier already owns those through
  `sn_integrity_findings`, which reads the registry as PROSE because a bare
  `SN-###` token in a paragraph is part of that tier's id universe.
- **Not** `spine_carrier.folded_needs`, which was the obvious carrier and is the
  trap: that fold projects onto `SN_CORE`, which has no `status` key at all, so
  a Status check reading it would have seen a blank cell on every row and passed
  vacuously — a green built out of the *fix*. `load_needs` is the honest read
  and the comment in place says why.
- Measured before/after on the same planted tree (a scaffold re-homed on the
  TOML need carrier with one `status = "Bananas"` row): **before**
  `integrity=0`, exit 0 under `--strict-integrity`; **after** `SN SN-001 has
  Status='Bananas', which is not in the closed vocabulary (allowed: Approved,
  Drafted, Modified)`, exit 1. Regression test:
  `tests/test_trace.py::test_sn_status_outside_the_closed_vocabulary_is_an_integrity_finding`
  plus its clean-row twin over all three live vocabulary words.

**Defect 2 — casing decided a maturity.** `spine_carrier.is_draft_need`
compared `str(need.get("status","")).strip() == "Drafted"` **exactly**, while
`trace.is_drafted` / `is_approved` / `is_modified` all lower the cell first (the
one Status-casing rule, process.md §4). The asymmetry failed in the unsafe
direction: this predicate does not *report* an unrecognized value, it returns
`False`, and `False` here means **ratified** — so a need written `drafted`
silently floated the derived gate upward, which is the exact failure
`is_draft_need`'s own docstring says the SN tier can least afford.

- Now `.strip().lower() == "drafted"`. Semantics preserved: closure is still
  enforced, by defect 1's `enum_integrity_findings`, which *reports* an
  out-of-vocabulary word instead of reading it as a maturity — the right
  instrument for that job.
- A grep for the sibling shape (`== "Drafted" | "Approved" | "Modified"`) across
  `spine_carrier.py` found **no other Status read**: line 852 writes the word
  from a markdown heading kind, and line 794 is a default. Nothing else to
  align.
- `tests/test_spine_carrier.py::test_draft_need_ids_reads_STATUS_and_nothing_else`
  **asserted the defect** ("the word is closed and case-sensitive… `drafted` is
  an unrecognized value"). That line is inverted, with the reasoning recorded
  beside it, and joined by a whitespace/upper case and two negative cases
  (`draft` is still a different word).

**Defect 3 — the `Contracts:` boilerplate sweep (the filed finding, discharged).**
`interfaces.csv` appeared in **45 places across 45 script modules**; the row of
record is `interfaces.toml` (`docs/declared-absences:37`). Classified per file
rather than swept blind:

- **40 modules — mechanically retired.** The one-per-module `Contracts: IF-###
  … rows of record in docs/requirements/interfaces.csv` boilerplate, matched on
  the `of record in docs/requirements/` clause so nothing else could be caught.
- **5 further boilerplate lines** in the modules that mention the token more
  than once (`trace.py`, `check_trajectory.py`, `gen_arch_map.py`,
  `plan_coverage.py`, `migrate_carrier.py`) — same retirement.
- **7 prose mentions describing the LIVE read — corrected**, because each was
  factually wrong about today's behaviour, not a legacy reference:
  `check_trajectory.py` ×4 (the opt-out/default-on posture at the module
  docstring, `read_interfaces_check_enabled`, `interface_findings`, and the lazy
  `covered` comment — all four modules read `interfaces.toml` today, `IF_CSV`
  at `:166` already points at it), `gen_arch_map.build_dependency_diagram`'s
  `if_rows` source, `plan_coverage.py` ×2 (the parsed contract and the
  no-such-row finding — `plan_coverage.py:346` loads `interfaces.toml`), and
  `trace.py`'s "trace already loads `interfaces.csv`, so the join is free".
- **2 mentions REWORDED rather than token-swapped**, because a swap would have
  produced a new false statement: `trace.py`'s "trace.py has read
  interfaces.csv **since WI-056**" is a historical claim (the carrier moved at
  WI-443), so it now names the *tier* — "has read the IF registry since
  WI-056" — which is true across both carriers; and the CSV structure sweep's
  worked example, which named `interfaces.csv` as "a registry this script never
  joins" and was wrong twice over (the tier moved to TOML, which that `*.csv`
  glob cannot see, *and* the tier IS joined now via `raw_ifs`). The example is
  dropped rather than re-spelled — a sweep that guards CSVs cannot illustrate
  itself with a TOML.
- **3 mentions LEFT, genuinely legacy/migration:**
  `gen_arch_map.load_interfaces` ("a repo that has not migrated off
  `interfaces.csv` still resolves" — that is the dual-carrier promise),
  `migrate_carrier.py:67` (the WI-443 sequencing note, history), and
  `migrate_carrier.OFFSPINE`'s `"docs/requirements/interfaces.csv"` key, which
  is the conversion **source** path and must keep naming the CSV.
- `docs/declared-absences:37` is untouched and still earns its place: the
  converter names the CSV in code, and pre-2026-08-13 prose keeps its token by
  that row's own rule.

**Defect 4 — `staged_findings` described a carrier it no longer reads.** The
filed finding asked whether `:3128`'s "Compares the staged WI CSV against its
HEAD version via git" matched `_staged_wi_registry`. It does not:
`_staged_wi_registry` → `_staged_spec_registry` reads **name listings**
(`git diff --cached --name-status` for the staged side, `ls-tree` at HEAD), and
a status change in the folder registry **is a rename** between status
directories — no row is parsed anywhere, so the companion claim that
"line-splitting the HEAD CSV is safe" describes nothing. Both corrected. The
WI-349 block comment at `:745` **quoted that sentence verbatim** as its own
premise, so it is corrected too rather than left dangling; what survives there
(and is now what it says) is the C0-control half — a cell being *text at all*,
the `9e2008a` backspace case — which no carrier change touches. `main()` had
already recorded the physical-line retirement where the WI rows are loaded; the
two homes now agree.

**Defect 5 — a quoted docstring that had moved.**
`docs/registry-machinery-reference.md` §12.2 quoted `check.py` as saying "the
`Tier` column in test-cases.csv is the registry source of truth". Verified
against the live `check.py:36` and updated to the exact current wording: "the
`Tier` field in test-cases.toml is the registry source of truth". The §12.2
argument (registry Tier and pytest marker are unreconciled) is unchanged — only
the quote.

**Regenerated.** `docs/architecture.md` via `gen_arch_map.py --strict-parse
--src project-trajectory/scripts` — **no change from this lane**, as expected:
the arch map extracts the IF *ids* from a `Contracts:` line, never the registry
path, so retiring the token cannot move it. (The two rows that differ in the
working tree are the scripts-sweep lane's, already generated by it.)

**Ratchet.** Two reviewed baseline bumps, both mine, both re-stamped in
`tests/test_module_size_ratchet.py` with their reasons: `trace.py` 4239 → 4272
(+33, the SN enum wiring plus the two comments that could not be token-swapped)
and `check_trajectory.py` 4169 → 4177 (+8, the corrected staged-close mechanism
in its two homes). `bootstrap.py` 2865 → 2878 is the concurrent
`docs/work/README.md` lane's and is **not** re-stamped here.

**Verification.**

```
$ ./.venv/bin/python -m pytest -q tests/test_trace.py tests/test_trace_rules.py \
    tests/test_spine_carrier.py tests/test_gen_arch_map.py \
    tests/test_generated_freshness_wiring.py tests/test_check_doc_refs.py
196 passed in 101.85s (0:01:41)

$ ./.venv/bin/python -m pytest -q -n auto tests/test_plan_coverage.py \
    tests/test_migrate_carrier.py tests/test_dogfood_sync.py tests/test_check_docs.py \
    tests/test_trace_briefs.py tests/test_check_harness.py tests/test_derive_gate.py \
    tests/test_check_need_form.py tests/test_gen_okf.py tests/test_hats.py
278 passed, 2 skipped in 53.16s

$ ./.venv/bin/python -m pytest -q tests/test_rule_sync.py tests/test_check_docs.py
100 passed in 58.97s

$ ./.venv/bin/ruff format --check <the 8 files edited>
8 files already formatted
```

`ruff check` on the edited scripts reports only the three pre-existing `F841`s
at `trace.py:3878` (`exts`/`bifs`/`rels`), outside this lane's hunks — the same
three the previous lane recorded at their pre-edit line number.

`trace.py --strict-integrity --root .` on the live repo: `SN=27 … integrity=0`,
exit 0 — all 27 of the kit's own needs carry a vocabulary Status, so the new
floor arms without a migration.

**Reported, not changed.**

- `check_trajectory.IF_CSV` (`:166`) is a constant named `*_CSV` whose value is
  `docs/requirements/interfaces.toml`. Same class of stale-carrier naming as the
  prose swept above, but a rename touches call sites, so it is a finding rather
  than a drive-by.
- `tests/test_module_size_ratchet.py` fails on `bootstrap.py 2865 -> now 2878`
  from the concurrent `docs/work/README.md` lane — that lane's re-stamp to make.
