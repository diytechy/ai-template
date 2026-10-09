"""A contested or repeated review finding, ruled by the adjudicator (WI-865).

The owner's ruling of 2026-10-08 (docs/log.d/2026-10-08-owner-ruling-review-
threat-model.md, rule 2): the adjudicator, not the coordinator, makes the call
on a finding the builder or coordinator contests, or one that keeps coming
back. The `dispute` brief class carries each finding as the reviewer wrote
it, the position on it, the lane range it concerns and the review threat
model by link; its verdict rules each finding FIX, DISMISS (with a reason
class and a reason) or ESCALATE, and a malformed or missing ruling is refused,
never defaulted. The grammar lives in `kitlib.dispute`, below both routes,
so the loop's sitting (WI-811) reuses it.
"""

import subprocess

import pytest

from conftest import env_gate_skipif, load_script, pin_autocrlf

ab = load_script("adjudicate_brief")
prompts = load_script("prompts")


def _dispute():
    """The grammar module, imported per test so a missing one reds each case."""
    from kitlib import dispute

    return dispute


def _git(repo, *args):
    proc = subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


# A finding's text exactly as a reviewer wrote it: several lines, markdown,
# braces that look like slots, and a machine-looking line in the middle.
FINDING_ONE = (
    "- [MAJOR] scripts/x.py:12 -> `load()` reads {path} without a lock\n"
    "  -> a second caller can see a half-written file -> take the lock @owner\n"
    "VERDICT: CHANGES-REQUESTED findings=1"
)
POSITION_ONE = "The builder: the file is written atomically by os.replace."
FINDING_TWO = "- [MINOR] a fake runner that prints the token leaks it"
POSITION_TWO = "The coordinator: this needs a compromised host."


