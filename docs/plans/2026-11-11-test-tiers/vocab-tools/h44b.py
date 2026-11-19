"""HANDOFF 4.4, the remaining rows: final read, merge admission, the frame's
party EXT-006, product operator, and the sub-agent that judges nothing."""

PT = "project-trajectory/"
S = PT + "scripts/"
RECIPES = tuple(
    p + "skills/coordinator-cycle/references/recipes.md"
    for p in (PT, ".claude/", ".agents/")
)
EXT = "docs/requirements/external.toml"
LLR = "docs/requirements/low-level-requirements.toml"

EDITS = [
    # --- the final read at release (was "Acceptance")
    ("README.md",
     "- **Acceptance — the owner's final read.** A human exercises the real product (including\n"
     "  manual/demonstration items) and approves.",
     "- **The operator's final read.** A person exercises the real product (including\n"
     "  manual/demonstration items) and signs off."),
    (PT + "KICKOFF_PROMPT.md",
     "- **Acceptance — the owner's final read.** A human/stakeholder exercises the real product\n"
     "  (including the Demonstration/Manual items) and signs off.",
     "- **The operator's final read.** A person or stakeholder exercises the real product\n"
     "  (including the Demonstration/Manual items) and signs off."),
    (PT + "PROCESS.md",
     "- **Acceptance — the owner's final read.** Human/stakeholder exercises the real product (incl.\n"
     "  Demonstration/Manual items) and approves. For shipped software this is the",
     "- **The operator's final read.** A person or stakeholder exercises the real product (incl.\n"
     "  Demonstration/Manual items) and signs off. For shipped software this is the"),
    (PT + "LOG.template.md",
     "| Acceptance | `DevStg-Release` (the owner's final read) |",
     "| Final read | `DevStg-Release` (the operator's final read) |"),
    # --- merge admission (was "accept path", "accepted-on-train")
    (S + "agent_brief.py", "a trailer is never an accept path", "a trailer is never an admission path"),
    (S + "agent_loop.py", "is accepted-on-train (locally green and committed), not reviewed",
                          "is admitted-on-train (locally green and committed), not reviewed"),
    (S + "integrate.py", "read as a CROSS-CHECK and never as an accept path",
                         "read as a CROSS-CHECK and never as an admission path"),
    (S + "kitlib/verdict.py", "THIS IS NOT AN ACCEPT PATH, and the distinction",
                              "THIS IS NOT AN ADMISSION PATH, and the distinction"),
    ("tests/test_verdict_record.py", "a CROSS-CHECK, never an accept path.", "a CROSS-CHECK, never an admission path."),
    # --- the party in this repository's frame, EXT-006 (was "Human operator")
    (EXT, 'name = "Human operator"', 'name = "Person"'),
    (EXT, "dropped: an adopting team is the human operator of the kit in its own",
          "dropped: an adopting team is the person operating the kit in its own"),
    (EXT, "It mediates for the human operator (EXT-006): an outcome landing on its crossings can be one that operator experiences.",
          "It mediates for the person (EXT-006): an outcome landing on its crossings can be one that person experiences."),
    ("docs/requirements/assumptions.toml",
     "# use: the human operator's own crossings (B-02 authority, B-09 read) or the\n"
     "# development session's, which mediates for that operator (B-01 writes, B-04",
     "# use: the person's own crossings (B-02 authority, B-09 read) or the\n"
     "# development session's, which mediates for that person (B-01 writes, B-04"),
    ("docs/requirements/stakeholder-needs.toml",
     "# human operator (EXT-006): an adopting team is the human operator of the kit in\n"
     "# its own repository.",
     "# person (EXT-006): an adopting team is the person operating the kit in\n"
     "# its own repository."),
    (LLR, "the human operator across B-09", "the person (EXT-006) across B-09", 5),
    ("tests/test_external_frame.py",
     "hosted-CI cut): the human operator and hosted CI drawn as parties, the",
     "hosted-CI cut): the person and hosted CI drawn as parties, the"),
    ("tests/test_external_frame.py",
     "and the Adopter folded into the human\n    operator. A count is",
     "and the Adopter folded into the\n    person. A count is"),
    ("tests/test_external_frame.py",
     "an adopting team is the human operator\n    # of the kit in its own repository (EXT-006);",
     "an adopting team is the person operating\n    # the kit in its own repository (EXT-006);"),
    # --- a stakeholder of the adopter's product (was bare "operator")
    (PT + "STATUS.template.md",
     "_(who or what the system serves — humans,\n  operators, or another system, represented by its owner)_",
     "_(who or what the system serves — humans,\n  product operators, or another system, represented by its owner)_"),
    (PT + "registries/stakeholder-needs.template.toml",
     "whoever the system serves: an end user, an\n# operator, or ANOTHER SYSTEM",
     "whoever the system serves: an end user, a\n# product operator, or ANOTHER SYSTEM"),
    # --- the sub-agent that "judges nothing" is not the operator
    (RECIPES, "  - a Claude operator sub-agent may render, tile, brief, launch the six",
              "  - a Claude sub-agent may render, tile, brief, launch the six"),
]
