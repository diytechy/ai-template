<!-- ============================================================
DISPATCHER NOTES (delete this block before sending the prompt)

Red-bar adjudication: the declared harness is failing on a tree that is
otherwise attested complete. This session sizes the remediation — is it a
defect, how big, at what tier, planned how, and over what scope. Send to a FRESH
session; strong tier. Authoring and source-separation rules: README.md in this
directory.

The failure event is keyed by tree, failing step and NORMALISED fingerprint, so
one defect raises exactly one adjudication however many cycles observe it. This
session sizes the remediation; ordinary queue admission still decides whether the
resulting draft may enter the queue.

Slots:
  {{BAR_STEP}}         = the declared harness step that failed, by name. Source
                         `harness`.
  {{FAILURE_OUTPUT}}   = its REAL output, verbatim, clipped head+tail if long
                         (say where it was clipped). Source `harness`. Never a
                         summary of the failure and never a claim about it.
  {{FINGERPRINT}}      = the normalised failure fingerprint. Source `ledger`.
  {{TREE}}             = the tree the failure was observed on. Source `ledger`.
  {{REQUIREMENT_ROWS}} = the SR/LLR/TC rows the failing step verifies, id +
                         text. Source `registry`.
  {{CODE_MAP}}         = the LLR module/symbol rows for the surfaces the failure
                         names. Source `registry`.
  {{PRIOR_FAILURES}}   = earlier failure events sharing this fingerprint, with
                         their trees and their dispositions, or "none". Source
                         `ledger`.

PROHIBITED: self-assessment. In particular, no session's account of having fixed
this, and no status prose claiming the bar is green. The output above is what the
bar did.

Output contract: `remediation-v1` (the block at the bottom of the body).
============================================================ -->

You are sizing the REMEDIATION of a red declared bar. The breakdown is attested
complete and the harness is failing anyway, so something is wrong: the code, the
test, or the requirement they were both derived from. Your job is to say which,
and to size the work that closes it.

You are not fixing it. Do not propose a patch, do not edit anything, and do not
speculate about a fix you cannot ground in the output below. An estimate built
on an imagined cause is worse than no estimate, because the queue will believe
it.

## What you have

### The failing step

{{BAR_STEP}}

### What it actually printed

{{FAILURE_OUTPUT}}

### Failure identity

Fingerprint: {{FINGERPRINT}}
Tree: {{TREE}}

### Prior observations of this same fingerprint

{{PRIOR_FAILURES}}

### The requirements this step verifies

{{REQUIREMENT_ROWS}}

### The code map for the surfaces named in the failure

{{CODE_MAP}}

## The rule you are applying

First, rule on what the red MEANS:

- **remediate** — real work is owed. The product is wrong, the test is wrong, or
  the requirement is wrong; say which in CAUSE, grounded in the output.
- **not-a-defect** — the failure is an artifact of the observation itself: an
  unsatisfied environment gate, a missing toolchain, a step that cannot run on
  this machine. Nothing is owed to the product, and something is owed to the
  harness's honesty about the gap. Say which in REASON.
- **insufficient-evidence** — the output does not identify a cause and you would
  be guessing. Name the run, the log or the row you would need. A red bar sized
  on a guess mints a work item whose scope is fiction.

Then size it:

- **SCOPE** — one line naming what must change, in terms of the modules and
  symbols in the code map, or the registry rows. Bounded: a scope that says "fix
  the tests" is not a scope.
- **TIER** — `quick` for mechanical, off-spine work; `medium` by default;
  `strong` for design-shaping or spine-touching work. A failure whose cause is
  the REQUIREMENT is strong by construction — changing an obligation is not a
  mechanical edit.
- **PLAN-MODE** — `single` when the shape of the fix is evident from the output;
  `dual-plan` when the fix is a design choice with real alternatives, touches
  more than one module or a declared interface seam, or when the cause is the
  requirement.
- **EFFORT** — `one-session` or `multi-session`. Say it from the scope, not from
  the size of the error message.

`PRIOR_FAILURES` is the sharpest signal you have. A fingerprint that has been
remediated before and is red again is not the same size of problem as a new one:
the previous fix addressed a symptom, and the scope should say so.

## What you must not assume

- Do not assume the test is wrong because the code is newer, or the code is
  wrong because the test is older. Both happen; the output usually says which.
- Do not assume a flake because a failure is unfamiliar. Flakiness is a claim
  that needs evidence — repeated observations with the same fingerprint and
  different outcomes — and `PRIOR_FAILURES` either shows it or does not.
- Do not widen the scope to adjacent problems you notice. They are separate
  items for the ordinary intake.
- Do not estimate to make the queue comfortable. An honest `multi-session` that
  gets scheduled beats a `one-session` that stalls a lane.

## Output

One block, nothing else:

```
VERDICT: remediate|not-a-defect|insufficient-evidence
CAUSE: product|test|requirement|environment|unknown
SCOPE: <one line, naming modules/symbols or registry rows>
TIER: quick|medium|strong|none
PLAN-MODE: single|dual-plan|none
EFFORT: one-session|multi-session|none
REASON: <one to three sentences, quoting the part of the output you relied on>
MISSING: <on insufficient-evidence only: exactly what you would need>
```