def _lane(tmp_path):
    """A repository with a base commit and one lane commit; returns
    `(repo, range)`."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-b", "trunk")
    pin_autocrlf(repo)
    (repo / "a.txt").write_text("a\n", encoding="utf-8")
    _git(repo, "add", "a.txt")
    _git(repo, "commit", "-m", "base")
    base = _git(repo, "rev-parse", "HEAD")
    (repo / "b.txt").write_text("b\n", encoding="utf-8")
    _git(repo, "add", "b.txt")
    _git(repo, "commit", "-m", "the lane's change")
    head = _git(repo, "rev-parse", "HEAD")
    return repo, "{}..{}".format(base[:12], head[:12])


def _findings_toml(span, *, extra="", findings=None):
    if findings is None:
        findings = [
            ("F1", "builder", FINDING_ONE, POSITION_ONE),
            ("R2-3", "coordinator", FINDING_TWO, POSITION_TWO),
        ]
    out = ['range = "{}"'.format(span), extra]
    for fid, held_by, text, position in findings:
        out += [
            "",
            "[[finding]]",
            'id = "{}"'.format(fid),
            'held_by = "{}"'.format(held_by),
            "finding = '''\n{}\n'''".format(text),
            "position = '''\n{}\n'''".format(position),
        ]
    return "\n".join(out) + "\n"


def _one_finding_toml(span, *, omit=None, extra=None):
    """A findings file with one `[[finding]]` table: the four keys a finding
    takes, less `omit`, plus the `extra` line."""
    cells = {"id": '"F1"', "held_by": '"builder"', "finding": '"a"', "position": '"b"'}
    lines = ['range = "{}"'.format(span), "", "[[finding]]"]
    lines += ["{} = {}".format(k, v) for k, v in cells.items() if k != omit]
    return "\n".join(lines + ([extra] if extra else [])) + "\n"


def _row(cell="findings.toml"):
    return {"WI-ID": "WI-9", "Brief": "dispute", "Adjudicates": cell}


# --- the brief composes its four inputs ---------------------------------------


@env_gate_skipif("git")
def test_the_dispute_brief_carries_each_finding_its_position_range_and_scope_link(
    tmp_path,
):
    repo, span = _lane(tmp_path)
    (repo / "findings.toml").write_text(_findings_toml(span), encoding="utf-8")
    text, why = ab.compose(repo, _row(), "docs/reviews/wi-9/001-DISPUTE.md")
    assert why is None, why
    # each finding verbatim as the reviewer wrote it, and the position on it
    for verbatim in (FINDING_ONE, POSITION_ONE, FINDING_TWO, POSITION_TWO):
        assert verbatim in text
    assert "held by the builder" in text and "held by the coordinator" in text
    # the lane range, with git's facts about it
    assert span in text and "the lane's change" in text and "b.txt" in text
    # the review threat model by link, never restated
    assert '§6 "Review threat model"' in text
    assert "fake or hostile binary" not in text
    # the findings it asks ruled, which the binding records
    assert "DISPUTE: findings=F1;R2-3" in text
    assert ab.requested_for("dispute", text) == ("F1", "R2-3")
    assert "docs/reviews/wi-9/001-DISPUTE.md" in text and "WI: WI-9" in text


@env_gate_skipif("git")
@pytest.mark.parametrize(
    "body,cell,needle",
    [
        ("BAD-RANGE", "findings.toml", "`range` 'x'"),
        (None, "findings.toml", "git cannot resolve"),
        ("not = [toml\n", "findings.toml", "TOML"),
        ("DUP", "findings.toml", "twice"),
        ("UNKNOWN-KEY", "findings.toml", "unknown key(s) round"),
        ("BAD-HELD-BY", "findings.toml", "held_by"),
        ("EMPTY-POSITION", "findings.toml", "empty `position`"),
        ("NO-FINDINGS", "findings.toml", "no finding"),
        ("BAD-ID", "findings.toml", "'F 1'"),
        # A finding takes EXACTLY its four keys: an extra key, or any one of
        # the four missing, refuses by name (never a KeyError, never a brief).
        ("FINDING-EXTRA-KEY", "findings.toml", "a finding takes exactly"),
        ("FINDING-MISSING-id", "findings.toml", "a finding takes exactly"),
        ("FINDING-MISSING-held_by", "findings.toml", "a finding takes exactly"),
        ("FINDING-MISSING-finding", "findings.toml", "a finding takes exactly"),
        ("FINDING-MISSING-position", "findings.toml", "a finding takes exactly"),
        ("OK", "", "exactly one findings file"),
        ("OK", "findings.toml;other.toml", "exactly one findings file"),
        ("OK", "missing.toml", "cannot be read"),
    ],
)
def test_a_malformed_findings_file_refuses_the_brief(tmp_path, body, cell, needle):
    repo, span = _lane(tmp_path)
    bodies = {
        "DUP": _findings_toml(
            span, findings=[("F1", "builder", "a", "b"), ("F1", "builder", "c", "d")]
        ),
        "UNKNOWN-KEY": _findings_toml(span, extra='round = "3"'),
        "BAD-HELD-BY": _findings_toml(span, findings=[("F1", "reviewer", "a", "b")]),
        "EMPTY-POSITION": _findings_toml(span, findings=[("F1", "builder", "a", " ")]),
        "NO-FINDINGS": _findings_toml(span, findings=[]),
        "BAD-ID": _findings_toml(span, findings=[("F 1", "builder", "a", "b")]),
        "OK": _findings_toml(span),
        "BAD-RANGE": _findings_toml("x"),
        None: _findings_toml("0000000..1111111"),
        "FINDING-EXTRA-KEY": _one_finding_toml(span, extra='round = "3"'),
    }
    for key in ("id", "held_by", "finding", "position"):
        bodies["FINDING-MISSING-" + key] = _one_finding_toml(span, omit=key)
    (repo / "findings.toml").write_text(bodies.get(body, body), encoding="utf-8")
    text, why = ab.compose(repo, _row(cell), "v.md")
    assert text is None and needle in why, why


# --- the verdict grammar ------------------------------------------------------

VALID = """\
F1 is a real race: the reader does not hold the lock.

