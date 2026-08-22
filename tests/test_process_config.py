"""`docs/process.toml` — the one policy home, and the two grammars that read it.

SN-028 folded ~10 one-word policy files into one TOML. That is a consolidation
with a sharp edge, and this module is the edge's guard: **two grammars read this
file.** `tomllib` reads it in Python, and the three git hooks read it in pure sh
so a Python-less box still refuses to skip a declared privacy gate (M-42,
repo-review 2026-07-21). TOML is far more expressive than a `grep -E` can
follow, and every shape only ONE of them understands is a silent flip of a
security gate.

The first cut of this consolidation shipped without this test and had exactly
that defect in five shapes, driven: a trailing comment (`privacy_check = true
# note`), a dotted key, an inline table, an uppercase `TRUE`, and a BOM each
made the hook and Python disagree — three of them fail-OPEN, i.e. a repo that
had declared the privacy gate committing with it silently off.

So the contract has three parts and all three are driven here:

  1. **The file's SHAPE is checked, not assumed** — `process_shape_findings`
     refuses dotted keys, inline tables, multi-line strings, and a hook-read
     key under the wrong section.
  2. **The sh read is ASYMMETRIC and fails closed** — broad "is it declared",
     narrow "is it provably false", ON in between.
  3. **The two readings AGREE** over a table of adversarial files, and the
     table is the one the review found the bugs with.

Plus the migration's own guarantees: a mixed config is refused rather than
resolved, a wrong-typed dial is refused rather than defaulted, and the
converter never deletes a legacy file whose value it did not manage to write.
"""

import shutil
import subprocess

import pytest
from conftest import KIT, ROOT, load_script, skip_without_env_gates

ac = load_script("agent_common")
bootstrap = load_script("bootstrap")
check_privacy = load_script("check_privacy")

HOOK = KIT / "hooks" / "pre-commit"


def write_toml(root, text):
    (root / "docs").mkdir(parents=True, exist_ok=True)
    with (root / "docs" / "process.toml").open(
        "w", encoding="utf-8", newline="\n"
    ) as fh:
        fh.write(text)


