#!/usr/bin/env python3
"""The commit bar's RESYNC entry check: a shipped kit change carries its entry.

A change, from its trunk base to the working tree (untracked files included),
that touches a file the kit ships must add at least one `RESYNC_PACK.md` §3/§4
entry, and every heading it adds must be a real entry anchored `[since <sha>]`
at that base. Otherwise this exits 1 and names each shipped path and each added
heading with its reason. An edit to an existing entry adds none: the count is
the added headings that are entries, less the base's entry headings the working
tree no longer holds verbatim, so a re-anchored or retitled entry counts zero.

"Shipped" has one home, the kit's own delivery inventory: a path under
`project-trajectory/` ships unless the inventory excludes it, a generator
source ships even when excluded, and a path the inventory never saw ships
(deny by default). Each side is classified by that side's own inventory code,
so a file that stops shipping still owes an entry.

It never passes on an input it cannot read: an unresolvable base, an absent or
unreadable pack on either side, or an inventory that cannot be computed each
refuse with the reason. Whether an entry says enough stays with review.

Usage:
  python scripts/check_resync.py [--root <repo>]

Stdlib-only, cross-platform (a meta-repo dev tool, like check_smoke_budget.py).
"""

import argparse
import io
import json
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "project-trajectory/scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from agent_common import default_base  # noqa: E402
from check_changed import changed_paths  # noqa: E402
from kitlib.config import utf8_console  # noqa: E402

KIT_PREFIX = "project-trajectory/"
PACK = KIT_PREFIX + "RESYNC_PACK.md"
SECTION_START = "\n## 3. What changed over time"
SECTION_END = "\n## 5. Promotion"
NO_ENTRY = "no RESYNC_PACK.md entry added for this change"

# The entry grammar. A heading that carries its anchor is checkable with a
# regex and liftable into a registry row without re-reading the prose under it.
# `pre-<sha>` is the escape for a change whose landing commit predates the
# earliest recoverable history; it never counts as a new change's entry.
ENTRY_RE = re.compile(r"^### (?P<title>.+) \[since (?P<sha>(?:pre-)?[0-9a-f]{7,40})\]$")
# The one anchor-free heading shape the entry sections admit while drafting;
# it is not an entry, and the pack's shape tests hold it at zero in a commit.
RESERVED_PREFIX = "### Reserved:"

# Run inside the classified tree's own interpreter process, so that tree's
# `bootstrap.delivery_inventory` reads that tree's files.
SNIPPET = """
import json, sys
sys.path.insert(0, sys.argv[1])
import bootstrap
sources, exclusions, _conditional, generated = bootstrap.delivery_inventory()
print(json.dumps({
    "present": sorted(sources),
    "excluded": sorted(exclusions),
    "generators": sorted({source for source, _dst in generated}),
}))
"""


class Refused(Exception):
    """An input the check cannot read: `subject` names it, `reason` says why."""

    def __init__(self, subject, reason):
        super().__init__(reason)
        self.subject = subject
        self.reason = reason


class Kit(NamedTuple):
    """One tree's delivery classes, in repo-relative paths for `present`."""

    present: frozenset
    excluded: frozenset
    generators: frozenset

    def ships(self, path):
        if not path.startswith(KIT_PREFIX):
            return False
        rel = path[len(KIT_PREFIX) :]
        return rel in self.generators or rel not in self.excluded


EMPTY_KIT = Kit(frozenset(), frozenset(), frozenset())


def entry_headings(text):
    """The `### ` lines of §3 and §4; a missing section marker is unreadable."""
    if SECTION_START not in text or SECTION_END not in text:
        raise ValueError("the pack lacks its §3 or §5 section heading")
    body = text.split(SECTION_START, 1)[1].split(SECTION_END, 1)[0]
    return [line for line in body.splitlines() if line.startswith("### ")]


