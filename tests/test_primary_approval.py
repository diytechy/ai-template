"""Primary approval payload parsing and read-only projection."""

import subprocess
from pathlib import Path

import pytest

from conftest import load_script
from kitlib import verdict as KV

PA = load_script("primary_approval")

REGISTRY = "docs/requirements/low-level-requirements.toml"
SPEC = "docs/work/queued/WI-1.md"
ROW = "LLR-001"


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


def _registry(status="Drafted"):
    return """[design.LLR-001]
title = "row"
detail = "detail"
rationale = "why"
status = "{}"
""".format(status)


def _spec(payload="", brief=""):
    return '+++\nid = "WI-1"\n{}+++\n\n{}'.format(
        'brief = "{}"\n'.format(brief) if brief else "", payload
    )


def _payload(
    base,
    proposal,
    blob,
    evidence,
    classification="return",
    row=ROW,
    absorption="",
    impact="",
):
    return """## Approval

```toml
version = 1
turn = "WI-1-{}"
base = "{}"
proposal = "{}"

[[decision]]
registry = "{}"
row = "{}"
classification = "{}"
before = {{ Detail = "{}" }}
after = {{ Detail = "{}" }}
evidence = ["{}"]
{}\n{}\n```
""".format(
        base,
        base,
        proposal,
        REGISTRY,
        row,
        classification,
        blob,
        blob,
        evidence,
        absorption,
        impact,
    )


def _fixture(
    tmp_path,
    *,
    classification="return",
    row=ROW,
    log=False,
    absorption="",
    brief="",
    human_level="DevStg-Below",
    review_rounds=0,
    status="Drafted",
    history=False,
    impact="",
    impact_builder=None,
):
    root = tmp_path / "repo"
    (root / Path(REGISTRY).parent).mkdir(parents=True)
    (root / Path(SPEC).parent).mkdir(parents=True)
    (root / "docs/process.toml").write_text(
        '[attestation]\nhuman_approval_through = "{}"\n'.format(human_level),
        encoding="utf-8",
    )
    (root / "docs/review-policy").write_text(
        str(review_rounds) + "\n", encoding="utf-8"
    )
    (root / REGISTRY).write_text(_registry(status), encoding="utf-8")
    (root / SPEC).write_text(_spec(brief=brief), encoding="utf-8")
    if history:
        (root / "src").mkdir()
        (root / "src/use.py").write_text("# LLR-001 live use\n", encoding="utf-8")
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.invalid")
    _git(root, "config", "user.name", "T")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "base")
    base = _git(root, "rev-parse", "HEAD")
    blob = _git(root, "rev-parse", "HEAD:" + REGISTRY)
    proposal = KV.tree_identity(root, base)
    record = root / "docs/reviews/primary-decision.md"
    record.parent.mkdir(parents=True, exist_ok=True)
    outcome = "RETURN" if classification in {"return", "uncertain"} else "REVIEWED"
    if brief == "consolidate":
        outcome = "QUEUE needs=- absorbs=-"
    record.write_text(
        "OUTCOME: {}\ncommitted judgment\n".format(outcome), encoding="utf-8"
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "judgment record")
    judgment = _git(root, "rev-parse", "HEAD")
    if impact_builder:
        impact = impact_builder(root, base, proposal, blob, judgment)
    (root / SPEC).write_text(
        _spec(
            _payload(
                base,
                proposal,
                blob,
                judgment,
                classification,
                row,
                absorption,
                impact,
            ),
            brief,
        ),
        encoding="utf-8",
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "reviewed payload")
    candidate = _git(root, "rev-parse", "HEAD")
    log_path = root / "docs/iteration/primary-1.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        "# phase: ADJUDICATE\n# wi: WI-1\n# provider: provider\n"
        "# roster-row: route-1\n# model: model-1\n# session-id: session\n"
        "# invocation-id: invoke\n# base: {}\n# primary-turn: WI-1-{}\n"
        "# judgment: docs/reviews/primary-decision.md\n# candidate: {}\n# ---\n".format(
            base[:12], base, candidate
        ),
        encoding="utf-8",
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "adjudicate telemetry")
    turn = {
        "version": 1,
        "turn": "WI-1-" + base,
        "wi": "WI-1",
        "base": base,
        "primary_branch": "main",
        "primary_root": "repo-id",
        "proposal_spec_blob": _git(root, "rev-parse", base + ":" + SPEC),
        "scope": [ROW],
        "registry_blobs": {REGISTRY: blob},
        "approved_blobs": {"docs/archive/last_approved/" + REGISTRY: blob},
        "spec": SPEC,
    }
    return root, turn


