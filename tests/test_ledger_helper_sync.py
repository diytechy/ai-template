"""F5 drift guard for the helpers the mechanized-loop slices duplicated.

The kit's F5 working agreement keeps each script independently copy-able, so a
helper two scripts both need is duplicated rather than extracted, and the census
(`docs/dupes-allow`) records the sanction. **A sanction is not a guard.** The
only real risk of two copies is that they drift — one learns to handle a shape
the other does not — and then two parts of the loop disagree about a fact while
both tests stay green.

This module removes that risk without a shared module, the same way
`tests/test_wi_loader_sync.py` does for the registry readers: it pushes ONE
fixture through BOTH copies and asserts they DECIDE the same, rather than
comparing source text. Text comparison would pass on two copies that are
identically wrong and fail on a comment reflow; behaviour is the property.

Three families are pinned, each named in the census's `mechanized-loop` class:

  * `handback.py` == `outcome.py` — the `-z` diff walk. Both drive the same
    lane-close machinery, and both must refuse a TRUNCATED stream rather than
    process a partial record, which is the failure the `-z` form exists to make
    detectable.
  * `agent_common.py` == `outcome.py` — the `+++` frontmatter parse. The scope
    digest is computed from what this parse returns, so a divergence here would
    make a spec's frozen scope mean one thing to the loader and another to the
    integrator.
  * `attest.py` == `outcome.py` — the append-only JSONL ledger. Contracts §2
    declares one envelope for every ledger; two writers that disagreed about it
    would produce a history no single reader could replay.

Each family's agreement guard is mutation-proven at the bottom — a guard nobody
has seen fail is not a guard (WI-293). Each proof derives what a DRIFTED COPY
would return and asserts the comparison reds. That shape is the point: a proof
that merely fed the guard two different INPUTS shows nothing about the guard's
ability to see drift, which is how family 3's first proof stayed green against a
copy that had forgotten the `id`/`ts` exclusion its own docstring calls
load-bearing.
"""

import hashlib
import json

import pytest
from conftest import load_script

handback = load_script("handback")
outcome = load_script("outcome")
acommon = load_script("agent_common")
attest = load_script("attest")


# --- family 1: the -z diff walk ----------------------------------------------
# Records, not pairs: a rename carries TWO paths after its status, so a reader
# that consumed the stream two tokens at a time would silently mis-associate
# every path after the first rename.
DIFF_STREAMS = [
    "",
    "M\0a.py\0",
    "M\0a.py\0A\0b.py\0D\0c.py\0",
    "R100\0old.py\0new.py\0M\0after.py\0",
    "C75\0src.py\0copy.py\0",
    "M\0docs/work/queued/WI-001-x.md\0M\0docs/log.d/frag.md\0",
]

# A truncated stream is a status token with no path after it (or a rename missing
# its second path) — NOT a stream ending in an empty field, which is what git's
# own `-z` output always produces.
TRUNCATED = [["M"], ["R100", "old.py"], ["M", "a.py", "A"]]


def _fields(stream):
    """Split a `-z` stream the way the real caller does — `[f for f in
    raw.split("\\0") if f]`.

    Dropping the empties is not cosmetic. git's `-z` output always ends with a
    NUL, so keeping the trailing empty field makes every fixture read as a
    status token with no path — i.e. as TRUNCATED — and both walks answer None.
    A comparison of two Nones passes while proving nothing, which is exactly how
    a drift guard becomes decorative.
    """
    return [f for f in stream.split("\0") if f]


@pytest.mark.smoke
@pytest.mark.parametrize("stream", DIFF_STREAMS)
def test_the_two_diff_walks_read_one_stream_alike(stream):
    fields = _fields(stream)
    mine = outcome.diff_records(list(fields))
    assert handback.diff_records(list(fields)) == mine
    # Guard against the vacuous pass described in `_fields`: every fixture but the
    # empty one must actually PRODUCE records for the comparison to mean anything.
    assert mine is not None and (mine != [] or stream == ""), (stream, mine)


