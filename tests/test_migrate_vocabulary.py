"""The vocabulary migrator rewrites stored values, and only those.

The kit's vocabulary was unified on 2026-11-11 and the core scripts read the
current spellings only (the operator's ruling: no compatibility readers). A
repository that stores an earlier spelling runs `migrate_vocabulary.py` once at
its re-sync. These tests hold what that run may touch: a whole value in a known
place, with every other byte kept, checked by parsing the file again.
"""

import tomllib

import pytest

from conftest import SCRIPTS, load_script, run_py

migrate = load_script("migrate_vocabulary")

BINDING = "brief = amendment\nkinds = amendment\noutcome = {}\nrows = SR-001=sha256:0123456789abcdef\n"

SR_TOML = '''# System requirements.
[requirement.SR-001]
title = "Adds two integers"
requirement = """The system shall add.
verification = "Attest" is how an earlier kit spelled the method."""
verification = "Test"  # mechanized
status = "Drafted"

[requirement.SR-002]
title = 'The theme fits the mood'
verification = "Attest"
status = "Drafted"
'''

SR_CSV = (
    "SR-ID,Title,Requirement,Verification,Status\r\n"
    'SR-001,Adds,"The system shall add, and say ""Attest"" nowhere.",Test,Drafted\r\n'
    'SR-002,"Theme, mood","Judged by the lead.\r\nAttest stays prose here.",Attest,Drafted\r\n'
)


def _write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    return path


def _run(root, *flags):
    return migrate.main(["--root", str(root), *flags])


# --- verdict bindings ----------------------------------------------------------


def test_a_binding_whose_outcome_reads_accepted_is_rewritten_to_recorded(tmp_path):
    """Implements: TC-427"""
    old = _write(
        tmp_path,
        "docs/reviews/wi-1/001-ADJUDICATE-a.md.requested",
        BINDING.format("accepted"),
    )
    failed = _write(
        tmp_path,
        "docs/reviews/wi-1/002-ADJUDICATE-b.md.requested",
        BINDING.format("failed"),
    )
    assert _run(tmp_path) == 0
    assert old.read_text(encoding="utf-8") == BINDING.format("recorded")
    assert failed.read_text(encoding="utf-8") == BINDING.format("failed")


def test_a_binding_keeps_its_line_endings_and_every_other_line(tmp_path):
    """Implements: TC-427"""
    crlf = BINDING.format("accepted").replace("\n", "\r\n")
    path = _write(tmp_path, "docs/reviews/wi-1/001-ADJUDICATE-a.md.requested", crlf)
    assert _run(tmp_path) == 0
    assert path.read_bytes() == crlf.replace("accepted", "recorded").encode("utf-8")


def test_only_the_outcome_line_of_a_binding_moves(tmp_path):
    """Implements: TC-427"""
    text = "brief = accepted\nkinds = accepted\noutcome = accepted\n"
    path = _write(tmp_path, "docs/reviews/x.md.requested", text)
    assert _run(tmp_path) == 0
    assert (
        path.read_text(encoding="utf-8")
        == "brief = accepted\nkinds = accepted\noutcome = recorded\n"
    )


# --- registries, the TOML carrier ----------------------------------------------


def test_a_toml_registry_gets_the_field_renamed_and_the_method_respelled(tmp_path):
    """Implements: TC-427"""
    path = _write(tmp_path, "docs/requirements/system-requirements.toml", SR_TOML)
    assert _run(tmp_path) == 0
    rows = tomllib.loads(path.read_text(encoding="utf-8"))["requirement"]
    assert rows["SR-001"]["verification_method"] == "Test"
    assert rows["SR-002"]["verification_method"] == "Vouch"
    assert all("verification" not in row for row in rows.values())


