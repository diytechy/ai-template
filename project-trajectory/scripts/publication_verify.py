"""Shared, lower-level product-bar and generated-surface readers."""

import configparser
import re
import subprocess
from pathlib import Path

import agent_common as ac

SCRIPTS = Path(__file__).resolve().parent

ADJUDICATION_SURFACES = (
    "docs/work/",
    "docs/archive/work/",
    "docs/log.d/",
    "docs/reviews/",
    "docs/requirements/system-requirements.toml",
    "docs/requirements/system-requirements.csv",
    "docs/requirements/low-level-requirements.toml",
    "docs/requirements/low-level-requirements.csv",
    "docs/test/test-cases.toml",
    "docs/test/test-cases.csv",
    "docs/requirements/open-items.toml",
    "docs/requirements/open-items.csv",
    "docs/handbacks/",
)


def run(argv, cwd):
    proc = subprocess.run(
        argv,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
    )
    out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    return proc.returncode, out


def branch_tree_script(wt, root, name):
    """The candidate tree's harness script, falling back to this kit copy."""
    rels = []
    try:
        rels.append(SCRIPTS.relative_to(root))
    except ValueError:
        pass
    rels.extend((Path("scripts"), Path("project-trajectory") / "scripts"))
    for rel in rels:
        candidate = Path(wt) / rel / name
        if candidate.is_file():
            return candidate
    return SCRIPTS / name


def passed_steps(output):
    names = set()
    for line in output.splitlines():
        if re.match(r"\s*PASS\s", line):
            parts = line.split()
            if len(parts) >= 2:
                names.add(parts[1])
    return names


def run_bar(wt, root, tier, gate=None):
    """Run the declared trunk-lane bar and fail closed on nonzero or SKIP."""
    py = ac.harness_python(root)
    check = branch_tree_script(wt, root, "check.py")
    argv = [str(py), str(check), "--jobs", "0", "--tier", tier, "--trunk-lane"]
    if gate:
        argv += ["--stage", gate]
    code, output = run(argv, wt)
    skips = [line for line in output.splitlines() if re.match(r"\s*SKIP\s", line)]
    if code != 0:
        return False, output, "bar exit {}".format(code)
    if skips:
        return (
            False,
            output,
            "bar reported SKIP - a skip is a refusal here:\n" + "\n".join(skips),
        )
    return (
        True,
        output,
        "bar PASS ({} steps, tier {}{})".format(
            len(passed_steps(output)), tier, ", gate " + gate if gate else ""
        ),
    )


def generated_table(root):
    """The stack.ini [generated] rows as ``{path: kind}``."""
    ini = Path(root) / "docs" / "stack.ini"
    if not ini.exists():
        return {}
    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str
    try:
        parser.read_string(ini.read_text(encoding="utf-8-sig", errors="replace"))
    except (configparser.Error, OSError):
        return {}
    if not parser.has_section("generated"):
        return {}
    return {
        key.strip(): (value or "").split("|")[0].strip()
        for key, value in parser.items("generated")
        if key.strip()
    }


def generated_paths(root):
    return list(generated_table(root))
