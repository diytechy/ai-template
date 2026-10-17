Reviewed: 1ca3674b801f8fde30f8ed2b2cc8c9f045764be9

Model: claude-opus-5-5 (independent reviewer, full-lane round, convergence stance)

Verified. Worst failure class this change admits: fail-open at the plan gate. Deleting the `_cap_problems` branch would let a capped, non-approving critique with an EMPTY blocking set pass whenever the record cites an accepted dispute, because `_dismissals` over an empty set returns `[]`. So I hunted reachability first, through the real functions `_critique_problems` calls before `_cap_problems`. A 584-case product (verdict word x 0-2 findings over BLOCKER/MAJOR/MINOR, mixed-case variants and the non-severities CRITICAL/NIT x declared counts 0-3) went through `kitlib.verdict.filing_refusal` -> `score_reviews.parse_verdict` -> `kitlib.verdict.effective_verdict` -> `plan_gate.blocking_ids`, and no case reached `_cap_problems` with an empty blocking set. The mechanism agrees with the code: `sitting.REVIEW` admits only APPROVE and CHANGES-REQUESTED; `_finding` upper-cases a severity that `FINDING_RE` limits to `SEVERITIES`; a bracketed non-severity is prose, so the declared count mismatches and is refused; a CHANGES-REQUESTED with zero findings is refused; one with all-MINOR findings reads as APPROVE. The branch was unreachable, so the deletion changes no reachable behaviour. No executable red-before test is possible, and the spec says so. The two premise tests (`test_a_critique_outside_the_verdict_format_is_refused_and_nothing_is_written[changes-without-findings]` at tests/test_plan_filing.py:61-73, `test_a_minor_only_change_request_passes` at tests/test_plan_filing.py:137) are kept and pass. Nothing in the repo (tests, skills, docs, LLR/TC cells) cites the deleted hold's message or the dropped "empty dispute set" sentence; `_cap_problems` keeps its `Implements: SR-154, LLR-337` tag, and LLR-337's `code_symbol` still lists it (K3).

SR-154 (K1/K2): only the `requirement` cell changed. Its word multiset is identical before and after; it has one `shall`; status stays Approved. The live row and the `last_approved` snapshot row are byte-equal, under act seq 122 (`reattested = ["SR-154"]`). The amended sentence puts "when unattended work reaches integration" inside the `obtain` predicate, so the coordinated `refuse ...` clause reads under its own "where" condition. No carrier is newly named. LLR-337, TC-367 and IF-295's registry row are untouched; the only registry file in the range is system-requirements.toml. The lane carries two ADJUDICATE records with `.requested` bindings (seen by file name only; the convergence stance bars reading them).

Residue text: I checked each IF-295 residue clause against `staged_lines` / `_squash_lines` / `_unattributed_squash`. A detached HEAD gives an empty `branch`, so `commit_lines` is never called. A hand merge on trunk resolves `gate_rows` for the trunk branch, which has no claim folder. An alias branch containing the tip makes `lanes` non-empty while its own `gate_rows` finds no folder. `git stash`'s internal reset drops SQUASH_MSG. A file copy carries no lane commits. The hook's corrected trunk sentence matches `staged_lines`' squash arm, and it points at IF-295 rather than copying the list. `docs/interface-reference.md` is the regenerated form of the new body: `gen_arch_map --check` exits 0.

Done-when map:
- (1) Branch deleted and docstring states why. Covered by the diff at project-trajectory/scripts/plan_gate.py:379-401, the two premise tests and the probe above.
- (2) Both modules pass in full. 68 passed.
- (3) Text in the tip. Covered by the diff and a clean interface-reference check.
- (4) SR-154 amended, re-attested by act 122, other rows unchanged. Verified above.
- (5) No RESYNC_PACK entry. Confirmed absent.
- (6) Bar: `check_trajectory --strict` clean and `trace.py --strict` exit 0 with no finding. The smoke tier was not run, because the round facts excluded it.

Rubric K4 note, not a finding: the range changes two shipped files (plan_gate.py, hooks/pre-commit) with no RESYNC_PACK entry, which K4 as written asks for. The spec of record's Done-when deliberately exempts it, since the change is comment and dead-code only to kit-owned files a resync overwrites and asks nothing of an adopter. I accept that exemption as sound for this diff.

Commands:
- `git rev-parse HEAD` -> 1ca3674b801f8fde30f8ed2b2cc8c9f045764be9
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-16c-coord/wi-922/gate/opus/wi-922 tests/test_plan_gate.py tests/test_plan_filing.py` -> `68 passed in 123.14s (0:02:03)` (0 environment-gated skips)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (932 work item(s), 808 done (87%), 30 cancelled, graph acyclic).`
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=3.`
- `python project-trajectory/scripts/trace.py --strict` -> exit=0, same summary line
- `python project-trajectory/scripts/gen_arch_map.py --src project-trajectory/scripts --contracts-doc docs/interface-reference.md --check` -> exit=0
- reachability probe (review scratch `probe/probe.py`, real kit functions) -> `cases 584 reaching _cap_problems with empty blocking: 0`
- SR-154 cell comparison (tomllib, base vs tip vs snapshot) -> `changed keys ['requirement']`, `same words True shall 1 status Approved snapshot==live True`

VERDICT: APPROVE findings=0
