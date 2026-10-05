"""An overrule is acted on in the same commit, and the retired key migrates
(WI-818; owner direction 2026-10-04).

The commit that sets a delegated-decisions entry `owner = "overruled"` must,
in the same diff, file or amend a queued or active work item whose spec cites
the entry as `docs/decisions/<run>.toml#D-NNN`. It is the ruling sync's
commit-against-its-parent shape (OI-102 Q3) and runs in the same two places:
the pre-commit hook's `ruling-sync` step over HEAD and the staged tree, and
the merge slot over each lane commit against its first parent, so a
`--no-verify` commit is still refused before it lands. Amending the queued row
the decision is scoped to satisfies it: nothing is minted.

The migrator rewrites `reviewed = true` to `owner = "confirmed"` and drops
`reviewed = false`, keeping each note and every other line.
"""

import string
import subprocess
import tomllib

import pytest

from conftest import SCRIPTS, load_script, pin_autocrlf, run_py

ar = load_script("acceptance_record")
integrate = load_script("integrate")
migrate = load_script("migrate_decisions")
decisions = ar._kitdecisions

RECORD = "docs/decisions/wi-050.toml"
CITE = RECORD + "#D-002"


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, encoding="utf-8"
    )
    assert proc.returncode == 0, proc.stderr
    return proc.stdout.strip()


def _entry(eid, owner=None, review=""):
    line = "" if owner is None else 'owner = "{}"\n'.format(owner)
    return (
        '[decision.{}]\ndecided = "d"\nalternative = "a"\nreversal_cost = "c"\n'
        'why_not_escalated = "w"\nreview = "{}"\n{}\n'.format(eid, review, line)
    )


def _record(root, d002_owner=None, rel=None):
    path = root / (rel or RECORD)
    path.parent.mkdir(parents=True, exist_ok=True)
    note = "Overruled: keep the flag." if d002_owner == "overruled" else ""
    path.write_text(
        "high_risk = []\n\n{}{}".format(
            _entry("D-001", "confirmed"), _entry("D-002", d002_owner, note)
        ),
        encoding="utf-8",
        newline="\n",
    )


def _spec(root, wid, prose, where="queued", slug="row"):
    path = root / "docs/work" / where / "{}-{}.md".format(wid, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '+++\nid = "{}"\ntitle = "row"\nsafety_class = "ordinary"\n+++\n\n'
        "## Done-when\n\n- {}\n".format(wid, prose),
        encoding="utf-8",
        newline="\n",
    )
    return path


def _commit(root, msg):
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "--no-verify", "-m", msg)
    return _git(root, "rev-parse", "HEAD")


def _base(tmp_path):
    """A record with D-002 not yet seen, and the queued row it is scoped to."""
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q", "-b", "main")
    pin_autocrlf(root)
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "t")
    _git(root, "config", "commit.gpgsign", "false")
    _record(root)
    _spec(root, "WI-051", "The export flag is dropped.")
    _commit(root, "base")
    return root


def _specs(root):
    return sorted(p.name for p in (root / "docs/work").rglob("WI-*.md"))


def test_an_overrule_with_no_citing_row_is_refused_at_the_commit(tmp_path):
    root = _base(tmp_path)
    _record(root, "overruled")
    _git(root, "add", "-A")
    (line,) = ar.staged_ruling_sync_lines(root)
    assert CITE in line and "overruled" in line
    proc = run_py([SCRIPTS / "check.py", "--ruling-sync"], root)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "FAIL  ruling-sync" in proc.stdout and CITE in proc.stdout


def test_a_citation_in_an_untouched_row_does_not_discharge_it(tmp_path):
    # The citing row must be filed or amended IN the overrule's commit: a row
    # that already cited the entry, left untouched, is not the act.
    root = _base(tmp_path)
    _spec(root, "WI-052", "Revisit {}.".format(CITE))
    _commit(root, "an earlier citation")
    _record(root, "overruled")
    _git(root, "add", "-A")
    (line,) = ar.staged_ruling_sync_lines(root)
    assert CITE in line


