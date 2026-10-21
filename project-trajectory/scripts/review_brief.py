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
    --scratch DIR --out FILE [--findings ROUND] [--rubric RUBRIC] [--stance
    ordinary|convergence] [--python EXE] [--root DIR]` writes one review
    round's brief to FILE: the shipped reviewer template strictly filled with
    the work item's spec, the range BASE..SHA (both resolved to full commits
    on DIR's branch, BASE an ancestor of SHA), the scope, the tests, the
    scratch area and the verdict path under it. A narrow round names the round
    file ROUND whose findings it answers; a full-lane round names none. The
    stance is `ordinary` by default, which adds nothing; `convergence` adds
    one fixed ROUND FACTS line after the range line, and its reading-scope
    command also leaves out `docs/decisions` and `docs/plans/*/critique-*`
    (WI-911). The brief is written only when SHA, or a commit beneath it
    that only record-only commits separate from it, carries a verified
    `bar=review` attestation whose tests digest is that of the tests; the
    command then prints the attested commit and that digest. `critique --wi
    WI-N --rubric RUBRIC --scratch DIR --out FILE [--root DIR]` writes the
    shipped critique template strictly filled with the work item's spec,
    RUBRIC and the registries the critic reads beside the spec, each named by
    its repo path and marked "(absent here)" when DIR lacks it: the component
    and interface registries, the derived architecture, the runtime flows and
    the dependency ledger. `file --review VERDICT --sha
    REV --scope narrow|full [--phase REVIEW-A|REVIEW-B] [--root DIR]` writes
    VERDICT, once it is bound to SHA's full commit (`Reviewed: <sha>` first),
    carries exactly one line whose keyword, in any case, is `VERDICT`, and that
    line is exactly `VERDICT: <APPROVE|CHANGES-REQUESTED> findings=<digits>`
    with a count that matches its finding lines, and names a finding when it
    requests changes, as the lane's next round file
    `docs/reviews/<branch>/NNN-<phase>-<sha7>[-narrow].md`, for a branch whose
    round file `kitlib.verdict.round_file` reads back as that branch's scope.
    THE SINGLE PLAN (WI-913):
    `plan --wi WI-N --scratch DIR --out FILE [--revise] [--root
    DIR]` writes the shipped single-plan template strictly filled with the
    work item's spec, its Done-when as `D1..Dn` clauses, the inputs the plan
    cites and the planner's one output path under DIR; `--revise` adds the
    committed plan and the latest filed critique's findings. `critique
    --plan --sha REV ...` writes the critique template over the plan at the
    commit REV, its spec and the coverage report the coverage gate writes
    under DIR over the Done-when (the second round also over the first
    critique's finding ids, which the revised plan must answer), its verdict
    opening `Reviewed: <REV>`, the second round in convergence stance.
    `plan-file --wi WI-N --dispute-findings PATH --positions FILE [--root
    DIR]` writes, at the cap, the dispute findings file PATH from HEAD's
    filed second critique: each BLOCKER and MAJOR finding under the `F#` the
    gate reads it by, its text verbatim, and the position FILE declares for
    it on an `F#: <position>` line, FILE naming exactly those ids.
    `plan-file --wi WI-N --critique VERDICT --sha REV [--root DIR]` files VERDICT, once it passes
    the `file` checks against REV (an ancestor of HEAD whose tree holds a
    plan whose `DELTA:` is `none` or `within`), as the next
    `docs/plans/<WI>/critique-<n>.md`, at most two; `plan-file --wi WI-N
    --pass [--dispute VERDICT]` writes `docs/plans/<WI>/pass.toml`
    (`kitlib.plan_pass`'s grammar) when HEAD holds the latest critique and
    any dispute verdict as filed and every check of `plan_gate.record_problems`
    and the coverage gate passes.
Contract IF-289: the command's exit codes. 0 when the brief is written or the
    review, critique, dispute findings file or pass record is filed; 2 when the call is refused (an
    unfilled template slot, a missing spec, plan, critique or Done-when, an
    unreadable or empty named input, a root not on a branch, a revision that
    is not a commit or a base that is not an ancestor, a branch that is not a
    review scope, a reviewed commit with no such attestation (the refusal
    names the commit, the cause and the attest command), a review that fails
    the IF-288 checks, a review round whose
    stance is not one of `ordinary` or `convergence`, a narrow round in the
    convergence stance, a
    convergence round over a reviewer template whose reading-scope command it
    cannot narrow, or a plan step the IF-288 plan rules refuse). A refusal writes no
    requested brief or review record.

Usage:
    python scripts/review_brief.py review --wi WI-123 --base <sha> --sha <sha> \\
        --scope full --scratch <dir> --tests tests/test_a.py --out <brief.md>
    python scripts/review_brief.py review ... --scope narrow \\
        --findings docs/reviews/<lane>/001-REVIEW-A-<sha7>.md
    python scripts/review_brief.py review ... --scope full --stance convergence
    python scripts/review_brief.py critique --wi WI-123 \\
        --rubric docs/rubrics/scope-critique.md --scratch <dir> --out <brief.md>
    python scripts/review_brief.py file --review <verdict.md> --sha <sha> --scope full
    python scripts/review_brief.py plan --wi WI-123 --scratch <dir> --out <brief.md>
    python scripts/review_brief.py critique --plan --wi WI-123 --sha <sha> \\
        --rubric docs/rubrics/plan-decomposition.md --scratch <dir> --out <brief.md>
    python scripts/review_brief.py plan-file --wi WI-123 --critique <v.md> --sha <sha>
    python scripts/review_brief.py plan-file --wi WI-123 \\
        --dispute-findings docs/reviews/<lane>/NNN-DISPUTE-findings.toml --positions <f>
    python scripts/review_brief.py plan-file --wi WI-123 --pass [--dispute <verdict>]
"""

import argparse
import dataclasses
import re
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import agent_brief  # noqa: E402  (path set above; the script-sibling idiom)
import agent_common  # noqa: E402
import plan_coverage  # noqa: E402
import plan_gate  # noqa: E402
import prompts  # noqa: E402
import score_reviews  # noqa: E402
from kitlib import dispute as kdispute  # noqa: E402
from kitlib import done_when as kdone  # noqa: E402
from kitlib import plan_pass  # noqa: E402
from kitlib.spine import toml_string  # noqa: E402
from kitlib import verdict as kverdict  # noqa: E402
from kitlib.config import utf8_console  # noqa: E402

SCOPES = ("narrow", "full")
# A review round's stance (WI-911; review-churn plan revision 8, and ruling 4's
# convergence round): `ordinary`, the default, renders today's brief, and
# `convergence` adds `_CONVERGENCE_ROUND`, one fixed ROUND FACTS line that
# marks the round and points at the reviewer template's convergence stance,
# restating none of it.
STANCES = ("ordinary", "convergence")
_CONVERGENCE_ROUND = "- STANCE: CONVERGENCE. This round runs in the convergence stance: apply the brief's convergence-stance paragraph as written."  # noqa: E501
# A convergence brief's reading scope (WI-911; revision 8: a convergence
# round never sees earlier verdicts). Only the convergence
# render leaves the decisions record and the plan's filed critiques out of the
# brief's one reading-scope command, beside the round files the template
# already leaves out; an ordinary or loop reviewer keeps reading them.
_RECORDS_EXCLUDE = "':(exclude)docs/reviews'"
_CONVERGENCE_EXCLUDES = (
    "':(exclude)docs/reviews' ':(exclude)docs/decisions' "
    "':(exclude)docs/plans/*/critique-*'"
)
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
    stance: str = "ordinary"

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
        if self.stance not in STANCES:
            raise BriefError(
                "stance {!r} is not one of {}".format(self.stance, ", ".join(STANCES))
            )
        if self.stance == "convergence" and self.scope == "narrow":
            raise BriefError(
                "a narrow round is never in the convergence stance: a "
                "convergence round reviews the full lane"
            )


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
    if rnd.stance == "convergence":
        lines.append(_CONVERGENCE_ROUND)
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
    filled strictly with the lane's facts. A convergence round's reading-scope
    command also leaves out the decisions record and the plan's filed
    critiques. Raises `BriefError` for a missing spec or named file, or a
    template whose command a convergence round cannot narrow, and
    `prompts.PromptError` for a slot left unfilled.

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
    text = prompts.load(prompts.REVIEWER)
    if rnd.stance == "convergence":
        if text.count(_RECORDS_EXCLUDE) != 1:
            raise BriefError(
                "the reviewer template's reading-scope command does not carry "
                "{} exactly once: a convergence brief cannot leave the earlier "
                "findings' records out of it".format(_RECORDS_EXCLUDE)
            )
        text = text.replace(_RECORDS_EXCLUDE, _CONVERGENCE_EXCLUDES)
    return prompts.fill(prompts.REVIEWER, text, values), verdict


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
            "Read beside it the registries the rubric's anchors are judged "
            "against. Each is a registry, never code:",
        ]
        + _registry_lines(root, _CRITIQUE_INPUTS)
        + [
            "",
            "### Rubric: {}".format(rubric),
            rubric_text,
        ]
    )
    text = prompts.load(prompts.CRITIQUE)
    return prompts.fill(prompts.CRITIQUE, text, {"brief": brief, "verdict": verdict})


