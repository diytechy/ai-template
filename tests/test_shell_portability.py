"""Every tracked shell file parses on the oldest /bin/sh the kit meets (WI-909).

WHY THESE TESTS EXIST. macOS still ships bash 3.2 as /bin/sh. It reads an
apostrophe inside a double-quoted expansion word ("${VAR:-it's}") as an opening
quote, so the file fails to parse. dash (Linux) and bash 5 (Git Bash) accept
it. WI-880's hook probe shipped that shape, and every git hook refused on a
stock Mac while the Linux and Windows bars stayed green.

Two checks, so the class is caught on every platform, not only on a Mac:

- the static rule: no single quote inside a ${NAME<op>word} word. It is pure
  Python, so it fails on Linux and Windows too, before a Mac ever sees it;
- the parse: `sh -n` on every file, which is the real failure wherever /bin/sh
  is bash 3.2 (CI's macOS job) and catches any other syntax error elsewhere.

WHAT IS DELIBERATELY NOT TESTED: ShellCheck-grade lint. That would be a
dependency (CLAUDE.md, the ledger rule), and this guard is for the class that
broke, nothing wider.
"""

import re
import subprocess

import pytest

from conftest import ROOT, env_gate_skipif

_SHEBANG = re.compile(rb"^#!\s*/(?:usr/)?bin/(?:env\s+)?(?:ba)?sh\b")
# ${NAME:-word} ${NAME-word} and the = + ? forms, with a ' in the word.
_QUOTE_IN_WORD = re.compile(r"\$\{[A-Za-z_][A-Za-z0-9_]*:?[-=+?][^}]*'")


def _shell_files():
    listed = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True
    ).stdout.split(b"\0")
    found = []
    for name in filter(None, listed):
        rel = name.decode()
        path = ROOT / rel
        if rel.startswith("docs/archive/") or not path.is_file():
            continue
        if rel.endswith((".sh", ".command")):
            found.append(rel)
            continue
        with path.open("rb") as fh:
            if _SHEBANG.match(fh.read(64)):
                found.append(rel)
    return found


SHELL_FILES = _shell_files()


def test_the_scan_finds_the_hooks_and_launchers():
    # An empty scan would pass every test below while reading nothing.
    for rel in ("project-trajectory/hooks/kit-python.sh", "agent-resume.sh"):
        assert rel in SHELL_FILES, rel


@pytest.mark.parametrize("rel", SHELL_FILES)
def test_no_single_quote_inside_an_expansion_word(rel):
    bad = [
        f"{rel}:{n}: {line.strip()}"
        for n, line in enumerate(
            (ROOT / rel).read_text(encoding="utf-8").splitlines(), 1
        )
        if not line.lstrip().startswith("#") and _QUOTE_IN_WORD.search(line)
    ]
    assert not bad, (
        "bash 3.2 (macOS /bin/sh) cannot parse a ' inside ${VAR:-word}; "
        "assign the default to a variable first:\n" + "\n".join(bad)
    )


def test_the_rule_catches_the_shape_that_broke():
    assert _QUOTE_IN_WORD.search('echo "${X:-it\'s here}"')
    assert not _QUOTE_IN_WORD.search('echo "${X:-$fallback}"')


@env_gate_skipif("posix-shell")
@pytest.mark.parametrize("rel", SHELL_FILES)
def test_every_shell_file_parses_under_sh(rel):
    result = subprocess.run(["sh", "-n", rel], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
