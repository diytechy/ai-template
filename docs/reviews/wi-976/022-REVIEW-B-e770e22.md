Reviewed: e770e22dc76866eaffc1b12d3bf6c8fd50823ce8

### Reviewer B (Opus, independent) — WI-976 full-lane review — convergence stance — 2026-10-26

**Verified.** `git rev-parse HEAD` printed the reviewed commit, and the worktree was clean before and after the run.

I checked the Done-when items against the diff and the commands below, and these hold:
- **Order.** The ruling fragment `docs/log.d/2026-10-25-wi976-sn036-ruling.md` lands at lane commit 8 (`159d2f5f4`). The first registry-row change is commit 11 (`97c695e63`), so the fragment comes first.
- **SN-036.** Its `acceptance` is the verbatim `contract_split` text, with `need` and `why` unchanged.
- **SR-161.** Its title, requirement, acceptance, Inspection verification, dated rationale and `coincident` cell match the proposed text. No SN or SR cell names a carrier (K2).
- **LLR-183.** Its opening and closing clauses match. TC-178's `expected` is split as asked.
- **TC-211.** It verifies SR-161 and SR-186, and its `inputs` name the 016 brief and verdict, both present on disk. No input names a sidecar.
- **Retirements.** LLR-297 and TC-312 are deleted, with `docs/log.d/retired/` records, and they appear in act 160.
- **New rows.** LLR-360 and TC-399 are added and approved in act 161. IF-133's `data` cell no longer lists `load`.
- **Rubric and procedure.** The rubric's R1/B1 and the inspection procedure are amended, the "missing perspective outcome" abnormal input is added, and the 2026-09-06 INCOMPLETE result is kept as history.
- **The record command.** `hats.py record` and `tests/test_hats_record.py` are gone, with no leftover imports (`datetime`, `write_atomic`, `toml_fields`, `toml_string`). The DECOMPOSITION-AMENDMENTS sidecar and its pointer paragraph are gone.
- **Instructions.** PROCESS.md §1, spine-questions (c3), both roster headers and all three recipe copies now state the review-record rule. The three skill copies are byte-identical.
- **Live-surface sweep.** A grep of every live surface the Done-when lists finds the sidecar or the `record` command nowhere. The only hits are "perspective record" meaning `Hat-Refs` (left unchanged on purpose) and the superseded RESYNC entry.
- **SAFETY.** It leaves the live roster ("Fifteen hats"); the template keeps it, and the test name pins are split.
- **RESYNC entry.** It covers the `record` removal, inert `.perspectives.toml` files, the optional `{hats}` slot with the override path, and the stale preserved roster header.
- **Byte budget.** The `byte-budget-guard` stamp of 97,962 matches PROCESS.md's actual size (98,185 at base).
- **Catalogue and CLI reference.** CATALOG.md and cli-reference.md are regenerated. `components.derived.toml` is stale at the tip (`gen_components.py --check` says STALE; it still lists LLR-297). That follows the landing recipe's restore-the-trunk-only-views rule, so it is not a finding.
- **K3.** Every new `Implements:` tag names an LLR whose `module` holds the file and whose `code_symbol` holds the function (LLR-360, LLR-167, LLR-271, LLR-273).

I drove the shipped paths, not just the source:
- The tests compose real first-approval, amendment and combined briefs. My probes ran `adjudicate_brief.compose` and `plan_briefs.round_questions` on fixture repos and on this repo's own roster.
- Hat outcome lines parse to identical rulings.
- An override without `{hats}` composes byte-identically, even over a malformed roster.

I confirmed each fix in the lane against the code before it, using test files from the fix commits:
- Applying `183da2b79`/`5d0c7d020`'s tests to `b33410766` code fails 7 tests, for the right reasons: need-b's question is missing, `count==0`, and mkprompt leaked the work item's own SR-Refs need.
- Applying `e8d7d308e`'s tests to `dd2c9eeea` code fails 6 tests, for the right reasons: the removed TC and DA rows are dropped, and an unknown token is not named.

Owner-held, not a builder defect: SN-036's re-attestation act has not been taken. `last_approved/stakeholder-needs.toml` still holds the old acceptance. By the spec's own Done-when, the lane must not land until the owner acts.

Coverage-extension note (fails closed, so no severity): `plan_briefs._roster_refusal` (plan_briefs.py:516) wraps every `HatsError` as "cannot be composed from docs/requirements/hats.toml". That includes errors that are not about the roster: an unknown SN named by a judged SR's SN-Refs, or an absent needs carrier. The refusal holds, but it names the wrong file.

