"""HANDOFF 10.6, hand edits in prose, templates, skills and rows, against the
text after r46a and r46b.

Sentences the phrase rules could not reach, the code_symbol cell that still
binds `attest`, the CLI surfaces in the interface rows, and the
`Review-Verdict:` trailer where rows called it an "attestation".
"""

SKILL = (
    "project-trajectory/skills/coordinator-cycle/SKILL.md",
    ".claude/skills/coordinator-cycle/SKILL.md",
    ".agents/skills/coordinator-cycle/SKILL.md",
)
RECIPES = tuple(p.replace("SKILL.md", "references/recipes.md") for p in SKILL)
IFACE = "docs/requirements/interfaces.toml"
LLR = "docs/requirements/low-level-requirements.toml"
SR = "docs/requirements/system-requirements.toml"
TC = "docs/test/test-cases.toml"

EDITS = [
    # ------------------------------------------------------------ skill
    (SKILL, "tag, TC row or `sr_refs` between the two, and attest a set that must",
            "tag, TC row or `sr_refs` between the two, and record checks for a set that must"),
    (SKILL, "A hook-refused commit or failed commit checks attest nothing,",
            "A hook-refused commit or failed commit checks record nothing,"),
    (RECIPES, "non-record paths, so attest them (stage them into the next record-checks run, or",
              "non-record paths, so record checks for them (stage them into the next record-checks run, or"),
    (RECIPES, "reviewer's brief at the record-only tip (the render finds the\n     attestation beneath it)",
              "reviewer's brief at the record-only tip (the render finds the\n     record beneath it)"),
    (RECIPES, "leg renders the round afresh at the same attested tip and records",
              "leg renders the round afresh at the same recorded tip and records"),
    (RECIPES, "  - The render's pytest line is the list the tip was attested with,\n"
              "    and a stage attested over a narrow list",
              "  - The render's pytest line is the list the tip's checks were recorded with,\n"
              "    and a stage recorded over a narrow list"),
    (RECIPES, "- A rebase changes every commit's `work=`, so no attestation survives it:\n"
              "  attest the rebased tip",
              "- A rebase changes every commit's `work=`, so no passed-checks record survives it:\n"
              "  record checks for the rebased tip"),
    (RECIPES, "set, refuses red, and commits the staged work with the attestation the review render",
              "set, refuses red, and commits the staged work with the passed-checks record the review render"),
    (RECIPES, "record-checks --branch <lane> --bar\n  review --message-file <file>`:",
              "record-checks --branch <lane> --checks\n  commit --message-file <file>`:"),
    (RECIPES, "copy the later stage's file aside, check it out at HEAD, attest the\n"
              "  first stage, then restore the file and attest the second",
              "copy the later stage's file aside, check it out at HEAD, record checks for\n"
              "  the first stage, then restore the file and record checks for the second"),
    (RECIPES, "commits without an\n  attestation (registry text), or is staged into the attest that carries\n"
              "  those tests. The first attest after it must hold",
              "commits without a\n  passed-checks record (registry text), or is staged into the record-checks run that\n"
              "  carries those tests. The first record-checks run after it must hold"),
    (RECIPES, "under other jobs' load an attest's\n", "under other jobs' load a record-checks run's\n"),
    # ------------------------------------------------------------ docs, templates
    ("docs/stack.ini", "names the\n#     one an attestation of a commit runs,",
                       "names the\n#     one `integrate.py record-checks` runs on a commit,"),
    ("docs/stack.ini", "#     marker refuses an attestation and a refresh alike);",
                       "#     marker refuses a record-checks run and a refresh alike);"),
    ("docs/runtime-flows.md", "the **bar is attested to a tree** on the",
                              "the **checks are recorded against a tree** on the"),
    ("docs/runtime-flows.md", "does the tip attest its OWN tree for the landing checks,",
                              "does the tip record the landing checks for its OWN tree,"),
    ("docs/enforcement-audit.md", "read as a CROSS-CHECK — an attestation contradicting the rounds",
                                  "read as a CROSS-CHECK — a trailer contradicting the rounds"),
    ("project-trajectory/process.toml.template",
     "#   commit   every commit a lane attests. `integrate.py record-checks` runs the named\n"
     "#            suite on the staged work, then the row's derived review tests,\n"
     "#            and records the green in the commit.",
     "#   commit   every commit a lane builds. `integrate.py record-checks` runs the named\n"
     "#            suite on the staged work, then the row's derived review tests,\n"
     "#            and records that they passed in the commit."),
    (("project-trajectory/prompts/worker.template.md", "tests/golden/worker-prompt-one-row.txt"),
     "outside any session's turn, and attests it with a `Checks-Passed:` trailer naming the tree it barred and the bar it ran (`checks=landing`).",
     "outside any session's turn, and records it with a `Checks-Passed:` trailer naming the tree it barred and the checks it ran (`checks=landing`)."),
    ("project-trajectory/PROCESS.md", "declares, attested before the\n", "declares, recorded before the\n"),
    ("project-trajectory/PROCESS_OPTIONS.md", "peeled off at the work sha it attests,", "peeled off at the work sha it records,"),
    # the [authority] dials' verdict artifacts: the act's record, not S1 (read with 10.6, as 9.9 asked)
    ("project-trajectory/PROCESS_OPTIONS.md", "(review file `docs/reviews/WI-<n>-<PHASE>.md`, critique, attestation)",
                                              "(review file `docs/reviews/WI-<n>-<PHASE>.md`, critique, acceptance)"),
    # ------------------------------------------------------------ interface rows
    (IFACE, 'data = "claim | refresh | attest | integrate | done-when-hold | audit;',
            'data = "claim | refresh | record-checks | integrate | done-when-hold | audit;'),
    (IFACE, "· record-checks --branch --bar --message-file ·", "· record-checks --branch --checks --message-file ·"),
    (IFACE, "and the empty commit an attestation rides when its bookkeeping is unchanged",
            "and the empty commit a trailer rides when its bookkeeping is unchanged"),
    (IFACE, "and the identity an attestation's carrier names", "and the identity a trailer's carrier names"),
    (IFACE, 'data = "claim, refresh, attest, integrate, finished_branches,',
            'data = "claim, refresh, record_checks, integrate, finished_branches,'),
    # ------------------------------------------------------------ design rows
    (LLR, "The trailer is a cross-check over the newest attestation at the tree under judgement,",
          "The trailer is a cross-check over the newest trailer at the tree under judgement,"),
    (LLR, "- the attestation's writer is best-effort,", "- the trailer's writer is best-effort,"),
    (LLR, "commits a verified passed-checks record whose summary reads no-bar honestly)",
          "commits a verified passed-checks record, `checks=none`, whose summary says honestly that no checks ran)"),
    (LLR, "branch_trailers;attest/_record_checks_preflight/", "branch_trailers;record_checks/_record_checks_preflight/"),
    (LLR, "admits a refresh subject only with that verified attestation and checks `landing` or `none`",
          "admits a refresh subject only with that verified record and checks `landing` or `none`"),
    (LLR, "returns the ordered attestation sequence per tree.", "returns the ordered trailer sequence per tree."),
    (LLR, "since the newest verified commit record and resets after that attestation.",
          "since the newest verified commit record and resets after that record."),
    (LLR, "set printing, attestation, draw, rendering,", "set printing, recording, draw, rendering,"),
    (LLR, 'title = "Expected-failure marks are declared, attested, and excluded from landing trees"',
          'title = "Expected-failure marks are declared, recorded, and excluded from landing trees"'),
    (LLR, "A removal made by a plain commit is judged at the next attestation.",
          "A removal made by a plain commit is judged at the next record-checks run."),
    (LLR, "Coverage bound: lane attestation and refresh, a plain commit followed by attestation,",
          "Coverage bound: lane record-checks run and refresh, a plain commit followed by a record-checks run,"),
    (LLR, "Hand-edited attestation trailers,", "Hand-edited Checks-Passed trailers,"),
    (LLR, "and earlier marks and attestations are not judged.", "and earlier marks and passed-checks records are not judged."),
    # ------------------------------------------------------------ requirement rows
    (SR, 'title = "Review briefs render only over a matching verified review record"',
         'title = "Review briefs render only over a matching verified passed-checks record"'),
    (SR, "when its commit carries a verified review record for the test set",
         "when its commit carries a verified passed-checks record for the test set"),
    # (SR "the lane's last review record": r46b's rule already moved it)
    # ------------------------------------------------------------ test cases
    (TC, "the attestation joins the message trailer block;", "the passed-checks record joins the message trailer block;"),
    (TC, "via the LLR-140 claim/integration contract and the LLR-207 attest, producer and refresh-record contract",
         "via the LLR-140 claim/integration contract and the LLR-207 record-checks, producer and refresh-record contract"),
    (TC, "does not have the quotation read as its own attestation;", "does not have the quotation read as its own trailer;"),
    (TC, "and TWO attestations at one governing tree", "and TWO trailers at one governing tree"),
    (TC, "the identical attestation words on a commit", "the identical trailer words on a commit"),
    (TC, "so copying a true attestation onto later work buys nothing.", "so copying a true trailer onto later work buys nothing."),
    (TC, "is asserted to CARRY the attestation, to name", "is asserted to CARRY the trailer, to name"),
    (TC, "between a round completing and its attestation landing,", "between a round completing and its trailer landing,"),
    (TC, "is refused because the attestor derives the actual", "is refused because the peel derives the actual"),
    (TC, "a genuine refresh attested to the sha it produced;", "a genuine refresh recorded for the sha it produced;"),
    (TC, "revoking the attestation; the deliberately forged attestation recorded as a STATED limit",
         "revoking the record; the deliberately forged record kept as a STATED limit"),
    (TC, "writes when a Review-Verdict attestation must land", "writes when a Review-Verdict trailer must land"),
    (TC, "to carry the coordinator's attestation under the key", "to carry the coordinator's trailer under the key"),
    (TC, "THE ATTESTATION'S CARRIER IS SCOPED TO ITS OWN PATHS", "THE TRAILER'S CARRIER IS SCOPED TO ITS OWN PATHS"),
    (TC, "nor an attestation ride a commit that changed the tree.", "nor a trailer ride a commit that changed the tree."),
    (TC, "or contradicted by its own attestation;", "or contradicted by its own trailer;"),
    (TC, "the refresh's attestation still verifies,", "the refresh's passed-checks record still verifies,"),
    (TC, 'expected = "A green review bar attests once and then draws the queued review."',
         'expected = "Passing commit checks are recorded once and then the queued review is drawn."'),
    (TC, 'expected = "Attestation accepts no hand test list,', 'expected = "record-checks accepts no hand test list,'),
    (TC, "the failed-checks records and the attestations.", "the failed-checks records and the passed-checks records."),
    (TC, 'method = "Run attestation integration cases for declaration,', 'method = "Run record-checks integration cases for declaration,'),
    (TC, 'expected = "Attestation refuses the stated declaration', 'expected = "record-checks refuses the stated declaration'),
]
