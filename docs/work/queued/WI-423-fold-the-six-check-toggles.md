+++
id = "WI-423"
title = "Fold the six remaining check-enablement toggles into docs/process.toml, or rule that they stay files. SN-028 consolidated ~10 one-word policy files into one TOML home and left SIX behind, naming them in the shipped template rather than omitting them quietly: docs/trajectory-check, docs/interfaces-check, docs/components-check (check_trajectory.py), docs/subagent-gate (subagent_gate.py), docs/live-status (agent_loop.py) and docs/okf-export (gen_okf.py). The stated reason each was left is real and is the whole question this row has to answer: every one is read by an INDEPENDENTLY COPYABLE checker that imports nothing of the config layer, so folding it in means each of those scripts grows its own local tomllib reader - a genuine cost paid five times over, against a benefit (one home) that is real but smaller for a toggle than for a policy. DECIDE IT, do not drift: either (a) fold them, accepting five small local readers and stating the F5 duplication in docs/dupes-allow like every other sanctioned copy, or (b) RULE that check-enablement is a different KIND of declaration from process policy - it answers 'is this check on', not 'how is work processed' - and record that line in process.toml's header as a decision rather than as a to-do. Whichever way it goes, the shipped template's paragraph 4 must stop describing an open question."
workstream = "scripts"
specref = "project-trajectory/process.toml.template"
buildtier = "medium"
safety_class = "ordinary"
+++

## Context

`project-trajectory/process.toml.template` currently says, in its own header,
that these six are "NOT YET HERE, and this file would be lying if it did not
say so". That honesty is right for a template mid-consolidation and wrong as a
permanent state: a header that describes an open question invites every future
reader to re-open it.

The line the template draws today — "those six answer 'is this CHECK on', not
'how is work processed'" — is already a defensible ruling. It may simply need
to be *stated as one*. The alternative is a real cost with a real benefit, and
the point of this row is that somebody weighs them once and writes down the
answer, rather than the question surviving another program.

Note the asymmetry that makes (a) more expensive than it looks: these checkers
are the ones an adopter copies individually. A local TOML reader in each is not
just five copies of a function, it is five copies of the *shape contract* the
hooks' sh parse depends on (`agent_common.process_shape_findings`), and that
contract is exactly the thing SN-028's review found five fail-OPEN bugs in.
