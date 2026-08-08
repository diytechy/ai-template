"""resume_plan.py — the pure resume planner, the component-safe spine batch and
the exactly-once red-bar rung (SR-145/SR-146/SR-147; LLR-168..171 + LLR-186;
TC-162/TC-163/TC-164, and the wiring half of TC-165/TC-180).

What these tests are actually built to defend, and the shape each is driven on:

  * **the precedence is a precedence, not a habit.** Every rung is selected by a
    snapshot that satisfies only it, AND — the half that matters — every ORDERED
    PAIR of rungs is driven: a snapshot satisfying both a higher and a lower rung
    must select the higher one, for all 28 pairs. Testing only the eight happy
    paths would pass on an implementation that checked the rungs in any order at
    all, since each fixture would have exactly one arm to hit.

  * **purity is a property, not a comment.** `plan` is called with
    `builtins.__import__`, `builtins.open`, `io.open`, `os.open` and
    `subprocess.Popen` all replaced by things that raise. A deferred import is a
    file read, so this is what actually holds the line against "just import
    attest here for the boundary" — the exact shortcut the snapshot's
    `decider` annotation exists to avoid. The fixture-tree half then proves the
    same thing from the other side: bytes in, bytes out, nothing moved.

  * **the collapse is the requirement, not the fallback.** The disconnected case
    proves batches can separate at all; each connecting edge and the missing
    owner prove they collapse. The three-row case is the one that matters: it
    distinguishes "collapsed because an ownership edge crossed" from "collapsed
    because everything was connected anyway", which a two-row fixture cannot,
    and it is the mutation proof for the cross-edge rung.

  * **exactly-once is the identity.** One failure, one event, one draft; the
    repeat drafts nothing; a different step drafts one more. The recovery case —
    a cycle that minted the event and died before drafting — is driven too,
    because that is the state a dedup-by-refusal-string implementation silently
    strands forever.

**The mutation proofs, RUN rather than reasoned to** (each applied to an
isolated copy of `resume_plan.py`, the suite run, the module restored):

| Mutation | Result (of 80) |
|---|---|
| delete the cross-ownership collapse loop from `spine_components` | 1 red — `..._collapses_more_than_connectivity_alone`, with exactly the predicted `(('WI-101','WI-102'),('WI-103',))` |
| add `import attest` to the body of `plan` | 8 red — every rung of the purity sweep |
| drop the adoption gate on the digest rung | 3 red — the unadopted-repo test, the trace-wiring test and the dispatcher's planner gate |
| delete the per-rung `_finding_stop` call | 9 red — every refuse permutation plus the corrupt-ledger and gate tests |
| reverse the declared rung order | 32 red — the pair sweep, wholesale |
| stop passing `snapshot.trace` to `spine_components` | 1 red — the trace-wiring test, which is why it exists beside the `spine_components` units |

No git and no subprocess: the failure key's tree id is a literal 40-hex (which
is all `outcome.failure_event` validates), the candidate mint reads folders, and
the one dispatch rung driven here takes its bar through the injection seam. The
drain behind the dispatcher's stop is `_station_exit`'s already-proven
machinery and is stubbed rather than rebuilt — what is driven here is which rung
stops and with which exit code.
"""

import builtins
import io
import itertools
import json
import os
import subprocess

import pytest
from conftest import load_script

resume_plan = load_script("resume_plan")
attest = load_script("attest")
outcome = load_script("outcome")
adjudicate = load_script("adjudicate")
dispatch = load_script("dispatch")

TREE = "c" * 40
TS = "2026-08-08T00:00:00Z"


# --- single-rung snapshot literals (TC-162) -----------------------------------
# One entry per declared rung: the smallest field set that makes THAT rung have
# work. Keyed by rung so the pair sweep below can merge any two without knowing
# what either contains.
ONLY = {
    resume_plan.OUTCOMES: {
        "outcomes": (
            {
                "event": "0123456789abcdef",
                "wi": "WI-041",
                "outcome": "partial",
                "triggers": ("outcome-partial",),
            },
        )
    },
    resume_plan.DIGESTS: {
        "digests": (
            {"kind": "SR", "id": "SR-140", "digest": "a" * 16, "decider": "human"},
        )
    },
    resume_plan.DRAFTS: {"drafts": ("docs/work/draft/WI-900-repair.md",)},
    resume_plan.CHECKPOINT: {"checkpoint": "final_full_spine_review=always"},
    resume_plan.SPINE: {
        "spine_ready": (
            {"id": "WI-101", "sr_refs": ["SR-140"], "components": ["CMP-004"]},
        )
    },
    resume_plan.ORDINARY: {"ordinary_ready": (("WI-102", "ordinary"),)},
    resume_plan.REMEDIATION: {
        "stage": 4,
        "gate": "G3",
        "bar": resume_plan.Bar(False, tree=TREE, step="tests", output="boom"),
    },
    resume_plan.DRAINED: {},
}


def _snapshot(*rungs, **over):
    """A Snapshot satisfying exactly the named rungs (plus any override)."""
    fields = {}
    for rung in rungs:
        fields.update(ONLY[rung])
    fields.update(over)
    return resume_plan.Snapshot(**fields)


