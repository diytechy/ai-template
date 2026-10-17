# WI-922 adjudication 004: amendment of SR-154's Requirement

I judged the one amended cell at `b35809891`. Since the anchor (`247dc36c4`), SR-154's `requirement` is the only line that moved in the SR registry. The SR rung is released (`human_approval_through = "DevStg-Boundary"`).

## amendment

- [CLARITY] SR-154 Requirement -> the delivered loop content "shall, when unattended work reaches integration, obtain" each required review or critique verdict from a non-author session, routed across declared families with documented degradation, every selection logged and non-convergence escalated, "and, where a claimed work item is marked for an in-lane single plan, refuse build output at its making or landing until a pass record binds its plan and Done-when" -> "shall obtain, when unattended work reaches integration," the same verdicts under the same routing, logging and escalation, and the same single-plan refusal -> identical obligation.
  - **What moved:** the one verb now precedes the when-clause, so the clause binds only the "obtain" predicate. The `Where` clause alone now conditions the refusal.
  - **What the attestation already says:** the recorded reading this row was blessed under is that the unattended condition scopes only the routing predicate and the planning hold rides the one `shall` as its own predicate. Sitting WI-913/011 re-attested SR-154 on exactly that reading, under the owner's choice recorded as D-008.
  - **Why the word had to move:** placed before the verb, the condition could be misread as also scoping the hold, as if an attended lane's single-plan commits were held only at unattended integration. The gate this row decomposes to holds an attended lane at every lane commit and at its landing.
  - **Why it is clarity:** the edit removes that misreading without changing what the row obliges. No routing term, condition, actor or refusal is added or dropped, and every approved word is kept. An implementation correct under the blessed reading of the old text (routing at unattended integration, the hold wherever a claimed row is marked single) is correct under the new one, and the new text forbids nothing that reading allowed. No file or carrier is named.

VERDICT: CLARITY rows=1

**Aftermath:** the row keeps its attestation. This session re-anchors it on the released rung, in its own act commit:

`python project-trajectory/scripts/intake.py snapshot --reattests SR-154`

SITTING: JUDGED kinds=amendment
