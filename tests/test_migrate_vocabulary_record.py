"""The vocabulary migrator over acceptance records the kit's own routes wrote.

Once the acceptance record's act ledger holds an entry carrying `kept`, the
record is judged at the row: each later copy must equal the previous one with
only an act's named rows taken from live. A copy the migrator wrote equal to
live would then carry a kept row's text in with no act, and the hook would
refuse it. So in such a record the migrator writes no copy, and while the
record still stores an earlier spelling it refuses the whole run (WI-1065,
the operator's refined (c)).

Every record judged here is written by the kit's own routes: the snapshot
writer's seed and acts (`baseline_snapshot.copy_live`, which the snapshot
command runs) and the migrator's own run over an earlier kit's record. Each
case builds a real git repository, so the module is slow-tiered
(`conftest.SLOW_MODULES`); the in-process cases are in
`test_migrate_vocabulary.py`.

Implements: TC-427
"""

import shutil
import subprocess

import pytest

from conftest import SCRIPTS, load_script, pin_autocrlf, run_py, skip_without_env_gates

migrate = load_script("migrate_vocabulary")
SNAP = load_script("baseline_snapshot")
CT = load_script("check_trajectory")

SR_REL = "docs/requirements/system-requirements.toml"
BINDING_REL = "docs/reviews/wi-1/001-ADJUDICATE-a.md.requested"
BINDING = "brief = amendment\noutcome = {}\n"
OLD, NEW = migrate.RECORD_DIRS

# An earlier kit's record: its directory, its ledger's keys and its rows'
# status all in the earlier spelling.
OLD_LEDGER = """# APPROVAL ACTS, appended by the snapshot command. Do not edit.

[[act]]
seq = 1
date = "2026-09-27"
approved = ["SR-001", "SR-002"]
reattested = []
"""

TWO_ROWS = """[requirement.SR-001]
title = "Row A"
requirement = "The kit shall do A."
status = "{a}"

[requirement.SR-002]
title = "Row B"
requirement = "The kit shall do B."
status = "{b}"
"""


def _repo(tmp_path):
    """`(root, git)`: a fresh git repository, its trace report ignored."""
    skip_without_env_gates("git")
    exe = shutil.which("git")
    root = tmp_path / "repo"
    root.mkdir()

    def git(*args):
        proc = subprocess.run(
            [exe, "-C", str(root), *args], capture_output=True, text=True
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        return proc.stdout

    git("init", "-q")
    pin_autocrlf(root)
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "T")
    (root / ".git" / "info" / "exclude").write_bytes(b"docs/test/report.*\n")
    return root, git


def _write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    return path


def _commit(git, message):
    git("add", "-A")
    git("commit", "-q", "-m", message)


def _record_bytes(root):
    """`{path: bytes}` of every file under either name of the record."""
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for home in migrate.RECORD_DIRS
        for p in sorted((root / home).rglob("*"))
        if p.is_file()
    }


def _record_findings(root):
    """The acceptance-record findings of the hook's registry-integrity step,
    run as the hook runs it. A two-row tree carries findings of its own (the
    registries a minimal record holds no copy of), so a caller compares two
    readings rather than asking for none."""
    proc = run_py([SCRIPTS / "trace.py", "--root", ".", "--strict-integrity"], root)
    return sorted(
        line
        for line in proc.stdout.splitlines()
        if line.startswith("FINDING (acceptance record)")
    )


def _run(root, *flags):
    return migrate.main(["--root", str(root), *flags])


