#!/usr/bin/env python3
"""Test-file tags against test cases, and the evidence column generated from them.

The test-file tag rule (`tc_tag_findings`) reports each refused tag, each
difference between a test case's tags and its `Evidence` cell, and each
accepted automated case no test declares. The evidence column is generated
from the same tags (`generated_evidence`, `evidence_regen`, `write_evidence`):
a cell's test-file parts follow the tags, and its other parts stay as written.
Their inputs come from `arch_inputs`; ``trajectory_arch`` re-exports them for
``check_trajectory``. The `Implements:`-tag crosscheck against a design row's
`Module` and `CodeSymbol` cells retired with the cells (WI-1023): a design row
names no file or symbol, and the files realizing it are read up from the tags
(`arch_inputs.implements_index`).

Component: CMP-006

The tag rule surface ``trajectory_arch`` re-exports.
`tc_tag_findings(root, tests_dir)` returns each refused tag as
`<file>:<line>: <shape>: <detail>`, then the tag and evidence differences,
then the accepted automated cases no test declares, `[]` with no test-case
registry. `evidence_regen(root, tests_dir)` returns `{TC id: (before, after)}`
for each cell the tags would change, and `write_evidence(root, tests_dir)`
writes those cells and nothing else into the test-case registry. They read
`gen_arch_map`'s walks; only `write_evidence` writes.
"""

import sys
from pathlib import Path

try:
    from kitlib import spine as _kitspine
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib import spine as _kitspine

import spine_carrier
from arch_inputs import TC_CSV

try:
    import gen_arch_map
except ImportError:
    try:  # pragma: no cover - in-process fallback
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import gen_arch_map
    except ImportError:
        gen_arch_map = None


# Test-file tags and `Evidence` cells are one fact: the cell's test-file parts
# are generated from the tags (`generated_evidence`, below), and this check is
# what "checked current" reads. The generator is the identity exactly when the
# parts equal the tags, so a cell this check passes is the generated cell.
def _tag_evidence_findings(rows, tags, refused, tests_dir):
    """Each difference between a live TC's tags and its `Evidence` parts under
    `tests_dir`, as `<TC>: evidence without a tag: <node>` or `<TC>: tag without
    evidence: <node>`, sorted by TC, then node.

    `rows` are the live TC rows, `tags` is `read_test_tags`' map, and `refused`
    holds the files it could not read, whose parts name nothing it could see, so
    they add no finding here. A part is its path, or its path and node with any
    `[case]` dropped; a part outside `tests_dir` is outside the rule.

    Implements: SR-157, LLR-366"""
    prefix = "".join(p + "/" for p in Path(tests_dir.replace("\\", "/")).parts)
    found = []
    for row in rows:
        tc = (row.get("TC-ID") or "").strip()
        parts = {
            path + "::" + node.split("[", 1)[0] if node else path
            for path, node in _kitspine.evidence_items(row.get("Evidence"))
            if path.startswith(prefix) and path not in refused
        }
        declared = set(tags.get(tc, ()))
        found += [(tc, n, "evidence without a tag") for n in parts - declared]
        found += [(tc, n, "tag without evidence") for n in declared - parts]
    return ["{}: {}: {}".format(tc, kind, n) for tc, n, kind in sorted(found)]


def _undeclared_case_findings(rows, tags, refused):
    """`<TC>: no test declares it` for each accepted or founded case whose
    `Automated` cell reads `yes`, stripped and case-folded as `trace.py` reads
    it, that no tag in `tags` names, sorted by TC.

    The cell decides nothing else: a note, no cell, a part outside the tests
    root and a path the tree lacks all read the same. A case with an `Evidence`
    part in a file `refused` as unreadable adds nothing, since that file's
    refusal is already a finding. It reads declarations only, so a tagged test
    still failing is clean here. It stays when the equality check retires.

    Implements: SR-157, LLR-395"""
    found = []
    for row in rows:
        tc = (row.get("TC-ID") or "").strip()
        owed = _kitspine.is_accepted(row) or _kitspine.is_founded(row)
        owed = owed and (row.get("Automated") or "").strip().casefold() == "yes"
        if not owed or tags.get(tc):
            continue
        parts = _kitspine.evidence_items(row.get("Evidence"))
        if not any(path in refused for path, _node in parts):
            found.append(tc)
    return ["{}: no test declares it".format(tc) for tc in sorted(found)]


