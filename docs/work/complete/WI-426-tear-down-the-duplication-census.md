+++
id = "WI-426"
title = "Tear down the duplication census (repo-lock D-7, owner-ruled 2026-08-10) and execute its six-item consequence inventory, none of it optional. (1) check_dupes.py retires from the kit: the script, its bootstrap.py MAPPING row, the README kit-contents row, docs/stack.ini [step:dupes] and its [generated] row, and check.py's advisory-step references. (2) docs/dupes-allow is DELETED, not archived - a registry states what IS, and git is the history (the D-1/D-4 doctrine). (3) tests/test_check_dupes.py (18 tests) and tests/test_dupes_census_audit.py (12) are deleted with their subject. (4) the spine chain SR-039 -> LLR-036 -> TC-039 is SUPERSEDED, which under D-4 means the rows are DELETED from the three registries, ids retired against docs/id-watermark, the act recorded in log.md's Decisions - the log entry IS the forwarding pointer home for the retired ids. This is the FIRST REAL SUPERSESSION D-4 performs, so the row doubles as D-4's proving case. The seam rows IF-007/IF-027 go with the module they describe: an IF row citing a deleted SR is a trace.py --strict FINDING, not a warn. (5) F5 becomes unbounded again and the mitigation is NAMED rather than implied - test_rule_sync is the anti-drift tool of record, new F5 duplication of POLICY requires a behavioral pin there, plumbing duplication is accepted unbounded (which the evidence ledger shows was its de-facto state anyway). Record that where the census's role was documented. (6) ADOPTING.md notes the removal; an adopter's copy is their file after copy-in. THE HEDGE, recorded as an instruction: if a genuinely cheaper form of the census turns up mid-execution, bring it to the owner rather than building it."
workstream = "scripts"
specref = ""
buildtier = "strong"
safety_class = "spine"
+++

## Deliverable

**DONE 2026-08-11 (`704ffd0d` + this close). All six inventory items executed;
nothing deferred, nothing optional dropped.** The links below are written for
`docs/work/complete/`, where this spec lands.

### 1–3. The tool, its census and its tests

`project-trajectory/scripts/check_dupes.py` (382 lines), `docs/dupes-allow`
(1033) and `tests/test_check_dupes.py` + `tests/test_dupes_census_audit.py`
(411 + 433 lines, **18 + 12 = 30 tests**) are **deleted, not archived** — git is
the history (the D-1/D-4 doctrine). Unwired with them: the `bootstrap.py`
`MAPPING` row and the script's name in the scaffold listing in its docstring,
the `project-trajectory/README.md` kit-contents row, the root `README.md` dial
row, `docs/stack.ini`'s `[step:dupes]` section **and** its
`docs/dupes-allow = dupes` row in `[generated]`, the `stack.ini.template`'s
`dupes` DATA-kind paragraph and its `[step:dup-code]` example, and the three
`check.py` docstrings that justified themselves by what the census had caught.

### 4. The spine chain — D-4's proving case

`SR-039 → LLR-036 → TC-039` are **DELETED** from
`docs/requirements/system-requirements.toml`,
`docs/requirements/low-level-requirements.toml` and
`docs/test/test-cases.toml`. Counts move exactly as predicted:
**SR 147→146, LLR 149→148, TC 146→145**, with `orphans=0 integrity=0`.

**`IF-007` and `IF-027` go with the module they describe** — this was not in the
inventory and is not scope creep: `trace.interface_findings` makes "an IF row
references unknown SR-039" a **--strict FINDING**, not a warn, so leaving them
would have traded one dangling pointer for two and reddened the gate.
`interfaces=107→105, interface-findings=0`. `components.csv` CMP-003's checker
list drops `check_dupes` in the same pass.

**Watermark verification — both rules hold, and neither could have been
violated.** `docs/id-watermark` is *unchanged by the deletion*: a mark only
rises, and `trace.py --bump-ids` raises to the live maximum, so removing a row
below the mark is a no-op for the file. *No mark decreased* (SR 147, LLR 166,
TC 160, IF 112, all as before) and *no live id exceeds its mark* (live maxima
SR-147, LLR-166, TC-160, IF-112 — the deleted ids were all interior, never the
maximum, so the headroom the marks already carried is exactly what retires
them). The four numbers stay spent forever. The file moved once in this WI, at
the CLAIM: `WI 425 → 426`, which is the mint counting from the watermark rather
than from `max(live)` — the same rule seen from the other side.

### 5. F5 is unbounded again, and the mitigation is NAMED

