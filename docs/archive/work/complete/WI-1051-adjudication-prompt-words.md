+++
id = "WI-1051"
title = "The adjudication prompts: the act names the repository's own scripts path, and first acceptance asks for ACCEPT"
workstream = "process"
sr_refs = ["SR-231"]
needs = []
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 3
planmode = "none"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1051`, cut from `refactor_again` at
`3c33b3783`, with the commit hooks on. No status moved, no act was taken, no
id was minted, and no requirement, design-row or test-case text was written
or amended. The specref (the queue-drill hand-off) is cleared at close, as a
terminal row's is. No decisions record was needed: the act takes the
`{scripts}` value exactly as the reviewer and worker briefs do, strict fill
included, so nothing called for a design call.

- `8ff6581dc`: the two templates, the act assembler, the tests, the
  regenerated catalogue, TC-368's regenerated evidence and the regenerated
  views. The hook passed (29 steps, all PASS; its readability step warned
  that touching `adjudicate_act.py` and `tests/test_adjudicate_act.py`
  surfaced their existing flag-axis debt, a positional `False` and the
  two-flag `_verdict` helper, both present before this row and neither
  gating).
- `28b768377`: the `RESYNC_PACK.md` §4 entry the three shipped files owe,
  anchored at `3c33b3783` (the smoke checks' re-sync step refused the
  branch without it). It says the composed act reads as before in a
  scaffold, and that an operator override of `ADJUDICATE-ACT` must now
  declare `{scripts}`. The hook passed (29 steps, all PASS).
- The commit after it: the close-out, this Deliverable, the move to
  `complete/` and the log fragment.

**1. The act names the repository's scripts directory.** The act template
declares a `{scripts}` slot in its notes, and its two instruction lines now
read `python {scripts}/intake.py snapshot --reaccepts ...` and
`python {scripts}/intake.py snapshot --accepts "..."`. `act_values` fills
`scripts` from `agent_brief.scripts_dir`, the value `review_brief` and
`agent_brief` give the reviewer and worker briefs, and renders both act
parts' commands from the same value, so `compose_act` fills it. A new test,
`test_the_filled_act_names_the_repositorys_own_scripts_directory`
(`tests/test_adjudicate_act.py`, tagged TC-368), composes the act of a
combined verdict in a repository laid out like this one
(`project-trajectory/scripts/check.py`) and in a scaffold
(`scripts/check.py`): the act carries exactly two commands, each running
`project-trajectory/scripts/intake.py` and `scripts/intake.py`
respectively, and all four mentions of the script name that directory. It
was red on the this-repository case before the fix. Two existing tests
followed the change: the coordinator-act stub adjudicator
(`tests/test_coordinator_act.py`) found commands by the literal
`python scripts/intake.py snapshot` and now finds them by the script name in
any directory, and the act brief's pinned slot set
(`tests/test_routing_and_prompts.py`) gains `scripts`. The module's IF-296
docstring says it now also reads the repository's scripts layout.

**2. ACCEPT, not APPROVE.** The first-acceptance template's "`APPROVE` only
when EVERY row you were shown is accepted" now reads "`ACCEPT` ...". A new
test, `test_every_machine_line_word_a_brief_asks_for_is_one_its_grammar_reads`
(`tests/test_prompts.py`, under that module's TC-157 tag), reads every brief
whose verdict closes on one machine line against the grammar its verdict is
parsed with: the eight adjudication classes with a `VERDICT_GRAMMAR` entry,
and the reviewer and critique briefs against the review line. The machine
line a brief writes out on its own line offers exactly its grammar's labels
and fields; one it quotes inline names only labels and fields the grammar
reads; and every verdict word quoted in its prose is one of those labels,
the keyword, or a tag of a row line the brief lays out. Run against the
pre-fix template it is red on the first-acceptance brief alone ("asks for
APPROVE, which its grammar (OUTCOME: ACCEPT|RETURN) does not read"); all ten
briefs pass after it. A companion test pins that the table names no brief
twice and holds the first-acceptance and combined briefs. The dispute brief
is outside it: it asks for one ruling line per finding, read by its own
parser.

**3. The catalogue.** `prompts/CATALOG.md` is regenerated:
`ADJUDICATE-ACT` `sha256:fc26ac978cf5` -> `sha256:0e5396336320`, with
`{scripts}` added to its slots, and `ADJUDICATE-FIRST-ACCEPTANCE`
`sha256:e5bc38971b88` -> `sha256:2ab89245b39e`.
`gen_prompt_catalog.py --check`: `fresh (14 prompts)`.

**Tests**, each line the real summary, at `8ff6581dc`:

- the modules importing the act assembler (`trace.py --tests-for
  adjudicate_act` and a grep of the importers), the modules holding TC-368's
  and TC-157's tests and the ones reading the two templates or the
  catalogue, and `test_import_layers.py`, `test_module_size_ratchet.py` and
  `test_dogfood_sync.py` (sixteen modules):
  `584 passed, 1 skipped in 1641.19s (0:27:21)`
  <!-- fig: derived="pytest -q -n 6 over the sixteen modules named on this line, at 8ff6581dc" -->
- `trace.py --root . --strict`: exit 0, `orphans=0 integrity=0` (`Traceability: SN=31 SR=138 LLR=355 TC=422 orphans=0 integrity=0 ...`)
- `check_trajectory.py --root . --strict`: exit 0, `check_trajectory: clean (1053 work item(s), 921 done (87%), 37 cancelled, graph acyclic).`
- the re-sync pack's readers (`test_resync_pack.py`, `test_check_resync.py`,
  `test_kit_path_invariant.py`, `test_held_rung_doctrine.py`,
  `test_generated_newlines.py`), at `28b768377`'s tree: `55 passed in 10.93s`
  <!-- fig: derived="pytest -q -n 4 over the five modules named on this line, at 28b768377's tree" -->
- `run_menu.py smoke`: `3737 passed, 3 skipped, 18 warnings in 293.37s (0:04:53)`, every step passing (`check_trajectory: clean (1053 work item(s), 922 done (88%), ...)`, `check_docs: OK ... 0 broken`, `check_resync: OK, 3 shipped path(s) changed`), with a CPU budget WARN only (908.6 s against 540 s on a box shared with four other builders)
  <!-- fig: derived="python project-trajectory/scripts/run_menu.py smoke, at the close-out tree after 28b768377" -->

**Acts owed for automated adjudication: none.** No row's text was written
or amended, and no row was added. TC-368's `evidence` cell gained the new
test by regeneration from its tag; `evidence` is a traced cell that routes
no adjudication (a test case's `verifies` is the one that does), and the new
`tests/test_prompts.py` tests fall under TC-157's file-level evidence,
which did not change.

**Left for the coordinator, not done here:**

- LLR-338's accepted Detail says "A first-acceptance APPROVE act" and "held
  APPROVE", the word the first-acceptance grammar refuses; so do the act
  template's dispatcher notes and one sentence of the act assembler's module
  docstring (neither is sent to a session). Amending LLR-338 is an
  Accepted-row amendment this row's Done-when did not ask for.
- Downstream: an operator override of `ADJUDICATE-ACT` written against the
  older template does not declare `{scripts}`, and the strict fill now
  refuses it, naming the slot, until the override adds it. That is the rule
  a reviewer override already lives under.

**Review** (the coordinator, 2026-11-22; queue-drill HANDOFF §4 step 4).
Round 1 over `3c33b3783..345522e9a`, the generated views and this spec's
copies withheld and the spec at the tip given whole. OpenAI Sol
(`gpt-6.1-sol`, low) read the whole diff, and Gemini Hydrogen
(`gemini-4-hydrogen-low`, the Antigravity CLI) the prose: the two
templates, the catalogue, the re-sync entry and the log fragment. Both
APPROVE, no findings. LLR-338's accepted Detail still says "APPROVE"; it
goes to WI-1018's list of stale row text, not to this row.

## Context

Filed on trunk on 2026-11-22 by the queue drill's coordinator, from the two
automated adjudication sittings run by hand (WI-1047, WI-1049; queue-drill
HANDOFF §3.7). Two prompt templates say something other than what the code
reads:

- **The act brief names an adopter's path.**
  `project-trajectory/prompts/adjudicate-act.template.md` hard-codes
  `python scripts/intake.py snapshot ...` in its instructions (lines 65 and
  66) and in the commands `adjudicate_act.compose_act` fills. That is the
  path in a scaffolded repository; in this repository the script is
  `project-trajectory/scripts/intake.py`, so an act taken here exactly as
  the brief words it fails, and the coordinator substituted the path by
  hand at both sittings. The reviewer and worker templates already take a
  `{scripts}` placeholder (`scripts` in a scaffolded repository, the kit
  master's path here; `prompts/CATALOG.md`).
- **The first-acceptance brief asks for a word its grammar refuses.**
  `adjudicate-first-acceptance.template.md` line 106 says "`APPROVE` only
  when EVERY row you were shown is accepted", but the section's machine line
  takes `OUTCOME: ACCEPT rows=N` or `OUTCOME: RETURN rows=N`, and the
  verdict grammar knows no APPROVE. Both sittings had to tell the
  adjudicator in a preface to read ACCEPT there.

The two stay one row on purpose: both are adjudication prompt templates
whose words disagree with what the code reads, both are found by the same
kind of test (a filled template read against the code), and both
regenerate the one prompt catalog.

## Done-when

- [x] The act template's commands name the repository's scripts directory
      through the same `{scripts}` value the reviewer and worker templates
      take, and `compose_act` fills it; a test shows the filled act naming
      `project-trajectory/scripts/intake.py` in this repository and
      `scripts/intake.py` in a scaffold.
- [x] The first-acceptance template asks for `ACCEPT` where it says
      `APPROVE`, and a test reads every machine-line word a template asks
      for against its section's verdict grammar.
- [x] `prompts/CATALOG.md`'s hashes and placeholder lists are regenerated.
