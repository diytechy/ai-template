+++
id = "WI-425"
title = "Repoint the ~71 live source citations of the three SN ids the 2026-08-10 sitting retired (SN-030, SN-031, SN-032) at the SR rows that now carry their obligation. The sitting ruled all three MIS-LEVELLED - each stated a mechanism rather than a need, and each decomposed into 1-3 SRs against a core-need mean of 12.7 - so their rows were deleted and their children re-parented: SR-141/142/143 to SN-025, SR-144/145 to SN-027, SR-146 to SN-005. What the ruling did NOT touch is the ~71 places kit scripts and tests cite the retired ids in comments and docstrings, which now name nothing. This is a live dangling pointer, NOT the case check_doc_refs already blesses: its docstring rules that a HISTORICAL document naming a retired file is accurate history, and that doctrine covers the plan/handoff/log records, which must keep their tokens. It does not cover an explanatory comment in shipped code. METHOD, and most of it is mechanical because the comments self-classify: an SN-030 comment names its rung (rung 1 -> SR-141 dispose-first, rung 3 -> SR-143 queue overlap, rung 6 -> SR-142 red-TC census), and an SN-031 comment names its shape (terminal / per-close report -> SR-144; lineage / successor / disposition -> SR-145). Read each site rather than sedding it: a comment citing the PROGRAM ('the SN-031 program retired X') is history and keeps its token, while one citing the OBLIGATION ('SN-031 LINEAGE: partial work continues by minting a successor') must move to the SR. Leave project-trajectory/EXAMPLE.md alone - its SN-030 is the shipped worked example's own namespace, not this repo's id. NOT a rewrite of the comments themselves: swap the citation, keep the prose."
workstream = "scripts"
specref = ""
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

