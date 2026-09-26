#!/usr/bin/env python3
"""check_readability.py — the per-change readability report over declared measures.

A REPORT PER CHANGE, NOT A CENSUS. Code stays readable only if getting worse is
visible when it happens; a census read after the fact arrives once other work is
already built on the worse code. So this reads the CHANGE — the index against
HEAD, or on a claimed work branch the merge base to the tip — runs each measure
the project declares over the parts that change touches, and prints every
worsening in one place, naming the measure, the part and the size of the change.

DECLARED IN THE STACK PROFILE. The measures are a list in `docs/stack.ini`:

    [readability]
    measures = complexity
    gating =

`measures` names what runs, in order; `gating` names the declared measures
whose worsening refuses the change. Reporting is the default because refusing
is a cost a project opts into once it trusts a measure's false-positive rate.
A profile that declares no measure prints one line saying nothing is measured
and exits 0: silence would read as "nothing got worse". A name no adapter
measures, or a gating name the section does not declare as a measure, is
reported on its own line naming it, because a typo that silently measured
nothing would be exactly that false silence.

THE EXIT IS NONZERO ONLY FOR A WORSENING IN A GATING MEASURE (LLR-256), and for
nothing else. A misspelt name and an unreadable change are both reported and
both exit 0: neither is a worsening, and a report that refused on its own
inputs would be a gate the project never declared.

ONE COMPARISON PER MEASURE, OWNED BY THE MEASURE. `MEASURES` maps a name to an
adapter that runs that measure's own comparison over the changed parts; this
module adds only the change and the report. The complexity adapter calls
`check_complexity`'s census, naming rule, baseline reader and comparison
through the module, so a function this report calls worse is one
`check_complexity.py` calls worse and there is no second copy to drift. A
measure joins only once it can name the part it worsened: a worsening with no
part gives a reviewer nothing to look at, and `worsened_findings` refuses one.

A PART IS WHAT THE MEASURE SCORES. For complexity that is a function of the
project's own code — a `.py` file under the profile's `[paths]` source or test
root — and a function is touched when a changed line of the new side falls
inside it (decorators included). An untouched function in a touched file is not
measured: its debt is not this change's worsening.

Contracts: IF-187 — the interface seam this module declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-187: the per-change readability verdict the harness reads back from
    a `[step:readability]`. It reads `[readability]` from the stack profile:
    `measures`, the names to run, and `gating`, the declared measures whose
    worsening refuses. Each worsening is one stdout line naming the measure, the
    part and the delta — WARN for a reporting-only measure, FAIL for a gating
    one — and one summary line follows. A name no adapter measures, and a
    gating name `measures` does not declare, each print one WARN line naming
    it; a change that cannot be read prints one SKIP line per declared measure
    saying why it was not evaluated. Exit 1 only when a gating measure
    worsened; exit 0 for everything else, those lines included. argparse's
    own exit 2 for a malformed command line is the one other code.
"""

import argparse
import ast
import re
import sys
import tempfile
from collections import namedtuple
from pathlib import Path

import check
import check_complexity
from kitlib.config import utf8_console
from kitlib.git import git_bytes, git_out

SECTION = "readability"

# `rev` is the blob side the new text is read from ("" is the index, as in
# `:path`); `parts` maps each changed path to its changed new-side line numbers.
Change = namedtuple("Change", "rev label parts")
Finding = namedtuple("Finding", "measure part delta")

# Rename detection on, so a moved file is a move and not a whole new file; no
# external diff driver, textconv or colour, so the parse reads git's own output.
_DIFF_FLAGS = ("-M", "--diff-filter=d", "--no-ext-diff", "--no-textconv", "--no-color")
_HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", re.M)


def _hunk_lines(block):
    """The new-side line numbers one file's `-U0` hunks touch. A pure deletion
    (`+N,0`) touches line N, the line the removal sits after, so a function
    that only lost lines still counts as changed."""
    lines = set()
    for m in _HUNK.finditer(block):
        start, count = int(m.group(1)), int(m.group(2) or 1)
        lines.update(range(start, start + count) if count else (max(start, 1),))
    return frozenset(lines)


