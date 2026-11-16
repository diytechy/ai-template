"""Write TC-427's evidence cell: every test of the migrator, by node id.

A test tagged `Implements: TC-427` must be named in that test case's evidence
cell (handoff trap 3); the file's path alone does not satisfy
check_trajectory. Run again whenever a test is added to the file.
"""

import re
from pathlib import Path

ROOT = Path(r"C:\Projects\ai-template-wt-vocabulary")
TESTS = "tests/test_migrate_vocabulary.py"
REGISTRY = ROOT / "docs/test/test-cases.toml"

names = re.findall(r"^def (test_\w+)\(", (ROOT / TESTS).read_text(encoding="utf-8"), re.M)
cell = "; ".join("{}::{}".format(TESTS, name) for name in names)
text = REGISTRY.read_bytes().decode("utf-8")
head = text.index("[test.TC-427]")
start = text.index('evidence = "', head)
end = text.index('"', start + len('evidence = "'))
new = text[:start] + 'evidence = "' + cell + text[end:]
REGISTRY.write_bytes(new.encode("utf-8"))
print("TC-427 evidence: {} test(s)".format(len(names)))
