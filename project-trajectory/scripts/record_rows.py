"""record_rows.py — the acceptance record written and judged row by row (WI-1060).

An acceptance act used to copy each registry it wrote whole, so it carried every
row of the file as it then stood, and the writer refused the act while any row
it did not name had drifted. That kept the record to what someone saw, but it
coupled every row of a file: one unblessed amendment held every blessed one in
its registry. An act now writes a registry's copy ROW BY ROW, and this module is
the one statement of what it writes, read by the writer (`baseline_snapshot`)
and by the judge (`acceptance_record`'s two mirror rules) alike. It imports
neither: the caller passes in the cell comparison (`split_changed_cells`), so
no import edge or cycle joins the writer and its judge.

THE RULE (`row_rule`). A row the act names (its status moved into acceptance,
it arrived accepted, or the re-accept option names it) takes its live text, or
leaves the copy when live no longer carries it (a retirement). A row the act
does not name FOLLOWS LIVE when its live text claims no acceptance (or, gone
from live, its recorded copy claimed none), or when its recorded copy and its
live text both claim acceptance and neither its accepted cells nor its ROUTED
traced cells (`ROUTED_TRACED_CELLS`: the traced cells whose change routes to
adjudication) differ, which refreshes its other traced cells. Every other row
the act does not name keeps its recorded text, or stays out of the copy when it
has none: those are the rows the act leaves owed. A template example row (an id
ending `-000`), which no reader of the record reads, follows live whatever its
status.

THE BYTES (`row_segments`, `expected_copy`). A registry text is a head (every
byte before the first row's table header), rows, and a tail (every byte after
the last row's last cell line). A row is its leading blank and whole-line
comment lines (none for the first row), its header and its cells up to its last
cell line, comments inside it included; line terminators belong to the line
they end. The copy an act writes keeps live's head and tail, holds its rows in
live order with each row's bytes taken whole from the side the rule names, and
places a kept row live no longer carries after the row it followed in the
previous copy. So an act that keeps no row writes the live file byte for byte,
and a record stays a plain diff away from live. A text that will not split into
rows each reading alone as the row the whole file holds is refused, never
guessed at. A legacy carrier (CSV, or the needs file's markdown) is copied
whole when no row would be kept, and refused otherwise.

THE READINGS. `row_problems` reads a written copy against the rule by parsing
it, independent of the composition, which is how the writer re-reads its own
result before writing anything (`act_copy`); `copy_problems` is the judge's
comparison, bytes first, naming each row when they differ. The judge reads the
trees through `tree_acts` (which rows each writing commit's act names, and
whether its record is judged row by row: its act ledger holds an entry
carrying `kept`), `written_problems` (one copy at the row) and
`whole_file_faults` (a copy written whole, judged as written), each handed the
judge's own readers so this module imports no sibling but the carrier. Since a
copy's last writer may be another reviewer's act that kept a row,
`acting_rev` reads who accepted a row from the act ledger's history instead.

Component: CMP-006
"""

import tomllib
from pathlib import PurePosixPath

try:
    import spine_carrier
    from kitlib import git as _kitgit
    from kitlib import spine as _kitspine
except ImportError:  # pragma: no cover - in-process fallback
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier
    from kitlib import git as _kitgit
    from kitlib import spine as _kitspine

# The traced cells that ROUTE to adjudication rather than staying silent
# (§A5.1 for `SN-Refs`/`Verifies`; the WI-388 ruling for LLR `SR-Refs`; WI-442
# for `Boundary-Refs` — the rulings are recorded at
# `acceptance_record.SPINE_TRACED_CELLS`, the cell-split table's home). Keyed
# per registry so a same-named column elsewhere never rides in. Moved here from
# `intake.py` at WI-1060, which keeps the name as an alias: the trunk mint reads
# it to decide what to mint, and the record reads it to decide what an act may
# refresh without naming the row, so both the writer and the judge need it and
# neither may import the lifecycle module that held it. `Constrains` (WI-1024)
# routes too: whether a row's text states the behaviour across the interface it
# names is the adjudication's question.
# Implements: SR-207, LLR-245, SR-178, LLR-420
ROUTED_TRACED_CELLS = {
    "docs/requirements/system-requirements.toml": frozenset(
        {"SN-Refs", "Boundary-Refs", "Constrains"}
    ),
    "docs/requirements/low-level-requirements.toml": frozenset(
        {"SR-Refs", "Constrains"}
    ),
    "docs/test/test-cases.toml": frozenset({"Verifies"}),
}

