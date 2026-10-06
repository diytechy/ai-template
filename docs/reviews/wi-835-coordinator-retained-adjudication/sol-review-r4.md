6cf73d95 NOT YET SOUND

| Round-3 finding | Assessment | Evidence |
|---|---|---|
| MAJOR: TC-321 assigns `2` to every pre-launch refusal | **RESOLVED** | [Method and Expected](C:/Projects/ai-template.wt/wi-835/docs/test/test-cases.toml:3248) now bound `2` and state sign-in refusal `7`; [implementation](C:/Projects/ai-template.wt/wi-835/project-trajectory/scripts/coordinator_adjudicate.py:262) agrees. |
| MINOR: TC-321 Expected omits attribution, release and default route | **RESOLVED** | [Expected](C:/Projects/ai-template.wt/wi-835/docs/test/test-cases.toml:3250) includes all three. Its 17 cited tests exist and passed. |
| MINOR: TC-322 Expected omits request fields and lease | **RESOLVED** | [Expected](C:/Projects/ai-template.wt/wi-835/docs/test/test-cases.toml:3261) covers the omitted fields and deadline-derived lease; composition tests passed. |

- **BLOCKER:** none introduced by this lane.

- **MAJOR — Seven trunk-only generated artifacts are committed on the work branch.** [stack.ini:1188](C:/Projects/ai-template.wt/wi-835/docs/stack.ini:1188) declares the generated files; [PROCESS_OPTIONS.md:2192](C:/Projects/ai-template.wt/wi-835/project-trajectory/PROCESS_OPTIONS.md:2192) prohibits committing them on claimed work branches.

  Reproduction: `git diff --name-only aa749a72..6cf73d95 -- PROJECT_STATE.html docs/status.md docs/stage docs/open-items.html docs/requirements/components.derived.toml docs/cli-reference.md docs/interface-reference.md` returns all seven. Ordinary build/spine commits carry them, rather than a station refresh. Restore these seven to claim-base bytes and leave regeneration to trunk. This finding predates the post-round-3 delta.

- **MINOR — The promised coordinator recipe update is absent.** [Done-when:70](C:/Projects/ai-template.wt/wi-835/docs/work/active/wi-835/WI-835-coordinator-retained-adjudication.md:70) requires both skill and recipe instructions. [D-010:74](C:/Projects/ai-template.wt/wi-835/docs/decisions/wi-835.toml:74) explicitly records that the recipe was not edited. The [actual recipe](C:/Projects/ai-template.wt/coordinator-tools/README.md:5) documents composition and review launching but contains no `coordinator_adjudicate` instruction. The skill portion is delivered.

**NOTEs**

The whole-lane Done-when assessment follows. Approved-row decisions were accepted as given.

| Done-when item | Delivery, testing and trace |
|---|---|
| Shared request/keep, record, log and verdict | Delivered through [entry composition](C:/Projects/ai-template.wt/wi-835/project-trajectory/scripts/coordinator_adjudicate.py:247) and [shared planning](C:/Projects/ai-template.wt/wi-835/project-trajectory/scripts/session_service.py:527). TC-321/322 passed; SR-227, LLR-305/306, IF-282..285 trace it. |
| No subagent; skill, recipe and WI-801 amendment | [Skill delivered](C:/Projects/ai-template.wt/wi-835/project-trajectory/skills/session-protocol/SKILL.md:72); all three copies match. [WI-801 amendment delivered](C:/Projects/ai-template.wt/wi-835/docs/work/queued/WI-801-ask-one-entry-point.md:37). Recipe remains incomplete above. |
| Three-state, noncreating, model-free probe | [Delivered](C:/Projects/ai-template.wt/wi-835/project-trajectory/scripts/session_service.py:636); TC-323 passed, tracing SR-227/LLR-305/IF-282. The reusable probe exists for WI-834 part C; that later integration is outside this lane. |
| Both routes refuse missing/unknown, naming setup | [Delivered before keep planning](C:/Projects/ai-template.wt/wi-835/project-trajectory/scripts/session_service.py:457); TC-324 passed with no launch, home creation or fallback. |
| Resume, clear-point retirement, composition and sign-in tests | Delivered and passed; TC-321 again cites both lifecycle tests, with TC-322..324 covering the remaining conditions. |
| Retain first approvals; template unchanged | [Live list updated](C:/Projects/ai-template.wt/wi-835/docs/process.toml:295); shipped list unchanged. Class-switch tests and live first-approval telemetry exercise it. |
| Confirm sign-in, set 55, amend WI-802 together | Confirmation recorded in [D-003](C:/Projects/ai-template.wt/wi-835/docs/decisions/wi-835.toml:23). Dial and WI-802 amendment share `43fbe9eb`; TC-266 tests the live/template split. |
| Terra spine rows and in-lane adjudication | Delivered through SR-227/231, LLR-270/305/306, IF-248/282..285 and TC-266/321..324. Verdicts 003..005 and acts 37..40 record the rulings. |
| Affected tests plus smoke | Requested tests: **267 passed in 45.89s**. Smoke qualification below. |
| Independent cross-family REVIEW-A | Performed over the whole requested range; approval withheld for the MAJOR. |
| RESYNC_PACK with trunk anchor | [Delivered at `aa749a72`](C:/Projects/ai-template.wt/wi-835/project-trajectory/RESYNC_PACK.md:7125); enabled/off-dial behavior passed affected tests. |

- **Post-round-3 delta:** no new evidenced runtime or row/code mismatch. LLR-305/306 tags match their declared modules and symbols. All cited tests exist. The spec reproduces `intake.parse_dispositions(...) == ([], None)`.
- **Snapshots:** every copy made by `dd55ccca`, `ef6de70f` and `13a8453f` matches live bytes at its act. At the tip, all three copied registries equal live files, with LF endings and no BOM/CR bytes. Only SR-227/231, LLR-270/305/306 and TC-266/321..324 moved.
- **Gates:** `check_trajectory --strict` passed. `trace --strict` exited `1` solely for pre-existing [LLR-292’s “minimal”](C:/Projects/ai-template.wt/wi-835/docs/requirements/low-level-requirements.toml:3071); zero orphan/integrity/interface/budget findings. Diff checks passed.
- **Smoke:** **1 failed, 2,261 passed, 2 skipped in 33.99s**. The unchanged [shallow-clone test](C:/Projects/ai-template.wt/wi-835/tests/test_text_then_act.py:314) hit Git `sh.exe` Win32 error 5; the same failure reproduced on trunk `681e3280`. The wall-budget evaluation passed. A fully green smoke run remains unverified in this sandbox.
- The spec remains active without a Deliverable. Closing this ordinary lane changes its governing tree, so the final review must cover that closed tree.
- Tracked lane status remained clean and HEAD remained `6cf73d95`. [Full scratch report](C:/Projects/ai-template.wt/review-tmp/wave17/sol-wi835-r4.md).