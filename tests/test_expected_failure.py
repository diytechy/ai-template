"""The expected-failure marker's rule in process (WI-996): the declaration, the
count and the per-file table `integrate.py record-checks` and the refresh both apply.

A test's red-before is proven by a strict expected-failure mark. The mark is
declared once, as `docs/stack.ini` `[product] expected_failure_marker`; a
file's count of it is taken from its bytes with ASCII whitespace removed; and
the table compares each test file's count at the lane's last recorded tree
with its count in the staged tree. The same reader answers the commit checks'
shell line, the other value a passed-checks record needs: `docs/process.toml`
`[required-checks] commit` names a check suite and `docs/stack.ini`
`[check-suites]` holds that suite's line. The real-lane cases are in
`tests/test_expected_failure_lane.py`.

The cases that pin the rule's text build the mark from `conftest.EXPECTED_FAILURE_MARKER`, so
`tests/` never holds it whole.
"""

import os
import re
import stat
import subprocess
from pathlib import Path

import pytest
from conftest import (
    EXPECTED_FAILURE_MARKER,
    SCRIPTS,
    env_gate_skipif,
    load_script,
    write_lf,
)
from kitlib import config as kconfig
from kitlib import expected_failure as kef
from kitlib import spine as kspine
from kitlib import verdict as kv

REPO = SCRIPTS.parent.parent
TEMPLATE = SCRIPTS.parent / "stack.ini.template"
POLICY_TEMPLATE = SCRIPTS.parent / "process.toml.template"
OWN_DECLARATION = REPO / "docs" / "stack.ini"
P = "tests/test_a.py"
Q = "tests/test_b.py"
OTHER = "tests/test_other.py"
# The fixtures' check suite. Not the name the templates ship, so no case
# passes on a reader that looks `smoke` up whatever the policy file names.
SUITE = "fast"
# A `docs/process.toml` naming it as the suite a commit must pass.
NAMED = '[required-checks]\ncommit = "{}"\n'.format(SUITE)
# An undeclared value's line opens with where the value belongs, then why it
# is not there.
MARKER_AT = "docs/stack.ini [product] expected_failure_marker - "
NAME_AT = "docs/process.toml [required-checks] commit - "
SUITE_AT = "docs/stack.ini [check-suites] {} - ".format(SUITE)
UNPARSED = "the file does not parse ("
NO_TABLE = "the table is absent"
NO_KEY = "the key is absent"
NO_NAME = "the value is not a suite's name"
# What a cause gains while the retired section still declares the old key.
RETIRED = "; the retired [bars] {} still declares it and is no longer read"


def _declare(root, text):
    write_lf(root, "docs/stack.ini", text)


def _policy(root, text):
    write_lf(root, "docs/process.toml", text)


def _section(name, *lines):
    return "[{}]\n".format(name) + "".join(line + "\n" for line in lines)


def _marker(value):
    """A `[product]` section declaring `value` as the marker."""
    return _section("product", "expected_failure_marker = " + value)


def _suite(line, name=SUITE):
    """A `[check-suites]` section whose suite `name` runs `line`."""
    return _section("check-suites", "{} = {}".format(name, line))


# A whole `docs/stack.ini`: the marker, and two suites, the shipped name's
# line beside the fixtures'.
WHOLE = _marker("mark(here)") + _section(
    "check-suites", "smoke = another suite", SUITE + " = run the checks"
)


def _marked(*marks):
    """Python source holding one test under each of `marks`."""
    return "\n".join(
        "@{}\ndef test_{}():\n    assert False\n".format(mark, n)
        for n, mark in enumerate(marks)
    ).encode("utf-8")


def _git(root, *args, stdin=None):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        input=stdin,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.decode("utf-8").strip()


def _git_repo(root):
    root.mkdir(exist_ok=True)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "config", "core.autocrlf", "false")
    return root


def _text(path):
    """A file's comment and value lines as one line of words."""
    return " ".join(
        re.sub(r"^#\s?", "", line).strip()
        for line in path.read_text(encoding="utf-8").splitlines()
    )


