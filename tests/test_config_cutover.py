"""The P13 cutover: every runtime reader on the canonical configuration (SR-139,
SR-141, LLR-159, LLR-161, TC-153's remaining permutations).

`test_config_hooks.py` proved the AGREEMENT bar before the cutover — the retired
shell pipeline and the new entry point reach the same verdict over a matrix of
declared values. This module proves the cutover itself, and it exists because
the naive version of it was *measured* to fail open: wiring the hooks to a
canonical key that no repo had set made a tree carrying `docs/privacy-check =
true` answer `false`, and the privacy gate vanished in silence.

So the cutover ships with a rung the first attempt did not have —
`config.unconverted_findings` — and this module drives the three states it
distinguishes:

  - **converted** (canonical key set): answered, whatever else is in the tree;
  - **never diverged** (retired file agrees with the schema, which is every
    freshly bootstrapped repo): answered, silently, at zero cost;
  - **unconverted** (retired file still declares something else, or something
    with no canonical form): REFUSED, and every hook blocks on the refusal.

The third case is the whole point. A rung that only fired on values nobody
writes would be decoration; the fixtures below use the exact value that caused
the incident.
"""

import shutil
import subprocess

import pytest
from conftest import KIT, SCRIPTS, env_gate_skipif, load_script, run_py

CONFIG = load_script("config")
MIGRATE = load_script("config_migrate")
COMMON = load_script("agent_common")

HOOKS = ("pre-commit", "commit-msg", "pre-push")
CONFIG_SCRIPTS = (
    "config.py",
    "config_query.py",
    "config_migrate.py",
    # The hooks delegate the actual scanning to check_privacy.py, so a hook
    # driven end to end needs it present — otherwise its non-zero exit is about
    # the fixture, not about the cutover.
    "check_privacy.py",
)


# --- the derived gate-authority vocabulary -----------------------------------
# The cutover moved the DIAL (docs/gate-policy -> the numeric boundary) and left
# the ruled tables that consume it speaking their own vocabulary. That inverse
# must stay pinned to the converter's tables, or the two halves of one migration
# drift apart while both look right in isolation.
def test_the_boundary_to_level_inverse_is_the_converters_own_mapping():
    """`agent_common.BOUNDARY_LEVEL` is READ OFF `config_migrate`, not invented.

    `GATE_AUTHORITY` says `attended` is boundary 3. `AMBIGUOUS` names 1 and 2 as
    `single-ratify`'s candidates and 0 as `autonomous`'s. Those two tables
    therefore determine the whole inverse, and this asserts the code agrees with
    them rather than with someone's memory of them.
    """
    assert MIGRATE.GATE_AUTHORITY == {"attended": 3}
    assert COMMON.escalation_level(3) == "attended"

    single = MIGRATE.AMBIGUOUS[("docs/gate-policy", "single-ratify")][0]
    boundaries = {
        int(t.rsplit("=", 1)[1]) for t in single if "human_ratification_through" in t
    }
    assert boundaries == {1, 2}, single
    for boundary in sorted(boundaries):
        assert COMMON.escalation_level(boundary) == "single-ratify"

    autonomous = MIGRATE.AMBIGUOUS[("docs/gate-policy", "autonomous")][0]
    boundaries = {
        int(t.rsplit("=", 1)[1])
        for t in autonomous
        if "human_ratification_through" in t
    }
    assert boundaries == {0}, autonomous
    assert COMMON.escalation_level(0) == "autonomous"


@pytest.mark.parametrize("bad", [-1, 4, "3", True, None])
def test_an_out_of_range_boundary_refuses_rather_than_clamping(bad):
    """Clamping would route a whole spine tier to a machine the adopter meant to
    reserve for a human. That is the one direction this dial must never drift
    in, so the mapping raises instead."""
    with pytest.raises(ValueError):
        COMMON.escalation_level(bad)


