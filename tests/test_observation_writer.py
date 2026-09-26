"""The observation writer, and the records the checker finds on disk (TC-230,
TC-231).

An observation result is recorded apart from its test case (SR-199), by one
command: `scripts/record_observation.py --tc TC-### --outcome pass|fail --by
<who or what>`. It refuses anything the record's policy forbids and writes
nothing then, it never opens the test-case registry for writing, and it stamps
each record with a digest of what the case declares it reads, so a later
change to those inputs makes the result stale without a clock. And a record
that reached the repository without the writer is judged when found: the
checker fails `--strict` naming the file.

Registered in `tests/conftest.py`'s `SLOW_MODULES`: every case drives the
writer or the checker as a subprocess over a bootstrapped scaffold. The
record's own format is pinned in memory in `tests/test_observation_record.py`.
"""

import datetime
import shutil

import pytest

from conftest import (
    ROOT,
    SCRIPTS,
    load_script,
    make_minimal_project,
    record_ids,
    run_py,
)

load_script("spine_carrier")  # puts scripts/ on the path for the package imports
import kitlib.observation as OBS  # noqa: E402
import kitlib.stage as STAGE  # noqa: E402

TC_CSV = "docs/test/test-cases.csv"
SR_CSV = "docs/requirements/system-requirements.csv"

# The minimal project's automated case, plus two observation cases: one
# declaring what it reads and a 30-day lifetime, one declaring no lifetime.
TEST_CASES = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,"
    "Status,Inputs,MaxAge\n"
    'TC-001,SR-001;LLR-001,Unit,call add and assert the sum,Smoke,"a=1; b=2",'
    '"Satisfies SR-001 AcceptanceCriteria",Yes,tests/test_demo.py::test_add_sr001,'
    "Approved,,\n"
    "TC-002,SR-001,Inspection,a reader reads the sum,Release,,"
    '"Satisfies SR-001 AcceptanceCriteria",No,docs/test/manual.md,Drafted,'
    "src/demo.py;SR-001,30\n"
    "TC-003,SR-001,Inspection,a reader reads the sum again,Release,,"
    '"Satisfies SR-001 AcceptanceCriteria",No,docs/test/manual.md,Drafted,,\n'
)


@pytest.fixture(scope="module")
def base(tmp_path_factory):
    """One bootstrapped minimal project for the whole module; each case works
    on its own copy."""
    root = tmp_path_factory.mktemp("observation-base")
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", root], cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    make_minimal_project(root)
    (root / TC_CSV).write_text(TEST_CASES, encoding="utf-8")
    record_ids(root)
    return root


@pytest.fixture
def repo(base, tmp_path):
    dest = tmp_path / "repo"
    shutil.copytree(base, dest)
    return dest


def _record(repo, *args):
    """Run the writer; also assert it never wrote the test-case registry."""
    before = (repo / TC_CSV).read_bytes()
    proc = run_py(["scripts/record_observation.py", *args], cwd=repo)
    assert (repo / TC_CSV).read_bytes() == before, "the writer edited the registry"
    return proc


def _written(repo):
    folder = repo / OBS.OBSERVATIONS_DIR
    if not folder.is_dir():
        return []
    return sorted(p.name for p in folder.iterdir())


def _utc(moment):
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


# --- TC-230: the writer refuses, writing nothing ------------------------------


@pytest.mark.parametrize(
    "args, needle",
    [
        (["--tc", "TC-099", "--outcome", "pass", "--by", "a reader"], "TC-099"),
        (["--tc", "TC-000", "--outcome", "pass", "--by", "a reader"], "TC-000"),
        (["--tc", "TC-001", "--outcome", "pass", "--by", "a reader"], "automated"),
        (["--tc", "TC-002", "--outcome", "maybe", "--by", "a reader"], "maybe"),
        (["--tc", "TC-002", "--outcome", "pass"], "provenance"),
        (["--tc", "TC-002", "--outcome", "pass", "--by", "   "], "provenance"),
        (["--tc", "TC-003", "--outcome", "pass", "--by", "a reader"], "MaxAge"),
    ],
    ids=[
        "undeclared",
        "the-template-example",
        "automated",
        "outcome",
        "no-provenance",
        "blank-provenance",
        "no-lifetime",
    ],
)
def test_the_writer_refuses_and_writes_nothing(repo, args, needle):
    proc = _record(repo, *args)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "REFUSED" in proc.stderr and needle in proc.stderr, proc.stderr
    assert _written(repo) == []


