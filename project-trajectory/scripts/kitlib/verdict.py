"""THE VERDICT RECORD: which artifact carries a lane's governing review verdict,
and what binds that verdict to the tree it judged.

WHY THIS EXISTS (OI-76, ruled 2026-08-31 — "B with C and the generated rollup;
governing = TREE IDENTITY"). The merge gate used to read a hand-authored
`docs/reviews/WI-<n>-REVIEW-A.md` rollup that **nothing in the kit wrote**, and
it judged that rollup's freshness by comparing commit TIMES. Three defects rode
together: nobody wrote it, so every mechanized lane stopped at a human; it
paraphrased evidence that already existed; and the trust was inverted — the
round files carry the anti-forgery story and the gate ignored them. The ruling
re-points the gate at the evidence and replaces the time comparison with an
identity: **a verdict counts only if it names the tree it judged.**

ONE DEFINITION, TWO READERS, and that is the whole reason this is a module
rather than two private helpers. `integrate._verdict_gate` (may this branch
merge?) and `agent_loop.review_owed_by_evidence` (does this lane still owe a
round?) are the same question asked from two sides, and they used to answer it
with two different rules over two different exclusion sets — which is how one
lane drew two identical `APPROVE findings=0` rounds because the loop's own
telemetry commits had moved HEAD past a verdict that was never invalidated.

THE IDENTITY, and why it is not a git tree sha. `tree_identity` folds
`git ls-tree -r <rev>` with the RECORD paths removed — `docs/reviews/`,
`docs/log.d/`, `docs/iteration/`. Those three are the process writing about
itself: a round file, a log fragment and a session log are records OF the work
under review, never the work, so a commit that only touches them cannot
invalidate a verdict. The digest is a truncation-free SHA-256 over the filtered
listing, 64 hex — deliberately NOT 40, because a 40-hex `tree=` beside the
`Bar-Green: tree=<40 hex>` trailer (which IS a git tree object id) would read as
the same kind of value and it is not one.

THE TRAILER is the machine half, the `Bar-Green:` pattern applied to a verdict:

    Review-Verdict: APPROVE|CHANGES-REQUESTED rounds=<N> tree=<64 hex>

It rides the commit that RECORDS the round, is written by the coordinator (never
by a session), and is additive — an adopter whose loop does not write one yet
pays nothing, because the round file's own filename carries the reviewed sha and
resolves to the same identity.

THE LOGGED-SESSION RESTRICTION closes the plan's finding K: a BUILD session once
wrote `010-REVIEW-A-e26ab03.md` into the review path — an implementer authoring
its own approval. A file in `docs/reviews/` is a ROUND only when the coordinator's
own committed session log for that (train, ordinal) declares a REVIEW phase.
The session log is written and committed by the loop, so the join is evidence a
session cannot forge for itself without also forging the coordinator's telemetry.

WHAT THIS MODULE DELIBERATELY DOES NOT DO: it never decides what an absent answer
MEANS (`kitlib.git`'s rule, inherited). `None` is "git had nothing to say"; the
merge gate reads that as a refusal and the loop's derivation reads it as "assume
a round is owed" — both fail toward more review, and each says so at its own
call site.

Contracts: IF-175 — the seam this module declares (process.md §8; row of record
in docs/requirements/interfaces.toml).

Contract IF-175: the verdict record, as functions two independent readers call
    to reach ONE answer. `tree_identity` (and its pure half `fold_listing`)
    gives the non-record tree identity a verdict names; `format_trailer` /
    `parse_trailer` the `Review-Verdict:` machine half; `round_file` /
    `session_log` the two name grammars `docs/reviews/` and `docs/iteration/`
    carry; `branch_paths` / `logged_rounds` / `round_entries` the round evidence
    a branch holds, restricted to rounds a logged reviewer session produced and
    to the tree under judgement; `branch_trailers` the verified attestations on
    the branch's own commits. Pure functions plus thin reads through
    `kitlib.git`, so nothing here writes and nothing imports a sibling service —
    the verdict parser arrives as an ARGUMENT rather than an import, which is
    what keeps this leaf free of an edge back into the scoring layer. Every
    function answers `None` where git had nothing to say and NEVER decides what
    that means: the merge slot reads it as a refusal, the loop's review-owed
    derivation as "assume a round is owed", and both directions are toward more
    review. The contract this row exists to hold is the SINGULARITY — a second
    reader of round evidence anywhere else is a finding against this row.
"""

import hashlib
import re

from .git import git_out

__all__ = [
    "RECORD_PREFIXES",
    "REVIEW_PHASES",
    "TRAILER_LABEL",
    "format_trailer",
    "parse_trailer",
    "is_record_path",
    "fold_listing",
    "tree_identity",
    "round_file",
    "session_log",
    "branch_paths",
    "logged_rounds",
    "round_entries",
    "branch_trailers",
]