def review_refusal(text, sha):
    """Why `text` is not a review of `sha` in the kit's verdict format, or None.

    The rule is `kitlib.verdict.filing_refusal`, which the merge gate's round
    reader applies too (WI-884): a committed round it refuses is invalid
    evidence there, so what is never filed here never clears the gate either.
    This boundary binds the scorer's parser, which reads the VERDICT line
    through the shared review-line reader (WI-870).

    Implements: SR-235, LLR-313
    """
    return kverdict.filing_refusal(text, sha, score_reviews.parse_verdict)


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
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as fh:
        fh.write(text.replace("\r\n", "\n"))
    return path


# --- the single plan (WI-913): the planner's brief, the plan critique, the
# filing step and its pass record ---------------------------------------------

# The registries a brief names for its reader, each by a label and its repo
# path. `_registry_lines` is their one renderer: a path the repository lacks
# is named as absent, never dropped.
_REGISTRIES = {
    "srs": ("its SR rows", "docs/requirements/system-requirements.toml"),
    "tcs": ("the TCs that verify them", "docs/test/test-cases.toml"),
    "interfaces": ("the interface registry", "docs/requirements/interfaces.toml"),
    "components": ("the component registry", "docs/requirements/components.toml"),
    "flows": ("the runtime flows", "docs/runtime-flows.md"),
    "derived": (
        "the derived architecture",
        "docs/requirements/components.derived.toml",
    ),
    "dependencies": ("the dependency ledger", "docs/dependencies.md"),
}
# What the planner must cite, by the registry that holds it.
_PLAN_INPUTS = ("srs", "tcs", "interfaces", "components", "flows")
# What the scope critic reads beside the spec for the coverage, delta and
# dependency anchors (WI-911; review-churn plan item 12, revision 20).
_CRITIQUE_INPUTS = ("components", "interfaces", "derived", "flows", "dependencies")
# The second critique's stance (owner, 2026-10-14): it judges the revised plan
# as it stands and never sees the first critique.
_CONVERGENCE = (
    "- This is the SECOND and last critique of this plan, after its one "
    "revision, in the convergence stance: judge the plan as it stands. A new "
    "finding is BLOCKER or MAJOR only if it is fail-open, data loss or a "
    "Done-when gap, and a supported workflow or the kit's own routes reach it; "
    "anything else is MINOR."
)


