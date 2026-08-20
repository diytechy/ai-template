+++
id = "WI-490"
title = "Retire the mechanical-ratification arm: the refusal becomes the ruled shape and the docstrings say who MAY move a Status cell (OI-45 ruled (b), 2026-08-20)"
specref = "docs/requirements/open-items.toml#OI-45"
workstream = "scripts"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Executes OI-45's ruling — (b) RETIRE THE ARM, carrying the owner's scope
note. The dead-code deletion itself already landed at the 2026-08-20 batch
review's iterate pass (MINOR-12: the write loops and `copy_live` went with
the arm); what this WI owes is the RECORD and its accuracy:

- **`intake._apply_flips`** stops presenting (a)/(b) as an open question —
  the question RULED. The refusal is the permanent shape, OI-45 is the
  record, and the "the ruling could restore a writer here" hedge dies.
  Whether `flip_verified`/`_cmd_adjudicate` keep their names, signatures
  and CLI surface is the implementing session's smallest-change call — but
  a subcommand whose only act is refusal must SAY so where its help text
  and docstring speak.
- **`intake._cmd_snapshot`** states that ratification authority was
  deliberately NOT mechanized (OI-45 is the record) and that the
  authority-gated snapshot refresh is the ONE mechanical toucher of the
  approval record.
- **The scope-note rule, applied to every comment this WI touches:** the
  record says "ratification was deliberately not MECHANIZED" and never
  "no agent may ever move a Status cell." The owner's note (recorded in
  OI-45's ruling): an LLM session or adjudicator is fully expected to flip
  a row's Status to `Approved` and further to `Founded` for spine content
  past the human approval gate/level (`human_ratification_through`) — at
  the human's request, or when working through content the declared level
  does not hold to human ratification. The dial (`agent_common.human_holds`)
  says who holds what; the arm's absence says only that no SCRIPT decides.
  Grep the touched surfaces for overstatements ("100% human", "only a
  human", "never mechanically") and reconcile each against that line.
- **D-9 consequence 2 touchpoint:** `trace.is_founded`'s docstring calls
  "whether a hand-authored `Founded` is itself an error" still open. The
  ruling answers its authority half — an agent-authored `Founded` under the
  conditions above is sanctioned — so that docstring's pointer updates to
  cite OI-45 rather than claiming the whole question open.
- **Tests:** whatever pins the refusal text/behavior updates with the
  wording; verify the MINOR-12 deletion did not regrow. No RESYNC entry is
  owed unless the CLI surface changes shape — if it does, one is.
