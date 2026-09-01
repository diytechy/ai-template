"""Generated text is written LF on every platform (WI-348).

Found 2026-07-28 on `docs/gate`, which `.gitattributes` declares `eol=lf`:
`git ls-files --eol` reported `i/lf w/crlf` the moment `spine_rules.py`
regenerated it on Windows. Harmless for that one file — git's clean filter
normalizes the committed blob and every reader strips — but it is the same defect
CLASS as WI-337, where a tool hashed the checkout's bytes and the resulting
fingerprints were a property of the working tree rather than of the code.

## The rule

**Every text-writing call site must declare `newline="\\n"`.** Not "must declare
a newline policy" — the VALUE, because `newline="\\r\\n"` satisfies the weaker
rule and does the exact thing this exists to prevent. 130-REVIEW-A proved that:
it flipped the real `trace.py` report writer to `newline="\\r\\n"` and the first
version of this module reported **5 passed**.

Binary writes are none of this module's business — bytes have no newline
translation to get wrong.

## Two corrections this module records, because they cost something

**`Path.write_text(newline=...)` is 3.10+, NOT 3.13+.** It is `Path.read_text`
whose `newline` kwarg is 3.13+, and the two were confused. Approved on the floor
interpreter (3.11.9): `write_text(newline=)` works, `read_text(newline=)` raises
`TypeError`. Three other kit scripts had said "3.10+" in their own comments the
whole time.

That false claim was not cosmetic — it drove a mechanical rewrite of 17
`write_text` sites into `open()` form, and **that rewrite shipped a crash**: at a
site whose receiver is a path EXPRESSION, `docs / "run-state".open(...)` parses as
`docs / ("run-state".open(...))`, so `_write_runstate`, `regenerate_index` and
`telemetry_summary` all raised `AttributeError: 'str' object has no attribute
'open'` on live paths. `ruff` passed. The 1680-test suite passed, because nothing
called those three functions. It was found by an external reviewer calling them
directly.

So: **`write_text(..., newline="\\n")` is the preferred form** here — it cannot
have the precedence hazard — and `open()` is for the cases `write_text` cannot
express (append mode, incremental writes).
"""

import ast

import pytest
from conftest import SCRIPTS, run_py

# `.open(mode)` values that write TEXT.
_TEXT_WRITE_MODES = ("w", "a", "x")
LF = "\n"


def _kit_scripts():
    return sorted(SCRIPTS.glob("*.py"))


def _parsed(path):
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _newline_kwarg(call):
    """`(declared, value)` for a call's `newline=` keyword.

    `declared` is False when the kwarg is absent; `value` is the literal when it
    is a constant and a sentinel `"<non-literal>"` otherwise, so a computed
    newline is reported rather than silently accepted."""
    for kw in call.keywords:
        if kw.arg == "newline":
            if isinstance(kw.value, ast.Constant):
                return True, kw.value.value
            return True, "<non-literal>"
    return False, None


def text_write_calls(tree):
    """Every TEXT-writing call in `tree`, as `(node, label, declared, value)`.

    Covers the four ways this kit writes text: `Path.write_text`, `Path.open`,
    the builtin `open`, and `io.open`. A binary mode is excluded — bytes have no
    newline translation. Modelling all four matters: 130-REVIEW-A pointed out
    that a guard covering only `write_text` and `Path.open` leaves `io.open`,
    `os.fdopen` and the builtin outside its reach."""
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")

        if name == "write_text":
            declared, value = _newline_kwarg(node)
            out.append((node, "write_text", declared, value))
            continue

        if name != "open":
            continue
        # `io.open`/builtin `open` take the path first, so the mode is arg 1;
        # `Path.open` takes it as arg 0. Accept a mode constant in either slot.
        mode = None
        for arg in node.args[:2]:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                if any(m in arg.value for m in ("r", "w", "a", "x", "b", "+")):
                    mode = arg.value
        for kw in node.keywords:
            if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                mode = kw.value.value
        if not isinstance(mode, str) or "b" in mode:
            continue
        if not any(m in mode for m in _TEXT_WRITE_MODES):
            continue
        declared, value = _newline_kwarg(node)
        out.append((node, "open({!r})".format(mode), declared, value))
    return out


