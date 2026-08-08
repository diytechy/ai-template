"""TC-172 / TC-173 / TC-174 — the queue-admission transaction and its refusals.

The value of this module is almost entirely in what it REFUSES, so every
declared precondition is driven to a refusal and every refusal is asserted to
NAME the offending thing. A bare `False` at any of these seams is
indistinguishable from "nothing was wrong", and a transaction whose whole job is
to stop bad rows entering the queue cannot be allowed to fail silently.

Three properties get their own attention because getting them wrong is silent:

  * **all-or-nothing.** A refused candidate must still be in `draft/` with an
    empty ledger behind it. A half-admitted row — moved but unruled, or ruled
    but unmoved — is the state the ordering argument in `admit`'s docstring
    exists to make unrepresentable, so it is asserted rather than assumed.
  * **overlap is a finding, not a conflict.** The graph is proved to report
    every shared dimension AND to rule on none of them; the finding sentences
    are asserted not to call an overlap a conflict, because the whole design
    turns on that distinction and prose is where it would quietly erode.
  * **the verdict expires.** A verdict that outlives the state it judged reads
    as a current ruling, so both digests are moved out from under a recorded
    verdict and the strict check is asserted to name which one moved.
"""

import json

import pytest
from conftest import load_script

ADMIT = load_script("admit")
OUTCOME = load_script("outcome")
ATTEST = load_script("attest")
CHECK = load_script("check_trajectory")
SCHEDULE = load_script("schedule")


# --- the fixture spine --------------------------------------------------------

SN_MD = """# Stakeholder Needs

## Core needs

| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-000 | _(example row, ignored)_ | _(why)_ | M | _(how we'd know)_ |
| SN-001 | A team can add two numbers. | It is the demo need. | M | add(1,2) gives 3. |
"""

SR_HEAD = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,"
    "Priority,Verification,Status,Phase,Area,SupersededBy\n"
)
SR_ROWS = (
    'SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.",'
    '"add(1,2) == 3",,M,Test,Verified,1,core,\n'
    'SR-002,Subtraction,SN-001,"The system shall subtract two numbers.",'
    '"Realizes SN-001.","sub(2,1) == 1",,M,Test,Verified,1,core,\n'
)
LLR_HEAD = (
    "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,Rationale,TestRefs,Status,"
    "Component,Phase\n"
)
LLR_ROWS = (
    'LLR-001,SR-001,Pure adder,src/demo,add,"Pure function: two numbers -> sum.",'
    '"Purity is testable.",(see TC),Implemented,CMP-001,1\n'
)
TC_HEAD = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,"
    "Status,Phase\n"
)
TC_ROWS = (
    'TC-001,SR-001;LLR-001,Unit,"call add and assert the sum",Smoke,"a=1; b=2",'
    '"Satisfies SR-001 AcceptanceCriteria",Yes,tests/test_demo.py,Verified,1\n'
)
CMP_CSV = (
    "CMP-ID,Name,Category,Knowledge,State,SupersededBy,PartOf,DetailDoc,Notes\n"
    "CMP-001,Core,software,,Active,,,,\n"
    "CMP-002,Edge,software,,Active,,,,\n"
)
IF_CSV = (
    "IF-ID,Direction,ThisProject,Counterpart,Contract,SR-Refs,Version,Stability,"
    "Status,Component,Notes\n"
    "IF-001,Provides,src/demo,cli,add,SR-001,1,Stable,Stable,CMP-001,\n"
    "IF-002,Provides,src/demo,cli,sub,SR-002,1,Stable,Stable,CMP-001,\n"
)


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


@pytest.fixture
def unattested_repo(tmp_path):
    """The same tree WITHOUT the attestation ledger — every spine row current
    but anchored by nothing."""
    root = tmp_path / "repo"
    req = root / "docs" / "requirements"
    _write(req / "stakeholder-needs.md", SN_MD)
    _write(req / "system-requirements.csv", SR_HEAD + SR_ROWS)
    _write(req / "low-level-requirements.csv", LLR_HEAD + LLR_ROWS)
    _write(req / "components.csv", CMP_CSV)
    _write(req / "interfaces.csv", IF_CSV)
    _write(root / "docs" / "test" / "test-cases.csv", TC_HEAD + TC_ROWS)
    _write(root / "docs" / "specs" / "WI-420.md", "# WI-420 spec of record\n")
    for folder in ADMIT.SPEC_STATUS_DIRS:
        (root / "docs" / "work" / folder).mkdir(parents=True, exist_ok=True)
    return root


@pytest.fixture
def repo(unattested_repo):
    """A tree with a complete four-tier spine, a SEEDED attestation ledger, the
    seven work-state folders and one spec-of-record for the SpecRef to hit."""
    ATTEST.seed(unattested_repo, unattested_repo / "docs")
    return unattested_repo


def _toml(front):
    lines = []
    for key, value in front.items():
        if isinstance(value, (list, tuple)):
            rendered = "[{}]".format(", ".join(json.dumps(str(v)) for v in value))
        else:
            rendered = json.dumps(str(value))
        lines.append("{} = {}".format(key, rendered))
    return "\n".join(lines)


