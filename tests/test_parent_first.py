"""A spine row is approved only after the rows it hangs from are, in process.

The rule's one home is a pure function over the four tiers' rows
(`kitlib.spine.parent_first_findings`): one entry per approved child, `Approved`
or `Founded`, citing a declared parent that is not approved, over an SR's
`SN-Refs` to SNs, an LLR's `SR-Refs` to SRs and a TC's `Verifies` to SRs and
LLRs. `parent_first_line` words each entry once. The commit judgement
(`acceptance_record.parent_first_lines`) reads a tree against its parents; its
arms that need a git failure are driven here with the git reads replaced, and
the real-repository cases live in `test_parent_first_git.py` (slow tier), whose
in-process pin this module is. The wiring pins (the lane-commit rider, the
pre-commit step) close the module.

Two evidence classes: new behaviour, each test red at its own assertion before
the rule existed; and a characterization of behaviour already correct, which
names in its docstring the wrong implementation it would catch.
"""

import sys

import pytest
from conftest import KIT, SCRIPTS, load_script

if str(SCRIPTS) not in sys.path:  # the kit's script-sibling import idiom
    sys.path.insert(0, str(SCRIPTS))

import spine_carrier  # noqa: E402
from kitlib import spine  # noqa: E402

ar = load_script("acceptance_record")
tta = load_script("text_then_act")
check = load_script("check")

# --- the shared row and registry builders (the git module imports them) -------

#: Each tier's id column, registry, TOML table and parent-reference key.
TIERS = {
    "SN": ("docs/requirements/stakeholder-needs.toml", "need", None),
    "SR": ("docs/requirements/system-requirements.toml", "requirement", "sn_refs"),
    "LLR": ("docs/requirements/low-level-requirements.toml", "design", "sr_refs"),
    "TC": ("docs/test/test-cases.toml", "test", "verifies"),
}

#: The parent-reference column each tier's rows carry under the readers' names.
REF_COLUMN = {"SR": "SN-Refs", "LLR": "SR-Refs", "TC": "Verifies"}


def tier_of(rid):
    return rid.split("-", 1)[0]


def row(rid, status, *parents):
    """One registry row under the readers' column names; `status` None leaves
    the cell out."""
    tier = tier_of(rid)
    out = {tier + "-ID": rid}
    if status is not None:
        out["Status"] = status
    if tier in REF_COLUMN:
        out[REF_COLUMN[tier]] = ";".join(parents)
    return out


def tiers(*rows):
    """`{label: rows}` over the four tiers, each present (empty when unused)."""
    out = {label: [] for label in TIERS}
    for r in rows:
        out[tier_of(next(iter(r.values())))].append(r)
    return out


def registry_text(*specs):
    """One tier's TOML registry text from `(id, status, *parents)` specs."""
    blocks = []
    for rid, status, *parents in specs:
        _path, table, key = TIERS[tier_of(rid)]
        lines = ["[{}.{}]".format(table, rid)]
        if key:
            lines.append(
                "{} = [{}]".format(key, ", ".join('"%s"' % p for p in parents))
            )
        lines.append('status = "{}"'.format(status))
        blocks.append("\n".join(lines) + "\n")
    return "\n".join(blocks)


def registries(*specs):
    """`{registry path: text}` for the tiers `specs` name, one file per tier."""
    grouped = {}
    for spec in specs:
        grouped.setdefault(tier_of(spec[0]), []).append(spec)
    return {TIERS[t][0]: registry_text(*s) for t, s in grouped.items()}


#: The four parent edges, as (child, parent) id pairs.
PAIRS = {
    "SR-SN": ("SR-001", "SN-001"),
    "LLR-SR": ("LLR-001", "SR-001"),
    "TC-SR": ("TC-001", "SR-001"),
    "TC-LLR": ("TC-001", "LLR-001"),
}


# --- the approval pair ------------------------------------------------------


def test_the_approval_pair_has_one_home():
    assert getattr(spine, "claims_approval", None) is ar._claims_approval


# --- the rule ---------------------------------------------------------------


@pytest.mark.parametrize("pair", sorted(PAIRS), ids=sorted(PAIRS))
def test_an_approved_child_under_an_unapproved_parent_is_found(pair):
    child, parent = PAIRS[pair]
    found = spine.parent_first_findings(
        tiers(row(parent, "Drafted"), row(child, "Approved", parent))
    )
    assert found == [(child, "Approved", parent, "Drafted")]