def test_the_schema_default_is_now_the_kits_only_home_for_the_boundary():
    """The kit shipped this default TWICE until P14, and the cutover's rung
    compared them: `config.SCHEMA` here, `gate-policy.template`'s `attended`
    there. If the two disagreed, every freshly bootstrapped repo met an
    unconverted refusal it did nothing to earn — and a refusal every new repo
    hits is a refusal everyone learns to ignore. (They DID disagree before the
    cutover: the schema said 1, the template `attended`, which converts to 3.)

    P14 deleted the template, so the agreement is now unfalsifiable rather than
    merely true — and THAT is what this test pins. It asserts the second home
    is gone, and that the surviving default still MEANS what the deleted one
    said: 3 is the boundary `attended` converted to, so a fresh scaffold's
    behaviour is byte-identical to a pre-cutover one.
    """
    assert not (KIT / "gate-policy.template").exists(), (
        "the second home of the ratification-boundary default is back; "
        "config.SCHEMA is the one home since P14"
    )
    default = CONFIG.DEFAULTS["attestation.human_ratification_through"]
    assert MIGRATE.GATE_AUTHORITY["attended"] == default
    assert COMMON.escalation_level(default) == "attended"


def test_the_attest_fallback_boundary_matches_the_schema_default():
    """`attest.DEFAULT_BOUNDARY` is the answer when config.py is unavailable. A
    fallback that is more permissive than the declared default is a hole that
    only opens on the machines least able to notice."""
    attest = load_script("attest")
    assert (
        attest.DEFAULT_BOUNDARY
        == CONFIG.DEFAULTS["attestation.human_ratification_through"]
    )


# --- the unconverted rung, driven ---------------------------------------------
def _tree(tmp_path):
    (tmp_path / "docs").mkdir(exist_ok=True)
    (tmp_path / "scripts").mkdir(exist_ok=True)
    for name in CONFIG_SCRIPTS:
        shutil.copyfile(SCRIPTS / name, tmp_path / "scripts" / name)
    return tmp_path


