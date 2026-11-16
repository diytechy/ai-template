# Vocabulary census: what the old words name today

The evidence behind `HANDOFF.md` §4. Read the handoff first; come here when a
row of its tables needs the identifiers, the files, or the reason a word stays.

Taken 2026-11-11 on `proposal/test-tiers` at `b5ea4d29c`. Nothing in the
repository was changed to produce it.

**How far to trust it.** Six sub-agents produced it: four classified the words
by reading the code and shipped prose, two inventoried stored data and the
adopters. The session that commissioned them checked nine quoted passages and
four counts against the source; one count was wrong and is corrected here
(work items with a `bar` key: 31, not 16). Per-sense splits are the
classifiers' estimates, good to about 10%. A `file:line` is where the
classifier read the claim; re-read it before editing, since lines move.

The role word used below is the new one, **operator**. Names in backticks are
spelled as they are on disk today.

## 1. Size

Occurrences, case-insensitive, tracked files, `OWNER_SCRATCHPAD.md` excluded.

| Stem | Scripts (`project-trajectory/scripts`, `scripts`) | Distinct names there | `tests` | Test functions named for it |
|---|---|---|---|---|
| `attest` | 875 | 73 | 1,258 | 113 |
| `approv` | 2,319 | 158 | 3,865 | 178 |
| `owner` | 1,019 | 54 | 1,049 | 44 |
| `human` | 625 | 41 | 469 | 17 |
| `accept` (already in use) | 620 | 42 | 750 | 57 |
| `operator` (already in use) | 89 | 8 | 98 | not counted |

Test files named for an old word: `test_bar_attestation.py`,
`test_integrate_attest.py`, `test_approval_level.py`,
`golden/approval-brief-no-assumptions.txt`. `test_interface_owner_reach.py`
uses the interface sense of "owner", which stays.

Records hold far more (`docs/iteration` alone: 9,251 `attest`, 22,140
`approv`). Records keep their words and are not counted as work.

## 2. The row lifecycle today

| Step | Status | The act | Who | Words in use |
|---|---|---|---|---|
| Author | `Drafted` | write the row | the authoring session | |
| First approval | `Drafted` to `Approved` | flip `status` and run `intake.py snapshot [--approves REG=REF]` in one commit (`PROCESS.md:481`, `intake.py:3785`) | on a held rung the operator or an attended session with a recorded delegation (`PROCESS.md:674`); on a released rung an independent adjudicator | approve, bless, accept ("who accepts", `PROCESS.md:450`), acceptor (gate-advance skill) |
| Demonstrated | `Founded` | computed, never typed (`PROCESS.md:492`) | derivation | |
| Amendment | stays `Approved` | the text moves; drift is measured against `docs/archive/last_approved/` | authoring session; an adjudicator rules CLARITY or MEANING | |
| Re-anchor | stays `Approved` | `intake.py snapshot --reattests IDs [--verdict F]` (`intake.py:3795`) | as for first approval; one exception lets an adjudicator re-anchor a CLARITY row on a held rung | re-attest |
| Retirement | row deleted | the same `--reattests`, naming the absent row (`adjudicate_act.py:49`) | as above | re-attest |

`status` is a closed set: `Drafted`, `Approved`, `Founded` (`kitlib/spine.py:547`).
`Approved` "says the row's TEXT is blessed and says nothing about tests
passing" (`PROCESS.md:491`). `Verified`, `Modified`, `Planned`, `Draft` are
retired values.

"Ratify" was retired on 2026-08-21 (WI-499) with the reason "ratification
holds a weight to it that the semantics here don't need"
(`check_vocab.py:22`). Two spellings survive: the directory `docs/ratify/` and
the legacy key `human_ratification_through`.

## 3. `attest`: seven things

| # | The thing | Who does it | Code | Tests | Prose |
|---|---|---|---|---|---|
| S1 | A script's record that checks passed on a tree | `integrate.py`, called by the loop or coordinator | ~270 | ~450 | ~115 |
| S2 | Re-anchoring an approved row after an amendment | operator or adjudicator, recorded by a script | ~395 | ~520 | ~230 |
| S3 | The `Attest` verification method | a named person | ~50 | ~55 | ~85 |
| S4 | The `[attestation]` policy table | scripts read it | ~70 | ~65 | ~35 |
| S5 | The work-item safety class `attestation` | dispatcher acts on it | ~13 | ~18 | ~10 |
| S6 | "Attestation" meaning the approval itself | operator or adjudicator | ~60 | ~125 | ~90 |
| S7 | A work item's status as the worker's claim | worker | 4 | ~2 | 0 |