DEFAULTS = {
    "title": "A candidate",
    "specref": "docs/specs/WI-420.md",
    "sr_refs": ["SR-001"],
    "needs": [],
    "safety_class": "ordinary",
    "source": ADMIT.SOURCE_OWNER,
    "components": ["CMP-001"],
    "modules": ["src/demo.py"],
    "interfaces": ["IF-001"],
    "likely_files": ["src/demo.py"],
}


def spec_text(wid="WI-420", **over):
    """A candidate spec's text, with its `scope_digest` filled in correctly.

    Two passes, and the second is free: `scope_digest` is not one of
    `outcome.SCOPE_KEYS`, so writing the digest into the frontmatter does not
    move the digest. An explicit `scope_digest=` in `over` survives — that is
    how the stale-digest permutation is driven."""
    front = {"id": wid}
    front.update(DEFAULTS)
    declared = over.pop("scope_digest", None)
    front.update(over)
    text = "+++\n" + _toml(front) + "\n+++\n"
    front["scope_digest"] = declared or OUTCOME.scope_digest(text)
    return "+++\n" + _toml(front) + "\n+++\n"


def write_spec(root, wid="WI-420", folder="draft", slug="thing", **over):
    path = root / "docs" / "work" / folder / "{}-{}.md".format(wid, slug)
    _write(path, spec_text(wid, **over))
    return path


def rel(root, path):
    return path.relative_to(root).as_posix()


def ledger(root):
    return ADMIT.read_admissions(root)


def joined(findings):
    return "\n".join(findings)


# --- TC-173 (Unit): the mechanical overlap graph ------------------------------

# Each row is (permutation, declaration key, the value both rows share).
DIMENSION_CASES = [
    ("requirement", "sr_refs", "SR-001"),
    ("component", "components", "CMP-001"),
    ("interface", "interfaces", "IF-001"),
    ("file", "likely_files", "src/demo.py"),
    ("predecessor", "needs", "WI-100"),
]


@pytest.mark.parametrize("dimension,key,shared", DIMENSION_CASES)
def test_each_shared_dimension_produces_an_overlap_finding(dimension, key, shared):
    a = {"id": "WI-420", key: [shared]}
    b = {"id": "WI-415", key: [shared]}
    findings = ADMIT.overlap_graph([a], [], [b])
    assert [f["dimension"] for f in findings] == [dimension]
    assert findings[0]["shared"] == [shared]
    assert findings[0]["a"] == "WI-420" and findings[0]["b"] == "WI-415"
    assert shared in findings[0]["finding"]


def test_a_disjoint_pair_produces_no_overlap_finding():
    """The `disjoint` permutation — the one that proves the graph is not simply
    reporting every pair it is handed."""
    a = {
        "id": "WI-420",
        "sr_refs": ["SR-001"],
        "components": ["CMP-001"],
        "interfaces": ["IF-001"],
        "likely_files": ["src/demo.py"],
        "needs": ["WI-100"],
    }
    b = {
        "id": "WI-415",
        "sr_refs": ["SR-002"],
        "components": ["CMP-002"],
        "interfaces": ["IF-002"],
        "likely_files": ["src/other.py"],
        "needs": ["WI-101"],
    }
    assert ADMIT.overlap_graph([a], [], [b]) == []


def test_overlap_findings_are_findings_and_never_call_themselves_conflicts():
    """The distinction the whole design turns on, asserted in the PROSE too:
    calling mechanical overlap a conflict would stall the queue on every
    ordinary pair, and prose is exactly where that erodes first."""
    a = {"id": "WI-420", "likely_files": ["src/demo.py"]}
    b = {"id": "WI-415", "likely_files": ["src/demo.py"]}
    sentence = ADMIT.overlap_graph([a], [], [b])[0]["finding"]
    assert "not a conflict" in sentence
    assert "ordering or partition" in sentence


def test_a_candidate_overlaps_active_work_too():
    a = {"id": "WI-420", "components": ["CMP-001"]}
    active = {"id": "WI-300", "components": ["CMP-001"]}
    findings = ADMIT.overlap_graph([a], [active], [])
    assert [(f["a"], f["b"], f["dimension"]) for f in findings] == [
        ("WI-420", "WI-300", "component")
    ]


def test_candidates_are_paired_against_each_other():
    """A batch admitted in one sitting can collide inside itself, and a graph
    blind to that would wave the collision through precisely when several rows
    arrive together."""
    a = {"id": "WI-420", "likely_files": ["src/demo.py"]}
    b = {"id": "WI-421", "likely_files": ["src/demo.py"]}
    findings = ADMIT.overlap_graph([a, b], [], [])
    assert [(f["a"], f["b"]) for f in findings] == [("WI-420", "WI-421")]


