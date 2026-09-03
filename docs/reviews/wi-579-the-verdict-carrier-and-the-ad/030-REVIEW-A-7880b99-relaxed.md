# Review A — WI-579 (the verdict carrier and the adjudication_review dial)

Model: anthropic/claude-opus-5 (relaxed heterogeneity)
Reviewed: `7880b998` against `contract_split...HEAD`

## Instruments (run here, summaries only)

`python project-trajectory/scripts/check.py --jobs 0` — Check summary (stage
DevStg-LLReqs, tier all): `registry-integrity PASS`, `vocabulary PASS`,
`need-form PASS`, `privacy PASS`, `doc-navigability PASS`, `skills-index PASS`,
`prompt-catalog PASS`, `staged-divergence PASS`, `approval-immutable PASS`;
`derived-stage` / `approval-fresh` / `verdict-rollup` SKIP ("work branch —
generated freshness is the trunk lane's"). **RESULT: PASS**.

`python project-trajectory/scripts/trace.py --strict-integrity` — final line:
`Traceability: SN=27 SR=76 LLR=190 TC=189 orphans=2 integrity=0
verified-mechanized=72 verified-demonstrated=3 verified-attested=0 drafts=13
budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=163
interface-findings=0 provenance-findings=1 paraphrase-advisories=3.`

## Worst failure classes this change admits, hunted first

The diff moves the merge gate from a hand-authored rollup onto computed
evidence, so the severity-ordered classes are (1) **fail-open at the merge
slot** — a merge cleared by evidence that is not what it claims to be; (2)
**silent wrong content in the identity** — two different trees folding equal;
(3) **wedge / fail-closed** — the two readers disagreeing. Prior rounds have
worked (2) and (3) hard. Finding 1 below is class (1), driven on the shipped
path.

## Findings

- [MAJOR] project-trajectory/scripts/kitlib/verdict.py:598 -> `logged_rounds` joins a round file to its coordinator session log by `(train, ordinal)` alone and only tests that the log's declared phase is a member of `REVIEW_PHASES` (line 590), never that it EQUALS the round file's own phase — so ONE logged REVIEW-A session's telemetry admits a `NNN-REVIEW-B-<sha>.md` written in the same commit, and at `review_rounds = 2` the gate clears on a single reviewer, defeating the independence that is the entire content of policy 2 (LLR-045, "N reviewer sessions over one tree"). Driven end-to-end through the shipped functions on the suite's own `rounds_repo(policy="2")` fixture: with one session log `docs/iteration/wi-401-003-...log` declaring `# phase: REVIEW-A` and both `003-REVIEW-A-7beb7f2.md` and `003-REVIEW-B-7beb7f2.md` committed, `logged_rounds` returns BOTH `(3, 'REVIEW-A', ...)` and `(3, 'REVIEW-B', ...)`; `branch_entries` -> `[('REVIEW-A', 3, 'APPROVE'), ('REVIEW-B', 3, 'APPROVE')]`; `round_count` -> `1`, so the `Review-Verdict` cross-check agrees and does not catch it either; and `integrate._verdict_gate(root, "wi-401", {"WI-401": "merged"})` -> `None`, i.e. **merge allowed**. The shipped default is `review_rounds = 1` in both `docs/process.toml:176` and `process.toml.template:166`, so the defect is latent here and bites the adopter who dials up to the stronger setting — which is why it is MAJOR rather than BLOCKER. -> Bind the round to the phase its coordinator log declares: rather than adding a phase-equality comparison, have `logged_rounds` carry the LOG's declared phase into the entry tuple and stop reading `ROUND_FILE_RE`'s `phase` group as an input at all — the defect cannot be made unrepresentable by a stricter type here because the round's phase currently has TWO sources, the session-chosen FILENAME and the coordinator-written session log, and deleting the session-chosen one leaves a single owning boundary that is validated once (the `antidote` skill's "smallest change that makes this fix unnecessary"), after which a file's name can no longer claim a phase its session did not serve. Add the case to TC-205, whose Method enumerates the policy-2 independence claim ("the gate clears only once a governing REVIEW-B joins it at the same identity") while `test_policy_two_requires_both_independent_verdicts` only ever drives two DISTINCT ordinals with matching session phases, and `test_an_implementer_authored_file_in_the_review_path_is_not_a_round` only drives a NON-review session phase (`session_phase="BUILD"`) — neither reaches the cross-phase class. -> @owner

