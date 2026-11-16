"""Apply one concept's rename rules to the vocabulary worktree.

  python vapply.py RULES.py [--dry] [--review OUT.txt]

RULES.py defines any of:
  TOKENS  = {old: new}      whole identifiers ([A-Za-z0-9_] on both sides is a no-match)
  PARTS   = {old: new}      snake/kebab parts (underscore and hyphen count as edges)
  REGEX   = [(pattern, repl), ...]            applied in order, after the two maps
  SCOPED  = [(glob, pattern, repl), ...]      regex limited to paths matching glob
  SKIP    = [glob, ...]     live paths this concept leaves alone
  EXTRA   = [glob, ...]     non-live paths this concept does touch
  PROTECT = [regex, ...]    spans never rewritten (record names, external flags)

Every changed line is written to the review file as old/new pairs, so the
change can be read line by line before anything else builds on it.
"""

import fnmatch
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\ai-template-wt-vocabulary")
sys.path.insert(0, str(ROOT / "project-trajectory" / "scripts"))
import check_vocab  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Never a working surface for a sweep, whatever a rule file says.
ALWAYS_SKIP = (
    "OWNER_SCRATCHPAD.md",
    "OPERATOR_SCRATCHPAD.md",
    "project-trajectory/RESYNC_PACK.md",  # dated entries: history of what changed
    "docs/plans/*",
    "PROJECT_STATE.html",
)


def _match(rel, globs):
    for g in globs:
        if fnmatch.fnmatch(rel, g):
            return True
        if g.endswith("/*") and rel.startswith(g[:-1]):
            return True
    return False


def tracked():
    return subprocess.run(
        ["git", "-C", str(ROOT), "ls-files"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    ).stdout.splitlines()


def scope(rules):
    skip = tuple(getattr(rules, "SKIP", ())) + ALWAYS_SKIP
    extra = tuple(getattr(rules, "EXTRA", ()))
    for rel in tracked():
        path = ROOT / rel
        if not path.is_file() or _match(rel, ALWAYS_SKIP):
            continue
        if _match(rel, extra):
            yield rel, path
            continue
        if _match(rel, skip):
            continue
        if check_vocab.in_scope(path, ROOT)[1] == "LIVE":
            yield rel, path


# A name inside a Python string literal often follows an escape: "...\nname = 1".
# The `n` of `\n` is a letter, so a plain word edge misses it (it missed eight
# fixtures in the Vouch concept). An escape counts as an edge.
_ESC = r"|(?<=\\n)|(?<=\\t)|(?<=\\r)"


def compile_rules(rules):
    steps = []
    for old, new in sorted(getattr(rules, "TOKENS", {}).items(), key=lambda kv: -len(kv[0])):
        steps.append((None, re.compile(r"(?:(?<![A-Za-z0-9_])" + _ESC + ")" + re.escape(old) + r"(?![A-Za-z0-9_])"), new))
    for old, new in sorted(getattr(rules, "PARTS", {}).items(), key=lambda kv: -len(kv[0])):
        steps.append((None, re.compile(r"(?:(?<![A-Za-z0-9])" + _ESC + ")" + re.escape(old) + r"(?![A-Za-z0-9])"), new))
    for pat, repl in getattr(rules, "REGEX", ()):
        steps.append((None, re.compile(pat), repl))
    for glob, pat, repl in getattr(rules, "SCOPED", ()):
        steps.append((glob, re.compile(pat), repl))
    return steps


def rewrite_line(line, steps, rel, protect):
    if not protect:
        out = line
        for glob, pat, repl in steps:
            if glob is None or _match(rel, (glob,)):
                out = pat.sub(repl, out)
        return out
    # Split the line into protected and free spans; rewrite only the free ones.
    spans, pos = [], 0
    for m in protect.finditer(line):
        if m.start() > pos:
            spans.append((False, line[pos : m.start()]))
        spans.append((True, m.group(0)))
        pos = m.end()
    spans.append((False, line[pos:]))
    out = []
    for kept, text in spans:
        if not kept:
            for glob, pat, repl in steps:
                if glob is None or _match(rel, (glob,)):
                    text = pat.sub(repl, text)
        out.append(text)
    return "".join(out)


def main():
    args = sys.argv[1:]
    dry = "--dry" in args
    review = None
    if "--review" in args:
        review = Path(args[args.index("--review") + 1])
    spec = importlib.util.spec_from_file_location("rules", args[0])
    rules = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rules)
    steps = compile_rules(rules)
    protect_pats = list(getattr(rules, "PROTECT", ()))
    protect = re.compile("|".join("(?:%s)" % p for p in protect_pats)) if protect_pats else None

    # A new name that already exists names something else (handoff trap 12):
    # say so before anything is written.
    new_names = {}
    for table in ("TOKENS", "PARTS"):
        for old, new in getattr(rules, table, {}).items():
            edge = "A-Za-z0-9_" if table == "TOKENS" else "A-Za-z0-9"
            new_names[new] = re.compile("(?<![%s])%s(?![%s])" % (edge, re.escape(new), edge))
    taken = {}
    if new_names and "--no-collide" not in args:
        for rel, path in scope(rules):
            try:
                text = path.read_bytes().decode("utf-8")
            except UnicodeDecodeError:
                continue
            for new, pat in new_names.items():
                n = len(pat.findall(text))
                if n:
                    taken.setdefault(new, []).append((rel, n))
    for new, where in sorted(taken.items()):
        print("ALREADY IN USE: {} ({} occurrence(s) in {} file(s), e.g. {})".format(
            new, sum(n for _r, n in where), len(where), where[0][0]))
    if taken and not dry and "--force" not in args:
        print("NOTHING WRITTEN: resolve the names above, or pass --force once each is read.")
        return 1

    changed_files, changed_lines, log = 0, 0, []
    for rel, path in scope(rules):
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        lines = text.split("\n")
        new_lines, hits = [], []
        for i, line in enumerate(lines, 1):
            new = rewrite_line(line, steps, rel, protect)
            if new != line:
                hits.append((i, line, new))
            new_lines.append(new)
        if not hits:
            continue
        changed_files += 1
        changed_lines += len(hits)
        log.append("=== {} ({})".format(rel, len(hits)))
        for i, old, new in hits:
            log.append("{}:{}".format(rel, i))
            log.append("  - " + old.strip())
            log.append("  + " + new.strip())
        if not dry:
            path.write_bytes("\n".join(new_lines).encode("utf-8"))
    if review:
        review.write_text("\n".join(log) + "\n", encoding="utf-8")
    print("{}: {} file(s), {} line(s){}".format(
        Path(args[0]).name, changed_files, changed_lines, " (dry run)" if dry else ""))


if __name__ == "__main__":
    main()