def test_founded_counts_as_approved_on_either_side():
    founded_child = tiers(row("SR-001", "Drafted"), row("LLR-001", "Founded", "SR-001"))
    assert spine.parent_first_findings(founded_child) == [
        ("LLR-001", "Founded", "SR-001", "Drafted")
    ]
    founded_parent = tiers(
        row("SR-001", "Founded"), row("LLR-001", "Approved", "SR-001")
    )
    assert spine.parent_first_findings(founded_parent) == []


def test_an_entry_names_the_child_the_parent_and_both_statuses():
    line = spine.parent_first_line(("LLR-281", "Approved", "SR-224", "Drafted"))
    assert line == (
        "LLR-281 (Approved) is approved under SR-224 (Drafted), which is not: "
        "approve SR-224 in its own approval act, or return LLR-281 to Drafted"
    )


@pytest.mark.parametrize("status", [None, "Bananas"], ids=["no-status", "unknown"])
def test_a_parent_with_no_status_or_an_unknown_word_is_not_approved(status):
    found = spine.parent_first_findings(
        tiers(row("SR-001", status), row("LLR-001", "Approved", "SR-001"))
    )
    assert [(e[0], e[2]) for e in found] == [("LLR-001", "SR-001")]


def test_only_declared_tier_parents_are_judged():
    """One real violation beside every id the rule must not judge: an IF id, a
    DA id, an id no row declares, a Drafted SN a TC cites (a TC's parents are
    SRs and LLRs only) and the `-000` example rows. Exactly the one real entry,
    so an over-reporting rule fails too."""
    found = spine.parent_first_findings(
        tiers(
            row("SN-001", "Approved"),
            row("SN-002", "Drafted"),
            row("SR-001", "Approved", "SN-001", "DA-001"),
            row("SR-002", "Drafted", "SN-001"),
            row("LLR-001", "Approved", "SR-002"),
            row("TC-001", "Approved", "SR-001", "IF-001", "LLR-999", "SN-002"),
            row("SR-000", "Drafted", "SN-000"),
            row("LLR-000", "Approved", "SR-000"),
            row("TC-000", "Approved", "SR-000", "LLR-000"),
        )
    )
    assert found == [("LLR-001", "Approved", "SR-002", "Drafted")]


def test_the_shipped_templates_example_rows_raise_no_finding():
    """The shipped registry templates yield no entry, so a freshly scaffolded
    project is not red. Adequacy witness: a rule that does not skip the `-000`
    example rows reports the template's `LLR-000` (Approved) under its `SR-000`
    (Drafted)."""
    shipped = {}
    for label, (path, _table, _key) in TIERS.items():
        name = path.rsplit("/", 1)[1].replace(".toml", ".template.toml")
        text = (KIT / "registries" / name).read_text(encoding="utf-8")
        rows = spine_carrier.tier_rows_from_text(text, label + "-ID", ".toml")
        shipped[label] = list(rows.values())
    assert shipped["LLR"], "the shipped LLR template carries its example row"
    assert spine.parent_first_findings(shipped) == []


# --- the commit judgement's failure arms, git reads replaced -----------------

_UNREADABLE = object()
SR_PATH = TIERS["SR"][0]
LLR_PATH = TIERS["LLR"][0]
BROKEN = "[requirement.SR-001\nstatus = \n"


def _fake_git(monkeypatch, trees, diff):
    """Replace the judgement's git reads: `trees` maps a `git show` prefix
    (`":"` the index, `"BASE:"` the parent) to `{path: text}`, a path absent
    from it unlisted and `_UNREADABLE` a listed blob git cannot read; `diff` is
    the changed-name list, or None for a diff git cannot produce."""

    def show(root, prefix, path):
        text = trees.get(prefix, {}).get(path)
        if text is _UNREADABLE:
            raise ar._kitgit.UnreadableBlob(prefix + path)
        return text

    def git(root, args, stdin=None):
        if "diff" not in args:
            return None
        if diff is None:
            return None
        sep = "\0" if "-z" in args else "\n"
        return "".join(name + sep for name in diff)

    def paths(root, args):
        return None if diff is None else list(diff)

    monkeypatch.setattr(ar._kitgit, "git_show", show)
    monkeypatch.setattr(ar._kitgit, "git_paths", paths)
    monkeypatch.setattr(ar._kitgit, "git_out", git)
    monkeypatch.setattr(ar, "_git", git)