# Every row table a registry carries, mapped to its tier's id column, so a row
# is keyed `(id column, id)` whichever carrier it was read from.
_TIER_OF_TABLE = {table: col for col, table in spine_carrier.REGISTRY_TABLE.items()}


class RowRecordError(ValueError):
    """A registry text this module cannot read or compose row by row: it does
    not parse, holds a table that is no tier's, will not split into whole rows,
    or sits on a legacy carrier where a row would be kept. The writer refuses
    the act on it; the judge reports it."""


def _lines(text):
    """`text`'s lines, each keeping its own terminator; split on `\\n` alone,
    so a `\\r` or a Unicode line separator inside a cell is never a break."""
    out, start = [], 0
    while start < len(text):
        end = text.find("\n", start)
        end = len(text) if end < 0 else end + 1
        out.append(text[start:end])
        start = end
    return out


def _header(line):
    """`(table, id)` when `line` is a row's table header (`[table.ID]`, the id
    bare or quoted), else None."""
    body = line.strip()
    if not (body.startswith("[") and body.endswith("]")) or body.startswith("[["):
        return None
    table, dot, rid = body[1:-1].partition(".")
    if not dot or not table.replace("_", "").isalnum():
        return None
    if rid.startswith('"') and rid.endswith('"') and len(rid) > 1:
        rid = rid[1:-1]
    return (table, rid) if rid and '"' not in rid else None


def _filler(line):
    """A blank line or a whole-line comment."""
    body = line.strip()
    return not body or body.startswith("#")


def row_segments(text):
    """`(head, [((id column, id), row text)], tail)` of a TOML registry text,
    validated: the parts concatenate to `text`, each row reads alone as exactly
    the row the whole text holds under its id, every row the text holds is one
    of them, and the head and tail hold no table or key. Raises
    `RowRecordError` otherwise (a header-looking line inside a multi-line
    string, a non-row table, a dotted key), so a text is never split by guess.

    Implements: SR-207, LLR-245"""
    lines = _lines(text)
    starts = [i for i, line in enumerate(lines) if _header(line)]
    if not starts:
        return text, [], ""
    rows, begin = [], starts[0]
    for n, at in enumerate(starts):
        stop = starts[n + 1] if n + 1 < len(starts) else len(lines)
        end = max(k for k in range(at, stop) if k == at or not _filler(lines[k])) + 1
        table, rid = _header(lines[at])
        rows.append(((_tier_col(table), rid), "".join(lines[begin:end])))
        begin = end
    head, tail = "".join(lines[: starts[0]]), "".join(lines[begin:])
    _check_split(text, head, rows, tail)
    return head, rows, tail


def _tier_col(table):
    """The id column of the tier whose rows live under `table`."""
    if table not in _TIER_OF_TABLE:
        raise RowRecordError("table [{}] is no registry tier's".format(table))
    return _TIER_OF_TABLE[table]


def _parse(text):
    try:
        return tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise RowRecordError("it does not parse as TOML ({})".format(exc)) from None


def _check_split(text, head, rows, tail):
    """Refuse a split that is not the text's own rows, read whole."""
    whole = _parse(text)
    held = {
        (_tier_col(t), rid): cells
        for t, table in whole.items()
        if isinstance(table, dict)
        for rid, cells in table.items()
    }
    if _parse(head) or _parse(tail) or len(held) != len(rows):
        raise RowRecordError("its text does not split into whole rows")
    for key, segment in rows:
        alone = _parse(segment)
        table = spine_carrier.REGISTRY_TABLE[key[0]]
        if list(alone) != [table] or alone[table] != {key[1]: held.get(key)}:
            raise RowRecordError(
                "{} does not read alone as the row the file holds".format(key[1])
            )


