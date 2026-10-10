#!/usr/bin/env python3
"""review_brief.py — an attended launcher's review and critique briefs, rendered
from the kit's own templates, and its review filed as a kit round file.

WHY THIS EXISTS (WI-852; the WI-841 retrospective, proposal §4(a), §6, §7.4).
An attended launcher — a coordinator working from an interactive session —
reviewed its lanes from briefs it hand-wrote outside the repository. Two costs
followed. The hand brief never carried the kit reviewer brief's two clauses
(name the failure classes the change admits and hunt those first; say for a
guard-adding remedy why the defect cannot be made unrepresentable), so findings
arrived as instances and were fixed as instances. And its review files used
their own format, so the generated verdict rollup saw no such lane at all.

So this module RENDERS, it never launches (the launcher is another component's):

  * `render_review` fills `prompts/reviewer.template.md` through `prompts.fill`
    — strict both ways, so an unfilled slot refuses — with the lane's facts as
    its values. The `{round_facts}` slot carries what only the launcher knows:
    the range and whether the round is NARROW (the commits since the last
    reviewed one, answering a named round file's findings) or FULL-LANE (claim
    base to tip, the fresh review a landing is judged on), how to run the tests
    in its scratch area, and that the launcher, not the reviewer, records the
    verdict. The unattended loop fills that slot empty.
  * `render_critique` fills `prompts/critique.template.md` over a work item's
    spec, with a rubric the caller names as its rubric input — the scope
    critique where a row is born.
  * `file_review` writes a review's text, once it validates, as the round file
    `docs/reviews/<lane>/NNN-REVIEW-X-<sha7>[-narrow].md` that
    `kitlib.verdict.round_file` parses and `gen_verdict_rollup.py` renders. A
    narrow round's name carries `-narrow`, which a human reading the rollup's
    file column can see. No reader of round files treats the tag as anything
    but an ordinary name suffix. The verdict gate counts a round file only
    when a committed session log for its lane and ordinal declares a review
    phase, and filing a review writes no session log.

THE BRIEF ASKS FOR THE KIT'S VERDICT FORMAT, AND ONE STEP FILES IT. A reviewer
the launcher keeps out of the worktree writes its verdict to a path in the
launcher's scratch area; `file` then validates it and places it. Validation is
at that one boundary because the text is a model's output: it must open with
`Reviewed: <the full sha>` (the binding between a review and the commit it
judged), carry exactly one `VERDICT:` line whose `findings=N` equals its finding
lines, and a CHANGES-REQUESTED must name a finding. Anything else is refused and
nothing is written.

A JUDGE'S BRIEF NEVER CARRIES THE JUDGED PARTY'S SELF-ASSESSMENT (prompts/
README.md rule 3). There is no slot for a builder's report. A narrow round
names the earlier round file whose findings the range answers — another
reviewer's judgement, labelled a claim under judgement, never the premise.

Stdlib only, Python 3.11+, Windows/POSIX.

Contracts: IF-288, IF-289 — the seams this module declares (process.md §8; rows
of record in docs/requirements/interfaces.toml).

Contract IF-288: the attended launcher's command line, its arguments.
    `review --wi WI-N --base REV --sha REV --scope narrow|full --tests T...
    --scratch DIR --out FILE [--findings ROUND] [--rubric RUBRIC] [--python
    EXE] [--root DIR]` writes one review round's brief to FILE: the shipped
    reviewer template strictly filled with the work item's spec, the range
    BASE..SHA (both resolved to full commits on DIR's branch, BASE an ancestor
    of SHA), the scope, the tests, the scratch area and the verdict path under
    it. A narrow round names the round file ROUND whose findings it answers; a
    full-lane round names none. `critique --wi WI-N --rubric RUBRIC --scratch
    DIR --out FILE [--root DIR]` writes the shipped critique template strictly
    filled with the work item's spec and RUBRIC. `file --review VERDICT --sha
    REV --scope narrow|full [--phase REVIEW-A|REVIEW-B] [--root DIR]` writes
    VERDICT, once it is bound to SHA's full commit (`Reviewed: <sha>` first),
    carries exactly one line whose keyword, in any case, is `VERDICT`, and that
    line is exactly `VERDICT: <APPROVE|CHANGES-REQUESTED> findings=<digits>`
    with a count that matches its finding lines, and names a finding when it
    requests changes, as the lane's next round file
    `docs/reviews/<branch>/NNN-<phase>-<sha7>[-narrow].md`, for a branch whose
    round file `kitlib.verdict.round_file` reads back as that branch's scope
    and whose directory is not the rollup generator's own.
Contract IF-289: the command's exit codes. 0 when the brief is written or the
    review is filed; 2 when the call is refused (an unfilled template slot, a
    missing spec, an unreadable or empty named input, a root not on a branch,
    a revision that is not a commit or a base that is not an ancestor, a branch
    that is not a review scope or names the rollup generator's directory, or a
    review that fails the IF-288 checks). A
    refusal writes no requested brief or review record.

Usage:
    python scripts/review_brief.py review --wi WI-123 --base <sha> --sha <sha> \\
        --scope full --scratch <dir> --tests tests/test_a.py --out <brief.md>
    python scripts/review_brief.py review ... --scope narrow \\
        --findings docs/reviews/<lane>/001-REVIEW-A-<sha7>.md
    python scripts/review_brief.py critique --wi WI-123 \\
        --rubric docs/rubrics/scope-critique.md --scratch <dir> --out <brief.md>
    python scripts/review_brief.py file --review <verdict.md> --sha <sha> --scope full
"""