def _declared(path):
    """`[product] expected_failure_marker` as declared in `path`, `""` when
    it declares none."""
    return kconfig.read_stack_ini(path).get(
        "product", "expected_failure_marker", fallback=""
    )


def _mark_comment():
    """The comment block above the template's `expected_failure_marker` line,
    as one line of lower-case words; `""` when the template has no such key."""
    lines = TEMPLATE.read_text(encoding="utf-8").splitlines()
    keys = [
        n for n, line in enumerate(lines) if line.startswith("expected_failure_marker")
    ]
    if not keys:
        return ""
    above = []
    for line in reversed(lines[: keys[0]]):
        if not line.startswith("#"):
            break
        above.insert(0, re.sub(r"^#\s?", "", line).strip())
    return " ".join(above).lower()


# --- the declaration ----------------------------------------------------------


def test_a_declared_value_is_the_stripped_text(tmp_path):
    """Implements: TC-421"""
    _declare(tmp_path, _marker("  mark(here)   ") + _suite("  run the checks  "))
    _policy(tmp_path, NAMED)
    settings = kef.read_commit_check_settings(tmp_path)
    assert settings.marker == "mark(here)"
    assert settings.commit_checks == "run the checks"
    assert settings.refusal("commit_checks", "marker") is None


def test_the_commit_checks_are_the_suite_the_policy_file_names(tmp_path):
    """Implements: TC-421"""
    # Two suites are declared, the shipped name among them: the line read is
    # the one `[required-checks] commit` names, and renaming it reads the other.
    _declare(tmp_path, WHOLE)
    _policy(tmp_path, NAMED)
    assert kef.read_commit_check_settings(tmp_path).commit_checks == "run the checks"
    _policy(tmp_path, NAMED.replace(SUITE, "smoke"))
    assert kef.read_commit_check_settings(tmp_path).commit_checks == "another suite"


@pytest.mark.parametrize(
    "stack, policy, key, at",
    [
        # The marker: `docs/stack.ini` `[product]`.
        (None, NAMED, "marker", MARKER_AT + "the file is absent"),
        (_marker("a") + _marker("b"), NAMED, "marker", MARKER_AT + UNPARSED),
        (
            _suite("run the checks"),
            NAMED,
            "marker",
            MARKER_AT + "the section is absent",
        ),
        (_section("product", "test = x"), NAMED, "marker", MARKER_AT + NO_KEY),
        (_marker(""), NAMED, "marker", MARKER_AT + "the value is empty"),
        (_marker("    "), NAMED, "marker", MARKER_AT + "the value is empty"),
        # The suite's name: `docs/process.toml` `[required-checks]`. Without it
        # no declared suite's line is read, the shipped name's included.
        (WHOLE, None, "commit_checks", NAME_AT + "the file is absent"),
        (WHOLE, "[required-checks\n", "commit_checks", NAME_AT + UNPARSED),
        (WHOLE, '[policies]\ntrunk = "main"\n', "commit_checks", NAME_AT + NO_TABLE),
        (WHOLE, 'required-checks = "fast"\n', "commit_checks", NAME_AT + NO_TABLE),
        (WHOLE, "[required-checks]\n", "commit_checks", NAME_AT + NO_KEY),
        (WHOLE, '[required-checks]\ncommit = ""\n', "commit_checks", NAME_AT + NO_NAME),
        (
            WHOLE,
            '[required-checks]\ncommit = "  "\n',
            "commit_checks",
            NAME_AT + NO_NAME,
        ),
        (WHOLE, "[required-checks]\ncommit = 3\n", "commit_checks", NAME_AT + NO_NAME),
        # The named suite's line: `docs/stack.ini` `[check-suites]`.
        (None, NAMED, "commit_checks", SUITE_AT + "the file is absent"),
        (_suite("a") + _suite("b"), NAMED, "commit_checks", SUITE_AT + UNPARSED),
        (
            _marker("mark(here)"),
            NAMED,
            "commit_checks",
            SUITE_AT + "the section is absent",
        ),
        (_suite("another suite", "smoke"), NAMED, "commit_checks", SUITE_AT + NO_KEY),
        (_suite(""), NAMED, "commit_checks", SUITE_AT + "the value is empty"),
        (_suite("    "), NAMED, "commit_checks", SUITE_AT + "the value is empty"),
    ],
    ids=[
        "marker-no-file",
        "marker-unparseable",
        "marker-no-section",
        "marker-no-key",
        "marker-empty",
        "marker-blank",
        "name-no-file",
        "name-unparseable",
        "name-no-table",
        "name-not-a-table",
        "name-no-key",
        "name-empty",
        "name-blank",
        "name-not-text",
        "suite-no-file",
        "suite-unparseable",
        "suite-no-section",
        "suite-no-key",
        "suite-empty",
        "suite-blank",
    ],
)
def test_each_undeclared_state_names_the_key_and_the_cause(
    tmp_path, stack, policy, key, at
):
    """Implements: TC-421"""
    if stack is not None:
        _declare(tmp_path, stack)
    if policy is not None:
        _policy(tmp_path, policy)
    settings = kef.read_commit_check_settings(tmp_path)
    assert getattr(settings, key) == ""
    assert settings.causes[key].startswith(at)
    assert at in settings.refusal(key)