def test_an_expiry_later_than_the_lifetime_allows_is_refused(repo):
    too_late = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=31
    )
    proc = _record(
        repo,
        *("--tc", "TC-002", "--outcome", "pass", "--by", "a reader"),
        *("--expires", _utc(too_late)),
    )
    assert proc.returncode != 0 and "REFUSED" in proc.stderr, proc.stderr
    assert "30" in proc.stderr
    assert _written(repo) == []


def test_an_expiry_in_a_form_other_than_canonical_utc_is_refused(repo):
    proc = _record(
        repo,
        *("--tc", "TC-002", "--outcome", "pass", "--by", "a reader"),
        *("--expires", "next tuesday"),
    )
    assert proc.returncode != 0 and "REFUSED" in proc.stderr, proc.stderr
    assert _written(repo) == []


def test_with_no_expiry_given_the_record_expires_after_the_cases_lifetime(repo):
    proc = _record(repo, "--tc", "TC-002", "--outcome", "fail", "--by", "a reader")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    (name,) = _written(repo)
    record = OBS.parse((repo / OBS.OBSERVATIONS_DIR / name).read_text(encoding="utf-8"))
    assert record is not None and record["tc"] == "TC-002"
    assert record["outcome"] == "fail" and record["provenance"] == "a reader"
    observed = OBS.parse_utc(record["observed_at"])
    assert OBS.parse_utc(record["expires"]) - observed == datetime.timedelta(days=30)
    assert name == OBS.record_name("TC-002", record["observed_at"])