def test_a_toml_registry_keeps_every_byte_outside_the_values_it_moves(tmp_path):
    """Implements: TC-427"""
    path = _write(
        tmp_path,
        "docs/requirements/system-requirements.toml",
        SR_TOML.replace("\n", "\r\n"),
    )
    assert _run(tmp_path) == 0
    expected = (
        SR_TOML.replace('\nverification = "Test"', '\nverification_method = "Test"')
        .replace(
            '\nverification = "Attest"\nstatus',
            '\nverification_method = "Vouch"\nstatus',
        )
        .replace("\n", "\r\n")
    )
    # The look-alike line inside SR-001's multi-line requirement is prose, and stays.
    assert 'verification = "Attest" is how an earlier kit' in expected
    assert path.read_bytes() == expected.encode("utf-8")


def test_a_look_alike_line_inside_a_cell_is_never_rewritten(tmp_path):
    """Implements: TC-427"""
    # A whole line of a multi-line cell that reads exactly as a field does.
    text = '[requirement.SR-001]\nrationale = """Earlier kits wrote\nverification = "Attest"\nfor this."""\nverification = "Attest"\n'
    path = _write(tmp_path, "docs/requirements/system-requirements.toml", text)
    assert _run(tmp_path) == 1
    assert path.read_text(encoding="utf-8") == text


def test_an_untouchable_registry_is_named_and_fails_the_run(tmp_path, capsys):
    """Implements: TC-427"""
    both = '[requirement.SR-001]\nverification = "Test"\nverification_method = "Test"\n'
    broken = '[requirement.SR-001\nverification = "Attest"\n'
    _write(tmp_path, "docs/requirements/both.toml", both)
    _write(tmp_path, "docs/requirements/broken.toml", broken)
    assert _run(tmp_path) == 1
    out = capsys.readouterr().out
    assert "docs/requirements/both.toml: a row carries both" in out, out
    assert "docs/requirements/broken.toml: it does not parse" in out, out
    assert out.count("left untouched") == 2, out
    assert (tmp_path / "docs/requirements/both.toml").read_text(
        encoding="utf-8"
    ) == both


def test_the_method_moves_only_in_its_own_field(tmp_path):
    """Implements: TC-427"""
    text = '[requirement.SR-001]\ntitle = "Attest"\npriority = "Attest"\nverification = "Demonstration"\n'
    path = _write(tmp_path, "docs/requirements/system-requirements.toml", text)
    assert _run(tmp_path) == 0
    row = tomllib.loads(path.read_text(encoding="utf-8"))["requirement"]["SR-001"]
    assert row == {
        "title": "Attest",
        "priority": "Attest",
        "verification_method": "Demonstration",
    }


def test_a_padded_method_is_matched_as_the_readers_match_it(tmp_path):
    """Implements: TC-427"""
    text = '[requirement.SR-001]\nverification = "Attest  "\n'
    path = _write(tmp_path, "docs/requirements/system-requirements.toml", text)
    assert _run(tmp_path) == 0
    assert (
        path.read_text(encoding="utf-8")
        == '[requirement.SR-001]\nverification_method = "Vouch  "\n'
    )


# --- registries, the CSV carrier -----------------------------------------------


def test_a_csv_registry_gets_the_header_renamed_and_the_method_respelled(tmp_path):
    """Implements: TC-427"""
    path = _write(tmp_path, "docs/requirements/system-requirements.csv", SR_CSV)
    assert _run(tmp_path) == 0
    expected = SR_CSV.replace(",Verification,", ",VerificationMethod,").replace(
        ",Attest,Drafted", ",Vouch,Drafted"
    )
    # "Attest" inside two quoted prose cells, one of them spanning lines, stays.
    assert expected.count("Attest") == 2
    assert path.read_bytes() == expected.encode("utf-8")


def test_a_quoted_header_cell_and_a_byte_order_mark_are_kept(tmp_path):
    """Implements: TC-427"""
    text = '\ufeff"SR-ID","Verification"\nSR-001,Attest\n'
    path = _write(tmp_path, "docs/requirements/system-requirements.csv", text)
    assert _run(tmp_path) == 0
    assert (
        path.read_text(encoding="utf-8")
        == '\ufeff"SR-ID","VerificationMethod"\nSR-001,Vouch\n'
    )