import argparse
import dataclasses
import re
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import agent_brief  # noqa: E402  (path set above; the script-sibling idiom)
import agent_common  # noqa: E402
import prompts  # noqa: E402
import score_reviews  # noqa: E402
from kitlib import sitting as ksitting  # noqa: E402
from kitlib import verdict as kverdict  # noqa: E402
from kitlib.config import utf8_console  # noqa: E402

SCOPES = ("narrow", "full")
PHASES = ("REVIEW-A", "REVIEW-B")
REVIEWS = "docs/reviews"
_ORDINAL_RE = re.compile(r"^(\d+)-")


class BriefError(Exception):
    """A brief cannot be rendered, or a review cannot be filed, as asked."""


@dataclasses.dataclass(frozen=True)
class Round:
    """One review round's facts, as the launcher states them.

    A narrow round answers a named round file's findings; a full-lane round is
    fresh and answers none. The two are refused in each other's shape, so a
    round that claims to be the fresh full-lane review cannot carry an earlier
    verdict into its brief.

    Implements: SR-146, LLR-313
    """

    wi: str
    lane: str
    base: str
    sha: str
    scope: str
    tests: tuple
    scratch: str
    python: str
    findings: str | None = None
    rubric: str | None = None

    def __post_init__(self):
        if self.scope not in SCOPES:
            raise BriefError(
                "scope {!r} is not one of {}".format(self.scope, ", ".join(SCOPES))
            )
        if self.scope == "narrow" and not self.findings:
            raise BriefError(
                "a narrow round names the round file whose findings it answers"
            )
        if self.scope == "full" and self.findings:
            raise BriefError(
                "a full-lane round is fresh: it answers no earlier findings"
            )
        if not self.tests:
            raise BriefError("a round names the tests the reviewer runs")


def _posix(path):
    return str(path).replace("\\", "/")


def spec_path(root, wi):
    """`wi`'s spec, repo-relative, as this tree holds it — searched across the
    spec homes, the copy chosen by `agent_common.authoritative_spec` (the
    merge slot's own choice) — or a refusal naming the id.

    Implements: SR-146, LLR-313
    """
    found = {}
    for home in agent_common.SPEC_HOMES:
        for hit in (Path(root) / home).rglob(wi + "-*.md"):
            found[hit.relative_to(Path(root)).as_posix()] = hit
    chosen = agent_common.authoritative_spec(found)
    if chosen is None:
        raise BriefError(
            "no spec for {} under {}".format(wi, ", ".join(agent_common.SPEC_HOMES))
        )
    return chosen


def _spec_title(root, rel):
    """The spec's `title`, or a placeholder that reads as unreadable rather
    than as a row with no scope."""
    try:
        text = (Path(root) / rel).read_text(encoding="utf-8")
        head = text.split("+++", 2)[1] if text.startswith("+++") else ""
        return str(tomllib.loads(head).get("title") or "").strip() or "(no title)"
    except (OSError, UnicodeDecodeError, IndexError, tomllib.TOMLDecodeError):
        return "(title unreadable)"


def _named_file(root, rel, what):
    """The text of `rel` when it names a readable, non-empty file under
    `root`, else a refusal: a path the launcher typed is checked once, here."""
    try:
        text = (Path(root) / rel).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise BriefError("the {} {} cannot be read: {}".format(what, rel, exc)) from exc
    if not text.strip():
        raise BriefError("the {} {} is empty".format(what, rel))
    return text


