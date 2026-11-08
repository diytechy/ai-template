"""The registry templates and the ID vocabulary name no language.

SR-035's second half: the shipped registry templates and the identifier
scheme's declarations carry no language-specific token, so a project on any
stack fills them as they stand. The claim is finite. The scan reads every
registry template (`registries/*.template.toml` and `*.template.csv`, globbed),
the work-item scaffold and the id-watermark template; and the vocabulary's
three declarations: `trace.WATERMARK_SPACES`, PROCESS.md section 2 and
INTERFACES.template.md "ID scheme & columns", each from its heading to the
next `## `. It looks only for the tokens declared once below. All other kit
prose is outside it, and so is arbitrary language-specific free text.

A kit script named as `<name>.py` or `scripts/<name>.py` is exempt: it is the
kit's own toolchain, which every adopter runs whatever its stack. Any other
`.py` path is still reported.

The scaffold half (a non-Python profile passing the strict registry checks) is
tests/test_profile.py::test_every_profile_permutation_scaffolds_green.

Implements: TC-165
"""

import re
import shutil

import pytest
from conftest import KIT, load_script

TRACE = load_script("trace")

LANGUAGE_TOKENS = (
    "python",
    "pytest",
    "pip",
    "pyproject",
    "conftest",
    "unittest",
    "mypy",
    "ruff",
    "virtualenv",
    "javascript",
    "typescript",
    "nodejs",
    "npm",
    "rust",
    "cargo",
    "golang",
    "java",
    "kotlin",
    "maven",
    "gradle",
    "junit",
    "csharp",
    "dotnet",
    "nuget",
    "ruby",
    "rubygems",
    "php",
    "cmake",
    "powershell",
)
SOURCE_EXTENSIONS = (
    "py",
    "pyi",
    "ipynb",
    "js",
    "mjs",
    "cjs",
    "ts",
    "tsx",
    "jsx",
    "rs",
    "go",
    "java",
    "kt",
    "cs",
    "rb",
    "php",
    "c",
    "cc",
    "cpp",
    "h",
    "hpp",
    "swift",
    "ps1",
)

_NAME = "A-Za-z0-9_"
_WORD = re.compile(
    r"(?<![{0}])({1})(?![{0}])".format(_NAME, "|".join(LANGUAGE_TOKENS)),
    re.IGNORECASE,
)
# An extension matches as a file-name suffix: a name character (or a wildcard
# standing for one) before the dot and no name character after it, so whatever
# follows (emphasis, an anchor, a query, any punctuation) ends the match.
_EXTENSION = re.compile(
    r"(?<=[{0}*?])\.({1})(?![{0}])".format(_NAME, "|".join(SOURCE_EXTENSIONS)),
    re.IGNORECASE,
)
# The token is the path-like run ending at that dot, so a separator of any
# platform or a wildcard name stays inside it.
_PATH_RUN = re.compile(r"[{0}/\\*?.\-]*\Z".format(_NAME))
_SCRIPT_REF = re.compile(r"(?:scripts/)?([{0}]+)".format(_NAME))


def _path_token(line, match):
    """The path-like token whose file name ends at the extension `match`. A
    leading run of `*` closed by the same run straight after the extension is
    Markdown emphasis around the token, not a wildcard in it."""
    dot, end = match.span()
    token = _PATH_RUN.search(line, 0, dot).group() + line[dot:end]
    stars = len(token) - len(token.lstrip("*"))
    if stars and line[end : end + stars] == "*" * stars:
        token = token[stars:]
    return token


SECTIONS = (
    ("PROCESS.md", "## 2. Identifier scheme"),
    ("INTERFACES.template.md", "## ID scheme & columns"),
)


def _surface_files(kit):
    """The scanned files, each glob required to match."""
    files = []
    for pattern in ("*.template.toml", "*.template.csv"):
        matched = sorted((kit / "registries").glob(pattern))
        assert matched, "registries/{} matched nothing".format(pattern)
        files += matched
    for rel in ("work/WI-000.template.md", "id-watermark.template"):
        assert (kit / rel).is_file(), "{} is missing".format(rel)
        files.append(kit / rel)
    return files


def _section(kit, rel, heading):
    """`(first line number, lines)` from `heading` to the next `## `; a missing
    heading fails."""
    lines = (kit / rel).read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if line.strip() == heading]
    assert starts, "{}: heading {!r} is missing".format(rel, heading)
    start = starts[0]
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")),
        len(lines),
    )
    return start + 1, lines[start:end]


def _line_hits(line, scripts):
    """The tokens one line carries, kit-script names excepted."""
    hits = [m.group(1).lower() for m in _WORD.finditer(line)]
    for m in _EXTENSION.finditer(line):
        token = _path_token(line, m)
        ext = m.group(1)
        ref = _SCRIPT_REF.fullmatch(token[: -len(ext) - 1])
        if ext.lower() == "py" and ref and ref.group(1) in scripts:
            continue
        hits.append(token)
    return hits


def scan(kit, spaces=TRACE.WATERMARK_SPACES):
    """Every `(file, line, token)` hit on the surface under `kit`, the shipped
    kit directory or a copy of it; `spaces` is the declared id-space set."""
    scripts = {p.stem for p in (kit / "scripts").glob("*.py")}
    sources = [("trace.WATERMARK_SPACES", 1, list(spaces))]
    for path in _surface_files(kit):
        text = path.read_text(encoding="utf-8")
        sources.append((path.relative_to(kit).as_posix(), 1, text.splitlines()))
    for rel, heading in SECTIONS:
        sources.append((rel,) + _section(kit, rel, heading))
    return [
        (name, first + offset, token)
        for name, first, lines in sources
        for offset, line in enumerate(lines)
        for token in _line_hits(line, scripts)
    ]


