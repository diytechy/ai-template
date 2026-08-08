<!-- ============================================================
DISPATCHER NOTES (delete this block before sending the prompt)

Disposition adjudication: a worker declared its attempt Partial or Cancelled;
this session confirms or overrides that call and drafts the successor. Send to a
FRESH session; strong tier; a family other than the implementer's where
available. Authoring and source-separation rules: README.md in this directory.

*** THE ONE RULE THIS TEMPLATE EXISTS FOR (SR-156) ***
The brief NEVER carries the worker's own rationale. The outcome event has a
`rationale` field; it is a declared source class of its own
(`worker-rationale`) and it is PROHIBITED here. A live adjudication brief once
opened with the judged party's verdict clipped mid-word, and everything after it
read as confirmation. The judge gets the frozen scope, the outcome ENUM, the
branch facts and the harness result — the defendant's account is not evidence
about the defendant.

There is no `{{RATIONALE}}` slot in this file and there must never be one. If
you find yourself adding one, you are building the incident.

Slots:
  {{WI_ID}}            = the attempted work item's id. Source `registry`.
  {{WI_TITLE}}         = its Title cell. Source `registry`.
  {{SCOPE_AT_CLAIM}}   = the spec body as FROZEN at claim — the obligation the
                        branch was not allowed to edit. Source `spec`.
  {{SCOPE_DIGEST}}     = the scope digest recorded at claim. Source `ledger`.
  {{DECLARED_OUTCOME}} = the enum ONLY: partial | cancelled. Source `ledger`.
                        Never the rationale, never a commit subject, never a
                        folder name someone inferred it from.
  {{BRANCH_COMMITS}}   = `git log --oneline` over base..HEAD. Source `diff`.
  {{BRANCH_CHANGES}}   = `git diff --name-status` over base..HEAD. Source `diff`.
  {{CLASSIFICATION}}   = the per-group keep/discard/quarantine labels the branch
                        owes before it may land (decision D-7). Source `ledger`.
  {{HARNESS_RESULT}}   = real output of the declared bar on the branch tree.
                        Source `harness`. Never a claim that it was green.
  {{DOWNSTREAM}}       = work items that depend on this one, id + title +
                        status. Source `registry`.

Output contract: `disposition-v1` (the block at the bottom of the body). The
disposition is APPENDED to the ledger; it never edits the worker's outcome
event, and the successor is a newly minted work item, never the original
revived (decision 6).
============================================================ -->

You are adjudicating the DISPOSITION of an attempted work item. A worker
declared the attempt did not complete. Your job is to rule on that declaration
from the record, and — if scope remains — to draft the successor that carries
it.

**You have not been shown the worker's own account of what happened, and that is
deliberate.** Do not ask for it, do not reconstruct it, and do not treat its
absence as evidence of anything. The scope says what was owed; the branch and
the harness say what arrived. Judge the distance between them.

## What you have

### The work item

{{WI_ID}} — {{WI_TITLE}}

### The scope, frozen at claim (the obligation)

{{SCOPE_AT_CLAIM}}

Scope digest at claim: {{SCOPE_DIGEST}}

This text is immutable for the life of the attempt. If the branch appears to
have delivered something else well, it still did not deliver this.

### The declared outcome

{{DECLARED_OUTCOME}}

That is an enum and nothing more. It is the claim under judgement, not evidence
for it.

### What the branch actually contains

{{BRANCH_COMMITS}}

{{BRANCH_CHANGES}}

### The keep / discard / quarantine classification the branch owes

{{CLASSIFICATION}}

### The declared bar, as it actually ran

{{HARNESS_RESULT}}

### Work items waiting on this one

{{DOWNSTREAM}}

## The rule you are applying

Rule on TWO things, in this order.

**1. The outcome.** Compare the frozen scope against the branch and the harness.

- **confirm** — the declared outcome matches the record. Partial: some of the
  scope arrived, green, and the rest did not. Cancelled: none of the scope
  should now be delivered — the need dissolved, it was superseded, or it was
  based on a premise the record refutes.
- **override-complete** — the whole scope is present and the declared bar is
  green on it. A worker may under-claim; a green complete attempt filed as
  partial still owes nothing.
- **override-partial** — filed Cancelled, but real, wanted work landed and the
  remaining scope is still owed. Cancelled discards a need; that is not what
  happened here.
- **override-cancelled** — filed Partial, but the remaining scope should not be
  pursued at all. Say why in REASON: this closes a need, which is a bigger act
  than it looks.
- **insufficient-evidence** — the record cannot support any of the above. Name
  what you would need. A guess here mints a successor for work nobody wants or
  closes a need nobody agreed to close.

Two traps, both of which have happened:

- **A green bar is not a complete attempt.** The bar proves the tree is healthy,
  not that the scope arrived. Check the scope's own done-conditions against
  BRANCH_CHANGES before you accept `override-complete`.
- **Unclassified changes are not landable.** If CLASSIFICATION does not cover
  every change group, that is a refusal to record, not a detail to wave through.
  A returned branch once merged green and landed rejected code as-is, precisely
  because nothing forced that call into the open.

**2. The successor.** If scope remains owed after your verdict, draft exactly one
successor work item carrying the REMAINING scope — never the whole original, and
never the original revived. It supersedes the attempt by lineage; the attempt's
record stays as it is.

- SUCCESSOR-SCOPE states what is still owed, in the scope text's own terms, and
  explicitly excludes what already landed and was kept.
- SUCCESSOR-TIER is `quick` for mechanical off-spine work, `medium` by default,
  `strong` for design-shaping or spine-touching work. A partial attempt is
  evidence about difficulty; use it.
- If nothing remains owed, `SUCCESSOR: none`. Minting an empty successor to look
  thorough costs a real session to discover and close.

## What you must not assume

- Do not assume the worker was wrong. Overriding is a power, not a duty; most
  declarations are honest and the record usually confirms them.
- Do not assume the worker was right either. `confirm` needs the same evidence
  `override` does.
- Do not infer a reason from a commit subject, a branch name or a folder. Those
  are bookkeeping, and every defect this layer exists for came from someone
  deriving an outcome from one of them.
- Do not widen the successor. Adjacent work you notice is a separate item for
  the ordinary intake, not scope you attach to a successor nobody asked for.
- Do not edit the scope, the spec, or the branch. Your output is a record.

## Output

One block, nothing else:

```
VERDICT: confirm|override-complete|override-partial|override-cancelled|insufficient-evidence
DELIVERED: <what of the frozen scope demonstrably arrived, or none>
REMAINING: <what of the frozen scope is still owed, or none>
CLASSIFICATION: accept|incomplete
SUCCESSOR: mint|none
SUCCESSOR-TITLE: <one line, or none>
SUCCESSOR-SCOPE: <the remaining scope, in the frozen scope's own terms, or none>
SUCCESSOR-TIER: quick|medium|strong|none
REASON: <one to three sentences, citing the branch or harness evidence you used>
MISSING: <on insufficient-evidence only: exactly what you would need>
```
