"""WI registry <-> spec-file converter (concurrency-restructure §2).

`wi_convert.py` is the mechanical half of "specs are the registry": one Markdown
spec file per `work-items.csv` row, status encoded as the file's DIRECTORY, the
row's columns as TOML frontmatter, and the long `Deliverable` cell as the body.
The design's own precondition is that *the converter is proven by a round-trip
before the CSV is demoted* (the 140-cell lesson), so this module runs that proof
against the REAL registry rather than a fixture — the file the next phase would
actually convert.

That proof is **representation-conditional** (Phase 2c-i): it follows whichever
home the repo actually carries — the CSV while the CSV is authoritative, the
spec folder once it is — because a proof pinned to the home it was written
against is a proof the flip commit has to rewrite. The branch this repo does not
take yet is not left as dead code: it is driven against a materialized fixture,
and mutation-proven, in the same file.

Every guard here is mutation-proven, per the repo's standing rule that a guard
you have not seen fail is not a guard (WI-293):

  * the cell-exact comparison is run over a DELIBERATELY corrupted spec and must
    report the corruption — otherwise "cell-exact: yes" means nothing;
  * the status classifier is fed a status it does not know and must REFUSE,
    because the failure mode that matters is a catch-all bucket silently
    reclassifying work (the `intra-module` census lesson, one layer over);
  * the escaping is exercised with the characters that break escapers —
    double quotes, backslashes, markdown headings, blank lines — not with the
    tame values the real registry happens to contain.

These run in-process (`conftest.load_script`), so a failure points at a line of
the converter rather than at a subprocess's exit code.
"""

import csv
import re

import pytest
from conftest import ROOT, load_script

# Phase 2c-i moved the converter from tools/ into the kit, so it loads like every
# other kit script — the bespoke tools/ importer this module used to carry is
# gone rather than kept working "just in case".
wi_convert = load_script("wi_convert")

REGISTRY = ROOT / "docs" / "requirements" / "work-items.csv"
WORK = ROOT / "docs" / "work"


@pytest.fixture(scope="module")
def live_csv(tmp_path_factory):
    """The live registry AS a CSV file, whichever home the repo carries: the
    real CSV while it exists, else a CSV rebuilt from docs/work/ (the home
    since the Phase 2c flip). The format tests below want realistic data, not
    an opinion about the home — this keeps their realism across the flip."""
    if REGISTRY.exists():
        return REGISTRY
    assert WORK.is_dir(), "the registry has no home at all"
    out = tmp_path_factory.mktemp("live-registry") / "work-items.csv"
    try:
        wi_convert.to_csv(WORK, out)
    except wi_convert.ConvertError as exc:
        # An in-flight active/<branch>/ claim: conversion is a drained-stop
        # operation (§3.2), so the realistic-data fixture is only definable at
        # a drained registry. The refusal itself is pinned by its own test.
        pytest.skip("live registry has in-flight claims: {}".format(exc))
    return out


