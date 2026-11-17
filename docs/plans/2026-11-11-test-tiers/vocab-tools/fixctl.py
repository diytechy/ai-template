"""Replace control characters a heredoc wrote into a rule file:
\x08 (from "\\b") back to a regex word edge, \x01 (from "\\1") to a group."""
import sys
from pathlib import Path

p = Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
n = t.count("\x08") + t.count("\x01")
t = t.replace("\x08", "\\b").replace("\x01", "\\1")
p.write_text(t, encoding="utf-8")
print("fixed", n)