def test_an_overrule_filed_with_a_new_citing_row_passes(tmp_path):
    root = _base(tmp_path)
    _record(root, "overruled")
    _spec(root, "WI-060", "Restore the export flag ({}).".format(CITE))
    _git(root, "add", "-A")
    assert ar.staged_ruling_sync_lines(root) == []
    proc = run_py([SCRIPTS / "check.py", "--ruling-sync"], root)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_an_overrule_amending_its_queued_row_passes_with_nothing_minted(tmp_path):
    root = _base(tmp_path)
    before = _specs(root)
    _record(root, "overruled")
    _spec(root, "WI-051", "The export flag is kept, per {}.".format(CITE))
    _git(root, "add", "-A")
    assert ar.staged_ruling_sync_lines(root) == []
    assert _specs(root) == before  # amended in place: no row minted


def test_an_active_row_counts_and_a_terminal_one_does_not(tmp_path):
    root = _base(tmp_path)
    _record(root, "overruled")
    _spec(root, "WI-061", "Undo {}.".format(CITE), where="active/wi-061")
    _git(root, "add", "-A")
    assert ar.staged_ruling_sync_lines(root) == []
    _git(root, "reset", "-q", "--hard")
    _git(root, "clean", "-qfd")
    _record(root, "overruled")
    path = root / "docs/archive/work/complete/WI-062-row.md"
    path.parent.mkdir(parents=True)
    path.write_text("Undo {}.\n".format(CITE), encoding="utf-8")
    _git(root, "add", "-A")
    assert len(ar.staged_ruling_sync_lines(root)) == 1


def test_a_citation_of_another_entry_does_not_match(tmp_path):
    root = _base(tmp_path)
    _record(root, "overruled")
    _spec(root, "WI-051", "See {}0 and {}.".format(CITE, RECORD + "#D-001"))
    _git(root, "add", "-A")
    (line,) = ar.staged_ruling_sync_lines(root)
    assert CITE in line


def test_an_entry_already_overruled_owes_nothing_again(tmp_path):
    root = _base(tmp_path)
    _record(root, "overruled")
    _spec(root, "WI-051", "Kept, per {}.".format(CITE))
    _commit(root, "overrule with its row")
    path = root / RECORD
    path.write_text(path.read_text() + "# an unrelated edit\n", encoding="utf-8")
    _git(root, "add", "-A")
    assert ar.staged_ruling_sync_lines(root) == []


def test_a_no_verify_overrule_is_refused_at_the_merge_slot(tmp_path):
    root = _base(tmp_path)
    _git(root, "checkout", "-q", "-b", "wi-070")
    _record(root, "overruled")
    bad = _commit(root, "overrule without a row")  # --no-verify
    _git(root, "checkout", "-q", "main")
    refusal = integrate._ruling_sync_refusal(root, "wi-070")
    assert refusal is not None and bad[:10] in refusal
    assert CITE in refusal and "nothing was merged" in refusal
    # A later commit that files the row does not repair it: each commit is
    # judged against its own parent.
    _git(root, "checkout", "-q", "wi-070")
    _spec(root, "WI-051", "Kept, per {}.".format(CITE))
    _commit(root, "amend the row afterwards")
    _git(root, "checkout", "-q", "main")
    assert integrate._ruling_sync_refusal(root, "wi-070") is not None
    # A lane whose overrule commit carries the amendment lands.
    _git(root, "checkout", "-q", "-b", "wi-071")
    _record(root, "overruled")
    _spec(root, "WI-051", "Kept, per {}.".format(CITE))
    _commit(root, "overrule with the row")
    _git(root, "checkout", "-q", "main")
    assert integrate._ruling_sync_refusal(root, "wi-071") is None


def test_a_record_that_does_not_parse_is_refused_at_the_commit_and_the_merge_slot(
    tmp_path,
):
    # Fail closed (owner rule: no degenerate path): an overrule behind a syntax
    # error is unreadable, never "no overrule". Both admission points refuse,
    # naming the record and the parse error, and a later commit that repairs
    # the syntax while dropping the verdict does not launder the lane.
    root = _base(tmp_path)
    _git(root, "checkout", "-q", "-b", "wi-072")
    _record(root, "overruled")
    path = root / RECORD
    path.write_text(path.read_text() + "broken = [\n", encoding="utf-8")
    _git(root, "add", "-A")
    (line,) = ar.staged_ruling_sync_lines(root)
    assert RECORD in line and "does not parse" in line
    bad = _commit(root, "overrule behind a syntax error")  # --no-verify
    _record(root)
    _commit(root, "repair the syntax, drop the verdict")
    _git(root, "checkout", "-q", "main")
    refusal = integrate._ruling_sync_refusal(root, "wi-072")
    assert refusal is not None and bad[:10] in refusal and RECORD in refusal


