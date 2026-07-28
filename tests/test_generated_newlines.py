"""Generated text is a repo artifact, so it is written LF on every platform (WI-348).

Found 2026-07-28 on `docs/gate`, which `.gitattributes` declares `eol=lf`:
`git ls-files --eol` reported `i/lf w/crlf` the moment `derive_gate.py`
regenerated it on Windows. Harmless for that one file — git's clean filter
normalizes the committed blob and every reader strips — but it is the same defect
CLASS as WI-337, where a tool hashed the checkout's bytes and the resulting
fingerprints were a property of the working tree rather than of the code.

Counted by AST, not grep: at the time, **all 17** `Path.write_text()` call sites
across the kit scripts passed no `newline` argument, and **zero** specified one.
(The row first said "4 already do"; 129-REVIEW-A refuted that — the grep behind
it had matched `open(..., newline=)`, a different API. Corrected rather than
restated, which is why this module measures instead of asserting a number.)

Two guards, deliberately different in kind:

- the **AST** one below is the invariant, and it is what makes the fix stick: a
  new generator written with a bare `write_text` is caught at the commit bar, on
  every platform, without needing a Windows runner to notice;
- the **byte** one runs a real generator and reads the result, so the invariant
  is anchored to observed behaviour rather than to a syntax rule that might not
  mean what it looks like.

`Path.write_text(newline=...)` is **3.13+** and the kit floor is 3.11, so the fix
is the `open(..., newline="\\n")` form. That is not a style choice and must not be
"simplified" back: a `write_text(..., newline="\\n")` would be a TypeError on the
oldest Python the kit claims. It is also why the ritual is inlined rather than
routed through a helper — the F5 independently-copyable rule means a helper would
have to be copied into all eight scripts, and eight copies of a helper is a worse
trade than the inline form (the census records that decision under
`lf-write-preamble`).
"""

import ast

import pytest
from conftest import SCRIPTS, run_py

# `.open(mode)` values that write TEXT. A binary write is none of this module's
# business — bytes have no newline translation to get wrong.
_TEXT_WRITE_MODES = ("w", "a", "x")


def _kit_scripts():
    return sorted(SCRIPTS.glob("*.py"))


def _parsed(path):
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _write_text_calls(tree):
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "write_text"
    ]


def _text_write_opens(tree):
    """`.open(...)` calls in TEXT write mode, as (node, declares_newline)."""
    out = []
    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "open"
        ):
            continue
        mode = None
        for arg in node.args[:1]:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                mode = arg.value
        for kw in node.keywords:
            if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                mode = kw.value.value
        if not isinstance(mode, str) or "b" in mode:
            continue
        if not any(m in mode for m in _TEXT_WRITE_MODES):
            continue
        out.append((node, any(kw.arg == "newline" for kw in node.keywords)))
    return out


def test_no_kit_script_writes_text_through_write_text():
    """`Path.write_text` cannot express the newline policy on the declared floor,
    so a kit script must not use it to write a repo artifact."""
    offenders = [
        "{}:{}".format(path.name, node.lineno)
        for path in _kit_scripts()
        for node in _write_text_calls(_parsed(path))
    ]
    assert not offenders, (
        "these write text without a newline policy — Path.write_text(newline=) is "
        "3.13+ and the kit floor is 3.11, so use "
        '`with p.open("w", encoding="utf-8", newline="\\n") as fh:` (WI-348):\n  '
        + "\n  ".join(offenders)
    )


def test_every_text_write_open_declares_a_newline_policy():
    """The other half: switching to `open()` buys nothing if the argument is
    then omitted. This is the assertion that actually holds the line."""
    offenders = [
        "{}:{}".format(path.name, node.lineno)
        for path in _kit_scripts()
        for node, declares in _text_write_opens(_parsed(path))
        if not declares
    ]
    assert not offenders, (
        "these open a file for TEXT writing without declaring `newline=`, so the "
        "platform decides and a Windows run leaves an eol=lf artifact CRLF in the "
        "working tree (WI-348):\n  " + "\n  ".join(offenders)
    )


def test_the_guard_can_fail(tmp_path):
    """Mutation proof, constructed rather than inherited: the two predicates must
    FIRE on the shapes they exist to ban and stay silent on the fixed form. Both
    assertions above pass vacuously on a tree with no offenders, which is exactly
    the state this repo is now in — so without this they would be untested."""
    bad = tmp_path / "bad.py"
    bad.write_text(
        "from pathlib import Path\n"
        "def f(p, s):\n"
        "    p.write_text(s, encoding='utf-8')\n"
        "    with p.open('w', encoding='utf-8') as fh:\n"
        "        fh.write(s)\n",
        encoding="utf-8",
    )
    tree = _parsed(bad)
    assert len(_write_text_calls(tree)) == 1
    assert [d for _, d in _text_write_opens(tree)] == [False]

    good = tmp_path / "good.py"
    good.write_text(
        "from pathlib import Path\n"
        "def f(p, s):\n"
        "    with p.open('w', encoding='utf-8', newline='\\n') as fh:\n"
        "        fh.write(s)\n"
        "    with p.open('rb') as fh:\n"
        "        fh.read()\n"
        "    with p.open('wb') as fh:\n"
        "        fh.write(b'x')\n",
        encoding="utf-8",
    )
    tree = _parsed(good)
    assert _write_text_calls(tree) == []
    # The read and the BINARY write must not be flagged — a rule that bans
    # `open('wb')` would be a different, wrong rule.
    assert [d for _, d in _text_write_opens(tree)] == [True]


@pytest.mark.parametrize(
    "script,args,artifact",
    [
        ("derive_gate.py", [], "docs/gate"),
        ("gen_okf.py", [], "docs/okf"),
    ],
)
def test_a_regenerated_artifact_has_no_cr_bytes(tmp_path, script, args, artifact):
    """Run a REAL generator into a scratch tree and read the bytes it wrote.

    The AST rule says the code cannot express the wrong policy; this says the
    running code does not produce it — on whichever platform the suite happens to
    be on, which is the only way a Windows-specific defect gets caught by a Linux
    CI lane and vice versa.
    """
    docs = tmp_path / "docs" / "requirements"
    docs.mkdir(parents=True)
    (tmp_path / "docs" / "requirements" / "system-requirements.csv").write_text(
        "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
        "Permutations,Priority,Verification,Status\n"
        'SR-001,T,SN-001,"The system shall.",R,AC,,M,Test,Verified\n',
        encoding="utf-8",
    )
    proc = run_py([SCRIPTS / script, "--root", tmp_path, *args], cwd=tmp_path)
    written = tmp_path / artifact
    if not written.exists():
        pytest.skip(
            "{} produced no {} in this fixture: {}".format(
                script, artifact, proc.stdout + proc.stderr
            )
        )
    # `docs/okf` is a DIRECTORY of generated files, `docs/gate` a single file —
    # scan whichever, so the assertion is about everything the generator wrote
    # rather than about one path shape.
    produced = (
        [p for p in sorted(written.rglob("*")) if p.is_file()]
        if written.is_dir()
        else [written]
    )
    assert produced, "{} produced nothing under {}".format(script, artifact)
    offenders = [
        p.relative_to(tmp_path).as_posix() for p in produced if b"\r" in p.read_bytes()
    ]
    assert not offenders, (
        "{} wrote CR bytes into these — a generated repo artifact must be LF on "
        "every platform (WI-348):\n  {}".format(script, "\n  ".join(offenders))
    )
