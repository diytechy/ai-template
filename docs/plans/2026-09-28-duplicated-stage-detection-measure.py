"""Duplicated-stage detection: the measurement behind the 2026-09-28 write-up.

A research prototype, not a kit script: it lives beside the write-up that cites
it, outside project-trajectory/scripts/ and tests/, so no gate, hook or commit
bar ever runs it. Stdlib only.

    python docs/plans/2026-09-28-duplicated-stage-detection-measure.py --show-truth --sample 12

About 12 minutes on a 4-core box; `--only code|head|queue` runs one half.

For each code consolidation named in CODE_TRUTH it checks out the consolidation
commit's PARENT in a detached worktree (removed afterwards), reads the ground
truth from the consolidation's own diff, runs every method over
project-trajectory/scripts/ and tests/, and prints recall and report volume.
It then prints the same volume at HEAD, a seeded sample of each method's HEAD
findings for hand judgement, and the queue half (near-miss text similarity
over work-item specs against the repository's queue consolidations).
"""

import argparse
import ast
import builtins
import hashlib
import io
import itertools
import keyword
import pathlib
import random
import re
import shutil
import subprocess
import sys
import tempfile
import tokenize
from pathlib import Path

SCOPES = ("project-trajectory/scripts", "tests")

# The consolidation commits the ground truth is read from: each one's message
# names it as extracting a stage two or more functions carried (the 0->A->B
# rule), and its parent is where the copies still stood.
CODE_TRUTH = [
    ("3b7ae3fd", "WI-346: one spine loader and one capture helper in gen_trajectory"),
    ("8fc5f813", "WI-345: the verdict plumbing two arms carried, one of them diverged"),
    ("ac348ac6", "WI-347: five one-off duplications extracted, not sanctioned"),
    ("a3373b94", "WI-465: git-initing fixtures pin core.autocrlf through one helper"),
    ("46de9442", "WI-448 slice 1: the duplicated helpers into kitlib"),
    ("87bd45dd", "WI-498: the stage ladder gets one home in kitlib"),
    ("2eae651e", "WI-448 slice 2: 33 _utf8_console copies"),
    ("0f3b4eca", "WI-448 slice 3: the spine row vocabulary"),
    ("23890e5d", "WI-448 slice 4: the residual duplicate groups"),
    ("fe6173d3", "WI-448 slice 5: schema of record and the TOML emitter"),
    ("e1c01f2b", "WI-520: one home for the credential class vocabulary"),
    ("dd7bc7fd", "WI-583 round 3: Done-when had three readers and two rules"),
    ("9ecb934f", "WI-657 parts 1-3: the ratchet back to green"),
]

# --------------------------------------------------------------------------
# Function inventory


def _stripped(body):
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        return body[1:]
    return body


class Func:
    __slots__ = ("key", "node", "src", "lines")

    def __init__(self, key, node, src):
        self.key = key
        self.node = node
        self.src = src
        self.lines = node.end_lineno - node.lineno + 1


def inventory(root):
    """{(relpath, qualname): Func} over SCOPES; unparsable files skipped."""
    out = {}
    for scope in SCOPES:
        base = Path(root) / scope
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            rel = path.relative_to(root).as_posix()
            try:
                text = path.read_text(encoding="utf-8")
                tree = ast.parse(text)
            except (SyntaxError, UnicodeDecodeError, ValueError):
                continue
            lines = text.splitlines()
            _walk(tree, [], rel, lines, out)
    return out


def _walk(node, stack, rel, lines, out):
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            q = ".".join(stack + [child.name])
            src = "\n".join(lines[child.lineno - 1 : child.end_lineno])
            out[(rel, q)] = Func((rel, q), child, src)
            _walk(child, stack + [child.name], rel, lines, out)
        elif isinstance(child, ast.ClassDef):
            _walk(child, stack + [child.name], rel, lines, out)
        else:
            _walk(child, stack, rel, lines, out)


# --------------------------------------------------------------------------
# Methods. Each returns a set of frozenset({key_a, key_b}) pairs.


def m0_census(funcs):
    """Today's census: identical docstring-stripped body AST, >= 4 lines."""
    groups = {}
    for f in funcs.values():
        body = _stripped(f.node.body)
        if not body or f.lines < 4:
            continue
        h = hashlib.sha1("\n".join(ast.dump(n) for n in body).encode()).hexdigest()
        groups.setdefault(h, []).append(f.key)
    return _pairs_from_groups(groups.values())