def test_one_file_declared_two_ways_is_one_token():
    """Otherwise the file dimension is defeated by a Windows author writing the
    separator their shell prints."""
    a = {"id": "WI-420", "likely_files": ["src\\demo.py"]}
    b = {"id": "WI-415", "likely_files": ["./src/demo.py"]}
    findings = ADMIT.overlap_graph([a], [], [b])
    assert [f["shared"] for f in findings] == [["src/demo.py"]]


def test_a_soft_predecessor_still_names_the_same_row():
    a = {"id": "WI-420", "needs": ["WI-100"]}
    b = {"id": "WI-415", "needs": ["~WI-100"]}
    assert [f["dimension"] for f in ADMIT.overlap_graph([a], [], [b])] == [
        "predecessor"
    ]


def test_every_dimension_of_one_pair_is_reported_not_just_the_first():
    a = {"id": "WI-420", "sr_refs": ["SR-001"], "likely_files": ["src/demo.py"]}
    b = {"id": "WI-415", "sr_refs": ["SR-001"], "likely_files": ["src/demo.py"]}
    assert [f["dimension"] for f in ADMIT.overlap_graph([a], [], [b])] == [
        "requirement",
        "file",
    ]


# --- TC-172 (Integration): the transaction and its preconditions --------------


def test_a_passing_candidate_is_admitted_with_its_verdict_recorded(repo):
    """The `passing` permutation: the spec moves, and exactly one event lands
    carrying the two digests the ruling was computed against."""
    path = write_spec(repo)
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert findings == []
    assert not path.exists()
    queued = repo / "docs" / "work" / "queued" / path.name
    assert queued.is_file()
    assert event["wi"] == "WI-420"
    assert event["verdict"] == ADMIT.NO_CONFLICT
    scope, spine = ADMIT.candidate_digests(repo, queued.read_text(encoding="utf-8"))
    assert (event["scope"], event["spine"]) == (scope, spine)
    assert len(ledger(repo)) == 1


def test_the_admitted_row_passes_the_strict_freshness_gate(repo):
    """The `current` permutation of TC-174, driven through the real transaction
    rather than through a hand-written event."""
    path = write_spec(repo)
    _event, findings = ADMIT.admit(repo, rel(repo, path))
    assert findings == []
    assert CHECK.admission_verdict_findings(repo) == []


@pytest.mark.parametrize(
    "over,expected",
    [
        pytest.param({"id": "WI-999"}, "filename carries WI-420", id="frontmatter"),
    ],
)
def test_bad_identity_is_refused_naming_it(repo, over, expected):
    """The `bad-identity` permutation: the id has two homes, so they are
    compared here rather than trusted apart."""
    path = write_spec(repo, **over)
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert expected in joined(findings)


def test_an_id_already_in_the_registry_is_refused(repo):
    write_spec(repo, folder="deferred", slug="incumbent")
    path = write_spec(repo, slug="candidate")
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "WI-420 is already the id of" in joined(findings)


def test_a_stale_scope_digest_is_refused(repo):
    """The `stale-digest` permutation: the draft was edited after its digest was
    frozen, which is the state that must never reach the queue — everything
    downstream compares delivered work against that number."""
    path = write_spec(repo, scope_digest="0123456789abcdef")
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "declares scope_digest 0123456789abcdef" in joined(findings)


def test_a_malformed_scope_digest_is_refused(repo):
    path = write_spec(repo, scope_digest="not-a-digest")
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "which is not 16 hex" in joined(findings)


def test_a_cyclic_predecessor_is_refused(repo):
    """The `cyclic-predecessor` permutation. The cycle closes THROUGH the
    candidate: WI-420 -> WI-300 -> WI-420."""
    write_spec(repo, wid="WI-300", folder="queued", slug="incumbent", needs=["WI-420"])
    path = write_spec(repo, needs=["WI-300"])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "close a dependency cycle" in joined(findings)


def test_a_self_predecessor_is_refused(repo):
    path = write_spec(repo, needs=["WI-420"])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "close a dependency cycle" in joined(findings)


def test_a_predecessor_that_is_not_a_work_item_is_refused(repo):
    path = write_spec(repo, needs=["WI-777"])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "predecessor WI-777, which is not a work item" in joined(findings)


@pytest.mark.parametrize("folder", ["cancelled", "partial"])
def test_a_terminal_but_unfinished_predecessor_is_refused(repo, folder):
    write_spec(repo, wid="WI-300", folder=folder, slug="attempt")
    path = write_spec(repo, needs=["WI-300"])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "depends on WI-300" in joined(findings)


def test_a_completed_predecessor_is_fine(repo):
    """The mirror of the rung above — depending on FINISHED work is ordinary,
    and a rule that refused it would make the successor pattern unusable."""
    write_spec(repo, wid="WI-300", folder="complete", slug="shipped")
    path = write_spec(repo, needs=["WI-300"])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert findings == []
    assert event["wi"] == "WI-420"


def test_reviving_a_terminal_row_is_refused(repo):
    """Decision 6 / SR-151: an attempted item never returns to the frontier."""
    write_spec(repo, folder="partial", slug="attempt")
    path = write_spec(repo, slug="revival")
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "WI-420 is already terminal at" in joined(findings)
    assert "never this row re-queued as itself" in joined(findings)