SCRIPTS_PY = sorted((KIT / "scripts").glob("*.py"))


@pytest.fixture
def kit_copy(tmp_path):
    """The scanned surface copied under a temp kit root, with the kit scripts
    present by name so the exemption reads them as it does in the kit."""
    copy = tmp_path / "kit"
    for path in _surface_files(KIT):
        dest = copy / path.relative_to(KIT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)
    for rel, _heading in SECTIONS:
        shutil.copyfile(KIT / rel, copy / rel)
    (copy / "scripts").mkdir()
    for path in SCRIPTS_PY:
        (copy / "scripts" / path.name).write_text("", encoding="utf-8")
    return copy


def _plant(copy, rel, text):
    """Put `text` on its own line in the copied `rel`, just under its declared
    heading when `rel` holds a declared section, else at the end; return its
    line number."""
    path = copy / rel
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    heading = dict(SECTIONS).get(rel)
    at = lines.index(heading + "\n") + 1 if heading else len(lines)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    lines.insert(at, text + "\n")
    path.write_text("".join(lines), encoding="utf-8", newline="\n")
    return at + 1


def test_shipped_surface_scans_clean():
    assert scan(KIT) == []


def test_the_vocabulary_is_read():
    """Catches a scan that reads no vocabulary: a token in a declared id space
    is reported against the space set."""
    assert scan(KIT, spaces=("SN", "PYTEST")) == [
        ("trace.WATERMARK_SPACES", 2, "pytest")
    ]


@pytest.mark.parametrize(
    "rel",
    [
        "registries/system-requirements.template.toml",
        "registries/assets.template.csv",
        "id-watermark.template",
        "work/WI-000.template.md",
        "PROCESS.md",
        "INTERFACES.template.md",
    ],
)
@pytest.mark.parametrize(
    "planted, token",
    [("Run pytest before review.", "pytest"), ("See src/app.py.", "src/app.py")],
)
def test_a_planted_token_is_reported_with_file_and_line(kit_copy, rel, planted, token):
    """Catches a scan that skips a surface class (one member of each is
    planted, a declared section inside its section), matches words only
    (missing the extension rule), or reports a hit without its place or with a
    line numbered from the section rather than the file."""
    line = _plant(kit_copy, rel, planted)
    assert scan(kit_copy) == [(rel, line, token)]


@pytest.mark.parametrize(
    "named",
    [
        "scripts/trace.py",
        "trace.py",
        "**scripts/trace.py**",
        "*trace.py*",
        "[trace](scripts/trace.py#L3)",
        "trace.py’s checks",
    ],
)
def test_a_kit_script_name_is_not_reported(kit_copy, named):
    """Catches an exemption that is missing, so the kit's own checks named in
    a template would read as the adopter's language, or one that a Markdown
    decoration around the name defeats."""
    _plant(kit_copy, "registries/system-requirements.template.toml", named)
    assert scan(kit_copy) == []


@pytest.mark.parametrize(
    "named",
    [
        "src/check.py",
        "project-trajectory/scripts/trace.py",
        "nope.py",
        "tests/*.py",
        "tests/test_*.py",
        "src\\check.py",
        "**/*.py",
    ],
)
def test_a_py_path_beyond_the_exemption_is_reported(kit_copy, named):
    """Catches an exemption that matches on the script name alone or on a
    fragment of the path (a Windows separator or a wildcard name cutting the
    token short), or exempts any `.py` path."""
    rel = "registries/system-requirements.template.toml"
    line = _plant(kit_copy, rel, named)
    assert scan(kit_copy) == [(rel, line, named)]


@pytest.mark.parametrize(
    "planted, token",
    [
        ("See **src/app.py** for it.", "src/app.py"),
        ("See *src/app.py* for it.", "src/app.py"),
        ("see [app](src/app.py#L3) here", "src/app.py"),
        ("src/app.py*", "src/app.py"),
        ("app.py’s", "app.py"),
        ("app.py—then", "app.py"),
        ("app.py&x", "app.py"),
        ("https://x/y.py?raw=1", "//x/y.py"),
    ],
)
def test_an_extension_ends_at_any_non_name_character(kit_copy, planted, token):
    """Catches a match whose end depends on a set of separators, so an
    extension followed by emphasis, an anchor, a wildcard, a curly apostrophe,
    a dash, an ampersand or a query goes unreported."""
    rel = "registries/system-requirements.template.toml"
    line = _plant(kit_copy, rel, planted)
    assert scan(kit_copy) == [(rel, line, token)]


def test_a_removed_section_heading_fails(kit_copy):
    """Catches a scan that skips a missing section rather than failing."""
    rel = "PROCESS.md"
    text = (kit_copy / rel).read_text(encoding="utf-8")
    text = text.replace("## 2. Identifier scheme\n", "## 2. Identifiers\n")
    (kit_copy / rel).write_text(text, encoding="utf-8", newline="\n")
    with pytest.raises(AssertionError, match="Identifier scheme"):
        scan(kit_copy)


def test_an_empty_glob_fails(kit_copy):
    """Catches a scan that reads no template as a clean surface."""
    for path in (kit_copy / "registries").glob("*.template.csv"):
        path.unlink()
    with pytest.raises(AssertionError, match="matched nothing"):
        scan(kit_copy)
