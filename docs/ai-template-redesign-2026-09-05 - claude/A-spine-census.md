# Appendix A — spine census: promises versus mechanism

Produced 2026-09-05 by a research agent over `docs/requirements/*.toml` and
`docs/test/test-cases.toml` at trunk `a9bf6cee`, with a stdlib script. `-000`
example rows dropped. Counts: 27 SN, 76 SR, 192 LLR, 191 TC, 167 IF.
Traversal: LLR→`sr_refs`→SR→`sn_refs`→SN; TC→`verifies`; IF→owner/consumer
module→LLR. Every LLR and TC reaches an SN; every IF reaches an LLR.

Classes used throughout: **(a) VISION-BEARING** — an adopter needs it for a
traced, gated, trustworthy process; **(b) LOOP-MECHANISM** — the unattended
multi-agent loop; **(c) SELF-DESCRIPTION / ACCIDENT** — internal detail,
historical fix, migration, repo convention, ratchet or rendering detail whose
absence fails no need; **(d) DASHBOARD / RENDERING**.

## A.1 Per-SN rollup (membership counts; an LLR reaching three SNs counts under all three)

| SN | Pri | gist | SR | LLR | TC | IF |
|---|---|---|---:|---:|---:|---:|
| SN-001 | M | Drop process into any repo, working immediately | 8 | 7 | 6 | 8 |
| SN-002 | M | Need→requirement→design→test verified, no orphans | 8 | 41 | 39 | 76 |
| SN-003 | M | Stack-agnostic; adopt by re-pointing declaration | 5 | 5 | 6 | 29 |
| SN-004 | M | Advance only through explicit approval gates | 7 | 16 | 16 | 43 |
| SN-005 | M | Agents and humans share one enforced playbook | 6 | 11 | 10 | 21 |
| SN-006 | S | Agent runs unattended, resumes from repo text | 10 | 39 | 36 | 70 |
| SN-007 | M | Kit holds itself to its own standard | 7 | 6 | 7 | 4 |
| SN-008 | M | Pass verdict never hides skip, stub, unmeasured | 11 | 41 | 41 | 87 |
| SN-009 | M | Secrets and private identity caught before publish | 5 | 7 | 7 | 14 |
| SN-010 | S | Docs navigable and honest; links resolve | 8 | 36 | 34 | 84 |
| SN-011 | M | Clean Python 3.11+, minimal argued dependencies | 3 | 1 | 4 | 1 |
| SN-012 | S | Right-sized process; small changes stay small | 10 | 40 | 39 | 77 |
| SN-023 | S | One dashboard shows progress and connections | 6 | 40 | 40 | 36 |
| SN-024 | S | Subjective/perceptual acceptance judged trustworthily | 5 | 39 | 38 | 41 |
| SN-025 | S | Configured LLM implements toward vision unaided | 7 | 44 | 42 | 95 |
| SN-026 | S | Owner configures several LLM families per job | 3 | 18 | 17 | 34 |
| SN-027 | S | Ready work fans out across parallel lanes | 5 | 26 | 24 | 64 |
| SN-028 | S | Every policy dial in one hand-edited file | 2 | 2 | 3 | 9 |
| SN-029 | S | Run goes as far as honestly possible | 6 | 24 | 23 | 48 |
| SN-033 | S | Each need reads as a stakeholder outcome | 1 | 1 | 1 | 2 |
| SN-034 | S | Two universal contributor actions, one command | 1 | 1 | 1 | 0 |
| SN-035 | C | One launcher lists the repo's actions | 1 | 1 | 1 | 4 |
| SN-036 | S | Needs examined from every expert perspective | 1 | 2 | 2 | 4 |
| SN-037 | M | See where each behavior crosses the boundary | 1 | 1 | 1 | 15 |
| SN-038 | M | Know why every kit-supplied file exists | 1 | 2 | 3 | 12 |
| SN-039 | S | Tell whether a need applies to template | 1 | 1 | 1 | 15 |
| SN-040 | S | Repeatable explanation of the partition | 1 | 1 | 1 | 15 |

