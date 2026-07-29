+++
id = "WI-355"
title = "`--gate` is silently ignored by `--run-step`/`--run-steps`, so the documented per-WI bar is weaker than it reads and `--list` advertises a command that is not the one run. check.py resolves the plan at gate \"all\" for both flags (check.py:1274 and :1293) no matter what --gate says. Measured 2026-07-28: `check.py --gate G3 --list` prints `check_trajectory.py --strict` while `check.py --gate G3 --run-steps trajectory` executes `check_trajectory.py` with no --strict. `trajectory` is the ONLY step that differs, because it alone keys on `gate in (\"G2\",\"G3\")` (check.py:469) while every other gate-conditional step includes \"all\" - but it is the step carrying the R-A..R-E, status.md forward-only and perceptual-stale promotions, so the whole coherence tier silently degrades to warn. This BIT the WI-354 session: the handoff's 18-step block reported 18/18 PASS while two real G3 errors were live (a done WI id in status.md, and the new CMP-001->CMP-003 import with no declared IF seam); both surfaced only on a direct --strict run. NOT a one-line fix: resolving at \"all\" is DELIBERATE for the shipped pre-commit hook (check.py:461-467), and the hook passes no --gate - but --gate DEFAULTS to the repo's active gate, so naively honouring `gate` would arm --strict in the commit floor, which that comment forbids. The fix needs an explicit-vs-default sentinel (argparse default=None) so an explicitly passed --gate is honoured while the hook's defaulted call stays warn-first, and must pin BOTH halves as tests: the hook's floor stays warn-first, and `--gate G3 --run-steps trajectory` really does gate. Also decide what `--list` should print, since today it renders a plan --run-steps will not execute."
workstream = "scripts"
specref = "docs/log.md#session-2026-07-28-cont--wi-354-the-same-reference-enforced-in-one-home-and-unread-in-the-other"
buildtier = "medium"
priority = 1
safety_class = "ordinary"
order = 352
+++
