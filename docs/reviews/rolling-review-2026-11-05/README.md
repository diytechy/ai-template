# Rolling review — 2026-11-05 — maintenance & sustainability

**Scope (owner request):** a deep review of the kit with maintenance and
sustainability as the lens. Four questions drive every finding:

1. Where does code duplicate behaviour that could be consolidated?
2. Where can the architecture-related skills and prose be improved?
3. Where can the requirement → implementation spine be improved, so that
   requirements and tests sit as close to the end user as possible — not at
   implementation altitude, and not testing other test infrastructure?
4. Where does the kit guard against contrived cases that should just warn?

**Method:** findings are appended as the investigation proceeds and committed
to `rolling_review` after each pass, so partial progress survives a usage
limit. Each finding carries a severity (`[HIGH]`/`[MED]`/`[LOW]`), an anchor
(file or rule), the issue, and a concrete change. Measurements are reproduced
with the command that produced them.

**Status:** second pass COMPLETE (2026-11-05, same day); every section
verified. The first full pass is §1–§7; the
second pass adds §8–§14: the growth trend, the adopter's first day, external
research, a re-tier exemplar, the adversarial verification of §1–§6 (§12), six
finders' new findings with their own verification (§13), and the revised,
ruling-positioned recommendations (§14). `measure.py` reproduces the first-pass
numbers, `trend.py` the §8 table, `exemplar/compare.py` §11, and `measures/`
the §13 figures. **Read §14 first; §12 and §13's verification blocks say what to
trust in §1–§7 and §13.** Audit
commits on this branch bypass the commit floor (`--no-verify`) at the owner's
direction (2026-11-05): §6.1 and §6.4 record why the floor refused them.

---

## 0. Orientation measurements (reproduced 2026-11-05)

```
wc -l project-trajectory/scripts/*.py            ->  98,627 lines, 116 files
wc -l project-trajectory/scripts/kitlib/*.py     ->  12,747 lines,  25 files
wc -l tests/*.py                                 -> 157,218 lines, 281 files
wc -c project-trajectory/PROCESS.md              ->  98,912 bytes
wc -c project-trajectory/PROCESS_OPTIONS.md      -> 199,478 bytes
wc -c project-trajectory/README.md               ->  93,389 bytes
wc -c project-trajectory/RESYNC_PACK.md          -> 643,982 bytes
wc -c project-trajectory/skills/*/SKILL.md       -> 144,330 bytes, 33 skills
registries: SN 31 (+4 STK; the first pass printed 35), SR 138, LLR 331, TC 363, IF 255, OI 120
```

These numbers are the headline finding on their own (see §1). Re-derive them
with `python docs/reviews/rolling-review-2026-11-05/measure.py`.

---

## 1. Findings — size and surface area

**[HIGH] 1.1 The kit is no longer a kit; it is a platform.** 111k lines of
Python (98.6k scripts + 12.7k `kitlib`), 157k lines of tests across 281 test
modules, and ~1.2 MB of shipped Markdown (PROCESS 99 KB, PROCESS_OPTIONS 199 KB,
README 93 KB, RESYNC_PACK 644 KB, 33 skills 144 KB, 19 prompts 140 KB). An
adopter receives 211 files from the bootstrap manifest, 115 of them `.py`. The
CLAUDE.md principle is "edit conservatively — this is a foundation many
projects inherit"; a foundation this size cannot be read by the people who
inherit it, and every downstream re-sync (RESYNC_PACK is 303 sections) carries
all of it. *Change:* see §7.1 (split the kit into a small core and opt-in
layers that ship as separate directories, each with its own manifest).

**[HIGH] 1.2 The unattended station is half the code, and it is not the
product's purpose.** Partitioning the scripts by subsystem (reproduced with the
tokenizer script in this review's log):

```
51,647 lines  50 files  unattended station & coordination (agent_loop, dispatch,
                        integrate, intake, session_*, coordinator_*, adjudicate_*,
                        handback, schedule, plan_*, hats, consolidate, ...)
26,368 lines  26 files  spine checks & trace (trace, check, check_trajectory, ...)
12,536 lines  32 files  kitlib + misc
12,409 lines  16 files  dashboard & generators
 3,961 lines   3 files  bootstrap / run menu
```

58 of 138 SRs and 101 of 331 LLRs are about the loop/lane/coordinator/adjudication
machinery. The vision tag is "maintainable and trustworthy downstream code";
the station is a *way of operating* the process, and PROCESS_OPTIONS already
classes it as opt-in ("Unattended operation (walk-away runs)", 500 lines).
The code does not follow that classification: `check.py` registers its steps
(`ruling-sync`, `text-then-act`, `held-status`, `done-when-blessed`,
`plan-gate`, `adoption-record`, ...) in the one floor every adopter runs.
*Change:* make the station a separately shipped layer with its own
`check.py` step registration (a `[step:...]`-style plug-in), so an adopter who
never runs an unattended loop never carries, reads or re-syncs it.

**[HIGH] 1.3 Comment-to-code ratio 0.82, and the comments are history.** 48.4k
comment/docstring lines against 58.8k code lines. 1,842 `WI-###` citations sit
in script comments (155 in `check_trajectory.py` alone), plus hundreds of
"owner ruling 2026-…" stamps. The kit's own rule (`AGENTS.template.md`
"State the constraint, not its history" — "at most once per module, a header
pointer, never a per-site sprinkle") is violated in nearly every module. A
reader cannot tell which comment is the current contract and which is a
receipt for a fix that no longer matters. *Change:* a one-time sweep that keeps
the *reason* and drops the *frame* (the same rule the spine applies to
`Rationale` cells), then enforce the existing rule with the existing
`trace_text` citation-frame detector pointed at `*.py` docstrings, warn-only.

**[MED] 1.4 The pre-commit floor is 38 steps, 33 s wall on 4 cores, and 350 of
its 520 output lines are WARN.** Measured 2026-11-05 on this clone. A floor
whose output is two-thirds warnings trains every reader to ignore it; the one
line that matters (`FAIL approval-fresh`) is invisible at that density. The
`trajectory` step alone is 27 s. *Change:* print WARN counts per step with the
first line of each class, and the full list only under `--verbose`; move the
long-running dashboard regeneration (`trajectory-map`, 18 s) out of the commit
floor to the merge slot (it is already trunk-only by rule).

**[MED] 1.5 The docs record is 85 MB of the 121 MB working tree.**
`docs/iteration` 46 MB, `docs/reviews` 16 MB, `docs/archive` 12 MB,
`docs/plans` 6 MB; 4,785 of 5,451 tracked files are under `docs/`. Every grep,
every agent context load, every clone pays for review transcripts and
superseded plans that no gate reads. *Change:* move `docs/iteration`,
`docs/reviews/*/` round files and `docs/archive` to a records branch or a
sibling repo, leaving a one-line index; the kit's own rule already names these
"records rather than navigation".

**[LOW] 1.6 17 of 33 shipped skills are domain-specific** (ros2, gaussian-splat,
urdf, sim2real, webgpu, lerobot, ...). They are gated by `--domain`, but they
are maintained, indexed and re-synced with the process kit. *Change:* ship them
as a separate `skills-domain/` pack with its own INDEX, or drop them.

**[MED] 1.7 A quarter of recent commits are bookkeeping.** Of the last 400
commits on this branch, 105 (26%) have subjects `claim:`/`pause:`/`unpause`
("pause: restored byte-identical after claiming WI-983 (sha256 checked
against the copy taken before the unpause)"), 38 are `mint:`, 20 `file:`,
130 `docs:`, and 80 carry a `WI-###` subject. 717 commits landed in the last
30 days (~24/day; 4,680 since 2026-06-04). A claim is three commits
(unpause, claim, re-pause) because the pause is a presence-as-semantics file
and the claim must be its own commit. The record is honest; it is also noise
that every `git log`, bisect and review has to read past. *Change:* the pause
and claim become rows in one hand-edited file (`docs/work/station.toml`) and
a claim is one commit; or keep the ritual but squash the three into one with
a trailer.

## 2. Findings — code duplication / consolidation candidates