def _registry_rows(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path, rows):
    """A fixture registry, written LF whatever the platform — a fixture that
    uses the platform default cannot test the platform (WI-337)."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        writer = csv.writer(handle, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        writer.writerow(wi_convert.COLUMNS)
        for row in rows:
            writer.writerow([row.get(column) or "" for column in wi_convert.COLUMNS])


def _row(wi_id, **kw):
    row = {column: "" for column in wi_convert.COLUMNS}
    row["WI-ID"] = wi_id
    row["Title"] = kw.pop("Title", wi_id)
    row["Status"] = kw.pop("Status", "queued")
    row.update(kw)
    return row


def _cell_mismatches(before, after):
    """Every differing cell between two row lists — the comparison `--verify`
    makes, exposed so the mutation proofs can drive it directly."""
    findings = []
    if len(before) != len(after):
        findings.append("row count {} != {}".format(len(before), len(after)))
    for lhs, rhs in zip(before, after):
        for column in wi_convert.COLUMNS:
            if (lhs.get(column) or "") != (rhs.get(column) or ""):
                findings.append("{} {}".format(lhs.get("WI-ID"), column))
    return findings


def _round_trip(tmp_path, rows):
    """rows -> CSV -> specs -> CSV -> rows, all under `tmp_path`."""
    source = tmp_path / "in.csv"
    _write_csv(source, rows)
    wi_convert.to_specs(source, tmp_path / "work")
    wi_convert.to_csv(tmp_path / "work", tmp_path / "out.csv")
    return wi_convert.load_csv(tmp_path / "out.csv")


# --- the proof that matters: the real registry --------------------------------
# The registry has TWO possible homes during the migration, and the round-trip
# proof follows whichever one is authoritative rather than pinning the CSV — a
# test that hard-codes the home it was written against is a test that has to be
# rewritten by the very commit whose safety it exists to establish. Both branches
# are LIVE: the folder direction is driven below against a materialized fixture,
# so the branch this repo does not take yet still ships exercised.


def _specs_by_id(work_dir):
    """`{WI-ID: row}` for every spec under `work_dir`."""
    return {row["WI-ID"]: row for row, _order, _rel in wi_convert.read_specs(work_dir)}


def _spec_row_diff(before, after):
    """Every differing cell between two `{id: row}` maps — the folder branch's
    comparison, exposed like `_cell_mismatches` so its mutation proof can drive
    it directly instead of trusting a green."""
    findings = []
    if set(before) != set(after):
        findings.append(
            "id set: lost {} / gained {}".format(
                sorted(set(before) - set(after)), sorted(set(after) - set(before))
            )
        )
    for wi_id, row in sorted(before.items()):
        other = after.get(wi_id) or {}
        findings.extend(
            "{} {}".format(wi_id, column)
            for column in wi_convert.COLUMNS
            if (row.get(column) or "") != (other.get(column) or "")
        )
    return findings


def _folder_home_round_trip(work_dir, scratch):
    """`(row_count, findings, rebuilt_dir)` for folder -> CSV -> folder.

    Compared by PARSE, not by bytes, and that is the honest instrument in this
    direction: a HAND-FILED spec carries no `order` key (the converter mints one
    on the way back) and its filename slug is cosmetic, so byte-equality would
    be a stricter claim than "the same registry" and would red on a difference
    that is not a loss. Parse-equality over all 17 columns of every spec is
    exactly the claim being made.
    """
    rebuilt_csv = scratch / "rebuilt.csv"
    before = _specs_by_id(work_dir)
    count = wi_convert.to_csv(work_dir, rebuilt_csv)
    rebuilt_dir = scratch / "work"
    wi_convert.to_specs(rebuilt_csv, rebuilt_dir)
    return count, _spec_row_diff(before, _specs_by_id(rebuilt_dir)), rebuilt_dir


def test_the_live_registry_round_trips_in_whichever_home_is_authoritative(
    tmp_path, capsys
):
    """The round-trip proof over the registry this repo actually carries.

    CSV home: `--verify` cell-exact AND byte-identical (the source file is the
    converter's own output shape, so the bytes are assertable here even though
    `verify` only ever REPORTS them in general). Folder home: the same claim in
    the direction that home can make it — folder -> CSV -> folder, parse-equal.
    """
    if REGISTRY.exists():
        assert wi_convert.verify(REGISTRY) is True
        summary = capsys.readouterr().out
        assert "cell-exact: yes" in summary, summary
        assert "byte-identical: yes" in summary, summary
        return

    assert WORK.is_dir(), (
        "neither docs/requirements/work-items.csv nor docs/work/ exists — the "
        "registry has no home at all, which is not a state this repo may be in"
    )
    try:
        count, findings, _rebuilt = _folder_home_round_trip(WORK, tmp_path)
    except wi_convert.ConvertError as exc:
        # With a claim in flight the round-trip proof is not definable - and
        # the converter must say so BY NAME rather than coerce or crash. That
        # refusal is this test's claim in the undrained state.
        assert "drained-stop" in str(exc), exc
        assert "active/" in str(exc), exc
        return
    assert count > 300, "the spec folder looks truncated: {} specs".format(count)
    assert findings == [], findings


def test_the_folder_home_round_trip_is_proven_against_a_materialized_registry(
    tmp_path,
):
    """The branch above that this repo does not take yet, driven for real.

    Home-independent by construction (it materializes its own folder), so the
    folder direction is not dead code waiting for the flip to discover it. The
    fixture deliberately carries the shapes that make folder -> CSV harder than
    CSV -> folder: a spec in every status directory — both TERMINALS included,
    which since WI-384 is the whole of how they are told apart — a multi-line
    Deliverable, the `~` soft prefix, and a HAND-FILED spec with no `order` key,
    which only ever exists in this direction.
    """
    rows = [
        _row("WI-001", Title="root", Status="done", Deliverable="shipped\n\nit\n"),
        _row(
            "WI-002",
            Title='a "quoted" one',
            Status="queued",
            **{"Predecessors": "WI-001;~WI-004", "SR-Refs": "SR-001;SR-002"},
        ),
        _row("WI-003", Title="parked", Status="deferred", Priority="2"),
        _row(
            "WI-004",
            Title="won't build",
            Status="cancelled",
            Deliverable="superseded",
        ),
        _row("WI-005", Title="still thinking", Status="draft"),
    ]
    source = tmp_path / "in.csv"
    _write_csv(source, rows)
    work = tmp_path / "work"
    wi_convert.to_specs(source, work)

    # The hand-filed spec: no `order`, and a slug the converter would not choose.
    (work / "queued" / "WI-009-filed-by-hand.md").write_text(
        '+++\nid = "WI-009"\ntitle = "filed by hand after the flip"\n'
        'needs = ["WI-002"]\n+++\n',
        encoding="utf-8",
        newline="\n",
    )

    count, findings, _rebuilt = _folder_home_round_trip(work, tmp_path / "scratch")
    assert count == 6, count
    assert findings == [], findings
    # The premise the hand-filed spec exists for: it really does lack `order`,
    # so the comparison above tolerated a difference that is not a loss.
    hand = next(
        order
        for row, order, _rel in wi_convert.read_specs(work)
        if row["WI-ID"] == "WI-009"
    )
    assert hand is None, hand


def test_an_in_flight_claim_refuses_conversion_by_name(tmp_path):
    """An active/<branch>/ spec (the Phase 4 claim) is not convertible content:
    conversion is a drained-stop operation (§3.2), and the converter says so by
    name instead of coercing the claim or crashing on the branch directory."""
    work = tmp_path / "work"
    row = {c: "" for c in wi_convert.COLUMNS}
    row.update({"WI-ID": "WI-9", "Title": "claimed work", "Status": "queued"})
    wi_convert.write_spec_file(work, row)
    (work / "active" / "wi-9").mkdir(parents=True)
    (work / "queued" / "WI-9-claimed-work.md").rename(
        work / "active" / "wi-9" / "WI-9-claimed-work.md"
    )
    with pytest.raises(wi_convert.ConvertError) as err:
        wi_convert.to_csv(work, tmp_path / "out.csv")
    assert "drained-stop" in str(err.value)
    assert "active/wi-9" in str(err.value)


def test_mutation_a_corrupted_rebuilt_spec_reds_the_folder_home_round_trip(tmp_path):
    """The folder branch's own failure shape, driven — otherwise its green is an
    unfalsified claim (WI-293). Two defects, one dropped and one retyped, both
    edited into the REBUILT tree after a clean round-trip proved the comparison
    is capable of reporting no findings at all."""
    rows = [
        _row("WI-001", Status="queued", Workstream="scripts"),
        _row("WI-002", Status="done", Deliverable="shipped"),
    ]
    source = tmp_path / "in.csv"
    _write_csv(source, rows)
    work = tmp_path / "work"
    wi_convert.to_specs(source, work)

    count, findings, rebuilt = _folder_home_round_trip(work, tmp_path / "scratch")
    assert (count, findings) == (2, []), (count, findings)

    before = _specs_by_id(work)
    victim = next(rebuilt.rglob("WI-001-*.md"))
    text = victim.read_text(encoding="utf-8")
    assert 'workstream = "scripts"' in text, text
    victim.write_text(
        text.replace('workstream = "scripts"', 'workstream = "docs"'),
        encoding="utf-8",
        newline="\n",
    )
    next(rebuilt.rglob("WI-002-*.md")).unlink()

    # Spelled out rather than summarized: a dropped spec reds BOTH the id-set
    # line and every cell it carried, which is the report you want when the
    # failure is real, and is only visible if the guard asserts it.
    assert _spec_row_diff(before, _specs_by_id(rebuilt)) == [
        "id set: lost ['WI-002'] / gained []",
        "WI-001 Workstream",
        "WI-002 WI-ID",
        "WI-002 Title",
        "WI-002 Status",
        "WI-002 Deliverable",
    ]


def test_the_real_registry_produces_one_spec_per_row(tmp_path, live_csv):
    """Row count is READ from the CSV, not asserted from memory — and the file
    is expected to be substantial, so a truncated registry cannot pass by
    round-tripping three rows perfectly."""
    expected = len(_registry_rows(live_csv))
    assert expected > 300, "the registry looks truncated: {} rows".format(expected)
    written = wi_convert.to_specs(live_csv, tmp_path / "work")
    assert len(written) == expected
    assert len(set(written)) == expected, "two rows produced the same spec path"
    rebuilt = wi_convert.to_csv(tmp_path / "work", tmp_path / "out.csv")
    assert rebuilt == expected


def test_status_becomes_the_directory_and_cancellation_stays_visible(
    tmp_path, live_csv
):
    """Location IS the state (§2.1), and since WI-384 location is the WHOLE of
    it: `cancelled/` is its own directory, so a cancellation is visible from the
    path and no frontmatter key carries — or could contradict — the state."""
    rows = _registry_rows(live_csv)
    written = wi_convert.to_specs(live_csv, tmp_path / "work")
    by_id = {row["WI-ID"]: row for row in rows}
    for relpath in written:
        wi_id = relpath.rsplit("/", 1)[1].split("-", 2)
        wi_id = "-".join(wi_id[:2])
        directory = relpath.split("/", 1)[0]
        assert directory == wi_convert.STATUS_DIRS[by_id[wi_id]["Status"]]
    cancelled = [r["WI-ID"] for r in rows if r["Status"] == "cancelled"]
    assert cancelled, "the registry has no cancelled rows — this guard is vacuous"
    for wi_id in cancelled:
        path = next(
            p
            for p in (tmp_path / "work" / "cancelled").iterdir()
            if p.name.startswith(wi_id)
        )
        # The deleted attribute stays deleted: the folder is the statement.
        # Two narrowings, each doing distinct work, because a whole-file
        # substring read convicts SEVEN of the sixteen cancelled rows (measured
        # 2026-08-01: WI-061, -063, -108, -158, -187, -271, -356) and none of
        # them carries the key — a repo whose own record discusses a retired
        # concept must be allowed to say its name.
        #   * The FRONTMATTER split gives the guard its subject. "The deleted
        #     ATTRIBUTE stays deleted" is a claim about schema, and six of the
        #     seven carry the word only in the Deliverable BODY, where it is
        #     plainly prose.
        #   * The KEY-ASSIGNMENT match separates prose from schema inside the
        #     frontmatter, which the split cannot: WI-356's `title` quotes a
        #     stale "By disposition" census line, so the split alone still reds
        #     it. (The key match alone, over the whole file, reds nothing today
        #     — but its subject would be unbounded, convicting a body that
        #     quoted the old schema at line start.)
        # Found on WI-386's composed tree, the first DRAINED registry this test
        # could run against at all: `live_csv` skips while any claim is in
        # flight, and both parents of that merge had one.
        head = path.read_text(encoding="utf-8").split("+++", 2)[1]
        assert not re.search(r"(?m)^\s*disposition\s*=", head)


def test_emitted_specs_are_lf_on_every_platform(tmp_path, live_csv):
    """The generated-artifact rule (WI-348): no CR bytes, whatever the OS."""
    wi_convert.to_specs(live_csv, tmp_path / "work")
    offenders = [
        p.name for p in (tmp_path / "work").rglob("*.md") if b"\r" in p.read_bytes()
    ]
    assert not offenders, offenders
    wi_convert.to_csv(tmp_path / "work", tmp_path / "out.csv")
    assert b"\r" not in (tmp_path / "out.csv").read_bytes()


# --- mutation proofs ----------------------------------------------------------


def test_an_unknown_status_is_refused_by_name(tmp_path):
    """(a) The classifier must REFUSE rather than invent a bucket, and the
    refusal must name the row — a converter that files an unknown status under
    `queued/` has silently reclassified somebody's work."""
    rows = [_row("WI-001", Status="queued"), _row("WI-002", Status="in-flight")]
    source = tmp_path / "in.csv"
    _write_csv(source, rows)
    with pytest.raises(wi_convert.ConvertError) as exc:
        wi_convert.to_specs(source, tmp_path / "work")
    message = str(exc.value)
    assert "WI-002" in message and "in-flight" in message, message
    # And the honest other half: the statuses it DOES know are not refused.
    for status in ("draft", "queued", "deferred", "done", "cancelled"):
        wi_convert.status_dir(_row("WI-009", Status=status))


