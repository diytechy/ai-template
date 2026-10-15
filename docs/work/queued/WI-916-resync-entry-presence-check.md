+++
id = "WI-916"
title = "A change to a shipped kit file passes the commit bar only when it adds its re-sync entry, anchored at its trunk base"
workstream = "process"
sr_refs = ["SR-036"]
specref = "docs/plans/2026-10-11-review-churn/README.md#6-run-the-strict-lints-after-every-build"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = ["~WI-914", "~WI-913"]
+++

## Context

Filed on trunk on 2026-10-14 by the attended coordinator, split from the
review-churn batch row B2 (WI-914) at filing under S1 (coordinator-2026-10-14
D-004). It carries plan item 6's second proposal and
K4's retirement from its third, under ruling 6. `RESYNC_PACK.md` §5 records
that "nothing enforces 'a kit change that needed an entry got one'"; the
reviewer rubric's K4 holds it by attention. The plan's sample counts a missed
entry among the findings an instrument would catch. The converse cost is on
record too: WI-823's only gate finding demanded an entry for a
`scope: this-repo` skill, and a dispute sitting dismissed it because that skill
never ships.

## Deliverables

1. **`scripts/check_resync.py`.** It is this repo's tooling, beside
   `check_smoke_budget.py` and `check_changed.py`, and untraced like them; no
   RESYNC entry.
   - **The change it judges:** from its trunk base to the working tree,
     untracked files included. The base is `agent_common.default_base`: the
     lane's merge base with trunk, and HEAD on trunk. So the staged squash at
     landing is judged against its parent.
   - **The rule:** if any changed path is shipped, the working tree's pack
     must add at least one entry heading that the base's pack lacks. Every
     added heading's anchor must resolve to the base itself, which is the
     recipes' "anchor the entry at the landing's parent". Otherwise the check
     exits 1, naming each shipped path and the reason.
   - **Shipped** (closed by the one inventory, with no second list): a path
     under `project-trajectory/` that `bootstrap.delivery_inventory()` does
     not exclude, read at the base and in the working tree, so a file that
     stops shipping still owes an entry.
     - The generator sources (`bootstrap.py`, `LICENSE`) count as shipped.
     - A kit path the inventory has not classified counts as shipped (deny by
       default).
     - A path outside `project-trajectory/` never ships.
   - **An entry:** a heading in §3 or §4 that matches the pack's entry grammar,
     `ENTRY_RE`. The grammar moves from `tests/test_resync_pack.py` into the
     check, and the test imports it, so it keeps one home. These do not count:
     an edit to an existing entry, a `### Reserved:` placeholder, a `pre-`
     anchor.
2. **Wiring.** The check joins `docs/stack.ini` `[run] smoke` after WI-914's
   lints and before the budget check, so every build round's bar and the
   landing commit run it. It does not go in:
   - the pre-commit hook (ruling 6);
   - a built-in `check.py` step, which ships to adopters, and adopters have no
     pack;
   - a `[step:]` with `paths`, because `check.py --path-triggered` runs those
     in the hook.
3. **Retirements and records:**
   - K4 retires from `docs/rubrics/kit-change-review.md`.
   - `RESYNC_PACK.md` §5's "nothing enforces" sentence says what the check
     holds (presence and anchor) and what stays with review (whether the entry
     says enough).
   - `docs/enforcement-audit.md` gains the rule's row.
4. **Tests in `tests/`** that fail before the change. They cover a shipped
   change with no entry, an entry anchored at another commit, an edited-only
   entry, a change only to a `this-repo` skill (no entry owed), a deleted
   shipped file, a change outside the kit, and an unreadable base.

## Trust

The pack's added heading is what lets this part of the bar pass, so the pack
gains a say over a gate input. Written before the claim, answering S2 under
`project-trajectory/PROCESS.md` §3, "When a guard is owed". The ruling goes
to the owner to confirm or overrule (coordinator-cycle §1 and §5).

- **Producer:** the lane's builder or the coordinator, editing `RESYNC_PACK.md`
  by hand in the same change. A failed write is any of: no added heading, a
  heading outside the grammar, a reserved placeholder, or an anchor naming
  another commit.
- **Consumers:** the new check only. Grepping `RESYNC_PACK` over `scripts/`,
  `project-trajectory/scripts/` and `tests/` finds no other mechanical reader;
  `tests/test_resync_pack.py` checks only the pack's shape.
- **Ruling:** the check refuses (exit 1) and states the reason for any of:
  - an absent or unreadable pack, at the base or in the working tree;
  - an unresolvable base;
  - an inventory that cannot be computed;
  - an added heading that fails the rules above.

  It never passes on an input it cannot read.
- **Binds to:** the headings the change itself adds between its base and the
  working tree, never a heading already present at the base.

## Done-when

- The check behaves as deliverable 1 states. Its tests fail on the code before
  the change and run in the smoke tier within its budget.
- `[run] smoke` runs it after the strict lints and before the budget check.
  The pre-commit hook is unchanged.
- K4 is gone from the rubric, and `RESYNC_PACK.md` §5 and the enforcement
  audit say what the check holds.
- The build starts only after the plan gate (WI-913) has landed, and the
  row lands after WI-914.
- The bar is green on the landing tip, and the landing's own entry passes the
  check.

## Scope answers

- **S1:** one deliverable set. The check, its wiring and K4's retirement land
  together, since the anchor retires only once the check holds it.
- **S2:** the pack gains a say over one input of the bar; see the Trust
  section.
- **S3:** closed. Shipped paths come from the one inventory, with deny by
  default for an unclassified kit path. An entry is one grammar with one
  anchor value, the base. The change is one range, base to working tree.
- **S4:** `single`. It promises behaviour over an input space (changed paths)
  and carries a Trust section, so it builds after the plan gate.
- **Architectural delta:** within scope. The bar's verdict gains a new input:
  the change's shipped paths against the pack's added headings. The check
  reads git and the delivery inventory, both existing boundaries. It adds no
  state or domain value and needs no preparatory refactor.
- **Dependencies:** WI-914, soft (its bar line, and the order in which
  mechanism changes land), and the plan gate WI-913, soft (`single`). No third-party dependency.

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-14; one finding):

- **S2, MINOR: adopted, as a citation rather than a link.** The Trust
  section now opens with "answering S2 under `project-trajectory/PROCESS.md`
  §3, "When a guard is owed"", the form WI-912's and WI-913's Trust sections
  use. A relative link would break when the claim moves this spec from
  `queued/` to `active/<branch>/`, one directory deeper.
