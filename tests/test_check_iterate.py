"""The iterate checks' selection: a change selects the tests it names, a shared
module is narrowed by the definitions it touches, and what cannot be focused
widens or is reported, never passed silently (scripts/check_iterate.py)."""

import ast

from conftest import CANARY, CANARY_MAX, ROOT, load_script, read_canary

STEP = load_script("check_iterate", ROOT / "scripts")
SRC = "project-trajectory/scripts/"


def _index(files):
    """A test index from `{file name: source}`, as `read_tests` builds it."""
    stems = frozenset(name[: -len(".py")] for name in files)
    return {
        "tests/" + name: STEP.read_test_file(text, stems)
        for name, text in files.items()
    }


def _select(tmp_path, paths, index, **kwargs):
    kwargs.setdefault("spine", lambda root, path: [])
    kwargs.setdefault("tagged", lambda root, tags: [])
    return STEP.select(tmp_path, paths, index, **kwargs)


def _touch(tmp_path, *names):
    for name in names:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("", encoding="utf-8")


def test_a_source_path_reads_as_its_importable_module():
    assert STEP.source_module(SRC + "trace.py") == ("trace", "trace")
    assert STEP.source_module(SRC + "kitlib/spine.py") == ("kitlib.spine", "spine")
    assert STEP.source_module(SRC + "kitlib/__init__.py") == ("kitlib", "kitlib")
    assert STEP.source_module("scripts/check_resync.py").leaf == "check_resync"
    assert STEP.source_module("docs/stack.ini") is None
    assert STEP.source_module("tests/test_trace.py") is None


def test_a_test_names_a_module_by_import_by_load_and_by_file_name():
    index = _index(
        {
            "test_a.py": "from kitlib import spine\n",
            "test_b.py": 'mod = load_script("spine", SCRIPTS / "kitlib")\n',
            "test_c.py": 'run_py([SCRIPTS / "kitlib" / "spine.py"], cwd)\n',
            "test_d.py": "import spine_rules\n",  # a different module
        }
    )
    module = STEP.source_module(SRC + "kitlib/spine.py")
    assert STEP.tests_naming(index, module) == [
        "tests/test_a.py",
        "tests/test_b.py",
        "tests/test_c.py",
    ]


def test_a_helper_carries_what_it_names_and_conftest_carries_nothing():
    index = _index(
        {
            "lane_fixtures.py": 'INTEGRATE = load_script("integrate")\n',
            "conftest.py": 'BOOT = "bootstrap.py"\n',
            "test_uses_helper.py": "from lane_fixtures import INTEGRATE\n",
            "test_plain.py": "from conftest import ROOT\n",
        }
    )
    integrate = STEP.source_module(SRC + "integrate.py")
    assert STEP.tests_naming(index, integrate) == ["tests/test_uses_helper.py"]
    assert STEP.tests_naming(index, STEP.source_module(SRC + "bootstrap.py")) == []


def test_a_changed_test_file_selects_itself_and_a_deleted_one_does_not(tmp_path):
    _touch(tmp_path, "tests/test_here.py")
    got = _select(tmp_path, ["tests/test_here.py", "tests/test_gone.py"], {})
    assert list(got.files) == ["tests/test_here.py"]
    assert got.behaviour and got.widen is None


def test_a_change_of_records_and_lint_held_state_runs_no_test(tmp_path):
    paths = [
        "docs/reviews/wi-1/round-1.md",
        "docs/handoff-2026-11-11.md",
        "docs/work/active/WI-1.md",
        "PROJECT_STATE.html",
    ]
    got = _select(tmp_path, paths, {})
    assert not got.behaviour and not got.files and not got.unmapped
    assert STEP.pytest_command(got, ["tests/test_x.py::test_y"], {}) == (None, 0)


def test_what_no_selection_can_be_honest_about_widens(tmp_path):
    assert _select(tmp_path, None, {}).widen  # the comparison was unavailable
    assert "pytest.ini" in _select(tmp_path, ["pytest.ini"], {}).widen
    wide = _select(tmp_path, ["pytest.ini"], {})
    command, functions = STEP.pytest_command(wide, ["tests/test_x.py::test_y"], {})
    assert command[-2:] == ["-m", "smoke or canary"] and functions is None


def test_an_unnamed_source_file_is_reported_unmapped_not_dropped(tmp_path):
    got = _select(tmp_path, [SRC + "brand_new.py"], _index({"test_a.py": "x = 1\n"}))
    assert got.unmapped == [SRC + "brand_new.py (no test names it)"]
    assert got.behaviour  # so the canary set still runs