**S1, the checks record.**
- Names: `attest` (function and subcommand), `_attest_commit`,
  `_attest_message`, `_attest_preflight`, `_AttestPlan` (`integrate.py`);
  `attest_build` (`agent_loop.py:2478`); `attest_refusal`
  (`kitlib/red_mark.py:316`); `_ATTEST_STEP` (`review_brief.py:192`);
  `_ATTEST_RE`, `BarAttestation`, `bar_attestation`, `read_bar_attestation`,
  `review_attestation`, `refresh_attestation`, `mechanical_close_attestation`
  (`kitlib/verdict.py:449-980`).
- Tests: `test_bar_attestation.py`, `test_integrate_attest.py` (both also
  named in `tests/conftest.py:142`), fixture `attest_repo` (44 uses).
- Surfaces: CLI `integrate.py attest --branch B --bar review` (parser
  `integrate.py:3770`; callers `agent_loop.py:2500`, `:3391`; hint
  `review_brief.py:192`). Default commit subject `attest: <branch> bar=review`
  (`integrate.py:3085`, read by nothing). Session-log `# phase: ATTEST` and
  the labels `ATTEST GREEN|RED` (`agent_loop.py:3441`, read by name by
  nothing). The trailer key itself, `Bar-Green:`, does not carry the word
  (`kitlib/station.py:134`).
- Who reads the trailer: `agent_loop.py:3386`, `review_brief.py:1083`,
  `integrate.py:1707`, `:2862`, `:2958`, `:3207`, `kitlib/verdict.py:531`,
  `:848`, `:875`, `:1000`, `:1505`. Each reads a lane against its base. No
  call site was found that walks landed history (found by grep of call sites,
  not by reading each function).
- The code says a trailer is "never an accept path" (`integrate.py:1684`,
  `agent_brief.py:1070`).

**S2, re-attestation.**
- Names: `reattest_model` (`trace.py:3922`), `reattest_lines` (`trace.py:4789`),
  parameter `reattests` (98 uses), `parse_reattests`
  (`baseline_snapshot.py:488`), `_refuse_reattests`, `_reattested_registry`,
  `reattested_between`, `reattest_scope_refusal`, `_reattested_added`,
  `_reattested_ids`, `_latest_reattest` (`acceptance_record.py`),
  `verdict_reattest_block` (`gen_open_items.py:943`), the in-memory kind
  `"reattest"` (`trace.py:3847`, `intake.py:3178`, `adjudicate_act.py:217`).
- Surfaces: flag `--reattests` (`intake.py:3795`), composed into command
  strings at `adjudicate_act.py:452`, `intake.py:908`, `pending.py:201`,
  `acceptance_record.py:1643`, `:1783`, `trace.py:4381`, `:4773`, `:4831`,
  `gen_open_items.py:825`, `:1107`, and typed in
  `prompts/adjudicate-act.template.md:32`, `:65`, `:69`. Ledger key
  `reattested` in `docs/archive/last_approved/acts.toml` (writer
  `baseline_snapshot.py:1833`; required by the validator at `:1637`; readers
  `acceptance_record.py:1140`, `:1164`, `kitlib/sitting.py:764`, `:801`,
  `gen_open_items.py:958`). Brief heading `# Re-attestation brief` in
  `docs/ratify/CURRENT.md` (`trace.py:4817`), regenerated and freshness-checked
  (`check.py:1044`); the dated copies are immutable (`check.py:1864-1960`).

**S3, the method.** Defined at `PROCESS.md:803-823`: "a named human's recorded
judgment", "trust-based, the box can be checked without the work having
happened", for "a playtest, a creative review, a physical action". Seven
methods are legal (`trace.py:634`): `Test`, `Demonstration`, `Manual`,
`Analysis`, `Inspection`, `Attest`, `Critique`. `Critique` is the model's
judgement against a written rubric, "deliberately separated from human
`Attest`".
- Names: `ATTESTED_METHODS` (`trace.py:770`), `attested_verified` (18 uses,
  `trace.py`), `LLR_EXEMPT` (`kitlib/spine.py:130`).
