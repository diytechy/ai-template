"""WI-969, in process: a disposition ADOPTS an already-filed successor.

The request's grammar (the adoption block, beside the drafts, inside a section
whose fences must pair), the disposed row read from the disposition row's
title, the acceptance rule over a listing the caller supplies, the record's
strict reader, the record-change judgement the commit check wraps, and the
shared close shape whose relink oracle admits the close's exact relinks. No
git beyond the census's `git ls-files`: the end-to-end close, commit check and
sweep live in test_handback.py, test_adoption_record.py, test_intake.py,
test_verdict_record.py and test_consolidate_close.py (slow tier); each family
keeps its in-process pin here, in the smoke tier.

Two evidence classes (coordinator-cycle skill §3, Intent): new or corrected
behaviour is a strict expected failure (`_RED`) whose red reaches the test's
own assertion, the absent functions standing as stubs; a characterization of
behaviour already correct is unmarked and names, in its docstring, the wrong
implementation it would catch.
"""

import re
import subprocess
import sys
import tomllib

import pytest
from conftest import ROOT, SCRIPTS, load_script

if str(SCRIPTS) not in sys.path:  # the kit's script-sibling import idiom
    sys.path.insert(0, str(SCRIPTS))

from kitlib import adoption  # noqa: E402
from kitlib import registry  # noqa: E402
from kitlib import verdict as kverdict  # noqa: E402

intake = load_script("intake")
consolidate = load_script("consolidate")

#: New or corrected behaviour: red until its build row lands, at its own
#: assertion (an import or attribute error is not this class's red).
_RED = {"strict": True, "raises": (AssertionError, pytest.fail.Exception)}

_PARTIAL_TITLE = (
    "dispose: the close recorded at docs/handbacks/WI-005-wi-005.md - cancel / "
    "defer / draft a successor (a disposition row never closes early; R3)"
)
_CANCEL_TITLE = (
    "dispose: the cancellation recorded at "
    "docs/archive/work/cancelled/WI-005-the-thing.md - cancel / defer"
)


def _section(*blocks):
    return "\n## Dispositions\n\n" + "".join(
        "```toml\n{}```\n\nprose\n\n".format(b) for b in blocks
    )


_DRAFT = 'title = "t"\nsupersedes = "WI-005"\n'


# --- P3: the request's grammar ------------------------------------------------


def test_an_adoption_block_is_parsed_apart_from_the_drafts():
    text = _section('adopts = "WI-450"\n', _DRAFT)
    drafts, adoptions, refusal = intake.parse_disposition_section(text, "w")
    assert refusal is None, refusal
    assert adoptions == ["WI-450"]
    assert [d["title"] for d in drafts] == ["t"]
    # The draft-only reader (scheduler, gate) sees the draft and nothing else.
    assert [d["title"] for d in intake.parse_dispositions(text, "w")[0]] == ["t"]
    assert adoption.KEY not in intake._DRAFT_KEYS


@pytest.mark.parametrize(
    "block,reason",
    [
        ('adopts = "WI-450"\ntitle = "t"\n', "exactly one key"),
        ('adopts = "WI-450"\nsupersedes = "WI-005"\n', "exactly one key"),
        ('adopts = "WI-450;WI-451"\n', "exactly one WI-### id"),
        ('adopts = ["WI-450"]\n', "exactly one WI-### id"),
        ('adopts = " WI-450"\n', "exactly one WI-### id"),
    ],
    ids=["beside-title", "beside-supersedes", "joined", "list", "padded"],
)
def test_a_malformed_adoption_block_is_a_parse_refusal(block, reason):
    drafts, adoptions, refusal = intake.parse_disposition_section(_section(block), "w")
    assert refusal is not None and reason in refusal, refusal
    assert drafts == [] and adoptions == []


