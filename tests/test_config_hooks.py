"""The old shell read and the new config query decide alike (SR-139, TC-153 part 1).

**Read this before "finishing" the wiring.** The hooks deliberately still parse
their retired one-value files. That is not an oversight and not a half-done
slice — it is the plan's staging: P2 builds the reader, proves it agrees with
what it will replace, and switches **no runtime caller**; P13 performs the
cutover in one reviewed change, together with deleting the retired files.

The staging is not bureaucratic. It was **driven**: wiring the hooks to the
query in the same slice that built it made every hook read a canonical key that
no repo had set yet, so a tree carrying only `docs/privacy-check = true` lost its
privacy gate and `pre-push` exited 0 on a reviewer `BLOCK`. Fourteen shipped hook
tests caught it. A security floor is exactly the wrong place to land a reader and
its cutover in one step, because the failure mode is silence.

So what P2 owes, and what this module proves, is the **agreement bar**: the
literal retired pipeline and the new entry point, driven over one matrix of
declared values, must reach the same verdict. Agreement is what makes the P13
cutover a no-op for behaviour rather than a policy change smuggled in as a
refactor.

TC-153's remaining permutations — each hook blocking when the query refuses —
are discharged at P13, where the call sites exist to drive.
"""

import os
import shutil
import subprocess

import pytest
from conftest import KIT, SCRIPTS, augment_env, env_gate_skipif, run_py

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

# Each retired security file, its canonical key, and the two predicates that say
# whether THE GATE IS LIVE — one reading the retired word, one reading the new
# answer. The predicates are the whole point: the two readers legitimately differ
# in representation (`off` vs `false`, absent vs defaulted) and may never differ
# in verdict, so comparing raw strings would either fail on nothing or pass on
# nothing. Note the two OPT-DOWN idioms, where absence is the STRICT answer:
# `secrets-scan` scans unless the file says `off`, and `privacy-review` blocks
# unless the file says `warn-unwired`. Getting either backwards is a fail-open.
#
# `privacy-review` was missing from the first draft of the contracts doc — the
# retired list named `docs/critique-policy`, which does not exist in this kit,
# and omitted the file `pre-push` actually parses. Driving the hooks found it.
SECURITY_KEYS = (
    (
        "privacy-check",
        "policy.privacy_check",
        lambda raw: raw == "true",
        lambda ans: ans == "true",
        ("true", "false", "# only a comment", "\n\n#c\n  true  ", None),
    ),
    (
        "secrets-scan",
        "policy.secrets_scan",
        lambda raw: raw != "off",
        lambda ans: ans == "true",
        ("off", "on", "# only a comment", "\n\n#c\n  off  ", None),
    ),
    (
        "privacy-review",
        "policy.privacy_review",
        lambda raw: raw != "warn-unwired",
        lambda ans: ans != "warn-unwired",
        (
            "warn-unwired",
            "require",
            "# only a comment",
            "\n\n#c\n  warn-unwired  ",
            None,
        ),
    ),
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
    real `sh`, not re-implemented."""
    path = root / "docs" / name
    if not path.exists():
        return None
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
    for legacy_name, key, old_live, new_live, declared_values in SECURITY_KEYS:
        for declared in declared_values:
            yield pytest.param(
                legacy_name,
                key,
                old_live,
                new_live,
                declared,
                id="{}-{}".format(
                    legacy_name, "absent" if declared is None else repr(declared)
                ),
            )


@pytest.mark.parametrize(
    "legacy_name,key,old_live,new_live,declared", list(_agreement_cases())
)
def test_old_shell_read_and_new_query_decide_alike(
    tree, legacy_name, key, old_live, new_live, declared
):
    """One declared value, two readers, one verdict.

    The verdict compared is the SECURITY question the hook asks — "is this gate
    live?" — not the raw string, because the two readers legitimately differ in
    representation and may never differ in effect.
    """
    if declared is not None:
        (tree / "docs" / legacy_name).write_text(
            declared if declared.endswith("\n") else declared + "\n",
            encoding="utf-8",
            newline="\n",
        )

    was_live = old_live(_legacy_value(tree, legacy_name))

    convert = run_py(
        [tree / "scripts" / "config_migrate.py", "--root", str(tree), "--write"],
        cwd=tree,
    )
    assert convert.returncode == 0, convert.stdout + convert.stderr

    got = _query(tree, key)
    assert got.returncode == 0, got.stdout + got.stderr
    answer = got.stdout.strip().lower()
    is_live = new_live(answer)

    assert is_live == was_live, (
        "{}: the retired pipeline read {!r} (live={}) but {} answered {!r} "
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
def test_the_hooks_still_read_the_retired_files_until_the_cutover(hook):
    """The deliberate not-yet-switched state, pinned so it is a decision.

    An unpinned "we'll wire it later" is indistinguishable from a forgotten
    slice. When P13 lands, this test INVERTS: it becomes
    `test_no_hook_still_parses_the_retired_privacy_file`, and the retired files
    are deleted in the same change. Until then, a hook that quietly stopped
    reading its legacy file would be the fail-open this module exists to prevent.
    """
    code = _code_lines(hook)
    reads_legacy = "privacy-check" in code or "privacy-review" in code
    assert reads_legacy, (
        "{} no longer parses its retired policy file. If this is the P13 cutover, "
        "invert this test and delete the retired files in the same change; if it "
        "is not, the security floor just lost its only reader."
    ).format(hook)
    assert "config_query.py" not in code, (
        "{} calls config_query.py, but the P13 cutover has not landed. Wiring the "
        "reader before any repo has set the canonical key is the measured "
        "fail-open: a tree carrying only docs/privacy-check=true loses its gate."
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
    """A below-floor interpreter must refuse rather than answer.

    Driven through the module's own declared floor rather than by finding an old
    Python: the property is that the check exists and names the floor, which is
    what a hook's error message has to be able to quote.
    """
    body = (SCRIPTS / "config_query.py").read_text(encoding="utf-8")
    assert "3, 11" in body or "3.11" in body, (
        "config_query.py declares no interpreter floor; a below-floor box would "
        "then fail on a syntax error rather than with a named refusal"
    )
    env = augment_env(dict(os.environ))
    assert env is not None
