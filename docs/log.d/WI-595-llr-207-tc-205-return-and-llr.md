## 2026-09-04 — WI-595: LLR-207/TC-205 return and LLR-208/TC-206 amendment

The verdict rows describe every mechanism that now holds them. Two cells
returned by `docs/reviews/wi-590-adjudicate-llr-207-llr-208/004-ADJUDICATE-774ef35.md`
(`OUTCOME: RETURN rows=4`), plus round 011's MAJOR against two rows that act
approved. The initial return named existing mechanisms; review round 005 then
found that one of those mechanisms was weaker than the returned row claimed,
so this same WI now carries its boundary hardening and regression too.

### Rework round 2 — forged-middle close subject

Review A round 005 demonstrated that `mechanical_close_attestation` validated
only the mechanical subject's prefix/suffix shape, not the exact composed WI
ids claimed by `LLR-207.detail`. Root cause: the one owning verifier never tied
the untrusted commit message's middle to the `docs/work/` rename it was
attesting. The owning verifier now derives those ids from paired same-name
active-to-complete moves in the commit's own no-renames diff and compares the
subject re-composed by the writer's helper. The real-git regression commits an
affix-correct forged middle over an otherwise plausible move, asserts
`mechanical_close_attestation` returns `None`, and asserts the merge gate asks
for review. TC-205 cites that node, LLR-207 states the strengthened contract,
and the approval brief was regenerated.

**Re-drove the spec's four claims before editing anything.** All four hold on
this tree:

- `_peel_target` (`kitlib/verdict.py:431-442`) peels TWO classes, not one —
  `refresh_attestation` and `mechanical_close_attestation` (`:376-428`).
- `work_tip` calls `refresh_attestation` DIRECTLY (`:466`), never
  `_peel_target`, so the reset path peels only the refresh. The asymmetry is
  deliberate and was invisible in `LLR-207.detail`.
- `mechanical_close_attestation` is an `__all__` export (`:141`) and
  `grep -rn 'mechanical_close' docs/requirements/ docs/test/` returns ZERO
  rows — `LLR-207` is not one of several possible homes for it, it is the only
  one.
- `gen_verdict_rollup._off_trunk_refusal` (`:227-249`) refuses a direct write
  off the trunk with exit 2 (`main`, `:268-272`); `trunk_step.py:591` passes
  `--trunk-step` as the one allowed off-trunk caller.

### What changed

`LLR-207.detail` — the `governing_rev` clause said the walk peels "any verified
refresh it meets". Restated to name both disposable classes, the ONE property
that admits them (machine-authored, and the tree moves without the lane
changing what it claims), the verification each is admitted by, and the
fail-toward-review direction. Added the `work_tip` asymmetry explicitly: the
destructive reset path peels only the refresh.

`LLR-207.code_symbol` — added `mechanical_close_attestation` beside
`refresh_attestation`. `_peel_target` deliberately left out: private, and the
two attestation readers are the named surface.

`TC-205.method` / `.evidence` — `THE PEEL` enumerated the refresh arm alone and
neither cell held the string "mechanical". Added the second class in the same
idiom the rest of the cell uses — the positive and its refusal arms — and cited
the three tests that already drove it but that no test case anywhere cited:
`test_the_mechanical_close_does_not_stale_the_round_it_follows`,
`test_only_the_machinerys_own_close_subject_peels`,
`test_a_close_that_reached_outside_docs_work_does_not_peel`. The positive also
drives the two peels COMPOSING (a refresh stacked on a close), which the cell
now states. Rework round 2 adds the distinct affix-correct forged-middle
refusal and its new evidence node.

`TC-205.tier` — re-tiered `Smoke` -> `Full`, and the basis is recorded in
`Method` so the reading is not left open. Ruled rather than deferred: 8 of the
row's 50 citations live in `test_integrate_admission` / `test_integrate_station`,
both in `tests/conftest.py` `SLOW_MODULES` and so excluded from `-m smoke`.
`Full` is the smallest tier at which the WHOLE cited set runs, `Smoke` claimed
cheap-gate coverage for a set the cheap gate only partly runs, and sibling
`TC-132` already reads `Full` while citing the same station module. The Tier
field and the pytest marker remain a known unreconciled pair
(`docs/registry-machinery-reference.md` §12.2); this edit does not reconcile
them, it stops this row from misreporting on the side §12.2 names as the
harmful one.

