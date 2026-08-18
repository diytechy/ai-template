"""The spine CARRIER's own contract (repo-lock D-5/D-6, SR-147).

WHY THIS MODULE EXISTS. The carrier's behaviours were tested wherever they
happened to be consumed — the vocabulary in `test_rule_sync`, the baseline reads
in `test_trajectory_staged`, the conversion in `test_migrate_carrier` — and the
adversarial review of the cutover found the predictable consequence: the TOML
arm's own edges had no home and so had no tests. Duplicate table ids were
covered; an explicitly empty value and a multi-line string were not, and most
functional fixtures deliberately run the LEGACY carrier
(`conftest.use_legacy_spine_carrier`), which left TOML behaviour leaning on this
repo's live registries — a moving target, and not a test.

So the properties the carrier CLAIMS are asserted here, against text, with no
scaffold: the claims are about parsing, and a fixture repo would only obscure
that.
"""

import tomllib

import pytest
from conftest import load_script

sc = load_script("spine_carrier")

SR = "SR-ID"


def _write(tmp_path, text, name="system-requirements.toml"):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


# --- what the carrier turned from a check into a property ---------------------


def test_a_duplicate_id_is_a_PARSE_error_not_a_check(tmp_path):
    # The id is the table key, and TOML forbids declaring one twice. This is the
    # first of the three rules the carrier absorbed; it must fail at the parse,
    # not somewhere downstream that might be skipped.
    path = _write(
        tmp_path,
        '[requirement.SR-001]\ntitle = "one"\n[requirement.SR-001]\ntitle = "two"\n',
    )
    with pytest.raises(SystemExit) as excinfo:
        sc.load(path, SR)
    assert "does not parse" in str(excinfo.value)


def test_a_ref_list_is_an_ARRAY_so_prose_cannot_become_an_orphan(tmp_path):
    # The second rule: `SN-001 and SN-002` used to yield an orphan called `and`.
    path = _write(tmp_path, '[requirement.SR-001]\nsn_refs = ["SN-001", "SN-002"]\n')
    (row,) = sc.load(path, SR)
    assert row["SN-Refs"] == "SN-001;SN-002"


def test_an_ABSENT_key_is_absent_and_reads_as_empty_downstream(tmp_path):
    # The third rule, and the one every consumer leans on: absent and empty
    # compare equal where it matters (`.get(col) or ""`) and stay
    # distinguishable where it does not (a key-set read).
    path = _write(tmp_path, '[requirement.SR-001]\ntitle = "T"\n')
    (row,) = sc.load(path, SR)
    assert "Rationale" not in row
    assert (row.get("Rationale") or "") == ""


# --- the edges the review found untested --------------------------------------


def test_an_EXPLICIT_empty_string_is_REFUSED_not_quietly_accepted(tmp_path):
    """`key = ""` is the third state the carrier exists to abolish.

    "An empty cell is an absent key" was true of machine-written files only: the
    converter omits an empty cell, but nothing stopped a HAND-authored
    `title = ""`, and TOML parses it happily. The row then came back with the
    key PRESENT and empty — so `.get(col) or ""` reads it as empty while a
    key-set check reads it as declared, and the two disagree about one cell.

    FAIL CLOSED: refused, naming the row and the key, rather than normalised
    away. Normalising would leave the file and the loaded row disagreeing about
    what the author wrote. (Owner ruling owed; this fork was never ruled.)
    """
    path = _write(tmp_path, '[requirement.SR-001]\ntitle = ""\nstatus = "Approved"\n')
    with pytest.raises(SystemExit) as excinfo:
        sc.load(path, SR)
    message = str(excinfo.value)
    assert "SR-001" in message and "Title" in message and "EMPTY STRING" in message