def test_tc162_two_runs_over_one_snapshot_return_one_decision():
    """`repeat`. SR-145's promise is that two readers of one tree dispatch the
    same work; over one frozen snapshot that reduces to the planner being a
    function, which is the only form of it a test can actually check."""
    snap = _snapshot(resume_plan.SPINE, resume_plan.ORDINARY)
    assert resume_plan.plan(snap) == resume_plan.plan(snap)


@pytest.mark.parametrize("rung", resume_plan.RUNGS)
def test_tc162_each_rung_is_selected_by_a_snapshot_that_satisfies_only_it(rung):
    """The eight declared permutations: `outcome | digest | vetting | checkpoint
    | spine | ordinary | red-bar | drained`."""
    decision = resume_plan.plan(_snapshot(rung))
    assert decision.rung == rung
    assert decision.rank == resume_plan.RANK[rung]
    assert decision.reason


@pytest.mark.parametrize(
    "higher,lower",
    [
        pair
        for pair in itertools.combinations(resume_plan.RUNGS, 2)
        if pair[1] != resume_plan.DRAINED
    ],
)
def test_tc162_no_lower_rung_is_selected_while_a_higher_one_has_work(higher, lower):
    """THE ORDERING PROPERTY, driven per pair rather than on the happy path.

    28 pairs, each a snapshot where two rungs have work at once. A planner that
    checked its rungs in any other order — or that returned the LAST match
    instead of the first — passes the eight single-rung tests above and fails
    here, which is exactly why both exist. (`drained` is excluded as a lower
    rung: it is the absence of work, so "both have work" is not a state it can
    be in.)"""
    decision = resume_plan.plan(_snapshot(higher, lower))
    assert decision.rung == higher
    assert decision.rank < resume_plan.RANK[lower]


def test_a_spine_batch_names_one_component_not_the_whole_frontier():
    """The spine rung hands its caller ONE batch (SR-146's exclusive unit), not
    every ready spine row: admitting two independent components together would
    be the composition nobody reviewed."""
    snap = resume_plan.Snapshot(
        spine_ready=(
            {"id": "WI-101", "sr_refs": ["SR-140"], "components": ["CMP-004"]},
            {"id": "WI-102", "sr_refs": ["SR-999"], "components": ["CMP-009"]},
        )
    )
    decision = resume_plan.plan(snap)
    assert decision.rung == resume_plan.SPINE
    assert decision.action == resume_plan.BATCH
    assert decision.items == ("WI-101",)


def test_a_digest_rung_inside_the_human_boundary_recommends_rather_than_enacts():
    """A rung whose whole population is a human's to decide must not tell the
    loop to enact it. Two words, not a boolean: `recommend` says what happens
    next where `False` would only say what does not."""
    human_only = resume_plan.plan(_snapshot(resume_plan.DIGESTS))
    assert human_only.action == resume_plan.RECOMMEND
    mixed = resume_plan.plan(
        resume_plan.Snapshot(
            digests=(
                {"kind": "SR", "id": "SR-140", "decider": "human"},
                {"kind": "TC", "id": "TC-150", "decider": "adjudicator"},
            )
        )
    )
    assert mixed.action == resume_plan.ADJUDICATE


def test_a_bar_result_nobody_took_is_not_a_green():
    """Stage 4 with NO bar in hand must not select the red rung, and must not
    pretend the bar passed either — it drains, because "we did not look" is a
    third state and this module refuses to fold it into the other two."""
    assert resume_plan.plan(resume_plan.Snapshot(stage=4)).rung == resume_plan.DRAINED
    green = resume_plan.Snapshot(stage=4, bar=resume_plan.Bar(True))
    assert resume_plan.plan(green).rung == resume_plan.DRAINED
    below = resume_plan.Snapshot(
        stage=3, bar=resume_plan.Bar(False, tree=TREE, step="tests", output="x")
    )
    assert resume_plan.plan(below).rung == resume_plan.DRAINED


@pytest.mark.parametrize(
    "rung", [r for r in resume_plan.RUNGS if r != resume_plan.DRAINED]
)
def test_an_unreadable_input_refuses_at_its_own_rung_and_stops_the_precedence(rung):
    """A rung whose input would not read must REFUSE, and must not let any lower
    rung run: a corrupt outcomes ledger read as "nothing pending" would dispatch
    work past the very record that might have withdrawn it. Driven per rung —
    every rung's finding must stop the ladder at its own height, and each is
    given the LOWEST rung with real work to be tempted by, so the refusal has
    the longest possible ladder to fall down before it is caught."""
    tempters = [] if rung == resume_plan.REMEDIATION else [resume_plan.REMEDIATION]
    snap = _snapshot(
        *tempters,
        findings=((rung, "resume_plan: REFUSED - the ledger is corrupt (test)"),),
    )
    decision = resume_plan.plan(snap)
    assert decision.rung == rung
    assert decision.action == resume_plan.REFUSE
    assert decision.items == ("resume_plan: REFUSED - the ledger is corrupt (test)",)


def test_a_finding_never_hides_a_higher_rung():
    """The other direction of the same rule: a finding at rung 6 must not
    suppress rung 1. Damage stops the ladder at its own height, no higher."""
    snap = _snapshot(
        resume_plan.OUTCOMES,
        findings=((resume_plan.ORDINARY, "unreadable frontier"),),
    )
    assert resume_plan.plan(snap).rung == resume_plan.OUTCOMES