- Surfaces: registry cell `verification = "Attest"` (CSV column
  `Verification`); report strings `verified-attested=N`, `## Verification
  basis (mechanized / demonstrated / attested)`, `Approved SRs — attested
  (human, §4)` (`trace.py:6425`, `:6187`, `:5989`), pinned by
  `tests/golden/{clean,offspine,orphan}.txt`; the test-case cell convention
  `attested-by=` / `attested-on=` (`EXAMPLE.md:321`, parsed by nothing);
  skill tag `attest` (`skills/INDEX.csv:13`).
- Use: no row in this repository. 18 cells in four adopters (§8).
- The field is read in 12 scripts.

**S4, the table.** `[attestation]` holds `human_approval_through`,
`final_review`, `keep_nondependent`, `complete_review`,
`complete_sample_rate`, `adjudication_review`, `decision_recording`
(`agent_policy.py:128`). Writers: `process.toml.template:60`,
`bootstrap.py:1120`, `:1427`, `:1566`. Readers: `kitlib/authority.py:171`,
`:200`; `agent_policy.py:855`, `:880`, `:927`, `:959`, `:1048`;
`bootstrap.py:1350`, `:1409`; about 33 fixture lines in 15 test files. The
template already refused "attest level" as the dial's name because `Attest`
was a method (`process.toml.template:115`).

**S5, the safety class.** `safety_class = "attestation"` in work-item front
matter; readers `schedule.py:151`, `:190`, `:208`, `intake.py:1855`, `:2499`;
output "queued attestation row(s)" (`dispatch.py:1025`). One archived item
uses it (WI-518).

**S6, the approval itself.** `_unattested_rows`, `_attestation_cards`, format
keys `{attest}` / `{attestations}`, HTML card id `<row>-attest`
(`gen_open_items.py:815`, `:902`, `:1039`, `:1079`, `:1117`). Retired
surfaces with no reader: `attestations.csv`, the old `intake.py attest`
subcommand, the need field `attestation = "pending"`, the
`RE-ATTESTATION-PENDING` commit convention.

**S7 and the plain verb.** "a trailer CLAIMS the WI, it does not attest the
work" (`check_trajectory.py:1954`). About 40 to 60 plain uses in all.

## 4. `owner`: seven things

| # | The thing | Names | Share of the 765 bare uses in scripts |
|---|---|---|---|
| 1 | The role in charge | `OWNER_SCRATCHPAD`, `OWNER_ONLY_PATHS` (`agent_common`, `agent_loop`, `spec_move`), `OWNER_KEY`, `OWNER_VALUES`, `owner_state`, `_owner_findings` (`kitlib/decisions.py`, `done_when.py`), `owner_cards` (`pending.py`, `dispatch.py`), `OWNER_PROMPT` (`plan_runner.py:539`), prose `owner-only`, `owner-ruled`, `owner-held`, `pending-owner-actions`, `owner-registry` | ~538, of which ~212 cite a past ruling ("owner ruling D-8") and ~50 name the decisions key |
| 2 | Holder of a claim, lock or key | `_ownership_refusal` (`coordinator_guard.py`), `_owner` (`review_set.py:118`). The code mostly says "holder" | ~8 |
| 3a | The providing side of an interface row | `seam_owner` (`kitlib/spine.py:476`), `owner_files`, `_file_owner_declarations`, `file_owners`, `_owner_exact_findings`, `OWNER-EXACT`, `owner_key` (`trajectory_arch`), `owner_node`, `ownerless` (`traj_views`), `_ID_OWNER_RE` (`migrate_carrier`) | ~187 |
| 3b | The single home of a rule or file | `single-owner`, `owners`, `OWNERSHIP` | ~7 |
| 4 | The def or module that owns a docstring or function | locals in `gen_arch_map.py`, `check_iterate.py`, `check_complexity.py` | ~21 |
| 5 | The accountable hat or team | prose; the finding-line tail `-> @owner` | ~4 |
| 6 | A GitHub account | `OWNER/REPO` placeholders | 0 |

Also legal ownership in `project-trajectory/LICENSE` (8 uses).

Only sense 1 moves. Its stored surfaces:

