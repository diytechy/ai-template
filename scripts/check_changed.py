#!/usr/bin/env python3
"""Local P9R validation selection; CI and the phase-close Full bar stay full.

Compare the complete proposed change to an explicit recorded base, including
the index, working tree and untracked files. Unknown impact always broadens.
This small table owns only omission of the expensive dashboard test family;
it does not select individual core tests or claim partial coverage as Full.
"""

import argparse
import json
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "project-trajectory/scripts"))
from kitlib.registry import parse_spec_frontmatter  # noqa: E402
from traj_status import STATUS_BEGIN, STATUS_END  # noqa: E402

HTML_TESTS = frozenset(
    "tests/" + name + ".py"
    for name in (
        "test_gen_trajectory",
        "test_dashboard_size_budget",
        "test_traj_graph",
        "test_traj_render",
        "test_traj_render_sweeps",
        "test_traj_views",
        "test_traj_panels",
    )
)
# These leaf validators do not produce stage, graph or snapshot values. Their
# own tests remain in the selected core set. Any new module starts as unknown.
CORE_ONLY = frozenset(
    "project-trajectory/scripts/" + name + ".py"
    for name in ("check_complexity", "check_figures", "check_need_form")
) | frozenset(
    "tests/" + name + ".py"
    for name in (
        "test_check_complexity",
        "test_check_complexity_cli",
        "test_check_figures",
        "test_check_need_form",
        "test_complexity_ratchet",
    )
)
REGISTRY_DATA = frozenset(
    "docs/requirements/" + name + ".toml"
    for name in (
        "stakeholder-needs",
        "system-requirements",
        "low-level-requirements",
        "interfaces",
        "components",
        "external",
        "open-items",
    )
) | {"docs/test/test-cases.toml"}
BOUNDARY_CASE = "tests/test_gen_trajectory.py::test_generates_self_contained_dashboard"
SOURCE_ROOT = "project-trajectory/scripts"
CLI_BEGIN = "<!-- BEGIN GENERATED CLI REFERENCE -->"
CLI_END = "<!-- END GENERATED CLI REFERENCE -->"
INTERFACE_BEGIN = "<!-- BEGIN GENERATED INTERFACE REFERENCE -->"
INTERFACE_END = "<!-- END GENERATED INTERFACE REFERENCE -->"
GENERATED_REGIONS = {
    "docs/status.md": (STATUS_BEGIN, STATUS_END),
    "docs/cli-reference.md": (CLI_BEGIN, CLI_END),
    "docs/interface-reference.md": (INTERFACE_BEGIN, INTERFACE_END),
}
GENERATED = frozenset(GENERATED_REGIONS) | frozenset(
    {
        "PROJECT_STATE.html",
        "docs/open-items.html",
        "docs/ratify/CURRENT.md",
        "docs/requirements/components.derived.toml",
        "docs/stage",
    }
)


