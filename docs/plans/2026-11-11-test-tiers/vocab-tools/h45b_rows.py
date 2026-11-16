"""HANDOFF 10.5 pass 2, step 9: the migrator's rows grow with its list step.

The migrator now respells an element of a list in the policy file: the brief
kind in `[adjudicator] retain_for`. LLR-369 names the new symbols and says
what they do, TC-427 names the cases, SR-247's criterion names the element.
The rows describe the earlier spelling without writing it, so that the later
passes' rules have nothing to reword here. All three rows are `Drafted`.
"""

LLR = "docs/requirements/low-level-requirements.toml"
TCS = "docs/test/test-cases.toml"
SRS = "docs/requirements/system-requirements.toml"

EDITS = [
    (
        LLR,
        "POLICY_TABLES/POLICY_KEYS/POLICY_VALUES/_policy_value/_policy_rest/_policy_table/_policy_line/migrate_policy/",
        "POLICY_TABLES/POLICY_KEYS/POLICY_VALUES/POLICY_ITEMS/_policy_value/_policy_rest/_policy_table/_policy_line/_code_part/_array_line/_array_opened/migrate_policy/",
    ),
    (
        LLR,
        "_policy_value applies it to a parsed value and _policy_rest to the one-line quoted value of a key line. ",
        "_policy_value applies it to a parsed value and _policy_rest to the one-line quoted value of a key line. "
        "POLICY_ITEMS maps, within a table and a key holding a list of strings, an earlier element to the current one, "
        "as the brief kind of the sitting that takes a row into acceptance in [adjudicator] retain_for; "
        "_policy_value applies it to each string of a parsed list, _array_opened respells the elements on the key line "
        "that opens such a list, and _array_line those on each line after it until a ] closes the list, each only "
        "before the comment _code_part finds, so a comment keeps its words. ",
    ),
    (
        LLR,
        "which tracks the table a line belongs to and stops tracking at a header it cannot read, and returns the text",
        "which tracks the table a line belongs to and stops tracking at a header it cannot read, and the lines of a "
        "respelled list through _array_opened and _array_line, and returns the text",
    ),
    (
        TCS,
        "and one writing it as an inline table or a multi-line string;",
        "and one writing it as an inline table or a multi-line string; a policy file whose adjudicator retains the "
        "first sitting's brief kind by its earlier name in a multi-line list carrying comments and in a one-line list, "
        "with the same key under another table, and one holding it in an inline table;",
    ),
    (
        SRS,
        "a table, a key and a value of the policy file;",
        "a table, a key, a value and an element of a list in the policy file;",
    ),
]
