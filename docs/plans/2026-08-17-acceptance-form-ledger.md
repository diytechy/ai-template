# Acceptance-form ledger — sitting-3 §0.4 item 19 executed (2026-08-17)

**The ruling (owner, 2026-08-17, verbatim):** "can you formulate the acceptance
criteria in terms of the exact boundaries, pass/fail conditions, and edge cases
for when the work is finished with respect to the behavior the system
requirement asks for?" — a THIRD form, superseding the two options on the
table (trace-tier move vs registry-id anchors): an SR acceptance cell states the
**behavioral fit criterion** — exact boundaries, pass/fail conditions and edge
cases defining "the work is finished" for the behavior the requirement asks —
naming **neither concrete artifacts nor the row's own decomposition chain**.
Artifact bindings live at the design/trace tier (LLR `module`/`detail`, TC
`evidence`); chain-completeness is the `Founded` state's claim (`2026-08-17m`),
never an acceptance criterion.

**Method (WI-444-style token verification):** population re-derived at the desk
(filename/path tokens in SR `acceptance_criteria`): **40 of 70 SRs** — the
sitting-3 table said 39; the +1 is `SR-112`, whose carrier trailer's
`project-trajectory/skills/` path the desk scan missed. 33 cells carried the
literal "current carrier" idiom; `SR-052/053/054` carried the chain-closure
opener. Before any name was stripped, its trace-tier home was verified per
token (LLR module/detail or TC cells under the same SR); where the acceptance
cell was the ONLY home, the binding was moved to the design tier **in this same
commit** (the WI-469 lesson: re-home first, then drop). No obligation weakened:
every observable the old cell demanded is still demanded in behavior terms, or
its removal is a pure carrier-naming drop recorded per row below.

**Counts:** 50 acceptance cells edited (39 artifact-stripped of the 40-row
population + 3 chain-closure-replaced + 8 re-worded for form with no path token
— `SR-018/019/031/113/160/175/176/177`); **1 flagged, not edited**: `SR-150` is
`Approved` (outside the open window — its `check_need_form.py` naming is the
sitting's to re-open, not this pass's); 19 rows read against the form and left
untouched as compliant. Re-homed bindings: 8 LLR `detail` cells
(`LLR-012/014/035/038/044/067/136/156`) + 2 SR `rationale` lines
(`SR-129` pointer correction, `SR-151` only-home carrier record). All row
`status` values unchanged.

**Old-cell provenance:** `sha256:12` of the pre-edit cell at `HEAD` when this
pass ran; the full old text is the parent commit's registry.

