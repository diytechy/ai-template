"""A work item cites the open item it waits on (WI-790; TC-301).

The `OI-###` token in a row's `needs` is the one edge between a work item and
an owner decision: the row reads `blocked`, the item named, until the item
leaves `pending`, and the open item carries no pointer back. An open item's
historical `wi_refs` cell is read by nothing.
"""

from copy import deepcopy

from conftest import SCRIPTS, load_script, run_py

sched = load_script("schedule")
ct = load_script("check_trajectory")
status = load_script("traj_status")
panels = load_script("gen_trajectory").traj_panels

OI = "docs/requirements/open-items.toml"


def _spec(root, wid, where="queued", **front):
    lines = ['id = "{}"'.format(wid), 'title = "{} title"'.format(wid)]
    front.setdefault("safety_class", "ordinary")
    for key, value in front.items():
        if isinstance(value, list):
            value = "[{}]".format(", ".join('"{}"'.format(v) for v in value))
        else:
            value = '"{}"'.format(value)
        lines.append("{} = {}".format(key, value))
    path = root / "docs/work" / where / "{}-test.md".format(wid)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("+++\n" + "\n".join(lines) + "\n+++\n", encoding="utf-8")
    return path


def _items(root, *rows):
    """Open-item rows as `(id, status)` or `(id, status, extra-toml)`."""
    text = "".join(
        '[open_item.{}]\ntitle = "{} title"\nstatus = "{}"\n{}\n'.format(
            r[0], r[0], r[1], r[2] if len(r) > 2 else ""
        )
        for r in rows
    )
    path = root / OI
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def repo(root, state="pending"):
    _items(root, ("OI-98", state))
    _spec(root, "WI-684", needs=["OI-98"], exclusive=["shared"])
    _spec(root, "WI-688", exclusive=["shared"])


def _records(root):
    return {
        r["id"]: r
        for r in sched.evaluate(sched._load(root), oi_status=sched.load_oi_status(root))
    }


def _frontier(root):
    return [
        r["id"]
        for r in sched.frontier(sched._load(root), oi_status=sched.load_oi_status(root))
    ]


def test_a_cited_pending_item_blocks_and_its_ruling_releases_the_row(tmp_path):
    repo(tmp_path)
    path = tmp_path / "docs/work/queued/WI-684-test.md"
    before = path.read_bytes()
    wis = sched._load(tmp_path)
    original = deepcopy(wis)
    oi_status = sched.load_oi_status(tmp_path)
    # Not offered, and it steals no mutex from WI-688.
    assert _frontier(tmp_path) == ["WI-688"]
    held = _records(tmp_path)["WI-684"]
    assert held["status"] == "queued" and held["disposition"] == "blocked"
    assert held["reasons"] == ["blocked:open-item-pending:OI-98"]
    assert held["open_items"] == [{"id": "OI-98", "title": "OI-98 title"}]
    assert sched.simulate(wis, 2, oi_status=oi_status) == [["WI-688"]]
    assert wis == original
    _items(tmp_path, ("OI-98", "ruled"))
    assert _frontier(tmp_path) == ["WI-684"]
    assert _records(tmp_path)["WI-684"]["open_items"] == []
    assert path.read_bytes() == before  # readiness needs no edit to the row


def test_no_waiting_state_is_left_for_an_open_item_edge(tmp_path):
    # A row with both kinds of edge is blocked, the item named, and keeps its
    # work-item waiting reason; a row with only a work-item edge still waits.
    repo(tmp_path)
    _spec(tmp_path, "WI-690", needs=["OI-98", "WI-688"])
    _spec(tmp_path, "WI-691", needs=["WI-688"])
    records = _records(tmp_path)
    assert records["WI-690"]["disposition"] == "blocked"
    assert records["WI-690"]["reasons"] == [
        "blocked:open-item-pending:OI-98",
        "waiting:hard-preds-not-done:WI-688",
    ]
    assert records["WI-691"]["disposition"] == "waiting"
    assert not any(
        "open-item" in code
        for r in records.values()
        if r["disposition"] == "waiting"
        for code in r["reasons"]
    )


