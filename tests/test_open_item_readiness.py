"""The registry-owned readiness gate and its projections (TC-301/TC-302)."""

from copy import deepcopy

import pytest

from conftest import load_script

sched = load_script("schedule")
ct = load_script("check_trajectory")
status = load_script("traj_status")


def repo(root, state="pending"):
    req = root / "docs/requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "open-items.toml").write_text(
        f'[open_item.OI-98]\ntitle = "Owner release"\nstatus = "{state}"\n'
        'wi_refs = ["WI-684"]\n',
        encoding="utf-8",
    )
    work = root / "docs/work/queued"
    work.mkdir(parents=True, exist_ok=True)
    for wid in ("WI-684", "WI-688"):
        (work / f"{wid}-test.md").write_text(
            f'+++\nid = "{wid}"\ntitle = "{wid} title"\n'
            'workstream = "process"\nsr_refs = []\nneeds = []\n'
            'safety_class = "ordinary"\nexclusive = ["shared"]\n+++\n',
            encoding="utf-8",
        )


def test_pending_gate_lifts_without_editing_the_work_item(tmp_path):
    repo(tmp_path)
    path = tmp_path / "docs/work/queued/WI-684-test.md"
    before = path.read_bytes()
    wis = sched._load(tmp_path)
    original = deepcopy(wis)
    assert [r["id"] for r in sched.frontier(wis)] == ["WI-688"]
    held = next(r for r in sched.evaluate(wis) if r["id"] == "WI-684")
    assert held["status"] == "queued"
    assert held["disposition"] == "blocked"
    assert held["open_items"] == [{"id": "OI-98", "title": "Owner release"}]
    assert sched.simulate(wis, 2) == [["WI-688"]]
    assert wis == original
    repo(tmp_path, "ruled")
    assert [r["id"] for r in sched.frontier(sched._load(tmp_path))] == ["WI-684"]
    assert path.read_bytes() == before


def test_frontier_and_snapshot_list_gates_apart(tmp_path):
    repo(tmp_path)
    frontier = "\n".join(status._frontier_lines(tmp_path))
    ready, blocked = frontier.split("- **Blocked**")
    assert "WI-688" in ready and "WI-684" not in ready
    assert "WI-684" in blocked
    assert "[OI-98" in blocked and "Owner release" in blocked
    assert "open-items.html#OI-98" in blocked
    assert frontier in status.status_block(tmp_path)
    repo(tmp_path, "ruled")
    assert "**Blocked**" not in "\n".join(status._frontier_lines(tmp_path))


@pytest.mark.parametrize("state", ["pending", "ruled"])
def test_dangling_wi_refs_are_findings(tmp_path, state):
    repo(tmp_path, state)
    path = tmp_path / "docs/requirements/open-items.toml"
    path.write_text(path.read_text().replace("WI-684", "WI-999"), encoding="utf-8")
    findings = ct.open_item_wi_ref_findings(
        tmp_path, ct.load_wis(ct.read_spec_rows(tmp_path / "docs/work"))[0]
    )
    assert len(findings) == 1
    assert "OI-98" in findings[0] and "WI-999" in findings[0]


@pytest.mark.parametrize("state", ["pending", "ruled"])
def test_example_wi_refs_are_inert(tmp_path, state):
    repo(tmp_path, state)
    path = tmp_path / "docs/requirements/open-items.toml"
    path.write_text(
        path.read_text().replace('"WI-684"', '"WI-000", "WI-999"'),
        encoding="utf-8",
    )
    findings = ct.open_item_wi_ref_findings(tmp_path, [])
    assert findings == ["OI-98: wi_refs names unknown work item WI-999"]


def test_examples_and_absent_registry_are_inert(tmp_path):
    repo(tmp_path)
    path = tmp_path / "docs/requirements/open-items.toml"
    path.write_text(path.read_text().replace("OI-98", "OI-000"), encoding="utf-8")
    assert sched.frontier(sched._load(tmp_path))[0]["id"] == "WI-684"
    assert ct.open_item_wi_ref_findings(tmp_path, []) == []
    path.unlink()
    assert ct.open_item_wi_ref_findings(tmp_path, []) == []
    assert sched.frontier(sched._load(tmp_path))[0]["id"] == "WI-684"


def test_worker_brief_does_not_offer_a_gated_row(tmp_path):
    repo(tmp_path)
    brief = load_script("agent_brief")
    text = brief.worker_prompt(tmp_path, {}, "WI-684", "lane", "HEAD")
    assert "BLOCKED" in text and "OI-98" in text
    assert "Owner release" in text
    assert "Worker assignment" not in text


def test_multiple_gates_all_have_to_be_ruled(tmp_path):
    repo(tmp_path)
    path = tmp_path / "docs/requirements/open-items.toml"
    with path.open("a", encoding="utf-8") as fh:
        fh.write(
            '\n[open_item.OI-99]\ntitle = "Second release"\nstatus = "pending"\nwi_refs = ["WI-684"]\n'
        )
    assert len(sched.evaluate(sched._load(tmp_path))[0]["open_items"]) == 2
    path.write_text(
        path.read_text().replace('status = "pending"', 'status = "ruled"', 1),
        encoding="utf-8",
    )
    held = next(r for r in sched.evaluate(sched._load(tmp_path)) if r["id"] == "WI-684")
    assert held["disposition"] == "blocked"
    assert held["open_items"] == [{"id": "OI-99", "title": "Second release"}]


def test_only_queued_rows_are_held_and_a_drained_frontier_still_lists_gates(tmp_path):
    repo(tmp_path)
    path = tmp_path / "docs/work/queued/WI-688-test.md"
    active = tmp_path / "docs/work/active/lane"
    active.mkdir(parents=True)
    path.rename(active / path.name)
    oi = tmp_path / "docs/requirements/open-items.toml"
    oi.write_text(
        oi.read_text(encoding="utf-8").replace(
            'wi_refs = ["WI-684"]', 'wi_refs = ["WI-684", "WI-688"]'
        ),
        encoding="utf-8",
    )
    records = {r["id"]: r for r in sched.evaluate(sched._load(tmp_path))}
    assert records["WI-688"]["status"] == "active"
    assert records["WI-688"]["disposition"] != "blocked"
    path = active / path.name
    done = tmp_path / "docs/archive/work/complete"
    done.mkdir(parents=True)
    path.rename(done / path.name)
    text = "\n".join(status._frontier_lines(tmp_path))
    assert "**Ready frontier**" not in text
    assert "**Blocked**" in text and "WI-684" in text
    assert (
        ct.open_item_wi_ref_findings(
            tmp_path, ct.load_wis(ct.read_spec_rows(tmp_path / "docs/work"))[0]
        )
        == []
    )
