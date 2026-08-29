+++
id = "WI-527"
title = "Build the component-side contract header: the grammar, the generated reference, its gate and the adopter migration (OI-66 ruled (a))"
specref = ""
workstream = "architecture"
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

The mechanism `OI-66` ruled: a module states each contract beside the code, and
a committed, freshness-gated `docs/interface-reference.md` harvests them. Record:
[../../../log.d/2026-08-29-wi527-contract-header.md](../../../log.d/2026-08-29-wi527-contract-header.md);
adversarial round in
[../../../reviews/2026-08-29-oi66-build-round/](../../../reviews/2026-08-29-oi66-build-round/).

**The binding precondition first.** The `Contracts:` marker must OPEN its line
and PARSE as an id list. Line-start alone was insufficient and the review proved
it: `Contracts: not IF-080; an example, not a declaration` opens correctly and
still leaked the id. `handback.py`'s false positive is gone.

**The grammar.** Bodies open `Contract IF-###:` — not a bare `IF-###:`, because
that is ordinary docstring prose and only a form nobody writes by accident is
safe to hard-fail on. Four refusals: body before the marker, undeclared id,
duplicate body, and an HTML comment that could close the generated document's own
end marker.

**The mechanism.** `--contracts-doc` mirrors `--cli-doc` exactly; wired as a
`check.py` step, a `[generated]` row, a `trunk_step --regen` step and a member of
the pre-commit hook floor. Stated contracts lead the reference; unstated
declarations are one compact line per module.

**A false green closed for all eleven declared artifacts**, not just this one: a
`[generated]` row naming an absent FILE now fails `staged_divergence`, because
every freshness step is vacuous on an absent target and deleting a declared
artifact therefore disarmed its own gate in silence.

**No silent loss on upgrade.** `check_trajectory` names both lossy marker forms.
0 findings on this tree; proved to fire by planting one. Two real declarations
the tightening exposed were fixed rather than absorbed — `plan_artifacts.py`'s
semicolon separators (grammar widened; this tightens against prose, never
against a separator style already in use) and `handback.py`'s denial (reworded).

**Adopter migration:** PROCESS.md section 8, `interfaces.template.toml`, and a
`RESYNC_PACK.md` entry with the grammar change, its search recipe, and the
instruction not to bump each IF row's `version`.

**Not done, and stated rather than hidden:** the 71-row cell pass (two rows done
as proof — `IF-013`, `IF-144`); `IF-134`/`IF-135` remain undeclared because the
git hooks are extensionless and a `*.py` scan cannot see them; and the reverse
check is still id-global rather than provider-exact.

## Context

`OI-66` ruled (a) GO on 2026-08-29, priced against `WI-512`'s measured analogue.
The ruling made the harvester fix a binding precondition, sequenced before any
cell moves.

## Done when

- [x] The harvester fix lands first.
- [x] The body grammar, its refusals and their tests.
- [x] The generated reference, its freshness gate, and hook-floor membership.
- [x] The adopter migration.
- [x] A cross-family adversarial round, its confirmed findings applied.
- [x] Commit bar green; ratchets re-stamped deliberately with reasons.
