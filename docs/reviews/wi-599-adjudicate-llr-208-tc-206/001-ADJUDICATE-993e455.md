# ADJUDICATE — WI-599 — amendment at 993e455

Question judged, per row, and the only one: did the amendment change the
requirement's MEANING, or only its CLARITY?

Scope verified independently against the anchor
(`docs/archive/last_approved/`, copied 2026-09-04 at 2c309c6a) rather than
taken on trust, by loading both sides and diffing every key of every row:
21 rows differ. In `system-requirements.toml` the ONLY differing key on all
17 SR rows is `rationale` — `title`, `statement`, `acceptance`, `sn_refs`,
`hat_refs`, `boundary_refs` and `status` are byte-identical, and every row is
`Approved` on both sides. In `low-level-requirements.toml` and
`test-cases.toml` four rows differ, and each differs in MORE cells than the
brief named: LLR-207 and LLR-208 also moved `code_symbol`, TC-205 and TC-206
also moved `evidence`. Those extra cells are recorded below beside the cells
I was briefed on, because a re-anchor absorbs them too and a judge who
copies a cell he never read has blessed it silently. `SR-183` is live-only —
a NEW row, not an amendment — and is outside this verdict.

The 17 SR rows are the identical set adjudicated CLARITY at WI-547 and again
at WI-593 (`docs/reviews/wi-593-adjudicate-llr-197-approved/001-ADJUDICATE-ae3d788.md`).
They are re-derived here from the anchor, not carried over, and the verdict
is reached independently; the concurrence is noted, not relied on.

The four LLR/TC rows are a different case, and they are why this verdict is
MEANING. Each states a NEW mechanism that did not exist in the text a human
blessed, and each is corroborated by the `code_symbol`/`evidence` cells that
moved with it: a correct implementation of the BEFORE text peels only a
refresh, writes a rollup from any branch, and runs TC-205 at the commit
floor — and would FAIL the AFTER text on all three counts.

Blessability, checked before re-anchoring rather than assumed from the diff:
`verdict.mechanical_close_attestation` / `_closed_wi_ids` / `_peel_target`
and `gen_verdict_rollup._off_trunk_refusal` all exist and read as the amended
cells describe them (one parent, `--no-renames` stream wholly under
`docs/work/`, one source `active/<branch>/`, unrecognised `A`/`D` refuses,
`M` unrestricted, exact composed-subject equality; exit 2 off trunk with
`--check` and `--trunk-step` exempt). The over-determined empty-close
refusal the LLR-207 cell states is present in `_closed_wi_ids`'s own
docstring in the same terms. TC-205's `Tier` correction is verified at its
root: `test_integrate_admission`, `test_integrate_station` and
`test_handback` are all three in `tests/conftest.py` `SLOW_MODULES`, so the
cited set does not run under `-m smoke` and `Smoke` was an over-claim.
`tests/test_verdict_record.py tests/test_trunk_step.py` plus
`test_handback.py::test_the_close_the_writer_lands_is_one_the_attestor_peels`
— 94 passed in 53.32s on this tip.

