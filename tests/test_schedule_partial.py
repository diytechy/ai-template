"""`partial/` — the third terminal state, and the scheduler half of SR-151
(TC-170, LLR-176).

The requirement is that **an attempted work item never returns to the
frontier**. The previous machinery made that a matter of remembering: a
handed-back spec went back to `queued/` carrying a self-`blockref`, so the
scheduler saw it as *blocked*, and clearing that marker — a human act nobody
was gated on — put the same row back in play with its history overwritten by
the next try. Terminality on the READ side deletes the marker and the memory
together: `partial` is a status the loader produces, `_TERMINAL_DISPOSITION`
answers it before readiness is considered at all, and no rung below can return
`ready`.

Two claims are pinned here, and the second is the one that bites:

  * **the vocabulary is terminal** — `partial` sits in both `TERMINAL_STATUSES`
    tables and in neither `OPEN_STATUSES` nor the frontier;
  * **the directory is declared in ALL THREE readers** — `SPEC_STATUS_DIRS` is
    duplicated verbatim across `agent_common.py`, `schedule.py` and
    `check_trajectory.py` under the F5 rule, and a folder declared in two of the
    three is SKIPPED by the third: its specs never enter that reader's registry,
    so the duplicate-id guard and the dashboard go blind to the ids they hold
    (docs/concurrency-v2.md §B3). That failure is silent, which is why it is
    asserted directly rather than left to whichever consumer notices first.

The `successor` permutation's *admission transaction* belongs to `admit.py`
(LLR-178) and is not tested here. What IS this module's is the scheduler's half
of "ready only after admission": a candidate sitting in `draft/` is never on the
frontier, and the same spec becomes ready exactly when admission has moved it
to `queued/`.
"""

import pytest
from conftest import load_script

sched = load_script("schedule")
ctraj = load_script("check_trajectory")
acommon = load_script("agent_common")
wi_convert = load_script("wi_convert")

MODULES = (("schedule", sched), ("check_trajectory", ctraj), ("agent_common", acommon))


def spec_text(wid, title="Thing", order=0, deliverable="", **frontmatter):
    """One spec file's text in the format `scripts/wi_convert.py` emits (the
    tests/test_wi_folder_loaders.py shape, copied — no test module in this suite
    imports another)."""
    lines = ['id = "{}"'.format(wid), 'title = "{}"'.format(title)]
    for key, value in frontmatter.items():
        if isinstance(value, list):
            lines.append(
                "{} = [{}]".format(key, ", ".join('"{}"'.format(v) for v in value))
            )
        elif isinstance(value, int):
            lines.append("{} = {}".format(key, value))
        else:
            lines.append('{} = "{}"'.format(key, value))
    if order is not None:
        lines.append("order = {}".format(order))
    text = "+++\n" + "".join(line + "\n" for line in lines) + "+++\n"
    if deliverable:
        text += "\n## Deliverable\n\n" + deliverable + "\n"
    return text


