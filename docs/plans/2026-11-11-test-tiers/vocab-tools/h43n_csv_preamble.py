"""The migrator's CSV step read the first record as the header row.

Found by tests/test_csv_header.py (the census of raw CSV readers) in the
fourth session's run: a registry CSV may open with a `#` declaration preamble,
which `kitlib.spine.csv_body` drops before the header row. The migrator took
the comment line as its header, so a `Verification` header under a preamble
was never renamed. It imports nothing from the kit, so it measures the same
preamble itself (`_csv_preamble`), keeps those bytes as they are, and is
named in the census's exceptions with that reason.

Apply after h43m_migrator.py (both edit LLR-369 and TC-427).
"""

MIG = "project-trajectory/scripts/migrate_vocabulary.py"
TEST = "tests/test_migrate_vocabulary.py"
LLR = "docs/requirements/low-level-requirements.toml"
TC = "docs/test/test-cases.toml"

EDITS = [
    (MIG,
     "def _csv_parsed(text):\n"
     "    return list(csv.reader(io.StringIO(text, newline=\"\")))\n",
     "def _csv_parsed(text):\n"
     "    \"\"\"The records of CSV `text` as the csv module reads them. A raw reader\n"
     "    on purpose, named in tests/test_csv_header.py: this script imports\n"
     "    nothing from the kit, and `_csv_preamble` has already cut off the\n"
     "    comment preamble the kit's reader would drop.\"\"\"\n"
     "    return list(csv.reader(io.StringIO(text, newline=\"\")))\n"),
    (MIG,
     "def migrate_csv(text):\n"
     "    \"\"\"`text` with its header cells and its cells' values in the current\n"
     "    vocabulary. Raises `Unsafe` when the result would not parse as exactly\n"
     "    that.\n"
     "\n"
     "    Implements: SR-247, LLR-369\n"
     "    \"\"\"\n"
     "    body = text.lstrip(\"\\ufeff\")\n"
     "    offset = len(text) - len(body)\n"
     "    records = _csv_records(body)\n",
     "def _csv_preamble(text):\n"
     "    \"\"\"The length of the leading run of blank and `#` comment lines in\n"
     "    `text`: the preamble the kit's CSV reader drops before the header row.\n"
     "    Only the leading run counts; a `#` opening a data line, or one inside a\n"
     "    quoted cell, is data.\"\"\"\n"
     "    end = 0\n"
     "    for line in text.splitlines(keepends=True):\n"
     "        if line.strip() and not line.lstrip().startswith(\"#\"):\n"
     "            break\n"
     "        end += len(line)\n"
     "    return end\n"
     "\n"
     "\n"
     "def migrate_csv(text):\n"
     "    \"\"\"`text` with its header cells and its cells' values in the current\n"
     "    vocabulary. A byte-order mark and a leading comment preamble are kept as\n"
     "    they are, and the header row is the first line after them. Raises\n"
     "    `Unsafe` when the result would not parse as exactly that.\n"
     "\n"
     "    Implements: SR-247, LLR-369\n"
     "    \"\"\"\n"
     "    offset = len(text) - len(text.lstrip(\"\\ufeff\"))\n"
     "    offset += _csv_preamble(text[offset:])\n"
     "    body = text[offset:]\n"
     "    records = _csv_records(body)\n"),
    # the test
    (TEST,
     "# --- the policy file -----------------------------------------------------------\n",
     "def test_a_csv_registrys_comment_preamble_is_kept_and_the_row_after_it_renamed(\n"
     "    tmp_path,\n"
     "):\n"
     "    \"\"\"Implements: TC-427\"\"\"\n"
     "    preamble = \"\\ufeff# Contracts: IF-001\\r\\n#   a declaration header\\r\\n\\r\\n\"\n"
     "    rows = SR_CSV + \"# SR-003,not a comment,a data line,Attest,Drafted\\r\\n\"\n"
     "    path = _write(tmp_path, \"docs/requirements/performance-budgets.csv\", preamble + rows)\n"
     "    assert _run(tmp_path) == 0\n"
     "    expected = rows.replace(\",Verification,\", \",VerificationMethod,\").replace(\n"
     "        \",Attest,Drafted\", \",Vouch,Drafted\"\n"
     "    )\n"
     "    assert expected.count(\",Vouch,Drafted\") == 2\n"
     "    assert path.read_bytes() == (preamble + expected).encode(\"utf-8\")\n"
     "\n"
     "\n"
     "# --- the policy file -----------------------------------------------------------\n"),
    # the census of raw CSV readers
    ("tests/test_csv_header.py",
     "        \"carrier, so a reader that dropped the leading block would drop content\"\n"
     "    ),\n"
     "}\n",
     "        \"carrier, so a reader that dropped the leading block would drop content\"\n"
     "    ),\n"
     "    \"migrate_vocabulary.py\": (\n"
     "        \"it imports nothing from the kit, so that it runs whatever state the \"\n"
     "        \"kit's own scripts are in; it cuts the same leading `#` preamble off \"\n"
     "        \"itself (`_csv_preamble`) before any CSV parse, and keeps its bytes\"\n"
     "    ),\n"
     "}\n"),
    # the spine rows
    (LLR, "/_csv_edits/migrate_csv/", "/_csv_edits/_csv_preamble/migrate_csv/"),
    (LLR,
     "migrate_csv reads cell spans with _csv_records,",
     "migrate_csv keeps a byte-order mark and the leading run of blank and "
     "comment lines that _csv_preamble measures, the preamble the kit's CSV "
     "reader drops, then reads cell spans after it with _csv_records,"),
    (TC,
     "with a byte-order mark and a quoted header cell;",
     "with a byte-order mark, a quoted header cell and a leading comment "
     "preamble with a data line opening with the comment mark below it;"),
]
