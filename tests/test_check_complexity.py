"""Verifies SR-183 / LLR-206 (TC-202) — the stdlib cognitive-complexity census.

Two layers. In-process unit cases over the counting function pin the metric: the
two correctness traps the pack named (`elif` flattening — Python parses `elif` as
a nested `If`, so a naive walker double-counts and over-nests every ladder — and
operator RUNS, where `a and b or c` is +2 while `a and b and c` is +1), the
nested-def/decorator battery, and an ORACLE battery transliterated from the Sonar
white paper's own worked examples (the only external check on a metric with no
reference test suite). The CLI drives — every mode as a subprocess — live in the
sibling test_check_complexity_cli.py, re-tiered SLOW because each pays interpreter
startup; the metric itself is pinned here, in-process and cheap.
"""

import ast

import pytest

from conftest import load_script

cc = load_script("check_complexity")


def score(src, name=None):
    """Cognitive complexity of the named (or only) top-level function in `src`."""
    tree = ast.parse(src)
    found = []
    cc._collect(tree, "", found)
    picked = [f for n, f in found if name is None or n == name]
    assert picked, "no function {!r} in the snippet".format(name)
    return cc.cognitive(picked[0])


# --- trap 1: elif is flat, else is +1 with no nesting increment ---------------


def test_elif_ladder_is_flat():
    src = """
def f(a):
    if a == 1:
        pass
    elif a == 2:
        pass
    elif a == 3:
        pass
    else:
        pass
"""
    assert score(src) == 4


def test_written_out_else_if_is_nested_not_flattened():
    """The naive-walker trap in reverse: an `else:` block that HAPPENS to hold a
    single `if` is genuinely nested and must cost more than the `elif` ladder
    above. The discriminator is the column, not the shape of the AST."""
    src = """
def f(a, b):
    if a:
        pass
    else:
        if b:
            pass
        else:
            pass
"""
    assert score(src) == 5


def test_else_is_plus_one_without_nesting():
    assert score("def f(a):\n    if a:\n        pass\n    else:\n        pass\n") == 2


def test_elif_body_still_nests_its_children():
    src = """
def f(a, b):
    if a:
        pass
    elif b:
        for x in b:
            pass
"""
    assert score(src) == 4  # if +1, elif +1, for +1+1


# --- trap 2: runs of like operators ------------------------------------------


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("a and b", 1),
        ("a and b and c", 1),
        ("a or b or c or d", 1),
        ("a and b or c", 2),
        ("a and b and c or d or e and f", 3),
        ("a and not (b and c)", 2),
        ("a", 0),
        ("not a", 0),
    ],
)
def test_boolean_operator_runs(expr, expected):
    assert score("def f(a, b, c, d, e, f):\n    return {}\n".format(expr)) == expected


def test_boolean_run_inside_a_condition_adds_to_the_if():
    src = "def f(a, b, c):\n    if a and b and c:\n        pass\n"
    assert score(src) == 2


# --- nesting increments -------------------------------------------------------


def test_nesting_increments_spec_my_method():
    """Spec p.9, `myMethod` — total 9."""
    src = """
def my_method(condition1, condition2):
    try:
        if condition1:
            for i in range(10):
                while condition2:
                    pass
    except (ValueError, TypeError):
        if condition2:
            pass
"""
    assert score(src) == 9


def test_try_and_finally_are_ignored():
    src = """
def f(a):
    try:
        pass
    finally:
        pass
    with open(a) as handle:
        pass
    assert a
    return a
"""
    assert score(src) == 0


def test_each_except_is_one_increment_however_many_types():
    src = """
def f():
    try:
        pass
    except (A, B, C, D):
        pass
    except E:
        pass
"""
    assert score(src) == 2


# --- nested defs and lambdas: nesting increment, no base increment ------------


def test_lambda_nests_without_incrementing():
    """Spec p.9, `myMethod2` — total 2."""
    src = "def my_method2(condition1, x, y):\n    r = lambda: x if condition1 else y\n    return r\n"
    assert score(src) == 2