@pytest.mark.parametrize(
    "title,disposition,wanted",
    [
        (_PARTIAL_TITLE, True, "WI-005"),
        (_CANCEL_TITLE, True, "WI-005"),
        ("dispose: the WI-005 close", True, None),
        ("dispose: the close recorded at docs/handbacks/notes.md", True, None),
        ("dispose: recorded at a/WI-1-x.md and recorded at b/WI-2-y.md", True, None),
        # Only a disposition row's title is read: a spot check owes no successor.
        (_PARTIAL_TITLE, False, None),
    ],
    ids=[
        "report",
        "cancellation",
        "no-token",
        "no-id",
        "two-tokens",
        "not-disposition",
    ],
)
def test_the_disposed_row_is_read_from_either_minted_title_form(
    title, disposition, wanted
):
    wid, refusal = adoption.disposed_id(title, disposition=disposition)
    if wanted:
        assert (wid, refusal) == (wanted, None)
    else:
        assert wid is None
        assert refusal is not None and "event token" in refusal, refusal


def _entry(state, wid, supersedes=None, text=None, raw=None):
    """One `(relpath, read)` listing entry, as the tree reader yields it:
    `read()` returns the spec's text, or raises as a strict decode does."""
    rel = "{}/{}-row.md".format(state, wid)
    if raw is not None:
        return rel, lambda: raw.decode("utf-8")
    lines = ['id = "{}"'.format(wid), 'title = "row"']
    if supersedes:
        lines.append("supersedes = {}".format(supersedes))
    body = text if text is not None else "+++\n" + "\n".join(lines) + "\n+++\n"
    return rel, lambda: body


_OTHER = _entry("queued", "WI-460", supersedes='"WI-005"')


@pytest.mark.parametrize(
    "listing,reason",
    [
        ([_OTHER, _entry("queued", "WI-450", supersedes='"WI-005"')], None),
        ([_entry("draft", "WI-450", supersedes='["WI-004", "WI-005"]')], None),
        ([_entry("active/wi-450", "WI-450", supersedes='"WI-005"')], None),
        ([_OTHER], "names no open row"),
        ([_entry("complete", "WI-450", supersedes='"WI-005"')], "names no open row"),
        ([_entry("cancelled", "WI-450", supersedes='"WI-005"')], "names no open row"),
        (
            [_entry("queued", "WI-450", raw=b'+++\nid = "WI-450"\n# \xff\n+++\n')],
            "cannot read",
        ),
        ([_entry("queued", "WI-450", text="+++\nid = \n+++\n")], "cannot read"),
        (
            [
                _entry("queued", "WI-450", supersedes='"WI-005"'),
                _entry("draft", "WI-450", supersedes='"WI-005"'),
            ],
            "cannot read",
        ),
        (
            [_entry("queued", "WI-450", supersedes='"WI-006"')],
            "does not supersede WI-005",
        ),
        ([_entry("queued", "WI-450")], "does not supersede WI-005"),
    ],
    ids=[
        "queued",
        "draft-list",
        "active",
        "missing",
        "complete",
        "cancelled",
        "not-utf8",
        "unparseable",
        "two-specs",
        "other-lineage",
        "no-supersedes",
    ],
)
def test_acceptance_is_read_against_the_registry_with_distinct_refusals(
    listing, reason
):
    refusal = adoption.row_refusal(listing, "WI-450", "WI-005")
    if reason is None:
        assert refusal is None, refusal
    else:
        assert refusal is not None and reason in refusal, refusal


def test_an_adoption_never_counts_as_an_absorption():
    """`consolidate._enacted_supersedes` is unchanged: it reads only a
    consolidate outcome's drafts' `supersedes`, and an adoption carries none.

    Adequacy witness: a reader that took any id-valued cell of a block,
    `adopts` included, as an absorbed row would answer `["WI-450"]` here."""
    text = '\n## Consolidation\n\n```toml\noutcome = "consolidate"\n```\n' + _section(
        'adopts = "WI-450"\n'
    )
    assert consolidate._enacted_supersedes(text, "w") == []


def test_a_repeated_adoption_is_a_parse_refusal():
    text = _section('adopts = "WI-450"\n', 'adopts = "WI-450"\n')
    drafts, adoptions, refusal = intake.parse_disposition_section(text, "w")
    assert refusal is not None and "repeat" in refusal.lower(), refusal
    assert "WI-450" in refusal
    assert drafts == [] and adoptions == []