# --- TC-163: purity -----------------------------------------------------------


class _Boom(Exception):
    pass


def _explode(*_a, **_kw):
    raise _Boom("the planner reached for the outside world")


@pytest.mark.parametrize("rung", resume_plan.RUNGS)
def test_tc163_the_planner_touches_no_file_and_spawns_no_process(monkeypatch, rung):
    """LLR-168's actual contract, made a guard rather than a claim.

    Everything a module could use to reach the outside world is replaced with a
    raise: `__import__` (a deferred import IS a file read — and it is the
    tempting shortcut here, since a rung could reach for `attest.requires_human`
    or `derive_gate.verification_gate_for`), `open`/`io.open`/`os.open`, and
    `subprocess.Popen`. Driven for every rung, because a violation added to one
    arm would otherwise hide behind the seven that do not run.

    MUTATION PROOF, RUN: adding `import attest` to the body of `plan` reds all
    eight of these. Adding `Path(snapshot.root).exists()` reds none of them,
    which is why the fixture-tree test below exists as well — this guard catches
    reaching OUT, that one catches writing.

    The patches are undone before anything is asserted. A `_Boom` escaping into
    pytest's own failure reporting takes the whole session down with an
    INTERNALERROR (measured), which is a violation reported as a crash instead
    of as one red test — so the escape is caught here and turned into a normal
    assertion."""
    monkeypatch.setattr(builtins, "open", _explode)
    monkeypatch.setattr(io, "open", _explode)
    monkeypatch.setattr(os, "open", _explode)
    monkeypatch.setattr(subprocess, "Popen", _explode)
    monkeypatch.setattr(builtins, "__import__", _explode)
    reached, decision = None, None
    try:
        decision = resume_plan.plan(_snapshot(rung))
    except _Boom as exc:
        reached = str(exc)
    finally:
        monkeypatch.undo()
    assert reached is None, "plan() at rung {}: {}".format(rung, reached)
    assert decision.rung == rung


# --- the fixture tree the snapshot is read from -------------------------------

SN_MD = """# Stakeholder Needs (SN-###)

## Core needs

| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-001 | Add two numbers. | Demo. | M | add(1,2) gives 3. |
"""

SRS = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,"
    "Priority,Verification,Status\n"
    "SR-001,Addition,SN-001,shall add,realizes,adds,,M,Test,Verified\n"
    "SR-002,Subtraction,SN-001,shall subtract,realizes,subtracts,,M,Test,Verified\n"
)
LLRS = (
    "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Component\n"
    "LLR-001,SR-001,Adder,src/demo,add,pure,(see TC),Implemented,CMP-001\n"
)
TCS = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
    "TC-001,SR-001;LLR-001,Unit,call add,Smoke,a=1,sum,Yes,tests/t.py,Verified\n"
)
IFS = (
    "IF-ID,Direction,ThisProject,Counterpart,Contract,SR-Refs,Version,Stability,"
    "Status,Component,Notes\n"
    "IF-001,Provides,a,b,the seam,SR-001;SR-002,v1,Stable,Stable,CMP-001,\n"
)


def _spec(root, folder, wid, *, safety="ordinary", extra=""):
    path = root / "docs" / "work" / folder / "{}-slug.md".format(wid)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "+++\n"
        'id = "{}"\n'
        'title = "Work {}"\n'
        'safety_class = "{}"\n'
        "{}"
        "+++\n"
        "\n## Context\n\nThe obligation as filed.\n".format(wid, wid, safety, extra),
        encoding="utf-8",
        newline="\n",
    )
    return path


def _tree(
    tmp_path,
    *,
    ledgers=("outcomes", "attestation", "admissions", "review-requests"),
    seed_draft=True,
    seed_queued=True,
):
    """A repo-shaped tree: the four registries, a queued spine row, a queued
    ordinary row, optionally a draft candidate, and whichever event ledgers this
    case says the repo has ADOPTED (an empty file is adoption — presence is
    consent)."""
    root = tmp_path / "repo"
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "stakeholder-needs.md").write_text(SN_MD, encoding="utf-8", newline="\n")
    (req / "system-requirements.csv").write_text(SRS, encoding="utf-8", newline="\n")
    (req / "low-level-requirements.csv").write_text(
        LLRS, encoding="utf-8", newline="\n"
    )
    (req / "interfaces.csv").write_text(IFS, encoding="utf-8", newline="\n")
    (root / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "test" / "test-cases.csv").write_text(
        TCS, encoding="utf-8", newline="\n"
    )
    for folder in ("draft", "queued", "complete", "cancelled", "partial"):
        (root / "docs" / "work" / folder).mkdir(parents=True, exist_ok=True)
    events = root / "docs" / "events"
    events.mkdir(parents=True, exist_ok=True)
    for name in ledgers:
        (events / (name + ".jsonl")).touch()
    if seed_queued:
        _spec(
            root,
            "queued",
            "WI-101",
            safety="spine",
            extra='sr_refs = ["SR-001"]\ncomponents = ["CMP-001"]\n',
        )
        _spec(root, "queued", "WI-102")
    if seed_draft:
        _spec(root, "draft", "WI-103")
    return root