def file_rows(text, suffix):
    """`{(id column, id): row}` of every row a registry text holds, under
    today's column names, whichever carrier `suffix` names. A TOML text that
    does not parse, or holds a table that is no tier's, raises
    `RowRecordError`.

    Implements: SR-207, LLR-245"""
    if suffix == ".toml":
        cols = [_tier_col(t) for t in _parse(text)]
    elif suffix == ".md":
        cols = ["SN-ID"]
    else:
        header = _kitspine.csv_reader(text.lstrip("﻿")).fieldnames or []
        cols = [c for c in header if c in _TIER_OF_TABLE.values()]
    out = {}
    for col in cols:
        rows = spine_carrier.tier_rows_from_text(text, col, suffix) or {}
        out.update({(col, rid): row for rid, row in rows.items()})
    return out


def readable(pair):
    """`pair` (`(text, suffix)`) when it reads as a registry, else None: a
    previous copy that does not parse is read as no copy, as the writer's
    repair of such a record reads it.

    Implements: SR-179, LLR-178"""
    if pair is None:
        return None
    try:
        file_rows(*pair)
    except RowRecordError:
        return None
    return pair


def _settled(rel, col, before, after, split):
    """Do the accepted cells and the routed traced cells of a row equal its
    recorded copy's? `split` is the cell comparison the caller owns."""
    changed = split(rel, col, before, after)
    routed = {spine_carrier.stem(k): v for k, v in ROUTED_TRACED_CELLS.items()}
    return not changed["accepted"] and not (
        set(changed["traced"]) & routed.get(spine_carrier.stem(rel), frozenset())
    )


def row_rule(rel, prev, live, named, split):
    """`{(id column, id): "live" | "record" | None}` for every row of `prev`
    (the previous copy's rows) and `live`: where the act's copy takes each row
    from, None for a row it leaves out. `named` is the ids the act names. The
    rule this module's docstring states, in one place.

    Implements: SR-207, LLR-245"""
    return {
        key: _source(rel, key, prev.get(key), live.get(key), named, split)
        for key in set(prev) | set(live)
    }


def _source(rel, key, before, after, named, split):
    """`row_rule` for one row: "live", "record", or None for a row the copy
    leaves out. Split out so the rule reads as one ordered list of cases.

    Implements: SR-207, LLR-245"""
    claims = _kitspine.claims_acceptance
    if key[1] in named or _kitspine.is_example(key[1]):
        # A named row, or a `-000` template row no reader of the record reads
        # whatever its status: taken from live, or retired with it.
        return "live" if after is not None else None
    if after is None:
        return "record" if claims(before) else None
    if not claims(after):
        return "live"
    if before is None or not claims(before):
        return "record" if before is not None else None
    return "live" if _settled(rel, key[0], before, after, split) else "record"


def kept_ids(sources, prev, live):
    """The ids the act leaves at a recorded text that differs from live, or
    that live no longer carries: the rows it leaves owed."""
    return sorted(
        key[1]
        for key, src in sources.items()
        if src == "record" and prev.get(key) != live.get(key)
    )


def _identity(sources, live):
    """Does the copy equal the live file: every live row taken from live and
    every other row left out?"""
    return all(
        (src == "live") if key in live else (src is None)
        for key, src in sources.items()
    )


def expected_copy(rel, prev, live, named, split):
    """`(text, kept ids)`: the copy an act naming `named` writes for registry
    `rel`, from `prev` (the previous copy as `(text, suffix)`, or None) and
    `live` (the live file as `(text, suffix)`). The live text itself when the
    act keeps nothing; otherwise composed row by row (this module's docstring),
    which needs both sides on the TOML carrier. Raises `RowRecordError` when
    the copy cannot be written without changing a row's bytes.

    Implements: SR-207, LLR-245"""
    prev_rows = file_rows(*prev) if prev else {}
    live_rows = file_rows(*live)
    sources = row_rule(rel, prev_rows, live_rows, named, split)
    kept = kept_ids(sources, prev_rows, live_rows)
    if _identity(sources, live_rows):
        return live[0], kept
    if live[1] != ".toml" or (prev and prev[1] != ".toml"):
        held = [
            "{}: {}".format(key[1], _moved(rel, key, prev_rows, live_rows, split))
            for key, src in sorted(sources.items(), key=lambda item: item[0][1])
            if (src != "live" if key in live_rows else src is not None)
        ]
        raise RowRecordError(
            "it sits on a legacy carrier, which is copied only whole, and this act "
            "would leave these rows at their recorded text — name them, or convert "
            "the registry to TOML: {}".format("; ".join(held))
        )
    return _compose(prev[0] if prev else "", live[0], sources), kept