**Fractional mass** (each LLR's weight split equally across the SNs it reaches;
sums to 192): SN-023 dashboard 21.5 · SN-012 right-sized 16.5 · SN-006
unattended 16.1 · SN-024 perceptual 15.8 · SN-002 traceability 14.6 · SN-010
docs 13.6 · SN-008 no-false-green 13.4 · SN-025 autonomous 12.9 · SN-029 honest
stop 10.8 · SN-027 lanes 9.8 · SN-004 gates 6.9 · SN-005 6.6 · SN-026 5.8 ·
SN-009 5.5 · SN-001 4.5 · the other twelve ≤3.5 each.

The top four (dashboard, right-sizing, unattended agent, perceptual
acceptance) carry 70 of 192 LLRs (36%). With the loop's three needs
(SN-025/027/029) it is 104 of 192 (54%). The four founding Must needs of the
vision statement (SN-002, SN-004, SN-008, SN-003) carry 38.7 (20%). The eight
late SNs (SN-033..040) carry ten LLRs between them but 67 IF memberships.

## A.2 LLR classification (192 rows, read from the `detail` cell)

| Class | Count | % | Kit SLOC in modules where the class dominates |
|---|---:|---:|---:|
| (a) VISION-BEARING | 47 | 24% | 14,929 |
| (b) LOOP-MECHANISM | 63 | 33% | 22,356 |
| (c) SELF-DESCRIPTION / ACCIDENT | 44 | 23% | 12,623 |
| (d) DASHBOARD / RENDERING | 38 | 20% | 8,334 |

Line-drawing notes: (d) is the renderer family (`gen_trajectory`, `traj_*`,
`gen_open_items`, `gen_arch_map`); `gen_okf` and `gen_components` fell to (c)
(moving them makes (d) 40 / (c) 42). LLR-021 (hook Python probe) kept in (a):
genuine cross-platform survival. LLR-034 (WI DAG validation) kept in (a): the
registry exists without the loop.

### The 44 (c) rows