def write_spec(root, where, wid, slug="thing", **kw):
    """Write `docs/work/<where>/<wid>-<slug>.md`; return its path.

    `newline="\\n"` explicitly: a fixture that takes the platform default cannot
    test the platform (the WI-337 lesson)."""
    path = root / "docs" / "work" / where / "{}-{}.md".format(wid, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(spec_text(wid, **kw), encoding="utf-8", newline="\n")
    return path


def dispositions(root):
    """`{id: (disposition, [reasons])}` for the spec folder under `root`."""
    rows = sched.read_spec_rows(root / "docs" / "work")
    return {
        r["id"]: (r["disposition"], r["reasons"])
        for r in sched.evaluate(sched.load_wis(rows))
    }


def ready_ids(root):
    rows = sched.read_spec_rows(root / "docs" / "work")
    return [r["id"] for r in sched.frontier(sched.load_wis(rows))]


# --- the three-copy declaration ----------------------------------------------


@pytest.mark.smoke
def test_the_three_readers_declare_the_same_status_directories():
    """The F5 drift guard aimed straight at the hazard: `SPEC_STATUS_DIRS` is
    three verbatim copies, and a folder added to two of them makes its specs
    invisible to the third reader rather than loudly wrong. Compared as whole
    tables, not just for the new key, because the next author adds a folder to
    the copy they happened to be editing."""
    tables = [(name, mod.SPEC_STATUS_DIRS) for name, mod in MODULES]
    reference = tables[0][1]
    for name, table in tables[1:]:
        assert table == reference, "{} has drifted from schedule".format(name)
    assert reference["partial"] == "partial"


@pytest.mark.smoke
def test_all_three_readers_see_a_partial_spec(tmp_path):
    """Declaration is not the claim — being READ is. `read_spec_rows` skips a
    file under a directory it does not know, so this drives the actual read."""
    write_spec(tmp_path, "partial", "WI-401", deliverable="Reached AC-1 only.")
    for name, mod in MODULES:
        rows = mod.read_spec_rows(tmp_path / "docs" / "work")
        assert [(r["WI-ID"], r["Status"]) for r in rows] == [("WI-401", "partial")], (
            name
        )


@pytest.mark.smoke
def test_partial_is_terminal_in_both_vocabularies_and_open_in_neither():
    """`partial` joins `done` and `cancelled`, and is deliberately absent from
    `OPEN_STATUSES` — an attempted item is not in flight, and treating it as
    open is precisely the revival SR-151 forbids."""
    assert "partial" in acommon.TERMINAL_STATUSES
    assert "partial" in ctraj.TERMINAL_STATUSES
    assert "partial" not in ctraj.OPEN_STATUSES
    assert "partial" not in ctraj.BACKLOG_STALE_STATUSES


@pytest.mark.smoke
def test_the_converter_round_trips_partial_and_still_refuses_active():
    """`wi_convert` maps status <-> directory both ways off one table, so the
    two directions cannot disagree. `active` stays ABSENT on purpose: a claim
    lives at `active/<branch>/`, two levels deep, so there is no single
    directory this table could name — and inventing a branch to file it under
    is exactly the catch-all this format refuses."""
    assert wi_convert.STATUS_DIRS["partial"] == "partial"
    assert wi_convert.DIR_STATUSES["partial"] == "partial"
    assert "active" not in wi_convert.STATUS_DIRS
    assert wi_convert.status_dir({"WI-ID": "WI-401", "Status": "partial"}) == "partial"
    assert wi_convert.status_from_location("partial", "docs/work") == "partial"
    with pytest.raises(wi_convert.ConvertError) as excinfo:
        wi_convert.status_dir({"WI-ID": "WI-401", "Status": "active"})
    assert "WI-401" in str(excinfo.value) and "no directory" in str(excinfo.value)


# --- TC-170: no terminal item is ready ---------------------------------------


@pytest.mark.smoke
def test_tc170_no_item_in_any_terminal_state_is_ready(tmp_path):
    """The three terminal permutations, driven side by side on one registry so
    the scheduler has to DISCRIMINATE rather than merely be empty: each keeps
    its own disposition and its own reason code, and none of the three reaches
    the frontier."""
    write_spec(tmp_path, "complete", "WI-401", deliverable="shipped", **_ordinary())
    write_spec(
        tmp_path, "cancelled", "WI-402", order=1, deliverable="never", **_ordinary()
    )
    write_spec(
        tmp_path, "partial", "WI-403", order=2, deliverable="AC-1 only", **_ordinary()
    )
    write_spec(tmp_path, "queued", "WI-404", order=3, **_ordinary())

    by_id = dispositions(tmp_path)
    assert by_id["WI-401"] == ("done", ["done:integrated"])
    assert by_id["WI-402"] == ("cancelled", ["cancelled:terminal-wont-build"])
    assert by_id["WI-403"] == ("partial", ["partial:terminal-attempted"])
    # ... and only the live row is on the frontier, so none of the three slipped
    # through on a rung below the terminal lookup.
    assert ready_ids(tmp_path) == ["WI-404"]


def _ordinary():
    """The frontmatter a schedulable row needs: `safety_class` FAILS CLOSED, so
    a fixture that omitted it would read `unclassified` and never be ready —
    which would make every assertion here pass for the wrong reason."""
    return {"safety_class": "ordinary", "workstream": "ws"}


@pytest.mark.smoke
def test_tc170_a_partial_row_is_terminal_whatever_else_it_declares(tmp_path):
    """The terminal lookup sits at the TOP of `_disposition`'s ladder, and that
    ordering is the requirement rather than a convenience: a partial row with
    every readiness precondition satisfied — classified, unblocked, no unmet
    predecessor — must still never be ready, or an unrelated edit could revive
    an attempt."""
    write_spec(tmp_path, "partial", "WI-401", deliverable="AC-1 only", **_ordinary())
    assert dispositions(tmp_path)["WI-401"][0] == "partial"
    assert ready_ids(tmp_path) == []


@pytest.mark.smoke
def test_tc170_a_partial_predecessor_is_a_hard_edge_that_never_clears(tmp_path):
    """A partial attempt never integrates `done`, so a row hard-blocked on one
    stays visibly waiting instead of proceeding on a will-never-happen
    dependency — the same posture `cancelled` has carried since WI-267. This is
    why a successor carries LINEAGE rather than a hard `needs` edge on the
    attempt it replaces."""
    write_spec(tmp_path, "partial", "WI-401", deliverable="AC-1 only", **_ordinary())
    write_spec(tmp_path, "queued", "WI-402", order=1, needs=["WI-401"], **_ordinary())

    disposition, reasons = dispositions(tmp_path)["WI-402"]
    assert disposition == "waiting"
    assert any("WI-401" in reason for reason in reasons)
    assert ready_ids(tmp_path) == []


@pytest.mark.smoke
def test_tc170_a_successor_is_ready_only_once_admission_has_queued_it(tmp_path):
    """The `successor` permutation, at the seam this module owns. A successor is
    a NEW id carrying the remaining scope, and it enters the queue only through
    admission (`admit.py`, LLR-178) — so while it is still a `draft/` candidate
    the scheduler must hold it off the frontier, and the same spec becomes ready
    exactly when admission has moved it to `queued/`. Both halves are asserted,
    because a candidate that was never ready in either place would satisfy the
    first alone."""
    write_spec(tmp_path, "partial", "WI-401", deliverable="AC-1 only", **_ordinary())
    candidate = write_spec(
        tmp_path,
        "draft",
        "WI-402",
        order=1,
        title="Successor to WI-401",
        supersedes="WI-401",
        **_ordinary(),
    )
    assert dispositions(tmp_path)["WI-402"] == ("draft", ["excluded:draft"])
    assert ready_ids(tmp_path) == []

    # Admission's effect, applied by hand: the candidate moves into the queue.
    admitted = tmp_path / "docs" / "work" / "queued" / candidate.name
    admitted.parent.mkdir(parents=True, exist_ok=True)
    admitted.write_text(candidate.read_text(encoding="utf-8"), encoding="utf-8")
    candidate.unlink()

    assert ready_ids(tmp_path) == ["WI-402"]
    # ... and the attempt it supersedes is still terminal, so the successor
    # replaced the row rather than reviving it.
    assert dispositions(tmp_path)["WI-401"][0] == "partial"


@pytest.mark.smoke
def test_the_lineage_key_is_inert_to_the_scheduler(tmp_path):
    """`supersedes` is a RECORD, not an edge. If the scheduler read it as a
    dependency the successor would inherit the attempt's dead hard edge and
    could never run — which would make "remaining scope re-enters the queue" a
    sentence with no behaviour behind it."""
    write_spec(tmp_path, "partial", "WI-401", deliverable="AC-1 only", **_ordinary())
    write_spec(
        tmp_path, "queued", "WI-402", order=1, supersedes="WI-401", **_ordinary()
    )
    assert ready_ids(tmp_path) == ["WI-402"]