- [CLARITY] SR-024 Rationale -> dimensional coverage is GENERATED from the SR's declared inputs, not hand-listed; the charter's fail-when-it-should half stays a separate obligation -> same -> only the `Hat-derived (hat.TEST-ENGINEER):` label dropped; "Systematic expansion reduces the risk…" and the both-halves carve-out are otherwise byte-identical, and `hat_refs` still carries the lens.
- [CLARITY] SR-033 Rationale -> the release gate carries a generated checklist surfacing warn-tier budgets for a human tick-off; the row is this project's ANSWER to the charter question, not a charter-imposed obligation -> same -> only the `Hat-derived (hat.PERFORMANCE),` label dropped; the "no wider than what the charter actually asks" limit and the must-not-be-read-as-prescribed warning survive.
- [CLARITY] SR-043 Rationale -> enumerate the one irreversible actor-starting action with the dial or human authority permitting it; the fail-open arm is deliberate and never relaxes the human-held override -> same -> only the `Hat-derived (hat.SECURITY):` label dropped; "C-SEC-2 asks…" and the whole WHY-THE-FAIL-OPEN-ARM clause are unchanged.
- [CLARITY] SR-052 Rationale -> keyboard operability, an accessible name per element, colour never the only channel, a readable contrast floor; method mechanical, acceptance the child chain -> same -> only the `Hat-derived (hat.ACCESSIBILITY):` label dropped; the ruled-`always` and closed-dependency reasoning survives and the lens is still in `hat_refs`.
- [CLARITY] SR-053 Rationale -> one cross-view coherence property, each clause pinned separately, acceptance the child chain; the fan-out is the anchor census, not a decision count -> same -> only the `Hat-derived (hat.CONSISTENCY):` label dropped; the sole-deriving-lens argument and the re-open-if-the-charter-is-cut note survive.
- [CLARITY] SR-054 Rationale -> task-level findability and legibility-as-robustness written from stakeholder intent; the one unpinnable first-time-reader clause named as a limit at the child -> same -> only the `Hat-derived (hat.UX-DESIGNER + hat.UX-ENGINEER):` label dropped; C-UXD-1/C-UXE-2 and the both-`always` reachability claim survive, and the now-unnamed "the designer's"/"the engineer's" referents are still carried by `hat_refs`.
- [CLARITY] SR-111 Rationale -> a recorded-origin stamp lets a maintainer identify the upstream version a scaffold came from and compute a re-sync diff; hash-derived versioning rejected -> same -> the trailing `Hat-derived (hat.MAINTAINER): C-MNT-7 …` block removed whole, including its own statement that the obligation "stands without the citation"; that block located where a clause is DEFINED and imposed nothing on a builder.
- [CLARITY] SR-112 Rationale -> per-agent skill copies are generated, the fan-out is forced, drift is a finding, and generated-marking stops a maintainer editing a disposable copy -> same -> the trailing `Hat-derived (hat.MAINTAINER):` block and the "same disposition as SR-111" note removed; the "identify itself as generated" substance is already carried by the surviving generated-marking sentence.
- [CLARITY] SR-129 Rationale -> the CAPABILITY is the converter as the check on a representation change; layout and claim detection belong to LLR-136; the 140-cell lesson -> same -> only the `Hat-derived (hat.TEST-ENGINEER):` label dropped; "A converter is the check on a representation change…" and the cell-exact round-trip survive.
- [CLARITY] SR-144 Rationale -> an immutable per-close record reconstructed from no mutable proxy; the split is a field because silence is unactionable -> same -> only the `Hat-derived (hat.UNATTENDED-OPS):` label dropped; the C-UNA-3 deadlocked-until-morning and C-UNA-5 pages-nobody clauses survive verbatim.
- [CLARITY] SR-146 Rationale -> steering prose ships as a reviewable file with a per-session digest; the transport decision stays one tier down at LLR-163 -> same -> only the `Hat-derived (hat.SECURITY):` label dropped; "C-SEC-5 requires that content composed for dispatch … carry a DECLARED inclusion rule" survives word for word.
- [CLARITY] SR-147 Rationale -> ONE obligation, a single structured carrier proved cell-for-cell by the converter BEFORE the authority flip; the measurement and the one-row argument -> same -> only the `Hat-derived (hat.TEST-ENGINEER):` label dropped; the enforcer-must-be-shown-to-bite clause survives.
- [CLARITY] SR-149 Rationale -> the vocabulary conversion is a standing CONDITION, carved out so history is not rewritten and an attestation never re-worded -> same -> only the `Hat-derived (hat.MAINTAINER):` label dropped; "C-MNT-3 gives every declared vocabulary value exactly one normative definition in one home…" survives intact.
- [CLARITY] SR-167 Rationale -> the perf verdict itself, BOTH breach arms in one exit contract, naming no artifact; vacuous here but shipped; the LLR-014/TC-014 re-point deliberately still owed -> same -> only the `Hat-derived (hat.PERFORMANCE):` label dropped; the charter's-third-clause paragraph and the still-owed act survive unchanged.
- [CLARITY] SR-175 Rationale -> a declared inclusion/exclusion rule for repository content briefed to external providers, content beyond SN-026's demand; the pull-channel limit and the not-yet-mechanized list -> same -> the front `Hat-derived (hat.DATA-PROTECTION, with hat.SECURITY C-SEC-5 and hat.LEGAL C-LEG-3 …)` wrapper is restructured in place into "derived from the data-protection lens, with the security and legal lenses converging on the same boundary control (three charters, three reasons, one crossing)"; the three-charters/one-crossing content, the amend-SN-026 rejection, the discipline-not-declaration account and the pull-channel limit all survive. The dropped `C-SEC-5`/`C-LEG-3` ids and plan path pointed at where a lens is written down; they were not conditions on this row.
- [CLARITY] SR-176 Rationale -> the matched value never reaches durable storage (the deliberate narrowing of C-DPR-2's retention/access ask); credential shapes redacted today, the PII classes the stated build debt -> same -> only the front `Hat-derived (hat.DATA-PROTECTION, C-DPR-2 — clause text …):` wrapper dropped; C-DPR-2 is still named where the narrowing is recorded, and the measurement, the mechanized half and the not-yet-mechanized half are untouched.
- [CLARITY] SR-177 Rationale -> the throughput claim made OBSERVABLE rather than BUDGETED, with the numeric-target refusal and its reason; lanes=1 here; NOT DECOMPOSED, the aggregation surface the whole build gap -> same -> only the front `Hat-derived (hat.PERFORMANCE, C-PRF-1 — clause text …):` wrapper dropped; C-PRF-1 is still named where the deliberate-less-than narrowing is recorded.
- [MEANING] LLR-207 Detail (and `code_symbol`, unbriefed, moving with it) -> the read-only `governing_rev` walk peels ONE disposable commit class, "any verified refresh it meets", and a branch with no refresh under it still walks -> TWO classes are disposable and the walk peels BOTH: the station refresh AND the machinery's own adjudication close, admitted by a NEW verifier `mechanical_close_attestation` against exactly one parent, a `--no-renames` changed-path stream wholly under `docs/work/`, deletions from exactly ONE `docs/work/active/<branch>/` paired with same-name additions under `complete/`, any unrecognised `A`/`D` refusing the whole commit while `M` rides free, ids ordered by the shared `mechanical_close_order` and composed through `mechanical_close_subject` to equal the subject exactly; plus the new statement that `work_tip` deliberately does NOT share this test -> the obligation moved on every axis the rung names. A behaviour was added (a second peelable class), an acceptance condition was added (six verification arms that did not exist), and a scope was drawn (the reset path excluded). A `governing_rev` correct under the BEFORE text peels no close and FAILS the AFTER text; `code_symbol` gaining `mechanical_close_attestation` is the same change restated in the cell that lists the seam.
- [MEANING] TC-205 Method + Tier (and `evidence`, unbriefed, moving with it) -> Method: drive the refresh peel and its refusal arms; Tier: `Smoke`, i.e. the arms must run at the commit floor -> Method: additionally drive the SECOND disposable class end to end — a positive asserted to have really moved the tree, the two peels COMPOSING, six named refusals each driven with every other clause satisfied, the two-row batch seeded non-canonically, the writer driven against the verifier through `handback.close_adjudication`, and the empty close asserted at the attestor and deliberately NOT at the gate; Tier: `Full` -> both cells moved the obligation, and either alone would carry the row. Method: a test suite satisfying the BEFORE text contains none of these arms and fails the AFTER text; `evidence` gaining nine `test_..._close_...`/`_peel...` ids plus the `test_handback` cross-check is that same addition in the cell that names the tests. Tier: the tier a row is run at is an acceptance condition, and `Smoke`→`Full` changes WHICH gate must see it green — correctly, since the cited set now includes three `SLOW_MODULES` modules that `-m smoke` deselects, so `Smoke` was claiming commit-floor coverage the commit floor does not give. A truthful correction is still a moved obligation.
- [MEANING] LLR-208 Detail (and `code_symbol`, unbriefed, moving with it) -> the exclusive-writer clause is held by ONE mechanism, membership in the trunk step's `verdict-rollup` regen set, and the work-branch stand-down; nothing refuses a direct write -> TWO mechanisms hold DIFFERENT halves and neither substitutes for the other: freshness is still the regen set, but enforcement is a NEW `_off_trunk_refusal` that exits 2 whenever the checkout is on a branch other than `agent_common.trunk_name` (the primary checkout's branch), with exactly one exemption, the trunk step's own `--trunk-step`, and `--check` never refused -> a new actor-scoped refusal with a new exit code and a declared exemption set. A generator correct under the BEFORE text returns 0 and writes from a lane; under the AFTER text that is a defect the row now forbids. `code_symbol` gaining `_off_trunk_refusal` restates it.
- [MEANING] TC-206 Method (and `evidence`, unbriefed, moving with it) -> drive the rollup as derived state: the three `--check` answers, the extra/prune arm, the flat pre-train layout and its collision refusal, the header sentence, and the trunk wiring -> additionally drive the exclusive writer as ENFORCED, in a real LINKED worktree on a claimed branch: the direct write asserted to exit 2 leaving NO file behind, and BOTH exemptions driven beside it (`--check` unrefused, `--trunk-step` writing) -> a required test arm was added, and one that cannot be reached by the single-checkout fixtures every other arm uses. A suite satisfying the BEFORE text omits it and fails the AFTER text; `evidence` gaining `test_a_work_branch_cannot_write_the_rollup_but_the_trunk_step_can` is the same addition in the cell that names the tests.