**Counts.** 69 sites found and classified (measured
`grep -rn "SN-03[012]" project-trajectory/scripts tests scripts --include="*.py" | grep -v EXAMPLE`,
post-repoint, plus the 2 `docs/dupes-allow` sites that grep doesn't reach
since it isn't a `.py` file): **56 repointed**, **11 kept as history**
(1 PROGRAM-citing comment + 9 size-ratchet ledger entries + 1 non-citation
test fixture), **2 deferred to D-7** (`docs/dupes-allow`, off-limits per this
row's scope). `project-trajectory/EXAMPLE.md`'s own `SN-030` (its worked
example's namespace) was left untouched, per spec. Zero sites map to
**SR-146**: the Context table's mint-time census (measured 2026-08-10)
counted "1 kit script" for `SN-032`, but re-measuring against the pre-edit
tree (`git show f1b4e0a8:<path>`) finds no `SN-032` citation anywhere in kit
scripts, only the two size-ratchet ledger lines below — the table's estimate
was simply off, not a site this row missed.

### Repointed (56)

**SR-141** (rung 1, dispose-first) — 2 standalone:
- `project-trajectory/scripts/dispatch.py:289` — `_judgement_first`'s docstring.
- `project-trajectory/scripts/agent_route.py:143` — **lower-confidence call**:
  the original read `SN-026 (SN-030 §7)`; `§7` traces to the 2026-08-08 plan
  doc's own section numbering ("SN D — the model/provider table", i.e.
  `SN-026`), not to an `SN-030` rung, so the parenthetical's `SN-030` half was
  never a rung citation in the first place. The surrounding prose explains why
  `ADJUDICATE` needs its own routing weight — the `adjudication` row *kind*
  that `SR-141` establishes — so it was repointed there (`SN-026 (SR-141)`)
  rather than dropped. Flagging this one: a reader who disagrees with the
  rung-1 read should feel free to re-open it.

**SR-142** (rung 6, red-TC census) — 5:
`project-trajectory/scripts/intake.py:195,1020,1041`;
`project-trajectory/scripts/dispatch.py:823,836`.

**SR-143** (rung 3, queue overlap) — 3:
`project-trajectory/scripts/check_trajectory.py:1918` (section banner),
`:1960`, `:3809`.

**SR-141 · SR-142 · SR-143 together** — 1 (module docstring covering all
three rungs at once):
`tests/test_loop_order.py:1` — repointed to
`"""SR-141 · SR-142 · SR-143 (under SN-025) — the loop-order contract, ..."""`.

**SR-144** (terminal / per-close report) — 28:
`project-trajectory/scripts/intake.py:129,545`;
`project-trajectory/scripts/bootstrap.py:1842,1848`;
`project-trajectory/scripts/check_trajectory.py:400,1877`;
`project-trajectory/scripts/check.py:598`;
`project-trajectory/scripts/handback.py:553` (the partial-close commit
message string itself, not just a comment — it would otherwise have kept
writing "The SN-031 outcome" into every future close);
`project-trajectory/scripts/integrate.py:124,131,1451,2126,2176,2185`;
`project-trajectory/scripts/traj_render.py:241`;
`project-trajectory/scripts/wi_convert.py:127`;
`project-trajectory/scripts/schedule.py:262`;
`project-trajectory/scripts/agent_common.py:1118,1234`;
`tests/test_dispatch.py:467`; `tests/test_handback.py:126,237,408`;
`tests/test_intake.py:277`; `tests/test_integrate.py:1194,1349`;
`tests/test_check_docs.py:489`; `tests/test_loop_order.py:137`.

**SR-145** (lineage / successor / typed-tier-field replacing the
`NEEDS-HUMAN` magic substring) — 16:
`project-trajectory/scripts/intake.py:97,120,706`;
`project-trajectory/scripts/check_trajectory.py:355,2052`;
`project-trajectory/scripts/handback.py:99,125`;
`project-trajectory/scripts/dispatch.py:520,902`;
`project-trajectory/scripts/wi_convert.py:107`;
`project-trajectory/scripts/schedule.py:217,793`;
`project-trajectory/scripts/agent_common.py:1189`;
`tests/test_traj_panels.py:472`; `tests/test_intake.py:334`;
`tests/test_loop_order.py:192`.

**SR-144 · SR-145 together** — 1 (module docstring naming the outcome model
as a whole, not one shape): `project-trajectory/scripts/handback.py:2` —
`"""handback.py — the lane closes that are not a clean merge (concurrency-v2
§A3, rewritten onto the SR-144/SR-145 outcome model)."""`.

### Kept as history (11)

**PROGRAM-citing (1):** `project-trajectory/scripts/intake.py:185` — `"THE
`handback` ARM IS GONE (SN-031, folding WI-417)."` narrates a completed
removal ("SN-031 retired X"), the exact shape the spec's own example names as
history; kept.

**Size-ratchet ledger (9), all in `tests/test_module_size_ratchet.py`:**
lines 397, 829, 845, 854, 943, 1076, 1232, 1254, 1429. Each is a dated entry
in a changelog-shaped comment (`"Then +75 (2946 -> 3021), SN-026/SN-032:
..."`) recording what a past module-size delta was *caused by* — the SN id
names the historical event, not a present obligation a reader would need to
resolve to understand current behavior. Same doctrine as the intake.py entry
above, just repeated nine times in one file's dated log.

**Not a citation at all (1):** `tests/test_rule_sync.py:189` —
`"## DRAFT (in review)\nSN-030 SN-000 SN-031\n"` is synthetic fixture text
for `test_sn_draft_ids_agrees`, which asserts two independent scanners agree
on which bare `SN-###` tokens sit under a "draft" heading. `SN-030`/`SN-031`
here are interchangeable with `SN-000`, `SN-010`, `SN-050` in the same test —
opaque strings exercising a generic regex, not a claim about what either need
requires. Left unchanged; repointing it would misrepresent it as a real
citation.

### Deferred to D-7 (2)

`docs/dupes-allow:871` (`"SN-031 re-stamped FIVE of the six: the schema
gained its 19th column..."`) and `:902` (`"...SN-031 re-keyed the sweep onto
the terminal folders..."`) are genuine obligation-citing sites — both would
repoint to SR-145 (lineage / disposition column, sweep re-keyed onto
terminal-outcome folders) under this row's own rule. Left untouched per this
row's explicit scope: `docs/dupes-allow` is scheduled for deletion at D-7
(the duplication-census teardown), so repointing it now is work that gets
thrown away. **Update at close (2026-08-11):** a separate D-7 teardown agent
is deleting `check_dupes.py`, `docs/dupes-allow` and their tests in this same
tree concurrently with this row's close; both sites go away with the file
rather than getting repointed, which is the outcome this row already
deferred to.

### Verification

`grep -rn "SN-03[012]" project-trajectory/scripts tests scripts --include="*.py" | grep -v EXAMPLE`
post-repoint returns exactly the 11 "kept as history" sites above — nothing
unaccounted for; re-run at close (HEAD `7aa87ca8`, after WI-415, WI-423 and
the D-5 review fix pass landed on top of this row's commits) returns the
identical 11 lines. `docs/architecture.md` and `PROJECT_STATE.html` were
regenerated (`gen_arch_map.py`, `gen_trajectory.py`): the module map's
docstring excerpts are derived from the same comments this row edited, so
they carried the same dangling ids and now resolve without further action.

**Bar.** Smoke tier immediately after this row's three repointing commits
(`08eb70fd`/`356b73f9`/`311fd487`): 880 passed, 6 skipped. Full unfiltered
suite at that same point (before WI-415/WI-423/the fix pass landed on top):
**2193 passed, 9 skipped** (349s). Since then WI-415, WI-423 and the D-5
review fix pass (`49ab1c1c`) landed on the branch and touched `tests/` and
some kit scripts again; that fix pass ran the full unfiltered suite green at
HEAD-adjacent state (**2215 passed, 9 skipped**, per its own report), so this
row did not re-run the full tier a second time. A fresh smoke run at this
row's actual close HEAD (`7aa87ca8`) is the evidence this row owns for that
later state:
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke" rev=7aa87ca8 -->
**900 passed, 6 skipped.**

## Context

Measured at mint time, 2026-08-10 on `infra/mechanized-loop`:

| retired id | kit scripts | kit tests | now carried by |
|---|---|---|---|
| SN-030 | 11 | 4 | SR-141 · SR-142 · SR-143 (under SN-025) |
| SN-031 | 35 | 18 | SR-144 · SR-145 (under SN-027) |
| SN-032 | 1 | 2 | SR-146 (under SN-005) |

**Nothing currently fails on this, and that is the reason it needs a row.**
`check_docs`' SN scan reads the registry to find ids that need a README bullet;
it never validates an `SN-###` token appearing in a `.py` comment. So the tree
stays green while ~71 comments cite ids that no longer exist — the silent-rot
shape the kit exists to prevent, sitting in the kit's own source.

**Why the ids are not being re-minted.** D-4 rules that supersession is deletion
and ids are never reused; the watermark (`docs/id-watermark`) holds `SN = 32`,
so the three numbers stay spent. A future `SN-030` would silently re-point every
one of these comments at a different meaning — which is exactly the hazard the
watermark was built for, and the reason repointing is worth doing while the
mapping is still obvious to a reader.

### Re-affirm, take 2 (2026-08-11)

The first Re-affirm paragraph below landed in the SAME commit as the
`queued/` -> `active/` move, so git's own rename detection read the pair as
one `R` status; `--diff-filter=AM` (the row-clock's own row-history mode)
drops a rename whatever else the commit did (WI-362's documented blind spot),
so the clock did not move. This paragraph is a content edit at the row's now
STABLE path, no rename riding along, which is what actually clears the warn.

`check_trajectory`'s backlog-staleness warn compares this row's own last-touched
commit against its SpecRef (`docs/repo-lock.md`); the row was minted at
`14925426` (2026-08-10) and repo-lock has moved four times since
(`cb7c27a5`, `da90b487`, `bb69a622`, `f1b4e0a8`, the last landing the D-5
carrier cutover). None of that movement touches this row's premise: repo-lock's
§8.4/D-5 material is the carrier migration and the queued sitting record, not
the SN-030/031/032 retirement or the SR-141…146 re-parenting this row repoints
against — that ruling is already landed on the spine
(`docs/requirements/system-requirements.toml`), independently verified below
before any site is touched. This content edit is the re-affirmation the clock
asks for.

**At close (2026-08-11):** `specref` is cleared per R-F — the terminal
transition's mechanical half; this row's own Deliverable above and
`docs/log.md`'s matching entry carry the backward record `docs/repo-lock.md`
was standing in for. `docs/repo-lock.md` itself is untouched — it is a live,
actively-cited ledger, not a `docs/specs/` scratch doc, so R-F's *archive*
clause does not reach it.