def _fingerprint(root):
    """Every file under `root` as `{relpath: bytes}` — the whole tree, so a write
    anywhere (a ledger line, a lock file, a cache) shows up as a difference
    rather than as a passing test that only checked the file we expected."""
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def test_tc163_the_snapshot_carries_every_declared_input(tmp_path):
    """LLR-169's list, field by field, off a real tree: the pending outcome
    events, the changed digests, the draft candidates, the checkpoint state, the
    frontier and the last bar result. A snapshot missing one of these is a
    planner deciding without it."""
    root = _tree(tmp_path)
    event, findings = outcome.write_outcome(
        root,
        "WI-041",
        "partial",
        "a" * 40,
        "b" * 40,
        "0123456789abcdef",
        ts=TS,
        commits=["b" * 40],
        checks=[{"step": "tests", "result": "1 passed"}],
    )
    assert findings == [], findings
    request = attest.review_request_event("the owner asked", by="peter")
    attest.append_event(root, request, ts=TS)

    bar = resume_plan.Bar(False, tree=TREE, step="tests", output="boom", gate="G3")
    snap = resume_plan.snapshot(root, bar=bar)

    assert snap.adopted == frozenset(resume_plan.LEDGERS)
    assert [o["event"] for o in snap.outcomes] == [event["id"]]
    assert snap.outcomes[0]["triggers"] == ("outcome-partial",)
    # Nothing is attested in this tree, so every spine row is a candidate.
    assert {c["id"] for c in snap.digests} == {
        "SN-001",
        "SR-001",
        "SR-002",
        "LLR-001",
        "TC-001",
    }
    assert all(c["decider"] in ("human", "adjudicator") for c in snap.digests)
    assert snap.drafts == ("docs/work/draft/WI-103-slug.md",)
    assert "the owner asked" in snap.checkpoint
    assert [row["id"] for row in snap.spine_ready] == ["WI-101"]
    assert snap.spine_ready[0]["components"] == ["CMP-001"]
    assert ("WI-102", "ordinary") in snap.ordinary_ready
    assert (snap.stage, snap.gate) == (0, "G1")
    assert snap.bar is bar
    assert snap.findings == ()


def test_tc163_snapshot_then_plan_leaves_the_tree_byte_identical(tmp_path):
    """`fixture-tree`. Every byte under the root, before and after — so a write
    the author did not think to look for still fails the test."""
    root = _tree(tmp_path)
    before = _fingerprint(root)
    snap = resume_plan.snapshot(root)
    decision = resume_plan.plan(snap)
    assert decision.rung in resume_plan.RUNGS
    assert _fingerprint(root) == before


def test_an_unadopted_repo_reads_drained_rather_than_stopped(tmp_path):
    """THE ADOPTION RULE, driven in both directions.

    Without an attestation ledger, `attest.detect_candidates` reports every
    spine row as unattested — so an ungated rung 2 would stop every existing
    repo on its first tick. With the ledger present (empty is enough: presence
    is consent), the same tree raises all five. One `touch` is the whole
    difference, which is what makes this a guard rather than a hope."""
    root = _tree(tmp_path, ledgers=())
    unadopted = resume_plan.snapshot(root)
    assert unadopted.adopted == frozenset()
    assert unadopted.digests == ()
    assert unadopted.outcomes == ()
    assert unadopted.drafts == ()
    assert unadopted.checkpoint == ""
    # It gets on with the work it has, which is the whole point.
    assert resume_plan.plan(unadopted).rung == resume_plan.SPINE

    (root / "docs" / "events" / "attestation.jsonl").touch()
    adopted = resume_plan.snapshot(root)
    assert len(adopted.digests) == 5
    assert resume_plan.plan(adopted).rung == resume_plan.DIGESTS


def test_a_corrupt_ledger_becomes_that_rungs_finding_not_a_silent_zero(tmp_path):
    """The snapshot half of the fail-closed rule: an unreadable ledger is
    recorded AGAINST ITS RUNG, so the pure planner can stop at exactly the
    height of the damage."""
    root = _tree(tmp_path)
    (root / "docs" / "events" / "outcomes.jsonl").write_text(
        "{not json\n", encoding="utf-8", newline="\n"
    )
    snap = resume_plan.snapshot(root)
    assert snap.outcomes == ()
    assert [where for where, _msg in snap.findings] == [resume_plan.OUTCOMES]
    decision = resume_plan.plan(snap)
    assert (decision.rung, decision.action) == (
        resume_plan.OUTCOMES,
        resume_plan.REFUSE,
    )


def test_the_trace_graph_is_read_from_the_registries_own_ref_cells(tmp_path):
    """`trace_edges` must be the registries' edges, not a second graph beside
    them: an LLR's SR-Refs, a TC's Verifies, an SR's SN-Refs and an IF row's
    SR-Refs."""
    root = _tree(tmp_path)
    edges = resume_plan.trace_edges(root)
    assert edges["LLR-001"] == ["SR-001"]
    assert edges["TC-001"] == ["LLR-001", "SR-001"]
    assert edges["SR-001"] == ["SN-001"]
    assert edges["IF-001"] == ["SR-001", "SR-002"]


# --- TC-164: the connected-component partition --------------------------------


def _row(wid, refs=(), interfaces=(), components=("CMP-001",)):
    return {
        "id": wid,
        "sr_refs": list(refs),
        "interfaces": list(interfaces),
        "components": list(components),
    }


