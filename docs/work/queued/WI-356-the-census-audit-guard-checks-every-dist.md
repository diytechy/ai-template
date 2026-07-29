+++
id = "WI-356"
title = "The census audit guard checks every distribution ROW against its section but never the declared TOTAL, so docs/dupes-allow's header can drift silently. Measured 2026-07-28 during WI-347: the header read 'The distribution (207 blocks)' while the sections held 201 fingerprint lines, and all 13 audit tests passed - because the guard compares each row's count to its own section header, every header did match its own lines, and nothing compares the sum to reality. The 'By disposition' summary line was stale the same way, reading 'extract 35' while the rows summed to 29. One block of the 6-block gap is explained (WI-341 merged two adjacent spine-loader runs); the rest was never tracked down, which is exactly the cost of an unchecked aggregate. Fix: assert the declared total equals the summed section counts AND the emitted census size, and assert the by-disposition line against the sections - or generate the whole header block from the sections, which is the rule this repo already applies to derived numbers. Guard it by mutating the header total and confirming red; a guard that cannot fail is the defect being fixed here."
workstream = "scripts"
specref = "docs/dupes-allow"
buildtier = "quick"
priority = 2
safety_class = "ordinary"
order = 353
+++
