"""The append-only attestation ledger, and the gap it closes (SN-029).

THE GAP, stated precisely, because it is subtle and it is the whole reason this
file exists. `check_trajectory.staged_spine_amendments` is the seam BOTH the
amend-without-flip warn and the adjudication mint consume, and it drops a record
when EITHER of two things is true:

    the row's own Status is not `Verified` on both sides   (a deliberate call
                                                            it does not
                                                            second-guess)
    its owning SR is flagged on the new side               (the sanctioned
                                                            amend+flip path)

Both exits are correct for what that seam is FOR. Together they mean an
amendment made the blessed way — amend the text, flip the row to `Modified`, one
commit — is invisible to both consumers. And an SN is invisible to the seam
entirely: it has no Status cell at all, so `stakeholder-needs.md` is not even in
`SPINE_CSVS`.

A digest recorded at ACCEPTANCE time is visible regardless of any Status
movement: the text either matches what was accepted or it does not. That is the
property under test here, and it is asserted by DRIVING the blind spot — an
amend+flip that the amendment seam reports as empty, and which the ledger
catches anyway.
"""

import csv

import pytest
from conftest import KIT, ROOT, load_script

ct = load_script("check_trajectory")
intake = load_script("intake")

SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,"
    "Priority,Verification,Status\n"
)


def _spine(root, requirement="the original text", status="Verified"):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    with (req / "system-requirements.csv").open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(
            SR_HEADER
            + 'SR-001,Adder,SN-001,"{}","why","ac",,M,Test,{}\n'.format(
                requirement, status
            )
        )
    with (req / "stakeholder-needs.md").open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(
            "# Needs\n\n## Core needs\n\n"
            "| SN-ID | Need | Why | Priority | Acceptance |\n"
            "|---|---|---|---|---|\n"
            "| SN-001 | The original need. | because | M | when it works |\n"
        )
    return root


def _ledger(root, rows):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    with (req / "attestations.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(
            ["ATT-ID", "Artifact", "TextDigest", "AcceptedCommit", "Decision", "Date", "Ref"]
        )
        for row in rows:
            writer.writerow(row)


# --- the digest ----------------------------------------------------------------


def test_the_digest_is_taken_over_the_RATIFIED_cells_only(tmp_path):
    # The digest reuses `spine_cell_class`, not a second list — which is what
    # keeps it and the amend-without-flip warn from ever disagreeing about what
    # "normative" means. A TRACED cell moving must not move the digest.
    csv_path = "docs/requirements/system-requirements.csv"
    base = {
        "SR-ID": "SR-001",
        "Title": "Adder",
        "SN-Refs": "SN-001",
        "Requirement": "shall add",
        "Rationale": "why",
        "AcceptanceCriteria": "ac",
        "Priority": "M",
        "Verification": "Test",
        "Status": "Verified",
        "Phase": "1",
    }
    first = ct.digest(ct.normative_text(csv_path, base))

    traced = dict(base, **{"SN-Refs": "SN-002", "Phase": "4", "Status": "Modified"})
    assert ct.digest(ct.normative_text(csv_path, traced)) == first, (
        "a TRACED cell (or the Status marker) must not move the digest"
    )

    ratified = dict(base, Requirement="shall add, and carry")
    assert ct.digest(ct.normative_text(csv_path, ratified)) != first


def test_an_sn_digest_is_the_raw_table_line(tmp_path):
    # NOT `trace._sn_prose`'s projection: that maps need=col0/why=col1/
    # acceptance=col3, which is the Core-needs shape — the edge-case table has a
    # different four-column shape, so those rows parse to a garbled projection
    # and a digest built on it would hash the garbling.
    text = (
        "## Core needs\n"
        "| SN-001 | The need. | because | M | when it works |\n"
        "## Edge-case expectations\n"
        "| SN-013 | Provision | no python | it reports clearly |\n"
    )
    assert "The need." in ct.sn_normative_text(text, "SN-001")
    assert "no python" in ct.sn_normative_text(text, "SN-013")
    assert ct.sn_normative_text(text, "SN-999") is None
    # Whitespace-collapsed, so re-indenting a table is not an amendment.
    spaced = text.replace("| SN-001 |", "|   SN-001   |")
    assert ct.sn_normative_text(spaced, "SN-001") == ct.sn_normative_text(text, "SN-001")