@pytest.mark.parametrize(
    "field, old, policy, at",
    [
        ("marker", "red_mark", None, MARKER_AT + "the section is absent"),
        ("commit_checks", "review", None, NAME_AT + "the file is absent"),
        ("commit_checks", "review", NAMED, SUITE_AT + "the section is absent"),
    ],
    ids=["the-marker", "the-suites-name", "the-suites-line"],
)
def test_a_retired_bars_section_is_never_read_and_is_named(
    tmp_path, field, old, policy, at
):
    """Implements: TC-421"""
    # `[bars]`, where both values lived, still declares them: neither is
    # read, and each cause says the old key is what stopped counting.
    retired = _section("bars", "review = the old suite", "red_mark = old_mark(")
    _declare(tmp_path, retired)
    if policy is not None:
        _policy(tmp_path, policy)
    settings = kef.read_commit_check_settings(tmp_path)
    assert (settings.commit_checks, settings.marker) == ("", "")
    assert settings.causes[field].startswith(at)
    assert RETIRED.format(old) in settings.causes[field]
    assert RETIRED.format(old) in settings.refusal(field)
    # A `[bars]` holding only the other key says nothing about this one.
    other = "red_mark" if old == "review" else "review"
    _declare(tmp_path, _section("bars", other + " = the old value"))
    assert "[bars]" not in kef.read_commit_check_settings(tmp_path).causes[field]
    # Declared where they now belong, the new values are the ones read.
    _declare(tmp_path, retired + WHOLE)
    _policy(tmp_path, NAMED)
    settings = kef.read_commit_check_settings(tmp_path)
    assert (settings.commit_checks, settings.marker) == ("run the checks", "mark(here)")
    assert settings.refusal("commit_checks", "marker") is None


def test_the_commit_checks_and_the_marker_come_from_one_parse(tmp_path, monkeypatch):
    """Implements: TC-421"""
    calls = []
    parse = kconfig.read_stack_ini

    def counted(path, **kwargs):
        calls.append(Path(path))
        return parse(path, **kwargs)

    monkeypatch.setattr(kconfig, "read_stack_ini", counted)
    _declare(tmp_path, WHOLE)
    _policy(tmp_path, NAMED)
    settings = kef.read_commit_check_settings(tmp_path)
    assert calls == [tmp_path / "docs" / "stack.ini"]
    assert (settings.commit_checks, settings.marker) == ("run the checks", "mark(here)")


