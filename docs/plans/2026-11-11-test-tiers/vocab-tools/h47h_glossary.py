"""HANDOFF 10.7 item 2, with 12.4 and 4.5.2/4.5.3/4.5.6 (ruled 2026-11-16):
the glossary by hand.

- New entries: **stage** (the development stage and nothing else, 12.4),
  **checks stage** (4.5.2's draft under the ruled name), **evidence gap**
  (4.5.3's draft), and 4.5.6's usage rule (**Passes and fails**) in the
  preamble beside the "Human" rule. 4.5.4, 4.5.5 and 4.5.7 are not glossary
  terms.
- "Stage" becomes "step" in the *lane state* entry (12.4).
- The older entries: "the owner" in *independence* and *arbiter*, "takes
  the approval act" in *adjudicator*, "approves only if it changes nothing"
  in *independence* (10.7 item 2).
- Links: the new entries link the terms they use; *landing checks* and *gate
  checks* link **stage** and **checks stage**.
"""

G = "project-trajectory/GLOSSARY.md"

EDITS = [
    # --- the preamble's usage rule (4.5.6)
    (
        G,
        '[operator](#operator). "Human" appears only in prose, where it states that a\n'
        "person is intended.\n",
        '[operator](#operator). "Human" appears only in prose, where it states that a\n'
        "person is intended.\n"
        "\n"
        "**Passes and fails.** A run of checks **passes** or **fails**. \"Red\" and\n"
        "\"green\" are not used for either, except once, where `process.md` names the\n"
        "red, green, refactor cycle. A threshold is named for what it is (a minimum,\n"
        "a standard, a level), never a \"bar\".\n",
    ),
    # --- independence: the adjudicator's own act, and the operator
    (
        G,
        "spine draft after an [adjudication reviewer](#adjudication-reviewer) has edited\n"
        "it: it approves only if it changes nothing.",
        "spine draft after an [adjudication reviewer](#adjudication-reviewer) has edited\n"
        "it: it [accepts](#accept) the rows only if the pass changes nothing.",
    ),
    (G, "for the owner's review.", "for the [operator](#operator)'s review."),
    # --- adjudicator
    (
        G,
        "The role that rules on spine rows, disputes and dispositions and takes the\n"
        "approval act,",
        "The role that rules on spine rows, disputes and dispositions and takes the\n"
        "[acceptance](#accept) act,",
    ),
    # --- arbiter
    (
        G,
        "alone; when each selects its own, the round becomes an open item for the owner,\n"
        "which offers running an independent third agent of the owner's choosing, only\n"
        "if the owner picks it.",
        "alone; when each selects its own, the round becomes an open item for the\n"
        "[operator](#operator), which offers running an independent third agent of the\n"
        "operator's choosing, only if the operator picks it.",
    ),
    # --- evidence gap, under Rows (4.5.3)
    (
        G,
        "how much does. Declared as `verification_method = \"Vouch\"`. Formerly `Attest`;\n"
        "**Vouch** is kept.\n",
        "how much does. Declared as `verification_method = \"Vouch\"`. Formerly `Attest`;\n"
        "**Vouch** is kept.\n"
        "\n"
        "### evidence gap\n"
        "\n"
        "A test case that is not [accepted](#accept) although every requirement it\n"
        "verifies is cited by a work item recorded done: the work is closed and its\n"
        "evidence is not. The gap census names each one, and the landing mints an\n"
        "adjudication row for it, briefed as the `evidence-gap` kind. Formerly a\n"
        "\"red TC\"; **evidence gap** is kept.\n",
    ),
    # --- lane state: a step of a lane, not a stage (12.4)
    (
        G,
        "A state names the stage\n"
        "whose work is owed next or is running now;",
        "A state names the step\n"
        "whose work is owed next or is running now;",
    ),
    # --- stage and checks stage, opening the Checks section
    (
        G,
        "## Checks\n\n### required checks\n",
        "## Checks\n"
        "\n"
        "### stage\n"
        "\n"
        "The development stage: the rung of the `DevStg-*` ladder a repository stands\n"
        "at, derived from its registries and recorded in `docs/stage`\n"
        "(`process.md` §4, \"A stage is a STATE\"). `check.py --stage`\n"
        "selects the steps that run at it. The word names this and nothing else: a\n"
        "step of a lane or of a pipeline in code is a **step**, and git's index keeps\n"
        "its own word, \"staged\". The retired axis of stage thresholds was the \"bar\";\n"
        "**stage** is kept.\n"
        "\n"
        "### checks stage\n"
        "\n"
        "The [stage](#stage) a work item pins its [landing checks](#landing-checks) to.\n"
        "A row claimed to deliver evidence at a stage is checked at that stage even if\n"
        "the repository's derived stage moves while its lane is in flight. Declared in\n"
        "the work item as `checks_stage`. Formerly the item's `bar`; **checks stage**\n"
        "is kept.\n"
        "\n"
        "### required checks\n",
    ),
    (
        G,
        "[landing](#landing): the full gate, run by the station refresh on the tree\n"
        "that becomes trunk. Not a declared setting.",
        "[landing](#landing): the full gate, run by the station refresh on the tree\n"
        "that becomes trunk, at the repository's [stage](#stage) or the work item's\n"
        "[checks stage](#checks-stage). Not a declared setting.",
    ),
    (
        G,
        "The full gate for a stage: `check.py` at that stage,",
        "The full gate for a [stage](#stage): `check.py` at that stage,",
    ),
]