def test_a_missing_open_item_stays_unsatisfied_under_the_dangling_edge_error(tmp_path):
    repo(tmp_path)
    _spec(tmp_path, "WI-692", needs=["OI-404"])
    held = _records(tmp_path)["WI-692"]
    assert held["disposition"] == "blocked"
    assert held["reasons"] == ["blocked:open-item-unknown:OI-404"]
    wis = ct.load_wis(ct.read_registry_rows(tmp_path / ct.WI_CSV))[0]
    errors = ct.validate(wis, set(), ct.load_known_ois(tmp_path))
    assert any("WI-692" in e and "OI-404" in e for e in errors), errors


def test_frontier_and_snapshot_list_gates_apart(tmp_path):
    repo(tmp_path)
    frontier = "\n".join(status._frontier_lines(tmp_path))
    ready, blocked = frontier.split("- **Blocked**")
    assert "WI-688" in ready and "WI-684" not in ready
    assert "WI-684" in blocked
    assert "[OI-98" in blocked and "OI-98 title" in blocked
    assert "open-items.html#OI-98" in blocked
    assert frontier in status.status_block(tmp_path)
    _items(tmp_path, ("OI-98", "ruled"))
    assert "**Blocked**" not in "\n".join(status._frontier_lines(tmp_path))


def test_the_next_work_card_names_the_item_that_holds_a_row(tmp_path):
    repo(tmp_path)
    html = panels._next_work_html(tmp_path)
    assert "WI-688" in html and "WI-684" in html
    assert "held by" in html and "docs/open-items.html#OI-98" in html
    assert html.index("WI-688") < html.index("WI-684")  # ready work first


def test_a_historical_wi_refs_pointer_holds_nothing(tmp_path):
    # The retired reader: an open item's `wi_refs` naming a row no longer
    # blocks it, and no finding resolves the pointer.
    repo(tmp_path)
    _items(tmp_path, ("OI-98", "pending"), ("OI-99", "pending", 'wi_refs = ["WI-688"]'))
    assert _records(tmp_path)["WI-688"]["disposition"] == "ready"
    assert not hasattr(ct, "open_item_wi_ref_findings")


def test_worker_brief_does_not_offer_a_gated_row(tmp_path):
    repo(tmp_path)
    brief = load_script("agent_brief")
    text = brief.worker_prompt(tmp_path, {}, "WI-684", "lane", "HEAD")
    assert "BLOCKED" in text and "OI-98" in text
    assert "OI-98 title" in text
    assert "Worker assignment" not in text


def test_multiple_gates_all_have_to_be_ruled(tmp_path):
    repo(tmp_path)
    _items(tmp_path, ("OI-98", "pending"), ("OI-99", "pending"))
    _spec(tmp_path, "WI-684", needs=["OI-98", "OI-99"])
    assert len(_records(tmp_path)["WI-684"]["open_items"]) == 2
    _items(tmp_path, ("OI-98", "ruled"), ("OI-99", "pending"))
    held = _records(tmp_path)["WI-684"]
    assert held["disposition"] == "blocked"
    assert held["open_items"] == [{"id": "OI-99", "title": "OI-99 title"}]


def test_only_queued_rows_are_held_and_a_drained_frontier_still_lists_gates(tmp_path):
    repo(tmp_path)
    path = tmp_path / "docs/work/queued/WI-688-test.md"
    done = tmp_path / "docs/archive/work/complete"
    done.mkdir(parents=True)
    path.rename(done / path.name)
    text = "\n".join(status._frontier_lines(tmp_path))
    assert "**Ready frontier**" not in text
    assert "**Blocked**" in text and "WI-684" in text


def _check(root, *flags):
    return run_py([SCRIPTS / "check_trajectory.py", "--root", str(root), *flags], root)