def _spec_text(root, rel):
    """The spec's text and its `sr_refs`, or a refusal."""
    text = _named_file(root, rel, "spec")
    try:
        head = text.split("+++", 2)[1] if text.startswith("+++") else ""
        return text, list(tomllib.loads(head).get("sr_refs") or [])
    except (IndexError, tomllib.TOMLDecodeError) as exc:
        raise BriefError("the spec {} has no readable frontmatter: {}".format(rel, exc))


def _clause_lines(text, rel):
    """The Done-when items as the `D1…Dn` clauses the coverage gate reads."""
    found = kdone.items(text)
    if not found:
        raise BriefError("the spec {} declares no Done-when items".format(rel))
    return "\n".join("- D{}: {}".format(n, item) for n, item in enumerate(found, 1))


def _registry_lines(root, names):
    """One brief line per registry in `names`, in that order: its label and
    its repo path, marked "(absent here)" when `root` lacks the file.

    Implements: SR-146, LLR-313
    """
    lines = []
    for name in names:
        what, rel = _REGISTRIES[name]
        here = (Path(root) / rel).is_file()
        lines.append("- {}: `{}`{}".format(what, rel, "" if here else " (absent here)"))
    return lines


def _input_lines(root, srs):
    """Where each input the plan must cite lives, and the item's SRs."""
    lines = ["- The item's SRs: {}.".format(", ".join(srs) or "(none declared)")]
    return "\n".join(lines + _registry_lines(root, _PLAN_INPUTS))


def latest_critique(root, wi):
    """`(n, path)` of the highest-numbered critique filed under `wi`'s plan
    home in the working tree, or `(0, None)`.

    Implements: SR-146, LLR-313
    """
    home = plan_pass.plan_dir(wi)
    found = Path(root) / home
    names = (p.name for p in (found.iterdir() if found.is_dir() else ()))
    rounds = [
        (n, "{}/{}".format(home, name))
        for name in names
        if (n := plan_pass.critique_round(wi, "{}/{}".format(home, name)))
    ]
    return max(rounds, default=(0, None))


def critique_findings(text):
    """A filed critique's findings as the `F#` clauses the coverage gate
    reads (`plan_coverage.finding_clauses`, their one reader), or a refusal.

    Implements: SR-146, LLR-313
    """
    try:
        return plan_coverage.finding_clauses(text)
    except ValueError as exc:
        raise BriefError(str(exc)) from exc