def test_corrupting_one_emitted_frontmatter_value_reds_the_comparison(tmp_path):
    """(b) The cell-exact check, driven over a spec whose frontmatter was edited
    after emission. Without this, "cell-exact: yes" is an unfalsified claim."""
    rows = [
        _row("WI-001", Title="first", Status="queued", Workstream="scripts"),
        _row("WI-002", Title="second", Status="done", Deliverable="shipped it"),
    ]
    source = tmp_path / "in.csv"
    _write_csv(source, rows)
    wi_convert.to_specs(source, tmp_path / "work")

    # Clean first: the comparison must be capable of reporting "no findings",
    # or the mutation below proves nothing.
    wi_convert.to_csv(tmp_path / "work", tmp_path / "clean.csv")
    assert _cell_mismatches(rows, wi_convert.load_csv(tmp_path / "clean.csv")) == []

    victim = next((tmp_path / "work").rglob("WI-001-*.md"))
    text = victim.read_text(encoding="utf-8")
    assert 'workstream = "scripts"' in text
    victim.write_text(
        text.replace('workstream = "scripts"', 'workstream = "docs"'),
        encoding="utf-8",
        newline="\n",
    )
    wi_convert.to_csv(tmp_path / "work", tmp_path / "dirty.csv")
    findings = _cell_mismatches(rows, wi_convert.load_csv(tmp_path / "dirty.csv"))
    assert findings == ["WI-001 Workstream"], findings