| Surface | Writer | Readers | Ships |
|---|---|---|---|
| `OWNER_SCRATCHPAD.md` | `bootstrap_manifest.py:647` from `OWNER_SCRATCHPAD.template.md` | `agent_common.py:319`, `:1366`; `agent_loop.py:255`, `:4139`; `spec_move.py:245`; `integrate.py:3601`; `dispatch.py:1553`; `check_docs.py:174`, `:336`; `check_vocab.py:299` | yes |
| `owner = "confirmed"` or `"overruled"` in `docs/decisions/<run>.toml` | by hand; `decisions.migrate_text` (`kitlib/decisions.py:601`) | `kitlib/decisions.py:236`, `:351`, `:390`; `done_when.py:393`; `gen_open_items.py:1146` | yes (`decisions.template.toml:24`) |
| Prompt slot `{{OWNER_PROMPT}}` | `plan_runner.py:539` | `prompts/dual-plan-arbiter.template.md:17`, `:42` | yes |
| Brief marker `AWAITING FIRST APPROVAL - HELD FOR THE OWNER, NOT YOURS TO FLIP` | `adjudicate_brief.py:951` | quoted in `prompts/adjudicate-first-approval.template.md:66`; tests | yes |
| Minted work-item title `owner act: …` | `intake.py:913` | not parsed | yes |
| Generated `docs/open-items.html` text | `gen_open_items.py:1068`, `pending.py:277` | byte-compared on freshness; regenerates | yes |

Sense 3a is stored too and stays: the `owner` key on every row of
`interfaces.toml` (258 rows here; central reader `kitlib/spine.py:491`), and
the `Owner` column of the performance-budget and repos templates.

No commit trailer, CLI flag, subcommand or parsed `Owner:` line exists.

## 5. `human`: eight things, and the line the code draws

| # | The thing | Names | Share of the 302 bare uses in scripts |
|---|---|---|---|
| S1 | Who may take the approval act on a held rung | `human_approval_through` (40 uses, 11 files), `human_held`, `human_holds`, `human_approves`, `human_approves_spine`, `human-held` against `loop-held` (`agent_route.py:1384`, `agent_loop.py:3847`, `intake.py:3220`), `HUMAN-HELD` | ~150 |
| S1b | A judged commit as against a scripted one; trunk as against a lane | "the human path", "a human trunk commit" (`intake.py:4`, `:3200`, `:3548`, `:3624`). The code says this "is a statement about which SCRIPT decides, not about who may act" (`intake.py:3630`) | inside S1 |
| S2 | Escalation | `EXIT_NEEDS_HUMAN = 7` (`agent_common.py:275`), `NEEDS-HUMAN`, `PAGE-HUMAN`, action `"page-human"` (`agent_route.py:1296`), `page_human()` (`agent_loop.py:1974`), `"stop-needs-human"` (`plan_round.py:93`) | ~35 |
| S3 | Push authority | value `"human"` in `PUSH_POLICY_CHOICES` (`bootstrap.py:1156`), read at `agent_loop.py:3852` | ~15 |
| S4 | A person verified or observed | `HUMAN_METHODS`, `human_srs`, `Human-verified` (`gen_release_checklist.py:100-481`) | ~22 |
| S5 | The operator, by another name | `Needs <human>` (`_NEEDS_HUMAN_RE`, `check_docs.py:738`; `STACK_NEEDS_HUMAN`, `bootstrap.py:1736`), `human-owed` | ~17 |
| S6 | Whoever launched the run, "not the model" | `subagent_gate.py:18`, the log reason `(human-set)` (`:229`) | ~7 |
| S7 | A reader | `human-readable`, `humanized` | ~46 |

**What the code enforces.** It never detects a model. It detects a session
the loop started: the loop sets `KIT_LOOP_SESSION`, everything it starts
inherits it (`kitlib/provenance.py:11`, `:111`), loop writers refuse a held
move (`agent_policy.py:812`), the `held-status` step refuses a marked commit
outside a lane (`check.py:1975`), and the commit-msg hook requires a
`Loop-Session:` trailer on marked commits (`hooks/commit-msg:35`). An unmarked
trunk commit "nothing judges" (`PROCESS.md:691`). So an attended model session
on trunk is indistinguishable from a person. The one test for a person at a
keyboard is the console check before the guard hooks are installed
(`coordinator_guard.py:1531`), and it says "person".

`PROCESS.md:674` already defines the dial's "human" as the operator "or an
attended session on the owner's explicit delegation".

