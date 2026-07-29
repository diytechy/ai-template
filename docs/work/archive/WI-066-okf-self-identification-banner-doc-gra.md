+++
id = "WI-066"
title = "OKF self-identification banner + doc-graph exclusion"
workstream = "scripts"
sr_refs = ["SR-042"]
needs = ["WI-034"]
order = 69
+++

## Deliverable

2026-07-11 OKF audit (owner-ruled): gen_okf.py now emits a one-line source-slotted GENERATED banner on every file (blockquote after the frontmatter, first in UPSTREAM.md) naming the file a reference copy, its source registry/doc and the regen command; the root index + UPSTREAM absorb their old routing sentences so it is stated once. check_docs.py drops docs/okf/ from doc discovery (doc count + link graph + orphan scan) via the gen_arch_map/gen_trajectory/check_doc_refs 'never lint generated output' idiom (OKF_DIR = gen_okf's OUT_DIR); links INTO the bundle still resolve. Meta orphan warns 219->1 (the pre-existing docs/test/report.md, out of scope). Regenerated the 218-file bundle + arch-map (new banner() row) + PROJECT_STATE.html. No SR/LLR/TC text change: the banner is presentation within SR-042's 'typed markdown concept per row' and the exclusion is scan-scope within SR-012. Tests in test_gen_okf.py + test_check_docs.py.
