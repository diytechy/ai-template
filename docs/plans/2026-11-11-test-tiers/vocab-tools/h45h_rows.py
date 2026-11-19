"""HANDOFF 10.5 pass 4, step 9: the migrator's rows grow with its last steps.

The status value (VALUES), and the acceptance record: the directory moved,
the act ledger re-keyed, each copy written equal to live with every absorbed
accepted cell named (D13). The decisions step now shares its line-edit proof
(`_rekeyed`) with the ledger, so `_decisions_expected` is gone from the code
symbols. Written without the earlier spellings, so no later rule rewords
them. All three rows are `Drafted`.
"""

LLR = "docs/requirements/low-level-requirements.toml"
TCS = "docs/test/test-cases.toml"
SRS = "docs/requirements/system-requirements.toml"

EDITS = [
    (LLR,
     "/DECISION_KEYS/_decision_entries/_decisions_expected/_decision_line/migrate_decisions_record/decisions/SCRATCHPAD_NAMES/scratchpad/STEPS/",
     "/_parsed/_moved_keys/_rekeyed/DECISION_KEYS/_decision_entries/_decision_line/migrate_decisions_record/decisions/SCRATCHPAD_NAMES/scratchpad/"
     "LEDGER_NAME/LEDGER_KEYS/_ledger_entries/_ledger_line/migrate_ledger/_record_rows/_absorbed/_record_copies/_copies_owed/_ledger_owed/_write_record/record/STEPS/"),
    (LLR,
     "and returns the text only when its parse equals _decisions_expected, the parse of the original with each entry's keys moved; an entry carrying both spellings, a file that does not parse and any other difference raise Unsafe. decisions applies it",
     "through _rekeyed, which parses the text with _parsed, moves each entry's keys in that parse with _moved_keys and returns the text only when the edited text parses as exactly that; an entry carrying both spellings, a file that does not parse and any other difference raise Unsafe. decisions applies it"),
    (LLR,
     "and reports a problem without moving either when both exist.\"\"\"",
     "and reports a problem without moving either when both exist. VALUES also maps the status a row holds once accepted from its earlier spelling to the current one, in each letter case a reader folds. "
     "record moves the acceptance record's directory from its earlier name to its current one, respells the two keys of each [[act]] entry in its act ledger through migrate_ledger (_ledger_entries and _ledger_line under the same _rekeyed proof), "
     "and writes each registry copy in it equal to its live registry, naming through _absorbed every cell of a row the copy holds as accepted that the live registry holds otherwise, and each such row the live registry no longer holds: "
     "_record_rows reads either carrier, _record_copies and _copies_owed find the copies that differ, _ledger_owed proves the ledger edit, and _write_record moves and writes only after both are proved. "
     "Both directory names present, a ledger edit that cannot be proved, or a copy with no live registry is a problem, and the first two leave the record untouched. STEPS runs the record last, so its copies equal live registries the registry step has already respelled.\"\"\""),
    (TCS,
     "the scratchpad under its earlier name, and under both names; then --check",
     "the scratchpad under its earlier name, and under both names; a TOML and a CSV registry whose rows hold the earlier status in two letter cases beside the same word in other cells; "
     "an acceptance record under its earlier name with a README, an act ledger and a registry copy that differs from live in an accepted row, a draft row and an accepted row live no longer holds, "
     "then a record under both names and a ledger with a look-alike key line inside a multi-line string; then --check"),
    (SRS,
     "a registry's field name and that field's value under either carrier",
     "a registry's field name and a field's value under either carrier"),
    (SRS,
     "It renames the operator's scratchpad from its earlier file name without reading it,",
     "It moves the acceptance record from its earlier directory name, respells its act ledger's keys and writes each registry copy in it equal to the live registry, naming every accepted cell a copy absorbs; "
     "a record present under both names, or a ledger whose rewrite would parse as anything else, is left as it is, is named, and makes the run exit 1. "
     "It renames the operator's scratchpad from its earlier file name without reading it,"),
]
