"""gen_cases.py: the spec grammar, the pairwise cover, and — critically — that
every dimensional spec shown in the kit's own docs actually parses."""

import csv
import itertools
import re
import tomllib

from conftest import KIT, SCRIPTS, load_script, run_py

gen_cases = load_script("gen_cases")

# Matches one dimension in the documented grammar wherever it appears in prose.
DIM_RE = re.compile(r"\w+=(?:set\{[^}]*\}|range\[[^\]]+\]|bool)")


def test_example_md_specs_parse():
    # EXAMPLE.md is the pattern people copy; every Permutations/spec snippet in
    # it must be accepted by the generator (regression: section 2 used to show
    # `field={...}` which gen_cases rejects).
    text = (KIT / "EXAMPLE.md").read_text(encoding="utf-8")
    assert not re.search(r"\w+=\{", text), (
        "EXAMPLE.md uses brace-set shorthand the gen_cases grammar rejects"
    )
    dims = DIM_RE.findall(text)
    assert dims, "EXAMPLE.md should demonstrate the Permutations grammar"
    for dim in dims:
        parsed, _ = gen_cases.parse_spec(dim)
        assert parsed, dim


def test_process_md_specs_parse():
    text = (KIT / "PROCESS.md").read_text(encoding="utf-8")
    for dim in DIM_RE.findall(text):
        parsed, _ = gen_cases.parse_spec(dim)
        assert parsed, dim


# EXAMPLE.md's registry snippets are the pattern people copy, and nothing else
# pins their cells: the 3771c003 Status-rename sweep missed EXAMPLE's four
# `Implemented` cells precisely because no test read them (WI-471). These two
# pins close that hole.
LEGAL_STATUS = {"Drafted", "Approved", "Modified"}
FENCED_BLOCK_RE = re.compile(r"```(toml|csv)\n(.*?)```", re.DOTALL)


def _example_status_cells():
    text = (KIT / "EXAMPLE.md").read_text(encoding="utf-8")
    cells = []
    for lang, block in FENCED_BLOCK_RE.findall(text):
        if lang == "toml":
            for table in tomllib.loads(block).values():
                for row_id, row in table.items():
                    if "status" in row:
                        cells.append((row_id, row["status"]))
        else:
            for row in csv.DictReader(block.strip().splitlines()):
                value = (row.get("Status") or "").strip()
                if value:
                    cells.append((row.get(next(iter(row))), value))
    return cells


def test_example_md_status_cells_stay_in_the_closed_vocabulary():
    cells = _example_status_cells()
    assert cells, "EXAMPLE.md should demonstrate Status cells"
    illegal = [(rid, v) for rid, v in cells if v not in LEGAL_STATUS]
    assert not illegal, (
        "EXAMPLE.md teaches out-of-vocabulary Status value(s): %s" % illegal
    )


def test_example_md_spine_walkthrough_teaches_the_toml_carrier():
    # The spine walkthrough must name the live TOML homes and never the
    # retired markdown/CSV spine carriers (the off-spine PB/procurement/
    # assets/repos templates legitimately stay CSV and are not listed here).
    text = (KIT / "EXAMPLE.md").read_text(encoding="utf-8")
    for home in (
        "stakeholder-needs.toml",
        "system-requirements.toml",
        "low-level-requirements.toml",
        "test-cases.toml",
        "[need.SN-",
        "[requirement.SR-",
        "[design.LLR-",
        "[test.TC-",
    ):
        assert home in text, "EXAMPLE.md no longer teaches %s" % home
    for retired in (
        "stakeholder-needs.md",
        "system-requirements.csv",
        "low-level-requirements.csv",
        "test-cases.csv",
    ):
        assert retired not in text, (
            "EXAMPLE.md still names the retired carrier %s" % retired
        )


