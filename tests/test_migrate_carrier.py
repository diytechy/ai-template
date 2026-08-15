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


# --- WI-443 / OI-14 part B: the last two registries onto the carrier ----------

IF_HEADER = [
    "IF-ID",
    "Direction",
    "ThisProject",
    "Counterpart",
    "Contract",
    "Signal",
    "SignalNote",
    "Rationale",
    "SR-Refs",
    "Version",
    "Stability",
    "Component",
    "Notes",
]
IF_ROW = {
    "IF-ID": "IF-001",
    "Direction": "Provides",
    "ThisProject": "scripts/trace",
    "Counterpart": "scripts/check",
    "Contract": 'trace.py CLI: --strict exits 1 on an orphan; writes "report.md"',
    "Signal": "discrete",
    "SignalNote": "",
    "Rationale": "",
    "SR-Refs": "SR-001;SR-002",
    "Version": "v1",
    "Stability": "Stable",
    "Component": "",
    "Notes": "source - consumes nothing declared",
}
CMP_HEADER = [
    "CMP-ID",
    "Name",
    "Category",
    "Knowledge",
    "State",
    "SupersededBy",
    "PartOf",
    "DetailDoc",
    "Notes",
]
CMP_ROW = {
    "CMP-ID": "CMP-001",
    "Name": "W1 Registry & conformance",
    "Category": "software",
    "Knowledge": "registry-hygiene",
    "State": "planned",
    "SupersededBy": "",
    "PartOf": "",
    "DetailDoc": "",
    "Notes": "the spine and everything that decides whether it holds",
}


@pytest.mark.parametrize(
    "table,id_col,header,row",
    [
        ("interface", "IF-ID", IF_HEADER, IF_ROW),
        ("component", "CMP-ID", CMP_HEADER, CMP_ROW),
    ],
)
def test_the_two_new_tiers_round_trip_cell_for_cell(table, id_col, header, row):
    """The cutover's own oracle, on the two registries WI-443 moved.

    Both waited on OI-14 deliberately — converting a registry before the ruling
    that rewrites what its rows ARE converts it twice — so this is the ONE
    conversion each gets, and the round-trip is what proves no cell was spent
    on it. `SR-Refs` re-joins on `;`, the separator the registries actually use;
    an empty cell is an ABSENT KEY, never `""`."""
    text = mc.rows_to_toml(table, id_col, [row], header)
    expected = _expected([row], header=header, id_col=id_col)
    assert mc.compare("f", table, expected, text) == []
    parsed = tomllib.loads(text)[table][row[id_col]]
    # The empty cells did not become empty strings.
    for absent in ("signal_note", "rationale", "component", "superseded_by", "part_of"):
        assert absent not in parsed or parsed[absent], absent
    # ...and the ref cell is a typed array, not a `;`-joined string.
    if table == "interface":
        assert parsed["sr_refs"] == ["SR-001", "SR-002"]
        assert parsed["signal"] == "discrete"


def test_the_retired_if_status_column_has_no_carrier_key():
    """OI-14 part B retired `Status` on the IF tier, and the absence is
    LOAD-BEARING rather than cosmetic: with no `KEY` entry a stray `Status`
    cell keys as the literal `Status`, where the schema tier sees it, instead
    of being silently absorbed under a name a reader would trust."""
    carrier = load_script("spine_carrier")
    assert "status" not in carrier.REGISTRY_KEYS["IF-ID"]
    assert "signal" in carrier.REGISTRY_KEYS["IF-ID"]
    assert "rationale" in carrier.REGISTRY_KEYS["IF-ID"]
    # WI-442: `stability` RETIRED in its turn, replaced by `approval` — the
    # same defect the `Status` retirement above fixed, one column later.
    assert "stability" not in carrier.REGISTRY_KEYS["IF-ID"]
    assert "approval" in carrier.REGISTRY_KEYS["IF-ID"]


def test_neither_new_registry_survives_under_its_old_carrier():
    """The house rule, asserted on the TREE rather than on a fixture: the
    conversion is only finished when the CSV is GONE. Both homes at once is a
    hard refusal (`spine_carrier.resolve`), so a lingering source file would
    red every reader — this catches it in one place instead."""
    for stale in (
        "docs/requirements/interfaces.csv",
        "docs/requirements/components.csv",
        "project-trajectory/registries/interfaces.template.csv",
        "project-trajectory/registries/components.template.csv",
    ):
        assert not (ROOT / stale).exists(), stale
    for live in (
        "docs/requirements/interfaces.toml",
        "docs/requirements/components.toml",
        "project-trajectory/registries/interfaces.template.toml",
        "project-trajectory/registries/components.template.toml",
    ):
        assert (ROOT / live).is_file(), live


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


