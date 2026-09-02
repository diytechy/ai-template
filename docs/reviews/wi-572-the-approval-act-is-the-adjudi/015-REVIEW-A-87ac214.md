# WI-572 REVIEW-A round 5 — tip 87ac214

Independent review. Scope: `git diff contract_split...HEAD` minus telemetry,
verdicts and generated artifacts. Requirement surface read: the archived spec
`docs/archive/work/complete/WI-572-the-approval-act-is-the-adjudi.md`, the cited
rows `LLR-158`/`LLR-129`/`IF-091`/`IF-092`/`OI-45`, PROCESS.md §4 and
PROCESS_OPTIONS.md "Who performs the approval act".

## Harness, run here

`python project-trajectory/scripts/check.py --jobs 0` — Check summary (stage
DevStg-LLReqs, tier all): registry-integrity PASS, vocabulary PASS, need-form
PASS, privacy PASS, doc-navigability PASS, skills-index PASS, prompt-catalog
PASS, staged-divergence PASS, approval-immutable PASS; derived-stage and
approval-fresh SKIP (work branch — trunk lane's). `RESULT: PASS`.

`python project-trajectory/scripts/trace.py --strict-integrity` — final line:
`Traceability: SN=27 SR=76 LLR=188 TC=187 orphans=2 integrity=0
verified-mechanized=72 verified-demonstrated=3 verified-attested=0 drafts=9
budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=162
interface-findings=0 provenance-findings=1 paraphrase-advisories=3.`

Touched test modules: `296 passed in 18.98s`.

## Worst failure classes hunted, in order

Fail-open at the merge slot; silent wrong content in the first-approval act;
data loss through the `read_specs` folder-home change.

**Driven, not read.** I built scaffolds and ran the shipped functions.
`_approval_act_refusal` refuses a work lane flipping `Drafted -> Approved` AND
`Drafted -> Founded`, and returns `None` for a `safety_class = "adjudication"`
lane performing the same flip — both arms confirmed live. `first_approval_values`
driven against this repo's real spine: scope `{LLR-205}` yields
`registries='docs/requirements/low-level-requirements.toml=WI-999'` and labels
`TC-201` out-of-scope; empty scope, an absent id and an already-`Approved` id all
REFUSE. The scope regression is genuinely mutation-proven — mutating
`in_scope = rid in scope` to `True` in a throwaway worktree fails
`test_the_first_approval_act_cannot_widen_past_the_rows_the_merge_handed_over`.

## Done-when mapping

1. Lanes cannot approve — COVERED (5 merge-slot tests; re-driven here, incl. `Founded`).
2. First-approval arm exists — COVERED at trigger and brief; **the `_adjudication_lane` exemption is UNCOVERED** (finding 3). The derived `--approves` half FAILS for multi-registry batches (finding 1).
3. Amendment aftermath derived — COVERED (`_aftermath`, both dial arms).
4. Doctrine stated once — prompt-catalog and doc-navigability PASS.
5. Tests — present and in-style; mutation-proof confirmed.

## Findings

- [BLOCKER] project-trajectory/scripts/adjudicate_brief.py:766 -> `first_approval_values` builds the derived `--approves` argument with `" ".join(...)`, but `baseline_snapshot.parse_approves` splits on `;` (its docstring: "`;`-joined `REGISTRY=REF` pairs, the kit's CLI list idiom"). A batch spanning two registries is the NORMAL case — `_first_approval_drafts` mints ONE row over every `Drafted` row of the merge regardless of registry, and this repo right now holds `LLR-205/206` beside `TC-199..204`. Driven: scope `LLR-205;TC-199` renders `'docs/requirements/low-level-requirements.toml=WI-999 docs/test/test-cases.toml=WI-999'`; pasted unquoted into the template's step 2 the real CLI dies with `intake.py: error: unrecognized arguments: docs/test/test-cases.toml=WI-999`, and quoted it SILENTLY mis-parses to `{'docs/requirements/low-level-requirements.toml': 'WI-999 docs/test/test-cases.toml=WI-999'}` — the second registry is neither authorised nor copied, and the corrupted ref is written verbatim into the snapshot's prose stamp, which "nothing validates, because nothing can". The adjudicator flips both Statuses (step 1) and the test-cases snapshot never moves: precisely the "approved-but-unanchored" state step 2 exists to prevent. -> join with `;` instead of `" "`. Cannot be made unrepresentable by a guard because the defect is a delimiter chosen TWICE — hand-joined here, hand-split in `baseline_snapshot`; the antidote (`antidote`'s "smallest change that makes this fix unnecessary") is a single owning boundary: give `baseline_snapshot` the inverse of `parse_approves` (`format_approves(mapping) -> str`) and have every producer call it, so no second module ever picks the separator. -> @owner

- [MINOR] project-trajectory/scripts/acceptance_record.py:587 -> the refusal text states an UNQUALIFIED rule — "does not flip a `Status` into `Approved`/`Founded`, does not mint a row already claiming one" — but `staged_approval_acts` walks only `SPINE_CSVS` (acceptance_record.py:122), which is SR/LLR/TC. The SN tier carries real approval status (all 27 `stakeholder-needs` rows read `Approved`) and all 162 `interfaces` rows read `Drafted`, so a lane flipping one of those to `Approved` is admitted silently while the refusal's own wording says it cannot be. The omission is pre-existing and deliberately declared in the `SPINE_CSVS` comment ("The SN tier is not listed ... doing so is its own decision"), so this is the new text over-claiming its reach rather than a new hole. -> for clarity, qualify the refusal and the `lane_approval_refusal` docstring to name the three registries the rung actually reads, so a lane cannot infer coverage the rung does not have. No antidote clause owed: this is a wording finding, not a compensating guard. -> @owner

- [MINOR] project-trajectory/scripts/integrate.py:1102 -> `_adjudication_lane` is the EXEMPTION that disables the whole approval rung, and no test drives it — `grep _adjudication_lane tests/` returns only the module-size ratchet's prose. It is the single highest-leverage predicate in the change: True for a work lane and every rung in this WI is bypassed; False for an adjudication lane and the arm can never land its flip, making the feature inert. I drove both arms by hand and both are correct today, so this is missing coverage, not a defect. -> pin both arms beside the five existing merge-slot tests (an `adjudication` lane's flip admitted; an `ordinary` lane's refused; unreadable frontmatter refused). Cannot be made unrepresentable because the exemption is a genuine trust boundary — the ruling names the adjudication session as the actor, so some predicate must decide who the actor is; what is available is making that predicate's two callers share one tested reader rather than two `safety_class` reads with opposite defaults. -> @owner

VERDICT: CHANGES-REQUESTED findings=3