def test_tc164_disconnected_rows_partition_into_separate_batches():
    """`disconnected`. Two rows citing nothing in common, owned by different
    components, admit as two batches — the case that proves the partition can
    separate at all, without which every other assertion here is vacuous."""
    partition = resume_plan.spine_components(
        [
            _row("WI-101", refs=["SR-001"], components=["CMP-001"]),
            _row("WI-102", refs=["SR-002"], components=["CMP-002"]),
        ]
    )
    assert partition.batches == (("WI-101",), ("WI-102",))
    assert not partition.collapsed


def test_tc164_a_trace_edge_collapses_the_batch():
    """`trace-edge`. Neither row cites the other and their spine refs are
    disjoint — but the registries declare `LLR-001 -> SR-001`, so the graph says
    they are one piece of work whatever the ownership column claims."""
    rows = [
        _row("WI-101", refs=["SR-001"], components=["CMP-001"]),
        _row("WI-102", refs=["LLR-001"], components=["CMP-002"]),
    ]
    apart = resume_plan.spine_components(rows)
    assert len(apart.batches) == 2  # without the edge they are independent
    together = resume_plan.spine_components(rows, trace={"LLR-001": ["SR-001"]})
    assert together.batches == (("WI-101", "WI-102"),)
    # A Snapshot carries the graph as PAIRS (a frozen record holds no dict), so
    # both shapes have to reach the same partition or the planner and a direct
    # caller would answer differently about the same registries.
    as_pairs = resume_plan.spine_components(rows, trace=(("LLR-001", ("SR-001",)),))
    assert as_pairs.batches == together.batches


def test_the_planner_partitions_with_the_registries_declared_trace_graph(tmp_path):
    """THE WIRING, which is the half a `spine_components` unit test cannot see:
    `snapshot` must actually hand the declared graph to `plan`, or LLR-170's
    trace edges are built and never used.

    Two spine rows whose refs are disjoint — `SR-001` and `LLR-001` — but which
    the fixture's own registry joins (`LLR-001` decomposes `SR-001`). The
    planner must return them as ONE batch. (No ledgers: this tree is about the
    spine rung, and an adopted-but-empty attestation ledger would legitimately
    stop it two rungs higher.)"""
    root = _tree(tmp_path, seed_draft=False, seed_queued=False, ledgers=())
    _spec(
        root,
        "queued",
        "WI-201",
        safety="spine",
        extra='sr_refs = ["SR-001"]\ncomponents = ["CMP-001"]\n',
    )
    _spec(
        root,
        "queued",
        "WI-202",
        safety="spine",
        extra='sr_refs = ["LLR-001"]\ncomponents = ["CMP-002"]\n',
    )
    snap = resume_plan.snapshot(root)
    assert dict(snap.trace)["LLR-001"] == ["SR-001"]
    decision = resume_plan.plan(snap)
    assert decision.rung == resume_plan.SPINE
    assert decision.items == ("WI-201", "WI-202")

    # MUTATION PROOF, in the test itself: drop the graph and the same two rows
    # admit as two independent batches — the unreviewed composition SR-146 is
    # about.
    without = resume_plan.plan(snap._replace(trace=()))
    assert without.items == ("WI-201",)


def test_the_trace_graph_is_not_read_when_there_is_no_spine_work(tmp_path):
    """Four registry reads per idle tick to build a graph nothing will ask about
    is pure cost, so the graph is read only when there is a partition to make."""
    root = _tree(tmp_path)
    snap = resume_plan.snapshot(root)
    assert snap.spine_ready and snap.trace  # spine work: the graph is there
    (root / "docs" / "work" / "queued" / "WI-101-slug.md").unlink()
    assert resume_plan.snapshot(root).trace == ()


def test_tc164_an_interface_edge_collapses_the_batch():
    """`interface-edge`. Same shape, the other edge kind: a shared declared seam
    is a connection even when no requirement is."""
    partition = resume_plan.spine_components(
        [
            _row(
                "WI-101", refs=["SR-001"], interfaces=["IF-001"], components=["CMP-001"]
            ),
            _row(
                "WI-102", refs=["SR-002"], interfaces=["IF-001"], components=["CMP-002"]
            ),
        ]
    )
    assert partition.batches == (("WI-101", "WI-102"),)


def test_tc164_a_row_with_no_owner_collapses_to_one_project_wide_batch():
    """`missing-owner`. The fail-safe direction: an unowned row cannot be
    excluded from a partition without guessing, and guessing wrong ships an
    unreviewed composition."""
    partition = resume_plan.spine_components(
        [
            _row("WI-101", refs=["SR-001"], components=["CMP-001"]),
            _row("WI-102", refs=["SR-002"], components=[]),
        ]
    )
    assert partition.batches == (("WI-101", "WI-102"),)
    assert partition.collapsed
    assert any("declares no owning component" in r for r in partition.reasons)