def test_a_repair_of_an_unparseable_parent_owes_every_overrule_it_shows(tmp_path):
    # The parent side unreadable reads as overruling nothing, so the commit
    # that makes the record readable owes the work for each overrule in it.
    root = _base(tmp_path)
    path = root / RECORD
    path.write_text(path.read_text() + "broken = [\n", encoding="utf-8")
    _commit(root, "a record broken before this rule")
    _record(root, "overruled")
    _git(root, "add", "-A")
    (line,) = ar.staged_ruling_sync_lines(root)
    assert CITE in line and "overruled" in line


def test_an_overrule_beside_the_retired_key_still_owes_its_work(tmp_path):
    # The surface reads such an entry as not yet seen, but the coupling reads
    # the `owner` key as written: a stale key never lets an overrule skip it.
    root = _base(tmp_path)
    _record(root, "overruled")
    path = root / RECORD
    path.write_text(path.read_text() + "reviewed = true\n", encoding="utf-8")
    _git(root, "add", "-A")
    (line,) = ar.staged_ruling_sync_lines(root)
    assert CITE in line


def test_an_unparseable_record_beside_a_cited_overrule_is_still_refused(tmp_path):
    # A parse refusal is never dropped because the same commit's owed
    # overrules are all cited, and it comes before any missing-citer line.
    root = _base(tmp_path)
    _record(root, "overruled")
    broken = root / "docs/decisions/wi-090.toml"
    broken.write_text("high_risk = [\n", encoding="utf-8", newline="\n")
    _spec(root, "WI-051", "Kept, per {}.".format(CITE))
    _git(root, "add", "-A")
    (parse,) = ar.staged_ruling_sync_lines(root)
    assert parse.startswith("docs/decisions/wi-090.toml ") and "does not parse" in parse
    _spec(root, "WI-051", "The export flag is dropped.")
    _git(root, "add", "-A")
    assert ar.staged_ruling_sync_lines(root) == [
        parse,
        "{} is overruled by this commit, and no queued or active work item it "
        "files or amends cites it: the overrule's commit files a work item, or "
        "amends the queued one the decision was scoped to, citing {}".format(
            CITE, CITE
        ),
    ]


def test_an_example_spec_does_not_discharge_an_overrule(tmp_path):
    # The `-000` example is never a work item, so its citation acts on nothing.
    root = _base(tmp_path)
    _record(root, "overruled")
    _spec(root, "WI-000", "Kept, per {}.".format(CITE), slug="example")
    _git(root, "add", "-A")
    assert "WI-000-example.md" in _specs(root)
    (line,) = ar.staged_ruling_sync_lines(root)
    assert line.startswith(CITE + " is overruled"), line


@pytest.mark.parametrize("broken", [False, True])
def test_a_record_path_git_would_quote_is_still_judged(tmp_path, broken):
    # core.quotePath (git's default) quotes and escapes a non-ASCII path in
    # plain `--name-only` output; the sync reads paths NUL-delimited, so such
    # a record is judged like any other at the commit and at the merge slot.
    rel = decisions.record_path("owner-é")
    root = _base(tmp_path)
    _git(root, "config", "core.quotePath", "true")
    _git(root, "checkout", "-q", "-b", "wi-073")
    _record(root, "overruled", rel=rel)
    if broken:
        path = root / rel
        path.write_text(path.read_text(encoding="utf-8") + "broken = [\n", "utf-8")
    _git(root, "add", "-A")
    (line,) = ar.staged_ruling_sync_lines(root)
    assert rel in line
    assert ("does not parse" in line) if broken else (rel + "#D-002" in line)
    bad = _commit(root, "overrule of a quoted record, no citing work")
    _git(root, "checkout", "-q", "main")
    refusal = integrate._ruling_sync_refusal(root, "wi-073")
    assert refusal is not None and bad[:10] in refusal and rel in refusal


