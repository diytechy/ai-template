"""HANDOFF 4.5.2, 10.3 step 9: the migrator's `work item` step in its three
rows (SR-247, LLR-369, TC-427, all Drafted). Run tc427_evidence.py after.
"""

LLR = "docs/requirements/low-level-requirements.toml"
SR = "docs/requirements/system-requirements.toml"
TC = "docs/test/test-cases.toml"

EDITS = [
    (
        LLR,
        "/decisions/SCRATCHPAD_NAMES/scratchpad/",
        "/decisions/WORK_DIRS/WORK_ITEM_KEYS/_front_matter_span/_disposition_spans/"
        "_top_level_line/migrate_work_item/_work_item_files/work_items/"
        "SCRATCHPAD_NAMES/scratchpad/",
    ),
    (
        LLR,
        "decisions applies it to each .toml file directly under docs/decisions. ",
        "decisions applies it to each .toml file directly under docs/decisions. "
        "WORK_ITEM_KEYS maps an earlier top-level key of a work item to the current "
        "one, as bar to checks_stage, the stage a row pins its landing checks to. "
        "migrate_work_item respells it in the item's front matter, the span "
        "_front_matter_span finds between the +++ line the file opens with and the "
        "next, and in each fenced ```toml block of its ## Dispositions section, the "
        "spans _disposition_spans finds up to the next ## heading: each segment is "
        "edited through _top_level_line, which stops respelling at the segment's "
        "first table header, under the same _rekeyed proof, so a segment carrying "
        "both spellings, one that does not parse and a look-alike line inside a "
        "multi-line string raise Unsafe. work_items applies it to each .md file "
        "_work_item_files yields under WORK_DIRS, docs/work and docs/archive/work, "
        "and names a file that is not UTF-8 or cannot be proved without writing it. ",
    ),
    (
        SR,
        "and the verdict key of each entry in a delegated-decisions record. ",
        "the verdict key of each entry in a delegated-decisions record; and the "
        "stage key of a work item's front matter and of each row its Dispositions "
        "section drafts. ",
    ),
    (
        TC,
        "and a page that is not UTF-8; then --check before and after a write, and a second write.",
        "and a page that is not UTF-8; a work item in the live and in the archived "
        "folder whose front matter and one drafted row carry the earlier stage key, "
        "under CRLF, beside the same line in prose, under a table header of a "
        "drafted row and in a block under another heading, the same page outside the "
        "work-item folders, then one carrying both spellings, one with a look-alike "
        "line inside a multi-line string, one whose drafted row does not parse and "
        "one that is not UTF-8; then --check before and after a write, and a second "
        "write.",
    ),
]