@pytest.mark.parametrize(
    "broken, failure",
    [(_UNREADABLE, "cannot be read"), (BROKEN, "does not parse")],
    ids=["unreadable", "unparseable"],
)
def test_a_commit_side_registry_that_cannot_be_read_or_does_not_parse_is_refused_by_name(
    tmp_path, monkeypatch, broken, failure
):
    clean = registries(("SR-001", "Approved"), ("LLR-001", "Approved", "SR-001"))
    index = dict(clean, **{SR_PATH: broken})
    _fake_git(monkeypatch, {"BASE:": clean, ":": index}, [SR_PATH])
    lines = ar.parent_first_lines(tmp_path, ["BASE"])
    assert any(SR_PATH in ln and failure in ln and "index" in ln for ln in lines), lines


def test_a_diff_git_cannot_produce_is_a_refusal_not_a_skip(tmp_path, monkeypatch):
    clean = registries(("SR-001", "Approved"), ("LLR-001", "Approved", "SR-001"))
    _fake_git(monkeypatch, {"BASE:": clean, ":": clean}, None)
    lines = ar.parent_first_lines(tmp_path, ["BASE"])
    assert lines and "cannot" in " ".join(lines), lines


def test_a_parent_side_that_does_not_parse_counts_every_status_as_moved(
    tmp_path, monkeypatch
):
    index = registries(("SR-001", "Drafted"), ("LLR-001", "Approved", "SR-001"))
    base = dict(index, **{SR_PATH: BROKEN})
    _fake_git(monkeypatch, {"BASE:": base, ":": index}, [SR_PATH])
    lines = ar.parent_first_lines(tmp_path, ["BASE"])
    assert len(lines) == 1, lines
    assert "LLR-001" in lines[0] and "SR-001" in lines[0], lines
    # The control: the same standing case over a parent that parses moved
    # neither status, so it is not this judgement's to refuse.
    _fake_git(monkeypatch, {"BASE:": dict(index), ":": index}, [SR_PATH])
    assert ar.parent_first_lines(tmp_path, ["BASE"]) == []


# --- characterizations of the settled rule and judgement --------------------


def test_a_parent_with_no_status_is_rendered_as_no_status():
    """A parent whose `Status` cell is missing reads "no status" in the line,
    never an empty pair of brackets. Adequacy witness: a line that printed the
    raw cell would read `SR-001 ()`."""
    (entry,) = spine.parent_first_findings(
        tiers(row("SR-001", None), row("LLR-001", "Approved", "SR-001"))
    )
    assert spine.parent_first_line(entry) == (
        "LLR-001 (Approved) is approved under SR-001 (no status), which is not: "
        "approve SR-001 in its own approval act, or return LLR-001 to Drafted"
    )


def test_an_unreadable_parent_side_counts_every_status_as_moved(tmp_path, monkeypatch):
    """A base whose registry is listed but cannot be read counts every status
    on the commit side as moved, so a standing pair the commit carries is
    reported. Adequacy witness: a judgement that skipped a base it cannot read
    would find no base against which anything moved, and pass."""
    index = registries(("SR-001", "Drafted"), ("LLR-001", "Approved", "SR-001"))
    base = dict(index, **{SR_PATH: _UNREADABLE})
    _fake_git(monkeypatch, {"BASE:": base, ":": index}, [SR_PATH])
    lines = ar.parent_first_lines(tmp_path, ["BASE"])
    assert len(lines) == 1, lines
    assert "LLR-001 (Approved) is approved under SR-001 (Drafted)" in lines[0], lines


def test_an_example_parent_and_a_boundary_id_raise_no_finding():
    """A child citing a `-000` example row, and a parent column naming a `B-##`
    boundary id, are not judged. Adequacy witness: a rule that kept `-000` rows
    as parents reports LLR-001 under the Drafted SR-000; one that read every
    cited id no approved row declares as unapproved reports SR-001 under B-01."""
    found = spine.parent_first_findings(
        tiers(
            row("SN-001", "Approved"),
            row("SR-000", "Drafted", "SN-000"),
            row("SR-001", "Approved", "SN-001", "B-01"),
            row("LLR-001", "Approved", "SR-000"),
        )
    )
    assert found == []


