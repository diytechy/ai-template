## 2026-08-25 — WI-520: the credential class vocabulary gets one home

**Summary.** `check_privacy.py`'s enforcement floor and `agent_common.py`'s
transcript redactor compiled their credential patterns independently. Driven
against the alignment pass's five samples, four disagreed, in both
directions — the one that mattered, a PEM private-key block refused at the
commit hook but passed **unredacted** into a committed transcript, so the
durable artifact was less protected than the ephemeral one. A new pure-data
module, `project-trajectory/scripts/kitlib/secret_classes.py`, is now the one
table both consumers derive their working pattern lists from; the floor's
`KEY_RE`/`TOKEN_RES` and the redactor's `_SECRET_RES` are comprehensions over
it, not hand copies, so the drift this row measured cannot reopen by one side
forgetting to update its own literal. One behavioral change: the redactor now
also redacts a PEM private-key header. Every other class's matching behavior,
on both sides, is unchanged — proven, not asserted (see Driven measurement).

Deferred open items: none — the row's Done-when is fully discharged and files
no new question.

### The vocabulary's home, and why

`kitlib.secret_classes.SECRET_CLASSES` is a tuple of
`SecretClass(name, scan_pattern, redact_pattern)` rows, one per class (private
key header, github token, github fine-grained token, slack token, aws access
key id, api secret key, generic bearer token). Either pattern may be `None` —
a stated decision, not an omission — and the comment beside each row records
why. `check_privacy.py` derives `KEY_RE` / `TOKEN_RES` and `agent_common.py`
derives `_SECRET_RES` by filtering comprehension over the table, so a class
added there reaches both consumers, or neither, by construction. `kitlib` is
the shipped shared-helper package (owner ruling D-8): a pure pattern table has
no dependencies, so it is the natural home, and it keeps `agent_common` from
importing a checker — the one edge the row's spec explicitly forbade.

### Driven measurement — before/after, both directions

fig: cmd="load check_privacy and agent_common by path, then evaluate KEY_RE + TOKEN_RES against _SECRET_RES over the five samples in the table" rev=2f054aab-dirty

| sample | hook scanner | transcript redactor (before) | transcript redactor (after) |
| --- | --- | --- | --- |
| PEM private key block | catch | **MISS** | **catch** |
| `Bearer <30 chars>` | miss (deliberate) | catch | catch |
| `ghp_` + 36 chars | catch | catch | catch |
| `ghp_` + 24 chars | miss (deliberate) | catch | catch |
| `sk-` + 22 chars | miss (deliberate) | catch | catch |

Row 1 is the fix. Rows 2, 4 and 5 are UNCHANGED — deliberate asymmetries
(`SECRET_CLASSES`'s own per-class comments): the redactor's threshold may
legitimately stay looser than the floor's, because a false-positive redaction
costs a reader nothing while a false-positive commit refusal costs a
contributor a lot. Asserting one side "contains" the other was explicitly not
done — the pin is on class coverage against each side's own recorded claim,
not on equality between the two lists.

**Regression proof, not just the five samples.** `tests/test_kitlib_secret_classes.py`
also carries a frozen, independent record of every pattern each module
compiled BEFORE this row (`_PRE_SCAN`/`_PRE_REDACT`, copied from git history,
never re-derived from the shared table) and drives both the old and the new
pattern over threshold-straddling probes per class, asserting they agree.
Confirmed: the enforcement floor's `KEY_RE`/`TOKEN_RES` are byte-for-byte
identical to their pre-row literals; every pattern the redactor compiled
before this row still matches everything it matched before (the one class
whose literal text changed, `slack token`, is a character-class member
REORDER — `xox[baprs]-` to `xox[abprs]-`, the same five letters — proven a
matching no-op over all six candidate 4th characters before being treated as
equivalent, not asserted).

### What was deliberately NOT unified (the spec's MUST NOTs, honored)

- **`redact_secrets` stays "deliberately imperfect."** Unknown token shapes
  still pass through; the raw unredacted stream still lands in gitignored
  `out/run-logs/`. This row closes the one measured, avoidable gap (a known,
  compiled class reaching the redactor), not exhaustiveness.
- **The three threshold asymmetries (`github token`, `github fine-grained
  token`, `api secret key`) are UNCHANGED**, on either side. The floor's
  tighter pattern was never touched — narrowing a false-positive-blocking
  pattern is a behavior change with real cost, not a cleanup.
- **`generic bearer token` was NOT added to the enforcement floor.** It has no
  distinguishing marker the way `ghp_`/`sk-`/`AKIA`/a PEM header do, so adding
  it to a commit-blocking floor risks refusing ordinary documentation edits —
  a design call outside this row's minimum (`SECRET_CLASSES`'s own comment
  records the decision).
