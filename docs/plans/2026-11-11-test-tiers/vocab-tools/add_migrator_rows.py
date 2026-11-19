"""Append the migrator's three spine rows (Drafted) to the live registries.

Run once. It refuses when any of the ids is already present.
"""

from pathlib import Path

ROOT = Path(r"C:\Projects\ai-template-wt-vocabulary")

SR = '''
[requirement.SR-247]
title = "An earlier kit's stored values reach the current vocabulary through a migrator"
sn_refs = ["SN-001", "SN-007"]
boundary_refs = ["B-05"]
hat_refs = ["CONSISTENCY"]
requirement = """The delivered kit shall provide a migrator that rewrites, in place, the stored values an earlier kit vocabulary spelled differently and a current script still reads, and that changes nothing else in a file it rewrites."""
rationale = """The kit's vocabulary was unified so that one word names one thing, and the operator ruled out readers of an earlier spelling in the core scripts. A repository that still stores one would then read as if the value were absent, so a purpose-built migrator is the path from an earlier kit and the one place the earlier spellings are known. It rewrites whole values in known places and proves each rewrite by parsing the file again, because a migration that guessed inside prose, or changed a cell it was not asked to change, would alter a record nobody reviewed."""
acceptance_criteria = """Run over a repository that stores earlier spellings, the migrator rewrites each value it names where that value is stored: the outcome of a verdict binding, and a registry's field name and that field's value under either carrier, in the live registry and in the acceptance record's copy of it. Every other byte of a rewritten file is unchanged, its line endings included. A file whose rewrite would parse as anything other than the named change is left untouched, is named in the output, and makes the run exit 1. With --check nothing is written and the run exits 1 when a rewrite is owed. A second run finds nothing to do and exits 0."""
priority = "S"
verification_method = "Test"
status = "Drafted"
phase = 6
aspect = "process"
'''

LLR = '''
[design.LLR-369]
sr_refs = ["SR-247"]
title = "The vocabulary migrator: verdict bindings and registries under both carriers"
module = "project-trajectory/scripts/migrate_vocabulary.py"
code_symbol = "Unsafe/_rewrite/bindings/registry_paths/_current/_toml_rows/_toml_expected/_toml_cell/migrate_toml/_csv_bare/_csv_quoted/_csv_records/_csv_parsed/_csv_expected/_csv_edits/migrate_csv/registries/STEPS/FIELDS/VALUES/main"
detail = """migrate_vocabulary.py imports nothing from the kit. STEPS names each step and main runs them in order, printing one line per rewritten file, per file that owes the rewrite under --check, and per file left untouched; it exits 1 when a file could not be rewritten safely, or under --check when a rewrite is owed. bindings rewrites the line outcome = accepted to outcome = recorded in each .requested file under docs/reviews through _rewrite, which keeps every byte outside the match. registry_paths yields each .toml and .csv file directly under docs/requirements and docs/test, then the same files under either name of the acceptance record's directory. FIELDS maps an earlier field name to the current one per carrier and VALUES maps an earlier value to the current one within a field; _current applies both to one cell, matching the value on its stripped text and keeping its padding. migrate_toml rewrites one-line quoted cells with _toml_cell and returns the text only when its parse equals _toml_expected, the parse of the original with each row's fields and values moved; a row carrying both spellings of a field, a file that does not parse and any other difference raise Unsafe. migrate_csv reads cell spans with _csv_records, which folds doubled quotes through _csv_quoted and ends a bare cell through _csv_bare; _csv_edits replaces the header cells and the cells beneath them inside their own spans, and the result is returned only when the csv module parses it as _csv_expected. registries applies the carrier's function to each registry path and reports an Unsafe file without writing it."""
rationale = """A whole value in a known place is the only thing a migrator can move without judging prose, and a second parse is what proves that nothing else moved: a look-alike line inside a multi-line cell changes the parse and so refuses the file. Spans keep quoting, padding, comments and line endings, so the diff a repository commits is the vocabulary and nothing else. Importing nothing from the kit lets the migrator run while the kit's own scripts cannot yet read the repository."""
test_refs = "TC-427"
status = "Drafted"
component = "CMP-006"
phase = 6
'''

TC = '''
[test.TC-427]
verifies = ["SR-247", "LLR-369"]
level = "Unit"
method = """Run the vocabulary migrator over temporary repositories: a verdict binding whose outcome reads accepted, beside one that reads failed and one whose other cells hold the word; a TOML registry and a CSV registry holding the earlier field name and the earlier method, with the same words inside quoted and multi-line prose cells, under LF and CRLF endings, with a byte-order mark and a quoted header cell; the acceptance record's copy under both of its directory names; a file outside the registry directories; a row carrying both spellings, a file that does not parse and a look-alike line inside a multi-line cell; then --check before and after a write, and a second write."""
tier = "Smoke"
expected = "Satisfies SR-247 AcceptanceCriteria"
automated = "Yes"
evidence = "tests/test_migrate_vocabulary.py"
status = "Drafted"
phase = 6
'''

TARGETS = (
    ("docs/requirements/system-requirements.toml", "[requirement.SR-247]", SR),
    ("docs/requirements/low-level-requirements.toml", "[design.LLR-369]", LLR),
    ("docs/test/test-cases.toml", "[test.TC-427]", TC),
)


def main():
    texts = {}
    for rel, header, _row in TARGETS:
        text = (ROOT / rel).read_bytes().decode("utf-8")
        if header in text:
            raise SystemExit("{} already holds {}".format(rel, header))
        if not text.endswith("\n"):
            raise SystemExit("{} does not end with a newline".format(rel))
        texts[rel] = text
    for rel, header, row in TARGETS:
        eol = "\r\n" if "\r\n" in texts[rel] else "\n"
        (ROOT / rel).write_bytes((texts[rel] + row.replace("\n", eol)).encode("utf-8"))
        print("appended", header, "to", rel)


if __name__ == "__main__":
    main()
