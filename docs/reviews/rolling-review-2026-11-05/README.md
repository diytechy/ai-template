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

**Status:** second pass IN PROGRESS (2026-11-05, same day). The first full pass is §1–§7;
the second pass adds §8 onward, re-measures with `measure.py` and `trend.py`, and
adversarially re-verifies §1–§6 (the verdicts land in §9 as they arrive). `measure.py`
beside this file reproduces every first-pass number; `trend.py` the §8 table. Audit
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
registries: SN 35 rows, SR 138, LLR 331, TC 363, IF 255, OI 120
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