# The process writing about itself. A commit touching only these cannot
# invalidate a verdict — see the module docstring for why each one is here.
RECORD_PREFIXES = ("docs/reviews/", "docs/log.d/", "docs/iteration/")

REVIEW_PHASES = ("REVIEW-A", "REVIEW-B")

TRAILER_LABEL = "Review-Verdict"

# The machine half. Anchored per-line (`re.M`) exactly like the `Bar-Green:`
# reader, and the verdict word is a CLOSED alternation rather than `\S+`: an
# unrecognized word must fail to parse (and so read as no verdict at all) rather
# than arrive downstream as a third outcome nobody wrote a rule for.
TRAILER_RE = re.compile(
    r"^{}:[ \t]+(APPROVE|CHANGES-REQUESTED)[ \t]+rounds=(\d+)[ \t]+"
    r"tree=([0-9a-f]{{64}})[ \t]*$".format(TRAILER_LABEL),
    re.M,
)

# `<ordinal>-<phase>-<reviewed sha7>[-<tag>].md`, the name `agent_loop` composes
# in `fresh_verdict_path`. The optional tag is `-relaxed` today (C5's recorded
# heterogeneity relaxation) and any later marker; it is captured by nobody here
# because the NAME's job is only to say which round this is and what it read.
ROUND_FILE_RE = re.compile(
    r"^(?P<ordinal>\d+)-(?P<phase>REVIEW-[A-Z])-(?P<sha>[0-9a-f]{7,40})"
    r"(?:-[A-Za-z0-9._-]+)?\.md$"
)

# `[<train>-]<ordinal>-<YYYYMMDD>-<HHMMSS>.log`, written by
# `agent_common.write_session_log`. The train prefix is optional because the
# attended (single-lane) layout has none.
SESSION_LOG_RE = re.compile(r"^(?:(?P<train>.+)-)?(?P<ordinal>\d+)-\d{8}-\d{6}\.log$")

_PHASE_HEADER_RE = re.compile(r"^# phase:[ \t]*(.*)$", re.M)

_REVIEWS = "docs/reviews"
_ITERATION = "docs/iteration"


# --- the trailer --------------------------------------------------------------


def format_trailer(word, rounds, tree):
    """The `Review-Verdict:` line for a round whose merged verdict is `word`."""
    return "{}: {} rounds={} tree={}".format(TRAILER_LABEL, word, int(rounds), tree)


def parse_trailer(message):
    """`(word, rounds, tree)` from the LAST `Review-Verdict:` line in `message`,
    or None when it carries none.

    The last, not the first: a commit message that quotes an earlier trailer
    (a rework commit citing the round it answers) must not have the quotation
    read as its own attestation, and the kit's convention puts a commit's own
    trailers at the end."""
    matches = TRAILER_RE.findall(message or "")
    if not matches:
        return None
    word, rounds, tree = matches[-1]
    return word, int(rounds), tree


# --- the identity -------------------------------------------------------------


def is_record_path(path):
    """Is `path` one of the process's records of itself, rather than work?"""
    norm = str(path).replace("\\", "/").lstrip("./")
    return any(norm.startswith(prefix) for prefix in RECORD_PREFIXES)


def fold_listing(listing):
    """The identity of a `git ls-tree -r` LISTING, with record paths dropped.

    Pure, so the rule is testable without a repository — which matters because
    this is the one function that decides whether two trees are "the same work".
    Each surviving line is folded whole (mode, type, blob sha and path), so a
    mode change or a rename is as invalidating as an edit."""
    fold = hashlib.sha256()
    for line in (listing or "").splitlines():
        if not line.strip():
            continue
        # `<mode> <type> <sha>\t<path>` — split on the TAB, since a path may
        # contain spaces and the fields before it never do.
        _meta, _tab, path = line.partition("\t")
        if not _tab or is_record_path(path):
            continue
        fold.update(line.encode("utf-8", "surrogateescape"))
        fold.update(b"\n")
    return fold.hexdigest()


def tree_identity(root, rev):
    """The verdict-relevant tree identity of `rev`, or None when git cannot say.

    `--full-tree` so the answer does not depend on the caller's cwd inside the
    repository, and `-z` is deliberately NOT used: the fold reads whole lines and
    a NUL-delimited listing would need its own splitting rule for no gain."""
    listing = git_out(root, ["ls-tree", "-r", "--full-tree", rev])
    if listing is None:
        return None
    return fold_listing(listing)


# --- the round evidence -------------------------------------------------------


def round_file(path):
    """`(train, ordinal, phase, reviewed_sha)` for a round file, else None.

    `train` is the `docs/reviews/<train>/` directory, or "" for the flat
    pre-train layout. The ordinal is an int so "latest" is a numeric comparison,
    which is what `score_reviews.latest_phase_verdicts` sorts on."""
    norm = str(path).replace("\\", "/")
    if not norm.startswith(_REVIEWS + "/"):
        return None
    rest = norm[len(_REVIEWS) + 1 :]
    train, _sep, name = rest.rpartition("/")
    if "/" in train:
        return None  # nested deeper than one train directory: not a round file
    matched = ROUND_FILE_RE.match(name)
    if not matched:
        return None
    return (
        train,
        int(matched.group("ordinal")),
        matched.group("phase"),
        matched.group("sha"),
    )


