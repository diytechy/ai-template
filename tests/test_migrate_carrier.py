"""The OI-12 carrier converter: `.md` + `.csv` registries -> one TOML carrier.

The conversion's whole claim is that it is LOSSLESS, so the tests that matter
are the ones proving the loss detector can actually fail. A round-trip check
that cannot report a dropped cell is worth nothing, and a green from it would
be exactly the "a green never hides a skipped check" failure SN-008 forbids —
so every corruption class is driven here, not just the happy path.
"""

import subprocess
import sys
import tomllib

import pytest
from conftest import ROOT, SCRIPTS, load_script

mc = load_script("migrate_carrier")

HEADER = ["SR-ID", "Title", "Requirement", "SN-Refs", "Phase", "Permutations"]
ROW = {
    "SR-ID": "SR-001",
    "Title": "Addition",
    "Requirement": "The system shall add two numbers.",
    "SN-Refs": "SN-001 SN-002",
    "Phase": "3",
    "Permutations": "",
}


def _expected(rows, header=HEADER, id_col="SR-ID"):
    return {
        (r.get(id_col) or "").strip(): {
            mc.KEY.get(c, c): (r.get(c) or "").strip()
            for c in header
            if c != id_col and (r.get(c) or "").strip()
        }
        for r in rows
    }


def _convert(rows=None):
    rows = rows or [ROW]
    text = mc.rows_to_toml("requirement", "SR-ID", rows, HEADER)
    return text, _expected(rows)


def test_a_clean_conversion_reports_nothing():
    text, expected = _convert()
    assert mc.compare("f", "requirement", expected, text) == []


def test_the_emitted_toml_parses_and_keys_on_the_prefixed_id():
    text, _ = _convert()
    parsed = tomllib.loads(text)
    # `[requirement.SR-001]` — bare key, prefix retained. The prefix is what
    # ~6,400 hand-authored citations grep for, so the registry has to stay
    # findable by the same token every commit message and log entry uses.
    assert list(parsed["requirement"]) == ["SR-001"]
    assert "[requirement.SR-001]" in text


def test_refs_become_a_typed_array_and_phase_an_int():
    text, _ = _convert()
    row = tomllib.loads(text)["requirement"]["SR-001"]
    # The typed array is what retires refs()'s split-on-whitespace rule, and
    # with it the `SN-001 and SN-002` -> "`and` is an orphan" defect.
    assert row["sn_refs"] == ["SN-001", "SN-002"]
    assert row["phase"] == 3 and isinstance(row["phase"], int)


def test_an_empty_cell_becomes_an_absent_key_not_an_empty_string():
    text, _ = _convert()
    # "unset" and "set to empty" stop being the same value — a distinction CSV
    # cannot carry at all.
    assert "permutations" not in tomllib.loads(text)["requirement"]["SR-001"]


def test_a_duplicate_id_is_a_PARSE_error_rather_than_a_check():
    text, expected = _convert()
    findings = mc.compare("f", "requirement", expected, text + text)
    assert findings and "twice" in findings[0]


@pytest.mark.parametrize(
    "corrupt,needle",
    [
        (lambda t: t.replace('title = "Addition"\n', ""), "title"),
        (lambda t: t.replace("add two numbers", "add three numbers"), "requirement"),
        (lambda t: t.replace('["SN-001", "SN-002"]', '["SN-001"]'), "sn_refs"),
        (lambda t: t.replace("phase = 3", "phase = 4"), "phase"),
    ],
    ids=["dropped-cell", "mangled-prose", "lost-ref", "changed-int"],
)
def test_the_loss_detector_actually_bites(corrupt, needle):
    text, expected = _convert()
    findings = mc.compare("f", "requirement", expected, corrupt(text))
    assert findings, "corruption of {} went unreported".format(needle)
    assert needle in findings[0]


def test_a_missing_row_is_reported():
    text, expected = _convert()
    expected["SR-999"] = {"title": "never emitted"}
    findings = mc.compare("f", "requirement", expected, text)
    assert any("SR-999" in f for f in findings)


def test_a_prose_cell_with_quotes_commas_and_a_pipe_survives():
    # The cells CSV fights: a literal `|` (which the SN markdown tables cannot
    # hold at all), embedded quotes, and commas.
    row = dict(ROW, Requirement='He said "a|b", then left.')
    text, expected = _convert([row])
    assert mc.compare("f", "requirement", expected, text) == []
    assert (
        tomllib.loads(text)["requirement"]["SR-001"]["requirement"]
        == 'He said "a|b", then left.'
    )


def test_the_meta_repos_own_registries_convert_losslessly():
    """The dogfood: the real spine, not a fixture. Reads only — `write=False`."""
    findings, written = mc.convert(ROOT, write=False)
    assert findings == [], findings[:5]
    assert written == []


SN_MD = (
    "## Core needs\n\n"
    "| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance |\n"
    "|---|---|---|---|---|\n"
    "| SN-001 | Add two numbers. | Demo. | M | add(1,2) is 3. |\n\n"
    "## Draft needs (unratified)\n\n"
    "| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance |\n"
    "|---|---|---|---|---|\n"
    "| SN-002 | Subtract. | Demo. | S | tbd |\n\n"
    "## Edge cases\n\n"
    "| SN-ID | Lifecycle | Scenario | Expected behavior |\n"
    "|---|---|---|---|\n"
    "| SN-003 | Provision | Missing dependency | named refusal |\n"
)