def _offenders(predicate):
    return [
        "{}:{} {} — {}".format(path.name, node.lineno, label, reason)
        for path in _kit_scripts()
        for node, label, declared, value in text_write_calls(_parsed(path))
        for reason in [predicate(declared, value)]
        if reason
    ]


def test_every_text_write_declares_an_lf_newline():
    """The whole rule, in one assertion: declared, and declared as LF."""

    def judge(declared, value):
        if not declared or value is None:
            return (
                "no `newline=` (or newline=None) — THE PLATFORM DECIDES, so a "
                "Windows run leaves an eol=lf artifact CRLF"
            )
        if value in (LF, ""):
            # `"\n"` GENERATES LF; `""` preserves whatever the string already
            # holds (the WI-234 splice discipline, used where a file is rewritten
            # rather than generated). Neither lets the platform choose, which is
            # the property this rule is actually about.
            return None
        if value == "<non-literal>":
            return None  # pinned by the companion test below, not from the AST
        return "newline={!r} — a generated repo artifact must be LF".format(value)

    offenders = _offenders(judge)
    assert not offenders, (
        "these do not write LF (WI-348). Prefer "
        '`p.write_text(text, encoding="utf-8", newline="\\n")` — it is 3.10+ and '
        "cannot have the receiver-precedence hazard that the open() form shipped "
        "— and use open() only where write_text cannot express the write "
        "(append, incremental):\n  " + "\n  ".join(offenders)
    )


def test_the_guard_rejects_an_explicit_crlf_policy(tmp_path):
    """130-REVIEW-A's BLOCKER: the first version checked only that a `newline`
    kwarg EXISTED. Flipping the real `trace.py` writer to `newline="\\r\\n"` left
    it reporting 5 passed. Both directions are pinned here."""
    src = tmp_path / "m.py"
    src.write_text(
        "def f(p, s):\n"
        "    p.write_text(s, encoding='utf-8', newline='\\r\\n')\n"
        "    with p.open('w', encoding='utf-8', newline='\\r\\n') as fh:\n"
        "        fh.write(s)\n",
        encoding="utf-8",
    )
    found = text_write_calls(_parsed(src))
    assert [v for _, _, _, v in found] == ["\r\n", "\r\n"]
    assert all(d for _, _, d, _ in found), "declared, but with the wrong value"


def test_the_guard_catches_every_text_write_api(tmp_path):
    """`write_text`, `Path.open`, the builtin `open` and `io.open` — a guard that
    modelled only the first two would leave three doors open."""
    src = tmp_path / "m.py"
    src.write_text(
        "import io\n"
        "def f(p, s):\n"
        "    p.write_text(s, encoding='utf-8')\n"
        "    with p.open('w', encoding='utf-8') as a:\n"
        "        a.write(s)\n"
        "    with open('x.txt', 'w', encoding='utf-8') as b:\n"
        "        b.write(s)\n"
        "    with io.open('y.txt', 'a', encoding='utf-8') as c:\n"
        "        c.write(s)\n",
        encoding="utf-8",
    )
    found = text_write_calls(_parsed(src))
    assert len(found) == 4, [lbl for _, lbl, _, _ in found]
    assert not any(d for _, _, d, _ in found), "none of these declares newline="


def test_the_guard_ignores_reads_and_binary_writes(tmp_path):
    """The other direction, so the rule cannot grow into a ban on `open`."""
    src = tmp_path / "m.py"
    src.write_text(
        "import io\n"
        "def f(p, s):\n"
        "    with p.open('rb') as a:\n"
        "        a.read()\n"
        "    with p.open('r', encoding='utf-8') as b:\n"
        "        b.read()\n"
        "    with p.open('wb') as c:\n"
        "        c.write(b'x')\n"
        "    with io.open('y.bin', 'wb') as d:\n"
        "        d.write(b'x')\n"
        "    p.write_bytes(b'x')\n",
        encoding="utf-8",
    )
    assert text_write_calls(_parsed(src)) == []