def test_a_citing_spec_path_git_would_quote_discharges_the_overrule(tmp_path):
    root = _base(tmp_path)
    _git(root, "config", "core.quotePath", "true")
    _record(root, "overruled")
    _spec(root, "WI-052", "Keep the flag, per {}.".format(CITE), slug="ré")
    _git(root, "add", "-A")
    assert ar.staged_ruling_sync_lines(root) == []


@pytest.mark.parametrize(
    "run",
    [
        "owner+cleanup",
        "owner@cleanup",
        "owner-cleanup",
        "feat/x.y_z",
        "ré",
        "owner\u00a0cleanup",
    ],
)
def test_the_citation_reads_every_run_name_the_record_path_writes(tmp_path, run):
    # One alphabet: whatever `record_path` keeps of a valid branch name, the
    # citation reader matches, so the exact generated citation discharges.
    rel = decisions.record_path(run)
    cite = decisions.citation(rel, "D-002")
    assert decisions.citations("Per `{}`, kept.".format(cite)) == {cite}
    root = _base(tmp_path)
    _git(root, "checkout", "-q", "-b", "wi-074")
    _record(root, "overruled", rel=rel)
    _spec(root, "WI-051", "Keep the flag, per {}.".format(cite))
    _git(root, "add", "-A")
    assert ar.staged_ruling_sync_lines(root) == []
    _commit(root, "overrule with its citing work")
    _git(root, "checkout", "-q", "main")
    assert integrate._ruling_sync_refusal(root, "wi-074") is None


def test_the_citation_reader_takes_no_surrounding_prose():
    text = "(see docs/decisions/a+b.toml#D-002), [docs/decisions/c@d.toml#D-3]."
    assert decisions.citations(text) == {
        "docs/decisions/a+b.toml#D-002",
        "docs/decisions/c@d.toml#D-3",
    }
    assert decisions.citations("docs/decisions/a b.toml#D-1") == set()
    assert decisions.citations("docs/decisions/x/y.toml#D-1") == set()


# --- Sol round 3: the run-name alphabet is git's, and paths read losslessly ----

# What git refuses in ANY branch name, one character at a time (git-check-ref-
# format(1): the ASCII control characters and space, DEL, and ~ ^ : ? * [ \).
GIT_REFUSED = {chr(c) for c in range(0x21)} | set("\x7f~^:?*[\\")
# The characters a branch may carry that a record's filename may not keep
# (WI-818 dispute 1): the path's separator, which becomes `-` (a run is one
# file), and the citation's delimiter, which no record name carries.
SEPARATOR, DELIMITER = "/", "#"
NON_ASCII = ["\u0085", " ", " ", "　", "é"]


def test_the_run_name_alphabet_is_what_git_refuses_plus_two_delimiters():
    # Pinned against git itself for every ASCII punctuation mark, the space,
    # DEL, three controls and whitespace Unicode adds (which git permits), so
    # the set is git's, matched ASCII-only, and never a guess. Only `/` is
    # rewritten; `#` and what git refuses raise, and every other character is
    # kept, so no two names a record can carry share a file by rewriting.
    probed = list(string.punctuation) + [" ", "\x7f", "\x01", "\t", "\n"]
    for ch in probed + NON_ASCII:
        proc = subprocess.run(
            ["git", "check-ref-format", "--branch", "a" + ch + "b"],
            capture_output=True,
        )
        assert (proc.returncode != 0) == (ch in GIT_REFUSED), repr(ch)
    for ch in [chr(c) for c in range(0x80)] + NON_ASCII:
        run = "a" + ch + "b"
        if ch == SEPARATOR:
            assert decisions.record_path(run) == "docs/decisions/a-b.toml"
        elif ch in GIT_REFUSED | {DELIMITER}:
            with pytest.raises(ValueError):
                decisions.record_path(run)
        else:
            want = "docs/decisions/{}.toml".format(run)
            assert decisions.record_path(run) == want, repr(ch)


