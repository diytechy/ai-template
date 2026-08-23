+++
id = "WI-099"
title = "Mechanize the trace/derive_gate rule-set sync promise (M1)"
workstream = "scripts"
order = 98
+++

## Deliverable

Extracted trace.py's inline LLR-exempt literal to a named LLR_EXEMPT constant (mirrors derive_gate.LLR_EXEMPT) and added tests/test_rule_sync.py pinning the two files' duplicated *policy* equal — LLR_EXEMPT set-equality plus behavioral is_draft/sn_draft_ids equivalence — so the orphan report and the derived gate can't silently disagree. Plumbing loaders (refs/load_csv) left to drift per F5. No spine change (G3). Full suite 700 passed.
