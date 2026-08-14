+++
id = "WI-454"
title = "Land SN-033's declared need-cell checker as a PLACEHOLDER, while the tier is clean (owner-ruled 2026-08-13u, sitting-2 decision 7 rider 2). SN-033 is RATIFIED and its acceptance commissions a check that does not exist: 'A declared check reports the row and phrase when a need cell contains an internal path, implementation-only identifier or process citation; a reviewed exception list distinguishes names that are themselves user-facing interfaces.' Measured 2026-08-13: 0 of 27 need cells carry such a token (the prose batch cleaned them) and 16 of 27 ACCEPTANCE cells do — correctly exempt, since SN-033 scopes itself to need cells only. So the check would report ZERO findings today, which is exactly why it lands NOW: it locks the clean state in ahead of the SR re-tier's churn rather than trusting a large pass not to dirty it. Shape (the kit's existing pattern, not a new one): a stdlib check_need_form.py in the check_* lint family, wired into check.py's step table WARN-FIRST (the DEFAULTED tier), scanning each need cell for path-like and implementation-identifier tokens against a declared exception list that ships EMPTY; the first row to dirty the tier is the one that reports. Verification: a unit test that constructs a dirty need cell and asserts the row AND the offending phrase are both named (the acceptance requires both), one asserting a user-facing interface name on the exception list passes, and one asserting the live registry is clean at zero findings. Scope guard: warn-first only — do not gate on it without an owner ruling, and do not scan acceptance or engineering-requirement cells (SN-033 exempts them by its own text)."
specref = "docs/plans/2026-08-13-sitting-2-boundary-and-context.md#decision-7--the-duplication-policy-for-the-re-statement-pass"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 2
+++