def _write(root, rel, text):
    path = root.joinpath(*rel.split("/"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def _query(root, key):
    return run_py(
        [root / "scripts" / "config_query.py", "--root", str(root), key], cwd=root
    )


def test_the_measured_fail_open_is_now_a_refusal(tmp_path):
    """THE INCIDENT, as a test. `docs/privacy-check = true` with no canonical key
    must never be answered `false` — it is refused, and the refusal names the
    file, the key and the fix."""
    root = _tree(tmp_path)
    _write(root, "docs/privacy-check", "true\n")

    proc = _query(root, "policy.privacy_check")
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert proc.stdout.strip() == "", (
        "a refusal must print NOTHING on stdout, or a hook capturing the answer "
        "reads a value nobody resolved: " + proc.stdout
    )
    told = proc.stderr
    assert "REFUSED" in told and "policy.privacy_check" in told, told
    assert "docs/privacy-check" in told, told
    assert "config_migrate" in told, "the refusal must name the fix: " + told


def test_converting_the_repo_makes_the_same_tree_answer(tmp_path):
    """The refusal is a MIGRATION step, not a wall: run the converter the message
    names and the identical tree answers — with the retired file still present,
    which is the transitional state a repo has to be able to commit in."""
    root = _tree(tmp_path)
    _write(root, "docs/privacy-check", "true\n")
    assert _query(root, "policy.privacy_check").returncode != 0

    convert = run_py(
        [root / "scripts" / "config_migrate.py", "--root", str(root), "--write"],
        cwd=root,
    )
    assert convert.returncode == 0, convert.stdout + convert.stderr

    assert (root / "docs" / "privacy-check").is_file(), (
        "the converter must not delete the retired file — keeping it is what "
        "makes the cutover revertible"
    )
    proc = _query(root, "policy.privacy_check")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout.strip() == "true"


def test_a_retired_file_that_agrees_with_the_schema_costs_nothing(tmp_path):
    """Every freshly bootstrapped repo lives here: `docs/push-policy: human`,
    `docs/review-policy: 1`, `docs/gate-policy: attended`, `docs/privacy-check:
    false` — all equal to their canonical defaults, so the rung is silent."""
    root = _tree(tmp_path)
    _write(root, "docs/privacy-check", "false\n")
    _write(root, "docs/push-policy", "human\n")
    _write(root, "docs/review-policy", "1\n")
    _write(root, "docs/gate-policy", "attended\n")

    for key, expected in (
        ("policy.privacy_check", "false"),
        ("policy.push", "human"),
        ("policy.review_rounds", "1"),
        ("attestation.human_ratification_through", "3"),
    ):
        proc = _query(root, key)
        assert proc.returncode == 0, key + ": " + proc.stdout + proc.stderr
        assert proc.stdout.strip() == expected, key


def test_an_ambiguous_retired_value_refuses_with_the_converters_reason(tmp_path):
    """`autonomous` has NO canonical form — the converter says so and writes
    nothing. A reader that answered the schema default here would be enacting a
    policy the adopter never chose, quietly, at the tier that decides who
    ratifies."""
    root = _tree(tmp_path)
    _write(root, "docs/gate-policy", "autonomous\n")

    proc = _query(root, "attestation.human_ratification_through")
    assert proc.returncode != 0, proc.stdout + proc.stderr
    told = proc.stderr
    assert "docs/gate-policy" in told and "REFUSES to map" in told, told
    assert "autonomous permitted NO early human checkpoint" in told, (
        "the refusal must quote the CONVERTER's reason, not a paraphrase: " + told
    )


def test_stack_ini_presence_is_not_evidence_of_an_unconverted_repo(tmp_path):
    """docs/stack.ini survives the migration — it is the declared toolchain, and
    it exists in every repo. A rung that treated its presence as "unconverted"
    would refuse every tree in the world."""
    root = _tree(tmp_path)
    _write(root, "docs/stack.ini", "[agent-loop]\nlanes = 2\n")
    assert CONFIG.unconverted_findings(root, ("automation.lanes",)) == []


def test_the_rung_only_reports_the_keys_the_caller_reads(tmp_path):
    """A refusal about a dial this caller never reads is noise, and noise is how
    a real refusal gets ignored."""
    root = _tree(tmp_path)
    _write(root, "docs/privacy-check", "true\n")
    _write(root, "docs/push-policy", "agent\n")

    assert [f.key for f in CONFIG.unconverted_findings(root, ("policy.push",))] == [
        "policy.push"
    ]
    assert [
        f.key for f in CONFIG.unconverted_findings(root, ("policy.privacy_check",))
    ] == ["policy.privacy_check"]


def test_a_set_canonical_key_stands_down_the_rung_even_beside_its_retired_file(
    tmp_path,
):
    """Both-present is the MIGRATION state and must stay commitable; it is
    `mixed_source_findings`' business at preflight, not this rung's. Refusing it
    here would mean a repo could never commit its own conversion."""
    root = _tree(tmp_path)
    _write(root, "docs/privacy-check", "true\n")
    _write(root, "docs/config.toml", "schema = 1\n\n[policy]\nprivacy_check = true\n")

    assert CONFIG.unconverted_findings(root, ("policy.privacy_check",)) == []
    assert [f.key for f in CONFIG.mixed_source_findings(root)] == [
        "policy.privacy_check"
    ]


# --- the hooks, driven --------------------------------------------------------
_hook_gate = env_gate_skipif("posix-shell", "git")


@pytest.fixture
def hook_tree(tmp_path):
    """A real git repo carrying the three hooks and the reader they now call."""
    root = _tree(tmp_path)
    hooks = root / ".githooks"
    hooks.mkdir()
    for name in HOOKS:
        dst = hooks / name
        shutil.copyfile(KIT / "hooks" / name, dst)
        dst.chmod(dst.stat().st_mode | 0o111)
    subprocess.run(["git", "init"], cwd=str(root), capture_output=True, text=True)
    return root


def _run_hook(root, hook, argv=(), stdin=""):
    return subprocess.run(
        [shutil.which("sh"), str(root / ".githooks" / hook), *argv],
        cwd=str(root),
        input=stdin,
        capture_output=True,
        text=True,
    )


@_hook_gate
@pytest.mark.parametrize("hook", HOOKS)
def test_no_hook_parses_the_retired_privacy_files_any_more(hook):
    """The INVERSION of `test_config_hooks.py`'s pre-cutover pin, which said in
    its own docstring that it would invert here.

    Comments are stripped before the check: the hooks legitimately still
    *discuss* the retired files (and test for their presence, in pure sh, to
    decide whether a Python-less box may skip). What must be gone is the PARSE —
    the grep pipeline that read a policy value out of one.
    """
    code = "\n".join(
        line
        for line in (KIT / "hooks" / hook).read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )
    assert "config_query.py" in code, (
        "{} does not call config_query.py — the cutover has not landed here"
    ).format(hook)
    for retired in ("docs/privacy-check", "docs/privacy-review"):
        assert "grep" not in code or retired not in code.split("grep", 1)[1], (
            "{} still greps {} for a value; the canonical reader is the one "
            "home of that answer".format(hook, retired)
        )
    assert "tr -d '[:space:]'" not in code, (
        "{} still carries the retired first-non-comment-line pipeline".format(hook)
    )


@_hook_gate
@pytest.mark.parametrize("hook", HOOKS)
def test_every_hook_blocks_when_the_configuration_refuses(hook, hook_tree):
    """TC-153's remaining permutation: a refused query BLOCKS, in all three.

    The refusal driven here is a MALFORMED document (a typo'd key), because that
    is the case where every hook's own logic is otherwise happy — nothing else
    about the tree is wrong, so a hook that let it through would be letting
    through a repo whose privacy posture is unknown.
    """
    _write(hook_tree, "docs/config.toml", "schema = 1\n\n[policy]\nprivacy_chek = 1\n")
    proc = _run_hook(hook_tree, hook, argv=("msg.txt",), stdin="")
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "REFUSED" in (proc.stdout + proc.stderr), proc.stdout + proc.stderr


@_hook_gate
@pytest.mark.parametrize("hook", HOOKS)
def test_every_hook_blocks_an_unconverted_repo(hook, hook_tree):
    """The measured fail-open, at each hook's own call site. A tree carrying only
    `docs/privacy-check = true` must not commit or push until it converts."""
    _write(hook_tree, "docs/privacy-check", "true\n")
    proc = _run_hook(hook_tree, hook, argv=("msg.txt",), stdin="")
    assert proc.returncode != 0, proc.stdout + proc.stderr
    told = proc.stdout + proc.stderr
    assert "policy.privacy_check" in told and "docs/privacy-check" in told, told


@_hook_gate
def test_pre_push_reads_the_unwired_opt_down_from_the_canonical_key(hook_tree):
    """`warn-unwired` still opts the unwired-reviewer case down to a warning —
    read from `policy.privacy_review` now, not from a one-word file."""
    _write(
        hook_tree,
        "docs/config.toml",
        'schema = 1\n\n[policy]\nprivacy_check = true\nprivacy_review = "warn-unwired"\n',
    )
    subprocess.run(
        ["git", "commit", "--allow-empty", "-m", "seed", "--no-verify"],
        cwd=str(hook_tree),
        capture_output=True,
        text=True,
        env={
            **subprocess_env(),
            "GIT_AUTHOR_NAME": "T",
            # An EXEMPT no-reply form: the deterministic lint layer runs before
            # the reviewer branch this test is about, and a contactable address
            # would block there and never reach it.
            "GIT_AUTHOR_EMAIL": "1+t@users.noreply.github.com",
        },
    )
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(hook_tree),
        capture_output=True,
        text=True,
    ).stdout.strip()
    zero = "0" * 40
    proc = _run_hook(
        hook_tree,
        "pre-push",
        stdin="refs/heads/main {} refs/heads/main {}\n".format(head, zero),
    )
    told = proc.stdout + proc.stderr
    assert proc.returncode == 0, told
    assert "warn-unwired" in told, told


def subprocess_env():
    """The ambient environment plus the identity a fresh temp repo lacks."""
    import os

    return dict(
        os.environ,
        GIT_COMMITTER_NAME="T",
        GIT_COMMITTER_EMAIL="1+t@users.noreply.github.com",
    )


# --- SR-141: a simulated re-sync, driven on a REAL bootstrapped scaffold -------
def test_a_resync_converts_the_retired_files_and_never_clobbers_the_config(scaffold):
    """SR-141, driven rather than read off bootstrap.py.

    Three properties in one run, on a real scaffold:

      1. a fresh bootstrap leaves a readable `docs/config.toml` (the blank form)
         and a tree that ANSWERS every dial the loop reads — no scaffolded repo
         may be born unconverted;
      2. an adopter's edits to that file survive a re-sync BYTE for BYTE, even
         under `--force`, which the copy pass otherwise honours;
      3. a retired source the adopter is still carrying is converted rather than
         ignored — the case an upgrading adopter actually hits.
    """
    for key in (
        "policy.privacy_check",
        "policy.privacy_review",
        "policy.push",
        "policy.review_rounds",
        "attestation.human_ratification_through",
    ):
        proc = run_py(
            [SCRIPTS / "config_query.py", "--root", scaffold, key], cwd=scaffold
        )
        assert proc.returncode == 0, (
            "a freshly bootstrapped repo must ANSWER {} — being born unconverted "
            "would mean its first commit is blocked: {}"
        ).format(key, proc.stdout + proc.stderr)

    # The adopter's edit: uncomment one dial IN PLACE. The blank form already
    # carries a [policy] table, so APPENDING a second one would be invalid TOML
    # and this test would end up proving the loader refuses its own fixture.
    config_path = scaffold / "docs" / "config.toml"
    edited = config_path.read_text(encoding="utf-8").replace(
        '# push = "human"', 'push = "agent"   # an adopter\'s own choice', 1
    )
    assert 'push = "agent"' in edited, "the blank form no longer carries policy.push"
    config_path.write_text(edited, encoding="utf-8", newline="\n")
    before = config_path.read_bytes()

    resync = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", scaffold, "--force"], cwd=scaffold
    )
    assert resync.returncode == 0, resync.stdout + resync.stderr
    assert config_path.read_bytes() == before, (
        "the re-sync rewrote docs/config.toml — it holds the adopter's whole "
        "behavioural setup, and an upgrade that costs them that makes upgrading "
        "the kit the expensive act it must never be (SR-141)"
    )
    proc = run_py(
        [SCRIPTS / "config_query.py", "--root", scaffold, "policy.push"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout.strip() == "agent", "the adopter's edit must be what is obeyed"


def test_a_resync_onto_a_repo_with_no_config_converts_its_retired_files(tmp_path):
    """The upgrading adopter: a tree carrying the retired files and NO canonical
    document gets its OWN values, not a blank form — which is what stops the
    upgrade from landing an unconverted (and therefore refusing) repo."""
    dest = tmp_path / "legacy"
    (dest / "docs").mkdir(parents=True)
    _write(dest, "docs/privacy-check", "true\n")
    _write(dest, "docs/push-policy", "agent-iteration\n")

    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    document = (dest / "docs" / "config.toml").read_text(encoding="utf-8")
    assert "privacy_check = true" in document, document
    assert 'push = "agent-iteration"' in document, document
    for key, expected in (
        ("policy.privacy_check", "true"),
        ("policy.push", "agent-iteration"),
    ):
        got = run_py([SCRIPTS / "config_query.py", "--root", dest, key], cwd=dest)
        assert got.returncode == 0, got.stdout + got.stderr
        assert got.stdout.strip() == expected


# --- P14: the mixed-source rung acquires its runtime call site -----------------
# Until P14 `config.mixed_source_findings` had NO caller, deliberately: this repo
# (and every mid-migration adopter) carried both the canonical key and its retired
# file, so wiring the refusal would have refused the very tree that had just
# converted. The deletions are what make it wirable, and these drive the wiring.


def test_declared_config_now_refuses_a_both_sources_tree(tmp_path):
    """The preflight rung, driven end to end through the coordinator's own entry
    point rather than through `config.py` directly — that is the seam a caller
    actually uses, and the seam a regression would come back through."""
    root = _tree(tmp_path)
    _write(root, "docs/config.toml", "schema = 1\n\n[policy]\nprivacy_check = true\n")
    _write(root, "docs/privacy-check", "true\n")

    _cfg, refusals = COMMON.declared_config(root, ("policy.privacy_check",))
    assert len(refusals) == 1, refusals
    assert "policy.privacy_check" in refusals[0]
    assert "docs/privacy-check is still live" in refusals[0]

    # Delete the retired file — the P14 act — and the same tree is answered.
    (root / "docs" / "privacy-check").unlink()
    _cfg, refusals = COMMON.declared_config(root, ("policy.privacy_check",))
    assert refusals == []


def test_the_mixed_rung_reports_only_the_caller_s_own_read_set(tmp_path):
    """The read-set filter is not tidiness — it is what lets a repo convert its
    ROUTES (whose canonical keys nothing reads until routing binds at P5) while
    the retired `docs/agents.csv` is still the live source. A whole-schema report
    would refuse the tree that converted them, and an exemption LIST would have to
    be remembered and deleted by hand; the filter simply starts refusing the day a
    caller declares it reads the key."""
    root = _tree(tmp_path)
    _write(
        root,
        "docs/config.toml",
        "schema = 1\n\n[policy]\nprivacy_check = true\n\n[routing]\nenabled = true\n",
    )
    _write(root, "docs/privacy-check", "true\n")
    _write(root, "docs/agents-enabled", "ANTHROPIC-OPUS\n")

    # A caller that reads only the privacy dial hears only about it.
    assert [
        f.key for f in CONFIG.mixed_source_findings(root, ("policy.privacy_check",))
    ] == ["policy.privacy_check"]
    # A caller that reads neither hears nothing at all.
    assert CONFIG.mixed_source_findings(root, ("policy.push",)) == []
    # The unfiltered audit still sees both — that surface is what a migration
    # tool and a human reviewer use, and it must not go quiet.
    assert [f.key for f in CONFIG.mixed_source_findings(root)] == [
        "policy.privacy_check",
        "routing.enabled",
    ]


def test_a_fresh_scaffold_scaffolds_no_retired_declared_policy_file(tmp_path):
    """The whole reason bootstrap's MAPPING rows went with the files. A scaffold
    that laid `docs/blackout` down beside `docs/config.toml` was WORSE than
    untidy: the template declared `12:00-19:00` while the schema default is `""`,
    so the coordinator's unconverted rung refused every freshly bootstrapped repo
    by name, on day one — a refusal every new adopter meets is a refusal everyone
    learns to ignore. Driven both ways: the scaffold is clean, and planting the
    retired file back reproduces the refusal.
    """
    dest = tmp_path / "fresh"
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    for name in (
        "gate-policy",
        "push-policy",
        "review-policy",
        "privacy-check",
        "blackout",
    ):
        assert not (dest / "docs" / name).exists(), name

    keys = ("automation.blackout", "policy.privacy_check", "policy.push")
    _cfg, refusals = COMMON.declared_config(dest, keys)
    assert refusals == [], refusals

    _write(dest, "docs/blackout", "12:00-19:00\n")
    _cfg, refusals = COMMON.declared_config(dest, keys)
    assert len(refusals) == 1, refusals
    assert "automation.blackout" in refusals[0] and "docs/blackout" in refusals[0]