def test_sn_edge_rows_keep_their_native_fields(tmp_path):
    """The edge-case table has its own columns, and the carrier keeps them.

    `traj_parse._sn_fields` folds an edge row onto the core four for the
    generated exports (its Scenario reads as the need). That fold is a
    PRESENTATION rule the markdown table forced; baking it into the carrier
    would make the export's reading the only reading there is.

    Driven over a FIXTURE rather than the live registry (which is TOML since the
    cutover, so it has no markdown source left to convert), and then re-asserted
    against the live carrier below — the fixture proves the conversion rule, the
    live half proves the repo actually carries it.
    """
    src = tmp_path / "stakeholder-needs.md"
    src.write_text(SN_MD, encoding="utf-8")
    needs = mc.read_sn(src)
    kinds = {kind for _, kind, _ in needs}
    assert kinds == {"core", "draft", "edge"}
    edge = next(f for _, kind, f in needs if kind == "edge")
    assert set(edge) == {"lifecycle", "scenario", "expected"}
    parsed = tomllib.loads(mc.sn_to_toml(needs))["need"]
    assert all("kind" in row for row in parsed.values())
    assert set(parsed["SN-003"]) == {"kind", "lifecycle", "scenario", "expected"}


def test_the_live_need_carrier_holds_the_edge_fields_unfolded():
    """The same property on the REPO'S OWN needs registry, post-cutover.

    The fixture above can only prove the converter's rule; this proves the
    conversion that actually shipped kept it — an edge need still carries
    `lifecycle`/`scenario`/`expected` and NONE of the core four, so nothing has
    quietly folded the tier on the way into the carrier. Non-vacuous by
    construction: it fails if the repo has no edge needs at all.
    """
    live = ROOT / "docs" / "requirements" / "stakeholder-needs.toml"
    needs = tomllib.loads(live.read_text(encoding="utf-8"))["need"]
    edges = [n for n in needs.values() if n.get("kind") == "edge"]
    assert edges, "the repo declares no edge-case needs — this check would be vacuous"
    for need in edges:
        assert {"lifecycle", "scenario", "expected"} >= set(need) - {"kind"}
        assert not {"need", "why", "priority", "acceptance"} & set(need)


# --- the loss oracle must not be the thing under test ------------------------


def _spine_repo(tmp_path, **files):
    (tmp_path / "docs" / "requirements").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    for rel, text in files.items():
        (tmp_path / rel).write_text(text, encoding="utf-8")
    return tmp_path


def test_a_need_under_an_UNRECOGNISED_heading_is_not_silently_dropped(tmp_path):
    """The review's BLOCKER 2(a).

    `read_sn` classified a table by its heading and skipped every row under a
    heading it did not name — and the loss oracle was built FROM `read_sn`'s
    output, so a whole table vanished with `findings == []`. A converter cannot
    certify its own blind spot. An unfamiliar heading is a naming choice, not a
    statement that the rows below are not needs.
    """
    root = _spine_repo(
        tmp_path,
        **{
            "docs/requirements/stakeholder-needs.md": (
                "## Miscellaneous\n\n"
                "| SN-ID | Need | Why | Priority | Acceptance |\n"
                "|---|---|---|---|---|\n"
                "| SN-123 | a real need | matters | M | works |\n"
            )
        },
    )
    findings, _ = mc.convert(root, write=False)
    assert findings == [], findings
    ids = [
        rid
        for rid, _kind, _f in mc.read_sn(
            root / "docs/requirements/stakeholder-needs.md"
        )
    ]
    assert ids == ["SN-123"]


def test_the_raw_oracle_bites_when_the_READER_goes_blind(monkeypatch, tmp_path):
    """...and the second leg, which is what makes the fix durable.

    Fixing `read_sn` closes today's hole; it does nothing for tomorrow's. The
    raw-source oracle reads need ids off the markdown with no reference to how
    the reader interpreted it, so ANY future reader regression surfaces as a
    finding instead of as a silent omission. Driven by blinding the reader.
    """
    root = _spine_repo(
        tmp_path,
        **{
            "docs/requirements/stakeholder-needs.md": (
                "## Core needs\n\n"
                "| SN-ID | Need | Why | Priority | Acceptance |\n"
                "|---|---|---|---|---|\n"
                "| SN-001 | a real need | matters | M | works |\n"
            )
        },
    )
    assert mc.convert(root, write=False)[0] == []
    monkeypatch.setattr(mc, "read_sn", lambda path: [])
    findings, _ = mc.convert(root, write=False)
    assert findings and "SN-001" in findings[0]
    assert "absent from the conversion" in findings[0]