def test_both_keys_undeclared_are_both_named(tmp_path):
    """Implements: TC-421"""
    _declare(tmp_path, "[paths]\ntests = tests\n")
    refusal = kef.read_commit_check_settings(tmp_path).refusal(
        "commit_checks", "marker"
    )
    assert "docs/process.toml [required-checks] commit" in refusal
    assert "docs/stack.ini [product] expected_failure_marker" in refusal
    _declare(tmp_path, _suite("run the checks"))
    _policy(tmp_path, NAMED)
    refusal = kef.read_commit_check_settings(tmp_path).refusal(
        "commit_checks", "marker"
    )
    assert "docs/stack.ini [product] expected_failure_marker" in refusal
    assert "[required-checks] commit" not in refusal
    assert "[check-suites]" not in refusal


def test_the_template_declares_the_reference_value_with_no_at_sign():
    """Implements: TC-421"""
    value = _declared(TEMPLATE)
    assert value == EXPECTED_FAILURE_MARKER
    assert "@" not in value


@pytest.mark.parametrize(
    "words",
    [
        ("required", "no default"),
        ("whitespace ignored",),
        ("strict expected-failure", "restricted to assertion failures"),
        ("test.failing", "helper", "re-throws"),
        ("every adopter", "never marks a test"),
    ],
    ids=["required", "whitespace", "other-stacks", "the-helper", "every-adopter"],
)
def test_the_template_comment_states_the_rule(words):
    """Implements: TC-421"""
    comment = _mark_comment()
    assert all(word in comment for word in words), comment


def test_this_repo_declares_the_templates_value():
    """Implements: TC-421"""
    assert _declared(OWN_DECLARATION) == _declared(TEMPLATE) == EXPECTED_FAILURE_MARKER


def test_the_shipped_templates_name_a_suite_they_declare(tmp_path):
    """Implements: TC-421"""
    # The declaration is two files: the suite the policy template names is
    # one the stack template gives a line, and this repository's pair agree.
    _declare(tmp_path, TEMPLATE.read_text(encoding="utf-8"))
    _policy(tmp_path, POLICY_TEMPLATE.read_text(encoding="utf-8"))
    for root in (tmp_path, REPO):
        settings = kef.read_commit_check_settings(root)
        assert settings.refusal("commit_checks", "marker") is None
        assert settings.commit_checks and settings.marker == EXPECTED_FAILURE_MARKER


def test_the_contract_names_the_key_and_its_refusal():
    """Implements: TC-421"""
    header = _text(OWN_DECLARATION)
    contract = header[
        header.index("Contract IF-022:") : header.index("Contract IF-049:")
    ]
    assert "`[product] expected_failure_marker`" in contract
    assert "whitespace ignored" in contract
    assert "the marker refuses a record-checks run and a refresh alike" in contract


# --- the count ----------------------------------------------------------------


def test_a_count_is_non_overlapping_occurrences():
    """Implements: TC-422"""
    assert kef.count(b"one ab two ab", "ab") == 2
    assert kef.count(b"ababab", "abab") == 1
    assert kef.count(b"nothing here", "ab") == 0


@pytest.mark.parametrize("newline", ["\n", "\r\n"], ids=["lf", "crlf"])
def test_a_formatter_wrapped_mark_counts_the_same(newline):
    """Implements: TC-422"""
    indent = newline + "\t    "
    wrapped = EXPECTED_FAILURE_MARKER.replace(
        "(strict", "(" + indent + "strict"
    ).replace(", raises", "," + indent + "raises")
    assert wrapped != EXPECTED_FAILURE_MARKER
    assert (
        kef.count(_marked(EXPECTED_FAILURE_MARKER, wrapped), EXPECTED_FAILURE_MARKER)
        == 2
    )


def test_a_param_mark_counts():
    """Implements: TC-422"""
    source = "pytest.param(1, marks={})\n".format(EXPECTED_FAILURE_MARKER).encode(
        "utf-8"
    )
    assert kef.count(source, EXPECTED_FAILURE_MARKER) == 1


def test_a_file_that_is_not_utf8_counts_as_bytes():
    """Implements: TC-422"""
    assert (
        kef.count(
            b"\xff\xfe" + _marked(EXPECTED_FAILURE_MARKER) + b"\xc3",
            EXPECTED_FAILURE_MARKER,
        )
        == 1
    )