- **`agent_common` does not import `check_privacy`.** The extraction went DOWN
  into `kitlib`, per the spec's explicit watch-for.

### Never-weaken proof

Before writing any code, the pre-row patterns were captured and compared to
the derived ones by MATCHING BEHAVIOR (not string identity, since the slack
token spelling changed cosmetically): `tests/test_kitlib_secret_classes.py::test_pre_wi520_scan_behavior_is_preserved`
and `::test_pre_wi520_redact_behavior_is_preserved_or_is_the_declared_addition`
parametrize every class against threshold-straddling probes. Nothing caught
before is caught less after; the one class gaining a redact pattern (`private
key header`) is the row's own stated minimum, asserted explicitly rather than
left to a passing coincidence.

### Spine

Two new Drafted rows (SR-017/SR-176 are both Approved, so nothing under them
is rewritten): `LLR-205` (`kitlib/secret_classes.py`, component `CMP-006` —
pure data, stdlib only, no sibling import, the same single-owner shape
`LLR-184`'s `ladder.py` established for a data-only kitlib module) and
`TC-201`. `docs/id-watermark`
bumped LLR 204→205, TC 200→201 via `trace.py --bump-ids`. `components.toml`'s
`CMP-006` notes gained one clause naming the new module, matching how every
prior kitlib module addition was recorded there. `docs/requirements/
components.derived.toml` (the generated component-view artifact) was STALE
after `LLR-205` landed — the pre-commit hook's `component-view` step caught
it and refused the first commit attempt; `gen_components.py` was re-run
(SR-017/SR-176 now correctly appear in `CMP-006`'s `sr_shared_refs`, since
`LLR-205` is the first row to cite both under a component neither SR was
previously placed in). `docs/stage` regenerated (fingerprint moved, drafts
4→6); `docs/status.md` and `PROJECT_STATE.html` regenerated to match.

**One owner-owed observation, not fixed here.** `LLR-177`'s Approved `detail`
cell enumerates the redactor's classes by name ("API keys, GitHub tokens and
PATs, AWS key ids, Bearer tokens, Slack tokens") and does not mention the PEM
class this row adds — a factually incomplete enumeration now, left untouched
because rewriting an Approved cell is the owner's act, not a worker's. Worth a
line at the next ratification pass over `SR-176`.

**One instrument gap noticed in passing, out of this row's scope.** Adding
`LLR-205` made `check_privacy.py` (`CMP-007`) and `agent_common.py` (`CMP-008`)
import a `CMP-006` module for the first time on a genuinely disjoint-component
edge — exactly the shape `cross_component_findings` (`SR-159`/`LLR-067`) exists
to police. It fired nothing, checked directly: `_classifiable_edges` records
the import stem as the dotted `kitlib.secret_classes` (from `internal_imports`'s
own `prefix + sep + sub` construction) but looks it up in a table keyed by the
BARE last path segment (`by_stem`, keyed off `n.rsplit("/", 1)[-1]`) — those
two strings never match, so the edge is silently treated as
"unknown/ambiguous stem" and skipped. Confirmed systemic, not new: every
existing `kitlib` submodule import (`config`, `git`, `registry`, `ladder`,
`stage`, `evidence`) shows the identical zero classifiable edges, which is
presumably also why none of THEIR `docs/kernel-modules-allow` entries have
ever had occasion to be exercised by this particular code path. Not fixed
here — it is a pre-existing gap in an unrelated checker, orthogonal to a row
about the credential-pattern vocabulary, and `check_trajectory.py --strict`
exits clean either way.

### Ratchets re-stamped, reasons recorded at each site

- `tests/test_module_size_ratchet.py`: `agent_common.py` 2634→2643 (+9),
  `bootstrap.py` 3138→3146 (+8) — the new import, the derived-tuple
  comprehensions replacing hand-copied literals, and one new `MAPPING` row.
- `docs/stack.ini` `[smoke-budget]`: `max-tests` 1335→1367 (+27, the new
  in-process test module — every node is a pure regex/string call, no
  subprocess, no scaffold). `seconds` untouched at 60 (measured well under:
  see Gates below).

### Gates

Per-commit bar (final, on the fully-settled tree): `pytest -q -n auto -m
smoke` green (1353 passed, 6 skipped, 1359 total — matches `--collect-only`,
19.58s); `check_smoke_budget.py --mode enforce`: 19.9s vs 60s budget, within;
`check_docs.py --stale`: OK (1093 docs, 1436 links, 0 broken — the "possibly
stale" hints are pre-existing, unrelated log/archive entries).
`check_trajectory.py --strict`: clean (0 errors — fixed two along the way,
see below). `derive_stage.py --check`: up to date.

Full unfiltered suite, two foreground batches at the smoke/slow boundary —
run TWICE, because the first "not smoke" pass caught a real staleness bug and
the second overlapped with two later prose-only fixes, so neither run alone
is the honest final record; both tails are pasted, not summarized:

```
# First pair (registry additions in, close not yet done):
python -m pytest -q -n auto -m smoke
1353 passed, 6 skipped in 22.65s

python -m pytest -q -n auto -m "not smoke"
1 failed, 1691 passed, 9 skipped in 613.41s (0:10:13)
  FAILED tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current
  (docs/stage's committed fingerprint predated the LLR-205/TC-201 registry
  edits above)

# Fixed: python project-trajectory/scripts/derive_stage.py; spot-verified:
python -m pytest tests/test_derive_stage.py -q
18 passed in 44.07s

# Second pair, after closing the WI (archive move + status.md/specref fixes,
# below) and re-running the smoke tier clean again:
python -m pytest -q -n auto -m smoke
1353 passed, 6 skipped in 21.14s / 20.52s / 30.01s (three re-runs across the
close-out edits, all green)

python -m pytest -q -n auto -m "not smoke"
1692 passed, 9 skipped in 615.00s (0:10:14)
```

**The second "not smoke" run is not trusted at face value**, even though it
came back green: two prose-only wording fixes (an overclaim in `LLR-205`'s
`Rationale` and in `kitlib/__init__.py`'s docstring — both said the module
"imports nothing," which is false; it imports `re`/`typing`) landed on disk
*while that run was in flight*, changing `low-level-requirements.toml`'s
bytes mid-run. `derive_stage.py --check`, run immediately after, correctly
reported `docs/stage` STALE from exactly that edit — proof the fingerprint
is content-sensitive and proof the overlap was real, not hypothetical. Rather
than accept a green produced by an inconsistent tree, `docs/stage` was
regenerated a final time and `test_derive_stage.py` was re-run alone (18
passed) on the truly final, settled tree; the two wording fixes touch only
prose/comments (no executable line), so nothing else in the full run could
have been affected by the overlap — but that is stated as reasoning, not
substituted for a rerun on the one test that measurably was.

3060 collected total (`--collect-only`); 1359 + 1701 = 3060 both times.

`check_trajectory.py --strict` was RED before this session's registry edits
were finished (one ERROR: `scripts/kitlib/secret_classes` named in the
arch-map but tagged to no `CMP-###` component) — the new module needed a
spine row before it could be classified, which is exactly what `LLR-205`
supplies. It is CLEAN now (exit 0). `trace.py --strict` (a stricter, separate
tool the commit bar does not name) carries 3 pre-existing findings unrelated
to this row (`LLR-197`'s own citation-frame debt, `SR-181`'s orphan status) —
confirmed unchanged by diffing against the pre-session baseline; this row
introduces zero new `trace.py` findings (two near-misses in `LLR-205`'s own
`Detail`/`TC-201`'s own `Method` — a `WI-508`/`WI-520` citation and, briefly,
the retired `ratif*` word — were caught by the same gates and corrected before
commit, not left for a later sweep).

Two more self-corrections caught before commit, recorded rather than quietly
folded in: `check_docs.py --stale` briefly FAILed on a mis-counted relative
link in the archived spec's Deliverable (two `../` where the file's new depth
under `docs/archive/work/complete/` needs three), fixed and re-verified clean
(0 broken, the one pre-existing gitignored-report orphan unchanged). And the
three literal PEM-header samples this file's own driven table and fixture
needed (`"-----BEGIN RSA PRIVATE KEY-----"` — privacy-ok: a documented example
of the pattern class, not a key, spelled out because the class's scan pattern
is a fixed header with no length to construct at runtime, unlike every other
class's samples) each carry an inline `privacy-ok` marker with a reason at
their own site in the source file, per the WI-508 sitting's precedent —
confirmed by both a targeted scan and a full `check_privacy.py --repo` sweep
reading clean.

### Deviations from spec

- The spec's Watch-for anticipated the new module needing a `bootstrap.py`
  MAPPING row, a `tests/test_bootstrap.py` file-list entry and a
  `RESYNC_PACK.md` entry; all three landed as described. It did not anticipate
  the module needing its own spine row to satisfy `check_trajectory.py`'s
  component-coverage check — that surfaced only when the full check was run,
  and `LLR-205`/`TC-201` (Drafted, per the "never rewrite Approved" rule) are
  the result.
- Claimed directly to `docs/archive/work/complete/` without the intermediate
  `docs/work/active/` hop the session opened by naming — the work completed
  within one continuous sitting with no handoff in between, so the
  intermediate state was never observed by anything that reads it.
