"""HANDOFF 10.5 pass 2, hand edits: a form the dial concept missed.

(As applied: the rename rewrites the whole key line, so the test holds every
OTHER line, not a comment on the dial line.)

`bootstrap._migrate_dial_key_name` reads the policy file's `[authority]` table
but passed the table's EARLIER name, "attestation", to `_confirmed_edit` on a
line of its own (the formatter had split the call, so r42_s4_dial's
`"attestation", old` rule never matched). `_confirmed_edit` then looked for a
`[attestation]` header, found none, and every rename of the retired dial key
under a bare `[authority]` header was refused and left in place. The only
test covered the inline-table refusal, which refuses either way. Fixed to
"authority", with a test of the bare-header rename (TC-152's "an ordinary
policy file still migrates"), and the inline-table test's docstring, which
still named the table by its earlier name.
"""

BOOT = "project-trajectory/scripts/bootstrap.py"
TEST = "tests/test_bootstrap.py"
TCS = "docs/test/test-cases.toml"

NEW_TEST = '''

def test_the_dial_key_under_a_bare_authority_header_is_renamed_in_place(tmp_path):
    """The migration renames the retired dial key on its own line under a bare
    `[authority]` header, keeping its value and every other line.

    Adequacy witness: a rename that looks for the line under any other header
    (the table's earlier name, as it did after the table was renamed) finds no
    line, refuses the file and leaves the old key in place; that fails here.

    Implements: TC-152
    """
    boot = load_script("bootstrap")
    old = boot.LEGACY_DIAL_KEY
    text = '# kept\\n[authority]\\n{} = "DevStg-Arch"\\nfinal_review = "off"\\n'
    path = _policy_repo(tmp_path, text.format(old))
    _moved, notes = boot.migrate_legacy_config(tmp_path)
    assert path.read_bytes() == text.format("operator_accepts_through").encode("utf-8")
    assert not any("LEFT IN PLACE" in n for n in notes), notes
'''

EDITS = [
    (
        BOOT,
        '''    edited = _confirmed_edit(
        text.splitlines(),
        "attestation",
        old,
''',
        '''    edited = _confirmed_edit(
        text.splitlines(),
        "authority",
        old,
''',
    ),
    (
        TEST,
        """    old key the parse holds inside an inline `attestation` table: the file's""",
        """    old key the parse holds inside an inline `authority` table: the file's""",
    ),
    (
        TEST,
        '''    assert any(old in n and "LEFT IN PLACE" in n for n in notes), notes


def test_an_ordinary_policy_file_still_migrates_and_sets_in_place(tmp_path):''',
        '''    assert any(old in n and "LEFT IN PLACE" in n for n in notes), notes
'''
        + NEW_TEST
        + '''

def test_an_ordinary_policy_file_still_migrates_and_sets_in_place(tmp_path):''',
    ),
    (
        TCS,
        "; tests/test_bootstrap.py::test_migration_writes_the_real_key_",
        "; tests/test_bootstrap.py::test_the_dial_key_under_a_bare_authority_header_is_renamed_in_place"
        "; tests/test_bootstrap.py::test_migration_writes_the_real_key_",
    ),
]