# --- the gap this closes -------------------------------------------------------


def test_the_amendment_seam_is_BLIND_to_an_amend_plus_flip(tmp_path):
    """The premise, driven rather than asserted. If this ever starts failing,
    the ledger's whole justification has changed and it should be re-argued."""
    pytest.importorskip("subprocess")
    import subprocess

    root = tmp_path / "repo"
    root.mkdir()
    for args in (
        ["init", "-q"],
        ["config", "user.email", "t@example.com"],
        ["config", "user.name", "T"],
        ["config", "commit.gpgsign", "false"],
    ):
        subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    _spine(root)
    subprocess.run(["git", "-C", str(root), "add", "-A"], capture_output=True)
    subprocess.run(
        ["git", "-C", str(root), "commit", "-qm", "attested"], capture_output=True
    )
    # The SANCTIONED amendment: change the text AND flip the row, one commit.
    _spine(root, requirement="the AMENDED text", status="Modified")
    subprocess.run(["git", "-C", str(root), "add", "-A"], capture_output=True)
    subprocess.run(
        ["git", "-C", str(root), "commit", "-qm", "amend + flip"], capture_output=True
    )

    records = ct.staged_spine_amendments(root, "HEAD~1", "HEAD")
    assert records == [], (
        "the seam is expected to be blind here — that blindness is the ledger's "
        "reason to exist"
    )


def test_the_ledger_catches_what_the_seam_cannot(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    _spine(root)
    accepted = ct.current_digests(root)
    _ledger(
        root,
        [["ATT-001", "SR-001", accepted["SR-001"], "abc1234", "ratified", "2026-08-08", ""]],
    )
    assert ct.attestation_findings(root) == [], "an unamended row owes nothing"

    # The amend+flip the seam cannot see.
    _spine(root, requirement="the AMENDED text", status="Modified")
    findings = ct.attestation_findings(root)
    assert len(findings) == 1
    assert "SR-001" in findings[0] and "ATT-001" in findings[0]


def test_an_SN_gets_an_anchor_it_structurally_lacks(tmp_path):
    # An SN has no Status cell, so `stakeholder-needs.md` is not in SPINE_CSVS
    # at all — the amendment machinery cannot see an SN change by ANY path.
    root = tmp_path / "repo"
    root.mkdir()
    _spine(root)
    accepted = ct.current_digests(root)
    assert "SN-001" in accepted
    _ledger(
        root,
        [["ATT-001", "SN-001", accepted["SN-001"], "abc1234", "ratified", "2026-08-08", ""]],
    )
    assert ct.attestation_findings(root) == []

    sn = root / "docs" / "requirements" / "stakeholder-needs.md"
    sn.write_text(
        sn.read_text(encoding="utf-8").replace("The original need.", "A DIFFERENT need."),
        encoding="utf-8",
        newline="\n",
    )
    findings = ct.attestation_findings(root)
    assert len(findings) == 1 and "SN-001" in findings[0]


def test_a_meaning_decision_is_the_recorded_state_not_a_finding(tmp_path):
    # A row the ledger already says owes a fresh ratification must not ALSO
    # nag: the divergence is what `meaning` records.
    root = tmp_path / "repo"
    root.mkdir()
    _spine(root)
    _ledger(
        root,
        [["ATT-001", "SR-001", "sha256:stale", "abc1234", "meaning", "2026-08-08", ""]],
    )
    assert ct.attestation_findings(root) == []


def test_an_artifact_with_no_ledger_row_is_silent(tmp_path):
    # The honest degrade: a repo mid-migration has rows nothing has attested
    # yet, and a ledger that nagged about every one of them would be noise
    # nobody could act on.
    root = tmp_path / "repo"
    root.mkdir()
    _spine(root)
    _ledger(root, [["ATT-001", "SR-999", "sha256:x", "abc", "ratified", "2026-08-08", ""]])
    assert ct.attestation_findings(root) == []


# --- the ledger's own shape ----------------------------------------------------


def test_the_ledger_refuses_a_malformed_row(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    _ledger(
        root,
        [
            ["ATT-001", "SR-001", "sha256:a", "abc", "ratified", "2026-08-08", ""],
            ["ATT-001", "SR-002", "sha256:b", "abc", "ratified", "2026-08-08", ""],
            ["ATT-003", "SR-003", "not-a-digest", "abc", "ratified", "2026-08-08", ""],
            ["ATT-004", "SR-004", "sha256:d", "abc", "guessed", "2026-08-08", ""],
            ["ATT-005", "", "sha256:e", "abc", "ratified", "2026-08-08", ""],
        ],
    )
    findings = " | ".join(ct.attestation_integrity_findings(root))
    assert "duplicate ledger id" in findings
    assert "not a sha256" in findings
    assert "is not one of" in findings
    assert "names no Artifact" in findings


def test_the_ledger_is_append_only(tmp_path):
    import subprocess

    root = tmp_path / "repo"
    root.mkdir()
    for args in (
        ["init", "-q"],
        ["config", "user.email", "t@example.com"],
        ["config", "user.name", "T"],
        ["config", "commit.gpgsign", "false"],
    ):
        subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    _ledger(root, [["ATT-001", "SR-001", "sha256:a", "abc", "ratified", "2026-08-08", ""]])
    subprocess.run(["git", "-C", str(root), "add", "-A"], capture_output=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "ledger"], capture_output=True)

    # APPENDING is fine.
    _ledger(
        root,
        [
            ["ATT-001", "SR-001", "sha256:a", "abc", "ratified", "2026-08-08", ""],
            ["ATT-002", "SR-002", "sha256:b", "def", "clarity", "2026-08-08", ""],
        ],
    )
    subprocess.run(["git", "-C", str(root), "add", "-A"], capture_output=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "append"], capture_output=True)
    assert ct.staged_attestation_rewrite_findings(root, "HEAD~1", "HEAD") == []

    # REWRITING an earlier row is not.
    _ledger(
        root,
        [
            ["ATT-001", "SR-001", "sha256:REWRITTEN", "abc", "ratified", "2026-08-08", ""],
            ["ATT-002", "SR-002", "sha256:b", "def", "clarity", "2026-08-08", ""],
        ],
    )
    subprocess.run(["git", "-C", str(root), "add", "-A"], capture_output=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "rewrite"], capture_output=True)
    findings = ct.staged_attestation_rewrite_findings(root, "HEAD~1", "HEAD")
    assert len(findings) == 1 and "REWRITTEN, not appended" in findings[0]