def test_an_expiry_within_the_lifetime_is_written_as_given(repo):
    within = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=10)
    proc = _record(
        repo,
        *("--tc", "TC-002", "--outcome", "pass", "--by", "a reader"),
        *("--expires", _utc(within)),
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    (name,) = _written(repo)
    record = OBS.parse((repo / OBS.OBSERVATIONS_DIR / name).read_text("utf-8"))
    assert record["expires"] == _utc(within)


# --- TC-230: the inputs digest -------------------------------------------------


def test_the_record_carries_the_digest_of_the_declared_inputs(repo):
    writer = load_script("record_observation")
    proc = _record(repo, "--tc", "TC-002", "--outcome", "pass", "--by", "a reader")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    (name,) = _written(repo)
    record = OBS.parse((repo / OBS.OBSERVATIONS_DIR / name).read_text("utf-8"))
    expected = writer.inputs_digest(repo, ["src/demo.py", "SR-001"])
    assert expected and record["judged"] == expected


def test_a_case_declaring_no_inputs_judges_the_empty_digest(repo):
    writer = load_script("record_observation")
    assert writer.inputs_digest(repo, []) == ""


def test_the_inputs_digest_ignores_line_endings_and_follows_content(repo):
    writer = load_script("record_observation")
    notes = repo / "docs" / "notes.md"
    notes.write_bytes(b"line one\nline two\n")
    lf = writer.inputs_digest(repo, ["docs/notes.md"])
    notes.write_bytes(b"line one\r\nline two\r\n")
    assert writer.inputs_digest(repo, ["docs/notes.md"]) == lf
    notes.write_bytes(b"line one\nline 2\n")
    assert writer.inputs_digest(repo, ["docs/notes.md"]) != lf


def test_a_registry_row_id_is_digested_from_that_rows_cells(repo):
    writer = load_script("record_observation")
    before = writer.inputs_digest(repo, ["SR-001"])
    # another row's edit leaves it alone...
    tcs = repo / TC_CSV
    tcs.write_text(
        tcs.read_text(encoding="utf-8").replace(
            "call add and assert the sum", "call add and check the sum"
        ),
        encoding="utf-8",
    )
    assert writer.inputs_digest(repo, ["SR-001"]) == before
    # ...and its own cell's edit moves it.
    srs = repo / SR_CSV
    srs.write_text(
        srs.read_text(encoding="utf-8").replace("Realizes SN-001.", "Serves SN-001."),
        encoding="utf-8",
    )
    assert writer.inputs_digest(repo, ["SR-001"]) != before


def test_the_order_of_the_declared_inputs_is_part_of_the_digest(repo):
    writer = load_script("record_observation")
    assert writer.inputs_digest(repo, ["src/demo.py", "SR-001"]) != (
        writer.inputs_digest(repo, ["SR-001", "src/demo.py"])
    )


# --- TC-230: every registry row id is digested from its cells ------------------
# A declared input naming a registry row must follow THAT row, whichever
# registry holds it: a row id the writer could not resolve would be digested as
# a missing path, so an edit to the row would never make a result stale. Each
# tier below gets one probe row with a cell reading `digest probe v1`.

TOML_PROBES = {
    "SN-901": ("docs/requirements/stakeholder-needs.toml", "need.SN-901", "need"),
    "STK-901": (
        "docs/requirements/stakeholder-needs.toml",
        "stakeholder.STK-901",
        "name",
    ),
    "SR-901": (
        "docs/requirements/system-requirements.toml",
        "requirement.SR-901",
        "title",
    ),
    "LLR-901": (
        "docs/requirements/low-level-requirements.toml",
        "design.LLR-901",
        "title",
    ),
    "TC-901": ("docs/test/test-cases.toml", "test.TC-901", "method"),
    "IF-901": ("docs/requirements/interfaces.toml", "interface.IF-901", "data"),
    "CMP-901": ("docs/requirements/components.toml", "component.CMP-901", "name"),
    "EXT-901": ("docs/requirements/external.toml", "entity.EXT-901", "name"),
    "B-901": ("docs/requirements/external.toml", "boundary.B-901", "carries"),
    "REL-901": ("docs/requirements/external.toml", "relationship.REL-901", "carries"),
    "DA-901": ("docs/requirements/assumptions.toml", "assumption.DA-901", "assumption"),
    "SUR-901": ("docs/requirements/assumptions.toml", "surrogate.SUR-901", "name"),
    "OI-901": ("docs/requirements/open-items.toml", "open_item.OI-901", "title"),
}
CSV_PROBES = {
    "PB-901": ("docs/requirements/performance-budgets.csv", "PB-ID,Metric"),
    "PART-901": ("docs/requirements/procurement.csv", "PART-ID,Name"),
    "ASSET-901": ("docs/requirements/assets.csv", "ASSET-ID,Name"),
    "REPO-901": ("docs/requirements/repos.csv", "REPO-ID,Delegated"),
}
# The legacy name for REPO: no template ships `modules.csv`, but a repo that
# still carries one is read through the same CSV rule, so it keeps its probe.
LEGACY_CSV_PROBES = {
    "MOD-901": ("docs/requirements/modules.csv", "MOD-ID,Delegated"),
}
WI_PROBE = "docs/work/queued/WI-901-digest-probe.md"
PROBED = sorted(TOML_PROBES) + sorted(CSV_PROBES) + ["WI-901"]
EVERY_TIER = PROBED + sorted(LEGACY_CSV_PROBES)


@pytest.fixture(scope="module")
def plain_base(tmp_path_factory):
    """A freshly bootstrapped scaffold, on the TOML carrier it ships with."""
    root = tmp_path_factory.mktemp("registry-tiers")
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", root], cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return root


def _plant_probe(root, rid):
    """Write the probe row for `rid` and return the file holding it."""
    if rid in TOML_PROBES:
        rel, table, key = TOML_PROBES[rid]
        path = root / rel
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        path.write_text(
            text.rstrip("\n") + '\n\n[{}]\n{} = "digest probe v1"\n'.format(table, key),
            encoding="utf-8",
        )
        return path
    if rid in CSV_PROBES or rid in LEGACY_CSV_PROBES:
        rel, header = {**CSV_PROBES, **LEGACY_CSV_PROBES}[rid]
        path = root / rel
        text = path.read_text(encoding="utf-8") if path.is_file() else header + "\n"
        path.write_text(
            text.rstrip("\n") + "\n{},digest probe v1\n".format(rid), encoding="utf-8"
        )
        return path
    path = root / WI_PROBE
    path.write_text(
        '+++\nid = "WI-901"\ntitle = "digest probe v1"\n+++\n', encoding="utf-8"
    )
    return path


def _absent(rid):
    """The digest a row id gets when no registry holds it."""
    import hashlib

    fold = hashlib.sha256()
    fold.update(rid.encode("utf-8") + b"\0" + b"(absent)" + b"\n")
    return "sha256:" + fold.hexdigest()


def _registry_csv_id_columns():
    """The id column (first header cell) of every registry CSV the kit ships as
    a template or this repo carries under the writer's registry folders: the
    CSVs the writer's last rule resolves an id through."""
    writer = load_script("record_observation")
    paths = sorted((ROOT / "project-trajectory" / "registries").glob("*.template.csv"))
    for folder in writer.REGISTRY_DIRS:
        paths += sorted((ROOT / folder).glob("*.csv"))
    out = set()
    for path in paths:
        header = path.read_text(encoding="utf-8-sig").splitlines()[0]
        out.add(header.split(",", 1)[0].strip())
    return out


def test_the_probes_are_exactly_the_tiers_the_writer_resolves():
    """The probes are written out so each can be planted, and this keeps them
    whole in both directions: the expected tiers are read from the sources the
    writer resolves ids through (the carrier's tables, which include the needs'
    own loader, and the registry CSV headers, which name the work items' spec
    folder too), so a registry the kit gains fails here until it has a probe,
    and a probe naming no registry fails too."""
    carrier = load_script("spine_carrier")
    columns = set(carrier.REGISTRY_TABLE) | _registry_csv_id_columns()
    expected = {col[: -len("-ID")] for col in columns if col.endswith("-ID")}
    assert {rid.rsplit("-", 1)[0] for rid in PROBED} == expected


@pytest.mark.parametrize("rid", EVERY_TIER)
def test_every_registry_tiers_row_id_is_digested_from_that_rows_cells(
    plain_base, tmp_path, rid
):
    root = tmp_path / "repo"
    shutil.copytree(plain_base, root)
    writer = load_script("record_observation")
    assert writer.inputs_digest(root, [rid]) == _absent(rid), "fixture: no such row"
    path = _plant_probe(root, rid)
    planted = writer.inputs_digest(root, [rid])
    assert planted != _absent(rid), "{} was not resolved to its row".format(rid)
    path.write_text(
        path.read_text(encoding="utf-8").replace("digest probe v1", "digest probe v2"),
        encoding="utf-8",
    )
    assert writer.inputs_digest(root, [rid]) not in (planted, _absent(rid))


# --- TC-230: recording a sample moves no stage or release evidence ------------

EVIDENCE = (
    "outcome = pass\ntier = full\ncommand = x\nrevision = x\nbinding = sha256:x\n"
)


@pytest.mark.parametrize("src", ["src", "."])
def test_recording_a_sample_leaves_the_fingerprint_and_the_binding_unchanged(repo, src):
    """Also with the widest legal source surface (`src = .`), where the
    records' directory lies inside the tree a release claim is bound to."""
    stack = repo / "docs" / "stack.ini"
    stack.write_text(
        stack.read_text(encoding="utf-8").replace("src = src", "src = " + src, 1),
        encoding="utf-8",
    )
    (repo / "docs" / "test" / "evidence").write_text(EVIDENCE, encoding="utf-8")
    fingerprint = STAGE.fingerprint(repo, memo=None)
    binding = STAGE.evidence_binding(repo, memo=None)
    proc = _record(repo, "--tc", "TC-002", "--outcome", "pass", "--by", "a reader")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _written(repo)
    assert STAGE.fingerprint(repo, memo=None) == fingerprint
    assert STAGE.evidence_binding(repo, memo=None) == binding


def test_a_fresh_scaffold_receives_the_writer_and_the_record_module(base):
    assert (base / "scripts" / "record_observation.py").is_file()
    assert (base / "scripts" / "kitlib" / "observation.py").is_file()
    proc = run_py(["scripts/record_observation.py", "--help"], cwd=base)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "--tc" in proc.stdout and "--outcome" in proc.stdout


# --- TC-231: records found on disk are checked --------------------------------

GOOD_NAME = "TC-002.2026-09-01T000000Z.toml"


def _text(**cells):
    rec = {
        "tc": "TC-002",
        "outcome": "pass",
        "observed_at": "2026-09-01T00:00:00Z",
        "provenance": "a reader",
        "expires": "2026-10-01T00:00:00Z",
        "judged": "",
    }
    rec.update(cells)
    return OBS.render(rec)


# (file name, text) for each defect the strict run must name.
DEFECTS = {
    "unparseable": ("TC-002.2026-09-02T000000Z.toml", 'tc = "TC-002"\noutcome = '),
    "not-canonical": (
        "TC-002.2026-09-03T000000Z.toml",
        _text(observed_at="2026-09-03 00:00:00Z"),
    ),
    "expiry-first": (
        "TC-002.2026-09-04T000000Z.toml",
        _text(observed_at="2026-09-04T00:00:00Z", expires="2026-09-03T00:00:00Z"),
    ),
    "no-provenance": (
        "TC-002.2026-09-05T000000Z.toml",
        _text(observed_at="2026-09-05T00:00:00Z", provenance="  "),
    ),
    "undeclared": ("TC-099.2026-09-01T000000Z.toml", _text(tc="TC-099")),
    "automated": ("TC-001.2026-09-01T000000Z.toml", _text(tc="TC-001")),
    "too-long": (
        "TC-002.2026-09-06T000000Z.toml",
        _text(observed_at="2026-09-06T00:00:00Z", expires="2026-10-15T00:00:00Z"),
    ),
    # A whole, in-policy record saved under a name other than its case's and
    # instant's: it must not become evidence by being renamed.
    "misnamed": (
        "misnamed.toml",
        _text(observed_at="2026-09-07T00:00:00Z", expires="2026-10-01T00:00:00Z"),
    ),
}


def _plant(repo, name, text):
    folder = repo / OBS.OBSERVATIONS_DIR
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_text(text, encoding="utf-8")


def _strict(repo):
    return run_py(["scripts/trace.py", "--strict"], cwd=repo)


def _naming(stdout, name):
    return [line for line in stdout.splitlines() if name in line]


def test_a_well_formed_record_produces_nothing(repo):
    _plant(repo, GOOD_NAME, _text())
    proc = _strict(repo)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _naming(proc.stdout, GOOD_NAME) == []
    assert "observation record" not in proc.stdout


def test_each_malformed_or_out_of_policy_record_fails_strict_naming_the_file(repo):
    _plant(repo, GOOD_NAME, _text())
    folder = repo / OBS.OBSERVATIONS_DIR
    for label, (name, text) in DEFECTS.items():
        _plant(repo, name, text)
        proc = _strict(repo)
        assert proc.returncode == 1, (label, proc.stdout + proc.stderr)
        named = _naming(proc.stdout, name)
        assert named and all(line.startswith("FINDING") for line in named), (
            label,
            proc.stdout,
        )
        assert _naming(proc.stdout, GOOD_NAME) == [], label
        (folder / name).unlink()


def test_a_leading_dot_file_is_ignored(repo):
    _plant(repo, GOOD_NAME, _text())
    _plant(repo, ".TC-002.2026-09-07T000000Z.toml", 'tc = "TC-002"\noutcome = ')
    proc = _strict(repo)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert ".TC-002" not in proc.stdout