**How the dial works.** Values: any `DevStg-*` rung, or `DevStg-Below` for
nothing held; shipped default `DevStg-Release`; this repository uses
`DevStg-Boundary`. A rung is held when it sits at or below the dial
(`kitlib/authority.py:262`); an unrecognised value counts as held.

Stored surfaces carrying the word:

| Surface | Where | Reader |
|---|---|---|
| `[attestation] human_approval_through` | `process.toml.template:118`, `docs/process.toml` | `kitlib/authority.py:107`, `:176`; `agent_policy.py:128`, `:496` |
| `[policies] push = "human"` (other values `agent-iteration`, `agent`) | template `:177`; legacy one-word file `docs/push-policy` | `agent_loop.py:3852`, the launch banner only |
| Exit code 7 | `agent_common.py:275` | `dispatch.py:600`, `:702`; `coordinator_adjudicate.py:397`; documented as IF-015 |
| `Needs <human>` heading | `STATUS.template.md:11`, `docs/status.md` | `check_docs.py:738-764` |
| `Provenance` value `human-made` (with `ai-generated`, `mixed`) | `registries/assets.template.csv` | none |
| Log table column `Human` | `LOG.template.md:31` | none |
| Generated heading `## 2. Human-verified requirements` | `gen_release_checklist.py:327` | none |

`NEEDS-HUMAN` and `PAGE-HUMAN` are console text. No live code greps for them;
the substring reader was retired (`intake.py:471`).

## 6. `accept` and `operator` as they stand

| # | Existing meaning of "accept" | Names | Stored surface |
|---|---|---|---|
| A1 | The acceptance record: the `last_approved` copy and its ledger. Also called the "approval record" (24 uses) and "approval stamp" | `acceptance_record` (118 uses, 17 files); module `acceptance_record.py` | the data is in `docs/archive/last_approved/` |
| A2 | Accepted verdict: a script records that the adjudicator's call succeeded and its verdict parses (`kitlib/sitting.py:620`) | `accepted`, `accepted_at`, `accepted_identities`, `accepted_part`, `unaccepted_refusal`, `_unaccepted_reason` | `outcome = accepted` in `<verdict>.requested` under `docs/reviews/` (values `pending`, `accepted`, `failed`); writer `adjudicate_brief.py:385`; readers `kitlib/sitting.py:661`, `adjudicate_act.py:162`, `plan_gate.py:418`, `plan_coverage.py:571` |
| A3 | Accepted risk on an assumption row | `AcceptedRisk`, `accepted_risk_state`, `risk_acceptance_act` | column `accepted_risk` |
| A4 | Acceptance criteria on a system requirement | | column `acceptance_criteria` (138 rows here) |
| A5 | Acceptance intent on a stakeholder need | | column `acceptance` |
| A6 | Acceptance rule on a sampled test case | | column `acceptance_rule` |
| A7 | Acceptor: who accepts a stage advance | | row labels in the scaffolded `docs/gate-policy.md` (`bootstrap.py:860`) |
| A8 | Acceptance: the final read at release (`PROCESS.md:562`) | | a row of `LOG.template.md:40`; the dial is `final_review` |
| A9 | Merge admission: "accepted-on-train", "not an accept path" | | none |
| A10 | Accepting a performance regression | | none |

About a fifth of the code uses are plain English ("accepts both forms").

| Existing meaning of "operator" | Where |
|---|---|
| Shell and boolean operators | `_PS_OPERATOR`, `_OPERATORS`; about a third of the code uses; unaffected |
| Whoever runs the kit's tools | "operator override" for `--prompt-map`, the `operator-notes` block (`prompts.py:50`, `:184`); about two thirds |
| The party in this repository's frame | `EXT-006` "Human operator" (`docs/requirements/external.toml:130`), the party behind all four stakeholders, including `STK-01` "Owner" |
| A stakeholder of the adopter's product | `stakeholder-needs.template.toml:15`, `STATUS.template.md:67`, the hats' "operator time" |
| "A Claude operator sub-agent … judges nothing" | `skills/coordinator-cycle/references/recipes.md:1628` |

Neither word is in `GLOSSARY.md`. No config key, flag or column contains
"operator".

Candidates checked for the method's new name, by existing use in
`project-trajectory/` and `scripts/`: `judg*` 1,770 occurrences; `confirm*`
180; `sign-off` 47 (hat sign-offs at stage gates, `PROCESS.md:527`);
`assess*` 40; `opinion` 19; `vouch*` 7; `witness*` 7; `apprais*` 0.