def _moved(rel, key, prev, live, split):
    """What moved on a row the act would keep: its changed cells, or that live
    no longer carries it."""
    if key not in live:
        return "removed from the live registry"
    changed = split(rel, key[0], prev.get(key) or {}, live[key])
    return ", ".join(sorted(set(changed["accepted"]) | set(changed["traced"])))


def _compose(prev_text, live_text, sources):
    """The copy's text: live's head and tail, the rows in live order from the
    side `sources` names, and each kept row live no longer carries after the row
    it followed in the previous copy."""
    _phead, prev_rows, _ptail = row_segments(prev_text)
    head, live_rows, tail = row_segments(live_text)
    texts = {"record": dict(prev_rows), "live": dict(live_rows)}
    order = [key for key, _seg in live_rows if sources.get(key)]
    earlier = [key for key, _seg in prev_rows]
    for at, key in enumerate(earlier):
        if key in texts["live"] or sources.get(key) != "record":
            continue
        before = next((k for k in reversed(earlier[:at]) if k in order), None)
        order.insert(order.index(before) + 1 if before else 0, key)
    return head + "".join(texts[sources[key]][key] for key in order) + tail


def row_problems(rel, prev, live, written, named, split):
    """One line per row whose text in `written` (a copy's text, on the live
    file's carrier) is not the text the rule gives it, read by parsing, never
    by the composition: `[]` when every row is what the act writes. The
    writer's re-read of its own result, and the judge's naming of a
    difference.

    Implements: SR-179, LLR-178, SR-207, LLR-245"""
    try:
        prev_rows = file_rows(*prev) if prev else {}
        live_rows = file_rows(*live)
        got = file_rows(written, live[1])
    except RowRecordError as exc:
        return ["{} cannot be read row by row: {}".format(rel, exc)]
    sources = row_rule(rel, prev_rows, live_rows, named, split)
    out = []
    for key in sorted(set(sources) | set(got), key=lambda k: k[1]):
        src = sources.get(key)
        want = {"live": live_rows, "record": prev_rows}.get(src, {}).get(key)
        if got.get(key) != want:
            out.append("{} {}: {}".format(rel, key[1], _why(key[1], src, got, named)))
    return out


def _why(rid, src, got, named):
    """What is wrong with one row of a written copy."""
    present = any(key[1] == rid for key in got)
    if rid in named:
        if src is None:
            return "retired by the act, but the copy still holds it"
        return "named by the act, but its recorded text is not its live text"
    if src == "record":
        if not present:
            return "dropped from the copy, and no act retired it"
        return "carries text the act did not name (an unnamed row's drift)"
    if src is None:
        return "in the copy, but no act carried it in"
    if not present:
        return "missing from the copy, which takes its live text"
    return "differs from its live text, which the copy takes"


def copy_problems(rel, prev, live, written, named, split):
    """The judge's comparison: `[]` when `written` is byte for byte the copy
    the act writes (`expected_copy`); otherwise each wrong row
    (`row_problems`), or one line for the bytes outside them.

    Implements: SR-179, LLR-178"""
    try:
        want, _kept = expected_copy(rel, prev, live, named, split)
    except RowRecordError as exc:
        return [str(exc)]
    if written == want:
        return []
    return row_problems(rel, prev, live, written, named, split) or [
        "{}: its bytes between or around the rows are not live's".format(rel)
    ]


def copy_carriers(rel):
    """Every carrier path a registry's copy can sit under, its own first."""
    needs = rel.startswith("docs/requirements/stakeholder-needs.")
    suffixes = spine_carrier.NEED_CARRIERS if needs else spine_carrier.CARRIERS
    own = PurePosixPath(rel).suffix
    paths = spine_carrier.carriers(rel, suffixes)
    return sorted(paths, key=lambda p: not p.endswith(own))