**[HIGH] 2.1 Duplicated POLICY is licensed by 2,300 lines of equality tests
instead of removed.** `tests/test_rule_sync.py` (1,784 lines) and
`tests/test_wi_loader_sync.py` (555) exist to pin that copies of a decision
agree by value. Their own docstrings record that the F5 ruling ("each script
independently copy-able") which justified the copies was superseded (D-8), that
`kitlib` now exists, and that most of the pinned pairs have since been folded
into it — so much of each file is now prose explaining which tests used to be
there. Verified 2026-11-05: the spec-folder reader IS consolidated
(`kitlib.registry.read_spec_rows`, re-exported by `schedule.py` and
`check_trajectory.py`), but the per-row normaliser still has two copies
(`schedule.load_wis` 45 lines, `check_trajectory.load_wis` 58 lines) and the
converter-fidelity and four-way equivalence batteries remain. The 0→A→B rule
in PROCESS §3 says extract the shared stage; a test that pins two copies equal
is the cost of not doing so, paid on every run. *Change:* one `load_wis` in
`kitlib.registry`; delete both sync modules, keeping only the value batteries
that test behaviour (a dozen cases).

**[MED] 2.2 Six git wrappers.** `kitlib.git.git_out`, `agent_common.git`,
`check_privacy.git`, `bookkeeping._git`, `derive_stage._git`, `traj_parse._git`
each run `git -C root …` with slightly different strip/stderr/stdin rules, and
`derive_stage._git` documents itself as "a four-line wrapper over
`kitlib.git.git_out` rather than a call to it" because the strip matters. One
wrapper with `strip=` and `stderr=` keyword arguments replaces all six.

**[MED] 2.3 Two ratchet implementations.** `check_complexity.py` and
`flag_axis.py` each carry `census`/`read_baseline`/`write_baseline`/
`compare`/`_report` over a TSV baseline with `#` comment lines. The test-side
siblings `test_module_size_ratchet.py` (2,098 lines) and
`test_complexity_ratchet.py` (471) carry baselines as Python dict literals, a
third representation. *Change:* one `kitlib.ratchet` (TSV baseline read/write,
compare, report) parameterised by the measure; the two test ratchets become
rows of `docs/complexity-baseline`, not test code.

**[MED] 2.4 The checker CLI shell is written 20+ times.** `check_vocab`,
`check_need_form`, `check_figures`, `check_doc_refs`, `check_stubs`,
`check_flows`, … each hand-roll `--root`, `--strict`, the "WARN vs ERROR"
label, the "(warn-first; --strict gates)" suffix and the `return 1 if strict
else 0` exit. 61 scripts use argparse, 51 declare `--root`. `kitlib.config`
has `utf8_console` but no CLI shell. *Change:* `kitlib.cli.checker(name,
scan_fn)` that owns the flags, labelling and exit code; each checker becomes
its `scan()`.

**[MED] 2.5 94 function names are defined in more than one module**
(`render` ×8, `parse` ×6, `_cell` ×5, `_report` ×5, `_clip` ×4, `evaluate`
×4, `render_report` ×4, `read_rows`/`load_csv`/`load_registry_rows`/`load_wis`
…). Not every one is a semantic duplicate, but `_clip` (4), `slugify` (2),
`esc` (2), `_id_number` (3), `load_csv` (3) are. The retired duplication census
(`check_dupes_census.py`, "WARN-ONLY FOREVER") was torn down for being
"structurally blind to a diverged copy"; the AST name census above took 20
lines and finds the diverged copies. *Change:* run it as a warn-only step.

**[LOW] 2.6 `check.py` and `integrate.py` each carry `_ruling_sync_refusal`
and `_text_then_act_refusal`.** The walk itself is shared
(`kitlib.git.lane_commit_walk`, used by `integrate._each_lane_commit`); what is
duplicated is the pair of refusal composers and their 20-line docstrings, which
differ only in "staged tree" vs "each lane commit". One composer taking the
tree source would do.

**[LOW] 2.7 Interface contract prose lives at 357 files.** 223 `Contract
IF-###:` bodies, ~199 KB, sit in file headers while the registry row holds
only `owner`/`data`. The rule ("stated at the owner, row of record in the
registry") is sound, but the header also restates the row's `data` list and the
process-doc citation on every file. *Change:* keep the one-paragraph contract at
the owner; drop the boilerplate frame ("the interface seam this module declares
(process.md §8; row of record in …)") that is identical on all 357 — a
generated banner, not prose.

## 3. Findings — architecture skills and prose

**[MED] 3.1 Architecture is described in seven homes.** PROCESS §3 (derived
map, thin orchestrators, flows), PROCESS §8 (seams), PROCESS_OPTIONS
"Intra-repo interfaces & the architecture graph" and "Component layer",
`AGENTS.template.md` "Code we want", the `architecture-decomposition` skill,
`docs/rubrics/architecture-decomposition.md`, and `deep-module-design`. The
skill and rubric are good (short, cite anchors by id, Parnas/SCR grounding);
the surrounding prose repeats them. *Change:* PROCESS §3 keeps only the
three invariants (derived map; authored flows; one home per behaviour) and
points at the rubric for the decomposition bar.

**[MED] 3.2 The component registry is nearly empty while the interface
registry is huge.** `components.toml` has 4 rows, `components.derived.toml` 6,
`interfaces.toml` 255. An architecture with 4 components and 255 interfaces is
an interface list, not a decomposition; the rubric's own anchors (A1: each
boundary hides a decision; "more components is not better") would score this
scope badly. The derived import graph (`test_import_layers.py` docstring: "not
layered services but ONE cycle") agrees. *Change:* run the kit's own
architecture-decomposition procedure on the kit; the first result is probably
the §1.2 split.

**[MED] 3.3 The shipped skills restate each other and cite this repo's
history.** `session-protocol`, `coordinator-cycle` (33 KB) and `gate-advance`
each describe the commit bar and smoke tier; `coordinator-cycle` carries 6
owner-ruling stamps and 6 WI citations, `session-protocol` 10 WI citations.
A downstream reader cannot follow a `WI-926` citation (CLAUDE.md: "a marker
naming one of this repo's own rulings cites a record they can never read").
*Change:* strip provenance from every `scope: kit` skill; `coordinator-cycle`
is `scope: this-repo` in substance and should be marked so.

**[LOW] 3.4 PROCESS_OPTIONS.md is 199 KB with 34 top-level layers**, each
with an *applies-when*. That is the right shape, but at this size the index
is the only part anyone reads. *Change:* one file per layer under
`process-options/`, the index stays; the resync pack can then address a layer
by file.

## 4. Findings — the spine: altitude of SN/SR/LLR/TC

**[HIGH] 4.1 LLR `detail` is code documentation, not a design expectation.**
252 of 331 LLR details contain code identifiers or filenames; the median is
759 characters; 58 exceed 1,500 and 18 exceed 3,000; LLR-270 is 11,427
characters. LLR-254 reads "`observation_test_cases(root, rev)` reads
observation cases at a revision. `checkpoint_for(root, rev, tc)` returns…".
That is a module docstring copied into a registry row: it duplicates the
code, rots when the code is renamed (the hook already warns that LLR-298's
`CodeSymbol` claims 16 symbols the tag does not enclose), and gives a human
reviewer at DevStg-Tests nothing they could not read in the source. The
`spine-authoring` skill says "LLR = solution-specific by design", which is
right, but solution-specific means *naming the decomposition choice* (which
module owns the decision, what crosses the boundary), not transcribing
signatures. *Change:* cap LLR `detail` (warn at 600 chars), forbid
function-call syntax in `detail` (warn), and move the symbol list to the
`code_symbol` cell it already has. Downstream prose: in
`prompts/spine-questions.md` §3 add "an LLR names the module and the decision
it hides; it never lists functions".

**[HIGH] 4.2 Half the TC `expected` cells are vacuous.** 174 of 363 TCs open
with "Satisfies SR-xxx AcceptanceCriteria via the LLR-yyy detail contract" —
a pointer to the parent, which the `verifies` cell already is. Meanwhile the
`method` cell is a long test-procedure narrative (92 mention the suite,
conftest, pytest, a ratchet or a baseline) that duplicates the test
function's own docstring. The tier is carrying its content in the wrong cell.
*Change:* `expected` states the observable outcome in the end-user's words
(one sentence); `method` is the one-line instrument class ("pytest, the named
module"); the narrative lives in the test docstring, where it already is.

**[HIGH] 4.3 TC evidence is pinned to 2,124 pytest node ids.** `evidence`
cells name `tests/test_x.py::test_name` 2,124 times (215 TCs name more than
one). Every test rename is a registry edit; four node ids already point at
functions that no longer exist (TC-079 ×2, TC-194, TC-333 — the harness's
"`::node` selector" is a recorded accepted gap). The reverse link is nearly
unused: 6 of 269 test files carry `Implements: TC-` tags. The kit's own rule
(PROCESS §3) says test files name their TC on the same line and "the
registry rows are authoritative" — i.e. evidence should be *derived* from the
tags, not hand-typed. *Change:* evidence = file-level only (or derived from
`Implements:` tags by `check_trajectory`); delete the node ids.

**[MED] 4.4 SR acceptance criteria are test procedures.** Median 484 chars,
max 2,471; SR-199's AC enumerates seven record fields and three refusal
cases. The SR tier should state the capability and its observable condition;
the enumerated cases are the TC's. Rationale cells (median 730, max 3,209,
119 KB total) are longer than the requirements they justify (45 KB total).
*Change:* warn on AC > 400 chars and Rationale > 500 chars; the
`spine-questions.md` §2 text should say "an AC is one observable condition a
stakeholder could witness, not a case list".

**[MED] 4.5 The spine describes the kit's own machinery, not an adopter's
outcome.** SR keyword census: "report" 42, "commit" 26, "loop" 24, "session"
22, "refuse" 19, "lane" 17, "coordinator" 11. Only ~31 SNs exist and they are
well written (SN-042/043 are at the right altitude). The descent from 31 SNs
to 138 SRs to 331 LLRs to 363 TCs is where altitude is lost: SR-156 has 11
direct LLR children, SR-168 has 8 (the fan-out detector already fires). The
"right-sizing" paragraph in PROCESS §3 ("over-aggressive traceability is a
failure mode") is the correct doctrine and the kit's own spine does not
follow it. *Change:* the kit's own spine is the EXAMPLE every adopter copies
from; a one-time re-tier that collapses implementation-mirroring LLRs into
their SR (keeping `module` as the pointer) would halve the LLR count and is
the single most persuasive sustainability fix.

**[MED] 4.7 The authoring prose is right; the rows break it; no detector
closes the gap.** `prompts/spine-questions.md` §3 already says an LLR "names
no implementation carrier (a code file, function or symbol)" and that the
`module`/`code_symbol` cells are the trace homes. 252 of 331 LLR rows violate
that sentence. The SR tier has warn-only advisories for the same altitude
rule (artifact token, shared artifact, EARS opening, fan-out); the LLR tier
has only the lexical paraphrase advisory. A rule that is stated but never
reported is the "unbacked rule" the enforcement audit says to delete or back.
*Change:* an LLR identifier advisory in `trace_text` (the 20-line regex in
`measure.py` finds them), warn-only, listed in the report like the SR ones.

**[LOW] 4.6 `SN-001`…`SN-004` and `STK-*` share one table and the sampler has
to special-case them;** `stakeholder-needs.toml` holds 35 rows of which 31
are needs. Minor, but a reader counting needs gets the wrong number.

## 5. Findings — tests testing test infrastructure

**[HIGH] 5.1 34 test modules (12,959 lines) have the test suite, CI config or
this repo's layout as their subject**, not the kit's behaviour: `smoke_tier`,
`conftest_isolation`, `cpu_cap` (547 lines on the conftest's CPU cap),
`module_size_ratchet` (2,098), `complexity_ratchet` (471), `import_layers`
(618), `rule_sync` (1,784), `wi_loader_sync` (555), `dogfood_sync` (918),
`ci_tier_declaration` (463), `smoke_budget*` (337), `launcher_interpreter`
(555), `status_vocabulary_contract` (364), `generated_newlines` (396),
`hooks_on_census`/`hooks_on_routes` (491), `commit_floor_census`,
`generated_freshness_census`/`_wiring`, `kit_path_invariant`,
`dashboard_size_budget`, `meta_repo_hook`, `shell_portability`, … Each is a
guard about a guard. They are 8% of the suite by line count and a much larger
share of its brittleness (a baseline dict literal of every module's line count
must be re-stamped on every refactor). *Change:* each ratchet/census becomes
a warn-only `check.py` step reading a committed TSV (§2.3); each "X agrees
with Y" pin is replaced by removing the second copy (§2.1); each "the suite
is partitioned/marked correctly" test is replaced by a one-line pytest plugin
assertion in conftest.

**[LOW] 5.2 Tests pin the kit's message wording.** Measured: 724 of 18,491
`assert` statements (4%) compare against a string literal of 40+ characters,
spread over 116 of 269 test modules. The share is modest; the cost is that any
wording improvement to a refusal is a multi-module test edit, which is one
reason the 90-word warnings in §6.3 persist. *Change:* assert on a short
stable token or the first clause; keep wording free.

## 6. Findings — guards vs warnings (contrived cases)

**[HIGH] 6.1 A shallow clone makes the commit floor fail closed with a false
"integrity" finding.** Reproduced on this session's depth-50 clone: three
steps FAILED (`approval-fresh`, `registry-integrity`, `open-items`) with
"docs/archive/last_approved/…components.toml is NOT byte-identical to
…components.toml at 2909cc24, the commit that last wrote it — this divergence
has LANDED". After `git fetch --unshallow` all three PASS; nothing changed but
history depth. `git log -1 -- path` on a shallow clone returns the graft
boundary, which the check then treats as the writing commit. Shallow clones
are the default for GitHub Actions, Claude cloud sessions and most CI. The
kit *does* know about shallow history (`baseline_snapshot._shallow_commits`,
`acceptance_record`, `check_test_first`: "unreadable is never a pass") but
applies it inconsistently. *Change:* one `kitlib.git.is_shallow(root)`;
every history-dependent step reports "unverifiable: shallow clone" as a WARN
with the unshallow command, never as a landed-divergence FAIL.

**[MED] 6.2 Every agent route refuses to start if hooks are off** (`kitlib.
commit_hooks`, 8 call sites, 491 lines of tests). The stated threat is "a
fresh clone where setup was skipped". But the merge slot already re-checks
every lane commit precisely because hooks are opt-in and `--no-verify`
exists (`integrate.py:1338`). The refusal therefore guards a case the
downstream slot already closes, and costs every adopter a mandatory
`core.hooksPath` dance (this session hit it). *Change:* warn once at route
start ("hooks are off; the merge slot will judge your commits"), do not
refuse.

**[MED] 6.3 Hand-tuned bans with WARN-length prose.** The `hold-by-rename`
warning (~90 words, "a lane parked by renaming its ref is BANNED (OI-70)")
fires on this branch's own HEAD for two lanes. A rule whose violation is the
normal state of the trunk is either not a rule or not enforced; either way the
text should be one line. The same applies to the 350 WARN lines in §1.4.

**[MED] 6.4 The approval snapshot is byte-compared against the live file and
refuses the *commit* when a row's text differs.** `intake.py snapshot` must
re-copy on every post-approval amendment. This is the right record to keep
but the wrong place to gate: an unrelated commit (this review's first commit)
is refused for a divergence it did not create. *Change:* `approval-fresh` and
the snapshot drift check belong at the merge slot and the gate, not the
commit floor; at commit they warn.

**[LOW] 6.5 Typed-value refusals for dials.** `process.toml` documents that a
value of the wrong type is "refused at preflight", a `privacy_review` typo
"reads as require", a non-parsing file "reads ask". These are three different
failure policies for one file. One policy (refuse a non-parsing file; warn and
use the default for an unknown value) is easier to document and to test.

## 7. Recommendations, ordered by leverage

Each item names the findings it discharges and a rough size. "Size" is the
owner's reading time plus the change; none of these needs new dependencies.

1. **Re-tier the kit's own spine at LLR and TC (§4.1–4.5, §4.7).** The kit's
   spine is the example every adopter copies and every prompt is tuned on.
   Collapse implementation-mirroring LLRs into their SR (keep `module` as the
   pointer), rewrite `expected` as a one-sentence outcome, drop node ids from
   `evidence`, and ship the LLR identifier advisory so the regression is
   visible. Target: LLR 331 → ~150, TC `expected` 100% non-vacuous, evidence
   file-level. Size: large but mechanical; the briefs render the diff.
   This one change also shrinks `check_trajectory` output and the dashboard.

2. **Ship the station as a layer, not the core (§1.1, §1.2, §1.6).** Move the
   50 station modules, their `check.py` steps, prompts, and the 17 domain
   skills under `project-trajectory/layers/<name>/` with a per-layer manifest
   that bootstrap copies only on opt-in. The core that remains (spine
   checks, trace, hooks, dashboard, bootstrap: ~45k lines) is what "a
   reusable kit" promised. Size: a directory move plus manifest rows; the
   import-layer ratchet already describes the boundary.

3. **Turn the meta-tests into warn-only steps and delete the equality pins
   (§2.1, §2.3, §5.1).** ~13k test lines and 2.3k pin lines go; two
   `kitlib.ratchet` TSV baselines replace two dict literals. Size: medium;
   every deletion is covered by a step that still reports.

4. **One policy for history-dependent checks (§6.1, §6.4).** `is_shallow`
   once in `kitlib.git`; any check that reads "the commit that last wrote X"
   says *unverifiable* on a shallow clone. Move `approval-fresh` and the
   snapshot byte-compare from the commit floor to the merge slot. Size:
   small; it unblocks every CI and cloud session that clones at depth.

5. **Downgrade hooks-on from refusal to warning (§6.2).** The slot already
   judges every commit; the refusal only taxes fresh checkouts. Size: tiny
   code change, ~500 test lines retire.

6. **Strip provenance from code comments and shipped skills (§1.3, §3.3).**
   Keep the reason, drop the `WI-###`/"owner ruling <date>" frame, the same
   rule the spine already applies to `Rationale`. Point the existing
   citation-frame detector at docstrings, warn-only. Size: a sweep;
   reviewable in chunks per module.

7. **Quiet the floor (§1.4, §6.3).** WARN lines summarised per class with
   counts; full lists under `--verbose`; `trajectory-map` moves to the slot.
   Size: small.

8. **Move records out of the working tree (§1.5).** `docs/iteration`,
   `docs/reviews/*/` rounds and `docs/archive` to a records branch; a
   one-line index stays. Size: a `git mv` plus one path in `check_docs`.

9. **Consolidate the small plumbing (§2.2, §2.4, §2.5, §2.6, §2.7).** One
   git wrapper, one checker CLI shell, one `_clip`/`slugify`/`esc`, the
   AST name census as a warn step, a generated contract banner. Size:
   small each; do them inside the moves above rather than as their own WIs.

10. **Split PROCESS_OPTIONS into one file per layer; de-duplicate the
    architecture prose (§3.1, §3.4).** Size: small, prose only.

**What this review did not do.** It did not run the full test suite (the
owner directed that audit commits bypass the floor; the smoke tier and the
38-step pre-commit floor were run and are green on the full clone). It did
not read every module; the §2 duplicates were found by AST census and
confirmed by reading the named functions. The spine altitude figures are
lexical proxies (identifier regex, opening-phrase match) and should be read
as lower bounds on the rows a human adjudicator would re-tier.


---

# Second pass (2026-11-05) — trend, history cost, verification, new findings

The first pass measured a snapshot. Sustainability is a derivative, so the second
pass starts from the kit's growth curve and the cost its own records impose on
every clone, then re-verifies §1–§6 adversarially (one skeptic per section, each
re-measuring every number) and adds what six independent finders, an adopter
simulation and external research turned up.

## 8. Findings — the trend (reproduced with `trend.py`)

One row per monthly snapshot: the commit at or before that date on this
branch, then the size of each surface at that commit (`-000` example rows
excluded; the July registries were still CSV).

| date | commit | SR | LLR | TC | IF | OI | py | pyLines | tests | testLines | PROCESS_KB | OPTIONS_KB | check.py | skills | commits/30d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-06-15 | 6d98b212 | 0 | 0 | 0 | 0 | 0 | 7 | 1792 | 6 | 557 | 21 | 0 | 218 | 0 | 13 |
| 2026-07-15 | 31dfb562 | 56 | 57 | 57 | 52 | 0 | 24 | 18919 | 46 | 14490 | 58 | 135 | 960 | 5 | 495 |
| 2026-08-15 | 0edd71f1 | 149 | 152 | 149 | 115 | 19 | 58 | 51182 | 117 | 57905 | 71 | 167 | 1806 | 27 | 1402 |
| 2026-09-15 | 607cf609 | 79 | 192 | 194 | 167 | 76 | 84 | 77099 | 154 | 87742 | 86 | 185 | 2495 | 29 | 1492 |
| 2026-10-15 | 2025f841 | 131 | 302 | 316 | 243 | 105 | 117 | 105782 | 232 | 125960 | 94 | 194 | 2722 | 32 | 796 |
| 2026-11-05 | 9faf96a9 | 138 | 331 | 363 | 255 | 119 | 128 | 116540 | 269 | 153370 | 96 | 194 | 2878 | 33 | 719 |

**[HIGH] 8.1 Every surface grows linearly and nothing shrinks except once.**
Over five months the kit added ~25 scripts, ~50 test modules, ~55 LLRs and
~60 TCs per month, and `check.py` grew from 218 to 2,878 lines. The one
contraction — SR 149 → 79 between August and September (the spine
restructure of 2026-08-08, which collapsed SRs) — was followed by regrowth to
138, while LLRs never fell: the content the SR tier shed moved DOWN a tier
(LLR 152 → 192 in the same window) and kept growing there. The lesson for
§7.1 is that a one-time re-tier does not hold unless the *authoring prose and
detectors* change with it; otherwise the rows come back one tier lower.
*Change:* pair any re-tier with the LLR identifier advisory (§4.7) and a
per-SR child-count report in the dashboard, so regrowth is visible monthly.

**[HIGH] 8.2 The commit floor's freshness rule makes a 3.9 MB generated file
the most-committed path in the repository.** `PROJECT_STATE.html` was
rewritten in 2,006 of 4,682 commits (43%); its history holds 2,006 blobs,
4.65 GB uncompressed (delta compression brings `.git` to 82 MB today, but every
clone unpacks the deltas and every `git log -p`, blame and bisect reads them).
`docs/open-items.html` adds 764 blobs / 362 MB, `docs/log.md` 648 / 738 MB.
The kit's own rule (PROCESS §3, "Large composite artifacts … are regenerated
every run, **gitignored**, and published by CI as artifacts. Don't diff these")
names exactly this class and the kit's own dashboard violates it: the
`trajectory-map` floor step requires the committed copy to be fresh, so every
registry edit re-commits 3.9 MB. *Change:* gitignore `PROJECT_STATE.html` and
`docs/open-items.html`, publish them from CI (the shipped `ci/check.yml`
already uploads artifacts) or regenerate them in the merge slot only; the
freshness *check* can stay as a WARN that the committed copy, if any, is stale.
Downstream cost: none — adopters who want a committed dashboard keep the step.

```
git rev-list --objects HEAD -- PROJECT_STATE.html | awk '{print $1}' \
  | git cat-file --batch-check='%(objecttype) %(objectsize)' \
  | awk '$1=="blob"{s+=$2;n++} END{printf "%d blobs, %.1f MB\n", n, s/1048576}'
git log --oneline -- PROJECT_STATE.html | wc -l      # 2006
```

**[MED] 8.3 The test-side ratchet is the seventh-largest path in history.**
`tests/test_module_size_ratchet.py` carries 75 MB of cumulative blob bytes
because its dict-literal baseline is re-stamped on nearly every refactor
(§2.3, §5.1 in the first pass): a baseline that lives inside a 2,098-line test
module is rewritten whole each time one number moves. The same query shows
`docs/requirements/work-items.csv` (retired) at 77 MB and
`docs/archive/last_approved/…low-level-requirements.toml` at 46 MB — the
approval snapshot (§6.4) is a second full copy of the LLR registry re-written
on every approval. *Change:* as §2.3 (TSV baseline, one line per module) and
§6.4 (snapshot drift judged at the slot, not re-copied per commit).

```
git rev-list --objects HEAD | git cat-file --batch-check='%(objecttype) %(objectsize) %(rest)' \
  | awk '$1=="blob"{s[$3]+=$2} END{for(p in s) printf "%.1f MB %s\n", s[p]/1048576, p}' | sort -rn | head -8
```

**[MED] 8.4 The spine's own ratio has inverted.** In July the tiers were
roughly 1:1:1 (SR 56, LLR 57, TC 57, one LLR and one TC per SR). Today they
are 1 : 2.4 : 2.6 (138 : 331 : 363) with 255 IF rows besides — 1,087 traced
rows for a kit whose 35 needs fit on two screens. The ratio is the measurable
form of §4.5: the descent from SR to LLR is where the rows multiply, and the
IF registry (52 → 255) grew faster than any spine tier. A healthy
downstream spine for a product of this size would be closer to the July
shape. *Change:* report the per-tier ratio in the dashboard's trajectory tab
beside the orphan count; it is the one number that shows a re-tier holding.

## 9. Findings — the adopter's first day (reproduced from a fresh scaffold)

**Method.** A reviewer with no history of this repo scaffolded a fresh Python
project exactly as the shipped docs say (`bootstrap.py --dest … --stack
python`, then README "How to use", the scaffolded README ladder, `AGENTS.md`
and ADOPTING §5, literally), wrote and approved one SN→SR→LLR→TC chain in
their own words, then tried a depth-1 clone and a machine without ruff/pytest.
Every command, its exit code, wall time and output is in
`adopter-logs/` beside this file (`t.sh` is the timing wrapper, `NOTES.md` the
narrative). Nothing in this repository was touched. Not simulated: Windows and
macOS, the interactive bootstrap prompts, a non-Python stack, a kit re-sync,
the unattended loop, the adjudicator route.

**What the adopter receives** (`--stack python`, non-interactive, no agent):

| kind | files | bytes |
|---|---:|---:|
| `.py` (scripts/, kitlib/, rendering/) | 125 | 5,184,824 |
| `.md` docs (AGENTS, process, options, glossary, status, log, plan, flows, interfaces, specs, rubrics, knowledge, work) | 22 | 391,024 |
| `prompts/*.md` | 20 | 139,761 |
| `.toml` registries + process.toml + agents.toml | 13 | 103,962 |
| launchers (.sh/.cmd/.command/.ps1) | 17 | 92,769 |
| hooks | 4 | 43,990 |
| other (stamps, stage, watermark, allow files, CI, csv, .gitkeep) | 26 | 61,842 |
| **total** | **227** | **6,018,172** |

86% of the bytes are Python the adopter is told never to edit. The docs they
are told to read before the first commit (`AGENTS.md` → `docs/process.md` →
`docs/glossary.md`, with `process-options.md` linked 43 times from process.md)
total 317,115 bytes / 45,666 words — **183 minutes at 250 wpm**, 115 of them
`process-options.md`. The registry templates they must fill are 68–85% comment
lines (`stakeholder-needs.toml` 103 of 121); `process.toml` is 434 comment
lines of 482.

**The documented command path**, condensed (full table in `adopter-logs/NOTES.md`):

| step | command (where documented) | result |
|---|---|---|
| hooks | `sh scripts/setup.sh` (AGENTS.md, README ladder) | **exit 2 in 0.00 s**: `set: Illegal option -o pipefail`; hooks never installed |
| hooks | `bash scripts/setup.sh` (the adopter's guess) | ok, 12.3 s; prints "Run … `--stage DevStg-Impl`" |
| bar | `python scripts/check.py` (ADOPTING §5) | PASS, 23 steps, all `[process]`, 3.1 s; 0 product steps |
| bar | `./scripts/check.sh --stage DevStg-Impl` (as setup told them) | **FAIL**: shipped `-000` rows, shipped example flow |
| map | `gen_trajectory.py` | "no work items … nothing to render"; no `PROJECT_STATE.html` |
| menu | `run_menu.py smoke` / `./run.sh` | exit 1: `[run]` ships commented out |
| chain | first four rows, `trace.py --strict` | **5 FINDINGs**: "id watermark stands at 0 … in a lane, reserve … on the trunk, `--bump-ids`" |
| chain | commit, attempt 1 | **FAIL** `okf` STALE (docs/okf/ did not exist), `open-items` STALE |
| chain | `trunk_step.py --regen` → commit, attempt 2 | regen "skipping okf (docs/okf/ absent)"; **FAIL** `okf` again |
| chain | `gen_okf.py` (undocumented) → commit, attempt 3 | landed; 26 PASS, 20 of them "nothing to check" |
| approve | Status flips by the author → regen → commit | landed; stage → **DevStg-Impl**; no snapshot, no adjudicator |
| bar | `check.py` (now at DevStg-Impl) | **FAIL** ×3: `-000` rows, README SN citation, placeholder flow |
| cleanup | delete `-000` rows, fix flow, cite SN | **FAIL**: "SN placeholder SN-000 still present" — a shipped *comment* on line 4 |

Machine time for the whole path was about a minute. The human time is the
three hours of reading plus four refused-commit loops, each resolved by a
command no shipped doc names (`grep -rn gen_okf docs AGENTS.md README.md` → 0).

**[HIGH] 9.1 The documented hook-install command fails on Debian/Ubuntu.**
`scripts/setup.sh:5` is `set -euo pipefail` (bash); the three places that tell
the adopter to run it say `sh scripts/setup.sh` (`AGENTS.template.md:64`,
`kitlib/commit_hooks.py:53`, `dev-setup.template.sh:410`). Under `/bin/sh` →
dash (Ubuntu's default) it dies before `core.hooksPath` is set, with a message
naming no fix. The kit's load-bearing rule — every agent route refuses without
hooks (§6.2) — is defeated by its own instructions on the most common Linux.
`tests/test_shell_portability.py` runs only `sh -n` (a parse), which cannot
see a runtime `set -o` error. *Change:* make `setup.sh` POSIX sh or write
`bash scripts/setup.sh` in all three strings, and one test that executes the
prologue under dash.

**[HIGH] 9.2 The first chain costs three refused commits and three
undocumented commands.** The id watermark (`trace.py --bump-ids`, explained in
lane/trunk/WI vocabulary the adopter has not met), the OKF export
(`gen_okf.py --check` demands a directory that `trunk_step.py --regen` skips
creating), and the regen ritual itself appear in no shipped doc. *Change:* on
trunk, record the watermark in the same commit instead of refusing; make the
regenerator and the checker agree (regen creates `docs/okf/` once a real row
exists, or OKF is opt-in); every freshness FAIL names `trunk_step.py --regen`;
a five-line "after editing a registry" note in `AGENTS.template.md`.

**[HIGH] 9.3 The author's own Status flip moves the stage to DevStg-Impl and
turns the default bar red.** PROCESS.md says the approval act is an independent
adjudicator's and writes `docs/archive/last_approved/`; at the floor nothing
holds that for a trunk-only adopter: five Status-only flips landed with
`text-then-act`, `held-status` and `parent-first` all PASS and `last_approved/`
holding only its README. `derive_stage` then wrote `DevStg-Impl`, and the next
`check.py` failed on the shipped `-000` rows, the shipped example flow and a
README citation rule — the "red bar from day one" PROCESS §7 says the derived
stage exists to prevent. *Change:* floor the derived stage at DevStg-Reqs while
any `-000` row or placeholder flow citation exists; either warn once when a
Status flip lands without a snapshot, or stop promising adopters a fixed point
nothing checks.

**[HIGH] 9.4 The bar never touches the adopter's code until DevStg-Impl, and
most of what it runs reports that it checked nothing.** At the derived stage
the plan is 23 steps, all `[process]`; format, lint and tests register at
DevStg-Impl, so the adopter's own pytest test is not executed by any bar for the
whole requirements phase (it was broken — see 9.5 — and nothing said so).
`skills-index` is literally `python -c pass` and prints PASS. Of the first
commit's 26 hook steps, 20 report "no staged … / vacuous / nothing to check"
by their own text. *Change:* register format/lint/tests from DevStg-Needs (they
are the adopter's tools and cost ~1 s); drop a step from the plan instead of
running `-c pass`; register station steps only with the station layer (§1.2);
collapse "nothing to check" lines into one summary line.

**[MED] 9.5 The kit's `pytest.ini` silently shadows the adopter's
`pyproject.toml`, and the shipped CI leaves `pip install -e .` commented out.**
pytest prints "configfile: pytest.ini (WARNING: ignoring pytest config in
pyproject.toml!)"; a src-layout project's `pythonpath = ["src"]` is lost, so
the shipped CI (`ci/check.yml:63`) and any clone without an editable install
fail with `ModuleNotFoundError`. *Change:* bootstrap does not write
`pytest.ini` when the destination declares `[tool.pytest.ini_options]`; CI
installs the project when `pyproject.toml` exists.

**[MED] 9.6 README and AGENTS tell the newcomer to start with
`PROJECT_STATE.html`, which is never generated for a repo without work items**
(`gen_trajectory.py`: "no work items … nothing to render; vacuously clean"),
even after four approved rows. The kit retired `docs/architecture.md` in favour
of this dashboard, so an adopter who skips the work-item layer has no
architecture view at all. *Change:* render from the spine and the source AST
alone (work items as one optional tab), or change both sentences.

**[MED] 9.7 Three hours of reading before the first row, and schema
documentation shipped inside the data files.** Numbers above. *Change:* a
two-page first-day guide the stubs point at; cell documentation moved out of
the registry templates into one schema reference; `-000` rows minimal;
PROCESS_OPTIONS split per layer (§3.4).

**[MED] 9.8 Five places give five different "what next" commands**, and
setup's is red. `setup.sh:71`/`setup.ps1:91`/`check.sh:4` say `--stage
DevStg-Impl`; the stage-less `check.py` (the documented default) is green.
*Change:* one "first green run" block (ADOPTING §5) that every other place
links to.

**[MED] 9.9 Two guards fire on normal first-day state.** (a) A package of
`__init__.py` + `core.py` is "the 2-module architecture [that] declares no
interfaces" on every commit — the first dial the adopter learns is the one that
silences a check (`trajectory_arch.py:283`). (b) `trace.py --no-placeholders`
regexes the raw file (`trace.py:2046`), so the shipped schema comment
`[need.SN-000]` on line 4 fails the gate after every real placeholder is gone,
and the message does not say it is a comment. *Change:* count cross-module
import edges (or ≥3 modules) and report once at the gate; scan parsed rows,
as the other three tiers already do.

**[MED] 9.10 A `--stack python`, no-agent adopter receives the whole station:**
agent_loop/dispatch/lane/integrate/intake/session_*, 20 prompt briefs,
agent-resume launchers and a `stack.ini` seeding `[agent-loop] lanes = 2`,
none of which they can run (`AGENT_CMD` is unfilled by design). This is the
adopter-side measurement of §1.1/§1.2 and of recommendation 7.2.

**[LOW] 9.11 Low-value warnings on the first rows and the first machine:**
the first SN ("any non-empty name") and LLR flagged as absolutes; `test-first`
warns that TC-001 was approved after SR-001's code landed although the test
predates every requirement; `dev-setup.sh --check` reports a missing `design`
role nobody declared (`ROLES="code design"` default); one untracked scratch
file in the kit checkout stamps the scaffold `-dirty`; the watermark advisory
fires before the first commit with no action available; every hook run begins
"No checks defined at stage all." Each is a one-line fix named in
`adopter-logs/NOTES.md`.

**[LOW] 9.12 Shallow-clone and missing-tool behaviour is reasonable on a
fresh repo, with two edges.** `test-first` says "history unreadable: this is a
shallow clone … (`git fetch --unshallow`) … which is not a pass" — honest and
actionable; a bare venv fails format/lint/tests naming `scripts/setup`. But the
shipped `ci/check.yml` uses `actions/checkout` at its default depth 1, so that
WARN prints on every CI run forever, and the hook header's "No step of this
hook is ever skipped" contradicts its own `SKIP format` on a missing tool. The
§6.1 shallow FAIL did not reproduce here only because nothing ever created a
`last_approved` snapshot (9.3); it reproduces on this repository (§10.9).

**The ten things an adopter must learn before the first chain is accepted**,
as the simulation met them (full list in `adopter-logs/NOTES.md`): the TOML
table grammar and five id spaces; the id watermark and lane/trunk/WI
vocabulary; the Status vocabulary and that the flip "is the approval act"; the
regen ritual (`--regen` plus a first `gen_okf.py`); the eight-rung ladder and
which steps run at which rung; EARS and the SR/TC cell vocabularies; the
reason-cell rules (no provenance, the altitude waiver, absolute terms); the
README contract (vision tag, SN citation, anchors); back-link tags and two
dials; and the optional-but-nagged frame (external.toml, hats, da_refs/form,
IF rows or the dial that silences them, a Mermaid flow). A small team will not
absorb this before the first commit; they will meet it as refusals.

## 10. Findings — what published practice says (two research briefs)

**Method and caveat.** Two agents searched for the published practice behind
the owner's four questions and tied each source to the kit file it bears on.
Most primary domains (incose.org, faa.gov, abseil.io, eslint.org,
doc.rust-lang.org, diataxis.fr, …) were outside this session's network
allowlist, so each source was read either from a GitHub-hosted copy of the
same document (cited as such) or only as a search snippet (marked). The full
source tables with quotes, URLs and the not-reached list are
`research/research-reqs-sources.md` (37 sources) and
`research/research-tooling-sources.md` (43). Treat snippet-only quotes as
pointers to verify, not as citations.

**What it bears on the spine (§4).** The standards the kit itself cites read
the LLR tier the other way from the kit's templates and skill:

- DO-178C defines a low-level requirement as one "from which source code can
  be directly implemented without further information" — a *completeness* bar
  for an implementer. EASA's certification memorandum CM-SWCEH-002 §24 states
  that "the use of pseudo-code to express low-level requirements is not
  compatible with the … definition", naming the mechanism: "suppliers develop
  the Source Code and then later on they produce the design in form of a
  reverse engineering activity". CAST-15 (now DO-248C FAQ #81) refuses merged
  levels that skip either level's objectives. INCOSE GtWR R31 permits a named
  solution only "unless there is rationale for constraining the design", and
  its characteristic C2 *Appropriate* ("amount of detail is appropriate to the
  level") is the published name for the altitude property §4.1 measured; ISO
  29148's rule hinges on *unnecessary* constraints. Ivy Hooks (1993) names
  "writing implementation (HOW) instead of requirements (WHAT)" as the oldest
  requirements defect.
- ISO/IEC/IEEE 29119-1 defines a test case by its preconditions, inputs and
  **expected results**, and 29119-3 keeps the test-case specification apart
  from the test-procedure specification. DO-178C trace data (item 11.21) and
  ISO 26262-6 trace requirement ↔ **test case**; nothing cited asks for a link
  below the test case. Beck's Test Desiderata ("structure-insensitive — tests
  should not change their result if the structure of the code changes"),
  Google's "Test Behaviors, Not Methods" / "Change-Detector Tests Considered
  Harmful", Hyrum's law and Cucumber's "would this phrasing need to change if
  the implementation changed?" state the test-authoring bar in one line each;
  van Deursen et al. (2001) name testing one thing through another *Indirect
  Testing*.
- On cost: Heindl & Biffl's value-based tracing reached about 35% of full
  tracing effort by descending only where risk or volatility is high; Mäder &
  Gotel show unmaintained links "get lost or represent false dependencies";
  Rath et al. found only ~60% of commits linked to issues in the wild;
  Mäder & Egyed measured +24% speed and +50% correctness *from the
  requirement↔test link*; Jones puts requirements change at ~1%/month, against
  this kit's 30–40%/month growth of LLR/TC rows during the build phase (§8).
  Gotel & Finkelstein locate most traceability problems on the *need* side.

**[HIGH] 10.1 The two shipped template cells manufacture §4.1 and §4.2.**
`registries/low-level-requirements.template.toml:19` tells the author
`detail = "… Name the real (or planned) module + symbol."` while
`prompts/spine-questions.md:245` says an LLR "names no implementation carrier
(a code file, function or symbol)". `registries/test-cases.template.toml:26`
says `expected = "Cite the verified requirement's AcceptanceCriteria by id (do
not paraphrase)."` — the sentence 202 of 363 live rows obey (they open
"Satisfies/Cite/See" or name AcceptanceCriteria). Adopters copy the template,
not the prompt; the template header calls the `-000` row "the only place the
vocabulary is written down". Measured: 205/331 LLR details repeat a token from
their own `code_symbol`, 80/331 contain call syntax `name(`. *Change:* line 19
→ "The design decision this row fixes — which module owns it, what crosses its
boundary, where it refuses — in words that survive a rename; the carrier is
named only in `module`/`code_symbol`." Line 26 → "The observable outcome for
this case's parameters, in the stakeholder's words, with the pass line (one
sentence); the AC id is already in `verifies`." §11 shows both applied.

**[MED] 10.2 `method` has no guidance and became the test procedure; `evidence`
is traced a tier deeper than any cited standard.** The template's `method`
value is "EXAMPLE - delete on first real entry" — the one cell with no
instruction — and IF-161 (`docs/test/README.md:7-9`) lists it undefined;
result: median `method` 516 chars vs median `expected` 135. 241/363 `evidence`
cells carry `::` node ids; the template's own example is file-level
(`docs/test/manual-smoke.md`) and PROCESS §3 says the registry rows are
authoritative over `Implements: TC-` tags. *Change:* `method` = one-line
instrument class ("pytest, the named module" | "inspection <id>" |
"observation <rubric>"), the procedure in the test docstring; `evidence` = a
path or command, with node-level binding derived from the tags by
`check_trajectory`, never typed.

**[MED] 10.3 The `spine-authoring` skill reads "directly implementable" as a
licence to name design elements (`SKILL.md:51-57`: "naming design elements at
LLR tier is the expected shape"); the regulators read it as a completeness test
on the design, and the skill's own failure mode #1 is "Implementation-
mirroring" (`SKILL.md:176`).** One sentence after line 57 closes it:
"Directly implementable means complete enough to code from, not written from
the code; a pseudo-code or symbol-list LLR fails the definition."

**[MED] 10.4 No shipped prose tells a test author to assert behaviour rather
than wording or structure.** A grep of `AGENTS.template.md`, both PROCESS
files and all 33 skills for behaviour-vs-wording, exact-message, public-API or
structure-insensitivity guidance returns nothing; the only test-authoring line
is "red → green → refactor" (`AGENTS.template.md:41`). The 724 literal-string
asserts of §5.2 and the structure tests of §11.6 are what authors produce
without that bar. *Change:* three lines beside line 41: test through the public
entry point the SR names; assert the outcome and a stable token of a refusal,
the sentence only where an SN makes the wording the contract; a test that a
behaviour-preserving refactor breaks, or whose subject is the suite, CI or
layout rather than the kit, is a test defect (Indirect Testing), not a guard.

**[LOW] 10.5 Altitude guidance is heaviest where the leak is smallest.**
`spine-questions.md` §2 (SR) is 133 of 315 lines, mostly hat attribution and
EARS traps, and the SR tier is lexically clean (0/138 ACs with call syntax);
§3 (LLR+TC), where 80/331 details carry call syntax and 241/363 evidence cells
carry node ids, gets 15 lines of voice guidance and no definition of
`expected` or `method`. INCOSE's whole rule set ships as a one-page sheet; EARS
is five patterns. *Change:* move the (c)–(c3) hat sub-bullets (~60 lines) to
the hats layer's own doc; add to §3 the completeness test, the C2
"appropriate to level" length test, and the two TC cell definitions.

**What it bears on the tooling (§1, §2, §6).**

**[HIGH] 10.6 The commit hook is a whole-repository presubmit, not a
staged-files hook.** pre-commit "only runs on the staged contents of files";
lint-staged exists because "running a task on a whole project can be slow";
Google's presubmit rule is "only fast, reliable ones". The kit's hook
regenerates the dashboard, open-items, CLI and interface references, skills
index and prompt catalog and re-reads git history on every commit: measured
here 28.0 s wall / 63.4 s CPU on 4 cores for the 25-step list alone
(`trajectory` 27.9 s, `trajectory-map` 19.8 s, `open-items` 12.7 s,
`registry-integrity` 10.1 s, `approval-fresh` 5.9 s; `research/hook-run-full-
clone.log`). Only the ruff step is scoped to `git diff --cached`. *Change:*
hook = staged-scoped, sub-10-second steps (format, integrity of the registries
actually touched, secrets); whole-tree generators and history-dependent checks
move to `hooks/pre-push` and CI; `--path-triggered` (already at
`pre-commit:287`) gates generator steps on the paths that feed them.

**[HIGH] 10.7 Permanent advisories are printed row by row on the floor, and
the warn level has no graduation path.** ESLint's rationale for "warn" is that
it is transitional ("typically used when introducing a new rule that will
eventually be set to error"); Rust declares a default level per lint (measured
over `rustc_lint_defs`: Allow 38 / Warn 80 / Deny 37) and caps lints in
dependencies so they cannot pollute a build; `#![deny(warnings)]` is a named
anti-pattern because new lints break builds that used to pass. In the floor
run 350 of 497 output lines were WARN, 178 of them from three per-row classes
("SR SR-N declares no Form" ×128, "IF IF-N Data is N characters" ×30, "SR SR-N
is unclassified" ×20); `check.py:765` and `:911` declare classes "WARN-ONLY
ALWAYS". A class that can never fail is a report, not a check. *Change:* each
advisory class is either transitional (declared promotion rung) or report-only;
report-only classes leave the floor's stdout for the trace report and
dashboard; the floor prints one line per class with a count and the first
instance, the full list under `--verbose`; kit-owned rows inside an adopter's
repo are capped like dependencies.

**[MED] 10.8 Three ratchet representations with opposite policies, and the
strict one is the known re-stamp anti-pattern.** `check_complexity.py:448-463`
FAILs when a function *improves* ("RE-STAMP DOWNWARD … in this same commit")
and keys on the qualified function name (every rename re-stamps);
`flag_axis.py:136` warns only on a rise; the test-side baseline is a dict
literal rewritten whole (§8.3). Betterer auto-updates its results file when a
result improves and fails only on regression; ESLint bulk suppressions key
file→rule→count with no line numbers and offer `--prune-suppressions`;
mypy-baseline is "carefully crafted to avoid merge conflicts"; Notion moved
its ratchet to one TSV line per file+rule for the same reason. *Change:* one
`kitlib.ratchet` — TSV keyed per file (+rule), count semantics, auto-tighten
on improvement, FAIL/WARN on regression per one severity table, `--prune` for
vanished rows; the two test-side dict literals become rows of it (§2.3, §5.1).

**[HIGH] 10.9 The shipped CI clones at depth 1 while the commit floor fails
closed on shallow history.** `project-trajectory/ci/check.yml:46` uses
`actions/checkout` with no `fetch-depth` ("Only a single commit is fetched by
default"); the kit's own `.github/workflows/test.yml` sets `fetch-depth: 0`
three times, so the kit never sees what every adopter's CI does. Reproduced
on a depth-50 clone of this repository: `approval-fresh`, `registry-integrity`
and `open-items` FAIL with "… is NOT byte-identical to … at 37bcca3b, the
commit that last wrote it" while nine other findings in the same run correctly
say "unverifiable — its landing lies past this shallow clone's history"
(`research/floor-run-depth50-clone.log`). setuptools-scm's default is
`warn_on_shallow`; GitVersion and mkdocs plugins document `fetch-depth: 0`;
semantic-release unshallows itself; SonarQube warns and degrades. *Change:* one
`kitlib.git.shallow_boundary(root)`; any last-writer lookup landing on a graft
commit returns *unverifiable* and the step WARNs with the remedy; `fetch-depth:
0` with a one-line reason in the shipped workflow. Confirms §6.1 and §7.4.

**[MED] 10.10 Downstream update is a 644 KB prose procedure; file ownership
and merging are not machine-readable.** Copier and Cruft solved "update an
already-generated project" with a stamped answers file, regeneration from the
new template version applied as a diff with conflict markers, a declared
`skip_if_exists` class for project-owned files, and several small templates
composed on one project ("1 template = 1 Git repository"); Backstage ships no
update channel and its community adds Copier because it is "version-aware".
The kit has the stamp (`docs/kit-version`) but its file classes and migration
entries are prose an LLM executes, `bootstrap --sync` force-overwrites
kit-owned files silently (`bootstrap.py:682-699`), and `RESYNC_PACK.md` grows
monotonically and is read whole on each resync. *Change:* an ownership column
per path in the bootstrap manifest; a `bootstrap --update` that three-way
merges old-kit → new-kit onto the adopter tree with conflict markers; a
"kit-version behind" WARN on the floor; the core, station and domain-skills
layers each with their own manifest and stamp. RESYNC_PACK shrinks to the
human-judgement entries per layer.

**[MED] 10.11 Provenance frames in code comments and kit-scope skills break
the kit's own rule, and the detector covers spine cells only.** Linux kernel
style ("tell WHAT your code does, not HOW"), Google's Python guide ("never
describe the code"; bug references belong on TODOs for temporary code) and
Clean Code's case against journal comments agree with `AGENTS.template.md:182`
("State the constraint, not its history"). Measured: 1,842 `WI-###` citations
in scripts, 90 of 122 modules with more than one (against "at most once per
module"), 42 files stamping "owner ruling", `check.py` 741 comment lines of
2,878; kit-scope skills `gate-advance` 5, `spine-authoring` 2 citations.
`trace_text.provenance_advisories` (`:692`) reads registry cells only.
*Change:* point the detector at `*.py` comments/docstrings and `SKILL.md`
(warn-only, one header pointer allowed); one sweep keeps the constraint and
drops the frame (§1.3, §7.6).

**[MED] 10.12 Owner rulings have no immutable, globally numbered record.**
`decisions.template.toml` is "ONE FILE PER RUN" with `D-001…` restarting per
run and owner/review cells edited in place; 42 script files cite rulings by
date. ADR practice (Nygard; adr-tools) keeps one short immutable record per
decision with a stable id and marks a reversed decision *superseded* rather
than deleting it. *Change:* `docs/decisions/ADR-NNN` (or a TOML registry with
global ids and proposed/accepted/superseded status) for owner rulings; living
docs and code cite nothing (the kit's rule); the log and archive cite the id;
`docs/archive/retired-vocabulary.md` becomes part of the same log.

**[LOW] 10.13 PROCESS.md and PROCESS_OPTIONS.md mix reference and
explanation.** Diataxis: reference "should be austere" and only describe;
explanation is where "design decisions, historical reasons" belong. The rules
and their rationale interleave across PROCESS (14,092 words), PROCESS_OPTIONS
(199 KB) and `check.py`'s comment banners, so the reference cannot be read
austerely and the explanation cannot be skipped. *Change:* PROCESS.md stays the
austere reference with stable § anchors; one RATIONALE.md absorbs the why;
options split per layer (§3.4). The kit's own `byte-budget-guard` skill
records the evidence that this needs a cap, not a watch: "hard caps hold and
watch-only does not" — capped `AGENTS.template.md` +2.6%, watched PROCESS.md
+91% and PROCESS_OPTIONS.md +1,101% in one 48-day window — yet both files
remain watch-only.

**[LOW] 10.14 No single table of step default levels.** Severity and strict
promotion are decided per step in scattered comments and flags
(`check.py:577-622`, `:1736-1751` "SEVERITY LIVES AT THE WIRING",
`:1891-1905`); rustc, Ruff and flake8 each publish one default-level table.
*Change:* a severity table (in `docs/stack.ini` or the `steps()` tuple)
naming each step's default level and promotion rung; the pre-commit, pre-push
and CI plans select by level from it.

**[LOW] 10.15 Records sit in the working tree with no owner or freshness
marker.** 104 `handoff-*.md` at the `docs/` root, 46 MB `docs/iteration`,
16 MB `docs/reviews`; Software Engineering at Google: "Documents without
owners become stale", provider-facing documents "kept apart" from what users
read; git-sizer on object-count costs. Extends §1.5. *Change:* handoffs and
review rounds under `docs/archive/` with the banner, or a records branch; one
index with owner and reviewed date; a `check_docs` WARN for a handoff older
than N days outside the archive.

## 11. The re-tier exemplar — three subtrees rewritten at end-user altitude

**Why.** Recommendation 7.1 is the largest change in this record and the
easiest to dismiss as taste. So one reviewer rewrote three SR subtrees chosen
for range — SR-156 (the station's merge seam, 11 LLRs / 15 TCs, 93,262 prose
chars), SR-199 (observation records, 3 / 3, call syntax in every detail) and
SR-157 (the trace check every adopter runs, 22 LLRs / 27 TCs, three times the
fan-out bound) — under the rules the kit already states: no provenance in
cells, no function or filename in LLR text, no file in SR or SN text, a TC
`expected` that states a condition. The verbatim BEFORE dumps, the proposed
AFTER rows as valid TOML, the comparison scripts and the rendered pairs are in
`exemplar/` beside this file (`python3 -I exemplar/compare.py . exemplar/after
SR-156 SR-199 SR-157` reproduces every number).

| metric (all three subtrees) | before | after | change |
|---|---:|---:|---|
| rows (SR+LLR+TC) | 84 | 31 | −63% |
| LLR / TC rows | 36 / 45 | 13 / 15 | −64% / −67% |
| prose chars | 138,627 | 19,692 | −86% |
| code identifiers in prose (broad regex) | 1,380 | 48 | −97% (residue: "non-fast-forward", "read-only", evidence paths) |
| evidence node ids (`path::test`) | 350 | 0 | −100% (every one of the 47 evidence *files* still cited) |
| TC `expected` opening "Satisfies" | 28 | 0 | −100% |
| longest LLR `detail` / TC `method` | 6,977 / 15,874 chars | 977 / 137 | −86% / −99% |
| kit's own gating text rules (form, provenance) | 0 findings | 0 findings | the detectors see neither shape |
| `sr_fanout_advisories` | 1 (SR-156; SR-157 re-stamped) | 0 | — |

The spread is the point: SR-199, already near altitude, loses one LLR and one
TC; SR-157, one-LLR-per-rule, loses 17 LLRs and 20 TCs.

**[HIGH] 11.1 LLR `detail` is a docstring copy, measurably.** With the kit's
own paraphrase tokenisation (alphabetic runs ≥4 chars), the median LLR detail
has **84%** of its significant words already present in the docstrings of the
module(s) its `module` cell names (303/331 rows ≥50%, 254 ≥70%); against an
unrelated module the median is 54%, and the own-module share wins on 271/331
rows (`exemplar/overlap.py`, `overlap_control.py`). The content the rows carry
is the code's documentation a second time, and it is the copy that rots.

**[HIGH] 11.2 The extreme case: TC-205 is 15,874 chars of `method` and 89 node
ids; LLR-207 is 6,977 chars of `detail` with 41 `code_symbol` tokens.** The 15
TCs of SR-156 hold 262 node ids over 47 files. The narrative already exists as
`tests/test_verdict_record.py`'s module docstring and its 81 test names; the
symbol list is `verdict.py`'s public surface restated (the anchor rule needs
*one* binding token, `check_doc_refs.py:592`). Every rename is a registry edit.

**[HIGH] 11.3 SR-157's 22-child fan-out is waived by a re-stamp whose argument
contradicts the row's own acceptance criteria.** The rationale says "the child
count tracks the number of declared rules rather than the number of decisions
this row makes" (`system-requirements.toml:755`); the AC says the rule
inventory is "recorded at its declaration site, not restated here" (`:756`).
The 22 LLRs then restate the inventory, one LLR per rule. The proposal keeps
five LLRs, each one decision (every rule is a pure predicate composed by one
engine; a finding's class, declared beside its rule, decides the exit code;
what a row's cells mean is defined once below every reader; the work registry
is one folder read once; a test-file declaration can only add a finding) and
moves each rule's firing shape into seven TCs' `expected` cells. 50 rows → 13.

**[HIGH] 11.4 The kit's own advisories are blind to altitude.** Over the BEFORE
rows the pure text rules return form 0, provenance 0, EARS 0, paraphrase 0,
comparative 0, SR-artifact 0, fan-out 1; a 15,874-char method and a 6,977-char
detail raise nothing (`exemplar/kit_rules.py`). The only live altitude signal
is the fan-out bound, and SR-157 re-stamped it. The registry can regrow to its
current shape with every detector green — which is what §8.1 shows it did.
*Change:* three warn-only advisories in `trace_text`, listed in the report like
the SR ones: LLR detail with call syntax, snake_case or a filename, or over
~800 chars; TC `expected` opening on a pointer ("Satisfies", "Cite", "See");
TC `evidence` containing `::`. Plus the per-SR direct-child count in the
dashboard's trajectory tab (§8.1, §8.4). The twenty-line regexes in
`measure.py` and `exemplar/compare.py` are the detectors.

**[MED] 11.5 SR acceptance criteria absorbed sibling SRs' content, and TCs
verify SR-156 only incidentally.** SR-156's 1,665-char AC carries SR-154's
review-gated-landing clauses and SR-232's Done-when brief grammar; TC-317
(coordinator guard) and TC-370 (hooks-off refusals) verify SR-156 only because
the claim's refusal ladder runs before the lock. The proposal's AC is 694
chars and states only what the row owns; the two TCs re-point to SR-229 and
SR-240 (not deleted).

**[MED] 11.6 Tests of code structure are traced as test cases.** TC-193 asserts
"every re-exported name … IS the kitlib.spine object (`is`, not `==`)"; TC-197
asserts "this module imports no sibling … no nested def". These verify the
shape of the code, not SR-157's observable. Under the proposal the behavioural
half survives (TC-914: the checker, the stage derivation and a fresh scaffold
answer alike for a row's cells) and the structural assertions stay as plain
tests with no TC row (§5.1).

**[LOW] 11.7 Two small hygiene classes.** `level` doubles as a verification
method on nine TCs (Analysis 3, Inspection 5, Critique 1) — one field, two
questions (spine-authoring §6). SN-027's `acceptance` names a spec file and
`--jobs 1`, SN-008's names `--lenient` and "(SR-006)"; §1(e) forbids both and
the SN artifact advisory excludes `.md` by design, so neither is reported.

**[MED] 11.8 Projection and order of operations.** Weighted over the three
subtrees the registry-wide target is roughly LLR 331 → 120–180 and TC 363 →
120–200, consistent with the first pass's ~150. Three SRs took one reviewer
session; 138 SRs is weeks of adjudication that §8.1 says will be undone within
months if new rows keep arriving at the template's altitude. *Order:* the
template and prompt fix (10.1–10.3) and the three advisories (11.4) first —
one lane, days; then re-tier in batches starting with the ten largest fan-outs
(SR-157 22, SR-148 16, SR-154 11, SR-054 11, SR-155 11, SR-156 11, SR-244 10,
SR-168 8, SR-053 8, SR-006 7) and the call-syntax extreme SR-225 (18 calls,
9,512 detail chars), each batch judged by the blind re-derivation the
`spine-authoring` skill §4 prescribes.

**What the rewrite loses, and where it already lives** (full table in
`exemplar/TABLES.md` §E): the record field tuple, canonical UTC form and
temp-file naming → `observation.py:21` ("WHAT MAKES A FILE A RECORD…");
per-rule mechanics (Jaccard window, EARS keyword list, port-script carve-out)
→ each rule's docstring, the `trace_text.py:5-18` table and
`docs/registry-machinery-reference.md`; the trailer grammars and 64-hex
identity → `verdict.py:1-152` and IF-175/IF-242; consolidation history in
LLR-197/LLR-201 → the log (and `kitlib/spine.py:1-30`, a second target for the
§1.3 sweep); per-case narratives and 350 node ids → test docstrings and names,
with evidence derived from `Implements: TC-` tags (the reader exists,
`gen_arch_map.read_test_tags`; 5 of 269 test files carry a tag today).

**Caveats the exemplar itself records.** It was not a blind re-derivation (the
reviewer read the rows and the code); each proposed `expected` was not checked
clause by clause against its evidence module; the interface rows named as the
new home of lost grammars (IF-175, IF-214, IF-215, IF-242, IF-286, IF-287)
were not re-read; the proposal was run through the kit's pure text rules but
not through `trace.py` end to end on a mutated registry, so `--strict-schema`
and the `CodeSymbol` binding of the new `code_symbol` values are unverified;
15 absolute-term advisories remain on the AFTER rows ("every rule", "each
claimed item").

**One pair in full — SR-199 after** (before: 7 rows, 5,794 chars; after: 5
rows, 2,922 chars; the other two pairs are rendered in `exemplar/TABLES.md`):

> **SR-199** The delivered process shall keep each result of an observation
> test as a record of its own, apart from the test case, stating the outcome,
> who or what observed it, when, until when it stands, and what it judged.
> *AC:* A reader finds the latest result of an observation test as a separate
> record naming the case, a pass or fail outcome, the observer, the
> observation time, an expiry no later than the case's declared lifetime, and
> a digest of the inputs the case declares (empty where it declares none); a
> record that is incomplete, malformed, aimed at a case that is not an
> observation test, or expiring beyond that lifetime is reported and is not
> read as a result; and recording a result leaves the test case's own row
> unchanged.
>
> **LLR-234** *A result is one whole record in the observation store, or
> nothing* — `module: kitlib/observation.py`, `code_symbol: parse/write_atomic`.
> Each result is one file of its own in the observation store, named by its
> test case and its instant, so results written on different lanes do not
> collide and a new sample does not edit an old one. A file is a result only
> when every field is present and well-formed, both instants are in the one
> canonical UTC form, the expiry is not before the observation and the
> observer is named; anything short of that reads as no result rather than as
> a wrong one. A write lands a whole record or leaves nothing where a reader
> looks.
>
> **LLR-235** *One record policy, applied when a result is written and when
> one is found* (absorbs LLR-236) — `record_observation.py;
> assumption_rules.py`, `record_refusal/observation_record_findings`. Results
> enter the store through one command, which refuses — writing nothing — a
> result the record policy forbids …; the traceability check judges each record
> it finds by the same policy and fails its strict run naming the file, so a
> record that reached the repository without the command stands on no other
> terms.
>
> **TC-229** *method:* pytest over the record module in a temporary directory.
> *expected:* A whole, well-formed record reads back as the result it states,
> while a record missing any field, cut off mid-file, outside the canonical
> time form, expiring before its observation or naming no observer reads as no
> result, and no partly written file is visible to a reader at any moment.
> *evidence:* `tests/test_observation_record.py`
>
> **TC-230** (absorbs TC-231) *method:* pytest over a bootstrapped scaffold,
> driving the writer and the traceability check as commands. *expected:* Each
> result the policy forbids is refused at the command with nothing written
> and, when planted on disk instead, fails the strict check naming the file; an
> admitted result leaves the test-case registry byte-identical and carries a
> digest that changes only when a declared input's content changes.
> *evidence:* `tests/test_observation_writer.py`

The before-row TC-229 read `expected = "Satisfies SR-199's acceptance clauses
on the record's fields, the empty digest for a case …"`; LLR-235 opened
"`record_observation.py --tc TC-### --outcome pass|fail --by <provenance>
[--expires <UTC>] resolves the test c…`".

## 12. Verification of the first pass — one skeptic per section

**Method.** Six independent reviewers each took one section of §1–§6 with the
brief to *refute* it: open every anchor, re-measure every number with their own
command, search for what the kit already does, and judge the proposed change
against downstream cost and the kit's own principles. Verdicts: CONFIRMED (holds
as written, numbers within 5%), PARTIAL (holds with the stated corrections),
REFUTED. The skeptics' full evidence (commands, outputs, line anchors) is in
the session's workflow journal; the corrected numbers below reproduce with the
revised `measure.py`. HEAD moved from `9faf96a97` to `1824c259b` during the
pass; §1–§6 were not edited.

**Corrections to §0.** "SN 35 rows" → 31 needs plus 4 stakeholders in a
separate `[stakeholder.*]` table (the miscount was `measure.py`'s own, now
fixed). "116 files" → 97 top-level scripts, 128 with `kitlib/` and
`rendering/` (116,540 lines). "281 test files" → 278 `.py`, 269 test modules
(153,370 lines). "1,842 WI citations" → 1,992 (the first pass skipped
`rendering/`). "38-step floor" → 29 `check.py` steps plus 4 script calls at
the hook; 47 steps registered at `--stage all`.

| § | first-pass tag | verdict | what stands after verification |
|---|---|---|---|
| 1.1 | HIGH | PARTIAL | The size statement holds; "an adopter receives ~1.2 MB of Markdown" does not: the manifest ships 0.53 MB of `.md` plus ≤86 KB of kit-scope skills; `RESYNC_PACK.md` (644 KB) and the kit README stay in the kit checkout, and the pack is range-filtered by design. Re-anchor the headline on what ships: 5.99 MB, of which 5.18 MB Python. |
| 1.2 | HIGH | PARTIAL | The station is ~48% of the code and its steps are in the floor (confirmed). The LLR share was understated (107 LLRs name only station modules, 159 at least one). The separable station is nearer 42k lines: ~9.4k lines the partition called "station" (`spine_carrier`, `baseline_snapshot`, `acceptance_record`, `agent_common`, `schedule`, `prompts`, `record_observation`) are imported by 10 core modules, and PROCESS.md itself speaks station vocabulary (lane ×12, sitting ×8). The split is a migration — shared modules to `kitlib` first, a declaration-driven hook list, a RESYNC entry moving 52 files — not "a directory move plus manifest rows". |
| 1.3 | HIGH | PARTIAL | Ratio 0.82 confirmed, but the guide *asks* for header and symbol docstrings, so the ratio is by design. The measurable defect is the per-site provenance frame: 1,992 `WI-###`, 96 of 128 modules citing more than one, 102 "owner ruling", 453 `OI-###`, 512 ISO dates. The rule ("at most once per module, a header pointer") is `AGENTS.template.md:182`, in the Working agreement, and no enforcer backs it. A detector must follow the sweep, or it prints ~3,000 lines. Tag stands on reading cost, not breakage. |
| 1.4 | MED | PARTIAL | 350 WARN of ≈520 lines, 27 s `trajectory`, 18 s `trajectory-map`: confirmed. The floor is green at HEAD; the "FAIL approval-fresh" was the review's own first commit. 201 of the 350 WARN come from four classes in two steps. The hook already skips the ten `_TRUNK_FRESHNESS_STEPS` on a claimed work branch (`check.py:1658`), so the cost falls on trunk commits — which in this repo are most commits. Moving `trajectory-map` changes a stated rule (PROCESS.md:310); name the whole set. |
| 1.5 | MED | PARTIAL | Docs are 80% of the tree (understated), but "that no gate reads" is wrong for most of `docs/archive`: 73% of it is live registry input (`work/`, `last_approved/`, `specs/`) read by 13 scripts, and the merge gate's verdict join reads `docs/reviews` and `docs/iteration` (`kitlib/verdict.RECORD_PREFIXES`). A records *branch* would break that join. Re-scope to closed lanes and prose history, or a retention rule in the loop. |
| 1.6 | LOW | PARTIAL → withdraw | 29 skills ship (4 are `scope: this-repo`); 15, not 17, are domain-gated; the 17 total 22 KB with zero process coupling. A second `skills-domain/` root would duplicate the IF-035 machinery for 22 KB of prose — net-negative under the kit's own one-home rule. Fix the two `any` domain lists if universal shipping is unwanted. |
| 1.7 | MED | CONFIRMED | Numbers hold within 1%. Window caveat: 26% is the last three weeks (18% over 1,000 commits, 6% over all 4,682); the ritual dates from 2026-08-30 and the scoped-unpause direction from 2026-10-04. Sharper root cause: the pause file is deliberately one-bit while the owner's standing instruction is a *scoped* unpause, which the file cannot express. The proposed `station.toml` conflicts with `process.toml`'s recorded presence-as-semantics exception; a scope key inside the pause file (`allow = ["WI-983"]`) honoured by `integrate.py:681` makes a scoped claim one commit. |
| 2.1 | HIGH | PARTIAL → MED | The two `load_wis` are projections over a ~10-line shared id-gate with deliberately opposite error policies (validator reports, scheduler skips); 69 live tests pass in 1.8 s; 40%/25% prose, not "most". Deleting `test_rule_sync` collides with ruling D-7 (`docs/stack.ini:1085`). The real unguarded duplicates the finding missed: `WI_ID_RE` verbatim in two modules with no home and no pin, and the `Predecessors` cell split three ways across six modules. Change: a `wi_rows(rows, on_error)` id-gate generator; each caller keeps its projection. |
| 2.2 | MED | PARTIAL → LOW/MED | 8 named wrappers plus ~10 inline `subprocess.run(["git"…])` sites; `derive_stage._git` already delegates to `kitlib.git.git_out`. They vary on seven axes (return shape, strip, stderr, stdin, env, bytes, OSError policy), so two keyword arguments cannot replace them, and a five-knob wrapper is the mode-flag shape the `deep-module-design` skill forbids. Feasible: one raw `kitlib.git.run` as the single subprocess site with `git_out` and an `(rc, text)` adapter as the two public shapes. |
| 2.3 | MED | PARTIAL → LOW | Only `read_baseline`/`write_baseline` (~20 lines) are semantic duplicates; `compare`/`_report` carry opposite *policies* (fail both directions vs warn on rise). The test ratchets hold 9 and 41 entries (not "every module"), and `test_complexity_ratchet` measures McCabe through `ruff`, which cannot become a row of the cognitive baseline without a shipped dependency. One TSV read/write pair in `kitlib`; two policies stay two functions. |
| 2.4 | MED | PARTIAL → LOW | The four-piece shell is written 4 times, a partial variant 13, the literal suffix 2; `check_flows.py` is not a warn-first checker (it exits 1) and `check_stubs` warns under `--strict`. `utf8_console` is already shared. 4–8 scripts × ~10 lines. |
| 2.5 | MED | REFUTED | `check_dupes_census.py` is not retired: it is the standing warn-only `[step:dupes-census]`; D-7 tore down `check_dupes.py`. 93 of the 94 name collisions have different bodies; of the five named pairs, `slugify` are homonyms, `_clip` two of four are wrappers over the one home, `esc` is a one-liner. Real pairs: `_id_number` ×2 inside `kitlib` (plus `spec_id_number`/`wi_convert`), `gen_release_checklist.load_csv`, two line-clips (~15 lines). A name-census step would add ~90 homonym WARNs and re-open D-7. |
| 2.6 | LOW | PARTIAL | The composers differ in rider set, remedy composition, squash reading and message frame, not only tree source; ~15 shared lines against 48 docstring lines. A §1.3 instance, not duplication; keep apart (`integrate.py:1338` states why the slot re-judges). |
| 2.7 | LOW | PARTIAL | 347 tracked files tree-wide, of which 105 kit files, 99 carrying the machine-read `Contracts:` marker; ~240 are records quoting headers (§1.5). The identical frame exists in ~27–30 files, 2.8 KB; the bodies are 228 / 334 KB (median 977). The marker is read by the connectivity check and the generated interface reference — do not delete it; the weight is the body length, the §4.1 problem in another cell. |
| 3.1 | MED | PARTIAL → LOW | The list names eight homes and omits PROCESS §4 and `spine-questions.md` §4. "The surrounding prose repeats the rubric" is refuted: the rubric's vocabulary appears zero times in PROCESS, OPTIONS or AGENTS. Real restatement is ~1 KB (the derived-map rule three times inside §3; the IF row model in §8 and the OPTIONS layer; two uncited AGENTS bullets). The rubric at 15.7 KB is the single largest architecture home. The proposed change ("§3 keeps only three invariants") is mis-aimed; the IF-model duplication and the derived-map triple are the cut. |
| 3.2 | MED | PARTIAL | `components.derived.toml` holds 4 entries and is a generated view, not a registry; the "ONE cycle" sentence is stale (the ratchet's baseline is empty, 7 tests pass); the component layer *is* consumed (gen_components, the `component-view` step, cross-component findings, membership join). The evidence that does support the thesis: 229 of 255 IF seams (90%) cross a boundary of only 4 components; 255 rows against the kit's own "~30–35" estimate; 14 multi-tagged modules suppress the seam rule; 6 SRs are unplaced; and the station cut already exists as CMP-008. |
| 3.3 | MED | REFUTED → LOW | `coordinator-cycle` and `session-protocol` are already `scope: this-repo` and never ship (`bootstrap.py:540`, `test_bootstrap.py:1457`); the `WI-926` example lives only in the this-repo `recipes.md`. The shipped surface carries 3 WI citations and ~5 ruling phrases (gate-advance, spine-authoring, antidote). The real provenance sink is `coordinator-cycle/references/recipes.md`: 102 KB, 61 WI citations, this-repo. Change: strip the handful; generalise `test_skills_index.py`'s stray-WI pin to every kit-scope skill. |
| 3.4 | LOW | PARTIAL | 27 layers, not 34. The file itself declares a deferred split of the two spec-sized layers (29% of its bytes) and records the +1,101% watch-only growth. Cost is understated: a per-layer split reworks bootstrap's profile omission, the manifest row, 8 dashboard hrefs, the OKF export, 4 test modules, and ~137 section-name cites no checker validates. Cheaper first step: move the two layers behind pointer stubs. |
| 4.1 | HIGH | PARTIAL | Lengths hold (median 759; 58 > 1,500; 18 > 3,000; LLR-270 11,427). "252 of 331" overcounts — 59 rows match only ALLCAPS English (TOML, HEAD, SCOPE); defensible: 112 name a call or `.py`, 199 by snake_case/call/`.py`, 204–209 repeat a token of their own `module`/`code_symbol`. The LLR-298 warning runs the other way (the cell is stale relative to the code). The proposed §3 prose already landed (B1). The shipped template line 19 is the unfixed authoring surface (§10.1). "Move the symbol list to `code_symbol`" contradicts ruled item 5 (the cells retire; code points up); a 600-char warn would fire on 197/331 of the kit's own rows. |
| 4.2 | HIGH | PARTIAL → MED | Strictly vacuous pointers are 96–119 (26–33%) depending on the heuristic; 202 open "Satisfies", 81 of those carry an outcome after a colon. The pointer is the shipped convention — template line 26 and `gen_cases.py:210/238` generate it. "Duplicates the test docstring" is refuted: 73% of the evidence functions have none. The measurable defect is `method` (median 516, max 15,874, 233 > 300). An `expected` rewrite is sound only in the exemplar's form (the case's observable outcome, never the AC restated). |
| 4.3 | HIGH | PARTIAL → tracking | 2,124 node ids and 6 of 269 tagged files: confirmed. Two of the four "dead" ids moved to another module. Deriving evidence from tags is not a gap: it is ruled (2026-10-11 rev 8, rev 35) and in flight — the tag reader landed 2026-11-04 (WI-994), seeding and the equality check are active (WI-997), the generated column is item 5's last step. The ruled design keeps *per-test* tags (replacing `::` cells); "file-level only" contradicts it. |
| 4.4 | MED | PARTIAL | Numbers hold; add `coincident` (71 rows, 15.5 KB). "Are test procedures" overstates: SR-199's AC names no instrument. Fixed thresholds would warn on 83/138 ACs and 104/138 rationales of the kit's own spine. Lead with the volume (119 KB of rationale for 45 KB of requirements). |
| 4.5 | MED | PARTIAL | Census holds. The fan-out detector fires for only 2 rows because 7 of the 9 over-bound SRs are re-stamped silent (SR-157 22, SR-148 16, SR-154/054/155 11, SR-244 10, SR-053 8). "Collapse LLRs into their SR keeping `module` as the pointer" is infeasible under the schema (no SR module cell; §2(b) forbids concrete names) and contradicts ruled decomposition (b) (LLRs decompose recursively under parent links) and "Module retires as a spine term". §7.1 is withdrawn in that form. |
| 4.6 | LOW | REFUTED | SN-001…004 are ordinary Approved needs; the four non-need rows are STK-01…04 in their own table by documented design; the kit's reader special-cases nothing. The miscount was the review's. |
| 4.7 | MED | PARTIAL | The gap is real and unlisted even in the enforcement audit. Three shipped surfaces disagree: §3 bans carriers, the template mandates them, the skill predicts the ban "gets bent silently". Ruled item 5's commit-time text check is the detector, sequenced "last"; the template-line fix is scheduled nowhere. |
| 5.1 | HIGH | PARTIAL → MED | The set is mis-drawn: 11 of the 34 modules test shipped behaviour or a shipped surface (`launcher_interpreter`, `hooks_on_routes`, `test_evidence`, `status_vocabulary_contract`, …) and two meta modules were omitted; corrected: ~25 modules, ~10.7k lines (6.8%), 49% of which is prose. The baseline dict holds 9 entries (modules over 1,000 SLOC) and was re-stamped in 277 of 2,986 commits because the ratchet is exact-equality in both directions; the shipped TSV churns too (38 re-stamps in 90 days) — the fix is a grow-only rule, not the carrier. `tests/` never ships, so the adopter cost is zero. Making the sensors warn-only reverses OI-68 (ruled 2026-08-30 with the evidence that advisories were not obeyed here). |
| 5.2 | LOW | PARTIAL → fold | True wording pins are ≈430–470 asserts (2.4%); 97% of long literals are pinned in one module, so a rewording is a one-module edit; the §6.3 causal link fails for its own example (`test_trajectory_holdban.py` pins two tokens). The heaviest pinners test prompt text, where the wording *is* the behaviour. |
| 6.1 | HIGH | PARTIAL (under-scoped) | Reproduced on a depth-50 clone: `approval-fresh`, `registry-integrity` and `open-items` FAIL; after `git fetch --unshallow` all 25 steps PASS. Only `registry-integrity` emits the "NOT byte-identical … has LANDED" text; the other two fail as STALE artefacts downstream of the same misattribution. The mechanism is one `git log --name-only` over the snapshot directory whose first commit at the graft boundary reads as the writer (`acceptance_record.py:1836-1856`); shallow handling exists in four separate implementations (`baseline_snapshot`, `retire`, `check_test_first`, `acceptance_record`) and `kitlib.git` has no `is_shallow`. The true writing commit is 2,349 commits back, so any depth below that misattributes. The shipped `ci/check.yml` checks out at the default depth 1 and fails `registry-integrity` on today's HEAD; the kit never saw it because its own CI fetches full history. A WARN in the integrity finding alone is not enough — the three consumers must receive "unverifiable" as a non-finding or the STALE cascade recurs. |
| 6.2 | MED | PARTIAL | Eight call sites and 491 route-test lines confirmed (plus a 241-line unit module for the detector). The slot re-check covers the pre-commit floor's rules and the bar, but *not* the commit-msg hook: a hooks-off lane's commit messages are never scanned and the loop-trailer check runs nowhere else. Two of the eight routes commit through plumbing or `git merge --no-ff` and never run the hook anyway, so there the refusal guards nothing. `setup.sh`/`setup.ps1` set `core.hooksPath`, so the cost falls only on a checkout that skipped setup — the cloud and CI case (and §9.1 shows the documented setup command fails under dash). The downgrade amends an Approved SR (SR-240), LLR-340, IF-297 and a CLAUDE.md line: a re-attest, not a patch. Alternative keeping the doctrine: refuse only where the route's own commits would run the hook; warn elsewhere. |
| 6.3 | MED | PARTIAL (re-anchored) | 80 words, not 90, and 2 of the 350 WARN lines. The rule is owner-ruled (OI-70) and enforced — WARN at the floor, ERROR under `--strict` from DevStg-Impl, this repo's stage. The real defect is a checkout-dependent false positive: the detector reads only `refs/heads/<lane>`, so it fires in any clone that did not fetch the lane branches (this session, CI, cloud) and vanishes when the refs exist. The shipped depth-1 CI therefore reds the `trajectory` step whenever any lane is active. Fix: consult `refs/remotes/*/<lane>` and report "unverifiable in this checkout" as a WARN, never ERROR. Same root as 6.1. |
| 6.4 | MED | PARTIAL (mis-anchored) | Reproduced: an unrelated staged file plus an unstaged SR text edit is refused — but by four working-tree freshness steps (`derived-stage`, `approval-fresh`, `open-items`, `trajectory-map`), while `registry-integrity` PASSED. The snapshot byte-compare refuses only a commit that *writes* a snapshot file or a landed forgery (`acceptance_record.py:1866`: "the snapshot is deliberately behind live while an amendment is pending, and that lag IS the signal"); it did not fire. Moving `approval-fresh` to the slot removes one of four FAILs; the lever is the floor's working-tree read — the index-reading destination OI-31 already records, or running a freshness step only when the staged diff touches its inputs. The anti-laundering rule (SR-179, Approved) should be left out of this finding. |
| 6.5 | LOW → MED | PARTIAL (understated) | At least six distinct failure policies across eight-plus reader functions for one file (refuse; read ON; read require; read ask; read the shipped default; translate-and-warn), and `privacy_review` has two readers with two policies. The file's own header documents two outcomes for the same event (IF-037 "a file that does not parse is refused" vs IF-038 "reads `ask`"). The proposed "warn and use the default" is unsafe as stated: `subagent_gate`'s shipped default is `off`, so an unknown value would flip a fail-closed gate open (OI-46 ruled against exactly that). Workable single policy: non-parsing file → refuse; unknown or wrong-typed value → the most restrictive value of that dial's alphabet, with a warning. 49 test files pin the current behaviours. |

**What the verification changes.**

- **Refuted:** 2.5, 4.6, and 3.3 as a shipped-skill problem. **Downgraded:**
  1.6 (withdrawn), 2.1, 2.2, 2.3, 2.4, 3.1, 4.2, 5.1, 5.2. **Confirmed with
  corrections:** every other finding; 1.7 fully.
- **The largest single correction is a document the first pass never
  cited:** the owner's ruled plan,
  `docs/plans/2026-10-11-review-churn/README.md` (revision 38, "Ruled: every
  item and call"). Its item 5 already rules the remedy for 4.1, 4.3 and 4.7 —
  no code carrier in any requirement row, `module`/`code_symbol` retire from
  the LLR schema, a commit-time text check, the TC evidence column generated
  from per-test tags in test files — and variant F / decomposition (b) rules
  that LLRs decompose *recursively* under authored parent links and that
  "Module retires as a spine term". §7.1's "collapse LLRs into their SR, keep
  `module` as the pointer" is the reverse of that ruling and is withdrawn; §14
  re-cuts it as "execute item 5, fix the templates first, re-tier in batches".
- **Two first-pass changes conflict with recorded rulings** and need a new
  ruling argued against the recorded evidence, not a work item: deleting
  `test_rule_sync` (D-7) and making the armed size/complexity sensors
  warn-only (OI-68).
- **§6.1, §6.3 and §6.4 share one root the first pass did not name:** floor
  steps read state the checkout may not carry — history depth, local lane
  refs, the working tree — and report its absence as a defect in the
  repository. One "unverifiable here → WARN with the repair" idiom in
  `kitlib.git` discharges 6.1 and 6.3 together; 6.4's lever is the recorded
  index-reading destination (OI-31), not the snapshot rule. The shipped
  `ci/check.yml` checks out at depth 1, so an adopter's first CI run on a
  repo with any pending amendment fails `registry-integrity` with a false
  "LANDED divergence"; the kit's own CI fetches full history and never sees
  it (§10.9 reproduces the same fact independently).
- **The first pass over-weighted code duplication and under-weighted two
  things the second pass surfaced:** the kit's own detectors are blind to
  the altitude defects (§11.4), and the shipped templates manufacture them
  (§10.1). Those two are where the leverage is.

## 13. New findings — six finders, one per dimension

**Method and status.** Six independent finders each took one dimension with the
first pass and §8–§11 as "already found", and returned new findings with
anchors, numbers and a reproducing command. Their scripts are in `measures/`
(prefixed by dimension), the test classification data in `tests-census/`, the
refusal inventory in `guards/TABLE.md`. **Adversarial verification:** seven
refuters (two with different lenses over the spine findings) re-measured each
finding and checked each change against the owner's ruled plan; their verdicts
close each sub-section below. Findings that only extend an
earlier section are folded into one line that names it.

### 13.A Surface area and operating cost

**[HIGH] 13.1 The declared per-commit bar is the smoke tier, not the hook.**
`CLAUDE.md:59` names `run.cmd smoke` the per-commit bar; its `[run]` line runs
`trace.py --strict` (6.9 s), `check_trajectory.py --strict` (27.2 s),
`check_docs --stale` (3.4 s), `check_resync` and the smoke tier, which collects
3,384 of 7,700 tests (44% of the suite) under a budget of 540 CPU-s / 600 s
wall; the latest handoff records 531 CPU-s for one landing. A "smoke" tier that
is nine CPU-minutes and half the suite is a full run by another name, paid on
every commit; §1.4's 33 s under-reports the declared bar by an order of
magnitude. The `[smoke-budget]` section is 937 comment lines for 3 values, with
98 "re-stamp" mentions. *Change:* invert the tier default (a test is smoke only
when its module opts in), target under 60 s, move the rest to `full` at the
merge slot; the section becomes three lines. Adopters are untouched (their
`stack.ini` seeds only `[tiers] smoke = -m smoke`).

**[HIGH] 13.2 `RESYNC_PACK.md` §4 is the kit's changelog in disguise, and it
grows ~120 KB a month.** §4 "concept renames" is 475,709 of 643,982 bytes (74%)
and holds 207 entries, 12 of which contain a rename; the newest are titled like
commit messages. Dated by `[since <sha>]`: §3 migrations got 2/30/46/5/0/0
entries from June to November while §4 got 46/60/87/7 — the switch coincides
with `scripts/check_resync.py` refusing any change to a shipped file that adds
no §3/§4 heading, so every lane adds the cheapest heading that passes the
grammar (164 entries carry the same boilerplate line). An adopter stamped
2026-08-15 who re-syncs today has 35 §3 + 197 §4 entries in range: 558 KB,
~93,000 words. That is a re-adoption, not a re-sync. *Change:* the entry
becomes a row (`since`, `class` migrate|rename|none, `action`, optional prose
pointer) in a shipped `migrations.toml` that generates §3/§4 and that
`check_resync.py` checks; `class = none` rows render as one line, which is what
195 of the current entries are; a byte/entry ratchet on the generated pack.
Pairs with §10.10.

**[HIGH] 13.3 The record has split in two: `docs/log.md` ("append-only
history") last changed 2026-09-05, and 159 uncompiled fragments sit in
`docs/log.d`.** `trunk_step.compile_log` folds fragments into the log and is
called only by `integrate.py refresh`; `refresh:` commits were 57 in August, 46
in September and zero since, because the hand-squash landing the recipes now
prescribe runs only `trunk_step.py --regen` (`coordinator-cycle/references/
recipes.md:642`). `log.md` is byte-identical at the 09-15, 10-15 and 11-05
snapshots; 18 kit scripts cite it as the record; nothing warns. *Change:*
either add `--compile-log` to the hand-landing recipe and a floor WARN when
`docs/log.d` holds fragments older than N landings, or declare `docs/log.d` the
record and retire `compile_log`. Pick one; today both homes are live and
neither is complete.

**[HIGH] 13.4 (extends §8.1) A quarterly re-sync is not performable as
documented.** For an adopter stamped 2026-08-15: 240 kit files changed (100
added, 4 deleted, 5 renamed), 147 of 149 scripts touched, 232 pack entries
(558 KB), 13 hook revisions, 24 `check.py` revisions. The pack's own §1.1
assumes "a handful of entries". *Change:* a release cadence (monthly or
quarterly tags), one migration table per release, `bootstrap --sync-kit <tag>`
taking overwrite-class files wholesale with a diff summary; per-commit `[since]`
entries become internal.

**[MED] 13.5 `docs/open-items.html` renders 1,071 unreviewed delegated
decisions as cards.** `docs/decisions/` holds 121 files with 1,122
`[decision.D-###]` rows, 1,071 of which have no `owner` field (48 confirmed, 3
overruled); the page carries 1,082 cards (1,073 D-rows, 9 open items) and is
regenerated and byte-compared on every commit (9.4 s). A queue that grows ~10 a
day and is never drained is a backlog rendered as a brief. *Change:* render only
`high_risk` decisions plus a count per lane; auto-expire low-risk rows into the
record after N landings.

**[MED] 13.6 `open-items.toml` is 92% ruled history parsed on every commit.**
110 of 120 rows are `ruled`; the header itself says "A ruled row is history, and
the Decisions log is its record"; a row averages 7.3 KB (OI-14's decision cell
alone is 16,149 chars); `one_line` has median 323 chars (max 1,504), 97 rows
exceed 200. *Change:* at ruling, `intake.py` moves the prose cells into a
`docs/log.d` fragment and leaves a five-field tombstone, or moves the row under
`docs/archive`; a warn-only 160-char advisory on `one_line`.

**[MED] 13.7 (extends §1.5, §10.15) 104 handoff files at the `docs/` root are
read by nothing but one exemption list and one "find the newest".** 1.15 MB,
85 written in October; the skill's own rule says a handoff holds state only and
"earlier handoffs are history". *Change:* one `docs/handoff.md` overwritten in
place with the derivable state block generated, and the 103 moved under
`docs/archive/handoffs/`.

**[MED] 13.8 The commit floor's step list lives in two homes and a test pins
them equal.** `hooks/pre-commit:288` hard-codes 25 step names; `check.py`'s
step tuple carries no "floor" attribute; `tests/test_commit_floor_census.py`
exists to hold the two consistent. The hook changed 62 times as the list grew
7 → 12 → 17 → 22 → 25, each change a kit-owned file every adopter must re-take.
*Change:* a `floor` field on the step tuple and `check.py --floor commit`; the
hook becomes one line that never changes; the census test retires. (Found
independently by the duplication finder.)

**[MED] 13.9 Configuration is spread over ~24 extensionless `docs/<word>`
files plus two dial files that are 82–92% comments.** The "one policy home"
fold (RESYNC §1.3) covered three files and stopped; `agents-enabled`,
`blackout`, `complexity-baseline`, `coverage-floors`, `declared-absences`,
`flag-axis-baseline`, `id-watermark`, `*-allow` (5), `okf-export`,
`status-lint`, `subagent-gate`, … remain, read by three different readers.
`process.toml.template` is 434 comment lines for 41 values; this repo's
`stack.ini` 1,251 for 94. A dial file whose values are 8% of its bytes is read
as a document, not a config. *Change:* fold the dials into `process.toml`
sections and the baselines into one `docs/baselines.toml`; one reader in
`kitlib.config`; measurement history out of `stack.ini` into the log.

**[MED] 13.10 The CLI surface an adopter must learn: 60 entry points, 37
subcommands, 202 distinct flag spellings (167 used by one script), 19 shell
launcher files for 4 commands, 20 identifier families.** `check.py`'s docstring
promises "one command that runs every quality gate"; the kit around it is
sixty. *Change:* one `kit` dispatcher over a `kitlib.cli` shell (§2.4's enabler)
with the scripts as subcommand modules; one launcher per OS; shims for one
release.

**[MED] 13.11 The floor spawns ~32 interpreters per commit and re-parses the
spine in each; the gate-only `check_test_first` replays every registry commit
with no cache (27.8 s, growing with history).** 7 of the 47 registered steps are
`check.py` re-spawning itself. *Change:* one process, one parsed spine handed
to the step modules; a cache keyed by registry blob for `check_test_first`.

**[LOW] 13.12 Skill fan-out tracks 437 KB of byte-identical copies
(`.claude/skills`, `.agents/skills`) and runs a per-commit `skills-sync` step to
prove they are identical.** `skills/README.md:107` names the alternative
(gitignore and regenerate on setup) as "deferred until a real need earns it".
The 17 domain skills are ~1.2 KB stubs; the recurring cost is the fan-out, not
the content. *Change:* the README's own deferred design.

**Verification of 13.A** (one skeptic; every number re-derived in a fresh clone,
the smoke tier run twice). 13.3, 13.5 and 13.12 CONFIRMED; 13.4 and 13.7 are
duplicates of §8.1/§10.10 and §10.15 (their new pieces — the adopter's
quarterly load table and the generated single-handoff form — are folded there);
the rest PARTIAL:

- **13.1 → MED.** `SLOW_MODULES` lists 139 modules, not 21. On a quiet 4-core
  box the declared bar costs ~38 s of lints plus ~98 s of tier (≈115 CPU-s), a
  sixth of the full suite by time; "nine CPU-minutes" is the owner's box and the
  540 budget is calibrated to it. The opt-out default is an owner-ruled design
  (2026-10-20), and moving the comment history out of config is already ruled
  (plan item 10 step 4). What stands unruled: a ceiling re-stamped 72 times
  sitting 0.7% above the live count.
- **13.2 → MED.** Substance holds (195 of 207 are not renames; §3 stopped in
  September; `check_resync.py` created the incentive). 22, not 35, hand-step
  entries. Mechanising the pack contradicts ruling 10 ("re-sync is carried out
  mainly by an LLM, so it doesn't need to be mechanized") and the pack's own §5
  promotion trigger; the finding must argue the trigger has fired. The
  byte/entry ratchet is the unruled, cheap piece.
- **13.3 CONFIRMED, MED.** `--compile-log` already exists (`trunk_step.py:667`),
  so the fix is one recipe line; `recipes.md:823` records the hand-landing as
  temporary "until the one-landing row moves coordinator landings onto the slot"
  — the route change was recorded, the compile dependency it broke was not.
  Fragments: Sep 46, Oct 105, Nov 18.
- **13.5 CONFIRMED.** Inflow is ~32 a day, not ~10; high-risk-first is already
  the render order; `docs/status.md:648` already shows "Decisions to review:
  1070". Auto-expiry changes what "delegated decision" promises the owner — an
  owner call; the per-lane count is the safe first step.
- **13.6.** "The kit carries each ruling twice" fails: the log records 16 OI
  rulings, so for ~94 ruled rows the registry cell is the only record. The
  tombstone proposal stands but must write the record first. Sizes hold.
- **13.8.** The census test is 139 lines; there are three homes, not two (the
  hook line, the absent attribute, `_TRUNK_FRESHNESS_STEPS`); the hook also runs
  `format` by name with the staged file list, which the new field must encode.
  Merge with §10.14's level table.
- **13.9.** "~24 files" conflates 12 live declared files with legacy names and
  generated stamps, and ~10 policy files were folded, not three. The dial fold
  and the history move are **already ruled** (plan item 10, "one TOML file",
  4–6 WIs); filing them again risks a second adopter migration, which the ruling
  explicitly avoids. The unruled remainder: eight allow-list/baseline files and
  three readers.
- **13.10.** `--root` is in 47 scripts; the 19 launchers serve 8 commands. The
  proposal is under-priced: a `kit` dispatcher renames 60 script paths at once
  (plan item 11 counts 203 of 243 IF owners as `scripts/…` paths) — the largest
  §4 rename the kit would ship, landing in the pack 13.2 calls unreadable. Do
  §2.4's shell first; a dispatcher only after item 11 makes paths generated.
- **13.11.** `check_test_first` is gate-only, not per-commit. A single-process
  floor collides with the hook's ruled design (ruling 6: "the pre-commit hook
  stays as it is") and with adopters' own `[step:*]` commands, which are
  subprocesses by contract. New and low-risk: a gitignored cache for
  `check_test_first` keyed by registry blob.
- **13.12 CONFIRMED.** The kit's stated flip trigger is "agent-specific
  frontmatter"; the finding should argue the trigger is mis-set.

The finder's five counter-findings against the first pass all **hold** and are
stronger than stated: 21 shipped scripts read `docs/reviews` and 13 read
`last_approved`; 57 scripts insert `sys.path`; the refresh route has had zero
commits since September, so "move the step to the slot" moves it to a route
nobody runs until the one-landing row lands.

### 13.B Code duplication

**[HIGH] 13.13 Two "one owning boundary" rules for which spec copy governs,
and they pick opposite copies.** `agent_policy.authoritative_spec` ranks
`docs/archive/work` above `docs/work`; `kitlib.done_when._copy_at`/`spec_at`
take `max(hits)` over a folder list where `docs/work/*` beats
`docs/archive/work/*` and a closed copy beats the active one. Three call sites
go through the first, twelve through the second; reproduced: for the same tree
they return different files. Duplicated *policy*, not plumbing. *Change:* one
precedence table in `kitlib`; `authoritative_spec` delegates.

**[HIGH] 13.14 The generator freshness arm is written nine times and the
generator set has four homes.** Every `gen_*.py --check` hand-rolls render,
read, compare, STALE, exit, write; the copies diverge on adopter-visible
decisions (a missing output is "nothing to check" in `gen_arch_map` but
STALE/exit 1 in `gen_components` and `gen_open_items`; STALE goes to stderr in
four, stdout in three; `gen_skills_index` calls `sys.exit`). Which generators
exist is then restated in `check.py` (one step each), `trunk_step.REGEN_STEPS`,
`docs/stack.ini [generated]` and `test_generated_freshness_wiring.WIRED`; every
new artifact is five edits plus a meta-test. *Change:*
`kitlib.generated.check_or_write(...)` and one `GENERATORS` table the steps, the
regen and the wiring test all read.

**[HIGH] 13.15 458 module-level re-export aliases (287 hops through sibling
scripts) make three modules façades; four names are bound twice.** When
behaviour moved, the old module kept `name = new_home.name`: `check_trajectory`
112 aliases, `agent_loop` 108, `agent_common` 71; `check_trajectory` binds
`_first_declared_line`, `_process_check`, `_split_refs` and `OPEN_ITEMS_REL`
twice (the later wins). 77 of 278 test modules load the three façades, so the
aliases are kept alive by tests, not production callers. *Change:* delete the
aliases; callers import from the home.

**[MED] 13.16 The `<key> — <reason>` declared-file grammar has five readers
and four copies of its parse finding; one accepts a hyphen the others refuse**
(`check_need_form`, `trace`, `trajectory_arch` ×2, `check_doc_refs`). *Change:*
`kitlib.declared.read_entries`.

**[MED] 13.17 `docs/process.toml` is opened and parsed at nine sites, five of
them inside `kitlib.config`, each with its own fail-direction arm**; 54 raw
`tomllib.loads` sites and 27 modules with their own `TOMLDecodeError` arm
remain. The policies are deliberate (§6.5); the *parse* is copied. *Change:*
one `process_toml(root)` read; dial readers take the parsed mapping and apply
their policy explicitly — which makes §6.5's one documented policy a one-line
change later.

**[MED] 13.18 Marker-block knowledge is spread over ten homes.**
`traj_status._splice_status` is a copy of `gen_arch_map.splice_region`; the
"skip GENERATED blocks" loop exists three times (one reads `utf-8-sig`, two
`utf-8`, so a BOM'd `status.md` is handled differently by the lint and the merge
slot); `_STATUS_GENERATED_RE` is defined identically twice; the STATUS marker
literal lives in 6 modules, `stack.ini.template`, and 7 test files, although
`[generated]` already declares the pair per artifact. *Change:* `kitlib.markers`
reading the pairs from the profile.

**[MED] 13.19 Row-id regexes: 35 compile sites, no `kitlib.ids`; the WI
token regex is diverged in one copy** (`trace_text.py:325` is `IGNORECASE` with
no trailing `\b`, so `wi-12x` is a WI token to the citation detector and to
nobody else); the tier-prefix list is hard-coded twice and differs. *Change:*
`kitlib.ids`.

**[MED] 13.20 "Text of a path at a revision" has five readers with four
contracts; one swaps the argument order and one reads the working tree where
the others read the index for `rev=None`**; 42 hand-formatted `git show
rev:path` sites in 23 modules. *Change:* `kitlib.git.text_at(root, rev, path)
-> (text, why)` keeping the ABSENT/UNREADABLE split the Done-when rules depend
on.

**[MED] 13.21 The current branch is read at 14 sites with two git commands
and different detached-HEAD behaviour; "which WI ids does a lane hold" has four
readers over two read models**, one of which imports the 3,700-line
`integrate.py` to avoid copying a function that `kitlib.git` already holds.

**[MED] 13.22 Nine live copies are still licensed by the retired F5 rule, and
one has diverged.** `check._split_template` and `agent_session.split_cmd`
tokenise the same command grammar, but only the loop sets `lex.commenters = ""`:
a `stack.ini` command with an unquoted `#` token is truncated by `check.py` and
run whole by the loop (reproduced). `integrate._RETIRED_BARS` duplicates
`intake.normalize_bar`'s table (equal today); `bootstrap.LEGACY_DIAL_ORDINALS`
copies `kitlib.authority`'s with a justification ("bootstrap imports no kit
sibling") that no longer holds. 71 `F5` mentions remain in scripts. *Change:*
import the home; drop the matching `rule_sync` pins; grep `F5` to zero.

**[MED] 13.23 Spec frontmatter (`+++`) is parsed four ways**; two of the
copies accept shapes the home refuses (a regex that reads CRLF differently; a
`split("+++", 2)` that treats a `+++` in the title as a fence).

**[MED] 13.24 The Python-3.11 interpreter probe is written in 11 launcher and
hook files with two different Windows candidate orders**, only seven of which
a test holds equal; on a Windows box where `py` and `python` resolve to
different installs, `run.cmd` and `agent-resume.cmd` pick different
interpreters. `hooks/kit-python.sh` already shows the shape (one sourced probe
for three hooks). *Change:* `kit-python.{sh,cmd,ps1}`.

**[MED] 13.25 Adopter-facing regeneration hints hardcode this repo's kit
path.** The generated status block, the open-items page header, the
pending-actions briefs and the dashboard footer tell every adopter to run
`python project-trajectory/scripts/…`, a path that does not exist in their
repo (the footer contradicts itself in two lines); `agent_brief.scripts_dir`
resolves it correctly and is used by one module. CLAUDE.md's own rule: a token
the kit mandates must mean something in the adopter's repo. *Change:*
`kitlib.config.kit_scripts(root)` used by every hint.

**[LOW] 13.26–13.30 Smaller duplicates:** three dead copies of the registry
CSV loader kept alive only by tests (`check_trajectory.read_rows`,
`schedule.load_rows`, `gen_okf.read_rows`; the live fourth differs from the
`kitlib` home on encoding); nine Markdown heading regexes in four grammars and
six section extractors with three termination rules; the cell normalisation
`(row.get(k) or "").strip()` inlined 247 times in 45 modules beside five named
`_cell` copies; two identical light/dark palettes, three HTML escapers (the
`trace.py` one lacks `'`), two Mermaid emitters, 46 raw `endswith("-000")`
sites beside `is_example`; 59 try/except import prologues that write 242 import
lines twice, 162 hand-prefixed log lines, and four floor steps that spawn
`python -c pass` when a kit-only generator is absent (two of them on every
adopter commit, since `gen_skills_index.py` is not in the manifest).

**Verification of 13.B** (one skeptic; the finder's eight scripts re-run in a
clone, 13.13 reproduced with a git fixture, 13.22 with `stack.ini`-style
commands). Twelve CONFIRMED (13.16–13.18, 13.20–13.23, 13.26, 13.27–13.29),
eight PARTIAL; none refuted:

- **13.13 → MED.** Precedence-bearing `done_when` callers are 3 external + 1
  internal, not 12; `adoption_record` carries a third policy (refuse on
  ambiguity). The headline case (archive ranked above work) needs the same WI in
  both homes, which no kit route writes; the realistic trigger is an active copy
  beside a closed copy under `docs/work`, where `authoritative_spec`'s
  alphabetical tie-break picks the ACTIVE copy against its own rationale — a
  real defect in its own right. `review_brief.py` reads the same spec under both
  rules (`:257` vs `:688`).
- **13.14 → MED.** Two stdout writers, not three; three no-op CRLF replaces. The
  missing-file divergence is a deliberate opt-in posture for optional docs, so
  the helper needs a per-generator missing policy. A single `GENERATORS` table
  cannot live in `kitlib` as proposed: `REGEN_STEPS`' component predicate imports
  `spine_carrier`, which `kitlib` may not.
- **13.15 → MED.** The four double bindings rebind the same object (redundancy,
  not a defect). `agent_loop`'s aliases are mostly its own call sites and
  `agent_common` is the shared layer by design; 239 internal call sites would be
  re-pointed, and five traced LLR rows plus TC-193 record the façade as the
  delivered shape ("re-exports every name under its former spelling so no caller
  had to move") — the re-tier (§11) has to go first.
- **13.16 CONFIRMED (+1).** `check_doc_refs.py:348` reads `utf-8` with no BOM
  strip where the other four read `utf-8-sig`: a BOM'd declared-absences file
  hides its first entry.
- **13.17 CONFIRMED.** `observation_cadence` has no fail arm at all (a tenth
  policy: crash); `authority.dial_from_config` reads the file at a revision, so
  the shared parse must take text, not a path+mtime cache. Already a recorded
  consolidation row (`docs/status.md`, wi-962/wi-958).
- **13.19.** Three in-text WI token shapes among six copies; the anchored id has
  six copies, not five; `trace_text`'s case-insensitivity is deliberate for
  prose, so the one home needs a prose variant.
- **13.20–13.21 CONFIRMED.** `plan_coverage`'s working-tree read is a different
  *source* and stays a separate call, not a flag; the claim-reader half is
  already a `status.md` row (wi-960).
- **13.22 CONFIRMED.** `kitlib.shell_line` is the wrong home (it reads whole
  shell lines for the guard); the right one is `agent_session.split_cmd`. Live
  impact of the `#` divergence is nil today; it is a reachable latent one.
- **13.23 CONFIRMED (+2).** `intake.py:341` and `:2177` add a fifth, CRLF-
  tolerant grammar: five grammars across six sites; partly recorded (wi-856).
- **13.24.** `tests/test_launcher_interpreter.py` does execute the launchers for
  the venv-first and 3.11 rules; only the PATH-candidate *order* is unpinned.
  Only 4 of the 11 files are kit-owned: the `run.*`/`agent-resume.*` launchers
  are adopter-owned ("preserve always"), so the fit is a kit-owned probe per
  dialect that adopter-owned launchers `call`.
- **13.25.** ADOPTING tells adopters to keep the kit at `project-trajectory/`
  "alongside or inside"; inside, the path resolves to the kit's copy. The defect
  is inconsistency across eight surfaces. Move `agent_brief.scripts_dir` into
  `kitlib` rather than add a second resolver.
- **13.26–13.30.** Bypass sites are 11, not 18 (seven are the wrapper bodies);
  the heading regexes reduce to four generic grammars across five modules
  (`sitting`'s narrow one is deliberate); the `_pget` half is ruled by plan item
  10 step 1; the vacuous spawns are §9.4.

All eight of the finder's counter-findings cite real constraints
(`kitlib/__init__.py:26-30`, `test_import_layers.py:52-62`,
`test_bootstrap.py:1680-1710`, OI-46 1a) and seven hold as written.

### 13.C Architecture prose and skills

**[HIGH] 13.31 The IF row count is produced by the "every module is an
endpoint" warn, not by decomposition decisions.** PROCESS_OPTIONS says the
connectivity warn is "warn-first FOREVER … every arch-map module is a declared
IF endpoint" and PROCESS §8 makes the layer default-on; the rubric says
"Inside a component, interfaces are optional" and the deep-module skill says
"the cost of a module is its interface". The warn wins: 106 of 121 kit modules
are IF endpoints, 149 of 255 rows have both endpoints inside one component, 73
are in-process calls with exactly one requestor, and OPTIONS' own estimate of a
fully-declared repo is "~30–35 hand-authored IF rows" (7× fewer). The cells
meant to make rows cheap are unused: `verified_by` 0/255; all 255 `Drafted`,
240 `v1`. Each row costs a header body (224 bodies, 203 KB), a TC citation or an
allowlist line, a `Data` cell whose symbols must resolve, a planning-brief row.
*Change:* delete the every-module warn; record a seam only when it crosses a
component boundary or leaves the repo; collapse the cli/exit-code/stdout
triples (13 and 6 owners) to one row; retire or make opt-in `verified_by`,
`version`, `status`. The kit's own registry can drop ~149 rows. (Check against
ruled item 11, variant F.)

**[HIGH] 13.32 No home exists for the decision a boundary hides.** Four
shipped texts each demand a different "stopping record" and name no field
((d2) in OPTIONS, spine-questions §3, rubric A8, SR-165); LLR-172's own detail
ends "NOT BUILT YET: the record cells do not exist on the CMP schema today";
the skill sends the result to "the component registry's partition record",
which `grep` finds nowhere. What exists: four CMP rows whose `notes` list
modules — the rubric's own B3 tell ("Its description lists its parts instead
of naming a decision it hides") — and a 129 KB plan folder SR-165 says is the
wrong home. *Change:* two optional CMP keys, `hides` and `stops`; the four
texts point at them; delete or re-scope SR-165/LLR-172; the Arch rung exits
"when every CMP row names what it hides"; a warn on an empty `hides`.

**[HIGH] 13.33 "Architecture is derived, never committed" is contradicted by
three committed generated architecture docs the floor keeps fresh.**
`docs/interface-reference.md` (229 KB, 108 commits, 17 MB of blobs),
`components.derived.toml` (94 commits) and `cli-reference.md` (57) are
mandated by §8 and the `interface-reference`/`component-view`/`cli-reference`
steps. PROCESS §3 spends 40 lines (372 words) on the `--doc`/`--flow`
marker-routing path the kit retired from its own floor at WI-455 and that no
live Markdown here carries; the "Routing" paragraph contradicts itself in two
sentences. Sentence census: §3's architecture prose is 50% machinery, §8 34%
method / 66% machinery. *Change:* state the true invariant, choose one posture
for the three committed docs (prefer gitignore + CI publish, §8.2), cut
§3:375-414 to four lines.

**[MED] 13.34 Two competing "contract at the code" formats.** AGENTS teaches
an Inputs/Outputs/Config/Raises block that "the code map harvests"; the kit's
code uses it in 6 places, `gen_arch_map.py` contains no handling of it, and §8
mandates a different block (224 `Contract IF-###:` bodies). *Change:* one
shape; delete the harvesting claim.

**[MED] 13.35 The runtime-flows rule is stated in three homes, enforced by
none, and not followed by the kit's own flows.** "Participants are the planned
modules (the LLR `Module` column)": `check_flows.py` checks headings, a fence
and cited ids only; the kit's `runtime-flows.md` names 38 of 49 participants in
prose (the readable ones), 0 dependency-table rows, flows 4–9 are station
internals, and the section opens with a 17-line drift-history block plus 7
WI/OI citations in a living doc. *Change:* relax the rule to roles-or-modules
(or a 10-line WARN that a module-shaped alias resolves); delete the history
block; stop routing the A4 table there.

**[MED] 13.36 The planning briefs embed all 255 IF rows verbatim (~48 KB,
~12k tokens) in every dual-plan planner and critic brief**, and §8 states this
as a feature. *Change:* filter to rows whose owner or far side intersects the
work item's scope plus boundary rows.

**[MED] 13.37 Rubric A3 ("a call states its typed request and answer, without
symbol names") contradicts §8's `Data` cell ("a named symbol or path must
resolve", enforced by `trace.py`)**; 112 of 255 `Data` cells carry a symbol or
path; EXAMPLE §9 puts behaviour in the body A3 assigns to the requirement. An
adopter cannot satisfy both with one cell. *Change:* `Data` is the typed form;
drop "must resolve" and its advisory.

**[MED] 13.38 Provenance in the shipped OPTIONS architecture layers (13
WI/OI/ruling citations in ~310 lines) and in both architecture allowlists (all
7 `kernel-modules-allow` entries open "WI-448/OI-48(d):").** Extends §10.11.

**[MED] 13.39 The rubric's SCR/Parnas grounding is cited, not explained:** ten
author-year citations with no title or gloss; three defined terms used by no
anchor; the one knowledge pack that explains the methods
(`docs/knowledge/system-decomposition-methods.md`, 16 KB) is neither shipped
nor cited. *Change:* a half-line per citation, delete the unused terms, ship or
drop the pack.

**[LOW] 13.40–13.44 Smaller:** the `(d2)` label names two different rules in
two shipped files and the skill cites a bare "(d2)"; EXAMPLE §9, the only
worked architecture example, shows seam bookkeeping but never applies A1–A8;
the derived component "partition" places 34 of 162 modules in two or more
components because membership is a projection of LLR `Module` tags, while A6
demands one owner; the seam-TC "migration allowlist" grew 116 → 147 entries in
eleven weeks (a permanent exemption surface with a longer name — make the
check WARN at every gate and delete the list); the IF owner rule is stated 7
times in 5 files and the IF column semantics in full 4 times (the concrete cut
list for §3.1).

**Verification of 13.C** (one skeptic; every count re-derived, the `hides`/
`stops` probe run in a clone, each change checked against ruled items 11 and
12). One finding refuted (13.43), two duplicates (13.41's template half →
§10.1; 13.44 → §3.1, where its census is the cut list §12 lacked), one
CONFIRMED (13.40), the rest PARTIAL. Five proposed changes collide with a
ruling and three are already ruled in the finder's direction:

- **13.31 → MED.** "149 internal seams" counts (row, component) refs: 132
  distinct rows are internal to at least one component view, 106 of those are
  boundary seams in another view (the 34 multi-component modules of §13.42),
  and only **26 rows (10%) are internal in every view**; 229 cross a boundary,
  as §12-3.2 records. The warn-produces-the-rows causation is plausible (87% of
  modules are endpoints; the warn still fires on 20) but not demonstrated.
  Variant F already requires interfaces "at every architectural boundary at
  any depth; optional inside" and names the per-module warn as something item
  11's migration "must migrate explicitly" — sequence (1) and (2) inside that
  phase. Collapsing the cli/exit-code/stdout triples contradicts OI-67 (a)'s
  one-row-one-channel rule; `status` must stay (OI-112 approves interfaces
  through sittings) and `version` is what a consuming side pins.
- **13.32 HIGH stands.** Facts hold (an Approved, Test-verified requirement
  unbuilt for 11.7 weeks; four incompatible specifications; the B3 tell).
  Corrections to the change: SR-165/LLR-172/TC-166 are Approved rows under
  SN-040 — deleting them is an amendment act and re-orphans the need unless
  `hides`/`stops` is minted as its replacement SR (the finder's own cheaper
  route, moving SR-165 under the dual-plan layer, is better); the skill's line
  18 ("the procedure never adds a file or a field") must change with it; rubric
  A8's four descend tests are ruled text (F-call 6) and stay. The cells
  themselves are unruled and compatible with ruling 5; the loader ignores
  unknown keys (probe).
- **13.33 → MED, and the gitignore route needs a re-ruling.** The `:193`
  invariant is scoped to the module map, import graph and seams; the committed
  `interface-reference.md` is **OI-66 ruled (a) GO** after a priced build, and
  §8 states it explicitly — a deliberate exception, not drift. The squarely
  contradicting file is `components.derived.toml` (25 KB). The three files'
  21 MB of history is 0.5% of §8.2's. Neither reference ships in the manifest
  (the step is vacuous when the doc is absent). The prose fix to `:193-196`
  and the 40 retired-routing lines stands; the anchor `pre-commit:288` should
  read `docs/stack.ini:1318`.
- **13.34 → LOW.** `gen_arch_map` *does* harvest the one-line summary and
  `Implements:` back-links the sentence claims; what is unharvested is the
  Inputs/Outputs/Config/Raises fields it never claimed. The two shapes describe
  different objects (a function's API vs the seam a module owns); the defect is
  the shared heading "interface contract". The proposed text is sound.
- **13.35.** "Flows 4–9 are station internals" is a judgement (for the
  station's operator the coordinator is the user); the provenance anchor is
  `AGENTS.template.md:182`, not PROCESS §3. Option (a) is **already ruled in
  substance** (revisions 35/36 retire "Module" and name `RUNTIME_FLOWS.template`
  in the sweep); option (b) would be built on the cell item 5 retires. Mode
  classes *are* ruled to live in `runtime-flows.md` (item 12); re-home the A4
  table only after 13.32's cells exist.
- **13.36.** The rendered surface is 52,889 B (~13k tokens), and the SR
  surface (55 KB) is as large and omitted. Aligned with the ruled build-brief
  component-context block (item 11); apply the same derivation to both slots.
- **13.37 → execute, don't decide.** The recommended option **is the ruled
  one** (item 11 decision 2: "a `call` form is its typed request and answer
  without symbol names"; F-call 9 makes `data` the form's home until generated
  from the body). `PROCESS.md:1318` and the template are pre-ruling text
  awaiting phase 3; strike the alternative; the EXAMPLE sub-change conflicts
  with the owner's Terms.
- **13.38 → LOW.** `kernel-modules-allow` and `if-tc-coverage-allow` are not
  shipped (absent from the manifest), so the provenance there is legitimate
  this-repo data and the kernel list's grammar *requires* a reason per entry;
  the finding holds only for the 13 tokens in the shipped OPTIONS layers.
  Extends §10.11.
- **13.39.** The rubric's ten terms are exactly the ten of the plan's
  value-domain research §4, and **F-call 7 rules that all ten go into the
  rubric** — the deletion contradicts it. Glossing each citation and shipping
  or citing the knowledge pack stand.
- **13.40 CONFIRMED (LOW/MED).** Prefer the reverse of the proposed direction:
  F-call 6 makes spine-questions §3 the ruled home of the stopping and descend
  rules, so OPTIONS' "(d2)" should become the pointer.
- **13.42.** Both measures stand (§12-3.2's 14 multi-tagged LLRs; this
  finding's 34 modules named by LLRs of different components), and the 34 are
  what inflates 13.31's internal count. The root cause is **already ruled away**
  (variant F point 1: membership declared on the realization; LLR → CMP
  retires); the glob key would be a third home against ruling 5 — drop it.
- **13.43 REFUTED.** Every seam minted since 2026-09-01 (93) arrived with a TC
  citation and none was added to the allowlist, which has not grown since
  2026-09-05 (152 → 147): the growth was the migration seed settling. What
  stands: a stale "116" header and 16 prunable entries. WARN-everywhere-and-
  delete-the-list contradicts OI-43 (a) and variant F's derived check.

The finder's counter-findings hold in part: "derived map" is not an invariant
the kit keeps today (`components.derived.toml`), the 0→A→B rule is cited by §
from three shipped files so §3 cannot shrink to three invariants, "run the
procedure on the kit" is already ruled as item 12's `run.cmd audit`, and a hard
participants check would read the cell item 5 removes. The contract-body census
differs between the finder (224 / 203 KB), the kit's own reader (225 / 190 KB)
and §12-2.7 (228 / 334 KB) only by body-extent convention; cite the kit's
`module_contract_bodies` grammar.

### 13.D The spine and the prose that steers it

**[HIGH] 13.45 The schema defines an LLR as "a row that binds to a Python
symbol".** `REQUIRED_FIELDS['LLR']` makes `Module` and `CodeSymbol` non-empty
under `--strict-schema`, and `check_doc_refs.symbol_findings` is enforced as
"THE DECOMPOSITION FLOOR … rung 4 TERMINATES WHERE A TOKEN BINDS"; spine-questions
§3 then tells the adjudicator the cells "stay filled and binding … never return
a row for keeping them". Result: 1,995 symbol tokens across 331 LLRs (median
3; 45 rows list ≥10; LLR-270 lists 80), 113 rows span ≥2 modules, 10 anchor on
`main`, 12 name only non-`.py` files and are reported "discharge NOT
computed"; the anchor check itself emits 22 untraced tokens and 53 unbound
modules on the kit's own spine. This is the structural reason the rows regrow
after any re-tier (§8.1): a Test-verified SR must have an LLR, that LLR must
bind a symbol, so the rows mirror the code by construction. A Go or shell
adopter gets a per-row advisory about a discharge that cannot apply. *Ruled
item 5 retires both cells*; until it lands, make `CodeSymbol` optional and
derive binding from `Implements:` tags.

**[HIGH] 13.46 "Every SR and LLR → ≥1 TC" plus the triangle rule produce a
1:1 TC shadow of the LLR tier.** 285 of 331 LLRs have exactly one TC; 306 of
363 TCs verify exactly one LLR; 64 TC-N rows verify LLR-N by the same number.
The triangle rule requires the TC to cite the LLR's SR, a fact derivable from
`sr_refs` — the "second source that can disagree" the kit's own §6 forbids —
and spine-questions §3 says the opposite of the bar ("An LLR may be satisfied
by its parent's coverage"); the bar wins because it has an orphan check. This
names the two rules behind §8.4's ratio. *Change:* "every SR → ≥1 TC; an LLR
is covered by its SR's TC unless it names its own"; the LLR-without-TC orphan
becomes a warn-only count; `verifies` names the leaf and the report derives
the SR. (Check against ruled decomposition (b).)

**[HIGH] 13.47 (extends §10.1) The vacuous `expected` cell is dictated by
four shipped sentences, one of which licenses it outright.** The template
("Cite … by id (do not paraphrase)"), EXAMPLE.md (three "Satisfies SR-001
AcceptanceCriteria" cells and the prose "cites the acceptance criteria by id
rather than paraphrasing them"), the machinery reference ("cite … by id"), and
spine-questions §3: "For a decomposed row the honest AC is usually *the chain,
passing, closed over the clauses*" — which is "Satisfies SR-x via LLR-y" in
other words. 202 of 363 cells open "Satisfies"; 104 are nothing but the
pointer; no detector reads `expected`. *Change:* rewrite all four; a warn-only
`expected` advisory (cell is only ids, "Satisfies", "folded into").

**[MED] 13.48 The opposite failure: 32 TCs paste the LLR `detail` into
`expected`** (TC-398 at 98% word overlap with LLR-359; TC-278's is 1,709
chars); 46 `expected` cells exceed 400 chars. The same fact then lives in
three cells. *Change:* the one-sentence rule plus a warn at >300 chars and a
paraphrase advisory one tier down (the LLR-vs-SR one exists).

**[MED] 13.49 TC `method` has become the test module's table of contents,
and `in-lane.md` generates it.** 72 methods open "Run/Drive the … suite"; 25
list pytest function names as prose; 16 name an internal function; 186 exceed
500 chars; TC-205's is 15,874 chars beside a 7,943-char evidence cell. The
template gives `method` no guidance, and `spine-authoring/references/
in-lane.md:24` instructs "For each LLR, list what it states … and the TC
clause that verifies each". *Change:* template guidance (instrument and
scenario in one or two sentences, never a list of functions); in-lane.md maps
the arms on a scratch worksheet, not in the row; warn at >400 chars.

**[MED] 13.50 The TC tier is the coverage sink for the 255-row interface
registry.** `in-lane.md:39` closes every lane with "Each interface row the
change adds or alters has a citing TC"; 122 of 363 TCs cite an IF id; 35
verify ≥5 ids; TC-331 verifies 14. A TC that verifies six requirements is a
test module's manifest. *Change:* derive IF coverage from the LLR → module →
IF-owner join `trace.py` already has.

**[HIGH] 13.51 The adjudicator's question list never asks the end-user
question.** §0 opens "state to yourself the obligation it imposes: what a
builder must do, what a test must check"; §2 (1,592 words) asks about EARS,
hats, derived labels, absolutes, artifact tokens and fan-out; §3 (793) about
refactor-proof contracts and coverage. Nowhere is a row asked "who outside the
system notices when this is unmet, and what do they see?". The only
stakeholder-facing test is §1(d) at SN intake. The result in the sample: 8 of
14 SRs state kit mechanism or schema; 131 of 138 SRs are `Test`-verified and 0
are Demonstration, Attest or Critique, although PROCESS §4 spends ~330 words
defining those methods and EXAMPLE §7 models them. `KICKOFF_PROMPT.md:170`
does carry the end-user lens ("what does the user experience, and is it
safe/clear/recoverable?") as a DevStg-Reqs checklist, composed into no brief.
*Change:* one §0 bullet composed into every sitting — "Name the witness: the
party outside the system who notices when the row is unmet and what they see.
A row whose only witness is another module of this product is a design
decision: it belongs at LLR, or inside its parent" — and one line in §2(b):
"If the AC can only be witnessed by reading this product's own source or
registries, the row is at the wrong tier." This is the single cheapest change
in the record and the one every re-tier depends on.

**[MED] 13.52 (extends §10.5) Per-sitting method prose is longer than the
rows it judges.** Reproducing `tier_questions`: the first-approval brief
composes 2,712 words of questions for an SR+LLR+TC batch (3,406 with the body;
the amendment sitting 4,072 for all four tiers) against a median SR chain of
938 words (p90 3,652); ~700 words of §2 describe detectors the judge does not
run. An authoring session reads 6,973 words before writing a row; the SR
template row alone is 942. *Change:* cap each § at ~250 words, one question
per bullet; move the detector descriptions beside the detectors; target
`{questions}` ≤ 900 words for any tier set.

**[MED] 13.53 (extends §10.1) `KICKOFF_PROMPT.md` teaches "`LLR-###` ↔
code" and "design expectation (links SR, names module/symbol)".**

**[MED] 13.54 `EXAMPLE.md` models the altitude faults it warns against.**
SR-002 states a mechanism ("write the export to a temporary file and atomically
rename it"), LLR-002 restates it ("Write bytes to <path>.tmp, then rename"),
both TCs carry a pointer `expected` and node-id `evidence`, the prose says the
evidence column names "a pytest node id", and §5 then tags the Rust test
file-level — teaching the inconsistency §4.3 measured. The good parts (the SN
rows, SR-001, LLR-001 "Pure function: records → String … No I/O", TC-201) are
short and at altitude; an adopter copies the first chain. *Change:* a six-line
edit (If-then EARS for SR-002, outcome sentences, file-level evidence).

**[MED] 13.55 The `coincident`/`da_refs`/`delivered_with`/`form`
classification demands an essay per SR whose content is one of two stock
answers.** `coincident` is filled 71 times (15.8 KB), 50 of them the stock
phrase "the output is the outcome"; `delivered_with` 8/138, `form` 10/138; 28
SRs carry none and `trace.py` prints 148 "unclassified" lines about them; the
template says changing `coincident` re-opens approval. *Change:* derive it from
`form`/`da_refs`; delete the prose cell (needs one ruling that removing
boilerplate is CLARITY).

**[LOW] 13.56 `permutations`/`gen_cases.py` is taught as core (~900 words
across PROCESS, EXAMPLE, KICKOFF, the template; a 326-line script) and used in
0 of 138 SRs**; TC `parameters` in 26 of 363. It is also where an SR author is
first told to think in test inputs rather than user outcomes. *Change:* an
opt-in layer with an applies-when.

**[LOW] 13.57 `test_refs` is a dead reverse pointer** the template seeds as
`(see TC)` and 331 rows fill by hand ("(see TC-N)" 166, "TC-N" 66, empty 56,
the literal placeholder 10) — the inverse of `verifies`, which `trace.py`
already joins; nothing reads it. *Change:* delete the key.

**[MED] 13.58 `in-lane.md` tells authors to pre-fill node ids and symbol
names for code that does not exist yet** ("Their trace fields … name the tests
and symbols the build will create, and bind when the set is reconciled") — the
authoring step that yields the dead node ids and the 22 untraced symbols.
*Change:* name the test file and the module; symbols bind from `Implements:`
tags once the code lands.

**[MED] 13.59 (extends §10.4) The worker brief gives no TC-authoring
guidance; the reviewer brief has the right question ("does it drive the
interface the requirement names, not handler source? would it fail on a
plausible wrong implementation?") but asks it only after the fact.** 139 of 363
TCs are `Unit`; 26 methods say "in memory"; the sampled subtrees verify helpers
such as `_implausible_branch_notice`. *Change:* the reviewer's question moves
into the worker bullet and the TC template.

**[MED] 13.60 The altitude detectors are inverted on the live spine.** A
`trace.py` run prints 210 WARN lines: paraphrase fires twice and fan-out twice
against 252 identifier-laden details and 32 TC-copies-LLR cells, while the
absolute-term advisory fires on 388 cells (97% of SRs). A detector that fires
on nearly every row discriminates nothing and buries the two that fire on
something. *Change:* sample the absolute-term advisory (a count and five
examples); extend paraphrase to TC-vs-LLR; ship the identifier advisory.

**[LOW] 13.61–13.62 Smaller:** `requirement` cells carry compound obligations
the one-`shall` rule cannot see (SR-239 is 968 chars and eight obligations under
one `shall`; 60 of 138 exceed 300 chars) — a warn at >350 chars or ≥3 clauses;
the `scope: kit` spine-authoring skill and the composed questions carry six
ruling stamps and "the kit repository's ruling of record: `OI-72`" into every
adopter's sitting (extends §3.3, §10.11).

**Verification of 13.D** (two skeptics with different lenses: the mechanized
rules, and the authoring prose read in context; both checked every change
against the ruled plan). The pattern is clear and matters for §14: **the
diagnoses mostly hold, and most of the proposed changes are either already
ruled (item 5) or contradict a ruling (variant F, decomposition (b), revisions
8/15/35/36).** Only 13.51, 13.48, 13.54 and 13.56 enter as clean new findings.

- **13.45 → MED, as a measurement footnote to §12's item-5 correction.** The
  anchor rule needs ONE binding token (`check_doc_refs.py:592`); the 1,995-token
  lists are authoring on top of it. Both rules bite only from DevStg-Impl.
  The remedy is largely ruled (item 5 layer 1 deletes *both* cells and makes the
  loader refuse undeclared keys); where it differs it contradicts "Module
  retires" (rev 35), the owner's withdrawal of a per-module `Implements:`
  mandate (rev 15: "encouraged, not mandated … the dial measures it") and rev
  36's instruction that the §3 sentence stay until item 5's lane. A one-line
  `REQUIRED_FIELDS` relaxation would land twice; do it inside item 5. Nothing
  is scheduled: no queued WI touches the schema.
- **13.46 → MED.** The mechanism is misattributed: the SR citation on every TC
  is forced by `coherence._sr_orphan_findings` reading `Verifies` *literally*
  (an SR is uncovered unless some TC names it directly), not by
  `triangle_findings`, which only checks coherence when both ids are present.
  59 of the 64 same-number rows are the July 1:1:1 seeding. `PROCESS.md:821` is
  a third home. The proposed downward coverage runs against decomposition (b),
  under which coverage flows *up* (children plus an integration TC discharge a
  parent) — re-cut the rule there; changing `PROCESS.md:525` edits the
  DevStg-Tests bar every adopter signs.
- **13.47 → fold into §10.1** as extra anchors (the machinery reference's
  "cite by id"; EXAMPLE.md's five pointer rows and its `:177-179` sentence).
  `spine-questions.md:293-294` is over-read: it is an SR-AC sentence (TCs have
  no AC cell), and the preceding bullet already states the condition rule.
  `trace_text` does read `expected` for citation frames; what is missing is the
  vacuity detector §11.4 proposes. "Never an id" would collide with the Attest
  convention, where the TC's Parameters/Expected record who attested.
- **13.48 CONFIRMED, MED.** Two cells, not three (73% of evidence functions have
  no docstring); only 10 of the 32 copies open "Satisfies", so this is a shape
  distinct from the pointer. Fire rates on the kit's own rows: `expected` > 300
  chars 72/363; > 60% overlap with the cited detail 73/363.
- **13.49 → LOW.** The causal claim is **refuted by dates**: "Map the arms"
  first appears 2026-10-09 (WI-848); a 15,092-char `method` already existed at
  the 2026-09-15 snapshot (27 cells > 500 chars in August, 69 in September, 169
  in October, 186 now). In context the bullet is a judging worksheet. A
  400-char warn would fire on 210/363 (58%); the exemplar's shape is the
  target, not a cap. New: 25 test-name lists, 16 internal-function methods.
- **13.50 → LOW.** The generator is OI-43(a)'s seam-TC coverage rule (ERROR
  under `--strict` from DevStg-Tests; 154 of 255 seams allowlisted), not
  in-lane prose; IF rows also carry `VerifiedBy`. The proposed derivation runs
  through the `Module` cell item 5 removes and contradicts variant F; the ruled
  F-call 3 check already owns the symptom.
- **13.51 CONFIRMED by one lens, PARTIAL by the other — record at HIGH/MED.**
  The tier test exists in the kit's *frame* vocabulary (§2(b3): a row whose
  output crosses no boundary "is a design decision and belongs at LLR";
  `boundary_refs` filled on 137/138 SRs; §0 sends back "an acceptance condition
  nobody could observe"); what is missing is the per-row prose cue, and the SR
  classification is a hand reading. Consistent with item 5 layer 3; §0 is ruled
  text (WI-911), so add a bullet, do not reword the ruled ones. Still the
  cheapest change in the record.
- **13.52.** The sub-bullet weights are swapped: (c)–(c3) = 697 words, (d)–(d2)
  = 375. Item 14 wired the hat *questions* into the briefs deliberately — move
  the mechanics, keep the questions. A 250-word cap collides with pinned ruled
  text (`test_prompts.py` pins §3's rev-35/36 clauses) and §-letters other kit
  text cites. Keep the per-sitting totals as the measurement.
- **13.53 → fold into §10.1** (the KICKOFF anchors); ruled in direction (rev
  35's "Module" sweep covers "shipped text that uses it as a spine unit").
- **13.54 CONFIRMED, MED (+1).** SR-002 is `verification = "Demonstration"`
  while its TC-002 is `automated = "Yes"` with asserts. The evidence wording
  must follow the ruled tag design (per-test tags, generated column), not
  "file-level".
- **13.55 → LOW.** "148 unclassified lines" is 20; the other 128 are "declares no
  Form" (two warn-only rules, both vacuous until a DA row exists). `coincident`
  is a ruled design (the 2026-09-20 assumption-tier plan made it an explicit
  waiver cell); deleting it needs an owner ruling. The stock frame holds (52 of
  71 contain "outcome") with row-specific content inside it.
- **13.56.** The block is 365 words, not 608, and "downstream cost: none" is
  wrong: `PROCESS.md:528-529` makes enumerated dimensions a DevStg-Tests gate
  criterion — which the kit's own spine fails (0 of 138), a dogfood gap.
- **13.57.** Three scripts read `test_refs` (intake renders it in the approval
  brief; two classify it); no check validates it — that part holds. Deletion
  must coordinate with item 5's strict loader and remove the key from rows.
- **13.58 → LOW.** The sentence describes what the current schema forces
  (`--strict-schema` plus `Automated=Yes` needs `Evidence`); the proposed
  wording ("TC Evidence names the test FILE") contradicts revisions 8 and 35
  (a generated column; tags may sit on a test function).
- **13.59 → fold into §10.4**, correcting it: `reviewer.template.md:68` does
  carry the behaviour-vs-helper sentence. The proposed rule is right for
  SR-tier TCs and over-broad for LLR-tier ones (the kit's own modelled shape is
  a Unit TC over a pure function).
- **13.60 REFUTED as stated.** The absolute-term advisory already prints one
  console summary line; the 388 rows appear only in `report.md`, where a
  per-row worklist is the section's purpose. The console's bulk is the Form
  advisory: 128 of 210 WARN lines (61%), which no finding had named. The
  paraphrase and fan-out blindness is §11.4 and §12-4.5. Withdrawn; the
  388/2/2 counts stay as a footnote to §11.4.
- **13.61.** > 350 chars fires on 46/138; ≥ 3 semicolons on 6/138 — the narrow,
  defensible detector. The owner softened single-`shall` to a guideline with
  reasoned exceptions (2026-08-13v).
- **13.62.** `SKILL.md:264` is §6's quoted bad example, so 5 tokens at 3 sites;
  the composed body carries 3 tokens (2026-08-18 twice, `OI-72`) into every
  adopter's brief — the new fact.

Also confirmed as a valid new anchor: the SR template's `acceptance_criteria`
guidance "Measurable condition a test/demo asserts (the contract with the Test
Engineer)" frames the AC as a test assertion (Volere's fit criterion is the
measure of meaning). Thresholds the finder proposed, measured on the kit's own
rows: `method` > 400 chars 210/363; `expected` > 300 chars 72/363;
`requirement` > 350 chars 46/138.

### 13.E Tests, and tests of the test infrastructure

**[HIGH] 13.63 The smoke bar spends 28% of its test time on META tests.** By
subject (`tests-census/classes.csv`, docstring plus first two tests): PRODUCT
209 modules / 133,605 lines, PLUMBING 17 / 3,543, META 39 / 15,544, HISTORY 4
/ 679. In the measured smoke tier (3,384 tests, 60.65 s wall at `-n 4`,
122.8 s summed) META consumed 33.7 s (27.5%) for 519 tests: `test_import_layers`
7.4 s (1,061 ms per test), `test_smoke_budget` 4.5, `test_env_gates` 4.0,
`test_stage_ladder` 3.2, `test_check_resync` 2.6, `test_module_size_ratchet`
2.5. The 39 split into 12 about the suite/CI, 11 source censuses, 7 this-repo
tooling, 5 equality pins, 4 ratchets. *Change:* a `meta` marker applied by the
same collection hook, run at phase close and CI only. (This refines §5.1's
set: the finder's class includes modules the §5 skeptic kept as product; the
refuter is asked to adjudicate.)

**[HIGH] 13.64 (extends §8.3, §5.1) `test_module_size_ratchet.py` has been
touched by 407 of 4,683 commits (30 of the last 722) and is 89% comments**
(1,859 of 2,098 lines) around a 9-entry dict; an exact-match ratchet re-stamps
on every honest refactor regardless of carrier, so a TSV relocates the churn.
*Change:* delete it (the complexity ratchet already answers "no new monolith")
or make it grow-only.

**[HIGH] 13.65 The smoke membership ratchet `max-tests` has been re-stamped 72
times in 93 days and sits 26 tests from its next bump**, while `cpu-seconds`
and `wall-seconds` were each stamped once; the count moves with the tree, not
the tests (24 modules parametrise over live-tree files: `test_shell_portability`
6 defs → 50 cases). *Change:* delete `max-tests` and its ratchet test.

**[HIGH] 13.66 The two-tier partition saves compute but its mechanism costs
more than it saves.** Membership is by module ancestry, not measured cost: 11
SLOW modules have no test that spawns a process (258 defs excluded from the bar
for free: `test_traj_views` 56, `test_agent_loop_policy` 43, …) while 7 smoke
modules spawn in ≥75% of tests, including the bar's costliest,
`test_adjudicate_act` (14.4 s). The mechanism: `SLOW_MODULES` (139 entries,
358 lines of which 215 comments, 66 commits), `check_smoke_budget.py` 437
lines, six budget/meter/census test modules and the root `conftest.py` CPU cap
(~2,900 lines in all), and 22 "in-process pin" modules (2,050 lines) that exist
only because tiering is module-granular. The bar as declared runs `-n auto`,
which the root conftest halves. *Change:* keep a fast tier; derive `slow` from
a committed per-test durations file regenerated at phase close; delete the
meter machinery and fold the pin modules back; or wire the existing
`scripts/check_changed.py` (unwired since 2026-09-06) as the local bar.

**[HIGH] 13.67 The `scaffold` fixture bootstraps a fresh repo per test: 538
tests × 2.6 s ≈ 1,400 CPU-seconds per full run for identical trees that a
0.14 s copy reproduces.** 51 further direct `bootstrap.py --dest` sites in 14
modules; 257 `make_minimal_project` calls. The in-repo precedent exists
(`test_trace_interfaces.py:1055`, module scope). *Change:* bootstrap once per
session and `copytree` into `tmp_path` — same fixture name, zero test edits,
~5 minutes of wall per full run.

**[MED] 13.68 The same scenario is re-tested across modules:** 94 tests in 22
modules assert "a fresh scaffold passes `trace.py --strict`"; five copies of
`test_the_pre_commit_hook_runs_the_<step>_step`; three each of "rides the lane
commit walk" and "squash judged through the shared walk" with a 45-line spy
helper copied three times; four near-identical "placeholder registry is inert"
bodies. *Change:* one parametrised test per scenario; delete the per-rule pins
the generic tests already hold.

**[MED] 13.69 Test helpers are copied, not shared:** a `_git` runner in 45
modules (28 distinct bodies; one 19-copy cluster) although `conftest` exports
`fixture_git`; 57 near-duplicate helper clusters, 872 redundant lines; four WI
registry writers copied across the `test_trajectory*` family; local helper code
is 19,731 lines (13% of `tests/`); 21 test modules exceed 1,500 lines
(`test_intake.py`, 3,762, is longer than `intake.py`).

**[MED] 13.70 Seven smoke tests fail in a fresh clone** because tests act on
the live checkout (`root="."` → `HooksOffRefused` unless the developer's own
`core.hooksPath` is set) or read the ambient environment (`ANTHROPIC_BASE_URL`,
~60 `CLAUDE_*` variables in a cloud session; `conftest` scrubs only `AGENT_*`).
35 modules pass the live checkout into kit functions. An agent running the bar
in a cloud container sees a red bar unrelated to its change. *Change:* scrub
the vendor variables; a `hooked_checkout` root for the service tests; treat
`root="."` in a test as a lint finding.

**[MED] 13.71 553 tests (9%, 98 modules) reach into `_private` names of kit
modules** (`_verdict_gate` 57, `_load` 42, `_abandoned_claim` 19, …); every
private rename is a multi-module test edit. This is §4.1's test-tier twin: the
tests pin the decomposition, not the behaviour. *Change:* test through the
public verb; promote or delete.

**[MED] 13.72 (extends §5.2) PRODUCT tests by shape:** 34% drive a kit script
as a subprocess, 22% spawn only git, 45% run in-process; 19% of PRODUCT tests
(1,003) assert a ≥25-char phrase (§5.2's 40-char cut gave 4%), led by
`test_trace_rules` (124 of 284 asserts) and `test_prompts` (54 of 183,
asserting sentences of the shipped prompt templates); four golden byte-pins
pin whole reports. The kit's findings carry no stable identifier, which is why
tests pin sentences. *Change:* a stable short code per finding class (the way
`check.py` already labels steps); assert the code; one golden per renderer.

**[MED] 13.73 The test infrastructure has a test suite larger than itself:**
~4,100 lines of conftest/fixtures and ~1,900 lines of tests about them
(`test_cpu_cap` 547 asks the OS what cap the running pytest is under;
`test_env_gates` 512 includes an AST lint over every test module and tests
that the lint catches an invented bypass — a test of a lint of the tests), plus
63 "adequacy witness" tests in 28 product modules that test the module's own
detector. None can fail on a kit regression; all fail on a refactor of the
suite.

**[MED] 13.74 Eleven source-census tests re-lint the kit's own code on every
run and refuse contrived shapes** (an added stdlib import in `acceptance_record`
fails `assert _imported_roots() == {…}`; a `write_text` without `newline=`
fails `test_generated_newlines`; 2,566 lines, 1.7–3.2 s each per smoke run).
Each is a refusal where the owner's stated policy is to warn. *Change:* the
rules that matter become one warn-only `check.py --run-step kit-lint`; delete
the import-set, generated-set and pack-structure pins.

**[LOW] 13.75–13.77 Smaller:** `tests/` carries 7,562 `WI-###` citations and
1,759 date stamps (four times the scripts); four HISTORY modules pin prose
wording of shipped documents (a copy-edit of PROCESS.md is a test edit);
`test_wi_convert.py` credits 888 tests to a converter for the retired CSV home
(retire both); 16 scripts have no test module of their own; this repo's CI runs
the 7,700-test suite about seven times per push (five matrix cells, a
smoke-budget job that is the smoke tier again, and the gate job under
subprocess coverage tracing).

**Verification of 13.E** (one skeptic; the finder's junit data re-split per
test, the slow tier's figures added, every change checked against OI-68, D-7,
OI-21, WI-940 and ruled item 13). Two CONFIRMED (13.67, 13.69), one refuted
(the `wi_convert` retirement in 13.75–13.77), one duplicate (13.64 → §8.3), the
rest PARTIAL — and the pattern repeats §13.D's: the measurements hold, the
deletions mostly reverse a ruling.

- **13.63 → MED.** The META class mixes three kinds: strict meta (suite, CI,
  ratchets, equality pins) 22.3 s / 18.2% of the smoke tier's summed time;
  censuses over *shipped* code 7.6 s / 6.2%; this-repo tooling with behaviour
  tests 3.8 s / 3.1%. "Tests that cannot catch a kit regression" is false for
  the second and third kinds: `stage_ladder` enforces the OI-21 ban on lexical
  rung compares, `generated_newlines` closed a live Windows CRLF defect
  (WI-348), `hooks_on_census` is SR-240, `shipped_tier` is TC-149. A `meta`
  marker is feasible and costs adopters nothing, but moving the censuses out
  of the bar reverses the reason they were made tests. `test_import_layers`
  (7.4 s) and `test_smoke_budget` (one nested `pytest --collect-only`, 4.3 s)
  are 35% of the META time on their own. Over the whole suite META is 4.5%; the
  costliest META module anywhere is `test_prereq_toolchain`, 135.7 s for four
  tests in the slow tier, which the finder never named.
- **13.64 → duplicate of §8.3**, with two new facts: 380 of the 407 commits
  changed a baseline *number* (3.6 a day over 106 days), against 38 stamps of
  the shipped complexity TSV in 90 days — so the carrier matters more than the
  §12 skeptic allowed, and the dict is also pinned to its own docstring
  wording. "Delete the size ratchet" is OI-68's declined option 1a; grow-only
  is compatible with "armed".
- **13.65 → LOW/MED.** `max-tests` is the one deterministic, machine-
  independent growth sensor (`docs/stack.ini:85`, `test.yml:89`); CPU and wall
  were stamped once by design (WI-940 declares a breach a finding, not a
  re-stamp). 72 stamps are 1.9% of the window's commits. Deleting it needs a
  ruling; a 10% headroom or stamping at phase close does not. The 865-line
  history log is already ruled out of the file (item 10 step 4).
- **13.66 → MED.** The mechanism cost is real; the misfiling evidence is not:
  spawn count is the wrong criterion and the finder's own junit shows 6 of the
  11 "misfiled" modules are the heaviest in-process modules in the suite
  (misfiled reduces to ~83 defs / 1.9 s). Stale the other way:
  `conftest.py:393` still says `test_wi_convert` costs 107 s; measured 0.9 s.
  `check_smoke_budget.py` *is* the bar's tier runner (`[run] smoke`), so it
  cannot be deleted; a committed durations file is the ratchet's own kind of
  bookkeeping. The 60 s tier is ruled (plan `:966`).
- **13.67 CONFIRMED, HIGH.** 586 runtime instances, ≈1,500 CPU-s of the full
  run's ≈4,750 s summed (~30%); the slow tier measured 1,178 s wall at `-n 4`
  (4,240 passed, 4 failed, 72 skipped). Zero scaffold tests in the smoke tier,
  so it does not touch the bar. Hand out copies, never the template.
- **13.68 → LOW.** 94 tests share a setup step, not a subject (~9 are the
  scenario). The per-rule hook and lane-walk pins assert *specific* wiring the
  generic tests do not (a rider in `LANE_COMMIT_RIDERS`; a step in the hook's
  line and not in `_TRUNK_FRESHNESS_STEPS`), and the git-dependency tests exist
  so the env-gate skip is counted (WI-326). Parametrise them; do not delete.
- **13.69 CONFIRMED.** The 28 distinct `_git` bodies differ in return shape, so
  one runner needs two public shapes (the §12-2.2 point). OI-68 2a has the
  complexity census cover `tests/`, but the module-size ratchet is scripts-only,
  so test-module growth has no sensor — which this finding evidences.
- **13.70 — higher, not lower.** Two of the three "ambient" failures are a
  POSIX case-folding defect in `test_accounts` that fails on every Linux/macOS
  box regardless of environment since 2026-10-20, so the kit's own Linux and
  macOS CI cells should be red (checked below). The slow tier adds four more
  fresh-clone reds: two `run.command` → `./run.sh: Permission denied` (exec
  bit) and two `check.sh: set: Illegal option -o pipefail` under dash — the
  §9.1 defect in a second launcher. The env scrub fixes one test; the hooked
  checkout fixture exists (`conftest.py:627`).
- **13.77a NEW, HIGH — the kit's own CI has not produced a green run since at
  least 2026-10-14.** Checked on GitHub Actions (`kit-tests`, 117 runs): every
  one of the fifteen most recent runs on the declared trunk `refactor_again`
  (2026-10-14 → 2026-11-05) ended `failure` or `cancelled`; none succeeded. The
  five full-suite matrix cells and the gate job are cancelled at exactly the
  20-minute `timeout-minutes` on every run (the owner's own commit message of
  2026-10-19 records the full suite at 22 min 43 s locally), and the
  `smoke-budget` job fails in 54 s with six red tests: four
  `test_session_adapters` `HooksOffRefused` (the runner's checkout has no
  `core.hooksPath`, §13.70) and the two `test_accounts` "DID NOT RAISE
  SigninRefused" platform failures (CPU 98.7 s, well within the 540 s budget).
  `test.yml`'s own rationale for every-branch CI — "an independent environment
  sees" the blind spot a local gate misses — is void while it is red by
  construction. *Change:* first make CI able to go green (hooked checkout for
  the service tests, fix or skip-with-reason the two platform failures, a
  timeout the suite can meet or the smoke tier in the matrix with the full
  suite nightly), then treat any red as a finding. No downstream cost; the
  shipped `ci/check.yml` is a different workflow.
- **13.71.** The example pins an owner-ruled rank table; 7–9%; aligned with
  ruled item 13 point 4 ("does each test drive the interface the requirement
  names, and not handler source").
- **13.72.** In-process share 49%; drop `test_prompts` as the exemplar (the
  wording *is* the behaviour, §12-5.2); stable finding codes are sound for
  `trace`/`check_trajectory` findings and must come before any assert rewrite.
- **13.73 → LOW.** Adequacy witnesses are a ruled convention (item 13 rev 16
  requires "a stated adequacy witness"); `test_commit_hooks` tests shipped code.
  The valid core is a lint of the tests with its own mutation tests
  (`test_env_gates:378-502`).
- **13.74 → LOW.** Three of the five named rules closed live defects (WI-348,
  OI-21) or enforce a CLAUDE.md principle (the dependency ledger); the
  import-set pin in `test_acceptance_record` is the one contrived refusal.
  D-7's recorded lesson is that warn-only checks "earn the ignore".
- **13.75–13.77.** The HISTORY set is mis-drawn (`status_vocabulary_contract`
  guards a shipped template; the rubric test pins anchor structure, not
  wording); the provenance half is §1.3. **Retiring `wi_convert` is refuted**:
  `kitlib.registry` and `kitlib.spine` import it, so the shipped folder
  registry would break. The CI count holds with two corrections: the gate job
  runs the smoke tier a second time (eight runs, not seven), and
  `timeout-minutes` is 20, not 360; dropping cells removes 3.11-on-Windows and
  every-branch CI is ruled (OI-8).

Counter-findings: codes-before-asserts CONFIRMED (a true-by-construction
assert was repaired 2026-08-20); the hooks-on downgrade must also retire 32
modules / 56 fixture sites CONFIRMED; "a TSV churns just as often" PARTIAL
(38 vs 380 stamps says otherwise).

### 13.F Guards vs warnings — the refusal inventory

The finder enumerated 77 refusal sites (`guards/TABLE.md`): **KEEP-REFUSE 50,
DOWNGRADE-TO-WARN 18, DELETE 7**, two pointing at §6 items. Two sites are
models of the posture the review wants and need no change:
`acceptance_record._commit_parents` (a shallow graft → "fetch the parent and
retry", never read as a root) and `bootstrap.py`'s dirty/tarball kit → WARN,
exit 0. The ten downgrades and deletions with the best cost/benefit:

| # | anchor | what refuses today | who stops paying | change |
|---|---|---|---|---|
| 13.78 **HIGH** | `check.py:1177-1183`, `:1843-1867` | `staged-divergence --strict`: any partial commit while a generated artifact is modified-but-unstaged (`git add -p` workflows); the code calls it "adopter-visible and deliberate", the root fix (OI-31 (a), index-reading steps) "deliberately not taken" | every adopter with a generated artifact | WARN at the commit floor; FAIL where the committed tree is read (CI, the slot) |
| 13.79 MED | `kitlib/stage.py:395-402`, `:703-706`; `check.py:1531` | a `docs/stage` rung not on the current ladder exits every `check.py` run and every agent route; `parse` refuses *before* the fingerprint miss that would have re-derived (reproduced with a renamed rung) | every adopter at every ladder-vocabulary upgrade | treat the parse error as "no usable record": derive fresh, one WARN |
| 13.80 MED | `check_privacy.py:348-367` vs `:264-320`; `kit-python.sh:158-168` | a mixed or unparseable privacy policy: the sh hook refuses every commit while the Python checker in the same module resolves the same state (fail-closed, ON) | every re-synced adopter with a legacy file; every `process.toml` typo | the hook takes the checker's resolved answer; delete `refuse=mixed` |
| 13.81 MED | `check_trajectory.py:942-960`, `:3405-3420` | a `pending` open item that no queued WI cites is an ERROR "whatever the gate", evaluated before the no-work-items vacuity return | adopters using open items without the queue | WARN plain / ERROR `--strict` |
| 13.82 MED | `check_trajectory.py:1484-1545` | R-A (Deliverable iff terminal) is a hard error at every run; its justification is the agent handoff | human-edited work-item specs | the WARN/`--strict` ladder unless the loop marker is set |
| 13.83 MED | `trace.py:6472-6495` | `--strict` fails the Impl gate on two prose rules (a provenance frame; >1 `shall`) that are advisories everywhere else, while the kit's own code carries 1,992 WI citations unguarded | every adopter at the Impl gate | move both to the advisory list |
| 13.84 MED | `hooks/kit-python.sh:85-100` | no Python 3.11 → no commit, on every stack; ADOPTING calls the interpreter "the only requirement" for running checks, the hook makes it a requirement to commit at all | non-Python adopters' contributors | WARN at pre-commit and commit-msg when `privacy=off`; pre-push keeps refusing (publication boundary) |
| 13.85 MED | `integrate.py:1766-1795`; `agent_common.py:389-489` | the merge slot refuses a repo with no `[product] test` (docs- or spec-only), and a pinned toolchain without `./.venv` although every pinned tool is importable (poetry/conda/uv; reproduced) | station adopters on other environment managers; documentation repos | run the process bar alone; delete the venv-location proxy (`_step_guard` already gates importability) |
| 13.86 MED | `prompts.py:264-270` | `fill` refuses a template that does not consume every provided value, so an operator override may never drop a field | every `--prompt-map` override | unknown provided keys → one WARN; unfilled slots keep raising |
| 13.87 LOW | `check.py:1891-1972` | `approval-immutable` refuses deleting, moving or correcting a dated brief although git history holds every byte | anyone archiving briefs | exempt `D`, WARN on `M` |

Further rows: hook/`check.py` version skew refuses every commit on one unknown
step name (`check.py:2826`; the hook changed 62 times) — skip with a WARN
naming `bootstrap --sync`; the model-slug regex refuses `@` so Vertex-style ids
cannot be registered, citing a shell-metacharacter class `@` is not in; two
copies of the dual-carrier refusal and the retired-`Modified` guard outlive
their migration window (set an end date, delete at it); a wrong-typed
`human_approval_through` is refused at the loop's preflight but silently read
as the most-held rung by the hook step and the slot, and the doc states only
the refusal (the silent value is right; the missing piece is one warning line —
extends §6.5); 424 refusal/warning messages exceed 80 chars, 45 exceed 40
words, 9 exceed 60 (`baseline_snapshot.py:1119` 125 words; six of the ten
longest would be served by one line; several cite rulings and dates an adopter
cannot resolve — extends §6.3); three guards whose case cannot occur
(`[arch-map] mode` exit when "no step here consumes the mode"; a squash of a
deleted branch "no landing recipe makes"; a watermark correction with no
open-items registry); and the eight station steps cost 1.82 s of the twenty
cheap floor steps' 8.97 s on a lane-less repo, answering "nothing to judge"
eight times (the number §1.2 lacked).

**Counter-findings the finders raised against the first pass** (kept here so
§14 can honour them): the hooks-on and Python-3.11 downgrades are safe only
because pre-push, CI and the slot re-run the floor — downgrade pre-commit and
commit-msg only, keep pre-push; the hooks-on refusal exists only on station
routes, so a non-station adopter is unaffected either way; "unverifiable →
WARN" is right for the commit floor and CI's advisory run and wrong for the
merge slot, which must keep refusing a range it cannot judge; moving
`approval-fresh` off the floor re-opens the WI-325 defect for a trunk-only
adopter unless the sitting tool refuses to render a stale brief; a per-class
WARN summary hides the one new warning among 128 standing ones — print every
instance whose row id appears in the staged diff; for `human_approval_through`
the safe fallback is the most-held rung, not the shipped default.

**Verification of 13.F** (one skeptic; 50+ of the 77 inventory rows opened,
five false fires reproduced in clones, every downgrade checked against the
recorded rulings). Every opened anchor exists and fires where the row says.
But the downgrade list shrinks sharply: of the ten ranked changes, **one is
confirmed (13.87's narrowed form and the `@` slug), one is refuted as
infeasible (13.84), four conflict with a recorded ruling, and the rest are
LOW**. Corrections to the inventory: rows 1–2, 4, 5, 8, 22, 40 and 62 become
KEEP; row 24 needs an OI-21 amendment; rows 31 and 42 are ruling conflicts;
row 55 conflicts with a review ruling; `hooks_refusal` has 8 call sites, not 9.

- **13.78 → MED, ruling conflict.** The `--strict` promotion is **ruled**
  (OI-31: "promotion to error is its own later act once it has run clean for a
  program"), taken at the WI-498 close on measured evidence: a forgotten
  `git add` after regenerating `docs/stage` passed every freshness step. A
  modified-but-unstaged declared artifact *does* mean the committed tree will
  be stale; the question is who catches it, and the §9 trunk-only adopter has
  no CI or slot downstream — so "downstream cost: none" is wrong for that
  class. The honest destination remains OI-31 option (a). Needs a ruling.
- **13.79 → LOW.** The mechanism is false: after a rung rename the fingerprint
  *still matches* (the ladder vocabulary is not a declared derivation input),
  so no re-derivation would have followed; without the refusal every
  `stage_ord` comparison raises anyway. The refusal implements OI-21 ("RAISES
  on unknown"), and RESYNC already names `derive_stage.py` as the migration
  step. Once per vocabulary upgrade; one documented command.
- **13.80 → LOW, and the new fact is the reverse.** The checker reads **OFF**
  for a both-false mixed config (an OR), while its own docstring says a mixed
  config "reads ON" — a doc/code mismatch worth recording. The hook's refusal
  is the documented posture ("refused, never resolved by precedence"), kept by
  plan item 10 and pinned by TC-021; the proposal would resolve by precedence.
  "Q12" resolves to no privacy ruling; the record is OI-46 plus IF-037.
- **13.81 → LOW.** The owner surface does *not* render an uncited pending row
  as a card (an integrity notice only), so the stated harm partly holds for a
  non-station repo too; the design is WI-790's and OI-70 exit (B). A
  vacuity-aware rule (ERROR only once a real work item exists) honours both.
- **13.82 → LOW.** R-A is the record defect itself ("done records what shipped;
  cancelled records why it never will", WI-267), loop or not; a marker-
  conditional severity adds a §6.5-class two-posture rule. Keep it hard;
  improve the message.
- **13.83 → LOW or withdraw.** The provenance gate under `--strict` is an owner
  ruling of 2026-07-27 made because 43 rows accumulated under warn ("a warn
  nobody must act on"); the form patterns were promoted on measurement
  (each fires on 0–1 rows); plan ruling 6 names the two-`shall` catch as a
  wanted instrument. "Downstream cost: none" is wrong: the adopter's Impl bar
  weakens.
- **13.84 REFUTED.** Infeasible as written: the privacy answer is computed by
  `$PY check_privacy.py --hook-policy` *after* the interpreter probe, so a
  machine without Python 3.11 has no answer, and reading the policy in shell
  is exactly the grep the owner retired after it failed open on a decoy
  comment (plan item 10). The commit floor also carries the secrets scan. A
  documented adoption prerequisite, not a contrived guard.
- **13.85 → LOW.** (b) inverts the proxies: `requirements-dev.txt` pins
  versions and importability does not check pins — the false-green shape
  ruled at WI-286's review; the floor arms only when that file exists, so
  conda/poetry users opt out by in-project venvs. (a) stands (station only).
- **13.86 → LOW.** The strictness is WI-418's design (a value the engine
  believes delivered, silently absent from the brief); the better fix is to
  preflight every prompt-map key the way REVIEW already is.
- **13.87 LOW, narrowed.** Exempting `D` outright re-opens the rewrite-by-
  rename WI-503 closed; exempt `D` only when the same commit stages no `A` of a
  dated brief; `M` stays refused.
- **Further rows.** Skipping an unknown step name with a WARN fails open on
  skew (the single-home `--floor` fix is the safe one); the model-slug `@`
  fix is CONFIRMED; the second dual-carrier copy is forced by the kitlib
  import boundary, and the `intake.py:3403` deletion is a **misread** (it
  guards `Drafted`/`Founded` → `Approved` mechanical flips); the long-message
  census holds (median 22 words) but its "ten longest" table is not the cited
  script's output; of the three "small deletions", the `[arch-map] mode` check
  is config validation whose value *is* consumed, and the unattributed-squash
  hold closes a bypass, so both are withdrawn; the eight station steps cost
  0.3 s per commit (one concurrent spawn), not 1.82 s.

Counter-findings: CF1 (floor-only downgrade; the slot keeps refusing)
CONFIRMED; CF2 CONFIRMED and strengthened — `trace.py --mint-approval-brief`
has no staleness check, so without `approval-fresh` at the floor an owner can
mint and attest from a stale brief, the WI-325 defect; CF3 (print the staged
diff's instances) feasible; CF4 (most-held fallback) is §12-6.5 verbatim.

## 14. Recommendations, revised — ordered by leverage and positioned against the ruled plan

**How the second pass changes the picture.** The first pass's §7 treated the
four concerns as roughly equal and led with the spine re-tier and the station
split. After verification the weight sits differently:

- **Spine altitude is the largest lever, and the kit already knows what to
  do about it.** The shipped templates manufacture the defects (§10.1), the
  schema and two orphan rules force them (§13.45, §13.46), the detectors are
  blind to them (§11.4), and the question list never asks who outside the
  system would notice (§13.51). The owner's ruled plan item 5 — no code carrier
  in any requirement row, `module`/`code_symbol` retired, a commit-time text
  check, test evidence generated from tags — is the remedy, is sequenced
  "last", and has no queued work item. The exemplar (§11) shows what the rows
  look like afterwards: 84 → 31 rows, prose −86%, every evidence file kept.
- **Guards-vs-warnings has one root, not twenty.** Of 77 refusal sites, 50
  should stay refusals. The downgrades cluster around a single defect: floor
  steps read state a checkout may not carry (history depth, local lane refs,
  the working tree) and report its absence as a repository defect (§6.1,
  §6.3, §6.4, §10.9, §13.78). The shipped CI checks out at depth 1, so this is
  an adopter's first CI experience.
- **Consolidation is real but second-order, and it is mostly *policy*
  duplication.** The line-count duplicates are ~20-line pairs; what matters
  is two precedence rules that pick opposite spec copies (§13.13), nine
  freshness arms that disagree on exit codes (§13.14), a tokenizer that
  truncates what another copy runs (§13.22), and 458 façade aliases that keep
  old import paths alive (§13.15). Several first-pass consolidations were
  mode-flag merges the kit's own skill forbids (§12).
- **The test suite's cost is this repo's, not the adopter's** — `tests/`
  never ships — but it is the kit developers' daily tax: the declared
  per-commit bar is a 98 s tier with a ratchet re-stamped 72 times, a scaffold
  rebuilt 538 times per run, and ~10% of the lines (28% of the smoke time)
  testing the suite itself (§13.63–13.67). Several fixes reverse rulings
  (OI-68, D-7) and need a ruling, not a lane.

**The list.** Each item names what it discharges, its ruling status, size and
downstream cost. "Ruled" means the owner's 2026-10-11 plan (revision 38)
already covers it; such items need scheduling, not debate.

1. **Land the authoring half of item 5 now, before any re-tier.** Rewrite the
   two template cells that produce the altitude defects
   (`low-level-requirements.template.toml:19`, `test-cases.template.toml:26`),
   give `method` and `evidence` their missing guidance (§10.2), fix the five
   EXAMPLE.md pointer rows and SR-002 (§13.54), the two KICKOFF lines, the SR
   template's "contract with the Test Engineer" (§13.D), and the skill's
   DO-178C sentence (§10.3). Add the one bullet to spine-questions §0 that asks
   for the witness (§13.51; add, do not reword the ruled bullets). Ship three
   warn-only advisories (§11.4): LLR detail with call syntax or a filename, TC
   `expected` that only points, TC `expected` that copies its LLR (§13.48).
   *Discharges* §4.1, §4.2, §4.7, §10.1–10.5, §11.4, §13.47–13.49, §13.53,
   §13.54, §13.58, §13.59. *Ruled:* item 5 layer 3 and B1 for the §3 text; the
   template, EXAMPLE, KICKOFF and §0 additions are unruled but compatible.
   *Size:* days, one lane. *Downstream:* one template resync; existing rows
   untouched (warn-only). Without this, §8.1 says any re-tier regrows.

2. **Then re-tier in batches, under the ruled shape.** Not §7.1's "collapse
   LLRs into their SR, keep `module` as the pointer" (withdrawn: no SR module
   cell, "Module retires", decomposition (b) decomposes LLRs *recursively*).
   Land the three exemplar subtrees first (§11; blind re-derivation per the
   spine-authoring skill §4), then the ten largest fan-outs (SR-157 22, SR-148
   16, SR-154/054/155 11, SR-244 10, SR-168 8, SR-053 8, SR-006 7) and the
   call-syntax extreme SR-225. Re-cut the two orphan rules as part of
   decomposition (b): coverage flows up (children plus an integration TC
   discharge a parent), `verifies` names the leaf (§13.46). Schedule item 5's
   schema lane so the cells cannot come back. *Discharges* §4.3–4.5, §8.4,
   §11, §13.45, §13.46. *Ruled:* item 5 layers 1–2, decomposition (b),
   WI-994/997 in flight. *Size:* weeks of adjudication. *Downstream:* the
   ruled migration's own RESYNC entry.

3. **One checkout-tolerance idiom.** A `kitlib.git` helper that answers "is
   this history, ref or tree readable here?"; any last-writer, lane-ref or
   working-tree read that lands on a boundary reports **unverifiable → WARN
   with the repair** at the commit floor and in CI's advisory run, and keeps
   refusing at the merge slot (the slot must not land a range it cannot
   judge). Apply it to the snapshot writer lookup (§6.1), hold-by-rename
   (§6.3), `staged-divergence --strict` (§13.78), the stage-file rung parse
   (§13.79) and `check_test_first`. Add `fetch-depth: 0` with a one-line
   reason to the shipped `ci/check.yml` (§10.9). *Discharges* §6.1, §6.3,
   §6.4, §7.4, §10.9, §13.78, §13.79. *Ruled:* unruled; conflicts with
   nothing. *Size:* small. *Downstream:* none; it removes a false red from
   every adopter's first CI run.

4. **Stop committing the generated views.** `PROJECT_STATE.html` and
   `docs/open-items.html` (§8.2) become CI-published artifacts, as PROCESS §3
   already says composites should be, and `components.derived.toml` — the one
   committed *derived structural view*, which the §3 invariant squarely
   contradicts (§13.33) — goes with them; the freshness steps become a WARN
   that a committed copy, if present, is stale. The committed
   `interface-reference.md` is OI-66 ruled (a) after a priced build and its
   history cost is 0.5% of the dashboard's, so leave it unless the owner
   re-rules; fix the `:193` invariant text so it states the exception. Sequence it after the hand-landing
   recipe regains its compile step (§13.3): today the merge-slot route nobody
   runs is where "move it to the slot" would send the work. *Discharges*
   §1.4 (half), §8.2, §8.3 (half), §10.6 (half), §13.33. *Ruled:* consistent
   with PROCESS §3; ruling 6 keeps the hook itself. *Size:* small plus a
   `[generated]` edit. *Downstream:* adopters who want a committed dashboard
   keep the step.

5. **Fix the first day.** `setup.sh` must run under `sh` (§9.1); the derived
   stage floors at DevStg-Reqs while any `-000` row or placeholder flow exists
   (§9.3); format, lint and tests register from DevStg-Needs (§9.4); the regen
   ritual agrees with its checker and is documented, and every freshness FAIL
   names `trunk_step.py --regen` (§9.2); `bootstrap` respects a `pyproject.toml`
   pytest section and the shipped CI installs the project (§9.5); the
   dashboard renders without work items or the two sentences change (§9.6);
   one "first green run" block that the five "what next" places link to
   (§9.8); the connectivity warn and the placeholder scan stop firing on
   first-day state (§9.9); the first-day warnings in §9.11. *Ruled:* unruled.
   *Size:* days. *Downstream:* positive for every new adopter.

6. **Quiet the floor and declare its policy once.** One line per WARN class
   with a count — but print every instance whose row id is in the staged diff,
   or the one new warning hides among 128 standing ones (§13.F
   counter-finding); report-only classes leave stdout for the report and
   dashboard (§10.7; the Form advisory alone is 61% of the console, §13.60);
   a per-step level table — default level, promotion rung, floor/gate/never —
   that the hook, pre-push and CI plans select from (§10.14, §13.8), so the
   hook's 25-name list disappears; move the station steps behind the station
   layer (§1.2, §9.4). *Ruled:* ruling 6 keeps the hook as a hook; item 10
   moves the measurement history out of config. *Size:* small. *Downstream:*
   one hook re-take, then zero hook churn.

7. **Keep the fifty refusals; downgrade the few the verification left
   standing.** The §13.F verdicts shrank the finder's ten downgrades to a
   short list that conflicts with no ruling: add `@` to the model-slug class
   (§13.F); exempt a dated brief's deletion only when the same commit stages
   no new dated brief (§13.87); preflight every `--prompt-map` key the way
   REVIEW already is (§13.86); a vacuity-aware rule for an uncited pending open
   item (§13.81); the process bar alone when no product test is declared
   (§13.85a); fix the `check_privacy` docstring that says a mixed config
   "reads ON" when the code reads OFF (§13.80); keep R-A hard and improve its
   message (§13.82). The hooks-on refusal (§6.2) is a spine amendment (SR-240,
   LLR-340, IF-297) that bites only station routes — downgrade it there, after
   §9.1 makes the setup command work, and retire the 32 modules of fixtures
   with it. Everything else the finder ranked is either a recorded ruling
   (`staged-divergence` at `--strict`: OI-31 at the WI-498 close; the
   provenance and form gates under `trace.py --strict`: owner ruling
   2026-07-27 and plan ruling 6; the rung parse: OI-21; the `./.venv` floor:
   WI-286's review) or infeasible (the Python-3.11 downgrade needs the shell
   policy grep the owner retired after it failed open on a decoy comment).
   *Ruled:* as listed. *Size:* small each. *Downstream:* strictly looser where
   anything changes.

8. **Make the kit's own CI green, then cut the suite's tax (this repo only).**
   First the red CI (§13.77a): a hooked checkout for the service tests, the
   two `test_accounts` platform failures fixed, the `check.sh`/`run.command`
   dash and exec-bit defects the slow tier exposed (§13.70), and a timeout the
   full suite can meet — or the smoke tier in the matrix and the full suite
   nightly. Then the verified savings: bootstrap the scaffold once per session
   and copy it (§13.67: ≈1,500 CPU-s, 30% of the full run, no effect on the
   60 s bar); one shared git fixture with two return shapes and one WI writer
   (§13.69); a `meta` marker for the strict-meta kind only (18% of the smoke
   tier's time — the shipped-shape censuses stay in the bar, §13.63); the
   module-size ratchet grow-only (§8.3, §13.64 — not deleted: OI-68) and
   `max-tests` stamped at phase close with headroom (not deleted: it is the
   one machine-independent sensor, §13.65); the stale `SLOW_MODULES` comment
   and `test_prereq_toolchain`'s 135.7 s for four tests (§13.66); a stable
   short code per finding class before any assert rewrite (§13.72, §5.2);
   tests through public verbs, per ruled item 13 (§13.71). Withdrawn: retiring
   `wi_convert` (the shipped folder registry imports it), the partition
   mechanism's replacement by a durations file (the 60 s tier is ruled and a
   durations file is the ratchet by another name), and the deletion of the
   adequacy witnesses (a ruled convention, item 13). *Ruled:* OI-68, D-7,
   OI-21, WI-940 and item 13 all constrain this item; the CI fix and the
   fixture change conflict with nothing. *Size:* medium. *Downstream:* none
   (`tests/` never ships).

9. **Ship the station as a layer — by attribute first.** Tag each step and
   module with its layer, filter the bootstrap manifest on it, move the seven
   shared plumbing modules (`spine_carrier`, `baseline_snapshot`,
   `acceptance_record`, `agent_common`, `schedule`, `prompts`,
   `record_observation`) into `kitlib` or a core package, and only then move
   directories — a directory move today is a §4 rename of fifty authored
   paths in the pack §13.2 calls unreadable, and the import boundary is
   tangled in ten core modules (§12-1.2). CMP-008 "W3 Autonomy" already names
   the cut; item 12's W3 dry run is the place to record it. *Discharges*
   §1.1, §1.2, §9.10, §13.F's eight vacuous station steps. *Ruled:* consistent
   with the Unattended layer's applies-when; item 12 ruled the decomposition
   moments. *Size:* large; the first-pass "directory move plus manifest rows"
   was wrong. *Downstream:* a non-station adopter stops receiving 52 scripts,
   20 prompts and the launchers.

10. **Consolidate the policy duplicates, not the homonyms.** In `kitlib`,
    themed, never a `common.py`: one spec-precedence table (and fix the
    active-beside-closed tie-break, §13.13); one generator `check_or_write`
    with a per-generator missing policy (§13.14); one `process.toml` parse
    taking text, each dial's fail-direction kept explicit (§13.17, already a
    `status.md` row); `kitlib.ids`, `kitlib.markers`, `kitlib.declared`, one
    `text_at` with the three-way shape (§13.18–13.20); the five frontmatter
    grammars → the home, CRLF-tolerant (§13.23); the F5-licensed copies →
    their homes, the shlex divergence first (§13.22); the kit-path hints →
    one resolver (§13.25); a probe per shell dialect that adopter-owned
    launchers call (§13.24). Leave the git-wrapper, ratchet and refusal-
    composer merges the skeptics judged as mode-flag shapes (§12-2.2, 2.3,
    2.6). Delete the façade aliases only after the re-tier retires the rows
    that record them as the delivered shape (§13.15). *Ruled:* several are
    recorded consolidation rows (wi-856, wi-958, wi-960, wi-962); item 10
    covers `_pget` and the dial readers. *Size:* small each. *Downstream:*
    none, except the shlex fix (a bare `#` token stops truncating).

11. **Architecture prose: fewer rows, one home per decision — inside item
    11's migration.** Retire the every-module-endpoint warn and record a seam
    only at a component boundary or the repo edge, as variant F already
    requires and as item 11's phase 3 "must migrate explicitly" (§13.31; only
    26 of 255 rows are internal in every view, so the registry trim is smaller
    than the finder claimed); give the decision a boundary hides a home — two
    optional CMP keys, `hides` and `stops`, minted as SN-040's replacement for
    the unbuilt SR-165 (§13.32); fix the "derived, never committed" invariant
    text and cut §3's 40 lines on the retired marker routing (§13.33); one
    contract-at-code heading (§13.34); the flows participant rule follows the
    ruled "Module retires" sweep (§13.35); the planning briefs take the same
    derived component context the build brief is ruled to get, for both the IF
    and SR slots (§13.36); execute item 11 decision 2 on `PROCESS.md:1318` and
    the template so `Data` is the form (§13.37); gloss the rubric's ten ruled
    terms and ship or cite the knowledge pack (§13.39); de-duplicate the IF
    model between §8 and the OPTIONS layer (§12-3.1, §13.44). *Ruled:* items
    11 and 12 govern the shape and several of these are their phase-3 work;
    the `hides`/`stops` cells and the prose edits are unruled and compatible.
    Not in this list because a ruling forbids them: deleting the rubric's
    terms (F-call 7), a CMP module glob (ruling 5), removing the seam-TC
    allowlist (OI-43 (a); §13.43 was refuted). *Size:* prose plus the ruled
    migration. *Downstream:* no adopter row breaks.

12. **Records, provenance and the pack.** Compile the log or declare
    `docs/log.d` the record (§13.3); tombstone ruled open items after writing
    the record (§13.6); render only high-risk decisions and a count (§13.5,
    owner call); one `docs/handoff.md` and the 103 archived (§10.15, §13.7);
    a byte/entry ratchet on `RESYNC_PACK.md` now and a per-release migration
    table when ruling 10's trigger fires (§13.2, §13.4, §10.10); the
    provenance sweep across code comments, shipped skills, prompts and tests
    with the detector pointed at them afterwards (§1.3, §3.3, §10.11, §13.62,
    §13.75); an immutable, globally numbered home for owner rulings (§10.12);
    PROCESS.md as the austere reference with its rationale in one explanation
    document, and a cap on it — the kit's own skill proves watch-only fails
    (§10.13). *Ruled:* ruling 10 forbids mechanising the pack beyond its
    trigger; item 10 moves history out of config. *Size:* a sweep. *Downstream:*
    none.

**What needs an owner ruling before any lane** (each conflicts with a recorded
ruling or changes a gate bar every adopter signs): deleting `test_rule_sync`
(D-7); making the size/complexity sensors warn-only (OI-68); deleting
`max-tests` (WI-940); the hooks-on downgrade (SR-240); moving `approval-fresh`
off the floor (WI-325's defect — the mint brief has no staleness check);
`staged-divergence` as a WARN at commit (OI-31, promoted at the WI-498 close);
the provenance and form gates under `trace.py --strict` (owner ruling
2026-07-27; plan ruling 6); the rung-parse refusal (OI-21); removing
`coincident` (the 2026-09-20 assumption-tier plan); an opt-in smoke default
(2026-10-20); mechanising the resync pack (ruling 10, §5's trigger); the
DevStg-Tests bar text "every SR and LLR → ≥1 TC" and the enumerated-
dimensions criterion (PROCESS §4); gitignoring `interface-reference.md`
(OI-66 (a)); the seam-TC allowlist (OI-43 (a)); retiring or sampling the
absolute-term advisory (SR-157/LLR-274).

**What this second pass did not do.** No blind re-derivation of any subtree
(the exemplar's author read the rows and the code); no Windows or macOS run of
the hooks or launchers; the full suite was run once, by the meta finder, with
seven environment failures it diagnosed (§13.70); external sources were read
from GitHub-hosted copies or search snippets because the primary domains were
outside this session's network allowlist, and are marked as such in
`research/`; the hand classifications (SR witness, META test subject) are
readings, not script output, and say so; the CI history was read for the
trunk's fifteen most recent runs, not its whole history. Every number elsewhere reproduces from `measure.py`,
`trend.py`, `exemplar/compare.py` or the scripts in `measures/`.