def test_a_placeholder_row_passes_every_check_and_is_blocked(tmp_path):
    # The minimum: a title, a safety class, the `needs` token and a specref
    # naming the item's own registry record (which R-E resolves). No Done-when.
    _items(tmp_path, ("OI-5", "pending"))
    _spec(tmp_path, "WI-001", needs=["OI-5"], specref=OI + "#OI-5")
    proc = _check(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "ERROR" not in proc.stderr
    assert _records(tmp_path)["WI-001"]["disposition"] == "blocked"


def test_an_uncited_pending_item_is_an_error_even_with_no_work_items(tmp_path):
    # Evaluated before the "vacuously clean" return, and without --strict.
    _items(tmp_path, ("OI-5", "pending"), ("OI-6", "ruled"))
    proc = _check(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "OI-5: pending, but no queued work item cites it" in proc.stderr
    assert "OI-6" not in proc.stderr
    # A draft or deferred citer does not surface the decision either.
    _spec(tmp_path, "WI-001", where="deferred", needs=["OI-5"])
    proc = _check(tmp_path)
    assert proc.returncode == 1 and "OI-5: pending" in proc.stderr
    path = tmp_path / "docs/work/deferred/WI-001-test.md"
    queued = tmp_path / "docs/work/queued"
    queued.mkdir(parents=True)
    path.rename(queued / path.name)
    proc = _check(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_a_ruled_items_row_may_not_keep_the_registry_as_its_specref(tmp_path):
    _items(tmp_path, ("OI-5", "ruled"), ("OI-6", "pending"))
    _spec(tmp_path, "WI-001", needs=["OI-5", "OI-6"], specref=OI + "#OI-5")
    assert (
        ct.open_item_specref_findings(
            tmp_path, ct.load_wis(ct.read_registry_rows(tmp_path / ct.WI_CSV))[0]
        )
        == []
    )
    _items(tmp_path, ("OI-5", "ruled"), ("OI-6", "ruled"))
    proc = _check(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "WI-001: every open item it cites (OI-5, OI-6) is ruled" in proc.stderr


def test_a_needs_token_naming_no_open_item_is_reported(tmp_path):
    _items(tmp_path, ("OI-5", "pending"))
    _spec(tmp_path, "WI-001", needs=["OI-5"])
    _spec(tmp_path, "WI-002", needs=["OI-77"])
    proc = _check(tmp_path)
    assert proc.returncode == 1
    assert "WI-002: open-item predecessor 'OI-77' is not a minted open item" in (
        proc.stderr
    )


def test_a_registry_specref_must_name_an_item_the_row_cites(tmp_path):
    # Sol review 1, MAJOR 5 (LLR-299, A6): a placeholder citing pending OI-5
    # whose specref anchors OI-6 is an ERROR, as is the CSV carrier's spelling.
    _items(tmp_path, ("OI-5", "pending"), ("OI-6", "ruled"))
    _spec(tmp_path, "WI-001", needs=["OI-5"], specref=OI + "#OI-6")
    proc = _check(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "WI-001: its specref names OI-6, which its needs do not cite" in (
        proc.stderr
    )
    _spec(tmp_path, "WI-001", needs=["OI-5"], specref=OI + "#OI-5")
    assert _check(tmp_path).returncode == 0


def test_the_csv_carriers_registry_specref_is_judged_too(tmp_path):
    # Sol review 1, MAJOR 2: the state check reads the registry's stem.
    path = tmp_path / "docs/requirements/open-items.csv"
    path.parent.mkdir(parents=True)
    path.write_text("OI-ID,Title,Status\nOI-5,t,ruled\n", encoding="utf-8")
    _spec(
        tmp_path,
        "WI-001",
        needs=["OI-5"],
        specref="docs/requirements/open-items.csv#OI-5",
    )
    findings = ct.open_item_specref_findings(
        tmp_path, ct.load_wis(ct.read_registry_rows(tmp_path / ct.WI_CSV))[0]
    )
    assert (
        len(findings) == 1
        and "every open item it cites (OI-5) is ruled" in (findings[0])
    )