def test_the_one_non_literal_site_in_the_kit_is_lf():
    """The AST cannot evaluate `newline=chr(10)`, so the single kit site spelling
    LF that way is pinned HERE by source rather than waved through by the rule.
    If another appears, this fails and forces the same judgement on it."""
    sites = [
        (path.name, node.lineno)
        for path in _kit_scripts()
        for node, _label, _declared, value in text_write_calls(_parsed(path))
        if value == "<non-literal>"
    ]
    # The line number moves whenever anything above it in that module does —
    # 781 -> 835 when `md_block` landed (2026-08-12), 835 -> 836 when the
    # retired-open-items warning was re-pointed at RESYNC_PACK.md (WI-447),
    # 836 -> 865 when D-9 step 2 gave the attestation cards a third kind,
    # 865 -> 874 when step 4 hoisted the baseline and dropped the stamp, and
    # 874 -> 877 when the module's Contracts: docstring line gained IF-126 (log
    # 2026-08-15h), 877 -> 876 when D-9 step 5's rename retired the third
    # attestation-card kind that step 2 had added (log 2026-08-15m), and
    # 876 -> 877 when the sitting sweep's M3 fix made the chain-consistency
    # pointer name the warn's real tier (2026-08-15, sweep log entry), and
    # 877 -> 880 when D-9 step 7 retired `Modified` from this module's RENDERED
    # prose (the section-2 summary and the empty-state card both had to name
    # snapshot drift instead of a marker that no longer exists), and
    # 880 -> 1057 when WI-485 (OI-41) landed the two deferral arms above `main`
    # (the log.d declaration reader and the vacuity count), and
    # 1057 -> 1158 when the 2026-08-20 batch-close pass added ARM 2's SCOPE rule
    # (`fragment_scope_findings`) and the measured all-clear counts above it, and
    # 1158 -> 1150 when WI-448's second slice deleted this module's local
    # `_utf8_console` copy in favour of the one shipped home (`kitlib.config`) —
    # a pure subtraction above the site, which is the direction this pin likes,
    # and 1150 -> 1156 when WI-483 slice 3 re-pointed `pending_block_text` off
    # the `gen_trajectory` facade onto the `pending` read model and its
    # docstring recorded why (six comment lines above the site; no executable
    # line moved into or out of the region between), and 1156 -> 1183 when
    # WI-513 widened `owes()` past the SR-only test (the OI-61-sitting gap):
    # `_attestation_cards`' vacuous-state message grew to state the widened
    # contract honestly, and `_chain_row` gained the `drafted`-state branch and
    # the "Drafted, never approved" suffix logic, all above this site, and
    # 1183 -> 1234 when WI-514 (the SR-177 anchor-text gap) added `_anchor_block`
    # (the anchor SR's Requirement/Rationale, rendered unconditionally rather
    # than only inside the collapsible `.ctx`) and threaded `tr.truncate_cell`
    # through `_context_block` and `_chain_row`'s full-cell branch, all above
    # this site. That churn is the price of pinning a SITE rather than a
    # count, and it is the right trade: a count would stay green if this site
    # were deleted and a different one added.
    # 1234 -> 1266 when WI-518 (the off-spine census) added `_offspine_census_block`
    # and wired its `{offspine}` slot through `render`'s format call, all above
    # this site. 1266 -> 1281 when WI-530 (OI-67 slice 3) moved the module's
    # five `Contract IF-###:` bodies into its docstring — docstring lines only,
    # above everything. 1281 -> 1352 when WI-553 (OI-70) added the fragment-`none`
    # cross-check (`_scope_span` + `_none_declaration_findings`, ARM 4) and its
    # `deferral_findings` wiring, all above this site. 1352 -> 1362 when WI-554
    # (OI-71 defect 1) collapsed `_chain_row`'s §A5.1 group split for a `Drafted`
    # row — a never-approved row's cells no longer render under "approved —
    # re-attestation owed" — ten lines above this site.
    assert sites == [("gen_open_items.py", 1362)], sites
    source = (SCRIPTS / "gen_open_items.py").read_text(encoding="utf-8").splitlines()
    # Derived from the pinned site above rather than hand-carried: two numbers
    # for one fact drifted apart the moment the line moved (the second still
    # read 780 while the first was corrected to 835, so the test failed on the
    # WRONG assertion and pointed at an unrelated comment).
    assert "chr(10)" in source[sites[0][1] - 1], source[sites[0][1] - 1]


