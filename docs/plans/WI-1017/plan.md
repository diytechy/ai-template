# WI-1017 plan: an LLR yields to a sustainable design

Planned on the maintenance branch `maint/wi-1017`, cut from trunk
`refactor_again` at `0d67302bd`, after the evidence sample the first
Done-when item asks for. The sample's full record, case by case, goes in the
row's Deliverable at close; this plan states what it found in short and what
each finding changes.

## What the sample found

Chosen so no case is picked by hand:

- every entry naming an LLR or a design row in the decisions records of the
  thirteen most recent lanes that kept one (`docs/decisions/wi-971.toml`
  to `wi-997.toml`): 92 of their 145 entries;
- the Deliverables of the thirteen rows built on maintenance branches since
  (WI-999 to WI-1011), which kept no decisions record;
- the 136 review verdicts of lanes wi-960 to wi-1002, 44 of which answer the
  reviewer brief's change-intake question by name;
- the two most recent handbacks (WI-828, WI-902), every LLR retirement
  record (four), and WI-1015's measurement
  (`docs/reviews/2026-11-21-code-vs-interfaces/`).

The concern holds in one form. No lane changed a behaviour to satisfy an
LLR's text: where a row was found unsuitable (six review verdicts), the remedy
was that row's amendment, and 27 decisions entries and seven maintenance rows
reshaped rows with their design. But when the design changed shape, the row
set did not:

- **WI-1007** split `trajectory_arch.py` into five modules and minted no
  design row ("a new `Drafted` row under SR-159 would be design written for a
  refactor"); three checks no row binds were placed beside a bound rule
  instead of in modules of their own, and "one check per module" was left
  undone for want of a design row. wi-971 D-001 reads a refactor the same
  way: traced cells only, no spine row.
- No retirement in the record was for a design that divided its behaviour
  differently: all four LLR retirements follow a ruling that dropped a
  feature.
- Rows absorb code rather than split: 48 of 345 live LLRs list more than ten
  symbols, 62 span three or more modules.
- Row text is left trailing the code at the end of a lane (eight decisions
  entries, two maintenance rows): five by the rule that a MINOR after the
  gate never moves the gated tip, one more by the cost of reopening a sitting
  (wi-977 D-023), two by a spec's named set of rows (wi-977 D-014, D-024);
  in the maintenance rows, one to avoid amending an accepted row (WI-1007's
  LLR-172) and one by deferring the authoring to the operator (WI-1001:
  "whether LLR-366 is amended, or an LLR minted, is the operator's call"; no
  LLR states that rule today).

The causes inside the guidance this row's homes hold:

1. PROCESS.md §5's change intake has no branch for re-cutting several rows;
   its "code only" path adds rows on the existing modules, and its design
   replacement bullet names only an amendment.
2. The spine-authoring skill says "Keep IDs where meaning remains" and
   nothing about the other case.
3. The spine questions' §3 says a refactor keeps a row true, which is right
   for row text but was read as "a refactor never changes the row set".
4. This repository's builder agent tags each new function with "the LLR whose
   `module` is that file", the route by which rows absorb code, and its
   reviewer rubric (K3) repeats it.

Causes outside those homes are named in the Deliverable as rows to file, not
built here: the post-gate MINOR rule and the unfiled follow-ups it leaves
(the coordinator's procedure, `coordinator-cycle` recipes §3), the
amend-by-addition rule for accepted rows (recipes, "Brief Terra to amend an
accepted row by addition"), and the re-acceptance act's cost.

## What changes where

The statement has one home. Every other reader points at it.

| Home | Change |
|---|---|
| `project-trajectory/PROCESS.md` §5, "Change intake" | The design-replacement bullet becomes the statement (below). The chart gains a node `RD` for the re-cut, reached from a violated row (`parent sound; design re-cut`) and from a new scope's solution (`existing LLRs do not fit`), and feeding `W`. § numbering unchanged. |
| `project-trajectory/skills/spine-authoring/SKILL.md` (mirrors `.claude/skills/`, `.agents/skills/`) | Adoption step 4: "Keep IDs where meaning remains"; where it does not, the rows are re-cut under `docs/process.md` §5, design replacement. |
| `project-trajectory/skills/spine-authoring/references/in-lane.md` (same mirrors) | "Author the subtree in one pass" includes each row the design re-cuts, pointing at §5. |
| `project-trajectory/prompts/spine-questions.md` §3 (the skill's question home, composed into every LLR sitting's brief) | The bullet "Replace an unsuitable design through the normal amendment route" stops restating §5: it names what to compare and points at §5's design replacement, covering a mechanism at fault and rows that divide the design wrongly. |
| `project-trajectory/prompts/worker.template.md` (the shipped builder brief) | Its change-intake line covers bending the design to fit a row, and points at §5's design replacement; `tests/golden/worker-prompt-one-row.txt` follows. |
| `.claude/agents/kit-builder.md` (this repository's builder agent) | A row that no longer fits the design is reported with the re-cut §5 calls for, never fitted; a new function is tagged with the LLR whose stated behaviour it implements. |
| `project-trajectory/prompts/reviewer.template.md` (the shipped reviewer brief, rendered by `review_brief.py review` and the loop) | Its change-intake sentence asks whether a workaround, or a design bent to fit, preserves an LLR that no longer suits the design, pointing at §5's design replacement; the restated preservation sentence goes. |
| `docs/rubrics/kit-change-review.md` K3 (the reviewer rubric `review_brief.py review --rubric` appends for this repository) | The tag rule follows the builder agent's, and a row the design no longer fits is re-cut under §5, never kept by bending the design. |
| `docs/rubrics/scope-critique.md` S5 (the scope critique's rubric, rendered by `review_brief.py critique`) | After the delta question: where the change re-cuts the design, the spec names the LLRs it splits, merges, moves or retires (§5, design replacement). |
| `project-trajectory/RESYNC_PACK.md` §4 | One entry `[since 0d67302bd]`: the shipped files to overwrite (PROCESS.md, the skill and its reference, the three prompts) and the catalogue to regenerate. |

*Corrected at review (Sol, round 1):* the worker and reviewer briefs, the
builder agent, K3 and S5 each keep their own instruction and the §5 pointer,
and none restates the rule: no talk of bending the design to a row, no list
of the re-cut's verbs. The pin fails a reader that does either, or that
shares any five-word run with the statement.

### The statement (PROCESS.md §5)

> **Design replacement** — an LLR records the current design, not a
> commitment. When a sustainable design needs a different decomposition, the
> LLRs are split, merged, moved under another parent or retired (`retire.py`,
> naming each successor) under their tier's acceptance authority, rather than
> the design bent to fit them; the parent SR keeps its acceptance, and the
> enduring behavioral regression tests and parent constraints stay. One row's
> mechanism at fault is that row's scoped amendment. Moving code that keeps
> every row's stated behavior moves trace cells only; a design that divides
> the behavior differently re-cuts the rows. Keeping an unsuitable row, or
> bending the design to fit it, to avoid an acceptance act is a finding.
> Authoring is not acceptance. Use the `spine-authoring` skill questions to
> distinguish an unsuitable LLR from a changed stakeholder obligation.

Checked against the rulings it must not contradict: SR-186 (each child keeps
an independent purpose: a re-cut satisfies it, and SR-186 is not amended);
§4's keep-or-mint rule (a changed row leans to a new id: the re-cut mints and
retires); the review-churn plan's variant F (ruled, unbuilt: a refactor moves
traced cells and never reopens a requirement row, which the statement's
"moves trace cells only" keeps); the operator's 2026-11-19 ruling on tests
("architectural changes are permitted to keep code clean and modular"); and
authoring is not accepting (re-cut rows are `Drafted` until their authority
accepts them).

## Tests

Test first: one pin in `tests/test_prompts.py`, beside the briefs' other
one-home pins, written and run red before the text changes. It asserts that
PROCESS.md holds the statement once, in §5's change intake, with its clauses
(the four re-cut verbs and `retire.py`, the parent's acceptance kept, the
trace-only refactor, keeping-to-avoid-an-act as a finding); that the chart
has the `RD` node with its two inbound edges and its edge to `W`; that the
skill's "Keep IDs where meaning remains" is followed by what to do when it
does not; and that each reader (the skill, its in-lane reference, the spine
questions, the worker and reviewer briefs, the builder agent, the two
rubrics) names §5's design replacement and carries none of the statement's
opening sentence. It rides the module's file-level tag, as its sibling
`test_both_builder_briefs_search_before_minting_a_file_or_function` does:
this row adds no spine row (decision D-002).

Then run every module the change reaches: `tests/test_prompts.py`,
`tests/test_agent_loop_worker.py` (the golden worker prompt),
`tests/test_review_brief.py` (the scope rubric's pins),
`tests/test_adjudicate_brief.py` and `tests/test_hats.py` (the spine questions
composed into briefs), `tests/test_skills_sync.py`, `tests/test_dogfood_sync.py`,
`tests/test_bootstrap.py -k "byte_caps or size_budget"`,
`tests/test_import_layers.py` and `tests/test_module_size_ratchet.py`. The
byte-budget guard before and after; `trunk_step.py --regen` for the prompt
catalogue.

## How each Done-when item is met

1. The sample: above, and case by case in the Deliverable, each with its lane
   and what kept the row. It lands first, in this plan's commit.
2. The guidance lands whatever the sample found; since it found cases, each
   named cause in the four homes above is changed here, and each cause outside
   them is named as a row to file.
3. PROCESS.md §5's statement and the chart's `RD` branch.
4. The pointers in the table; "keep IDs where meaning remains" says what to
   do when it does not.
5. Nothing in the guidance rewards keeping an unsuitable LLR: the statement
   makes keeping one to avoid an act a finding, the builder agent and its
   rubric stop tagging new code by file, and the chart offers the re-cut where
   it offered only rows on the existing modules.

## Decisions (`docs/decisions/maint-wi-1017.toml`)

- **D-001**: the coordinator's procedure (`coordinator-cycle`, a this-repo
  skill) is read as outside the guidance this row changes; its two causes are
  rows to file.
- **D-002**: no spine row is minted; the pin rides `tests/test_prompts.py`'s
  file-level tag.