def test_a_run_name_carrying_the_citation_delimiter_has_no_record(tmp_path):
    # `owner#cleanup` and `owner.toml#D-002` are valid branches. No record is
    # named by either: `#` is refused, never folded into `owner-cleanup`'s file.
    for run in ("owner#cleanup", "owner.toml#D-002"):
        with pytest.raises(ValueError, match="'#'"):
            decisions.record_path(run)
    assert decisions.record_path("owner-cleanup") == "docs/decisions/owner-cleanup.toml"
    # One parse: a spec citing `owner.toml#D-002` discharges that entry and
    # no other record's D-002.
    cite = decisions.record_path("owner") + "#D-002"
    root = _base(tmp_path)
    _record(root, "overruled")
    _record(root, "overruled", rel=decisions.record_path("owner"))
    _spec(root, "WI-051", "Keep the flag, per `{}`.".format(cite))
    _git(root, "add", "-A")
    (line,) = ar.staged_ruling_sync_lines(root)
    assert line.startswith(CITE + " is overruled"), line


def _index_only(root, raw, text):
    """Stage `text` at the raw byte path `raw` through git's plumbing, so no
    file of that name is needed on disk."""
    sha = subprocess.run(
        ["git", "-C", str(root), "hash-object", "-w", "--stdin"],
        input=text.encode(),
        capture_output=True,
        check=True,
    ).stdout.strip()
    subprocess.run(
        ["git", "-C", str(root), "update-index", "--add", "-z", "--index-info"],
        input=b"100644 " + sha + b"\t" + raw + b"\0",
        capture_output=True,
        check=True,
    )


def test_a_record_path_that_is_not_utf8_is_refused_never_read_as_absent(tmp_path):
    # Git keeps a path's raw bytes. Read through a replacing decoder, the path
    # `owner-\xff.toml` came back as another path that no tree lists, so the
    # overrule escaped the sync. The listing is read losslessly, and a path
    # the kit cannot hand back to git as text is refused by name.
    root = _base(tmp_path)
    _git(root, "checkout", "-q", "-b", "wi-076")
    raw = b"docs/decisions/owner-\xff.toml"
    _index_only(root, raw, "high_risk = []\n" + _entry("D-002", "overruled", "U"))
    (listed,) = ar._git_paths(root, ["diff", "--cached", "--name-only"])
    assert listed.encode("utf-8", "surrogateescape") == raw
    (line,) = ar.staged_ruling_sync_lines(root)
    assert "docs/decisions/owner-\\xff.toml" in line and "not UTF-8" in line
    line.encode("utf-8")  # printable on a UTF-8 stream: no lone surrogate
    _git(root, "commit", "-q", "--no-verify", "-m", "raw path overrule")
    (line,) = ar.commit_ruling_sync_lines(root, _git(root, "rev-parse", "HEAD"))
    assert "not UTF-8" in line
    _git(root, "checkout", "-q", "main")
    refusal = integrate._ruling_sync_refusal(root, "wi-076")
    assert refusal is not None and "not UTF-8" in refusal


def test_a_path_that_is_not_utf8_and_never_read_is_not_refused(tmp_path):
    # The sync reads only the records and specs it judges: a non-UTF-8 path
    # elsewhere in the diff is listed losslessly and left alone.
    root = _base(tmp_path)
    _index_only(root, b"src/caf\xe9.txt", "data\n")
    assert ar.staged_ruling_sync_lines(root) == []


FIXTURE = """\
# a record from before WI-818
high_risk = ["D-002"]

[decision.D-001]
decided = "d1"
alternative = "a"
reversal_cost = "c"
why_not_escalated = "w"
review = "Confirmed by the owner, 2026-10-04."
reviewed = true

[decision.D-002]
decided = "d2"
alternative = "a"
reversal_cost = "c"
why_not_escalated = "w"
review = ""
reviewed = false

[decision.D-003]
decided = "d3"
alternative = "a"
reversal_cost = "c"
why_not_escalated = "w"
review = "Looked."
reviewed = "maybe"
"""


def test_the_migrator_rewrites_the_retired_key_keeping_each_note():
    text, left = decisions.migrate_text(FIXTURE)
    assert left == ["D-003"]  # outside the retired vocabulary: left, still a finding
    assert "reviewed = true" not in text and "reviewed = false" not in text
    assert 'review = "Confirmed by the owner, 2026-10-04."\nowner = "confirmed"\n' in (
        text
    )
    assert text.startswith("# a record from before WI-818\n")
    unseen, overruled, confirmed = decisions.review_queue(text)
    assert [e["id"] for e in unseen] == ["D-002", "D-003"] and confirmed == 1
    assert overruled == []
    (finding,) = decisions.record_findings(text)
    assert finding.startswith("D-003: `reviewed` is retired")
    assert decisions.migrate_text(text) == (text, ["D-003"])  # idempotent


