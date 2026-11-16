"""Add the spine tags to the migrator's public functions and to its tests.

`Implements: SR-247, LLR-369` closes the docstring of each function the design
row names as an entry point; `Implements: TC-427` opens each test's docstring.
Idempotent.
"""

import re
from pathlib import Path

ROOT = Path(r"C:\Projects\ai-template-wt-vocabulary")
SCRIPT = ROOT / "project-trajectory/scripts/migrate_vocabulary.py"
TESTS = ROOT / "tests/test_migrate_vocabulary.py"
TAG = "Implements: SR-247, LLR-369"
ENTRY = ("bindings", "migrate_toml", "migrate_csv", "registries", "main")


def tag_script():
    text = SCRIPT.read_bytes().decode("utf-8")
    for name in ENTRY:
        m = re.search(r'^def %s\(.*?\):\n    """(.*?)"""' % re.escape(name), text, re.S | re.M)
        if not m:
            raise SystemExit("no docstring found for " + name)
        if TAG in m.group(1):
            continue
        body = m.group(1).rstrip()
        new_doc = '"""' + body + "\n\n    " + TAG + '\n    """'
        text = text[: m.start()] + m.group(0).replace('"""' + m.group(1) + '"""', new_doc) + text[m.end() :]
    SCRIPT.write_bytes(text.encode("utf-8"))


def tag_tests():
    lines = TESTS.read_bytes().decode("utf-8").split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if line.startswith("def test_"):
            # the signature may span lines; find its end
            j = i
            while not lines[j].rstrip().endswith(":"):
                j += 1
                out.append(lines[j])
            nxt = lines[j + 1] if j + 1 < len(lines) else ""
            if "Implements: TC-427" not in nxt:
                out.append('    """Implements: TC-427"""')
            i = j
        i += 1
    TESTS.write_bytes("\n".join(out).encode("utf-8"))


if __name__ == "__main__":
    tag_script()
    tag_tests()
    print("tagged")
