"""HANDOFF 10.7 item 1, 9.11's leftover: "bar" in this repository's own docs,
by line (hline.py), each read and given the word its sense needs, as
3cf264ccd did: a run of checks takes the glossary's terms (commit checks,
landing checks, gate checks), a stage is a stage (4.5.5), a threshold is a
minimum, standard, limit or threshold (4.5.7).

Kept: the retired bar axis named as retired (registry-machinery-reference.md
14-15, declared-absences 93), the placeholder `Foo.bar` (enforcement-audit.md
53, registry-machinery-reference.md 930). Not touched: docs/concurrency-v2.md,
a closed and ruled plan (its header says so), which common.RECORDS lists and
which every earlier concept left in its own words ("owner", "re-attest").
"""

EA = "docs/enforcement-audit.md"
RMR = "docs/registry-machinery-reference.md"
KN = "docs/knowledge/"

LINES = [
    # a threshold (4.5.7)
    (EA, 10, "The bar is honesty:", "The standard is honesty:"),
    (EA, 94, "the RULING-3 bar", "the RULING-3 standard"),
    # the backlink-coverage dial at 50: a minimum the gate holds
    (EA, 132, "here is a bar, not a report.", "here is a minimum, not a report."),
    (EA, 144, "audit's bar.", "audit's standard."),
    # runs of checks: the glossary's terms
    (
        EA,
        24,
        "at pre-commit, every bar, CI and the merge slot's bar)",
        "at pre-commit, every stage's checks, CI and the merge slot's landing checks)",
    ),
    # check_resync runs in `[run] smoke`, the commit checks
    (EA, 36, "it runs in the bar, not the pre-commit hook", "it runs in the commit checks, not the pre-commit hook"),
    (EA, 36, "a lane commit made without the bar is caught", "a lane commit made without the commit checks is caught"),
    (EA, 36, "at the next build round's bar or at landing", "at the next build round's commit checks or at landing"),
    (EA, 36, "a trunk-direct commit made without the bar escapes", "a trunk-direct commit made without the commit checks escapes"),
    (EA, 38, "`check.py --gate` runs the bar;", "`check.py --gate` runs the gate checks;"),
    (RMR, 193, "(the DevStg-Impl bar)", "(a DevStg-Impl gate check)"),
    # the Release rung: a stage (4.5.5)
    (RMR, 482, "the release bar is the harness's answer", "the release stage is the harness's answer"),
    (RMR, 571, "never gets a silently weaker bar.", "never gets silently weaker checks."),
    (RMR, 583, "not a relaxed bar", "not a relaxed standard"),
    (
        RMR,
        647,
        "**The entire product bar — format, lint and the test suite — is DevStg-Impl-only.**",
        "**All the product checks — format, lint and the test suite — are DevStg-Impl-only.**",
    ),
    (RMR, 674, "the bars run it in warn mode", "the checks run it in warn mode"),
    (RMR, 677, "inside the tier on every bar.", "inside the tier on every check run."),
    (RMR, 725, "unclaimed, the full bar", "unclaimed, the full checks"),
    (RMR, 726, "applies. `--trunk-lane`", "apply. `--trunk-lane`"),
    (RMR, 730, "runs a genuinely weaker bar than", "runs genuinely weaker checks than"),
    (RMR, 975, "### 12.3 The entire product bar is DevStg-Impl-only", "### 12.3 All the product checks are DevStg-Impl-only"),
    (RMR, 1043, "# the DevStg-Tests bar", "# the DevStg-Tests gate checks"),
    (RMR, 1046, "# the DevStg-Impl bar", "# the DevStg-Impl gate checks"),
    (
        "docs/declared-absences",
        111,
        "written when the bar's check.py passes --html",
        "written when check.py passes --html",
    ),
    ("docs/declared-absences", 111, "absence until a bar run writes it", "absence until a check run writes it"),
    # the shipped tier's admission threshold
    ("docs/dependencies.md", 18, "so the bar is highest", "so the threshold is highest"),
    (KN + "crash-atomicity-recovery.md", 16, "to hold as the bar:", "to hold as the standard:"),
    (KN + "cross-platform-scripting.md", 21, "the stdlib bar is strictest", "the stdlib rule is strictest"),
    (KN + "rendered-surface-review.md", 13, "The bar for all three", "The standard for all three"),
    (KN + "rendered-surface-review.md", 51, "a stated bar?", "a stated standard?"),
    (KN + "rendered-surface-review.md", 53, "SR-052 is that bar made explicit", "SR-052 is that standard made explicit"),
    # automated link recovery: a suggester, never a check that gates
    (KN + "traceability-enforcement.md", 203, "as a bar.", "as a check."),
    # the log template: the stable ids an entry cites
    ("project-trajectory/LOG.template.md", 9, "(OI-n, stage/bar names, dates)", "(OI-n, stage names, dates)"),
]