def kit_classes(kit_dir):
    """Classify `kit_dir` with the inventory code that tree itself carries."""
    proc = subprocess.run(
        [sys.executable, "-I", "-B", "-c", SNIPPET, str(Path(kit_dir) / "scripts")],
        cwd=str(kit_dir),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    try:
        if proc.returncode != 0:
            tail = proc.stderr.strip().splitlines()
            raise ValueError(tail[-1] if tail else "exit {}".format(proc.returncode))
        data = json.loads(proc.stdout)
        return Kit(
            frozenset(KIT_PREFIX + p for p in data["present"]),
            frozenset(data["excluded"]),
            frozenset(data["generators"]),
        )
    except (ValueError, KeyError, TypeError) as exc:
        raise Refused(
            "inventory", "the delivery inventory cannot be computed: {}".format(exc)
        )


def _git(root, *args):
    return subprocess.run(
        ["git", *args], cwd=str(root), capture_output=True, check=True
    ).stdout


def base_kit(root, base):
    """The base's `project-trajectory/` tree, classified by its own inventory."""
    try:
        archive = _git(root, "archive", "--format=tar", base, "project-trajectory")
    except (OSError, subprocess.CalledProcessError) as exc:
        raise Refused("inventory", "the base's kit tree cannot be read: {}".format(exc))
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            tar.extractall(tmp, filter="data")
        return kit_classes(Path(tmp) / "project-trajectory")


def _heading_refusal(heading, base_sha, resolve):
    """The reason an added heading is not this change's entry, or None."""
    if heading.startswith(RESERVED_PREFIX):
        return "a reserved placeholder is not an entry"
    match = ENTRY_RE.match(heading)
    if not match:
        return "outside the entry grammar `### <title> [since <sha>]`"
    sha = match.group("sha")
    if sha.startswith("pre-"):
        return "a `pre-` anchor cannot be a new change's entry"
    if resolve(sha) != base_sha:
        return "anchored at {}, not at the change's base {}".format(sha, base_sha)
    return None


def _judged_paths(changed, shipped_base, shipped_head, present_base, present_head):
    """The kit paths this change owes an entry for."""
    seen = present_base | present_head
    judged = {
        path
        for path in changed
        if path in shipped_base
        or path in shipped_head
        or (path.startswith(KIT_PREFIX) and path not in seen)
    }
    both = present_base & present_head
    judged |= {p for p in both if (p in shipped_base) != (p in shipped_head)}
    return sorted(judged)


def judge(
    changed,
    shipped_base,
    shipped_head,
    present_base,
    present_head,
    base_headings,
    head_headings,
    base_sha,
    resolve,
):
    """The pure verdict: a list of `(subject, reason)` refusals, empty to pass.

    Every heading the change adds is judged, whether or not anything shipped.
    Each base entry heading the working tree no longer holds verbatim cancels
    one counted entry, so an edited heading (re-anchored or retitled) adds
    none; losing one is never refused on its own.
    `resolve(sha)` returns the full commit a short anchor names, or None.
    """
    before, after = set(base_headings), set(head_headings)
    added = [h for h in dict.fromkeys(head_headings) if h not in before]
    refusals = []
    entries = -sum(1 for h in before - after if ENTRY_RE.match(h))
    for heading in added:
        reason = _heading_refusal(heading, base_sha, resolve)
        if reason:
            refusals.append((heading, reason))
        else:
            entries += 1
    judged = _judged_paths(
        changed, shipped_base, shipped_head, present_base, present_head
    )
    if judged and entries < 1:
        refusals.extend((path, NO_ENTRY) for path in judged)
    return refusals


def _resolver(root):
    def resolve(sha):
        try:
            return (
                _git(root, "rev-parse", "--verify", "-q", sha + "^{commit}")
                .decode()
                .strip()
            )
        except (OSError, subprocess.CalledProcessError, UnicodeError):
            return None

    return resolve


def _read_packs(root, base_sha):
    try:
        before = _git(root, "show", base_sha + ":" + PACK).decode("utf-8")
        after = (Path(root) / PACK).read_text(encoding="utf-8")
        return entry_headings(before), entry_headings(after)
    except (OSError, subprocess.CalledProcessError, UnicodeError, ValueError) as exc:
        reason = "the pack is absent or unreadable at the base or in the working tree"
        raise Refused("RESYNC_PACK.md", "{}: {}".format(reason, exc))


def _inputs(root, base):
    """Everything `judge` reads; raises Refused on any input it cannot read."""
    if base is None:
        raise Refused("base", "the change's trunk base is unreadable (claim history)")
    base_sha = _resolver(root)(base)
    if not base_sha:
        raise Refused("base", "the base {} does not resolve to a commit".format(base))
    changed = changed_paths(Path(root), base_sha)
    if changed is None:
        raise Refused("base", "the change from {} cannot be read".format(base_sha))
    base_headings, head_headings = _read_packs(root, base_sha)
    before, after = EMPTY_KIT, EMPTY_KIT
    if any(path.startswith(KIT_PREFIX) for path in changed):
        before = base_kit(root, base_sha)
        after = kit_classes(Path(root) / "project-trajectory")
    return base_sha, changed, before, after, base_headings, head_headings


def run(root, base):
    """`(refusals, summary)`: refusals empty means the change passes."""
    try:
        base_sha, changed, before, after, base_heads, head_heads = _inputs(root, base)
    except Refused as exc:
        return [(exc.subject, exc.reason)], None
    shipped_base = {p for p in before.present if before.ships(p)}
    shipped_head = {p for p in after.present if after.ships(p)}
    refusals = judge(
        changed,
        shipped_base,
        shipped_head,
        set(before.present),
        set(after.present),
        base_heads,
        head_heads,
        base_sha,
        _resolver(root),
    )
    owed = _judged_paths(
        changed, shipped_base, shipped_head, set(before.present), set(after.present)
    )
    if owed:
        summary = "{} shipped path(s) changed; entry anchored at {}".format(
            len(owed), base_sha
        )
    else:
        summary = "no shipped path changed (base {})".format(base_sha)
    return refusals, summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=str(ROOT), help="the repository to judge")
    args = parser.parse_args(argv)
    utf8_console()
    root = Path(args.root).resolve()
    refusals, summary = run(root, default_base(root))
    for subject, reason in refusals:
        print("check_resync: REFUSED {}: {}".format(subject, reason))
    if refusals:
        return 1
    print("check_resync: OK, " + summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
