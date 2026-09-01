# WI-508 — REVIEW-A (2026-08-30)

**Reviewers:** OPENAI-TERRA (`gpt-5.6-terra`) via the `codex` CLI for eight rounds, OPENAI-SOL (`gpt-5.6-sol`) for one, and OPENCODE-GROK (`opencode-go/grok-4.6`) via `opencode run --dir <lane>` for the governing round — every round cross-family to the Anthropic builder, fresh context each time, independent of the lane. Charter: the kit's reviewer brief (`project-trajectory/prompts/reviewer.template.md`). Given the branch diff (`contract_split...wi508-architectural-remap` from the lane's first refresh `7e2d3f82`) and the requirement surface: the WI-508 row (`docs/archive/work/complete/WI-508-architectural-remap-program.md`), `OI-58`, the amended `SR-163` and its four minted children. The spec's `## Deliverable` prose was supplied only as claims-to-verify.

**This file is a COMPILATION, not a judgement.** The merge slot's verdict rung (`integrate._verdict_gate`, RULING-7) reads this WI-level file, while the loop's reviewers write per-round files under `docs/reviews/wi508-architectural-remap/`; nothing in the kit bridges the two, so — as every coordinator sitting before this one did — the supervising session of the delegated unattended run transcribes the rounds here. Every finding line and every machine line below is quoted verbatim from its round file; the dispositions the lane took between rounds are in the lane's `docs/log.d/2026-08-30-wi508-*` fragments and in `docs/decisions-for-review-2026-08-31.md` (decisions 7–14). Why a compilation is needed at all is decision 7 there.

**Final verdict: APPROVE at `b8d57e9f` (round 10 of 10, `010-REVIEW-A-b8d57e9.md`, commit `899352b7`).** Rounds 1–9 CHANGES-REQUESTED. The machine line that governs is the last one in this file.

---

## Round 1 — at f179a0b (OPENAI-TERRA, `gpt-5.6-terra`; loop-drawn, after the close commit f179a0b4)

Round file: `docs/reviews/wi508-architectural-remap/003-REVIEW-A-f179a0b.md`.

- [MAJOR] docs/test/test-cases.toml:2022 -> TC-199 is now Approved as evidence for SR-163, but LLR-203 records that no file-to-requirement join exists and that the test walks only declared destinations; this falsely marks the full every-shipped-file mapping obligation as covered -> keep this partial evidence Drafted or add and approve a TC that drives the complete SR-163 join and shipped-file universe -> @owner
- [MAJOR] docs/test/test-cases.toml:2033 -> TC-200 is now Approved as evidence for SR-163, but LLR-204 records that its grammar checks the inverse direction and excludes templates, registry seeds, launchers, workflows, and process documents; this falsely marks the remaining core SR-163 coverage as verified -> keep this partial evidence Drafted or add and approve a TC that drives SR-163's required direction and complete universe -> @owner
- [MAJOR] docs/log.d/2026-08-30-wi508-slice6-spine-approval-and-close.md:6 -> the newly added OI-64/OI-65 link has no target, so the repository's stage-selected `check.py` fails `doc-navigability` -> replace it with the extant durable record or remove the dead link, then rerun the harness -> @owner

`VERDICT: CHANGES-REQUESTED findings=3`


## Round 2 — at 82fb76a (OPENAI-TERRA, `gpt-5.6-terra`; loop-drawn, after the round-1 rework 82fb76a9)

Round file: `docs/reviews/wi508-architectural-remap/005-REVIEW-A-82fb76a.md`.

- [MAJOR] docs/archive/work/complete/WI-508-architectural-remap-program.md:29 -> The record says SR-163's still-unverified file-to-requirement join and shipped-universe obligation is carried by the filed consolidation WIs, but WI-519, WI-520, and WI-521 have empty SR-Refs and no SR-163/LLR-203/LLR-204 scope, silently turning an unowned gap into owned work -> replace that claim with an honest unscheduled state, or file and cite one active WI whose scope covers SR-163's full acceptance criteria -> @owner
- [MINOR] docs/archive/work/complete/WI-508-architectural-remap-program.md:27 -> for clarity, saying TC-199/TC-200 "verify only their LLRs" conflicts with each formal Verifies list, which still directly includes SR-163, so the record does not distinguish a pending trace link from an uncorrected overclaim -> state that their tests exercise only the delivered LLR arms while their direct SR-163 links remain Drafted, non-evidence -> @owner

`VERDICT: CHANGES-REQUESTED findings=2`


## Round 3 — at 085de8d (OPENAI-TERRA, `gpt-5.6-terra`; supervisor-drawn, after the Sol design-check rework and the brief regen 085de8de)

Round file: `docs/reviews/wi508-architectural-remap/010-REVIEW-A-085de8d.md`.

- [BLOCKER] docs/ratify/CURRENT.md:51 -> TC-199 and TC-200 are rendered “Drafted, never approved” although `580df781` approved and snapshotted them; `4824c0ba` then rewrote that historical snapshot during a rollback, contrary to PROCESS.md §4's approval-only, wholesale snapshot rule, so this regeneration ships a false attestation record -> restore the actual approval snapshot, preserve the demotion as an auditable state, and regenerate the brief so it reports the prior approval instead of laundering it -> @owner