def test_a_csv_registrys_comment_preamble_is_kept_and_the_row_after_it_renamed(
    tmp_path,
):
    """Implements: TC-427"""
    preamble = "\ufeff# Contracts: IF-001\r\n#   a declaration header\r\n\r\n"
    rows = SR_CSV + "# SR-003,not a comment,a data line,Attest,Drafted\r\n"
    path = _write(
        tmp_path, "docs/requirements/performance-budgets.csv", preamble + rows
    )
    assert _run(tmp_path) == 0
    expected = rows.replace(",Verification,", ",VerificationMethod,").replace(
        ",Attest,Drafted", ",Vouch,Drafted"
    )
    assert expected.count(",Vouch,Drafted") == 2
    assert path.read_bytes() == (preamble + expected).encode("utf-8")


# --- the policy file -----------------------------------------------------------

POLICY = """# Policy dials.
[attestation]
# The highest rung held.
human_approval_through = "DevStg-Boundary"  # held
final_review = "always"

[policies]
review_rounds = 1
human_approval_through = "not a dial in this table"
"""


def test_the_policy_files_table_and_dial_key_are_renamed_in_place(tmp_path):
    """Implements: TC-427"""
    path = _write(tmp_path, "docs/process.toml", POLICY.replace("\n", "\r\n"))
    assert _run(tmp_path) == 0
    expected = POLICY.replace("[attestation]", "[authority]").replace(
        '\nhuman_approval_through = "DevStg-Boundary"',
        '\noperator_accepts_through = "DevStg-Boundary"',
    )
    # The same key name under another table is that table's own, and stays.
    assert 'human_approval_through = "not a dial in this table"' in expected
    assert path.read_bytes() == expected.replace("\n", "\r\n").encode("utf-8")
    dial = tomllib.loads(expected)["authority"]["operator_accepts_through"]
    assert dial == "DevStg-Boundary"


def test_a_policy_file_declaring_both_spellings_is_named_and_left(tmp_path, capsys):
    """Implements: TC-427"""
    tables = (
        '[attestation]\nfinal_review = "off"\n\n[authority]\nfinal_review = "always"\n'
    )
    path = _write(tmp_path, "docs/process.toml", tables)
    assert _run(tmp_path) == 1
    out = capsys.readouterr().out
    assert (
        "docs/process.toml: it declares both `[attestation]` and `[authority]`" in out
    )
    assert path.read_bytes() == tables.encode("utf-8")
    keys = (
        '[authority]\nhuman_approval_through = "DevStg-Reqs"\n'
        'operator_accepts_through = "DevStg-Reqs"\n'
    )
    path = _write(tmp_path, "docs/process.toml", keys)
    assert _run(tmp_path) == 1
    out = capsys.readouterr().out
    assert "carries both `human_approval_through` and `operator_accepts_through`" in out
    assert path.read_bytes() == keys.encode("utf-8")


PUSH = """# Who may publish.
[policies]
review_rounds = 1
push = "human"  # the default

[checks]
push = "human"
"""


def test_the_push_authoritys_earlier_default_is_respelled_in_place(tmp_path):
    """Implements: TC-427"""
    path = _write(tmp_path, "docs/process.toml", PUSH.replace("\n", "\r\n"))
    assert _run(tmp_path) == 0
    expected = PUSH.replace(
        'push = "human"  # the default', 'push = "operator"  # the default'
    )
    # A key of the same name in another table is that table's own, and stays.
    assert expected.endswith('[checks]\npush = "human"\n')
    assert path.read_bytes() == expected.replace("\n", "\r\n").encode("utf-8")
    assert tomllib.loads(expected)["policies"]["push"] == "operator"
    for other in ("agent", "agent-iteration", "operator"):
        text = '[policies]\npush = "{}"\n'.format(other)
        path = _write(tmp_path, "docs/process.toml", text)
        assert _run(tmp_path) == 0
        assert path.read_bytes() == text.encode("utf-8")


