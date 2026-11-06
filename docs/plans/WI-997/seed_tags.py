#!/usr/bin/env python3
"""WI-997's seed: write each test-case evidence part into its test file as a tag.

Unshipped, one-time tooling, run from any directory with no arguments:

    python docs/plans/WI-997/seed_tags.py

A file-only part becomes a module-docstring tag, a `file::node` part a tag in
that test's docstring, and a parametrized part a tag on its test. The cell is
read by `kitlib.spine.evidence_items`, so free-text mentions are never a source.
A tag already present is left alone, so a re-run adds only what is missing.

It refuses and writes nothing on a node naming no test, a file that is no
Python test file, or a docstring form it does not handle.
"""

import ast
import io
import sys
import tokenize
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "project-trajectory" / "scripts"))

import check_trajectory  # noqa: E402
import gen_arch_map  # noqa: E402
import spine_carrier  # noqa: E402
from kitlib import spine  # noqa: E402

TC_REGISTRY = "docs/test/test-cases.toml"
QUOTES = b'"""'
OPENERS = {"(", "[", "{"}
CLOSERS = {")", "]", "}"}
DEF_STATEMENTS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


class Refused(Exception):
    """A part the seed cannot place."""


def wanted_tags(root, tests_dir):
    """`({path: {target: {TC id}}}, live ids)` from the evidence cells, `target`
    being `""` for a whole file and the node with any `[case]` dropped otherwise."""
    rows = spine_carrier.load(root / TC_REGISTRY, "TC-ID", False)
    prefix = Path(tests_dir.replace("\\", "/")).as_posix().rstrip("/") + "/"
    wanted = {}
    for row in rows:
        for path, node in spine.evidence_items(row.get("Evidence")):
            if path.startswith(prefix):
                targets = wanted.setdefault(path, {})
                targets.setdefault(node.split("[", 1)[0], set()).add(row["TC-ID"])
    return wanted, {row["TC-ID"] for row in rows}


def missing_tags(root, tests_dir):
    """`wanted_tags`, less each tag the shipped reader already finds."""
    wanted, live = wanted_tags(root, tests_dir)
    present, _findings = gen_arch_map.read_test_tags(root, tests_dir, live)
    for tc, nodes in present.items():
        for node in nodes:
            path, _sep, target = node.partition("::")
            wanted.get(path, {}).get(target, set()).discard(tc)
    missing = {}
    for path, targets in wanted.items():
        kept = {target: ids for target, ids in targets.items() if ids}
        if kept:
            missing[path] = kept
    return missing


def read_source(root, rel):
    """A test file's bytes, refused unless the seed can edit them as `\\n` lines."""
    path = root / rel
    if not path.is_file():
        raise Refused("no such file")
    is_test_file = path.stem.startswith("test_") or path.stem.endswith("_test")
    if path.suffix != ".py" or not is_test_file:
        raise Refused("not a Python test file")
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf") or b"\r\n" in data:
        raise Refused("carries a byte-order mark or CRLF")
    return data


def owners_by_target(tree):
    """`{target: [owner]}` for the file and every test the shipped reader reads."""
    owners = {"": [tree]}
    for owner, suffix in gen_arch_map._docstring_sites(tree, "", True):
        if suffix is not None:
            owners.setdefault(suffix[2:], []).append(owner)
    return owners


def tag_line(ids):
    """One `Implements:` line, its ids sorted numerically."""
    ordered = sorted(ids, key=lambda tc: int(tc.split("-")[1]))
    return "Implements: {}".format(", ".join(ordered)).encode("ascii")


