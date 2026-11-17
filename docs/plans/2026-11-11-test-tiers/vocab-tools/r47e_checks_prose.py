"""HANDOFF 10.7 item 1, 9.10's leftover: "bar" where it names a run of checks,
in the comments, docstrings and messages of the scripts and tests. Run after
r47e_checks_names.py and n47e_names.py.

Only `project-trajectory/scripts/`, `scripts/` and `tests/` are in scope here:
there the word means a run of checks almost everywhere, so a phrase map, a
generic rule and a verb-agreement pass are safe enough to read line by line.
Shipped prose and repository docs mix the senses (a threshold, a stage, the
retired axis) and are edited by hand (`h47g*.py`), as are the modules listed
in `_HAND` below, whose bar prose mixes the senses too.

Agreement. "Checks" is plural where "bar" was singular, so every "checks" a
rule writes carries an invisible mark (U+2063) until the agreement rule has
seen it: a "checks" that was already in the text (`record-checks writes`,
`the commit checks is`) keeps its verb. The last rule drops the mark.

Left alone: the retired bar axis and what is named for it (PROTECT and
`_HISTORY`), a visual bar, a placeholder (`foo`/`bar`), "bar" for "except".
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT as _PROTECT, RECORDS  # noqa: E402

ROOT = Path(r"C:/Projects/ai-template-wt-vocabulary")
_HISTORY = (
    # each module's bar prose is the retired bar axis, named as retired
    "project-trajectory/scripts/spine_rules.py",
    "project-trajectory/scripts/kitlib/ladder.py",
    "project-trajectory/scripts/kitlib/stage.py",
    "project-trajectory/scripts/traj_status.py",
    "project-trajectory/scripts/derive_stage.py",
    "project-trajectory/scripts/check_vocab.py",
    "project-trajectory/scripts/kitlib/config.py",
    "tests/test_stage_ladder.py",
    "tests/test_spine_rules.py",
    "tests/test_selection_at_or_above.py",
    "tests/test_traj_status.py",
    "tests/test_rule_sync_driven.py",
    "tests/test_kitlib_stage.py",
    "tests/test_kitlib_ladder.py",
    "tests/test_derive_stage.py",
    "tests/test_generated_freshness_census.py",
    "tests/test_stack_profile.py",
)
_HAND = (
    # mixed senses (stage, threshold, the retired axis, a visual bar, a
    # placeholder): edited by hand
    "project-trajectory/scripts/check.py",
    "project-trajectory/scripts/check_trajectory.py",
    "project-trajectory/scripts/coherence.py",
    "project-trajectory/scripts/agent_policy.py",
    "project-trajectory/scripts/gen_arch_map.py",
    "project-trajectory/scripts/trace_text.py",
    "project-trajectory/scripts/trajectory_arch.py",
    "scripts/dashboard-shots/README.md",
    "tests/test_traj_panels.py",
    "tests/test_traj_render.py",
    "tests/test_trace_rules.py",
    "tests/test_shipped_tier.py",
    "tests/test_rule_sync.py",
    "tests/test_check_harness.py",
    "tests/test_gen_arch_map.py",
    "tests/test_blackout_window.py",
    "tests/test_dependency_ledger.py",
    "tests/test_acceptance_level.py",
    "tests/test_old_kit_resync.py",
)


def _outside():
    """Globs for every tracked path outside the three trees in scope."""
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files"], capture_output=True, text=True, check=True
    ).stdout.splitlines()
    tops = sorted({rel.split("/", 1)[0] for rel in out} - {"project-trajectory", "scripts", "tests"})
    kit = sorted(
        {rel.split("/")[1] for rel in out if rel.startswith("project-trajectory/")} - {"scripts"}
    )
    globs = []
    for top in tops:
        globs += [top, top + "/*"]
    for name in kit:
        globs += ["project-trajectory/" + name, "project-trajectory/" + name + "/*"]
    return globs


SKIP = RECORDS + HAND_ONLY + _outside() + list(_HISTORY) + list(_HAND) + [
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
    "tests/test_module_size_ratchet.py",
    "tests/test_complexity_ratchet.py",
    # the worker prompt's golden copy moves with the shipped template, by hand
    "tests/golden/*",
]

M = "\u2063"
C = "checks" + M

_VERBS = {
    "is": "are", "was": "were", "has": "have", "does": "do", "goes": "go",
    "runs": "run", "passes": "pass", "fails": "fail", "reads": "read",
    "needs": "need", "sees": "see", "writes": "write", "leaves": "leave",
    "edits": "edit", "stages": "stage", "catches": "catch", "applies": "apply",
    "vouches": "vouch", "stands": "stand", "refuses": "refuse", "carries": "carry",
    "says": "say", "takes": "take", "judges": "judge", "skips": "skip",
    "rises": "rise", "exists": "exist", "moves": "move", "bites": "bite",
    "holds": "hold", "names": "name", "counts": "count", "asks": "ask",
    "sits": "sit", "gets": "get", "keeps": "keep", "lands": "land",
    "measures": "measure", "wants": "want", "costs": "cost", "reports": "report",
    "creates": "create", "rebuilds": "rebuild", "speaks": "speak", "touches": "touch",
    "spends": "spend", "returns": "return", "selects": "select", "owns": "own",
    "reds": "fail", "flags": "flag", "lives": "live", "decides": "decide",
    "itself": "themselves",
}
_VERB_RE = "|".join(sorted(_VERBS, key=len, reverse=True))

REGEX = [
    # --- a threshold, not a run of checks (4.5.7)
    (r"\b(complexity|C901|cognitive) bar\b", r"\1 limit"),
    (r"\b(coverage|back-link coverage|backlink coverage|backlink) bar\b", r"\1 minimum"),
    (r"\b(quality|shipped|code-quality|shared) bar\b", r"\1 standard"),
    (r"\bstdlib bar\b", "stdlib rule"),
    (r"\bcleared the bar\b", "cleared the threshold"),
    (r"\bmargin below the bar\b", "margin below the threshold"),
    (r"\bthe strictest bar\b", "the strictest minimum"),
    (r"\b([Tt])he harness is (still )?the bar\b", r"\1he harness is \2the standard"),
    (r"\b([Aa]) bar nobody\b", r"\1 standard nobody"),
    (r"\bthe rubric is the bar\b", "the rubric is the standard"),
    (r"\bThe bar is deliberately high\b", "The threshold is deliberately high"),
    (r"\barm a bar\b", "arm a minimum"),
    (r"\bmeasurement into a bar\b", "measurement into a standard"),
    (r"\ba standing bar\b", "a standing rule"),
    (r"\bA test whose bar\b", "A test whose standard"),
    # --- a stage, not a run of checks (4.5.5)
    (r"\bAT EVERY BAR\b", "AT EVERY STAGE"),
    (r"\b(at|At) (every|any|each) bar\b", r"\1 \2 stage"),
    (r"\bbelow the top bar\b", "below the top stage"),
    (r"\bderived bar\b", "derived stage"),
    # --- verbs: to bar is to run the checks over something
    (r"\b(would|to) bar\b", r"\1 check"),
    (r"\band bar THERE\b", "and check THERE"),
    # --- a passing or failing run, before the noun moves
    (r"\b[Aa] red (review |refresh |landing |commit )?bar\b", "failing " + C),
    (r"\b[Aa] green (review |refresh |landing |commit )?bar\b", "passing " + C),
    (r"\bred (review |refresh |landing |commit )?bars?\b", "failing " + C),
    (r"\bgreen (review |refresh |landing |commit )?bars?\b", "passing " + C),
    (r"\b(the|its) bar is RED\b", r"\1 " + C + " FAIL"),
    (r"\bbar is RED\b", C + " FAIL"),
    (r"\b(the|its) bar (is|goes) red\b", r"\1 " + C + " fail"),
    (r"\b(the|its) bar went red\b", r"\1 " + C + " failed"),
    (r"\b(the|its) bar (is|goes) green\b", r"\1 " + C + " pass"),
    (r"\bthe bar passed\b", "the " + C + " passed"),
    # --- named runs: the glossary's words for each
    (r"\b(review|commit) bars?\b", "commit " + C),
    (r"\b(Review|Commit) bars?\b", "Commit " + C),
    (r"\b(landing|refresh|merge|composed-tree) bars?\b", "landing " + C),
    (r"\b(gate|rung) bars?\b", "gate " + C),
    (r"\bcheck bars\b", C),
    (r"\bsmoke bar\b", "smoke tier"),
    (r"\bbar tier\b", "check tier"),
    (r"\b([Aa]) bar runner\b", r"\1 check runner"),
    # --- a bar as a countable run
    (r"\b([Aa]) bar run\b", r"\1 check run"),
    (r"\b([Aa]) bar\b", r"\1 check run"),
    (r"\bbar run\b", "check run"),
    # --- generic
    (r"\bbar's\b", "checks'"),
    (r"\bbars\b", C),
    (r"\bbar\b", C),
    (r"\bBars\b", "Checks" + M),
    (r"\bBar\b", "Checks" + M),
    (r"\bBARS\b", "CHECKS" + M),
    (r"\bBAR\b", "CHECKS" + M),
    (r"\bbarred\b", "checked"),
    # --- agreement: only where a rule above wrote the plural
    (
        r"\b(checks|CHECKS|Checks)" + M + r" (" + _VERB_RE + r")\b",
        lambda m: "{} {}".format(m.group(1), _VERBS[m.group(2)]),
    ),
    (
        r"\bchecks" + M + r" (\w+ly) (runs|passes|fails|reads|names)\b",
        lambda m: "checks {} {}".format(m.group(1), _VERBS[m.group(2)]),
    ),
    (M, ""),
]

PROTECT = list(_PROTECT) + [
    r"(?i:\bbar[- ]axis\b)",
    r"(?i:three-value bar\b)",
    r"(?i:\bbar ordinals?\b)",
    r"(?i:\bbar-era\b)",
    r"(?i:\bbar-only\b)",
    r"(?i:vacuous-lowest-bar)",
    r"bar_failures: 0",
    r"\[bars\]",
    r"\"bars\"",
    r"(?i:retired[- ]bars?\b)",
    r"\bDevBar\S*",
    r"Foo\.bar",
    r"`Bar\.",
    r"\bfoo\b.{0,3}\bbar\b",
    r"_LEGACY_BAR_THRESHOLD|_RETIRED_BARS|_RETIRED_WI_BARS",
    r"bar=review",
    r"Bar-Green",
    r"\bbar-(summary|red)\b",
    r"\bprogress bar\b",
    r"\btab bar\b",
    r"\(bar the\b",
    r"three-bar\b",
    r"\u2298 barred",
    r"that bar closed the Impl rung",
    r"docs/gate BAR\b",
    r"(?i:\bbar spans?\b)",
    r"\bbar = \"=\" \* 70",
    r"^\s+bar,\s*$",
    r"parametrize\(\"bar\"",
    r"\(bar == \"red\"\)|bar == \"(red|green)\"",
]