def git(root, *args):
    return subprocess.run(
        ["git", *args],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout


def changed_paths(root, base):
    """None means the comparison is unavailable, never an empty change."""
    try:
        commit = git(root, "rev-parse", "--verify", base + "^{commit}").decode().strip()
        git(root, "merge-base", "--is-ancestor", commit, "HEAD")
        tracked = git(root, "diff", "--name-only", "-z", "--no-renames", commit, "--")
        added = git(root, "ls-files", "--others", "--exclude-standard", "-z")
        return sorted({p.decode("utf-8") for p in (tracked + added).split(b"\0") if p})
    except (OSError, subprocess.CalledProcessError, UnicodeError):
        return None


def shape(value):
    """Conservative TOML shape comparison, not a second schema validator.

    New/deleted rows or fields broaden. Scalar edits and homogeneous array
    values may narrow; the ordinary trace checks still judge their validity.
    """
    if isinstance(value, dict):
        return tuple((k, shape(v)) for k, v in sorted(value.items()))
    if isinstance(value, list):
        return ("array", frozenset(shape(v) for v in value))
    return type(value).__name__


def data_only(root, base, path):
    try:
        old_text = git(root, "show", base + ":" + path).decode("utf-8")
        new_text = (root / path).read_text(encoding="utf-8")
        if path.endswith(".toml"):
            before, after = tomllib.loads(old_text), tomllib.loads(new_text)
        else:
            before = parse_spec_frontmatter(old_text, path)[0]
            after = parse_spec_frontmatter(new_text, path)[0]
        return shape(before) == shape(after)
    except (OSError, subprocess.CalledProcessError, UnicodeError, ValueError):
        return False


def generated_region_prose_unchanged(root, base, path):
    """A block generator may accompany a change only if its prose is untouched."""

    begin, end = GENERATED_REGIONS[path]

    def authored(text):
        if text.count(begin) != 1 or text.count(end) != 1:
            return None
        head, tail = text.split(begin)
        _, foot = tail.split(end)
        return head, foot

    try:
        before = authored(git(root, "show", base + ":" + path).decode("utf-8"))
        after = authored((root / path).read_text(encoding="utf-8"))
        return before is not None and before == after
    except (OSError, subprocess.CalledProcessError, UnicodeError, ValueError):
        return False


def select(root, base, *, full=False):
    paths = changed_paths(root, base) if base else None
    reason = "Full assurance requested" if full else "comparison base unavailable"
    primary = [p for p in paths or () if p not in GENERATED]
    if not full and primary:
        unknown = [
            path
            for path in paths
            if not (
                path in CORE_ONLY
                and (root / path).is_file()
                or (
                    path in REGISTRY_DATA
                    or (
                        path.startswith("docs/work/")
                        and Path(path).name.startswith("WI-")
                        and path.endswith(".md")
                    )
                )
                and data_only(root, base, path)
                or path in GENERATED
                and (root / path).is_file()
                and (
                    path not in GENERATED_REGIONS
                    or generated_region_prose_unchanged(root, base, path)
                )
            )
        ]
        if not unknown:
            return {
                "suite": "core+boundary",
                "reason": "only declared independent validators or unchanged registry shapes",
                "paths": paths,
            }
        reason = "HTML/shared/schema/tooling or unknown impact: " + ", ".join(unknown)
    elif paths == [] and not full:
        reason = "no proposed change; no narrower assurance claimed"
    elif paths and not full:
        reason = "generated-output-only change has no classified source"
    return {"suite": "full", "reason": reason, "paths": paths}


def commands(root, selection):
    pytest = [sys.executable, "-m", "pytest", "-q", "-n", "auto"]
    if selection["suite"] == "full":
        return [pytest]
    # Explicit files avoid collecting the omitted HTML modules. Every other
    # test, including registry, architecture and other HTML emitters, remains.
    core = sorted(
        p.relative_to(root).as_posix()
        for p in (root / "tests").rglob("test_*.py")
        if p.relative_to(root).as_posix() not in HTML_TESTS
    )
    scripts = SOURCE_ROOT + "/"
    freshness = [
        [sys.executable, scripts + name, *args, "--check"]
        for name, args in (
            ("gen_open_items.py", ("--root", ".")),
            ("gen_components.py", ("--root", ".")),
            (
                "gen_arch_map.py",
                (
                    "--root",
                    ".",
                    "--src",
                    SOURCE_ROOT,
                    "--cli-doc",
                    "docs/cli-reference.md",
                ),
            ),
            (
                "gen_arch_map.py",
                (
                    "--root",
                    ".",
                    "--src",
                    SOURCE_ROOT,
                    "--contracts-doc",
                    "docs/interface-reference.md",
                ),
            ),
            ("trace.py", ("--root", ".", "--approve", "modified")),
        )
    ]
    return [
        [*pytest, *core],
        [*pytest, BOUNDARY_CASE],
        [sys.executable, scripts + "derive_stage.py", "--root", ".", "--check"],
        [
            sys.executable,
            scripts + "trace.py",
            "--root",
            ".",
            "--strict",
            "--no-placeholders",
            "--strict-schema",
        ],
        [sys.executable, scripts + "gen_trajectory.py", "--root", ".", "--check"],
        [
            sys.executable,
            scripts + "gen_trajectory.py",
            "--root",
            ".",
            "--status",
            "--check",
        ],
        *freshness,
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="recorded base of the entire proposed change")
    parser.add_argument(
        "--full",
        action="store_true",
        help="phase close, periodic assurance, or known layout stress",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="execute; otherwise print the selection and commands",
    )
    args = parser.parse_args(argv)
    result = select(ROOT, args.base, full=args.full)
    planned = commands(ROOT, result)
    print(json.dumps({**result, "commands": planned}, indent=2), flush=True)
    if args.run:
        for command in planned:
            code = subprocess.run(command, cwd=ROOT).returncode
            if code:
                return code
    return 0


if __name__ == "__main__":
    sys.exit(main())