def test_quotes_backslashes_and_semicolon_refs_round_trip_exactly(tmp_path):
    """(c) The characters that break a hand-rolled escaper, plus the multi-ref
    cells — including the `~` SOFT-dependency prefix, which is meaning and must
    survive verbatim."""
    nasty = 'a "quoted" title with a \\ backslash and a \\" pair'
    rows = [
        _row(
            "WI-001",
            Title=nasty,
            Status="queued",
            **{
                "SR-Refs": "SR-001;SR-002;SR-003",
                "Predecessors": "WI-000;~WI-999;~WI-042",
            },
        )
    ]
    back = _round_trip(tmp_path, rows)
    assert _cell_mismatches(rows, back) == []
    assert back[0]["Title"] == nasty
    assert back[0]["Predecessors"] == "WI-000;~WI-999;~WI-042"

    spec = next((tmp_path / "work").rglob("*.md")).read_text(encoding="utf-8")
    assert 'needs = ["WI-000", "~WI-999", "~WI-042"]' in spec, spec


def test_a_markdown_deliverable_round_trips_exactly(tmp_path):
    """(d) Headings, quotes and blank lines in the body — the reason the
    Deliverable lives in the body and never passes through the escaper."""
    deliverable = (
        "## A heading inside the cell\n"
        "\n"
        'Then a "quoted" line, a `backtick`, and a backslash \\ for good measure.\n'
        "\n"
        "- a bullet\n"
        "- another; with a semicolon\n"
        "\n"
        "+++ a line that looks like a frontmatter fence\n"
    )
    rows = [_row("WI-001", Status="done", Deliverable=deliverable)]
    back = _round_trip(tmp_path, rows)
    assert back[0]["Deliverable"] == deliverable
    assert _cell_mismatches(rows, back) == []