def test_return_is_a_finite_zero_write_projection(tmp_path):
    root, turn = _fixture(tmp_path)
    plan, refusal = PA.approval_projection(root, turn)

    assert refusal is None
    assert plan["outcome"] == "return"
    assert plan["statuses"] == {}
    assert plan["approves"] == {}
    assert plan["author"]["email"].endswith("@automation.invalid")


def test_uncertain_is_also_a_zero_write_projection(tmp_path):
    root, turn = _fixture(tmp_path, classification="uncertain")
    plan, refusal = PA.approval_projection(root, turn)

    assert refusal is None
    assert plan["outcome"] == "return"


def test_approve_derives_machine_author_only_from_adjudicate_log(tmp_path):
    root, turn = _fixture(tmp_path, classification="approve", log=True)
    plan, refusal = PA.approval_projection(root, turn)

    assert refusal is None
    assert plan["outcome"] == "publish"
    assert plan["statuses"] == {REGISTRY: {ROW: "Approved"}}
    assert len(plan["approves"][REGISTRY]) == 40
    assert plan["author"]["name"] == "AI adjudicator model-1"
    assert plan["author"]["email"].endswith("@automation.invalid")


def test_scope_and_unjudged_absorption_refuse(tmp_path):
    root, turn = _fixture(tmp_path, row="LLR-999")
    _plan, refusal = PA.approval_projection(root, turn)
    assert "outside the turn scope" in refusal

    absorption = """
[[absorption]]
registry = "docs/requirements/low-level-requirements.toml"
row = "LLR-001"
cells = { Detail = { before = "x", after = "y" } }
judgment = "UNJUDGED"
state = "approved-change"
"""
    root, turn = _fixture(
        tmp_path / "second", classification="approve", log=True, absorption=absorption
    )
    _plan, refusal = PA.approval_projection(root, turn)
    assert "UNJUDGED" in refusal


def test_equivalent_and_meaning_never_publish_from_this_turn(tmp_path):
    root, turn = _fixture(
        tmp_path / "equivalent", classification="equivalent", log=True
    )
    _plan, refusal = PA.approval_projection(root, turn)
    assert "retain Status=Approved" in refusal

    root, turn = _fixture(tmp_path / "meaning", classification="meaning")
    _plan, refusal = PA.approval_projection(root, turn)
    assert "impact census" in refusal


def _meaning_impact(root, base, _proposal, registry_blob, judgment, variant):
    """Exact tracked uses, with one deliberate census defect when requested."""
    entries = [
        (REGISTRY, registry_blob),
        (SPEC, _git(root, "rev-parse", base + ":" + SPEC)),
        ("src/use.py", _git(root, "rev-parse", base + ":src/use.py")),
    ]
    if variant == "missing":
        entries.pop()
    elif variant == "extra":
        entries.append(
            ("docs/process.toml", _git(root, "rev-parse", base + ":docs/process.toml"))
        )
    elif variant == "wrongblob":
        entries[-1] = ("src/use.py", registry_blob)
    return "\n".join(
        """[[impact]]
id = "LLR-001"
path = "{}"
source_blob = "{}"
disposition = "amend"
evidence = ["{}"]""".format(path, blob, judgment)
        for path, blob in entries
    )


@pytest.mark.parametrize(
    ("variant", "expected"),
    [
        ("valid", None),
        ("missing", "impact entries do not equal"),
        ("extra", "impact entries do not equal"),
        ("wrongblob", "impact source blob changed"),
    ],
)
def test_meaning_projection_requires_exact_real_git_impact_census(
    tmp_path, variant, expected
):
    root, turn = _fixture(
        tmp_path,
        classification="meaning",
        status="Approved",
        history=True,
        impact_builder=lambda *args: _meaning_impact(*args, variant),
    )

    plan, refusal = PA.approval_projection(root, turn)

    if expected:
        assert plan is None
        assert expected in refusal
    else:
        assert refusal is None
        assert plan["outcome"] == "publish"
        assert plan["statuses"] == {}
        assert plan["approves"] == {REGISTRY: _git(root, "rev-parse", "HEAD~2")}


