"""CLI surface census: for each kit script, does it define main(), build an
argparse parser, how many flags / subcommands does it declare, and how many
distinct flag spellings exist across the kit."""
import ast
import sys
from pathlib import Path

root = Path(sys.argv[1])
scripts = sorted(p for p in root.glob("*.py"))
rows = []
all_flags = {}
subcmds = {}
for p in scripts:
    src = p.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(src)
    except SyntaxError:
        continue
    has_main = any(isinstance(n, ast.FunctionDef) and n.name == "main" for n in ast.walk(tree))
    has_guard = '__name__ == "__main__"' in src or "__name__ == '__main__'" in src
    uses_argparse = "argparse" in src
    flags = []
    positionals = []
    subs = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr == "add_argument" and n.args:
                a0 = n.args[0]
                if isinstance(a0, ast.Constant) and isinstance(a0.value, str):
                    if a0.value.startswith("-"):
                        flags.append(a0.value)
                        all_flags.setdefault(a0.value, set()).add(p.name)
                    else:
                        positionals.append(a0.value)
            if n.func.attr == "add_parser" and n.args:
                a0 = n.args[0]
                if isinstance(a0, ast.Constant):
                    subs.append(a0.value)
    if subs:
        subcmds[p.name] = subs
    loc = src.count("\n")
    rows.append((p.name, has_main, has_guard, uses_argparse, len(flags), len(positionals), len(subs), loc))

entry = [r for r in rows if r[1] and r[2]]
print(f"scripts scanned: {len(rows)}")
print(f"entry points (def main + __main__ guard): {len(entry)}")
print(f"entry points using argparse: {sum(1 for r in entry if r[3])}")
print(f"total flag declarations: {sum(r[4] for r in rows)}")
print(f"total positional declarations: {sum(r[5] for r in rows)}")
print(f"distinct flag spellings: {len(all_flags)}")
print(f"flags used by exactly one script: {sum(1 for v in all_flags.values() if len(v) == 1)}")
print(f"scripts with subcommands: {len(subcmds)}; total subcommands: {sum(len(v) for v in subcmds.values())}")
for k, v in sorted(subcmds.items()):
    print(f"  {k}: {len(v)} -> {v}")
print()
print("entry points sorted by flag count:")
for r in sorted(entry, key=lambda r: -r[4]):
    print(f"  {r[0]:34s} flags={r[4]:3d} pos={r[5]} subs={r[6]} loc={r[7]}")
print()
print("non-entry modules (no main+guard):")
for r in rows:
    if not (r[1] and r[2]):
        print(f"  {r[0]:34s} main={r[1]} guard={r[2]} loc={r[7]}")