def test_the_empty_refusal_names_EVERY_offending_cell(tmp_path):
    # One finding per cell, so a registry with several is fixed in one pass
    # rather than one refusal at a time.
    path = _write(
        tmp_path,
        '[requirement.SR-001]\ntitle = ""\nrationale = ""\n'
        '[requirement.SR-002]\narea = ""\n',
    )
    rows = sc.rows_seq_from_text(path.read_text(encoding="utf-8"), SR, ".toml")
    findings = sc.empty_value_findings(rows, SR)
    assert len(findings) == 3, findings
    assert {"SR-001", "SR-002"} == {f.split()[0] for f in findings}


def test_a_BASELINE_read_stays_permissive_about_empty_strings(tmp_path):
    """History is not editable, so the strict reader must not reach it.

    `rows_from_text` is what the baseline/two-tree reads go through, and a
    revision that predates the rule cannot be fixed by anyone. Refusing there
    would red a check over a file nobody can edit — the opposite of the
    live-read case, where there IS a file to fix and a person to tell.
    """
    rows = sc.rows_from_text('[requirement.SR-001]\ntitle = ""\n', SR, ".toml")
    assert rows["SR-001"]["Title"] == ""


def test_a_MULTILINE_string_round_trips_including_its_newlines(tmp_path):
    # The prose cells are multi-line by nature; a reader that flattened or
    # truncated them would silently shorten attested text.
    body = "First line.\nSecond line, with a # hash and an = sign.\nThird."
    path = _write(
        tmp_path,
        '[requirement.SR-001]\nrequirement = """{}"""\n'.format(body),
    )
    (row,) = sc.load(path, SR)
    assert row["Requirement"] == body


def test_a_multiline_cell_may_QUOTE_registry_syntax_without_becoming_it(tmp_path):
    # The counterexample that broke intake's line rewrite, asserted on the READ
    # side too: a cell containing `status = ...` and a `[table]` line is one
    # cell, not three declarations.
    body = 'status = literal prose\n[requirement.SR-999]\nkey = "value"'
    path = _write(
        tmp_path,
        '[requirement.SR-001]\nrequirement = """{}"""\nstatus = "Modified"\n'.format(
            body
        ),
    )
    (row,) = sc.load(path, SR)
    assert row["Requirement"] == body
    assert row["Status"] == "Modified"
    assert len(tomllib.loads(path.read_text(encoding="utf-8"))["requirement"]) == 1


# --- the loader preserves the FILE, not a projection of it --------------------


def test_the_live_loader_keeps_DUPLICATE_csv_ids_for_the_integrity_check(tmp_path):
    """Under the legacy carrier a duplicate id is still a check, not a parse
    error — so the loader must hand back both rows. Keying by id collapsed them,
    which destroyed the first thing `--strict-integrity` is required to fail on
    (SR-002)."""
    path = tmp_path / "system-requirements.csv"
    path.write_text(
        "SR-ID,Title,Status\nSR-001,one,Approved\nSR-001,two,Approved\n",
        encoding="utf-8",
    )
    rows = sc.load(path, SR)
    assert [r["Title"] for r in rows] == ["one", "two"]


def test_BOTH_homes_at_once_is_refused_rather_than_resolved(tmp_path):
    _write(tmp_path, '[requirement.SR-001]\ntitle = "T"\n')
    (tmp_path / "system-requirements.csv").write_text(
        "SR-ID,Title\nSR-001,T\n", encoding="utf-8"
    )
    with pytest.raises(SystemExit) as excinfo:
        sc.load(tmp_path / "system-requirements.toml", SR)
    assert "BOTH carriers" in str(excinfo.value)


def test_resolve_does_not_mangle_a_MULTI_DOT_filename(tmp_path):
    # `Path.with_suffix` treats everything after the LAST dot as the suffix, so
    # `system-requirements.template.toml` resolved to `system-requirements.toml`
    # — a different file, silently.
    live = _write(
        tmp_path, "[requirement.SR-000]\n", "system-requirements.template.toml"
    )
    other = _write(tmp_path, "[requirement.SR-001]\n", "system-requirements.toml")
    assert sc.resolve(live) == live
    assert sc.resolve(other) == other


# --- the schema of record -----------------------------------------------------


