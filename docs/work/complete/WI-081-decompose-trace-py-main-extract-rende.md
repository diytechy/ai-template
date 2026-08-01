+++
id = "WI-081"
title = "Decompose trace.py main() (extract render_report)"
workstream = "scripts"
needs = ["WI-006", "~WI-080"]
buildtier = "medium"
order = 80
+++

## Deliverable

WI-081 (2026-07-16, four slices A-D, behavior-preserving): trace.py main() decomposed from ~790 lines to 114 orchestration-only lines, under a byte-identical golden-master net. A: tests/test_trace_golden.py + tests/golden/{clean,offspine,orphan}.txt pin report.md + normalized stdout + exit code byte-for-byte over three fixtures (clean, off-spine-rich, orphaned). B: load_registries(docs)->Registries + analyze(reg,args)->Findings extracted via the unpack/verbatim/bind pattern (recorded: analyze threads reg.docs). C: render_report(reg,findings,args,forest)->str + render_console + exit_code extracted; main() now argparse->load_registries->(--ratify)->analyze->build_forest->write->console->exit. Fold-in M8: _bucket_by_ref indexes the SR->LLR->TC joins once (matrix loop + build_forest), O(SR*LLR+SR*TC+LLR*TC)->O(N), output byte-identical. D: module docstring 229->72 lines (contract+usage+pointers to process.md/derived-gate; no rule restatement). Golden net green throughout with zero existing-test edits; new unit tests for _bucket_by_ref + exit_code. Phase-close check.py --gate G3 PASS (932 passed, 91.11% coverage, trace.py 97%). Recorded costs: main() 114 lines (target met); docstring 72 vs <=60; the three bag-unpack headers add minor intra-file dup (covered by the trace.py self-dup census line). Commits 6ead1ae/c7620e5/ff24fe6/1529ef9 + census refresh.