def sh_privacy_declared_true(root):
    """The SHIPPED hook's own `privacy_declared_true`, run as sh.

    Sourced out of the real hook rather than re-implemented: a guard that
    carries its own copy of the thing under test can only ever agree with
    itself. The hook is `. `-sourced with a stub `exit` so its top-level
    mixed-config rung cannot end the probe."""
    skip_without_env_gates("posix-shell")
    sh = shutil.which("sh")
    script = (
        'REPO_ROOT="$1"\n'
        # EVERY function comes out of the shipped hook, `_ptoml_body` INCLUDED.
        # It used to be re-implemented on the line below, which is exactly the
        # defect this docstring warns about — and the warning did not save it:
        # the local copy went stale, so this table kept passing while the
        # shipped reader failed OPEN on a trailing-comment decoy. A guard that
        # carries its own copy of the thing under test can only agree with
        # itself.
        + _extract_function(HOOK, "_ptoml_body")
        + _extract_function(HOOK, "privacy_declared_true")
        + _extract_function(HOOK, "process_declares")
        + "if privacy_declared_true; then echo TRUE; else echo FALSE; fi\n"
    )
    proc = subprocess.run(
        [sh, "-c", script, "sh", str(root)], capture_output=True, text=True
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip() == "TRUE"


def _extract_function(path, name):
    """One shell function's source, verbatim, out of a hook file."""
    text = path.read_text(encoding="utf-8")
    start = text.index(name + "() {")
    end = text.index("\n}\n", start) + len("\n}\n")
    return text[start:end]


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
    # THE DECOY PAIR — the shape the FINAL review found failing OPEN, and the
    # reason `_ptoml_body` strips TRAILING comments rather than only whole-line
    # ones. `privacy_check = true # privacy_check = false` is legal TOML whose
    # value is `true`; the hook's narrow "provably false" test matched the decoy
    # INSIDE the comment, so the gate switched off while Python read it ON. The
    # hook is what blocks the commit, so the hook's answer is the one that
    # decides — this was the M-42 contract inverted.
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
    # A `#` inside a legal string value: the strip can truncate it, and every
    # consequence runs the SAFE way (a truncated value is LESS able to prove
    # `false`), so the two readers still agree.
    (
        "hash-inside-a-string",
        '[policies]\nprivacy_review = "a#b"\nprivacy_check = true\n',
        True,
    ),
    # A key mentioned ONLY in a trailing comment declares nothing — which is
    # what `tomllib` says, so the broad test must agree with it rather than
    # fail closed on a decoy.
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


@pytest.mark.parametrize("label,text,expected", SHAPES, ids=[s[0] for s in SHAPES])
def test_the_hook_sh_and_tomllib_agree_on_every_shape(tmp_path, label, text, expected):
    """THE cross-parser pin. `expected is None` means "this file declares
    nothing", where both readers must fall through to the legacy file."""
    write_toml(tmp_path, text)
    hook = sh_privacy_declared_true(tmp_path)
    python = check_privacy.read_privacy_enabled(tmp_path)
    assert hook == python, "{}: hook={} python={}".format(label, hook, python)
    if expected is not None:
        assert hook is expected, label


UNPARSEABLE = [
    ("uppercase-TRUE", "[policies]\nprivacy_check = TRUE\n"),
    ("malformed", "[policies\nprivacy_check = true\n"),
    ("bare-word", "[policies]\nprivacy_check = yes\n"),
]


@pytest.mark.parametrize("label,text", UNPARSEABLE, ids=[s[0] for s in UNPARSEABLE])
def test_an_unparseable_file_reads_ON_in_both_readers(tmp_path, label, text):
    """FAIL CLOSED, together. A file that exists and does not parse must never
    read as an opted-OUT privacy gate in either grammar — the hook keeps acting
    on the text it can see, so Python must not conclude "off" behind it."""
    write_toml(tmp_path, text)
    assert sh_privacy_declared_true(tmp_path) is True, label
    assert check_privacy.read_privacy_enabled(tmp_path) is True, label


NON_GREPPABLE = [
    ("dotted-key", "policies.privacy_check = true\n"),
    ("inline-table", "policies = { privacy_check = true }\n"),
    ("multiline-string", '[policies]\nnote = """\nprivacy_check = true\n"""\n'),
    ("wrong-section", "[attestation]\nprivacy_check = true\n"),
]


@pytest.mark.parametrize("label,text", NON_GREPPABLE, ids=[s[0] for s in NON_GREPPABLE])
def test_a_shape_the_hooks_cannot_follow_is_refused_and_still_reads_ON(
    tmp_path, label, text
):
    """The shapes that made the two grammars disagree are REFUSED by the shape
    check — and, because a refusal is only as good as what happens when someone
    ignores it, they also still read ON in both readers."""
    write_toml(tmp_path, text)
    findings = ac.process_shape_findings(tmp_path / "docs")
    assert findings, "{}: must be refused as un-greppable".format(label)
    assert sh_privacy_declared_true(tmp_path) is True, label
    assert check_privacy.read_privacy_enabled(tmp_path) is True, label


def test_the_shipped_template_and_this_repos_own_file_pass_the_shape_check():
    # The guard is worthless if the two files it exists for do not satisfy it.
    assert ac.process_shape_findings(ROOT / "docs") == []
    assert ac.process_shape_findings(KIT) == [] or not (KIT / "process.toml").exists()


def test_both_hooks_carry_the_same_reader_byte_for_byte():
    # pre-commit and commit-msg gate two boundaries of the same commit; a
    # divergence between their copies would gate one and not the other.
    for fn in ("privacy_declared_true", "process_declares", "mixed_config_refusal"):
        a = _extract_function(HOOK, fn)
        b = _extract_function(KIT / "hooks" / "commit-msg", fn)
        assert a == b, fn


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
    # rotting.
    docs = _docs(tmp_path)
    (docs / "privacy-check").write_text("# header\ntrue\n", encoding="utf-8")
    assert check_privacy.read_privacy_enabled(tmp_path) is True
    assert sh_privacy_declared_true(tmp_path) is True


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
    # sentinel for "no rung is a human's to ratify".
    assert cfg["attestation"]["human_ratification_through"] == "DevStg-Below"
    assert cfg["attestation"]["keep_nondependent"] is True
    assert cfg["attestation"]["final_review"] == "off"
    assert "gate_policy" not in cfg["attestation"]
    assert ac.ratification_through(tmp_path / "docs") == "DevStg-Below"
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