def test_nested_def_is_charged_to_the_enclosing_function():
    """Spec Appendix A, `not_a_decorator` — total 2. The nested def takes the
    nesting increment and no base increment, and does NOT get its own row."""
    src = """
def not_a_decorator(a, b, condition):
    my_var = a * b
    def inner(func):
        if condition:
            print(b)
        func()
    return inner
"""
    assert score(src) == 2
    tree = ast.parse(src)
    found = []
    cc._collect(tree, "", found)
    assert [n for n, _ in found] == ["not_a_decorator"]


def test_decorator_shape_is_exempt_from_the_nesting_increment():
    """Spec Appendix A, `a_decorator` — total 1."""
    src = """
def a_decorator(a, b, condition):
    def inner(func):
        if condition:
            print(b)
        func()
    return inner
"""
    assert score(src) == 1


def test_decorator_generator_is_exempt_all_the_way_down():
    """Spec Appendix A, `decorator_generator` — total 1."""
    src = """
def decorator_generator(a, b, condition):
    def generator(func):
        def decorator(func):
            if condition:
                print(b)
            return func()
        return decorator
    return generator
"""
    assert score(src) == 1


def test_decorator_exemption_needs_the_return_to_name_the_inner_def():
    """The narrow reading. `traj_parse._spine` has the decorator SHAPE — a
    nested def and a return — but returns a tuple of CALLS, so its inner def is
    real nesting and must be charged."""
    src = """
def _spine(root):
    def rows(rel):
        for r in load(rel):
            if r:
                yield r
    return (rows("a"), rows("b"))
"""
    assert score(src) == 5  # nesting 1 for the inner def: for +2, if +3


def test_method_rows_are_qualified_by_class():
    src = "class C:\n    def m(self):\n        pass\n"
    found = []
    cc._collect(ast.parse(src), "", found)
    assert [n for n, _ in found] == ["C.m"]


# --- recursion ----------------------------------------------------------------


def test_direct_recursion_adds_one():
    src = """
def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)
"""
    assert score(src) == 2


def test_method_recursion_through_self_adds_one():
    src = """
class C:
    def walk(self, node):
        for child in node:
            self.walk(child)
"""
    assert score(src, "C.walk") == 2


def test_delegation_to_a_same_named_function_elsewhere_is_not_recursion():
    """`RoutingState.cool` calling `agent_route.cool` is a DELEGATION. Matching
    on the bare attribute name scores it as recursion, and that false positive
    is live in the kit (it also fires on `parse_args` calling
    `ap.parse_args()`)."""
    src = """
class C:
    def cool(self, route_id):
        agent_route.cool(self.cooldowns, route_id)
"""
    assert score(src, "C.cool") == 0


def test_loop_else_is_plus_one():
    src = "def f(xs):\n    for x in xs:\n        pass\n    else:\n        pass\n"
    assert score(src) == 2


# --- comprehensions, ternaries, match ----------------------------------------


def test_comprehension_condition_takes_a_nesting_increment():
    assert score("def f(xs):\n    return [x for x in xs if x]\n") == 2


def test_comprehension_inside_a_branch_nests_deeper():
    src = "def f(xs, flag):\n    if flag:\n        return [x for x in xs if x]\n    return []\n"
    assert score(src) == 4  # if +1, comprehension-if +1 + nesting 2


def test_comprehension_without_a_condition_is_free():
    assert score("def f(xs):\n    return [x for x in xs]\n") == 0


def test_ternary_is_one_increment_and_nests():
    assert score("def f(a, b):\n    return 1 if a else 2\n") == 1
    assert score("def f(a, b):\n    return 1 if a else (2 if b else 3)\n") == 3


def test_match_is_one_increment_for_the_whole_switch():
    """Spec, "Switches": a switch and ALL its cases combined is ONE structural
    increment — the point of the metric, and the opposite of cyclomatic."""
    src = """
def get_words(number):
    match number:
        case 1:
            return "one"
        case 2:
            return "a couple"
        case 3:
            return "a few"
        case _:
            return "lots"
"""
    assert score(src) == 1


def test_match_case_guard_adds_one():
    src = """
def f(x, y):
    match x:
        case 1 if y:
            return 1
        case _:
            return 0
"""
    assert score(src) == 2