def test_pairwise_covers_all_pairs_with_documented_count():
    # The 4x2x2 example from EXAMPLE.md: 8 cases (the doc's claim), every pair
    # of values across every pair of dimensions covered at least once.
    spec = (
        "field=set{plain,comma,quote,newline}; size=range[0..2GiB]; "
        "enc=set{utf8,utf16}; @pairwise"
    )
    dims, strategy = gen_cases.parse_spec(spec)
    assert strategy == "pairwise"
    values = [d[1] for d in dims]
    cases = gen_cases.all_pairs(values)
    assert len(cases) == 8  # keep EXAMPLE.md's stated reduction honest
    for i, j in itertools.combinations(range(len(values)), 2):
        want = set(itertools.product(values[i], values[j]))
        got = {(c[i], c[j]) for c in cases}
        assert got == want, "uncovered pairs between dims {} and {}".format(i, j)


def test_boundary_corners_localize_dimensions():
    dims, _ = gen_cases.parse_spec("a=range[0..10]; b=range[0..5]; c=bool")
    cases = gen_cases.boundary_corners(dims)
    assert cases[0] == ("0", "0", "true")  # all-low
    assert cases[1] == ("10", "5", "false")  # all-high
    # plus each dimension flipped high on its own, de-duplicated
    assert len(cases) <= 2 + len(dims)
    assert len(set(cases)) == len(cases)


def test_range_interior_points_are_not_boundaries():
    dims, _ = gen_cases.parse_spec("n=range[1..100|50]")
    ((_name, values, flags),) = dims
    assert values == ["1", "100", "50"]
    assert flags == [True, True, False]


def _template_tc_keys():
    """The keys the shipped TC template declares — the schema, now that the
    carrier has no header line to read."""
    text = (KIT / "registries" / "test-cases.template.toml").read_text(encoding="utf-8")
    return set(tomllib.loads(text)["test"]["TC-000"])


def test_toml_format_matches_the_shipped_registry_schema(tmp_path):
    # Repo-review 2026-07-21 M-2: the "ready to paste" rows drifted to 9 columns
    # when the registry grew Evidence/Phase — pasted raw they tripped trace.py's
    # own structure check. The carrier cutover makes the same point louder: a
    # paste form has to speak the carrier it is pasted INTO, so the emitted
    # tables are pinned to the template's key vocabulary, and the output must
    # parse as TOML at all — which is the structural check the column count was
    # standing in for.
    proc = run_py(
        [
            SCRIPTS / "gen_cases.py",
            "--spec",
            "a=bool; b=set{x,y}",
            "--format",
            "toml",
            "--id",
            "SR-001",
        ],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # The emitted tables all share the placeholder id, which is legal TOML only
    # once — parse ONE case, and assert every case is byte-identical in shape.
    # [0] is the dimensional-analysis preamble the tool prints first, not a row.
    blocks = [b for b in proc.stdout.split("[test.TC-xxx]")[1:] if b.strip()]
    assert len(blocks) > 1, proc.stdout  # the spec above yields several cases
    template_keys = _template_tc_keys()
    for block in blocks:
        parsed = tomllib.loads("[test.TC-xxx]" + block)["test"]["TC-xxx"]
        assert set(parsed) <= template_keys, sorted(set(parsed) - template_keys)
        assert parsed["verifies"] == ["SR-001"]
        assert parsed["parameters"]


def test_csv_format_stays_available_for_the_legacy_carrier(tmp_path):
    # An adopting repo that has not run migrate_carrier yet still writes CSV, so
    # the legacy paste form ships on. Pinned to the same schema, rendered as a
    # header: one column per template key, id first.
    proc = run_py(
        [
            SCRIPTS / "gen_cases.py",
            "--spec",
            "a=bool; b=set{x,y}",
            "--format",
            "csv",
            "--id",
            "SR-001",
        ],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    lines = proc.stdout.splitlines()
    header = next(ln for ln in lines if ln.startswith("TC-ID,"))
    assert len(header.split(",")) == len(_template_tc_keys()) + 1  # + the id
    data = lines[lines.index(header) + 1 :]
    rows = [r for r in csv.reader(data) if any(cell.strip() for cell in r)]
    assert rows, proc.stdout
    for row in rows:
        assert len(row) == len(header.split(",")), row
