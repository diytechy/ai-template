"""The old shell read and the new config query decide alike (SR-139, TC-153 part 1).

The staging this module was written for is now history, and the history is the
point: P2 built the reader and switched **no runtime caller**; P13 performed the
cutover in one reviewed change. The reason for that order was **driven**, not
procedural — wiring the hooks to the query in the same slice that built it made
every hook read a canonical key that no repo had set yet, so a tree carrying only
`docs/privacy-check = true` lost its privacy gate and `pre-push` exited 0 on a
reviewer `BLOCK`. Fourteen shipped hook tests caught it. A security floor is
exactly the wrong place to land a reader and its cutover in one step, because the
failure mode is silence.

What this module proves is the **agreement bar**: the literal retired pipeline
and the new entry point, driven over one matrix of declared values, reach the
same verdict. Agreement is what makes the cutover a no-op for behaviour rather
than a policy change smuggled in as a refactor — and it stays green after the
cutover because the retired files are still in the tree (P14 deletes them),
which is exactly what keeps the cutover revertible.

TC-153's remaining permutations — each hook blocking when the query refuses, and
the unconverted repo that caused the incident — are discharged in
`tests/test_config_cutover.py`, where the call sites now exist to drive.
"""

import shutil
import subprocess

import pytest
from conftest import KIT, SCRIPTS, env_gate_skipif, run_py

pytestmark = env_gate_skipif("posix-shell", "git")

HOOKS = ("pre-commit", "commit-msg", "pre-push")

# The retired parse, verbatim: the first non-comment, non-blank line with all
# whitespace removed. This is the pipeline the hooks carry TODAY, quoted here so
# the agreement bar drives the real thing rather than a Python re-implementation
# of it (a re-implementation would agree with itself, which proves nothing).
LEGACY_PIPELINE = (
    "grep -v '^[[:space:]]*#' \"$1\" | grep -v '^[[:space:]]*$' | "
    "head -n 1 | tr -d '[:space:]'"
)

CONFIG_SCRIPTS = ("config.py", "config_query.py", "config_migrate.py")

# Each retired security file, its canonical key, the RETIRED readers that decide
# whether THE GATE IS LIVE, the same question asked of the new answer, and the
# declared values to drive. The verdict is what is compared, never the raw
# string: the readers legitimately differ in representation (`off` vs `false`,
# absent vs defaulted) and may never differ in effect. Note the two OPT-DOWN
# idioms, where absence is the STRICT answer: `secrets-scan` scans unless the
# file says `off`, and `privacy-review` blocks unless the file says
# `warn-unwired`. Getting either backwards is a fail-open.
#
# The retired side is a LIST of NAMED readers, not one predicate, because a
# retired file can have more than one reader and for `docs/privacy-check` the two
# disagree TODAY — the shell hooks compare `[ "$p" = "true" ]` while
# `check_privacy.read_privacy_enabled` lowercases first. One predicate would have
# to misquote a real reader, and the first draft did exactly that in the other
# direction: it modelled `docs/secrets-scan` as `raw != "off"` when its only
# production reader is `raw.lower() != "off"`. That is a booby trap rather than a
# rounding error — it makes `OFF` read as a converter bug when the converter is
# the side that matches production.
#
# `privacy-review` was missing from the first draft of the contracts doc — the
# retired list named `docs/critique-policy`, which does not exist in this kit,
# and omitted the file `pre-push` actually parses. Driving the hooks found it.
SECURITY_KEYS = (
    (
        "privacy-check",
        "policy.privacy_check",
        (
            # hooks/pre-commit, commit-msg, pre-push: `[ "$p" = "true" ]`.
            ("the git hooks", lambda raw: raw == "true"),
            # check_privacy.py read_privacy_enabled: `(...).lower() == "true"`.
            ("check_privacy.read_privacy_enabled", lambda raw: raw.lower() == "true"),
        ),
        lambda ans: ans == "true",
        (
            "true",
            "TRUE",
            "True",
            "false",
            "# only a comment",
            "\n\n#c\n  true  ",
            None,
        ),
    ),
    (
        "secrets-scan",
        "policy.secrets_scan",
        # check_privacy.py read_secrets_scan is the only reader: no hook parses
        # this file; pre-push defers the whole floor to the script.
        (("check_privacy.read_secrets_scan", lambda raw: raw.lower() != "off"),),
        lambda ans: ans == "true",
        ("off", "OFF", "Off", "on", "# only a comment", "\n\n#c\n  off  ", None),
    ),
    (
        "privacy-review",
        "policy.privacy_review",
        # hooks/pre-push is the only reader: `[ "$review_policy" = "warn-unwired" ]`,
        # case-sensitive, so any other spelling reads as require (the strict side).
        (("hooks/pre-push", lambda raw: raw != "warn-unwired"),),
        lambda ans: ans != "warn-unwired",
        (
            "warn-unwired",
            "WARN-UNWIRED",
            "Warn-Unwired",
            "require",
            "# only a comment",
            "\n\n#c\n  warn-unwired  ",
            None,
        ),
    ),
)