def _scope_lines(rnd):
    """The range and what kind of round it is."""
    span = "`{}..{}`".format(rnd.base, rnd.sha)
    if rnd.scope == "full":
        return [
            "- Range {}: a FULL-LANE review, the whole lane from its trunk base "
            "to its tip. It is the fresh review a landing is judged on.".format(span)
        ]
    return [agent_brief.narrow_scope_line(rnd.base, rnd.sha, rnd.findings)]


def _ps(value):
    """`value` as one PowerShell argument: single-quoted, so nothing in it
    expands, with an embedded quote doubled. Every path a rendered command
    carries goes through here, so a space or a quote never splits one."""
    return "'{}'".format(str(value).replace("'", "''"))


def _run_lines(rnd, scripts):
    """How the reviewer runs things inside the launcher's scratch area."""
    basetemp = "{}/{}".format(rnd.scratch.rstrip("/"), rnd.lane)
    ceiling = _posix(Path(rnd.scratch).parent)
    python = "& " + _ps(rnd.python)
    return [
        "- How to run things. These commands take the place of the "
        "`check.py --jobs 0` run above; do not run the full suite or the smoke "
        "tier. They run on this worktree's checkout, so first confirm that "
        "`git rev-parse HEAD` prints `{}`; if it does not, run nothing and "
        "report that the checkout is not the reviewed commit. In PowerShell, "
        "from this worktree:".format(rnd.sha),
        "      $env:GIT_CEILING_DIRECTORIES = {}".format(_ps(ceiling)),
        "      {} -m pytest -q -p no:cacheprovider -n 2 --basetemp {} {}".format(
            python, _ps(basetemp), " ".join(_ps(t) for t in rnd.tests)
        ),
        "      {} {}".format(python, _ps(scripts + "/check_trajectory.py"))
        + " --strict",
        "  Pass that literal `--basetemp` path, never a temporary-directory "
        "variable. A check that already fails at `{}` fails for a pre-existing "
        "reason: report it only where this range makes it worse.".format(rnd.base),
    ]


def _record_lines(rnd, verdict):
    """Where the verdict goes, who records it, and its shape."""
    return [
        "- The launcher records the verdict. Write it to {} (outside this "
        "repository), commit nothing, and create or change no file in this "
        "worktree. Your one writable area is `{}`.".format(verdict, rnd.scratch),
        "- The verdict file's first line is exactly `Reviewed: {}`. Then a short "
        "Verified paragraph (what you checked and found right) and a Commands "
        "list (each command you ran, with its summary line). Then the finding "
        "lines and the one machine line above. Cite locations as plain "
        "repo-relative `path:line`, never as markdown links.".format(rnd.sha),
    ]


def round_facts(rnd, spec, verdict, scripts):
    """The `{round_facts}` value: what only the launcher of this round knows.

    Implements: SR-146, LLR-313
    """
    lines = [
        "",
        "",
        "ROUND FACTS (stated by the attended launcher that rendered this brief):",
        "- Work item {}, spec `{}`. Read it in full, with its `specref` target "
        "and any owner ruling or adjudicator draft it quotes.".format(rnd.wi, spec),
        "- Lane `{}`, this worktree; the reviewed commit is `{}`.".format(
            rnd.lane, rnd.sha
        ),
    ]
    lines += _scope_lines(rnd)
    if rnd.rubric:
        lines.append(
            "- This repository's review rubric for this round: `{}`. Judge its "
            "anchors too, and cite an anchor id in each finding it "
            "raises.".format(rnd.rubric)
        )
    lines += _run_lines(rnd, scripts)
    lines.append(
        "- The views `docs/stack.ini` `[generated]` declares are generated. A "
        "lane commit may carry them regenerated: that is not a finding, but an "
        "authored change hidden among them is."
    )
    return "\n".join(lines + _record_lines(rnd, verdict))


def render_review(root, rnd):
    """`(brief, verdict path)` for one review round: the kit reviewer template
    filled strictly with the lane's facts. Raises `BriefError` for a missing
    spec or named file, `prompts.PromptError` for a slot left unfilled.

    Implements: SR-146, LLR-313
    """
    spec = spec_path(root, rnd.wi)
    for rel, what in ((rnd.findings, "findings file"), (rnd.rubric, "rubric")):
        if rel:
            _named_file(root, rel, what)
    verdict = "{}/{}-{}-{}-review.md".format(
        rnd.scratch.rstrip("/"), rnd.lane, rnd.sha[:7], rnd.scope
    )
    scripts = agent_brief.scripts_dir(root)
    values = {
        "verdict": verdict,
        "trunk": rnd.base,
        "head": rnd.sha,
        "process_doc": agent_brief.process_doc_path(root),
        "scripts": scripts,
        "wis": "  - {} — {}".format(rnd.wi, _spec_title(root, spec)),
        "round_facts": round_facts(rnd, spec, verdict, scripts),
    }
    return prompts.fill(
        prompts.REVIEWER, prompts.load(prompts.REVIEWER), values
    ), verdict