@pytest.mark.parametrize(
    "valid,unclosed",
    [
        ('adopts = "WI-450"\n', 'adopts = "WI-451"\n'),
        (_DRAFT, 'title = "u"\nsupersedes = "WI-005"\n'),
    ],
    ids=["adoption", "draft"],
)
def test_a_valid_block_then_an_unclosed_one_is_refused(valid, unclosed):
    text = _section(valid) + "```toml\n" + unclosed + "\nmore prose\n"
    drafts, adoptions, refusal = intake.parse_disposition_section(text, "w")
    assert refusal is not None and "fence" in refusal.lower(), refusal
    assert drafts == [] and adoptions == []
    # The drafts-only reader refuses the same section: no draft is lost.
    assert intake.parse_dispositions(text, "w")[0] == []


@pytest.mark.parametrize("fence", ["```text", "````"], ids=["text", "four"])
def test_a_fence_that_is_not_toml_or_a_bare_close_is_refused(fence):
    text = _section(_DRAFT) + fence + "\nsome lines\n" + fence + "\n"
    drafts, adoptions, refusal = intake.parse_disposition_section(text, "w")
    assert refusal is not None and "fence" in refusal.lower(), refusal
    assert drafts == [] and adoptions == []


#: A second block written off column zero, after a valid first one: indented
#: and left unclosed, nested under a list bullet, or opened at column zero and
#: closed by an indented fence.
_INDENTED = {
    "indented-unclosed": ' ```toml\nadopts = "WI-451"\n\nunfinished successor\n',
    "bullet-nested": '- also:\n  ```toml\n  adopts = "WI-451"\n  ```\n',
    "indented-close": '```toml\nadopts = "WI-451"\n  ```\n',
}


@pytest.mark.parametrize("tail", list(_INDENTED.values()), ids=list(_INDENTED))
@pytest.mark.parametrize(
    "valid", ['adopts = "WI-450"\n', _DRAFT], ids=["adoption", "draft"]
)
def test_a_fence_line_off_column_zero_is_refused(valid, tail):
    """A line whose text begins with three backticks after leading whitespace
    is a fence line too, and only the column-zero form is canonical: an
    indented one refuses the section by name rather than folding its block
    into the previous block's scope prose."""
    text = _section(valid) + tail
    drafts, adoptions, refusal = intake.parse_disposition_section(text, "w")
    assert refusal is not None and "fence" in refusal.lower(), refusal
    assert "not start at column zero" in refusal, refusal
    assert drafts == [] and adoptions == []


# --- D12: the census over every Dispositions section the repository holds -----

#: Trunk's own block reader, frozen as it stood before the fences paired, so
#: the census compares the new parser with what the old one returned.
_FROZEN_FENCE_RE = re.compile(r"```toml\s*\n(.*?)```", re.S)
_DISPOSITIONS_RE = re.compile(r"^## Dispositions\s*$", re.M)
_CENSUS_HOMES = ("docs/work", "docs/archive/work", "docs/reviews")


def _census_files():
    """`[(relpath, text)]` of every tracked markdown file under the census
    homes that carries a `## Dispositions` section."""
    listed = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--", *_CENSUS_HOMES],
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.split()
    found = []
    for rel in listed:
        if not rel.endswith(".md"):
            continue
        text = (ROOT / rel).read_text(encoding="utf-8")
        if _DISPOSITIONS_RE.search(text):
            found.append((rel, text))
    return found


def _frozen_titles(text):
    """The draft titles trunk's frozen reader found in the section, and how
    many blocks it saw; None when a block is not TOML (trunk refused it)."""
    section = text.partition("\n## Dispositions")[2].split("\n## ", 1)[0]
    blocks = _FROZEN_FENCE_RE.findall(section)
    try:
        parsed = [tomllib.loads(block) for block in blocks]
    except tomllib.TOMLDecodeError:
        return None
    return [p.get("title") for p in parsed if adoption.KEY not in p], len(blocks)


