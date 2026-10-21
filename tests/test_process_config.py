"""`docs/process.toml` — the one policy home, and every reader of it agreeing.

SN-028 folded ~10 one-word policy files into one TOML. That is a consolidation
with a sharp edge, and this module is the edge's guard: the git hooks and the
Python checkers both act on this file, and every shape only ONE of them
understands is a silent flip of a security gate.

The first cut of this consolidation shipped without this test and had exactly
that defect in five shapes, driven: a trailing comment (`privacy_check = true
# note`), a dotted key, an inline table, an uppercase `TRUE`, and a BOM each
made the hook and Python disagree — three of them fail-OPEN, i.e. a repo that
had declared the privacy gate committing with it silently off.

So the contract has three parts and all three are driven here:

  1. **The file's SHAPE is checked, not assumed** — `process_shape_findings`
     refuses dotted keys, inline tables, multi-line strings, and a hook-read
     key under the wrong section.
  2. **The shipped hook and the checker AGREE** over a table of adversarial
     files, the table the review found the bugs with, driven through the real
     pre-push hook rather than a function extracted from it.
  3. **The hooks refuse what they cannot read** — an unreadable or
     unparseable file, a mixed config, and a policy answer that fails or
     falls outside its set — and they read it once, after the interpreter
     probe.

Plus the migration's own guarantees: a mixed config is refused rather than
resolved, a wrong-typed dial is refused rather than defaulted, and the
converter never deletes a legacy file whose value it did not manage to write.
"""

import os
import shutil
import subprocess
import tomllib

import pytest
from conftest import (
    KIT,
    ROOT,
    load_script,
    pin_autocrlf,
    python_stand_ins,
    skip_without_env_gates,
)

ac = load_script("agent_common")
bootstrap = load_script("bootstrap")
check_privacy = load_script("check_privacy")


def test_declared_policy_surface_is_reexported_from_its_behavior_module():
    policy = load_script("agent_policy")
    for name in ("process_config", "config_conflicts", "human_holds"):
        exported = getattr(ac, name)
        owned = getattr(policy, name)
        assert exported.__module__ == "agent_policy"
        assert exported.__code__.co_code == owned.__code__.co_code


# The three shipped git hooks; each sources the probe shipped beside it.
SHIPPED_HOOKS = ("pre-commit", "commit-msg", "pre-push")
# The deterministic lint identity and the noreply author test_pre_push_hook uses.
FAKE_USER = "privacyprobeuser"
NOREPLY = "12345+t@users.noreply.github.com"
ZERO = "0" * 40


def write_toml(root, text):
    (root / "docs").mkdir(parents=True, exist_ok=True)
    with (root / "docs" / "process.toml").open(
        "w", encoding="utf-8", newline="\n"
    ) as fh:
        fh.write(text)


def _git(root, *args):
    return subprocess.run(["git", *args], cwd=str(root), capture_output=True, text=True)


