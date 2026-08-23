## 2026-08-22 — WI-507: the consolidation doctrine lands, the census stands, antidote is vendored

Executes OI-58's ruled (a)+(b) plus the owner's vendoring instruction, on
branch `requirements/ears-and-quality-characteristics`.

**1. The doctrine.** `PROCESS.md` §3 gains the full clause — "Consolidate,
don't duplicate — the 0→A→B rule": edit-conservatively is scoped to the task
in front of you, consolidation is scoped to the whole codebase when the task
IS consolidation, extract the shared stage a duplicated fix wants (0→B, 0→D
become 0→A→B, 0→A→D), restructure where outputs overlap, and validate/
implement once at the owning boundary — the vendored `antidote` skill's
per-fix half of the same principle. `CLAUDE.md` and `AGENTS.template.md` each
carry one pointer line beside their own existing conservatism bullet, never a
restatement (single-source-of-truth).

Byte deltas, one line per touched file (`wc -c`, before -> after):

- `CLAUDE.md`: 7238 -> 7513 (**+275**; cap 8500, 987 headroom left)
- `project-trajectory/AGENTS.template.md`: 9941 -> 9980 (**+39**; cap 10000,
  20 headroom left — at-cap file, paid for by tightening the "one fact, one
  home" bullet in the same edit, per the skill's own convention)
- `project-trajectory/PROCESS.md`: 84881 -> 85889 (**+1008**, FLAGGED; watched,
  not capped)
- `project-trajectory/skills/byte-budget-guard/SKILL.md` (+ its `.claude`/
  `.agents` fan-out copies, kept byte-identical): 4877 -> 4841 (**-36**; cap
  5000) — re-stamped all four rows above in the same commit.

**2. The measurement.** `project-trajectory/scripts/check_dupes_census.py` is
a new, standing, **warn-first-forever** check (never fails a gate, not even
under `--strict`) — the WI-448 duplicated-function-body census (AST body-hash,
bodies >= 4 lines, docstring stripped), now one named function instead of a
`python -c` one-liner re-typed into every prior measurement. Wired as
`[step:dupes-census]` in `docs/stack.ini` (`layer = product`,
`from-stage = DevStg-Impl`). Baseline stamped in `docs/stack.ini`
`[dupes-census]`:

  <!-- fig: cmd="python -c 'import ast,hashlib,pathlib,collections;P=\"project-trajectory/scripts\";G=\"*.py\";C=\"__pycache__\";B=lambda n:(n.body[1:] if n.body and isinstance(n.body[0],ast.Expr) and isinstance(n.body[0].value,ast.Constant) and isinstance(n.body[0].value.value,str) else n.body);g=collections.defaultdict(list);[g[hashlib.sha1(chr(10).join(map(ast.dump,B(n))).encode()).hexdigest()].append(n.end_lineno-n.lineno+1) for p in sorted(pathlib.Path(P).rglob(G)) if C not in p.parts for n in ast.walk(ast.parse(p.read_bytes())) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and B(n) and n.end_lineno-n.lineno+1>=4];d=[v for v in g.values() if len(v)>1];print(len(d),sum(len(v)-1 for v in d),sum(sum(v[1:]) for v in d))'" rev=1806f5c8 -->

**15 groups / 15 redundant copies / 202 redundant lines.** This is a FRESH
measurement of the same producing command, not a restatement of the WI-448
slice-3 close's own figure (15/15/194 at commit `2eae651e`) — trunk moved
between the two measurements (unrelated WIs touching
`project-trajectory/scripts/`) and the group/copy counts held while an
existing duplicate class grew by 8 redundant lines. Re-stamped downward-only
by hand thereafter, like the module-size and smoke-budget ratchets.

**This deliberately re-opens only the narrower half of a prior ruling.**
`docs/stack.ini` records that `[step:dupes]` — a GATING duplication step —
was torn down by owner ruling 2026-08-10 (D-7, executed WI-426): it gated on
an unbounded population where 93% of its findings were accepted idioms, and F5
duplication was ruled UNBOUNDED. OI-58 (2026-08-22) re-arms the MEASUREMENT,
not the gate: `check_dupes_census.py` never exits nonzero, under any flag.
Both the check's docstring and its new SR-182 spell this out so a future
editor does not "helpfully" wire in real `--strict` teeth without bringing
that case back to the owner, per D-7's own instruction.

New spine rows (Approved, riding this commit's approval): **SR-182** (the
obligation — report, never gate), **LLR-195** (the realization —
`check_dupes_census.py`'s `measure`/`main`), **TC-190** (the test —
`tests/test_check_dupes_census.py`, 5 cases: no-baseline reporting,
unchanged/regression/improvement judging including the never-gates-even-under
`--strict` pin, and the vacuous no-scripts-dir case). `trace.py --bump-ids`
and `intake.py snapshot` ran in this commit so the new Approved rows ride the
`docs/archive/last_approved/` copy in the same act.

A call-graph behavioral-overlap measure was NOT added: it is recorded as the
named follow-up rather than forced — OI-58's own ruling already minted
**WI-508** (the blind-remap architectural exercise, sequenced behind the
wi448/wi483 lanes) as the program-scale home for that question, and building
a second, cheaper instrument here risked pre-empting that program's own
design rather than feeding it.

**3. Antidote, vendored.** Read whole before vendoring
(`C:/Projects/antidote/skills/antidote/SKILL.md` + its repo `README.md`):
pure-prompt, MIT-licensed, "no scripts, no network calls, no dependencies"
(the source's own compatibility claim, and the content itself confirms it —
a root-cause-vs-patch coding checklist, nothing that reads as a credential,
network, or process-conflict risk). No stop condition triggered.

- `project-trajectory/skills/antidote/SKILL.md` — vendored verbatim below a
  short provenance note (source, MIT license, commit
  `8e0350e3d86df36852d56ad0a502376e24de870c`, upstream v1.1.0), frontmatter
  rewritten to this kit's schema (`name`/`description`/`stacks`/`domains`/
  `phases`/`tags`/`scope`; `scope: kit`, `domains: [any]` — a default the pack
  ships). `skills/INDEX.csv` regenerated (29 skills). Dogfooded byte-identical
  into `.claude/skills/antidote/` and `.agents/skills/antidote/`
  (`gen_skills_index.py --check-agents`: OK, 16 copies match source).
  `docs/dependencies.md` gains a `kit`-tier row (a new tier: vendored content,
  not a Python import) naming the source, the license, the pinned commit and
  the ruling; `EXTERNAL_SKILLS.md` gets one paragraph distinguishing this
  ruled exception from its own "mine, don't install" reading-list posture, so
  the two pages don't quietly contradict each other.