def _assert_census_entry(rel, text):
    drafts, adoptions, refusal = intake.parse_disposition_section(text, rel)
    assert refusal is None or "fence" not in refusal.lower(), (rel, refusal)
    frozen = _frozen_titles(text)
    if rel.startswith("docs/reviews/") or refusal or frozen is None:
        return  # a verdict file is checked for pairing only
    titles, count = frozen
    assert [d["title"] for d in drafts] == titles, rel
    assert len(drafts) + len(adoptions) == count, rel


#: The block each planted case appends to a real section: unclosed at column
#: zero, or complete but nested under a list bullet.
_PLANTS = {
    "planted": '\n\n```toml\ntitle = "planted"\n\nprose\n',
    "planted-indented": '\n\n- planted:\n  ```toml\n  title = "planted"\n  ```\n',
}


def _planted(files, case):
    """One real spec whose `## Dispositions` section ends the file, with the
    `case` block appended to that section."""
    rel, text = next(
        (r, t)
        for r, t in files
        if not r.startswith("docs/reviews/")
        and "\n## " not in t.partition("\n## Dispositions")[2]
    )
    return rel, text.rstrip("\n") + _PLANTS[case]


@pytest.mark.parametrize(
    "case",
    [
        "repository",
        "planted",
        "planted-indented",
    ],
)
def test_every_dispositions_section_in_the_repository_passes_the_fence_grammar(
    case,
):
    """D12: no tracked `## Dispositions` section fails the tightened grammar,
    and each spec's drafts are the drafts trunk's reader returned.

    The `repository` case is a characterization (it passes before and after
    P3). Adequacy witness: a pairing step that refused a bare closing fence,
    or a parser that dropped a block the frozen reader found, fails it; so
    does any tracked section holding a fence line off column zero, which the
    parser refuses. The planted cases are the census's live instruments: an
    unpaired copy of a real section, and one with a bullet-nested block, must
    be refused, or the census proves nothing."""
    files = _census_files()
    assert files, "the census found no Dispositions section to judge"
    if case == "repository":
        for rel, text in files:
            _assert_census_entry(rel, text)
        return
    rel, text = _planted(files, case)
    _drafts, _adoptions, refusal = intake.parse_disposition_section(text, rel)
    assert refusal is not None and "fence" in refusal.lower(), (rel, refusal)


# --- P5: the record's cell, its strict reader and the record-change table -----


@pytest.mark.parametrize(
    "data,wanted",
    [
        ({}, None),
        ({"adopted": ["WI-450"]}, ["WI-450"]),
        ({"adopted": ["WI-451", "WI-450"]}, ["WI-451", "WI-450"]),
        ({"adopted": "WI-450"}, "refused"),
        ({"adopted": []}, "refused"),
        ({"adopted": {"id": "WI-450"}}, "refused"),
        ({"adopted": [450]}, "refused"),
        ({"adopted": ["WI-450", "WI-450"]}, "refused"),
        ({"adopted": ["WI-45x"]}, "refused"),
        ({"adopted": [" WI-450"]}, "refused"),
    ],
    ids=[
        "absent",
        "one",
        "two-in-order",
        "bare-string",
        "empty-list",
        "table",
        "non-string",
        "repeated",
        "malformed",
        "padded",
    ],
)
def test_the_record_reader_accepts_only_a_list_of_distinct_ids(data, wanted):
    ids, refusal = adoption.record_ids(data, "w.md")
    if wanted is None:
        assert (ids, refusal) == (None, None)
    elif wanted == "refused":
        assert ids is None
        assert refusal is not None and "adopted" in refusal, refusal
        assert "w.md" in refusal
    else:
        assert refusal is None, refusal
        assert ids is not None and list(ids) == wanted


def test_an_adopted_cell_survives_the_spec_row_reader():
    text = '+++\nid = "WI-401"\ntitle = "t"\nadopted = ["WI-450", "WI-451"]\n+++\n'
    row, _order = registry.parse_spec_row(text, "complete/WI-401-t.md")
    assert row.get("Adopted") == "WI-450;WI-451"


_A = ("WI-450",)
_B = ("WI-451",)


#: A parent's (record, request) pair: none, the request alone, or both.
_NONE, _ASKED, _HELD = (None, None), (None, _A), (_A, _A)