`LLR-208.detail` (AMENDMENT to an Approved cell, §A5.2) — the cell said regen-set
membership "is the only thing that makes the exclusive-writer clause above
true". False since `7ea3cce7`. Amended to state BOTH mechanisms and keep them
distinct: `_off_trunk_refusal` is what ENFORCES the clause, regen-set membership
is what keeps the artifact FRESH. Neither substitutes for the other — a refusal
with no regenerator leaves the artifact written by nobody, and a regenerator
with no refusal is the state that shipped the WI-590 round 005 defect.

`LLR-208.code_symbol` — added `_off_trunk_refusal` (the row already names the
private `_extra`, so this matches its own convention).

`TC-206.method` / `.evidence` — stated the refusal arm and cited
`tests/test_verdict_record.py::test_a_work_branch_cannot_write_the_rollup_but_the_trunk_step_can`.

### Two decisions the cells cannot record themselves

**`LLR-208.hat_refs` left unset, deliberately.** `check_trajectory` warns that
an approved Detail moved while Hat-Refs stayed put, and notes that an unchanged
cell cannot say whether that was a decision. It was: the row carries no
`hat_refs` and inherits `INTEGRITY-RECOVERABILITY` from `SR-170`, which is
exactly the lens the amendment writes about — a refusal that stops a silent bad
write. Setting the cell would OVERRIDE the inheritance rather than add to it, so
the smallest honest edit is none.

Surfaced as a separate finding, not fixed here: the WI-590 round 005 defect was
an UNATTENDED lane writing the artifact with the stand-down hiding it, which
reads as an `UNATTENDED-OPS` concern that `SR-170` does not carry (sibling
`SR-156` carries both). Whether `SR-170`'s hat set is short is a question about
the SR, not about this amendment, and widening an Approved row's perspective
record was not in this return's scope.

**Provenance kept out of the cells.** A first draft of `TC-205.method` named
`WI-586` as the measured failure; `trace.py --strict-integrity` raised it as a
spine stand-alone FINDING (`provenance-findings=1`) and it was rewritten to
state the standing reason instead — the close archiving a judged row stales the
APPROVE that had just judged it, and an adjudication lane cannot avoid it by
ordering because its round is drawn while the row is still in `active/`. The
account lives here; the cell states the system. Same rule applied to
`LLR-208.detail` and `TC-206.method`, which name the failure shape and no ids.

### The peel's path-set arm is NON-EMPTY, and the cell now says so

A later read of `mechanical_close_attestation` caught the first draft of
`LLR-207.detail` under-describing the arm it had just added. The cell said the
close is admitted against "a changed-path set lying wholly under `docs/work/`" —
a clause the EMPTY set satisfies vacuously. The code does not:
`if not paths or any(not path.startswith(_WORK_PREFIX) for path in paths)`
(`kitlib/verdict.py:426`) refuses a zero-path commit outright. The clause now
reads "a NON-EMPTY changed-path set".

