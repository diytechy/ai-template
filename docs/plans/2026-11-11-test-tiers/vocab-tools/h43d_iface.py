"""HANDOFF 4.3 / 10.4, owner: the role sentences inside the interface files.

r43b skips these files and r43c reaches only phrases that name nothing but the
role. These are the rest, found by listing every "owner" in the files and
reading each: the role (the person in charge, their queue, their edits, their
rulings) moves; the providing side of an interface, a module that owns a
rule, and acts.toml's own writer keep the word. In interfaces.toml the
decisions key is also named by its spelling (`owner (optional: ...)`,
"raw owner value"), and follows the key.

Written against the text after r43c_owner_iface.py.
"""

IFACE = "docs/requirements/interfaces.toml"
SPINE = "project-trajectory/scripts/kitlib/spine.py"

EDITS = [
    # kitlib/spine.py
    (SPINE, "-> WI-099). Owner\nruling D-8", "-> WI-099). Operator\nruling D-8"),
    (SPINE, "a pending open item on the owner's\n# queue:",
     "a pending open item on the operator's\n# queue:"),
    (SPINE, "THE ONE QUEUE PROJECTION of the owner's pending decisions",
     "THE ONE QUEUE PROJECTION of the operator's pending decisions"),
    (SPINE, "cannot disagree about what the owner owes.",
     "cannot disagree about what the operator owes."),
    (SPINE, "the decision reaches the owner through the queue.",
     "the decision reaches the operator through the queue."),
    # the other code and prose files
    ("project-trajectory/scripts/gen_arch_map.py", "per F5 (owner 2026-07-12,",
     "per F5 (operator 2026-07-12,"),
    ("project-trajectory/scripts/migrate_carrier.py",
     "the re-attestation brief the owner is about to work",
     "the re-attestation brief the operator is about to work"),
    ("project-trajectory/scripts/rendering/traj_views.py",
     "# the owner's \"> 3\" rule)", "# the operator's \"> 3\" rule)"),
    ("project-trajectory/MULTI_REPO.md",
     "Six decisions, confirmed with the product owner.",
     "Six decisions, confirmed with the operator."),
    # interfaces.toml: the role
    (IFACE, "is a live question for the frame's owner;",
     "is a live question for the operator;"),
    (IFACE,
     "The dial file is what the owner edits and every enforcer reads; one value "
     "per dial, read alike by each reader, is the outcome the owner asked for.",
     "The dial file is what the operator edits and every enforcer reads; one "
     "value per dial, read alike by each reader, is the outcome the operator "
     "asked for."),
    (IFACE, "verdict audit, owner actions; Decisions to review last",
     "verdict audit, operator actions; Decisions to review last"),
    (IFACE, "the re-attestation chains for the owner to rule on;",
     "the re-attestation chains for the operator to rule on;"),
    (IFACE, "where the owner's uncommitted work also lives",
     "where the operator's uncommitted work also lives"),
    (IFACE, "discarding an edit of the owner's,", "discarding an edit of the operator's,"),
    (IFACE, "The owner's approval brief sets apart", "The operator's approval brief sets apart"),
    (IFACE, "keeps the owner's surface, the mint", "keeps the operator's surface, the mint"),
    (IFACE, "and the owner edits in place afterwards.",
     "and the operator edits in place afterwards."),
    # interfaces.toml: the decisions key, named by its spelling
    (IFACE, "why_not_escalated, review, owner (optional: confirmed | overruled;",
     "why_not_escalated, review, operator (optional: confirmed | overruled;"),
    (IFACE, "owner is the owner's verdict.", "operator is the operator's verdict."),
    (IFACE, "whatever owner value accompanies it", "whatever operator value accompanies it"),
    (IFACE, "and raw owner value;", "and raw operator value;"),
    (IFACE, "whatever owner it carries", "whatever operator it carries"),
]
