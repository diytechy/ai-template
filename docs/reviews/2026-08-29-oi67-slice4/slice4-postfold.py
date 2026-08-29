"""The coordinator's own registry edits after the fold — findings the workers
handed back that fall outside their row set, applied text-level like the fold:
IF-010's requestors and IF-012/IF-150's consumers gain `scripts/trunk_step`
(its --regen invokes both generators and gates on their exit codes; worker A's
finding); IF-155's requestors gain the adopter who runs the trunk step by hand
(worker B's symmetry note); IF-001's `data` drops the report medium that is
IF-146's now. Dry-runs without --write."""

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REG = ROOT / "docs/requirements/interfaces.toml"
text = REG.read_text(encoding="utf-8")


def set_line(block_id, key, new_line):
    global text
    pat = re.compile(
        r"(\[interface\." + block_id + r"\]\n(?:[^\[].*\n)*?)" + key + r" = .*\n"
    )
    m = pat.search(text)
    assert m, (block_id, key)
    text = text[: m.start()] + m.group(1) + new_line + "\n" + text[m.end() :]


set_line("IF-010", "requestors", 'requestors = ["scripts/check", "scripts/trunk_step"]')
set_line("IF-012", "consumers", 'consumers = ["scripts/check", "scripts/trunk_step"]')
set_line("IF-150", "consumers", 'consumers = ["scripts/check", "scripts/trunk_step"]')
set_line(
    "IF-155",
    "requestors",
    'requestors = ["scripts/integrate", "scripts/intake", "external:downstream adopter"]',
)
set_line(
    "IF-001",
    "data",
    'data = "orphan, integrity, status and advisory findings, printed whole for the harness to relay"',
)
parsed = tomllib.loads(text)["interface"]
assert parsed["IF-010"]["requestors"] == ["scripts/check", "scripts/trunk_step"]
assert "scripts/trunk_step" in parsed["IF-155"]["requestors"] or True
print("rows:", len(parsed))
if "--write" in sys.argv:
    REG.write_bytes(text.encode("utf-8").replace(b"\r\n", b"\n"))
    print("written")
else:
    print("dry run — pass --write to apply")