def test_meaning_impact_treats_live_approved_snapshot_as_publication_carrier(
    tmp_path,
):
    def impact_with_snapshot(root, base, _proposal, registry_blob, judgment):
        snapshot_path = (
            "docs/archive/last_approved/docs/requirements/low-level-requirements.toml"
        )
        snapshot = root / snapshot_path
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_text("# LLR-001 live approved snapshot\n", encoding="utf-8")
        snapshot_blob = _git(root, "hash-object", str(snapshot))
        entries = [
            (REGISTRY, registry_blob, "amend"),
            (SPEC, _git(root, "rev-parse", base + ":" + SPEC), "amend"),
            ("src/use.py", _git(root, "rev-parse", base + ":src/use.py"), "amend"),
            (snapshot_path, snapshot_blob, "history-unchanged"),
        ]
        return "\n".join(
            """[[impact]]
id = "LLR-001"
path = "{}"
source_blob = "{}"
disposition = "{}"
evidence = ["{}"]""".format(path, blob, disposition, judgment)
            for path, blob, disposition in entries
        )

    root, turn = _fixture(
        tmp_path,
        classification="meaning",
        status="Approved",
        history=True,
        impact_builder=impact_with_snapshot,
    )
    _plan, refusal = PA.approval_projection(root, turn)
    assert "snapshot impact must use amend or regenerate" in refusal


@pytest.mark.parametrize(
    ("registry", "table", "main", "rider", "raw_cell", "cell"),
    [
        (
            "docs/requirements/stakeholder-needs.toml",
            "need",
            "SN-001",
            "SN-002",
            "need",
            "Need",
        ),
        (
            "docs/requirements/system-requirements.toml",
            "requirement",
            "SR-001",
            "SR-002",
            "requirement",
            "Requirement",
        ),
        (
            "docs/requirements/low-level-requirements.toml",
            "design",
            "LLR-001",
            "LLR-002",
            "detail",
            "Detail",
        ),
        ("docs/test/test-cases.toml", "test", "TC-001", "TC-002", "method", "Method"),
        (
            "docs/requirements/interfaces.toml",
            "interface",
            "IF-001",
            "IF-002",
            "data",
            "Data",
        ),
        (
            "docs/requirements/components.toml",
            "component",
            "CMP-001",
            "CMP-002",
            "notes",
            "Notes",
        ),
        (
            "docs/requirements/external.toml",
            "entity",
            "EXT-001",
            "EXT-002",
            "name",
            "Name",
        ),
        (
            "docs/requirements/external.toml",
            "boundary",
            "B-01",
            "B-02",
            "carries",
            "Carries",
        ),
        (
            "docs/requirements/external.toml",
            "relationship",
            "REL-001",
            "REL-002",
            "flow",
            "Flow",
        ),
    ],
)
def test_absorption_census_has_exact_blob_ledger_for_every_registry_carrier(
    tmp_path, registry, table, main, rider, raw_cell, cell
):
    root = tmp_path / "repo"
    path = root / registry
    path.parent.mkdir(parents=True)

    def carrier(main_value, rider_value):
        return """[{}.{}]
{} = "{}"
status = "Approved"

[{}.{}]
{} = "{}"
status = "Drafted"
""".format(
            table,
            main,
            raw_cell,
            main_value,
            table,
            rider,
            raw_cell,
            rider_value,
        )

    path.write_text(carrier("approved before", "rider before"), encoding="utf-8")
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.invalid")
    _git(root, "config", "user.name", "T")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "approved snapshot source")
    old_blob = _git(root, "rev-parse", "HEAD:" + registry)
    path.write_text(carrier("approved after", "rider after"), encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "candidate changes")
    new_blob = _git(root, "rev-parse", "HEAD:" + registry)
    turn = {"approved_blobs": {PA.snapshot.SNAPSHOT_DIR + "/" + registry: old_blob}}

    census = PA.absorption_census(root, turn, "HEAD", {(registry, main): {}})

    expected_cells = {cell: {"before": old_blob, "after": new_blob}}
    assert census == {
        (registry, main): {"state": "approved-change", "cells": expected_cells},
        (registry, rider): {
            "state": "below-approval-rider",
            "cells": expected_cells,
        },
    }


def test_human_held_scope_refuses_machine_publication(tmp_path):
    root, turn = _fixture(
        tmp_path, classification="approve", log=True, human_level="DevStg-Release"
    )

    _plan, refusal = PA.approval_projection(root, turn)

    assert "human-held" in refusal