ENTRY = '[decision.D-001]\ndecided = "d"\nalternative = "a"\nreversal_cost = "c"\n'
ENTRY += 'why_not_escalated = "w"\n'


def test_the_migrator_drops_a_retired_line_beside_an_existing_owner():
    text = 'high_risk = []\n\n{}review = "Undo."\nowner = "overruled"\n'.format(ENTRY)
    new, left = decisions.migrate_text(text + "reviewed = true\n")
    assert (new, left) == (text, [])


def test_the_migrator_never_rewrites_inside_a_multiline_note():
    note = '"""\nThe old example was:\nreviewed = true\nKeep this note.\n"""'
    head = "high_risk = []\n\n{}review = {}\n".format(ENTRY, note)
    text = head + "reviewed = true\n"
    new, left = decisions.migrate_text(text)
    assert (new, left) == (head + 'owner = "confirmed"\n', [])
    entry = tomllib.loads(new)["decision"]["D-001"]
    assert entry["review"] == tomllib.loads(text)["decision"]["D-001"]["review"]
    assert entry["owner"] == "confirmed" and "reviewed" not in entry


def test_the_migrator_rewrites_a_multiline_string_verdict_whole():
    for literal in ('"""\ntrue\n"""', "'''\nyes\n'''"):
        text = 'high_risk = []\n\n{}review = "r"\nreviewed = {}\n# after\n'.format(
            ENTRY, literal
        )
        new, left = decisions.migrate_text(text)
        assert left == []
        assert new.endswith('review = "r"\nowner = "confirmed"\n# after\n'), new
        assert tomllib.loads(new)["decision"]["D-001"]["owner"] == "confirmed"


def test_the_migrator_refuses_what_it_cannot_rewrite_in_place():
    # An inline-table record carries the retired key where no top-level
    # assignment can be rewritten: the re-parse would differ, so it refuses.
    text = 'high_risk = []\ndecision = { D-001 = { decided = "d", reviewed = true } }\n'
    with pytest.raises(ValueError, match="re-parse"):
        decisions.migrate_text(text)


def test_the_migrator_keeps_a_trailing_comment_on_the_line_it_rewrites():
    head = 'high_risk = []\n\n{}review = "r"\n'.format(ENTRY)
    note = "# Owner confirmed after discussing the rollback"
    new, left = decisions.migrate_text(head + "  reviewed = true  {}\r\n".format(note))
    assert (new, left) == (head + '  owner = "confirmed"  {}\r\n'.format(note), [])
    new, left = decisions.migrate_text(head + "reviewed = false # Waiting\n")
    assert (new, left) == (head + "# Waiting\n", [])
    new, _ = decisions.migrate_text(head + "reviewed = 'yes' # kept\n")
    assert new == head + 'owner = "confirmed" # kept\n'
    statement = 'reviewed = "a # b" # c\n'  # a `#` inside a string is no comment
    assert decisions._comment_start(statement) == statement.rindex("#")
    new, _ = decisions.migrate_text(head + 'reviewed = """\n# no\ntrue\n""" # kept\n')
    assert (new, _) == (head + 'reviewed = """\n# no\ntrue\n""" # kept\n', ["D-001"])


@pytest.mark.parametrize("nan", ["nan", "+nan", "-nan"])
def test_the_migrator_accepts_a_record_carrying_nan(tmp_path, nan):
    clean = 'high_risk = []\n\n{}review = "r"\nextra = {}\n'.format(ENTRY, nan)
    assert decisions.record_findings(clean) == []
    assert decisions.migrate_text(clean) == (clean, [])
    old = clean + "reviewed = true\n"
    assert decisions.migrate_text(old) == (clean + 'owner = "confirmed"\n', [])
    folder = tmp_path / "docs/decisions"
    folder.mkdir(parents=True)
    (folder / "clean.toml").write_text(clean, encoding="utf-8")
    assert migrate.main(["--root", str(tmp_path), "--check"]) == 0