def test_a_child_with_a_word_outside_the_vocabulary_is_not_approved():
    """Only `Approved` and `Founded` claim approval on the child side too: a
    child reading a word outside the vocabulary raises no finding (its own
    integrity finding names the word). Adequacy witness: a rule that read any
    status but `Drafted` as approved reports LLR-001 under SR-001."""
    found = spine.parent_first_findings(
        tiers(row("SR-001", "Drafted"), row("LLR-001", "Bananas", "SR-001"))
    )
    assert found == []


@pytest.mark.parametrize(
    "toml_status, csv_status, found",
    [("Approved", "Drafted", False), ("Drafted", "Approved", True)],
    ids=["toml-approved", "toml-drafted"],
)
def test_when_both_carriers_of_a_tier_exist_the_first_listed_decides(
    tmp_path, monkeypatch, toml_status, csv_status, found
):
    """`spine_carrier.tier_carriers` lists `.toml` before `.csv`, and a tree
    holding both reads the tier from the first. Adequacy witness: a reader
    that let the last listed carrier win reads SR-001 from the CSV, so each
    case flips."""
    assert spine_carrier.tier_carriers(SR_PATH, "SR-ID")[0] == SR_PATH
    csv = SR_PATH[: -len(".toml")] + ".csv"
    index = registries(("SR-001", toml_status), ("LLR-001", "Approved", "SR-001"))
    index[csv] = "SR-ID,Title,SN-Refs,Status\nSR-001,One,,{}\n".format(csv_status)
    base = registries(("SR-001", toml_status), ("LLR-001", "Drafted", "SR-001"))
    base[csv] = index[csv]
    _fake_git(monkeypatch, {"BASE:": base, ":": index}, [LLR_PATH])
    lines = ar.parent_first_lines(tmp_path, ["BASE"])
    assert bool(lines) is found, lines


def test_approval_is_read_in_any_letter_case():
    """The status vocabulary is matched case-insensitively on both sides: a
    child reading `approved` under a Drafted parent is found, and a child under
    a parent reading `FOUNDED` is not. Adequacy witness: a case-sensitive
    comparison misses the lower-case child and reports the child under the
    upper-case parent."""
    found = spine.parent_first_findings(
        tiers(row("SR-001", "Drafted"), row("LLR-001", "approved", "SR-001"))
    )
    assert found == [("LLR-001", "approved", "SR-001", "Drafted")]
    founded = tiers(row("SR-001", "FOUNDED"), row("LLR-001", "Approved", "SR-001"))
    assert spine.parent_first_findings(founded) == []


def test_a_tier_absent_on_the_commit_side_supplies_no_rows(tmp_path, monkeypatch):
    """The commit deletes the SR registry while the LLR registry keeps an
    approved child citing SR-001, which the parent tree held Drafted. The
    absent tier supplies no rows and no refusal (an undeclared parent is the
    orphan rules'), and the parent tree's rows are not read in its place.
    Adequacy witness: a judgement that read a missing commit-side tier from the
    parent tree finds LLR-001 under the Drafted SR-001 and refuses."""
    base = registries(("SR-001", "Drafted"), ("LLR-001", "Drafted", "SR-001"))
    index = registries(("LLR-001", "Approved", "SR-001"))
    _fake_git(monkeypatch, {"BASE:": base, ":": index}, [SR_PATH, LLR_PATH])
    assert ar.parent_first_lines(tmp_path, ["BASE"]) == []


# --- the wiring -------------------------------------------------------------


def test_the_rule_rides_the_lane_commit_walk():
    names = [rider.__name__ for rider in tta.LANE_COMMIT_RIDERS]
    assert "commit_parent_first_lines" in names, names


def test_the_pre_commit_hook_runs_the_parent_first_step():
    hook = (KIT / "hooks" / "pre-commit").read_text(encoding="utf-8")
    (batched,) = [
        ln for ln in hook.splitlines() if "--run-steps" in ln and not ln.startswith("#")
    ]
    steps = batched.split("--run-steps", 1)[1].split()[0].split(",")
    assert "parent-first" in steps, steps
    assert "parent-first" in check.BUILTIN_STEP_NAMES
    assert "parent-first" not in check._TRUNK_FRESHNESS_STEPS
