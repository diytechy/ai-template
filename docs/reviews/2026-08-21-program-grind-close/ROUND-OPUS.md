# ROUND-OPUS — adversarial review of the 2026-08-20/21 program-grind batch

Range: `b94bf58c..bd8fce68` (23 commits), branch
`requirements/ears-and-quality-characteristics`, HEAD `bd8fce68`.
Reviewer: internal Opus.

**Method.** Every finding below was reproduced against the tree at `bd8fce68`;
commands and their real output are quoted. Where a guard's strength was in
question I ran a **mutation**: broke the production code in a scratchpad copy of
the repo and re-ran the guarding test to see whether it reds. No tracked file was
modified — the only write is this review. Claims I could not reproduce are
labelled SUSPICION and kept out of the numbered findings.

**Counts:** 2 CRITICAL, 13 MAJOR, 18 MINOR.

---

## CRITICAL

### C-1. The recorded-correction verb's authority is a comment inside the file it guards — the id watermark is hand-forgeable in two lines, on a ruling that need not exist

**Evidence.** `project-trajectory/scripts/trace.py:910-931` (`read_corrections`)
parses the authorising record out of `docs/id-watermark`'s own header text.
`trace.py:995-1005` then accepts an otherwise-illegal raise whenever that parsed
record matches the observed `(was, now)` pair:

```
        justified = max(was, live.get(space, 0))
        if now > justified:
            fix = corrections.get(space)
            if fix is not None and fix[0] == was and fix[1] == now:
                continue
```

`trace.py:1027` wires it end to end —
`_mark_history_findings(marks, live, previous, read_corrections(root))` — with
`previous` supplied by `committed_watermark(root)` (`trace.py:1096`): the
committed file versus the working tree. Nothing verifies that the cited ruling
exists, that it concerns this space, that it authorised this value, or that the
line was emitted by `correct_watermark` rather than typed.

**Reproduced** against the real committed baseline (`B=8`, `SR=180`):

| attack | result |
|---|---|
| hand-raise `SR = 180 → 500`, no record | **REFUSED** — control; the guard does work |
| same raise + hand-typed `# correction: SR 180 -> 500 (OI-47)` | **ACCEPTED, no findings** |
| chained second correction on an already-corrected space (`B 8 → 40`) | **ACCEPTED, no findings** |
| same, citing a ruling that does not exist (`OI-999`) | **ACCEPTED, no findings** |

The one-shot property is enforced **only in the writer** (`correct_watermark`,
`trace.py:1195` refuses a replay); the *checker* has no such rule, so
corrections chain indefinitely by hand. Worse, `read_corrections` returns a dict
keyed by space (`trace.py:927-929`), so a second correction line for a space
**silently erases the first from the parsed record** — in the chained attack,
`B`'s ruled `7 -> 8` record vanished from the map, leaving only the forged
`8 -> 40`. The audit trail the mechanism exists to create is itself
overwritable.

Regeneration does not heal it: `bump_watermark` keeps existing marks and never
lowers (`docs/id-watermark:8-9`) and carries corrections forward unchanged
(`trace.py:1147-1148`), so a forged value is stable under `--bump-ids`. Once
committed, `previous` becomes the forged value and no justification is needed at
all.

**Failure scenario.** An agent hits an id collision and wants `SR` to skip ahead.
It edits `docs/id-watermark`: sets `SR = 500`, appends
`# correction: SR 180 -> 500 (OI-47)`. `trace.py --strict-integrity` passes
clean, the pre-commit floor passes, CI passes. 320 SR ids are permanently burned
and the record cites a ruling that says nothing about SR. This is exactly the act
the file's own header forbids in prose ("Never by hand", `docs/id-watermark:11`)
and that `da4d3bcd`'s message claims has been mechanised.

**Fix.** Bind the record to something outside the guarded file: require the cited
ruling id to resolve to a `ruled` row in `docs/requirements/open-items.toml` that
names the space; move the one-shot rule from the writer into
`_mark_history_findings` (refuse a space that already carries a committed
correction); and append rather than overwrite in `read_corrections` so a chained
record reds instead of replacing.

### C-2. WI-491 shipped under the subject "align subagent_gate's parse-failure arm **fail-closed**" and, in one scenario, converted an explicit `deny` into `ask`

**Evidence.** `f3cb9801`'s own test rewrite states the behaviour change
(`tests/test_subagent_gate.py`,
`test_corruption_no_longer_falls_through_to_the_legacy_file`):

```
-    assert proc.returncode == 2
-    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
+    assert proc.returncode == 0
+    assert out["hookSpecificOutput"]["permissionDecision"] == "ask"
```

The fixture is a corrupt `docs/process.toml` **plus a legacy
`docs/subagent-gate` reading `deny`**. `subagent_gate.py:250-251` now
short-circuits on `policy is UNPARSEABLE` before the legacy fallback at
`:251-252` is reached, and `decide()` (`subagent_gate.py:184-188`) resolves
`UNPARSEABLE` to `ask`.

**Reproduced end-to-end** — I ran the real hook binary at both revisions against
the same fixture, not the unit test:

```
POST-WI-491 (bd8fce68), corrupt process.toml + legacy `deny`:
  permissionDecision "ask"   exit=0
PRE-WI-491  (00a2c6f2), corrupt process.toml + legacy `deny`:
  permissionDecision "deny"  exit=2
```

Relative to `allow`, `ask` is closing — which is the direction the commit
message, the module docstring and the fragment all describe. Relative to the
behaviour it *replaced in this exact fixture*, it is **opening**: an operator's
explicit `deny` becomes unreachable the moment `process.toml` fails to parse.
The commit narrates a tightening and the test it rewrote records a loosening.

**Failure scenario.** An adopter mid-migration has both surfaces live (this is
the supported state — `main()` still falls back to the legacy file, and
`bootstrap.py --migrate-config` exists precisely because repos carry both). They
set `deny`. A merge-conflict marker or a truncated write lands in
`process.toml`. An unattended run that previously **halted at exit 2** now
returns `ask` at exit 0 — and in a non-interactive harness where `ask` degrades
to proceed, the spawn happens.

**Fix.** On `UNPARSEABLE`, consult the legacy file and take the **more
restrictive** of the two rather than short-circuiting to `ask`; and correct the
module docstring and RESYNC entry to say that the parse-failure arm is `ask`,
not "fail-closed" unqualified.

---

## MAJOR

### M-3. Two docstrings that declare an id UNCLAIMED are parsed as declarations OF that id — the disclaimer is the tag

**Evidence.** `check_trajectory.py:1059` and `:1117`, both authored by this batch
(`366a8131`, WI-488):

```
1059:   DELIBERATELY UNCLAIMED (no `Implements:` line): `LLR-042` (`SR-159`) is
1117:   `Implements:` line names `LLR-042` here.
```

`gen_arch_map.backlink_ids` (`gen_arch_map.py:270-271`) partitions on the literal
token and harvests every id **after** it, anywhere on the line. Both lines carry
the token followed by the ids.

**Reproduced** — calling `gen_arch_map.implements()` on the two functions:

```
if_tc_coverage_findings      -> implements() ['LLR-042', 'SR-159']
if_tc_allow_hygiene_findings -> implements() ['LLR-042']
```

The arch map's third column therefore reports both functions as implementing
exactly the row the author spent two paragraphs explaining they must **not**
claim — because, as `check_trajectory.py:1062-1063` says, `LLR-042`'s detail is
"now FALSE of the seam-TC rule this function promotes."

`backlink_ids`' own docstring (`gen_arch_map.py:266-268`) shows the authors knew
the hazard — "this function's own prose is inside the surface it scans, and an
illustration would be harvested as a real declaration — the very defect it
describes" — but the defence was applied only to that one file.

**Blast radius, measured.** I audited *all* declaration-parsing lines in the
scanned surface, not a sample: these two are the **only** prose lines that parse
as declarations, and the reverse-coverage count is unaffected (`LLR-042` also
carries a genuine tag at `check_trajectory.py:877`). The damage is to the map,
not the percentage — but it is a **false traceability link rendered in a derived
artifact**, which the same docstring calls "worse than one that has none."

**Failure scenario.** The genuine tag at `:877` is later removed as part of a real
repair. Coverage still counts `LLR-042` as covered and the map still shows it
implemented — sourced entirely from the sentence asserting it is not. The
disclaimer becomes undetectable cover for the gap.

**Fix.** Require the token to open the comment/docstring line (nothing but
whitespace, comment markers or quotes before it) — the rule my audit used, which
classified all 83 genuine declarations correctly and both prose lines as prose.

### M-4. CI's authority to *enforce* the 60 s smoke budget rests on a figure that is ~7x off, and no one in this 23-commit range re-measured it

**Evidence.** `scripts/check_smoke_budget.py:10-14` (echoed in
`.github/workflows/test.yml:93-99`):

> "the re-tiered tier is startup-dominated, not core-bound — measured **~7.5 s at
> 24 cores**, ~8.1 s at 4, ~10.5 s at 2 (WI-281 rework, 2026-07-23, 3.11.9) — so
> the 60 s budget keeps **~5x headroom** on any real runner and a breach means
> the tier stopped being a smoke test … not runner noise."

**Measured on this box (24 cores, 3.11.9), foreground:**

```
1284 passed, 5 skipped in 55.46s     (wall 55.9 s)
```

and a second independent timing in this review session returned **57.14 s**, with
a third under `check_smoke_budget.py --mode enforce` returning **64.6 s, verdict
OVER, exit 1**. The batch's own record corroborates the spread: of 17 smoke wall
times recorded in `docs/log.d/2026-08-20-program-grind.md`, **12 exceed 60 s**
(up to 142.9 s). CLAUDE.md's own note records 54.9 / 64.0 / 55.7.