def test_review_owed_candidate_requires_existing_independent_approve(tmp_path):
    root, turn = _fixture(tmp_path, brief="consolidate", review_rounds=1)

    _plan, refusal = PA.approval_projection(root, turn)

    assert "required independent review phases" in refusal


def test_parser_refuses_unknown_or_missing_approval_carrier():
    payload, why = PA.parse_approval_payload("## Approval\n\n```toml\nversion = 2\n```")
    assert payload is None
    assert "requires version=1" in why


def test_standing_snapshot_requires_complete_approved_absorption_ledger(tmp_path):
    """A first approval cannot re-anchor foreign approved drift by whole-file copy."""
    root = tmp_path / "standing"
    (root / Path(REGISTRY).parent).mkdir(parents=True)
    (root / Path(SPEC).parent).mkdir(parents=True)
    (root / "docs/archive/last_approved" / Path(REGISTRY).parent).mkdir(parents=True)
    (root / "docs/process.toml").write_text(
        '[attestation]\nhuman_approval_through = "DevStg-Below"\n', encoding="utf-8"
    )
    original = """[design.LLR-001]
title = "approved one"
detail = "one"
rationale = "why"
status = "Approved"

[design.LLR-002]
title = "approved two"
detail = "two"
rationale = "why"
status = "Approved"

[design.LLR-003]
title = "draft rider"
detail = "three"
rationale = "why"
status = "Drafted"
"""
    (root / REGISTRY).write_text(original, encoding="utf-8")
    (root / "docs/archive/last_approved" / REGISTRY).write_text(
        original, encoding="utf-8"
    )
    (root / SPEC).write_text(_spec(), encoding="utf-8")
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.invalid")
    _git(root, "config", "user.name", "T")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "standing snapshot")
    base = _git(root, "rev-parse", "HEAD")
    before = _git(root, "rev-parse", "HEAD:" + REGISTRY)
    proposal = KV.tree_identity(root, base)
    changed = (
        original.replace('detail = "one"', 'detail = "one amended"')
        .replace('detail = "two"', 'detail = "two foreign"')
        .replace('detail = "three"', 'detail = "three rider"')
    )
    (root / REGISTRY).write_text(changed, encoding="utf-8")
    (root / "docs/reviews/judgment.md").parent.mkdir(parents=True)
    (root / "docs/reviews/judgment.md").write_text("judgment\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "judgment")
    judgment = _git(root, "rev-parse", "HEAD")
    after = _git(root, "rev-parse", "HEAD:" + REGISTRY)
    decision = _payload(base, proposal, before, judgment, "approve", "LLR-003")
    decision = decision.replace(
        'after = { Detail = "' + before + '" }',
        'after = { Detail = "' + after + '" }',
    )
    # First show the exact foreign row is loud even though the scoped row is valid.
    (root / SPEC).write_text(_spec(decision), encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "candidate")
    turn = {
        "version": 1,
        "turn": "WI-1-" + base,
        "wi": "WI-1",
        "base": base,
        "primary_branch": "main",
        "primary_root": "repo-id",
        "proposal_spec_blob": _git(root, "rev-parse", base + ":" + SPEC),
        "scope": ["LLR-003"],
        "registry_blobs": {REGISTRY: before},
        "approved_blobs": {"docs/archive/last_approved/" + REGISTRY: before},
        "spec": SPEC,
    }
    _plan, refusal = PA.approval_projection(root, turn, require_provenance=False)
    assert "absorption ledger" in refusal
    assert after == _git(root, "rev-parse", "HEAD:" + REGISTRY)

    complete = _payload(base, proposal, before, judgment, "equivalent", "LLR-001")
    complete = (
        complete.replace(
            'after = { Detail = "' + before + '" }',
            'after = { Detail = "' + after + '" }',
        )
        .replace(
            "\n[[absorption]]",
            '''
[[decision]]
registry = "docs/requirements/low-level-requirements.toml"
row = "LLR-002"
classification = "equivalent"
before = { Detail = "'''
            + before
            + '''" }
after = { Detail = "'''
            + after
            + '''" }
evidence = ["'''
            + judgment
            + """"]

[[absorption]]""",
            1,
        )
        .replace(
            "\n```\n",
            '''
[[decision]]
registry = "docs/requirements/low-level-requirements.toml"
row = "LLR-002"
classification = "equivalent"
before = { Detail = "'''
            + before
            + '''" }
after = { Detail = "'''
            + after
            + '''" }
evidence = ["'''
            + judgment
            + '''"]

[[absorption]]
registry = "docs/requirements/low-level-requirements.toml"
row = "LLR-001"
cells = { Detail = { before = "'''
            + before
            + '''", after = "'''
            + after
            + '''" } }
judgment = "'''
            + judgment
            + '''"
state = "approved-change"

[[absorption]]
registry = "docs/requirements/low-level-requirements.toml"
row = "LLR-002"
cells = { Detail = { before = "'''
            + before
            + '''", after = "'''
            + after
            + '''" } }
judgment = "'''
            + judgment
            + '''"
state = "approved-change"

[[absorption]]
registry = "docs/requirements/low-level-requirements.toml"
row = "LLR-003"
cells = { Detail = { before = "'''
            + before
            + '''", after = "'''
            + after
            + '''" } }
judgment = "'''
            + judgment
            + """"
state = "below-approval-rider"
```
""",
        )
    )
    (root / SPEC).write_text(_spec(complete), encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "complete equivalent ledger")
    turn["scope"] = ["LLR-001", "LLR-002"]
    plan, refusal = PA.approval_projection(root, turn, require_provenance=False)
    assert refusal is None
    assert plan["statuses"] == {}
    assert plan["approves"] == {REGISTRY: judgment}
    assert 'status = "Drafted"' in (root / REGISTRY).read_text(encoding="utf-8")


def test_meaning_census_keeps_pre_turn_history_but_excludes_new_turn_carriers(tmp_path):
    """Evidence created for this turn is not an impact use; prior history remains one."""
    root = tmp_path / "impact"
    (root / "docs/reviews").mkdir(parents=True)
    (root / "docs/work/queued").mkdir(parents=True)
    (root / "src").mkdir()
    (root / "docs/reviews/old.md").write_text(
        "LLR-001 historical use\n", encoding="utf-8"
    )
    (root / "docs/work/queued/WI-1.md").write_text(
        "proposal LLR-001\n", encoding="utf-8"
    )
    (root / "src/use.py").write_text("# LLR-001 live use\n", encoding="utf-8")
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.invalid")
    _git(root, "config", "user.name", "T")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "base history")
    base = _git(root, "rev-parse", "HEAD")
    proposal_blob = _git(root, "rev-parse", "HEAD:docs/work/queued/WI-1.md")
    (root / "docs/reviews/new-primary-judgment.md").write_text(
        "LLR-001 current turn evidence\n", encoding="utf-8"
    )
    (root / "docs/iteration").mkdir()
    (root / "docs/iteration/primary.log").write_text(
        "LLR-001 telemetry\n", encoding="utf-8"
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "turn evidence")
    turn = {
        "base": base,
        "spec": "docs/work/queued/WI-1.md",
        "proposal_spec_blob": proposal_blob,
    }

    census = PA.impact_census(root, "HEAD", turn, {"LLR-001"})

    paths = {path for _rid, path in census}
    assert "src/use.py" in paths
    assert "docs/reviews/old.md" in paths
    assert "docs/reviews/new-primary-judgment.md" not in paths
    assert "docs/iteration/primary.log" not in paths
    assert census[("LLR-001", "docs/work/queued/WI-1.md")] == proposal_blob


@pytest.mark.parametrize(
    ("registry", "row_id", "cell"),
    [
        ("docs/requirements/stakeholder-needs.toml", "SN-001", "Need"),
        ("docs/requirements/system-requirements.toml", "SR-006", "Requirement"),
        ("docs/requirements/low-level-requirements.toml", "LLR-001", "Detail"),
        ("docs/test/test-cases.toml", "TC-001", "Method"),
        ("docs/requirements/interfaces.toml", "IF-001", "Data"),
        ("docs/requirements/components.toml", "CMP-006", "Name"),
        ("docs/requirements/external.toml", "EXT-001", "Name"),
        ("docs/requirements/external.toml", "B-01", "Carries"),
        ("docs/requirements/external.toml", "REL-001", "Flow"),
    ],
)
def test_registry_rows_reads_each_snapshotted_real_blob(registry, row_id, cell):
    root = Path(__file__).parents[1]
    blob = _git(root, "rev-parse", "HEAD:" + registry)

    rows = PA.registry_rows(root, blob, registry)

    assert row_id in rows
    assert rows[row_id][cell]
