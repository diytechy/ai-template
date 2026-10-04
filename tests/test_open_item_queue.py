"""The owner surface follows the queue (WI-790; IF-074, OI-102 Q2).

One queue projection, `kitlib.spine.open_item_queue`, feeds the owner
surface's cards and counts, its integrity notice, the status snapshot's
open-items and Blocked lists and the checker's uncited-pending error. A pending
open item shows only when a queued work item cites it in `needs`, beside the
rows it holds; a pending item no queued row cites is named in an integrity
notice instead, and the page then never claims the queue is empty.
"""

import re

from conftest import load_script

gen = load_script("gen_open_items")
pending = load_script("pending")
status = load_script("traj_status")
ct = load_script("check_trajectory")


def _queue(work, ois):
    kit = ct._kitspine
    return kit.open_item_queue(
        [{"WI-ID": w, "Status": s, "Predecessors": p} for w, s, p in work],
        [{"OI-ID": o, "Status": s, "Title": o + " title"} for o, s in ois],
    )


def test_the_projection_surfaces_only_what_a_queued_row_cites():
    queue = _queue(
        [
            ("WI-1", "queued", "OI-5;WI-9"),
            ("WI-2", "queued", "OI-5;OI-6"),
            ("WI-3", "deferred", "OI-7"),
            ("WI-4", "done", "OI-8"),
            ("WI-000", "queued", "OI-9"),
        ],
        [
            ("OI-5", "pending"),
            ("OI-6", "ruled"),
            ("OI-7", "pending"),
            ("OI-8", "pending"),
            ("OI-9", "pending"),
            ("OI-000", "pending"),
        ],
    )
    assert [(row["OI-ID"], citers) for row, citers in queue["cards"]] == [
        ("OI-5", ["WI-1", "WI-2"])
    ]
    # Cited only by a deferred, a closed or an example row: uncited.
    assert queue["uncited"] == ["OI-7", "OI-8", "OI-9"]
    assert queue["held"] == {"WI-1": ["OI-5"], "WI-2": ["OI-5"]}


def _spec(root, wid, needs=(), where="queued"):
    path = root / "docs/work" / where / "{}-row.md".format(wid)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '+++\nid = "{}"\ntitle = "{} row"\nneeds = [{}]\nsafety_class = "ordinary"\n'
        "+++\n".format(wid, wid, ", ".join('"{}"'.format(n) for n in needs)),
        encoding="utf-8",
    )


def _registry(root, rows):
    path = root / "docs/requirements/open-items.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(
            '[open_item.{o}]\ntitle = "{o} title"\nstatus = "{s}"\n'
            'one_line = "rule {o}"\n\n'.format(o=o, s=s)
            for o, s in rows
        ),
        encoding="utf-8",
    )


def _section1(root):
    page = gen.render(root)
    return page.split("1 · Pending decisions", 1)[1].split("2 · Approval", 1)[0]


def test_a_cited_pending_item_is_a_card_beside_the_rows_it_holds(tmp_path):
    _registry(tmp_path, [("OI-5", "pending")])
    _spec(tmp_path, "WI-001", ["OI-5"])
    section = _section1(tmp_path)
    assert 'id="OI-5"' in section and "WI-001" in section
    assert "Holds (queued work items citing it)" in section
    assert 'role="alert"' not in section
    assert "1 pending decision(s)" in gen.render(tmp_path)


def test_an_uncited_pending_item_is_a_notice_not_a_card(tmp_path):
    _registry(tmp_path, [("OI-5", "pending"), ("OI-6", "pending")])
    _spec(tmp_path, "WI-001", ["OI-5"])
    section = _section1(tmp_path)
    assert 'id="OI-6"' not in section  # not shown as a card
    notice = section.split('role="alert"', 1)[1].split("</p>", 1)[0]
    assert "OI-6" in notice and "OI-5" not in notice
    assert 'href="requirements/open-items.toml#OI-6"' in notice
    assert "0 pending decision(s)" not in gen.render(tmp_path)
    # ...and the checker reports it, from the same projection.
    rows = ct.read_registry_rows(tmp_path / ct.WI_CSV)
    findings = ct.uncited_open_item_findings(tmp_path, rows)
    assert len(findings) == 1 and findings[0].startswith("OI-6: pending")


def test_only_uncited_items_never_claim_an_empty_queue(tmp_path):
    _registry(tmp_path, [("OI-5", "pending")])
    section = _section1(tmp_path)
    assert "the owner queue is empty" not in section
    assert 'role="alert"' in section and "OI-5" in section
    _registry(tmp_path, [("OI-5", "ruled")])
    assert "the owner queue is empty" in _section1(tmp_path)


def test_the_status_snapshot_lists_the_same_projection(tmp_path):
    _registry(tmp_path, [("OI-5", "pending"), ("OI-6", "pending"), ("OI-7", "ruled")])
    _spec(tmp_path, "WI-001", ["OI-5"])
    block = status.status_block(tmp_path)
    assert "  - **OI-5** — rule OI-5 _(holds WI-001)_" in block
    assert "**OI-6**" not in block and "OI-7" not in block
    assert "no queued work item cites it" in block and "OI-6" in block
    blocked = block.split("- **Blocked**", 1)[1]
    assert "**WI-001**" in blocked and "[OI-5 — OI-5 title](open-items.html#OI-5)" in (
        blocked
    )


def test_the_projection_reads_the_queue_not_a_historical_pointer(tmp_path):
    path = tmp_path / "docs/requirements/open-items.toml"
    path.parent.mkdir(parents=True)
    path.write_text(
        '[open_item.OI-5]\ntitle = "t"\nstatus = "pending"\nwi_refs = ["WI-001"]\n',
        encoding="utf-8",
    )
    _spec(tmp_path, "WI-001")
    queue = pending.open_item_queue(tmp_path)
    assert queue["cards"] == [] and queue["uncited"] == ["OI-5"]


def test_decisions_to_review_is_the_pages_last_section(tmp_path):
    # LLR-118: the owner surface's sections run in a fixed order, and
    # Decisions to review is the last of them.
    page = gen.render(tmp_path)
    eyebrows = re.findall(
        r'<section class="band"[^>]*><p class="eyebrow">([^<]+)</p>', page
    )
    assert [e.split(" · ", 1)[0] for e in eyebrows] == ["1", "2", "3", "4"]
    assert eyebrows[-1] == "4 · Decisions to review"
