"""The migrator's Drafted rows follow its new policy-file step."""

SR = "docs/requirements/system-requirements.toml"
LLR = "docs/requirements/low-level-requirements.toml"
TC = "docs/test/test-cases.toml"

EDITS = [
    (SR, "the outcome of a verdict binding, and a registry's field name and that field's value under either carrier, in the live registry and in the acceptance record's copy of it.",
         "the outcome of a verdict binding; a registry's field name and that field's value under either carrier, in the live registry and in the acceptance record's copy of it; and a table and a key of the policy file."),
    (LLR, 'title = "The vocabulary migrator: verdict bindings and registries under both carriers"',
          'title = "The vocabulary migrator: verdict bindings, registries under both carriers and the policy file"'),
    (LLR, "/registries/STEPS/FIELDS/VALUES/main", "/registries/POLICY_TABLES/POLICY_KEYS/_policy_table/_policy_line/migrate_policy/policy/STEPS/FIELDS/VALUES/main"),
    (LLR, "registries applies the carrier's function to each registry path and reports an Unsafe file without writing it.",
          "registries applies the carrier's function to each registry path and reports an Unsafe file without writing it. POLICY_TABLES maps an earlier table name of docs/process.toml to the current one and POLICY_KEYS maps, within a table, an earlier key to the current one. migrate_policy rewrites header lines and the key lines beneath them through _policy_line, which tracks the table a line belongs to and stops tracking at a header it cannot read, and returns the text only when its parse equals the original's with each table passed through _policy_table; a file declaring both spellings of a table or of a key, an inline or dotted table the line edit cannot reach, and any other difference raise Unsafe. policy applies it to the one file."),
    (TC, "a row carrying both spellings, a file that does not parse and a look-alike line inside a multi-line cell; then --check",
         "a row carrying both spellings, a file that does not parse and a look-alike line inside a multi-line cell; a policy file naming the earlier table and dial key, with the same key under another table, then one declaring both spellings of the table or of the key, one writing the dial as an inline table or a dotted key, and one already current; then --check"),
]
