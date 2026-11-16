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


RETAIN = """[adjudicator]
context_reset_pct = 55
# first sittings too: "first-approval" stays in a comment
retain_for = [
    "disposition", "amendment", "first-approval",  # "first-approval" was its name
    'first-approval', "done-when",
]
keepwarm_minutes = 0

[reviewer]
retain_for = ["first-approval"]
"""


def test_the_adjudicators_retained_brief_kinds_are_respelled_in_place(tmp_path):
    """Implements: TC-427"""
    path = _write(tmp_path, "docs/process.toml", RETAIN.replace("\n", "\r\n"))
    assert _run(tmp_path) == 0
    expected = RETAIN.replace(
        '"amendment", "first-approval",  #', '"amendment", "first-acceptance",  #'
    ).replace("    'first-approval', ", "    'first-acceptance', ")
    # A comment keeps its words, and a key of the same name in another table
    # is that table's own.
    assert '# first sittings too: "first-approval" stays in a comment' in expected
    assert '# "first-approval" was its name' in expected
    assert expected.endswith('[reviewer]\nretain_for = ["first-approval"]\n')
    assert path.read_bytes() == expected.replace("\n", "\r\n").encode("utf-8")
    retain = tomllib.loads(expected)["adjudicator"]["retain_for"]
    assert retain.count("first-acceptance") == 2 and "first-approval" not in retain
    assert _run(tmp_path, "--check") == 0
    one_line = '[adjudicator]\nretain_for = ["first-approval", "combined"]\n'
    path = _write(tmp_path, "docs/process.toml", one_line)
    assert _run(tmp_path) == 0
    assert path.read_bytes() == one_line.replace("approval", "acceptance").encode()


