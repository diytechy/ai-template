Reviewed: f1c7693037ce4153ddea33b0ca003d3ee7444803

# WI-993 full-lane review (independent reviewer B, convergence stance)

Failure classes hunted first, in severity order: a planned owner-held step whose claim a kit route drops (silent loss of the rule this row states); a mint that writes an item for text no sitting saw, or hides a held row from every surface (fail-open); a published command the real act refuses (wrong content); a replay that mints twice.

**Verified.**

The mint arm holds. I drove the real code paths, and every state in the Trust table behaves as ruled.

- 274 tests pass, and `check_trajectory --strict` is clean.
- Twelve mutants, run on an exported copy outside the lane, were all killed by the lane's tests: any-MEANING in place of the latest ruling; reading the verdict text without `accepted_at`; no `text_as_bound`; no dial; `carried` unfiltered; the old `--verdict` in the command; one draft across registries; a gone row not kept; no copy comparison; a swallowed copy failure; citers queued only; citers any open row. The `--verdict` mutant restores the pre-fix command found in the lane's patch history, and five tests fail on it.
- Driving `_held_act_drafts` over the lane's own range with its real bindings: as dialled it mints nothing, so this landing files no owner row. With the dial forced held it yields two drafts, one per registry, with all seven rows at their bound text. The real binding digests therefore match `approved_text_digest`.
- Further probes:
  - DA and SUR rows mint one item whose command exits 0.
  - 44 rows mint a 431-character title, and the slug stays short.
  - The minted fixture passes the real `check_trajectory --strict` CLI.
  - The card shows `<record>` escaped.
  - A carried row stays on the page's approval section as drift, so SR-178 still reports it.
  - A routed traced cell moved after the sitting still mints, because the binding's digest covers approved cells only. That row goes to the owner, the stronger authority, so this is not fail-open.
- `PROCESS.md` and `PROCESS_OPTIONS.md` byte stamps match the files. The three skill copies are byte-identical. The RESYNC file list matches the diff.

Done-when map:

| Done-when item | Coverage |
| --- | --- |
| §5 definition and pointers | Corrected text at `project-trajectory/PROCESS.md:927`, the skill's step 3 and the template headers; a grep finds no live narrower site outside dated handoffs and ruled items |
| Keeps its claim (call 1) | Text sites amended, but see the MAJOR below |
| OI-126 | `project-trajectory/PROCESS.md:942` to `project-trajectory/PROCESS.md:946`, the skills |
| Sitting verdict writes the item | `tests/test_intake_held_act.py` (TC-147) |
| Claimed citers | `tests/test_open_item_queue.py`, `tests/test_open_item_readiness.py` (TC-123, TC-314) |
| Routine push and closing an item (calls 3, 4) | §5 text |
| No detector (call 7) | None added; confirmed in the diff |
| RESYNC | One entry |
| Review bar | This round |

Requirement and interface relationships, by changed side and counterpart, with my decision on each:

- IF-073 v2 with LLR-299, LLR-118, TC-314 and SR-148: carried. SR-148 words no queued-only citer, so it is retained.
- IF-074 `data` with LLR-118 and TC-123: carried. It is a wording widening, so its version is retained.
- IF-054: retained. "A queued placeholder cites a pending OI" stays true, and a claimed citer is not a placeholder.
- IF-091 with LLR-153, LLR-364 and TC-147: carried; the module contract matches.
- IF-224 requestor with TC-147: carried.
- LLR-153 and LLR-364 with SR-174, SR-228 and SR-178: parent text retained. SR-228 already leaves a MEANING change the owner's, and SR-178 still reports the drift.
- LLR-288: retained, and it is true for a claimed row (`schedule._disposition` read `blocked` in my drive).

No row was split, so no decomposition judgement is owed. No workaround preserves an unsuitable LLR: LLR-153 and LLR-364 are amended rather than worked around.

K2 holds: no SN or SR cell changed. K3 holds: each new function's `Implements:` tag names LLR-153, whose `module` and `code_symbol` now carry it, and no status flipped.