def test_tc164_a_cross_ownership_edge_collapses_more_than_connectivity_alone():
    """THE CASE THAT MAKES THE CROSS-EDGE RUNG NON-VACUOUS, and the reason a
    two-row fixture cannot prove it.

    Three rows: WI-101 and WI-102 are connected but declare DIFFERENT owning
    components; WI-103 is connected to neither. Connectivity alone answers two
    batches (`{101,102}`, `{103}`) — and that answer is wrong, because the
    ownership partition the batch would be reviewed under has an edge crossing
    it. The correct answer is one project-wide batch of all three.

    MUTATION PROOF: delete the cross-ownership loop from `spine_components` and
    this test alone fails, with `batches == (('WI-101','WI-102'),('WI-103',))`.
    Every other TC-164 case still passes without it, which is precisely why it
    is here."""
    rows = [
        _row("WI-101", refs=["SR-001"], components=["CMP-001"]),
        _row("WI-102", refs=["SR-001"], components=["CMP-002"]),
        _row("WI-103", refs=["SR-009"], components=["CMP-003"]),
    ]
    partition = resume_plan.spine_components(rows)
    assert partition.batches == (("WI-101", "WI-102", "WI-103"),)
    assert partition.collapsed
    assert any("crossing the proposed partition" in r for r in partition.reasons)

    # And the control: give the connected pair one shared owner and the third
    # row separates again, so the collapse above is the ownership edge and not
    # merely "this function collapses".
    rows[1] = _row("WI-102", refs=["SR-001"], components=["CMP-001", "CMP-002"])
    kept = resume_plan.spine_components(rows)
    assert kept.batches == (("WI-101", "WI-102"), ("WI-103",))
    assert not kept.collapsed


def test_a_row_with_no_id_collapses_rather_than_being_dropped():
    """A row nobody can name cannot be placed in a batch — and must not be
    silently omitted, which would hand back a partition that excluded live
    work."""
    partition = resume_plan.spine_components([_row("WI-101"), _row("")])
    assert partition.collapsed
    assert partition.batches == (("WI-101",),)
    assert any("declares no id" in r for r in partition.reasons)


def test_a_declaration_carries_its_refs_in_any_shape_the_readers_write_them():
    """A spec's TOML frontmatter holds lists, a registry cell holds a
    `;`-separated string, and a hand-written frontmatter holds a bare string.
    All three name the same rows, so the graph's edges must not depend on which
    reader filled the record."""
    partition = resume_plan.spine_components(
        [
            {"id": "WI-101", "sr_refs": "SR-001;SR-002", "components": "CMP-001"},
            {"id": "WI-102", "sr_refs": ["~SR-002"], "component": ["CMP-001"]},
        ]
    )
    assert partition.batches == (("WI-101", "WI-102"),)
    assert not partition.collapsed


def test_no_candidate_rows_is_an_empty_partition_not_a_batch_of_nothing():
    assert resume_plan.spine_components([]) == resume_plan.Partition((), ())


# --- P12: the exactly-once red-bar rung ---------------------------------------


def _failure_text(*, colour=False, secs="3.10", stamp="2026-08-08T04:15:02Z"):
    """One harness failure as TWO observers would print it. Everything varied
    here is observer state — the terminal's colour support, the wall clock, how
    long the machine took — and none of it is the defect, so both spellings must
    normalise to one fingerprint."""
    head = "\x1b[31mFAIL\x1b[0m" if colour else "FAIL"
    return (
        "{}  tests            exit 1\n"
        "  tests/test_widget.py:42: AssertionError\n"
        "  assert widget(2) == 4\n"
        "  1 failed, 39 passed in {}s at {}\n".format(head, secs, stamp)
    )


def _bar(step="tests", output=None, tree=TREE):
    return resume_plan.Bar(
        False,
        tree=tree,
        step=step,
        output=_failure_text() if output is None else output,
        gate="G3",
    )


def _drafts(root):
    return sorted(p.name for p in (root / "docs" / "work" / "draft").glob("WI-*.md"))


def test_the_red_bar_rung_mints_one_event_and_one_draft_then_none(tmp_path):
    """SR-147 end to end through `remediate`: `first | repeat | different-step |
    different-fingerprint`.

    The repeat is the SAME failure seen by a DIFFERENT OBSERVER — colour on
    instead of off, another clock, another machine's timing — because the
    identity is a property of the failure and not of the cycle that watched it.
    A repeat that varied the defect itself would prove nothing."""
    root = _tree(tmp_path, seed_draft=False)

    first = resume_plan.remediate(root, _bar(), effort="40000", buildtier="strong")
    assert first.findings == () or list(first.findings) == []
    assert first.draft.startswith("draft/")
    assert first.event
    text = (root / "docs" / "work" / first.draft).read_text(encoding="utf-8")
    assert adjudicate.read_lineage(text)["source_event"] == first.event
    assert 'buildtier = "strong"' in text
    assert 'est_tokens = "40000"' in text
    assert _drafts(root) == [first.draft.split("/")[-1]]

    again = resume_plan.remediate(
        root,
        _bar(
            output=_failure_text(
                colour=True, secs="31.02", stamp="2026-08-09T22:00:41Z"
            )
        ),
    )
    assert again.draft is None
    assert again.event == first.event
    assert any(first.draft in f for f in again.findings), again.findings
    assert _drafts(root) == [first.draft.split("/")[-1]]

    # different-step and different-fingerprint each mint one more.
    other_step = resume_plan.remediate(root, _bar(step="lint"))
    assert other_step.draft and other_step.event != first.event
    other_failure = resume_plan.remediate(
        root, _bar(output=_failure_text().replace("widget(2) == 4", "widget(3) == 9"))
    )
    assert other_failure.draft and other_failure.event != first.event
    assert len(_drafts(root)) == 3

    ledger = (root / "docs" / "events" / "failures.jsonl").read_text(encoding="utf-8")
    assert len(ledger.splitlines()) == 3


