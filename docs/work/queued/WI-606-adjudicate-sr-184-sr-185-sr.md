+++
id = "WI-606"
title = "adjudicate: SR-184, SR-185, SR-186, TC-209, TC-210, TC-211 first approval after perspective-review amendment"
workstream = "process"
sr_refs = ["SR-184", "SR-185", "SR-186"]
needs = ["WI-625"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["SR-184", "SR-185", "SR-186", "TC-209", "TC-210", "TC-211"]
+++

## Context

First-approval batch for the authored Drafted H2/H3/H5 rows. Read each row's whole chain and the actual independent review/Inspection evidence: SR-184/TC-209 (Critique provenance), SR-185/TC-210 (requirement/interface counterpart semantics), and SR-186/TC-211 (proportional decomposition plus the actual hat-by-hat review record).

Dependency: WI-610 must first adjudicate the approved SR-161/LLR-183 amendment coherently. TC-211 now directly verifies SR-161 and SR-186, so this first approval must read the post-adjudication SR-161 chain, TC-178's supplementary mechanical linkage, and the fresh TC-211 Inspection result. An old INCOMPLETE result is historical evidence, not a pass for the revised procedure.

Approval is limited to SR-184, SR-185, SR-186, TC-209, TC-210 and TC-211. Do not request approval of any other Drafted or drifted row. Record the exact decision in this spec; after independent review, the primary publisher may apply its Status/snapshot effects only when the live whole-registry absorption ledger has no unjudged changed cell. The 18 older SR rationale changes and older LLR drift remain outside this batch. WI-601, WI-603 and WI-605 are restructured into WI-610 under OI-88; preserve their original scope and evidence in the archive. The existing pause remains; queueing and adjudication do not authorize a claim.