def test_every_tier_schema_key_is_one_the_carrier_can_map():
    # SPINE_TIER_KEYS is the anchor test_dogfood_sync checks the template and the
    # live registry against; a key it states that SPINE_COLUMN cannot map would
    # be a cell the loader silently drops.
    assert sc.SPINE_TIER_KEYS  # non-vacuous
    for id_col, keys in sc.SPINE_TIER_KEYS.items():
        assert id_col in sc.SPINE_TABLE, id_col
        assert keys, id_col
        assert len(set(keys)) == len(keys), id_col
        for key in keys:
            assert key in sc.SPINE_COLUMN, (id_col, key)


# --- batch-2: the off-spine registries (repo-lock §8.1) -----------------------


def test_the_vocabulary_unions_without_redefining_a_shared_column():
    """D-3 rules that a column name means ONE thing repo-wide, which is what
    lets spine and batch-2 share a single map. `Title`, `Status`, `Tier` and
    `Notes` appear in registries on both sides; if either half redefined one,
    the union would silently take whichever half was applied second."""
    for key in set(sc.SPINE_COLUMN) & set(sc.OFFSPINE_COLUMN):
        assert sc.SPINE_COLUMN[key] == sc.OFFSPINE_COLUMN[key], key
    assert sc.REGISTRY_COLUMN == dict(sc.SPINE_COLUMN, **sc.OFFSPINE_COLUMN)
    # ...and no two keys map onto one column, which would make the inverse
    # ambiguous and the round-trip unprovable.
    assert len(set(sc.REGISTRY_COLUMN.values())) == len(sc.REGISTRY_COLUMN)


def test_an_open_items_registry_that_does_not_parse_is_absent_never_empty(tmp_path):
    """The false green this whole rule exists for: `{}` on a DECISION QUEUE
    reads as "no open items", so an unreadable registry would publish "nothing
    is waiting on the owner" and every gate would stay green."""
    p = tmp_path / "open-items.toml"
    p.write_text('[open_item.OI-1]\ntitle = "unterminated\n', encoding="utf-8")
    assert sc.rows_from_toml(p.read_text(encoding="utf-8"), "OI-ID") is None
    with pytest.raises(SystemExit) as exc:
        sc.load(p, "OI-ID")
    assert "does not parse" in str(exc.value)


def test_an_absent_registry_is_still_an_empty_list(tmp_path):
    # ...and the other side of that fork stays cheap: a repo carrying no
    # decisions renders a view rather than failing.
    assert sc.load(tmp_path / "open-items.toml", "OI-ID") == []
    assert sc.load(tmp_path / "agents.toml", "Id") == []


def test_an_unquoted_dotted_id_is_refused_rather_than_read_as_a_table(tmp_path):
    """`[agent.ANTHROPIC-OPUS-4.8]` written BARE is valid TOML declaring nested
    tables, so the file parses and the row's real id is simply gone — replaced
    by `ANTHROPIC-OPUS-4` whose one 'cell' is a sub-table. Fail-closed, for
    `empty_value_findings`' reason: the fix is a two-character edit the author
    must make, and repairing it silently would leave the file and the loaded
    registry disagreeing about what it says."""
    p = tmp_path / "agents.toml"
    p.write_text('[agent.ANTHROPIC-OPUS-4.8]\nfamily = "ANTHROPIC"\n', encoding="utf-8")
    findings = sc.nested_table_findings(p.read_text(encoding="utf-8"), "Id")
    assert findings and "must be QUOTED" in findings[0]
    with pytest.raises(SystemExit) as exc:
        sc.load(p, "Id")
    assert "QUOTED" in str(exc.value)


def test_the_quoted_form_loads_clean(tmp_path):
    # The guard must not fire on the shape the converter actually writes.
    p = tmp_path / "agents.toml"
    p.write_text(
        '[agent."ANTHROPIC-OPUS-4.8"]\nfamily = "ANTHROPIC"\ntier = "strong"\n',
        encoding="utf-8",
    )
    assert sc.nested_table_findings(p.read_text(encoding="utf-8"), "Id") == []
    rows = sc.load(p, "Id")
    assert [r["Id"] for r in rows] == ["ANTHROPIC-OPUS-4.8"]
    assert rows[0]["Family"] == "ANTHROPIC"  # the key -> column vocabulary


