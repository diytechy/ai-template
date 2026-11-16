"""Replace a literal U+FEFF inside the migrator and its tests with the escape,
so the byte-order mark the code strips is visible in the source."""

from pathlib import Path

ROOT = Path(r"C:\Projects\ai-template-wt-vocabulary")
BOM = chr(0xFEFF)
ESCAPE = chr(92) + "ufeff"
for rel in ("project-trajectory/scripts/migrate_vocabulary.py", "tests/test_migrate_vocabulary.py"):
    path = ROOT / rel
    text = path.read_bytes().decode("utf-8")
    n = text.count(BOM)
    if n:
        path.write_bytes(text.replace(BOM, ESCAPE).encode("utf-8"))
    print(rel, n)
