"""WI-340: the duplicate census's CLASSIFICATION must stay an audit, not a bucket.

`docs/dupes-allow` is both the allowlist and the census (WI-078/WI-276): every
sanctioned duplicated block is one line, grouped under a named class whose
header states a DISPOSITION — `deliberate`, `extract WI-nnn`, or `debt WI-nnn`.
`check_dupes.py` itself ignores all of that: comments are inert to it, so the
grouping is exactly the kind of prose that rots silently. It has rotted twice:

  * WI-334 signed "MOST of the blocks are the deliberate CLI preamble" over 164
    sanctions; 127-REVIEW-A reconstructed 34 vs 50 and refuted it.
  * WI-338's replacement audit reached "0 unclassified" only because all 64
    SAME-FILE blocks went into one `intra-module` class charged wholesale to
    WI-280. 128-REVIEW-A (BLOCKER 2) refuted that too: a class you can compute
    from two path strings without reading the block is metadata, not an
    acceptance rationale — and WI-304 had already made and retracted the same
    mistake, extracting the boilerplate instead of charging it to WI-280.

Both failures share one shape: a class broad enough to make the count reach
zero. So this guard checks the properties a broad class breaks —

  1. the grouping covers the emitted census EXACTLY (multiset, count-aware), so
     a re-stamp cannot leave classified lines behind or invent them;
  2. every class declares one valid disposition and a reason;
  3. every declared header count matches its section;
  4. the audit header's distribution table matches the sections it describes;
  5. a class charged to a WI names a WI that EXISTS, is still OPEN, and whose
     registry row NAMES every module in the class — this is the anti-catch-all
     rule, and it is what the old `intra-module` class failed: WI-280's row
     names gen_trajectory and the session/train/route objects, never
     check_docs.py, gen_arch_map.py or gen_okf.py;
  6. no class is named after the PATH RELATION between its two files. That is
     the metadata, and naming a class for it is how a bucket gets built.

Every one of the six is mutation-proven in the tests at the bottom of this file:
each check is run against a census deliberately broken in that one way, and must
fail. A guard that cannot fail is not a guard (WI-293).
"""

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest
from conftest import load_script

ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "docs/dupes-allow"
WI_WORK = ROOT / "docs/work"
SCRIPTS = ROOT / "project-trajectory/scripts"

HEADER_RE = re.compile(r"^# --- (?P<name>[A-Za-z0-9-]+) \((?P<n>\d+) blocks?\)")
DISPOSITION_RE = re.compile(
    r"^# disposition: (deliberate|extract WI-\d+|debt WI-\d+)\s*$"
)
DISTRIBUTION_RE = re.compile(
    r"^#\s+(?P<name>[a-z0-9-]+)\s+(?P<n>\d+)\s+(?:\(\d+%\)\s+)?"
    r"(?P<disp>deliberate|extract WI-\d+|debt WI-\d+)\s*$"
)
# A class must be named for WHAT the block is, never for how its two paths
# relate. `intra-module`/`same-file` is the shape 128-REVIEW-A refuted; the
# cross- forms are the same error mirrored.
PATH_RELATION_NAMES = {
    "intra-module",
    "intra-file",
    "same-file",
    "same-path",
    "cross-module",
    "cross-file",
    "inter-module",
}


class Section:
    def __init__(self, name, declared, line):
        self.name = name
        self.declared = declared
        self.line = line
        self.disposition = None
        self.prose = []
        self.entries = []

    @property
    def modules(self):
        """Every distinct module basename named by this class's entries."""
        mods = set()
        for entry in self.entries:
            _fp, _sp, pair = entry.partition(" ")
            for side in pair.split("=="):
                side = side.strip()
                if side:
                    mods.add(Path(side).name)
        return mods


def parse_census(text):
    """(sections, distribution, stray_entries) — the census's declared structure.

    `stray_entries` are sanction lines that precede every class header; they are
    a finding in themselves (an entry nobody classified).
    """
    sections, distribution, stray = [], {}, []
    current = None
    for raw in text.splitlines():
        line = raw.strip()
        header = HEADER_RE.match(raw)
        if header:
            current = Section(header.group("name"), int(header.group("n")), raw)
            sections.append(current)
            continue
        if line.startswith("#"):
            if current is not None and current.disposition is None:
                match = DISPOSITION_RE.match(line)
                if match:
                    current.disposition = match.group(1)
                    continue
            if current is not None and current.entries == []:
                current.prose.append(line)
            dist = DISTRIBUTION_RE.match(line)
            if dist and current is None:
                distribution[dist.group("name")] = (
                    int(dist.group("n")),
                    dist.group("disp"),
                )
            continue
        if not line:
            continue
        if current is None:
            stray.append(line)
        else:
            current.entries.append(line)
    return sections, distribution, stray