def test_match_case_body_nests():
    src = """
def f(x, y):
    match x:
        case 1:
            if y:
                return 1
    return 0
"""
    assert score(src) == 3  # match +1, if +1 + nesting 1


# --- oracle: transliterated Sonar white-paper examples ------------------------


ORACLE_OVERRIDDEN = """
def overridden_symbol_from(self, class_type):
    if class_type.is_unknown():
        return UNKNOWN
    unknown_found = False
    symbols = class_type.get_symbol().members().lookup(self.label)
    for override_symbol in symbols:
        if override_symbol.is_kind(MTH) and not override_symbol.is_static():
            method_symbol = override_symbol
            if self.can_override(method_symbol):
                overriding = self.check_overriding_parameters(method_symbol, class_type)
                if overriding is None:
                    if not unknown_found:
                        unknown_found = True
                elif overriding:
                    return method_symbol
    if unknown_found:
        return UNKNOWN
    return None
"""

ORACLE_TO_REGEXP = """
def to_regexp(ant_pattern, directory_separator):
    escaped = "!" + directory_separator
    out = ["^"]
    i = 1 if ant_pattern.startswith("/") or ant_pattern.startswith("@") else 0
    while i < len(ant_pattern):
        ch = ant_pattern[i]
        if ch in SPECIAL_CHARS:
            out.append("!" + ch)
        elif ch == "*":
            if i + 1 < len(ant_pattern) and ant_pattern[i + 1] == "*":
                if i + 2 < len(ant_pattern) and is_slash(ant_pattern[i + 2]):
                    out.append("(?:.*" + escaped + "|)")
                    i += 2
                else:
                    out.append(".*")
                    i += 1
            else:
                out.append("[^" + escaped + "]*?")
        elif ch == "?":
            out.append("[^" + escaped + "]")
        elif is_slash(ch):
            out.append(escaped)
        else:
            out.append(ch)
        i += 1
    out.append("$")
    return "".join(out)
"""

ORACLE_SUM_OF_PRIMES = """
def sum_of_primes(max_n):
    total = 0
    for i in range(1, max_n + 1):
        for j in range(2, i):
            if i % j == 0:
                continue
        total += i
    return total
"""


@pytest.mark.parametrize(
    "src, expected, source_note",
    [
        (ORACLE_OVERRIDDEN, 19, "Appendix C, JavaSymbol.overriddenSymbolFrom = 19"),
        (ORACLE_TO_REGEXP, 20, "Appendix C, WildcardPattern.toRegexp = 20"),
        # The paper scores 7; +1 of that is `continue OUT`, a JUMP TO LABEL.
        # Python has no labeled continue, so the Python-equivalent oracle is 6.
        (ORACLE_SUM_OF_PRIMES, 6, "p.10, sumOfPrimes = 7 minus the label jump"),
    ],
)
def test_white_paper_oracles(src, expected, source_note):
    assert score(src) == expected, source_note


# --- SLOC and public symbols --------------------------------------------------


def test_sloc_excludes_blanks_comments_and_docstrings():
    src = '''
def f(a):
    """Doc.

    More doc.
    """
    # a comment
    b = 1

    return b
'''
    tree = ast.parse(src)
    found = []
    cc._collect(tree, "", found)
    lines, docs = src.splitlines(), cc._doc_lines(tree)
    assert cc.sloc(found[0][1], lines, docs) == 3  # def, b = 1, return b


def test_public_symbol_count_ignores_underscored_names():
    src = "X = 1\n_y = 2\ndef pub():\n    pass\ndef _priv():\n    pass\nclass K:\n    pass\n"
    assert sorted(cc._public(ast.parse(src))) == ["K", "X", "pub"]


# --- census, baseline round-trip (in-process) ---------------------------------


SAMPLE = """
def tangled(a, b, c, d):
    for x in a:
        if b:
            while c:
                if d:
                    for y in d:
                        if y:
                            pass
    return a


def simple(a):
    return a
"""


@pytest.fixture()
def repo(tmp_path):
    target = tmp_path / "project-trajectory" / "scripts"
    target.mkdir(parents=True)
    (target / "mod.py").write_text(SAMPLE, encoding="utf-8")
    return tmp_path