def test_cell_whitespace_is_CONTENT_and_survives_the_conversion(tmp_path):
    """The review's BLOCKER 2(b).

    The converter stripped each cell and the oracle stripped its expectation,
    so a cell whose leading/trailing whitespace was content lost it and the
    round-trip check reported `findings == []` — comparing the converter's
    output against the converter's own reading of the source.
    """
    padded = "  leading and trailing prose  "
    root = _spine_repo(
        tmp_path,
        **{
            "docs/requirements/system-requirements.csv": (
                'SR-ID,Title,Requirement,Status\nSR-001,T,"{}",Verified\n'.format(
                    padded
                )
            )
        },
    )
    findings, _ = mc.convert(root, write=True)
    assert findings == [], findings
    out = tomllib.loads(
        (root / "docs/requirements/system-requirements.toml").read_text(
            encoding="utf-8"
        )
    )
    assert out["requirement"]["SR-001"]["requirement"] == padded

    # A whitespace-ONLY cell is still an empty cell — an absent key, not a
    # cell holding spaces. That is the one place the strip survives.
    root2 = _spine_repo(
        tmp_path / "b",
        **{
            "docs/requirements/system-requirements.csv": (
                'SR-ID,Title,Requirement,Status\nSR-001,T,"   ",Verified\n'
            )
        },
    )
    findings2, _ = mc.convert(root2, write=True)
    assert findings2 == [], findings2
    out2 = tomllib.loads(
        (root2 / "docs/requirements/system-requirements.toml").read_text(
            encoding="utf-8"
        )
    )
    assert "requirement" not in out2["requirement"]["SR-001"]


def test_the_ADOPTING_recipe_run_verbatim_leaves_the_registries_TRACKED(tmp_path):
    """The review's BLOCKER 1, driven as the adopter would run it.

    The recipe wrote four TOML files and then staged four DELETIONS with
    `git rm`, never staging the new files — so an adopter following it verbatim
    committed the removal of their whole spine. This lifts the fenced commands
    OUT of ADOPTING.md and runs them, so the doc and the behaviour cannot drift:
    a recipe nobody executes is prose.
    """
    import re

    adopting = (ROOT / "project-trajectory" / "ADOPTING.md").read_text(encoding="utf-8")
    block = adopting.split("**Run it, check it, then stage BOTH sides")[1]
    recipe = block.split("```")[1]
    # The commands, with the doc's line continuations joined and comments cut.
    commands = [
        line.strip()
        for line in re.sub(r"\\\n\s+", " ", recipe).split("\n")
        if line.strip() and not line.strip().startswith("#")
    ]
    assert any(c.startswith("git add") for c in commands), commands
    assert any(c.startswith("git rm") for c in commands), commands

    root = _spine_repo(
        tmp_path,
        **{
            "docs/requirements/stakeholder-needs.md": (
                "## Core needs\n\n"
                "| SN-ID | Need | Why | Priority | Acceptance |\n"
                "|---|---|---|---|---|\n"
                "| SN-001 | a need | matters | M | works |\n"
            ),
            "docs/requirements/system-requirements.csv": (
                "SR-ID,Title,SN-Refs,Status\nSR-001,Adder,SN-001,Verified\n"
            ),
            "docs/requirements/low-level-requirements.csv": (
                "LLR-ID,SR-Refs,Title,Status\nLLR-001,SR-001,Core,Verified\n"
            ),
            "docs/test/test-cases.csv": (
                "TC-ID,Verifies,Method,Status\nTC-001,SR-001;LLR-001,run,Verified\n"
            ),
        },
    )

    def run(*argv):
        return subprocess.run(argv, cwd=root, check=True, capture_output=True)

    run("git", "init", "-q")
    run("git", "add", "-A")
    run("git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "before")

    for command in commands:
        argv = command.split("#")[0].split()
        if argv[0] == "python":
            # The adopter's `scripts/migrate_carrier.py` is this kit's shipped
            # copy; everything else about the invocation is theirs, including
            # `--root .` resolving against their repo, so it runs as a
            # SUBPROCESS from `root` rather than in-process from the test's cwd.
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS / "migrate_carrier.py")] + argv[2:],
                cwd=root,
                capture_output=True,
                text=True,
            )
            assert proc.returncode == 0, command + "\n" + proc.stdout + proc.stderr
        elif argv[:2] == ["git", "status"]:
            continue
        else:
            run(*argv)
    run("git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "cutover")

    tracked = subprocess.run(
        ["git", "ls-files"], cwd=root, capture_output=True, text=True
    ).stdout.split()
    for rel in (
        "docs/requirements/stakeholder-needs.toml",
        "docs/requirements/system-requirements.toml",
        "docs/requirements/low-level-requirements.toml",
        "docs/test/test-cases.toml",
    ):
        assert rel in tracked, (rel, tracked)
    for rel in (
        "docs/requirements/stakeholder-needs.md",
        "docs/requirements/system-requirements.csv",
    ):
        assert rel not in tracked, rel
    # ...and the committed content is the CONVERSION, not an empty shell.
    committed = subprocess.run(
        ["git", "show", "HEAD:docs/requirements/system-requirements.toml"],
        cwd=root,
        capture_output=True,
        text=True,
    ).stdout
    assert tomllib.loads(committed)["requirement"]["SR-001"]["title"] == "Adder"