| Id | Module | Reason |
|---|---|---|
| LLR-004 | trace_text | warn-only wording advisory; gates nothing |
| LLR-013 | check_flows | one repo's authored flow-doc format |
| LLR-015 | trace | verbatim restatement of LLR-005 clause |
| LLR-022 | check_vendored | vendored-copy drift, kit-internal convention |
| LLR-024 | gen_cases | opt-in permutation grammar, unused layer |
| LLR-025 | gen_skills_index | regenerates the kit's own skills index |
| LLR-031 | check_privacy | one-line config-parse helper extraction |
| LLR-039 | gen_okf | typed-concept export nobody gates on |
| LLR-043 | gen_skills_index | byte-syncs skill copies between agent dirs |
| LLR-047 | run_menu | actions-menu launcher; convenience, not process |
| LLR-049 | check_trajectory | top-view size ratchet on module count |
| LLR-050 | spine_rules | records content this row's mechanism lost |
| LLR-060 | trunk_step | retirement record for deleted surfaces |
| LLR-068 | check_trajectory | repo-specific spec-file section convention |
| LLR-075 | check_trajectory | forward-only status.md, a repo convention |
| LLR-083 | trace | widens one enum to accept Critique |
| LLR-084 | check_trajectory | warn-only ratchet on critique closes |
| LLR-097 | check_trajectory | repo spec-lifecycle bookkeeping findings |
| LLR-124 | trunk_step | generated status block; trunk-lane convention |
| LLR-135 | trace_text | warn-only paraphrase advisory, never gates |
| LLR-136 | wi_convert | converter for a retired CSV home |
| LLR-146 | check_figures | opt-in figure-provenance marker convention |
| LLR-147 | spine_rules | narrowing record after a deleted function |
| LLR-156 | bootstrap | legacy dial converter, migration window |
| LLR-164 | gen_prompt_catalog | generated catalogue of the kit's prompts |
| LLR-165 | migrate_carrier | one-time markdown/CSV to TOML migrator |
| LLR-169 | check_vocab | enforces retired vocabulary; migration ratchet |
| LLR-172 | check_trajectory | partition-argument record nothing consumes |
| LLR-176 | plan_briefs | pins today's convention until surface exists |
| LLR-179 | trace_text | warn-only EARS advisory, never gates |
| LLR-181 | kitlib/* | internal shared-helper package extraction |
| LLR-183 | check_trajectory | perspective cell plumbing; optional roster layer |
| LLR-184 | kitlib/ladder | stage vocabulary re-homed into kitlib |
| LLR-185 | kitlib/stage | carrier extraction siting under LLR-186 |
| LLR-194 | trace | seam described as not-yet-extended |
| LLR-195 | check_dupes_census | duplicate-body census, warn-first forever |
| LLR-197 | kitlib/spine | row vocabulary re-homed into kitlib |
| LLR-198 | pending; traj_status | read model plus compatibility shim |
| LLR-199 | gen_components | derived component view, optional surface |
| LLR-201 | coherence | re-sites LLR-001 rules into module |
| LLR-202 | acceptance_record | Hat-Refs arm of an optional layer |
| LLR-205 | kitlib/secret_classes | secret-class vocabulary re-homed into kitlib |
| LLR-206 | check_complexity | complexity/SLOC ratchet against a baseline |
| LLR-209 | derive_stage | repo authoring rule about off-phase tags |

Three sub-patterns account for most of (c): **six rows describe their own
retirement or narrowing** (LLR-050's title literally reads "The gate-axis
computation this row named is retired"); **eight rows are pure code-siting**
("this vocabulary now lives in kitlib/"); **one outright duplicate** (LLR-005
and LLR-015 state the same PB-Refs rule on the same module, each with its own
TC, and the registry documents the split as deliberate).

## A.3 TC classification (191 rows; inherit the parent LLR's class)

| Class | TCs | % |
|---|---:|---:|
| (a) VISION-BEARING | 51 | 27% |
| (b) LOOP-MECHANISM | 60 | 31% |
| (c) SELF-DESCRIPTION / ACCIDENT | 43 | 23% |
| (d) DASHBOARD / RENDERING | 37 | 19% |

Shape: 111 Integration / 75 Unit / 3 Analysis / 1 Inspection / 1 Critique;
141 Full-tier vs 50 Smoke; 189 automated.

**27 of 191 (14%) assert something an adopter would observe** — a fresh
scaffold's harness runs green (TC-010), a re-run leaves files unchanged
(TC-011), a staged secret blocks the commit (TC-017/019), a secret in the push
range blocks the push (TC-020), a missing tool fails the gate (TC-006/008), a
stub fails (TC-016), a broken link fails (TC-012), onboard/dev-setup reach
green (TC-032), the CI matrix passes on three OSes (TC-035), a non-Python
scaffold passes trace unmodified (TC-165), the launcher picks a usable
interpreter (TC-188), the CI verdict IS the harness exit (TC-186), the
dashboard generates (TC-038). **The other 164 (86%) test the kit's tooling
against its own fixtures** ("run the X suite; a malformed Y is a finding";
"fixture-drive the rung"). The 191 TCs sit atop 59,966 SLOC across 151 test
modules — larger than the 58,242 SLOC of kit scripts they test.

## A.4 Module footprint

All 82 scripts carry at least one LLR; none carries zero. The LLR tier is
functioning as a per-module inventory.

| LLRs | a | b | c | d | Module |
|---:|---:|---:|---:|---:|---|
| 17 | 0 | 0 | 0 | 17 | traj_render |
| 15 | 0 | 0 | 0 | 15 | gen_trajectory |
| 13 | 5 | 1 | 7 | 0 | check_trajectory |
| 11 | 0 | 11 | 0 | 0 | agent_loop |
| 10 | 6 | 0 | 4 | 0 | trace |
| 8 | 0 | 0 | 0 | 8 | traj_views |
| 7 | 0 | 0 | 0 | 7 | traj_panels |
| 7 | 0 | 7 | 0 | 0 | schedule |
| 7 | 1 | 6 | 0 | 0 | agent_common |
| 6 | 5 | 0 | 1 | 0 | bootstrap |
| 5 | 2 | 0 | 3 | 0 | trace_text |
| 4 | 3 | 1 | 0 | 0 | check |
| 4 | 0 | 0 | 0 | 4 | traj_parse |
| 4 | 2 | 0 | 0 | 2 | gen_arch_map |
| 4 | 0 | 2 | 2 | 0 | trunk_step |

The dashboard renderer family carries 53 LLR namings — more than trace, check,
bootstrap and the hooks combined (22). Twenty-two of those (LLR-099..LLR-120)
are one row per rubric anchor per residue ("the mechanized core of usability
anchor T2"), each with a TC sweeping every emitter for a CSS token, a ΔE floor
or a WCAG ratio.

## A.5 Interfaces (167 rows)

| Class | Rows | Channels |
|---|---:|---|
| Intra-kit, code↔code | **96 (57%)** | 72 call, 16 exit-code, 4 stdout, 2 cli, 2 file |
| Crosses the boundary (adopter, git, agent CLI, launchers) | **52 (31%)** | 29 file, 8 exit-code, 6 cli, 5 stdout, 2 git, 2 bytes |
| Kit code ↔ a repo file (registries, stack.ini, docs/work) | 19 (11%) | 14 file, 3 exit-code, 2 bytes |

- The 96 intra-kit rows have 40 distinct owners; the 72 `call` rows have 28.
  `spine_carrier` alone owns 19 separate `call` rows — the same API, one row
  per importing module. `trace` (7), `check_trajectory` (6), `gen_arch_map`
  (6), `schedule` (5), `prompts` (5), `baseline_snapshot` (4) repeat it.
- Collapsed to (owner, channel) the registry is 104 distinct pairs, so about
  63 rows are additional consumers of a surface already declared.
- `verified_by` is documented at length and set zero times. Eight TCs cite an
  IF id at all, naming 16 seams; the other 151 have no test that names them.
- 22 rows use `carried_by` (constituents of a bundle another row declares).

The 52 boundary-crossing rows are the load-bearing half and are what SN-037
asks for. The 96 intra-kit rows are an import graph transcribed into a
requirements registry, taxed on every import edit by `check_trajectory
--strict`, for information `gen_arch_map`'s AST scan already derives.

## A.6 The agent's assessment

1. The vision's floor is small and healthy: trace + check + bootstrap + the two
   hooks + check_privacy + check_docs + derive_stage/spine_rules +
   check_coverage/check_stubs — about 40 of the 47 (a) rows — is the whole
   "traced, gated, trustworthy, stack-agnostic" promise.
2. Half the spine is the loop (63 LLR, 60 TC, ~22k SLOC). Deliberate, but it
   should be one optional layer, not diffused through the tier that carries
   the traceability floor.
3. The dashboard is over-decomposed by an order of magnitude (40 LLR / 40 TC
   for "one dashboard-like file").
4. SN-024 (perceptual acceptance) is a process invention with 39 LLRs serving
   a need no adopter has asked for.
5. The 44 (c) rows would not be re-authored; a rebuild starts without them
   and nothing breaks.
6. The registries track the code, not the requirements: every script has an
   LLR; 19 IF rows for one module's API; `verified_by` unused.
7. The TC tier tests checkers, not outcomes — 164 of 191.

**On the six candidate SNs:** SN-023 keep the need, delete the acceptance
clause that mandates the interface graph (it dragged in the IF registry, the
arch-map, component derivation and 40 LLRs). SN-035 harmless accretion, one
row each tier. SN-037 the best value-per-row need in the registry; keep.
SN-040 legitimate need, write-only mechanism (LLR-172's record is consumed by
nothing); replace the checker with a prose section. SN-026 not accretion but a
sub-need of SN-025. **SN-027 (parallel lanes) is the most defensible cut: 26
LLR / 24 TC / 64 IF memberships buy throughput, not trust, and every gate
works identically at one lane.** SN-027 and SN-024 together free 65 LLRs and
62 TCs at the least cost to the vision; independently of any SN decision, the
44 (c) rows and ~63 redundant intra-kit IF rows are deletable today without
touching a single need.