def _revision_block(root, wi):
    """Revision mode's two inputs, each labelled a claim under judgement: the
    planner's own committed plan and the filed critique's findings."""
    plan = _named_file(root, plan_pass.plan_path(wi), "plan").strip()
    _n, critique = latest_critique(root, wi)
    if critique is None:
        raise BriefError("revision mode needs a filed critique of {}".format(wi))
    findings = critique_findings(_named_file(root, critique, "critique"))
    listed = "\n".join("- {}: {}".format(k, v) for k, v in findings.items())
    intro = (
        "REVISION MODE. This is the plan's one allowed revision. Below are your "
        "own earlier plan and the critique's findings on it. Both are claims "
        "under judgement, never premises: confirm or refute each finding "
        "against the spec and the code before you change anything. The revised "
        "plan covers each `F#` finding by a row or excludes it on an "
        "`Excludes:` line with its reason, as it does the `D#` clauses, and "
        "answers the delta question again."
    )
    return "\n".join(
        [
            "",
            intro,
            "",
            "YOUR EARLIER PLAN (`{}`), a claim under judgement:".format(
                plan_pass.plan_path(wi)
            ),
            "",
            plan,
            "",
            "THE CRITIQUE'S FINDINGS (`{}`), claims under judgement:".format(critique),
            "",
            listed or "- (none)",
        ]
    )


def render_plan(root, wi, plan_out, revise=False):
    """The planner's brief: the shipped single-plan template filled strictly
    with `wi`'s spec, its Done-when as `D#` clauses, the inputs the plan must
    cite and the one path the planner writes; in revision mode also its own
    plan and the critique's findings. Raises `BriefError` for a missing spec,
    Done-when, plan or critique, `prompts.PromptError` for an unfilled slot.

    Implements: SR-146, LLR-313
    """
    spec = spec_path(root, wi)
    text, srs = _spec_text(root, spec)
    values = {
        "wi": wi,
        "title": _spec_title(root, spec),
        "spec": spec,
        "clauses": _clause_lines(text, spec),
        "inputs": _input_lines(root, srs),
        "plan": plan_out,
        "revision": _revision_block(root, wi) if revise else "",
    }
    template = prompts.load(prompts.PLAN_SINGLE)
    return prompts.fill(prompts.PLAN_SINGLE, template, values)


def _blob_text(root, rev, rel, what):
    """`rel`'s text at the commit `rev`, or a refusal naming `what`."""
    data, why = plan_pass.blob(root, rev, rel)
    if data is None:
        tail = ": " + why if why else ""
        raise BriefError("the {} {} is not at {}{}".format(what, rel, rev[:10], tail))
    return data.decode("utf-8", "replace")


