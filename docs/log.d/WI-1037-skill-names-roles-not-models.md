## 2026-11-21 — WI-1037: the coordinator-cycle skill names each role, never the model that fills it

Deferred open items: none. The row changes text only and takes no
operator decision; its three calls are in the decisions record
(`../decisions/maint-wi-1037.toml`, D-001 to D-003).

Review: round 1, Argon (prose) APPROVE; Sol one MINOR, adopted: seven
observations' model labels restored as "observed with <model>"; its
request for a label-pinning test declined by the coordinator.

Built on the maintenance branch `maint/wi-1037` from `1aa6c439a`, with the
commit hooks on. The record is in the row's Deliverable
(`../archive/work/complete/WI-1037-skill-names-roles-not-models.md`).

- **The skill** (`97f2246dd`). The Roles table names each role (the
  builder, the author, the code reviewers, the critic, the adjudicator) and
  states no model or effort; a list under it says where each is set: the
  route (`codex_call.py`'s `ROLE_ROUTES` against `docs/agents.toml` and
  `docs/agents-enabled`, the adjudicator's default entry, `--route`), the
  builder's definition, and D-008 for the REVIEW-B stand-in. The recipes and
  `scripts/coordinator/README.md` name roles throughout, and their headings
  ("A `codex_call.py` call", "The author, first turn", "The author,
  resumed") follow. A gotcha seen with one model keeps its evidence as
  "observed with <model>". "Codex" stays where it names the CLI; file
  names, role ids and `codex_call.py` are unchanged.
- **The copies:** refreshed by `bootstrap.py --dest . --sync`; the
  skills-sync check reads 22 copies matching, the index fresh.
- **Tests:** a new pin, the cycle names each role and never the model that
  fills it (red on the prior text at 290 sites, green after); the TC-385
  blackout pin and three pins keyed to the old wording follow it, their
  names unchanged. The 14 modules reading the skill and the whole-tree
  tests: `522 passed, 1 skipped in 109.79s (0:01:49)`. `run_menu.py smoke`:
  `3699 passed, 3 skipped, 18 warnings in 355.60s (0:05:55)`, with a CPU
  budget WARN only. `trace.py --strict`: `orphans=0 integrity=0`;
  `check_trajectory.py --strict`: clean.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Byte deltas:** no budgeted or watched file was touched. The skill's
  `SKILL.md` +895 and `recipes.md` +1,029 bytes, the README +191.
- **Acts owed:** none. TC-385's text still names Sol and Terra; it is left
  as accepted (D-003).
- **Found, not changed:** `scripts/coordinator/terra-spine-prompt.template.md`
  names models; recipes §5's CR-count bullet has lost its `\r` escapes.
