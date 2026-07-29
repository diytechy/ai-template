+++
id = "WI-293"
title = "Dashboard dark-theme hub contrast fails WCAG AA (116-CRITIQUE A4) - the Process working-loops hub paints `.hub rect{fill:var(--accent)}` with white labels (`.hubname{fill:#fff;font-size:13px}`, `.hubsub` at 0.85 opacity); under prefers-color-scheme:dark --accent is #818cf8, so #ffffff on #818cf8 measures 2.98:1 against the 4.5:1 AA floor for normal text (hubsub ~2.57:1). Light theme is 6.29:1 and fine, which is why earlier passes missed it - the defect is dark-theme-only. Verified independently against the emitted artifact; visible in 1280px-dark-process-full.png. Fix: give the hub a dark-theme fill that keeps >=4.5:1 against white (e.g. hold the light #4f46e5 for the hub), or move the label to --text on a darker fill; re-check `.hubsub` at its reduced opacity. BLOCKS WI-273: SR-052's rubric requires every anchor and A1/A2/A3 already pass on the current render, so A4 is the ONLY thing standing between WI-273 and an APPROVE critique."
workstream = "dashboard"
sr_refs = ["SR-052"]
buildtier = "medium"
safety_class = "ordinary"
order = 290
+++

## Deliverable

Fixed 2026-07-24 (hand-applied, owner-directed 'fix A4 then land WI-273'). The Process hub fill moved off --accent onto a new THEME-INVARIANT --hub token (#4f46e5, declared in :root and deliberately NOT overridden in the dark block), and .hubsub lost its fill-opacity:.85 discount - the same rule .sub/.bsub already followed. White-on-fill measures 6.29:1 in BOTH themes, up from 2.98:1 (name) / 2.57:1 (sub) in dark; verified against the emitted artifact and the re-shot 1280px-dark-process-full.png. VALIDATION CHAIN (the point - the fix must not land in the artifact alone): test_a4_theme_token_fills_behind_white_text_meet_the_floor is new and closes the actual gap the sibling A4 tests had - they check palette CONSTANTS, so a fill declared as a per-theme var() was invisible to them; test_a4_hub_fill_is_not_the_page_accent guards the regression; and test_a4_no_sub_label_opacity_discount was moved from the with_bundle fixture to with_gate, where .hubsub actually renders - under with_bundle that guard was VACUOUS for it (it passed with the defect reintroduced). All three were confirmed to FAIL against the original code before being kept. Ratchet re-stamped 4587 -> 4598 (mostly the rationale comment). Unblocks WI-273: A4 was the only anchor SR-052's rubric still failed.
