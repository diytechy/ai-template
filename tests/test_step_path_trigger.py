"""A sensor follows relevant changes even before its stage rung."""

import configparser
from pathlib import Path

import pytest
from conftest import ROOT, load_script

check = load_script("check")


def profile(paths="src/* docs/baseline scripts/sensor.py docs/stack.ini"):
    out = configparser.ConfigParser(interpolation=None)
    out.read_string(
        "[step:sensor]\ncommand = {py} scripts/sensor.py\nfrom-stage = DevStg-Impl\npaths = "
        + paths
    )
    return out


def selected(monkeypatch, changes, stage="DevStg-Reqs", config=None):
    monkeypatch.setattr(check, "changed_paths", lambda root: changes, raising=False)
    plan = check.resolve_plan(stage, 85, "smoke", None, config or profile())
    return "sensor" in {step[0] for step in plan}


@pytest.mark.parametrize(
    "path", ["src/nested/a.py", "docs/baseline", "scripts/sensor.py", "docs/stack.ini"]
)
def test_matching_change_below_rung(monkeypatch, path):
    assert selected(monkeypatch, {path})


def test_unrelated_change_below_rung(monkeypatch):
    assert not selected(monkeypatch, {"docs/notes.md"})


def test_at_rung_with_no_change(monkeypatch):
    assert selected(monkeypatch, set(), "DevStg-Impl")


def test_unknown_change_runs_below_rung(monkeypatch):
    assert selected(monkeypatch, None)


@pytest.mark.parametrize("changes", [None, {"src/a.py"}, set()])
def test_no_paths_remains_rung_only(monkeypatch, changes):
    config = profile("")
    assert not selected(monkeypatch, changes, config=config)
    assert selected(monkeypatch, changes, "DevStg-Impl", config)
    config.remove_option("step:sensor", "paths")
    assert not selected(monkeypatch, changes, config=config)


@pytest.mark.parametrize("raw", [None, b""])
def test_no_staged_diff_is_unknown(monkeypatch, raw):
    monkeypatch.setattr(check._kitgit, "git_bytes", lambda *args: raw)
    monkeypatch.setattr(check, "_work_branch", lambda root: False)
    assert check.changed_paths(Path(".")) is None


def test_staged_paths_include_deletions_and_both_rename_sides(monkeypatch):
    calls = []

    def diff(root, args):
        calls.append(args)
        return b"src/old.py\0docs/new name.md\0src/deleted.py\0"

    monkeypatch.setattr(check._kitgit, "git_bytes", diff)
    assert check.changed_paths(Path(".")) == {
        "src/old.py",
        "docs/new name.md",
        "src/deleted.py",
    }
    assert "--cached" in calls[0] and "--no-renames" in calls[0]
    assert "--diff-filter=d" not in calls[0]


@pytest.mark.parametrize(
    "base,raw,expected",
    [
        (None, b"", None),
        ("base", None, None),
        ("base", b"src/a.py\0", {"src/a.py"}),
        ("base", b"", None),
    ],
)
def test_lane_range_or_unknown(monkeypatch, base, raw, expected):
    import agent_common

    monkeypatch.setattr(check, "_work_branch", lambda root: True)
    monkeypatch.setattr(agent_common, "default_base", lambda root: base)
    monkeypatch.setattr(
        check._kitgit,
        "git_bytes",
        lambda root, args: b"" if "--cached" in args else raw,
    )
    assert check.changed_paths(Path(".")) == expected


@pytest.mark.parametrize(
    "changes,stage,expected",
    [
        ({"src/a.py"}, "DevStg-Reqs", ["sensor"]),
        ({"docs/notes.md"}, "DevStg-Reqs", []),
        (None, "DevStg-Reqs", ["sensor"]),
        (set(), "DevStg-Impl", ["sensor"]),
    ],
)
def test_hook_runs_only_selected_path_steps(monkeypatch, changes, stage, expected):
    config = profile()
    seen = []
    monkeypatch.setattr(
        check.sys, "argv", ["check.py", "--path-triggered", "--stage", stage]
    )
    monkeypatch.setattr(check, "load_profile", lambda: config)
    monkeypatch.setattr(check, "changed_paths", lambda root: changes, raising=False)
    monkeypatch.setattr(
        check, "run_plan", lambda plan, *args: seen.extend(s[0] for s in plan) or []
    )
    check.main()
    assert seen == expected


def test_repo_sensors_include_their_inputs():
    config = check.load_profile(ROOT / "docs/stack.ini")
    from kitlib.config import step_paths

    declared = step_paths(config)
    own = {
        "complexity": [
            "docs/complexity-baseline",
            "project-trajectory/scripts/check_complexity.py",
        ],
        "dupes-census": ["project-trajectory/scripts/check_dupes_census.py"],
        "readability": [
            "docs/complexity-baseline",
            "docs/flag-axis-baseline",
            "project-trajectory/scripts/check_readability.py",
        ],
        "smoke": [
            "scripts/check_smoke_budget.py",
            "tests/conftest.py",
            "tests/test_smoke_budget.py",
        ],
    }
    for name, inputs in own.items():
        for path in [
            *inputs,
            "docs/stack.ini",
            "tests/nested/test_example.py",
            "project-trajectory/scripts/kitlib/config.py",
        ]:
            assert any(
                check.fnmatch.fnmatchcase(path, pattern) for pattern in declared[name]
            ), (name, path)


def test_hook_without_path_declarations_needs_no_stage(monkeypatch):
    config = profile("")
    monkeypatch.setattr(check.sys, "argv", ["check.py", "--path-triggered"])
    monkeypatch.setattr(check, "load_profile", lambda: config)

    def forbidden(*args):
        pytest.fail("a rung-only adopter's hook must not resolve stage or read git")

    monkeypatch.setattr(check, "resolve_stage", forbidden)
    monkeypatch.setattr(check, "changed_paths", forbidden)
    check.main()


@pytest.mark.parametrize(
    "changes,stage", [(None, "DevStg-Reqs"), (set(), "DevStg-Impl")]
)
def test_hook_excludes_smoke_but_gate_keeps_it(monkeypatch, changes, stage):
    config = profile()
    config.read_string(
        "[step:smoke]\ncommand = {py} -m pytest -m smoke\n"
        "from-stage = DevStg-Impl\npaths = src/* docs/stack.ini"
    )
    seen = []
    monkeypatch.setattr(check, "load_profile", lambda: config)
    monkeypatch.setattr(check, "changed_paths", lambda root: changes)
    monkeypatch.setattr(
        check, "run_plan", lambda plan, *args: seen.extend(s[0] for s in plan) or []
    )
    monkeypatch.setattr(
        check.sys, "argv", ["check.py", "--path-triggered", "--stage", stage]
    )
    check.main()
    assert seen == ["sensor"]
    assert "smoke" in {
        s[0] for s in check.resolve_plan(stage, 85, "smoke", None, config)
    }