@env_gate_skipif("git")
def test_tree_counts_read_the_tests_root_and_leave_a_link_out(tmp_path):
    """Implements: TC-422"""
    repo = _git_repo(tmp_path / "repo")
    marked = _marked(EXPECTED_FAILURE_MARKER)
    write_lf(repo, "tests/test_a.py", marked.decode("utf-8"))
    write_lf(repo, "tests/test_b.py", "plain\n")
    write_lf(
        repo,
        "tests/sub/test_c.py",
        _marked(EXPECTED_FAILURE_MARKER, EXPECTED_FAILURE_MARKER).decode("utf-8"),
    )
    write_lf(repo, "elsewhere/test_d.py", marked.decode("utf-8"))
    _git(repo, "add", "-A")
    blob = _git(repo, "rev-parse", ":tests/test_a.py")
    _git(repo, "commit", "-qm", "seed")
    link = "120000,{},tests/link.py".format(blob)
    module = "160000,{},tests/module".format(_git(repo, "rev-parse", "HEAD"))
    _git(repo, "update-index", "--add", "--cacheinfo", link)
    _git(repo, "update-index", "--add", "--cacheinfo", module)
    tree = _git(repo, "write-tree")
    assert kef.tree_counts(repo, tree, "tests/", EXPECTED_FAILURE_MARKER) == {
        "tests/sub/test_c.py": 2,
        "tests/test_a.py": 1,
        "tests/test_b.py": 0,
    }


@env_gate_skipif("git")
def test_a_tests_root_of_dot_counts_only_the_files_the_review_set_reads(tmp_path):
    """Implements: TC-422"""
    repo = _git_repo(tmp_path / "repo")
    _declare(repo, "[paths]\ntests = .\n" + _marker(EXPECTED_FAILURE_MARKER))
    quoted = _marked(EXPECTED_FAILURE_MARKER).decode("utf-8")
    write_lf(repo, "README.md", quoted)
    write_lf(repo, "notes.txt", quoted)
    write_lf(repo, ".claude/skills/test_copy.py", quoted)
    write_lf(repo, "pkg/__pycache__/test_cached.py", quoted)
    write_lf(repo, "test_plain.py", "def test_plain():\n    assert True\n")
    _git(repo, "add", "-A")
    assert kef.read_commit_check_settings(repo).tests_prefix == ""
    assert kef.landing_refusal(repo) is None
    write_lf(repo, "test_failing.py", quoted)
    _git(repo, "add", "-A")
    tree = _git(repo, "write-tree")
    counts = kef.tree_counts(repo, tree, "", EXPECTED_FAILURE_MARKER)
    assert counts == {"test_plain.py": 0, "test_failing.py": 1}
    refusal = kef.landing_refusal(repo)
    assert "test_failing.py: 1 marked" in refusal
    assert "stack.ini" not in refusal.split(":\n", 1)[1]


@pytest.mark.parametrize(
    "paths, prefix",
    [("[paths]\ntests = checks/\n", "checks/"), ("", "tests/")],
    ids=["declared", "default"],
)
def test_the_tests_root_resolves_as_the_review_set_resolves_it(tmp_path, paths, prefix):
    """Implements: TC-422"""
    _declare(tmp_path, paths + _marker("mark(here)"))
    resolved = load_script("review_set")._roots(tmp_path)[1]
    assert kef.read_commit_check_settings(tmp_path).tests_prefix == kspine.root_prefix(
        resolved
    )
    assert kspine.root_prefix(resolved) == prefix


@env_gate_skipif("git")
def test_this_repos_tests_root_holds_no_mark():
    """Implements: TC-422"""
    settings = kef.read_commit_check_settings(REPO)
    assert settings.marker, "this repository declares no mark"
    listed = _git(REPO, "ls-files", "-z", "--", settings.tests_prefix).split("\0")
    counts = {
        path: kef.count((REPO / path).read_bytes(), settings.marker)
        for path in listed
        if path and (REPO / path).is_file()
    }
    assert {path: n for path, n in counts.items() if n} == {}