## 7. Stored data in this repository

**Commit messages** (8,989 commits on all refs).

| Line | Commits | Dates | Read by a script |
|---|---|---|---|
| `Bar-Green: tree= work= bar=review tests=` | 367 | 2026-10-21 to 2026-11-08 | yes |
| `Bar-Green:` without `bar=` | 98 | 2026-08-01 to 2026-09-05 | no: "not read at all" (`kitlib/verdict.py:494`) |
| `Bar:` | 744 | 2026-07-10 to 2026-11-08 | no |
| `Smoke:` | 189 | 2026-08-02 to 2026-10-15 | no |

`bar=` has one value in history, `review`. No trailer key contains attest,
approve or human. Subject prefixes `attest:` (4), `reattest:` (15),
`approve:` (22), `owner:` (6) are convention; nothing parses them.

**Registries** (TOML under `docs/requirements` and `docs/test`).
- 904 rows carry `status = "Approved"`; 258 interface rows and 20 assumption
  rows are `Drafted`.
- Rows whose text holds an old word, the status and evidence cells excluded:
  `attest` 88, `owner` 82, `human` 73, `approv` 171. Any of the first three:
  196. Any of the four: 286. These are upper bounds, since some uses stay.
- Evidence cells that cite a test named for an old word: `attest` 21,
  `approv` 25, `owner` 7, `human` 2.

**Other machine-read data.**

| Item | Count |
|---|---|
| `docs/archive/last_approved/acts.toml` entries, each with `approved` and `reattested` keys | 181 |
| `owner =` keys in `docs/decisions/*.toml` (`confirmed` 49, `overruled` 3) | 52 in 16 files |
| Work items with a `bar` key, all archived (33 lines in 31 files: `DevStg-Reqs` 14, `DevStg-Tests` 17, `DevStg-Impl` 2) | 31 |
| Work items with `safety_class = "attestation"`, archived | 1 |
| Work items with `brief = "first-approval"`, archived | 36 |
| `docs/ratify/` files, four of them named `*-reattest.md` | 16 |
| `docs/process.toml`: `[attestation]`, `human_approval_through = "DevStg-Boundary"`, `push = "human"` | |
| `docs/stack.ini`: a path-map line `docs/ratify/ = approve` | |
| `docs/complexity-baseline` rows keyed by function name, including `_needs_human_block`, `reattest_model`, `approval_lines` | |

One lane worktree existed on 2026-11-11: `C:/Projects/ai-template.wt/wi-902`.

## 8. Adopters on this machine

Ten, all stamped at July 2026 kit commits, all vendoring their own copy of
the kit scripts. None has `docs/process.toml`, and none holds `[attestation]`,
`human_approval_through`, `human_ratification_through`, `[bars]`, `red_mark`,
a `Bar-Green:` trailer, a work-item `bar` key or a `Needs <human>` heading.
Their vocabulary is older still: `G1` to `G3`, "bar", "ratify".

| Adopter | `docs/kit-version` | Registries | Old-word data it holds |
|---|---|---|---|
| gilbert | `0fc58fb` 2026-07-31 | CSV | `docs/push-policy` = `human`; `docs/gate-policy` = `attended`; `docs/gate` = `G1`; `gates = G3` in `stack.ini`; `OWNER_SCRATCHPAD.md`; a hook naming the retired step `ratify-fresh` |
| FileBackup | `9b697cc` 2026-07-02 | TOML | status `Approved`; `docs/gate` = `G3` |
| Finance-Auditor | `cb747cd` 2026-07-05 | CSV | `push-policy` = `human`; `gate-policy` = `autonomous`; one test case with method `Attest` |
| NotHomeWrecker | `dc4ba24` 2026-07-05 | TOML | status `Approved`; `push-policy` = `human`; four `Attest` cells |
| NagLight | `9670982` 2026-07-01 | TOML | status `Approved` (7 rows) |
| PictureSorter | `9b697cc` 2026-07-02 | TOML | status `Approved` |
| Pictures2VideoSlideShow (two clones) | `9b697cc` 2026-07-02 | CSV | `docs/gate` = `G2` |
| MinecraftKeeper | `605252d` 2026-07-03 | CSV | one test case with method `Attest` |
| MiniPC-Deployer | `605252d` 2026-07-03 | CSV | `docs/gate` = `G1` |
| BandWars | `605252d` 2026-07-03 | CSV | twelve requirements with `Verification` = `Attest` |