**Commands.**
- `pytest -q -p no:cacheprovider -n 2 --basetemp .../revb/wi-976` over the 15 declared modules: `793 passed, 3 skipped in 1180.57s (0:19:40)`. The skips are environment-gated (posix-shell).
- `check_trajectory.py --strict`: `check_trajectory: clean (976 work item(s), 865 done (89%), 34 cancelled, graph acyclic).`
- `trace.py --strict-integrity`: `Traceability: SN=31 SR=138 LLR=326 TC=353 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=2.` Exit 0, and no tracked file changed.
- `gen_components.py --check`: `components.derived.toml STALE`. This is the trunk-only view restored to base, as the landing recipe says.
- Pre-fix replays, from `git archive` exports in the scratch directory:
  - `183da2b79` tests on `b33410766`: `7 failed`.
  - `e8d7d308e` tests on `dd2c9eeea`: `6 failed`.
- Probes `probe/p1.py` and `probe/p2.py` (results quoted in the first finding).

Findings:
- [MAJOR] project-trajectory/scripts/plan_briefs.py:435 -> The round's hats are widened by the tags of whichever row `compose` is handed. On the kit's unattended route that row is the merge-minted adjudication row (`agent_loop.py:406`). Its Workstream is always `process` and its SafetyClass `adjudication` (`intake.py:933`). So the authoring work item's tags are lost, which contradicts LLR-360's "widens each need by the authoring work item's declared tags" and the Done-when's "widened by the work item's tags" (K1). Driven through `adjudicate_brief.compose` with a hat on `tags contains "scripts"`:
  - the authoring lane's row (Workstream `scripts`) asks it: `scripts hat asked: True`;
  - the same first-approval as a merge-minted row omits it: `scripts hat asked: False`.

  On this repo's own roster that silently drops CROSS-PLATFORM (and UNATTENDED-OPS for `unattended`/`loop` work) and adds FIRST-RUN-ADOPTER. For an adopter it drops the template's SAFETY hat whenever SafetyClass carries `safety`. Only the in-lane `compose_lane.py` route, which passes the lane's own row, is covered by tests. -> Concrete change: the first-approval and amendment mints (`intake._first_approval_drafts` and the amendment drafts) carry the merged work item's id or its tag cells onto the minted row, and `round_questions` widens by the authoring work item's tags. Alternatively, LLR-360 is amended to say "the composing row's tags", with the trunk consequence stated. Add a test that composes a merge-minted row. This passes data along rather than adding a guard -> @builder convergence-class: yes
- [MINOR] docs/test/inspection-procedures.md:67 -> The lane lands TC-211 red on its own sample: the 2026-10-26 observation reads `outcome = "fail"`, on R2 / SR-186's stopping reason. The red reading replaces the 2026-10-03 PASS, and the lane files no follow-up row. The re-judge also ran before SN-036's owner act, although deliverable 6 orders "TC-211's re-judge after the acts". If the owner returns SN-036's text, the judged sample goes stale. Because `red_tc_census` keys on Status, which stays `Approved`, the merge will not mint a red-TC row for it. -> Concrete change: after the owner's SN-036 act, either re-sit sitting 016's stopping reason and re-judge, or file the follow-up row the FAIL owes (citing TC-211 and SR-186) before landing. The kit-change-review rubric has no anchor for this -> @coordinator
- [MINOR] project-trajectory/scripts/adjudicate_brief.py:652 -> The split moved helpers shared by every brief into the arm-named `amendment_brief.py`: `adjudicates`, `tier_questions`, `_REGISTRY_OF`, `_loop_approves`, `_copy_stamp_lines`, `TC_REGISTRY` and `JUDGED_TEXT`. The composer and the first-approval arm now reach across modules into that module's private names (`amendment_brief._loop_approves`, `._REGISTRY_OF` at :678/:912/:927, `._copy_stamp_lines` at :896). Every other arm (red-tc, consolidate, combined, done-when) reads its scope through `amendment_brief.adjudicates`. The module boundary follows the size ratchet rather than ownership (`deep-module-design`). -> Concrete change: give the shared scope, tier and registry helpers a neutral home that both arms import as public names, keeping only the amendment arm in `amendment_brief.py`. This is a design smell surfaced separately, per CLAUDE.md, and no guard is involved. The kit-change-review rubric has no anchor for it -> @builder
- [MINOR] project-trajectory/scripts/amendment_brief.py:9 -> For clarity: the docstring says the arm was "Moved here whole and unchanged from `adjudicate_brief.py`". The same range changes the arm's behaviour:
  - removed scoped rows are briefed (`_removed_amended_rows`);
  - unknown scope tokens now refuse;
  - `_cell_block` is new;
  - `HAT_PARENTS` reporting is new.

  A reader trusting the docstring would skip reviewing the new behaviour (K1, text true). -> Concrete change: say it was moved from `adjudicate_brief.py` and then extended by WI-976 (removal briefing, unknown-token refusal, hat parents) -> @builder

VERDICT: CHANGES-REQUESTED findings=4