# --- the table ----------------------------------------------------------------


def _joined(before, after, tests, digest):
    return "\n".join(kef.findings(before, after, tests, digest))


@pytest.mark.parametrize("n", [0, 2], ids=["0=0", "2=2"])
def test_an_equal_count_is_not_judged(n):
    """Implements: TC-423"""
    assert kef.findings({P: n}, {P: n}, [], None) == []


@pytest.mark.parametrize("before", [{P: 1}, {}], ids=["added", "new-file"])
def test_a_raised_count_passes_when_the_set_names_the_file(before):
    """Implements: TC-423"""
    assert kef.findings(before, {P: 2}, [P], None) == []


def test_a_raised_count_unnamed_is_refused_naming_the_file():
    """Implements: TC-423"""
    assert P in _joined({P: 0}, {P: 1}, [OTHER], None)


def test_a_lowered_count_passes_on_a_matching_record():
    """Implements: TC-423"""
    digest = kv.tests_digest([P])
    assert kef.findings({P: 2}, {P: 0}, [P], digest) == []
    assert kef.findings({P: 2}, {P: 1}, [P], digest) == []


@pytest.mark.parametrize(
    "tests, digest, condition",
    [
        ([P], None, "no commit record"),
        ([P], kv.tests_digest([OTHER]), "another test set"),
        ([OTHER], kv.tests_digest([OTHER]), "does not name"),
    ],
    ids=["no-record", "another-set", "set-not-naming-it"],
)
def test_a_lowered_count_refuses_naming_the_condition(tests, digest, condition):
    """Implements: TC-423"""
    refusal = _joined({P: 1}, {P: 0}, tests, digest)
    assert P in refusal
    assert condition in refusal


@pytest.mark.parametrize("after", [{}, {Q: 0}], ids=["deleted", "renamed-away"])
def test_a_file_gone_from_the_staged_tree_is_not_judged(after):
    """Implements: TC-423"""
    assert kef.findings({P: 1}, after, [], None) == []


def test_a_rename_is_a_deletion_plus_an_addition():
    """Implements: TC-423"""
    assert kef.findings({P: 1}, {Q: 1}, [Q], None) == []
    refusal = _joined({P: 1}, {Q: 1}, [P], None)
    assert Q in refusal
    assert P not in refusal


@pytest.mark.parametrize(
    "entry",
    [P + "::test_it", "tests", "tests/"],
    ids=["node-id", "directory", "directory-slash"],
)
def test_a_node_id_or_a_directory_does_not_name_the_file(entry):
    """Implements: TC-423"""
    assert P in _joined({P: 0}, {P: 1}, [entry], None)


@pytest.mark.parametrize(
    "entry", ["./" + P, P.replace("/", "\\")], ids=["dot-slash", "backslash"]
)
def test_a_spelling_of_the_set_still_names_the_file(entry):
    """Implements: TC-423"""
    assert kef.findings({P: 0}, {P: 1}, [entry], None) == []


def test_each_refused_file_is_named_in_one_refusal():
    """Implements: TC-423"""
    refusal = _joined({P: 0, Q: 2}, {P: 1, Q: 1}, [OTHER], None)
    assert P in refusal and "0 -> 1" in refusal
    assert Q in refusal and "2 -> 1" in refusal


@env_gate_skipif("git")
def test_an_unread_tree_refuses_naming_the_read(tmp_path):
    """Implements: TC-423"""
    repo = _git_repo(tmp_path / "repo")
    _declare(repo, _marker("mark(here)"))
    write_lf(repo, "tests/test_a.py", "plain\n")
    _git(repo, "add", "-A")
    blob = _git(repo, "rev-parse", ":tests/test_a.py")
    loose = repo / ".git" / "objects" / blob[:2] / blob[2:]
    os.chmod(loose, stat.S_IWRITE)
    loose.unlink()
    assert "cannot read the staged tree" in kef.landing_refusal(repo)