def blob_texts(root, specs):
    """`{spec: (text, suffix) | None}` for each `<rev>:<path>` (or `:<path>`,
    the index) in `specs`, read byte for byte in one `git cat-file --batch`
    and decoded as UTF-8 with no newline translation; None for a spec git
    reports missing. None overall when git cannot answer.

    Implements: SR-179, LLR-178"""
    if not specs:
        return {}
    feed = "".join(spec + "\n" for spec in specs).encode("utf-8")
    out = _kitgit.git_bytes(root, ["cat-file", "--batch"], stdin=feed)
    if out is None:
        return None
    texts, at = {}, 0
    for spec in specs:
        end = out.find(b"\n", at)
        line = out[at:end] if end >= 0 else b""
        if line.endswith(b" missing"):
            texts[spec], at = None, end + 1
            continue
        header = line.split()
        if len(header) != 3 or header[1] != b"blob":
            return None
        size = int(header[2])
        body = out[end + 1 : end + 1 + size].decode("utf-8", "replace")
        texts[spec] = (body, PurePosixPath(spec.partition(":")[2]).suffix)
        at = end + 2 + size
    return texts


# --- the act's copy, and the judgement of a written one ------------------------
# The writer composes and re-reads with `act_copy`; the record's two mirror rules
# read the trees with the rest. Each takes the cell comparison and the reading of
# "the entries a commit adds" from its caller, so this module imports neither.


def act_copy(rel, prev, live, named, split):
    """`(text, kept ids, problems)`: the copy an act writes for `rel` and the
    rows it leaves owed (`expected_copy`), with the composed text re-read by
    parsing (`row_problems`); `problems` names what keeps it from being
    written, `[]` when nothing does.

    Implements: SR-207, LLR-245"""
    try:
        text, kept = expected_copy(rel, prev, live, named, split)
    except RowRecordError as exc:
        return None, [], ["{}: {}".format(rel, exc)]
    return text, kept, row_problems(rel, prev, live, text, named, split)


def unretired(prev, named):
    """The ids of the rows a previous copy records as accepted that `named`
    does not retire: what keeps a copy of a registry live no longer carries
    from being removed."""
    rows = file_rows(*prev) if prev else {}
    return [
        k[1]
        for k, row in rows.items()
        if _kitspine.claims_acceptance(row) and k[1] not in named
    ]


def read_file(path):
    """`(text, suffix)` of a registry file read byte for byte, or None."""
    if path is None:
        return None
    return path.read_bytes().decode("utf-8", "surrogateescape"), path.suffix


def ledger_entries(text):
    """The `[[act]]` tables of an act ledger's text, `[]` for none or for text
    that does not parse (the act ledger's own rule reports that)."""
    try:
        acts = tomllib.loads(text or "").get("act", [])
    except tomllib.TOMLDecodeError:
        return []
    return [a for a in acts if isinstance(a, dict)] if isinstance(acts, list) else []


def act_rows(parent_ledgers, new_ledger, added_entries):
    """`(named, by_row)` for a tree that writes the record, from the act
    ledger's text in each parent and in the tree: the ids the entries the tree
    adds (`added_entries`, the caller's one reading of that) list as accepted
    or re-accepted — an act names those rows, and a tree adding no entry names
    none — and whether its copies are judged row by row: a parent's ledger, or
    an entry the tree adds, carries `kept`, which the row-by-row writer records
    on every act. A record whose ledger holds no such entry was written whole,
    and is judged as it was written.

    Implements: SR-179, LLR-178"""
    sides = [ledger_entries(text) for text in parent_ledgers]
    added = added_entries(ledger_entries(new_ledger), sides)
    named = frozenset(
        str(r)
        for a in added
        for key in ("accepted", "reaccepted")
        for r in a.get(key) or ()
    )
    return named, any("kept" in a for side in sides + [added] for a in side)


def texts_of(root, specs):
    """`blob_texts` with each `(text, suffix)` reduced to its text."""
    read = blob_texts(root, specs) or {}
    return {spec: (read.get(spec) or (None,))[0] for spec in specs}