def test_the_migrator_cli_rewrites_the_records_and_check_reports_them(tmp_path):
    folder = tmp_path / "docs/decisions"
    folder.mkdir(parents=True)
    path = folder / "old.toml"
    path.write_text(FIXTURE.replace('"maybe"', "true"), encoding="utf-8")
    proc = run_py([SCRIPTS / "migrate_decisions.py", "--check"], tmp_path)
    assert proc.returncode == 1 and "old.toml" in proc.stdout
    assert "reviewed = true" in path.read_text()  # --check writes nothing
    proc = run_py([SCRIPTS / "migrate_decisions.py"], tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "reviewed" not in path.read_text().replace("review =", "")
    assert decisions.record_findings(path.read_text()) == []
    proc = run_py([SCRIPTS / "migrate_decisions.py", "--check"], tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert migrate.main(["--root", str(tmp_path), "--check"]) == 0


# --- Dispute 1 ruling: the migrator clauses LLR-304 states and no test held ---

OLD_HEAD = 'high_risk = []\n\n{}review = "r"\n'.format(ENTRY)


def test_the_migrator_reads_a_numeric_retired_value():
    assert decisions.migrate_text(OLD_HEAD + "reviewed = 1\n") == (
        OLD_HEAD + 'owner = "confirmed"\n',
        [],
    )
    assert decisions.migrate_text(OLD_HEAD + "reviewed = 0\n") == (OLD_HEAD, [])


def test_the_migrator_reads_a_multiline_note_holding_a_lone_quote():
    # The note's lone `"` must not end the multiline string, or the note's own
    # `reviewed = true` line would read as a statement and be rewritten.
    note = '"""a "quoted\nreviewed = true\n"""'
    head = "high_risk = []\n\n{}review = {}\n".format(ENTRY, note)
    new, left = decisions.migrate_text(head + "reviewed = true\n")
    assert (new, left) == (head + 'owner = "confirmed"\n', [])
    assert tomllib.loads(new)["decision"]["D-001"]["review"] == (
        'a "quoted\nreviewed = true\n'
    )


def test_the_migrator_reads_past_a_comment_holding_a_quote_or_bracket():
    text = OLD_HEAD + "# the owner's \"call [see\nreviewed = true\n"
    new, left = decisions.migrate_text(text)
    assert (new, left) == (
        OLD_HEAD + '# the owner\'s "call [see\nowner = "confirmed"\n',
        [],
    )


@pytest.mark.parametrize("line", ['"reviewed" = true', "'reviewed' = \"yes\""])
def test_the_migrator_rewrites_a_quoted_retired_key(line):
    new, left = decisions.migrate_text(OLD_HEAD + line + "\n")
    assert (new, left) == (OLD_HEAD + 'owner = "confirmed"\n', [])


def _records(tmp_path, **texts):
    folder = tmp_path / "docs/decisions"
    folder.mkdir(parents=True)
    for name, text in texts.items():
        (folder / (name + ".toml")).write_bytes(text.encode("utf-8"))
    return folder


def test_the_migrator_cli_keeps_a_records_line_endings(tmp_path):
    old = (OLD_HEAD + "reviewed = true\n").replace("\n", "\r\n")
    clean = (OLD_HEAD + 'owner = "confirmed"\n').replace("\n", "\r\n")
    folder = _records(tmp_path, old=old, clean=clean)
    assert migrate.main(["--root", str(tmp_path)]) == 0
    assert (folder / "old.toml").read_bytes() == clean.encode("utf-8")
    assert (folder / "clean.toml").read_bytes() == clean.encode("utf-8")


def test_the_migrator_cli_names_what_it_leaves_and_fails_on_an_unparseable_record(
    tmp_path, capsys
):
    folder = _records(tmp_path, odd=OLD_HEAD + 'reviewed = "maybe"\n')
    assert migrate.main(["--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "odd.toml: D-001 keeps a `reviewed` value" in out, out
    broken = "high_risk = [\nreviewed = true\n"
    (folder / "broken.toml").write_bytes(broken.encode("utf-8"))
    assert migrate.main(["--root", str(tmp_path)]) == 1
    out = capsys.readouterr().out
    assert "broken.toml: " in out and "left untouched" in out, out
    assert (folder / "broken.toml").read_bytes() == broken.encode("utf-8")
