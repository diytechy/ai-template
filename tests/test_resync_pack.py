"""RESYNC_PACK.md — the LLM re-sync pack's structural contract (OI-27).

WHY THESE TESTS EXIST. The ruling (owner, 2026-08-13) picked option (e), the
prose pack, over (c), a detector-carrying migration registry — but named (c) as
the promotion target and made ONE discipline non-negotiable: **every entry is
SHA-anchored**, naming the kit commit range it applies to. That anchor is what
keeps an LLM's applicability selection sharp (stamp-to-target range picks the
entries that apply) and what makes the later promotion a mechanical LIFT of
entries into rows rather than a re-derivation.

Prose cannot enforce that on itself, and the brief's own evidence says what
happens to unenforced re-sync prose here: the `downstream-resync` skill's copied
recipe drifted within WEEKS, at zero re-sync traffic, caught only by an audit. So
the anchoring discipline gets a grammar the entry format is BUILT for
(`### <title> [since <sha>]`), a check that every anchor names a commit that
really exists, and a one-home pin over the two surfaces that used to carry the
same recipes.

WHAT IS DELIBERATELY NOT TESTED: whether an entry's PROSE is correct. That is
what `tests/test_old_kit_resync.py` measures end to end for the procedure, and
what a reviewer reads for the rest. These tests hold the SHAPE.
"""

import re
import subprocess

from conftest import KIT, ROOT, load_script, skip_without_env_gates

PACK = KIT / "RESYNC_PACK.md"

# The entry grammar, and the whole reason the format looks like this: a heading
# that carries its anchor is checkable with a regex and liftable into a registry
# row without re-reading the prose under it. `pre-<sha>` is the honest escape for
# a change whose landing commit predates the earliest recoverable history.
ENTRY_RE = re.compile(r"^### (?P<title>.+) \[since (?P<sha>(?:pre-)?[0-9a-f]{7,40})\]$")
# A change that has NOT LANDED has no SHA, and inventing one would defeat the
# whole discipline — so a reserved placeholder is the one anchor-free heading
# shape the entry sections admit. It is a DRAFTING state only: the anchor check
# below skips it (an unanchored reservation is a backlog finding, not a grammar
# one) and `test_no_reserved_placeholder_survives_a_commit` then holds the
# backlog at zero, so the exemption cannot become a hiding place.
RESERVED_PREFIX = "### Reserved:"


def _pack_text():
    return PACK.read_text(encoding="utf-8")


def _split(text, start, end=None):
    body = text.split(start, 1)[1]
    return body.split(end, 1)[0] if end else body


def _entry_sections():
    """(§3 what-changed, §4 translation-helper) bodies — the two anchored parts."""
    text = _pack_text()
    changed = _split(
        text, "\n## 3. What changed over time", "\n## 4. Translation helper"
    )
    renames = _split(text, "\n## 4. Translation helper", "\n## 5. Promotion")
    return changed, renames


def _headings(body):
    return [ln for ln in body.splitlines() if ln.startswith("### ")]


def _anchors(body):
    return [m.group("sha") for m in (ENTRY_RE.match(h) for h in _headings(body)) if m]


def test_the_pack_ships_inside_the_portable_unit():
    """Adoption IS copying `project-trajectory/`, so the pack has to live there.

    It is deliberately NOT a bootstrap MAPPING destination (see the next test),
    which makes membership in the copied kit tree the ONLY thing that gets it to
    an adopter — including the tarball adopter, whose `docs/kit-version` reads
    `unknown` and who therefore needs the pack more than anyone.
    """
    assert PACK.is_file(), "the kit must ship RESYNC_PACK.md"
    text = _pack_text()
    for section in (
        "\n## 1. The procedure",
        "\n## 2. The file-by-file deviation review",
        "\n## 3. What changed over time",
        "\n## 4. Translation helper",
        "\n## 5. Promotion",
    ):
        assert section in text, "the pack is missing its section: " + section.strip()


def test_the_pack_is_not_scaffolded_and_that_is_the_ruling():
    """The pack is a kit REFERENCE doc, like ADOPTING.md — not copied into repos.

    Recorded as a test rather than a comment because the tempting change is to
    "helpfully" add a MAPPING row. A copy scaffolded into an adopting repo is
    frozen at that repo's adoption commit, so it is missing exactly the entries
    that repo needs on the day it re-syncs — a stale re-sync doc is worse than
    none, and it would also re-create the second home OI-27's ruling exists to
    kill. The pack is read from the kit checkout being synced TO; the README kit
    contents row and the pack's own header both say so.
    """
    bootstrap = load_script("bootstrap")
    srcs = {src for src, _ in bootstrap.MAPPING}
    assert "RESYNC_PACK.md" not in srcs, (
        "RESYNC_PACK.md became a scaffold destination — a copy frozen at the "
        "adopter's adoption commit cannot carry the entries added since, which "
        "is precisely the range a re-sync reads"
    )
    readme = (KIT / "README.md").read_text(encoding="utf-8")
    assert "`RESYNC_PACK.md`" in readme, "the kit contents table must list the pack"
    assert re.search(r"`RESYNC_PACK\.md`.*not scaffolded", readme), (
        "the kit contents row must state the not-scaffolded decision"
    )


