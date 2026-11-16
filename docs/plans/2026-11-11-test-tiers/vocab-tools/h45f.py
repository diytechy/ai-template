"""HANDOFF 10.5 pass 3, fixes found by its test run.

1. The chain renders a row's status lower-cased (`SR-001 [approved]`): the
   status moves in pass 4, so this expectation waits for it.
2. A fixture's work-item file name (`WI-600-approve.md`, from its slug) was
   held by r45c's `*approv*.md` protection, meant for dated record names,
   while the slug moved: the name follows the slug.
3. PROCESS.md:692, "the risk the operator accepts by delegating": plain
   "accept" the renamed gate-authority tripwire (test_gate_policy) now
   catches, and a use a reader could take for the act (4.4's last paragraph).
4. The open-item brief lint (WI-146b) keyed on the word `approv` in pending
   rows' prose; rows are now written with "accept", so the signal and the
   view-link token follow the current word. `ratif` stays (the record
   directory kept its name).
"""

CT = "project-trajectory/scripts/check_trajectory.py"

EDITS = [
    ("tests/test_adjudicate_brief.py", 'assert "SR-001 [accepted]" in chain', 'assert "SR-001 [approved]" in chain'),
    ("tests/test_dispatch.py", '"WI-600-approve.md"', '"WI-600-accept.md"'),
    ("project-trajectory/PROCESS.md", "the risk the operator accepts by delegating.",
     "the risk the operator takes on by delegating."),
    (CT, "# still reads `docs/ratify/CURRENT.md` / `docs/ratify/<date>-*.md`. `approv` is\n"
         "# matched too, for a link authored against the word the kit uses everywhere else.",
     "# still reads `docs/ratify/CURRENT.md` / `docs/ratify/<date>-*.md`. `accept` is\n"
     "# matched too, for a link authored against the word the kit uses everywhere else."),
    (CT, 'r"(?:ratif|approv|hierarch)\\w*[^\\s]*\\.(?:md|html|csv)|\\]\\([^)]*(?:ratif|approv|hierarch)[^)]*\\)",',
     'r"(?:ratif|accept|hierarch)\\w*[^\\s]*\\.(?:md|html|csv)|\\]\\([^)]*(?:ratif|accept|hierarch)[^)]*\\)",'),
    (CT, "        # `approv` (not `ratif`, WI-499): live prose no longer uses the retired\n"
         "        # spelling, so a freshly-authored row's own text is the \"this decision\n"
         "        # is about an operator acceptance\" signal now.",
     "        # `accept` (not `ratif`, WI-499, nor `approv`, 2026-11-16): live prose\n"
     "        # no longer uses a retired spelling, so a freshly-authored row's own\n"
     "        # text is the \"this decision is about an operator acceptance\" signal."),
    (CT, '            r"approv", body, re.IGNORECASE', '            r"accept", body, re.IGNORECASE'),
]