def _pairs_from_groups(groups, cap=None):
    pairs = set()
    for g in groups:
        g = sorted(set(g))
        if len(g) < 2 or (cap and len(g) > cap):
            continue
        for a, b in itertools.combinations(g, 2):
            if not _nested(a, b):
                pairs.add(frozenset((a, b)))
    return pairs


def _nested(a, b):
    """One function defined inside the other: the outer function's source
    holds the inner's, so a text method would pair them with themselves."""
    if a[0] != b[0]:
        return False
    return a[1].startswith(b[1] + ".") or b[1].startswith(a[1] + ".")


def _callee(func):
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


class _Calls(ast.NodeVisitor):
    """Callee names in evaluation order (arguments before the call they feed),
    not descending into nested functions, lambdas or classes."""

    def __init__(self):
        self.seq = []

    def visit_Call(self, node):
        self.generic_visit(node)
        name = _callee(node.func)
        if name:
            self.seq.append(name)

    def visit_FunctionDef(self, node):
        pass

    visit_AsyncFunctionDef = visit_FunctionDef
    visit_Lambda = visit_FunctionDef
    visit_ClassDef = visit_FunctionDef


def call_sequence(f):
    v = _Calls()
    for stmt in _stripped(f.node.body):
        v.visit(stmt)
    return v.seq


def m1_callseq(funcs, k, cap=None):
    """Call-sequence fingerprints: two functions share a stage when their
    ordered callee sequences share a contiguous run of k calls. `cap` drops a
    run shared by more than `cap` functions (an idiom, by frequency)."""
    return _shared_runs({f.key: call_sequence(f) for f in funcs.values()}, k, cap)


def _shared_runs(streams, n, cap):
    """Pairs of functions whose streams share a run of n items, plus a
    self-pair frozenset({key}) for a function whose own stream repeats a run
    at two non-overlapping places (two arms of one function carrying one
    stage). A run held by more than `cap` functions is dropped as an idiom."""
    index = {}
    repeats = {}
    for key, seq in streams.items():
        first = {}
        for i in range(len(seq) - n + 1):
            run = hash(tuple(seq[i : i + n]))
            index.setdefault(run, set()).add(key)
            if run in first and i - first[run] >= n:
                repeats.setdefault(run, set()).add(key)
            first.setdefault(run, i)
    pairs = _pairs_from_groups(index.values(), cap)
    for run, keys in repeats.items():
        if cap and len(index[run]) > cap:
            continue
        pairs.update(frozenset((key,)) for key in keys)
    return pairs


# Names a project function may share with the standard library's builtins and
# common types; a callee spelled like one of these is not counted as the
# project's own operation even when the project also defines it.
_STDLIB_NAMES = set(dir(builtins)).union(
    dir(str),
    dir(list),
    dir(dict),
    dir(set),
    dir(pathlib.Path),
    dir(argparse.ArgumentParser),
)


def _local_names(funcs):
    return {
        q for (rel, q) in funcs if rel.startswith(SCOPES[0]) and "." not in q
    } - _STDLIB_NAMES


def m1_local(funcs, k, cap=None):
    """Call-sequence fingerprints over the project's OWN operations only: a
    callee counts when it is the name of a module-level function in the
    scanned product tree and not also a builtin or a str/list/dict/set/Path/
    ArgumentParser method name, so the plumbing every script shares drops out
    of the sequence before runs are matched."""
    local = _local_names(funcs)
    streams = {
        f.key: [c for c in call_sequence(f) if c in local] for f in funcs.values()
    }
    return _shared_runs(streams, k, cap)


