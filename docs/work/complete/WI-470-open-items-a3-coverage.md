+++
id = "WI-470"
title = "SR-052 coverage: bring gen_open_items.py inside the mechanized A3 no-colour-alone closure, and word the dashboard's two thin spots — the process-flow 'you are here' tier (accent border, no word) and the hero-meter identities (which-meter-is-which rides fill colour). The C-ACC-2 remainder: the candidate itself was ruled matched-to-SR-052 (sitting-3 §0.4 item 8, 2026-08-17; log 2026-08-17h) because SR-052's Approved text already states no-information-by-colour-alone with LLR-113/TC-118 mechanizing it — what is left is exactly this coverage work, not a spine row."
workstream = "dashboard"
sr_refs = ["SR-052"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Extended the A3 no-colour-alone closure to `gen_open_items.py` with two
targeted regression tests — the diff-mark shape-cue CSS pin (del keeps
line-through, ins keeps its box-shadow underline substitute) and the
kind-pill distinct-wording render check over a real page carrying both
pill kinds (the case a CSS-only check cannot catch); the module's idioms
were already correct, so the closure gained TESTS, not source change.
Gave the process-flow "now" marker a worded `nowtag` cue — deliberately
accent TEXT on surface (6.29:1 light / 5.98:1 dark, the `.pflow .g` idiom)
after measuring the filled-badge alternative at 2.98:1 in dark theme,
below the dashboard's own A4 floor. Gave each hero meter an `aria-label`
naming itself independent of its sibling label and fill colour. The
`.empty` border ruled out of A3 scope with the reasoning in-file; the
retired accessibility rubric deliberately not widened. Three new tests;
targeted suites 83+120 passed; smoke green.

## Context

Filed 2026-08-17 out of the item-8 ruling at the sitting-3 desk (log
`2026-08-17h`). The C-ACC-2 candidate ("no verdict, gate outcome or status by
colour alone, on any surface") was dispositioned **matched to `SR-052`** —
whose text already states the obligation for the state view, mechanized as
`LLR-113` → `TC-118` (`test_a3_every_painted_vocabulary_member_is_explained_in_words`
plus three drift guards) — and the alignment record annotated accordingly.
The measured remainder is narrower than the candidate and is this WI
(grounding: `docs/plans/2026-08-17-wi468-obligation-intake-options.md` §4):

1. **`gen_open_items.py` is outside the mechanized A3 sweep.** Its idioms are
   good — ins/del carries line-through + box-shadow "so the grouping survives
   a monochrome print"; pills carry words — but they are held by comment
   discipline, not by the closure. Extend the A3 painted-vocabulary closure
   (or an equivalent test) to the open-items surface, so a colour-only
   encoding added there fails rather than shipping.
2. **The process-flow "you are here" tier** marks the current stage with an
   accent border and no word — one panel away from a plain-text "Next gate"
   sentence. Give the now-marker a worded cue.
3. **The two hero meters**: the values are texted, but which-meter-is-which
   rides fill colour. Give each meter a worded identity at the meter.

Out of scope: any spine-row change (the candidate is dispositioned; `SR-052`
is `Approved` and its text already covers the obligation); the rubric's
declared scope (`docs/rubrics/dashboard-accessibility.md` names
`PROJECT_STATE.html` — widening it to the open-items surface is part of item
1 IF the executing session finds that the cleanest closure home, and its own
call otherwise); `LLR-113`'s recorded same-document narrowing and the JS
detail-badge exclusion, both recorded limits that stand.