The census header was the only live home of the **2026-07-12 owner ruling**
that rejected a shared `_kitcommon.py`. Deleting it without rehoming would have
destroyed the statement of the rule along with its meter, so the rule now lives
in **`tests/test_rule_sync.py`'s module docstring**, stated in full:
duplicated **plumbing** is accepted **unbounded** (the ledger shows that was its
de-facto state anyway); duplicated **policy** owes a **behavioural pin there**,
asserted BY VALUE — equality alone can be vacuous, which repo-lock §5's
`_sn_fields` case already proved. `tests/test_wi_loader_sync.py` is the same
instrument aimed at the WI-registry readers and says so.

Every other place the census's role was documented got an honest disposition,
not a deletion: `docs/enforcement-audit.md` records the **downgrade** of "one
fact, one home" from Harness to Test-plus-Reviewer with the evidence, and keeps
the retired census-audit rule as a struck line because its reasoning is reusable
the next time somebody proposes a classified allowlist; `docs/status.md`,
`docs/archive/history/wrap-up-plan.md`, `docs/orphans-allow`, `docs/coverage-floors`,
`project-trajectory/orphans-allow.template` and `tests/conftest.py` all restated
the standing rule on its surviving half (*editing a declared list to clear a
finding IS accepting what it measures*) instead of pointing at a dead file;
`docs/registry-machinery-reference.md`, `PROCESS_OPTIONS.md`,
`docs/rubrics/registry-contradiction-audit.md` and `docs/concurrency-v2.md`
lost the tool from their live claims. **`PROCESS.md` and `AGENTS.template.md`
mention the census nowhere** — checked, so neither byte-budgeted file was
touched.

### 6. ADOPTING.md

A migration recipe under "Migration recipes for specific kit changes" states
what a re-sync will and will not do: it **deletes the script** (no longer
kit-owned) and **never touches the adopter's census file**, which lives under
their `docs/`. Keeping the check is recorded as a legitimate choice with the
command to pin the last shipped copy; dropping it names the three things that
must go together or the harness reds.

### The inbound-citation disposition, which is most of the actual work