def extend_docstring(lines, doc, tag):
    """`(edit, kind)` adding `tag` as `doc`'s last paragraph, the closing quotes on
    their own line. `ast` offsets are UTF-8 bytes, and `lines` are bytes."""
    first, last = doc.lineno - 1, doc.end_lineno - 1
    closing = doc.end_col_offset - len(QUOTES)
    well_formed = (
        lines[first][doc.col_offset :].startswith(QUOTES)
        and lines[last][closing : doc.end_col_offset] == QUOTES
        and not lines[first][: doc.col_offset].strip()
        and doc.value.strip()
    )
    if not well_formed:
        raise Refused("line {}: unhandled docstring form".format(doc.lineno))
    indent = b" " * doc.col_offset
    before = lines[last][:closing]
    if not before.strip():
        blank = [] if not lines[last - 1].strip() else [b""]
        return (last, last, blank + [indent + tag]), "closing quotes on their own line"
    trailer = lines[last][doc.end_col_offset :]
    new = [before.rstrip(), b"", indent + tag, indent + QUOTES + trailer]
    kind = "one-line" if first == last else "closing quotes after text"
    return (last, last + 1, new), kind


def header_end(tokens, owner):
    """The 1-based line holding the colon that closes `owner`'s def header."""
    depth = 0
    for token in tokens:
        if token.start[0] < owner.lineno or token.type != tokenize.OP:
            continue
        depth += (token.string in OPENERS) - (token.string in CLOSERS)
        if token.string == ":" and depth == 0:
            return token.start[0]
    raise Refused("line {}: no header colon".format(owner.lineno))


def new_docstring(tokens, owner, tag):
    """The edit giving a test with no docstring `tag` as its first statement, above
    any leading comment. A def or class next takes a blank line, for `ruff format`."""
    statement = owner.body[0]
    end = header_end(tokens, owner)
    starts = [statement.lineno]
    starts.extend(d.lineno for d in getattr(statement, "decorator_list", []))
    if min(starts) <= end:
        raise Refused("line {}: a one-line def".format(owner.lineno))
    new = [b" " * statement.col_offset + QUOTES + tag + QUOTES]
    if isinstance(statement, DEF_STATEMENTS):
        new.append(b"")
    return end, end, new


def tag_edit(lines, tokens, owner, tag):
    """`(edit, kind)` placing `tag` on `owner`, an edit being `(start, stop, lines)`
    over 0-based line indexes."""
    if ast.get_docstring(owner, clean=False) is not None:
        return extend_docstring(lines, owner.body[0].value, tag)
    if isinstance(owner, ast.Module):
        raise Refused("no module docstring")
    return new_docstring(tokens, owner, tag), "new test docstring"


def seed_file(root, rel, targets, counts):
    """The file's bytes with every tag in `targets` placed; `counts` takes each
    placement's kind."""
    data = read_source(root, rel)
    text = data.decode("utf-8")
    tree = ast.parse(data)
    tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    lines = data.split(b"\n")
    owners = owners_by_target(tree)
    edits = []
    for target, ids in sorted(targets.items()):
        found = owners.get(target, [])
        if len(found) != 1:
            label = target or "the module"
            raise Refused("{} names {} tests".format(label, len(found)))
        edit, kind = tag_edit(lines, tokens, found[0], tag_line(ids))
        edits.append(edit)
        counts[kind] += 1
        counts["module tags" if not target else "test tags"] += 1
    for start, stop, new in sorted(edits, key=lambda e: e[0], reverse=True):
        lines[start:stop] = new
    return b"\n".join(lines)


def main():
    tests_dir = check_trajectory._tests_dir(ROOT)
    counts = Counter()
    rewritten, refusals = {}, []
    for rel, targets in sorted(missing_tags(ROOT, tests_dir).items()):
        try:
            rewritten[rel] = seed_file(ROOT, rel, targets, counts)
        except Refused as exc:
            refusals.append("{}: {}".format(rel, exc))
    if refusals:
        print("seed_tags: refused, nothing written:")
        print("\n".join("  " + refusal for refusal in refusals))
        return 1
    for rel, data in rewritten.items():
        (ROOT / rel).write_bytes(data)
    print("seed_tags: {} file(s) written".format(len(rewritten)))
    for kind, count in sorted(counts.items()):
        print("  {}: {}".format(kind, count))
    return 0


if __name__ == "__main__":
    sys.exit(main())