def test_superseding_a_live_row_is_refused(repo):
    write_spec(repo, wid="WI-300", folder="queued", slug="live")
    path = write_spec(repo, supersedes=["WI-300"])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "supersedes WI-300, which is queued" in joined(findings)


def test_superseding_itself_is_refused(repo):
    path = write_spec(repo, supersedes=["WI-420"])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "WI-420 supersedes itself" in joined(findings)


def test_superseding_a_row_that_does_not_exist_is_refused(repo):
    path = write_spec(repo, supersedes=["WI-777"])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "supersedes WI-777, which is not a work item" in joined(findings)


def test_a_successor_of_a_partial_attempt_is_admitted(repo):
    write_spec(repo, wid="WI-300", folder="partial", slug="attempt")
    path = write_spec(repo, supersedes=["WI-300"])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert findings == []
    assert event["declared"]["supersedes"] == ["WI-300"]


def test_a_reference_to_a_row_that_does_not_exist_is_refused(repo):
    """One half of the `stale-reference` permutation."""
    path = write_spec(repo, sr_refs=["SR-404"])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "references SR-404, which resolves to no spine row" in joined(findings)


def test_a_reference_whose_text_moved_since_its_anchor_is_refused(repo):
    """The other half: the requirement was amended after it was accepted, so the
    candidate would be built against a version nobody ratified."""
    csv_path = repo / "docs" / "requirements" / "system-requirements.csv"
    _write(
        csv_path,
        csv_path.read_text(encoding="utf-8").replace(
            "shall add two numbers", "shall add two integers"
        ),
    )
    path = write_spec(repo)
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "normative text has moved since its accepted anchor" in joined(findings)


def test_a_reference_with_no_anchor_at_all_is_refused(unattested_repo):
    """The same rung with an EMPTY ledger — an unattested row is refused for its
    own reason, not confused with an amended one."""
    path = write_spec(unattested_repo)
    event, findings = ADMIT.admit(unattested_repo, rel(unattested_repo, path))
    assert event is None
    assert "has no accepted attestation anchor" in joined(findings)


def test_a_specref_that_does_not_resolve_is_refused(repo):
    path = write_spec(repo, specref="docs/specs/absent.md")
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "does not resolve to an in-repo file" in joined(findings)


def test_a_candidate_with_no_specref_is_refused(repo):
    path = write_spec(repo, specref="")
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "no SpecRef" in joined(findings)


@pytest.mark.parametrize("key", list(ADMIT.DECLARED_LISTS))
def test_an_absent_declaration_is_refused(repo, key):
    """The `unclassified` permutation. An absent list is not an empty one:
    `interfaces = []` states that the row touches no seam, where a missing key
    states only that nobody thought about it."""
    # Built without the helper: `spec_text` always writes all four keys, and the
    # permutation under test is a key that is ABSENT rather than empty.
    front = {"id": "WI-420"}
    front.update({k: v for k, v in DEFAULTS.items() if k != key})
    text = "+++\n" + _toml(front) + "\n+++\n"
    front["scope_digest"] = OUTCOME.scope_digest(text)
    path = repo / "docs" / "work" / "draft" / "WI-420-thing.md"
    _write(path, "+++\n" + _toml(front) + "\n+++\n")
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "declares no {}".format(key) in joined(findings)
    assert "= [] to state that it touches none" in joined(findings)


def test_an_unclassified_safety_class_is_refused(repo):
    path = write_spec(repo, safety_class="")
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "declares safety_class ''" in joined(findings)


def test_an_undeclared_safety_class_word_is_refused(repo):
    path = write_spec(repo, safety_class="probably-fine")
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "probably-fine" in joined(findings)


def test_a_component_that_resolves_to_no_row_is_refused(repo):
    path = write_spec(repo, components=["CMP-404"])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "CMP-404, which resolves to no row" in joined(findings)


def test_an_interface_that_resolves_to_no_row_is_refused(repo):
    path = write_spec(repo, interfaces=["IF-404"])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "IF-404, which resolves to no row" in joined(findings)


def test_an_empty_declaration_is_a_legal_declaration(repo):
    path = write_spec(repo, interfaces=[])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert findings == []
    assert event["declared"]["interfaces"] == []


def test_an_absolute_declared_path_is_refused(repo):
    path = write_spec(repo, likely_files=["/etc/passwd"])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "absolute path" in joined(findings)


def test_a_declared_path_escaping_the_repo_is_refused(repo):
    path = write_spec(repo, modules=["../elsewhere/x.py"])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "escapes the repo" in joined(findings)


# --- the source event ---------------------------------------------------------


def test_a_candidate_with_no_source_is_refused(repo):
    path = write_spec(repo, source="")
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "declares no source" in joined(findings)


def test_an_invented_provenance_word_is_refused(repo):
    path = write_spec(repo, source="the-planner")
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "may not invent its own provenance word" in joined(findings)