# --- the writer ----------------------------------------------------------------


def test_record_attestations_appends_and_never_rewrites(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    _spine(root)
    first = intake.record_attestations(root, ["SR-001"], "ratified")
    assert first == ["ATT-001"]
    assert ct.attestation_findings(root) == []

    second = intake.record_attestations(root, ["SN-001"], "ratified", ref="WI-999")
    assert second == ["ATT-002"]
    rows = ct.read_attestations(root)
    assert [r["ATT-ID"] for r in rows] == ["ATT-001", "ATT-002"]
    assert rows[1]["Ref"] == "WI-999"
    assert ct.attestation_integrity_findings(root) == []


def test_the_writer_refuses_an_artifact_with_no_normative_text(tmp_path, capsys):
    root = tmp_path / "repo"
    root.mkdir()
    _spine(root)
    assert intake.record_attestations(root, ["SR-999"], "ratified") == []
    assert "no normative text" in capsys.readouterr().err


def test_the_writer_refuses_an_unknown_decision(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    _spine(root)
    assert intake.record_attestations(root, ["SR-001"], "probably-fine") == []


def test_the_shipped_template_is_a_valid_empty_ledger():
    # The blank form an adopter copies must itself pass every rule, or the
    # first thing a fresh scaffold does is fail its own integrity check.
    template = KIT / "registries" / "attestations.template.csv"
    with template.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    assert [r["ATT-ID"] for r in rows] == ["ATT-000"], "one inert -000 exemplar"
    assert rows[0]["Decision"] in ct.ATTESTATION_DECISIONS


def test_this_repos_own_ledger_is_shaped_correctly():
    # Dogfood: whatever this repo carries must satisfy the rules it ships.
    assert ct.attestation_integrity_findings(ROOT) == []
