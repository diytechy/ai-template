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

THE SAME QUESTION HAS A SECOND DIMENSION: not only WHICH tree a verdict names
but HOW MANY of the declared phases have spoken about it. The two readers
diverged there too, and later — the gate was taught to require every phase the
`review_rounds` dial declares while the loop still read "any verdict at this
tree means the round was served", so a run that died between REVIEW-A and
REVIEW-B (the phase queue is in-memory) resumed scheduling nothing against a
gate refusing the missing phase. `declared_phases` is the span both slice;
`phases_owed` is what a resume still has to draw.

THE IDENTITY, and why it is not a git tree sha. `tree_identity` folds
`git ls-tree -r <rev>` with the RECORD paths removed — `docs/reviews/`,
`docs/log.d/`, `docs/iteration/`. Those three are the process writing about
itself: a round file, a log fragment and a session log are records OF the work
under review, never the work, so a commit that only touches them cannot
invalidate a verdict. The digest is a truncation-free SHA-256 over the filtered
listing, 64 hex — deliberately NOT 40, because a 40-hex `tree=` beside the
`Bar-Green: tree=<40 hex>` trailer (which IS a git tree object id) would read as
the same kind of value and it is not one.

WHAT CANNOT INVALIDATE A VERDICT HAS TWO HALVES, AND ONE OWNER. The record
PATHS above are the first; the station's REFRESH COMMIT is the second, and it is
here for the same reason rather than in the merge slot. A refresh merges the
trunk in and re-runs the compile/regen: it moves the tree without the lane
having changed its work, so a verdict is governed by the tree at the peeled work
tip (`governing_rev`), not at the branch tip. WI-560 Done-when 1 asks for ONE
definition of "the last commit that could invalidate a verdict" — that sentence
covers which commit as much as which paths, so `governing_identity` is the
single answer BOTH readers are handed. When the peel lived in `integrate` and
the loop measured at `HEAD` instead, the two readers disagreed across exactly
one refresh commit and a resumed lane drew a round the gate would not read
(REVIEW-A round 007, finding 2).

THE TWO HALVES INTERACT, which is the part that had to be driven to be believed.
The peel is written twice on purpose: `work_tip` peels only a refresh sitting
literally on the tip, because it feeds a `reset --hard` where peeling one commit
too far destroys committed work, and `governing_rev` walks THROUGH any commit
whose identity equals its parent's to reach a refresh it would otherwise hide.
While the identity used the tip-only peel, a single telemetry commit — a record
path, which the fold is built to ignore — moved the identity anyway, by burying
the refresh under it. A read-only question can afford an answer a destructive
one cannot. The walk's step condition is the module's own sentence rather than a
proxy for it ("a commit that cannot invalidate a verdict"), which is why the
empty attestation carrier `commit_telemetry` writes needs no case of its own.

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
    gives the non-record tree identity a verdict names, and
    `governing_identity` — over `governing_rev` / `refresh_attestation` — gives
    the rev that identity is measured at, so neither reader chooses its own
    (`work_tip` is the tip-only peel the `reset --hard` shares, deliberately
    NOT the same walk);
    `format_trailer` / `parse_trailer` the `Review-Verdict:` machine half;
    `round_file` / `session_log` the two name grammars `docs/reviews/` and
    `docs/iteration/`
    carry; `branch_paths` / `logged_rounds` / `round_entries` the round evidence
    a branch holds, restricted to rounds a logged reviewer session produced and
    to the tree under judgement; `declared_phases` / `phases_owed` the phase span
    a review policy declares and which of those phases a tree has never had
    DRAWN — the resume's question, weaker than the gate's demand for a parseable
    APPROVE on exactly the mangled-verdict class and no other, so the two
    readers share a span without pretending to share a threshold;
    `branch_trailers` the verified attestations on
    the branch's own commits, in commit order. Pure functions plus thin reads through
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

from .git import git_bytes, git_out
from .station import BAR_GREEN