VERDICT: MEANING rows=21

## Aftermath performed

The LLR/SR/TC rungs are RELEASED to the loop by the declared gate authority,
so the re-attestation is this session's. Taken in its OWN commit, separate
from this verdict, with no `Status` edited and no registry CELL touched.

**Scope of the re-anchor, and it is deliberately narrower than the rows
judged.** `intake.py snapshot --approves` is copied per registry
(`baseline_snapshot._authorised_registries`), so the act can name
`docs/requirements/low-level-requirements.toml` and `docs/test/test-cases.toml`
and leave `system-requirements.toml` byte-identical. It does. The 17 SR rows
are CLARITY: their attestations stand, they owe no fresh one, and absorbing
them into the anchor under a MEANING verdict about four unrelated rows would
launder seventeen copies nobody asked for. That is a real cost, stated rather
than hidden: because a CLARITY verdict by design does not re-anchor, this
same SR drift will raise this same row a fourth time (WI-547, WI-593, here).
It is a detector/aftermath seam, not a defect in any of the three verdicts,
and it is not this row's to close.

LLR-207 and TC-205 are `Drafted` on BOTH sides — no attestation exists on
them to have been falsified, so the MEANING ruling above is the honest answer
to the question asked and not an approval act. Their amended text rides into
the anchor as file-scope collateral of copying the two registries, which is
inherent to a byte-for-byte carrier copy and is recorded here so the copy is
not read as a blessing of a row no one has approved.

No `## Dispositions` are drafted: every amended cell was verified against the
shipped code and the cited tests, and all four MEANING rows state what the
machinery actually does. There is nothing here I would decline to bless.