def _sh_path(path):
    """`path` as the POSIX shell spells it when absolute (`/c/...` under Git
    Bash), asked of the shell itself, so a hook's absolute-path test sees it."""
    proc = subprocess.run(
        [shutil.which("sh"), "-c", 'cd "$1" && pwd', "sh", str(path)],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    return proc.stdout.strip()


def hook_repo(tmp_path):
    """A minimal git repo holding the shipped hooks and their probe, copied
    byte-for-byte from the kit, with one commit by the noreply identity.
    Returns its root (`tmp_path / "repo"`)."""
    skip_without_env_gates("posix-shell", "git")
    root = tmp_path / "repo"
    (root / ".githooks").mkdir(parents=True)
    for name in SHIPPED_HOOKS + ("kit-python.sh",):
        shutil.copyfile(KIT / "hooks" / name, root / ".githooks" / name)
    assert _git(root, "init").returncode == 0
    pin_autocrlf(root)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(root, "config", "user.name", "Test User")
    _git(root, "config", "user.email", NOREPLY)
    _git(root, "config", "core.hooksPath", ".git/hooks")
    (root / "a.txt").write_text("clean base\n", encoding="utf-8")
    assert _git(root, "add", "a.txt").returncode == 0
    proc = _git(root, "commit", "-m", "base")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return root


def run_shipped_hook(root, hook, scripts_dir=None, path_prefix=None):
    """Run one shipped hook in `root` the way git does: pre-push with the
    remote on argv and HEAD's push line (against the zero sha) on stdin,
    commit-msg with a message file, pre-commit bare. KIT_SCRIPTS_DIR names
    `scripts_dir` (the kit's own scripts by default), absolute; `path_prefix`
    goes first on PATH. No reviewer is wired."""
    env = dict(os.environ)
    for var in ("LOGNAME", "USER", "LNAME", "USERNAME"):
        env[var] = FAKE_USER
    env.pop("REVIEW_CMD", None)
    env["KIT_SCRIPTS_DIR"] = _sh_path(scripts_dir or KIT / "scripts")
    if path_prefix is not None:
        env["PATH"] = str(path_prefix) + os.pathsep + env.get("PATH", "")
    args, stdin = [], ""
    if hook == "pre-push":
        head = _git(root, "rev-parse", "HEAD").stdout.strip()
        args = ["origin", "https://example.invalid/repo.git"]
        stdin = "refs/heads/main {} refs/heads/main {}\n".format(head, ZERO)
    elif hook == "commit-msg":
        (root / "MSG.txt").write_text("an innocent message\n", encoding="utf-8")
        args = ["MSG.txt"]
    return subprocess.run(
        [shutil.which("sh"), ".githooks/" + hook, *args],
        cwd=str(root),
        input=stdin,
        capture_output=True,
        text=True,
        env=env,
    )


def hook_privacy_answer(root):
    """The SHIPPED pre-push hook's privacy answer, driven whole: `off` when the
    push passes with no review demanded, `on` when it fails closed for the
    unwired reviewer, `refused:<stderr>` for any other refusal.

    The real hook, never a function extracted from it: a guard that carries
    its own copy of the thing under test can only ever agree with itself, and
    an extracted copy once went stale while the shipped reader failed OPEN on
    a trailing-comment decoy."""
    proc = run_shipped_hook(root, "pre-push")
    if proc.returncode == 0 and "FAILING CLOSED" not in proc.stderr:
        return "off"
    if proc.returncode != 0 and "FAILING CLOSED" in proc.stderr:
        return "on"
    return "refused:" + proc.stderr


# The adversarial table. Each row: (label, file text, what tomllib means).
# Every one of these was a real disagreement in the first cut, or is the
# control that proves the fix did not over-correct.
SHAPES = [
    ("plain-true", "[policies]\nprivacy_check = true\n", True),
    ("plain-false", "[policies]\nprivacy_check = false\n", False),
    ("no-spaces", "[policies]\nprivacy_check=true\n", True),
    ("tabs", "[policies]\nprivacy_check\t=\ttrue\n", True),
    ("leading-space", "[policies]\n  privacy_check = true\n", True),
    ("trailing-comment-true", "[policies]\nprivacy_check = true  # on\n", True),
    ("trailing-comment-false", "[policies]\nprivacy_check = false  # off\n", False),
    # THE DECOY PAIR — the shape the FINAL review found failing OPEN.
    # `privacy_check = true # privacy_check = false` is legal TOML whose value
    # is `true`; a hook text read that matched the decoy INSIDE the comment
    # switched the gate off while Python read it ON. The hook is what blocks
    # the commit, so the hook's answer is the one that decides — this was the
    # M-42 contract inverted.
    (
        "decoy-false-in-comment",
        "[policies]\nprivacy_check = true # privacy_check = false\n",
        True,
    ),
    (
        "decoy-true-in-comment",
        "[policies]\nprivacy_check = false # privacy_check = true\n",
        False,
    ),
    # A `#` inside a legal string value.
    (
        "hash-inside-a-string",
        '[policies]\nprivacy_review = "a#b"\nprivacy_check = true\n',
        True,
    ),
    # A key mentioned ONLY in a trailing comment declares nothing — which is
    # what `tomllib` says, so no reader may fail closed on a decoy here.
    (
        "key-only-in-a-comment",
        "[policies]\nsecrets_scan = true # privacy_check = true\n",
        None,
    ),
    ("crlf", "[policies]\r\nprivacy_check = true\r\n", True),
    ("bom", "﻿[policies]\nprivacy_check = true\n", True),
    (
        "commented-decoy",
        "[policies]\n# privacy_check = true\nsecrets_scan = true\n",
        None,
    ),
    ("similar-key", "[policies]\nx_privacy_check = true\n", None),
    ("absent", "[policies]\nsecrets_scan = true\n", None),
]

# The shapes the shape check refuses, each in a true and a false variant. A
# key the parser does not place under [policies] (a multi-line string, the
# wrong section) reads ON whatever its text says: fail closed.
NON_GREPPABLE = [
    ("dotted-key-true", "policies.privacy_check = true\n", True),
    ("dotted-key-false", "policies.privacy_check = false\n", False),
    ("inline-table-true", "policies = { privacy_check = true }\n", True),
    ("inline-table-false", "policies = { privacy_check = false }\n", False),
    (
        "multiline-string-true",
        '[policies]\nnote = """\nprivacy_check = true\n"""\n',
        True,
    ),
    (
        "multiline-string-false",
        '[policies]\nnote = """\nprivacy_check = false\n"""\n',
        True,
    ),
    ("wrong-section-true", "[attestation]\nprivacy_check = true\n", True),
    ("wrong-section-false", "[attestation]\nprivacy_check = false\n", True),
]

# A dial that is not the boolean `false` reads ON.
WRONG_TYPE = [
    ("wrong-type-string", '[policies]\nprivacy_check = "false"\n', True),
    ("wrong-type-int", "[policies]\nprivacy_check = 0\n", True),
]


def _d4_rows():
    """The D4 table: (label, process.toml text or None, expected, legacy
    docs/privacy-check text or None). `expected is None` means the file
    declares nothing, so every reader falls through to the (absent) legacy
    file."""
    rows = [(label, text, exp, None) for label, text, exp in SHAPES]
    rows += [(label, text, exp, None) for label, text, exp in NON_GREPPABLE]
    rows += [(label, text, exp, None) for label, text, exp in WRONG_TYPE]
    # The legacy arm with no TOML at all (the dual-read window).
    rows.append(("legacy-only-true", None, True, "# header\ntrue\n"))
    # The legacy word in any case reads ON in the checker, so the hook must
    # read it ON too: an exact lowercase match once let it push unreviewed.
    rows.append(("legacy-only-uppercase", None, True, "# header\nTRUE\n"))
    return rows


D4_ROWS = _d4_rows()


def _write_d4_row(root, text, legacy):
    if text is not None:
        write_toml(root, text)
    if legacy is not None:
        (_docs(root) / "privacy-check").write_text(legacy, encoding="utf-8")


@pytest.mark.parametrize(
    "label,text,expected,legacy",
    [
        pytest.param(
            *row,
            id=row[0],
        )
        for row in D4_ROWS
    ],
)
def test_the_shipped_hook_and_the_checker_agree_on_every_shape(
    tmp_path, label, text, expected, legacy
):
    """TC-031 (SR-031: one parse, one answer). THE cross-reader pin: the real
    pre-push hook's privacy answer equals `check_privacy.read_privacy_enabled`
    on every row, and the `expected` column where given.

    The `multiline-string-false` and `wrong-section-false` rows catch a hook
    that reads OFF from text the parser does not place under [policies]
    (a fail-open divergence). Adequacy witness for the rest: a hook that matched
    the decoy inside a trailing comment fails `decoy-false-in-comment`, one
    that missed a BOM-prefixed or CRLF section header fails `bom` or `crlf`,
    and one that read only a typed `true` fails `wrong-type-string`."""
    root = hook_repo(tmp_path)
    _write_d4_row(root, text, legacy)
    python = "on" if check_privacy.read_privacy_enabled(root) else "off"
    hook = hook_privacy_answer(root)
    assert hook == python, "{}: hook={} python={}".format(label, hook, python)
    if expected is not None:
        assert hook == ("on" if expected else "off"), label


# Present but unreadable or unparseable: the hooks refuse, naming the file
# (fail closed; never read as a default).
UNREADABLE = [
    ("malformed", "[policies\nprivacy_check = true\n"),
    ("uppercase-TRUE", "[policies]\nprivacy_check = TRUE\n"),
    ("bare-word", "[policies]\nprivacy_check = yes\n"),
    ("undecodable", b"\xff\xfe[policies]\n"),
    ("directory", None),
]


def write_unreadable(root, content):
    """`docs/process.toml` as one UNREADABLE case: TOML text that does not
    parse, bytes that do not decode, or (None) a directory at the path."""
    path = _docs(root) / "process.toml"
    if content is None:
        path.mkdir()
    elif isinstance(content, bytes):
        path.write_bytes(content)
    else:
        write_toml(root, content)


def _parser_message(text):
    try:
        tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        return str(exc)
    raise AssertionError("expected an unparseable file: {!r}".format(text))


@pytest.mark.parametrize(
    "hook,case,content",
    [
        pytest.param(hook, case, content, id="{}-{}".format(hook, case))
        for hook in SHIPPED_HOOKS
        for case, content in UNREADABLE
    ],
)
def test_every_hook_refuses_an_unreadable_policy_file(tmp_path, hook, case, content):
    """TC-021, TC-031: a present but unreadable or unparseable
    `docs/process.toml` refuses the commit or push at every hook, naming the
    file, and for a parse error carrying the parser's message; it never
    reads as a default and never reaches the reviewer check."""
    root = hook_repo(tmp_path)
    write_unreadable(root, content)
    proc = run_shipped_hook(root, hook)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "docs/process.toml" in proc.stderr, proc.stderr
    assert "cannot be read or parsed" in proc.stderr, proc.stderr
    assert "FAILING CLOSED" not in proc.stderr, proc.stderr
    if case == "malformed":
        assert _parser_message(content) in proc.stderr, proc.stderr


def _write_mixed(root):
    write_toml(root, "[policies]\nprivacy_check = false\n")
    (root / "docs" / "privacy-check").write_text("true\n", encoding="utf-8")


def test_every_hook_refuses_a_mixed_config_with_one_text(tmp_path):
    """TC-021, TC-031: `[policies] privacy_check` and the legacy
    `docs/privacy-check` both present refuse at all three hooks, naming both
    files and the migrator, in one text once the hook's name is removed."""
    root = hook_repo(tmp_path)
    _write_mixed(root)
    texts = {}
    for hook in SHIPPED_HOOKS:
        proc = run_shipped_hook(root, hook)
        assert proc.returncode != 0, (hook, proc.stdout + proc.stderr)
        for needle in ("docs/process.toml", "docs/privacy-check", "--migrate-config"):
            assert needle in proc.stderr, (hook, proc.stderr)
        texts[hook] = proc.stderr.replace(hook, "<hook>")
    assert len(set(texts.values())) == 1, texts


# Stand-ins for the kit's privacy checker whose policy answer fails or falls
# outside the closed token set.
POLICY_STUBS = [
    ("exits-3", "import sys\nsys.exit(3)\n"),
    ("foreign-token", 'import sys\nsys.stdout.write("privacy=maybe")\n'),
    ("silent", ""),
    ("carriage-return", 'import sys\nsys.stdout.buffer.write(b"privacy=off\\r")\n'),
]


@pytest.mark.parametrize(
    "hook,stub",
    [
        pytest.param(hook, body, id="{}-{}".format(hook, label))
        for hook in SHIPPED_HOOKS
        for label, body in POLICY_STUBS
    ],
)
def test_every_hook_refuses_a_failed_or_foreign_policy_answer(tmp_path, hook, stub):
    """TC-021: a policy read that exits nonzero, prints nothing, or prints
    anything outside its tokens (a near-token with a stray carriage return
    included) refuses the commit or push, naming the read."""
    root = hook_repo(tmp_path)
    stub_dir = tmp_path / "stub_scripts"
    stub_dir.mkdir()
    (stub_dir / "check_privacy.py").write_text(stub, encoding="utf-8")
    proc = run_shipped_hook(root, hook, scripts_dir=stub_dir)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "check_privacy.py" in proc.stderr, proc.stderr
    assert "--hook-policy" in proc.stderr, proc.stderr


@pytest.mark.parametrize("hook", SHIPPED_HOOKS)
def test_the_mixed_refusal_runs_after_the_interpreter_probe(tmp_path, hook):
    """TC-021: with a mixed config and no runnable Python on PATH, each hook
    refuses for the interpreter, naming dev-setup's install and the 3.11
    floor, and never reaches the mixed-config refusal (the policy is read
    once, after the probe)."""
    root = hook_repo(tmp_path)
    _write_mixed(root)
    proc = run_shipped_hook(root, hook, path_prefix=python_stand_ins(tmp_path))
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "dev-setup" in proc.stderr and "3.11" in proc.stderr, proc.stderr
    assert "--migrate-config" not in proc.stderr, proc.stderr


def _hook_answer(root):
    """The checker's one policy answer for the hooks, or a marker string the
    assertion names when the checker has no such answer yet."""
    answer = getattr(check_privacy, "hook_policy_answer", None)
    return (
        "<no hook_policy_answer in check_privacy>" if answer is None else answer(root)
    )


@pytest.mark.parametrize(
    "label,text,legacy,content",
    [pytest.param(r[0], r[1], r[3], None, id="shape-" + r[0]) for r in D4_ROWS]
    + [
        pytest.param(case, None, None, content, id="unreadable-" + case)
        for case, content in UNREADABLE
    ],
)
def test_the_hook_answer_and_the_checker_agree_in_process(
    tmp_path, label, text, legacy, content
):
    """TC-031: the in-process pin of the D4 table. The checker's hook answer
    is `privacy=on review=require` exactly where `read_privacy_enabled` reads
    ON (no row wires the review opt-down), `privacy=off` where it reads OFF,
    and `refuse=unreadable` for every unreadable case."""
    if label in dict(UNREADABLE):
        write_unreadable(tmp_path, content)
        want = "refuse=unreadable"
    else:
        _write_d4_row(tmp_path, text, legacy)
        on = check_privacy.read_privacy_enabled(tmp_path)
        want = "privacy=on review=require" if on else "privacy=off"
    assert _hook_answer(tmp_path) == want, label


NON_GREPPABLE_ON = [row[:2] for row in NON_GREPPABLE if row[0].endswith("-true")]


@pytest.mark.parametrize(
    "label,text", NON_GREPPABLE_ON, ids=[s[0] for s in NON_GREPPABLE_ON]
)
def test_a_shape_the_hooks_cannot_follow_is_refused_by_the_shape_check(
    tmp_path, label, text
):
    """The shapes the two readers once disagreed on are REFUSED by the shape
    check, and, because a refusal is only as good as what happens when
    someone ignores it, they still read ON in the checker."""
    write_toml(tmp_path, text)
    findings = ac.process_shape_findings(tmp_path / "docs")
    assert findings, "{}: must be refused as un-greppable".format(label)
    assert check_privacy.read_privacy_enabled(tmp_path) is True, label


def test_the_shipped_template_and_this_repos_own_file_pass_the_shape_check():
    # The guard is worthless if the two files it exists for do not satisfy it.
    assert ac.process_shape_findings(ROOT / "docs") == []
    assert ac.process_shape_findings(KIT) == [] or not (KIT / "process.toml").exists()


# --- the mixed-config refusal --------------------------------------------------


def test_a_mixed_config_is_refused_by_name(tmp_path):
    write_toml(tmp_path, "[policies]\nprivacy_check = false\n")
    (tmp_path / "docs" / "privacy-check").write_text("true\n", encoding="utf-8")
    refusals = ac.config_conflicts(tmp_path / "docs")
    assert any("declared TWICE" in r and "privacy-check" in r for r in refusals)
    assert any("--migrate-config" in r for r in refusals)


def test_a_mixed_config_reads_ON_in_the_hooks_which_cannot_refuse(tmp_path):
    # The Python layer refuses; the hooks must still decide, and the only safe
    # decision is the gate the adopter asked for somewhere.
    write_toml(tmp_path, "[policies]\nprivacy_check = false\n")
    (tmp_path / "docs" / "privacy-check").write_text("true\n", encoding="utf-8")
    assert check_privacy.read_privacy_enabled(tmp_path) is True


def test_a_wrong_typed_dial_is_refused_not_defaulted(tmp_path):
    # `review_rounds = "2"` is a plausible hand edit — every other value in
    # [policies] is quoted — and it once meant NO review verdict was required.
    write_toml(tmp_path, '[policies]\nreview_rounds = "2"\n')
    refusals = ac.config_conflicts(tmp_path / "docs")
    assert any("review_rounds" in r and "expected int" in r for r in refusals)


def test_a_non_string_trunk_is_refused_by_the_config_check(tmp_path):
    # The trunk reader refuses a bare `trunk = 1` only on the routes that read
    # the trunk; the config check refuses it at every guarded entry point,
    # naming the key and the type, as for every dial.
    write_toml(tmp_path, "[policies]\ntrunk = 1\n")
    refusals = ac.config_conflicts(tmp_path / "docs")
    assert any("trunk" in r and "expected str" in r for r in refusals), refusals


def test_a_clean_config_refuses_nothing(tmp_path):
    shutil.copy(KIT / "process.toml.template", _docs(tmp_path) / "process.toml")
    assert ac.config_conflicts(tmp_path / "docs") == []


def _docs(root):
    d = root / "docs"
    d.mkdir(parents=True, exist_ok=True)
    return d


# --- precedence and the legacy arm ---------------------------------------------


def test_declared_policy_prefers_the_toml_then_the_legacy_file_then_the_default(
    tmp_path,
):
    docs = _docs(tmp_path)
    assert ac.declared_policy(docs, "push-policy", "human") == "human"

    (docs / "push-policy").write_text("# note\nagent\n", encoding="utf-8")
    assert ac.declared_policy(docs, "push-policy", "human") == "agent"

    write_toml(tmp_path, '[policies]\npush = "agent-iteration"\n')
    assert ac.declared_policy(docs, "push-policy", "human") == "agent-iteration"


def test_a_typed_value_renders_in_the_legacy_string_vocabulary(tmp_path):
    # The migration must change no downstream comparison: every consumer still
    # compares strings.
    write_toml(
        tmp_path,
        "[policies]\nreview_rounds = 2\nprivacy_check = true\nsecrets_scan = false\n",
    )
    docs = tmp_path / "docs"
    assert ac.declared_policy(docs, "review-policy", "1") == "2"
    assert ac.declared_policy(docs, "privacy-check", "false") == "true"
    assert ac.declared_policy(docs, "secrets-scan", "on") == "false"


def test_the_legacy_arm_still_works_with_no_toml_at_all(tmp_path):
    # The dual-read window is the whole reason an adopter is not broken by this
    # release; a test that only ever writes the new home would not notice it
    # rotting. The shipped hook's half is the `legacy-only-true` row of the
    # D4 table above.
    docs = _docs(tmp_path)
    (docs / "privacy-check").write_text("# header\ntrue\n", encoding="utf-8")
    assert check_privacy.read_privacy_enabled(tmp_path) is True


# --- the converter --------------------------------------------------------------


def _migrated(tmp_path, legacy):
    shutil.copy(KIT / "process.toml.template", _docs(tmp_path) / "process.toml")
    for name, value in legacy.items():
        (tmp_path / "docs" / name).write_text(value + "\n", encoding="utf-8")
    return bootstrap.migrate_legacy_config(tmp_path)


def test_migration_folds_every_dial_in_and_deletes_the_file(tmp_path):
    moved, notes = _migrated(
        tmp_path,
        {
            "gate-policy": "autonomous",
            "push-policy": "agent",
            "review-policy": "2",
            "privacy-check": "true",
            "secrets-scan": "off",
            "blackout": "09:00-17:00",
        },
    )
    assert len(moved) == 6, moved
    cfg = ac.process_config(tmp_path / "docs")
    # SN-029: `gate-policy` is the one legacy file that is NOT a rename. Its
    # word expands to the THREE dials it always meant — folding it to a single
    # key is what lost two of the three and let a repo scaffold with one
    # posture while running with another.
    # WI-493 re-keyed the dial to the DevStg-* rung it always meant: the
    # loop-held end that used to be the ordinal `0` is now `DevStg-Below`, the
    # sentinel for "no rung is a human's to approve".
    assert cfg["attestation"]["human_approval_through"] == "DevStg-Below"
    assert cfg["attestation"]["keep_nondependent"] is True
    assert cfg["attestation"]["final_review"] == "off"
    assert "gate_policy" not in cfg["attestation"]
    assert ac.approval_through(tmp_path / "docs") == "DevStg-Below"
    assert ac.human_holds(tmp_path / "docs", "DevStg-Needs") is False, (
        "the whole point: `autonomous` must actually read as loop-held"
    )
    assert cfg["policies"] == {
        "push": "agent",
        "review_rounds": 2,
        "privacy_check": True,
        "secrets_scan": False,
        "privacy_review": "require",
        "guardrails": "off",
        "blackout": "09:00-17:00",
        "trunk": "main",
    }
    for name in ("gate-policy", "push-policy", "review-policy", "privacy-check"):
        assert not (tmp_path / "docs" / name).exists(), name
    assert ac.config_conflicts(tmp_path / "docs") == []
    # Idempotent: a second pass has nothing to do.
    assert bootstrap.migrate_legacy_config(tmp_path) == ([], [])


def test_migration_never_deletes_a_file_it_could_not_write(tmp_path):
    """The defect this test exists for: `set_process_key` answered "missing" on
    a hand-trimmed process.toml, the caller deleted the legacy file anyway, and
    a declared `privacy_check = true` vanished under a green `migrated:` line.

    The fix makes the write TOTAL (the key is appended under its section), so
    the honest assertion is that the value SURVIVES — either folded in or left
    on disk — never that it is silently gone."""
    _docs(tmp_path)
    write_toml(tmp_path, '# my customized file\n[policies]\npush = "human"\n')
    (tmp_path / "docs" / "privacy-check").write_text("true\n", encoding="utf-8")
    (tmp_path / "docs" / "review-policy").write_text("2\n", encoding="utf-8")

    bootstrap.migrate_legacy_config(tmp_path)
    cfg = ac.process_config(tmp_path / "docs")
    assert cfg["policies"]["privacy_check"] is True, "a declared gate was DROPPED"
    assert cfg["policies"]["review_rounds"] == 2
    assert check_privacy.read_privacy_enabled(tmp_path) is True


def test_migration_leaves_an_unparseable_value_in_place(tmp_path):
    moved, notes = _migrated(tmp_path, {"review-policy": "sometimes"})
    assert moved == []
    assert any("not a valid value" in n for n in notes)
    assert (tmp_path / "docs" / "review-policy").is_file()


def test_dry_run_mutates_nothing(tmp_path):
    shutil.copy(KIT / "process.toml.template", _docs(tmp_path) / "process.toml")
    (tmp_path / "docs" / "privacy-check").write_text("true\n", encoding="utf-8")
    before = (tmp_path / "docs" / "process.toml").read_bytes()

    moved, _notes = bootstrap.migrate_legacy_config(tmp_path, dry_run=True)
    assert moved == ["docs/privacy-check"]
    assert (tmp_path / "docs" / "privacy-check").is_file()
    assert (tmp_path / "docs" / "process.toml").read_bytes() == before


def test_migration_notes_a_discarded_comment_header(tmp_path):
    _moved, notes = _migrated(tmp_path, {"push-policy": "# my own note\nagent"})
    assert any("comment lines" in n for n in notes)


def test_set_process_key_reports_three_states(tmp_path):
    shutil.copy(KIT / "process.toml.template", _docs(tmp_path) / "process.toml")
    assert bootstrap.set_process_key(tmp_path, "policies", "push", "agent") == "set"
    assert bootstrap.set_process_key(tmp_path, "policies", "push", "agent") == "same"
    assert bootstrap.set_process_key(tmp_path, "policies", "nope", 1) == "missing"
    assert (
        bootstrap.set_process_key(tmp_path, "policies", "nope", 1, add_if_missing=True)
        == "set"
    )
    assert ac.process_config(tmp_path / "docs")["policies"]["nope"] == 1