__all__ = [
    "RECORD_PREFIXES",
    "REVIEW_PHASES",
    "TRAILER_LABEL",
    "format_trailer",
    "parse_trailer",
    "is_record_path",
    "fold_listing",
    "tree_identity",
    "refresh_subject",
    "refresh_attestation",
    "work_tip",
    "governing_rev",
    "governing_identity",
    "round_file",
    "session_log",
    "branch_paths",
    "logged_rounds",
    "round_entries",
    "branch_entries",
    "declared_phases",
    "phases_owed",
    "round_count",
    "format_branch_trailer",
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
    if isinstance(path, bytes):
        norm = path.replace(b"\\", b"/").lstrip(b"./")
        return any(
            norm.startswith(prefix.encode("ascii")) for prefix in RECORD_PREFIXES
        )
    norm = str(path).replace("\\", "/").lstrip("./")
    return any(norm.startswith(prefix) for prefix in RECORD_PREFIXES)


def fold_listing(entries):
    """The identity of `git ls-tree -r` ENTRIES, with record paths dropped.

    Each entry is one raw `<mode> <type> <sha>\\t<path>` byte record. It takes
    a split SEQUENCE rather than git's complete stdout deliberately: without
    `-z` git QUOTES any path holding a non-ASCII or special character
    (`"docs/reviews/002-REVIEW-A-abcdef\\303\\251.md"`), the leading quote
    defeats every `RECORD_PREFIXES` test, and a single accented filename under
    `docs/log.d/` folds into the identity and silently stales every governing
    verdict on the branch (REVIEW-A round 007, finding 3, driven both ways).
    Splitting is the caller's job so no reader here ever sees git's DISPLAY
    encoding. The record-prefix boundary and hash are byte-native: decoding
    before either one collapses distinct invalid-UTF-8 paths onto the same
    replacement character (REVIEW-A round 019, driven on `\\200` -> `\\201`).

    Pure, so the rule is testable without a repository — which matters because
    this is the one function that decides whether two trees are "the same work".
    Each surviving entry is folded whole (mode, type, blob sha and path), so a
    mode change or a rename is as invalidating as an edit."""
    fold = hashlib.sha256()
    for line in entries or ():
        if not line.strip():
            continue
        # `<mode> <type> <sha>\t<path>` — split on the TAB, since a path may
        # contain spaces and the fields before it never do.
        _meta, _tab, path = line.partition(b"\t")
        if not _tab or is_record_path(path):
            continue
        fold.update(line)
        fold.update(b"\n")
    return fold.hexdigest()


def tree_identity(root, rev):
    """The verdict-relevant tree identity of `rev`, or None when git cannot say.

    `--full-tree` so the answer does not depend on the caller's cwd inside the
    repository, and `-z` because it is the ENCODING BOUNDARY: NUL-delimited
    output is never quoted or escaped, so `fold_listing` is handed raw bytes and
    the record-path test cannot be defeated by a filename (see its docstring).
    A NUL split also survives a path containing a newline, which the line split
    it replaced could not. No decode sits in this path: path bytes are part of
    the identity, not display text."""
    if rev is None:
        return None
    listing = git_bytes(root, ["ls-tree", "-r", "-z", "--full-tree", rev])
    if listing is None:
        return None
    return fold_listing(listing.split(b"\0"))


# --- the rev the identity is measured at --------------------------------------


# The station's refresh attestation, VERIFIED against git. The label comes from
# `station` so the writer (`integrate.refresh`) and this verifier share one
# spelling rather than two literals that must agree.
_ATTEST_RE = re.compile(
    r"^{}\s+tree=([0-9a-f]{{40}})\s+work=([0-9a-f]{{40}})\s+(\S.*)$".format(BAR_GREEN)
)

# How far back `work_tip` will peel refresh commits. The disposable-commit rule
# means at most ONE can ever sit on the tip, so this is a guard against a
# hand-made pathological history, not an expected depth.
_MAX_REFRESH_PEEL = 8


def refresh_subject(branch):
    """The refresh commit's subject prefix for `branch` - one home, because the
    writer and the verifier must agree on it exactly."""
    return "refresh: {} onto trunk ".format(branch)


def refresh_attestation(root, branch, rev=None):
    """`(work_tip_sha, bar summary)` if `rev` is a GENUINE refresh commit for
    `branch`, else None. `rev` defaults to the branch tip.

    The bar is attested to a TREE, and this is where that sentence is made
    true rather than merely written down. A commit message is not evidence: it
    can be copied, hand-written, amended onto different content, cherry-picked
    or rebased, and every one of those carries the words onto a tree nobody
    barred (REVIEW-A round 1, driven both ways - a forged trailer on an
    ordinary work commit, and `commit --amend` adding a file to a real one).

    So the trailer NAMES what it attests and all three names are verified
    against git:

        Bar-Green: tree=<40 hex> work=<40 hex> <bar summary>

      * `tree=` must equal the commit's OWN tree. This is the load-bearing one:
        no edit that changes content can keep it, because the tree sha IS the
        content. `git write-tree` is what lets the refresh know the value
        before it commits - the index it barred is the tree it commits.
      * `work=` must equal the commit's first parent, so the disposable-commit
        peel below has a stated target rather than a guessed one, and a
        cherry-pick or rebase (new parent) is rejected.
      * the SUBJECT must be this branch's own `refresh: <branch> onto trunk`,
        so a refresh commit merged in from elsewhere is not read as this
        branch's.

    THE HONEST BOUND: this defeats ACCIDENT, not INTENT. Every accidental
    carrier refuses - a copied message, an amend, a rebase, a cherry-pick, a
    trailer quoted in an ordinary commit. But forging one deliberately is FOUR
    git invocations in the lane worktree and no bar at all: `add -A`, `T=$(git
    write-tree)`, `P=$(git rev-parse <branch>)`, and the `commit` that carries
    those two values in the trailer. REVIEW-A round 2 drove exactly that and landed an
    unbarred file on trunk. The format is printed in every refresh commit, so
    the cost is reading, not reverse-engineering.

    That is accepted, deliberately. The only structural closure is a bar the
    slot itself runs and cannot skip, and DECISION 3 (owner ruling 2026-07-31)
    deleted the merge bar outright: a kept-just-in-case bar is exactly the
    shape §0's governing principle warns against. So the threat model here is
    the same one the rest of the coordinator holds - bugs, drift and a lane that
    goes wrong, not a lane that lies on purpose. A lane is trusted code the
    operator chose to run. If that ever stops being true, the answer is a
    slot-side bar and a reopened DECISION 3, not a longer trailer.
    """
    rev = rev or branch
    message = git_out(root, ["log", "-1", "--format=%B", rev]) or ""
    lines = message.splitlines()
    if not lines or not lines[0].strip().startswith(refresh_subject(branch)):
        return None
    matched = None
    for line in lines:
        matched = _ATTEST_RE.match(line.strip())
        if matched:
            break
    if not matched:
        return None
    tree, work, summary = matched.group(1), matched.group(2), matched.group(3)
    if _rev(root, rev + "^{tree}") != tree:
        return None  # the message rode onto a tree it does not describe
    if _rev(root, rev + "^1") != work:
        return None  # ...or onto a different parent than the one it names
    return work, summary.strip()


def work_tip(root, branch):
    """The branch's last WORK commit as a sha: the tip, with any refresh commit
    peeled off at the work sha that refresh ITSELF recorded.

    Two callers, one meaning. `integrate.refresh` resets here before it merges
    (the §A2.1 disposable-commit rule: a retry never stacks a second merge on
    the first, because docs/log.md is append-compiled and the stack would
    conflict on the file end). `governing_identity` measures code-time here,
    because the refresh is MECHANICAL bookkeeping - it rewrites the compiled log
    and the generated artifacts, and if that counted as code it would stale the
    honest APPROVE that had to precede it.

    The peel is why `refresh_attestation` had to become a verification rather
    than a substring test: this function feeds a `reset --hard`, so peeling one
    commit too far DESTROYS committed work. A work commit whose message merely
    quoted the trailer used to be peeled, and its file left the branch (REVIEW-A
    round 1, driven). Now nothing is peeled that does not carry its own tree and
    parent, which an ordinary commit cannot do by accident.
    """
    rev = branch
    for _ in range(_MAX_REFRESH_PEEL):
        attested = refresh_attestation(root, branch, rev)
        if attested is None:
            return _rev(root, rev)
        rev = attested[0]
    return _rev(root, rev)


# How far `governing_rev` will walk. Deeper than `_MAX_REFRESH_PEEL` because
# what it walks THROUGH is identity-preserving commits, and a lane accumulates
# one telemetry commit per session. Hitting the bound stops the walk, which
# measures at a later rev and so can only ask for MORE review, never less.
_MAX_GOVERNING_WALK = 64


def governing_rev(root, branch, rev=None):
    """The commit whose tree governs a verdict on `branch`: `rev` (default: the
    tip), with refresh commits peeled AND identity-preserving commits walked
    through.

    `rev` IS A PARAMETER BECAUSE THE ROUND EVIDENCE ASKS THE SAME QUESTION AT A
    DIFFERENT COMMIT. `round_entries` must decide which tree a round NAMES, and
    the only honest answer is the one this function gives for the sha that round
    read — measuring the reviewed sha raw while the gate measured the tip
    composed left two rev-choices for one definition, and a round drawn after a
    station refresh matched neither reader forever (REVIEW-A round 015). The
    `branch` argument stays separate from `rev` because the peel VERIFIES a
    refresh commit against the branch it names, which is a property of the
    branch and not of the commit being measured.

    WHY THIS IS NOT `work_tip`. Both peel a refresh, and they must not share an
    implementation, because `work_tip` feeds a `reset --hard` and may only ever
    peel a refresh sitting literally on the tip — peeling one commit further
    there DESTROYS committed work. This function only ever reads, so it can
    afford the honest question: is there a refresh commit under here that
    nothing invalidating has been stacked on?

    That gap was a live defect, driven. The fold already ignores
    `RECORD_PREFIXES`, so a telemetry commit cannot move the identity — but a
    telemetry commit landing ON TOP of a refresh made the tip stop being a
    refresh commit, the tip-only peel stopped applying, and the identity flipped
    from the pre-refresh work tree to the post-refresh one. An APPROVE served
    before the refresh then named a tree nothing governed: the loop answered
    `owed=True` and the merge slot refused "no logged review round names its
    current tree" — both readers agreeing on the WRONG answer, and an honest
    approval parked at a supervisor stop by the coordinator's own telemetry.
    That is the OI-76 failure mode this row exists to eliminate, surviving one
    commit further down than the round-007 fix reached.

    THE STEP CONDITION IS THE DEFINITION ITSELF, not a proxy for it. A commit
    may be walked through exactly when its non-record identity EQUALS its first
    parent's — which is, in as many words, "a commit that cannot invalidate a
    verdict", the sentence this whole module is built around. Measuring it
    directly is what makes every WALK step provably identity-neutral: stepping
    can only ever reach a rev carrying the identity it stepped from, so the walk
    cannot invent an answer, only see PAST commits to a refresh they would
    otherwise hide. The PEEL is the one step that does move the identity, and
    deliberately — that is the whole job of a refresh, and it is admitted by
    verification against git rather than by measurement — so the returned rev
    carries the tip's identity only on a branch with no refresh under it.

    It replaces a predicate that CLASSIFIED THE PATHS a commit touched, and the
    replacement is the fix for round 012's finding 1 rather than a tidy-up. That
    predicate had to answer for every commit shape whose paths it could not
    read — a merge, an empty commit — and it answered "stop", which reads as
    "this might have invalidated the verdict" for a commit that provably did
    not. `agent_common.commit_telemetry` then began writing exactly that shape:
    a `Review-Verdict:` attestation must land even when the bookkeeping it rides
    is unchanged, so it commits EMPTY, and the very commit that RECORDS an
    approval buried the refresh underneath it. Asking the identity question
    directly makes the empty carrier, the merge commit and the quoted-path trap
    (`is_record_path` against git's display encoding, round 007's finding 3
    pointed the more dangerous way round) all unrepresentable at once, because
    no path is classified here at all."""
    rev = rev or branch
    identity = tree_identity(root, rev)
    for _ in range(_MAX_GOVERNING_WALK):
        attested = refresh_attestation(root, branch, rev)
        if attested is not None:
            rev = attested[0]
            identity = tree_identity(root, rev)
            continue
        parent = _rev(root, rev + "^1")
        if identity is None or parent is None:
            break  # git had nothing to say, or a root commit: nothing under it
        parent_identity = tree_identity(root, parent)
        if parent_identity != identity:
            break  # this commit changed the work, so it is where the walk ends
        rev, identity = parent, parent_identity
    return _rev(root, rev)


def governing_identity(root, branch, rev=None):
    """The non-record tree identity a verdict at `rev` on `branch` governs, or
    None. `rev` defaults to the branch tip: the identity a verdict must NAME.

    THE ONE ANSWER EVERY READER IS HANDED (WI-560 Done-when 1). The merge slot
    asks "may this branch merge?" and the loop asks "does this lane still owe a
    round?"; they are the same question from two sides, and each computing its
    own rev is how they came to disagree across a refresh commit. Composing the
    two halves HERE — the record-path fold and the refresh peel — leaves the
    callers nothing to choose.

    "EVERY READER" INCLUDES THE ONES THAT ASK ABOUT A COMMIT rather than about
    the branch — `round_entries` for the sha a round file cites, and
    `branch_trailers` for the commit an attestation rides. They used to call
    `tree_identity` directly, which is the same composition with the peel left
    out, and the two answers part company across exactly one refresh commit:
    a round drawn AFTER a refresh named the post-refresh tree while the gate
    governed by the pre-refresh one, so the round was invisible to BOTH readers
    and no commit on the branch could ever make them agree (REVIEW-A round 015).
    One function, one rev rule, asked at whichever commit the caller holds."""
    return tree_identity(root, governing_rev(root, branch, rev))


def _rev(root, rev):
    """`rev` resolved to a full sha, or None."""
    out = git_out(root, ["rev-parse", "--verify", "--quiet", rev])
    return out.strip() if out and out.strip() else None


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

    The tree a round names is the GOVERNING identity of the commit its FILENAME
    cites — the reviewed head, which the reviewer session did not author. That
    is the binding; the `Review-Verdict:` trailer is the same name spelled for a
    machine (see `branch_trailers`), never a second source of truth.

    GOVERNING, not raw: through `governing_identity` and not `tree_identity`,
    because `want` is composed that way and a binding must be computed by the
    same definition it is compared against. A reviewer that read the branch
    right after a station refresh cites the POST-refresh sha, while the gate
    governs by the peeled PRE-refresh tree — so the raw fold made the two
    permanently unequal, the round invisible to the merge slot AND to
    `agent_loop.review_owed_by_evidence`, and the lane re-drew an identical
    round every tick: the double-identical-round class WI-560 Done-when 1 exists
    to make unrepresentable, re-entered through the binding rather than through
    the rev (REVIEW-A round 015). It is reachable on the shipped path because
    `dispatch._advance` spawns a lane's refresh as soon as its worker is DONE
    and BEFORE `integrate.integrate` runs, so any slot refusal parks the branch
    with a refresh commit and no round, and the next launch draws the round on
    top of it.

    `parse` is `score_reviews.parse_verdict`, injected rather than imported so
    this leaf keeps no edge back into the scoring layer."""
    entries = []
    resolved = {}
    for ordinal, phase, sha, path in rounds:
        if sha not in resolved:
            resolved[sha] = governing_identity(root, branch, sha)
        if resolved[sha] != want:
            continue
        text = git_out(root, ["show", "{}:{}".format(branch, path)])
        if text is None:
            continue
        entries.append((phase, ordinal, parse(text).verdict))
    return entries


def branch_entries(root, branch, base, want, parse):
    """Tree-bound entries from logged rounds in `base..branch`, or None when
    the branch's committed path set cannot be read."""
    paths = branch_paths(root, branch, base)
    if paths is None:
        return None
    return round_entries(root, branch, logged_rounds(root, branch, paths), want, parse)


def declared_phases(required):
    """The review phases a policy of `required` declares, in dispatch order.

    THE SPAN BOTH READERS SLICE, and it is here because they must slice it
    identically: the merge slot demands a verdict for each of these phases and
    the loop schedules each of them, so a policy the two read to different
    lengths is a lane that draws what will not clear or refuses what will never
    be drawn. The clamp is the whole content — a policy above `REVIEW_PHASES`
    asks for a phase no reviewer can be routed to (`agent_loop.
    _clamped_review_rounds` clamps the dial to the same span), and a NEGATIVE
    one slices from the END, so a bare `REVIEW_PHASES[:required]` would answer
    a policy of -1 with `("REVIEW-A",)` — a wrong answer rather than an empty
    one. Both callers guard the negative case today; neither should have to."""
    return list(REVIEW_PHASES[: max(0, required)])


def phases_owed(entries, required):
    """The declared phases with NO entry among `entries` — the phases this tree
    has never had DRAWN, which is `agent_loop.resume_owed_round`'s question.

    THE WEDGE THIS CLOSES. The merge slot began requiring every declared phase
    (round 022's finding — `review_rounds = 2` had been collapsed to a boolean,
    so a lone REVIEW-A cleared the gate) while `review_owed_by_evidence` still
    read "any entry at this tree means the round was served". A run that died
    between REVIEW-A and REVIEW-B left exactly that state — the phase queue is
    in-memory run state and does not survive the run — so the resumed lane
    scheduled nothing while the gate refused the merge for a phase nobody would
    ever draw. Answering with the MISSING PHASES rather than a yes/no is what
    lets the resume redraw only those, which matters as much as the fix: a
    resume that redrew the whole round would re-run a phase already served at
    this identity, and if that phase had DISSENTED the redraw would read as a
    reroll-until-green and be escalated — the gate's own `flipped` rule firing
    on an honest crash recovery.

    DELIBERATELY NOT THE GATE'S QUESTION, and the divergence is the design.
    This asks whether a phase was drawn; the gate asks whether it produced a
    parseable APPROVE (`score_reviews.latest_phase_verdicts`). They must differ
    on exactly one class — a round whose verdict file is present but UNPARSEABLE
    — because the two answers there are "do not draw it again" (it was drawn;
    redrawing it is the double-round class WI-560 DW1 exists to kill) and "do
    not merge on it" (a mangled meant-to-dissent must page, WI-260 review fix
    2). What they may NOT differ on is the phase span, which is why both slice
    `declared_phases`."""
    served = {phase for phase, _ordinal, _verdict in entries or ()}
    return [ph for ph in declared_phases(required) if ph not in served]


def round_count(entries):
    """Completed review cycles represented by the entries for ONE tree.

    A cycle contributes one entry per configured phase (REVIEW-A and, at
    policy 2, REVIEW-B), so the cycle count is the largest per-phase count —
    not the raw number of reviewer files. Callers first restrict `entries` to
    one tree through `round_entries`; rework therefore starts this count over.
    """
    per_phase = {}
    for phase, _ordinal, _verdict in entries:
        per_phase[phase] = per_phase.get(phase, 0) + 1
    return max(per_phase.values(), default=0)


def format_branch_trailer(root, branch, base, word, parse):
    """The tree-bound trailer derived from logged branch evidence, or None.

    Stamped at `governing_identity`, the value both readers key on. Naming the
    branch's RAW tree instead filed the attestation under a key
    `integrate._round_refusal` never looks up, so on a refreshed branch the
    cross-check silently stood down instead of cross-checking (REVIEW-A round
    015). `branch` must therefore be the lane's BRANCH NAME and not `HEAD`: the
    peel verifies a refresh commit against the branch it names, and `HEAD`
    matches no refresh subject."""
    if not word:
        return None
    tree = governing_identity(root, branch)
    if tree is None:
        return None
    entries = branch_entries(root, branch, base, tree, parse)
    if entries is None:
        return None
    count = round_count(entries)
    return format_trailer(word, count, tree) if count else None


def branch_trailers(root, branch, base):
    """`{reviewed tree: [(word, rounds), ...]}` from every VERIFIED
    `Review-Verdict:` trailer on the branch's own commits, or None when git
    cannot answer. Each list is in COMMIT ORDER, oldest first, so `[-1]` is the
    newest attestation for that tree.

    A SEQUENCE, not one attestation per tree, and the type is the fix. One tree
    carries more than one attestation whenever a round is re-drawn without the
    work changing — `score_reviews.latest_phase_verdicts` exists precisely
    because "a phase was re-run at the same commit" — and a last-write-wins map
    fed from `git log` (which is NEWEST-first) handed its reader the OLDEST
    stamp. Driven: two honest rounds at one governing tree, stamped `rounds=1`
    then `rounds=2`, made the merge slot report the evidence and the attestation
    as disagreeing and park an approved lane at a supervisor stop — the OI-76
    failure mode, re-created by the cross-check meant to prevent it (REVIEW-A
    round 007, finding 1). The order of a git history is not this module's to
    own, so the shape that let a superseded stamp arrive SILENTLY is gone rather
    than guarded.

    VERIFIED means the trailer names the GOVERNING identity of the commit that
    CARRIES it — the `Bar-Green` verification applied to a verdict, through the
    one rev rule rather than beside it. The record commit only touches record
    paths, so the tree it governs IS the reviewed tree, and a trailer amended
    onto a commit that changed the work names a tree that is not its carrier's.
    Verifying with the raw fold instead would reject every honest attestation on
    a refreshed branch, because the writer must stamp the value the READERS key
    on and that value is the peeled one.

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
    # `git log` is newest-first; reversed() makes each list oldest-first, which
    # is the order a reader means by "the latest attestation".
    for record in reversed(log.split("\x1e")):
        sha, _sep, message = record.partition("\x1f")
        sha = sha.strip()
        if not sha:
            continue
        parsed = parse_trailer(message)
        if parsed is None:
            continue
        word, rounds, tree = parsed
        if governing_identity(root, branch, sha) != tree:
            continue  # the words rode onto a tree they do not describe
        by_tree.setdefault(tree, []).append((word, rounds))
    return by_tree