def test_every_entry_carries_a_sha_anchor():
    """The non-negotiable discipline, as a grammar over the entry headings."""
    changed, renames = _entry_sections()
    unanchored = []
    for body, label in ((changed, "§3"), (renames, "§4")):
        for h in _headings(body):
            if h.startswith(RESERVED_PREFIX):
                continue
            if not ENTRY_RE.match(h):
                unanchored.append(label + " " + h)
    assert not unanchored, (
        "pack entries without a `[since <sha>]` anchor — the anchor is what "
        "selects the entry for a stamp-to-target range and what makes the "
        "promotion to a migration registry a lift rather than a re-derivation:\n"
        + "\n".join(unanchored)
    )
    # ...and there is a real body of entries, so the grammar is not vacuously true.
    assert len(_anchors(changed)) >= 40, "the what-changed narrative lost entries"
    assert len(_anchors(renames)) >= 8, "the translation helper lost entries"


def test_no_reserved_placeholder_survives_a_commit():
    """The Reserved backlog is held at ZERO, not merely kept anchor-free.

    This test used to say only "a `Reserved:` heading must not carry a SHA" and
    exempted those headings from the anchor check above — which made the ONE
    unanchored shape the pack admits also the one shape nothing counted. It ran
    0 → 3 in a single day before a review caught it, and every one of those three
    entries was invisible to a re-sync: an entry with no anchor falls in no
    stamp-to-target range, so an adopter does not skip it loudly, they never see
    it. A silent backlog is the worst failure this document has, because the
    document's whole value is being complete for the range you read.

    So the rule is now the strong one: **a Reserved heading may exist while you
    are drafting, and must not exist in a commit.** The escape hatch that makes
    that always satisfiable — and the reason a bounded-and-listed backlog was not
    worth the machinery — is the pack's own long-standing convention, stated in
    §3's preamble and used by four entries: a change whose landing SHA is not
    knowable yet anchors at the PRECEDING commit and says so in a parenthetical.
    That anchor resolves, selects a range one commit wide of correct, and needs no
    follow-up commit to become true. Deliberately reserving a slot anyway means
    editing this assertion, which is the point: it becomes an act with a reviewer.

    Both halves are asserted, so the shape rule still bites if the emptiness rule
    is ever relaxed back to a bound.
    """
    changed, renames = _entry_sections()
    reserved = [
        h
        for body in (changed, renames)
        for h in _headings(body)
        if h.startswith(RESERVED_PREFIX)
    ]
    for h in reserved:
        assert not ENTRY_RE.match(h), (
            "a reserved (not-yet-landed) heading carries a SHA anchor, which "
            "cannot be a real commit: " + h
        )
    assert not reserved, (
        "the pack carries reserved (unanchored) entries, which no re-sync range "
        "can select — anchor each at the preceding commit with the parenthetical "
        "§3 describes, or delete it:\n" + "\n".join(reserved)
    )


def test_no_entry_hides_below_the_closing_section():
    """Entries live in §3/§4; an append past §5 is outside every check AND reader.

    Sibling defect to the reserved backlog, found in the same review and just as
    silent: three entries had been appended after "## 5. Promotion", where the
    anchor grammar, the landing-order rule and the §1.3 worklist an operator
    actually reads all stop looking. They were well-formed and unreachable. §5 is
    the pack's closing argument, so the check is simply that nothing follows it.
    """
    tail = _split(_pack_text(), "\n## 5. Promotion")
    stragglers = _headings(tail)
    assert not stragglers, (
        "entry heading(s) below §5 — an entry there is read by no operator and "
        "checked by no grammar; move them into §3 in landing order:\n"
        + "\n".join(stragglers)
    )


def test_bite_the_grammar_rejects_a_planted_unanchored_entry():
    """Bite-proof both directions on synthetic headings, so the check cannot be
    passing because the regex matches everything."""
    assert ENTRY_RE.match("### A change [since 704ffd0d]")
    assert ENTRY_RE.match("### A very old change [since pre-7762bc7f]")
    assert not ENTRY_RE.match("### A change (2026-08)")
    assert not ENTRY_RE.match("### A change [since WI-426]")
    assert not ENTRY_RE.match("### A change [since 704ffd0d] and more")