@pytest.mark.parametrize(
    "text",
    (
        'attestation = { human_approval_through = "DevStg-Reqs" }\n',
        'attestation.human_approval_through = "DevStg-Reqs"\n',
        '[policies]\nnote = """\n[attestation]\n"""\n\n[attestation]\nfinal_review = "off"\n',
        'policies = { push = "human" }\n',
        '[policies]\npush = """human"""\n',
        'adjudicator = { retain_for = ["first-approval"] }\n',
    ),
    ids=(
        "inline-table",
        "dotted-key",
        "look-alike-header-in-a-string",
        "push-in-an-inline-table",
        "push-in-a-multi-line-string",
        "retained-kind-in-an-inline-table",
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


# --- delegated-decisions records and the scratchpad -----------------------------

DECISIONS = """# A delegated run's record.
high_risk = ["D-002"]
owner = "not an entry's key"

[decision.D-001]
decided = "Kept the parser."
review = "Confirmed in session; owner = confirmed in prose stays."
owner = "confirmed"  # in session

[decision.D-002]
decided = 'Split the module.'
review = "Do it the other way."
owner = "overruled"

[decision.D-003]
decided = "Not yet seen."
review = ""
"""


def test_a_decisions_records_verdict_key_is_renamed_in_each_entry(tmp_path):
    """Implements: TC-427"""
    crlf = DECISIONS.replace("\n", "\r\n")
    path = _write(tmp_path, "docs/decisions/wi-1.toml", crlf)
    assert _run(tmp_path) == 0
    expected = DECISIONS.replace('\nowner = "confirmed"', '\noperator = "confirmed"')
    expected = expected.replace('\nowner = "overruled"', '\noperator = "overruled"')
    # The same key outside an entry, and the word in prose, stay as written.
    assert 'owner = "not an entry\'s key"' in expected
    assert "owner = confirmed in prose stays" in expected
    assert path.read_bytes() == expected.replace("\n", "\r\n").encode("utf-8")
    entries = tomllib.loads(expected)["decision"]
    verdicts = [entries[d].get("operator") for d in ("D-001", "D-002", "D-003")]
    assert verdicts == ["confirmed", "overruled", None]
    assert _run(tmp_path, "--check") == 0


@pytest.mark.parametrize(
    "text",
    (
        '[decision.D-001]\nowner = "confirmed"\noperator = "overruled"\n',
        '[decision.D-001]\nreview = """\nowner = "confirmed"\n"""\nowner = "confirmed"\n',
        'decision = { D-001 = { owner = "confirmed" } }\n',
    ),
    ids=("both-spellings", "look-alike-line-in-a-string", "inline-table"),
)
def test_a_decisions_record_the_line_edit_cannot_prove_is_named_and_left(
    tmp_path, capsys, text
):
    """Implements: TC-427"""
    path = _write(tmp_path, "docs/decisions/wi-1.toml", text)
    assert _run(tmp_path) == 1
    out = capsys.readouterr().out
    assert "decisions record NOT rewritten: docs/decisions/wi-1.toml" in out
    assert path.read_bytes() == text.encode("utf-8")


# --- work items ------------------------------------------------------------------

WORK_ITEM = """+++
id = "WI-575"
title = "bar = 'a title, not a key'"
safety_class = "spine"
bar = "DevStg-Reqs"  # pinned
+++

## Deliverable

The line bar = "DevStg-Reqs" in prose stays.

## Dispositions

```toml
title = "A successor"
bar = 'DevStg-Tests'
```

The successor's scope, with
bar = "DevStg-Impl" written as prose.

```toml
title = "A second successor"

[open_item]
bar = "a table's own key"
```

## Context

```toml
bar = "an example under another heading"
```
"""


def test_a_work_items_stage_key_is_renamed_in_its_front_matter_and_drafted_rows(
    tmp_path,
):
    """Implements: TC-427"""
    crlf = WORK_ITEM.replace("\n", "\r\n")
    live = _write(tmp_path, "docs/work/queued/WI-575-x.md", crlf)
    archived = _write(tmp_path, "docs/archive/work/complete/WI-576-y.md", WORK_ITEM)
    other = _write(tmp_path, "docs/notes/WI-577-z.md", WORK_ITEM)
    assert _run(tmp_path, "--check") == 1
    assert live.read_bytes() == crlf.encode("utf-8")
    assert _run(tmp_path) == 0
    expected = WORK_ITEM.replace(
        '\nbar = "DevStg-Reqs"  # pinned', '\nchecks_stage = "DevStg-Reqs"  # pinned'
    ).replace("\nbar = 'DevStg-Tests'", "\nchecks_stage = 'DevStg-Tests'")
    # Prose, a table's own key and a block under another heading keep the word.
    assert expected.count("\nbar = ") == 3
    assert live.read_bytes() == expected.replace("\n", "\r\n").encode("utf-8")
    assert archived.read_text(encoding="utf-8") == expected
    assert other.read_text(encoding="utf-8") == WORK_ITEM
    assert _run(tmp_path, "--check") == 0


@pytest.mark.parametrize(
    "text",
    (
        '+++\nid = "WI-1"\nbar = "DevStg-Reqs"\nchecks_stage = "DevStg-Tests"\n+++\n',
        '+++\nid = "WI-1"\nnote = """\nbar = "x"\n"""\nbar = "DevStg-Reqs"\n+++\n',
        '+++\nid = "WI-1"\n+++\n\n## Dispositions\n\n```toml\nbar = \n```\n',
    ),
    ids=(
        "both-spellings",
        "look-alike-line-in-a-string",
        "a-block-that-does-not-parse",
    ),
)
def test_a_work_item_the_line_edit_cannot_prove_is_named_and_left(
    tmp_path, capsys, text
):
    """Implements: TC-427"""
    path = _write(tmp_path, "docs/work/queued/WI-1-x.md", text)
    assert _run(tmp_path) == 1
    out = capsys.readouterr().out
    assert "work item NOT rewritten: docs/work/queued/WI-1-x.md" in out, out
    assert path.read_bytes() == text.encode("utf-8")


def test_a_work_item_that_is_not_utf8_is_named_and_left(tmp_path, capsys):
    """Implements: TC-427"""
    raw = '+++\nid = "WI-1"\ntitle = "caf\xe9"\nbar = "DevStg-Reqs"\n+++\n'.encode(
        "latin-1"
    )
    path = tmp_path / "docs/archive/work/complete/WI-1-x.md"
    path.parent.mkdir(parents=True)
    path.write_bytes(raw)
    assert _run(tmp_path) == 1
    out = capsys.readouterr().out
    assert "docs/archive/work/complete/WI-1-x.md: not UTF-8; left untouched" in out
    assert path.read_bytes() == raw


def test_the_scratchpad_is_renamed_to_its_current_name_with_every_byte_kept(
    tmp_path,
):
    """Implements: TC-427"""
    notes = "# notes\r\nowner: me \u2014 half-formed\r\n".encode("utf-8")
    old, new = (tmp_path / name for name in migrate.SCRATCHPAD_NAMES)
    old.write_bytes(notes)
    assert _run(tmp_path, "--check") == 1
    assert old.read_bytes() == notes and not new.exists()
    assert _run(tmp_path) == 0
    assert not old.exists() and new.read_bytes() == notes
    assert _run(tmp_path, "--check") == 0


def test_a_scratchpad_under_both_names_is_named_and_neither_is_touched(
    tmp_path, capsys
):
    """Implements: TC-427"""
    old = _write(tmp_path, "OWNER_SCRATCHPAD.md", "earlier\n")
    new = _write(tmp_path, "OPERATOR_SCRATCHPAD.md", "current\n")
    assert _run(tmp_path) == 1
    out = capsys.readouterr().out
    assert "OPERATOR_SCRATCHPAD.md exists too; merge the two by hand" in out
    assert old.read_bytes() == b"earlier\n" and new.read_bytes() == b"current\n"


# --- the acceptance record's copies, and the run as a whole ---------------------


@pytest.mark.parametrize("record", migrate.RECORD_DIRS)
def test_the_acceptance_records_copy_of_a_registry_moves_with_it(tmp_path, record):
    """Implements: TC-427"""
    live = _write(tmp_path, "docs/requirements/system-requirements.toml", SR_TOML)
    _write(tmp_path, record + "/docs/requirements/system-requirements.toml", SR_TOML)
    assert _run(tmp_path) == 0
    copy = (
        tmp_path / migrate.RECORD_DIRS[1] / "docs/requirements/system-requirements.toml"
    )
    assert copy.read_bytes() == live.read_bytes() != SR_TOML.encode("utf-8")
    assert not (tmp_path / migrate.RECORD_DIRS[0]).exists()


STATUS_TOML = """[requirement.SR-001]
title = "Approved by the operator, in prose"
status = "Approved"

[requirement.SR-002]
status = 'approved'  # read case-folded
note = "Approved"

[requirement.SR-003]
status = "Drafted"
"""

STATUS_CSV = (
    "SR-ID,Title,Status\r\n"
    'SR-001,"Approved, in prose",Approved\r\n'
    "SR-002,Approved,Drafted\r\n"
)


def test_a_rows_earlier_status_is_respelled_in_both_carriers(tmp_path):
    """Implements: TC-427"""
    toml = _write(tmp_path, "docs/requirements/system-requirements.toml", STATUS_TOML)
    csv_ = _write(tmp_path, "docs/test/test-cases.csv", STATUS_CSV)
    assert _run(tmp_path) == 0
    # Only the status cell moves: the word in a title or another key stays.
    assert toml.read_bytes() == STATUS_TOML.replace(
        'status = "Approved"', 'status = "Accepted"'
    ).replace("status = 'approved'", "status = 'accepted'").encode("utf-8")
    assert csv_.read_bytes() == STATUS_CSV.replace(
        'in prose",Approved', 'in prose",Accepted'
    ).encode("utf-8")


LEDGER = """# APPROVAL ACTS, appended by `intake.py snapshot`. Do not edit.

[[act]]
seq = 1
date = "2026-09-27"
approved = ["SR-001"]
reattested = []

[[act]]
seq = 2
date = "2026-09-28"
approved = []
reattested = ["SR-001"]  # re-anchored
verdict = "docs/reviews/wi-1/001-ADJUDICATE-a.md"
"""

LIVE_SR = """[requirement.SR-001]
requirement = "The system shall add, now in other words."
status = "Approved"

[requirement.SR-002]
requirement = "A draft."
status = "Drafted"
"""

COPY_SR = """[requirement.SR-001]
requirement = "The system shall add."
status = "Approved"

[requirement.SR-002]
requirement = "An older draft."
status = "Drafted"

[requirement.SR-009]
requirement = "Retired since."
status = "Approved"
"""


def _record(root, home=None):
    """A repository with an acceptance record under `home` (the earlier name
    by default): its README, its ledger and a copy of one registry."""
    home = home or migrate.RECORD_DIRS[0]
    live = _write(root, "docs/requirements/system-requirements.toml", LIVE_SR)
    _write(root, home + "/README.md", "# `last_approved` — the record\n")
    _write(root, home + "/acts.toml", LEDGER)
    _write(root, home + "/docs/requirements/system-requirements.toml", COPY_SR)
    return live


def test_the_acceptance_record_moves_rekeys_and_absorbs_naming_each_cell(
    tmp_path, capsys
):
    """Implements: TC-427"""
    live = _record(tmp_path)
    old, new = (tmp_path / d for d in migrate.RECORD_DIRS)
    assert _run(tmp_path, "--check") == 1
    assert old.is_dir() and not new.exists(), "--check wrote"
    capsys.readouterr()
    assert _run(tmp_path) == 0
    out = capsys.readouterr().out
    assert not old.exists() and new.is_dir()
    # The README keeps its words; the ledger's keys move and nothing else.
    assert (
        (new / "README.md").read_text(encoding="utf-8").startswith("# `last_approved`")
    )
    ledger = (new / "acts.toml").read_text(encoding="utf-8")
    assert ledger == LEDGER.replace("\napproved = ", "\naccepted = ").replace(
        "\nreattested = ", "\nreaccepted = "
    )
    acts = tomllib.loads(ledger)["act"]
    assert [sorted(a) for a in acts][0] == ["accepted", "date", "reaccepted", "seq"]
    # The copy equals the live registry, status respelled in both.
    copy = new / "docs/requirements/system-requirements.toml"
    assert copy.read_bytes() == live.read_bytes()
    assert 'status = "Accepted"' in live.read_text(encoding="utf-8")
    # Every accepted cell it absorbed is named; a draft's moved text is not.
    rel = "docs/requirements/system-requirements.toml"
    assert "{} absorbs SR-001 requirement".format(rel) in out, out
    assert "{} absorbs SR-009 (the whole row)".format(rel) in out, out
    assert "SR-002" not in out, out
    assert _run(tmp_path, "--check") == 0


def test_a_record_under_both_names_is_named_and_neither_is_touched(tmp_path, capsys):
    """Implements: TC-427"""
    _record(tmp_path)
    _write(tmp_path, migrate.RECORD_DIRS[1] + "/acts.toml", LEDGER)
    assert _run(tmp_path) == 1
    assert "merge the two by hand" in capsys.readouterr().out
    for home in migrate.RECORD_DIRS:
        assert (tmp_path / home / "acts.toml").read_text(encoding="utf-8") == LEDGER


def test_a_ledger_the_line_edit_cannot_prove_leaves_the_record_untouched(
    tmp_path, capsys
):
    """Implements: TC-427"""
    decoy = LEDGER + 'note = """\napproved = []\n"""\n'
    _record(tmp_path)
    ledger = _write(tmp_path, migrate.RECORD_DIRS[0] + "/acts.toml", decoy)
    assert _run(tmp_path) == 1
    assert "the record is left untouched" in capsys.readouterr().out
    assert ledger.read_text(encoding="utf-8") == decoy
    assert not (tmp_path / migrate.RECORD_DIRS[1]).exists()


# A page linking into the record by its earlier directory, inline and by a
# reference definition, beside the name in a label, in prose, in a code span
# and inside a longer path segment, none of which is a link target.
LINKED = (
    "See [the ledger](../archive/last_approved/acts.toml) and [the stamp][s].\n"
    "\n"
    "[s]: docs/archive/last_approved/README.md#refreshes\n"
    "[last_approved](notes/last_approved_count.md) names `last_approved/` and\n"
    "the last_approved folder in prose.\n"
)


def test_links_into_the_record_follow_it_and_every_other_word_stays(tmp_path, capsys):
    """Implements: TC-427"""
    page = _write(tmp_path, "docs/reviews/old.md", LINKED.replace("\n", "\r\n"))
    hidden = _write(tmp_path, ".claude/notes.md", LINKED)
    vendored = _write(tmp_path, "node_modules/pkg/README.md", LINKED)
    assert _run(tmp_path) == 0
    assert "docs/reviews/old.md: 2 link(s)" in capsys.readouterr().out
    expected = LINKED.replace(
        "../archive/last_approved/acts", "../archive/last_accepted/acts"
    ).replace("docs/archive/last_approved/README", "docs/archive/last_accepted/README")
    assert page.read_bytes() == expected.replace("\n", "\r\n").encode("utf-8")
    assert hidden.read_text(encoding="utf-8") == LINKED
    assert vendored.read_text(encoding="utf-8") == LINKED


def test_links_owed_are_reported_under_check_and_a_page_not_utf8_is_named(
    tmp_path, capsys
):
    """Implements: TC-427"""
    page = _write(tmp_path, "README.md", LINKED)
    latin = tmp_path / "docs/latin.md"
    latin.parent.mkdir(parents=True)
    latin.write_bytes("caf\xe9 [x](last_approved/acts.toml)\n".encode("latin-1"))
    assert _run(tmp_path, "--check") == 1
    out = capsys.readouterr().out
    assert "acceptance-record link owes the rewrite: README.md: 2 link(s)" in out
    assert "acceptance-record link NOT rewritten: docs/latin.md: not UTF-8" in out
    assert page.read_text(encoding="utf-8") == LINKED
    assert _run(tmp_path) == 1
    capsys.readouterr()
    latin.unlink()
    assert _run(tmp_path, "--check") == 0
    assert "nothing stored in an earlier spelling" in capsys.readouterr().out


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