def test_a_source_event_that_resolves_nowhere_is_refused(repo):
    path = write_spec(repo, source="0123456789abcdef")
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "resolves in no ledger" in joined(findings)


def test_a_source_event_that_resolves_is_accepted(repo):
    """A real producer's provenance: the id of an event actually in a ledger."""
    produced = OUTCOME.append_event(
        repo / "docs" / "events" / "outcomes.jsonl",
        {"schema": 1, "kind": "note", "what": "minted the candidate"},
    )
    path = write_spec(repo, source=produced["id"])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert findings == []
    assert event["source"] == produced["id"]


# --- the overlap disposition --------------------------------------------------


def test_an_unreviewed_overlap_refuses_admission(repo):
    write_spec(repo, wid="WI-300", folder="queued", slug="incumbent")
    path = write_spec(repo)
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "no adjudicated verdict" in joined(findings)
    assert "not a conflict" in joined(findings)


def test_no_conflict_may_not_be_recorded_over_an_overlap(repo):
    write_spec(repo, wid="WI-300", folder="queued", slug="incumbent")
    path = write_spec(repo)
    event, findings = ADMIT.admit(repo, rel(repo, path), verdict=ADMIT.NO_CONFLICT)
    assert event is None
    assert "an overlap that exists is disposed of, not ignored" in joined(findings)


def test_compatible_overlap_without_an_ordering_or_partition_is_refused(repo):
    write_spec(repo, wid="WI-300", folder="queued", slug="incumbent")
    path = write_spec(repo)
    event, findings = ADMIT.admit(repo, rel(repo, path), verdict=ADMIT.COMPATIBLE)
    assert event is None
    assert "neither an ordering nor a partition" in joined(findings)


def test_compatible_overlap_with_a_declared_ordering_is_admitted(repo):
    write_spec(repo, wid="WI-300", folder="queued", slug="incumbent")
    path = write_spec(repo)
    event, findings = ADMIT.admit(
        repo,
        rel(repo, path),
        verdict={
            "verdict": ADMIT.COMPATIBLE,
            "ordering": ["WI-300", "WI-420"],
            "by": "adjudicator",
            "rationale": "disjoint symbols in one file; WI-300 lands first",
        },
    )
    assert findings == []
    assert event["ordering"] == ["WI-300", "WI-420"]
    assert event["overlaps"], "the graph the ruling answered is recorded with it"


def test_compatible_overlap_with_a_declared_partition_is_admitted(repo):
    write_spec(repo, wid="WI-300", folder="queued", slug="incumbent")
    path = write_spec(repo)
    event, findings = ADMIT.admit(
        repo,
        rel(repo, path),
        verdict={
            "verdict": ADMIT.COMPATIBLE,
            "partition": [["WI-300"], ["WI-420"]],
        },
    )
    assert findings == []
    assert event["partition"] == [["WI-300"], ["WI-420"]]


def test_a_partition_whose_groups_share_an_id_is_refused(repo):
    write_spec(repo, wid="WI-300", folder="queued", slug="incumbent")
    path = write_spec(repo)
    event, findings = ADMIT.admit(
        repo,
        rel(repo, path),
        verdict={"verdict": ADMIT.COMPATIBLE, "partition": [["WI-300"], ["WI-300"]]},
    )
    assert event is None
    assert "partition groups share WI-300" in joined(findings)


def test_a_conflict_ruling_refuses_admission_and_writes_nothing(repo):
    """A conflict cancels the candidate or replaces it with a draft; both are
    moves AWAY from the queue, so the transaction stops and records nothing."""
    write_spec(repo, wid="WI-300", folder="queued", slug="incumbent")
    path = write_spec(repo)
    event, findings = ADMIT.admit(
        repo,
        rel(repo, path),
        verdict={"verdict": ADMIT.CONFLICT, "cancels": "WI-420"},
    )
    assert event is None
    assert "cannot be admitted" in joined(findings)
    assert path.is_file()
    assert ledger(repo) == []


def test_a_conflict_verdict_recorded_directly_still_demands_its_resolution(repo):
    event, findings = ADMIT.admission_verdict(
        repo, "WI-420", ADMIT.CONFLICT, "0" * 16, "1" * 16
    )
    assert event is None
    assert "neither a cancellation nor a replacement draft" in joined(findings)


def test_an_undeclared_event_field_is_refused(repo):
    event, findings = ADMIT.admission_verdict(
        repo, "WI-420", ADMIT.NO_CONFLICT, "0" * 16, "1" * 16, instruction="do this"
    )
    assert event is None
    assert "undeclared event field(s): instruction" in joined(findings)


def test_a_verdict_word_outside_the_vocabulary_is_refused(repo):
    event, findings = ADMIT.admission_verdict(
        repo, "WI-420", "looks-fine", "0" * 16, "1" * 16
    )
    assert event is None
    assert "is not an admission verdict" in joined(findings)


def test_a_verdict_naming_no_digests_is_refused(repo):
    event, findings = ADMIT.admission_verdict(
        repo, "WI-420", ADMIT.NO_CONFLICT, "", "nope"
    )
    assert event is None
    assert "scope digest '' is not 16 hex" in joined(findings)
    assert "spine digest 'nope' is not 16 hex" in joined(findings)


