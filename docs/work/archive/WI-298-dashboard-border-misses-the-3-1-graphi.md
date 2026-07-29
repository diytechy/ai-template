+++
id = "WI-298"
title = "Dashboard --border misses the 3:1 graphical-boundary floor in both themes (004-CRITIQUE A4, OPENAI-SOL) - the --border token supplies the boundary for focusable .view regions, detail cards and linked Process-stage rectangles, but measures light #e2e8f0 = 1.23:1 on --surface #ffffff and 1.18:1 on --bg #f8fafc, dark #1e293b = 1.22:1 on --surface #0f172a and 1.29:1 on --bg #0b1120, against the 3:1 floor the accessibility rubric's A4 states for graphical/UI boundaries. All four ratios re-verified independently. NOTE THE CRITIC DISAGREEMENT: 116-CRITIQUE (OPENCODE-GROK) dismissed this under WCAG 1.4.11's identifiable-by-other-means exception (a card with a text label needs no boundary contrast); 004-CRITIQUE (OPENAI-SOL) held that these particular elements ARE controls - focusable regions and links - so the exception does not apply. Owner ruling needed, same reason as WI-297. Fix if upheld: theme-specific boundary colours reaching 3:1 against every adjacent surface, or another persistent boundary cue meeting the same threshold. Distinct from WI-293, which fixed TEXT-on-fill contrast, not boundaries."
workstream = "dashboard"
sr_refs = ["SR-052"]
buildtier = "medium"
safety_class = "ordinary"
disposition = "retired"
order = 295
+++

## Deliverable

RETIRED 2026-07-24 as NOT-A-DEFECT, owner-ruled after verification against the artifact. The finding claimed --border supplies sub-3:1 boundaries for 'focusable .view regions, detail cards, and linked Process-stage rectangles'. Checked: --border appears in exactly FOUR rules - `nav.tabs`, `#process .gnow`, `#process .pflow li`, `#process .stg rect` - and `.view` has NO border rule at all (its only styling is `.view svg{display:block}`), so that half of the finding is factually wrong. The one genuine CONTROL among the four is the Process stage rectangle inside `<a class="stg">`, and those carry VISIBLE TEXT LABELS (Intake / Triage -> WIs / Resume loop / ...) - exactly WCAG 1.4.11's stated exception, a component identifiable by its text label needs no 3:1 boundary - and they additionally switch to --accent at stroke-width 2 on hover/focus. So 116-CRITIQUE (GROK), which dismissed this under 1.4.11, read it correctly, and 004-CRITIQUE (SOL) over-claimed. Kept as a RETIRED row rather than deleted so the over-claim AND its refutation stay traceable - this is evidence about critique reliability, not just a dead finding. The genuinely broken contrast SOL was standing next to is the FOCUS RING, which is real and lives in WI-299.