- [MAJOR] project-trajectory/scripts/agent_loop.py:2755 -> WI-579 Done-when 3 (WI-559 Done-when 2, "a committing ADJUDICATE session schedules its review round exactly as a committing BUILD does") is UNCOVERED at its scheduling half: `schedule_adjudication_round` and `dispositions_drafted` have no test anywhere — the only occurrence of either name under `tests/` is inside the prose of the `test_module_size_ratchet.py:542` ratchet comment. What TC-205 actually drives is the shared dial reader `agent_common.adjudication_review_owed` and the merge-gate side (`integrate._verdict_owed`); nothing drives the loop arm that calls `on_committed_build` + `schedule_review_round`, so the Done-when's "exactly as a committing BUILD does" is asserted and not demonstrated, and `always` is never driven through a repo fixture at all (`test_an_adjudication_lane_owing_no_round_merges_with_no_verdict_file` parametrizes only `["never", "when-minting"]`). Compounding it, the "ONE reader, so the two cannot disagree" claim holds for the DIAL but not for the `drafts` input it consumes: the loop computes drafts by `rglob` over the working tree in the order `("docs/work", "docs/archive/work")` (agent_loop.py:2755) while the gate reads them by `git show` in the OPPOSITE order `(ARCHIVE_WORK, WORK)` (integrate.py:1189), so a branch momentarily carrying the spec in both homes hands the scheduler and the gate different `## Dispositions` and reproduces the very come-apart WI-559 exists to close. -> Add a scaffold test driving `build_bookkeeping` through the `outcome == "COMMITTED" and phase == "ADJUDICATE"` arm for all three dial values and asserting the queue it leaves, and give the spec lookup a single owning boundary — one helper both callers call, with one precedence order — rather than reconciling two orderings after the fact, since the disagreement is only representable because "where the branch's spec lives" is answered independently in two modules. -> @owner

- [MINOR] docs/requirements/low-level-requirements.toml:2187 -> LLR-207's `detail` asserts "logged_rounds joins branch-scoped round files to coordinator session logs **by train, ordinal and review phase**" — the phase term is false of the shipped code per finding 1, so a living spine cell states a binding stronger than its module implements, and nothing detects a row that over-claims its own mechanism. The cell states the CORRECT rule, so the code is what is wrong. -> Discharged by finding 1's code fix; if that fix is deferred, correct the cell instead so the row stops asserting a join that does not exist. (No guard added, so no unrepresentability clause is owed.) -> @owner

- [MINOR] project-trajectory/scripts/gen_verdict_rollup.py:76 -> `train_dirs` enumerates review scopes by iterating only DIRECTORIES under `docs/reviews/`, so the pre-train FLAT layout — which `kitlib.verdict.round_file` explicitly supports and `test_round_and_session_names_parse_including_the_relaxed_tag` pins (`docs/reviews/003-REVIEW-A-abc1234.md` -> train `""`) — produces no rollup at all, and `--check` reports fresh because it compares against the same empty target set. An adopter on that layout gets a silently empty `docs/reviews/rollup/` and a green freshness step, which is the "reports a state its own remedy cannot clear" shape the module docstring says it exists to avoid, in the opposite direction. Low severity: the rollup is a human artifact the gate never reads. -> Derive the scope set from `round_file`'s own `train` field over every round file found under `docs/reviews/` rather than from directory structure — that deletes the second, independent notion of "what a review scope is" instead of adding a flat-layout case beside it, so the two cannot disagree. -> @owner

## Done-when coverage

DW1 (WI-558 1-5): 1 COVERED but incomplete (finding 1); 2 COVERED — no test
drives a trailer ALONE with no round file, so "never an accept path" is shown
only as "a contradicting trailer refuses"; 3 COVERED for `--check`/`[generated]`
wiring, with `trunk_step.py REGEN_STEPS` membership and "the gate never reads
the rollup" both UNCOVERED by a negative test; 4 COVERED
(`test_the_legacy_rollup_path_warns_while_it_clears` asserts both the `None` and
the stderr WARN); 5 COVERED. DW2 (WI-560 DW1) COVERED across five commit
classes, though "unrepresentable" is shown behaviorally rather than
structurally. DW3 (WI-559 DW2) PARTIAL — banner half covered, scheduling half
UNCOVERED (finding 2). DW4 artifacts all present (`process.toml.template:156`,
`enforcement-audit.md:58`, `RESYNC_PACK.md:4462`) but pinned by no test,
including the closed-vocabulary preflight refusal the audit row claims. DW5 not
re-driven here.

The regression tests for previously-fixed defects that I spot-checked do drive
the real producers rather than lookalikes — notably
`test_the_empty_carrier_commits_its_own_paths_and_never_the_index`, which
obtains the zero-path carrier by calling `agent_common.commit_telemetry` itself.

VERDICT: CHANGES-REQUESTED findings=4