def test_an_empty_deliverable_and_an_empty_optional_cell_round_trip(tmp_path):
    """Absent and empty mean the same thing in this registry; the emitter omits
    empty keys, so the reader must reconstruct them as empty strings."""
    rows = [_row("WI-001", Status="queued", Deliverable="")]
    back = _round_trip(tmp_path, rows)
    assert _cell_mismatches(rows, back) == []
    spec = next((tmp_path / "work").rglob("*.md")).read_text(encoding="utf-8")
    assert "## Deliverable" not in spec
    assert "workstream" not in spec


def test_the_bar_cell_round_trips_and_a_context_body_is_read_past(tmp_path):
    """WI-388: the `Bar` column (bar declares verification strictness for this
    row's lane; it never affects scheduling) crosses the round trip like any
    scalar, and the advisory `## Context` body section a minted spec carries is
    read PAST exactly like `## Handback` — `--to-csv` on a minted folder must
    not refuse, and the section maps to no CSV column."""
    rows = [_row("WI-001", Status="queued", Bar="DevBar-Tests")]
    back = _round_trip(tmp_path, rows)
    assert back[0]["Bar"] == "DevBar-Tests"
    assert _cell_mismatches(rows, back) == []
    # A minted, context-only body parses with an empty Deliverable...
    assert wi_convert.parse_deliverable("\n## Context\n\n- advisory joins\n", "w") == ""
    # ...and a closed row's Deliverable survives with the Context clipped off.
    body = "\n## Deliverable\n\nshipped\n\n## Context\n\n- joins, kept\n"
    assert wi_convert.parse_deliverable(body, "w") == "shipped"


