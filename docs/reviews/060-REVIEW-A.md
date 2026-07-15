### REVIEW-A — WI-146 — 2026-07-14
Findings:
- [MAJOR] project-trajectory/scripts/check_trajectory.py:1069 -> the lint treats any `trace.py --ratify` text as proof that a ratification brief links the generated hierarchy, so a brief can pass while carrying no view at all (or only an unexecuted/wrong-scope command) -> require a Markdown link to a generated ratification view and test that a command mention without that link still warns -> @owner
- [MAJOR] project-trajectory/scripts/trace.py:974 -> the generated `SN -> SR -> LLR/TC` view prints only each SN id, omitting the stakeholder Need, Why it matters, and acceptance intent despite the WI requiring the tree with full registry prose; the observed `--ratify v3` output begins `## SN-010` with no SN prose -> parse and render the selected SN rows' prose before their SRs, with a fixture assertion -> @owner
VERDICT: CHANGES-REQUESTED findings=2