@pytest.mark.xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))
def test_a_run_after_a_row_by_row_act_lands_past_the_hook_and_the_committed_history(
    tmp_path, capsys
):
    """Done-when 2 and 3: the migrator's own run moves an earlier kit's record,
    an act through the snapshot writer then keeps a drifted row, and a later
    run for a binding writes no record file, so its commit passes the hook's
    integrity step and the committed-history check.

    Implements: TC-427
    """
    root, git = _repo(tmp_path)
    _write(root, SR_REL, TWO_ROWS.format(a="Approved", b="Approved"))
    _write(root, OLD + "/README.md", "# `last_approved` - the record\n")
    _write(root, OLD + "/acts.toml", OLD_LEDGER)
    _write(root, OLD + "/" + SR_REL, TWO_ROWS.format(a="Approved", b="Approved"))
    _commit(git, "an earlier kit's record")
    assert _run(root) == 0
    assert not (root / OLD).exists() and (root / NEW / "acts.toml").is_file()
    _commit(git, "the vocabulary migration")
    live = root / SR_REL
    text = live.read_bytes().replace(b'"Row A"', b'"Row A, re-accepted"')
    live.write_bytes(text.replace(b'"Row B"', b'"Row B, unread"'))
    _commit(git, "the text")
    SNAP.copy_live(root, reaccepts=["SR-001"])
    assert SNAP.read_acts(root)[-1]["kept"] == ["SR-002"]
    _commit(git, "the act, SR-002 kept")
    binding = _write(root, BINDING_REL, BINDING.format("accepted"))
    _commit(git, "a binding in the earlier spelling")
    findings = _record_findings(root)
    record = _record_bytes(root)
    capsys.readouterr()

    assert _run(root, "--check") == 1
    out = capsys.readouterr().out
    assert "verdict binding owes the rewrite: " + BINDING_REL in out, out
    assert "acceptance record" not in out, out
    assert _run(root) == 0
    assert binding.read_text(encoding="utf-8") == BINDING.format("recorded")
    assert _record_bytes(root) == record
    git("add", "-A")
    assert _record_findings(root) == findings
    assert CT.staged_snapshot_findings(root) == []
    git("commit", "-q", "-m", "the migrator's run for the binding")
    assert CT.committed_snapshot_findings(root) == []
    assert _record_findings(root) == findings
    capsys.readouterr()
    assert _run(root, "--check") == 0
    assert "nothing stored in an earlier spelling" in capsys.readouterr().out


def _refused(root, capsys, named):
    """Run the migrator in check mode and for real over `root`: each exits 1,
    names `named` and the way back, and leaves the working tree as committed."""
    for flags in (("--check",), ()):
        assert _run(root, *flags) == 1
        out = capsys.readouterr().out
        assert "acceptance record NOT rewritten: " + named in out, out
        assert "before its first row-by-row act" in out, out


@pytest.mark.xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))
def test_a_record_seeded_over_an_earlier_status_refuses_and_writes_nothing(
    tmp_path, capsys
):
    """The snapshot writer's seed, over a live registry still holding the
    earlier status (a repository that took the kit and skipped the migrator),
    writes a record that holds a row-by-row act and an earlier spelling.

    Implements: TC-427
    """
    root, git = _repo(tmp_path)
    _write(root, SR_REL, TWO_ROWS.format(a="Accepted", b="Approved"))
    SNAP.copy_live(root, seed=True)
    assert SNAP.read_acts(root)[-1]["kept"] == []
    _write(root, BINDING_REL, BINDING.format("accepted"))
    _commit(git, "the seed, over an earlier status")
    capsys.readouterr()
    _refused(
        root, capsys, "{}/{}: a copy storing an earlier spelling".format(NEW, SR_REL)
    )
    assert git("status", "--porcelain") == ""
    assert CT.committed_snapshot_findings(root) == []


@pytest.mark.xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))
def test_a_record_seeded_beside_its_earlier_directory_refuses_and_writes_nothing(
    tmp_path, capsys
):
    """The seed writes the current record beside an earlier kit's record left
    standing. Today the registry step would rewrite the earlier record's copy
    before the record step refused; now nothing is written.

    Implements: TC-427
    """
    root, git = _repo(tmp_path)
    _write(root, OLD + "/README.md", "# `last_approved` - the record\n")
    _write(root, OLD + "/acts.toml", OLD_LEDGER)
    _write(root, OLD + "/" + SR_REL, TWO_ROWS.format(a="Approved", b="Approved"))
    _write(root, SR_REL, TWO_ROWS.format(a="Accepted", b="Accepted"))
    SNAP.copy_live(root, seed=True)
    _commit(git, "the seed, beside the earlier record")
    capsys.readouterr()
    _refused(root, capsys, OLD + ": the record's earlier directory name")
    assert git("status", "--porcelain") == ""
