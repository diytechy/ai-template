"""traj_parse.py's `frame_context`, the depth-0 frame as a read model.

Split verbatim from `tests/test_traj_parse.py`, whose other cases patch the
git/subprocess seam or drive real git and which is registered in
`tests/conftest.py`'s `SLOW_MODULES`. These four read registries only (a tmp
tree, the shipped blank form, and this repository's own locked frame), so they
keep TC-196's read-model clauses in the per-commit smoke tier. The pin over the
live frame belongs here most of all: in a slow module a registry change that
staled it went unseen until a close run.

Named outside the `test_traj_*` family on purpose: `tests/test_smoke_tier.py`
holds every module of that family slow, because each drives the real
`gen_trajectory.py`, and this one drives nothing.
"""

from conftest import ROOT, load_script
from traj_core_fixtures import FRAME, write_frame


# --- WI-455: `frame_context`, the depth-0 frame as a read model ----------------


def test_frame_context_is_none_without_a_declared_frame(tmp_path):
    # The registry's own applies-when: a project that never declares a boundary
    # simply does not create the file, and the reader says so with None rather
    # than an empty-but-present frame the view would render as a blank picture.
    tp = load_script("traj_parse")
    assert tp.frame_context(tmp_path) is None


def test_frame_context_drops_the_blank_form_s_example_rows(tmp_path):
    # A freshly bootstrapped scaffold HAS the file — the blank form, all of whose
    # rows end `-000`. Same rule as every other tier: example rows are not data.
    tp = load_script("traj_parse")
    write_frame(
        tmp_path,
        (
            ROOT / "project-trajectory" / "registries" / "external.template.toml"
        ).read_text(encoding="utf-8"),
    )
    assert tp.frame_context(tmp_path) is None


def test_frame_context_joins_the_tie_backs_and_keeps_id_order(tmp_path):
    tp = load_script("traj_parse")
    write_frame(tmp_path, FRAME)
    (tmp_path / "docs" / "requirements" / "interfaces.toml").write_text(
        """[interface.IF-001]
owner = "src/m"
consumers = ["external:downstream adopter"]
channel = "cli"
status = "Drafted"
interface_to_external = "B-01"

[interface.IF-002]
owner = "external:git"
consumers = ["src/m"]
channel = "git"
status = "Drafted"
notes = "No tie-back: git is not a party of its own here."
""",
        encoding="utf-8",
    )
    frame = tp.frame_context(tmp_path)
    assert [e["id"] for e in frame["entities"]] == ["EXT-001", "EXT-002"]
    assert [c["id"] for c in frame["crossings"]] == ["B-01", "B-02"]
    by_id = {c["id"]: c for c in frame["crossings"]}
    # the realization is JOINED from interfaces.toml, with the side it ties on...
    assert by_id["B-01"]["realized_by"] == [("IF-001", "out")]
    # ...and a crossing nothing realizes stays declared, not dropped
    assert by_id["B-02"]["realized_by"] == []
    # the entity name resolves for display without the frame row restating it
    assert by_id["B-01"]["entity_name"] == "Downstream adopter"
    # the untied `external:` endpoint carries the reason its own row records
    assert [(u["id"], u["endpoint"]) for u in frame["untied"]] == [
        ("IF-002", "external:git")
    ]
    assert frame["untied"][0]["reason"].startswith("No tie-back")


def test_frame_context_reads_this_repo_s_own_locked_frame():
    # The meta repo's own frame, pinned as data rather than as a picture: the
    # locked depth-0 table is 5 parties, 7 crossings and 1 relationship since the
    # C1 sitting (WI-643) redrew it (4, 4 and 3 before), `B-02` is the crossing
    # deliberately left unrealized (SR-140's condition, stated in the registry
    # header), and WI-455 slice 2's adjudication left exactly three `external:`
    # rows tied back to nothing, each with its reason on the row (seven since
    # OI-67 slice 4, nine since WI-534, ten since WI-678, below).
    tp = load_script("traj_parse")
    frame = tp.frame_context(ROOT)
    assert len(frame["entities"]) == 5
    assert [c["id"] for c in frame["crossings"]] == [
        "B-01",
        "B-02",
        "B-04",
        "B-05",
        "B-09",
        "B-10",
        "B-11",
    ]
    assert len(frame["relationships"]) == 1
    by_id = {c["id"]: c for c in frame["crossings"]}
    # B-02 stays unrealized by design. B-09, B-10 and B-11 are unrealized today
    # and pinned so: the C1 package's §7 defers re-tying IF-041 to B-10 and the
    # dashboard's own IF row, so a later re-tie moves this pin deliberately.
    assert by_id["B-02"]["realized_by"] == []
    for crossing in ("B-09", "B-10", "B-11"):
        assert by_id[crossing]["realized_by"] == [], crossing
    # the two rows slice 2 gave a facing, and the largest bundle in the frame
    assert {"IF-080", "IF-081"} <= {i for i, _side in by_id["B-05"]["realized_by"]}
    # OI-67 slice 4 added four: the agent CLI's stdin arm and the three argv
    # arms an external party drives (the adopter's session, the launchers) —
    # information coming IN from a party the frame declares no IN crossing
    # for, each stating so on the row. The arms round (WI-534) added two of
    # the same kind: the fragment drop-box's write arm and schedule.py's own
    # argv, both driven by the adopter's session. The second build wave added
    # one more of that kind, the observation writer's argv; WI-678 took the
    # act ledger's `external:` consumer off, since only the kit reads that
    # file, rather than leaving it here without a reason. The spine-linked
    # test listing's argv joined them, driven by the adopter's session too,
    # and so did the release re-judge checkpoint's argv (IF-229), run by the
    # person preparing a release, and the flag-axis census's argv (IF-240),
    # run by the adopter's session.
    assert [u["id"] for u in frame["untied"]] == [
        "IF-032",
        "IF-036",
        "IF-041",
        "IF-151",
        "IF-154",
        "IF-155",
        "IF-157",
        "IF-168",
        "IF-171",
        "IF-215",
        "IF-229",
        "IF-233",
        "IF-240",
    ]
    assert all(u["reason"].startswith("No tie-back") for u in frame["untied"])