def written_problems(root, record_dir, name, parents, new_rev, named, split):
    """The faults of the registry copy `name` (under `record_dir`) that tree
    `new_rev` (`""`, the index) writes, judged at the row: it must be the copy
    its act writes from the copy in the first of `parents` (none when it holds
    none, or one that does not parse) and the live registry in the tree, with
    the rows `named` taken from live (`copy_problems`). `[]` when git cannot
    answer or the tree holds no such copy.

    Implements: SR-179, LLR-178"""
    live_rel = name[len(record_dir) + 1 :]
    prev_specs = [
        "{}:{}/{}".format(parents[0], record_dir, c) for c in copy_carriers(live_rel)
    ]
    specs = prev_specs + ["{}:{}".format(new_rev, live_rel), new_rev + ":" + name]
    read = blob_texts(root, specs)
    if not read or read[specs[-1]] is None:
        return []
    if read[specs[-2]] is None:
        return ["{} does not exist where its copy was written".format(live_rel)]
    prev = readable(next((read[s] for s in prev_specs if read[s]), None))
    return copy_problems(
        live_rel, prev, read[specs[-2]], read[specs[-1]][0], named, split
    )


def whole_file_faults(root, pairs):
    """`[(name, live rel, rev, fault)]` over copies written whole, each `(name,
    live rel, rev)` judged byte-identical to its live counterpart at `rev` by
    blob id in one `cat-file --batch-check`: `fault` "absent" (no live
    counterpart in its own writing commit) or "differs". A copy the commit
    deleted is the deletion rule's, not a mirror question. `[]` when git
    cannot answer.

    Implements: SR-179, LLR-178"""
    if not pairs:
        return []
    specs = [s for n, live, rev in pairs for s in (rev + ":" + n, rev + ":" + live)]
    batch = _kitgit.git_out(
        root, ["cat-file", "--batch-check=%(objectname)"], "\n".join(specs) + "\n"
    )
    ids = batch.splitlines() if batch is not None else []
    if len(ids) != len(specs):
        return []
    out = []
    for i, (name, live_rel, rev) in enumerate(pairs):
        snap_id, live_id = ids[2 * i].strip(), ids[2 * i + 1].strip()
        if snap_id.endswith("missing") or snap_id == live_id:
            continue
        fault = "absent" if live_id.endswith("missing") else "differs"
        out.append((name, live_rel, rev, fault))
    return out


def tree_acts(root, ledger, trees, added_entries):
    """`{key: (named, by_row)}` (`act_rows`) for each `key: (parent revs, new
    rev)` of `trees` (a rev `""` is the index), the act ledger at `ledger`
    read at every one of those trees in one batch.

    Implements: SR-179, LLR-178"""
    specs = sorted({r + ":" + ledger for ps, new in trees.values() for r in [*ps, new]})
    texts = texts_of(root, specs)
    return {
        key: act_rows(
            [texts[p + ":" + ledger] for p in parents],
            texts[new + ":" + ledger],
            added_entries,
        )
        for key, (parents, new) in trees.items()
    }


def acting_rev(root, ledger, row_id, copies, shallow, added_entries):
    """`(rev, paths)` at which `git log -1 <rev> -- <paths>` names the commit of
    the act that accepted row `row_id`, whose author is the row's acting
    reviewer. That is the latest commit adding an act-ledger entry (the ledger
    at `ledger`) that lists the row accepted or re-accepted, its added entries
    read over EVERY parent (`added_entries`), so an entry a merge carries from
    one side stays its own commit's act; a row an act kept keeps its reviewer.
    For a row no entry names, it is the commit that last wrote the registry's
    copy (`copies`) before the first commit adding an entry that carries
    `kept` (`act_rows`), or at HEAD while none does: until then each act wrote
    its copy whole. A shallow clone's boundary commits (`shallow`) are not
    read, since their diff reads as adding every entry.

    Implements: SR-140, LLR-173"""
    log = _kitgit.git_out(root, ["log", "--format=%H %P", "--", ledger]) or ""
    commits = [c for c in map(str.split, log.splitlines()) if c and c[0] not in shallow]
    texts = texts_of(root, sorted({r + ":" + ledger for c in commits for r in c}))
    fallback = "HEAD"
    for sha, *parents in commits:
        sides = [texts[p + ":" + ledger] for p in parents]
        named, by_row = act_rows(sides, texts[sha + ":" + ledger], added_entries)
        if row_id in named:
            return sha, []
        fallback = sha + "^" if by_row else fallback
    return fallback, copies