def coverage_run(root, rev, wi, branch, findings=None, out=None):
    """`(exit code, report lines)` of the coverage gate over `wi`'s spec and
    plan as the commit `rev` holds them, with a filed critique at `rev` as
    its `--findings` clauses when one is named: the gate runs on committed
    bytes, never on a working-tree copy.

    Implements: SR-146, LLR-313
    """
    _path, spec, why = kdone.spec_at(root, rev, branch, wi)
    if spec is None:
        raise BriefError(
            "no spec of {} at {}: {}".format(wi, rev[:10], why or "absent")
        )
    files = {
        "spec.md": spec,
        "plan.md": _blob_text(root, rev, plan_pass.plan_path(wi), "plan"),
    }
    if findings:
        files["findings.md"] = _blob_text(root, rev, findings, "critique")
    script = Path(__file__).resolve().parent / "plan_coverage.py"
    with tempfile.TemporaryDirectory() as tmp:
        for name, text in files.items():
            Path(tmp, name).write_text(text, encoding="utf-8", newline="\n")
        argv = [sys.executable, str(script), "--item", str(Path(tmp, "spec.md"))]
        argv += [str(Path(tmp, "plan.md")), "--root", str(root)]
        argv += ["--findings", str(Path(tmp, "findings.md"))] if findings else []
        argv += ["--out", str(out)] if out else []
        done = subprocess.run(
            argv, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
    said = done.stdout.splitlines() + done.stderr.splitlines()
    return done.returncode, [ln for ln in said if ln.startswith("plan_coverage: ")]


def _critique_round_to_open(root, wi):
    """The next critique round of `wi`, refused past the cap."""
    n = latest_critique(root, wi)[0] + 1
    if n > plan_pass.MAX_CRITIQUES:
        raise BriefError(
            "{} already has its {} critiques: the cap goes to a dispute sitting "
            "or the owner".format(wi, plan_pass.MAX_CRITIQUES)
        )
    return n


def _critiqued_plan(root, sha, wi):
    """The plan at `sha`, refused when absent or when its delta line is
    missing or `beyond`: such a plan is never critiqued and never passes."""
    plan = _blob_text(root, sha, plan_pass.plan_path(wi), "plan")
    value, why = plan_pass.delta(plan)
    if value not in plan_pass.PASSING_DELTAS:
        raise BriefError(
            "the plan is not critiqued: {}".format(
                why or "its delta is `beyond`: the lane closes partial"
            )
        )
    return plan


def _critique_coverage(root, sha, wi, n, report):
    """Run the coverage gate for critique round `n` over the plan at `sha`,
    writing its report to `report`, or refuse: over the Done-when, and in the
    revision round also against the first critique's findings (`plan_coverage
    --findings`, deliverable 3), so a revision that answers none of them is
    refused before the critic's one run is spent. The report carries clause
    ids, never a finding's text, so the second critic still never meets the
    first verdict.

    Implements: SR-146, LLR-313
    """
    branch = agent_common.git(root, "branch", "--show-current")[1].strip()
    first = _answered(root, sha, wi, n)
    code, said = coverage_run(root, sha, wi, branch, findings=first, out=report)
    if code != 0:
        against = " against the first critique's findings ({})".format(first)
        raise BriefError(
            "the plan fails the coverage gate{}:\n{}".format(
                against if first else "", "\n".join(said)
            )
        )


def render_plan_critique(root, wi, rubric, sha, scratch):
    """`(brief, verdict path)` for the plan critique: the shipped critique
    template over the plan at the lane commit `sha`, read with its spec and
    the coverage report `plan_coverage.py --item --out` writes over the
    Done-when (in round two also over the first critique's finding ids, never
    their text: `_critique_coverage`), judged on `rubric`.
    The verdict opens `Reviewed: <sha>` and goes to its own path per round.
    Refuses a missing spec, plan or rubric, a plan whose delta is missing or
    `beyond`, a round past the cap, and a plan the coverage gate fails.

    Implements: SR-146, LLR-313
    """
    spec = spec_path(root, wi)
    rubric_text = _named_file(root, rubric, "rubric").strip()
    _critiqued_plan(root, sha, wi)
    n = _critique_round_to_open(root, wi)
    base = _posix(scratch).rstrip("/")
    report = Path("{}/{}-plan-coverage-{}.md".format(base, wi, n))
    report.parent.mkdir(parents=True, exist_ok=True)
    _critique_coverage(root, sha, wi, n, report)
    verdict = "{}/{}-plan-critique-{}.md".format(base, wi, n)
    lines = [
        "### Artifact: the implementation plan `{}` of {} — {}, at the lane "
        "commit `{}`".format(plan_pass.plan_path(wi), wi, _spec_title(root, spec), sha),
        "Artifact recipe: read the plan as that commit holds it (`git show "
        "{}:{}`), its work item's spec `{}` in full with its `specref` target, "
        "and the coverage report below, which the coverage gate computed over "
        "the Done-when (in a revision round, also over the first critique's "
        "finding ids, never their text). Judge whether the plan's rows are solvable, cover "
        "the Done-when honestly and in buildable order, and whether its `DELTA:` "
        "answer is right: does the work item add a state, add a value to a "
        "domain, make an output depend on a new input, or cross a new boundary, "
        "and if so does the plan carry the change? Read no `critique-*.md` "
        "beside the plan: another critic's verdict is not your "
        "input.".format(sha, plan_pass.plan_path(wi), spec),
        "- The verdict file's first line is exactly `Reviewed: {}`.".format(sha),
    ]
    lines += [_CONVERGENCE] if n == plan_pass.MAX_CRITIQUES else []
    lines += ["", "### Coverage report", report.read_text(encoding="utf-8").strip()]
    lines += ["", "### Rubric: {}".format(rubric), rubric_text]
    values = {"brief": "\n".join(lines), "verdict": verdict}
    text = prompts.load(prompts.CRITIQUE)
    return prompts.fill(prompts.CRITIQUE, text, values), verdict


def file_plan_critique(root, wi, text, sha):
    """File a plan critique as the next `docs/plans/<WI>/critique-<n>.md`;
    return its path. Refused, writing nothing: a verdict not bound to `sha`
    (`Reviewed: <sha>` first) or outside the verdict format, a reviewed
    commit whose tree holds no plan or one whose delta is missing or
    `beyond`, a round past the cap, and a row already passed.

    Implements: SR-146, SR-235, LLR-313
    """
    why = review_refusal(text, sha)
    if why:
        raise BriefError("the critique is not filed: " + why)
    _critiqued_plan(root, sha, wi)
    if (Path(root) / plan_pass.record_path(wi)).exists():
        raise BriefError("{} already has a pass record".format(wi))
    path = Path(root) / plan_pass.critique_path(wi, _critique_round_to_open(root, wi))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as fh:
        fh.write(text.replace("\r\n", "\n"))
    return path


def _committed(root, head, rel, what):
    """HEAD's bytes of `rel` when the working tree holds no change to it, as
    git compares them (its line-ending conversion included), else a refusal:
    the pass form cites only what HEAD holds."""
    data, why = plan_pass.blob(root, head, rel)
    changed = agent_common.git(root, "diff", "--quiet", head, "--", rel)[0]
    if data is None or changed != 0:
        tail = " ({})".format(why) if why else ""
        raise BriefError(
            "HEAD does not hold the {} {} as filed: commit it alone first{}".format(
                what, rel, tail
            )
        )
    return data


def _lane_claim(root, wi):
    """`(HEAD, branch, claim text)` for the lane, or a refusal."""
    head = agent_common.git(root, "rev-parse", "HEAD")[1].strip()
    branch = agent_common.git(root, "branch", "--show-current")[1].strip()
    try:
        base = agent_common.default_base(root)
    except agent_common.TrunkUndeclared as exc:
        raise BriefError(str(exc)) from exc
    claimed, why = kdone.claim_copy(root, base, branch, wi)
    if claimed is None:
        raise BriefError(
            "{} has no readable claim copy on {}: {}".format(
                wi, branch, why or "absent"
            )
        )
    return head, branch, claimed


def _answered(root, head, wi, n):
    """The first critique, when the revision critique `n` judges must answer
    its findings (`plan_coverage.py --findings`), else None: a first plan
    answers none, and a first critique naming no finding leaves nothing to
    answer."""
    if n < 2:
        return None
    first = plan_pass.critique_path(wi, 1)
    text = _blob_text(root, head, first, "critique")
    return first if score_reviews.parse_verdict(text).findings else None


def pass_fields(root, wi, dispute=None):
    """The pass record's fields HEAD supports, or a refusal: the latest filed
    critique and any dispute verdict must be in HEAD as filed, every reason
    `plan_gate.record_problems` gives refuses, and the coverage gate must
    pass on HEAD's plan (the revision also covering the first critique's
    findings).

    Implements: SR-146, LLR-313
    """
    n, critique = latest_critique(root, wi)
    if critique is None:
        raise BriefError("no critique of {} is filed".format(wi))
    head, branch, claimed = _lane_claim(root, wi)
    data = _committed(root, head, critique, "critique")
    first = data.decode("utf-8", "replace").split("\n", 1)[0].removesuffix("\r")
    plan, delta, _why = plan_pass.plan_digest(root, head, wi)
    done, _why = plan_pass.done_when_digest(root, head, branch, wi, claimed)
    fields = dict.fromkeys(plan_pass.FIELDS, "")
    fields.update(wi=wi, plan=plan or "", done_when=done or "", delta=delta or "")
    fields.update(critique=critique, critique_digest=plan_pass.bytes_digest(data))
    fields.update(reviewed=first.removeprefix("Reviewed: ").strip())
    if dispute:
        cited = _committed(root, head, dispute, "dispute verdict")
        fields.update(dispute=dispute, dispute_digest=plan_pass.bytes_digest(cited))
    problems = plan_gate.record_problems(root, head, fields, branch, wi, claimed)
    problems += _ruled_findings(root, head, fields, data) if dispute else []
    first_round = _answered(root, head, wi, n)
    code, said = coverage_run(root, head, wi, branch, findings=first_round)
    if code != 0:
        problems.append("the plan fails the coverage gate: " + "; ".join(said))
    if problems:
        raise BriefError("no pass record is written: " + "; ".join(problems))
    return fields


def _ruled_findings(root, head, fields, critique):
    """Why the dispute verdict's rulings are not shown to be this critique's
    BLOCKER and MAJOR findings: each `F#` (the coverage gate's numbering) must
    be the finding the findings file beside the verdict records under that
    id (`plan_coverage.ruling_problem`, read at HEAD), or [].

    Implements: SR-146, LLR-313
    """
    text = critique.decode("utf-8", "replace")
    clauses = critique_findings(text)
    out = []
    for fid in plan_gate.blocking_ids(score_reviews.parse_verdict(text).findings):
        cite = plan_coverage.RULING_CITE_RE.search(
            "{}#{}".format(fields["dispute"], fid)
        )
        why = "{} is not a dispute verdict path".format(fields["dispute"])
        why = (
            plan_coverage.ruling_problem(root, cite, fid, clauses[fid], head)
            if cite
            else why
        )
        if why:
            out.append("{}: {}".format(fid, why))
    return out


def dispute_findings(root, wi, positions):
    """The dispute findings file's text for the cap (`kitlib.dispute`'s
    shape), or a refusal: ONE OWNER of a finding's number. Each of the filed
    second critique's BLOCKER and MAJOR findings is written under the `F#`
    the gate and the filing step read it by (`plan_gate.blocking_ids`: its
    position among ALL the critique's findings, so a MAJOR after a MINOR is
    F2), with its text exactly as `critique_findings` gives it. `positions`
    declares one `F#: <position>` line per blocking finding (the coverage
    gate's declared-clause shape) and nothing else; the range is the lane's
    claim base to HEAD. The text reads back through `kitlib.dispute` before
    it is returned.

    Implements: SR-146, LLR-313
    """
    n, critique = latest_critique(root, wi)
    if n != plan_pass.MAX_CRITIQUES:
        raise BriefError("a dispute sitting follows only the second critique")
    head = agent_common.git(root, "rev-parse", "HEAD")[1].strip()
    text = _committed(root, head, critique, "critique").decode("utf-8", "replace")
    clauses = critique_findings(text)
    ids = plan_gate.blocking_ids(score_reviews.parse_verdict(text).findings)
    try:
        held = plan_coverage.parse_goal(positions, plan_coverage.FINDING_DECL_RE)
    except ValueError as exc:
        raise BriefError(str(exc)) from exc
    if not ids or list(held) != ids:
        raise BriefError(
            "the positions name {}; the second critique's BLOCKER and MAJOR "
            "findings are {}".format(
                ", ".join(held) or "none", ", ".join(ids) or "none"
            )
        )
    try:
        base = agent_common.default_base(root)
    except agent_common.TrunkUndeclared as exc:
        raise BriefError(str(exc)) from exc
    if not base:
        raise BriefError("the lane's claim base cannot be read")
    lines = ["range = {}".format(toml_string("{}..{}".format(base, head)))]
    for fid in ids:
        lines += ["", "[[finding]]", "id = " + toml_string(fid)]
        lines += ['held_by = "coordinator"', "finding = " + toml_string(clauses[fid])]
        lines += ["position = " + toml_string(held[fid])]
    body = "\n".join(lines) + "\n"
    found, why = kdispute.read_findings(body, "the dispute findings file")
    if why or [f["finding"] for f in found["findings"]] != [clauses[i] for i in ids]:
        raise BriefError("the dispute findings file is not written: {}".format(why))
    return body


def write_dispute_findings(root, wi, positions, rel):
    """Write `dispute_findings` to the repo-relative `rel`, never over an
    existing file; return its path.

    Implements: SR-146, LLR-313
    """
    path = Path(root) / rel
    if path.exists():
        raise BriefError("{} already exists".format(rel))
    body = dispute_findings(root, wi, positions)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    return path


def write_pass(root, wi, dispute=None):
    """Write `wi`'s pass record (`kitlib.plan_pass.render`, the reader's own
    grammar) from HEAD's evidence; return its path. Refused, writing nothing,
    for every reason `pass_fields` gives and for a row already passed.

    Implements: SR-146, LLR-313
    """
    path = Path(root) / plan_pass.record_path(wi)
    if path.exists():
        raise BriefError("{} already has a pass record".format(wi))
    text = plan_pass.render(pass_fields(root, wi, dispute))
    with path.open("x", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
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


def _review_bar_refusal(root, lane, sha, tests):
    """The commit whose verified `review` attestation for `tests` stands for
    the reviewed commit `sha`, or `BriefError` naming `sha`, the cause and the
    step that records one. The render trusts the record and never runs the bar.

    Implements: SR-241, LLR-341
    """
    attested, cause = kverdict.review_attestation(root, sha, tests)
    if attested is not None:
        return attested
    raise BriefError(
        "{} carries no review bar attestation for the round's tests: {}. Run "
        '"$PY" {}/integrate.py attest --branch {} --bar review --tests {} from '
        "the primary checkout (staging the work it attests, or nothing for an "
        "empty attestation commit), then render again".format(
            sha, cause, agent_brief.scripts_dir(root), lane, " ".join(tests)
        )
    )


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
        stance=args.stance,
    )
    attested = _review_bar_refusal(args.root, lane, sha, rnd.tests)
    text, verdict = render_review(args.root, rnd)
    _write(args.out, text)
    print(
        "review_brief: {} renders over the review bar's attestation at {} "
        "(tests={})".format(sha, attested, kverdict.tests_digest(rnd.tests))
    )
    print("review_brief: wrote {}; the reviewer writes {}".format(args.out, verdict))
    print(
        "review_brief: file it with `review_brief.py file --review {} --sha {} "
        "--scope {}`".format(verdict, sha, args.scope)
    )
    return 0


def _cmd_critique(args):
    if args.plan:
        if not args.sha:
            raise BriefError("a plan critique names the lane commit holding the plan")
        _lane, _base, sha = lane_commits(args.root, args.sha, args.sha)
        rendered = render_plan_critique(
            args.root, args.wi, args.rubric, sha, args.scratch
        )
        text, verdict = rendered
    else:
        verdict = "{}/{}-scope-critique.md".format(
            _posix(args.scratch).rstrip("/"), args.wi
        )
        text = render_critique(args.root, args.wi, args.rubric, verdict)
    _write(args.out, text)
    print("review_brief: wrote {}; the critic writes {}".format(args.out, verdict))
    return 0


def _cmd_plan(args):
    rnd = "-r2" if args.revise else ""
    scratch = _posix(args.scratch).rstrip("/")
    plan_out = "{}/{}-plan{}.md".format(scratch, args.wi, rnd)
    _write(args.out, render_plan(args.root, args.wi, plan_out, args.revise))
    print("review_brief: wrote {}; the planner writes {}".format(args.out, plan_out))
    return 0


def _cmd_plan_file(args):
    if args.passed:
        path = write_pass(args.root, args.wi, args.dispute)
    elif args.dispute_findings and args.positions:
        try:
            held = Path(args.positions).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise BriefError("cannot read {}: {}".format(args.positions, exc)) from exc
        path = write_dispute_findings(args.root, args.wi, held, args.dispute_findings)
    elif args.critique and args.sha:
        _lane, sha, _head = lane_commits(args.root, args.sha, "HEAD")
        try:
            text = Path(args.critique).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise BriefError("cannot read {}: {}".format(args.critique, exc)) from exc
        path = file_plan_critique(args.root, args.wi, text, sha)
    else:
        raise BriefError("name a critique and the commit it reviewed, or --pass")
    print("review_brief: filed {}; commit it alone".format(_posix(path)))
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
    rev.add_argument(
        "--stance",
        default="ordinary",
        choices=STANCES,
        help="convergence: the round confirms fixes (never with --scope narrow)",
    )
    rev.add_argument("--python", default=sys.executable, help="the interpreter to run")
    rev.add_argument("--out", required=True, help="where to write the brief")
    crit = sub.add_parser("critique", help="render a work item's scope critique")
    crit.add_argument("--wi", required=True, help="the work item whose scope is judged")
    crit.add_argument("--rubric", required=True, help="the scope rubric, repo-relative")
    crit.add_argument("--scratch", required=True, help="the critic's writable area")
    crit.add_argument("--out", required=True, help="where to write the brief")
    crit.add_argument("--plan", action="store_true", help="critique the row's plan")
    crit.add_argument("--sha", help="with --plan: the lane commit holding the plan")
    pln = sub.add_parser("plan", help="render a single row's planner brief")
    pln.add_argument("--wi", required=True, help="the claimed work item to plan")
    pln.add_argument("--scratch", required=True, help="the planner's writable area")
    pln.add_argument("--out", required=True, help="where to write the brief")
    pln.add_argument("--revise", action="store_true", help="the one revision")
    pfl = sub.add_parser("plan-file", help="file a plan critique, or the pass")
    pfl.add_argument("--wi", required=True, help="the work item whose plan it is")
    pfl.add_argument("--critique", help="the critic's verdict file to file")
    pfl.add_argument("--sha", help="the lane commit the critique reviewed")
    pfl.add_argument(
        "--pass", dest="passed", action="store_true", help="write the pass record"
    )
    pfl.add_argument("--dispute", help="with --pass at the cap: the dispute verdict")
    pfl.add_argument(
        "--dispute-findings",
        help="at the cap: write the dispute findings file here (repo-relative)",
    )
    pfl.add_argument(
        "--positions", help="with --dispute-findings: one `F#: <position>` per line"
    )
    fil = sub.add_parser("file", help="file a review as the lane's next round file")
    fil.add_argument("--review", required=True, help="the reviewer's verdict file")
    fil.add_argument("--sha", required=True, help="the reviewed commit")
    fil.add_argument("--scope", required=True, choices=SCOPES)
    fil.add_argument("--phase", default="REVIEW-A", choices=PHASES)
    for each in (rev, crit, fil, pln, pfl):
        each.add_argument(
            "--root", default=".", help="the lane worktree (default: cwd)"
        )
    return ap


def main(argv=None):
    utf8_console()
    args = _parser().parse_args(argv)
    run = {
        "review": _cmd_review,
        "critique": _cmd_critique,
        "file": _cmd_file,
        "plan": _cmd_plan,
        "plan-file": _cmd_plan_file,
    }
    try:
        return run[args.cmd](args)
    except (BriefError, prompts.PromptError) as exc:
        print("review_brief: REFUSED — {}".format(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
