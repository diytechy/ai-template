# WI-834 round 7: spine change list (answers round 020's observations O1, O2)

The builder changed no registry row's text. O1's and O2's pins joined
existing tests (TC-339's QUOTED_DENIED, TC-345's in-process opt-in test).
`Word` (already in LLR-300's `code_symbol`) changed its attribute, not its
name. One trace cell pair changed: the round took `coordinator_guard.py` past
the 1000-line module ratchet, so the opt-in's ownership and merge moved into a
new pure module, `kitlib/guard_hooks.py` (D-023).

- LLR-322 `module`: before `…/dev-setup.template.ps1;project-trajectory/scripts/coordinator_guard.py`,
  after `…;project-trajectory/scripts/coordinator_guard.py;project-trajectory/scripts/kitlib/guard_hooks.py`.
- LLR-322 `code_symbol`: before `offer_hooks/OfferHooks;hooks_state/enable_hooks`,
  after `offer_hooks/OfferHooks;hooks_state/enable_hooks;guard_groups/bind/command_shapes/merged`
  (each new function tagged `Implements: SR-032, LLR-322`).

The proposals below refine round 6's (`019-SPINE-CHANGES-r6.md`), which
refine round 5's.

## LLR-300, `detail` (O1 and 020's wording note): refines 019's clause

- **019's proposed clause:** "reads a PowerShell assignment, recognised by
  its operator whatever its target, as running its right-hand command, while
  a quoted or variable right-hand value stays data"
- **Proposed now:** "reads a PowerShell assignment, recognised by an unquoted
  assignment operator wherever it stands (quotedness is known for every
  character of a word), whatever its target, as running its right-hand
  command; a quoted right-hand value and a variable right-hand value stay
  data, while a chained assignment whose final right-hand side is a command
  runs that command"
- **Why:** 020 observation O1, which also asked that the wording not imply
  that the first quoted piece stands for every later operator's quotedness.
  020's deferred wording note asked to distinguish a variable value (data,
  `$r = $other`) from a chained assignment that launches (`$a = $b = claude`,
  D-022). Still optional: sitting 017 found "any command word" covers the
  case.

## LLR-322, `detail` (O2): refines 019's merge clause

- **019's proposed merge clause:** "replacing only the guard's own commands
  and preserving every other command, its group's configuration and
  unrelated settings"
- **Proposed now:** "replacing only the guard's own commands (a command is
  the guard's only in the exact shape the shipped example defines: an
  interpreter, either the example's own word or a bound absolute path, then
  the guard's script and hook subcommand) and preserving every other command,
  including one that merely names the guard's file, its group's
  configuration and unrelated settings"
- **Why:** 020 observation O2. Ownership by filename mention deleted a user's
  `ruff check …/coordinator_guard.py`.

## TC-339, `method` (O1): refines 019's

- **019's proposed method clause:** "PowerShell assignments of any target
  form (property, index, array-type, scoped, comma list, chained) with
  command, quoted and variable right-hand sides"
- **Proposed now:** "PowerShell assignments of any target form (property,
  index, array-type, scoped, comma list, chained), with the operator spaced
  or written against a word that holds a quoted piece, and with command,
  quoted and variable right-hand sides"

## TC-345, `expected` (O2): refines 019's

- **019's proposed first clause:** "… replacing only the guard's own
  commands, so a user command sharing a group with a guard command keeps its
  place and its group's matcher, …"
- **Proposed now:** "… replacing only the guard's own commands, defined by
  the shipped example's command shape, so a user command sharing a group
  with a guard command (one that names the guard's file included) keeps its
  place and its group's matcher, and an older bare-`python` guard command is
  replaced by the bound one, …"
