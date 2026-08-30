"""OI-67 slice 6: a registry CSV may open with a `#` declaration header — the
`Contracts:` marker and `Contract IF-###:` bodies a CSV owner states — and ONE
reader (`kitlib.spine.csv_body` / `csv_reader` / `csv_rows`) strips it before
the header row for every kit consumer, so `performance-budgets.csv` can declare
its seam without any loader losing `PB-ID`.
"""

from pathlib import Path

from conftest import (
    ROOT,
    load_script,
    make_minimal_project,
    record_ids,
    run_py,
    use_legacy_spine_carrier,
)

CARRIER = load_script(
    "spine_carrier"
)  # puts scripts/ on sys.path for the package import

from kitlib import spine as KIT  # noqa: E402

HEADER = (
    "# a registry CSV — the OI-67 declaration header\n"
    "#\n"
    "# Contracts: IF-031\n"
    "# Contract IF-031: the budgets registry.\n"
)
PB_HEADER = "PB-ID,Metric,Refs,Budget,Unit,Tolerance,Direction,Tier,Gate,Owner,Notes\n"
PB_ROW = "PB-001,Metric,SR-001,5,s,50%,lower-better,Full,warn,Integration,note\n"


def test_csv_body_strips_only_the_leading_comment_block():
    body = KIT.csv_body("﻿" + HEADER + PB_HEADER + PB_ROW)
    assert body == PB_HEADER + PB_ROW  # the BOM goes with the header
    # A `#` opening a DATA line, or inside a quoted cell, is data and stays.
    data = (
        PB_HEADER
        + '"#PB-9",m,SR-001,1,s,5%,lower-better,Full,warn,x,"line one\n# line two"\n'
    )
    assert KIT.csv_body(data) == data
    rows = KIT.csv_rows(HEADER + data)
    assert [r["PB-ID"] for r in rows] == ["#PB-9"]
    assert rows[0]["Notes"] == "line one\n# line two"
    assert KIT.csv_rows("") == [] and KIT.csv_rows(HEADER) == []
    assert KIT.csv_reader(HEADER + PB_HEADER).fieldnames == PB_HEADER.strip().split(",")


def test_load_csv_and_every_registry_reader_skip_the_header(tmp_path):
    path = tmp_path / "performance-budgets.csv"
    path.write_text(HEADER + PB_HEADER + PB_ROW, encoding="utf-8")
    assert [r["PB-ID"] for r in KIT.load_csv(path)] == ["PB-001"]
    perf = load_script("check_perf")
    assert [r["PB-ID"] for r in perf.load_budgets(path)] == ["PB-001"]
    rel = load_script("gen_release_checklist")
    assert [r["PB-ID"] for r in rel.load_csv(path)] == ["PB-001"]
    # The spine carrier's legacy CSV arm reads the same way, both shapes.
    sc = load_script("spine_carrier")
    text = HEADER + "SR-ID,Title,Status\nSR-001,one,Approved\nSR-001,two,Approved\n"
    assert [r["Title"] for r in sc.rows_seq_from_text(text, "SR-ID", ".csv")] == [
        "one",
        "two",
    ]
    assert sc.rows_from_text(text, "SR-ID", ".csv")["SR-001"]["Title"] == "two"
    # And the work-item converter's header check sees the REAL header.
    wc = load_script("wi_convert")
    wi = tmp_path / "work-items.csv"
    wi.write_text("# declared header\n" + ",".join(wc.COLUMNS) + "\n", encoding="utf-8")
    assert wc.load_csv(wi) == []
    # trace's structural check counts columns past the header, never over it.
    trace = load_script("trace")
    assert trace.structure_findings(path) == []
    path.write_text(HEADER + PB_HEADER + "PB-002,a,b\n", encoding="utf-8")
    found = trace.structure_findings(path)
    assert len(found) == 1 and "PB-002" in found[0]
    # ...and the reported line number is the FILE's line, header included.
    assert "(line {})".format(HEADER.count("\n") + 2) in found[0]


def test_the_kits_own_budget_registry_declares_and_still_loads():
    # The dogfood: IF-031's owner carries its `Contracts:` header, and every
    # reader still hands back the four real budget rows with `PB-ID` intact.
    path = ROOT / "docs" / "requirements" / "performance-budgets.csv"
    text = path.read_text(encoding="utf-8")
    assert text.startswith("#") and "Contracts: IF-031" in text.split("PB-ID,", 1)[0]
    gen_arch_map = load_script("gen_arch_map")
    ids, bodies = gen_arch_map.file_contracts(path)
    assert ids == ["IF-031"] and "IF-031" in bodies
    ids_seen = [r["PB-ID"] for r in KIT.load_csv(path)]
    assert ids_seen and all(i.startswith("PB-") for i in ids_seen)
    assert [
        r["PB-ID"] for r in load_script("check_perf").load_budgets(path)
    ] == ids_seen
    assert load_script("trace").structure_findings(path) == []


def test_check_perf_reads_a_header_carrying_registry_end_to_end(scaffold):
    make_minimal_project(scaffold)
    use_legacy_spine_carrier(scaffold)
    (scaffold / "docs" / "requirements" / "performance-budgets.csv").write_text(
        HEADER + PB_HEADER + PB_ROW.replace("warn", "fail"), encoding="utf-8"
    )
    (scaffold / "docs" / "test" / "perf-metrics.json").write_text(
        '{"PB-001": 9}', encoding="utf-8"
    )
    record_ids(scaffold)
    proc = run_py(["scripts/check_perf.py", "--tier", "full"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "PB-001" in proc.stdout and "FAIL" in proc.stdout
    # The integrity floor is clean over the same file.
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "performance-budgets.csv: row" not in proc.stdout


def test_a_header_on_the_shipped_template_would_be_read_the_same_way(tmp_path):
    # The template ships headerless (a spreadsheet opens it clean), and the
    # reader treats a copy WITH a header identically — so an adopter may add
    # one the day their budgets file owns a seam.
    tmpl = (
        ROOT / "project-trajectory" / "registries" / "performance-budgets.template.csv"
    ).read_text(encoding="utf-8")
    plain = KIT.csv_rows(tmpl)
    headed = KIT.csv_rows(HEADER + tmpl)
    assert plain == headed and [r["PB-ID"] for r in plain] == ["PB-000"]
    assert Path(tmp_path).exists()
