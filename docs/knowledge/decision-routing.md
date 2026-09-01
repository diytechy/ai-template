# Decision routing evidence: decide / record-for-affirmation / escalate

This pack preserves the 2026-08-31 research base for the "decisions for owner
review" question — whether agent decisions can be routed among deciding
silently, recording for a non-blocking owner second look, and escalating
(handback / open item), and what signal should drive the routing. The design
itself is undecided; this pack holds the evidence, not the ruling.

## Findings retained

**LLM confidence is not a usable primary routing signal.** The Anthropic
Messages API exposes no logprobs (verified against the live parameter list,
2026-08-31), ruling out token-probability methods entirely. Verbalized
confidence is better calibrated than logprobs on RLHF models (Tian et al.,
EMNLP 2023) but systematically overconfident and dominated by prompt wording
(Yang et al., arXiv:2412.14737: 17 prompt methods spanned ~7% to near-random
ECE). Self-consistency sampling fails directly: GPT-4.1 reached agreement
>=0.8 on 77% of GPQA items and was wrong 48% of the time in exactly that
high-agreement regime, and a confidence-routed cascade lost to always using
the mid-tier model (Ding, arXiv:2607.08065). Multi-model panels are less
independent than they look: a 9-judge, 7-family panel yielded ~2.18 effective
votes, with Claude x Gemini the most error-correlated pair (phi = 0.603;
Kohli, arXiv:2605.29800). Whether extended thinking helps calibration is
contested in both directions (arXiv:2505.14489 vs arXiv:2508.15050).
Usable residue: confidence works only as a ONE-WAY RATCHET — low self-report
or panel dissent may promote a decision to more scrutiny; high confidence or
consensus may never demote one.

**Practitioners route on action properties, not model introspection.** The
convergent industry pattern gates on reversibility tier (free-undo /
compensable / partially-reversible / irreversible) crossed with blast radius,
with categories pre-authorized in advance (ITIL standard changes; Renovate's
semver tiers: patch auto-merges, major needs a human — with autonomy EARNED
by an observation window, not granted on day one). The AI Control literature
(Greenblatt et al., ICML 2024; Lindner et al., arXiv:2512.22154) supplies the
operating rule: the escalation threshold is DERIVED FROM REVIEWER CAPACITY —
a human who can audit 2% of traffic needs a monitor calibrated to ~2% FPR.
The dial is a budget, bounded by construction, not an open-ended risk score.

**Agents recognize but do not volunteer.** Models judge ambiguity correctly
60-80% of the time when explicitly asked, yet spontaneously flag it under 5%
of the time when just told to do the task; more retrieved context REDUCES
flagging (Su & Cardie, arXiv:2605.25284). A separate detector agent beat
self-monitoring-via-reminder-prompt by 8 points on underspecified SWE-bench
(UA-Multi 69.4% vs UA-Single 61.2%, arXiv:2603.26233). Prompted transcript
auditors cap out around 74% risk-recognition vs an 89% human baseline
(R-Judge, EMNLP Findings 2024), need >20% false positives to reach 80%
detection (Anthropic SHADE-Arena), and degrade as transcripts lengthen
(classifier context rot, arXiv:2605.12366) — a backstop, never the net.
The fix with measured support is structural: a REQUIRED per-decision field
removes silence as an option (the disclosure analogue of this kit's own
`split_decided_by`, itself born from the 2026-08-03 merged-rejected-code
incident and the one mechanism here with a proven record of converting an
implicit judgment into an explicit one).

**Review queues decay measurably unless filtered and instrumented.** Clinical
decision support overrides run 90%+ pooled (Health Informatics J 2024), with
only ~7% of alerts judged appropriate in one study — a low-precision queue
manufactures false assurance. At 1% target prevalence, reviewers miss over
4x more than at 50% — a criterion shift that diligence and expertise do not
fix (Wolfe, Nature 2005); complacency and automation bias survive training
and instruction, and only structural change helps (Parasuraman & Manzey,
Human Factors 2010). Explanations INCREASE acceptance of wrong
recommendations without improving accuracy; showing confidence alone did as
well (Bansal, CHI 2021) — a queue entry should carry checkable evidence, not
reasoning narrative. Review capacity has three independent limits: per item
(~200-400 LOC-equivalent; Google's median reviewed change is 24 lines), per
session (~60 min), and per period (total review volume negatively predicts
detection — Chromium OS study, arXiv:2102.06909). What actually detects a
rubber stamp: seeded known-bad items (content-moderation "reverse quality
sampling"; aviation TIP) and instrumenting the reviewer (affirmation rate
trending to 100%, time-per-item trending to zero).

**Autonomy-ladder precedent.** Sheridan & Verplank's 1978 levels 5-8 map
onto escalate / veto-window / record / decide-silently: level 6 (execute
after a delay unless countermanded) is a distinct tier that degrades into
"record" when the owner is away and "escalate" when watching. Shipping
products use a few NAMED MODES, not a continuous slider. "Defer to
conservative" (take the reversible default and record it) converts would-be
escalations into recordings — a fourth outcome beyond the three tiers.

**This repo's own measured evidence** (2026-08-31 survey): the
decisions-for-review pattern arose ad hoc three times (72 entries total);
4 were ever affirmed, nothing machine-reads the files, and the declared
prose format degraded within one session (21 of 46 entries carried the
`Decided:` field). The one affirmation that happened was per-sitting with
exceptions, recorded as a ratify-style commit quoting the owner — not a
per-entry queue worked down. 44 of the 46 most recent entries were
supervisor-altitude decisions about running the loop, an altitude the
OI-70 adjudicator-exits doctrine does not reach.

## Application here

- Route on FIELDS AND COUNTS over the action (reversibility, registries
  touched, kit files touched), never on a matcher over prose or a model's
  self-assessment — the same instrument class OI-41's ruling chose, for the
  same bounded-error reason.
- Any recording obligation should be a required structured field on an
  artifact already produced and already validated (the `split_decided_by`
  pattern), not brief prose or a post-hoc auditor.
- Size any owner-review surface from the owner's real capacity first, then
  set what qualifies to fill that budget; keep its precision high enough
  that reading it stays worth doing.
- Land records where the owner already stops (a sitting, a ratify record, a
  generated band on the open-items surface) rather than minting a new inbox.
- If a detector pass is wanted, make it a separate agent with its own
  context, run per-segment on long transcripts, reading visible reasoning.

## Failed or bounded approaches

- Confidence-thresholded escalation: wrong-at-high-agreement is common
  (48% in-regime error) and cascades measurably underperform fixed policies.
- Panel consensus as assurance: ~2 effective votes from 9 judges; dissent
  informs, agreement does not.
- "Escalate when uncertain" as an instruction: <5% spontaneous flagging
  against 60-80% recognition — silence must be structurally impossible,
  not discouraged.
- Exhaustive per-entry human review: the override/prevalence literature and
  this repo's own 4-of-72 affirmation rate agree it decays into reflex.
- A prose entry contract without a schema: degraded within one session here
  (the 2026-08-31 file), the same class OI-41 called "a mechanizable gap
  rather than a cultural one."