| what cited a deleted id / path | disposition |
|---|---|
| `IF-007`, `IF-027` (`interfaces.csv`) | **deleted** — a `--strict` finding, not a warn |
| `CMP-003` `Notes` (`components.csv`) | `check_dupes` removed from the checker list |
| `WI-037`, `WI-078` (`complete/`) `sr_refs = ["SR-039"]` | **cleared** — a machine-read join field cannot point at nothing. Their PROSE keeps every citation, with a dated note recording the teardown: the history belongs in prose, the pointer does not |
| `WI-390` (`queued/`) — names `check_dupes.py` in its VERIFY list | dated Context note: the member is gone, `test_rule_sync` is the substitute, the rest of the list and the §4 re-stamp obligation are intact |
| `WI-422` (`queued/`) — title argues three ratchets miss dead symbols | dated Context note: one of the three is gone and the row's premise is **unaffected**, arguably stronger |
| `docs/concurrency-v2.md` §A9 (WI-390's SpecRef) | the verify list and the stamp clause corrected in place, with the substitute named |
| `docs/log.md`, `docs/archive/`, `docs/reviews/`, `docs/repo-review-*`, the four handoffs, `docs/spine-restructure-2026-08-08.md`, `docs/plans/`, `docs/ratify/2026-07-*`, `repo-lock.md` itself | **untouched** — the `check_doc_refs` doctrine rules that a historical document naming a retired thing is accurate history, and "fixing" it falsifies the record |
| the three retired PATHS, named by live and historical prose alike | declared in `docs/declared-absences` with their reason — the same mechanism the `work-items.csv` retirement used. This is what holds `check_doc_refs --strict` at its **baseline 17 dangling instead of 37** |
| five markdown **links** to the deleted files (`archive/specs/WI-334`, two handoffs, `log.md`) | converted to code spans. A link is a navigational promise that can no longer be kept; the TEXT is the history and is unchanged. Without this `check_docs` reports 5 broken links |
| `test_module_size_ratchet.py`'s two "check_dupes caught X" comments | **kept** — past-tense records of why a decomposition happened, in a file that is explicitly a dated changelog |

### The hedge instruction: nothing to bring back

Reported as the ruling asked. No cheaper form of the census surfaced during
execution. The member-list improvement was already weighed and rejected in the
ruling, and the teardown's own evidence points the other way: the census's
structural blind spot is *divergence*, and no cheaper variant of exact-token
fingerprinting fixes that — a tool that only sees identical copies is quietest
exactly when a copy has started to rot.

### Verification — run on a CLEAN WORKTREE, and here is why that matters

Another agent is working WI-424 in this same checkout and has uncommitted edits
plus an untracked new module (`scripts/adjudicate_brief.py`). A suite run in the
shared tree is therefore not evidence about *this* commit — the first full run
produced two failures that were entirely theirs (a half-written `Brief` column)
and one module-size failure mixing both agents' deltas. So the bar was met in a
detached worktree at this WI's own commit, which is stricter than the pre-commit
hook, not weaker. (The hook itself was bypassed once, for the same reason and
stated in that commit message: its arch-map step reads the WORKING tree and
demanded a map entry for the other agent's module, which this commit does not
add.)

```
$ pytest -q -n auto        # detached worktree @ 704ffd0d + this close's docs
2188 passed, 6 skipped in 425.38s (0:07:05)
```
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=704ffd0d -->

Zero failures, and `2188 + 6 = 2194` — the collection count below, so the green
covers the whole population rather than a filtered slice.

**The 30-test delta, measured rather than asserted** — collection counts at the
two revisions, which is an exact population count and not a subtraction:

```
$ pytest -q --collect-only   @ 8c0e78b3 (before)   2224 tests collected
$ pytest -q --collect-only   @ 704ffd0d (after)    2194 tests collected
```
<!-- fig: cmd=".venv/bin/python -m pytest -q --collect-only" rev=704ffd0d -->

`-30` exactly, matching D-7's stated 18 + 12 — no test was lost that did not
belong to the deleted subject.

```
Traceability: SN=29 SR=146 LLR=148 TC=145 orphans=0 integrity=0 ...
              components=5 component-findings=0 interfaces=105 interface-findings=0
```
<!-- fig: cmd="python project-trajectory/scripts/trace.py --root . --strict" rev=704ffd0d -->

`check_docs --root . --stale`: **0 broken** links. `check_doc_refs --strict`:
**17 dangling**, unchanged from the pre-teardown baseline. `derive_gate`:
**G1, unchanged** — only the basis counts move (`SR=147→146 LLR=149→148
TC=146→145`), which is the point: a supersession must not move the gate.
Every generated surface is `--check` fresh in the same commit — arch map, OKF
bundle (5 concepts pruned, 7 rewritten), derived gate, dashboard, status
snapshot, open-items.

### Deviations from spec

Two, both additive and both forced by the orphan check the row demanded:
**(a)** `IF-007`/`IF-027` and the `CMP-003` note were not in D-7's six-item
inventory but had to go with the module — deleting `SR-039` without them is a
`--strict` red; **(b)** `docs/declared-absences` gained three entries and five
markdown links became code spans, without which `check_doc_refs` goes 17→37 and
`check_docs` reports 5 broken links. Nothing was re-litigated, and no item of
the inventory was reduced.

## Context

**This is faithful execution of a ruled decision, not a re-litigation.** The
owner ruled on the evidence ledger in [`repo-lock.md`](../../repo-lock.md) §2
D-7: *"unless there is a better alternative it seems to be creating more
maintenance structure than it really solves, so it should probably just be torn
down."* The member-list improvement was on the table and was judged not worth
keeping the apparatus for.

**Why (the ledger, repo-lock §"Is the census earning its keep"):** one real
catch at the one-time triage and zero recorded since; structurally blind to both
real drift incidents this repo suffered (a diverged copy is no longer an
identical token block, so the tool goes silent exactly when duplication becomes
dangerous); 93% of its 253 census lines register accepted idioms; and it carried
its own defect chain, a 12-test meta-audit over its own prose, and three churn
cycles in one session.

**Why it lands HERE, in step 7.** repo-lock §5 step 7 is the batch that builds
the D-3/D-4 schema changes once, on the D-5 carrier. D-4 says supersession is
deletion; nothing in this repo had yet performed one. This row is the proving
case, which is why `safety_class = "spine"`: it deletes three ratified spine
rows and must leave the watermark's two rules intact — *the mark never
decreases*, and *no live id exceeds it*.

**The care point that makes this more than a `git rm`.** A deleted id is a join
key that other rows and documents cite. Every inbound reference must be
dispositioned before the delete, on the line the `check_doc_refs` docstring
already draws: a HISTORICAL document naming a retired id is accurate history and
keeps its citation (`docs/log.md`, `docs/archive/`, the reviews, the handoffs,
repo-lock itself); a LIVE typed join field pointing at a row that no longer
exists is a dangling pointer and must be re-grounded or cleared.