# Declared values on which one file's retired readers disagree WITH EACH OTHER,
# so "the retired verdict" is not a single fact and there is nothing for the
# cutover to preserve. Enumerated rather than tolerated: each entry is a case a
# reader can check, and a NEW split — one an edit to the hooks or to
# check_privacy introduces — has nowhere to hide.
#
# Both entries are the same case: `docs/privacy-check` spelled with any capital.
# The git hooks read it as OFF, check_privacy reads it as ON. `config_migrate`'s
# `true-exact` coercion answers this by REPORTING the value and writing nothing,
# so the canonical key stays unset and resolves to its schema default — a policy
# the adopter is told to choose rather than one the converter picked for them.
# That refusal is the property asserted below; agreement is not available here.
SPLIT_RETIRED_READERS = frozenset(
    {("privacy-check", "TRUE"), ("privacy-check", "True")}
)


@pytest.fixture(scope="module")
def _hook_tree(tmp_path_factory):
    """A minimal repo carrying the hooks and the reader they will call at P13.

    Built once per module: `git init` plus the file copies is the expensive part
    and nothing here is what the tests mutate.
    """
    root = tmp_path_factory.mktemp("hooktree")
    (root / "scripts").mkdir()
    hooks = root / ".githooks"
    hooks.mkdir()
    for name in HOOKS:
        dst = hooks / name
        shutil.copyfile(KIT / "hooks" / name, dst)
        dst.chmod(dst.stat().st_mode | 0o111)
    (root / "docs").mkdir()
    subprocess.run(["git", "init"], cwd=str(root), capture_output=True, text=True)
    return root


@pytest.fixture
def tree(_hook_tree):
    """The shared tree with the mutable parts reset."""
    for name in CONFIG_SCRIPTS:
        shutil.copyfile(SCRIPTS / name, _hook_tree / "scripts" / name)
    for stale in _hook_tree.joinpath("docs").iterdir():
        if stale.is_file():
            stale.unlink()
    return _hook_tree


