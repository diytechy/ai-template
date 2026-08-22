## 2026-08-22 — WI-500: the test-evidence carrier — `DevStg-Release` gets its one producer, and it is not a cell

**Summary.** The rung WI-498 slice 3 left deliberately empty now has exactly one
input. `scripts/record_test_evidence.py` RUNS the declared bar through the
documented harness entry point and writes `docs/test/evidence` only on exit 0;
`kitlib/evidence.py` holds the record's format and the declared source surface
its claim binds to; `kitlib.stage.evidence_verdict` is the one question asked of
it; and `spine_stage(..., evidence_passed=)` is the only way `DevStg-Release` is
returned. The slice-3 structural pin ("the rung has no producer") was retired
DELIBERATELY — the act its own docstring named — and replaced by the claim that
is now true and worth pinning: **exactly one producer, and it is guarded by the
bare harness-verdict parameter**, driven against three mutants.

**THIS REPO DOES NOT HAVE VALID RELEASE EVIDENCE AND THAT IS CORRECT.** Nobody
has run the producer on a green full run at this HEAD, and none was contrived to
green the rung. `docs/stage` reads `DevStg-LLReqs` before and after this change,
byte-identical in every derived field; the repo's own path to the top rung is a
real green run someone actually performs, later. A carrier that shipped with its
first record already written by the session that built it would be exactly the
claim this mechanism exists to distrust.

Deferred open items: none — the design questions the row could have deferred
were all ruled or measurable. "What counts as the declared suite" was already
answered by `docs/stack.ini` `[tiers]` and is not re-litigated here: the producer
names a TIER and refuses a partial one. Evidence LIFETIME needed no policy,
because the value binding makes lifetime a derived fact rather than a dial — a
record lives exactly as long as the tree it measured. The one thing declined
rather than deferred (hosted CI committing the record back) is recorded below
with its reasons.

### The trust model — the five decisions, each against what it defeats

| decision | the alternative it beat, and why |
| --- | --- |
| **Format**: `docs/test/evidence`, key=value addressed BY NAME, generated header, `outcome`/`tier`/`command`/`revision`/`binding` | the `docs/stage` idiom, and for its recorded reason — the retired `docs/gate` put its machine value on "the first non-comment line", an idiom five readers re-implemented and none could validate. A JSON report was refused: the harness emits none today, and adding one would make the claim depend on a plugin every adopter must install. |
| **Binding**: SHA-256 over the LF-normalized content of the spine registries **plus** the declared `[paths]` src/tests trees **plus** `docs/stack.ini` | the WI-492 precedent applied to a measurement: **value-bound, not space-bound**. A timestamp cannot see an edit; a revision alone cannot see a dirty tree; a binding over the registries alone rides any code change; one over the source alone rides a newly authored test case. Both halves are load-bearing and each covers what the other cannot. |
| **Producer**: a driver that WRAPS `check.py --tier <t>` and writes only on exit 0 | a check STEP was refused on a structural ground, not a stylistic one: a verdict about the whole harness run can only be written by something that outlives the run, and a step recording a verdict it is itself part of is not a measurement. There is no flag that records without running and no `outcome = fail` state. |
| **Consumer**: `evidence_verdict` → `derive_stage` → `spine_stage(evidence_passed=)`, the rung's only return | keeping the rung out of `spine_stage` (lifting it in `derive_stage` after the fact) would have split the ladder across two files. The parameter keeps `spine_stage` a pure row function AND makes OI-30 D2 structural: no row can set it, and the pin now demands the guard be the bare parameter, so a guard computed from cells is unrepresentable. |
| **Staleness**: a hard finding in the consumer, never a warning | the verdict answers False (rung drops) AND the stage fingerprint folds the source surface **whenever a record is present**, so the committed `docs/stage` goes stale and `derive_stage --check` — the commit-bar and CI freshness step — reds. Both directions were needed: the verdict alone is silent, the fingerprint alone is unattributed. |

**THE HOLE THAT DESIGN CLOSES, and it is the whole reason the fingerprint grew a
second half.** The row's brief said the carrier "joins `DECLARED_INPUTS`", and it
does. But if that were the *only* edit, the silent ride is still reachable and
INVISIBLE: a committed `docs/stage` reading `DevStg-Release`, a product edited
afterwards, and an evidence file whose bytes never moved — the fingerprint
matches, `read_stage` returns the recorded rung, and no consumer ever asks
whether the evidence still holds. This is the same shape as ROUND-SOL-RAW 6's
dual-carrier finding on `input_paths` (a forbidden state reachable AND invisible,
which is worse than either alone). So `fingerprint` folds the declared source
surface too — **but only when a record is present**, so a repo below the rung,
and every fresh scaffold, pays nothing and computes byte-identically to before
apart from one `(absent)` row. Driven both ways in
`test_the_STAGE_fingerprint_moves_with_the_SOURCE_only_while_a_record_exists`.