def test_re_recording_an_unchanged_verdict_is_refused(repo):
    event, findings = ADMIT.admission_verdict(
        repo, "WI-420", ADMIT.NO_CONFLICT, "0" * 16, "1" * 16
    )
    assert findings == []
    again, findings = ADMIT.admission_verdict(
        repo, "WI-420", ADMIT.NO_CONFLICT, "0" * 16, "1" * 16
    )
    assert again is None
    assert "already carries this exact ruling (event {})".format(event["id"]) in joined(
        findings
    )


# --- the transaction's shape --------------------------------------------------


def test_a_spec_outside_draft_may_not_be_admitted(repo):
    path = write_spec(repo, folder="queued", slug="already")
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert "is not in docs/work/draft/" in joined(findings)


def test_an_absent_candidate_is_refused(repo):
    event, findings = ADMIT.admit(repo, "docs/work/draft/WI-999-nothing.md")
    assert event is None
    assert "there is no candidate file at" in joined(findings)


def test_a_refused_candidate_is_left_in_draft_with_an_empty_ledger(repo):
    """ALL-OR-NOTHING. A half-admitted row — moved but unruled — is the state
    the ordering argument exists to make unrepresentable."""
    path = write_spec(repo, safety_class="nonsense", sr_refs=["SR-404"])
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert event is None
    assert path.is_file()
    assert not (repo / "docs" / "work" / "queued" / path.name).exists()
    assert ledger(repo) == []


def test_every_failing_precondition_is_reported_not_just_the_first(repo):
    """A producer fixing a candidate learns all of them in one run (contracts
    §5), rather than one refusal per attempt."""
    path = write_spec(
        repo,
        safety_class="nonsense",
        sr_refs=["SR-404"],
        specref="docs/specs/absent.md",
        components=["CMP-404"],
        source="",
    )
    _event, findings = ADMIT.admit(repo, rel(repo, path))
    assert len(findings) >= 5
    assert all(f.startswith("admit: REFUSED - ") for f in findings)


def test_the_admitted_event_records_the_declaration_it_ruled_on(repo):
    path = write_spec(repo)
    event, findings = ADMIT.admit(repo, rel(repo, path))
    assert findings == []
    assert event["declared"]["components"] == ["CMP-001"]
    assert event["declared"]["sr_refs"] == ["SR-001"]
    assert event["declared"]["safety_class"] == "ordinary"


def test_the_event_id_is_derived_from_the_facts(repo):
    path = write_spec(repo)
    event, _ = ADMIT.admit(repo, rel(repo, path))
    assert event["id"] == OUTCOME.event_id(event)


# --- TC-174 (Integration): the freshness gate ---------------------------------


def test_a_direct_write_into_the_queue_is_refused_by_the_strict_check(repo):
    """The `direct-write` permutation of TC-172 and the `absent` permutation of
    TC-174 are one state seen from one side: a queued spec no transaction ruled
    on.

    The repo must have ADOPTED the transaction first, which is what the ledger's
    presence means. Without that step this test passed vacuously for the wrong
    reason — a repo with no admissions ledger has never run an admission, so
    every queued row it has predates the transaction and the rung is deliberately
    silent (a rule about a transaction the repo never adopted would otherwise red
    every fixture tree in the suite that builds a queued spec). The defect under
    test is a write that went AROUND a transaction the repo has, so the fixture
    has to have one.
    """
    admitted = write_spec(repo)
    _event, findings = ADMIT.admit(repo, rel(repo, admitted))
    assert findings == [], findings

    # A DISTINCT id: `write_spec` defaults to one, and two specs sharing it made
    # the smuggled row match the admitted row's verdict by id — the rung saw a
    # ruling and stayed silent, so the test passed for a reason that had nothing
    # to do with the property.
    write_spec(repo, wid="WI-421", folder="queued", slug="smuggled")
    findings = CHECK.admission_verdict_findings(repo)
    assert len(findings) == 1, findings
    assert "smuggled" in findings[0]
    assert "queued with no admission verdict" in findings[0]
    assert "admit.py" in findings[0]


def test_the_rung_is_silent_until_the_repo_has_adopted_the_transaction(repo):
    """Presence-as-consent, pinned so the silence is a decision.

    The same tree, with and without the ledger. Unpinned, this reads as the rung
    being broken; pinned, it reads as the migration boundary it is — and if a
    later change makes the rung fire before adoption, the seven fixture modules
    it would red are found HERE instead of in their own suites.
    """
    write_spec(repo, folder="queued", slug="predates-the-transaction")
    ledger = repo / "docs" / "events" / "admissions.jsonl"
    assert not ledger.exists()
    assert CHECK.admission_verdict_findings(repo) == []

    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text("", encoding="utf-8", newline="\n")
    findings = CHECK.admission_verdict_findings(repo)
    assert len(findings) == 1, findings
    assert "queued with no admission verdict" in findings[0]


