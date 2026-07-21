# Rubrics (`docs/rubrics/`)

A **rubric** is the written reference a `Critique`-verified requirement is judged
against — the instrument that makes *subjective* acceptance ("a realistic-looking
render", "the two artifacts read as the same scene") auditable instead of left to
whoever happened to ship it. It is read by an **independent critical eye** (an LLM
one, deliberately separated from human `Attest`; process-options.md "Critique
verification & the critique loop"), never by the session that produced the
artifact.

Why it exists: an implementer session cannot judge its own output, and the
original TC may have been lax — a project shipped awkward render artifacts because
"the agent didn't know how to judge it, it just shipped it". The critique loop
gives another agent a *different hat* to say **where and why** something isn't good
enough, and drives rework toward a written bar rather than a fresh opinion each
round.

## Derived from the SN/SR intent, never from the TC

A rubric is written from the **stakeholder-need / system-requirement intent** — what
"good enough" *means* — **not** from the test case. That inversion is the point: a
lax TC is caught and hardened rather than inherited. When a critique round proposes
a measurable sub-criterion, it routes through the change-intake flow (process.md
§5) to harden the TC — the critic never edits the spine.

## Shape

A rubric file is `rubric-<name>.md` (see the worked example
[`rubric-000.md`](rubric-000.md)):

- **An intent statement** — one paragraph naming what acceptance means, in the
  stakeholder's terms, traced to the SN/SR it derives from.
- **Numbered good anchors (`G1`, `G2`, …) and bad anchors (`B1`, `B2`, …)** —
  definite, citable entries describing what constitutes good and known-bad
  patterns (seam artifacts, impossible shadows, floating geometry), *the same way
  test cases are called out*. Each anchor is a numbered, referenceable line; a
  critique **verdict cites anchor ids**, which is what makes rounds comparable
  across sessions.
- **The artifact recipe** lives on the TC's `Parameters` cell (the command/steps
  that produce the screenshot/render/output under judgment) — the rubric names the
  bar, the TC names how to produce what's judged.

## The accumulation rule (the reference builds over time)

A critique finding that names a **new** failure mode is added to the rubric's
bad-anchors as a **new `B#` line at rework**, so the next round judges against the
**accumulated** reference, not a fresh opinion. This is how the rubric stops being
the quality ceiling: it grows every time the critic finds something the last
version missed. Verdicts and the lax-TC ratchet both look for exactly this — a
`CHANGES-REQUESTED` round that closes without hardening the TC **or adding an
anchor** trips the no-validation-delta warn (`check_trajectory --staged`).

## What a rubric is not

Not a second source of truth. The requirement lives in the `SN→SR→LLR→TC` spine;
the rubric is the *judgment reference* for the subjective slice the TC can't pin.
Durable references inside a rubric are `SN-/SR-/TC-` ids or in-repo paths — never
session-local codenames.

The `-000` example is inert (it names no real requirement), so a fresh scaffold
that never adopts `Critique` verification carries it for free.