Stance disclosure. My first command printed the lane's recent commit subjects, before I had read the stance paragraph. Driving the arm printed the row rulings of `docs/reviews/wi-993/007` and `008`, and I read one binding's cells. I read no verdict's findings or prose, and no finding below rests on any of it.

**Commands.**

- `git rev-parse HEAD`: `f1c7693037ce4153ddea33b0ca003d3ee7444803`
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp ... ` (the eight listed files): `274 passed in 321.48s (0:05:21)`
- `python project-trajectory/scripts/check_trajectory.py --strict`: `check_trajectory: clean (998 work item(s), 886 done (89%), 34 cancelled, graph acyclic).`, exit 0
- Mutation run of `tests/test_intake_held_act.py`, `tests/test_open_item_queue.py` and `tests/test_open_item_readiness.py` on an exported copy: 12 of 12 killed
- Probe over `dispatch.run`, the lane's own `tests/test_dispatch.py` fixtures, on a claimed row citing a pending item, the state §5 sanctions:
  - `blocked ['blocked:open-item-pending:OI-1']`, and `_parked_branches` returns `['wi-402']`
  - `worker_prompt`: `BLOCKED WI-402: OI-1 ... no worker assignment.`
  - Recorded worker exit 3, 4 or 7: `dispatch: cycle 1 - resuming parked branch wi-402`, then `handback: closed WI-402 as partial from wi-402`
  - After that close: `OI-1: pending, but no queued or claimed work item cites it`
  - Recorded worker exit 0, with WI-401 ready beside the lane: `STALL - 2 consecutive cycle(s) left the trunk unmoved`, rc 4, and WI-401 never claimed
- Real `agent_loop.py --wi WI-402` with a stub agent on the same lane: `WORKER EXIT 4`. My stub's sessions logged as ERROR rather than NO-COMMIT, so this shows the stall guard's count, not a model's reaction to the prompt.

**Findings.**

- [MAJOR] project-trajectory/scripts/dispatch.py:1183 -> K1: the kit's own unattended route drops the claim this row says a lane keeps. `agent-resume` reaches `dispatch.run`, whose parked arm reads no schedule, so a lane at a planned owner-held step is relaunched on the first tick, against the row's Trust sentence "a claimed one draws no worker assignment" (docs/work/active/wi-993/WI-993-owner-held-step-is-an-oi.md:130) and against "Nothing reads an item to keep, drop or release a claim: that is the coordinator's rule" (project-trajectory/PROCESS.md:946), since on this route the dispatcher is the coordinator. The worker's prompt is the bare BLOCKED line, its no-commit sessions end in exit 4 (in `_WORKER_OUTCOMES`), and the dispatcher then closes the lane partial, which leaves the item uncited: the checker's error on trunk. A worker that exits 0 instead stalls the run at rc 4 with a ready row unclaimed, so the skill's "moves to the next row" fails too -> have `_parked_branches` leave out a lane whose row reads `blocked` in `schedule.evaluate`, with the run going on to the frontier and ending without a stall, and add a `tests/test_dispatch.py` case over such a lane asserting no launch, the claim kept and the next row claimed; if the owner rules that out under call 7, §5 and the Trust section must instead state that an unattended run closes such a lane, and the row's sentence goes. The state cannot be made unrepresentable: a claimed row citing a pending item is the state the ruling creates, so the one owning boundary is this resume admission, which reads the existing `blocked` disposition and adds no second predicate -> @owner convergence-class: yes
- [MINOR] docs/requirements/low-level-requirements.toml:1540 -> K1, for clarity: LLR-153 labels the new trigger "(d)", while its module labels it "(f)" (project-trajectory/scripts/intake.py:65) and uses "(d)" for drafts-not-mints, so one label names two triggers across the LLR and its code -> drop the letter in the cell, or use the module's "(f)" -> @owner

VERDICT: CHANGES-REQUESTED findings=2