def render_critique(root, wi, rubric, verdict):
    """The scope critique's brief: the kit critique template over `wi`'s spec,
    with the rubric at `rubric` as its rubric input. Raises `BriefError` for a
    missing spec or rubric, `prompts.PromptError` for a slot left unfilled.

    Implements: SR-146, LLR-313
    """
    spec = spec_path(root, wi)
    rubric_text = _named_file(root, rubric, "rubric").strip()
    brief = "\n".join(
        [
            "### Artifact: the work item spec `{}` ({} — {})".format(
                spec, wi, _spec_title(root, spec)
            ),
            "Artifact recipe: read `{}` in full, and its `specref` target where "
            "it names one. The artifact is the row's scope as written: judge the "
            "scope, never code. This is attended use: write the verdict to the "
            "assigned path, commit nothing, and the launcher records "
            "it.".format(spec),
            "",
            "### Rubric: {}".format(rubric),
            rubric_text,
        ]
    )
    text = prompts.load(prompts.CRITIQUE)
    return prompts.fill(prompts.CRITIQUE, text, {"brief": brief, "verdict": verdict})


def review_refusal(text, sha):
    """Why `text` is not a review of `sha` in the kit's verdict format, or None.

    Implements: SR-235, LLR-313
    """
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines or lines[0].strip() != "Reviewed: " + sha:
        return "its first line is not `Reviewed: {}`".format(sha)
    # The one reader of a review's VERDICT line, which the merge gate's round
    # reader uses too (WI-870): what it refuses is never filed.
    machine, why = ksitting.review_line(text)
    if why:
        return why
    label, count = machine
    found = len(score_reviews.parse_verdict(text).findings)
    if count != found:
        return "its VERDICT line says findings={} but it carries {}".format(
            count, found
        )
    if label == "CHANGES-REQUESTED" and not found:
        return "it requests changes but names no finding"
    return None


def round_path(root, lane, phase, sha, scope):
    """The next round file for `lane`: one ordinal above every numbered file
    already in its review directory.

    Implements: SR-235, LLR-313
    """
    home = Path(root) / REVIEWS / lane
    taken = [
        int(m.group(1))
        for p in (home.iterdir() if home.is_dir() else ())
        if (m := _ORDINAL_RE.match(p.name))
    ]
    suffix = "-narrow" if scope == "narrow" else ""
    name = "{:03d}-{}-{}{}.md".format(max(taken, default=0) + 1, phase, sha[:7], suffix)
    return home / name


