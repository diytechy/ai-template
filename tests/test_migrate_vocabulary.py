"""The vocabulary migrator rewrites stored values, and only those.

The kit's vocabulary was unified on 2026-11-11 and the core scripts read the
current spellings only (the operator's ruling: no compatibility readers). A
repository that stores an earlier spelling runs `migrate_vocabulary.py` once at
its re-sync. These tests hold what that run may touch: a whole value in a known
place, with every other byte kept, checked by parsing the file again.

Once the acceptance record holds a row-by-row act (an act-ledger entry
carrying `kept`), the record is judged at the row, so the migrator writes no
copy into a record in the current vocabulary and refuses the whole run while
the record still stores an earlier spelling (WI-1065). The cases that build
such a record in a real git repository, through the snapshot writer, live in
`test_migrate_vocabulary_record.py`.
"""

import ast
import pathlib
import sys
import tomllib

import pytest

from conftest import SCRIPTS, load_script, run_py

migrate = load_script("migrate_vocabulary")
record_rows = load_script("record_rows")

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


def test_the_retained_evidence_gap_kind_is_respelled_beside_the_others(tmp_path):
    """Implements: TC-427"""
    text = (
        "[adjudicator]\n"
        'retain_for = ["disposition", "red-tc", "first-approval"]  # red-tc\n'
    )
    path = _write(tmp_path, "docs/process.toml", text)
    assert _run(tmp_path) == 0
    assert path.read_text(encoding="utf-8") == (
        "[adjudicator]\n"
        'retain_for = ["disposition", "evidence-gap", "first-acceptance"]'
        "  # red-tc\n"
    )