def test_a_cycle_that_minted_but_never_drafted_recovers_on_its_next_pass(tmp_path):
    """THE CRASH CASE, and the reason the key is looked up rather than parsed
    back out of a refusal sentence.

    A cycle that persisted the failure event and then died before drafting must,
    next pass, find that event and draft from it. An implementation that keyed
    the recovery on `failure_event`'s refusal string would strand this state
    forever: the mint refuses, and nothing ever drafts."""
    root = _tree(tmp_path, seed_draft=False)
    bar = _bar()
    event, findings = outcome.failure_event(
        root, bar.tree, bar.step, bar.output, gate=bar.gate, ts=TS
    )
    assert findings == [] and event
    assert _drafts(root) == []

    recovered = resume_plan.remediate(root, bar)
    assert recovered.event == event["id"]
    assert recovered.draft
    assert len(_drafts(root)) == 1
    ledger = (root / "docs" / "events" / "failures.jsonl").read_text(encoding="utf-8")
    assert len(ledger.splitlines()) == 1  # no second event for one failure


def test_a_green_bar_mints_nothing_and_refuses_by_name(tmp_path):
    """A remediation event asserts a failure. Minting one from a pass would put
    a defect nobody observed into the queue."""
    root = _tree(tmp_path, seed_draft=False)
    result = resume_plan.remediate(root, resume_plan.Bar(True, gate="G3"))
    assert result.draft is None and result.event == ""
    assert any("REFUSED" in f and "GREEN" in f for f in result.findings)
    assert not (root / "docs" / "events" / "failures.jsonl").exists()
    assert _drafts(root) == []


def test_an_untyped_bar_result_is_refused_rather_than_keyed_on(tmp_path):
    """The failure key is read off `Bar`'s declared fields; an untyped result
    would key the event on whatever it happened to carry."""
    root = _tree(tmp_path)
    result = resume_plan.remediate(root, {"ok": False, "step": "tests"})
    assert result.draft is None
    assert any("does not carry the declared bar fields" in f for f in result.findings)
    assert not (root / "docs" / "events" / "failures.jsonl").exists()


# --- the dispatch wiring ------------------------------------------------------


def test_the_dispatch_remediation_rung_stops_the_run_nonzero(tmp_path):
    """A red trunk bar at stage 4 records the event, drafts the repair, and ends
    the run NON-ZERO. Recording the failure and then exiting 0 would be this
    kit's own dishonest green: the queue really is drained, and trunk really is
    broken, and the second fact is the one that decides the exit code.

    Stage 4 is REAL here, not stubbed: `attest.seed` writes a baseline anchor
    for every row, so `derive_gate.spine_stage` derives 4 from the ledger the
    way it will in production. Faking the stage would have proved the fake. The
    repeat is driven with the admission ledger ABSENT, so the drafts rung is
    silent and the repeat genuinely re-reaches this rung — the adopted case is
    the test below, where a higher rung takes over instead."""
    root = _tree(
        tmp_path, seed_draft=False, seed_queued=False, ledgers=("attestation",)
    )
    attest.seed(root)
    calls = []

    def probe(root_, gate, tier):
        calls.append((gate, tier))
        return _bar()

    code = dispatch._remediation_rung(root, "all", probe)
    assert code == 1
    assert calls == [("G3", "all")]
    assert len(_drafts(root)) == 1
    assert (root / "docs" / "events" / "failures.jsonl").is_file()

    # A repeat records nothing new and STILL stops the run: exactly-once is
    # about the RECORD, never about whether trunk is still broken.
    again = dispatch._remediation_rung(root, "all", probe)
    assert again == 1
    assert len(_drafts(root)) == 1
    ledger = (root / "docs" / "events" / "failures.jsonl").read_text(encoding="utf-8")
    assert len(ledger.splitlines()) == 1


def test_a_repair_row_awaiting_admission_outranks_a_second_remediation(tmp_path):
    """Once the repair candidate exists and the repo has adopted the admission
    transaction, the loop's next answer is the DRAFT rung — vet the row — and
    not another lap at the red bar. That is the flowchart's `N -> F` edge, and
    it is what stops the rung from being a spin: the second cycle's answer is
    the thing that was produced by the first."""
    root = _tree(tmp_path, seed_draft=False, seed_queued=False)
    attest.seed(root)
    assert dispatch._remediation_rung(root, "all", lambda r, g, t: _bar()) == 1
    assert len(_drafts(root)) == 1

    probed = []
    assert (
        dispatch._remediation_rung(
            root, "all", lambda r, g, t: probed.append(g) or _bar()
        )
        is None
    )
    assert resume_plan.plan(resume_plan.snapshot(root)).rung == resume_plan.DRAFTS


def test_the_dispatch_remediation_rung_never_probes_below_stage_four(tmp_path):
    """The probe is a full harness run. A repo whose breakdown is still in
    process must never pay for it — and a stage the planner could not derive is
    not a stage 4."""
    root = _tree(tmp_path)  # nothing attested: stage 0
    called = []

    def probe(root_, gate, tier):
        called.append(gate)
        return _bar()

    assert dispatch._remediation_rung(root, "all", probe) is None
    assert called == []