def norm_tokens(f):
    """Type-2 normalized token stream: identifiers -> ID, literals -> LIT,
    keywords and operators kept; comments and layout dropped; the docstring
    dropped, and so are nested functions and classes: they are functions of
    their own, and leaving their text in the parent pairs the parent with
    them and with itself."""
    body = _stripped(f.node.body)
    if not body:
        return []
    lines = f.src.splitlines()
    for stmt in body:
        for n in ast.walk(stmt):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start = min([n.lineno] + [d.lineno for d in n.decorator_list])
                for i in range(start - f.node.lineno, n.end_lineno - f.node.lineno + 1):
                    lines[i] = ""
    first = body[0].lineno - f.node.lineno
    src = _dedent("\n".join(lines[first:]))
    out = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            t = tok.type
            if t == tokenize.NAME:
                out.append(tok.string if keyword.iskeyword(tok.string) else "ID")
            elif t in (tokenize.NUMBER, tokenize.STRING):
                out.append("LIT")
            elif t == tokenize.OP:
                out.append(tok.string)
            elif t in (tokenize.INDENT, tokenize.DEDENT):
                out.append(tokenize.tok_name[t])
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass
    return out


def _dedent(src):
    lines = src.splitlines()
    widths = [len(ln) - len(ln.lstrip()) for ln in lines if ln.strip()]
    cut = min(widths) if widths else 0
    return "\n".join(ln[cut:] for ln in lines) + "\n"


def m2_window(funcs, w, cap=None, tokens=None):
    """Near-miss fragments: two functions share a normalized token window of
    w tokens (a renamed or re-literalled copy of one stage still matches)."""
    return _shared_runs({key: tokens[key] for key in funcs}, w, cap)


def m2_jaccard(funcs, threshold, shingle=8, min_tokens=40, tokens=None):
    """Near-miss whole functions: Jaccard similarity of normalized 8-token
    shingles at or above `threshold`."""
    sh = {}
    for f in funcs.values():
        toks = tokens[f.key]
        if len(toks) < min_tokens:
            continue
        sh[f.key] = {
            hash(tuple(toks[i : i + shingle])) for i in range(len(toks) - shingle + 1)
        }
    inverted = {}
    for key, s in sh.items():
        for x in s:
            inverted.setdefault(x, []).append(key)
    cand = {}
    for keys in inverted.values():
        if len(keys) > 200:
            continue
        for a, b in itertools.combinations(sorted(keys), 2):
            cand[(a, b)] = cand.get((a, b), 0) + 1
    pairs = set()
    for (a, b), inter in cand.items():
        union = len(sh[a]) + len(sh[b]) - inter
        if union and inter / union >= threshold and not _nested(a, b):
            pairs.add(frozenset((a, b)))
    return pairs


def methods(funcs):
    toks = {k: norm_tokens(f) for k, f in funcs.items()}
    return {
        "M0": m0_census(funcs),
        "M1-k3": m1_callseq(funcs, 3),
        "M1-k4": m1_callseq(funcs, 4),
        "M1-k4-cap5": m1_callseq(funcs, 4, cap=5),
        "M1-k6": m1_callseq(funcs, 6),
        "M1L-k2-cap5": m1_local(funcs, 2, cap=5),
        "M1L-k3": m1_local(funcs, 3),
        "M2-w30": m2_window(funcs, 30, tokens=toks),
        "M2-w50": m2_window(funcs, 50, tokens=toks),
        "M2-w50-cap5": m2_window(funcs, 50, cap=5, tokens=toks),
        "M2-j0.5": m2_jaccard(funcs, 0.5, tokens=toks),
        "M2-j0.7": m2_jaccard(funcs, 0.7, tokens=toks),
    }


# --------------------------------------------------------------------------
# Ground truth from a consolidation commit's own diff


def _names_in(node):
    names = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Name):
            names.add(n.id)
        elif isinstance(n, ast.Attribute):
            names.add(n.attr)
    return names


def _import_bindings(root, rel):
    """{bound name: source name} for every `from x import a as b` / `b = x.a`
    at module level in the file."""
    p = Path(root) / rel
    try:
        tree = ast.parse(p.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, UnicodeDecodeError, ValueError):
        return {}
    out = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom):
            for a in n.names:
                out[a.asname or a.name] = a.name
        elif isinstance(n, ast.Assign) and isinstance(n.value, ast.Attribute):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    out[t.id] = n.value.attr
    return out