def load_wi_rows():
    """WI rows from the registry's one home, the `docs/work/` spec folder — read
    through the validator's own reader (Phase 5: the CSV home retired, so there
    is no second home for this audit to have an opinion about)."""
    ct = load_script("check_trajectory")
    return {row["WI-ID"]: row for row in ct.read_spec_rows(WI_WORK)}


def emitted_census():
    """The census check_dupes ACTUALLY finds right now, as a multiset."""
    proc = subprocess.run(
        # Relative --src on purpose: check_dupes echoes the path it was GIVEN,
        # so an absolute one would emit lines that could never match the census.
        [
            sys.executable,
            str(SCRIPTS / "check_dupes.py"),
            "--src",
            "project-trajectory/scripts",
            "--emit-census",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
        cwd=str(ROOT),
    )
    assert proc.returncode == 0, proc.stderr
    return Counter(ln.strip() for ln in proc.stdout.splitlines() if ln.strip())


# --------------------------------------------------------------------------
# The six checks, as functions so the mutation tests can re-run them on a
# deliberately broken census. Each returns a list of findings (empty == clean).
# --------------------------------------------------------------------------


def check_grouping_covers_census(sections, stray, emitted):
    grouped = Counter(e for s in sections for e in s.entries)
    findings = ["unclassified sanction line: " + e for e in stray]
    for entry, n in (grouped - emitted).items():
        findings.append(
            "classified but not found by check_dupes ({}x): {}".format(n, entry)
        )
    for entry, n in (emitted - grouped).items():
        findings.append(
            "found by check_dupes but classified nowhere ({}x): {}".format(n, entry)
        )
    return findings


def check_dispositions(sections):
    findings = []
    for s in sections:
        if s.disposition is None:
            findings.append("{}: no `# disposition:` line".format(s.name))
        if not s.prose:
            findings.append("{}: no reason under the header".format(s.name))
    return findings


def check_counts(sections):
    return [
        "{}: header says {} blocks, section holds {}".format(
            s.name, s.declared, len(s.entries)
        )
        for s in sections
        if s.declared != len(s.entries)
    ]


def check_distribution_table(sections, distribution):
    findings = []
    by_name = {s.name: s for s in sections}
    for name, (n, disp) in distribution.items():
        if name not in by_name:
            findings.append("distribution row `{}` names no class".format(name))
            continue
        s = by_name[name]
        if n != len(s.entries):
            findings.append(
                "distribution says {} has {} blocks; it has {}".format(
                    name, n, len(s.entries)
                )
            )
        if disp != s.disposition:
            findings.append(
                "distribution says {} is `{}`; its header says `{}`".format(
                    name, disp, s.disposition
                )
            )
    for name in by_name:
        if name not in distribution:
            findings.append(
                "class `{}` is missing from the distribution table".format(name)
            )
    return findings


def check_charged_classes_name_their_modules(sections, wi_rows):
    """The anti-catch-all rule.

    Charging a block to a WI is a claim that THAT work item will dissolve THIS
    duplication. The claim is only checkable if the WI's row names the module,
    so require it — and require the WI to still be open, since a closed WI
    cannot own future work.
    """
    findings = []
    for s in sections:
        if s.disposition in (None, "deliberate"):
            continue
        wid = s.disposition.split()[-1]
        row = wi_rows.get(wid)
        if row is None:
            findings.append(
                "{}: charged to {}, which is not in the registry".format(s.name, wid)
            )
            continue
        status = (row.get("Status") or "").strip().lower()
        if status in ("done", "retired"):
            findings.append(
                "{}: charged to {}, which is already {}".format(s.name, wid, status)
            )
        text = " ".join((row.get(k) or "") for k in ("Title", "Deliverable"))
        for module in sorted(s.modules):
            if module not in text and Path(module).stem not in text:
                findings.append(
                    "{}: charged to {}, whose row never names {} — a WI cannot own "
                    "duplication in a module it does not mention".format(
                        s.name, wid, module
                    )
                )
    return findings


def check_no_path_relation_class(sections):
    return [
        "{}: a class named for the path relation is metadata, not a rationale".format(
            s.name
        )
        for s in sections
        if s.name.lower() in PATH_RELATION_NAMES
    ]


@pytest.fixture(scope="module")
def census():
    return parse_census(CENSUS.read_text(encoding="utf-8"))


def test_every_sanctioned_block_is_classified_exactly_once(census):
    sections, _distribution, stray = census
    assert check_grouping_covers_census(sections, stray, emitted_census()) == []


def test_every_class_states_a_disposition_and_a_reason(census):
    sections, _distribution, _stray = census
    assert check_dispositions(sections) == []


def test_every_header_count_matches_its_section(census):
    sections, _distribution, _stray = census
    assert check_counts(sections) == []


def test_the_distribution_table_matches_the_sections(census):
    sections, distribution, _stray = census
    assert distribution, "the audit header has no distribution table"
    assert check_distribution_table(sections, distribution) == []


def test_a_class_charged_to_a_wi_names_a_wi_that_owns_those_modules(census):
    sections, _distribution, _stray = census
    assert check_charged_classes_name_their_modules(sections, load_wi_rows()) == []


def test_no_class_is_named_after_the_path_relation(census):
    sections, _distribution, _stray = census
    assert check_no_path_relation_class(sections) == []


# (test_the_triage_is_not_one_broad_class — the same-file majority rule —
# RETIRED at concurrency-restructure Phase 5 per the 2026-07-28 audit ruling on
# WI-350: 129-REVIEW-A drove and bypassed it with an even split plus a
# keyword-stuffed row, and the Phase 5 deletion then FALSE-POSITIVED it the
# other way — retiring the dispatcher's same-file classes honestly concentrated
# the remainder in graph-layout (a single-module debt class charged to WI-280),
# which the majority arithmetic cannot tell from a rebuilt catch-all. The
# property is a Reviewer-tier judgment now, recorded as such in
# docs/enforcement-audit.md; the checkable halves — per-section counts, the
# distribution table, and charged-class ownership — remain the tests above.)


# --------------------------------------------------------------------------
# Mutation proofs — each check must FAIL on a census broken in exactly its way.
# --------------------------------------------------------------------------


def _mutate(text, old, new, count=1):
    assert text.count(old) >= count, "fixture premise gone: {!r} not in census".format(
        old
    )
    return text.replace(old, new, count)


def test_mutation_a_dropped_line_reds_the_coverage_check(census):
    sections, _d, _s = census
    victim = sections[0].entries[0]
    broken = parse_census(
        _mutate(CENSUS.read_text(encoding="utf-8"), victim + "\n", "")
    )
    assert check_grouping_covers_census(broken[0], broken[2], emitted_census()) != []


def test_mutation_a_removed_disposition_reds_the_disposition_check():
    broken = parse_census(
        _mutate(CENSUS.read_text(encoding="utf-8"), "# disposition: deliberate\n", "")
    )
    assert check_dispositions(broken[0]) != []


def test_mutation_a_wrong_header_count_reds_the_count_check():
    broken = parse_census(
        _mutate(
            CENSUS.read_text(encoding="utf-8"),
            "# --- cli (96 blocks)",
            "# --- cli (89 blocks)",
        )
    )
    assert check_counts(broken[0]) != []


def test_mutation_a_stale_distribution_row_reds_the_table_check():
    broken = parse_census(
        _mutate(
            CENSUS.read_text(encoding="utf-8"),
            "#   cli                   96",
            "#   cli                   82",
        )
    )
    assert check_distribution_table(broken[0], broken[1]) != []


def test_mutation_charging_a_foreign_module_to_wi_280_reds_the_ownership_check(census):
    """The exact defect 128-REVIEW-A found, replayed.

    Put a check_docs.py block under a WI-280-charged class — the same move
    WI-338's `intra-module` bucket made 64 times — and the ownership rule must
    catch it, because WI-280's row never names check_docs. WI-280 S9 dissolved
    the last debt-charged class in the live census, so the mutation FABRICATES
    the charged class it replays: the rule outlives the classes it once
    policed, and this proves it still bites.
    """
    sections, _d, _s = census
    foreign = next(
        e for s in sections for e in s.entries if "check_docs.py == project" in e
    )
    text = CENSUS.read_text(encoding="utf-8") + (
        "\n# --- fabricated-debt (1 block) -----------------------------------\n"
        "# disposition: debt WI-280\n"
        "# mutation fixture: a check_docs block charged to WI-280.\n" + foreign + "\n"
    )
    broken = parse_census(text)
    findings = check_charged_classes_name_their_modules(broken[0], load_wi_rows())
    assert any("check_docs.py" in f for f in findings), findings


def test_mutation_a_path_relation_class_name_reds_that_check(census):
    sections, _d, _s = census
    victim = sections[-1]
    broken = parse_census(
        _mutate(
            CENSUS.read_text(encoding="utf-8"),
            "# --- {} (".format(victim.name),
            "# --- intra-module (",
        )
    )
    assert check_no_path_relation_class(broken[0]) != []
