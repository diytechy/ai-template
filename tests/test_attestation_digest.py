"""The attestation DIGEST — what survived the ledger (SN-029, then D-1).

`docs/requirements/attestations.csv` is retired (docs/repo-lock.md D-1, owner
ruling 2026-08-09): attestation STATE was always the row's own `Status`,
`derive_gate` computes the gate from those cells and never referenced the
ledger, and three of the ledger's seven columns duplicated cells the row already
carried. What it got right — a digest of the NORMATIVE text, recorded at
acceptance time, visible regardless of any `Status` movement — is kept, and its
home becomes the artifact's own row once the carrier question (OI-12) is ruled.

So this module tests the ENGINE, not a mechanism: what text a digest is taken
over, and that it moves when the obligation moves and not when bookkeeping does.

THE PREMISE IS DRIVEN, NOT ASSERTED. `test_the_amendment_seam_is_BLIND...`
reproduces the gap that makes an anchor necessary at all:
`check_trajectory.staged_spine_amendments` — the seam both the
amend-without-flip warn and the adjudication mint consume — drops a record when
the row's own Status is not `Verified` on both sides, OR when its owning SR is
flagged on the new side. Both exits are correct for what that seam is FOR, and
together they mean the SANCTIONED amendment (change the text, flip to
`Modified`, one commit) is invisible to both consumers. An SN is invisible by
every path, having no `Status` cell at all. If that test ever starts failing,
the anchor's whole justification has changed and it must be re-argued before
the anchor half is built.
"""

import pytest
from conftest import load_script

ct = load_script("check_trajectory")

SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,"
    "Priority,Verification,Status\n"
)


def _spine(root, requirement="the original text", status="Verified"):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    with (req / "system-requirements.csv").open(
        "w", encoding="utf-8", newline="\n"
    ) as fh:
        fh.write(
            SR_HEADER
            + 'SR-001,Adder,SN-001,"{}","why","ac",,M,Test,{}\n'.format(
                requirement, status
            )
            + 'SR-000,EXAMPLE,SN-000,"placeholder","why","ac",,M,Test,Draft\n'
        )
    with (req / "stakeholder-needs.md").open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(
            "# Needs\n\n## Core needs\n\n"
            "| SN-ID | Need | Why | Priority | Acceptance |\n"
            "|---|---|---|---|---|\n"
            "| SN-001 | The original need. | because | M | when it works |\n"
            "\nSN-002 is mentioned only in prose, never as a table row.\n"
        )
    return root


# --- what the digest is taken over ---------------------------------------------


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
    assert ct.sn_normative_text(spaced, "SN-001") == ct.sn_normative_text(
        text, "SN-001"
    )


def test_current_digests_covers_the_spine_AND_the_needs(tmp_path):
    # The one reader that joins both halves. It is what an anchor writer will
    # consume, so its COVERAGE is the property worth pinning: every real spine
    # row, every SN that is an actual table row, no `-000` example, and nothing
    # for an id that appears only in prose (`sn_normative_text` answers None,
    # and a digest of None would anchor a need that does not exist).
    root = tmp_path / "repo"
    root.mkdir()
    _spine(root)
    digests = ct.current_digests(root)

    assert set(digests) == {"SR-001", "SN-001"}, (
        "expected exactly the real spine row and the real need — got {}".format(
            sorted(digests)
        )
    )
    assert all(v.startswith("sha256:") for v in digests.values())
    assert "SR-000" not in digests and "SN-000" not in digests, "-000 is inert"
    assert "SN-002" not in digests, "a prose-only SN mention is not an anchorable row"

    # And it MOVES with the obligation: same reader, amended text, new digest.
    before = digests["SR-001"]
    _spine(root, requirement="the AMENDED text", status="Modified")
    assert ct.current_digests(root)["SR-001"] != before


# --- the premise: why an anchor is owed at all ---------------------------------


def test_the_amendment_seam_is_BLIND_to_an_amend_plus_flip(tmp_path):
    """The gap, driven rather than asserted. If this ever starts failing, the
    anchor's whole justification has changed and it should be re-argued before
    the anchor half is built on it."""
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
        "the seam is expected to be blind here — that blindness is why an "
        "anchor recorded at acceptance time is owed"
    )
    # The digest is NOT blind to it: same tree, same moment, the text moved.
    assert ct.current_digests(root)["SR-001"], "the anchor's engine still answers"