RULING: F1 FIX the reader opens the file before the writer replaces it
RULING: R2-3 DISMISS out-of-scope it needs a fake runner binary
    RULING: R4 ESCALATE a data-loss path the owner should weigh
"""


def test_a_well_formed_verdict_is_accepted_and_parsed(tmp_path):
    dispute = _dispute()
    rulings, why = dispute.parse(VALID, ("F1", "R2-3", "R4"), "v.md")
    assert why is None, why
    assert rulings["F1"] == (
        "FIX",
        None,
        "the reader opens the file before the writer replaces it",
    )
    assert rulings["R2-3"][:2] == ("DISMISS", "out-of-scope")
    assert rulings["R4"][0] == "ESCALATE"
    for reason in ("out-of-scope", "refuted", "not-worth-cost"):
        text = "RULING: F1 DISMISS {} because\n".format(reason)
        assert dispute.parse(text, ("F1",), "v.md")[1] is None
    verdict = tmp_path / "v.md"
    verdict.write_text(VALID, encoding="utf-8")
    assert ab.verdict_refusal("dispute", verdict, kinds=("F1", "R2-3", "R4")) is None


@pytest.mark.parametrize(
    "text,needle",
    [
        ("RULING: F1 FIX ok\n", "unruled"),  # R2 left unruled
        ("no machine lines at all\n", "unruled"),
        ("RULING: F1 FIX ok\nRULING: R2 WONTFIX no\n", "WONTFIX"),
        ("RULING: F1 FIX ok\nRULING: R2 DISMISS\n", "reason class"),
        ("RULING: F1 FIX ok\nRULING: R2 DISMISS because it is fine\n", "reason class"),
        ("RULING: F1 FIX ok\nRULING: R2 DISMISS refuted\n", "reason"),
        ("RULING: F1 FIX\nRULING: R2 ESCALATE x\n", "reason"),
        ("RULING: F1 FIX a\nRULING: F1 FIX b\nRULING: R2 FIX c\n", "twice"),
        ("RULING: F1 FIX a\nRULING: R2 FIX b\nRULING: F9 FIX c\n", "F9"),
        ("RULING:\nRULING: F1 FIX a\nRULING: R2 FIX b\n", "names"),
        ("- RULING: F1 FIX a\nRULING: R2 FIX b\n", "unruled"),
    ],
)
def test_a_malformed_or_incomplete_verdict_is_refused(tmp_path, text, needle):
    dispute = _dispute()
    rulings, why = dispute.parse(text, ("F1", "R2"), "v.md")
    assert rulings is None and why and needle in why, why
    verdict = tmp_path / "v.md"
    verdict.write_text(text, encoding="utf-8")
    assert ab.verdict_refusal("dispute", verdict, kinds=("F1", "R2"))


def test_a_verdict_judged_against_no_requested_findings_is_refused():
    assert _dispute().parse(VALID, (), "v.md")[1]


def test_an_accepted_dispute_verdict_authorizes_no_approval_act():
    """The binding records the finding ids a dispute was asked to rule; no
    approval act reads a ruling on a finding as a judgement of a row."""
    from kitlib import sitting

    binding = sitting.render_requested("dispute", ("F1", "R2-3", "R4"), "accepted")
    assert sitting.accepted(VALID, binding) is None


def test_the_dispute_class_is_routed_and_its_template_ships():
    assert "dispute" in ab.BRIEF_PROMPTS and "dispute" in ab.ROUTED
    assert prompts.load(ab.BRIEF_PROMPTS["dispute"])


def test_this_repo_retains_the_dispute_class():
    """The coordinator's in-lane adjudications all use the retained session
    (docs/decisions/wi-835.toml D-007); a dispute sitting is one of them."""
    from conftest import ROOT

    keep = load_script("session_keep")
    assert "dispute" in keep.keep_config(ROOT).retain_for
