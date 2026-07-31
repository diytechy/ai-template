## 2026-07-31 — WI-377: the bar step count is honest

**One line:** `integrate.py` counted every `PASS` line in check.py's output,
but under `--jobs` each step's status prints twice (lane runner + final
summary), so a 20-step G3 bar was recorded as "bar PASS (40 steps)" in merge
records — the count is now by **distinct step name**, identical at
`--jobs 1` and `--jobs N`.

**Deliverables:** `_passed_steps(out)` — a pure helper returning the
distinct step names matching the `PASS` line shape (a malformed name-less
PASS line is skipped, FAIL/SKIP never count) — with `_run_bar` reporting
`len()` of it; one regression test in `tests/test_integrate.py` pinning
that the doubled `--jobs` output shape and the serial shape of the same
plan report the same count (and the malformed-line guard).

**Why it mattered:** the figure had already leaked into records as if it
were 40 units of work — the merge records for two earlier closes say "40
steps", and one spec title repeated it. This kit treats recorded evidence
as load-bearing; a doubled count is a false measurement in exactly the
surface that is supposed to be trustworthy. (Existing log entries stay as
written — history records what the tool printed at the time; this fixes
the tool.)

**Deviation from the filed remedy options:** the row offered "count only
the summary block (split on the `=` banner) or a machine-readable total
from check.py". Distinct-name counting was chosen instead: it needs no
check.py change (the smaller blast radius), and it is robust to BOTH output
shapes without depending on the banner's exact width — the banner-split
form would silently fall back to double-counting on any banner change. The
regression test pins the actual property the row asked for (same count,
both jobs modes).

**Bars:** targeted integrator tests green; smoke green except the standing
work-branch red; `check_docs` OK. No budgeted file touched.