So the tier runs at roughly **0.9–1.1x of budget**, not 0.2x. The measurement is
not merely stale; it is the *stated justification for enforcing*, and every
premise it offers ("startup-dominated", "5x headroom", "a breach means a heavy
module slipped back in, not runner noise") is falsified by the current tier.

**Failure scenario.** The `smoke-budget` job runs `--mode enforce` on every push
(`test.yml:116`). It passes today only because the hosted runner happens to land
under the line; one runner-contention spike reds an unrelated PR, and the
message tells the author a heavy module slipped into the tier — sending them to
re-tier a module that is not the cause. Conversely, a genuinely heavy module can
now be added inside the noise band and never breach.

**Fix.** Replace the `~7.5 s / ~5x headroom` sentence in both files with a dated
2026-08-20 re-measurement and a re-argued verdict, or drop `--mode enforce`
until the tier is re-tiered. The budget number itself should not move to fit
the box — that discipline is correct and is being kept.

### M-5. `docs/stack.ini` banks a 46.97 s reading that nothing reproduces, and uses it to argue the budget question closed

**Evidence.** `docs/stack.ini:357-364` (WI-483 re-stamp):

> "measured at this re-stamp 1261 collected / **46.97 s wall at -n auto** …
> The seconds budget is NOT touched here, in either direction — **a run that came
> in comfortably** is no more a reason to tighten it than the 64.0 s run was a
> reason to raise it."

46.97 s is the fastest reading anywhere in the repo — faster than all 17 log
readings (minimum 56.78 s), faster than CLAUDE.md's three warm runs, and faster
than all three timings taken in this review (55.46 / 57.14 / 64.6). It is the
only stamp in the range that makes the tier look comfortable, and it is the one
cited to leave the budget alone.

The stamp's *reasoning* is admirably careful — it explicitly refuses to treat the
fast reading as evidence the tier got cheaper. But it then leans on the same
reading's comfort for its conclusion, and the reading does not reproduce.

**Failure scenario.** A future author reads `stack.ini`, concludes the tier runs
at ~78% of budget, and accepts the stamp's own invitation ("new in-process unit
tests SHOULD accrue"). CI's enforce lane goes red and the diagnosis points at
their tests rather than at a budget that was already exhausted.

**Fix.** Annotate `stack.ini:358` as a single unreproduced outlier, or re-stamp
with a median of ≥3 warm runs as the 54.9 / 64.0 / 55.7 entry did.

### M-6. The smoke membership stamp is stale by 6 and its declared headroom is false at HEAD

**Evidence.** `docs/stack.ini:391-393` stamps `max-tests = 1291` with
`fig: rev=046843eb-dirty` and the sentence **"+8 over the measured 1283 keeps the
same ~0.6% membership headroom as the last nine stamps."**

**Reproduced** with the declared fig command:

```
1289/2746 tests collected (1457 deselected) in 0.70s
```

Actual headroom is **2 tests (0.16%)**, not 8 / 0.6%. Ten commits landed after
`046843eb` (WI-484 → WI-492) and added six smoke tests with no re-stamp. The
stamp is also internally inconsistent: `stack.ini:381` says "1282 collected",
`:391` says "the measured 1283".

**Failure scenario.** The next WI adds three in-process unit tests — the growth
this ratchet is documented to welcome — and
`test_smoke_tier_stays_within_its_membership_budget`
(`tests/test_smoke_budget.py:84`) reds on the **commit bar** with a message
telling the author to re-tier a heavy module into `SLOW_MODULES`, which is not
what happened.

**Fix.** Re-stamp `max-tests` at HEAD with the WI-487..WI-492 delta named, and
correct the 1283 → 1289 headroom sentence.

### M-7. The byte-budget guard's own baseline row is stale, and the headroom claim printed inside it is false about itself

**Evidence.** `project-trajectory/skills/byte-budget-guard/SKILL.md:34` declares
its own `Baseline | 4,925`. Real size at HEAD: **4,982 bytes** (4,905 at
`b94bf58c` — so the row was already ~20 bytes wrong before the range, and the
range grew the file a further 77 bytes without touching it). Cap is 5,000, so
**18 bytes free**.

`SKILL.md:36-37` then asserts: "`AGENTS.template.md` is parked at its cap: 52
bytes free (0.5%). **Every other capped file holds 2–18%**." The guard itself
holds **0.36%** — the claim is false about the very file it is printed in.

**Why nothing caught it.** `tests/test_bootstrap.py:397`
(`test_always_loaded_docs_stay_within_byte_caps`) checks *size ≤ cap*. Nothing
anywhere tests that a `Baseline` cell equals the real size; the Watched table is
explicitly "Enforced by convention", and the Capped table's baseline column has
the same non-enforcement without saying so.

**Failure scenario.** The next author follows the skill's own procedure, records
"before = 4,925", adds a 40-byte row, computes "+40, still under 5,000", commits
— and the cap test reds at 5,022, because the true before was 4,982. The skill
whose job is preventing this causes it.

**Fix.** Re-stamp the row to the measured value, correct "2–18%", and add one
assertion pinning each `Baseline` cell to `len(read_bytes())`.

### M-8. `test_the_floor_never_runs_a_step_twice` cannot fail — the dedup guard has zero coverage (proved by mutation)

**Evidence.** `tests/test_product_floor.py:107-129` builds `held` from the real
repo profile, where `held == []` (measured). `full = held + plan` is therefore
just `plan`, and the assertion reduces to "the `DevStg-Reqs` gating plan has
unique step names" — a fact about the base step table, nothing about the floor.

**Mutation proof** (scratchpad copy; real tree untouched) — the dedup guard at
`check.py:1320` was deleted, i.e. exactly the behaviour the test's docstring
claims to pin:

```
 5 passed in 2.83s
```

**Fix.** Give the test a fixture with a product step tagged
`{DevStg-Reqs, DevStg-Tests}` so the name is in both the base plan and the floor
table, then assert it appears once.

### M-9. `test_the_floor_holds_product_steps_and_never_process_ones` has no positive half, and 4 of 5 floor tests survive total removal of the feature

**Evidence.** `tests/test_product_floor.py:82-104`. Its docstring claims "THE TWO
AXES … asserted in both directions. The positive half alone would pass a floor
that simply re-ran the higher bar's entire plan." There is no positive half:
with `held == []`, line 99 (`assert layers <= {"product"}`) is
`set() <= {"product"}` and line 104 (`assert "traceability" not in …`) is over an
empty set. The one live assertion (line 103) tests the step table, not the floor.

**Mutation proof** — `floor_plan` returning `[]` unconditionally (the feature
fully disarmed):

```
FAILED tests/test_product_floor.py::test_one_drafted_row_does_not_lose_an_established_product_check
1 failed, 4 passed in 11.21s
```

Only the end-to-end scaffold test at `:172` catches disarmament; it is real and
load-bearing, and it is the *only* one. A second mutation (dropping the layer
filter so process steps get promoted) does red this test, so its **negative**
direction is live — the gap is one-directional.

**Fix.** Add a non-empty assertion on `held` using the same profile-injected
`CANARY_PRODUCT` shape the fixture already knows how to build.

### M-10. The product floor's live set is empty in every shipped configuration — not merely "dormant for the three built-ins"

**Evidence.** OI-51 and the log frame the gap as: the three built-ins are
`{DevStg-Impl}`-only so the floor is dormant *for them*, but is "CORRECT and live
for adopter-declared `[step:*] layer = product` rows". Measured, that
understates it:

- `ex-draft` can never exceed `DevStg-Tests` (`derive_gate.py:390-401`,
  `_RELEASE_CEILING = BAR_TESTS`), and `floor_plan` engages only when
  `bar_ord(floor) > bar_ord(gate)` (`check.py:1314`) using **set membership**
  (`floor in step[3]`, `check.py:1320`). So the only bar the floor ever selects
  at is `DevStg-Tests`.
- **Every** product-layer step in the kit and in this repo is tagged
  `DevStg-Impl` only — six, not three: `format`, `lint`, `tests+coverage`
  (`check.py:603-605`) plus this repo's `doc-refs`, `figures`,
  `module-coverage` (`docs/stack.ini:438,455,481`).
- The default for an adopter-declared step is also `DevStg-Impl`
  (`check.py:375`, `fallback=BAR_RELEASE`), and
  `project-trajectory/stack.ini.template` ships no `[step:*]` section at all.

Measured: `HELD (repo profile) = []`, `HELD (profile=None) = []`. The floor fires
only if an adopter hand-writes both `gates = DevStg-Tests` and `layer = product`
into a `[step:*]` — the configuration `tests/test_product_floor.py:41-46`
invents. **Today the mechanism is live only in its own test fixture.**

**Fix.** OI-51's `blast_radius` should read "live for a product step explicitly
tagged `DevStg-Tests`; no shipped artifact produces one, so the live set is empty
until (a) or (b) is ruled."

### M-11. Two adopter-facing documents tell adopters the floor covers format/lint/test, which it provably cannot

**Evidence.** `project-trajectory/RESYNC_PACK.md:2401`: "**Which steps this
covers:** everything at `layer = product` — `[product]` format/lint/test plus each
`[step:*]` you declared as product." `project-trajectory/PROCESS_OPTIONS.md:205`:
"**And a product check does not fall at all.** … `check.py` selects
product-layer steps (`docs/stack.ini`'s `[product]`, plus each `[step:*] layer =
product`) at `max(derived bar, ex-draft)`."

Both are false for `[product]` format/lint/test — the three steps the same
commit's own test proves the floor cannot reach (M-10). The dormancy caveat
exists only in the log fragment and OI-51; these two files are what a downstream
adopter actually reads, and `RESYNC_PACK` even primes them to expect a red ("your
first push after this re-sync reds") that cannot occur.

**Failure scenario.** An adopter re-syncs, reads that product checks no longer
fall when a requirement is drafted, drafts one, and ships an unlinted, untested
PR believing the floor covers it.

**Fix.** One sentence in both, naming the `DevStg-Impl` tagging and OI-51.

### M-12. `tests/test_import_layers.py` is blind to new cycle edges *inside* the SCC — the density the WI exists to reduce (proved by mutation)

**Evidence.** `test_no_new_import_cycle` (`tests/test_import_layers.py:231`)
asserts `found == baseline` where both are **SCC partitions** — sets of module
names. An edge added between two modules already in the same SCC leaves the
partition identical.

**Mutation proof** (scratchpad copy) — two brand-new deferred cycle edges
appended to `lane.py`:

```python
def _adversarial_new_edge():
    import dispatch   # NEW deferred cycle edge inside the SCC
    import handback
    return dispatch, handback
```
```
3 passed in 1.11s
```

Zero signal — and function-body deferred imports are precisely the pattern the
module docstring calls "the exact failure mode the review describes."

**Positive control** (the instrument is not inert): `import integrate` inside a
function of `traj_panels.py` reds two tests, so a module *joining* the SCC and
any view→lifecycle edge are both caught. The blindness is to density only.

**Failure scenario.** WI-483's remaining slices are paid to cut
`intake → dispatch`, `integrate → handback`, `integrate → intake`. Nothing stops
a worker adding three more deferred edges inside the SCC first, and nothing
notices if a cut edge is re-added between two modules still in the component —
the ratchet reports success while the tangle tightens.

**Fix.** Add a second ratchet line beside `CYCLES`: the intra-SCC edge count,
asserted `<=` and re-stamped downward only.

### M-13. The backlink dial was raised 0 → 50, and the two documents that state its value still say 0

**Evidence.** `docs/process.toml:176` now reads `backlink_coverage_min = 50`.
Neither `README.md` nor `docs/enforcement-audit.md` was touched in the range
(`git log b94bf58c..bd8fce68 -- README.md docs/enforcement-audit.md` is empty),
and both still describe the pre-campaign state:

- `README.md:427`, in the dial table whose third column is *this repo's own
  value*: "`0` — measured **1 of 161 (0.6%)**; 50 is the recorded target …
  and **the dial rises only after the tags land**."
- `docs/enforcement-audit.md:114`: "It ships report-only
  (`backlink_coverage_min = 0`)" — in the document whose whole purpose is mapping
  each rule to its **strongest** enforcer, which now understates it.

Nothing pins either: no test compares the README dial column against
`docs/process.toml`.

**Failure scenario.** A future worker consults the README dial table — the
declared one-stop tour of the policy home — is told the backlink bar is off, and
either "restores" the dial to 0 as drift or plans on the belief that no coverage
bar exists. The enforcement audit reports a gap that was closed.

**Fix.** Update both cells in a trunk step; consider pinning the README dial
column the way `test_rule_sync.py` already pins `OWNER_DIALS`.

### M-14. WI-469 multiplied the `;`-joined endpoint defect the same program had just documented — 1 row to 7, and the registry's two readers now disagree on all of them

**Evidence.** The WI-455 section of the fragment records IF-097 as "the only
`;`-joined endpoint cell in the registry, a population of one." `aa46953e`
(WI-469) added six more `counterpart` cells in that shape —
`docs/requirements/interfaces.toml` IF-029, IF-035, IF-037, IF-047, IF-070,
IF-072.

`check_trajectory._declared_seam_pairs` (`check_trajectory.py:1359`) calls
`_norm_module` on the whole cell and never splits on `;`; `trace.py:2210-2215`
**does** split on `;` (its comment cites IF-097 by name). Two readers of the same
cells now disagree on seven rows instead of one.

**Reproduced** — 14 of 249 declared seam pairs carry an unsplit, non-existent
module name as an endpoint:

```
('scripts/check_flows', 'scripts/check_flows; scripts/gen_okf; scripts/traj_parse')
('scripts/check_trajectory; scripts/integrate; scripts/score_reviews', 'scripts/score_reviews')
('scripts/agent_common', 'scripts/agent_common; scripts/gen_okf; scripts/traj_status')
```

None of the six new rows contributes a resolvable coverage pair. Latent today —
`check_trajectory.py --strict` exits 0.

**Failure scenario.** IF-047 declares `score_reviews` ↔ `check_trajectory`
(CMP-008 ↔ CMP-006). If `check_trajectory` ever gains an `import score_reviews`,
`_cross_component_scan` looks for
`('scripts/check_trajectory', 'scripts/score_reviews')`, does not find it, and
errors "cross-component import has no declared IF-### seam" — while the seam row
plainly exists and names both modules. The cheapest fix available to that author
is to duplicate or delete a correct row.

**Fix.** Split `counterpart`/`this_project` on `;` in
`_declared_seam_pairs`, matching `trace.py`; or refuse a multi-valued endpoint
cell at intake so the readers cannot diverge again.

### M-15. WI-469 created three self-referential seams: `counterpart == this_project`

**Evidence.** `aa46953e` set `counterpart` to the row's own `this_project` on
IF-025 (`scripts/gen_arch_map`), IF-026 (`scripts/check_stubs`), IF-045
(`scripts/agent_route`). The registry header defines `counterpart` as "the far
side's" endpoint (`interfaces.toml:26-27`); a row whose far side is itself has no
far side.

**Reproduced** — `_declared_seam_pairs` yields three self-loops:

```
('scripts/agent_route', 'scripts/agent_route')
('scripts/check_stubs', 'scripts/check_stubs')
('scripts/gen_arch_map', 'scripts/gen_arch_map')
```

`traj_views` orients the dashboard seam graph from the same cells, so the
rendered architecture graph gains three self-loops. With M-14's six, **9 of the
10 "verified real consumer" rows now contain themselves.**

**Failure scenario.** A reader auditing "which modules does `agent_route` talk
to" reads IF-045 and learns only that it talks to itself; the real far side —
the agents registry and enable-list — was overwritten by the re-authoring pass.

**Fix.** Re-author the three to name the real counterpart, or convert them to
`external:` like the other 16.

---

## MINOR

**m-16. The seam-TC migration allowlist has no growth detector.** The seeding is
honest (see NR-1), but `if_tc_allow_hygiene_findings`
(`check_trajectory.py:1100-1130`) reports only *shrinkage* signals — a listed
seam that gained a TC, or an id no longer live. Nothing reports that the list
grew, and no test pins its size (a grep of `tests/` for `if-tc-coverage-allow`
finds only `tmp_path` fixtures at `tests/test_trajectory_arch.py:460,485`; no
repo allowlist — `if-tc-coverage-allow`, `orphans-allow`, `provenance-allow` —
has a size or content pin). The per-line reason is unenforced by construction:
the header (`docs/if-tc-coverage-allow:21-24`) states the 120 entries carry no
per-line reason, so a bare 121st line is lexically indistinguishable from the
baseline, and `read_if_tc_allow` discards the reason field when absent. *Scenario:*
a new seam reds `--strict`, and the one-line fix that makes it green is appending
its id — no check, no hygiene line, no test. *Fix:* pin the seeded id set in a
test, and require a ` — <reason>` beyond it.

**m-17. IF-045's "fan-out=1 / sole direct reader" is refuted in the tree today.**
`interfaces.toml:696-706` claims `agent_route` is the sole direct reader of the
registry + enable-list; `dispatch.py:162-166` reads `docs/agents-enabled` bytes
and parses its lines directly with no call into `agent_route`, and
`migrate_carrier.py:85` loads `docs/agents.csv`. Since "fan-out=1" was the stated
discriminator for keeping the row internal rather than converting it to B-05, the
measurement that decided the row's classification is wrong.

**m-18. The same file is classified both ways in one pass — IF-037 vs IF-038 over
`docs/process.toml`.** IF-038 (`interfaces.toml:614-624`) converts to B-05
because "9 kit scripts read docs/process.toml directly"; IF-037 (`:602-612`)
keeps an internal three-module counterpart as "Low fan-out: three direct
readers" — but IF-037's `contract` cell names `docs/process.toml` **first** among
its surfaces, with `agent_common` on both sides. *Fix:* state which surface
IF-037's fan-out was measured over.

**m-19. IF-072's counterpart names a non-consumer and omits the consumer its own
contract names.** `interfaces.toml:934-944` lists `scripts/check_vocab`, which
(`check_vocab.py:188,221`) only includes the file in a byte scan and never parses
the `<path> — <reason>` grammar the contract defines; meanwhile the contract
names `tests/test_dogfood_sync.py` (real, `tests/test_dogfood_sync.py:679-680`),
which is not in the cell. Off by one in each direction.

**m-20. IF-070 names a module that does not read the file.**
`interfaces.toml:909-919` lists `scripts/check`, which touches `COVERAGE_JSON`
only as a constant (`check.py:210`) and an `unlink` (`check.py:2065`). The note
concedes this; the cell still asserts it as an endpoint.

**m-21. WI-455's deferral rationale for IF-056/IF-077 expired with nothing
tracking it.** `interfaces.toml:841` and `:1000` still name retired CMP ids;
WI-455 left them because they "sit inside the held Contract-cell clause the
WI-469 pass deletes whole," but `aa46953e`'s own message says "no
owner/direction/contract cell was touched anywhere in this pass." The deletion
pass is unperformed and carries no OI row.

**m-22. The WI-469 log summary overstates by one.** The fragment says "All 27
SR-owned file-as-endpoint Consumes rows … re-authored"; the diff touches 26
(IF-028 was fixed by a different WI). The commit message states it correctly.

**m-23. The duplication "after" figure is stale at close, and the `fig:` marker
pins only the "before".** The table
(`docs/log.d/2026-08-20-program-grind.md:63-66`) reports after = 17 / 48 / **477**
with `rev=b94bf58c` — the *before* revision. Running the declared command:

```
46de9442 -> 17 48 477     (WI-448's own commit — TRUE here)
3bc20bc8 -> 17 48 477
bd8fce68 -> 17 48 484     (HEAD — stale by 7 lines)
```

Honest at its own revision, unattributed at the close. *Fix:* give the "after"
row its own `rev=`.

**m-24. Three sections of this fragment trip the very deferral-parse warn the
fragment banks against other workers.** `gen_open_items.py` emits six warnings,
not the three the WI-455 worker banked — the last three are this batch's own
WI-490/491/492 sections (`:1493`, `:1631`, `:1716`), each phrased "Deferred open
items: none — OI-45 is fully executed by this row". The parser cannot distinguish
"none, because OI-45 is done" from "OI-45 is deferred". The banked finding was
recorded and then reproduced three more times inside the fragment the closing
review reads. The **top-matter union is correct** by human reading (OI-48 at
§WI-448, OI-49/50 at §WI-455, OI-51 at §WI-473, all others "none"); it is the
machine's reading that disagrees. *Fix:* phrase the none-case without naming an
OI id on that line.

**m-25. The banked watermark finding names ids that were never at risk and omits
the two that were.** `docs/log.d/2026-08-20-program-grind.md:1968-1977` cites
`B-06`, `B-07`, `EXT-004` against marks `B = 7` / `EXT = 5` — but those ids sit
*below* their marks and were never mintable. The genuinely exposed ids were the
next mints, `B-08` and `REL-004`, which is what `external.toml`'s (now-retired)
SPENT IDS block named and what WI-492 actually corrected — note it corrected
`REL`, a space the banked finding never mentions, and left `EXT`, the space it
did. Conclusion right, cited evidence wrong, and it stands as the closing
review's account of the problem.

**m-26. The campaign's banked staleness list is incomplete.** My cross-check of
every tag against its row surfaced one WI-487 did not bank: `LLR-175`'s
`CodeSymbol` names `LaneState.note_session`, but no `LaneState` exists — the live
class is `RoutingState` (`agent_loop.py:913`) and the tag correctly sits on
`RoutingState.note_session` (`:1152-1157`). `LLR-011`'s `CodeSymbol`
(`write/--force + write_kit_version`) likewise names no real symbol for its
"write" half while the tag sits on `copy_kit_files` (`bootstrap.py:2633-2638`),
which genuinely realises the row. Same class as the banked items: honest tag,
stale row.

**m-27. The module-size census cannot see packages, and the docstring's escape
hatch is unreachable for them.** `tests/test_module_size_ratchet.py:1848` globs
`scripts/*.py` non-recursively and keys on `path.name` (`:1851`), so all of
`scripts/kitlib/` (639 lines across 5 files) is invisible — and a package module
can never *earn* a baseline either, contradicting the file's own rule at
`:30-33` ("the new module … earns its own reviewed baseline"). Honestly banked at
`docs/log.d/2026-08-20-program-grind.md:1999-2006` with a stated reason for
deferring, so this is disclosed rather than concealed — but the docstring is now
factually wrong and should say so.

**m-28. `test_subagent_gate_log_filename_matches_the_writer` is a source-text
assertion.** `tests/test_agent_loop.py:404-415` asserts
`'"out" / "subagent-gate.log"' in inspect.getsource(...)` — it pins formatting,
not behaviour, and `tests/test_module_size_ratchet.py:697-699` records that a
`ruff format` unwrap already caused this trap twice in this batch. *Fix:* write a
log and assert the count, plus `subagent_gate.LOG_NAME`.

**m-29. The OI-51 dormancy pin guards a proxy, not the property.**
`tests/test_product_floor.py:152` reads `derive_gate._RELEASE_CEILING`; if
someone rewrote `sn_bar` to return `BAR_RELEASE`, or changed `_raw_level`'s
empty-`srs` branch, the constant would still equal `BAR_TESTS` and the pin stays
green while `DevStg-Impl` becomes reachable. Its third assertion (`:169`) is also
vacuous over an empty `held`, and it covers 3 of this repo's 6 unreachable
product steps. *Fix:* assert `compute(docs)["ex_draft"] <= BAR_TESTS` on a
fully-decomposed fixture.

**m-30. `deferred >= 3` is a near-unfalsifiable corroborator.**
`tests/test_import_layers.py:224` — the tree has 20 deferred edges; the threshold
is 3, and the preceding specific pin at `:215` already covers walker breakage.
It would survive an 85% loss of detection.

**m-31. `--gate` no longer means `--gate`.** `resolve_plan` calls
`product_floor()` unconditionally (`check.py:1350`), reading `docs/gate` even
when the operator passed an explicit lower `--gate`. `--gate all` is guarded
(`:1314`); explicit lower bars are not. Consistent with the stated "no off dial",
but undocumented in the `--gate` help.

**m-32. The gate banner surfaces decision VOLUME where the ruling asked for
fail-open VISIBILITY.** OI-46 (2a)'s stated problem was that fail-open allows
were recorded and never read. `_subagent_gate_log_count`
(`agent_loop.py:1795-1814`) counts lines, and the banner (`:1871-1877`) prints
"N decision(s) recorded … — read it if that count looks high". The banner text is
honest about what it counts, so this is not an overclaim — but a log with 500
routine allows and one fail-open reads identically to one with 501 routine
allows, so the single event the ruling wanted surfaced is the one the number
cannot distinguish. *Fix:* count the `failing open` lines separately.

**m-33. `docs/gate`'s provenance stamp is 10 commits stale.** `docs/gate:29`
reads `# computed 2026-08-20 (as-of bab4d0ee)` — commit 13 of 23, with six
spine-touching commits after it. `derive_gate.py --check` returns 0 because the
`as-of` line is excluded from the freshness compare (deliberate), so the value is
correct but the provenance line names a commit that is not where it was last
confirmed.

---

## Claims I tried hardest to refute and could not

**NR-1. The seam-TC migration allowlist's 120 is an exact, honest measurement of
the seeding tree — no padding, no pre-emptive exemptions, no stale entries.**
I expected list-padding, because a seed measured on a moving tree is where
ratchets usually launder. Measured at `bd8fce68`: **130** live IF rows, **120**
uncited by any TC, **120** allowlisted, `uncited NOT allowlisted = []`,
`allowlisted but ALREADY cited = []`, `allowlisted but NOT a live IF = []`. The
ruling's older figure of 115 versus the seeded 120 is a genuine re-measurement on
the landed tree, not a widened net. The gate is vacuous today — and *honestly*
so — but it **can** fail: an uncited seam not on the list produces a finding that
`check_trajectory.py:4140-4146` collects into `if_tc_errors` and `:4159/:4183`
folds into the exit code under `--strict`. My criticism (m-16) is about its
future, not its seeding.

**NR-2. The Hat-Refs backfill's "traced-cell" classification is defensible, and
`docs/archive/last_approved` stays green for the right reason.** This was the
edit I most expected to be laundering — 17 Approved rows edited without arming a
re-attest window. It holds. `spine_cell_class` returns `traced` for `Hat-Refs`,
`ratified` for `Requirement` and `Rationale`, and — critically — `ratified` for
**any unclassified column**, so the default fails safe.
`baseline_snapshot.is_drifted` consumes only `changed["ratified"]`, so a
`Hat-Refs` edit cannot arm drift while a requirement-text edit still does; I
verified both directions by driving `split_changed_cells` with mutated rows. And
it is green for the *right* reason, not vacuously: the snapshot at
`docs/archive/last_approved/docs/requirements/system-requirements.toml` holds all
73 SR rows and carries no `hat_refs` key, so the backfilled cells genuinely
differ from their snapshot copies and are genuinely being classified away rather
than compared-equal by accident.

**NR-3. The back-link campaign's 83/165 is an honest number, and the tags
themselves are honestly placed.** Given the batch's own cardinal rule ("a wrong
`Implements:` tag is worse than a missing one") this was the biggest claim
surface, and I attacked it three ways. (a) The figure reproduces exactly via the
declared command: `83/165 live LLR rows (50.3%)`. (b) I audited **every** covered
id, not a sample, for whether its coverage rests on a real declaration line
rather than harvested prose — all 83 have at least one genuine, correctly-placed
declaration, and the only two prose artifacts in the whole scanned surface (M-3)
are not any id's sole carrier. (c) I cross-checked every tag's enclosing symbol
against its row's `CodeSymbol` and `Module`, then read the 14 rows behind the
mismatches: all are placed on symbols that genuinely realise the row, with the
**row** rather than the tag being stale in each case (m-26). I also checked
whether the dial was fitted to its own result: it was not — `README.md:427`,
`docs/enforcement-audit.md:114` and WI-486's spec all record the 50 target in the
future tense *before* the campaign, so the raise was sanctioned rather than
reverse-engineered. The dial does gate nothing in this repo today (`docs/gate`
reads `DevStg-Reqs`; `--strict-backlinks` is appended only at
`BAR_TESTS`/`BAR_RELEASE`, `check.py:552-555`), but nothing in the batch claims
otherwise.

**Also checked and not refuted:** WI-491's fail-closed arm is real against
`allow` — I ran the actual hook binary, and a corrupt `process.toml` returns
`ask` while genuine absence still returns `allow` (opt-in posture preserved);
C-2 is the one direction where it regressed. WI-467's ancestry claim is true
(`git merge-base --is-ancestor` confirms both `cda29c42` and `dea8364e`).
WI-455's 22-cell CMP sweep is complete — no live registry cell under
`docs/requirements/` still names a retired CMP-001..005 id outside the two
deliberately-deferred Contract cells (m-21) — and no re-authored `notes` cell
carries a surviving citation frame. IF-134/135 realize the crossings they claim:
`LLR-019.module`/`LLR-020.module` are byte-identical to their rows'
`this_project`, so the derivability agreement is literal rather than lucky, and
IF-135's B-04-only choice is honest (`SR-020.boundary_refs` names both, the row
says so, and B-01's `carries` text genuinely does not describe a push). Every
raised module-size bound carries a recorded reason (8 of 8, plus one lowered),
and WI-487's "docstring/comment lines only, no executable change" claim holds
under a filtered diff. Exactly one complexity bound moved
(`check_trajectory.main` 22 → 24) with an 8-line recorded reason. No byte **cap**
was loosened — `BYTE_CAPS` is byte-identical to `b94bf58c`; the five
"tightenings" were Watched-table baseline re-stamps. `check_smoke_budget.py` does
a genuine wall-clock measurement and can fail (verified both arms). The
`ex-draft` reader abstains correctly in all seven crafted cases, and hand-lowering
`ex-draft=` to disarm the floor reds a gating step because `derive_gate --check`
compares the full basis line.

---

## Suspicion, not fact

- `external:git` (IF-032 at `interfaces.toml:543`, IF-134 at `:1732`, IF-135 at
  `:1748`) names a party the locked frame does not have — `external.toml`
  dissolves git into EXT-001, and IF-032's own notes argue that dissolution as
  the reason it takes *no* tie-back, while IF-134/135 use the same endpoint value
  and *do* tie back. I could not establish this as a rule violation: the prefix
  is a free-text endpoint convention, not an EXT-id reference. Flagged as a
  reader trap.
- The batch's CRLF exposure is latent rather than live. `.gitattributes:2`
  declares `* text=auto eol=lf` and all capped/watched files are `i/lf w/lf` on
  this box today — but 51 tracked files currently carry `w/crlf`, and two of the
  three caps are inside the blast radius if the mechanism reaches them
  (`byte-budget-guard/SKILL.md` 4,982 → 5,072 with CRLF against a 5,000 cap;
  `AGENTS.template.md` 9,948 → 10,138 against 10,000). The banked finding is
  correct; I could not make it fire.
