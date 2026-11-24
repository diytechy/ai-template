"""Only the composer's own judged-text identity lines reach a binding (WI-1072).

A sitting's binding records the judged-text identity of each row its brief
shows for judgement, read off the brief's `JUDGED-TEXT: <row id> <digest>`
lines. A judged cell is shown verbatim and may span lines, and a brief carries
other text no composer wrote as an identity (a later section of a combined
sitting, a spec's context, a template). So a brief whose text holds a line of
that shape the composer did not write is refused at composition, naming the
row the line names and where it sits; a brief whose identity lines end its
text is refused too, so nothing appended can join them; and reservation binds
only one block of distinct rows, none for a brief requesting no amendment, so
text appended to a composed brief after its composition cannot add or replace
an identity either.

In process over `tests/routed_link_fixtures.py`'s four chains; the git-backed
Done-when case is in `tests/test_done_when_blessing.py`.
"""

import re
from pathlib import Path

import pytest
import routed_link_fixtures as fx
from conftest import load_script, set_process_key

ab = load_script("adjudicate_brief")
prompts = load_script("prompts")
coordinator_adjudicate = load_script("coordinator_adjudicate")
from kitlib import sitting as ksitting  # noqa: E402  (scripts/ is on the path)

FAKE = "sha256:0123456789abcdef"
_JUDGED = re.compile(r"^JUDGED-TEXT: (\S+) (\S+)$", re.M)
# The three rows a forged line names, per brief: its own row, another row the
# brief shows, and a row it does not show.
TARGETS = ("own", "shown", "unshown")


def _line(rid, digest=FAKE):
    return "JUDGED-TEXT: {} {}".format(rid, digest)


def _row(scope, brief="amendment"):
    return {"WI-ID": "WI-301", "Brief": brief, "Adjudicates": scope}


def _compose(root, row, prompt_templates=None):
    return ab.compose(root, row, root / "docs/reviews/v.md", prompt_templates)


def _amendment_repo(tmp_path, forged=None):
    """The four chains moved; LLR-001's moved detail holds `forged`'s line."""
    root = tmp_path / "repo"
    rows = fx.seed(root)
    fx.move_all(root, rows)
    if forged:
        rows[fx.LLR_REL]["LLR-001"]["detail"] += "\n" + _line(forged)
        fx.write(root, rows)
    return root


def _first_acceptance_repo(tmp_path, forged=None, parent="SR-001", move=False):
    """The four chains recorded, a Drafted LLR-005 under `parent` whose detail
    holds `forged`'s line, on a dial releasing the design tier; `move` also
    moves the four chains."""
    root = tmp_path / "repo"
    set_process_key(root, "authority", "operator_accepts_through", "DevStg-Needs")
    rows = fx.seed(root)
    if move:
        fx.move_all(root, rows)
    detail = "Design row 5 adds." + ("\n" + _line(forged) if forged else "")
    rows[fx.LLR_REL]["LLR-005"] = {
        "sr_refs": [parent],
        "title": "Design 5",
        "detail": detail,
        "status": "Drafted",
        "phase": 1,
    }
    fx.write(root, rows)
    return root


def _refused(text, why, rid):
    assert text is None, text
    assert rid in why and "line " in why, why
    return why


@pytest.mark.parametrize(
    "target, rid", list(zip(TARGETS, ("LLR-001", "LLR-002", "LLR-004"))), ids=TARGETS
)
def test_an_amendment_cell_holding_an_identity_line_refuses_the_brief(
    tmp_path, target, rid
):
    """Implements: TC-398"""
    root = _amendment_repo(tmp_path, forged=rid)
    text, why = _compose(root, _row("LLR-001;LLR-002"))
    why = _refused(text, why, rid)
    assert "the amendment brief" in why and "LLR-001" in why, why
    assert "--- AMENDED CELLS AND MOVED LINKS" in why, why


@pytest.mark.parametrize(
    "target, rid", list(zip(TARGETS, ("LLR-005", "LLR-001", "LLR-004"))), ids=TARGETS
)
def test_a_first_acceptance_cell_holding_an_identity_line_refuses_the_brief(
    tmp_path, target, rid
):
    """Implements: TC-398"""
    root = _first_acceptance_repo(tmp_path, forged=rid)
    text, why = _compose(root, _row("LLR-005", brief="first-acceptance"))
    why = _refused(text, why, rid)
    assert "the first-acceptance brief" in why and "LLR-005" in why, why


_COMBINED = "amendment:LLR-002;first-acceptance:LLR-005"