def file_review(root, lane, text, sha, scope, phase="REVIEW-A"):
    """Write a validated review as `lane`'s next round file; return its path.
    A refused review writes nothing.

    Implements: SR-235, LLR-313
    """
    if phase not in PHASES or scope not in SCOPES:
        raise BriefError(
            "phase {!r} / scope {!r} is not a review round".format(phase, scope)
        )
    why = review_refusal(text, sha)
    if why:
        raise BriefError("the review is not filed: " + why)
    path = round_path(root, lane, phase, sha, scope)
    # The round reader's own grammar decides whether `lane` names a review
    # scope: a name it would not read back as this lane's round is refused.
    rel = path.relative_to(Path(root)).as_posix()
    parsed = kverdict.round_file(rel)
    if parsed is None or parsed[0] != lane:
        raise BriefError(
            "the review is not filed: branch {!r} is not a review scope the "
            "round reader reads (docs/reviews/<scope>/ is one directory "
            "level)".format(lane)
        )
    # The rollup generator owns its directory and prunes what it did not write.
    # Compared casefolded on every platform: a directory that collides with it
    # on any supported filesystem (Windows and macOS fold case) is the
    # generator's, wherever the commit is later checked out.
    home = path.parent.relative_to(Path(root)).as_posix()
    if home.casefold() == kverdict.ROLLUP_DIR.casefold():
        raise BriefError(
            "the review is not filed: branch {!r} names the rollup generator's "
            "own directory {}".format(lane, kverdict.ROLLUP_DIR)
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as fh:
        fh.write(text.replace("\r\n", "\n"))
    return path


def lane_commits(root, base, sha):
    """`(lane, base, sha)` with both revisions resolved to full commit ids:
    the lane is the worktree's branch, and `base` must be an ancestor of `sha`.

    Implements: SR-146, SR-235, LLR-313
    """
    _c, lane = agent_common.git(root, "branch", "--show-current")
    if not lane.strip():
        raise BriefError(
            "{} is not on a branch: run from the lane's worktree".format(root)
        )
    full = []
    for rev in (base, sha):
        code, out = agent_common.git(root, "rev-parse", "--verify", rev + "^{commit}")
        if code != 0:
            raise BriefError("{!r} is not a commit in {}".format(rev, root))
        full.append(out.strip())
    code, _o = agent_common.git(root, "merge-base", "--is-ancestor", full[0], full[1])
    if code != 0:
        raise BriefError("{} is not an ancestor of {}".format(full[0], full[1]))
    return lane.strip(), full[0], full[1]


def _write(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text + "\n")


def _cmd_review(args):
    lane, base, sha = lane_commits(args.root, args.base, args.sha)
    rnd = Round(
        wi=args.wi,
        lane=lane,
        base=base,
        sha=sha,
        scope=args.scope,
        tests=tuple(args.tests),
        scratch=_posix(args.scratch),
        python=_posix(args.python),
        findings=args.findings,
        rubric=args.rubric,
    )
    text, verdict = render_review(args.root, rnd)
    _write(args.out, text)
    print("review_brief: wrote {}; the reviewer writes {}".format(args.out, verdict))
    print(
        "review_brief: file it with `review_brief.py file --review {} --sha {} "
        "--scope {}`".format(verdict, sha, args.scope)
    )
    return 0


def _cmd_critique(args):
    verdict = "{}/{}-scope-critique.md".format(
        _posix(args.scratch).rstrip("/"), args.wi
    )
    _write(args.out, render_critique(args.root, args.wi, args.rubric, verdict))
    print("review_brief: wrote {}; the critic writes {}".format(args.out, verdict))
    return 0


def _cmd_file(args):
    lane, _base, sha = lane_commits(args.root, args.sha, args.sha)
    try:
        text = Path(args.review).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise BriefError("cannot read {}: {}".format(args.review, exc)) from exc
    path = file_review(args.root, lane, text, sha, args.scope, args.phase)
    print("review_brief: filed {}".format(_posix(path)))
    return 0


def _parser():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    rev = sub.add_parser("review", help="render one review round's brief")
    rev.add_argument("--wi", required=True, help="the work item under review")
    rev.add_argument("--base", required=True, help="the range's base commit")
    rev.add_argument("--sha", required=True, help="the reviewed commit (the lane tip)")
    rev.add_argument("--scope", required=True, choices=SCOPES)
    rev.add_argument(
        "--tests", required=True, nargs="+", help="tests the reviewer runs"
    )
    rev.add_argument("--scratch", required=True, help="the reviewer's writable area")
    rev.add_argument("--findings", help="narrow: the round file this range answers")
    rev.add_argument("--rubric", help="a repository review rubric to judge too")
    rev.add_argument("--python", default=sys.executable, help="the interpreter to run")
    rev.add_argument("--out", required=True, help="where to write the brief")
    crit = sub.add_parser("critique", help="render a work item's scope critique")
    crit.add_argument("--wi", required=True, help="the work item whose scope is judged")
    crit.add_argument("--rubric", required=True, help="the scope rubric, repo-relative")
    crit.add_argument("--scratch", required=True, help="the critic's writable area")
    crit.add_argument("--out", required=True, help="where to write the brief")
    fil = sub.add_parser("file", help="file a review as the lane's next round file")
    fil.add_argument("--review", required=True, help="the reviewer's verdict file")
    fil.add_argument("--sha", required=True, help="the reviewed commit")
    fil.add_argument("--scope", required=True, choices=SCOPES)
    fil.add_argument("--phase", default="REVIEW-A", choices=PHASES)
    for each in (rev, crit, fil):
        each.add_argument(
            "--root", default=".", help="the lane worktree (default: cwd)"
        )
    return ap


def main(argv=None):
    utf8_console()
    args = _parser().parse_args(argv)
    run = {"review": _cmd_review, "critique": _cmd_critique, "file": _cmd_file}
    try:
        return run[args.cmd](args)
    except (BriefError, prompts.PromptError) as exc:
        print("review_brief: REFUSED — {}".format(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