def _range_and_rev(root):
    """`(diff range, blob rev, label)`, or None when a claimed branch's base
    cannot be read. The claimed-branch question is the harness's own
    (`check._work_branch`) and the base is the loop's own integration base
    (`agent_common.default_base`), so this report cannot disagree with either
    about which branch it is on or where its work began."""
    if not check._work_branch(root):
        return ["--cached"], "", "index against HEAD"
    import agent_common  # IF-189; deferred so the trunk path loads none of it

    base = agent_common.default_base(root)
    if not base:
        return None
    return [base, "HEAD"], "HEAD", "merge base {} to HEAD".format(base[:10])


def changed_parts(root):
    """The change under review as a `Change`, or None when it cannot be read
    (no git, no repository, an unreadable claim history).

    The change is the index against HEAD, or merge base to tip on a claimed
    branch. Paths come from `--name-only -z`, which git never quotes, and are
    paired with the `-U0` patch's per-file blocks in the order git emits both.

    Implements: SR-216, LLR-256
    """
    picked = _range_and_rev(root)
    if picked is None:
        return None
    spec, rev, label = picked
    names = git_out(root, ["diff", *spec, *_DIFF_FLAGS, "--name-only", "-z"])
    patch = git_out(root, ["diff", *spec, *_DIFF_FLAGS, "-U0"])
    if names is None or patch is None:
        return None
    paths = [p for p in names.split("\0") if p]
    blocks = re.split(r"(?m)^diff --git ", patch)[1:]
    if len(paths) != len(blocks):
        return None
    return Change(rev, label, {p: _hunk_lines(b) for p, b in zip(paths, blocks)})


def _span(node):
    first = min([node.lineno] + [d.lineno for d in node.decorator_list])
    return range(first, node.end_lineno + 1)


def _touched_functions(root, change, rel, lines, into):
    """The census names of the functions in `rel` that a changed line touches,
    writing the new-side text under `into` for the census to score. None when
    the new side cannot be parsed, which the caller reports as not measured."""
    data = git_bytes(root, ["cat-file", "blob", "{}:{}".format(change.rev, rel)])
    try:
        tree = ast.parse(data.decode("utf-8"))
    except (AttributeError, SyntaxError, UnicodeDecodeError, ValueError):
        return None
    target = into / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {
        name
        for name, node in check_complexity.functions(tree)
        if not lines.isdisjoint(_span(node))
    }


def _complexity_delta(was, now, threshold):
    if was is None:
        return "cognitive {} over the threshold {} with no baseline row (+{})".format(
            now, threshold, now - threshold
        )
    return "cognitive {} -> {} (+{})".format(was, now, now - was)


def _declared_code(root):
    """Path prefixes of the profile's `[paths]` source and test roots (the
    harness's own defaults when undeclared). The project's code is what the
    complexity measure scores: an adopter's vendored kit `scripts/` is not its
    code, and reporting the kit's debt on every re-sync would bury the
    project's own worsenings under warnings nobody can act on."""
    profile = check.load_profile(Path(root) / check.PROFILE_FILE)
    out = []
    for key, default in (("src", check.SRC), ("tests", check.TESTS)):
        value = check._pget(profile, "paths", key, default)
        value = value.strip().replace("\\", "/").strip("/")
        out.append("" if value in ("", ".") else value + "/")
    return tuple(out)


def _complexity(root, change):
    """Cognitive complexity over the touched functions of the declared source
    and test roots, against the stamped `docs/complexity-baseline`: the census
    scores, the baseline reader reads and `compare` decides, all called
    through `check_complexity`."""
    threshold = check_complexity.DEFAULT_THRESHOLD
    code = _declared_code(root)
    touched = {}
    with tempfile.TemporaryDirectory() as tmp:
        for rel, lines in sorted(change.parts.items()):
            if not (rel.endswith(".py") and rel.startswith(code) and lines):
                continue
            names = _touched_functions(root, change, rel, lines, Path(tmp))
            if names is None:
                print(
                    "readability: SKIP - complexity cannot read or parse {} ({})".format(
                        rel, change.label
                    )
                )
            elif names:
                touched[rel] = names
        rows, _modules = check_complexity.census(Path(tmp), ("**/*.py",))
    over = [r for r in rows if r[1] in touched.get(r[0], ()) and r[2] > threshold]
    baseline = check_complexity.read_baseline(Path(root) / check_complexity.BASELINE)
    old = {key: row for key, row in baseline.items() if key[0] in touched}
    grew, _improved = check_complexity.compare(over, old)
    return [
        ("{}::{}".format(rel, name), _complexity_delta(was, now, threshold))
        for rel, name, was, now in grew
    ]