def session_log(path):
    """`(train, ordinal)` for a coordinator session log, else None."""
    norm = str(path).replace("\\", "/")
    if not norm.startswith(_ITERATION + "/"):
        return None
    name = norm[len(_ITERATION) + 1 :]
    if "/" in name:
        return None
    matched = SESSION_LOG_RE.match(name)
    if not matched:
        return None
    return matched.group("train") or "", int(matched.group("ordinal"))


def branch_paths(root, branch, base):
    """Every path `base..branch`'s OWN commits touched under the two record
    directories, or None when git cannot answer.

    Scoped to the branch's own commits on purpose: a lane branch carries every
    historical train's round files inherited from the trunk, and resolving a
    tree identity for each of them would cost hundreds of git calls to reject
    hundreds of rounds that could not name this tree anyway."""
    out = git_out(
        root,
        [
            "log",
            "--format=",
            "--name-only",
            "{}..{}".format(base, branch),
            "--",
            _REVIEWS,
            _ITERATION,
        ],
    )
    if out is None:
        return None
    return sorted({ln.strip() for ln in out.splitlines() if ln.strip()})


def logged_rounds(root, branch, paths):
    """The rounds among `paths` that a LOGGED REVIEWER SESSION produced, as
    `(ordinal, phase, reviewed_sha, path)` — the plan's finding K, closed.

    A round file with no coordinator session log for its (train, ordinal), or
    one whose log declares a non-review phase, is NOT a round: it is a file
    somebody wrote in the review path. An unreadable log is treated the same
    way, which is the fail-toward-more-review direction."""
    reviewer = set()
    for path in paths:
        key = session_log(path)
        if key is None:
            continue
        blob = git_out(root, ["show", "{}:{}".format(branch, path)])
        if blob is None:
            continue
        header = _PHASE_HEADER_RE.search(blob[:4000])
        if header and header.group(1).strip() in REVIEW_PHASES:
            reviewer.add(key)
    rounds = set()
    for path in paths:
        parsed = round_file(path)
        if parsed is None:
            continue
        train, ordinal, phase, sha = parsed
        if (train, ordinal) in reviewer:
            rounds.add((ordinal, phase, sha, path))
    return sorted(rounds)


def round_entries(root, branch, rounds, want, parse):
    """The `(phase, ordinal, verdict)` entries `score_reviews.latest_phase_verdicts`
    reads, restricted to the rounds that NAME the tree `want`.

    The tree a round names is the identity of the commit its FILENAME cites —
    the reviewed head, which the reviewer session did not author. That is the
    binding; the `Review-Verdict:` trailer is the same name spelled for a
    machine (see `branch_trailers`), never a second source of truth.

    `parse` is `score_reviews.parse_verdict`, injected rather than imported so
    this leaf keeps no edge back into the scoring layer."""
    entries = []
    resolved = {}
    for ordinal, phase, sha, path in rounds:
        if sha not in resolved:
            resolved[sha] = tree_identity(root, sha)
        if resolved[sha] != want:
            continue
        text = git_out(root, ["show", "{}:{}".format(branch, path)])
        if text is None:
            continue
        entries.append((phase, ordinal, parse(text).verdict))
    return entries


def branch_trailers(root, branch, base):
    """`{reviewed tree: (word, rounds)}` from every VERIFIED `Review-Verdict:`
    trailer on the branch's own commits, or None when git cannot answer.

    VERIFIED means the trailer names the non-record tree identity of the commit
    that CARRIES it — the `Bar-Green` verification applied to a verdict. The
    record commit only touches record paths, so its own non-record identity IS
    the reviewed tree, and a trailer amended onto any other commit names a tree
    that is not its carrier's.

    THIS IS NOT AN ACCEPT PATH, and the distinction is the whole anti-forgery
    story. Anyone with commit access can type a trailer onto their own commit
    and it will verify, because it is their tree. What a trailer cannot forge is
    the coordinator's committed session log, which is why the ROUND EVIDENCE
    decides and the trailer is read as a CROSS-CHECK: a trailer that names the
    tree under judgement and contradicts the rounds is a signal, not a verdict."""
    log = git_out(root, ["log", "--format=%H%x1f%B%x1e", "{}..{}".format(base, branch)])
    if log is None:
        return None
    by_tree = {}
    for record in log.split("\x1e"):
        sha, _sep, message = record.partition("\x1f")
        sha = sha.strip()
        if not sha:
            continue
        parsed = parse_trailer(message)
        if parsed is None:
            continue
        word, rounds, tree = parsed
        if tree_identity(root, sha) != tree:
            continue  # the words rode onto a tree they do not describe
        by_tree[tree] = (word, rounds)
    return by_tree