**What is NOT claimed, stated at the module so no surface overclaims it.** This
is not a signature: a determined author can compute a valid binding by hand.
Forgery resistance needs a key and a verifier, which is a different and
adopter-hostile mechanism. What is built defeats the failure this kit actually
has — a green that was true once and quietly outlived its tree — and the honest
sentence is that one, not "unforgeable".

**Declined, not deferred: hosted CI does not write the record.** It would need
write credentials, a bot identity and a lane no reviewer signs, and the ratifying
acts of this kit are reviewable history rather than side effects of a job. CI's
half needs no new machinery: a stale record already reds `derive_stage --check`
wherever that step runs. Recorded in the driver's docstring, LLR-191's rationale
and the RESYNC entry, because an adopter will ask.

### The pin retirement, and the three mutants it is driven against

`test_the_RELEASE_rung_has_no_PRODUCER_in_the_source` →
`test_the_RELEASE_rung_has_EXACTLY_ONE_PRODUCER_and_it_is_the_EVIDENCE_VERDICT`.
Its predecessor's docstring said "deleting this test is how the harness driver
lands: an act, not a drift" — so this is that act, performed as a replacement
rather than a deletion. All three of the properties the deletion would have
thrown away are kept, and a fourth added:

| arm | catches |
| --- | --- |
| 1 — the VALUE absent from the unparsed body | `return "DevStg-Release"` (Opus's mutant at the WI-498 close) |
| 2 — every other return provably a rung below | `return _ladder.STAGE_ORDER[-1]` (Sol's mutant), and now also a SECOND Release return |
| 3 — the one Release return guarded by the bare `evidence_passed` **parameter** | `if all(is_founded(r) for r in srs): return STAGE_RELEASE` — a Status cell reaching the top rung by the back door, which is what OI-30 D2 actually forbids |

Driven, each mutant applied to `spine_rules.py` and reverted:

```
M1 literal `return "DevStg-Release"`            -> FAILED (caught)
M2 row-computed guard `if all(is_founded(...))` -> FAILED (caught)
M3 second producer `if not srs: return REL`     -> FAILED (caught)
clean tree                                       -> passed
```
fig: cmd="for each mutant: patch spine_rules.py; python -m pytest -q tests/test_ratification_level.py::test_the_RELEASE_rung_has_EXACTLY_ONE_PRODUCER_and_it_is_the_EVIDENCE_VERDICT" rev=c3c9b36a-dirty

The exhaustive 2×4³ = 128-spine arm is UNCHANGED and still green: `evidence_passed`
defaults False, so no combination of Status cells reaches the rung. That is the
point of the default, not a coincidence of the fixture.

### Two seams the change touched and deliberately did not widen

- **The phase rule reads the spine with evidence at its default (False), on BOTH
  sides.** It polices spine AUTHORING — an edit that lowers the reading must
  surface as a phase change — and evidence is not an authored row. A red suite or
  a stale record would otherwise read as an un-phased authoring decrease and
  demand a phase tag nobody can supply. Symmetric omission, commented at
  `_effective`.
- **`REPO_GLOBAL_RUNGS` was NOT extended.** Release is not like the three rungs
  in that set: those are ones where *every* phase reads the same value at once,
  while a phase reaches Release only if its OWN rows are settled. Adding it would
  have made the set's stated meaning false. The residual — a phase-anchor
  recording reach `DevStg-Release` would see a drop attributed to it when the
  repo's evidence goes stale — is unreachable today (no anchor records that rung)
  and is a WARN-only detector; it is recorded here rather than fixed speculatively.

### Deliverables

- **`project-trajectory/scripts/kitlib/evidence.py` (NEW).** The record's format
  (`FIELDS`/`HEADER`/`render`/`parse`/`read`), `WHOLE_SUITE_TIERS`, and the
  declared source surface (`source_paths` reads `[paths]` from the toolchain file
  rather than restating it; `source_files` excludes build residue;
  `fold_sources` takes its digest function so the caller's memo covers these
  files too). Imports no sibling — the stage carrier composes the two folds, so
  the package stays free of a cycle. Parsing NEVER raises, unlike `stage.parse`,
  because this file is a CLAIM rather than derived state.
- **`project-trajectory/scripts/kitlib/stage.py`.** `DECLARED_INPUTS` gains the
  evidence file (the one-list edit the input design promised); `fingerprint`
  folds the source surface when a record is present; new `evidence_binding`
  (the declared inputs MINUS the evidence file — it cannot contain its own
  digest — plus the sources), `evidence_verdict` (`(holds, reason)`, one home for
  the decision and its explanation) and `evidence_passed`.
- **`project-trajectory/scripts/record_test_evidence.py` (NEW).** The producer.
  `--tier` (whole-suite only), `--check`, `--dry-run`. Refuses an undeclared or
  empty source surface by name (a binding over nothing would match forever — and
  the count is compared against ONE, because `stack.ini` folds itself in).
- **`project-trajectory/scripts/spine_rules.py`.** `spine_stage` gains
  `evidence_passed=False` and the one guarded `return STAGE_RELEASE`; three
  docstring/table passages re-stated.
- **`project-trajectory/scripts/derive_stage.py`.** One read of the verdict,
  handed to both the live and settled folds through `frame` so a per-phase call
  sees the same repo-wide fact.
- **Spine rows minted, discharging the owner-directed fold-in.** `SR-151` and
  `SR-152` were the two orphaned SRs whose subject IS this carrier and its CI
  lane; both are now decomposed and neither appears in the orphan list.
  `LLR-190`/`TC-185` (the moment-to-tier declaration and its two-way pin,
  CMP-007), `LLR-191`/`TC-186` (the verdict is the harness's exit, in the hosted
  job and in the durable record, CMP-007), `LLR-192`/`TC-187` (the record and its
  value binding, CMP-006). Watermarks via `trace.py --bump-ids` (LLR 189→192,
  TC 184→187); `docs/archive/last_approved` refreshed with
  `intake.py snapshot` — `baseline_snapshot.refresh_refusal` read clean (`''`)
  against the PRE-refresh snapshot, so no ratified cell was laundered.
- **Adopter surface.** `bootstrap.py` MAPPING (both new files, with their
  must-arrive-whole reasons), `tests/test_bootstrap.py` file lists,
  `project-trajectory/README.md` kit-contents, `docs/kernel-modules-allow`
  (evidence.py, consumers spanning CMP-006/007), `gitignore.template` (a comment
  saying the record is deliberately NOT ignored and the directory must never be
  globbed — ignoring it would make the top rung reachable only on the machine
  that ran the suite), PROCESS.md §4, PROCESS_OPTIONS.md, and a RESYNC_PACK §3
  entry anchored `[since c3c9b36a]`. Reference surfaces updated too:
  `docs/registry-machinery-reference.md` §8.3 + the `Approved` row (the
  "DevStg-Release for nothing at all" sentence is now false and says so), and a
  new `docs/enforcement-audit.md` row for the claim itself, honest residue
  included.
- **Tests.** `tests/test_test_evidence.py` (NEW, 29 tests): the record's
  round-trip and its never-raise parse; the verdict's four refusals; the binding
  driven STALE over five independent edits (source, test, new source file, the
  declared bar itself, a newly authored test case) and NOT stale over build
  residue; the fingerprint's both-ways proof; the rung end to end (Impl → record
  → Release → source edit → Impl); and the producer's green/red/no-overwrite/
  partial-tier/dry-run/check arms. Plus the rebuilt Release pin in
  `tests/test_ratification_level.py`.

### Scaffold verification — a real `bootstrap.py --dest` run, the standing lesson

```
fresh scaffold                       -> docs/stage: DevStg-Reqs; --check: "no test-evidence record"
+ all-Founded frame-free spine       -> DevStg-Impl
producer with the REAL harness       -> RESULT: FAIL (6 steps) -> "NOTHING WRITTEN"   [red path, real check.py]
producer, harness substituted green  -> wrote docs/test/evidence (binding sha256:3a3915fc…)
  --check                            -> HOLDS — the declared suite passed at full on this exact tree
  derive_stage                       -> wrote docs/stage -> DevStg-Release   (per-phase = 1=DevStg-Release)
edit ONE byte of src/app.py          -> --check: STALE (exit 1); derive_stage --check: STALE (exit 1)
delete the record                    -> DevStg-Impl
```
fig: cmd="python project-trajectory/scripts/bootstrap.py --dest <scratch>/scaffold500 --stack python; then the sequence above in that scaffold" rev=c3c9b36a-dirty

The red path used the scaffold's REAL `check.py`; only the green path substituted
the harness (the shipped writer, binding and reader all ran from the scaffold's
own `scripts/`). Substituting a green harness rather than making a hand-built
scaffold pass six unrelated steps is the honest split: the part that was stubbed
is the part just proven for real one line above.

### Gates

```
python -m pytest -q -n auto --basetemp=D:\pytest-tmp   -> 2876 passed, 14 skipped in 1069.76s (0:17:49)  [FINAL TREE]
python -m pytest -q -n auto --basetemp=D:\pytest-tmp   -> 2875 passed, 14 skipped in 1100.33s (0:18:20)  [mid-row]
python -m pytest -q -n auto -m smoke                   -> 1397 passed, 5 skipped, 55.27 s  [FINAL TREE, idle box]
python -m pytest -q -n auto -m smoke                   -> 1394 passed, 5 skipped, 53.32 s  [mid-row, before the re-stamps]
python project-trajectory/scripts/check_docs.py --root . --stale  -> OK - 1012 doc(s), 1346 link(s), 0 broken
python project-trajectory/scripts/trace.py --root . --strict      -> integrity=0 (orphans 10, all pre-existing)
python project-trajectory/scripts/check_vocab.py --root .         -> clean (431 live authored files)
python -m ruff format --check / ruff check                        -> clean on every file this row touched
```
fig: cmd="python -m pytest -q -n auto --basetemp=D:\pytest-tmp" rev=c3c9b36a-dirty

**Ratchets re-stamped deliberately, both reasons here rather than in the diff:**

- `docs/stack.ini` `[smoke-budget] max-tests` **1378 → 1409** (measured 1402,
  headroom +7, within a test of the absolute slack the last sixteen stamps carried). The
  growth is one new in-process module plus three arms on the Release pin; every
  test is a pure in-process call and nothing bootstraps a scaffold. The SECONDS
  budget stays 60 and is not touched.
  fig: cmd="python -m pytest -q -m smoke --collect-only" rev=c3c9b36a-dirty
- `tests/test_module_size_ratchet.py` `bootstrap.py` **3030 → 3042**: two MAPPING
  rows and their reason comments, plus the docstring inventory line. Declaration
  only; no code moved in or out.

**Byte deltas, one line per touched file:**

```
project-trajectory/PROCESS.md          84,803 -> 84,881  (+78 FLAGGED: the top rung stops being "derived by nothing" and names its one input)
project-trajectory/PROCESS_OPTIONS.md 177,292 -> 177,704 (+412 FLAGGED: the per-artifact passage said the carrier had not landed; it now teaches the producer, the binding and the refused partial tier)
project-trajectory/skills/byte-budget-guard/SKILL.md  4,925 -> 4,877 (−48; 123 under its 5,000 cap; both watched rows re-stamped, superseded reasons removed)
```

### Deviations from the spec, and two pre-existing reds found

- **The spec's "the shipped ci lane is the natural producer" was NOT taken
  literally** — see "Declined, not deferred" above. The driver is the producer;
  the shipped workflow is unchanged, which also keeps SR-151's
  one-definition-of-passing pin (`tests/test_ci_tier_declaration.py`) intact.
- **The fingerprint edit is larger than "an edit to one list."** The one-list
  edit was made and is not sufficient; the reason is recorded above at length
  because a future reader will otherwise try to simplify it back.
- **`specref` cleared at close (R-F).** The row named the ruled plan as its
  spec of record; a terminal WI clears the field (the WI-498/WI-494 precedent),
  and the plan stays live for the rest of the program, cited in the spec's
  Context rather than archived.
- **Pre-existing on this branch at `c3c9b36a`, confirmed by measurement on a
  stashed tree, NOT introduced here and NOT fixed here (out of scope):**
  `check_trajectory --strict` reports `ERROR - R-F WI-501: status=done but
  SpecRef 'docs/requirements/open-items.toml#OI-53' is still set` (the
  pre-commit hook runs that check with `|| true`, so it does not block), and
  `ruff check` reports two unused imports (`tests/test_agent_loop.py:16
  inspect`, `tests/test_trace_hats.py:38 pytest`).
