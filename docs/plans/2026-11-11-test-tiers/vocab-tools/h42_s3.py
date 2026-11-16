"""HANDOFF 4.2, the method `Vouch`: the sentences the rules could not word.

Applied after r42_s3_vouch.py. Trap 15 is closed here: `Manual` no longer
defines itself against the method, and "LLM-Attest" is a delegated `Vouch`.
"""

PT = "project-trajectory/"
S = PT + "scripts/"
PROC = PT + "PROCESS.md"
OPT = PT + "PROCESS_OPTIONS.md"
EX = PT + "EXAMPLE.md"
GATE = tuple(p + "skills/gate-advance/SKILL.md" for p in (PT, ".claude/", ".agents/"))
GOLD = tuple("tests/golden/%s.txt" % n for n in ("clean", "offspine", "orphan"))
REF = "docs/registry-machinery-reference.md"
TR = S + "trace.py"

EDITS = [
    # --- PROCESS.md
    (PROC, "Where verification can't be mechanized, a **recorded human\nattestation** (§4 `Vouch`) is the honest floor",
           "Where verification can't be mechanized, the **operator's\nrecorded word** (§4 `Vouch`) is the honest floor"),
    (PROC, "`Manual` (a human procedure that isn't\n`Vouch`), `Vouch`, and `Critique`.",
           "`Manual` (a procedure a person carries out, whose result\nanother could repeat), `Vouch`, and `Critique`."),
    (PROC, "physical action) — a **named human's recorded judgment**, **trust-based, the box",
           "physical action) — the **operator's recorded word**, **trust-based, the box"),
    (PROC, "check. Its TC records **who** attested and **when**", "check. Its TC records **who** vouched and **when**"),
    (PROC, 'under "attested vs mechanized" so an audit sees the trust footprint.',
           'under "vouched vs mechanized" so an audit sees the trust footprint.'),
    (PROC, "(an LLM one, deliberately separated from human `Vouch`) judges",
           "(an LLM one, deliberately separated from `Vouch`) judges"),
    # --- PROCESS_OPTIONS.md
    (OPT, "- **(b) Attestation is the honest floor — and honestly trust-based.** Where\n"
          "  verification cannot be mechanized, the floor is a **recorded human\n"
          "  attestation**: a named person's recorded judgment that the acceptance\n",
          "- **(b) A vouch is the honest floor — and honestly trust-based.** Where\n"
          "  verification cannot be mechanized, the floor is the **operator's recorded\n"
          "  word**: a named person's recorded judgment that the acceptance\n"),
    (OPT, "  happened.** Attestation is trust; a mechanized check is proof. The process does\n"
          "  **not** pretend they are equivalent — its job is to make the attestation\n"
          '  **explicit** (a real verification kind, not a silent "Verified"), **named** (who\n'
          "  attested), and **auditable**",
          "  happened.** A vouch is trust; a mechanized check is proof. The process does\n"
          "  **not** pretend they are equivalent — its job is to make the vouch\n"
          '  **explicit** (a real verification kind, not a silent "Verified"), **named** (who\n'
          "  vouched), and **auditable**"),
    (OPT, 'verification kind (§4) and the "attested vs mechanized" split in the trace',
          'verification kind (§4) and the "vouched vs mechanized" split in the trace'),
    (OPT, "LLR — unless the Verification is LLR-exempt Analysis/Inspection/Vouch — plus a",
          "LLR — unless the verification method is LLR-exempt Analysis/Inspection/Vouch — plus a"),
    (OPT, "peer-tier second opinion *before* execution), human `Vouch` by LLM-Attest.",
          "peer-tier second opinion *before* execution), a person's `Vouch` by a delegated one."),
    (OPT, "### LLM-Attest (replaces human Attest at `autonomous`)\n\n"
          "For subjective judgments that must not fake being tests: the TC records\n"
          "`Vouch` with **which model** attested, when, and the one-line judgment —\n"
          "reported in the vouched-vs-mechanized split as *machine* attestation, never\n"
          "disguised as `Test`. The owner's final read is where the owner's eyes replace these.",
          "### Delegated `Vouch` (in place of a person's at `autonomous`)\n\n"
          "For subjective judgments that must not fake being tests: the TC records\n"
          "`Vouch` with **which model** vouched, when, and the one-line judgment —\n"
          "reported in the vouched-vs-mechanized split as a *delegated* vouch, never\n"
          "disguised as `Test`. The operator's final read is where a person's eyes replace these."),
    (OPT, "`CRITIQUE` leg is its mechanization; human **`Vouch`** stays a distinct, unmixed",
          "`CRITIQUE` leg is its mechanization; **`Vouch`** stays a distinct, unmixed"),
    (OPT, "**the critic gates iteration; the human\n  owns acceptance.** A critic `APPROVE` ends rework; gate closure still carries the\n"
          "  human `Vouch` (the strong-model floor",
          "**the critic gates iteration; the operator\n  owns acceptance.** A critic `APPROVE` ends rework; gate closure still carries the\n"
          "  operator's `Vouch` (the strong-model floor"),
    (OPT, "7. **Acceptance:** human `Vouch` closes the round per the gate philosophy;",
          "7. **Acceptance:** the operator's acceptance closes the round per the gate philosophy;"),
    # --- EXAMPLE.md
    (EX, "the honest verification method is **`Vouch`**: a **named human's recorded\njudgment** (process.md §4",
         "the honest verification method is **`Vouch`**: the **operator's recorded\nword** (process.md §4"),
    (EX, "the process makes the attestation *explicit, named, and auditable* rather than",
         "the process makes the vouch *explicit, named, and auditable* rather than"),
    (EX, "whose cell records **who attested and when**:", "whose cell records **who vouched and when**:"),
    (EX, '**"Verification basis (attested vs mechanized)"**', '**"Verification basis (vouched vs mechanized)"**'),
    # --- the gate-advance skill and its two mirrors, and the index row it feeds
    (GATE, "how to record human attestation with Attest, and how", "how to record the operator's word with Vouch, and how"),
    (GATE, "Use the **`Vouch`** verification method: a **named human's\nrecorded judgment**, captured in",
           "Use the **`Vouch`** verification method: the **operator's\nrecorded word**, captured in"),
    (GATE, "## Report attested vs. mechanized\n\n"
           '`trace.py` always emits a **"Verification basis (attested vs mechanized)"**\n'
           "count. When reporting a bar's readiness, state that split honestly — how many SRs\n"
           "are machine-verified vs. resting on a human attestation — so a reviewer sees the\n"
           'trust footprint rather than a single "all green". An attested bar can be\n'
           "legitimate; hiding that it's attested is not.",
           "## Report vouched vs. mechanized\n\n"
           '`trace.py` always emits a **"Verification basis (vouched vs mechanized)"**\n'
           "count. When reporting a bar's readiness, state that split honestly — how many SRs\n"
           "are machine-verified vs. resting on someone's word — so a reviewer sees the\n"
           'trust footprint rather than a single "all green". A vouched bar can be\n'
           "legitimate; hiding that it's vouched is not."),
    (PT + "skills/INDEX.csv", "stages ladder devstg approval attest verification sign-off",
                              "stages ladder devstg approval vouch verification sign-off"),
    (PT + "skills/INDEX.csv", "how to record human attestation with Attest, and how", "how to record the operator's word with Vouch, and how"),
    # --- the reference doc
    (REF, "- **attested** = `Vouch` — rests on a named human's recorded judgment.",
          "- **vouched** = `Vouch` — rests on the operator's recorded word."),
    (REF, "`Verification ∈ {Analysis, Inspection, Vouch}`", "`VerificationMethod ∈ {Analysis, Inspection, Vouch}`"),
    (REF, "`Verification ∈ LLR_EXEMPT`", "`VerificationMethod ∈ LLR_EXEMPT`"),
    (PT + "rubrics/README.template.md", "one, deliberately separated from human `Vouch`; process-options.md",
                                         "one, deliberately separated from `Vouch`; process-options.md"),
    # --- scripts
    (S + "agent_loop.py", "the human owns final acceptance via Attest at gate\n    closure.",
                          "the operator owns final acceptance at gate\n    closure."),
    (S + "bootstrap.py", '"§4 `Vouch` (named human judgment)",\n            "a human attests",\n'
                         '            "LLM-Attest: named *model* judgment, reported honestly as machine "\n'
                         '            "attestation in the trace report\'s vouched-vs-mechanized split",',
                         '"§4 `Vouch` (the operator\'s recorded word)",\n            "the operator vouches",\n'
                         '            "a delegated `Vouch`: a named *model*\'s word, reported as delegated "\n'
                         '            "in the trace report\'s vouched-vs-mechanized split",'),
    (TR, "# Verification methods whose approval rests on a recorded human judgment,",
         "# Verification methods whose approval rests on the operator's recorded word,"),
    (TR, "Attest rests on a named\n    human's recorded judgment (attested — trust-based).",
         "Vouch rests on the\n    operator's recorded word (vouched — trust-based)."),
    (TR, "or on a named human's recorded judgment (Attest)? Split", "or on the operator's recorded word (Vouch)? Split"),
    (TR, "the demonstrated and attested ids are listed", "the demonstrated and vouched ids are listed"),
    (TR, '"rows rest on a named human\'s recorded judgment (trust-based — the box can "',
         '"rows rest on the operator\'s recorded word (trust-based — the box can "'),
    (GOLD, "`Vouch` rows rest on a named human's recorded judgment (trust-based",
           "`Vouch` rows rest on the operator's recorded word (trust-based"),
    # --- tests
    ("tests/test_trace.py", "# --- WI-1.7: human-attestation verification kind (Attest) ---------------------",
                            "# --- WI-1.7: the verification method that rests on someone's word (Vouch) ----"),
    ("tests/test_trace.py", "# A Vouch SR: a named human's recorded judgment, no code to decompose (so\n"
                            "# LLR-exempt), but it still needs a TC that records who/when attested.",
                            "# A Vouch SR: the operator's recorded word, no code to decompose (so\n"
                            "# LLR-exempt), but it still needs a TC that records who vouched and when."),
    ("tests/test_trace.py", "def test_attest_sr_is_llr_exempt_but_needs_tc(", "def test_a_vouch_sr_is_llr_exempt_but_needs_tc("),
    ("tests/test_trace.py", "# SR-002 (Attest) has no LLR yet is not an orphan", "# SR-002 (Vouch) has no LLR yet is not an orphan"),
    ("tests/test_trace.py", "def test_attest_verified_accepted_and_surfaced_distinctly(",
                            "def test_a_verified_vouch_sr_passes_and_is_surfaced_distinctly("),
    ("tests/test_trace.py", "def test_attest_is_in_verification_vocabulary(", "def test_vouch_is_in_the_verification_vocabulary("),
]
