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
adversarially re-verifies §1–§6 (the verdicts land in §12 as they arrive). `measure.py`
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
