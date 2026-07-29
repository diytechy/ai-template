"""WI registry <-> spec-file converter (concurrency-restructure §2, Phase 2a).

`wi_convert.py` is the mechanical half of "specs are the registry": one Markdown
spec file per `work-items.csv` row, status encoded as the file's DIRECTORY, the
row's columns as TOML frontmatter, and the long `Deliverable` cell as the body.
The design's own precondition is that *the converter is proven by a round-trip
before the CSV is demoted* (the 140-cell lesson), so this module runs that proof
against the REAL registry rather than a fixture — the file the next phase would
actually convert.

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

import importlib.util

import pytest
from conftest import ROOT


def _load_tool(name):
    # wi_convert lives in tools/ (meta-repo tooling), not the kit's scripts/:
    # it ships at Phase 2c with the spine amendment, so conftest.load_script
    # (pinned to scripts/) deliberately cannot see it.
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


wi_convert = _load_tool("wi_convert")

REGISTRY = ROOT / "docs" / "requirements" / "work-items.csv"


def _registry_rows():
    with REGISTRY.open(newline="", encoding="utf-8-sig") as handle:
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


def test_the_real_registry_round_trips_cell_exact(capsys):
    """`--verify` over `docs/requirements/work-items.csv` itself."""
    assert wi_convert.verify(REGISTRY) is True
    summary = capsys.readouterr().out
    assert "cell-exact: yes" in summary, summary


def test_the_real_registry_produces_one_spec_per_row(tmp_path):
    """Row count is READ from the CSV, not asserted from memory — and the file
    is expected to be substantial, so a truncated registry cannot pass by
    round-tripping three rows perfectly."""
    expected = len(_registry_rows())
    assert expected > 300, "the registry looks truncated: {} rows".format(expected)
    written = wi_convert.to_specs(REGISTRY, tmp_path / "work")
    assert len(written) == expected
    assert len(set(written)) == expected, "two rows produced the same spec path"
    rebuilt = wi_convert.to_csv(tmp_path / "work", tmp_path / "out.csv")
    assert rebuilt == expected


def test_status_becomes_the_directory_and_retirement_stays_visible(tmp_path):
    """Location IS the state (§2.1); `retired` shares `archive/` with `done` and
    is told apart by `disposition`, so retirement is never a deletion."""
    rows = _registry_rows()
    written = wi_convert.to_specs(REGISTRY, tmp_path / "work")
    by_id = {row["WI-ID"]: row for row in rows}
    for relpath in written:
        wi_id = relpath.rsplit("/", 1)[1].split("-", 2)
        wi_id = "-".join(wi_id[:2])
        directory = relpath.split("/", 1)[0]
        assert directory == wi_convert.STATUS_DIRS[by_id[wi_id]["Status"]]
    retired = [r["WI-ID"] for r in rows if r["Status"] == "retired"]
    assert retired, "the registry has no retired rows — this guard has gone vacuous"
    for wi_id in retired:
        path = next(
            p
            for p in (tmp_path / "work" / "archive").iterdir()
            if p.name.startswith(wi_id)
        )
        assert 'disposition = "retired"' in path.read_text(encoding="utf-8")


def test_emitted_specs_are_lf_on_every_platform(tmp_path):
    """The generated-artifact rule (WI-348): no CR bytes, whatever the OS."""
    wi_convert.to_specs(REGISTRY, tmp_path / "work")
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
    for status in ("done", "retired", "queued", "deferred"):
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


def test_row_order_survives_a_registry_that_is_not_id_sorted(tmp_path):
    """The live registry is NOT id-sorted, which is why `order` is carried
    explicitly. Reconstructing by id would silently reorder an authoritative
    file, so the guard uses a deliberately out-of-order fixture."""
    rows = [_row("WI-070"), _row("WI-066"), _row("WI-201"), _row("WI-191")]
    back = _round_trip(tmp_path, rows)
    assert [r["WI-ID"] for r in back] == ["WI-070", "WI-066", "WI-201", "WI-191"]
    # And the premise: the REAL registry is out of id order, so this matters.
    ids = [wi_convert._id_number(r["WI-ID"]) for r in _registry_rows()]
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
    """The inverse classifier refuses too — `active/<branch>/` is a §2.3 state
    this converter does not yet own, and it says so rather than guessing."""
    source = tmp_path / "in.csv"
    _write_csv(source, [_row("WI-001", Status="queued")])
    wi_convert.to_specs(source, tmp_path / "work")
    spec = next((tmp_path / "work").rglob("*.md"))
    moved = tmp_path / "work" / "active" / spec.name
    moved.parent.mkdir(parents=True)
    spec.rename(moved)
    with pytest.raises(wi_convert.ConvertError) as exc:
        wi_convert.to_csv(tmp_path / "work", tmp_path / "out.csv")
    assert "not a status" in str(exc.value)


def test_columns_are_pinned_to_the_shipped_registry_header():
    """`wi_convert.COLUMNS` is a fourth hand-maintained copy of the 17-column
    schema (beside the shipped template, `plan_artifacts.WI_HEADER`, and
    test_plan_artifacts's fixture line). It is sanctioned as F5 duplication in
    `docs/dupes-allow` under `wi-registry`, and the WI-291 precedent is that the
    duplication is fine while the DRIFT is guarded — so it is guarded here,
    against the same one truth the other three are pinned to."""
    template = ROOT / "project-trajectory" / "registries" / "work-items.template.csv"
    with template.open(encoding="utf-8-sig", newline="") as handle:
        assert next(csv.reader(handle)) == wi_convert.COLUMNS
    with REGISTRY.open(encoding="utf-8-sig", newline="") as handle:
        assert next(csv.reader(handle)) == wi_convert.COLUMNS


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