def test_both_carriers_at_once_is_refused_for_the_new_registries(tmp_path):
    # The dual-home refusal is the rule that makes a half-finished migration
    # visible; it must cover the registries the migration just moved.
    (tmp_path / "agents.toml").write_text("", encoding="utf-8")
    (tmp_path / "agents.csv").write_text("Id\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        sc.resolve(tmp_path / "agents.toml")
    assert "BOTH carriers" in str(exc.value)


# --- drafted-ness: the field the whole SN tier's maturity rides on ------------


def test_draft_need_ids_reads_STATUS_and_nothing_else():
    """The coverage hole the status unification found, closed.

    `draft_need_ids` / `is_draft_need` own the SN tier's maturity — the derived
    gate drops to DevBar-Below while any need is drafted, so this predicate is
    the whole rung — and this module had ZERO direct tests of it. It was proved
    only sideways, through `test_check_docs` and `test_rule_sync`, which is how
    the field managed to be spelled three different ways
    (`docs/plans/2026-08-16-registry-status-unification.md` §4.4).
    """
    needs = [
        {"id": "SN-001", "status": "Drafted"},
        {"id": "SN-002", "status": "Approved"},
        {"id": "SN-003", "status": "Modified"},
    ]
    assert sc.draft_need_ids(needs) == {"SN-001"}

    # `Modified` is amended-and-unsigned, NOT drafted: an amended need keeps the
    # maturity it was signed at until the sitting re-signs it. Reading it as a
    # draft would drop the derived gate on every amendment.
    assert sc.is_draft_need({"id": "SN-003", "status": "Modified"}) is False

    # The RETIRED spelling must not answer. This is the mutation the migration
    # turns on: while the fallback stood, `kind = "draft"` returned True here,
    # so this line fails against the pre-step-4 selector and against any future
    # re-introduction of a second field for one axis.
    assert sc.is_draft_need({"id": "SN-004", "kind": "draft"}) is False

    # An absent cell is not a maturity. A reader must not invent one — the
    # missing key is a SCHEMA finding upstream, not a draft row here.
    assert sc.draft_need_ids([{"id": "SN-005"}]) == set()

    # The word is closed and case-sensitive: the lowercase legacy spelling is
    # not a synonym, it is an unrecognized value.
    assert sc.is_draft_need({"id": "SN-006", "status": "drafted"}) is False


def test_legacy_markdown_draftness_survives_the_field_it_moved_to():
    """Section-as-state still answers, through `status` now.

    The legacy carrier had no maturity FIELD; it had a heading. The reader
    translates that at the boundary, and this pins the translation — because the
    failure mode when it is missing is silent and upward: every drafted need in
    an un-migrated repo reads as ratified and the derived gate RISES.
    """
    text = (
        "## Core needs\n\n| SN-ID | Need | Priority | Acceptance |\n|---|---|---|---|\n"
        "| SN-001 | ratified | M | x |\n\n"
        "## Draft needs (unratified)\n\n"
        "| SN-ID | Need | Priority | Acceptance |\n|---|---|---|---|\n"
        "| SN-050 | not yet | M | x |\n"
    )
    needs = sc.needs_from_markdown(text)
    assert {n["id"]: n["status"] for n in needs} == {
        "SN-001": "Approved",
        "SN-050": "Drafted",
    }
    assert sc.draft_need_ids(needs) == {"SN-050"}
    # ...and the whole-text entry point agrees, over both carriers.
    assert sc.draft_ids_from_text(text) == {"SN-050"}
    assert sc.draft_ids_from_text(
        '[need.SN-050]\nstatus = "Drafted"\nneed = "n"\n'
    ) == {"SN-050"}