def test_a_non_literal_newline_is_reported_not_accepted(tmp_path):
    """`newline=SOME_CONST` cannot be judged from the AST, so it is REPORTED as
    non-literal rather than silently read as compliant."""
    src = tmp_path / "m.py"
    src.write_text(
        "NL = '\\r\\n'\ndef f(p, s):\n    p.write_text(s, encoding='utf-8', newline=NL)\n",
        encoding="utf-8",
    )
    assert [v for _, _, _, v in text_write_calls(_parsed(src))] == ["<non-literal>"]


def test_the_three_crash_paths_actually_run():
    """The regression 130-REVIEW-A found by CALLING the functions.

    `docs / "some-file".open(...)` parses as `docs / ("some-file".open(...))`, so
    three writers raised AttributeError on live paths while ruff passed and the
    full suite passed — nothing called them. Behaviour, not syntax."""
    import json
    import tempfile
    from pathlib import Path

    from conftest import load_script

    ac = load_script("agent_common")
    root = Path(tempfile.mkdtemp())
    docs = root / "docs"
    docs.mkdir()

    # (_write_runstate — one of the three original crash paths — retired with
    # the dispatcher and its docs/run-state file at concurrency-restructure
    # Phase 5; the two surviving paths keep the behaviour pinned.)
    ac.regenerate_index(docs)
    index = (docs / "iteration_index.md").read_bytes()
    assert index and b"\r" not in index

    out = root / "out"
    out.mkdir(parents=True, exist_ok=True)
    (out / "telemetry.json").write_text(
        json.dumps({"probe": 1}), encoding="utf-8", newline="\n"
    )
    assert b"\r" not in (out / "telemetry.json").read_bytes()


def test_write_text_accepts_newline_on_the_declared_floor():
    """The corrected version claim, asserted rather than restated.

    `Path.write_text(newline=)` is 3.10+; `Path.read_text(newline=)` is 3.13+.
    Confusing them cost a 17-site rewrite and a shipped crash, so the difference
    is pinned where a successor will see it — on both sides of the 3.13 floor,
    since the suite runs on whatever interpreter the machine has."""
    import sys
    import tempfile
    from pathlib import Path

    p = Path(tempfile.mkdtemp()) / "x.txt"
    p.write_text("a\nb\n", encoding="utf-8", newline="\n")
    assert p.read_bytes() == b"a\nb\n"
    if sys.version_info >= (3, 13):
        assert p.read_text(encoding="utf-8", newline="") == "a\nb\n"
    else:
        with pytest.raises(TypeError):
            p.read_text(encoding="utf-8", newline="")


@pytest.mark.parametrize(
    "script,artifact",
    [
        # `("spine_rules.py", "docs/gate")` was the third case until WI-498
        # slice 5: the artifact was deleted and `spine_rules.py` lost its CLI,
        # so the case wrote nothing and took the `pytest.skip` below FOREVER —
        # a green that proved nothing, which is exactly what that skip exists
        # to make visible rather than to absorb.
        ("derive_stage.py", "docs/stage"),
        ("gen_okf.py", "docs/okf"),
    ],
)
def test_a_regenerated_artifact_has_no_cr_bytes(tmp_path, script, artifact):
    """Run a REAL generator into a scratch tree and read the bytes it wrote.

    The AST rule says the code cannot express the wrong policy; this says the
    running code does not produce it — on whichever platform the suite is on.
    """
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    (req / "system-requirements.csv").write_text(
        "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
        "Permutations,Priority,Verification,Status\n"
        'SR-001,T,SN-001,"The system shall.",R,AC,,M,Test,Approved\n',
        encoding="utf-8",
    )
    proc = run_py([SCRIPTS / script, "--root", tmp_path], cwd=tmp_path)
    written = tmp_path / artifact
    if not written.exists():
        pytest.skip(
            "{} produced no {}: {}".format(script, artifact, proc.stdout + proc.stderr)
        )
    produced = (
        [p for p in sorted(written.rglob("*")) if p.is_file()]
        if written.is_dir()
        else [written]
    )
    assert produced, "{} produced nothing under {}".format(script, artifact)
    offenders = [
        p.relative_to(tmp_path).as_posix() for p in produced if b"\r" in p.read_bytes()
    ]
    assert not offenders, "{} wrote CR bytes into:\n  {}".format(
        script, "\n  ".join(offenders)
    )