def test_a_non_python_file_selects_the_tests_that_name_it(tmp_path):
    index = _index(
        {
            "test_hook.py": 'HOOK = KIT / "hooks" / "pre-commit"\n',
            "test_other.py": 'NAME = "pre-commit-config"\n',  # a longer name
        }
    )
    got = _select(tmp_path, ["project-trajectory/hooks/pre-commit"], index)
    assert list(got.files) == ["tests/test_hook.py"]


def test_a_broadly_named_file_keeps_only_the_readers_of_the_repos_own_copy(tmp_path):
    files = {
        "test_scaffold_{}.py".format(
            n
        ): '(scaffold / "docs" / "stack.ini").write_text("")\n'
        for n in range(STEP.BROAD_MENTION + 1)
    }
    files["test_live.py"] = 'STACK = ROOT / "docs" / "stack.ini"\n'
    got = _select(tmp_path, ["docs/stack.ini"], _index(files))
    assert list(got.files) == ["tests/test_live.py"]
    del files["test_live.py"]
    got = _select(tmp_path, ["docs/stack.ini"], _index(files))
    assert not got.files and "too broad to focus" in got.unmapped[0]


SOURCE = '''"""Module docstring."""

import os

LIMIT = 3


def judge(row):
    """Decide one row.

    Implements: SR-210, LLR-249
    """
    return row


class Reader:
    def load(self):
        """Implements: LLR-300"""
        return os.getcwd()


if os.name == "nt":
    LIMIT = 4
'''


def _line(needle):
    return SOURCE.splitlines().index(needle) + 1


def test_a_changed_line_names_its_definition_and_that_definitions_requirements():
    at = _line("    return row")
    got = STEP.touched(SOURCE, [(at, at)])
    assert got == (frozenset({"judge"}), frozenset({"SR-210", "LLR-249"}), False)
    at = _line("        return os.getcwd()")
    got = STEP.touched(SOURCE, [(at, at)])
    assert got.symbols == {"Reader", "load"} and got.tags == {"LLR-300"}
    assert STEP.touched(SOURCE, [(_line("LIMIT = 3"),) * 2]).symbols == {"LIMIT"}


def test_comments_imports_and_the_docstring_touch_nothing_and_loose_code_is_whole():
    quiet = [(1, 1), (_line("import os"),) * 2, (2, 2)]
    assert STEP.touched(SOURCE, quiet) == (frozenset(), frozenset(), False)
    at = _line("    LIMIT = 4")
    assert STEP.touched(SOURCE, [(at, at)]).whole
    assert STEP.touched("def broken(:\n", [(1, 1)]) is None


def test_hunk_ranges_read_the_new_side_and_a_pure_removal_touches_one_line():
    diff = "@@ -10,2 +12,3 @@ def f\n+a\n@@ -40 +44 @@\n+b\n@@ -50,4 +53,0 @@\n-c\n"
    assert STEP.hunk_ranges(diff) == [(12, 14), (44, 44), (53, 53)]