- **No pre-existing "vendored-skill pattern" was found to follow** — every
  shipped skill under `project-trajectory/skills/` today is kit-authored, not
  vendored from an external source (`EXTERNAL_SKILLS.md`'s own posture is
  explicitly mine-don't-install). This WI establishes the convention (a
  provenance note under the frontmatter, a `docs/dependencies.md` ledger row)
  rather than following one — recorded as a deviation from the WI text's
  premise, not a blocker: the owner's OI-58 ruling explicitly names vendoring
  as the intended act ("VENDOR the antidote skill into the kit as a default
  skill the pack ships, alongside the existing vendored skills"), so the
  absence of precedent reads as imprecise phrasing in the ruling, not as
  missing authorization.

**Scaffold verification.** `bootstrap.py --dest <scratchpad>/wi507-scaffold
--agents claude --domain any --stack python`: `.claude/skills/antidote/
SKILL.md` is created and byte-identical to the kit source (`diff`, no output).
Scratchpad cleaned up after.

**Gates, real output:**

```
python -m pytest -q -n auto -m smoke
1404 passed, 5 skipped in 69.27s (0:01:09)
```
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=1806f5c8-dirty -->

Over the WI-281 60s budget on this box — the same one-machine reading
`CLAUDE.md` already records; the budget is not moved to fit it.
`docs/stack.ini` `[smoke-budget]` re-stamped **1409 -> 1416** (measured 1409
collected, exactly the previous ceiling — `tests/test_check_dupes_census.py`'s
5 new tests, same class as `tests/test_check_figures.py` beside it: tiny
`run_py` subprocess fixtures, no scaffold). +7 restores the same absolute
slack the recent stamps carried.

```
python project-trajectory/scripts/check_docs.py --root . --stale
OK - 1023 doc(s), 1354 intra-repo link(s), 0 broken (1 orphan warning(s))
```

```
python project-trajectory/scripts/check_trajectory.py --root . --strict
clean (507 work item(s), 473 done (93%), 21 cancelled, graph acyclic)
```

```
python project-trajectory/scripts/trace.py --root . --strict-integrity
Traceability: ... integrity=0 ...
```

```
python -m pytest -q -n auto --basetemp=D:\pytest-tmp-w507b
2899 passed, 14 skipped in 1092.39s (0:18:12)
```
<!-- fig: cmd="python -m pytest -q -n auto --basetemp=D:\pytest-tmp-w507b" rev=1806f5c8-dirty -->

(A first full-suite run, launched before the spec-close edits — `spec_move`,
`trace.py --bump-ids`, `intake.py snapshot` — landed, read a mid-edit tree and
red one test on a stale `docs/stage` fingerprint,
`tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current`;
re-run alone against the settled tree passed immediately, and the second full
run above — against the fully closed tree — confirms it clean.)

**Deviations from spec.**

1. The [dupes-census] baseline is stamped at the fresh reading (15/15/202,
   commit `1806f5c8`), not the WI text's cited figure (15/15/194, commit
   `2eae651e`) — trunk moved between the two measurements; a fresh measurement
   of the same command, not a restatement, per this repo's own established
   convention for exactly this situation.
2. `check_dupes_census.py`'s never-gates-even-under-`--strict` posture is a
   narrower reactivation of a specific prior ruling (D-7, the `[step:dupes]`
   teardown) than the WI text's plain "standing warn-first check" phrasing
   states — spelled out explicitly (docstring, SR-182 rationale, this
   fragment) so it reads as a deliberate boundary, not an oversight, should a
   later session consider widening it.
3. No pre-existing vendored-skill pattern existed to follow (see §3 above);
   one was established rather than found.
4. A full SR/LLR/LLR/TC spine addition (SR-182/LLR-195/TC-190) was minted for
   `check_dupes_census.py` that the WI text did not explicitly ask for — the
   module is a real `project-trajectory/scripts/` script, and
   `check_trajectory.py --strict` reds on an untagged arch-map module with no
   owning component; the spine rows are the mechanical fix the gate itself
   demands, not scope creep.

Deferred open items: none — OI-58's (c) program row is WI-508, already minted
and sequenced by the owner's own ruling; nothing here is left undecided.
