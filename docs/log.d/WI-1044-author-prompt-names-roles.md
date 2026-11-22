## 2026-11-21 — WI-1044: the author's prompt template and TC-385 name roles; recipes §5's `\r` escapes restored

Deferred open items: none. The row changes text only and takes no operator
decision; it needed no decisions record.

Built on the maintenance branch `maint/wi-1044` from `1b22c9355`, with the
commit hooks on. The record is in the row's Deliverable
(`../archive/work/complete/WI-1044-author-prompt-names-roles.md`).

- **The template** (`f9aa0914f`).
  `scripts/coordinator/terra-spine-prompt.template.md` names the spine
  author, the builder and an independent adjudicator where it named "GPT
  Terra", "a Claude Opus builder" and "Claude Opus adjudicator". It holds no
  observation tied to one model. Its file name and its `@LANE_SLUG@-terra`
  basetemp path stay.
- **The pins:** the intent-form pin follows the new wording, and WI-1037's
  role pin now reads the template too (red on the prior template at 7
  sites, green after), the pin that makes the first Done-when item hold.
- **TC-385** (Accepted, text only): its method and expected cells name the
  author, critic and REVIEW-A calls where they named Sol and Terra; its
  status and evidence are unchanged.
- **Recipes §5:** the CR-count bullet's three escapes read `\r` again, in
  the source and its two copies, refreshed by `bootstrap.py --dest . --sync`
  and checked byte for byte.
- **Tests:** the 23 modules reading the template, the skill, its copies or
  the live test-case registry, and the whole-tree tests:
  `1011 passed, 2 skipped, 18 warnings in 572.87s (0:09:32)`.
  `run_menu.py smoke`: `1 failed, 3713 passed, 3 skipped, 18 warnings in 338.56s (0:05:38)`;
  the one failure is trunk's (the vocabulary check on WI-1024's queued
  spec, written at `1b15d07fb` and fixed on trunk at `dd8f79e6c`), with a
  CPU budget WARN only. `trace.py --strict`: `orphans=0 integrity=0`;
  `check_trajectory.py --strict`: clean.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Byte deltas:** no budgeted or watched file was touched. The template
  -49 bytes, `recipes.md` +3 in each copy, `test-cases.toml` +39,
  `tests/test_prompts.py` +172.
- **Acts owed:** TC-385's drift, for automated adjudication (the SR-243
  chain in `docs/ratify/CURRENT.md`).
- **Found, not changed:** SR-243 still names "Sol or Terra" in its
  requirement and acceptance; filed on trunk as WI-1046.
