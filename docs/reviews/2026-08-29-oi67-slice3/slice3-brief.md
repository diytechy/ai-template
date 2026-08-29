# Slice 3 worker brief — the cell pass on the new interface row shape

You are one of four parallel workers on WI-530 in the repo at `c:\Projects\ai-template`
(Windows; the repo's Python is `.venv/Scripts/python.exe`). Read this whole brief,
then `docs/plans/2026-08-29-if-row-shape-plan.md` §1, then `project-trajectory/PROCESS.md`
section 8, before touching anything.

## The shape (ruled, OI-67 (a))

An interface row in `docs/requirements/interfaces.toml` is ONE OWNER, its FAR SIDE, and a
TYPED STATEMENT:

- `owner` — the providing THING: a module path (`scripts/check`), a file or directory path
  (`docs/stack.ini`, `docs/work/`), or `external:<party>`. It is what the information plugs
  into; it DEFINES the surface.
- `requestors` OR `consumers` — exactly one, a list. The KEY is the direction. `requestors`
  put information INTO the surface the owner defines (they call the function, invoke the
  CLI, set the env var, write the file). `consumers` take what the owner emits (they read the
  file, the exit code, the stdout). A call is one row (its requestors send the arguments and
  get the return). A CLI's arguments and its exit code are TWO rows (requestors in,
  consumers out).
- `channel` — closed: `cli` (an invocation surface: argv), `exit-code` (a finite code
  alphabet), `stdout` (emitted text: findings, a report), `file` (a file or directory medium
  with a schema; a dial read from a config file is `file`; a source tree walked by AST is
  `file`), `call` (an in-process API another module imports), `env` (an environment
  variable or launcher slot), `git` (repository state), `bytes` (opaque content).
- `data` — OPTIONAL, ≤160 characters: the finite alphabet when there is one
  (`0 pass · 1 fail · 2 usage`, `off | ask | deny`) or a one-clause schema pointer. No
  work-item id, no decision citation, no `because`/`rather than`/`so that`/`since`. A named
  symbol or path in it must exist.
- `contract` — LEGACY prose, the definition rows carried before the header existed. Its
  content moves into the owner's header (below) and the cell is then DELETED.
- `rationale` / `notes` — argument, never citation. Since the owner is a path now, every
  note arguing about which requirement id owns the row ("owner = SR-006, not SR-007 …",
  "twelve requirement-owned provider-side rows …", "no design row exists whose module is …")
  is MOOT and is deleted. A note that still states something true about the seam itself
  (the honesty valve `source`/`sink` as the FIRST word; a measured reader set; why the seam
  is drawn here) stays.

## Where the definition lives

The definition — what the owner PROMISES: the flags, the exit codes, the schema, the
guarantees, the failure behaviour — lives in the owner's header and NOWHERE else:

- A Python module: in its module docstring, one marker line and one body per seam:

```
Contracts: IF-013, IF-022, IF-040, IF-144 — the seams this module declares (process.md §8).

Contract IF-013: SR-006's obligation delivered as a CLI here. Runs a gate's declared
    steps as subprocesses and exits nonzero on any required failure, degrading only to
    a reported SKIP — never to a silent pass.
Contract IF-022: reads docs/stack.ini's declared toolchain — ...
```

  The marker must OPEN its line (`Contracts:` first token) and its id list must parse
  (`IF-###` comma- or semicolon-separated; prose may follow after an em dash, colon,
  hyphen or parenthesis, but NO id may appear in that tail that the list does not already
  carry). A body opens `Contract IF-###:` (exactly that; a bare `IF-###:` is prose) and runs
  to the next such line, a blank line, or the end of the docstring; wrapped lines join.
  Four hard refusals: a body before the marker, a body for an id not on the marker, two
  bodies for one id, an HTML comment in a body. Put the marker and bodies in the module
  DOCSTRING (the top-of-file `#` comment form also works for a Python file, but keep to
  the docstring where one exists). A body must state something — a body that states
  nothing is refused.

- A non-Python file (a registry, a config file, a git hook, a Markdown doc): in its LEADING
  comment header — `#` lines at the very top of a TOML/INI/CSV/shell/extensionless file
  (a `#!` shebang on line 1 is skipped; the block ends at the first non-`#` line) or the
  FIRST `<!-- ... -->` block at the top of a Markdown file. Same marker, same bodies, same
  refusals; strip the `# ` prefix mentally and the grammar is identical. A blank `#` line
  ends a body.