def _changed_files(repo, parent, commit):
    out = subprocess.run(
        ["git", "diff", "--name-only", parent, commit],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return {ln.strip() for ln in out.splitlines() if ln.strip().endswith(".py")}


def ground_truth(repo, before_root, after_root, parent, commit):
    """{home name: set of copy keys at the parent}.

    A function at the parent is a COPY of a home when the consolidation commit
    either deletes it and binds its name to an import of the home (the
    re-export form every WI-448 slice used), or keeps it but removes at least
    two of its lines and makes it newly reference a function the commit added.
    """
    before = inventory(before_root)
    after = inventory(after_root)
    changed = _changed_files(repo, parent, commit)
    new_names = {k[1].split(".")[-1] for k in after if k not in before}
    after_names = {k[1].split(".")[-1] for k in after}
    homes = {}
    for key, f in before.items():
        rel, q = key
        if rel not in changed:
            continue
        bare = q.split(".")[-1]
        if key not in after:
            if "." in q:
                continue
            bound = _import_bindings(after_root, rel).get(bare)
            if bound and bound in after_names:
                homes.setdefault(bound, set()).add(key)
            continue
        g = after[key]
        removed = f.lines - g.lines
        if removed < 2:
            continue
        fresh = (_names_in(g.node) - _names_in(f.node)) & new_names
        uses = _name_uses(g.node)
        for name in fresh:
            homes.setdefault(name, set()).add(key)
            if uses.get(name, 0) >= 2:
                # Two arms of this one function now call the home: an
                # intra-function instance of its own.
                homes.setdefault("{} (arms of {})".format(name, q), set()).add(key)
    return {h: keys for h, keys in homes.items() if len(keys) >= 2 or " (arms of " in h}


def _name_uses(node):
    counts = {}
    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            name = _callee(n.func)
            if name:
                counts[name] = counts.get(name, 0) + 1
    return counts


# --------------------------------------------------------------------------
# Worktrees


class Worktree:
    def __init__(self, repo, rev):
        self.repo = repo
        self.rev = rev
        self.path = Path(tempfile.mkdtemp(prefix="dupstage-")) / "wt"

    def __enter__(self):
        subprocess.run(
            ["git", "worktree", "add", "--detach", str(self.path), self.rev],
            cwd=self.repo,
            capture_output=True,
            check=True,
        )
        return self.path

    def __exit__(self, *exc):
        subprocess.run(
            ["git", "worktree", "remove", "--force", str(self.path)],
            cwd=self.repo,
            capture_output=True,
        )
        shutil.rmtree(self.path.parent, ignore_errors=True)
        return False


def rev_parse(repo, rev):
    return subprocess.run(
        ["git", "rev-parse", "--short=8", rev],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


# --------------------------------------------------------------------------
# Scoring


def score(instance, pairs):
    """(recalled?, copies linked to another copy of the same instance). An
    instance of one function is two arms inside it: recalled by a self-pair."""
    if len(instance) == 1:
        hit = frozenset(instance) in pairs
        return hit, len(instance) if hit else 0
    linked = set()
    for a, b in itertools.combinations(sorted(instance), 2):
        if frozenset((a, b)) in pairs:
            linked.update((a, b))
    return bool(linked), len(linked)


def run_code(repo, show_truth, only=None):
    totals = {}
    print("## Code ground truth and recall\n")
    for commit, label in CODE_TRUTH:
        if only and commit not in only:
            continue
        parent = rev_parse(repo, commit + "^")
        with Worktree(repo, parent) as before, Worktree(repo, commit) as after:
            truth = ground_truth(repo, before, after, parent, commit)
            funcs = inventory(before)
            found = methods(funcs)
        print("### {} (parent {}) {}".format(commit, parent, label))
        print("functions scanned: {}".format(len(funcs)))
        for home, keys in sorted(truth.items()):
            print(
                "  instance {}: {} copies{}".format(
                    home,
                    len(keys),
                    (": " + ", ".join("{}::{}".format(*k) for k in sorted(keys)))
                    if show_truth
                    else "",
                )
            )
        for home, keys in sorted(truth.items()):
            hits = [n for n, p in found.items() if score(keys, p)[0]]
            print("    {} found by: {}".format(home, " ".join(hits) or "none"))
        for name, pairs in found.items():
            t = totals.setdefault(name, [0, 0, 0, 0, 0])
            hit = copies = linked = 0
            for keys in truth.values():
                r, n = score(keys, pairs)
                hit += r
                copies += len(keys)
                linked += n
            t[0] += hit
            t[1] += len(truth)
            t[2] += linked
            t[3] += copies
            t[4] += len(pairs)
            print(
                "  {:12s} instances {}/{}  copies {}/{}  pairs reported {}".format(
                    name, hit, len(truth), linked, copies, len(pairs)
                )
            )
        print()
    print("### Totals over every code instance\n")
    for name, (hit, n, linked, copies, reported) in totals.items():
        print(
            "  {:12s} instances {}/{}  copies {}/{}  pairs reported (sum) {}".format(
                name, hit, n, linked, copies, reported
            )
        )
    print()


def run_head(repo, sample, seed):
    print("## Report volume at HEAD, and a sample for judgement\n")
    funcs = inventory(repo)
    found = methods(funcs)
    print("functions scanned: {}".format(len(funcs)))
    rng = random.Random(seed)
    for name, pairs in found.items():
        src = sum(1 for p in pairs if all(k[0].startswith(SCOPES[0]) for k in p))
        own = sum(1 for p in pairs if len(p) == 1)
        print(
            "  {:12s} pairs {:6d}  both in scripts {:6d}  within one function {:5d}".format(
                name, len(pairs), src, own
            )
        )
    if not sample:
        return
    local = _local_names(funcs)
    for name in JUDGED:
        pairs = [
            sorted(p) for p in found[name] if all(k[0].startswith(SCOPES[0]) for k in p)
        ]
        print(
            "\n### sample of scripts-only pairs: {} ({} such)".format(name, len(pairs))
        )
        chosen = rng.sample(sorted(pairs), min(sample, len(pairs)))
        for pair in chosen:
            a, b = pair[0], pair[-1]
            fa, fb = funcs[a], funcs[b]
            sa, sb = call_sequence(fa), call_sequence(fb)
            if name.startswith("M1L"):
                sa = [c for c in sa if c in local]
                sb = [c for c in sb if c in local]
            run = _longest_common_run(sa, sb)
            print(
                "  {}::{} L{}+{}  <->  {}::{} L{}+{}  | longest shared call run: {}".format(
                    a[0].split("/")[-1],
                    a[1],
                    fa.node.lineno,
                    fa.lines,
                    b[0].split("/")[-1],
                    b[1],
                    fb.node.lineno,
                    fb.lines,
                    " ".join(run) or "-",
                )
            )


# The methods whose HEAD findings are sampled for hand judgement.
JUDGED = (
    "M0",
    "M1-k4-cap5",
    "M1-k6",
    "M2-w50-cap5",
    "M2-j0.7",
    "M2-w30",
    "M1L-k2-cap5",
    "M1L-k3",
)


def _longest_common_run(x, y):
    """The longest contiguous run of callees two call sequences share."""
    best, end = 0, 0
    prev = [0] * (len(y) + 1)
    for i in range(1, len(x) + 1):
        cur = [0] * (len(y) + 1)
        for j in range(1, len(y) + 1):
            if x[i - 1] == y[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best, end = cur[j], i
        prev = cur
    return x[end - best : end]


# --------------------------------------------------------------------------
# The queue half: near-miss text similarity over work-item specs


QUEUE_TRUTH = {
    # 2026-09-27 hand consolidation (docs/log.d/2026-09-27-wave4-consolidation.md)
    "8aae3af3": [
        ["WI-582", "WI-677", "WI-644"],
        ["WI-672", "WI-663", "WI-598", "WI-619"],
        ["WI-656", "WI-670", "WI-626", "WI-658"],
        ["WI-651", "WI-666", "WI-671"],
        [
            "WI-615",
            "WI-609",
            "WI-613",
            "WI-614",
            "WI-556",
            "WI-668",
            "WI-610",
            "WI-536",
        ],
        ["WI-620", "WI-605", "WI-606", "WI-551"],
        ["WI-621", "WI-608", "WI-622"],
        ["WI-616", "WI-617"],
        ["WI-581", "WI-659", "WI-570"],
        ["WI-638", "WI-634"],
        ["WI-657", "WI-539", "WI-623", "WI-624"],
    ],
    # 2026-09-02 restructure (docs/plans/2026-09-02-backlog-restructure-and-consolidation.md §2.2):
    # the absorbed rows each new host drew from; a row split across hosts sits
    # in each group it fed.
    "9de63e78": [
        ["WI-558", "WI-559", "WI-560"],
        ["WI-559", "WI-560", "WI-562"],
        ["WI-561", "WI-562", "WI-560"],
        ["WI-564", "WI-565", "WI-576"],
    ],
}

# The WI-689 census's seven candidates (e26e22aa): the judge absorbed none and
# ordered one pair (WI-655 needs WI-616), so every pair is a judged negative
# for consolidation.
QUEUE_NEGATIVE = (
    "e26e22aa",
    ["WI-615", "WI-616", "WI-620", "WI-651", "WI-655", "WI-657", "WI-667"],
)

_WORD = re.compile(r"[a-z0-9_]+")


def _spec_rows(repo, rev):
    """{WI id: text} for queued and deferred specs at `rev` (read with git show)."""
    out = subprocess.run(
        [
            "git",
            "ls-tree",
            "-r",
            "--name-only",
            rev,
            "docs/work/queued/",
            "docs/work/deferred/",
        ],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    rows = {}
    for path in out:
        m = re.search(r"(WI-\d+)", path)
        if not m or m.group(1) == "WI-000" or not path.endswith(".md"):
            continue
        text = subprocess.run(
            ["git", "show", "{}:{}".format(rev, path)],
            cwd=repo,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        ).stdout
        rows[m.group(1)] = text
    return rows


def _shingles(text, n=3):
    words = _WORD.findall(text.lower())
    return {tuple(words[i : i + n]) for i in range(len(words) - n + 1)}


def _jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


def run_queue(repo):
    print("## Queue half: word-trigram Jaccard over queued specs\n")
    for rev, groups in QUEUE_TRUTH.items():
        rows = _spec_rows(repo, rev)
        sh = {k: _shingles(v) for k, v in rows.items()}
        truth = set()
        for g in groups:
            for a, b in itertools.combinations(sorted(set(g)), 2):
                if a in sh and b in sh:
                    truth.add(frozenset((a, b)))
        sims = sorted(
            (
                (_jaccard(sh[a], sh[b]), frozenset((a, b)))
                for a, b in itertools.combinations(sorted(sh), 2)
            ),
            key=lambda x: -x[0],
        )
        print(
            "### at {}: {} rows, {} pairs, {} ground-truth pairs".format(
                rev, len(sh), len(sims), len(truth)
            )
        )
        for top in (len(truth), 2 * len(truth), 100):
            got = sum(1 for _, p in sims[:top] if p in truth)
            print(
                "  top {:4d} pairs by similarity: {} of {} ground-truth pairs".format(
                    top, got, len(truth)
                )
            )
        for thr in (0.02, 0.04, 0.06, 0.08):
            rep = [p for s, p in sims if s >= thr]
            got = sum(1 for p in rep if p in truth)
            print(
                "  jaccard >= {:.2f}: {} pairs reported, {} ground truth".format(
                    thr, len(rep), got
                )
            )
        print()
    rev, ids = QUEUE_NEGATIVE
    rows = _spec_rows(repo, rev)
    sh = {k: _shingles(v) for k, v in rows.items()}
    print("### WI-689's judged negatives at {}".format(rev))
    for a, b in itertools.combinations(ids, 2):
        if a in sh and b in sh:
            print("  {} {} jaccard {:.3f}".format(a, b, _jaccard(sh[a], sh[b])))
    allsims = sorted(
        (_jaccard(sh[a], sh[b]) for a, b in itertools.combinations(sorted(sh), 2)),
        reverse=True,
    )
    print(
        "  every pair in that queue: max {:.3f}, 90th pct {:.3f}".format(
            allsims[0], allsims[len(allsims) // 10]
        )
    )


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".")
    ap.add_argument("--show-truth", action="store_true")
    ap.add_argument("--sample", type=int, default=0)
    ap.add_argument("--seed", type=int, default=624)
    ap.add_argument("--only", choices=("code", "head", "queue"))
    ap.add_argument("--commit", action="append", help="limit the code half")
    args = ap.parse_args()
    repo = str(Path(args.root).resolve())
    if args.only in (None, "code"):
        run_code(repo, args.show_truth, args.commit)
    if args.only in (None, "head"):
        run_head(repo, args.sample, args.seed)
    if args.only in (None, "queue"):
        run_queue(repo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