What the `Attest` rows are: playtest judgements in BandWars ("Core loop is
fun", "Hits feel impactful"), visual judgement of galleries in
NotHomeWrecker, and one hand-performed release check each in Finance-Auditor
and MinecraftKeeper.

`EPC-*` is a partial adopter (a privacy hook only).

## 9. How the kit has renamed before

| Posture | Used for |
|---|---|
| Read, warn, migrate in place | the dial key `human_ratification_through` (`kitlib/authority.py:129`, `:203`; `bootstrap.py:1326`), the 0 to 4 dial ordinal, `gates =` in `stack.ini`, the one-word policy files (`LEGACY_CONFIG`, 14 rows) |
| Read silently | the work-item `bar` tags (`intake.py:214`, duplicated at `integrate.py:1926`) |
| Read and translate by meaning, warn | `--gate G1..G3`, `DevBar-*` (`kitlib/config.py:536`) |
| Refuse, naming the new key | `[bars]`, `red_rounds_max` (this branch) |
| Cut with no reader | `Bar-Green` without `bar=` |

Migration tools that exist: `bootstrap.py --migrate-config` (run by every
scaffold pass, `bootstrap.py:1440`, `:2848`), `migrate_carrier.py` (CSV and
markdown registries to TOML), `migrate_decisions.py` (rewrote a retired key;
no reader was kept). `bootstrap.py` keeps its own copies of literals because
it may not import kit modules.

The core scripts hold twelve named legacy or retired tables:
`RETIRED_STAGE_ALIASES`, `_LEGACY_BAR_THRESHOLD`, `_RETIRED_WI_BARS`,
`_RETIRED_BARS`, `LEGACY_DIAL_ORDINALS`, `LEGACY_DIAL_KEY` (re-exported as
`LEGACY_ATTESTATION_KEY`), `LEGACY_GATE_DIALS`, `LEGACY_APPROVAL`,
`LEGACY_CONFIG`, `PROCESS_KEY_LEGACY_VALUES`, `_RETIRED_FLAG`,
`RED_ROUNDS_RETIRED_KEY`, and the check's `RETIRED_TAG_RE`.

**The vocabulary check**, `project-trajectory/scripts/check_vocab.py`, shipped
(`bootstrap_manifest.py:521`), step `vocabulary` from `DevStg-Needs`
(`check.py:753`), strict from `DevStg-Impl`.
- One regex, `RETIRED_TAG_RE` (`:111-135`): `G0` to `G3`, `G-Release`,
  `G-Final`, `DevBar-*`, and every inflection of `ratif`, with the path
  `docs/ratify/` carved out. Suggestions in `SUGGEST` (`:136`).
- It anchors on word boundaries, and an underscore is a word character, so it
  does not fire inside a snake-case name. `human_ratification_through` escapes
  it only for that reason.
- Exemptions: the markers `check_vocab: allow` and `check_vocab: allow-file`;
  `EXEMPT_GLOBS` (`:234`), which covers `docs/archive/*`, `docs/log.md`,
  `docs/log.d/*`, `docs/rubrics/*`, `docs/ratify/*`, generated files and
  open-item rows.

`project-trajectory/RESYNC_PACK.md` is prose only (10,844 lines). An entry is
headed `### <title> [since <sha>]` and has four parts: what changed, what to
do, kit-owned files to overwrite, regenerated files. `scripts/check_resync.py`
(repo-local) refuses a change to a shipped path without a new entry.

## 10. Found in passing

- `skills/gate-advance/SKILL.md:146` says to amend and re-copy in the same
  commit. `PROCESS.md:506` says text first, the act second, and
  `acceptance_record.py:1640` agrees with the process doc.
- `bootstrap.py:906` writes `LLM-Attest` into the scaffolded gate-policy
  register as a model's judgement, while `PROCESS.md:817` keeps model
  judgement apart, under `Critique`.
- `Critique` is counted as "a human observing" in the trace report
  (`trace.py:773`, `:6191`).
- `docs/stack.ini:197` names a test file that does not exist,
  `test_attestation_ledger`.
- `bootstrap.py:1868` has a variable `human_anchor` that anchors on the "In
  flight" bullet.
- gilbert's pre-commit hook still names `ratify-fresh`, a step the current
  `check.py` does not have.