def test_row_order_survives_a_registry_that_is_not_id_sorted(tmp_path, live_csv):
    """The live registry is NOT id-sorted, which is why `order` is carried
    explicitly. Reconstructing by id would silently reorder an authoritative
    file, so the guard uses a deliberately out-of-order fixture."""
    rows = [_row("WI-070"), _row("WI-066"), _row("WI-201"), _row("WI-191")]
    back = _round_trip(tmp_path, rows)
    assert [r["WI-ID"] for r in back] == ["WI-070", "WI-066", "WI-201", "WI-191"]
    # And the premise: the REAL registry is out of id order, so this matters.
    # (Post-flip the `order` frontmatter keys carry that original order into
    # the rebuilt CSV, so the premise stays checkable in either home.)
    ids = [wi_convert._id_number(r["WI-ID"]) for r in _registry_rows(live_csv)]
    assert ids != sorted(ids), "the registry is id-sorted now — re-derive `order`"


def test_priority_is_an_int_only_when_that_is_reversible(tmp_path):
    """`1` becomes a TOML integer; `01` stays a string, because `str(int("01"))`
    is not `"01"` and a converter may not quietly normalize a cell."""
    rows = [_row("WI-001", Priority="1"), _row("WI-002", Priority="01")]
    back = _round_trip(tmp_path, rows)
    assert _cell_mismatches(rows, back) == []
    specs = {
        p.name: p.read_text(encoding="utf-8") for p in (tmp_path / "work").rglob("*.md")
    }
    assert any(
        "priority = 1\n" in t for n, t in specs.items() if n.startswith("WI-001")
    )
    assert any(
        'priority = "01"' in t for n, t in specs.items() if n.startswith("WI-002")
    )