def test_the_planner_gate_stops_on_an_upper_rung_and_falls_through_below_it(
    tmp_path, monkeypatch
):
    """The dispatcher's half of the precedence: the four judgement rungs end the
    run into the owner's queue, and the work rungs fall THROUGH to §A8
    admission, whose barrier and merge slot this module does not re-decide.

    The drain behind the stop is `_station_exit`'s own machinery and is stubbed
    here — what is driven is which rung stops and with which code."""
    root = _tree(tmp_path, ledgers=())
    monkeypatch.setattr(dispatch, "_residue_wi_count", lambda r: 0)
    monkeypatch.setattr(dispatch, "_drain", lambda r, t: 0)
    state = {"merged": 0, "stall": 0, "cycles": 0, "fatal": None}

    # Unadopted: the ordinary rung — fall through, admission decides.
    assert dispatch._planner_gate(root, "all", state) is None

    # Adopt attestation and the digest rung stops the run at 0.
    (root / "docs" / "events" / "attestation.jsonl").touch()
    assert dispatch._planner_gate(root, "all", state) == 0

    # A corrupt ledger stops it NON-ZERO: "unreadable" is not "empty".
    (root / "docs" / "events" / "outcomes.jsonl").write_text(
        "{not json\n", encoding="utf-8", newline="\n"
    )
    assert dispatch._planner_gate(root, "all", state) != 0


def test_the_planner_gate_never_runs_before_a_parked_branch_is_resumed():
    """Crash recovery outranks every judgement (plan §9). The parked-resume arm
    returns before the planner is consulted, so a claimed branch always comes
    home first — asserted over the source's own ordering because the alternative
    is a live station."""
    import inspect

    source = inspect.getsource(dispatch._admit)
    assert source.index("_admit_parked") < source.index("_planner_gate")


@pytest.mark.parametrize(
    "report,expected",
    [
        ("  PASS  lint      ok\n  FAIL  tests     exit 1\n", "tests"),
        # A SKIP is a refusal (`integrate._run_bar`'s rule), so it names the
        # step too — and it sorts AFTER any FAIL, because a step that failed is
        # a better description of the failure than a step that never ran.
        ("  SKIP  privacy   no tool\n  FAIL  tests     exit 1\n", "tests"),
        ("  SKIP  privacy   no tool\n", "privacy"),
        ("no such interpreter", "bar"),
    ],
)
def test_the_bar_probe_names_the_first_red_step(report, expected):
    """The `step` half of the failure key, read out of check.py's own report
    line. `bar` stands in when the report names nothing at all — which is what a
    probe that could not launch produces, and which must still be a red."""
    assert dispatch._failing_step(report) == expected


def test_the_bar_probe_runs_the_integrators_declared_bar_not_a_second_one(
    tmp_path, monkeypatch
):
    """`_trunk_bar` must go through `integrate._run_bar`, which already owns how
    this kit runs its declared bar — the repo's own check.py, `--trunk-lane`,
    and the fail-closed reading in which a SKIP is a refusal. A private copy
    would be a second answer to "was the bar green", and the two would drift the
    first time either is corrected."""
    root = _tree(tmp_path)
    seen = {}

    def fake_run_bar(wt, root_, tier, gate=None):
        seen.update(wt=str(wt), tier=tier, gate=gate)
        return False, "  FAIL  tests     exit 1\n", "bar exit 1"

    monkeypatch.setattr(dispatch.integrate, "_run_bar", fake_run_bar)
    monkeypatch.setattr(dispatch.ac, "git", lambda r, *a: (0, TREE + "\n"))
    bar = dispatch._trunk_bar(root, "G2", "smoke")
    assert seen == {"wt": str(root), "tier": "smoke", "gate": "G2"}
    assert (bar.ok, bar.step, bar.tree, bar.gate) == (False, "tests", TREE, "G2")
    assert "FAIL  tests" in bar.output

    monkeypatch.setattr(
        dispatch.integrate, "_run_bar", lambda *a, **k: (True, "RESULT: PASS", "ok")
    )
    green = dispatch._trunk_bar(root, "G2", "smoke")
    assert green.ok and green.tree == ""  # a green bar carries no failure key


def test_the_planner_module_ships_to_a_scaffold():
    """dispatch.py reaches for `resume_plan` at every idle tick, so a scaffold
    without it cannot run the walk-away loop at all. A MAPPING row is the whole
    fix, and its absence would be invisible until an adopter's first run."""
    bootstrap = load_script("bootstrap")
    assert ("scripts/resume_plan.py", "scripts/resume_plan.py") in bootstrap.MAPPING


def test_the_planner_json_records_are_plain_json_serialisable(tmp_path):
    """A Decision's items and reason travel into logs and, at P13, into events.
    Anything that cannot round-trip as JSON is a surprise deferred to the caller
    that first tries."""
    root = _tree(tmp_path)
    decision = resume_plan.plan(resume_plan.snapshot(root))
    json.dumps(
        {
            "rung": decision.rung,
            "action": decision.action,
            "items": list(decision.items),
        }
    )
