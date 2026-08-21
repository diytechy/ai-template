+++
id = "WI-490"
title = "Retire the mechanical-ratification arm: the refusal becomes the ruled shape and the docstrings say who MAY move a Status cell (OI-45 ruled (b), 2026-08-20)"
specref = ""
workstream = "scripts"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Executes OI-45's ruling (b) RETIRE THE ARM as a **record-only** row: the
code deletion (the write loops and `copy_live`) had already landed at the
2026-08-20 batch review's iterate pass (MINOR-12), so this WI's job was
making every touched docstring/comment say the question is RULED, not open.

- **`intake.flip_verified`** — the docstring paragraph framing "what the
  `flip` arm still has to move" as an open question now states the ruled
  shape: mechanical ratification is retired, permanently, and the
  distinction is about the SCRIPT, not agent judgment. Its inline comment
  above the no-anchor-owed note updated the same way.
- **`intake._apply_flips`** — docstring rewritten to state OI-45's ruling
  in place of the (a)/(b) open question, keep the two candidate shapes as
  history (what D-9 step 7 left open, what got ruled), and drop the "the
  ruling could restore a writer here" hedge. The trailing comment after the
  refusal loop (documenting the MINOR-12 deletion) updated the same way.
- **`intake.adjudication_action`** — gained a paragraph noting that even
  where this returns `"flip"`, `_apply_flips` writes nothing; the name
  survives only to route the caller's brief text.
- **`intake._cmd_adjudicate`** and the `adjudicate` subcommand's `--help`
  text — both now say the subcommand recommends, never enacts, since a
  subcommand whose only act is refusal must say so where its help text and
  docstring speak (the CLI surface — flags, subcommand name — is unchanged,
  so no RESYNC entry is owed).
- **`intake._cmd_snapshot`** — gained a paragraph stating ratification
  authority was deliberately NOT mechanized (OI-45 is the record) and that
  this refresh is the ONE mechanical toucher of the approval record.
- **`trace.is_founded`** — docstring split D-9 consequence 2 into its two
  halves: whether a tool ever writes the cell stays open, but whether an
  agent-authored `Founded` is itself an error is now answered (sanctioned,
  under the declared human-ratification level) — cites OI-45 rather than
  claiming the whole question open.
- **`docs/registry-machinery-reference.md`** — the `Founded` row repeated
  the same now-stale "still open" claim about `is_founded`; corrected to
  match, since a live reference doc restating a retired framing is the same
  defect class the WI exists to close.
- **The scope-note rule applied throughout**: every touched surface says
  "ratification was deliberately not MECHANIZED," never "no agent may ever
  move a Status cell" — an LLM session or adjudicator is still expected to
  flip a row's Status to `Approved`/`Founded` for spine content past the
  declared human-ratification level (`agent_common.human_holds` says
  which). A repo-wide grep for `100% human`, `only a human`, `never
  mechanically` found no other live occurrence of the overstatement this
  WI's scope note warns against (the hits outside `tests/`/archived plans
  are about unrelated judgments — spec-correctness, PlanMode/SafetyClass
  conflicts — not this arm).
- **Tests**: no test pinned the retired docstring text or the deleted
  write-and-copy block by source grep (confirmed by search); the smoke
  suite's behavioral pins on `flip_verified`/`_apply_flips`/
  `adjudication_action` are untouched and still green, so the MINOR-12
  deletion did not regrow. `tests/test_module_size_ratchet.py` re-stamped
  `trace.py` (4989 -> 4993) and `intake.py` (1864 -> 1901) with reasons —
  docstring-only growth, no executable line moved.
- **No RESYNC_PACK.md entry**: the CLI surface (subcommand name, flags,
  behavior) did not change shape, only its stated meaning — the WI's own
  condition for owing one is not met.

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