This is not pedantry about a set-theory edge: the zero-path commit is a REAL
class in this system, and `TC-205.method` already drives it two sections
earlier — `agent_common.commit_telemetry` writes an empty commit when a
Review-Verdict attestation must land on unchanged bookkeeping, and the cell
records that "that is the commit shape a walk classifying PATHS could not
classify and so stopped at". The `not paths` guard is what keeps the close peel
from being the walk that classifies it wrongly in the other direction. The
module DOCSTRING has the same gap ("every path it changed must live under
`docs/work/`"); the cell is now more precise than the docstring it describes.

FINDING, surfaced not fixed: no test drives the empty-path refusal. `TC-205`
cites the subject refusal and the reached-outside-`docs/work/` refusal, and the
`not paths` disjunct is the third arm with no citation. Writing it is a
regression this return is not scoped for ("no new mechanism and no regression
to write" — the spec's IN SCOPE fence), and the cell does not claim a test it
lacks. Recorded here so a successor can take it deliberately rather than
rediscover it; the same treatment the `SR-170`/`UNATTENDED-OPS` question got.

### Not inherited, not widened

WI-586's findings were re-driven and are all DISCHARGED (the spec's `## Context`
records the re-drive). NOT taken: the module docstring's contract paragraph and
`work_tip`'s docstring (`:448-455`), which still claims "`governing_identity`
measures code-time here" — false since `governing_identity` calls
`governing_rev`. That is a source-comment defect in a code lane's scope, not a
spine cell, and this return did not widen into it.

### Bar

`DevStg-Tests`, strong tier.

**Spine checks, at the pre-close tip `57792a3b`.**
`trace.py --strict-integrity`: `SN=27 SR=76 LLR=191 TC=190 orphans=0
integrity=0 drafts=11 budget-findings=0 component-findings=0
interface-findings=0 paraphrase-advisories=3` — no provenance finding, so the
frame-dropping rework held. `check_trajectory.py`: `clean (595 work item(s),
544 done (91%), 21 cancelled, graph acyclic)`. Both carry only advisory WARNs
that reproduce at the integration base.

**Full unfiltered suite** (`pytest -q -n auto`, the venv interpreter at
`/Users/diytechy/Documents/ai-template/.venv` — this lane is a linked worktree
and has no `.venv` of its own; it was NOT symlinked one):

    1 failed, 3383 passed, 25 skipped in 646.97s (0:10:46)

The one red is `tests/test_derive_stage.py::
test_this_repo_s_committed_stage_is_current`, on the fingerprint alone
(`5ad22a34…` recorded vs `a4bc065e…` derived). It is **CAUSED by this branch
and benign because every derived field is unchanged** — the six registries are
`kitlib/stage.py` `DECLARED_INPUTS`, so any cell edit moves the input hash.

Driven BOTH ways rather than argued, since a bare "per-phase matches" reading
proves less:

- At the integration base `bd431c5b`, in a throwaway `git worktree`, the single
  node PASSES (`1 passed in 0.04s`). So it is this branch's, not trunk's — the
  base is clean, therefore the branch caused it.
- At this tip in a second throwaway worktree, running `derive_stage.py --root .`
  and re-running the same node PASSES (`1 passed in 0.03s`). Diffing that
  regenerated `docs/stage` against the committed one, the ONLY lines that move
  are `fingerprint` and the `# computed … (as-of …)` comment; `stage`,
  `stage-ord`, `stage-of`, `floored`, `settled-stage`, `live-stage`, `phase`,
  `per-phase`, `per-phase-live` and `drafted` (11, unmoved — this return minted
  no new row) are byte-identical.

`docs/stage` was deliberately NOT regenerated on this lane: it is a declared
generated artifact whose freshness is the trunk lane's
(concurrency-restructure §5.2), the commit bar's own `derived-stage --check`
SKIPS on a work branch, and the regenerated bytes above ARE the post-merge
state. The node is in `conftest.SLOW_MODULES`, so the smoke commit bar never
sees it.

**Re-run at the CLOSING tip `23cbacfa`**, because the close is itself an input
change — draining `docs/work/active/` changes what the claim-reading nodes
answer, so the pre-close numbers are a different tree's:

    1 failed, 3387 passed, 21 skipped in 625.67s (0:10:25)

Same single red, same fingerprint pair, same both-ways provenance. The counts
MOVED (3383 passed / 25 skipped -> 3387 / 21) and the four are attributed
rather than assumed: all four are in `tests/test_wi_convert.py`, all four
skipped pre-close with the reason `live registry has in-flight claims: … an
in-flight claim (active/wi-595-llr-207-tc-205-return-and-llr) — conversion is
a drained-stop operation`, and all four PASS once the claim drains —
`test_the_real_registry_produces_one_spec_per_row`,
`test_status_becomes_the_directory_and_cancellation_stays_visible`,
`test_emitted_specs_are_lf_on_every_platform`,
`test_row_order_survives_a_registry_that_is_not_id_sorted`. Measured by running
the module with `-rs` at this tip and in a throwaway worktree at the pre-close
commit `57792a3b`. Nothing regressed; four nodes stopped being masked.

Worth recording because the standing expectation was the opposite: closing the
LAST active claim was known to RED
`test_the_live_registry_round_trips_in_whichever_home_is_authoritative` on
`docs/work/cancelled/README.md: does not start with a +++ frontmatter fence`.
It does not any more — that node PASSES on this drained tip. The
`drained-stop` refusal is no longer masking a real defect behind it.

`trace.py --strict-integrity` and `check_trajectory.py` were also re-driven at
the closing tip: `integrity=0` again, and `clean (595 work item(s), 545 done
(92%), 21 cancelled, graph acyclic)` — the done count up one and both of this
row's own WARNs (the stale `SpecRef` clock, and sharing a spec of record with
WI-598) gone, which is the close registering.

### Rework round 1 — the empty-close finding, taken in the half that holds

Review A (`docs/reviews/wi-595-llr-207-tc-205-return-and-llr/003-REVIEW-A-149698f.md`)
returned one MAJOR: `LLR-207.detail` newly makes a NON-EMPTY changed-path set an
admission condition, and `TC-205` cited no test for it. That half is correct —
the return authored a claim and left it unevidenced, which is exactly the defect
this WI existed to fix in the other direction. A regression now exists and is
cited.