| Row | Old acceptance (first line + hash) | New acceptance (first line) | What was strengthened / moved / justified-dropped |
|---|---|---|---|
| SR-006 | `3aa3d254db8c` check.py --gate <bar> runs that bar's steps; a required-but-absent tool fails the gate with guidance… | Invoked for a bar, the harness runs that bar's declared steps; a required-but-absent tool fails the … | check.py + flag names (--gate/--lenient/--tier) re-voiced as the harness/declared modes; the three named still-running steps replaced by the strictly stronger 'every non-freshness step still runs' (the requirement's own clause); carrier trailer dropped. Binding: LLR-006/008/141 module=check.py. |
| SR-007 | `3b0daaf76ac9` check.py resolves each step's command from stack.ini; changing the profile changes the commands run,… | Each step's command resolves from the declared stack profile; changing the profile changes the comma… | check.py/stack.ini re-voiced as the declared stack profile; trailer dropped. Binding: LLR-007/LLR-008 (module check.py), TC-007 (stack.ini). |
| SR-009 | `09c643805170` A non-Python profile omits Python-only artifacts and seeds files-mode arch-map; a profile that selec… | A non-Python profile omits Python-only artifacts and seeds files-mode arch-map; a profile that selec… | Carrier trailer (bootstrap.py) dropped; behavioral clauses untouched. Binding: LLR-009. |
| SR-010 | `035adedef1e9` bootstrap.py --dest produces a scaffold on which the harness passes; the meta-suite runs every scrip… | A freshly generated scaffold is one on which the delivered harness passes with no edit; the kit's ow… | 'bootstrap.py --dest' re-voiced as the freshly generated scaffold + the kit's own suite; trailer dropped. Binding: LLR-010, TC-010. |
| SR-011 | `5d5a3b26640b` A re-run leaves every existing file (kit- or project-owned) byte-unchanged without --force; --force … | A re-run leaves every existing file (kit- or project-owned) byte-unchanged unless the explicit overw… | '--force' re-voiced as the explicit overwrite; trailer dropped. Binding: LLR-011 and TC-011 both carry --force. |
| SR-018 | `074b42968d39` With privacy-check on, an identity/PII class is flagged unless the author is in EXEMPT_EMAILS; with … | With privacy-check on, an identity/PII class is flagged unless the author is a configured exempt ide… | Code symbol EXEMPT_EMAILS re-voiced as a configured exempt identity. Binding: LLR-018 (module check_privacy.py, 'exempting configured author identities'), TC-018. |
| SR-019 | `43344cb1e0cc` The hook runs trace --strict-integrity and the secrets scan on staged content and blocks a commit th… | The hook runs the registry-integrity floor and the secrets scan on staged content and blocks a commi… | 'trace --strict-integrity' re-voiced as the registry-integrity floor; the git --no-verify edge kept verbatim (it IS the edge the row exists to pin). Binding: LLR-019 (Approved) detail carries the command. |
| SR-022 | `e14ea0f36df8` A drifted vendored copy is a finding; an in-sync copy passes. Read off the current carrier, as the c… | A drifted vendored copy is a finding; an in-sync copy passes.… | Carrier trailer (check_vendored.py) dropped. Binding: LLR-022, TC-022. |
| SR-024 | `6aa2f2824ce1` A spec grammar (range/set/bool with @full\|@pairwise\|@boundaries) yields the expected case set. Read … | A spec grammar (range/set/bool with @full\|@pairwise\|@boundaries) yields the expected case set.… | Carrier trailer (gen_cases.py) dropped; the spec grammar tokens kept (declared input vocabulary, not an artifact). Binding: LLR-024, TC-024. |
| SR-026 | `45be3d64a9ce` A worker reconciles from its assignment + committed evidence and the integrator from trunk history; … | A worker reconciles from its assignment + committed evidence and the integrator from trunk history; … | Carrier trailer (agent_loop.py) dropped. Binding: LLR-026/061/143, TC-026. |
| SR-027 | `fe51cfd52b03` Outside a git repo, with no agent CLI, or with a private author under privacy-check, preflight exits… | Outside a git repo, with no agent CLI, or with a private author under privacy-check, preflight exits… | Carrier trailer (agent_loop.py) dropped. Binding: LLR-027/029/030, TC-027/029/030. |
| SR-028 | `c5bc68ec730a` Every declared end state returns its assigned outcome code, and an unrecognized end state fails rath… | Every declared end state returns its assigned outcome code, and an unrecognized end state fails rath… | Carrier trailer (agent_loop.py) dropped. Binding: LLR-028, TC-028. |
| SR-031 | `757871d19f7c` Every enforcer reads the same value for the same dial; the two delivered grammars (tomllib and the h… | Every enforcer reads the same value for the same dial; the two delivered reader grammars return the … | Parenthetical '(tomllib and the hooks' sh)' dropped; 'the two delivered reader grammars' keeps the two-reader boundary. Binding: LLR-155 detail (the sh-vs-parse pair), SR-137 rationale, code. |
| SR-033 | `3b9732c26d85` Running the generator emits the checklist content: the perf-budget section lists each warn-tier PB w… | Running the generator emits the checklist content: the perf-budget section lists each warn-tier PB w… | Carrier trailer (gen_release_checklist.py) dropped. Binding: LLR-033, TC-033. |
| SR-034 | `d66da8c0f5ed` An AST scan of scripts/*.py resolves every top-level import to stdlib, a local sibling, or a Kind=py… | Every kit script's top-level imports resolve to the standard library, a local kit sibling, or a revi… | 'AST scan of scripts/*.py', 'Kind=python row in docs/dependencies.md' and the trailer re-voiced as the ledger-row condition; the scan mechanism and concrete path live in TC-034's method/evidence (tests/test_dependency_ledger.py). |
| SR-035 | `4b533c99f215` A non-Python-profile scaffold passes trace.py --strict-integrity --strict-schema unmodified; a token… | A non-Python-profile scaffold passes the delivered registry checks at their strict integrity and sch… | 'trace.py --strict-integrity --strict-schema' re-voiced as the delivered registry checks at their strict integrity and schema tiers; trailer dropped. Binding: LLR-171, TC-035/165. |
| SR-036 | `b0c33e2827b9` Following ADOPTING.md section 6 against the docs/kit-version diff, kit-owned files are taken wholesa… | Following the documented re-sync procedure against the recorded kit-version diff, kit-owned files ar… | ADOPTING.md section 6 + docs/kit-version re-voiced as the documented re-sync procedure + recorded kit-version diff; trailer dropped. Binding: TC-036 (Approved) names both. |
| SR-040 | `b2c9d0e39a46` A mapped session phase invokes its own command template and the default template does not fire; a br… | A mapped session phase invokes its own command template and the default template does not fire; a br… | docs/process.toml [policies] review_rounds -> the declared reviewer dial; status.md -> the resume surface; AGENT_STATUS_WARN_BYTES=0 -> a declared zero/negative threshold. FLAG for the sitting: the env var named by the old cell occurs NOWHERE in the delivered code or tests (status_size_warning retired with the serial driver, WI-210) - the old cell named a phantom carrier; LLR-037 (Approved) still describes the retired symbol. Divergence recorded, not ruled here. |
| SR-043 | `a0091743e77b` With [checks] subagent_gate = "deny": a Task/Agent spawn is refused (permissionDecision=deny, exit 2… | With the declared subagent-gate dial deny, a subagent spawn is refused (a deny decision at the tool … | '[checks] subagent_gate'/Task/Agent/SUBAGENT_GATE=allow re-voiced as the declared dial, a subagent spawn, the launcher-held override (the requirement itself names the env override); trailer dropped. Binding: LLR-040 detail carries the full concrete set, TC-043. |
| SR-046 | `0655f96c5b74` run_menu.py --list prints one name<TAB>desc line per declared capability in declaration order; run_m… | A machine listing prints one name-and-description line per declared capability in declaration order;… | run_menu.py/run.cmd/run.sh/run.command/[run]/RUN_CMD re-voiced as the selector, the platform launchers, the capability declaration; exit 1 and the closed-stdin edge kept numerically. Binding: TC-047 (Approved) method carries the whole concrete set verbatim; LLR-047 module=run_menu.py. |
| SR-049 | `6c49826db5d7` derive_gate.py --print on the meta computes the per-phase gates from the current states (an amended … | The per-phase gates derive from the current artifact states alone (an amended row's phase reads the … | derive_gate.py --print/--check and docs/gate re-voiced as the derived per-phase gates, the freshness check, the cached derived value's basis. Binding: LLR-050/147/148 (module derive_gate.py; docs/gate in detail), TC-050/141/142. |
| SR-052 | `4f5feb3c9924` Acceptance is the row's decomposed chain, passing: each clause of the requirement — keyboard reachab… | Operating the produced view with keyboard alone reaches and activates every interactive element — ta… | Chain-closure opener REPLACED by the behavioral fit criterion per the item-19 ruling: keyboard reachability incl. the hidden-focusable edge, non-empty non-bare-id accessible names, colour-removed readability, the declared contrast floor; pass = full sweep of every emitted view, fail = one failing element/encoding/pair. Thresholds stay the children's (LLR-101..114, TC-104..119); no chain reference remains. |
| SR-053 | `5a81f63c1f2c` Acceptance is the row's decomposed chain, passing: each clause of the requirement — one type scale a… | Across every tab, view and emitter of the produced state view: every font size resolves to a step of… | Chain-closure opener REPLACED: one type scale/rhythm, one colour vocabulary with no cross-vocabulary reuse, uniform node/edge/legend/panel styling with one highlight idiom, one interaction idiom per role; fail conditions stated; sweep closed over every emitter ('a new emitter joins the bar by existing'). Token sets stay the children's (LLR-102..111, TC-105..116). |
| SR-054 | `fc1be81c8167` Acceptance is the row's decomposed chain, passing: each clause of the requirement a test can hold — … | A first-time reviewer reaches each core reading task — the project state, the next work, and how the… | Chain-closure opener REPLACED: labelled entry point per core task within one tab switch, start-collapsed above the declared threshold, detail-with-return-path, label legibility over real volumes; fail conditions stated; the non-mechanized first-time-reader clause stated as resting on a recorded human judgement, a stated limit (TC-055's recorded verdict), with no chain or instrument named. |
| SR-070 | `d4b3b364e98d` Regeneration from unchanged sources is byte-identical; a generated artifact opens and stays usable w… | Regeneration from unchanged sources is byte-identical; a generated artifact opens and stays usable w… | Carrier trailer (gen_trajectory.py --check, gen_arch_map.py --check, gen_okf.py) dropped. Binding: LLR-023/035/039, TC-023/038/042. |
| SR-111 | `bf1e82d30e66` docs/kit-version records the kit SHA and date; a scaffold from an uncommitted kit tree is marked -di… | The recorded stamp carries the kit commit SHA and date; a scaffold generated from an uncommitted kit… | docs/kit-version + trailer re-voiced as the recorded stamp. Binding: LLR-121 (Approved) detail names docs/kit-version and -dirty. |
| SR-112 | `09df6f5343d3` A per-agent copy that diverges byte-for-byte from source is detectable and refreshed by one command.… | A per-agent copy that diverges byte-for-byte from source is detectable and refreshed by one command.… | Carrier trailer (.claude/.gemini/.agents copies from project-trajectory/skills/) dropped. Binding: LLR-025/043 (gen_skills_index.py), TC-025/045. |
| SR-113 | `2ca84cf9cb45` After dev-setup the pre-commit floor is active without a separate setup step. Read off the current c… | After the scaffolded developer setup runs, the pre-commit floor is active without a separate setup s… | Trailer (dev-setup script, core.hooksPath) dropped; 'the scaffolded developer setup' keeps the subject. Binding: LLR-122 (module dev-setup.template.sh; hooksPath), TC-032. |
| SR-129 | `2bdf16f19ba3` wi_convert --verify over a populated registry exits 0 reporting cell-exact equality; an unknown stat… | A verification pass over a populated registry exits 0 reporting cell-exact equality; an unknown stat… | wi_convert --verify and folder->CSV->folder re-voiced as a verification pass and the current/legacy representations (the requirement's own vocabulary); trailer's two carriers (docs/work/, work-items.csv) MOVED to LLR-136 detail in this commit (re-home first, then drop); SR-129 rationale's 'to acceptance as current-carrier evidence' pointer corrected to the design row in the same act. |
| SR-137 | `c98869c747dd` A dial declared in both homes produces a refusal naming the key and both files, at every guarded ent… | A dial declared in both homes produces a refusal naming the key and both files, at every guarded ent… | Carrier trailer (docs/process.toml + legacy files) dropped; the refusal/entry-point/shape boundaries untouched. Binding: LLR-155 detail parses docs/process.toml; TC-150. |
| SR-138 | `a1f203484f39` A repo carrying legacy files converts in one pass and reports what moved; a second pass is a no-op; … | A repo carrying legacy files converts in one pass and reports what moved; a second pass is a no-op; … | Carrier trailer (bootstrap.py --migrate-config, docs/process.toml) dropped; the flag and destination MOVED to LLR-156 detail in this commit. Binding: LLR-156, TC-152. |
| SR-147 | `24430cd37140` migrate_carrier.py --check over the live registries exits 0 reporting the round-trip clean for every… | A migration check over the live registries exits 0 reporting the round-trip clean for every row of e… | migrate_carrier.py --check re-voiced as a migration check; 'tomllib' re-voiced as the declared format's standard parser. Binding: LLR-165 (Approved, module migrate_carrier.py, TOML emission detail), TC-159. |
| SR-149 | `6f8b4541e949` check_vocab.py reports a planted retired tag in a live authored file with its path and line, exits 0… | A planted retired tag in a live authored file is reported with its path and line, at exit 0 under th… | Subject 'check_vocab.py' dropped; every severity, carve-out class, marker and the 'gate' edge kept verbatim. Binding: LLR-169 (module check_vocab.py), TC-163. |
| SR-151 | `f8ded7f11546` tests/test_ci_tier_declaration.py pins the shipped workflow's trigger set and per-trigger tier again… | The shipped workflow's trigger set and per-trigger tier match the declared moment-to-tier table, pin… | tests/test_ci_tier_declaration.py + [ci-tiers] re-voiced as the declared moment-to-tier table, pinned by test. ONLY-HOME re-home: the row has no design or test child yet, so the two carriers are recorded in the row's own rationale in this commit (flagged for the sitting: the binding should move to the LLR/TC minted at decomposition). |
| SR-154 | `d75dbc21477d` A declared review policy of N schedules N independent reviewer sessions; the declared (family x mode… | A declared review policy of N schedules N independent reviewer sessions; the declared (family x mode… | docs/agents.toml + docs/agents-enabled re-voiced as the delivered agent registry's pair-rows and the declared consent surface; both carriers MOVED to LLR-044 detail in this commit. |
| SR-156 | `6c58f766bc06` A launch with independent ready work runs up to the configured lane ceiling concurrently in isolated… | A launch with independent ready work runs up to the configured lane ceiling concurrently in isolated… | Carrier trailer (integrate.py, lane.py, agent_common.py) dropped. Binding: LLR-138/140/150/151, TC-131/132/145. |
| SR-157 | `62968261f48d` Each declared registry rule violation is reported with row-level attribution; the declared strict se… | Each declared registry rule violation is reported with row-level attribution; the declared strict se… | The 'as the current set' checker enumeration (trace.py/trace_text.py/check_trajectory.py symbols, flags, [checks] key) re-voiced as the rule inventory the delivered checkers publish, by class; the scope-default clause kept verbatim. Bindings verified per token: ID_PATTERNS/flags at LLR-002/003, form/provenance vs advisories at LLR-004/133/134/135, work-item rules at LLR-077/084, trajectory_check opt-out at LLR-034. |
| SR-158 | `5da6a7a40998` A dead intra-repo link, an absent PROJECT-VISION tag, a stale generated doc under --stale, a danglin… | A dead intra-repo link, an absent or repeated vision declaration, a stale generated doc under the st… | The declaration-site enumeration (check.py step, check_docs/check_doc_refs/check_figures, stack.ini rows, orphans-allow, declared-absences) re-voiced as per-class severity boundaries (which class gates at which bar, warn defaults, dangling-only gating); the undeclared-class clause kept. Re-homed in this commit: the check.py doc-navigability wiring + docs/orphans-allow to LLR-012, the [step:doc-refs] declaration + docs/declared-absences to LLR-038; check_figures/stack.ini already at LLR-146/TC-140. |
| SR-159 | `d6c2ddd8dc7f` Malformed or unresolvable IF rows are findings; undeclared endpoints, uncovered cross-component edge… | Malformed or unresolvable IF rows are findings; undeclared endpoints, uncovered cross-component edge… | Same treatment: checker/file names re-voiced by rule class; TOP_VIEW_MAX -> its declared bound (bound value at LLR-049/TC-049); [checks] opt-outs -> two declared opt-outs (LLR-042); the SR-162/SR-157 carve-out paragraph kept verbatim (registry-id anchors). Re-homed in this commit: the gen_arch_map.py generated block in docs/architecture.md as the joined inventory, to LLR-067. |
| SR-160 | `38d4bfdbfc9c` A fresh scaffold and this repository each carry both launcher sets (dev-setup and agent-resume) at t… | A fresh scaffold and this repository each carry both launcher sets (environment preparation and loop… | Launcher basenames '(dev-setup and agent-resume)' re-voiced as the two action classes the requirement names; 'python3' re-voiced as a working interpreter (the requirement's own vocabulary). Binding: the launcher sets are pinned by tests (test_onboard_devsetup/test_bootstrap) via SR-113's and this row's TCs. |
| SR-166 | `3580f0a01dff` A manifest entry whose destination a fresh scaffold does not contain fails naming the destination; a… | A manifest entry whose destination a fresh scaffold does not contain fails naming the destination; a… | The Evidence sentence (tests/test_bootstrap.py, tests/test_dogfood_sync.py) dropped from acceptance; the row's own rationale already names both tests as the verification evidence (no home lost); both behavioral clauses and the deliberate SR-163 non-restatement kept. |
| SR-167 | `f4487dfaf88c` Read off the current carrier — check_perf.py, the harness's built-in perf-budgets step (IF-004/IF-03… | An in-tier hard-gated performance-budget row whose measured metric breaches its absolute Budget, or … | The carrier preamble (check_perf.py, IF-004/IF-031), Gate=fail/warn schema vocabulary, the two json paths and the Evidence sentence re-voiced as hard-/warn-gated rows against the committed baseline, 'proven end to end against a bootstrapped scaffold' kept as the virtualization boundary; metrics/baseline paths + --update-baseline MOVED to LLR-014 detail in this commit. |
| SR-168 | `97797396be36` The state view carries per-tier completeness, the requirement decomposition down to its leaves, the … | The state view carries per-tier completeness, the requirement decomposition down to its leaves, the … | Carrier trailer (PROJECT_STATE.html, gen_trajectory.py --status) dropped; the artifact name MOVED to LLR-035 detail in this commit. |
| SR-169 | `3143d9b01664` Declared components render with their containment preserved at each visible level; each declared int… | Declared components render with their containment preserved at each visible level; each declared int… | Carrier trailer (How-SW/interface-graph views of PROJECT_STATE.html) dropped; the root-artifact binding lives at LLR-035 (one home); the view identities are pinned by TC-081/087-090 evidence test names. |
| SR-170 | `bd854463f235` The compiled activity log and the generated project-state artifacts are written only by the serial m… | The compiled activity log and the generated project-state artifacts are written only by the serial m… | Carrier trailer (trunk_step.py, check.py) dropped; the cross-row partition sentences (SR-173's/SR-174's/SR-006's) kept - registry ids are sanctioned anchors. Binding: LLR-060/124/137 (trunk_step.py), LLR-141 (check.py). |
| SR-173 | `5472fc1e08f1` Regeneration runs the declared artifact families in declared dependency order, with a producer befor… | Regeneration runs the declared artifact families in declared dependency order, with a producer befor… | Carrier trailer (trunk_step.py --regen) dropped. Binding: LLR-142 detail describes the regen sequence; TC-135/170 name the tests. |
| SR-174 | `00eaf43705e0` Two actors finishing against the same tree cannot obtain the same work-item identity; an identity fr… | Two actors finishing against the same tree cannot obtain the same work-item identity; an identity fr… | Carrier trailer (intake.py, post-merge arm of integrate.py) dropped. Binding: LLR-153/154 modules, TC-147/148/158. |
| SR-175 | `61586b5e1d05` The inclusion rule for each brief class the loop dispatches is readable as a declared set naming wha… | The inclusion rule for each brief class the loop dispatches is readable as a declared set naming wha… | The 'Read off the current carriers' idiom re-voiced; the conventions-made-declared content and the stated build gap kept in full (no artifact was named). |
| SR-176 | `b44fbf351782` A planted value matched by a scanning class appears 0 times in any tracked artifact after the run th… | A planted value matched by a scanning class appears 0 times in any tracked artifact after the run th… | The idiom re-voiced; the redaction-seam boundary (credential classes hold, PII/identity classes are the stated gap) kept in full. Binding: LLR-177 detail carries the concrete seam. |
| SR-177 | `5364cc5ad8c0` A completed run's report states the lanes configured, the lanes actually occupied, and the work item… | A completed run's report states the lanes configured, the lanes actually occupied, and the work item… | The idiom re-voiced; the telemetry-aggregation boundary and stated build gap kept in full (no artifact was named). |

## Rows flagged for the sitting (not ruled here)

- **SR-150 (`Approved`)** — the one population row not edited: its acceptance
  still opens with `check_need_form.py`. Amending it is an attestation override
  (a lone re-attest window outside a batched one); the sitting can re-word it in
  the same act that re-attests it. Binding already exists: LLR-170 module,
  TC-164 evidence.
- **SR-040 / LLR-037 phantom carrier** — the old acceptance named
  `AGENT_STATUS_WARN_BYTES`, which occurs nowhere in the delivered code or
  tests (`status_size_warning` retired with the serial driver, WI-210); LLR-037
  (`Approved`) still describes the retired symbol. The re-word states the
  behavior without the phantom name; whether the tripwire obligation itself
  still stands is an acceptance-vs-implementation divergence for the sitting.
- **SR-151 only-home residue** — carriers recorded in the row's rationale
  because no LLR/TC exists yet; at decomposition the binding moves to the
  minted design/test rows and the rationale line retires.

---

# Addendum — the 2026-08-18 pre-brief pass (log `2026-08-18a`)

**The directive (owner, 2026-08-18, verbatim):** *"please implement any items
that might block / affect the spine's attributes that I am preparing to
approve, so I do not have to do it twice."* This sanctions **deliberate rides**
on `Approved` rows where the fix is owed anyway; each is named below as a ride.

**Method — unchanged from the pass above:** per-cell before/after with the
pre-edit cell's `sha256:12` taken at `HEAD` (`4cf98e4f`), so any claim here is
checkable against the parent commit. No obligation is weakened without a
code-truth justification stated in the row's own rationale.

**Rides taken (4):** `SR-140`, `SR-150`, `LLR-037`, `TC-040` — all
`Approved` → `Modified`. **Mints (4, all `Drafted`):** `SR-178`, `SR-179`,
`LLR-178`, `TC-173`. `SR-040` and `SR-173` were already open and did not ride.

## A. The `SR-140` split (directive item 1)

Three `shall` clauses in one row, under a waiver that never resolved the
finding. Split on the one-decision doctrine; **no obligation dropped** — each
clause became the normative text of exactly one row, and every child moved to
the obligation it actually serves.

| Row | Cell | old `sha256:12` → new | Obligation now carried |
|---|---|---|---|
| SR-140 | `requirement` | `1ad8b87fadf5` → `7819502f76fb` | clause 1 only — the RECORD (byte-identical copy riding the approval commit; transition + acting reviewer queryable). Clauses 2 and 3 removed **because they moved**, not because they were dropped |
| SR-140 | `acceptance_criteria` | `6c3c7ce66f97` → `326ae486506a` | the record's criteria + the SEED rule; the drift clause left for SR-178, the refusal clause for SR-179 |
| SR-140 | `rationale` | `a9dea99645a8` → `a27608bdd9de` | the 13v waiver paragraph replaced by the split record (waiver **SPENT**, and stated so); the SN-029 delegated-approval argument **kept verbatim in substance** — it is this row's content |
| SR-140 | `status` | `Approved` → `Modified` | **RIDE 1**, inherent to the split: the row's own text moved, so the row flips |
| SR-178 | *(mint)* | — | clause 2 — report text moved away from the record **regardless of Status movement**, needs included |
| SR-179 | *(mint)* | — | clause 3 — refuse a copy not byte-identical to live **in the commit that writes it** |

**Chain re-parenting, per obligation:**

| Child | before | after | why |
|---|---|---|---|
| LLR-158 `sr_refs` | `e9a500af65b1` `["SR-140"]` | `37ca9c1e4145` `["SR-178"]` | it IS the comparison basis — the drift rule's mechanism |
| TC-153 `verifies` | `d1f4e6c057f7` | `0a115acdfd65` | follows LLR-158; its four cases are the drift split's corners |
| TC-153 `expected` | `9c7e27617155` | `d2cc6eaf8b3c` | re-pointed SR-140 → SR-178 |
| LLR-173 / TC-167 | — | stay on SR-140 | they are the RECORD's design and test |
| LLR-173 `detail` | `8ed63a6a39ed` → `79e2e0b35786` | sibling pointers re-aimed at SR-178/SR-179 and LLR-178; no mechanism claim changed |
| TC-167 `method` | `d3adaf330ec0` → `4f01a12b77bd` | mirror-invariant clause **moved** to TC-173 rather than covered twice; remaining clauses re-lettered |
| LLR-178 / TC-173 | *(mint)* | → SR-179 | the refusal's real home is `check_trajectory.staged_snapshot_findings`, a different module from LLR-173's. Minted so the obligation keeps a chain instead of becoming an undecomposed draft |

**TC-173's evidence is function-granular** (six named tests, all verified to
exist), deliberately: the SR-040 finding below is what a file-granular evidence
cell costs.

**Gating consequence:** `trace.py --strict` **exits 0** — the form finding
that gated the `traceability` step is gone and signing now greens the step.

## B. `SR-173` — truth-matched from code (directive item 2)

| Cell | old → new | Justification |
|---|---|---|
| `title` | `f5141015dcf4` → `3302549a9287` | "leaves no partial result" → "commits no partial result" |
| `requirement` | `f53da721e68e` → `c729759c3483` | "leaving no partially regenerated set BEHIND" → "committing no partially regenerated set" |
| `acceptance_criteria` | `3ae098385afa` → `85e924988013` | **strengthened**: adds "runs no later family" and "moves the recorded history not at all", and states the working-tree residue as by-design |
| `rationale` | `cb7868dde0e6` → `761abd8ca4d5` | carries the adjudication and its evidence |

**This is truth-matching, not weakening, and the evidence is decisive.** The
regen step touches git **not at all**, so on a first failure it exits nonzero
having run no later step, with HEAD unmoved and nothing committed — and it
**deliberately leaves** the already-green steps' output dirty in the working
tree, because the design assigns the commit to the caller (LLR-142: *"never
commits; the caller owns the commit"*). `TC-170`'s own evidence test asserts
`git status --porcelain` is **NON-EMPTY** after the failure, so an
implementation that cleaned up after itself would **FAIL** the test that holds
this row. "Behind" therefore claimed something the system does not do and is
tested *not* to do. The transactional rollback a reader might infer from
"behind" is real but belongs to the **wrapping callers** (the integrator and
intake each reset the branch to its last work commit on failure); stating it
here would have credited this row with a guarantee a bare invocation does not
provide.

## C. `SR-150` — the acceptance-form holdout (directive item 3)

| Cell | old → new | What changed |
|---|---|---|
| `acceptance_criteria` | `ed8efc61bc26` → `866004f68167` | `check_need_form.py` re-voiced behaviorally; `--strict` → "the declared strict mode"; each clause kept and two made sharper ("naming the row **and each offending phrase separately** rather than the row alone"; "that list **ships empty**") |
| `status` | `Approved` → `Modified` | **RIDE 2**, the sanctioned one this pass was told to take |

Binding already exists at **LLR-170 / TC-164**, so this is a pure
carrier-naming drop — the same disposition the other 50 cells got. The form
pass is now **51 of 51 with no holdout**.

## D. `SR-040` — the tripwire, adjudicated (directive item 4)

**Verdict: NOTHING serves the obligation. Nothing was invented.**

| Row | Cell | old → new | What changed |
|---|---|---|---|
| SR-040 | `acceptance_criteria` | `2dee722294af` → `197ce689c93e` | the unsatisfiable clause ("a declared zero or negative threshold silences the warning") replaced by a stated **fit criterion explicitly marked as not a discharge** |
| SR-040 | `rationale` | `de0e9bb87e15` → `27f60ce273ac` | gains the retirement record, the refused substitute and its evidence, and the two dispositions left to the sitting |
| LLR-037 | `title` | `9f8f3c9feaa8` → `50209b97a89c` | "+ size tripwire" dropped — the module has none |
| LLR-037 | `code_symbol` | `ff2ab2c944c3` → `ae2a74ff1a43` | `status_size_warning` (**deleted symbol**) → `parse_map/read_declared` (both live) |
| LLR-037 | `detail` | `3de37567ff1d` → `e455aeae8116` | the phantom mechanism's description removed; the absence stated rather than papered over |
| LLR-037 | `status` | `Approved` → `Modified` | **RIDE 3** — an `Approved` design row was publishing a deleted symbol into the generated knowledge bundle |
| TC-040 | `method` | `f0a094b4e405` → `1cd0367c5521` | the clause "a bloated status.md warns without blocking" **struck — no test in its evidence file performs it** |
| TC-040 | `expected` | `99f18ab0af7f` → `fa9893e20c35` | states the tripwire clause is unverified BY CONSTRUCTION, having no carrier |
| TC-040 | `evidence` | `34670079c539` → `0ee4169f05b1` | file-granular (`tests/test_agent_loop.py`, 63 tests) → **three named functions**, all verified to exist |
| TC-040 | `status` | `Approved` → `Modified` | **RIDE 4** — it was `Approved` while claiming a test that does not exist |

**Why the live look-alike was REFUSED rather than adopted.** `check_docs`'
status line-budget warn is the only live "surface exceeds a declared threshold"
warner in the tree, and it is a **different obligation**, not a partial serve:

| axis | SR-040 demands | the look-alike delivers |
|---|---|---|
| actor | the **delivered coordinator** (the row's own subject) | a documentation checker |
| moment | run start / mid-run, unattended | the commit and gate bar |
| surface | the **lane resume surface** a resuming session inherits | `docs/status.md` as lean prose for a human reviewer — the "human noticing" C-UNA-8 calls the wrong mechanism |
| ownership | this row | already the carrier of **another** requirement |
| threshold | "a declared zero or negative threshold **silences** the warning" | a declared `0`/`-1` makes it warn on **every non-empty file**; only `off` silences |

The threshold inversion was **measured, not read off the source** — the
function was exercised on declared values `0`, `-1`, `off` and `200`. Adopting
it would have been carrier substitution across a different requirement,
component, actor and moment, with inverted semantics.

**Correction to the sweep that produced this finding, recorded because it was
mine to check:** the investigation also flagged `parse_map` as undefined in the
declared module. It is **live** — re-exported at `agent_loop.py:231` from
`agent_common` — so it stays named in LLR-037. Only `status_size_warning` was
the phantom.

**This is the one residue the sitting must still rule**, and it is a ruling,
not work: rebuild the tripwire in the coordinator against the *current* resume
surface, or strike the clause and answer its two hat lenses elsewhere.