@pytest.mark.smoke
@pytest.mark.parametrize("fields", TRUNCATED)
def test_both_diff_walks_refuse_a_truncated_stream(fields):
    assert handback.diff_records(list(fields)) is None
    assert outcome.diff_records(list(fields)) is None


@pytest.mark.smoke
@pytest.mark.parametrize("stream", DIFF_STREAMS[1:])
def test_the_two_revert_op_derivations_agree(stream):
    records = handback.diff_records(_fields(stream))
    assert records, stream
    for status, paths in records:
        assert handback._revert_ops(status, paths) == outcome._revert_ops(status, paths)


# --- family 2: the +++ frontmatter parse --------------------------------------
SPECS = [
    '+++\nid = "WI-001"\ntitle = "t"\n+++\n',
    '+++\nid = "WI-002"\ntitle = "t"\nsr_refs = ["SR-1", "SR-2"]\n+++\n\n## Deliverable\n\nshipped\n',
    '+++\nid = "WI-003"\ntitle = "multi\\nline"\nneeds = ["~WI-002"]\n+++\n\n## Context\n\njoins\n',
    '+++\nid = "WI-004"\ntitle = ""\npriority = 3\n+++\n',
]


@pytest.mark.smoke
@pytest.mark.parametrize("text", SPECS)
def test_the_two_frontmatter_parses_agree(text):
    mine = outcome.parse_spec(text)
    theirs = acommon.parse_spec_frontmatter(text, "fixture.md")
    # outcome.parse_spec returns whatever shape its own caller needs; the SHARED
    # decision is the frontmatter mapping and the body split, so compare those.
    assert mine[0] == theirs[0]
    assert mine[1] == theirs[1]


@pytest.mark.smoke
@pytest.mark.parametrize(
    "bad", ["no fence at all\n", "+++\nid = 1\n", '+++\nid = "x"\n[[[\n+++\n']
)
def test_both_frontmatter_parses_refuse_the_same_malformations(bad):
    mine = theirs = None
    try:
        outcome.parse_spec(bad)
    except Exception as exc:  # noqa: BLE001 — the TYPE is what is pinned below
        mine = type(exc)
    try:
        acommon.parse_spec_frontmatter(bad, "fixture.md")
    except Exception as exc:  # noqa: BLE001
        theirs = type(exc)
    # The TYPE, not merely "did it raise". Two copies that refuse the same text
    # with different exception types are already drifted for any caller that
    # catches by type, and the weaker `(mine is None) == (theirs is None)` this
    # line used to carry could not see that — while the `noqa` above claimed it
    # could.
    assert mine == theirs, (mine, theirs)


# --- family 3: the append-only JSONL ledger -----------------------------------
# A line as it comes BACK off disk, carrying the derived id and the timestamp.
# Both copies exclude those two keys before hashing, and both docstrings call the
# exclusion load-bearing (`ts` is why observing one fact twice is one event, not
# two). Without a fixture that carries them the agreement guard never exercises
# the exclusion at all: a copy that had forgotten it would still agree with its
# sibling on every other fixture below.
REPLAYED_EVENT = {
    "kind": "probe",
    "a": 1,
    "id": "0123456789abcdef",
    "ts": "2026-08-08T07:37:43Z",
}

LEDGER_EVENTS = [
    {"kind": "probe", "a": 1},
    {"kind": "probe", "a": 1, "nested": {"b": [1, 2, 3]}},
    {"kind": "probe", "unicode": "re-wrap — em dash"},
    REPLAYED_EVENT,
]


@pytest.mark.smoke
@pytest.mark.parametrize("payload", LEDGER_EVENTS)
def test_the_two_event_id_derivations_agree(payload):
    """One payload, one id — whichever module hashes it.

    Contracts §2 makes the id the SHA-256 of the canonical payload, which is what
    makes a duplicate detectable and a reader able to verify the ledger rather
    than trust it. Two derivations that disagreed would make the same fact two
    events.
    """
    assert attest.event_id(dict(payload)) == outcome.event_id(dict(payload))