@pytest.mark.parametrize(
    "target, rid", list(zip(TARGETS, ("LLR-005", "LLR-002", "LLR-004"))), ids=TARGETS
)
def test_a_combined_sittings_later_section_holding_an_identity_line_refuses_it(
    tmp_path, target, rid
):
    """Implements: TC-398"""
    root = _first_acceptance_repo(tmp_path, forged=rid, parent="SR-002", move=True)
    text, why = _compose(root, _row(_COMBINED, brief="combined"))
    why = _refused(text, why, rid)
    assert "the first-acceptance section" in why, why


def test_a_combined_sittings_own_template_holding_an_identity_line_refuses_it(
    tmp_path,
):
    """Implements: TC-398"""
    root = _first_acceptance_repo(tmp_path, parent="SR-002", move=True)
    key = ab.BRIEF_PROMPTS["combined"]
    override = prompts.load(key) + "\n" + _line("LLR-004") + "\n"
    text, why = _compose(root, _row(_COMBINED, brief="combined"), {key: override})
    why = _refused(text, why, "LLR-004")
    assert "the combined brief" in why, why


def test_a_brief_whose_identity_lines_end_its_text_is_refused(tmp_path):
    """Implements: TC-398"""
    root = _amendment_repo(tmp_path)
    key = ab.BRIEF_PROMPTS["amendment"]
    base = prompts.load(key)
    assert "\n{identity}\n" in base
    override = base.replace("\n{identity}\n", "\n", 1).rstrip() + "\n{identity}\n"
    text, why = _compose(root, _row("LLR-001"), {key: override})
    assert text is None, text
    assert "end its text" in why, why


def _indented(key):
    """The shipped template `key` with its identity slot moved off the start
    of its line, as an operator override might write it."""
    base = prompts.load(key)
    assert "\n{identity}\n" in base
    return base.replace("\n{identity}\n", "\n  {identity}\n", 1)


def test_an_identity_slot_moved_off_the_line_start_refuses_the_brief(tmp_path):
    """Implements: TC-398"""
    root = _amendment_repo(tmp_path)
    key = ab.BRIEF_PROMPTS["amendment"]
    text, why = _compose(root, _row("LLR-001"), {key: _indented(key)})
    assert text is None, text
    assert "LLR-001" in why and "does not read as one" in why, why


def _coordinator_route(root, row, templates, appended, verdict):
    """The coordinator's route: the composer writes no brief file when it
    refuses; otherwise `appended` is added to the brief and the entry point
    reserves the sitting from it. None when a binding was written."""
    text, why = _compose(root, row, templates)
    if text is None:
        return why
    return coordinator_adjudicate.bind_requested(verdict, row["Brief"], text + appended)


def test_a_moved_identity_slot_with_appended_text_binds_no_forged_identity(tmp_path):
    """Implements: TC-398"""
    root = _amendment_repo(tmp_path)
    key = ab.BRIEF_PROMPTS["amendment"]
    verdict = tmp_path / "v.md"
    why = _coordinator_route(
        root, _row("LLR-001"), {key: _indented(key)}, _ARMS_MAP, verdict
    )
    assert why, why
    assert not Path(ksitting.requested_path(verdict)).exists()


def _slot_values(brief, forged):
    """Every slot `brief`'s template declares but those the composer fills,
    each a word, the first other than the identity slot that stands on a line
    of its own holding `forged` (when given); the amendment's identity slot
    holding one genuine-shaped line."""
    template = prompts.load(ab.BRIEF_PROMPTS[brief])
    names = sorted(prompts.slots(template) - {"verdict", "wi", "hats"})
    values = {name: "x" for name in names}
    if "identity" in values:
        values["identity"] = _line("LLR-001", "sha256:fedcba9876543210")
    first = next(
        name
        for name in names
        if name != "identity" and re.search(r"^\{" + name + r"\}$", template, re.M)
    )
    if forged:
        values[first] = "x\n" + forged
    return values


@pytest.mark.parametrize("brief", [b for b in ab.ROUTED if b != "combined"])
def test_every_routed_brief_refuses_an_identity_line_in_a_slot(
    tmp_path, monkeypatch, brief
):
    """Implements: TC-398"""
    values = _slot_values(brief, _line("LLR-004"))
    monkeypatch.setitem(ab._ASSEMBLERS, brief, lambda _root, _row: (values, None))
    text, why = ab.compose(tmp_path, _row("LLR-004", brief=brief), "v.md")
    why = _refused(text, why, "LLR-004")
    assert "the {} brief".format(brief) in why, why