`VERDICT: CHANGES-REQUESTED findings=1`


## Round 4 — at 5175065 (OPENAI-SOL, `gpt-5.6-sol`; supervisor-drawn on the strong route, after the round-010 record 51750651)

Round file: `docs/reviews/wi508-architectural-remap/010-REVIEW-A-5175065.md`.

- [BLOCKER] docs/plans/2026-08-25-blind-minimal-map-brief.md:3 -> The core anti-post-hoc condition is UNCOVERED: git shows the supposedly pre-run brief and both agent returns first appearing together in 64e9bf2a, so there is no immutable evidence that the question was fixed before the answers existed -> rerun the exercise with the brief committed (or otherwise immutably timestamped) before either derivation starts, and commit the returns only afterward -> @owner
- [BLOCKER] docs/plans/2026-08-25-blind-minimal-map-derivation.md:29 -> Both purportedly independent blind teams received this repository's instruction context (and Team B a memory index), violating the brief's closed five-file input set and weakening convergence with shared live-layout knowledge -> rerun both derivations from sterile contexts/cwds containing only the five declared inputs, then redo the alignment from those uncontaminated returns -> @owner
- [MINOR] docs/plans/2026-08-25-blind-minimal-map-derivation.md:62 -> The reported Team A census is wrong: the return defines 25 modules (24 owning SRs plus zero-SR F5), not 24, so the 3.1 mean and “22 of A's 24” summary—and the archived Deliverable's 24-module claim—are internally inconsistent -> derive the module total from the definitions including zero-owner modules and correct every dependent figure/claim -> @owner
- [BLOCKER] docs/archive/last_approved/docs/test/test-cases.toml:2022 -> The 4824c0ba rework changed the last-approved copy of TC-199/TC-200 from Approved to Drafted even though PROCESS.md defines this directory as the byte-for-byte record of the last approval, written only by that approval act; this erases 580df781's recorded approval and lets CURRENT.md falsely say the rows were “never approved” -> reconstruct the branch so the corrective de-approval changes only the live rows while the 580df781 approval snapshot remains intact, then regenerate the re-attestation brief from that truthful baseline -> @owner
- [MAJOR] docs/test/test-cases.toml:2015 -> TC-199 formally verifies SR-163 although its Method/Evidence only exercise inventory/materialization arms (including tests already used by SR-166/TC-176), while approved LLR-203 explicitly says the purpose join and full shipped universe are not discharged -> remove the direct SR-163 verification/parent-satisfaction claim until a TC drives the complete file-to-requirement-to-need join and all SR-163 finding classes; keep partial mechanism evidence scoped to LLR-203 -> @owner
- [MAJOR] docs/test/test-cases.toml:2026 -> TC-200 formally verifies SR-163 although it tests the opposite-direction design-row backlink scan over source roots only, and approved LLR-204 explicitly says both direction and universe remain undischarged; approving the pending brief would recreate the false SR verification -> remove the direct SR-163 verification/parent-satisfaction claim until a TC drives the inverse all-shipped-file universe required by SR-163; keep grammar/policy evidence scoped to LLR-204 -> @owner
- [MAJOR] docs/stage:40 -> The shipped composed path is red: `check.py --trunk-lane` reports cached drafts=6 versus actual drafts=4, `gen_trajectory.py --check` reports PROJECT_STATE.html stale, and `gen_trajectory.py --status --check` reports the status snapshot stale -> regenerate docs/stage first, then PROJECT_STATE.html and the generated status block, and rerun the trunk-lane harness to green -> @owner
- [MAJOR] docs/status.md:256 -> Hand-authored status still says the archived WI-508 lane is OPEN and that LLR/TC blessing is the owner's act, contradicting both the completed spec and `docs/process.toml`'s current `human_approval_through = "DevStg-Needs"` policy that releases SR/LLR/TC approval to ordinary review -> remove the closed-lane recap from the forward-only surface and point approval authority to the declared policy instead of paraphrasing a stale value -> @owner

`VERDICT: CHANGES-REQUESTED findings=8`


## Round 5 — at 5835bf4 (OPENAI-TERRA, `gpt-5.6-terra`; supervisor-drawn, after the round-011 record 5835bf42)

Round file: `docs/reviews/wi508-architectural-remap/010-REVIEW-A-5835bf4.md`.

- [MAJOR] docs/status.md:256 -> the hand-authored status says WI-508 is OPEN, reports four Drafted rows, and calls their blessing "the owner's act", although the archived WI-508 spec closes the lane with only TC-199/TC-200 Drafted and docs/process.toml:116 holds only DevStg-Needs; the submitted fragment knowingly defers that misinformation -> update the hand-authored status in the integration refresh to remove the closed-lane prose and state the current loop-held approval policy -> @owner
- [MAJOR] docs/log.d/2026-08-30-wi508-review-011-dispositions.md:71 -> this new commit explicitly records that pytest was not re-run for a record-only commit, despite the mandatory per-commit bar; independently, the full harness ends `RESULT: FAIL` because docs/stage caches drafts=6 while the live registries have 4 -> run and record the mandatory commit-bar results, then complete the required refresh before sending this record for integration -> @owner