def tc_tag_findings(root, tests_dir):
    """Each refused test-file tag under `tests_dir`, the declared tests root, as
    a `<file>:<line>: <shape>: <detail>` string, then each difference between the
    tags and the `Evidence` cells (`_tag_evidence_findings`), then each accepted
    automated case no tag declares (`_undeclared_case_findings`).
    `check_trajectory` owns the declared-root read, so the value is handed in.

    `[]` (vacuous) with no TC registry, and with no tests root, which
    `read_test_tags` walks as no files and the comparison must not read as every
    part untagged. `[arch-map] mode = files` is no reason to be vacuous: this
    reads test files, not the source surface. A registry holding only `-000` rows
    is not vacuous either, so every tag there is unknown. No `hasattr` guard,
    unlike the other architecture rules' `gen_arch_map` reads: a stale sibling
    must fail loudly, since "no tags" is the reading this rule refuses. A
    placeholder row is not loaded, so it owes no declaration.

    Implements: SR-157, LLR-365, LLR-366"""
    if gen_arch_map is None or spine_carrier.resolve(root / TC_CSV) is None:
        return []
    rows = spine_carrier.load(root / TC_CSV, "TC-ID", False)
    live_tcs = {(r.get("TC-ID") or "").strip() for r in rows}
    tags, findings = gen_arch_map.read_test_tags(root, tests_dir, live_tcs)
    lines = [
        "{}:{}: {}: {}".format(f["file"], f["line"], f["shape"], f["detail"])
        for f in findings
    ]
    if (root / tests_dir).is_dir():
        refused = {f["file"] for f in findings if f["shape"] == "unreadable"}
        lines += _tag_evidence_findings(rows, tags, refused, tests_dir)
        lines += _undeclared_case_findings(rows, tags, refused)
    return lines


# --- The evidence column, generated from the tags (WI-1023) ------------------
# A test case's `Evidence` cell names its tests, and the tests name their case:
# two homes of one fact. The test-file half is generated from the tags, read
# as LLR-366 reads it, and everything else the cell says stays authored and is
# kept as written: a part outside the declared tests root (a CI workflow, an
# inspection or review record), a parenthetical note, and a part in a file the
# tag reader refused as unreadable, whose declarations nobody can see.


def _tests_prefix(tests_dir):
    """The declared tests root as the path prefix its parts start with; `""`
    for a root of `.`, which holds every part (LLR-366's reading)."""
    return "".join(p + "/" for p in Path(tests_dir.replace("\\", "/")).parts)


def _drop_span(cell, start, end):
    """`cell` without the token at `start:end` and the separator after it, or,
    for the last token, the separator before it."""
    after = end + len(cell[end:]) - len(cell[end:].lstrip(" \t\n;"))
    if after < len(cell):
        return cell[:start] + cell[after:]
    head = cell[:start].rstrip(" \t\n;")
    return head + cell[after:]


def generated_evidence(cell, tagged, tests_dir, refused=()):
    """One test case's `Evidence` cell as the tags make it.

    `tagged` is the case's declared nodes (`read_test_tags`' map, one case's
    set), `tests_dir` the declared tests root and `refused` the files the tag
    reader could not read. A tests-root part a tag declares is kept as written,
    a parametrized case included; one no tag declares is dropped with its
    separator; a declared node the cell lacks is appended, `; `-joined and
    sorted. Every other part, every note and every part in a refused file stays
    verbatim. The identity whenever the parts equal the tags.

    Implements: SR-251, LLR-406"""
    prefix = _tests_prefix(tests_dir)
    cell = cell or ""
    present, drops = set(), []
    for token, start, end in _kitspine.evidence_spans(cell):
        if token.startswith("("):
            continue
        path, _sep, node = token.partition("::")
        path = path.split("#", 1)[0].replace("\\", "/")
        if not path.startswith(prefix) or path in refused:
            continue
        part = path + "::" + node.split("[", 1)[0] if node else path
        if part in tagged:
            present.add(part)
        else:
            drops.append((start, end))
    for start, end in reversed(drops):
        cell = _drop_span(cell, start, end)
    added = sorted(set(tagged) - present)
    if not added:
        return cell
    kept = cell.rstrip(" \t\n;")
    return "; ".join(([kept] if kept else []) + added)


def evidence_input_missing(root, tests_dir):
    """What the evidence regeneration has nothing to read from, as a phrase
    naming it (`no test-case registry at ...`, `no tests root at ...`), or `""`
    when both inputs are there. The one test of both: `evidence_regen` reads
    nothing without them, and the regeneration command reports the phrase
    rather than calling every cell current.

    Implements: SR-251, LLR-406"""
    if spine_carrier.resolve(Path(root) / TC_CSV) is None:
        return "no test-case registry at {}".format(TC_CSV)
    if not (Path(root) / tests_dir).is_dir():
        return "no tests root at {}".format(tests_dir)
    return ""