def _hub(extra):
    """An index in which agent_common's tests hold more than HUB_FUNCTIONS
    test functions, spread over four filler files, plus `extra`."""
    case = ["def test_case():", "    pass"] * (STEP.HUB_FUNCTIONS // 4 + 1)
    body = "\n".join(['load_script("agent_common")', *case, ""])
    files = {"test_filler_{}.py".format(n): body for n in range(4)}
    files.update(extra)
    return _index(files)


def test_a_shared_module_is_narrowed_to_its_own_tests_mentions_and_tagged_evidence(
    tmp_path,
):
    index = _hub(
        {
            "test_agent_common_harness.py": 'ac = load_script("agent_common")\n',
            "test_route.py": 'ac = load_script("agent_common")\nac.judge(1)\n',
            "test_tagged.py": "x = 1\n",
        }
    )
    path = SRC + "agent_common.py"
    change = STEP.Touched(frozenset({"judge"}), frozenset({"LLR-249"}), False)
    got = _select(
        tmp_path,
        [path],
        index,
        change_of=lambda p: change,
        tagged=lambda root, tags: ["tests/test_tagged.py"] if "LLR-249" in tags else [],
    )
    assert list(got.files) == [
        "tests/test_agent_common_harness.py",
        "tests/test_route.py",
        "tests/test_tagged.py",
    ]
    assert got.notes and "kept 3" in got.notes[0]


def test_a_shared_module_changed_outside_a_definition_keeps_every_test(tmp_path):
    index = _hub({"test_route.py": 'ac = load_script("agent_common")\n'})
    path = SRC + "agent_common.py"
    for change in (None, STEP.Touched(frozenset(), frozenset(), True)):
        got = _select(tmp_path, [path], index, change_of=lambda p, c=change: c)
        assert len(got.files) == 5 and not got.notes


def test_a_conftest_helper_selects_its_users_and_a_conftest_hook_widens(tmp_path):
    index = _index(
        {
            "test_tier.py": "from conftest import SLOW_MODULES\n",
            "test_other.py": "from conftest import ROOT\n",
        }
    )
    helper = STEP.Touched(frozenset({"SLOW_MODULES"}), frozenset(), False)
    got = _select(tmp_path, ["tests/conftest.py"], index, change_of=lambda p: helper)
    assert list(got.files) == ["tests/test_tier.py"] and got.widen is None
    hook = STEP.Touched(
        frozenset({"pytest_collection_modifyitems"}), frozenset(), False
    )
    assert _select(
        tmp_path, ["tests/conftest.py"], index, change_of=lambda p: hook
    ).widen
    assert _select(tmp_path, ["conftest.py"], index).widen  # the change is unreadable


def test_the_one_run_names_the_focus_files_and_the_canary_nodes_outside_them(tmp_path):
    _touch(tmp_path, "tests/test_a.py")
    index = _index({"test_a.py": "def test_one():\n    pass\n"})
    got = _select(tmp_path, ["tests/test_a.py"], index)
    canary = ["tests/test_a.py::test_one", "tests/test_b.py::test_alive"]
    command, functions = STEP.pytest_command(got, canary, index)
    assert command[-2:] == ["tests/test_a.py", "tests/test_b.py::test_alive"]
    assert functions == 2 and "no:xdist" in command


def test_a_handful_runs_serially_and_a_large_run_never_takes_the_whole_machine():
    half = max(1, (STEP.os.cpu_count() or 2) // 2)
    assert STEP.workers_for(STEP.SERIAL_BELOW - 1) == 0
    assert STEP.workers_for(STEP.SERIAL_BELOW) == 2
    assert STEP.workers_for(10**6) <= half
    assert STEP.workers_for(20, heavy=16) == min(half, 8)  # one per two canaries


def test_an_inventory_of_script_names_does_not_name_each_script():
    sources = frozenset("script_{}".format(n) for n in range(40))
    names = ", ".join('"scripts/script_{}.py"'.format(n) for n in range(40))
    listing = "FILES = [{}]; ".format(names)
    inventory = STEP.read_test_file(listing, (), sources)
    loader = STEP.read_test_file(listing + 'load_script("script_3")', (), sources)
    driver = STEP.read_test_file('run_py([SCRIPTS / "script_3.py"])', (), sources)
    module = STEP.Module("script_3", "script_3")
    assert inventory.inventory and not STEP.names_module(inventory, module)
    assert STEP.names_module(loader, module)  # a load still names it
    assert not driver.inventory and STEP.names_module(driver, module)


def test_the_lints_are_the_declared_commit_checks_own_and_none_is_the_tier_step():
    lints = STEP.declared_lints(ROOT)
    assert lints and all("check_smoke_budget" not in step for step in lints)
    assert lints[0] == "python project-trajectory/scripts/trace.py --strict"


def test_the_canary_set_is_capped_and_every_node_it_lists_is_a_real_test():
    listed = read_canary()
    assert listed and len(listed) == len(set(listed)) == len(CANARY)
    assert tuple(STEP.read_canary(ROOT)) == listed  # one list, two readers
    assert len(listed) <= CANARY_MAX, (
        "the canary set is fixed-size: past {} a new entry replaces one "
        "(tests/canary.txt)".format(CANARY_MAX)
    )
    for node in listed:
        path, _sep, name = node.partition("::")
        tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
        defined = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
        assert name in defined, node


def test_a_definitions_design_rows_are_followed_before_its_system_requirement():
    assert STEP.design_tags({"SR-156", "LLR-207"}) == {"LLR-207"}
    assert STEP.design_tags({"SR-156"}) == {"SR-156"}  # no design row named


def test_a_spine_link_outside_the_index_is_skipped_and_only_test_files_can_run(
    tmp_path,
):
    # The spine can link a path the index does not hold (evidence names a
    # golden file, or a file since removed). Narrowing skips it; it is not an
    # error, and only a test file is ever a candidate for the run.
    path = SRC + "agent_common.py"
    change = STEP.Touched(frozenset({"judge"}), frozenset({"LLR-1"}), False)
    got = _select(
        tmp_path,
        [path],
        _hub({}),
        spine=lambda root, p: ["tests/test_linked_elsewhere.py"],
        change_of=lambda p: change,
    )
    assert "tests/test_linked_elsewhere.py" not in got.files
    assert STEP._is_test("tests/test_a.py")
    assert not STEP._is_test("tests/golden/a.txt")
    assert not STEP._is_test("tests/traj_fixtures.py")