def test_a_moved_scope_stales_the_verdict(repo):
    """The `stale-scope` permutation."""
    path = write_spec(repo)
    _event, findings = ADMIT.admit(repo, rel(repo, path))
    assert findings == []
    queued = repo / "docs" / "work" / "queued" / path.name
    _write(
        queued,
        queued.read_text(encoding="utf-8").replace(
            '"A candidate"', '"A quietly widened candidate"'
        ),
    )
    findings = CHECK.admission_verdict_findings(repo)
    assert len(findings) == 1
    assert "computed against scope digest" in findings[0]
    assert "the ruling judged different text" in findings[0]


def test_a_moved_spine_stales_the_verdict(repo):
    """The `stale-spine` permutation: the referenced requirement was amended
    after the ruling, so the verdict judged a different requirement tree."""
    path = write_spec(repo)
    _event, findings = ADMIT.admit(repo, rel(repo, path))
    assert findings == []
    csv_path = repo / "docs" / "requirements" / "system-requirements.csv"
    _write(
        csv_path,
        csv_path.read_text(encoding="utf-8").replace(
            "shall add two numbers", "shall add two integers"
        ),
    )
    findings = CHECK.admission_verdict_findings(repo)
    assert len(findings) == 1
    assert "computed against spine digest" in findings[0]
    assert "a different requirement tree" in findings[0]


def test_an_attestation_alone_stales_the_verdict(unattested_repo):
    """The spine digest covers the ANCHOR as well as the current text, and this
    is the case where that second half is the ONLY thing that moves: not one
    character of the requirement changes, but the row goes from unattested to
    anchored, and a ruling made before that was made against a weaker tree.

    It is driven through the MIGRATION path on purpose, because that is the only
    way a row reaches the queue over unattested references — `admit` refuses
    them outright (`test_a_reference_with_no_anchor_at_all_is_refused`), which
    is precisely why the anchor half earns its place: it covers the rows the
    precondition never saw."""
    write_spec(unattested_repo, folder="queued", slug="legacy")
    written, findings = ADMIT.seed(unattested_repo)
    assert (written, findings) == (["WI-420"], [])
    assert CHECK.admission_verdict_findings(unattested_repo) == []
    ATTEST.seed(unattested_repo, unattested_repo / "docs")
    findings = CHECK.admission_verdict_findings(unattested_repo)
    assert len(findings) == 1
    assert "computed against spine digest" in findings[0]


def test_a_queued_row_under_a_conflict_ruling_is_refused(repo):
    """A ruling that REFUSED admission is not a ruling that permits the row to
    sit in the queue — otherwise the transaction's own refusal is ignored by
    leaving the file where it is."""
    write_spec(repo, folder="queued", slug="ruled-out")
    queued = repo / "docs" / "work" / "queued" / "WI-420-ruled-out.md"
    scope, spine = ADMIT.candidate_digests(repo, queued.read_text(encoding="utf-8"))
    event, findings = ADMIT.admission_verdict(
        repo, "WI-420", ADMIT.CONFLICT, scope, spine, cancels="WI-420"
    )
    assert findings == [] and event is not None
    findings = CHECK.admission_verdict_findings(repo)
    assert len(findings) == 1
    assert "queued under a conflict ruling" in findings[0]


def test_the_example_row_is_not_a_registry_entry(repo):
    _write(repo / "docs" / "work" / "queued" / "WI-000-example.md", "+++\n+++\n")
    assert CHECK.admission_verdict_findings(repo) == []


def test_the_gate_is_vacuous_on_an_empty_queue(repo):
    assert CHECK.admission_verdict_findings(repo) == []


def test_a_malformed_ledger_line_is_reported_rather_than_swallowed(repo):
    """ "the ledger is unreadable" and "no row has a verdict" are different facts
    and must not print the same."""
    write_spec(repo, folder="queued", slug="incumbent")
    path = repo / "docs" / "events" / "admissions.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not json}\n", encoding="utf-8", newline="\n")
    findings = CHECK.admission_verdict_findings(repo)
    assert len(findings) == 1
    assert "admissions.jsonl line 1 is not valid JSON" in findings[0]


# --- the migration arm --------------------------------------------------------


def test_seed_writes_one_pre_transaction_verdict_per_unruled_queued_row(repo):
    write_spec(repo, wid="WI-300", folder="queued", slug="legacy-a")
    write_spec(repo, wid="WI-301", folder="queued", slug="legacy-b")
    written, findings = ADMIT.seed(repo)
    assert findings == []
    assert written == ["WI-300", "WI-301"]
    assert {e["verdict"] for e in ledger(repo)} == {ADMIT.BASELINE}
    assert CHECK.admission_verdict_findings(repo) == []


def test_the_migration_word_is_not_an_adjudicated_one(repo):
    """`attest.BASELINE`'s reasoning, dogfooded: a machine cannot adjudicate,
    and a ledger of machine baselines spelled `no-conflict` is later counted as
    that many rulings that were never made."""
    assert ADMIT.BASELINE not in ADMIT.VERDICTS
    assert ADMIT.BASELINE in ADMIT.DECISIONS


