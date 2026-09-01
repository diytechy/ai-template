"""WI-509 (OI-59 ruled (a)+(c)): pin the kit-path invariant.

`bootstrap.py` deliberately never copies *itself* into a scaffold - it is not
a row in its own `MAPPING` (the kit folder is the tool; the adopter's
scaffolded repo is the product; option (b), shipping a second installer copy
into the scaffold, was DECLINED by the ruling because two installers drift).
That means any instructing surface that tells a reader to *run* `bootstrap.py`
must address a path that actually exists from the reader's assumed working
directory - never a bare `scripts/bootstrap.py`, which resolves (from inside
an adopter's own repo) to a file that repo was never given. WI-498's slice-5
recovery hit exactly this defect live (docs/log.d/2026-08-21-wi498-stage-
unification.md, "the recovery's census"): a re-sync recipe's own step read
`python scripts/bootstrap.py --migrate-config --dest .`, and a literal
follower got `can't open file ... scripts/bootstrap.py`.

Two tiers, because the kit ships instructions from two different assumed
CWDs (both real, both used elsewhere in the kit's own prose):

- **STRICT surfaces** - every file `bootstrap.py`'s own `MAPPING` copies or
  generates into an adopter's scaffolded repo (its SOURCE, read from this kit
  checkout), plus `RESYNC_PACK.md` (its recipes describe actions taken while
  standing in an ALREADY-ADOPTED repo, per its own §1 procedure). The reader's
  CWD here is the adopter's own repo root, which never contains
  `scripts/bootstrap.py` - every invocation must spell the kit-relative path,
  `project-trajectory/scripts/bootstrap.py` (the convention OI-59's ruling and
  ADOPTING.md's "where the machinery lives" paragraph both name: keep the kit
  checkout, conventionally at that path, precisely so this command keeps
  working).
- **FRAMED surfaces** - the fresh-scaffold reference docs (`ADOPTING.md`, the
  kit's own root `README.md`, `KICKOFF_PROMPT.md`) are read by someone who has
  the KIT ITSELF checked out as their CWD, so a bare `scripts/bootstrap.py` is
  legitimate there - but only when the same sentence (the line, the line
  right before, or the line right after - markdown prose wraps) says so
  explicitly ("kit folder", "kit checkout", "from this kit", "from inside
  it"). A reader who copies just the command line otherwise has no way to
  know which directory it assumes.

`bootstrap.py`'s own docstring, describing its own invocation, is exempt: it
is the machinery, not an instruction pointing at it from somewhere else.

The machinery filename (`bootstrap.py`) and the two migration/sync flags this
pin cares about are read from `bootstrap.py` itself (`MAPPING` for the
filename check; `--migrate-config`/`--sync` are named directly in OI-59's
ruling and confirmed present in `bootstrap.py`'s own `argparse` surface below)
rather than hand-listed, so the pin cannot drift from the one home for the
inventory it is a claim about.
"""

import re

from conftest import KIT, ROOT

BOOTSTRAP_PY = KIT / "scripts" / "bootstrap.py"

# The two migration/sync flags OI-59's ruling names explicitly. Asserted
# present in bootstrap.py's own argparse surface (not just assumed) so this
# list cannot silently drift from the one home for the machinery it names.
_MACHINERY_FLAGS = ("--migrate-config", "--sync")

# A runnable invocation: literal "python" followed by a bare `scripts/`
# bootstrap.py path. Deliberately narrow - it does not fire on a prose mention
# like "copied into a new repo by `scripts/bootstrap.py`", which names the
# tool without claiming a CWD, and it does not fire on the correct forms
# (`project-trajectory/scripts/bootstrap.py`, or bootstrap.py's own
# self-referential docstring).
_BARE_INVOCATION_RE = re.compile(r"python\s+scripts/bootstrap\.py")
_KIT_PREFIXED_RE = re.compile(r"project-trajectory/scripts/bootstrap\.py")

_FRAMING_RE = re.compile(
    r"kit folder|kit checkout|from this kit|from inside it|inside this kit",
    re.IGNORECASE,
)

# STRICT surfaces: every MAPPING source (read from the kit checkout; each
# copies or generates into an adopter's own scaffolded repo) plus
# RESYNC_PACK.md, whose recipes run in an already-adopted repo.
_STRICT_EXTRA = (KIT / "RESYNC_PACK.md",)

# FRAMED surfaces: fresh-scaffold reference docs, read with the kit itself as
# the CWD. A bare invocation is legal there only next to explicit framing.
_FRAMED_SURFACES = (
    KIT / "ADOPTING.md",
    KIT / "README.md",
    KIT / "KICKOFF_PROMPT.md",
)


def _mapping_sources():
    """The `(source, dest)` pairs bootstrap.py's own MAPPING declares - the
    one home for "what does a scaffold receive", read rather than hand-kept."""
    text = BOOTSTRAP_PY.read_text(encoding="utf-8")
    m = re.search(r"^MAPPING = \[(.*?)^\]", text, re.S | re.M)
    assert m, (
        "bootstrap.py's `MAPPING = [...]` list was not found by this test's "
        "regex - MAPPING's shape changed; update "
        "tests/test_kit_path_invariant.py's `_mapping_sources` to match."
    )
    # A MAPPING row may carry a third element (its SR-163 requirement
    # reference) after the (source, dest) pair; the optional tail keeps this
    # source-inventory reader tolerant of both pairs and triples.
    pairs = re.findall(
        r'\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*(?:,\s*"[^"]+"\s*)?\)', m.group(1)
    )
    assert pairs, (
        "tests/test_kit_path_invariant.py parsed bootstrap.py's MAPPING as "
        "empty - the parsing regex is stale."
    )
    return pairs


