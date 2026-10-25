Reviewed: 3cf85aa73d8e82d6bfdffed785a969556d1cf24f

### REVIEW-B (Opus) — WI-878 full-lane review — convergence stance — 2026-10-25

**Verified.** I hunted these failure classes first, worst first. (1) Fail-open: a cited DISMISS or SUCCESSOR resolving a finding it did not rule, either through a wrong or spoofed record or through a sibling scan that survived. (2) Silent loss of the record on the outcome rewrite, which would turn every new dispute into a refusal. (3) Fail-open on the HEAD route (`pass_fields`). None of the three reproduced.

How I tested each part:

- **Gate, old vs new.** I loaded the shipped `plan_coverage.ruling_problem` in process, from both the pre-fix (a7c89a5) and post-fix sources, and ran it over constructed lanes.
  - Two rounds reusing F2: each round's own citation is refused by the old code ("whose finding F2 is not this review's F2") and resolves (None) in the new code.
  - Round 1's verdict cited for round 2's F2: refused by both.
  - A binding with no record and a matching sibling file: resolves in the old code and is refused by name in the new code ("whose binding records no findings file").
  - So the Done-when tests T1/T2/T3 fail on the pre-fix behaviour.
  - A sitting-id alias (`#A`) and a CRLF binding both read correctly.
- **Brief line.** `requested_file` reads the FIRST `FINDINGS-FILE:` line. In the shipped template `{request}` comes before `{commits}` and `{findings}`, so a `FINDINGS-FILE:` line inside a finding's text cannot take over the record.
- **Recorded file that is a directory.** At a commit, `git show` of a directory prints a tree listing. `read_findings` refuses that listing, so the gate fails closed.
- **Record survives the rewrite.** `record_outcome` reads the binding before rewriting it and carries `findings_file` through `write_binding`. The entry-point test confirms this for both the accepted and the failed outcome, end to end through the real `compose` → `cli.main`.
- **Consolidation.** I found no duplicated function: `_cells` is now the one cell reader shared by `read_requested` and `read_findings_file`, `requested_file` reuses `_keyword_rests`, and `_ruled_texts`/`_tree_tomls` are deleted along with their `code_symbol` entries.
- **K3 back-links.** `file_line`/`requested_file` → LLR-314, `read_findings_file` → LLR-310, `_correspondence_problem` → LLR-069 and `dispute_values` → LLR-315. Each LLR names the module, and each function is in that LLR's `code_symbol`.
- **K1/K2.** The amended LLR-069/310/314/315 detail cells and the TC-069/327/334 method/expected cells match the code. No SN or SR cell is amended, and none names a carrier.
- **Done-when coverage.**
  - (1) Binding records the file and the gate reads only that file: covered by `test_a_dispute_binding_records_its_findings_file_through_the_outcome`, `test_the_entry_points_dispute_binding_resolves_only_its_own_rounds_finding` and `test_the_dispute_brief_names_the_findings_file_it_was_composed_over`.
  - (2) A binding with no record refuses and no sibling is read: covered by `test_a_binding_without_the_findings_record_refuses_and_reads_no_sibling` and `test_at_the_cap_a_dismissal_bound_without_its_findings_file_is_refused`.
  - (3) Red-first tests: covered by `test_two_dispute_rounds_reusing_ids_each_resolve_their_own_finding`, `test_round_ones_verdict_cited_for_round_twos_same_id_finding_refuses` and the parametrized missing/directory/not-TOML/no-such-id refusals. The existing cases pass in the run below.
  - (4) Rows amended: done in this diff. The combined sitting's own record lies under `docs/decisions`/`docs/reviews`, which this stance does not read, so I could not verify it here.
  - (5) RESYNC entry: present, anchored `[since a7c89a5da]`. It names the downstream migration: pre-change disputes now refuse.

**Requirement/interface decisions.**

- IF-287 (binding grammar: data and notes changed) ↔ LLR-310. The counterpart carries the matching change (record written by the one writer, kept through the rewrite, an absent record reads as none). Requestors are unchanged and correct: `plan_coverage` already consumed IF-287.
- IF-290 (dispute grammar: `file_line`, `requested_file` added) ↔ LLR-314 and LLR-315. Both carry the change: LLR-314 has the line grammar, LLR-315 has the request value carrying the line. Requestors are unchanged and correct: `adjudicate_brief` is the caller.
- LLR-069 ↔ SR-236. SR-236 is kept unchanged on purpose. Its acceptance ("a finding that cannot be shown ... is refused") already states the capability. The new record is a mechanism below it, so the SR does not become untrue.
- SR-232 and SR-234 are kept unchanged. Neither names the binding's cells or the brief's lines, and their sitting/verdict-grammar capability is unchanged.
- No decomposition was added.

**Commands.**

- `git rev-parse HEAD` → `3cf85aa73d8e82d6bfdffed785a969556d1cf24f`
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../gate/b/wi-878 tests/test_plan_coverage.py tests/test_plan_filing.py tests/test_dispute.py tests/test_coordinator_adjudicate.py tests/test_done_when_blessing.py tests/test_adjudicate_brief.py tests/test_adjudicate_act.py tests/test_held_status.py tests/test_integrate_admission.py tests/test_prompts.py tests/test_skills_sync.py tests/test_resync_pack.py tests/test_check_resync.py` → `631 passed in 765.98s (0:12:45)` (0 environment-gated skips; posix-shell gate reported unsatisfied)
- `python project-trajectory/scripts/check_trajectory.py --strict` → `check_trajectory: clean (971 work item(s), 860 done (89%), 34 cancelled, graph acyclic).` (WARN lines only, none from this range's code)
- `python .../gate/b/probe.py .../gate/b/probe-run`: an in-process old-vs-new `ruling_problem` over constructed lanes, results as stated above.

Findings:
- [MINOR] docs/test/test-cases.toml:747 -> K3: Approved TC-069's `tier` is changed from "Smoke" to "Full", which the spec does not grant. The Done-when's row list asks for TC-069's method/expected/evidence to change, not its tier, and no evidence move forces it. TC-069's evidence still includes `tests/test_plan_coverage.py`, which is not in `SLOW_MODULES`, so `kitlib.spine.tier_findings` accepts "Smoke" as before. The new `tests/test_plan_filing.py` evidence (slow) only adds a full-tier item. The retier makes the approved cell understate where its evidence runs, and it silently drops the per-commit evidence-join check that would have caught `test_plan_coverage` later moving to slow. -> restore `tier = "Smoke"` on TC-069, keeping the amended method/expected/evidence -> @owner

VERDICT: APPROVE findings=1
