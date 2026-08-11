+++
id = "WI-427"
title = "SN-010 says every generated artifact carries a --check freshness contract; two committed, DECLARED-generated artifacts have a working --check that runs NOWHERE, so the need is currently false. (1) project-trajectory/prompts/CATALOG.md, declared generated at docs/stack.ini [generated] as `promptcatalog`: gen_prompt_catalog.py --check works, and zero references to it exist in check.py, the pre-commit hook, .github/workflows or ci/check.yml. (2) project-trajectory/skills/INDEX.csv, declared as `skillsindex`: gen_skills_index.py --check (index-vs-SKILL.md staleness) is wired nowhere, and only the DIFFERENT --check-agents mode (per-agent copy drift) runs, as the skills-sync step - so a stale INDEX.csv passes every gate. Wire both into check.py's built-in step table and the hook's --run-steps list following the arch-map/okf/derived-gate/ratify-fresh idiom, deciding each step's GATE SET on what the artifact means rather than by copying the most common value, and deciding fold-vs-separate for the skills index on the two modes' actual properties. MAKE THEM NON-VACUOUS: plant a defect in a temp tree and prove each step REDS, with a test per step - a freshness step that cannot fail is the SN-008 green-hides-a-skipped-check failure and would be worse than the gap. ALSO verify the census claim that these are the only two gaps, reporting the full [generated]-vs-wiring table."
workstream = "scripts"
specref = ""
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

**DONE 2026-08-11 (`d960d127` + this close). SN-010's universal is TRUE again:
every artifact declared in `docs/stack.ini`'s `[generated]` section now has a
named freshness enforcer, and both new steps are proven able to go RED.** Links
below are written for `docs/work/complete/`, where this spec lands.

### The verified `[generated]`-vs-wiring table

All ten rows read from `docs/stack.ini` `[generated]`; every gate set read back
out of `check.steps()` rather than from the source comments.

| `[generated]` row | kind | regenerator | enforcer | gate set | commit floor |
|---|---|---|---|---|---|
| `PROJECT_STATE.html` | `trajectory` | `gen_trajectory.py` | step `trajectory-map` | `{G3}` | yes |
| `docs/okf/` | `okf` | `gen_okf.py` | step `okf` | `{G3}` | yes |
| `docs/architecture.md` | `archmap` | `gen_arch_map.py` | step `arch-map` | `{G3}` | yes |
| `docs/status.md` | `status` | `gen_trajectory.py --status` | step `status-map` | `{G3}` | yes |
| `tests/test_module_size_ratchet.py` | `linecounts` | **none by design** | the file **is** a test | n/a | runs in pytest |
| `docs/gate` | `gate` | `derive_gate.py` | step `derived-gate` | `{G1,G2,G3}` | yes |
| `docs/open-items.html` | `openitems` | `gen_open_items.py` | step `open-items` | `{G3}` | yes |
| `docs/ratify/` | `ratify` | `trace.py --ratify` | step `ratify-fresh` | `{G2,G3}` | yes |
| `project-trajectory/skills/INDEX.csv` | `skillsindex` | `gen_skills_index.py` | **NEW** step `skills-index` | `{G1,G2,G3}` | **yes (new)** |
| `project-trajectory/prompts/CATALOG.md` | `promptcatalog` | `gen_prompt_catalog.py` | **NEW** step `prompt-catalog` | `{G1,G2,G3}` | **yes (new)** |

**The census claim holds: there was no third gap.** Eight of ten were already
wired; the two known-special rows behave as the row predicted. `linecounts` is a
hand-stamped baseline with *no regenerator by design* — re-deriving it would
blindly ratify whatever the tree currently measures, which is the ratchet
inverted — and its enforcer is that the artifact **is** a test that re-measures
every kit module on every run. `docs/gate` was already gated at all three gates.

The census is no longer a claim in a document: `test_generated_freshness_wiring`
parses the `[generated]` section and fails on any row whose kind resolves to
neither a `check.py` step nor a named non-step enforcer, so the *third* unwired
artifact reds the day it is declared. It also fails in the other direction, so
the table cannot outlive the rows it describes.

