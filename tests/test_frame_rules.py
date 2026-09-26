"""The frame's system-of-interest rules, called on in-memory rows (TC-213).

`frame_rules.py` is a pure join module beside `coherence.py`: it reads no file,
so every rule here is driven with plain row dicts, and the checker-level
behaviour (which pipe a finding rides, the exit code) is pinned separately in
`tests/test_frame_system.py`, which drives `trace.py` over scaffold frames.

Two systems of interest share one frame (SR-187): the system in OPERATION and
the system that builds and DELIVERS it. A crossing declares which one it
belongs to; a requirement's system is DERIVED from the crossings it names and
never recorded on the requirement (SR-219).
"""

import copy

from conftest import load_script

FRAME_RULES = load_script("frame_rules")
import kitlib.spine as SPINE  # noqa: E402  (after the load above puts scripts/ on the path)

OP = {"B-ID": "B-01", "System": "operation"}
OP2 = {"B-ID": "B-02", "System": "operation"}
DEL = {"B-ID": "B-04", "System": "delivery"}
NONE = {"B-ID": "B-05"}


def _sr(sid, *crossings):
    return {"SR-ID": sid, "Boundary-Refs": ";".join(crossings)}


# --- the closed pair has one home ---------------------------------------------


def test_the_closed_pair_is_declared_once_in_the_schema_module():
    assert SPINE.SYSTEM_VALUES == ("operation", "delivery")
    assert "system" in SPINE.OFFSPINE_KEYS["B-ID"]


# --- crossing_systems ----------------------------------------------------------


def test_crossing_systems_maps_each_declaring_crossing_and_leaves_out_the_rest():
    assert FRAME_RULES.crossing_systems([OP, DEL, NONE]) == {
        "B-01": "operation",
        "B-04": "delivery",
    }


def test_crossing_systems_of_no_frame_is_empty():
    assert FRAME_RULES.crossing_systems([]) == {}


# --- sr_system_advisories (SR-219) ---------------------------------------------


def test_a_requirement_naming_only_operation_crossings_is_placed_silently():
    srs = [_sr("SR-001", "B-01", "B-02")]
    assert FRAME_RULES.sr_system_advisories(srs, [OP, OP2, DEL]) == []


def test_a_requirement_naming_only_delivery_crossings_is_placed_silently():
    srs = [_sr("SR-001", "B-04")]
    assert FRAME_RULES.sr_system_advisories(srs, [OP, DEL]) == []


def test_a_requirement_spanning_both_systems_is_one_advisory_naming_a_crossing_of_each():
    srs = [_sr("SR-007", "B-01", "B-02", "B-04")]
    out = FRAME_RULES.sr_system_advisories(srs, [OP, OP2, DEL])
    assert len(out) == 1
    line = out[0]
    assert "SR-007" in line
    assert "B-04" in line  # the delivery crossing
    assert "B-01" in line or "B-02" in line  # one operation crossing
    assert "operation" in line and "delivery" in line


def test_a_crossing_with_no_system_places_nothing():
    """The requirement is placed by its OTHER crossings: one undeclared and one
    operation crossing is an operation requirement, not a mixed one."""
    srs = [_sr("SR-001", "B-05", "B-01")]
    assert FRAME_RULES.sr_system_advisories(srs, [OP, NONE]) == []


def test_an_out_of_pair_crossing_places_nothing_and_makes_no_mixed_advisory():
    """A value outside the pair already fails the frame check; it must not also
    place a requirement, or a typo would read as a mixed-system requirement."""
    staging = {"B-ID": "B-09", "System": "staging"}
    assert FRAME_RULES.crossing_systems([OP, staging]) == {"B-01": "operation"}
    srs = [_sr("SR-001", "B-01", "B-09")]
    assert FRAME_RULES.sr_system_advisories(srs, [OP, staging]) == []


def test_with_no_crossings_at_all_every_requirement_produces_nothing():
    srs = [_sr("SR-001", "B-01", "B-04"), _sr("SR-002")]
    assert FRAME_RULES.sr_system_advisories(srs, []) == []


def test_nothing_is_written_back_to_a_requirement_or_a_crossing():
    """The placement is recomputed on every run and never recorded on the
    requirement (SR-219's acceptance), so the inputs compare equal afterwards."""
    srs = [_sr("SR-007", "B-01", "B-04"), _sr("SR-008", "B-05")]
    bifs = [OP, DEL, NONE]
    before = copy.deepcopy((srs, bifs))
    FRAME_RULES.sr_system_advisories(srs, bifs)
    FRAME_RULES.crossing_systems(bifs)
    FRAME_RULES.frame_system_findings(bifs)
    assert (srs, bifs) == before


# --- frame_system_findings (SR-187, in memory) -----------------------------------


def test_crossings_declaring_a_value_from_the_pair_produce_nothing():
    assert FRAME_RULES.frame_system_findings([OP, DEL]) == ([], [])


def test_a_value_outside_the_pair_is_a_failure_naming_the_crossing():
    failures, advisories = FRAME_RULES.frame_system_findings(
        [OP, {"B-ID": "B-09", "System": "staging"}]
    )
    assert len(failures) == 1 and "B-09" in failures[0] and "staging" in failures[0]
    assert advisories == []


def test_a_crossing_declaring_nothing_is_an_advisory_naming_it():
    failures, advisories = FRAME_RULES.frame_system_findings([OP, NONE])
    assert failures == []
    assert len(advisories) == 1 and "B-05" in advisories[0]


def test_a_blank_value_reads_as_declaring_nothing():
    failures, advisories = FRAME_RULES.frame_system_findings(
        [{"B-ID": "B-05", "System": "  "}]
    )
    assert failures == [] and len(advisories) == 1


def test_a_frame_with_no_crossing_is_vacuous():
    assert FRAME_RULES.frame_system_findings([]) == ([], [])