def test_a_byte_difference_is_reported_with_its_reason_not_asserted(tmp_path):
    """`--verify` reports byte identity and, when it fails, WHY.

    On the live registry the bytes happen to match, so that reporting path
    would otherwise ship unexercised — and a diagnosis nobody has ever seen
    produced is not a diagnosis. Driven here over a CSV whose only difference
    from the writer's output is quoting style, which is exactly the benign case
    the report exists to distinguish from a lost cell.
    """
    rows = [_row("WI-001", Status="queued", Workstream="scripts")]
    over_quoted = tmp_path / "quoted.csv"
    with over_quoted.open("w", encoding="utf-8", newline="\n") as handle:
        writer = csv.writer(handle, quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writerow(wi_convert.COLUMNS)
        for row in rows:
            writer.writerow([row.get(column) or "" for column in wi_convert.COLUMNS])

    lines = []
    assert wi_convert.verify(over_quoted, emit=lines.append) is True
    summary = "\n".join(lines)
    assert "cell-exact: yes" in summary, summary
    assert "byte-identical: no" in summary, summary
    assert "quoting style" in summary, summary

    # And the reason function itself, on the two other differences it names.
    assert "BOM differs" in wi_convert._byte_reason(b"\xef\xbb\xbfa\n", b"a\n")
    assert "line endings differ" in wi_convert._byte_reason(b"a\r\nb\r\n", b"a\nb\n")


# --- refusals -----------------------------------------------------------------


def test_to_specs_refuses_a_non_empty_work_dir_without_force(tmp_path):
    """Double-materialization is how you get two files for one work item and no
    way to tell git which one to believe."""
    source = tmp_path / "in.csv"
    _write_csv(source, [_row("WI-001", Status="queued")])
    work = tmp_path / "work"
    wi_convert.to_specs(source, work)
    assert list(work.rglob("*.md"))

    with pytest.raises(wi_convert.ConvertError) as exc:
        wi_convert.to_specs(source, work)
    assert "not empty" in str(exc.value)

    # --force is the documented escape, and it must actually work.
    assert wi_convert.to_specs(source, work, force=True) == ["queued/WI-001-wi-001.md"]


def test_a_wrong_header_is_refused(tmp_path):
    """A converter that guesses at an unknown column set is how a column gets
    dropped."""
    source = tmp_path / "in.csv"
    with source.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("WI-ID,Title,Status\nWI-001,t,queued\n")
    with pytest.raises(wi_convert.ConvertError) as exc:
        wi_convert.load_csv(source)
    assert "header is not the declared work-item schema" in str(exc.value)


def test_a_spec_in_an_unknown_directory_is_refused(tmp_path):
    """The inverse classifier refuses a directory it has never heard of, by
    name — never a catch-all bucket. (`active/<branch>/` is no longer unknown:
    it is the §2.3 in-flight claim, refused separately as a drained-stop
    operation — see test_an_in_flight_claim_refuses_conversion_by_name.)"""
    source = tmp_path / "in.csv"
    _write_csv(source, [_row("WI-001", Status="queued")])
    wi_convert.to_specs(source, tmp_path / "work")
    spec = next((tmp_path / "work").rglob("*.md"))
    moved = tmp_path / "work" / "parked" / spec.name
    moved.parent.mkdir(parents=True)
    spec.rename(moved)
    with pytest.raises(wi_convert.ConvertError) as exc:
        wi_convert.to_csv(tmp_path / "work", tmp_path / "out.csv")
    assert "not a status" in str(exc.value)
    assert "parked" in str(exc.value)


def test_columns_are_pinned_to_the_shipped_registry_header():
    """`wi_convert.COLUMNS` is a fourth hand-maintained copy of the 17-column
    schema (beside the shipped template, `plan_artifacts.WI_HEADER`, and
    test_plan_artifacts's fixture line). It is sanctioned F5 duplication (the
    rule's live home is `tests/test_rule_sync.py`, since D-7/WI-426 deleted the
    census that used to record it), and the WI-291 precedent is that the
    duplication is fine while the DRIFT is guarded — so it is guarded here,
    against the same one truth the other three are pinned to."""
    template = ROOT / "project-trajectory" / "registries" / "work-items.template.csv"
    with template.open(encoding="utf-8-sig", newline="") as handle:
        assert next(csv.reader(handle)) == wi_convert.COLUMNS
    # (The live-CSV half of this pin retired with the CSV at the Phase 2c flip;
    # the template is the schema of record for the legacy format.)


def test_the_toml_emitter_escapes_what_tomllib_must_read_back():
    """Direct unit cover for the hand-rolled serializer, including a control
    character no registry cell contains today — the escaper must be correct for
    the input it MIGHT get, not only for the input it has."""
    import tomllib

    for value in (
        'a "b"',
        "back\\slash",
        "tab\there",
        "line\nbreak",
        "bell\x07",
        "§ é →",
    ):
        text = "k = " + wi_convert.toml_string(value) + "\n"
        assert tomllib.loads(text)["k"] == value, text