### The three decisions, and what decided them

**Gate set `{G1,G2,G3}` for both — not the `{G3}` doc-freshness family.** That
family (`arch-map`/`trajectory-map`/`status-map`/`open-items`/`okf`) is G3-only
for a *stated* reason: its members are views of the project's own evolving spine
and "churn while the plan is still forming", so gating them early reds a repo for
drift in an artifact whose inputs are still being written. These two have the
opposite input profile — they index the **apparatus** (the kit's skill library,
the loop's prompt templates), which does not move as a downstream plan matures,
so there is no early-stage churn to protect — and their consumers are live from
the first session: an agent reads `INDEX.csv` to decide whether a skill applies;
an operator reads `CATALOG.md` to join a session log's `prompt-sha` back to the
template that produced it, i.e. *while debugging a session that already behaved
oddly*. That is `derived-gate`'s shape, not the dashboards'.

The decisive evidence is concrete rather than aesthetic: **this repo's own
`docs/gate` reads `G1`** (`computed=G0`, held up by `drafts=37 modified=38` — the
open ratification window). A `{G3}` step therefore does not run in the kit's own
CI *at all* for the whole duration of that window. Wiring these at `{G3}` would
have re-created the exact gap this row exists to close, while looking fixed.

**Its own step, not folded into `skills-sync`.** The two modes check genuinely
different properties, and they differ in every dimension that picks a step:
input (a *generated artifact* vs hand-authored copies of hand-authored source —
`docs/stack.ini` deliberately declares only `INDEX.csv` in `[generated]`, the
per-agent copies "stay absent, being hand-authored source", WI-231), fix
(`gen_skills_index.py` vs `bootstrap.py --sync`), and gate set. There is also a
mechanical reason: `check.py`'s step tuple carries exactly **one** argv list, so
folding would mean changing the generator to make the harness table simpler —
inventing an idiom rather than following one. The difference is driven, not
asserted: `test_skills_sync_cannot_see_index_staleness` plants the defect
`skills-index` catches and shows `--check-agents` stays green on it.

**`ci/check.yml` needs no change — verified by reading it, not assumed.** It
invokes `check.py` as a single entry point at three tiers (`--tier smoke` on
push, `--tier full` on PR, `--gate all --tier release` on a tag) and never names
a step, so a step added to the built-in table is inherited for free. Same for the
kit's own `.github/workflows/test.yml`, which runs `check.py --jobs 0`. Both were
grepped: zero occurrences of either step name, and the steps run anyway. Pinned
by `test_the_reference_ci_inherits_new_steps_without_editing_it`, so the finding
cannot quietly stop being true if CI ever grows a hand-listed step set.

### Non-vacuity — the acceptance bar

**One vacuous-pass trap was found and defused before it shipped.**
`gen_skills_index.py --check` defaults `--skills` to a **CWD-relative** `skills`,
and in this repo the source lives at `project-trajectory/skills`; the naive
wiring exits **0** with `gen_skills_index: no skills dir at skills`. That is a
permanently green check of nothing — the SN-008 failure this row exists to
remove, reproduced in the act of fixing it. The step passes `--skills` explicitly,
derived from the script's own location, and
`test_skills_index_step_never_falls_back_to_the_cwd_default` asserts both the
argv and the absence of that message end-to-end.

Each step was then driven RED against a defect planted in a **copy** of the
harness under `tmp_path` — the live tree was never corrupted — green → red →
green:

```
=== prompt-catalog : .../scratchpad/redproof/project-trajectory/scripts/gen_prompt_catalog.py --check ===
gen_prompt_catalog: project-trajectory/prompts/CATALOG.md is STALE — a template changed
and the catalogue did not. Run `python scripts/gen_prompt_catalog.py` and commit the result.
rc=1
```

```
=== skills-index : .../gen_skills_index.py --skills .../redproof/project-trajectory/skills --check ===
gen_skills_index: STALE - .../redproof/project-trajectory/skills/INDEX.csv does not match
the SKILL.md files; run `python scripts/gen_skills_index.py`.
  FAIL  skills-index     exit 1 (0.0s)
```

Both defects are the *real* failure modes: a prompt template edited without
regenerating, and a `SKILL.md` added without regenerating.

### Verification

`python project-trajectory/scripts/check.py --jobs 0` → **RESULT: PASS**, with
both new steps in the **gating** section (not the advisory tier) — which is the
`{G1,G2,G3}` decision visible in the output:

```
Check summary (gate G1, tier all):
  PASS  registry-integrity 0.3s
  PASS  derived-gate     0.1s
  PASS  privacy          1.1s
  PASS  doc-navigability 1.0s
  PASS  skills-index     0.1s
  PASS  prompt-catalog   0.0s
```
<!-- fig: cmd="python project-trajectory/scripts/check.py --jobs 0" rev=d960d127 -->

The shipped hook exercises them — run directly as
`KIT_SCRIPTS_DIR=project-trajectory/scripts sh project-trajectory/hooks/pre-commit`,
and again by the two real commits of this WI:

```
=== skills-index : .../gen_skills_index.py --skills .../project-trajectory/skills --check ===
  PASS  skills-index     0.1s
=== prompt-catalog : .../gen_prompt_catalog.py --check ===
  PASS  prompt-catalog   0.1s
```
<!-- fig: cmd="KIT_SCRIPTS_DIR=project-trajectory/scripts sh project-trajectory/hooks/pre-commit" rev=d960d127 -->

`trace.py --strict` → rc 0; `check_trajectory.py --strict` → rc 0. All generated
surfaces `--check` fresh (`arch-map`, `okf`, `trajectory-map`, `status-map`,
`open-items`, `derived-gate`, `ratify-fresh`, and now both new ones).

Suite, on the committed tree: **2227 passed, 5 skipped in 393.96s** over `2242`
collected, i.e. the full unfiltered suite minus the **10** tests of
`tests/test_agent_loop_critique.py`.
<!-- fig: cmd="python -m pytest -q -n auto --ignore=tests/test_agent_loop_critique.py" rev=881a46ce -->
**The arithmetic ties to the baseline exactly**, which is the real evidence that
nothing regressed: `2228` baseline passed `+ 9` added here `− 10` excluded
`= 2227`, with the skip count unchanged at `5`. (An earlier run of the same
command at `d960d127` read `2223 passed, 9 skipped` — the four extra skips are
env-gated tests, which is why the committed-tree figure is the one quoted.)
Smoke bar: **917 passed, 6 skipped in 18.11s**.
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=d960d127 -->

**That exclusion is a measured pre-existing defect, not this row's.** See the
finding below; it reproduces byte-for-byte at `a1144566`, the commit before this
WI's claim.

### Findings surfaced, not fixed here

1. **The full-suite bar is unrunnable for seven hours a day (pre-existing,
   reproduced at base).** `tests/test_agent_loop_critique.py` hangs — every test
   in it — on a weekday between **12:00 and 19:00 UTC**. The chain:
   `conftest.set_process_key(..., seed=True)` seeds a test repo's
   `docs/process.toml` from `project-trajectory/process.toml.template`; that
   template has declared `blackout = "12:00-19:00"` since `f862cc72` (it shipped
   `blackout = ""`, disabled, when `docs/process.toml` was introduced at
   `c560f928`); `critique_repo` is the only session-driving fixture that calls
   `set_process_key`, so it is the only scaffold that inherits a live window.
   `agent_loop` then correctly honors it and sleeps — measured
   `blackout_wake("12:00-19:00", 2026-08-11T14:22Z) == 16650` s (4 h 37 m) — so
   the test blocks rather than fails. Confirmed by running the module at
   `a1144566` in a detached worktree: identical hang, same
   `time.sleep`-in-`blackout_wait` stack. The other ten agent_loop / dispatch /
   dual-plan modules were probed under a hard 240 s timeout and all PASS, so the
   blast radius today is exactly this one module. Two candidate fixes for a
   follow-up row, deliberately not chosen here: seed test scaffolds with
   `blackout = ""`, or restore the template's shipped default to `""` and let an
   adopter opt in. **This one deserves an id** — a bar that silently blocks for a
   third of the day teaches people to skip it.
2. **A pre-existing lint error**, unrelated to this row and untouched:
   `tests/test_id_watermark.py:82` `E741 Ambiguous variable name: 'l'`. It is why
   the advisory `lint` step reads FAIL above; the other advisory FAILs
   (`traceability`, `doc-refs`, `figures`) are the open ratification window and
   other WIs' closed spec files.
3. **The smoke membership ratchet has thin headroom** — `923` of the declared
   `max-tests = 930` after this row's 8 in-process tests. The next few in-process
   modules will need a re-stamp.
4. **`skills-sync` sits at `{G3}` while its sibling `skills-index` now sits at
   `{G1,G2,G3}`**, which reads as an asymmetry. It is defensible (the per-agent
   copies are a downstream materialization concern), but its recorded reason is
   "G3 only, like the other generated-artifact freshness gates" — a
   copy-the-neighbors reason, which is exactly the reasoning this row was told
   not to reproduce. Surfaced as a separate question rather than changed inline.

### Deliberate non-changes

`_TRUNK_FRESHNESS_STEPS` gains neither step. The `[generated]` section declares
*ownership*, but that set encodes which owners the **trunk** can mechanically
regenerate — and `trunk_step.py`'s `REGEN_STEPS` re-derives six document families,
neither of these among them (`docs/stack.ini` records that asymmetry explicitly).
Standing them down on a branch would leave the artifact ungated on the only side
that can fix it (the branch editing the `SKILL.md` / prompt template) and
unfixable on the side that gates it. This matches `skills-sync`'s own exclusion.

Untouched as instructed: `OWNER_SCRATCHPAD.md`, `docs/repo-lock.md`,
`docs/plans/*`, every registry row's text, and `docs/requirements/*.toml`
content. SN-010's prose amendment remains sitting territory — this row makes the
need true, it does not edit the need.

## Context

**SN-010 is a ratified core stakeholder need**, and it is stated universally:
*every* generated artifact carries a `--check` freshness contract. A universal
claim is false the moment one instance fails it. Two do.

**This row makes the need TRUE; it does not edit the need.** SN-010's own prose
is sitting territory (the 2026-08-10 prose-rewrite plan) and is out of scope
here, as are `docs/repo-lock.md`, `docs/plans/*`, and any registry row's text.

**Why this is worse than an ordinary gap.** Both artifacts are declared in
`docs/stack.ini`'s `[generated]` section — the §5.2 declaration of *what the
repo owns as derived*. A declaration with no enforcer is the shape SN-008
forbids from the other direction: the tree asserts a contract that nothing
holds it to, so a reader (human or agent) reasonably concludes the artifact is
gated when it is not. `CATALOG.md`'s whole purpose is to answer *"which prompt
template did that session use"* from a session log's `prompt-sha` — a lying
catalogue is worse than no catalogue, as its own module docstring says.
`INDEX.csv` is what an agent reads to decide whether a skill applies.

**The three decisions this row owns**, to be argued from the precedents rather
than assumed: each step's gate set (the existing spread is real —
`derived-gate` at `{G1,G2,G3}`, `ratify-fresh` at `{G2,G3}`, the doc-freshness
family at `{G3}`); whether the INDEX staleness check folds into the existing
`skills-sync` step or becomes its own; and whether the shipped reference CI
(`project-trajectory/ci/check.yml`) needs any change — it invokes `check.py` as
a single entry point, which must be *verified* rather than assumed.

**Non-vacuity is the acceptance bar, not a nicety.** Wiring a check that cannot
fail converts a visible gap into an invisible one. Each new step must be shown
red against a planted defect, in a temp tree, with the proof kept as a test.