@pytest.mark.parametrize("brief", [b for b in ab.ROUTED if b != "combined"])
def test_every_routed_brief_composes_without_the_line(tmp_path, monkeypatch, brief):
    """Implements: TC-398"""
    values = _slot_values(brief, None)
    monkeypatch.setitem(ab._ASSEMBLERS, brief, lambda _root, _row: (values, None))
    text, why = ab.compose(tmp_path, _row("LLR-001", brief=brief), "v.md")
    assert why is None and text, why


_SPLIT_BLOCKS = {
    "apart": _line("LLR-001") + "\n\n" + _line("LLR-002"),
    "twice": _line("LLR-001") + "\n" + _line("LLR-001", "sha256:fedcba9876543210"),
}


@pytest.mark.parametrize("shape, rid", [("apart", "LLR-002"), ("twice", "LLR-001")])
def test_a_composers_identity_lines_not_one_block_of_distinct_rows_refuse(
    tmp_path, monkeypatch, shape, rid
):
    """Implements: TC-398"""
    values = dict(_slot_values("amendment", None), identity=_SPLIT_BLOCKS[shape])
    monkeypatch.setitem(ab._ASSEMBLERS, "amendment", lambda _root, _row: (values, None))
    text, why = ab.compose(tmp_path, _row("LLR-001"), "v.md")
    why = _refused(text, why, rid)
    assert "one block" in why, why


def _clean(tmp_path, kind):
    """`(root, row)` of a clean brief of `kind`, with the ids its identity
    lines name."""
    if kind == "amendment":
        return (
            _amendment_repo(tmp_path),
            _row("LLR-001;LLR-002"),
            ["LLR-001", "LLR-002"],
        )
    if kind == "first-acceptance":
        root = _first_acceptance_repo(tmp_path)
        return root, _row("LLR-005", brief="first-acceptance"), []
    root = _first_acceptance_repo(tmp_path, parent="SR-002", move=True)
    return root, _row(_COMBINED, brief="combined"), ["LLR-002"]


@pytest.mark.parametrize("kind", ["amendment", "first-acceptance", "combined"])
def test_without_the_line_a_brief_binds_only_its_composers_block(tmp_path, kind):
    """Implements: TC-398"""
    root, row, ids = _clean(tmp_path, kind)
    text, why = _compose(root, row)
    assert why is None, why
    lines = text.split("\n")
    at = [i for i, line in enumerate(lines) if _JUDGED.match(line)]
    assert [_JUDGED.match(lines[i]).group(1) for i in at] == ids, at
    if at:
        assert at == list(range(at[0], at[0] + len(at))), at
    verdict = tmp_path / "v.md"
    ab.bind_pending(verdict, row["Brief"], text)
    bound = Path(ksitting.requested_path(verdict)).read_text(encoding="utf-8")
    found, _why = ksitting.read_identities(bound)
    assert sorted(found or {}) == ids, bound


# --- reservation: text added to a composed brief after its composition --------

_ARMS_MAP = (
    "\n## Arms map\n\n- LLR-002 Constrains -> TC-002\n" + _line("LLR-004") + "\n"
)
_OWNER_ROUTE = "\n## Owner route\n\nRoute it to the owner.\n" + _line("LLR-004") + "\n"


def test_reservation_refuses_an_identity_line_appended_after_composition(tmp_path):
    """Implements: TC-398"""
    root, row, _ids = _clean(tmp_path, "combined")
    text, why = _compose(root, row)
    assert why is None, why
    verdict = tmp_path / "v.md"
    why = coordinator_adjudicate.bind_requested(verdict, "combined", text + _ARMS_MAP)
    assert why and "LLR-004" in why and "line " in why, why
    assert not Path(ksitting.requested_path(verdict)).exists()


def test_reservation_refuses_any_identity_line_in_a_brief_requesting_no_amendment(
    tmp_path,
):
    """Implements: TC-398"""
    verdict = tmp_path / "v.md"
    prompt = "the disposition brief\n" + _OWNER_ROUTE
    why = coordinator_adjudicate.bind_requested(verdict, "disposition", prompt)
    assert why and "LLR-004" in why and "no amendment" in why, why
    assert not Path(ksitting.requested_path(verdict)).exists()


def test_reservation_refuses_a_block_naming_one_row_twice(tmp_path):
    """Implements: TC-398"""
    prompt = "the brief\n{}\n{}\nthe rest\n".format(
        _line("LLR-001"), _line("LLR-001", "sha256:fedcba9876543210")
    )
    with pytest.raises(ValueError, match="LLR-001"):
        ab.bind_pending(tmp_path / "v.md", "amendment", prompt)
    assert not Path(ksitting.requested_path(tmp_path / "v.md")).exists()