@pytest.mark.parametrize(
    "text",
    (
        'attestation = { human_approval_through = "DevStg-Reqs" }\n',
        'attestation.human_approval_through = "DevStg-Reqs"\n',
        '[policies]\nnote = """\n[attestation]\n"""\n\n[attestation]\nfinal_review = "off"\n',
        'policies = { push = "human" }\n',
        '[policies]\npush = """human"""\n',
        'adjudicator = { retain_for = ["first-approval"] }\n',
        "authority = { operator_accepts_through = 3 }\n",
        "[authority]\noperator_accepts_through = +3\n",
        "[authority]\noperator_accepts_through = 0x3\n",
        "build = { red_rounds_max = 5 }\n",
        'authority = { human_ratification_through = "DevStg-Arch" }\n',  # check_vocab: allow
        '[authority]\nnote = """\noperator_accepts_through = 2\n"""\n'
        "operator_accepts_through = 3\n",
    ),
    ids=(
        "inline-table",
        "dotted-key",
        "look-alike-header-in-a-string",
        "push-in-an-inline-table",
        "push-in-a-multi-line-string",
        "retained-kind-in-an-inline-table",
        "ordinal-in-an-inline-table",
        "ordinal-with-a-sign",
        "ordinal-in-hexadecimal",
        "failure-cap-in-an-inline-table",
        "earliest-key-in-an-inline-table",
        "ordinal-look-alike-in-a-string",
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


# The dial under its earliest key name, holding the retired integer.
EARLIEST_KEY = "human_ratification_through"  # check_vocab: allow
DIAL = "# The dial.\n[{}]\n{} = {}  # the old ordinal\nfinal_review = 1\n"


@pytest.mark.parametrize(
    "ordinal, rung",
    (
        (0, "DevStg-Below"),
        (1, "DevStg-Boundary"),
        (2, "DevStg-Arch"),
        (3, "DevStg-LLReqs"),
        (4, "DevStg-Release"),
    ),
)
@pytest.mark.parametrize("header", ("attestation", "authority"))
def test_the_dials_earliest_key_and_retired_integer_are_respelled_in_place(
    tmp_path, header, ordinal, rung
):
    """Implements: TC-427"""
    text = DIAL.format(header, EARLIEST_KEY, ordinal)
    path = _write(tmp_path, "docs/process.toml", text.replace("\n", "\r\n"))
    assert _run(tmp_path) == 0
    expected = (
        '# The dial.\n[authority]\noperator_accepts_through = "{}"  # the old '
        "ordinal\nfinal_review = 1\n".format(rung)
    )
    assert path.read_bytes() == expected.replace("\n", "\r\n").encode("utf-8")
    # The integer moves in its own key only: another integer in the table stays.
    assert tomllib.loads(expected)["authority"]["final_review"] == 1
    assert _run(tmp_path, "--check") == 0


def test_a_dial_holding_no_retired_integer_keeps_its_value(tmp_path):
    """Implements: TC-427"""
    for value in ("true", "7", '"DevStg-Arch"'):
        text = "[authority]\noperator_accepts_through = {}\n".format(value)
        path = _write(tmp_path, "docs/process.toml", text)
        assert _run(tmp_path) == 0
        assert path.read_bytes() == text.encode("utf-8")
    text = "[authority]\noperator_accepts_through = 3\n"
    path = _write(tmp_path, "docs/process.toml", text)
    assert _run(tmp_path) == 0
    assert path.read_bytes() == text.replace("3", '"DevStg-LLReqs"').encode()


def test_the_failure_caps_earlier_key_is_renamed_in_place(tmp_path, capsys):
    """Implements: TC-427"""
    text = "[build]\nred_rounds_max = 5  # stop after five\n\n[other]\nred_rounds_max = 1\n"
    path = _write(tmp_path, "docs/process.toml", text)
    assert _run(tmp_path) == 0
    cap = "stop_lane_after_consecutive_commit_check_failures"
    expected = text.replace("[build]\nred_rounds_max", "[build]\n" + cap)
    assert path.read_bytes() == expected.encode("utf-8")
    both = "[build]\nred_rounds_max = 5\n{} = 3\n".format(cap)
    path = _write(tmp_path, "docs/process.toml", both)
    assert _run(tmp_path) == 1
    assert "carries both `red_rounds_max` and `{}`".format(cap) in (
        capsys.readouterr().out
    )
    assert path.read_bytes() == both.encode("utf-8")


def test_a_dial_under_two_earlier_keys_is_named_and_left(tmp_path, capsys):
    """Implements: TC-427"""
    text = '[authority]\nhuman_approval_through = "DevStg-Reqs"\n{} = 1\n'.format(
        EARLIEST_KEY
    )
    path = _write(tmp_path, "docs/process.toml", text)
    assert _run(tmp_path) == 1
    out = capsys.readouterr().out
    assert "carries both `human_approval_through` and `{}`".format(EARLIEST_KEY) in out
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


# --- the stack profile -------------------------------------------------------------

# The retired tags a step's list could hold, each named once.
TAG_1 = "G1"  # check_vocab: allow
TAG_2 = "G2"  # check_vocab: allow
TAG_3 = "G3"  # check_vocab: allow
BAR_REQS = "DevBar-Reqs"  # check_vocab: allow
BAR_RELEASE = "DevBar-Release"  # check_vocab: allow

STACK = (
    "# The product toolchain.\n"
    "[run]\n"
    "gates = not a step's list\n"
    "\n"
    "[step:duplo]\n"
    "command = {py} -m duplo {src}\n"
    "gates = " + TAG_2 + " " + TAG_3 + "\n"
    "layer = product\n"
    "\n"
    "[step:docs]\n"
    "command = npx thing\n"
    "GATES: " + TAG_1 + ", DevStg-Impl\n"
    "# gates = DevStg-Impl stays a comment\n"
    "\n"
    "[step:reqs]\n"
    "command = {py} reqs.py\n"
    "gates    = DevStg-Reqs " + BAR_RELEASE + "\n"
    "\n"
    "[step:bar]\n"
    "command = {py} bar.py\n"
    "gates = DevStg-Tests, " + BAR_REQS + "\n"
    "\n"
    "[step:spare]\n"
    "command = {py} spare.py\n"
    "gates =\n"
    "\n"
    "[step:current]\n"
    "command = {py} x.py\n"
    "from-stage = DevStg-Arch\n"
)


def test_a_steps_list_of_stages_becomes_the_one_stage_it_meant(tmp_path):
    """Implements: TC-427"""
    from kitlib import config as kconfig

    path = _write(tmp_path, "docs/stack.ini", STACK.replace("\n", "\r\n"))
    owed = [line for line in migrate.spellings_owed(tmp_path) if "stack" in line]
    assert owed == ["stack profile owes the rewrite: docs/stack.ini"]
    assert _run(tmp_path) == 0
    moves = (
        ("gates = " + TAG_2 + " " + TAG_3, "from-stage = DevStg-Impl"),
        ("GATES: " + TAG_1 + ", DevStg-Impl", "from-stage: DevStg-Needs"),
        ("gates    = DevStg-Reqs " + BAR_RELEASE, "from-stage    = DevStg-Needs"),
        ("gates = DevStg-Tests, " + BAR_REQS, "from-stage = DevStg-Needs"),
        ("gates =\n", "from-stage = DevStg-Impl\n"),
    )
    expected = STACK
    for old, new in moves:
        assert expected.count(old) == 1, old
        expected = expected.replace(old, new)
    # A section that is not a step keeps its key, and a comment its words.
    assert "[run]\ngates = not a step's list\n" in expected
    assert "# gates = DevStg-Impl stays a comment\n" in expected
    assert path.read_bytes() == expected.replace("\n", "\r\n").encode("utf-8")
    profile = kconfig.read_stack_ini(path)
    stages = {s: kconfig.step_threshold(profile, s) for s in profile.sections()[1:]}
    assert stages == {
        "step:duplo": "DevStg-Impl",
        "step:docs": "DevStg-Needs",
        "step:reqs": "DevStg-Needs",
        "step:bar": "DevStg-Needs",
        "step:spare": "DevStg-Impl",
        "step:current": "DevStg-Arch",
    }
    assert migrate.spellings_owed(tmp_path) == []
    assert _run(tmp_path, "--check") == 0


@pytest.mark.parametrize(
    "text, problem",
    (
        ("[step:a]\ngates = G9\n", "[step:a] gates names 'G9'"),
        ("[step:a]\ngates = " + TAG_2 + " ; noted\n", "[step:a] gates names ';'"),
        (
            "[step:a]\ngates = " + TAG_2 + "\n  " + TAG_3 + "\n",
            "[step:a] continues its `gates` list",
        ),
        (
            "[DEFAULT]\ngates = " + TAG_1 + "\n\n[step:a]\ncommand = x\n",
            "[DEFAULT] declares `gates`",
        ),
        (
            "[step:a]\ngates = " + TAG_1 + "\nfrom-stage = DevStg-Impl\n",
            "[step:a] declares both `gates` and `from-stage`",
        ),
        ("[step:a]\ngates = " + TAG_1 + "\n[step:a]\n", "it does not parse"),
        (
            "[step:a]\ncommand = run\n  gates = " + TAG_1 + "\ngates = " + TAG_2 + "\n",
            "would change more than the vocabulary",
        ),
    ),
    ids=(
        "unknown-token",
        "inline-comment",
        "continuation-line",
        "under-default",
        "both-keys",
        "does-not-parse",
        "look-alike-continuation",
    ),
)
def test_a_stack_profile_the_rewrite_cannot_prove_is_named_and_left(
    tmp_path, capsys, text, problem
):
    """Implements: TC-427"""
    path = _write(tmp_path, "docs/stack.ini", text)
    assert _run(tmp_path) == 1
    out = capsys.readouterr().out
    assert "stack profile NOT rewritten: docs/stack.ini: " in out, out
    assert problem in out, out
    assert path.read_bytes() == text.encode("utf-8")


def test_a_stack_profile_that_is_not_utf8_is_named_and_left(tmp_path, capsys):
    """Implements: TC-427"""
    raw = "[step:a]\ncommand = caf\xe9\ngates = DevStg-Impl\n".encode("latin-1")
    path = tmp_path / "docs" / "stack.ini"
    path.parent.mkdir(parents=True)
    path.write_bytes(raw)
    assert _run(tmp_path) == 1
    assert "docs/stack.ini: not UTF-8; left untouched" in capsys.readouterr().out
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

[requirement.SR-004]
status = "APPROVED"
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
    # Only the status cell moves, in each letter case a reader folds: the word
    # in a title or another key stays.
    assert toml.read_bytes() == STATUS_TOML.replace(
        'status = "Approved"', 'status = "Accepted"'
    ).replace("status = 'approved'", "status = 'accepted'").replace(
        'status = "APPROVED"', 'status = "ACCEPTED"'
    ).encode("utf-8")
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


def test_a_record_copy_whose_live_registry_is_gone_is_named_and_left(tmp_path, capsys):
    """Implements: TC-427"""
    _record(tmp_path)
    orphan = '[test.TC-001]\nmethod = "Run it."\nstatus = "Accepted"\n'
    _write(tmp_path, migrate.RECORD_DIRS[0] + "/docs/test/test-cases.toml", orphan)
    assert _run(tmp_path) == 1
    where = migrate.RECORD_DIRS[1] + "/docs/test/test-cases.toml"
    assert (
        "{}: no live docs/test/test-cases.toml to write it from; left untouched".format(
            where
        )
        in capsys.readouterr().out
    )
    assert (tmp_path / where).read_bytes() == orphan.encode("utf-8")


def _current(text):
    """`text` with the earlier spellings this module's fixtures hold respelled."""
    return (
        text.replace('"Approved"', '"Accepted"')
        .replace("\napproved = ", "\naccepted = ")
        .replace("\nreattested = ", "\nreaccepted = ")
    )


def test_spellings_owed_names_what_check_names_less_the_records_copies(tmp_path):
    """Implements: TC-427"""
    _record(tmp_path)
    owed = migrate.spellings_owed(tmp_path)
    rel = "docs/requirements/system-requirements.toml"
    assert "registry owes the rewrite: " + rel in owed, owed
    assert (
        "acceptance record owes the rewrite: docs/archive/last_approved -> "
        "docs/archive/last_accepted" in owed
    ), owed
    assert any(
        line.startswith("acceptance record owes the rewrite: ") and "keys" in line
        for line in owed
    ), owed
    assert not [
        line for line in owed if "written equal" in line or " absorbs " in line
    ], owed
    assert (tmp_path / migrate.RECORD_DIRS[0]).is_dir(), "spellings_owed wrote"


def test_a_record_copy_that_differs_from_live_is_owed_by_a_run_but_not_a_spelling(
    tmp_path,
):
    """Implements: TC-427"""
    home = migrate.RECORD_DIRS[1]
    _write(tmp_path, "docs/requirements/system-requirements.toml", _current(LIVE_SR))
    _write(tmp_path, home + "/acts.toml", _current(LEDGER))
    _write(
        tmp_path,
        home + "/docs/requirements/system-requirements.toml",
        _current(COPY_SR),
    )
    assert migrate.spellings_owed(tmp_path) == []
    # A run would still write the copy, absorbing its accepted cells.
    assert _run(tmp_path, "--check") == 1


def _check_vocab(root, *flags):
    return run_py([SCRIPTS / "check_vocab.py", "--root", str(root), *flags], root)


def test_check_vocab_reports_what_the_migrator_owes_until_it_has_run(tmp_path):
    """Implements: TC-427"""
    _record(tmp_path)
    warn = _check_vocab(tmp_path)
    assert warn.returncode == 0, warn.stdout + warn.stderr
    line = (
        "check_vocab: WARN - registry owes the rewrite: "
        "docs/requirements/system-requirements.toml - stored in an earlier "
        "spelling; run `python scripts/migrate_vocabulary.py`"
    )
    assert line in warn.stdout, warn.stdout
    strict = _check_vocab(tmp_path, "--strict")
    assert strict.returncode == 1, strict.stdout + strict.stderr
    assert "acceptance record owes the rewrite" in strict.stdout
    assert " absorbs " not in strict.stdout and "written equal" not in strict.stdout
    assert _run(tmp_path) == 0
    clean = _check_vocab(tmp_path, "--strict")
    assert clean.returncode == 0, clean.stdout + clean.stderr
    assert "nothing stored in an earlier spelling" in clean.stdout


# --- a record that holds a row-by-row act ----------------------------------------

# An act ledger the row-by-row writer wrote: every entry carries `kept`, the
# seed's empty, a later act's naming the row it left owed.
KEPT_LEDGER = """# ACCEPTANCE ACTS, appended by the snapshot command. Do not edit.

[[act]]
seq = 1
date = "2026-11-23"
accepted = ["SR-001", "SR-009"]
reaccepted = []
copied = ["docs/requirements/system-requirements.toml"]
kept = []

[[act]]
seq = 2
date = "2026-11-23"
accepted = []
reaccepted = []
copied = ["docs/requirements/system-requirements.toml"]
kept = ["SR-001", "SR-009"]
"""

# An entry the earlier kit keyed by its earlier names.
EARLIER_ENTRY = """
[[act]]
seq = 3
date = "2026-09-27"
approved = ["SR-001"]
reattested = []
"""

COPY_REL = "docs/requirements/system-requirements.toml"
# The guidance a refusal carries.
FIRST_ACT = "before its first row-by-row act"


def _row_by_row(root, ledger=KEPT_LEDGER, copy=None, home=None):
    """A repository whose acceptance record, under `home` (the current name by
    default), holds `ledger` and a copy of one registry (`copy`, by default the
    current spelling of a copy that differs from live in an accepted row, a
    draft row and an accepted row live no longer holds). Live is current."""
    home = home or migrate.RECORD_DIRS[1]
    _write(root, COPY_REL, _current(LIVE_SR))
    _write(root, home + "/README.md", "# `last_accepted` - the record\n")
    _write(root, home + "/acts.toml", ledger)
    _write(root, home + "/" + COPY_REL, _current(COPY_SR) if copy is None else copy)


def _tree_bytes(root):
    """`{repo-relative path: bytes}` of every file under `root`."""
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def test_a_row_by_row_record_in_the_current_vocabulary_has_no_copy_written(
    tmp_path, capsys
):
    """Implements: TC-427"""
    _row_by_row(tmp_path)
    binding = _write(
        tmp_path,
        "docs/reviews/wi-1/001-ADJUDICATE-a.md.requested",
        BINDING.format("accepted"),
    )
    record = tmp_path / migrate.RECORD_DIRS[1]
    before = _tree_bytes(record)
    assert _run(tmp_path, "--check") == 1
    out = capsys.readouterr().out
    assert "verdict binding owes the rewrite: docs/reviews/wi-1/" in out, out
    # Neither the kept row's drift nor the draft's is owed, and nothing absorbs.
    assert "acceptance record" not in out, out
    assert _run(tmp_path) == 0
    capsys.readouterr()
    assert binding.read_text(encoding="utf-8") == BINDING.format("recorded")
    assert _tree_bytes(record) == before
    assert _run(tmp_path, "--check") == 0
    assert "nothing stored in an earlier spelling" in capsys.readouterr().out
    assert migrate.spellings_owed(tmp_path) == []


# Act ledgers, each read by the kit as row by row or not: no entry; an entry
# without `kept`; `kept` outside an act entry, at the top and in another
# table array; an empty and a non-empty `kept`; a byte-order mark the kit's
# reader does not strip; and a ledger that does not parse.
_PLAIN_ENTRY = '\n[[act]]\nseq = 1\ndate = "2026-11-23"\naccepted = ["SR-001"]\n'
LEDGER_READINGS = (
    "",
    _PLAIN_ENTRY,
    "kept = []\n" + _PLAIN_ENTRY,
    _PLAIN_ENTRY + "\n[[other]]\nkept = []\n",
    _PLAIN_ENTRY + "kept = []\n",
    KEPT_LEDGER,
    "﻿" + KEPT_LEDGER,
    KEPT_LEDGER + "\n[[act\n",
)


def test_the_record_is_read_as_row_by_row_as_the_kit_reads_its_ledger(tmp_path):
    """The migrator's reading of the act ledger is its own (it imports nothing
    from the kit), so it is held to the kit's: over each ledger, a copy holding
    an earlier spelling is left as it is (the run refuses) exactly when the
    kit's reading calls the record row by row, and rewritten otherwise.

    Implements: TC-427
    """
    readings = []
    for i, ledger in enumerate(LEDGER_READINGS):
        root = tmp_path / str(i)
        _row_by_row(root, ledger, copy=COPY_SR)
        copy = root / migrate.RECORD_DIRS[1] / COPY_REL
        _run(root)
        kit = record_rows.act_rows([ledger], ledger, lambda new, sides: [])[1]
        readings.append((i, kit, copy.read_bytes() == COPY_SR.encode("utf-8")))
    assert [kit for _i, kit, _left in readings] == [
        False,
        False,
        False,
        False,
        True,
        True,
        False,
        False,
    ]
    assert all(kit == left for _i, kit, left in readings), readings


# Each way a record that holds a row-by-row act can still store an earlier
# spelling, and the path its refusal names.
EARLIER_RECORDS = {
    "earlier-directory-holding-the-ledger": (
        lambda root: _row_by_row(root, home=migrate.RECORD_DIRS[0]),
        migrate.RECORD_DIRS[0] + ": the record's earlier directory name",
    ),
    "earlier-directory-beside-the-record": (
        # The earlier kit's record left standing beside the current one.
        lambda root: (_record(root), _row_by_row(root)),
        migrate.RECORD_DIRS[0] + ": the record's earlier directory name",
    ),
    "earlier-ledger-key": (
        lambda root: _row_by_row(root, KEPT_LEDGER + EARLIER_ENTRY),
        migrate.RECORD_DIRS[1] + "/acts.toml: act entries keyed approved, reattested",
    ),
    "earlier-status-in-a-copy": (
        lambda root: _row_by_row(root, copy=COPY_SR),
        migrate.RECORD_DIRS[1]
        + "/"
        + COPY_REL
        + ": a copy storing an earlier spelling",
    ),
    "earlier-field-in-a-copy": (
        lambda root: _row_by_row(
            root,
            copy=_current(COPY_SR).replace(
                '\nstatus = "Drafted"', '\nverification = "Test"\nstatus = "Drafted"'
            ),
        ),
        migrate.RECORD_DIRS[1]
        + "/"
        + COPY_REL
        + ": a copy storing an earlier spelling",
    ),
    "copy-that-does-not-parse": (
        lambda root: _row_by_row(root, copy="[requirement.SR-001\n"),
        migrate.RECORD_DIRS[1] + "/" + COPY_REL + ": it does not parse",
    ),
}


@pytest.mark.parametrize("case", sorted(EARLIER_RECORDS))
def test_a_row_by_row_record_storing_an_earlier_spelling_refuses_the_whole_run(
    tmp_path, capsys, case
):
    """Implements: TC-427"""
    build, named = EARLIER_RECORDS[case]
    build(tmp_path)
    # Beside it, a binding and a live registry in an earlier spelling, which a
    # run that went ahead would rewrite.
    _write(tmp_path, "docs/reviews/x.md.requested", BINDING.format("accepted"))
    _write(
        tmp_path, "docs/test/test-cases.toml", '[test.TC-001]\nstatus = "Approved"\n'
    )
    before = _tree_bytes(tmp_path)
    for flags in (("--check",), ()):
        assert _run(tmp_path, *flags) == 1
        out = capsys.readouterr().out
        lines = out.splitlines()
        assert all(
            line.startswith("migrate_vocabulary: acceptance record NOT rewritten: ")
            for line in lines
        ), out
        assert any(named in line for line in lines), out
        assert "nothing is written" in out and FIRST_ACT in out, out
        assert _tree_bytes(tmp_path) == before
    owed = migrate.spellings_owed(tmp_path)
    assert owed == [
        line.replace(
            "migrate_vocabulary: acceptance record NOT rewritten: ",
            "acceptance record cannot be rewritten: ",
        )
        for line in lines
    ], owed


def test_check_vocab_reports_the_refusal(tmp_path):
    """Implements: TC-427"""
    _row_by_row(tmp_path, copy=COPY_SR)
    warn = _check_vocab(tmp_path)
    assert warn.returncode == 0, warn.stdout + warn.stderr
    assert (
        "check_vocab: WARN - acceptance record cannot be rewritten: {}/{}: ".format(
            migrate.RECORD_DIRS[1], COPY_REL
        )
        in warn.stdout
    ), warn.stdout
    assert FIRST_ACT in warn.stdout, warn.stdout
    assert "registry owes the rewrite" not in warn.stdout, warn.stdout
    strict = _check_vocab(tmp_path, "--strict")
    assert strict.returncode == 1, strict.stdout + strict.stderr


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


# Links into the record written inside code, which keep their words: inline
# spans of one and of two backticks (the second holding a backtick), a fenced
# block of backticks holding a link and a reference definition, one of tildes,
# and a run of three backticks with more on its line, which opens an inline
# span and not a fence. Beside them, a stray backtick no run closes in its
# paragraph, and one link in prose, the only one that moves.
CODED = (
    "Write `[the ledger](docs/archive/last_approved/acts.toml)` to link it,\n"
    "or ``[a `tick`](last_approved/acts.toml)`` with a backtick inside.\n"
    "\n"
    "```markdown\n"
    "[the stamp](docs/archive/last_approved/README.md)\n"
    "[s]: docs/archive/last_approved/README.md\n"
    "```\n"
    "\n"
    "~~~~\n"
    "[the ledger](../archive/last_approved/acts.toml)\n"
    "~~~~\n"
    "\n"
    "```[x](last_approved/acts.toml)``` stays inline code.\n"
    "\n"
    "A stray ` backtick, then [a real one](docs/archive/last_approved/acts.toml).\n"
    "\n"
    "Its paragraph ended, so ` this one closes nothing either.\n"
)


def test_links_into_the_record_follow_it_and_every_other_word_stays(tmp_path, capsys):
    """Implements: TC-427"""
    page = _write(tmp_path, "docs/reviews/old.md", LINKED.replace("\n", "\r\n"))
    coded = _write(tmp_path, "docs/reviews/code.md", CODED.replace("\n", "\r\n"))
    hidden = _write(tmp_path, ".claude/notes.md", LINKED)
    vendored = _write(tmp_path, "node_modules/pkg/README.md", LINKED)
    cached = _write(tmp_path, "pkg/__pycache__/notes.md", LINKED)
    assert _run(tmp_path) == 0
    out = capsys.readouterr().out
    assert "docs/reviews/old.md: 2 link(s)" in out, out
    assert "docs/reviews/code.md: 1 link(s)" in out, out
    # A link written inside code is code, and keeps its words.
    moved = CODED.replace(
        "[a real one](docs/archive/last_approved/acts.toml)",
        "[a real one](docs/archive/last_accepted/acts.toml)",
    )
    assert coded.read_bytes() == moved.replace("\n", "\r\n").encode("utf-8")
    expected = LINKED.replace(
        "../archive/last_approved/acts", "../archive/last_accepted/acts"
    ).replace("docs/archive/last_approved/README", "docs/archive/last_accepted/README")
    assert page.read_bytes() == expected.replace("\n", "\r\n").encode("utf-8")
    assert hidden.read_text(encoding="utf-8") == LINKED
    assert vendored.read_text(encoding="utf-8") == LINKED
    assert cached.read_text(encoding="utf-8") == LINKED


@pytest.mark.parametrize("name", migrate.SCRATCHPAD_NAMES)
def test_the_links_walk_never_reads_the_scratchpad(tmp_path, monkeypatch, name):
    """The scratchpad holds a person's private notes: the run renames it
    without opening it, and the link walk passes it by, a link into the
    record's earlier directory inside it included.

    Implements: TC-427
    """
    notes = "# notes\n[the ledger](docs/archive/last_approved/acts.toml)\n"
    _write(tmp_path, name, notes)
    page = _write(tmp_path, "docs/page.md", notes)
    opened = []

    def spy(method):
        real = getattr(pathlib.Path, method)

        def read(self, *args, **kwargs):
            opened.append(self.name)
            return real(self, *args, **kwargs)

        return read

    for method in ("read_bytes", "read_text", "open"):
        monkeypatch.setattr(pathlib.Path, method, spy(method))
    assert _run(tmp_path) == 0
    monkeypatch.undo()
    pad = tmp_path / migrate.SCRATCHPAD_NAMES[1]
    assert pad.read_text(encoding="utf-8") == notes
    assert not set(migrate.SCRATCHPAD_NAMES) & set(opened), opened
    # The walk ran: the page beside it moved.
    assert "last_accepted/acts.toml" in page.read_text(encoding="utf-8")


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


def test_the_migrator_imports_from_the_kit_only_the_stack_profile_parse():
    """It runs while the kit's own scripts cannot yet read the repository, so
    its module-level imports are the standard library's, and its one import
    from the kit sits inside the stack profile step.

    Implements: TC-427
    """
    tree = ast.parse((SCRIPTS / "migrate_vocabulary.py").read_text(encoding="utf-8"))
    top = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            top |= {alias.name.split(".")[0] for alias in node.names}
        elif isinstance(node, ast.ImportFrom):
            top.add((node.module or "").split(".")[0])
    assert top <= set(sys.stdlib_module_names), top
    nested = [
        (fn.name, getattr(node, "module", None))
        for fn in ast.walk(tree)
        if isinstance(fn, ast.FunctionDef)
        for node in ast.walk(fn)
        if isinstance(node, (ast.Import, ast.ImportFrom))
    ]
    assert nested == [("_stack_parse", "kitlib.config")], nested