def test_a_migrated_row_still_expires(repo):
    """The whole reason a migration beats an exemption list: the debt is
    recorded AND current."""
    write_spec(repo, wid="WI-300", folder="queued", slug="legacy")
    ADMIT.seed(repo)
    assert CHECK.admission_verdict_findings(repo) == []
    queued = repo / "docs" / "work" / "queued" / "WI-300-legacy.md"
    _write(
        queued,
        queued.read_text(encoding="utf-8").replace('"A candidate"', '"Wider now"'),
    )
    findings = CHECK.admission_verdict_findings(repo)
    assert len(findings) == 1
    assert "scope digest" in findings[0]


def test_seed_never_writes_over_a_ruling_somebody_made(repo):
    path = write_spec(repo)
    ADMIT.admit(repo, rel(repo, path))
    written, findings = ADMIT.seed(repo)
    assert (written, findings) == ([], [])
    assert len(ledger(repo)) == 1


def test_seed_carries_a_ruling_of_its_own_nowhere(repo):
    event, findings = ADMIT.admission_verdict(
        repo, "WI-420", ADMIT.BASELINE, "0" * 16, "1" * 16, ordering=["WI-420"]
    )
    assert event is None
    assert "records pre-transaction carrying a ruling" in joined(findings)


# --- the spine digest's declared boundary -------------------------------------


def test_the_spine_digest_covers_only_the_referenced_rows(repo):
    """The boundary `spine_digest` states rather than leaves to be discovered:
    amending an UNREFERENCED requirement does not stale a verdict."""
    before = ADMIT.spine_digest(repo, ["SR-001"])
    csv_path = repo / "docs" / "requirements" / "system-requirements.csv"
    _write(
        csv_path,
        csv_path.read_text(encoding="utf-8").replace(
            "shall subtract two numbers", "shall subtract two integers"
        ),
    )
    assert ADMIT.spine_digest(repo, ["SR-001"]) == before
    assert ADMIT.spine_digest(repo, ["SR-002"]) != ADMIT.spine_digest(repo, ["SR-001"])


def test_the_spine_digest_is_a_function_of_the_reference_set_not_its_order(repo):
    assert ADMIT.spine_digest(repo, ["SR-001", "SR-002"]) == ADMIT.spine_digest(
        repo, ["SR-002", "SR-001", "SR-001"]
    )


def test_the_digest_prefix_is_inside_the_hashed_bytes():
    """Changing the rule must change the prefix, so an old digest reads as old
    rather than as agreeing (contracts §4)."""
    assert ADMIT.SPINE_PREFIX == "spine-v1"


# --- the entry point ----------------------------------------------------------


def test_the_cli_admits_and_exits_zero(repo, capsys):
    path = write_spec(repo)
    assert ADMIT.main(["--root", str(repo), rel(repo, path)]) == 0
    assert "WI-420 -> docs/work/queued" in capsys.readouterr().out
    assert len(ledger(repo)) == 1


def test_the_cli_prints_every_refusal_and_exits_non_zero(repo, capsys):
    """Contracts §5: a finding list is printed one per line, ALL of them, before
    the exit — a caller fixing a candidate learns every problem in one run."""
    path = write_spec(repo, safety_class="nonsense", sr_refs=["SR-404"], source="")
    assert ADMIT.main(["--root", str(repo), rel(repo, path)]) == 1
    err = capsys.readouterr().err.strip().splitlines()
    assert len(err) >= 3
    assert all(line.startswith("admit: REFUSED - ") for line in err)


def test_the_overlaps_arm_reports_and_changes_nothing(repo, capsys):
    write_spec(repo, wid="WI-300", folder="queued", slug="incumbent")
    path = write_spec(repo)
    assert ADMIT.main(["--root", str(repo), "--overlaps", rel(repo, path)]) == 0
    out = capsys.readouterr().out
    assert "admit: OVERLAP -" in out
    assert path.is_file()
    assert ledger(repo) == []


def test_the_seed_arm_reports_what_it_migrated(repo, capsys):
    write_spec(repo, wid="WI-300", folder="queued", slug="legacy")
    assert ADMIT.main(["--root", str(repo), "--seed"]) == 0
    assert "seeded 1 pre-transaction verdict(s)" in capsys.readouterr().out


# --- the F5 copies this module carries ----------------------------------------


def test_the_safety_class_vocabulary_matches_the_scheduler():
    """A copy is sanctioned; DRIFT is not. Two vocabularies that disagree would
    let a class pass admission and then fail to schedule."""
    assert ADMIT.SAFETY_CLASSES == SCHEDULE.SAFETY_CLASSES


def test_the_status_directory_table_matches_the_validator():
    """A folder declared in some readers and not others is SKIPPED by the ones
    that do not know it, so its ids go missing from the uniqueness guard this
    transaction leans on."""
    assert ADMIT.SPEC_STATUS_DIRS == CHECK.SPEC_STATUS_DIRS
