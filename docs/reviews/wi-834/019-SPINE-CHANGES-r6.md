# WI-834 round 6: spine change list (answers narrow round 018 F1, F2)

The builder changed no registry row's text, and no trace cell this round:
F1's and F2's pins joined existing tests (TC-339's QUOTED_DENIED /
QUOTED_ALLOWED, TC-345's in-process opt-in test). The new private helpers
(`_operator_end`, `_tail`, `_without_guard`, `_merged`) carry no
`Implements:` tag, like the existing ones, and the tagged `_assigned` is
already in LLR-300's `code_symbol`. These changes add to round 5's list
(`017-SPINE-CHANGES-r5.md`). The construction choices round 6's directions
leave open are D-022.

## LLR-300, `detail` (F1): round 5's optional clause, widened

- **Round 5's proposed clause:** "reads a PowerShell assignment's right-hand
  command as a command word while a quoted or variable right-hand value stays
  data"
- **Proposed now:** "reads a PowerShell assignment, recognised by its
  operator whatever its target, as running its right-hand command, while a
  quoted or variable right-hand value stays data"
- **Why:** 018 F1. Round 5 recognised assignments by target shape, which
  missed property, index and array-type targets. The clause stays optional:
  sitting 017 found "any command word" already covers the case.

## LLR-322, `detail` (F2): round 5's proposed text, one clause added

- **Round 5's proposed text, its merge clause:** "by merging the guard hooks
  into the machine-local settings, each command bound to the floor-resolved
  interpreter that runs the opt-in, while preserving existing hooks and
  unrelated settings"
- **Proposed now:** "by merging the guard hooks into the machine-local
  settings, each command bound to the floor-resolved interpreter that runs
  the opt-in, replacing only the guard's own commands and preserving every
  other command, its group's configuration and unrelated settings"
- **Why:** 018 F2. Round 5 replaced whole groups, so a user command sharing a
  group with a guard command was deleted.

## TC-339, `method` (F1)

- **Round 5's proposed method clause:** "PowerShell assignments with command,
  quoted and variable right-hand sides"
- **Proposed now:** "PowerShell assignments of any target form (property,
  index, array-type, scoped, comma list, chained) with command, quoted and
  variable right-hand sides"

## TC-345, `expected` (F2)

- **Round 5's proposed expected, its first clause:** "Consent enables the
  coordinator hooks in the machine-local settings, bound to the opt-in's
  interpreter, by preserving existing settings and hooks"
- **Proposed now:** "Consent enables the coordinator hooks in the
  machine-local settings, bound to the opt-in's interpreter, replacing only
  the guard's own commands, so a user command sharing a group with a guard
  command keeps its place and its group's matcher, and preserving existing
  settings and hooks"