@pytest.mark.parametrize(
    "parents,record,asked,moved,close,invalid,refused",
    [
        # The close's own commit: record equal to request, validation passing.
        ([_ASKED], _A, _A, True, True, None, False),
        # Carried unchanged with its request: a later move, or an edit
        # elsewhere in the spec.
        ([_HELD], _A, _A, True, False, None, False),
        ([_HELD], _A, _A, False, False, None, False),
        # A merge whose record and request some parent already held.
        ([_NONE, _HELD], _A, _A, False, False, None, False),
        ([(_A, _B), _HELD], _A, _A, False, False, None, False),
        # A spec that requests nothing and records nothing.
        ([_NONE], None, None, True, True, None, False),
        # Refused: a record added, changed or removed outside the close.
        ([_ASKED], _A, _A, False, False, None, True),
        ([_ASKED], _A, _A, True, False, None, True),
        ([_HELD], _B, _A, False, False, None, True),
        ([_HELD], None, _A, False, False, None, True),
        # Refused: a carried record whose request changed or was removed.
        ([_HELD], _A, _B, False, False, None, True),
        ([_HELD], _A, None, True, False, None, True),
        # Refused at the close: record unequal to request, or failing validation.
        ([(None, _B)], _A, _B, True, True, None, True),
        ([_ASKED], _A, _A, True, True, "names no open row", True),
        # Refused: a requesting spec moved into complete/ with no record.
        ([_ASKED], None, _A, True, True, None, True),
        ([_ASKED], None, _A, True, False, None, True),
        # A merge whose record neither parent held.
        ([_ASKED, _ASKED], _A, _A, False, False, None, True),
    ],
    ids=[
        "close",
        "carried-moved",
        "carried-edited",
        "merge-held",
        "merge-request-held",
        "neither",
        "added-outside-close",
        "hand-close",
        "changed",
        "removed",
        "carried-request-changed",
        "carried-request-removed",
        "close-unequal",
        "close-invalid",
        "close-no-record",
        "move-no-record",
        "merge-unheld",
    ],
)
def test_the_record_change_table(
    parents, record, asked, moved, close, invalid, refused
):
    got = adoption.record_change(parents, record, asked, moved, close, invalid)
    if refused:
        assert got is not None and "adopted" in got, got
    else:
        assert got is None, got


# --- P7: the shared close shape and its relink oracle -------------------------

_ACTIVE = "docs/work/active/wi-401/WI-401-dispose.md"
_COMPLETE = "docs/work/complete/WI-401-dispose.md"
_REVIEW = "docs/reviews/wi-401/001-REVIEW-A-abc1234.md"


def _fields(*entries):
    return [part.encode("utf-8") for entry in entries for part in entry]


def test_the_close_shape_admits_outside_paths_only_through_the_oracle():
    moved = (("D", _ACTIVE), ("A", _COMPLETE))
    outside = _fields(*moved, ("M", _REVIEW))
    calls = []

    def oracle(answer):
        def relinked(old, new, path, remap):
            calls.append((old, new, path, remap))
            return answer

        return relinked

    def blobs(path):
        return b"old " + path.encode(), b"new " + path.encode()

    # No oracle: the peel's reading, unchanged - an outside path refuses.
    assert kverdict._closed_wi_ids(outside) is None
    # The oracle admits an outside modification only when it answers true...
    got = kverdict._closed_wi_ids(outside, relinked=oracle(True), blobs=blobs)
    assert got == ["WI-401"]
    # ...and receives the path's two blobs and the commit's own remap.
    assert calls == [
        (
            b"old " + _REVIEW.encode(),
            b"new " + _REVIEW.encode(),
            _REVIEW,
            {_ACTIVE: _COMPLETE},
        )
    ]
    assert kverdict._closed_wi_ids(outside, relinked=oracle(False), blobs=blobs) is None
    # An outside path the close created or destroyed is never a relink.
    for status in ("A", "D"):
        fields = _fields(*moved, (status, _REVIEW))
        assert (
            kverdict._closed_wi_ids(fields, relinked=oracle(True), blobs=blobs) is None
        )
