# Slice 4 worker brief — the split (WI-531, OI-67 slice 4)

You are one of three parallel workers on WI-531 in the repo at `c:\Projects\ai-template`
(Windows; the repo's Python is `.venv/Scripts/python.exe`; run scripts from the repo root).
Read this whole brief, then `docs/plans/2026-08-29-if-row-shape-plan.md` §1 and §3 "Slice 4",
then `docs/reviews/2026-08-29-oi67-slice3/slice3-brief.md` (the header grammar and the
report discipline — the same rules apply here), before touching anything.

## What this slice does

The registry `docs/requirements/interfaces.toml` must read ONE ROW = ONE OWNER, ONE DIRECTION,
ONE KIND. Slice 3 moved every definition beside its owner; slice 4 SPLITS the rows that still
describe two kinds (a request and its answer; a read and a write; a CLI and the file it writes),
COLLAPSES two duplicate pairs, and fixes the far sides slice 3 measured as stale. The registry
is folded serially by the coordinator from your report. You write the DEFINITIONS — the
`Contract IF-###:` bodies in the owners' headers — and you MEASURE the far sides marked
`MEASURE`.

Your worklist is `slice4-batch-<X>.json` (path given in your task): one object per row action.

- `new` — a row minted for a kind that had no row. Its id is FIXED (assigned from the
  watermark by the coordinator — never renumber). Write its body in `body_home`; add the id to
  that file's `Contracts:` marker (create the marker where the file has none, in the module
  docstring or the file's leading `#` / `<!-- -->` header per the slice-3 brief).
- `edit` — an existing row whose cells change (channel corrected, far side re-measured, a
  sibling collapsed into it). Update the body in `body_home` so it states what the row now
  says; confirm or correct the cells; report them.
- `delete` — a row collapsing into `into`. Remove its id from the marker and its body from
  the header; merge the clauses worth keeping into the `into` row's body.

For every row: the `why` field tells you what the slice-3 worker found and what to CONFIRM.
**Read the code before writing** — a body is a promise the code must honour. Where a cell
says `MEASURE`, grep the tree, read each site, and report the measured list; where a list is
stated, confirm it against the code and correct it in your report if the code disagrees.

## Body rules (unchanged from slice 3)

A body opens `Contract IF-###:` on its own line under the file's `Contracts:` marker, runs to
the next opener, a blank line or the end of the docstring/header, wrapped lines joining. Two
to six lines. State the typed facts: what is read or written, the flags, the exit codes, the
schema, what fails loud. No work-item id, no `OI-`, no `D-`, no date, no "since"/"rather than".
The four hard refusals (body before marker, body for an undeclared id, two bodies for one id,
an HTML comment in a body) still apply. A split row's body must NOT restate its sibling's kind:
the exit-code row states the alphabet and when each code is returned; the stdout row states the
line grammar; the cli row states the argv surface; the file row states the medium's shape.

A Markdown file's header is the FIRST `<!-- ... -->` block in the file, BEFORE any heading.
A `#`-line file (TOML/INI/CSV/extensionless) declares in its leading `#` block. A directory
declares in its `README.md` (create one where the batch says CREATE: an HTML-comment header,
then an H1 and one short paragraph; under 30 lines).

## What you must NOT do

- Do NOT edit `docs/requirements/interfaces.toml` — the coordinator folds it.
- Do NOT touch files outside your batch's `body_home` set (plus a README you are told to
  create). Do NOT edit `docs/id-watermark`, `docs/if-tc-coverage-allow`, `docs/test/test-cases.toml`,
  any test, or any executable code — docstrings and comment headers only.
- Do NOT run `gen_arch_map.py --contracts-doc` without `--check`; do NOT `git add`/`commit`.
- Do NOT run the test suite (other workers' edits are in flight); the coordinator does.

## Verify before reporting

For each Python file you edited:

```
.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'project-trajectory/scripts'); import ast, gen_arch_map as g; from pathlib import Path; p=Path('<file>'); t=p.read_text(encoding='utf-8'); tree=ast.parse(t); print(sorted(g.module_contracts(tree, t.splitlines()))); print(sorted(g.module_contract_bodies(tree, t.splitlines())))"
```

and for a non-Python file:

```
.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'project-trajectory/scripts'); import gen_arch_map as g; from pathlib import Path; ids,b=g.file_contracts(Path('<file>')); print(ids, sorted(b))"
```

Both must print exactly the id set your batch leaves the file owning (existing ids the batch
does not touch stay), with a body for each. Then `.venv/Scripts/ruff.exe format <py files>`
and `.venv/Scripts/ruff.exe check <py files>`.

## Your report — the ONLY output the coordinator reads

Write `slice4-report-<X>.json` beside your batch file: a JSON list, one object per row in your
batch, EXACTLY these keys:

```
{"id": "IF-145",
 "action": "new",                        # echoed from the batch
 "owner": "scripts/trace",               # the confirmed owner (for IF-164: the module you determined)
 "far_key": "consumers",                 # requestors | consumers
 "far": ["scripts/check"],               # the CONFIRMED or MEASURED list
 "channel": "exit-code",
 "data": "0 clean · 1 ...",              # <= 160 chars, or "" when nothing finite/pointable
 "tie_from": "", "tie_to": "B-05",       # the tie-backs the row carries after this slice ("" = none)
 "component": "",                        # the CMP-### tag or ""
 "notes": "",                            # a notes cell to SET on a new row ("" = none); for edit rows: "" = leave as is
 "rationale_moot": false,                # edit rows only: true = delete the rationale cell
 "notes_moot": false,                    # edit rows only: true = delete the notes cell
 "body_written": true,
 "note": "<one clause for the coordinator: what you measured, what you corrected, anything blocking>"}
```

For a `delete` row report `{"id": ..., "action": "delete", "into": "IF-075", "body_written": false, "note": ...}`.
Report facts, not narrative. Your final message is a plain-text summary: files edited, READMEs
created, rows reported, anything you could not do and why.
