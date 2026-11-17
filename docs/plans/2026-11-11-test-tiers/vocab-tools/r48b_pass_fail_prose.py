"""HANDOFF 4.5.6 (ruled 2026-11-16, 10.7 item 1's leftover): a run of checks
passes or fails; "red" and "green" are not used for either, except once,
where PROCESS.md names the red, green, refactor cycle. This file is the
phrase map for prose, comments, docstrings, messages and registry rows; the
test names moved in a57a85553 (D4). What the map cannot read safely is edited
by line afterwards (h48b*.py).

The words map by part of speech, so number holds without a mark:
  verb      "reds X" -> "fails X", "would red" -> "would fail",
            "goes red" -> "fails", "is green" -> "passes", "are green" -> "pass",
            "stays green" -> "still passes", "keep it green" -> "keep it passing"
  adjective "a red tier" -> "a failing tier", "green commit checks" -> "passing commit checks"
  noun      "a red" -> "a failure", "a green" -> "a pass", "greens" -> "passes",
            "a false green" -> "a false pass"

Python names are not prose: `red`, `green`, `reds` as locals and parameters,
`STUB_CHECK_GREEN` and the like keep their spelling (4.5.6 covers prose,
comments and messages). The rules are phrases, never a bare word, and the
generic verb rules look ahead for a prose word, so a code line is not reached;
the dry run is read to make sure.

Left alone (SKIP or PROTECT): colours (rendering/, the dashboard and its
tests, a done-green fill, a red glyph), the retired spellings and the readers
of them (`red-tc`, `Bar-Green`, `# bar-red:`, the red mark, the red-round
maximum), the idiom "red flags", fixture data (`check-red`, "harness green"
titles, the quick red fox), the review-flip name `reroll-until-green` (a
review's verdict, not a run of checks), records and the size ratchets'
histories.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT as _PROTECT, RECORDS  # noqa: E402

SKIP = RECORDS + HAND_ONLY + [
    # colours: the dashboard, its emitters and its tests
    "project-trajectory/scripts/rendering/*",
    "tests/test_traj_*",
    "tests/test_gen_trajectory*",
    "tests/traj_fixtures.py",
    "tests/traj_core_fixtures.py",
    "tests/golden/dashboard-*",
    "scripts/dashboard-shots/*",
    # histories of the size ratchets: each comment records a bump of its day
    "tests/test_module_size_ratchet.py",
    "tests/test_complexity_ratchet.py",
    "docs/complexity-baseline",
    # the readers of retired spellings and their tests
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
    # fixture data: a review file, golden reports
    "tests/fixtures/*",
    # a spec of record
    "docs/specs/WI-910.md",
    # generated from the skills' descriptions; regenerated after
    "project-trajectory/skills/INDEX.csv",
]

_ADJ_NOUNS = (
    r"tier|tiers|run|runs|test|tests|check|checks|build|builds|refresh|refreshes|"
    r"close|closes|result|results|suite|gate|gates|cell|harness|commit|commits|queue|"
    r"merge|lane|step|steps|code|round|rounds|trunk|CI|matrix|generator|verdict|"
    r"setup|exit|handback|drain|landing|claim|condition|checkpoint|baseline|half|"
    r"tip|rework|commit checks|commit-check|stub harness|check harness|smoke run|"
    r"developer setup|scaffold|named test|tests\+coverage|non-merged lane|ratchets|"
    r"candidate|path|output"
)

_FAIL_VERB = {"goes": "fails", "go": "fail", "going": "failing", "went": "failed", "gone": "failed"}
_PASS_VERB = {"goes": "passes", "go": "pass", "going": "passing", "went": "passed", "gone": "passed"}
_IS_FAIL = {"is": "fails", "are": "fail", "was": "failed", "were": "failed", "be": "fail", "been": "failed"}
_IS_PASS = {"is": "passes", "are": "pass", "was": "passed", "were": "passed", "be": "pass", "been": "passed"}
_NOT = {"is": "does not", "are": "do not", "was": "did not", "were": "did not", "be": "not", "been": "not"}
_RUN_PASS = {"runs": "passes", "run": "pass", "ran": "passed", "running": "passing"}
_STAY_PASS = {
    "stays": "keeps passing", "stay": "keep passing", "stayed": "kept passing",
    "remains": "keeps passing", "remain": "keep passing",
}
_STAY_FAIL = {"stays": "keeps failing", "stay": "keep failing", "stayed": "kept failing"}
_START_PASS = {"starts": "passes from the start", "start": "pass from the start"}
_TURN = {"turn": "make", "turns": "makes", "turned": "made", "turning": "making"}


def _is(m, table):
    verb, adv = m.group(1), m.group(2)
    if adv == "not ":
        if verb == "been":
            return "not " + table[verb]
        return "{} {}".format(_NOT[verb], table["be"])
    return adv + table[verb]


def _adj(word):
    out = "failing" if word.lower() == "red" else "passing"
    if word.isupper():
        return out.upper()
    if word[0].isupper():
        return out.capitalize()
    return out


REGEX = [
    # --- compounds and fixed phrases first
    (r"\b([Ff])alse-green\b", r"\1alse-pass"),
    (r"\b([Ff])alse green\b", r"\1alse pass"),
    (r"\bFALSE GREEN\b", "FALSE PASS"),
    (r"\bfalse \"green\"", "false \"pass\""),
    (r"\b([Ff])alse-red\b", r"\1alse-failure"),
    (r"\b([Ff])alse red\b", r"\1alse failure"),
    (r"\bsilent-green\b", "silent-pass"),
    (r"\bsilent green\b", "silent pass"),
    (r"\bdishonest-green\b", "dishonest-pass"),
    (r"\bdishonest green\b", "dishonest pass"),
    (r"\b([Hh])onest green\b", r"\1onest pass"),
    (r"\b([Hh])onest red\b", r"\1onest failure"),
    (r"\bvacuous green\b", "vacuous pass"),
    (r"\bun-run greens\b", "un-run passes"),
    (r"\bindividually-green\b", "individually passing"),
    (r"\bcurrently-red\b", "currently failing"),
    (r"\balways-red\b", "always-failing"),
    (r"\bred-first\b", "failing-first"),
    (r"\bgreen-but-not-accepted\b", "passing-but-not-accepted"),
    (r"\b([Dd]riven) (red|RED)\b", lambda m: m.group(1) + (" to FAIL" if m.group(2) == "RED" else " to fail")),
    (r"\bDRIVEN RED\b", "DRIVEN TO FAIL"),
    # --- verbs of becoming: go, turn, stay, start, run, read
    (r"\b(goes|go|going|went|gone) red\b", lambda m: _FAIL_VERB[m.group(1)]),
    (r"\b(goes|go|going|went|gone) RED\b", lambda m: _FAIL_VERB[m.group(1)].upper()),
    (r"\b(goes|go|going|went|gone) green\b", lambda m: _PASS_VERB[m.group(1)]),
    (
        r"\b(turn|turns|turned|turning) (them|it|this|the suite|the gate|its tests) (red|green)\b",
        lambda m: "{} {} {}".format(_TURN[m.group(1)], m.group(2), "fail" if m.group(3) == "red" else "pass"),
    ),
    (r"\b(stays|stay|stayed|remains|remain) green\b", lambda m: _STAY_PASS[m.group(1)]),
    (r"\b(stays|stay|stayed) red\b", lambda m: _STAY_FAIL[m.group(1)]),
    (r"\b(starts|start) green\b", lambda m: _START_PASS[m.group(1)]),
    (r"\bun-run green\b", "un-run pass"),
    (r"(?<!-)\b(runs|run|ran|running) green\b", lambda m: _RUN_PASS[m.group(1)]),
    (r"\breads green\b", "passes"),
    (r"\breading green\b", "passing"),
    (r"\b(reports|reported|report|printed|prints) green\b", r"\1 a pass"),
    # keep or leave something green: it keeps passing
    (r"\b(keep|keeps|kept|keeping|left|leave|leaves|leaving) ((?:[\w'-]+ ){1,3}?)green\b", r"\1 \2passing"),
    (r"\b(with (?:its|every|all|the) (?:[\w-]+ )?(?:tests?|checks?)) green\b", r"\1 passing"),
    (r"\b([Gg])reen first\b", lambda m: ("P" if m.group(1) == "G" else "p") + "assing first"),
    # --- adjective before a noun ("was RED commit checks" is an adjective)
    (
        r"\b(red|green|RED|GREEN|Red|Green) (" + _ADJ_NOUNS + r")\b",
        lambda m: "{} {}".format(_adj(m.group(1)), m.group(2)),
    ),
    # is green / is red
    (r"\b(is|are|was|were|be|been) (not |still |never |now |already |genuinely |)green\b", lambda m: _is(m, _IS_PASS)),
    (r"\b(is|are|was|were|be|been) (not |still |never |now |already |)red\b", lambda m: _is(m, _IS_FAIL)),
    (r"\b(is|are|was) (RED|GREEN)\b", lambda m: (_IS_FAIL if m.group(2) == "RED" else _IS_PASS)[m.group(1)].upper()),
    # --- nouns
    (r"\b(consecutive|designed|deep|those|[Tt]wo|three|distinct|WI-275|batch-shim) reds\b", r"\1 failures"),
    (r"\bskips-and-reds\b", "skips-and-failures"),
    (
        r"\b([Aa]|[Tt]he|[Ii]ts|[Oo]ne|[Tt]hat|[Tt]his|[Ee]ach|[Nn]o|[Aa]nother|second|real|same|newest|first) "
        r"(red|green)\b(?![-_(.=\[]| one\b)",
        lambda m: "{} {}".format(m.group(1), "failure" if m.group(2) == "red" else "pass"),
    ),
    (r"\bgreens\b(?![-_(=\[])", "passes"),
    # --- verbs: to red is to make fail
    (r"\b(would|will|can|could|must|should|to|never|not|may|might|cannot|does|did|n't) red\b(?= [\w`*(\"'])", r"\1 fail"),
    (r"\bto green (a|the) ([\w-]+)\b", r"to make \1 \2 pass"),
    (r"\breddens\b", "fails"),
    (r"\breddened\b", "failed"),
    (r"\bREDS\b(?= )", "FAILS"),
    (r"\breds(?=[ ]+[\w`*(\"'-])", "fails"),
    (r"\breds(?=[.,;:]?\s*$)", "fails"),
    (r"\breds(?=[;:])(?!\):)", "fails"),
    (r"\breds(?=, (?!last\b))", "fails"),
]

PROTECT = list(_PROTECT) + [
    # the cycle PROCESS.md names, and the other mentions edited by hand
    r"red → green(?: → refactor)?",
    r"red->green",
    r"red/green|green/red",
    r"red-then-green",
    # colours
    r"done-green|done's green",
    r"\bone-red\b",
    r"quick red fox|<ins>red</ins>",
    r"\b[Rr]ed flags?\b|red-flagged",
    # retired spellings and their readers
    r"red-tc|red-TC|Bar-Green|bar-red|bar-summary|red[-_ ]mark|red-round|red record|red_rounds\w*|red TC",
    r"\bRED_\w+|\w+_RED\b|\w+_GREEN\w*|_red_\w+|_green\b|_reader_green",
    # the review-flip name: a review's verdict, not a run of checks
    r"reroll-until-green",
    # fixture data
    r"check-red",
    r",harness green",
    # Python shapes that hold the names as code
    r"\b(?:red|green|reds)\s*(?:=(?!=)|\.(?=[a-z_])|\[)",
    r"\bif (?:not )?(?:red|green|reds)\b(?=:| is| ==| else)",
    r"\bin reds\b",
    r"\((?:red|green|reds)(?= and|\)|,)",
    r"parametrize\(\"(?:red|green|reds)\"",
]