def _legacy_value(root, name):
    """What the retired shell pipeline reads out of `docs/<name>` — run through a
    real `sh`, not re-implemented.

    An absent file reads as the empty string, which is what every production
    reader sees: the hooks initialise `privacy=""` before the `-f` test, and
    check_privacy's readers spell it `(_first_declared_line(...) or "")`.
    """
    path = root / "docs" / name
    if not path.exists():
        return ""
    proc = subprocess.run(
        [shutil.which("sh"), "-c", LEGACY_PIPELINE, "sh", str(path)],
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip()


def _query(root, key):
    """What the new entry point answers for one canonical key."""
    proc = run_py(
        [root / "scripts" / "config_query.py", "--root", str(root), key], cwd=root
    )
    return proc


# --- the agreement bar --------------------------------------------------------
def _agreement_cases():
    for legacy_name, key, old_readers, new_live, declared_values in SECURITY_KEYS:
        for declared in declared_values:
            yield pytest.param(
                legacy_name,
                key,
                old_readers,
                new_live,
                declared,
                id="{}-{}".format(
                    legacy_name, "absent" if declared is None else repr(declared)
                ),
            )


@pytest.mark.parametrize(
    "legacy_name,key,old_readers,new_live,declared", list(_agreement_cases())
)
def test_old_shell_read_and_new_query_decide_alike(
    tree, legacy_name, key, old_readers, new_live, declared
):
    """One declared value, every reader of it, one verdict.

    The verdict compared is the SECURITY question the hook asks — "is this gate
    live?" — not the raw string, because the readers legitimately differ in
    representation and may never differ in effect.

    Where the retired readers of one file disagree with each other there is no
    old verdict to preserve, so the bar changes shape: the case must be declared
    in `SPLIT_RETIRED_READERS`, the converter must REFUSE it out loud and leave
    the canonical key unset, and — SINCE THE P13 CUTOVER — the query must refuse
    it too rather than answering the schema default. That last clause is the
    cutover's own strengthening: before it, "the adopter is told to choose" left
    the loop quietly obeying a default in the meantime; now an unconverted repo
    cannot commit until the choice is made. A converter that quietly picked a
    side would hand the repo a security policy nobody chose, in whichever
    direction it happened to prefer — the failure this module exists to make
    impossible.
    """
    if declared is not None:
        (tree / "docs" / legacy_name).write_text(
            declared if declared.endswith("\n") else declared + "\n",
            encoding="utf-8",
            newline="\n",
        )

    raw = _legacy_value(tree, legacy_name)
    was_live = {name: predicate(raw) for name, predicate in old_readers}

    convert = run_py(
        [tree / "scripts" / "config_migrate.py", "--root", str(tree), "--write"],
        cwd=tree,
    )
    assert convert.returncode == 0, convert.stdout + convert.stderr

    got = _query(tree, key)

    verdicts = set(was_live.values())
    if len(verdicts) > 1:
        assert (legacy_name, declared) in SPLIT_RETIRED_READERS, (
            "{}: the retired readers of docs/{} disagree about {!r} ({}) and "
            "nothing declares the split. Add the case to SPLIT_RETIRED_READERS "
            "with the reason, or fix the reader that is wrong."
        ).format(legacy_name, legacy_name, declared, was_live)
        told = convert.stdout + convert.stderr
        assert "NOT CONVERTED" in told and legacy_name in told, (
            "{}: the retired readers split on {!r} ({}) and the converter said "
            "nothing — a silently picked side is a security policy nobody "
            "chose.\n{}"
        ).format(legacy_name, declared, was_live, told)
        # Assignments only. The report names the key in its candidate list, so a
        # substring test over the whole document would pass on the comment and
        # never see a written value.
        assignments = [
            line
            for line in (tree / "docs" / "config.toml")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.startswith(key.split(".")[-1] + " = ")
        ]
        assert assignments == [], (
            "{}: {} was written anyway, so the report was decoration: {}"
        ).format(legacy_name, key, assignments)
        assert got.returncode != 0, (
            "{}: the retired readers split on {!r}, the converter wrote nothing, "
            "and the query ANSWERED anyway — with a default the adopter was "
            "supposed to be choosing. Since the cutover that is the fail-open "
            "the unconverted rung exists to close.\n{}"
        ).format(legacy_name, declared, got.stdout + got.stderr)
        return

    assert got.returncode == 0, got.stdout + got.stderr
    answer = got.stdout.strip().lower()
    is_live = new_live(answer)
    assert is_live == verdicts.pop(), (
        "{}: the retired readers read {!r} as {} but {} answered {!r} "
        "(live={}). The cutover may not change behaviour."
    ).format(legacy_name, declared, was_live, key, answer, is_live)


def test_a_second_conversion_refuses_and_leaves_the_file_untouched(tree):
    """Re-running the converter is safe, because it refuses rather than rewrites.

    SR-141 makes bootstrap and re-sync run this automatically, so "what happens
    on the second run" is not a corner — it is every run after the first. The
    answer is a refusal plus a byte-identical file: an adopter's edits survive,
    and the automatic call site can treat "already converted" as done rather than
    as an error to work around.
    """
    (tree / "docs" / "privacy-check").write_text(
        "true\n", encoding="utf-8", newline="\n"
    )
    first = run_py(
        [tree / "scripts" / "config_migrate.py", "--root", str(tree), "--write"],
        cwd=tree,
    )
    assert first.returncode == 0, first.stdout + first.stderr
    once = (tree / "docs" / "config.toml").read_bytes()

    (tree / "docs" / "config.toml").write_bytes(once + b"\n# an adopter's own note\n")
    edited = (tree / "docs" / "config.toml").read_bytes()

    second = run_py(
        [tree / "scripts" / "config_migrate.py", "--root", str(tree), "--write"],
        cwd=tree,
    )
    assert second.returncode != 0, second.stdout + second.stderr
    assert "never overwrites" in (second.stdout + second.stderr)
    assert (tree / "docs" / "config.toml").read_bytes() == edited


def test_a_value_the_schema_refuses_is_reported_not_written(tree):
    """The converter must never write a document its own loader rejects.

    Driven because it happened: a junk word in a retired file was tolerated by a
    `grep` that only ever asked "is it exactly this word?", and converting it
    verbatim produced a canonical file that refused at preflight — leaving the
    adopter with a broken new source AND the old one still the only honest
    record. SR-140 says report what cannot be mapped; a value the schema refuses
    cannot be mapped.
    """
    (tree / "docs" / "push-policy").write_text(
        "nonsense\n", encoding="utf-8", newline="\n"
    )
    proc = run_py(
        [tree / "scripts" / "config_migrate.py", "--root", str(tree), "--write"],
        cwd=tree,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout + proc.stderr
    assert "NOT CONVERTED" in out and "push-policy" in out and "policy.push" in out

    got = _query(tree, "policy.push")
    assert got.returncode == 0, got.stdout + got.stderr
    assert got.stdout.strip() == "human", (
        "the schema default must survive the junk value"
    )


# --- the migration state, pinned rather than assumed --------------------------
def _code_lines(hook):
    """The hook's executable lines — comments dropped, so prose ABOUT a file is
    not mistaken for a parse OF it."""
    return "\n".join(
        line
        for line in (KIT / "hooks" / hook).read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )


@pytest.mark.parametrize("hook", HOOKS)
def test_the_hooks_read_the_canonical_configuration_since_the_cutover(hook):
    """INVERTED at P13, exactly as the pre-cutover form of this test said it
    would be.

    It used to pin the deliberate not-yet-switched state ("the hooks still
    parse their retired one-value files"), because an unpinned "we'll wire it
    later" is indistinguishable from a forgotten slice. The cutover landed, so
    the pin turns around: every hook must now call the canonical reader, and
    none may carry the retired first-non-comment-line pipeline.

    Deleting the test instead would have thrown away the only mechanical record
    that this migration has TWO states and that the tree is in one of them. What
    a REVERT of the cutover then meets is a red test naming the file, which is
    the point of pinning a migration in both directions.

    (The retired FILES survive this slice on purpose — they are what makes the
    cutover revertible; P14 deletes them. What must be gone here is the PARSE.
    `tests/test_config_cutover.py` drives the behaviour; this stays the cheap
    source-level pin beside the agreement bar it belongs to.)
    """
    code = _code_lines(hook)
    assert "config_query.py" in code, (
        "{} does not call config_query.py. The P13 cutover moved every policy "
        "read to the canonical entry point; a hook that skipped it is reading a "
        "dial nobody maintains."
    ).format(hook)
    assert "tr -d '[:space:]'" not in code, (
        "{} still carries the retired first-non-comment-line pipeline. Two live "
        "readers of one security dial is the divergence this program exists to "
        "end — and the retired one wins silently, because it never refuses."
    ).format(hook)


def test_the_query_is_importable_and_fast_enough_for_a_hook(tree):
    """The reader a hook will call must not drag in the world.

    A hook runs on every commit, so the entry point's cost is paid constantly.
    This is a floor, not a benchmark: it catches an accidental heavyweight import
    landing in the module, not a few milliseconds of drift.
    """
    (tree / "docs" / "config.toml").write_text(
        "schema = 1\n\n[policy]\nprivacy_check = false\n",
        encoding="utf-8",
        newline="\n",
    )
    proc = _query(tree, "policy.privacy_check")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout.strip().lower() == "false"

    body = (SCRIPTS / "config_query.py").read_text(encoding="utf-8")
    for heavy in (
        "import csv",
        "import subprocess",
        "import urllib",
        "import unittest",
    ):
        assert heavy not in body, (
            "config_query.py imports {} — a hook pays this on every commit".format(
                heavy
            )
        )


def test_an_undeclared_key_exits_non_zero(tree):
    proc = _query(tree, "policy.no_such_dial")
    assert proc.returncode != 0
    assert "policy.no_such_dial" in (proc.stderr + proc.stdout)


def test_a_refused_configuration_exits_non_zero(tree):
    """Fail closed: an unreadable policy is never an absent one.

    This is the M-42 property the cutover must preserve — and D-1 strengthens it,
    because the grep being replaced answered "absent" here and let the commit
    proceed.
    """
    (tree / "docs" / "config.toml").write_text(
        "schema = 1\n\n[policy]\nprivacy_chek = true\n", encoding="utf-8", newline="\n"
    )
    proc = _query(tree, "policy.privacy_check")
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "REFUSED" in (proc.stderr + proc.stdout)


def test_an_interpreter_below_the_floor_refuses_by_name(tree):
    """A below-floor interpreter BLOCKS the commit instead of answering it.

    Driven, not grepped. The previous form of this test asserted only that the
    string "3.11" appeared somewhere in the source, which survives deleting
    `floor_refusal` and its call site outright — a green that proves nothing
    about the behaviour its own name claims.

    The below-floor box is simulated by raising the tree's COPY of the declared
    floor above every real interpreter. That is faithful because `floor_refusal`
    decides on nothing but `sys.version_info[:2] >= MIN_PYTHON`: moving the floor
    up and moving the interpreter down drive the identical comparison, and the
    copy is the shipped file byte for byte apart from that one constant. There is
    no below-floor Python to hand this suite, and a test-only argument on `main`
    would be a second contract. The `tree` fixture re-copies the scripts for
    every test, so the edit cannot leak.

    Driven through a SUBPROCESS rather than an import because that is how a hook
    calls it: what the hook acts on is the exit code, and what it shows a human
    is the stderr line — so an empty stdout and a named floor are the properties,
    not the presence of a version string in the source.
    """
    (tree / "docs" / "config.toml").write_text(
        "schema = 1\n\n[policy]\nprivacy_check = true\n",
        encoding="utf-8",
        newline="\n",
    )
    live = _query(tree, "policy.privacy_check")
    assert live.returncode == 0 and live.stdout.strip() == "true", (
        "control: this call must ANSWER while the floor is satisfied, or the "
        "refusal below would not be evidence about the floor: "
        + live.stdout
        + live.stderr
    )

    script = tree / "scripts" / "config_query.py"
    source = script.read_text(encoding="utf-8")
    below_floor = source.replace("MIN_PYTHON = (3, 11)", "MIN_PYTHON = (99, 0)")
    assert below_floor != source, (
        "config_query.py no longer declares `MIN_PYTHON = (3, 11)`, so this "
        "simulation is not moving the floor and the drive below is vacuous"
    )
    script.write_text(below_floor, encoding="utf-8", newline="\n")

    proc = _query(tree, "policy.privacy_check")
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert proc.stdout == "", (
        "a below-floor box must print NOTHING on stdout: a hook capturing the "
        "answer would otherwise read a value nobody resolved"
    )
    assert "config_query: REFUSED" in proc.stderr, proc.stderr
    assert "99.0" in proc.stderr, (
        "the refusal must NAME the floor it wants — it is the whole of what a "
        "hook can show a human: " + proc.stderr
    )