`VERDICT: CHANGES-REQUESTED findings=2`


## Round 6 — at c225c34 (OPENAI-TERRA, `gpt-5.6-terra`; supervisor-drawn, after the station refresh c225c34d)

Round file: `docs/reviews/wi508-architectural-remap/010-REVIEW-A-c225c34.md`.

- [MAJOR] docs/test/test-cases.toml:2015 -> TC-199 (and TC-200 at :2026) formally verifies SR-163 even though both TC methods and their LLRs explicitly leave SR-163's required file-to-requirement join and shipped-file universe unimplemented; trace.py consequently reports SR-163 as covered now, and a future approval of these already-passing draft TCs can silently advance a false mapping claim -> remove the direct SR-163 targets until a complete mapping TC/check exists (or add that complete coverage before approving either TC) -> @owner

`VERDICT: CHANGES-REQUESTED findings=1`


## Round 7 — at 747c396 (OPENAI-TERRA, `gpt-5.6-terra`; supervisor-drawn, after the verifies rework 747c3963)

Round file: `docs/reviews/wi508-architectural-remap/010-REVIEW-A-747c396.md`.

- [MINOR] docs/test/test-cases.toml:2019 -> for clarity: TC-199's Expected (mirrored by TC-200 at :2030) still foregrounds parent SR-163 although these TCs now verify only LLR-203/LLR-204 and their LLR Details explicitly leave SR-163's complete join and shipped-file universe undischarged -> state in both Expected cells that they cover only their LLR arm, not SR-163 -> @owner

`VERDICT: CHANGES-REQUESTED findings=1`


## Round 8 — at c028eb0 (OPENAI-TERRA, `gpt-5.6-terra`; supervisor-drawn, after the Expected rework c028eb02)

Round file: `docs/reviews/wi508-architectural-remap/010-REVIEW-A-c028eb0.md`.

- [MAJOR] docs/test/test-cases.toml:2019 -> TC-199's new LLR-203-only coverage claim still cites `test_the_common_package_ships_complete` and `test_every_sibling_imported_module_is_shipped_by_mapping`, which TC-176 already assigns to LLR-181/SR-166; SR-166 expressly owns fresh-scaffold manifest arrival and its rationale also names `test_scaffold_mapping_covered_or_declared`. This double attribution collapses SR-163's purpose-coverage scope into SR-166's materialization checks and leaves the new Expected false as a coverage statement -> split or reassign TC-199 so it retains only SR-163's source-absence/unmapped-file evidence, and record the manifest-materialization/dogfood checks only through LLR-181/TC-176 (or distinct LLR arms with accurate SR references) -> @owner

`VERDICT: CHANGES-REQUESTED findings=1`


## Round 9 — at 31a1d6b (OPENAI-TERRA, `gpt-5.6-terra`; supervisor-drawn, after the TC-199 evidence trim 31a1d6ba)

Round file: `docs/reviews/wi508-architectural-remap/010-REVIEW-A-31a1d6b.md`.

- [MAJOR] docs/test/test-cases.toml:2017 -> TC-199 now says its package-completeness and sibling-import checks are TC-176 evidence for LLR-181/SR-166, yet LLR-203's only Test-Refs still names TC-199 while its Detail names those same package-direction checks as its delivered MISSING FILES arm. The arm is therefore unclaimed by its stated LLR or reattributed to SR-166, whose rationale expressly excludes a shipped file absent from the manifest. A real scaffold with scripts/kitlib/config.py removed made its shipped check.py fail with ModuleNotFoundError while all three TC-199 dogfood nodes passed. -> Reconcile the LLR/TC boundaries: either make LLR-203/TC-199 dogfood-only and remove its package arm, or give the package-presence arm a trace that does not assert it is SR-166 materialization evidence; do not retain both claims. -> @owner
- [MINOR] docs/test/test-cases.toml:2017 -> for clarity: the Method opens with “two delivered finding classes,” but its sole Evidence cell now has only the dogfood class and the next sentence expressly disclaims the package class. -> Name only the dogfood class in the opening claim, or identify how the second is verified. -> @owner

`VERDICT: CHANGES-REQUESTED findings=2`


## Round 10 — at b8d57e9 (OPENCODE-GROK, `opencode-go/grok-4.6`; supervisor-drawn on the third family (OpenAI at its usage limit), after the round-016 rework b8d57e9f)

Round file: `docs/reviews/wi508-architectural-remap/010-REVIEW-A-b8d57e9.md`.

_(no findings)_

`VERDICT: APPROVE findings=0`

---

Governing machine line (round 10, quoted from `010-REVIEW-A-b8d57e9.md`; the reviewer ran the cited test nodes, `trace.py`, a scaffold drive of the package-direction arm, `check.py --jobs 0`, the smoke tier, the budget and `check_docs --stale` before writing it):

VERDICT: APPROVE findings=0