def test_census_scores_and_sorts(repo):
    rows, modules = cc.census(repo, cc.DEFAULT_INCLUDE)
    assert [r[1] for r in rows] == ["simple", "tangled"]
    assert rows[0][2] == 0
    assert rows[1][2] > cc.DEFAULT_THRESHOLD
    assert modules[0][0] == "project-trajectory/scripts/mod.py"
    assert modules[0][1] == 2  # two public defs


def test_restamp_writes_lf_only_debt_headed_tsv(repo):
    assert cc.main(["--root", str(repo), "--restamp"]) == 0
    baseline = repo / cc.BASELINE
    raw = baseline.read_bytes()
    assert b"\r\n" not in raw, "baseline must be LF-only"
    text = raw.decode()
    assert "DEBT STATEMENT, NOT AN APPROVAL" in text, "header states its stance"
    assert cc.HEADER in text.splitlines(), "the column header is present"
    assert "project-trajectory/scripts/mod.py\ttangled\t" in text
    assert "\tsimple\t" not in text, "under-threshold rows are not baselined"


def test_baseline_round_trip_preserves_the_reason_column(repo):
    cc.main(["--root", str(repo), "--restamp"])
    baseline = repo / cc.BASELINE
    rows = baseline.read_text(encoding="utf-8").splitlines()
    rows[-1] = rows[-1] + "seeded debt, not an approval"
    baseline.write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    parsed = cc.read_baseline(baseline)
    assert parsed[("project-trajectory/scripts/mod.py", "tangled")][2].startswith(
        "seeded debt"
    )
    cc.main(["--root", str(repo), "--restamp"])
    assert "seeded debt" in baseline.read_text(encoding="utf-8"), (
        "re-stamp keeps the reason"
    )


def test_threshold_boundary_is_exclusive(repo):
    """The boundary is strictly OVER (`>`), not "reaches" (`>=`): a function
    scoring exactly the threshold is UNDER it and is not baselined. Pins the one
    reading shared by SR-183, LLR-206 and the baseline's over-threshold rows.
    `tangled` scores exactly 21."""
    key = ("project-trajectory/scripts/mod.py", "tangled")
    assert cc.main(["--root", str(repo), "--threshold", "21", "--restamp"]) == 0
    assert key not in cc.read_baseline(repo / cc.BASELINE), "at threshold: not over"
    assert cc.main(["--root", str(repo), "--threshold", "20", "--restamp"]) == 0
    assert key in cc.read_baseline(repo / cc.BASELINE), "one below threshold: over"


def test_collect_descends_through_every_control_flow_container():
    """A module-level `def` under `for`/`while`/`match` — not only `if`/`try`/
    `with` — is a real symbol and must be collected, without descending into a
    function body."""
    src = """
for _i in range(1):
    def under_for(a):
        def nested(b):
            return b
        return a
while False:
    def under_while(a):
        return a
"""
    found = []
    cc._collect(ast.parse(src), "", found)
    assert sorted(n for n, _ in found) == ["under_for", "under_while"]


def test_threshold_is_a_dial(repo):
    assert cc.main(["--root", str(repo), "--threshold", "1000", "--restamp"]) == 0
    baseline = repo / cc.BASELINE
    assert cc.read_baseline(baseline) == {}, "nothing over threshold 1000"
    assert cc.HEADER in baseline.read_text(encoding="utf-8").splitlines()


def test_warn_mode_reports_without_failing(repo, capsys):
    cc.main(["--root", str(repo), "--restamp"])
    path = repo / "project-trajectory" / "scripts" / "mod.py"
    path.write_text(
        SAMPLE.replace("    return a\n", "    if b:\n        return a\n"),
        encoding="utf-8",
    )
    assert cc.main(["--root", str(repo), "--mode", "warn"]) == 0
    assert "SIMPLIFY" in capsys.readouterr().err


def test_the_checker_passes_its_own_check():
    """The ratchet must not be a baseline entry in its own census."""
    from pathlib import Path

    own = Path(cc.__file__).resolve()
    rows, _ = cc.census(own.parent, (own.name,))
    worst = max(rows, key=lambda r: r[2])
    assert worst[2] < cc.DEFAULT_THRESHOLD, worst
