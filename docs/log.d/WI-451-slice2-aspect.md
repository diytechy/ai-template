## 2026-08-14 — WI-451 slice 2, act 5: `SR.Area` retires for the closed `Aspect` vocabulary (owner ruling `2026-08-14h`)

**The ruling (owner, in session).** Asked whether the Area→aspect conversion
should ride this window or wait — since the vocabulary is *provisional* and
sitting-2 decision 10 says it re-ratifies "on re-derived numbers", and those
numbers had just moved hard (the registry it was sized against was 148 rows
and is now 64) — the owner ruled **convert now**. Recorded because the
alternative was live: waiting would have meant a second full-registry touch
for a column already being rewritten in this one.

**It is not a rename, and that is the whole point.** Decision 10's own
measurement: of the 31 `Area` values, **25 were a component by another name**
(derivable from the decomposition, therefore redundant) and only **6 spanned
components** — which is what an aspect IS, a cross-cutting concern no
partition can express. So the conversion **DROPS** the derivable values rather
than remapping them. Verified against the ruling's own fingerprint before
executing anything: the six name-matched values carry **exactly 65 of the 147**
base rows, the figure decision 10 states — which is what made the mapping
certain rather than inferred from name resemblance.
<!-- fig: cmd="python - # tomllib over `git show ad0d0456:docs/requirements/system-requirements.toml`; sum the six name-matched Area values -> 65" rev=ad0d0456 -->

**On the re-tiered registry: 21 of 64 rows keep an aspect, 42 drop the cell**
(`process` 7 · `trajectory` 6 · `portability` 3 · `unattended-loop` 3 ·
`connectivity` 1 · `perf` 1). That sparseness is the ruled end state, not data
loss — the ruling says so in its own words: *"Portability's homelessness is not
a defect."*

**The vocabulary is CLOSED, and now enforced rather than merely declared.**
`ENUM_FIELDS` gains `Aspect`, so a non-empty out-of-vocabulary value is a schema
finding naming the row and the allowed set — reported at the schema tier,
gating under `--strict`, the same severity contract its `Verification`/`Tier`
siblings carry — while a **blank cell is never a finding**. Both directions are
driven by new bite tests; a checker that demanded a value on every row would
push authors straight back to inventing component-shaped ones, which is the
defect the ruling diagnosed. **This is NOT the D-9/D12 Status vocabulary**,
which stays held for its own atomic act (`2026-08-14e`).

**Schema touched end to end:** `spine_carrier`'s key→column map and the SR
tier's declared key set, `migrate_carrier`'s inverse (the `test_rule_sync`
pin), `check_trajectory`'s traced cells, `gen_okf`'s fact row, `trace.py`'s
per-aspect report section, and the **shipped template** — which now states the
closed set, since an author cannot honour a vocabulary the template does not
name. Adopters get a `RESYNC_PACK` entry (`[since 9861e957]`) that spells out
the drop-don't-remap rule, because a downstream repo doing a mechanical rename
would preserve exactly the redundancy this retires. `trace.py` baseline
re-stamped 3833 → 3853 (reviewed bump, the vocabulary block plus the reasoning
that makes it readable). Goldens regenerated deliberately: 4 lines, all rename.

**Four tests the smoke tier hid were caught by the full suite** before
committing — the fixture column, the template pin, the golden report section
and the staged traced-cells set. That is act 4's lesson applied rather than
merely recorded.

Bar: `pytest -q -n auto` → **2490 passed, 11 skipped**;
`trace.py --strict --strict-schema` → `orphans=0 integrity=0
schema-findings=0`; `check_docs` OK.