def test_every_anchor_names_a_commit_that_really_exists():
    """An anchor is only worth its line if it resolves. One batched git call.

    Skips (never fails) where the history is unreachable — a shallow CI clone or
    a source export is an ENVIRONMENT fact, the same verdict
    `test_old_kit_resync.py` reaches for the same reason.
    """
    skip_without_env_gates("git")
    changed, renames = _entry_sections()
    shas = [
        s for s in _anchors(changed) + _anchors(renames) if not s.startswith("pre-")
    ]
    assert shas
    probe = subprocess.run(
        ["git", "cat-file", "--batch-check"],
        cwd=str(ROOT),
        input="\n".join(s + "^{commit}" for s in shas) + "\n",
        capture_output=True,
        text=True,
    )
    if probe.returncode != 0:
        import pytest

        pytest.skip("git cat-file unavailable: " + probe.stderr.strip())
    missing = [
        sha
        for sha, line in zip(shas, probe.stdout.splitlines())
        if "commit" not in line.split()
    ]
    if missing and len(probe.stdout.splitlines()) == len(shas):
        # A shallow clone reports every SHA missing; that is the environment, not
        # a defect in the pack. Only a PARTIAL miss is a real finding.
        if len(missing) == len(shas):
            import pytest

            pytest.skip("no pack anchor resolves — shallow clone or source export")
    assert not missing, (
        "pack entry anchor(s) name no commit in this repo's history — an anchor "
        "that does not resolve selects nothing: " + ", ".join(missing)
    )


def test_the_what_changed_entries_are_in_landing_order():
    """Oldest first, because that is the order a re-sync APPLIES them in.

    §1.3 tells the operator to work the applicable entries oldest first (a later
    entry may supersede an earlier one), so the document order has to BE that
    order — otherwise the instruction and the page disagree.
    """
    skip_without_env_gates("git")
    changed, _ = _entry_sections()
    shas = [s for s in _anchors(changed) if not s.startswith("pre-")]
    dates = []
    for sha in shas:
        p = subprocess.run(
            ["git", "log", "-1", "--format=%ad", "--date=short", sha],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        if p.returncode != 0:
            import pytest

            pytest.skip("history unreachable for " + sha)
        dates.append((p.stdout.strip(), sha))
    out_of_order = [
        (dates[i - 1], dates[i])
        for i in range(1, len(dates))
        if dates[i][0] < dates[i - 1][0]
    ]
    assert not out_of_order, (
        "§3 entries are not in landing order (oldest first): " + str(out_of_order)
    )


def test_the_promotion_trigger_is_recorded_with_both_halves():
    """The ruled trigger is a DECISION, not a vibe — both halves stay written."""
    text = _split(_pack_text(), "\n## 5. Promotion")
    # Unwrap: markdown hard-wraps at 80 columns, so a two-word phrase can land
    # across a newline. The assertions are about the WORDS, not the line breaks.
    low = re.sub(r"[\s*]+", " ", text.lower())
    assert "out-of-sphere adopter" in low
    assert "second observed drift incident" in low
    assert "migration registry" in low and "detect" in low, (
        "§5 must name what promotion promotes TO (registry rows with per-entry "
        "detect probes), or the trigger fires into nothing"
    )


def test_adopting_section_6_points_at_the_pack_and_carries_no_recipes():
    """ONE HOME, pinned from the other side (the spirit of the skill's pin).

    §6 keeps the procedure-level FRAMING and points; the recipe content lives in
    the pack. The pin is shaped as "no recipe-shaped content", using the two
    forms the recipes actually take: a `[since <sha>]` anchor (the pack's entry
    key) and the old dated/WI-keyed recipe bullet headers §6 used before the
    move.
    """
    text = (KIT / "ADOPTING.md").read_text(encoding="utf-8")
    section6 = _split(text, "\n## 6. Re-syncing", "\n## 7. Standards crosswalk")
    assert "RESYNC_PACK.md" in section6, "§6 must point at the pack"

    anchors = sorted(set(re.findall(r"\[since [0-9a-f]{7,40}\]", section6)))
    assert not anchors, (
        "ADOPTING §6 carries pack entry anchors ({}) — the entries have one "
        "home".format(", ".join(anchors))
    )
    assert "Migration recipes for specific kit changes" not in section6, (
        "§6's recipe list came back; it moved to RESYNC_PACK.md §3"
    )
    strays = sorted(set(re.findall(r"\bWI-\d+\b", section6)))
    assert not strays, (
        "ADOPTING §6 names work items ({}) — that is the recipe-keying form the "
        "content moved to the pack under".format(", ".join(strays))
    )


def test_the_pack_states_which_copy_to_read():
    """The stale-copy trap, stated where the reader is standing.

    Two checkouts are open during a re-sync — the adopter's repo and the kit
    being synced to. Only the second carries the entries added since adoption, so
    the pack says so in its own header rather than trusting the reader to infer
    it from the not-scaffolded decision.
    """
    header = _pack_text().split("\n## 1. The procedure", 1)[0]
    assert "not** scaffolded" in header or "not scaffolded" in header
    assert (
        "syncing TO" in header or "syncing **TO**" in header or "kit checkout" in header
    )