- A DIRECTORY owner declares through `<dir>/README.md` (its first `<!-- ... -->` block).
  Where the README does not exist, CREATE a short one: a one-paragraph description of what
  the directory holds, opening with the HTML-comment header. Keep it under 30 lines.

Examples of good bodies are in `project-trajectory/scripts/check.py` (IF-013, IF-144) and
`project-trajectory/hooks/pre-commit` (IF-134). Look at what the owner actually does before
writing — the body is a promise the code must honour, so read the code. The legacy
`contract` cell is your starting material; it often restates the owner's requirement or
argues — keep the typed facts (what is read, what is written, what the exit codes mean,
what fails loud), drop the argument and every citation (WI-###, OI-###, D-#, dates,
"since", "rather than"). Two to six lines per body is typical.

## Your batch

Your batch file (`slice3-batch-<X>.json`, path given in your task) has two parts:

1. `files` — `{owner_path: [rows]}`. For every row under an owner file you own: write the
   body in that owner's header; make sure the owner's `Contracts:` marker lists EXACTLY
   the ids of the rows the registry owns to it (add the missing ones, and REMOVE any id the
   registry does not own to this file — those rows belong to another owner). Confirm the
   row's `channel` and its far-side key/list against what the code really does; confirm or
   correct nothing in the registry yourself — REPORT it (below).
2. `remove_from_markers` — `{file: [ids]}`: markers in files of your batch that currently
   declare ids the registry owns to a DIFFERENT file. Remove those ids from those markers
   (and any `Contract IF-###:` body for them in that file — the body belongs to the owner).
   If a marker would become empty, delete the marker line (and its explanatory tail).

Rows owned by `external:` parties have no header to write; report only.

## What you must NOT do

- Do NOT edit `docs/requirements/interfaces.toml`. The registry is folded serially from your
  report by the coordinator.
- Do NOT touch any file outside your batch's `files` and `remove_from_markers` keys, except
  a README.md you create for a directory owner in your batch.
- Do NOT run `gen_arch_map.py --contracts-doc` without `--check` (the reference is
  regenerated once, by the coordinator). Do NOT run `git add`/`commit`.
- Do NOT change code behaviour — docstrings and comment headers only.

## Verify before reporting

For every module you edited, `.venv/Scripts/python.exe -c "import ast,sys; ..."` is not
enough — run the harvester on it:

```
.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'project-trajectory/scripts'); import ast, gen_arch_map as g; from pathlib import Path; p=Path('<file>'); t=p.read_text(encoding='utf-8'); tree=ast.parse(t); print(g.module_contracts(tree, t.splitlines())); print(g.module_contract_bodies(tree, t.splitlines()))"
```

and for a non-Python file:

```
.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'project-trajectory/scripts'); import gen_arch_map as g; from pathlib import Path; print(g.file_contracts(Path('<file>')))"
```

Both must print the exact owned id set with a body for each. Also run
`.venv/Scripts/ruff.exe format <py files>` and `.venv/Scripts/ruff.exe check <py files>`.
Do not run the test suite (another worker's edits are in flight); the coordinator does.

## Your report — the ONLY output the coordinator reads

Write `slice3-report-<X>.json` next to your batch file: a JSON list, one object per row in
your batch (every row, including external-owned ones), with EXACTLY these keys:

```
{"id": "IF-013",
 "channel": "exit-code",                 # the confirmed value (may differ from the batch's)
 "far_key": "consumers",                 # "requestors" or "consumers", confirmed
 "far": ["external:downstream adopter"], # the confirmed list (usually unchanged)
 "data": "0 pass · 1 fail · 2 usage",    # "" when there is no finite alphabet / one-clause pointer
 "body_written": true,                   # false only for external owners or a row you could not place
 "notes_moot": true,                     # true = delete the notes cell entirely
 "rationale_moot": false,                # true = delete the rationale cell entirely
 "note": "<one clause: anything the coordinator must know — a wrong owner, a row that should split, a body you could not write and why>"}
```

Keep `note` empty when there is nothing to say. Report facts, not narrative. When the
batch's `channel`/`far_key` is right, echo it. Your final message to the coordinator is a
plain-text summary: files edited, READMEs created, rows reported, and anything blocking.