def evidence_regen(root, tests_dir):
    """`{TC id: (before, after)}` for each live test case whose `Evidence`
    cell the tags would change (`generated_evidence`), `{}` when every cell is
    current, or when an input is missing (`evidence_input_missing`).

    Implements: SR-251, LLR-406"""
    if gen_arch_map is None or evidence_input_missing(root, tests_dir):
        return {}
    rows = spine_carrier.load(root / TC_CSV, "TC-ID", False)
    live = {(r.get("TC-ID") or "").strip() for r in rows}
    tags, findings = gen_arch_map.read_test_tags(root, tests_dir, live)
    refused = {f["file"] for f in findings if f["shape"] == "unreadable"}
    out = {}
    for row in rows:
        tc = (row.get("TC-ID") or "").strip()
        before = row.get("Evidence") or ""
        after = generated_evidence(before, set(tags.get(tc, ())), tests_dir, refused)
        if after != before:
            out[tc] = (before, after)
    return out


_TOML_DELIMS = ('"""', "'''")


def _extend(keys, tables, last, end):
    """Stretch key `last`'s span, and its table's, to end before line `end`."""
    keys[last] = (keys[last][0], end)
    tables[last[0]] = (tables[last[0]][0], end)


def _table_spans(lines):
    """`{table header: (first key line, end)}` over a TOML text's lines, and
    `{(table header, key): (start, end)}` for each top-level key, multi-line
    strings tracked so a line inside one is data, never a key or a header."""
    tables, keys = {}, {}
    header, last, open_delim = None, None, None
    for i, line in enumerate(lines):
        if open_delim is not None:
            if line.count(open_delim) % 2:
                open_delim = None
                _extend(keys, tables, last, i + 1)
            continue
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            header = stripped
            tables[header] = (i + 1, i + 1)
        elif header is not None and "=" in stripped and not stripped.startswith("#"):
            last = (header, stripped.split("=", 1)[0].strip())
            keys[last] = (i, i + 1)
            _extend(keys, tables, last, i + 1)
            open_delim = next((d for d in _TOML_DELIMS if line.count(d) % 2), None)
    return tables, keys


def write_evidence(root, tests_dir):
    """Write each changed cell `evidence_regen` returns into the test-case
    registry in place, and return the ids written, sorted. Only those `evidence`
    lines move; every other byte, comments, order and newline style included,
    is kept. A cell that becomes empty leaves its key (an empty cell is an
    absent key); a case with none gains one after its last key. The rewrite is
    re-read and refused, writing nothing, unless it parses to the same rows
    with exactly those cells changed.

    Implements: SR-251, LLR-406"""
    changed = evidence_regen(root, tests_dir)
    if not changed:
        return []
    path = spine_carrier.resolve(root / TC_CSV)
    if path.suffix != ".toml":
        raise SystemExit(
            "arch_tags: the evidence column is written into the TOML carrier "
            "only; convert {} first (scripts/migrate_carrier.py)".format(path)
        )
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        raw = fh.read()
    eol = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.split(eol)
    tables, keys = _table_spans(lines)
    edits = []
    for tc, (_before, after) in changed.items():
        header = "[{}.{}]".format(spine_carrier.REGISTRY_TABLE["TC-ID"], tc)
        new = ["evidence = " + _kitspine.toml_string(after)] if after else []
        if (header, "evidence") in keys:
            edits.append(keys[(header, "evidence")] + (new,))
        elif header in tables:
            edits.append((tables[header][1], tables[header][1], new))
    for start, end, new in sorted(edits, reverse=True):
        lines[start:end] = new
    text = eol.join(lines)
    expected = spine_carrier.rows_from_text(raw, "TC-ID", ".toml") or {}
    for tc, (_before, after) in changed.items():
        expected[tc].pop("Evidence", None)
        if after:
            expected[tc]["Evidence"] = after
    if spine_carrier.rows_from_text(text, "TC-ID", ".toml") != expected:
        raise SystemExit(
            "arch_tags: REFUSED - the evidence rewrite of {} did not re-read as "
            "the generated cells and nothing else; nothing written".format(path)
        )
    path.write_text(text, encoding="utf-8", newline="")
    return sorted(changed)


def evidence_regen_report(root, tests_dir):
    """Regenerate the evidence column (`write_evidence`) and say what happened,
    as the one line the regeneration command prints: the cases written, that
    every cell is current, or, with an input missing (`evidence_input_missing`),
    that nothing was regenerated or written and which input it lacks.

    Implements: SR-251, LLR-406"""
    missing = evidence_input_missing(root, tests_dir)
    if missing:
        return "nothing regenerated - {}; nothing written".format(missing)
    written = write_evidence(root, tests_dir)
    if not written:
        return "every evidence cell is current"
    return "evidence regenerated for {}".format(", ".join(written))