# Implements: SR-216, LLR-256
MEASURES = {"complexity": _complexity}


def declared_measures(profile):
    """`(measures, gating, problems)` from `[readability]`: the declared names
    an adapter measures and the gating names among them, in declared order, and
    one WARN line per name that cannot take part — a measure no adapter
    measures, or a gating name `measures` does not declare. All three are
    empty when the profile or the section is absent."""

    def names(key):
        if profile is None or not profile.has_section(SECTION):
            return []
        raw = profile.get(SECTION, key, fallback="")
        return list(dict.fromkeys(raw.replace(",", " ").split()))

    declared, gating = names("measures"), names("gating")
    problems = [
        "readability: WARN - unknown measure {!r} declared in [{}]; nothing is "
        "measured for it (known: {})".format(n, SECTION, ", ".join(sorted(MEASURES)))
        for n in declared
        if n not in MEASURES
    ]
    problems += [
        "readability: WARN - gating names {!r}, which [{}] measures does not "
        "declare; it gates nothing".format(n, SECTION)
        for n in gating
        if n not in declared
    ]
    measures = [n for n in declared if n in MEASURES]
    return measures, [n for n in gating if n in measures], problems


def worsened_findings(findings, gating, label):
    """`(lines, refused)` — one line per worsening naming the measure, the part
    and the delta, then one summary line. `refused` is True only when a
    worsening belongs to a measure the profile declares gating.

    Implements: SR-216, LLR-256
    """
    lines = []
    for f in findings:
        if not f.part:
            raise ValueError(
                "measure {!r} reported a worsening without naming the part it "
                "worsened".format(f.measure)
            )
        level = "FAIL" if f.measure in gating else "WARN"
        lines.append(
            "readability: {} - {} worsened {}: {}".format(
                level, f.measure, f.part, f.delta
            )
        )
    refused = sum(1 for f in findings if f.measure in gating)
    if not findings:
        lines.append("readability: OK - no worsening ({})".format(label))
    elif refused:
        lines.append(
            "readability: FAIL - {} worsening(s) ({}), {} in a measure declared "
            "gating".format(len(findings), label, refused)
        )
    else:
        lines.append(
            "readability: {} worsening(s) reported ({}); none is in a measure "
            "declared gating, so the change is not refused".format(len(findings), label)
        )
    return lines, bool(refused)


def _report(root, measures, gating):
    """Measure the change and print the report; the exit code."""
    change = changed_parts(root)
    if change is None:
        for name in measures:
            print(
                "readability: SKIP - {} not evaluated: the change cannot be read "
                "(no git repository, or an unreadable claim history)".format(name)
            )
        return 0
    if not change.parts:
        print("readability: OK - no change to measure ({})".format(change.label))
        return 0
    findings = [
        Finding(name, part, delta)
        for name in measures
        for part, delta in MEASURES[name](root, change)
    ]
    lines, refused = worsened_findings(findings, gating, change.label)
    print("\n".join(lines))
    return 1 if refused else 0


def main(argv=None):
    """The `[step:readability]` entry point.

    Implements: SR-216, LLR-256
    """
    utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    profile = check.load_profile(root / check.PROFILE_FILE)
    measures, gating, problems = declared_measures(profile)
    for line in problems:
        print(line)
    if not measures:
        print(
            "readability: no known measure is declared in [{}] of {} - nothing is "
            "measured".format(SECTION, check.PROFILE_FILE.as_posix())
        )
        return 0
    return _report(root, measures, gating)


if __name__ == "__main__":
    sys.exit(main())