@pytest.mark.parametrize(
    "text",
    (
        'attestation = { human_approval_through = "DevStg-Reqs" }\n',
        'attestation.human_approval_through = "DevStg-Reqs"\n',
        '[policies]\nnote = """\n[attestation]\n"""\n\n[attestation]\nfinal_review = "off"\n',
        'policies = { push = "human" }\n',
        '[policies]\npush = """human"""\n',
    ),
    ids=(
        "inline-table",
        "dotted-key",
        "look-alike-header-in-a-string",
        "push-in-an-inline-table",
        "push-in-a-multi-line-string",
    ),
)
def test_a_dial_the_line_edit_cannot_reach_is_refused_not_guessed(tmp_path, text):
    """Implements: TC-427"""
    path = _write(tmp_path, "docs/process.toml", text)
    assert _run(tmp_path) == 1
    assert path.read_bytes() == text.encode("utf-8")


def test_a_policy_file_in_the_current_vocabulary_is_untouched(tmp_path):
    """Implements: TC-427"""
    text = '[authority]\noperator_accepts_through = "DevStg-Release"\n'
    path = _write(tmp_path, "docs/process.toml", text)
    assert _run(tmp_path, "--check") == 0
    assert _run(tmp_path) == 0
    assert path.read_bytes() == text.encode("utf-8")


# --- the acceptance record's copies, and the run as a whole ---------------------


@pytest.mark.parametrize("record", migrate.RECORD_DIRS)
def test_the_acceptance_records_copy_of_a_registry_moves_with_it(tmp_path, record):
    """Implements: TC-427"""
    live = _write(tmp_path, "docs/requirements/system-requirements.toml", SR_TOML)
    copy = _write(
        tmp_path, record + "/docs/requirements/system-requirements.toml", SR_TOML
    )
    assert _run(tmp_path) == 0
    assert copy.read_bytes() == live.read_bytes() != SR_TOML.encode("utf-8")


def test_a_file_that_is_not_a_registry_is_left_alone(tmp_path):
    """Implements: TC-427"""
    note = _write(
        tmp_path, "docs/notes.toml", '[requirement.SR-001]\nverification = "Attest"\n'
    )
    deep = _write(
        tmp_path,
        "docs/requirements/deeper/x.toml",
        '[requirement.SR-001]\nverification = "Attest"\n',
    )
    assert _run(tmp_path) == 0
    assert "verification_method" not in note.read_text(encoding="utf-8")
    assert "verification_method" not in deep.read_text(encoding="utf-8")


def test_check_reports_what_is_owed_and_writes_nothing_and_a_second_run_is_clean(
    tmp_path,
):
    """Implements: TC-427"""
    binding = _write(
        tmp_path, "docs/reviews/x.md.requested", BINDING.format("accepted")
    )
    registry = _write(tmp_path, "docs/requirements/system-requirements.toml", SR_TOML)
    proc = run_py([SCRIPTS / "migrate_vocabulary.py", "--check"], tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert (
        "verdict binding owes the rewrite: docs/reviews/x.md.requested" in proc.stdout
    )
    assert (
        "registry owes the rewrite: docs/requirements/system-requirements.toml"
        in proc.stdout
    )
    assert binding.read_text(encoding="utf-8") == BINDING.format("accepted")
    assert registry.read_text(encoding="utf-8") == SR_TOML
    proc = run_py([SCRIPTS / "migrate_vocabulary.py"], tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    after = (binding.read_bytes(), registry.read_bytes())
    proc = run_py([SCRIPTS / "migrate_vocabulary.py", "--check"], tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "nothing stored in an earlier spelling" in proc.stdout
    assert _run(tmp_path) == 0
    assert (binding.read_bytes(), registry.read_bytes()) == after


def test_a_repository_with_nothing_to_migrate_is_clean(tmp_path, capsys):
    """Implements: TC-427"""
    assert _run(tmp_path, "--check") == 0
    assert "nothing stored in an earlier spelling" in capsys.readouterr().out