def test_the_live_need_carrier_holds_no_orphaned_edge_fields():
    """The edge TIER retired from the live registry (OI-18, ruled 2026-08-13).

    The ten edge rows dissolved into the requirements that already carried
    them, so the live registry now holds ZERO `kind = "edge"` rows — and no
    surviving row may carry the edge-only fields (`lifecycle`/`scenario`/
    `expected`), which would be a half-dissolved state no reader defines.
    The converter's edge-field RULE stays proven by the fixture test above,
    and the SHIPPED TEMPLATE still carries edge examples until the schema
    batch sheds those fields (the OI-18 blast-radius sequencing).
    """
    live = ROOT / "docs" / "requirements" / "stakeholder-needs.toml"
    needs = tomllib.loads(live.read_text(encoding="utf-8"))["need"]
    edges = [nid for nid, n in needs.items() if n.get("kind") == "edge"]
    assert not edges, (
        "OI-18 dissolved the edge tier; a resurrected edge row is a "
        "regression against the ruling: " + str(edges)
    )
    strays = {
        nid: sorted({"lifecycle", "scenario", "expected"} & set(n))
        for nid, n in needs.items()
        if {"lifecycle", "scenario", "expected"} & set(n)
    }
    assert not strays, "edge-only fields on non-edge rows: " + str(strays)


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
                'SR-ID,Title,Requirement,Status\nSR-001,T,"{}",Approved\n'.format(
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
                'SR-ID,Title,Requirement,Status\nSR-001,T,"   ",Approved\n'
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


def test_the_pack_recipe_run_verbatim_leaves_the_registries_TRACKED(tmp_path):
    """The review's BLOCKER 1, driven as the adopter would run it.

    The recipe wrote four TOML files and then staged four DELETIONS with
    `git rm`, never staging the new files — so an adopter following it verbatim
    committed the removal of their whole spine. This lifts the fenced commands
    OUT of the doc and runs them, so the doc and the behaviour cannot drift:
    a recipe nobody executes is prose. (The recipe moved from ADOPTING.md §6 to
    RESYNC_PACK.md at OI-27's one-home ruling; the extraction follows it.)
    """
    import re

    adopting = (ROOT / "project-trajectory" / "RESYNC_PACK.md").read_text(
        encoding="utf-8"
    )
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
                "SR-ID,Title,SN-Refs,Status\nSR-001,Adder,SN-001,Approved\n"
            ),
            "docs/requirements/low-level-requirements.csv": (
                "LLR-ID,SR-Refs,Title,Status\nLLR-001,SR-001,Core,Approved\n"
            ),
            "docs/test/test-cases.csv": (
                "TC-ID,Verifies,Method,Status\nTC-001,SR-001;LLR-001,run,Approved\n"
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


# --- batch-2: the off-spine registries (repo-lock §8.1) ------------------------
# open-items and agents joined the carrier on the SAME converter, which is the
# ruling's point: a second converter drifts from the first, and the divergence
# is silent content loss. What is genuinely new on this branch is a COMMENT
# (agents.csv carries a `# tag-rank:` line agent_route PARSES) and a DOTTED ID
# (`ANTHROPIC-OPUS-4.8`, which TOML reads as a table path unless quoted), so
# both get their own planted corruption.

AGENTS_CSV = (
    "Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes\n"
    "# a prose line, with commas, that DictReader would read as a nine-cell row\n"
    "# tag-rank: ga>preview>beta>exp\n"
    'ANTHROPIC-OPUS-4.8,ANTHROPIC,opus,4.8,strong,"c -p {model}",K=v,note\n'
    "# a comment BETWEEN rows, which must stay between them\n"
    "OPENAI-GPT-5.2,OPENAI,gpt,5.2,quick,codex {model},,\n"
)


def _convert_agents(tmp_path, text=AGENTS_CSV):
    src = tmp_path / "docs" / "agents.csv"
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text(text, encoding="utf-8", newline="")
    findings, written = mc.convert(tmp_path, write=True)
    return findings, (tmp_path / "docs" / "agents.toml").read_text(encoding="utf-8")


def test_a_dotted_id_is_quoted_so_toml_does_not_read_it_as_a_table_path(tmp_path):
    findings, out = _convert_agents(tmp_path)
    assert findings == [], findings
    assert '[agent."ANTHROPIC-OPUS-4.8"]' in out
    # ...and the id comes back WHOLE, which is the property that matters.
    parsed = tomllib.loads(out)["agent"]
    assert set(parsed) == {"ANTHROPIC-OPUS-4.8", "OPENAI-GPT-5.2"}
    assert parsed["ANTHROPIC-OPUS-4.8"]["version"] == "4.8"


def test_the_dotted_id_leg_catches_a_bare_key(tmp_path):
    """PLANTED CORRUPTION on the oracle that exists for this defect.

    Written bare, `[agent.ANTHROPIC-OPUS-4.8]` is VALID TOML — it declares two
    nested tables — so the emitted file parses, and a checker built from the
    converter's own key construction finds the row exactly where it put it. Only
    reading the ids off the RAW source catches it, which is what `raw_id_findings`
    does; this proves it can fail."""
    _findings, out = _convert_agents(tmp_path)
    corrupt = out.replace('[agent."ANTHROPIC-OPUS-4.8"]', "[agent.ANTHROPIC-OPUS-4.8]")
    assert corrupt != out
    tomllib.loads(corrupt)  # still parses — that is the whole hazard
    findings = mc.raw_id_findings("agents.csv", "agent", AGENTS_CSV, corrupt)
    assert findings and "ANTHROPIC-OPUS-4.8" in findings[0]


def test_comments_survive_byte_for_byte_and_in_place(tmp_path):
    _findings, out = _convert_agents(tmp_path)
    lines = out.split("\n")
    for raw in (
        "# a prose line, with commas, that DictReader would read as a nine-cell row",
        "# tag-rank: ga>preview>beta>exp",
        "# a comment BETWEEN rows, which must stay between them",
    ):
        assert raw in lines, raw
    # IN PLACE: the between-rows comment stays between them, so prose that
    # documents a row keeps pointing at the row it documents.
    assert lines.index(
        "# a comment BETWEEN rows, which must stay between them"
    ) > lines.index('[agent."ANTHROPIC-OPUS-4.8"]')
    assert lines.index("# a comment BETWEEN rows, which must stay between them") < (
        lines.index('[agent."OPENAI-GPT-5.2"]')
    )


def test_the_comment_leg_catches_a_dropped_comment(tmp_path):
    """The `# tag-rank:` line is EXECUTABLE — `agent_route.load_tag_rank` parses
    it — so a converter that silently dropped comments would reset the maturity
    vocabulary that resolves a version-less enable-list token. Planted."""
    _findings, out = _convert_agents(tmp_path)
    _h, _r, comments, _f = mc.read_csv_records(AGENTS_CSV, "Id")
    assert mc.raw_comment_findings("agents.csv", comments, out) == []
    corrupt = out.replace("# tag-rank: ga>preview>beta>exp\n", "")
    findings = mc.raw_comment_findings("agents.csv", comments, corrupt)
    assert findings and "tag-rank" in findings[0]


def test_a_comment_is_never_read_as_a_row(tmp_path):
    """`csv.DictReader` splits the prose line on its commas and hands back a row
    whose `Id` is the first clause — which is how a comment becomes a model the
    router might try to launch. The record split refuses that."""
    _h, rows, comments, _f = mc.read_csv_records(AGENTS_CSV, "Id")
    assert [r["Id"] for r in rows] == ["ANTHROPIC-OPUS-4.8", "OPENAI-GPT-5.2"]
    assert len(comments) == 3


def test_a_long_open_items_cell_round_trips_cell_for_cell(tmp_path):
    """The loudest case in the repo: open-items holds a 3,126-character cell.
    A multi-line TOML string is what makes it representable at all."""
    long_cell = "· ".join(
        "option {} with its FOR and AGAINST".format(i) for i in range(90)
    )
    assert len(long_cell) > 3000
    src = tmp_path / "docs" / "requirements" / "open-items.csv"
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text(
        'OI-ID,Title,Status,Options,WI-Refs\nOI-1,t,pending,"{}","WI-1;WI-2"\n'.format(
            long_cell
        ),
        encoding="utf-8",
        newline="",
    )
    findings, _written = mc.convert(tmp_path, write=True)
    assert findings == [], findings
    out = (tmp_path / "docs" / "requirements" / "open-items.toml").read_text(
        encoding="utf-8"
    )
    row = tomllib.loads(out)["open_item"]["OI-1"]
    assert row["options"] == long_cell  # byte-exact, not merely "close"
    assert row["wi_refs"] == ["WI-1", "WI-2"]  # a ref list is a typed array


def test_an_embedded_newline_survives_the_off_spine_branch(tmp_path):
    """CSV *can* hold a newline inside a quoted cell, and the record splitter
    recovers raw lines through `csv.reader.line_num` precisely so a `#` inside
    one is not mistaken for a comment (which would cut the row in half)."""
    src = tmp_path / "docs" / "requirements" / "open-items.csv"
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text(
        "OI-ID,Title,Status,Decision\n"
        'OI-1,t,pending,"first line\n# not a comment\nthird line"\n',
        encoding="utf-8",
        newline="",
    )
    findings, _written = mc.convert(tmp_path, write=True)
    assert findings == [], findings
    out = (tmp_path / "docs" / "requirements" / "open-items.toml").read_text(
        encoding="utf-8"
    )
    assert (
        tomllib.loads(out)["open_item"]["OI-1"]["decision"]
        == "first line\n# not a comment\nthird line"
    )


def test_a_cell_past_the_header_is_a_finding_not_a_silent_truncation(tmp_path):
    """`zip(header, record)` drops a trailing cell without a word. The shape
    check exists because a stray comma inside an unquoted cell is content, and
    content is not this conversion's to lose."""
    _h, _r, _c, findings = mc.read_csv_records(
        "OI-ID,Title\nOI-1,t,an extra cell nobody declared\n", "OI-ID"
    )
    assert findings and "past the" in findings[0]


def test_the_meta_repos_own_off_spine_registries_are_already_converted():
    """Post-cutover this is the IDEMPOTENCE proof: the `.csv` sources are gone,
    so `convert` skips them and reports nothing — the same shape that lets an
    adopter run the tool twice."""
    findings, written = mc.convert(ROOT, write=False)
    assert findings == [], findings[:5]
    for rel in ("docs/requirements/open-items.csv", "docs/agents.csv"):
        assert not (ROOT / rel).exists(), rel
