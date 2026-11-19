"""Every tracked shell file parses on the oldest /bin/sh the kit meets (WI-909).

WHY THESE TESTS EXIST. macOS still ships bash 3.2 as /bin/sh. It reads an
apostrophe inside a double-quoted expansion word ("${VAR:-it's}") as an opening
quote, so the file fails to parse. dash (Linux) and bash 5 (Git Bash) accept
it. WI-880's hook probe shipped that shape, and every git hook refused on a
stock Mac while the Linux and Windows checks kept passing.

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


# setup.sh and check.sh are bash scripts (`set -o pipefail`). `sh -n` above only
# parses, so it cannot see that dash (Debian/Ubuntu's /bin/sh) stops at that
# line before doing anything. An instruction that says `sh scripts/setup.sh`
# therefore leaves the commit hooks off on the most common Linux.
_BASH_ONLY = ("setup.sh", "check.sh")
_RUN_WITH_SH = re.compile(r"(?<![\w/.-])sh scripts/(?:setup|check)\.sh")


def test_no_shipped_instruction_runs_a_bash_script_with_sh():
    for name in _BASH_ONLY:
        path = ROOT / "project-trajectory" / "scripts" / name
        text = path.read_text(encoding="utf-8")
        assert "pipefail" in text, name + " is no longer bash-only; drop this pin"
    listed = subprocess.run(
        ["git", "ls-files", "-z", "project-trajectory"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout.split(b"\0")
    bad = []
    for rel in filter(None, (name.decode() for name in listed)):
        # RESYNC_PACK.md narrates past releases, wording included.
        if rel.endswith("RESYNC_PACK.md") or not (ROOT / rel).is_file():
            continue
        try:
            text = (ROOT / rel).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        # Backticks and line wraps removed, so `sh\n  scripts/setup.sh` counts.
        if _RUN_WITH_SH.search(" ".join(text.replace("`", "").split())):
            bad.append(rel)
    assert not bad, "say `bash scripts/setup.sh` (or check.sh) in: " + ", ".join(bad)


# --- the hooks read the policy through one parse (SR-031, LLR-021) ----------

HOOKS_DIR = ROOT / "project-trajectory" / "hooks"
HOOK_NAMES = ("pre-commit", "commit-msg", "pre-push")
# A policy file named as a whole file name: `privacy-review.XXXXXX`, the
# pre-push review dump's temp-file prefix, names no policy file.
_POLICY_FILE = re.compile(
    r"(?<![\w.-])(?:process\.toml|privacy-check|privacy-review)(?![\w.-])"
)
_MESSAGE = re.compile(r"(?:echo|printf)\b")
_TEXT_TOOL_PIPE = re.compile(r"\|\s*(?:grep|sed|awk|head|cat|tr|cut)\b")


def _code_lines(path):
    """(line number, line) for every non-blank, non-comment line."""
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip() and not line.lstrip().startswith("#"):
            yield n, line


def test_no_hook_reads_the_policy_as_text():
    """TC-031 (SR-031: one parse, one answer): no shipped hook and not the
    probe touches docs/process.toml, docs/privacy-check or
    docs/privacy-review with a text tool. Every code line naming one of them
    is an echo or printf message, piped into no text tool.

    Implements: TC-031
    """
    bad = []
    for name in HOOK_NAMES + ("kit-python.sh",):
        for n, line in _code_lines(HOOKS_DIR / name):
            if not _POLICY_FILE.search(line):
                continue
            body = line.strip()
            if _MESSAGE.match(body) and not _TEXT_TOOL_PIPE.search(body):
                continue
            bad.append("{}:{}: {}".format(name, n, body))
    assert not bad, "a hook reads the policy as text:\n" + "\n".join(bad)


def _call_lines(lines, function, hook):
    """The line numbers of the code lines calling `function <hook>`."""
    call = re.compile(r"\s*{} {}\b".format(function, hook))
    return [n for n, text in lines if call.match(text)]


def _own_resolution(hook, lines):
    """The code lines where a hook names the policy read or the scripts
    override itself, rather than leaving both to the probe."""
    return [
        "{}:{}: {}".format(hook, n, text.strip())
        for n, text in lines
        if "--hook-policy" in text or "KIT_SCRIPTS_DIR" in text
    ]


def test_each_hook_runs_the_one_read_once_after_the_probe():
    """TC-021 (LLR-021): each hook calls the probe's one policy read exactly
    once, after its interpreter probe, and resolves neither the read nor the
    scripts directory itself; the probe holds the one read and the one
    interpreter candidate loop.

    Implements: TC-021
    """
    for name in HOOK_NAMES:
        lines = list(_code_lines(HOOKS_DIR / name))
        probe = _call_lines(lines, "kit_python", name)
        read = _call_lines(lines, "kit_policy", name)
        assert len(probe) == 1 and len(read) == 1, (name, probe, read)
        assert read[0] > probe[0], (name, probe, read)
        own = _own_resolution(name, lines)
        assert not own, own
    shared = [text.strip() for _, text in _code_lines(HOOKS_DIR / "kit-python.sh")]
    reads = [s for s in shared if "--hook-policy" in s and not _MESSAGE.match(s)]
    assert len(reads) == 1, reads
    loops = [s for s in shared if "for cand in" in s]
    assert len(loops) == 1, loops