@pytest.mark.smoke
def test_both_readers_refuse_an_unparseable_line_naming_the_file_and_line(tmp_path):
    """A malformed line is a hard read error naming file AND line, in both.

    Contracts §2 forbids silently skipping a record: a ledger that quietly drops
    a line it cannot parse reports a history that never happened, and replayable
    history is the whole reason these files exist.

    What is NOT pinned here, deliberately: the two readers accept different event
    KINDS (attest owns attestation/review-*, outcome owns outcome/bar-failure),
    so feeding one ledger to both would only prove that each rejects the other's
    vocabulary. The shared contract is the ENVELOPE and the refusal, not the
    vocabulary — so the fixture is a line neither can parse as JSON at all.
    """
    path = tmp_path / "ledger.jsonl"
    path.write_text("not json at all\n", encoding="utf-8", newline="\n")
    for module in (attest, outcome):
        with pytest.raises(ValueError) as caught:
            module.read_events(path)
        message = str(caught.value)
        assert "REFUSED" in message, (module.__name__, message)
        assert "ledger.jsonl" in message, (module.__name__, message)
        assert "1" in message, (module.__name__, message)


@pytest.mark.smoke
def test_both_readers_read_an_empty_ledger_as_no_events(tmp_path):
    """An absent history is empty, never an error — both replay from nothing."""
    path = tmp_path / "ledger.jsonl"
    path.write_text("", encoding="utf-8", newline="\n")
    assert attest.read_events(path) == []
    assert outcome.read_events(path) == []


# --- mutation proofs ----------------------------------------------------------
def test_mutation_a_diverged_diff_walk_reds_the_guard():
    """Prove family 1's guard fires: a copy that stops handling renames diverges."""
    stream = [f for f in "R100\0old.py\0new.py\0".split("\0") if f]
    theirs = outcome.diff_records(list(stream))
    drifted = [(status, paths[:1]) for status, paths in theirs]
    assert drifted != handback.diff_records(list(stream))


def test_mutation_a_diverged_frontmatter_parse_reds_the_guard():
    """Prove family 2's guard fires — on BOTH halves it compares.

    Family 2 shipped with no proof at all while the module docstring claimed one,
    which is the same defect class this module exists to catch: a sanction
    standing in for a guard.
    """
    text = SPECS[1]
    data, body = acommon.parse_spec_frontmatter(text, "fixture.md")
    assert isinstance(data.get("sr_refs"), list), "the fixture must carry an array"

    # A copy that stopped carrying array values across. `sr_refs` is exactly that
    # shape, and it is inside the frozen scope digest, so the divergence would be
    # invisible until an integrator refused a merge nobody had changed.
    dropped_arrays = {k: v for k, v in data.items() if not isinstance(v, list)}
    assert dropped_arrays != outcome.parse_spec(text)[0]

    # A copy whose body split kept the closing fence — the off-by-one that would
    # put `+++` inside every frozen region.
    kept_fence = outcome.SPEC_FENCE + "\n" + body
    assert kept_fence != outcome.parse_spec(text)[1]


def _event_id_forgetting_the_exclusion(payload):
    """`event_id` as a copy that dropped the `id`/`ts` exclusion would compute it.

    Written out here rather than monkeypatched onto a module: the drift being
    modelled is a source divergence between two independently-copyable files, so
    the proof has to show the guard SEEING a different derivation, not a module
    being handed a different answer.
    """
    return hashlib.sha256(
        json.dumps(
            payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    ).hexdigest()[:16]


def test_mutation_a_diverged_event_id_reds_the_guard():
    """Prove family 3's guard fires against the drift both docstrings name.

    The first version of this proof compared `event_id({a: 1})` with
    `event_id({a: 2})` — two different payloads — so it restated that hashing is
    injective and stayed green against a copy that had genuinely drifted. It
    never touched the `id`/`ts` exclusion, which is what makes the same fact
    observed twice one event rather than two.
    """
    assert "id" in REPLAYED_EVENT and "ts" in REPLAYED_EVENT, REPLAYED_EVENT
    drifted = _event_id_forgetting_the_exclusion(dict(REPLAYED_EVENT))
    assert drifted != attest.event_id(dict(REPLAYED_EVENT))
    assert drifted != outcome.event_id(dict(REPLAYED_EVENT))