def _bare_offenses(path):
    """Yield (line_no, line) for every bare `python scripts/bootstrap.py`
    invocation in `path` that is not already spelled with the kit-relative
    prefix (`project-trajectory/scripts/bootstrap.py`)."""
    try:
        text = path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError):
        return
    lines = text.splitlines()
    for i, line in enumerate(lines):
        for m in _BARE_INVOCATION_RE.finditer(line):
            start = m.start()
            # A match immediately preceded by the kit-relative prefix (i.e.
            # the "scripts/bootstrap.py" tail of
            # "project-trajectory/scripts/bootstrap.py") is already correct.
            prefix = line[: start + len("python ")]
            if prefix.rstrip().endswith("project-trajectory"):
                continue
            yield i + 1, line, lines


def test_bootstrap_stays_out_of_its_own_mapping():
    """OI-59 ruled (a): bootstrap.py is not a MAPPING destination - the
    bundle IS the kit folder, and a fresh scaffold never receives its own
    installer. (b), a second installer copy shipped into the scaffold, was
    DECLINED by the same ruling."""
    pairs = _mapping_sources()
    offenders = [dest for _src, dest in pairs if "bootstrap.py" in dest]
    assert not offenders, (
        "bootstrap.py MAPPING now copies itself into the scaffold at "
        f"{offenders} - OI-59 ruled (a): the kit folder is the tool, the "
        "scaffold is the product, and bootstrap.py must stay out of its own "
        "MAPPING. If this is a deliberate reversal it needs a fresh OI ruling, "
        "not a silent MAPPING row."
    )


def test_bootstrap_declares_the_machinery_flags_this_pin_names():
    """The two flags OI-59's ruling names (`--migrate-config`, `--sync`) are
    read from bootstrap.py's own argparse surface, so this pin's flag list
    cannot silently drift from what the machinery actually accepts."""
    text = BOOTSTRAP_PY.read_text(encoding="utf-8")
    for flag in _MACHINERY_FLAGS:
        assert '"{}"'.format(flag) in text, (
            "bootstrap.py no longer declares {} - update OI-59's ruling / "
            "this pin's _MACHINERY_FLAGS, or restore the flag.".format(flag)
        )


def test_strict_surfaces_never_use_a_bare_scaffold_relative_bootstrap_path():
    """Every MAPPING-shipped source, plus RESYNC_PACK.md, describes commands
    run while standing in the adopter's OWN repo - which never contains
    `scripts/bootstrap.py`. Every invocation there must spell the kit-relative
    path."""
    pairs = _mapping_sources()
    strict_files = [KIT / src for src, _dest in pairs] + list(_STRICT_EXTRA)

    findings = []
    for path in strict_files:
        if not path.is_file():
            continue
        for line_no, line, _lines in _bare_offenses(path):
            rel = path.relative_to(ROOT).as_posix()
            findings.append(
                "{}:{}: {!r} - reader stands in the ADOPTER's own repo here "
                "(this file ships there), which has no scripts/bootstrap.py. "
                "Fix: spell the kit-relative path, "
                "`python project-trajectory/scripts/bootstrap.py ...` "
                "(the convention ADOPTING.md's 'where the machinery lives' "
                "paragraph names).".format(rel, line_no, line.strip())
            )

    assert not findings, "kit-path invariant violated:\n" + "\n".join(findings)


def test_framed_surfaces_frame_every_bare_bootstrap_invocation():
    """ADOPTING.md, the kit's own README.md, and KICKOFF_PROMPT.md are read
    with the KIT ITSELF as the CWD, so a bare `scripts/bootstrap.py` is
    legitimate there - but only when the same sentence (the line, the one
    before it, or the one after - markdown prose wraps) says so, so a reader
    who copies just the command isn't guessing the directory."""
    findings = []
    for path in _FRAMED_SURFACES:
        if not path.is_file():
            continue
        for line_no, line, lines in _bare_offenses(path):
            # current line, the one before, and the one after - markdown
            # prose wraps, so framing text following the command on the same
            # sentence can land on the next source line.
            window = " ".join(lines[max(0, line_no - 2) : line_no + 1])
            if _FRAMING_RE.search(window):
                continue
            rel = path.relative_to(ROOT).as_posix()
            findings.append(
                "{}:{}: {!r} - a bare scripts/bootstrap.py invocation with no "
                "kit-folder framing on this line or the one before it. Fix: "
                "either spell the kit-relative path "
                "(project-trajectory/scripts/bootstrap.py) or add explicit "
                "CWD framing ('From the kit folder:', 'from this kit', "
                "'kit checkout') so a reader who copies just the command "
                "line still knows where to stand.".format(rel, line_no, line.strip())
            )

    assert not findings, "kit-path invariant violated:\n" + "\n".join(findings)