The remedy as SPECIFIED — "a real-git empty-close refusal test that asserts the
merge gate asks for review" — was not written, and the reason is measured rather
than argued. `_peel_target` is the ONLY caller of `mechanical_close_attestation`
(grep over `project-trajectory/scripts` and `tests`), and `governing_rev` does
not merely peel: it also WALKS THROUGH any commit whose non-record identity
equals its first parent's. An empty commit satisfies that by construction. So
the empty-path clause cannot change what the gate answers.

Driven, not reasoned. With `if not paths or …` deleted from
`mechanical_close_attestation` and the whole module re-run:

    1 failed, 57 passed in 58.99s

The single red is the new boundary assertion. On the same fixture — a judged
round, a REAL mechanical close, then an empty commit carrying the composed
subject — `kv.governing_identity` still returns the judged tree and
`integ._verdict_gate` still returns None in BOTH arms. `verdict.py` was restored
byte-clean (`git diff` empty) and the module re-run: `58 passed in 94.18s`.

So the finding's stated consequence — "would let it preserve an earlier
approval" — describes both arms equally, and preserving it is the CORRECT
answer: a commit that changed nothing has invalidated no verdict. A test
asserting a gate refusal here would pin a behaviour the module does not have and
should not acquire. The clause is a guard on a public `__all__` export's
contract, made redundant at the gate by the walk.

What landed:

- `tests/test_verdict_record.py::test_an_empty_close_is_refused_and_the_walk_covers_it_regardless`
  plus its `_empty_close` helper (`git commit --allow-empty`, since a zero-path
  diff is the one close shape a file-writing fixture cannot reach). It asserts
  the refusal AND that the refusal strands nothing — the honest pair.
- `TC-205.evidence` cites it; `TC-205.method` states the third refusal, where it
  is observable, and why the gate assertion is deliberately absent.
- `LLR-207.detail`: "can only ask for more" was overstated in this same spot —
  on the empty arm the later rev carries the SAME identity, so it asks for
  exactly as much. Now "can never ask for LESS", with the equality named.

`LLR-207` and `TC-205` were already `Drafted` and stay so; no `Status` was
flipped and no `docs/archive/last_approved/` written.

### Rework round 2 verification

The forged-middle finding is fixed at the one owning boundary, not papered
over in a caller. `mechanical_close_attestation` now reads a NUL-delimited
`--name-status --no-renames` diff, requires paired same-filename moves from one
active branch into `complete/`, derives their WI ids, and uses
`station.mechanical_close_subject` to compare the exact canonical subject.
The former affix-only constants are no longer imported by the verifier.

Evidence driven on the completed tree:

- Focused forged/positive/empty close selection: `3 passed, 56 deselected in
  9.87s`.
- Whole verdict-record module: `59 passed in 116.87s`.
- Full unfiltered suite: `1 failed, 3389 passed, 21 skipped in 1251.23s`; the
  sole failure is
  `tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current`,
  the worker-lane fingerprint mismatch (`5ad22a…` recorded vs `749e75…` live).
  No generated artifact was rewritten on this branch; the trunk lane owns that
  refresh.
- `trace.py --strict --no-placeholders`: `orphans=0 integrity=0`, exit 0.
- `check_trajectory.py`: `clean (595 work item(s), 545 done (92%), 21
  cancelled, graph acyclic)`, exit 0; its existing advisories include WI-598's
  SpecRef clock because this assigned spine edit necessarily changes the shared
  low-level-requirements file.
- `check_docs.py --stale`: 0 broken links, exit 0. Ruff check and format check:
  clean.
- Smoke tests passed twice under host contention: `1533 passed, 4 skipped in
  155.47s`, then the budget enforcer's independent run `1533 passed, 4 skipped
  in 172.19s`; the latter honestly returned FAIL at `173.0s > 60s`. After the
  new regression entered the tier, a two-worker capped enforcer run passed all
  `1534` tests (4 skipped) in `120.15s` and likewise failed its timing contract
  at `120.4s > 60s`; after the competing smoke runs cleared, six workers
  improved that to `86.3s`, still over. The final 12-worker retry passed the
  same `1534` tests (4 skipped) in `58.93s`, and the enforcer reported `59.2s
  vs 60s budget -> within`. A full suite remained active in the primary
  checkout throughout. The budget was not re-stamped and no heavy module was
  re-tiered to hide machine load.

Deviations from the rework finding: none. Byte-budgeted files changed: none.
Deferred open items: none — round 005's one finding is resolved in this WI.
