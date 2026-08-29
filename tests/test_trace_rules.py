"""trace.py — the pure registry-rule decisions, unit-checked in process
(WI-277: split verbatim from tests/test_trace.py by behavior boundary).

The spine-prose predicates (a row states the system not its own history; one
testable obligation; the paraphrase advisory that warns but never gates; the
optional LLR Rationale column), the WI-129 LLR/TC status-coherence lint, the WI-146(a)
--approve hierarchy view, and the WI-081 Slice C render/exit helpers
(_bucket_by_ref pre-indexing + the exit_code gate policy).
"""

from conftest import load_script, make_minimal_project, run_py


def test_a_spine_row_states_the_system_not_its_own_history():
    # Owner-raised at the first re-attestation sitting, on LLR-050's `WI-316:`
    # changelog prefix: a spine row must be stand-alone — a reader with none of
    # this repo's history reads one row and knows what the system does and why.
    # Provenance has better homes (work-items.csv, the log's Decisions), and the
    # row OBEYS the process rather than citing it.
    from conftest import load_script

    trace = load_script("trace")

    def flags(sr=None, llr=None, tc=None):
        def rows(cells, key, rid):
            if cells is None:
                return []
            cells.setdefault(key, rid)
            return [cells]

        return trace.provenance_findings(
            rows(sr, "SR-ID", "SR-101"),
            rows(llr, "LLR-ID", "LLR-101"),
            rows(tc, "TC-ID", "TC-101"),
        )

    # The two token shapes, in the normative cells of all THREE registries — the
    # scope the SR-only version could not see, and where 43 of the 45 rows lived.
    assert flags(sr={"Requirement": "Shall resume (WI-210, one path)."})
    assert flags(sr={"AcceptanceCriteria": "Modified (WI-316) rows re-attest."})
    assert flags(sr={"Rationale": "Re-scoped by WI-210 to one path."})
    assert flags(sr={"Title": "Resume authority (WI-210)"})
    assert flags(llr={"Detail": "WI-316: is_modified recognized."})
    assert flags(llr={"Title": "Derived gate (WI-316)"})
    # The LLR's `Rationale` is normative text like its `Detail`, so the rule
    # reaches it. Without this the new column would be a provenance loophole —
    # exactly the "largest pocket is the layer the rule cannot see" failure the
    # SR-only scope already made once.
    assert flags(llr={"Rationale": "Chosen in WI-300's option (f) ruling."})
    assert flags(llr={"Rationale": "Required by process.md section 3."})
    assert flags(tc={"Method": "Ported from the tracks suite, WI-210."})
    assert flags(tc={"Expected": "Live set as of the WI-314 binding."})
    assert flags(tc={"Parameters": "the 109-character WI-308 clause"})
    assert flags(sr={"Requirement": "The gate derives per process.md section 7."})
    assert flags(llr={"Detail": "See process-options.md 'Phased delivery'."})
    # The NEGATIVE half, and the whole reason the rule can be narrow: 65 SR rows
    # name a script, 6 an artifact path and 5 a rubric, and every one is
    # legitimate — this kit's product IS its scripts, so the name is the system
    # under specification. A rule that fired on those gets scrolled past.
    assert not flags(sr={"Requirement": "trace.py --strict shall exit nonzero."})
    assert not flags(sr={"Requirement": "The derived gate caches to docs/gate."})
    assert not flags(sr={"AcceptanceCriteria": "Judged against docs/rubrics/x.md."})
    assert not flags(llr={"Detail": "gen_trajectory.py renders PROJECT_STATE.html."})
    assert not flags(sr={"Requirement": "Bounded by SR-055; decomposed to LLR-050."})
    assert not flags(tc={"Method": "Run tests/test_trace.py against a scaffold."})
    # Not a WI id merely because the letters occur, and not any .md file.
    assert not flags(sr={"Requirement": "A SWITCH-210 dial selects the tier."})
    assert not flags(llr={"Detail": "Documented in ADOPTING.md section 6."})
    # Pointer columns are out of scope BY DESIGN — they exist to point.
    assert not flags(llr={"Detail": "x", "Module": "wi_210.py", "TestRefs": "WI-210"})
    # A placeholder row never gates a scaffold.
    assert not flags(sr={"SR-ID": "SR-000", "Requirement": "Example (WI-210)."})
    # It reports the registry, the row, the cell and WHAT it cited.
    (msg,) = flags(llr={"Detail": "Resumes (WI-210) per process.md."})
    assert msg.startswith("LLR LLR-101 Detail")
    assert "'WI-210'" in msg and "'process.md'" in msg
    # And it names a home that EXISTS. The message used to send an author to
    # `work-items.csv`, a carrier whose presence is itself an integrity finding —
    # a lint telling you to move provenance into a file the checker forbids.
    assert "work-items.csv" not in msg
    assert "move provenance to the log" in msg


def test_a_living_cell_carries_no_citation_frame_but_never_gates_on_one():
    # The owner ruling that repealed "a ruling reference is optional context on
    # top of a sentence that stands alone": NO provenance citation in a living
    # registry cell, on all FOUR spine tiers, in the reason cell as loudly as in
    # the normative ones. Warn-first by the same ruling — the population is ~300
    # tokens over ~150 live rows, and a gate would wedge the harness on a prose
    # campaign rather than guard a clean state.
    from conftest import load_script

    trace = load_script("trace")

    def flags(need=None, sr=None, llr=None, tc=None, allow=()):
        def rows(cells, key, rid):
            if cells is None:
                return []
            cells.setdefault(key, rid)
            return [cells]

        return trace.provenance_advisories(
            rows(need, "id", "SN-101"),
            rows(sr, "SR-ID", "SR-101"),
            rows(llr, "LLR-ID", "LLR-101"),
            rows(tc, "TC-ID", "TC-101"),
            allow,
        )

    # THE NEED TIER, which the gating rule cannot see and where the owner's own
    # worked examples lived. Its rows arrive lower-cased off `load_needs`.
    assert flags(
        need={"why": "AMENDED 2026-08-17 (C-ACC-2): the hue is not the signal."}
    )
    assert flags(need={"acceptance": "The launcher exists. (Ruled 2026-08-13, OI-17.)"})
    assert flags(
        need={"need": "Resumes from tracked state (WI-180 retired the pointer)."}
    )
    # THE REASON CELL, the whole point of the widening: a bare date is provenance
    # here, because this is the cell whose job is argument and nothing else.
    assert flags(sr={"Rationale": "Settled 2026-08-15: one home for the observable."})
    assert flags(sr={"Rationale": "The split landed on 2026-08-16."})
    assert flags(llr={"Rationale": "Chosen at sitting-3 over the alternative."})
    # The rest of the vocabulary, each an ENUMERATED shape.
    assert flags(sr={"Rationale": "Raised as OI-29 and answered there."})
    assert flags(sr={"Rationale": "Under repo-lock D-6 the vocabulary has one home."})
    assert flags(sr={"Rationale": "The bar is argument (owner RULING-3)."})
    # THE RULING STAMP THIS REPO ACTUALLY WRITES is the date with a serial
    # letter, and a bare `\d{4}-\d{2}-\d{2}` could not see it: 12 such tokens sat
    # in the registries reporting nothing while the plain-date form beside them
    # reported. The suffix must END the token, so a word beginning with the same
    # letter cannot drag the date into it.
    assert flags(sr={"Rationale": "The owner ruling 2026-08-13u settled this."})
    assert flags(llr={"Rationale": "Cut by 2026-08-16q with the frame locked."})
    assert not flags(sr={"Rationale": "Held 2026-08-13until the sitting ruled."})
    # A NORMATIVE cell reports an edit stamp, never a bare date: a requirement
    # may legitimately carry a date as DATA, and a rule that reads a fixture as a
    # changelog is the cry-wolf failure this whole module is measured against.
    assert flags(tc={"Method": "MINTED 2026-08-18 out of the SR-140 split."})
    assert not flags(tc={"Parameters": "cutover = 2026-08-15; before = 2026-08-14"})
    assert not flags(sr={"Requirement": "The loop shall stamp 2026-08-15 on the row."})

    # THE STAMP THAT LOST ITS DATE. A sweep that used the dated shape as its
    # definition of done deleted the DATES and left 33 bare verbs standing on 31
    # live rows. The corpus writes a stamp as an ALL-CAPS verb opening a clause,
    # optionally behind a short all-caps subject, and that is what this reads.
    assert flags(sr={"Rationale": "One home. MINTED out of the SR-170 split."})
    assert flags(sr={"Rationale": "SPLIT ON THE ONE-DECISION RULE: three shalls."})
    assert flags(llr={"Detail": "The seam holds. RE-POINTED onto what survived."})
    assert flags(tc={"Method": "Runs green. CORRECTED: the fourth clause is gone."})
    assert flags(sr={"Rationale": "OWNER RE-POINTED: the endpoint is the LLR's."})

    # --- THE MEASURED FALSE-POSITIVE HAZARDS, pinned SILENT -------------------
    # (1) A general `<LETTER>-<n>` id pattern was tried and REVERTED once for
    # reading the data pack's own `M-10` crossing ids as rulings. Nothing here
    # generalises over id shapes, so the crossing ids stay data.
    assert not flags(sr={"Rationale": "The M-10 crossing carries the verdict."})
    assert not flags(llr={"Rationale": "Joined against B-04, M-10 and REL-003."})
    # (2) `ruling` / `retired` / `amended` / `attestation` are SUBJECT NOUNS in
    # every row that specifies the approval machinery itself — 217
    # occurrences over 108 live rows. The stamp shape needs a DATE behind the
    # verb, so a row ABOUT amendment is silent and a row RECORDING its own
    # amendment is not.
    assert not flags(sr={"Rationale": "An amended requirement drops the stage."})
    assert not flags(sr={"Requirement": "The gate shall record each attestation."})
    assert not flags(llr={"Detail": "Names the ruling that retired the id."})
    assert not flags(tc={"Expected": "A retired row reports as retired, not absent."})
    # (3) THE SAME HAZARD ONE FLOOR UP: the all-caps verbs are also ordinary
    # PARTICIPLES mid-sentence, and every one of these is a live cell's real
    # wording. The clause-opening constraint is the whole separation — measured
    # over every live spine + IF cell at 36 hits, 36 of them genuine stamps.
    assert not flags(llr={"Detail": "An APPROVED SN cited by zero SRs caps the bar."})
    assert not flags(sr={"Rationale": "So an AMENDED requirement drops the stage."})
    assert not flags(tc={"Method": "A stale file is DELETED in the same act."})
    assert not flags(tc={"Method": "Assert a RULED row does not render as a brief."})
    assert not flags(llr={"Detail": "Arm the comparison on the APPROVED half only."})
    # (4) THE REVIEW-CODE ARM IS GONE, and this is the case that removed it. A
    # `C-<HAT>-<n>` "review-round code" pattern shipped and measured 20 hits, 20
    # of them FALSE — every live occurrence names a hat-charter CLAUSE as the
    # standing constraint the row answers, which is the row's REASON. The token
    # carries no signal about which use it is; the FRAME around it does, and the
    # stamp arms above are what read a frame.
    assert not flags(
        sr={"Rationale": "C-MNT-3 gives each value exactly one definition."}
    )
    assert not flags(sr={"Rationale": "Hat-derived: C-SEC-2 asks for the list."})
    assert not flags(sr={"Rationale": "It must stay usable as it grows (C-UXE-2)."})
    # (5) A DATED PATH is a pointer, not a stamp: reporting "cites 2026-08-16"
    # about a plan filename names the wrong thing (12 of 76 measured date
    # matches). It is suppressed under BOTH date-bearing arms — the edit-stamp
    # arm used to be unguarded, so whether a pure pointer reported was decided by
    # how long the filename was.
    assert not flags(sr={"Rationale": "Design: docs/plans/2026-08-16-derivation.md"})
    assert not flags(sr={"Rationale": "Restated in docs/plans/2026-08-16-blind.md"})
    assert not flags(llr={"Rationale": "Moved to docs/archive/x.2026-07-20.md"})
    # Placeholder rows never report; a scaffold's example rows are a form.
    assert not flags(sr={"SR-ID": "SR-000", "Rationale": "Ruled 2026-08-13, OI-17."})

    # --- THE REVIEWED EXCEPTION LIST IS TOKEN-SCOPED --------------------------
    # An entry silences the ONE token it names. The cell-scoped key it replaced
    # was measured hiding 67 unadjudicated tokens over 22 rows behind entries
    # that each justified a single parenthetical.
    cell = {"Rationale": "OPEN (2026-08-16 round, F1). MINTED out of SR-140."}
    both = {
        trace.allow_key("SR-101", "Rationale", "2026-08-16"),
        trace.allow_key("SR-101", "Rationale", "MINTED"),
    }
    assert not flags(sr=dict(cell), allow=both)
    # Allowing ONE of the two leaves the other reported — the whole point.
    (msg,) = flags(
        sr=dict(cell), allow={trace.allow_key("SR-101", "Rationale", "2026-08-16")}
    )
    assert "'MINTED'" in msg and "'2026-08-16'" not in msg
    # A key naming the row, or the row and the cell, declares NOTHING: those are
    # the two shapes that over-suppressed, and they must not keep working.
    assert flags(sr=dict(cell), allow={"SR-101"})
    assert flags(sr=dict(cell), allow={"SR-101 Rationale"})
    # Wrong cell, wrong row: no match either way.
    assert flags(
        sr=dict(cell), allow={trace.allow_key("SR-101", "Title", "2026-08-16")}
    )

    # It reports the tier, row, cell and what it found — and says KEEP the reason.
    (msg,) = flags(sr={"Rationale": "REWORDED 2026-08-17 at sitting-3."})
    assert msg.startswith("SR SR-101 Rationale")
    assert "'REWORDED 2026-08-17'" in msg and "'sitting-3'" in msg
    assert "KEEP the reason" in msg


def test_the_off_spine_living_registries_get_the_same_citation_frame_sweep():
    # Sol-F2: `components.toml` and `external.toml` were SWEPT in the same pass
    # that guarded the four spine tiers, and then left unwatched — a clean state
    # nothing was watching. An adopter reads a component's notes and an entity's
    # description to learn what the system's neighbourhood IS, with no more
    # access to this repo's sittings than they have to its requirements.
    from conftest import load_script

    trace = load_script("trace")

    def flags(cmp=None, ext=None, allow=()):
        def rows(cells, key, rid):
            if cells is None:
                return []
            cells.setdefault(key, rid)
            return [cells]

        return trace.off_spine_advisories(
            rows(cmp, "CMP-ID", "CMP-101"), rows(ext, "EXT-ID", "EXT-101"), allow
        )

    assert flags(cmp={"Notes": "Cut at the 2026-08-13o merge, per OI-19."})
    assert flags(ext={"Notes": "A CLI is a CLI (owner merge, 2026-08-13o)."})
    assert flags(ext={"Description": "MINTED at sitting-2 out of the v1 frame."})
    (msg,) = flags(cmp={"Notes": "Ruled at sitting-3."})
    assert msg.startswith("CMP CMP-101 Notes") and "KEEP the reason" in msg
    # `Description` is NORMATIVE, so a bare date there is data, not a stamp —
    # the same split the spine tiers use between `Requirement` and `Rationale`.
    assert not flags(ext={"Description": "Cuts over on 2026-08-15 for adopters."})
    assert not flags(ext={"Notes": "They touch the SESSION, never the system."})
    assert not flags(cmp={"CMP-ID": "CMP-000", "Notes": "Ruled at sitting-3."})
    assert not flags(
        cmp={"Notes": "Ruled at sitting-3."},
        allow={trace.allow_key("CMP-101", "Notes", "sitting-3")},
    )


def test_the_if_reason_cells_are_swept_for_citation_frames_warn_only():
    # The IF tier's `Notes`/`SignalNote`, the pocket the Contract-only rule could
    # not see: 216 provenance tokens over 76 rows, 118 of them in `Notes`.
    from conftest import load_script

    trace = load_script("trace")

    def flags(row, allow=()):
        row.setdefault("IF-ID", "IF-101")
        return trace.if_note_advisories([row], allow)

    assert flags({"Notes": "MINTED 2026-08-15 (log 2026-08-15h) with LLR-173."})
    assert flags({"Notes": "One home is an owner ruling (2026-08-10, repo-lock D-6)."})
    assert flags({"SignalNote": "derived at the WI-443 conversion: unbounded."})
    # The Contract cell is NOT this arm's: one token, one finding, one home.
    assert not flags({"Contract": "consumes load(path) -> rows (WI-443)."})
    # A `Notes` cell ARGUING is that cell working correctly — the Contract arm's
    # connective and length rules must not follow it here.
    assert not flags({"Notes": "Declared because a copy diverges silently."})
    assert not flags({"Notes": "x" * 900})
    # Same hazards, same silence.
    assert not flags({"Notes": "The M-10 crossing is the counterpart here."})
    assert not flags({"Notes": "Kept rather than retired; the ruling stands."})
    # A placeholder row stays quiet, and so does a TOKEN-SCOPED exception — the
    # IF arm reads the same list under the same rule as the spine tiers, so a
    # cell-scoped key declares nothing here either.
    assert not flags({"IF-ID": "IF-000", "Notes": "Minted 2026-08-15."})
    assert not flags(
        {"Notes": "Minted 2026-08-15."},
        allow={trace.allow_key("IF-101", "Notes", "Minted 2026-08-15")},
    )
    assert flags({"Notes": "Minted 2026-08-15."}, allow={"IF-101 Notes"})


def test_the_if_rationale_cell_is_swept_too_since_wi523():
    # WI-523 (OI-65 ruled (iv)). WI-522's cleanup moved non-crossing content out
    # of `Contract` and into `Rationale` on 36 rows in one pass, taking that cell
    # from 1 user to 37 — and until this arm was widened, `Rationale` was the one
    # cell in the registry that nothing read. Driven over the 37 live cells when
    # the change landed: 0 findings, so the widening lights up the class without
    # handing anyone a cleanup list.
    from conftest import load_script

    trace = load_script("trace")

    assert "Rationale" in trace.IF_REASON_CELLS

    def flags(row, allow=()):
        row.setdefault("IF-ID", "IF-101")
        return trace.if_note_advisories([row], allow)

    # A citation frame in `Rationale` is now reported, on the same terms as
    # `Notes` — same severity, same wording, same exception list.
    assert flags({"Rationale": "MINTED 2026-08-15 (log 2026-08-15h) with LLR-173."})
    assert flags({"Rationale": "Split at the WI-443 conversion."})
    # And the cell doing its job stays silent: `Rationale` is where the argument
    # the Contract cell may not hold is SUPPOSED to live, so arguing, connectives
    # and length must not fire here.
    assert not flags({"Rationale": "Declared because a copy diverges silently."})
    assert not flags({"Rationale": "Kept rather than retired; the ruling stands."})
    assert not flags({"Rationale": "x" * 900})
    # Placeholder rows and token-scoped exceptions behave as they do for `Notes`.
    assert not flags({"IF-ID": "IF-000", "Rationale": "Minted 2026-08-15."})
    assert not flags(
        {"Rationale": "Minted 2026-08-15."},
        allow={trace.allow_key("IF-101", "Rationale", "Minted 2026-08-15")},
    )


def test_a_work_item_citation_is_found_whatever_its_capitalisation():
    # WI-523 (OI-65 ruled (iv)). `IF-082`/`IF-083`/`IF-084` carried `wI-280` in
    # `Notes` through three rounds of this arm without being seen, because the
    # detector was case-sensitive. A detector a shift key defeats is not a
    # detector; the token SHAPE is unchanged, only the case-blindness is new.
    from conftest import load_script

    trace_text = load_script("trace_text")

    for spelling in ("WI-280", "wI-280", "Wi-280", "wi-280"):
        assert trace_text._WI_TOKEN_RE.search(
            "sink - {} slice 11: the import moved.".format(spelling)
        ), spelling

    # Still a bounded token, not a substring match: no digits, no word boundary,
    # no finding.
    assert not trace_text._WI_TOKEN_RE.search("SWI-280 is a different token")
    assert not trace_text._WI_TOKEN_RE.search("WI- is not an id")


def test_a_condition_stated_outside_the_ears_patterns_warns_but_never_gates():
    # process.md section 3, "The statement pattern is EARS". Measured over this
    # repo's 70 SRs before shipping: two rows opened on a non-EARS condition
    # ("Before ...", "For ..."), both re-worded in the same change, so the rule
    # guards zero-to-zero rather than handing anyone a cleanup list.
    from conftest import load_script

    trace = load_script("trace")

    def flags(text, **cells):
        cells["Requirement"] = text
        cells.setdefault("SR-ID", "SR-101")
        return trace.ears_advisories([cells])

    # The four condition keywords open a conforming row, in any case.
    for opening in (
        "When a run starts,",
        "While a run is live,",
        "If the file is missing, then",
        "Where the layer is enabled,",
    ):
        assert not flags(f"{opening} the system shall exit nonzero.")
    # So does the ubiquitous pattern -- a bare subject, whatever its determiner.
    for subject in (
        "The system",
        "Every kit script",
        "A re-sync",
        "Any durable record",
    ):
        assert not flags(f"{subject} shall exit nonzero.")

    # A condition dressed in some OTHER keyword is the finding: the same
    # condition, in the one place no reader and no tool looks for it.
    assert flags("Before the run integrates, the system shall exit nonzero.")
    assert flags("For contested work, the system shall exit nonzero.")
    assert flags("During an unattended run, the system shall exit nonzero.")

    # A Drafted row IS in scope, unlike the gating form rules beside it: an
    # opening is finished the moment it is written, and both rows this rule
    # found at landing were Drafted.
    assert flags("Before the run integrates, the system shall exit.", Status="Drafted")
    # An example row and an empty cell are not.
    assert not flags("Before x, the system shall y.", **{"SR-ID": "SR-000"})
    assert not flags("")

    # ADVISORY, always: the pipe never joins the exit code.
    assert isinstance(flags("Before x, the system shall y."), list)


def test_a_requirement_states_one_testable_obligation():
    # WI-328. The stand-alone rule says a row must not carry its own HISTORY;
    # this says what is left must be DECIDABLE — 29148's individual-requirement
    # characteristics, restricted to the half a checker settles without judgement.
    from conftest import load_script

    trace = load_script("trace")

    def flags(sr=None, llr=None, tc=None):
        def rows(cells, key, rid):
            if cells is None:
                return []
            cells.setdefault(key, rid)
            return [cells]

        return trace.form_findings(
            rows(sr, "SR-ID", "SR-101"),
            rows(llr, "LLR-ID", "LLR-101"),
            rows(tc, "TC-ID", "TC-101"),
        )

    # SINGULAR — measured at 13 of 110, the only pattern with a real population.
    assert flags(sr={"Requirement": "x shall a. y shall b."})
    # UNAMBIGUOUS — 'shall' is the obligation; the rest are goal/permission/fact.
    assert flags(sr={"Requirement": "trace.py should exit nonzero."})
    assert flags(sr={"Requirement": "trace.py shall exit; it will also warn."})
    # VERIFIABLE — an actorless passive names nobody to fail.
    assert flags(sr={"Requirement": "The gate shall be computed at each run."})
    # UNFALSIFIABLE terms and OPEN-ENDED scope, in any registry.
    assert flags(sr={"Requirement": "x shall be robust."})
    assert flags(sr={"AcceptanceCriteria": "Overhead stays minimal."})
    assert flags(llr={"Detail": "Handles the cases, such as a missing file."})
    assert flags(tc={"Expected": "Exit 0, etc."})
    # An LLR decomposes; it does not re-state the obligation a tier below where
    # it is traced.
    assert flags(llr={"Detail": "The loader shall reject a malformed row."})

    # The NEGATIVE half. A correct requirement, and the shapes that look like
    # defects and are not — this is what keeps the rule from crying wolf.
    assert not flags(sr={"Requirement": "trace.py shall exit nonzero on an orphan."})
    # A multi-clause AC enumerates how ONE obligation is checked. 110 rows do
    # this and gating on it would be the check_doc_refs failure again.
    assert not flags(
        sr={
            "Requirement": "trace.py shall join the registries.",
            "AcceptanceCriteria": "--strict exits 0 on a linked chain and 1 when "
            "any SR lacks an LLR, any LLR lacks a parent, or any SN lacks an SR; "
            "the orphan list names each at-fault id.",
        }
    )
    # Passive WITH a named actor is fine — the actor is what was missing.
    assert not flags(
        sr={"Requirement": "The gate shall be computed by spine_rules.py."}
    )
    # ZERO 'shall' is NOT a finding. A placeholder, or a project whose obligation
    # keyword is not the English word "shall", is following a different convention
    # rather than making an error — and this rule ships downstream, where flagging
    # it would red a legitimate scaffold on its first re-sync.
    assert not flags(sr={"Requirement": "x does a."})
    # 'must' likewise: 29148 reserves `shall`, but a repo that standardised on
    # 'must' would have EVERY row flagged, which is the cry-wolf failure.
    assert not flags(sr={"Requirement": "trace.py must exit nonzero."})
    # A Drafted row is pre-approval and process.md §4 already exempts it from
    # the decomposition rules — 'TBD' in a Drafted acceptance criterion is what
    # Drafted MEANS, so flagging it would break the state's whole purpose.
    assert not flags(
        sr={
            "Status": "Drafted",
            "Requirement": "x shall a.",
            "AcceptanceCriteria": "TBD",
        }
    )
    assert flags(
        sr={
            "Status": "Approved",
            "Requirement": "y shall b.",
            "AcceptanceCriteria": "TBD",
        }
    )
    # A Rationale legitimately says 'would' (the consequence of the alternative
    # that lost) and an AC legitimately says 'may' (a permitted outcome), so the
    # modal rule is scoped to Requirement ALONE.
    assert not flags(sr={"Rationale": "Polling would miss a mid-run amendment."})
    assert not flags(sr={"AcceptanceCriteria": "The run may emit either form."})
    # 'minimal' is vague; 'minimum' inside a measured bound is not vocabulary the
    # rule owns, and a placeholder row never gates a scaffold.
    assert not flags(sr={"SR-ID": "SR-000", "Requirement": "Example shall shall."})
    # It reports the registry, the row, the cell, and what it found.
    (msg,) = flags(sr={"Requirement": "x shall a and y shall b."})
    assert msg.startswith("SR SR-101 Requirement carries 2 'shall'")


def test_a_child_that_rewords_its_parent_warns_but_never_gates():
    # WI-328. 'Decompose, don't paraphrase' made visible. Lexical overlap is a
    # HEURISTIC — 38 of 118 LLRs trip it and most are legitimate, which is
    # precisely why it warns forever instead of gating.
    from conftest import load_script

    trace = load_script("trace")

    sr = {
        "SR-ID": "SR-101",
        "Requirement": "The exporter shall write records to a comma separated "
        "values file using an atomic rename.",
    }
    echo = {
        "LLR-ID": "LLR-101",
        "SR-Refs": "SR-101",
        "Detail": "The exporter writes records to a comma separated values file "
        "using an atomic rename.",
    }
    assert trace.paraphrase_advisories([sr], [echo])
    # A real decomposition names the module and the mechanism, so it does NOT
    # trip: the check must reward the thing the process actually asks for.
    real = {
        "LLR-ID": "LLR-102",
        "SR-Refs": "SR-101",
        "Detail": "src/export/io.write_atomic buffers to <path>.tmp then renames; "
        "the temp is removed on any error and the rename is atomic within one "
        "volume.",
    }
    assert not trace.paraphrase_advisories([sr], [real])
    # An SR whose Rationale merely re-words its own Requirement.
    dup = dict(
        sr,
        Rationale="The exporter shall write records to a comma "
        "separated values file using an atomic rename.",
    )
    assert trace.paraphrase_advisories([dup], [])
    assert not trace.paraphrase_advisories(
        [dict(sr, Rationale="A half-written file reads as valid to the next run.")],
        [],
    )
    # And it NEVER gates, whatever it finds — the whole point of the tier.
    findings = trace.Findings()
    for attr in vars(trace.Findings()):
        setattr(findings, attr, None)
    findings.paraphrase = trace.paraphrase_advisories([sr], [echo])
    assert findings.paraphrase


def test_the_llr_carries_a_rationale_column_and_it_is_optional():
    # WI-328. `Detail` was the LLR's ONLY prose cell, so the what, the why, the
    # ruled-out alternatives and the authoring history were structurally forced
    # into one field — measured: 75 of 118 Details under 300 chars, but the 24
    # walls (one over 3,000) all in the rows whose reasons were richest. Rationale
    # is a requirement attribute at EVERY level in 29148; the SR had one and the
    # LLR did not, and that asymmetry was the bug.
    from conftest import ROOT, load_script

    trace = load_script("trace")

    # The column exists in BOTH the shipped template and the kit's own registry.
    # Read through the CARRIER, which is what "the registry has this column"
    # means now: TOML has no header, so the question is whether the key is set
    # — by the template's `-000` schema row, and by at least one live row. The
    # "sits beside Detail" half is retired with the header: key order inside a
    # TOML table carries no meaning, so asserting it would pin a non-fact.
    carrier = load_script("spine_carrier")
    for path in (
        ROOT / "project-trajectory/registries/low-level-requirements.template.toml",
        ROOT / "docs/requirements/low-level-requirements.toml",
    ):
        columns = carrier.columns(path, "LLR-ID")
        assert columns, path  # an empty column set would make this vacuous
        assert "Rationale" in columns, path
        assert "Detail" in columns, path

    # The deliberate asymmetry: required on the SR, optional on the LLR. A short
    # decomposition row's why IS its parent SR's, so requiring one everywhere
    # would manufacture the restatement the column exists to prevent.
    assert "Rationale" in trace.REQUIRED_FIELDS["SR"]
    assert "Rationale" not in trace.REQUIRED_FIELDS["LLR"]

    # Which means an LLR with no Rationale is clean...
    bare = {
        "LLR-ID": "LLR-101",
        "SR-Refs": "SR-1",
        "Title": "t",
        "Module": "m",
        "CodeSymbol": "c",
        "Detail": "d",
        "Status": "Approved",
    }
    assert trace.schema_findings("LLR", [bare]) == []
    # ...and an SR with an empty one is not (zero-to-zero: all 110 carry one).
    sr = {
        "SR-ID": "SR-101",
        "Title": "t",
        "SN-Refs": "SN-1",
        "Requirement": "r",
        "Rationale": "",
        "AcceptanceCriteria": "a",
        "Priority": "1",
        "Verification": "Test",
        "Status": "Approved",
    }
    (found,) = trace.schema_findings("SR", [sr])
    assert "empty required field Rationale" in found

    # A pre-migration registry that lacks the COLUMN entirely still validates —
    # the same graceful path TC's Evidence column documents (ADOPTING.md §6).
    del bare["Detail"]
    legacy = trace.schema_findings("LLR", [bare])
    assert legacy == ["LLR LLR-101 has empty required field Detail"], legacy


def test_duplicate_of_malformed_id_reports_duplicated():
    # WI-106 L4: a malformed id appearing twice must report "duplicated" for its
    # second occurrence, not "malformed" a second time.
    from conftest import load_script

    trace = load_script("trace")
    found = trace.integrity_findings("SR", [{"SR-ID": "SR-bad"}, {"SR-ID": "SR-bad"}])
    assert any("malformed" in f for f in found), found
    assert any("duplicated" in f for f in found), found
    # A well-formed duplicate still reports only "duplicated" (no regression).
    dup = trace.integrity_findings("SR", [{"SR-ID": "SR-001"}, {"SR-ID": "SR-001"}])
    assert dup == ["SR id SR-001 is duplicated"], dup


# --- WI-129: LLR/TC status-coherence warn (registry lint) ---------------------
def test_llr_status_coherence_predicate():
    # Done-when 1-3: the coherence predicate itself, unit-level.
    from conftest import load_script

    trace = load_script("trace")

    def warns(llrs, tcs):
        return trace.llr_status_advisories(llrs, tcs)

    # RE-POINTED AT D-9 STEP 5, NOT DROPPED: this lint's subject is a
    # BELOW-APPROVED LLR, and the fold left exactly one such value (`Drafted`),
    # so the fixture moves onto it rather than onto the `Approved` the raw value
    # map would have produced — which would have made the test assert its own
    # negative case.
    impl = {"LLR-ID": "LLR-010", "SR-Refs": "SR-010", "Status": "Drafted"}
    ver_tc = {"TC-ID": "TC-010", "Verifies": "SR-010;LLR-010", "Status": "Approved"}

    # (1) Drafted LLR, sole citing TC Approved -> exactly the warn.
    found = warns([impl], [ver_tc])
    assert len(found) == 1, found
    assert "LLR LLR-010 reads 'Drafted'" in found[0]
    assert "every citing TC is Approved" in found[0]

    # (1, cont.) Lifting the LLR to Approved silences it.
    assert warns([{**impl, "Status": "Approved"}], [ver_tc]) == []

    # (3) Case-insensitive via the shared is_approved() predicate: a lowercase
    # 'approved' LLR is silent, and a lowercase citing TC still counts as approved.
    assert warns([{**impl, "Status": "approved"}], [ver_tc]) == []
    assert len(warns([impl], [{**ver_tc, "Status": "approved"}])) == 1

    # (2) Quiet: one citing TC is not Approved -> not "every citing TC".
    planned_tc = {"TC-ID": "TC-011", "Verifies": "LLR-010", "Status": "Drafted"}
    assert warns([impl], [ver_tc, planned_tc]) == []

    # (2) Quiet: an LLR with no citing TC is the orphan rules' job, not this lint's.
    assert warns([impl], []) == []


def test_a_FOUNDED_llr_is_exempt_from_the_status_advisory():
    # THE EXEMPTION MOVED AT D-9 STEPS 7/8, and it moved for the reason it
    # existed. It named `Modified`, whose below-`Approved` status was
    # DELIBERATE — a post-approval amendment awaiting re-attest — so the
    # "lift to Approved" nag would have told the owner to erase the marker the
    # sitting needed. That word retired; `Founded` reads ABOVE `Approved`, so
    # a Founded LLR has nothing to lift and the nag would tell it to move DOWN
    # the ladder. Mutation proof unchanged in shape: the same row as `Drafted`
    # DOES warn, so the exemption is the value, not a broken lint.
    from conftest import load_script

    trace = load_script("trace")
    ver_tc = {"TC-ID": "TC-010", "Verifies": "SR-010;LLR-010", "Status": "Approved"}
    founded = {"LLR-ID": "LLR-010", "SR-Refs": "SR-010", "Status": "Founded"}
    assert trace.llr_status_advisories([founded], [ver_tc]) == []
    impl = {**founded, "Status": "Drafted"}
    assert len(trace.llr_status_advisories([impl], [ver_tc])) == 1
    # ...and the RETIRED word is NOT exempt any more, which is the direction
    # that would otherwise go unnoticed: a `Modified` LLR is out-of-vocabulary
    # and the integrity floor names it, so this lint has no reason to be quiet
    # about it as well.
    stale = {**founded, "Status": "Modified"}
    assert len(trace.llr_status_advisories([stale], [ver_tc])) == 1


def test_llr_status_advisory_is_warn_only_and_reported(scaffold):
    # Done-when 1+4: a below-`Approved` LLR-001 under an `Approved` TC-001 makes
    # trace emit the warn on stdout and in the report — but it never changes the
    # --strict or --strict-integrity exit code.
    #
    # THE FIXTURE IS SET HERE RATHER THAN SHIPPED BY `make_minimal_project`
    # (D-9 step 5). The shared project used to ship `Planned`, which was
    # below-`Verified` AND non-capping; the fold left one below-approval value
    # (`Drafted`) and that one DOES cap the derived gate, so leaving it in the
    # shared fixture would have dropped the gate for every test built on it.
    make_minimal_project(scaffold)
    llr_csv0 = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    llr_csv0.write_text(
        llr_csv0.read_text(encoding="utf-8").replace(
            ",(see TC),Approved", ",(see TC),Drafted"
        ),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARNING (advisory): LLR LLR-001 reads 'Drafted'" in proc.stdout
    assert "llr-status-advisories=1" in proc.stdout
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "Status-coherence advisories" in report
    assert "LLR-001 reads 'Drafted'" in report

    # --strict-integrity likewise unaffected (the warn never joins the integrity set).
    proc2 = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc2.returncode == 0, proc2.stdout + proc2.stderr

    # Lifting LLR-001 to Approved silences the warn.
    llr_csv = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    llr_csv.write_text(
        llr_csv.read_text(encoding="utf-8").replace(",Drafted", ",Approved"),
        encoding="utf-8",
    )
    proc3 = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc3.returncode == 0, proc3.stdout + proc3.stderr
    assert "reads 'Drafted'" not in proc3.stdout
    assert "llr-status-advisories" not in proc3.stdout
    report3 = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "None. No unlifted LLRs." in report3


# --- WI-146(a): the --approve batch-scoped approval hierarchy view ---------
# A generated SN->SR->LLR/TC tree carrying the prose an approver needs (Requirement/
# AC, LLR Detail, TC Method/Expected, cited rubric), scoped by an SR-id list or a
# phase tag. A generator mode: it runs no checks and always exits 0.

# An SR with a Phase cell and a rubric citation, still traced to LLR-001/TC-001.
PHASED_RUBRIC_SR = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status,Phase\n"
    'SR-001,Addition,SN-001,"The system shall add two numbers.",'
    '"Realizes SN-001.","Judged against docs/rubrics/adder.md",,'
    "M,Critique,Approved,v9\n"
)


def test_approval_sr_list_emits_prose(scaffold):
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--approve", "SR-001"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    assert "# Approval hierarchy" in out and "scope: SR-001" in out
    assert "1 SR(s)" in out
    assert "SR-001" in out and "Addition" in out
    # The stakeholder need's own prose heads its subtree, not a bare SN id
    # (WI-146 REVIEW-A): Need / Why it matters / Acceptance intent from the SN row.
    assert "## SN-001" in out
    assert "**Need.** Add two numbers." in out
    assert "**Why it matters.** Demo." in out
    assert "**Acceptance intent.** add(1,2) gives 3." in out
    assert "The system shall add two numbers." in out  # SR Requirement prose
    assert "Pure function: two numbers -> sum." in out  # LLR Detail prose
    assert "TC-001" in out and "Satisfies SR-001 AcceptanceCriteria" in out  # TC


def test_approval_phase_scope_and_rubric(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        PHASED_RUBRIC_SR, encoding="utf-8"
    )
    proc = run_py(["scripts/trace.py", "--approve", "v9"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SR-001" in proc.stdout and "Addition" in proc.stdout
    assert "**Rubrics.** docs/rubrics/adder.md" in proc.stdout
    # A non-matching phase is REFUSED, not rendered empty (D-9 §F2). Until this
    # hardening it fell through to a brief that read "there is nothing to
    # approve" at exit 0 — the most expensive way for this tool to be wrong,
    # because a typo, a retired phase tag or an unknown reserved word all
    # produced a document a human then signed.
    empty = run_py(["scripts/trace.py", "--approve", "v1"], cwd=scaffold)
    assert empty.returncode != 0
    combined = empty.stdout + empty.stderr
    assert "matches no SR" in combined and "refusing to emit an empty" in combined
    # ...and NOTHING is written to stdout: the old behaviour emitted a document
    # whose own body said "no SR matched this scope", which is a brief a human
    # can read and act on. A refusal must leave no artifact at all.
    assert empty.stdout == ""


def test_approval_out_writes_linkable_file(scaffold):
    make_minimal_project(scaffold)
    proc = run_py(
        ["scripts/trace.py", "--approve", "SR-001", "--out", "docs/ratify/x.md"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    written = (scaffold / "docs" / "ratify" / "x.md").read_text(encoding="utf-8")
    assert "# Approval hierarchy" in written
    assert "The system shall add two numbers." in written
    assert "trace: wrote approval view" in proc.stdout


# --- WI-081 Slice C: the render/exit extraction + M8 pre-indexing --------------
# The report render/console/exit block moved out of main() into render_report /
# render_console / exit_code (byte-identity pinned by test_trace_golden.py). These
# unit-check the two new pure helpers the golden net does not isolate: the M8
# ref-bucket index and the gate exit-code policy.


def test_bucket_by_ref_groups_preserves_order_and_parses_multi():
    from conftest import load_script

    trace = load_script("trace")
    rows = [
        {"LLR-ID": "LLR-001", "SR-Refs": "SR-001"},
        {"LLR-ID": "LLR-002", "SR-Refs": "SR-002"},
        {"LLR-ID": "LLR-003", "SR-Refs": "SR-001;SR-002"},
    ]
    index = trace._bucket_by_ref(rows, "SR-Refs")
    # Grouped by each referenced id, children kept in input order.
    assert [r["LLR-ID"] for r in index["SR-001"]] == ["LLR-001", "LLR-003"]
    assert [r["LLR-ID"] for r in index["SR-002"]] == ["LLR-002", "LLR-003"]
    # A row whose ref cell names two parents appears under BOTH (cell parsed once).
    assert rows[2] in index["SR-001"] and rows[2] in index["SR-002"]
    # An id nobody references is simply absent (no empty buckets); a blank/absent
    # ref cell contributes nothing.
    assert "SR-999" not in index
    assert trace._bucket_by_ref([{"SR-Refs": ""}, {"SR-Refs": None}], "SR-Refs") == {}


# The attributes `exit_code` reads, NAMED — the readable statement of the gate's
# input schema, and the thing a reviewer checks. `_exit_code_attrs` derives the
# same set from the function itself, and the two are asserted equal below.
EXIT_CODE_INPUTS = {
    "orphans",
    "status_findings",
    "integrity",
    "placeholders",
    "schema",
    "budget_findings",
    "module_findings",
    "component_findings",
    "interface_backlink_findings",
    "frame_backlink_findings",
    "hat_dangling",
    "provenance",
    "form",
}


def _exit_code_attrs(trace):
    """Every `findings.<attr>` `trace.exit_code` actually reads.

    2026-08-21 review, Sol 9: this stub used to be a HAND-MAINTAINED MIRROR of
    that function's reads, and `trace.Findings` is a bare class with no
    defaults, so the two were independent schemas. It drifted the moment
    `exit_code` gained an arm (WI-484): the stub lacked the attribute and the
    tests below raised `AttributeError` instead of testing the rule — and
    because this module is outside the smoke tier, the commit bar stayed green
    and the FULL suite found it later. Deriving the set means a new arm can no
    longer crash these tests, and `test_the_stub_matches_what_exit_code_reads`
    makes the addition visible rather than silent."""
    import ast
    import inspect

    tree = ast.parse(inspect.getsource(trace.exit_code).lstrip())
    return {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "findings"
    }


def _findings_stub(trace, **overrides):
    """A Findings bag with every attribute exit_code reads defaulted to empty."""
    f = trace.Findings()
    for attr in EXIT_CODE_INPUTS | _exit_code_attrs(trace):
        setattr(f, attr, [])
    for attr, value in overrides.items():
        setattr(f, attr, value)
    return f


def test_the_stub_matches_what_exit_code_reads():
    """One schema, asserted from both ends."""
    from conftest import load_script

    trace = load_script("trace")
    assert _exit_code_attrs(trace) == EXIT_CODE_INPUTS, (
        "trace.exit_code's inputs changed. Add the new arm to EXIT_CODE_INPUTS "
        "in the same edit and give it a test — a gate arm nothing exercises is "
        "an arm nobody has seen fire."
    )


def test_exit_code_gate_policy():
    import argparse

    from conftest import load_script

    trace = load_script("trace")

    def ns(strict=False, strict_integrity=False):
        return argparse.Namespace(strict=strict, strict_integrity=strict_integrity)

    # --strict fails on any gated finding (orphans here)...
    orphaned = _findings_stub(trace, orphans=["SR-002 has no test (TC)"])
    assert trace.exit_code(orphaned, ns(strict=True)) == 1
    # ...and on integrity (integrity is in the strict set too).
    bad_id = _findings_stub(trace, integrity=["SR id SR-001 is duplicated"])
    assert trace.exit_code(bad_id, ns(strict=True)) == 1
    # --strict-integrity fails on integrity...
    assert trace.exit_code(bad_id, ns(strict_integrity=True)) == 1
    # ...but the integrity floor ignores orphans (a gate criterion, not always-invalid).
    assert trace.exit_code(orphaned, ns(strict_integrity=True)) == 0
    # No gating flag -> always 0, even with findings present.
    loud = _findings_stub(trace, orphans=["x"], integrity=["y"], status_findings=["z"])
    assert trace.exit_code(loud, ns()) == 0


# --- Re-tier v2 R2/R3: the two warn-first tiering detectors -------------------
# Owner ruling 2026-08-15 (log `2026-08-15p`). Both report a TIERING smell — a
# requirement that decided which artifact carries a capability, and a row whose
# fan of children says it merged several decisions — and both stay advisory
# forever, because clearing them means re-writing requirements, which is the
# campaign's schedule and not the checker's.


def test_a_row_stating_two_verification_methods_warns():
    """The verification-coherence lint (log `2026-08-16p`). The occasion: two
    rows flipped `Critique`->`Test` when their anchors were bound to tests, and
    their prose went on demanding an APPROVE verdict from rubrics that by then
    declared themselves RETIRED. Every strict gate passed at rc=0 for three
    weeks, because nothing compared the `Verification` field against the prose
    that says how anyone would know the row is satisfied."""
    trace = load_script("trace")

    # The defect, in both cells that can carry it.
    ac_rot = {
        "SR-ID": "SR-101",
        "Verification": "Test",
        "AcceptanceCriteria": "A fresh CRITIQUE session returns APPROVE citing "
        "numbered anchors.",
    }
    rationale_rot = {
        "SR-ID": "SR-102",
        "Verification": "Test",
        "Rationale": "Acceptance is adjudicated by an independent critical eye "
        "against a written rubric instead.",
    }
    assert len(trace.verification_coherence_advisories([ac_rot])) == 1
    assert len(trace.verification_coherence_advisories([rationale_rot])) == 1
    assert "AcceptanceCriteria" in trace.verification_coherence_advisories([ac_rot])[0]
    assert "Rationale" in trace.verification_coherence_advisories([rationale_rot])[0]

    # A row that DECLARES Critique is naming its own instrument, not contradicting
    # itself — the lint runs one direction only.
    assert (
        trace.verification_coherence_advisories(
            [dict(ac_rot, **{"Verification": "Critique"})]
        )
        == []
    )

    # The NEGATIVE half, and the reason the vocabulary is case-split: lowercase
    # "verdict"/"approve" are ordinary prose the corpus really uses (SR-137 and
    # SR-148 both say "the integrator's verdict gate" about a subsystem), so
    # matching them case-insensitively would put standing false accusations on
    # correct rows and teach an author to skip the pipe.
    for prose in (
        "Refusals fire at the integrator's verdict gate and intake's adjudication arm.",
        "The owner approves the split before it lands.",
    ):
        clean = {"SR-ID": "SR-103", "Verification": "Test", "Rationale": prose}
        assert trace.verification_coherence_advisories([clean]) == []

    # `Requirement` is deliberately NOT scanned: SR-040's shall enumerates the
    # session phases a coordinator routes (PLAN/BUILD/.../CRITIQUE), where the
    # word NAMES a phase rather than claiming a verdict.
    phase_list = {
        "SR-ID": "SR-104",
        "Verification": "Test",
        "Requirement": "The coordinator shall route each phase "
        "(PLAN/BUILD/REVIEW-A/CRITIQUE) through its declared template.",
    }
    assert trace.verification_coherence_advisories([phase_list]) == []

    # A row with no declared method cannot contradict one.
    assert (
        trace.verification_coherence_advisories([dict(ac_rot, **{"Verification": ""})])
        == []
    )
    # A `-000` example row is a blank form, not a requirement.
    assert (
        trace.verification_coherence_advisories([dict(ac_rot, **{"SR-ID": "SR-000"})])
        == []
    )


def test_a_requirement_that_names_a_concrete_artifact_warns():
    from conftest import load_script

    trace = load_script("trace")

    # A bare script name and a path-qualified one both read as one artifact
    # binding stated in the tier that has no business holding it.
    bare = {
        "SR-ID": "SR-101",
        "Requirement": "trace.py shall exit nonzero when an orphan exists.",
    }
    pathed = {
        "SR-ID": "SR-102",
        "Requirement": "The harness shall run scripts/check.py at every commit.",
    }
    assert len(trace.sr_artifact_advisories([bare])) == 1
    assert len(trace.sr_artifact_advisories([pathed])) == 1
    assert "'trace.py'" in trace.sr_artifact_advisories([bare])[0]
    assert "'scripts/check.py'" in trace.sr_artifact_advisories([pathed])[0]

    # The NEGATIVE half, and the reason the rule can be this cheap: the signal is
    # the literal `.py` EXTENSION, never the letters. A word that merely ends in
    # "py" is not an artifact, and a rule that said otherwise would fire on
    # ordinary English and get scrolled past (the check_doc_refs lesson).
    for word in ("numpy", "happy", "occupy", "copy"):
        clean = {
            "SR-ID": "SR-103",
            "Requirement": "The delivered harness shall be {} to run.".format(word),
        }
        assert trace.sr_artifact_advisories([clean]) == []
    # Capability voice — the wording R2 asks for — is silent.
    assert (
        trace.sr_artifact_advisories(
            [
                {
                    "SR-ID": "SR-104",
                    "Requirement": "The delivered harness shall refuse a commit "
                    "whose registries carry an orphan.",
                }
            ]
        )
        == []
    )
    # A `-000` example row is a blank form, not a requirement.
    assert trace.sr_artifact_advisories([dict(bare, **{"SR-ID": "SR-000"})]) == []


def test_a_recorded_waiver_silences_the_row_but_not_a_shared_artifact():
    from conftest import load_script

    trace = load_script("trace")

    waived = {
        "SR-ID": "SR-101",
        "Requirement": "trace.py shall exit nonzero when an orphan exists.",
        "Rationale": "Recorded waiver: the carrier and the name it "
        "verifies are one contract, and splitting them separates a claim from "
        "the proof that makes it checkable.",
    }
    # The recorded per-row valve — the SAME declared marker the one-`shall`
    # waivers use, not a second grammar an author has to learn.
    assert trace.sr_artifact_advisories([waived]) == []
    # RENAMED FROM `13v`, a DECISION ID, which the citation-frame rule bans from
    # the very cell this valve is written in — and which named a ruling of THIS
    # repo that no adopting project can read. The retired token no longer works.
    assert trace.sr_artifact_advisories(
        [dict(waived, Rationale="One-shall waiver (13v): one contract.")]
    )
    # And the COLON earns its keep: prose ABOUT a waiver is not a claim of one.
    # `\b13v\b`'s only two live hits were rows saying the waiver was SPENT.
    assert trace.sr_artifact_advisories(
        [dict(waived, Rationale="The recorded waiver covered one shall and is SPENT.")]
    )
    # An unwaived row with the same text is not silenced, so the suppression is
    # the Rationale's doing and not an accident of the token regex.
    assert trace.sr_artifact_advisories(
        [{k: v for k, v in waived.items() if k != "Rationale"}]
    )

    # The SECOND census, deliberately not folded into the first: two rows sharing
    # one artifact identity is a different defect (R1's "one home per method"),
    # and a waiver excusing one row's naming says nothing about it — so WAIVED
    # ROWS STILL COUNT here.
    other = {
        "SR-ID": "SR-102",
        "Requirement": "The launcher shall invoke trace.py before every push.",
    }
    shared = [
        a for a in trace.sr_artifact_advisories([waived, other]) if "all name" in a
    ]
    assert len(shared) == 1
    assert "SR-101" in shared[0] and "SR-102" in shared[0] and "'trace.py'" in shared[0]
    # One row naming one artifact is not a shared identity.
    assert [a for a in trace.sr_artifact_advisories([other]) if "all name" in a] == []


def test_a_need_whose_acceptance_names_a_concrete_artifact_warns():
    """The SN arm of the artifact-voice rule (owner directive 2026-08-18).

    Rows arrive in the `spine_carrier.load_needs` shape — lower-case `id` and
    cells — NOT the `<TIER>-ID`/Title-case shape the SR rules read, so the
    fixtures here are written that way deliberately.
    """
    from conftest import load_script

    trace = load_script("trace")

    script = {
        "id": "SN-101",
        "acceptance": "`trace.py --strict` reports zero orphans across the spine.",
    }
    config = {
        "id": "SN-102",
        "acceptance": "The toolchain is declared once in `docs/stack.ini`.",
    }
    page = {"id": "SN-103", "acceptance": "The root `PROJECT_STATE.html` renders it."}
    # The vocabulary is WIDER than the SR arm's `.py` anchor on purpose: the need
    # tier's instruments are mostly configs and generated pages, not scripts.
    for row in (script, config, page):
        assert len(trace.sn_artifact_advisories([row])) == 1
    assert "'trace.py'" in trace.sn_artifact_advisories([script])[0]
    assert "'docs/stack.ini'" in trace.sn_artifact_advisories([config])[0]
    assert "'PROJECT_STATE.html'" in trace.sn_artifact_advisories([page])[0]

    # CONDITION voice — the wording the rule asks for — is silent.
    assert (
        trace.sn_artifact_advisories(
            [
                {
                    "id": "SN-104",
                    "acceptance": "The strict traceability check reports zero "
                    "orphans across the joined spine.",
                }
            ]
        )
        == []
    )
    # A word that merely ends in a vocabulary suffix is not an artifact: the
    # signal is the dotted EXTENSION, the same rule the SR arm is built on.
    for word in ("numpy", "happy", "minimal", "shell", "sh"):
        assert (
            trace.sn_artifact_advisories(
                [{"id": "SN-105", "acceptance": "It stays {} to run.".format(word)}]
            )
            == []
        )
    # A `-000` example row is a blank form, not a need.
    assert trace.sn_artifact_advisories([dict(script, id="SN-000")]) == []
    # An empty or absent acceptance cell reports nothing rather than crashing.
    assert trace.sn_artifact_advisories([{"id": "SN-106"}]) == []
    assert trace.sn_artifact_advisories([{"id": "SN-106", "acceptance": "  "}]) == []


def test_the_need_arm_scans_acceptance_only_and_excludes_markdown():
    from conftest import load_script

    trace = load_script("trace")

    # `need` belongs to check_need_form.py, which reports internal paths there on
    # SN-033's commission. Scanning it here too would report one token from two
    # checks — the anti-duplication rule applied to the detectors themselves.
    assert (
        trace.sn_artifact_advisories(
            [{"id": "SN-101", "need": "A reviewer can trust `trace.py`."}]
        )
        == []
    )
    # `why` is exempt for the reason `Rationale` is exempt at SR: it is the reason
    # cell, and it is where this rule's own waiver is recorded.
    assert (
        trace.sn_artifact_advisories(
            [{"id": "SN-101", "why": "Because `trace.py` would otherwise rot."}]
        )
        == []
    )
    # `.md` is EXCLUDED, and that exclusion was measured rather than assumed: a
    # markdown name is rarely the INSTRUMENT that observes the condition, and a
    # markdown name that IS a citation is forbidden outright by the provenance
    # rule rather than waived here — so this arm would only ever double-report.
    assert (
        trace.sn_artifact_advisories(
            [
                {
                    "id": "SN-102",
                    "acceptance": "Spec of record: `docs/concurrency-restructure.md`.",
                }
            ]
        )
        == []
    )


def test_a_recorded_why_waiver_silences_a_need_and_there_is_no_shared_census():
    from conftest import load_script

    trace = load_script("trace")

    waived = {
        "id": "SN-101",
        "acceptance": "`docs/process.toml` holds every process dial.",
        "why": "Recorded waiver: the single-home promise IS a promise "
        "about this file, so a class-voice rewrite would delete the need.",
    }
    # The waiver home at SN is `why` — the tier's reason cell, since the need
    # schema (`SPINE_TIER_KEYS['SN-ID']`) carries no `Rationale` — and the marker
    # is the SAME `recorded waiver:` the SR valve uses, not a second grammar.
    assert trace.sn_artifact_advisories([waived]) == []
    # The suppression is the `why` cell's doing, not an accident of the regex.
    assert trace.sn_artifact_advisories(
        [{k: v for k, v in waived.items() if k != "why"}]
    )
    # A `why` that records something else does not silence it.
    assert trace.sn_artifact_advisories(
        [dict(waived, why="One home per dial is cheaper for the owner.")]
    )

    # NO PER-ARTIFACT CENSUS at SN, unlike the SR arm: two needs may honestly
    # describe outcomes one file happens to serve without either of them
    # deciding anything about it. That is a requirement-tier defect only.
    other = {"id": "SN-102", "acceptance": "`docs/process.toml` is refused twice."}
    both = trace.sn_artifact_advisories(
        [{k: v for k, v in waived.items() if k != "why"}, other]
    )
    assert len(both) == 2
    assert not [a for a in both if "all name" in a]


def test_the_fanout_detector_fires_past_the_declared_bound_only():
    from conftest import load_script

    trace = load_script("trace")
    # The bound is DECLARED on the rule's own module (trace.py re-exports the
    # predicates, never the dial — a second name for one number is how two
    # bounds start disagreeing).
    trace_text = load_script("trace_text")

    # A DECLARED DIAL of the TOP_VIEW_MAX family, not a hard cap.
    assert trace_text.SR_FANOUT_MAX == 7

    sr = {"SR-ID": "SR-101", "Requirement": "The harness shall report coverage."}

    def children(n):
        return [
            {"LLR-ID": "LLR-{:03d}".format(i), "SR-Refs": "SR-101"}
            for i in range(1, n + 1)
        ]

    # AT the bound is silent; one past it warns. The boundary is the whole
    # contract of a declared number, so it is asserted from both sides.
    assert trace.sr_fanout_advisories([sr], children(trace_text.SR_FANOUT_MAX)) == []
    over = trace.sr_fanout_advisories([sr], children(trace_text.SR_FANOUT_MAX + 1))
    assert len(over) == 1
    assert "SR-101" in over[0] and "8 direct LLR children" in over[0]
    assert "declared bound of 7" in over[0] and "not a cap" in over[0]
    # A downstream project declares its own bound without editing the rule.
    assert trace.sr_fanout_advisories([sr], children(9), bound=20) == []

    # The per-row escape is a RE-STAMP with a stated reason, matched
    # case-insensitively as the multi-word phrase authors actually write.
    stamped = dict(
        sr,
        Rationale="Fan-out re-stamp: the eight children are one observable "
        "class each, and merging any two would hide a distinct failure mode.",
    )
    assert trace.sr_fanout_advisories([stamped], children(8)) == []
    # An unrelated Rationale does not silence it.
    assert trace.sr_fanout_advisories(
        [dict(sr, Rationale="Coverage is the only honest readout.")], children(8)
    )
    # Children are counted per DIRECT parent ref: an LLR under another SR is not
    # this row's fan-out.
    elsewhere = [
        {"LLR-ID": "LLR-{:03d}".format(i), "SR-Refs": "SR-999"} for i in range(9)
    ]
    assert trace.sr_fanout_advisories([sr], elsewhere) == []


def test_the_two_tiering_detectors_warn_but_never_gate():
    # Mirrors the paraphrase advisory's never-gates half. Warn-first is the
    # RULING, not an implementation convenience: the live registries trip both
    # today (seven fan-out offenders, several rows naming a script), and a gate
    # that is red on the day it ships is a gate someone turns off.
    import argparse

    from conftest import load_script

    trace = load_script("trace")

    def ns(strict=False, strict_integrity=False):
        return argparse.Namespace(strict=strict, strict_integrity=strict_integrity)

    for attr in ("sr_artifact_advis", "sr_fanout_advis"):
        loud = _findings_stub(trace, **{attr: ["SR-101 tripped the detector"]})
        # Under the LOUDEST flag the kit has, and under the always-on integrity
        # floor, and with no flag at all: still 0.
        assert trace.exit_code(loud, ns(strict=True)) == 0
        assert trace.exit_code(loud, ns(strict_integrity=True)) == 0
        assert trace.exit_code(loud, ns()) == 0


# --- Re-tier v2 R4, EXECUTED: no row states a provider its owner derives ------
# Owner ruling 2026-08-15 (log `2026-08-15p`) staged it; `OI-60` (a) ordered it
# behind the counterpart-to-consumers rename and WI-455 ran both (2026-08-23).
# `Provider` is now ABSENT wherever `owner` -> LLR -> `Module` derives it, and
# this advisory is what holds that state: a row that states one anyway is
# reported as redundant, and one that CONTRADICTS its owner as a disagreement.

_LLR = {"LLR-014": "project-trajectory/scripts/check_perf.py"}


def _if_row(**over):
    row = {
        "IF-ID": "IF-101",
        "Provider": "scripts/check_perf",
        "Consumers": "scripts/check",
        "Owner": "LLR-014",
    }
    row.update(over)
    return row


def test_a_provider_that_disagrees_with_its_owner_llrs_module_warns():
    from conftest import load_script

    trace = load_script("trace")
    llrs = [{"LLR-ID": k, "Module": v} for k, v in _LLR.items()]

    # The owner answers for the PROVIDER side, and this row names a different
    # module than the owner LLR implements — the derivation the shed rests on
    # would silently change the row's meaning.
    fires = trace.if_provider_advisories(
        [_if_row(Provider="scripts/spine_rules")], llrs
    )
    assert len(fires) == 1
    assert "IF-101" in fires[0] and "Provider='scripts/spine_rules'" in fires[0]
    assert "LLR-014" in fires[0] and "check_perf.py" in fires[0]
    assert "the two must agree" in fires[0]
    assert "warn-only, never the exit code" in fires[0]

    # AGREEMENT IS NOT SILENT — IT IS THE OTHER FINDING. The cell restates what
    # the owner already derives, which is exactly the cell WI-455 removed, so
    # the rule asks for it to go rather than nodding at it. Both spellings read
    # as one module (the arch-map short form and the full repo path with its
    # extension), or every correctly-filed row would report a disagreement.
    for spelling in ("scripts/check_perf", "project-trajectory/scripts/check_perf.py"):
        fires = trace.if_provider_advisories([_if_row(Provider=spelling)], llrs)
        assert len(fires) == 1 and "already derives" in fires[0], spelling
        assert "drop it" in fires[0]

    # A ROW THAT STATES NO PROVIDER IS THE NORMAL SHAPE and is silent — that is
    # what 85 of the kit's 135 rows look like after the shed.
    assert trace.if_provider_advisories([_if_row(Provider="")], llrs) == []


def test_a_bundle_moduled_owner_keeps_its_provider_cell():
    from conftest import load_script

    trace = load_script("trace")
    # A MULTI-MODULE OWNER DERIVES A SET, NOT THE FACT (the live IF-088 /
    # IF-117 / IF-131 / IF-132 / IF-141 shape), so those rows KEEP the cell and
    # this rule must not ask them to drop it — nor read the bundle as a
    # disagreement, which is what an unsplit `norm_module` over the whole cell
    # would do.
    llrs = [
        {
            "LLR-ID": "LLR-014",
            "Module": "project-trajectory/scripts/check_perf.py;"
            "project-trajectory/scripts/spine_rules.py",
        }
    ]
    assert trace.if_provider_advisories([_if_row()], llrs) == []
    assert trace.if_provider_advisories([_if_row(Provider="scripts/trace")], llrs) == []


def test_the_derivability_advisory_ranges_over_llr_owned_module_endpoints_only():
    from conftest import load_script

    trace = load_script("trace")
    llrs = [{"LLR-ID": k, "Module": v} for k, v in _LLR.items()]

    # An SR owner names no module, so nothing is derivable and the cell is the
    # only record of the provider — the 24 requirement-owned rows keep it.
    assert (
        trace.if_provider_advisories(
            [_if_row(Owner="SR-014", Provider="scripts/spine_rules")], llrs
        )
        == []
    )
    # A dangling owner is `if_ownership_advisories`' finding ("Owner references
    # unknown LLR-999"), and reporting it twice under two headings would make one
    # defect look like two.
    assert (
        trace.if_provider_advisories(
            [_if_row(Owner="LLR-999", Provider="scripts/spine_rules")], llrs
        )
        == []
    )
    # NON-MODULE PROVIDERS ARE NOT A DISAGREEMENT — a file medium, a directory
    # or a named external party is a legitimate provider that no design row can
    # ever be, so the module comparison does not range over them. They read as
    # the redundancy arm's "no module-shaped endpoint to compare", which is the
    # quiet answer, not an accusation.
    for endpoint in (
        "docs/requirements/performance-budgets.csv",
        "docs/stage",
        "external:downstream adopter",
        "agent CLI",
        ".github/workflows/check.yml",
    ):
        fires = trace.if_provider_advisories([_if_row(Provider=endpoint)], llrs)
        assert all("names no module matching" not in f for f in fires), endpoint
    # An owner LLR with no Module cell is the required-field rule's finding.
    assert (
        trace.if_provider_advisories(
            [_if_row(Provider="scripts/spine_rules")], [{"LLR-ID": "LLR-014"}]
        )
        == []
    )
    # A `-000` example row is a blank form, not a seam.
    assert (
        trace.if_provider_advisories(
            [_if_row(**{"IF-ID": "IF-000", "Provider": "scripts/spine_rules"})], llrs
        )
        == []
    )


def test_the_derivability_advisory_warns_but_never_gates():
    # The same never-gates half the S2 detectors carry, for the same reason: the
    # live registry trips it today, and clearing it means re-pointing owners across
    # the corpus — the campaign's schedule, not the checker's.
    import argparse

    from conftest import load_script

    trace = load_script("trace")

    def ns(strict=False, strict_integrity=False):
        return argparse.Namespace(strict=strict, strict_integrity=strict_integrity)

    loud = _findings_stub(trace, if_provider_advis=["IF-101 disagrees with its owner"])
    assert trace.exit_code(loud, ns(strict=True)) == 0
    assert trace.exit_code(loud, ns(strict_integrity=True)) == 0
    assert trace.exit_code(loud, ns()) == 0


# --- OI-61 ruled (d): the named-symbol / named-path tripwire ------------------
# The four form rules on a `Contract` cell cannot see CONTENT, which is how a
# live row named the deleted `SCHED_*` classification constants for weeks while
# the presence-only module back-link reported 27/27 complete over it. This rule
# reads the one thing a grammar honestly can: a token that CLAIMS to be a symbol
# or a path must resolve.


def _surface_root(tmp_path, body):
    """A minimal repo whose `[paths] src` holds one real module."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = src\n\n[arch-map]\nmode = symbols\n", encoding="utf-8"
    )
    src = tmp_path / "src"
    src.mkdir()
    (src / "widget.py").write_text(body, encoding="utf-8")
    return tmp_path


_LIVE_MODULE = (
    '"""A module."""\n'
    "LIVE_CONSTANT = 1\n"
    "SCHED_READY = 'ready'\n"
    "\n"
    "def harvest(x):\n"
    "    return x\n"
    "\n"
    "class Router:\n"
    "    def route(self):\n"
    "        return None\n"
)


def _contract_advisories(trace, root, contract):
    return trace.if_contract_advisories(
        [{"IF-ID": "IF-101", "Contract": contract}], root
    )


def test_a_contract_naming_a_deleted_symbol_family_is_reported(tmp_path):
    # THE ACCEPTANCE CASE, and it is the live exhibit's own shape: `SCHED_*` is
    # a FAMILY, so a rule that only read whole names would have missed the very
    # defect it was ruled for. Driven both ways round on one tree — the family
    # present resolves, the family deleted reports.
    from conftest import load_script

    trace = load_script("trace")

    root = _surface_root(tmp_path, _LIVE_MODULE)
    assert _contract_advisories(trace, root, "emits the SCHED_* states") == []

    (root / "src" / "widget.py").write_text(
        _LIVE_MODULE.replace("SCHED_READY = 'ready'\n", ""), encoding="utf-8"
    )
    fires = _contract_advisories(trace, root, "emits the SCHED_* states")
    assert len(fires) == 1
    assert "IF-101" in fires[0] and "SCHED_*" in fires[0]
    assert "no such symbol exists" in fires[0]


def test_the_tripwire_reads_calls_constants_and_dotted_names(tmp_path):
    from conftest import load_script

    trace = load_script("trace")
    root = _surface_root(tmp_path, _LIVE_MODULE)

    # Every shape that RESOLVES is silent: a call, a module-scope constant, a
    # class method by qualname, and a module-qualified name (a module is not a
    # def, so the whole token is never in the AST's name set — the tail is).
    for good in (
        "harvest() returns the record",
        "LIVE_CONSTANT bounds the run",
        "Router.route picks the pair",
        "widget.harvest is the entry point",
    ):
        assert _contract_advisories(trace, root, good) == [], good

    # And every shape that does NOT resolve is named individually.
    for dead, token in (
        ("vanished() returns nothing", "vanished"),
        ("DEAD_CONSTANT bounds the run", "DEAD_CONSTANT"),
        ("Router.gone picks the pair", "Router.gone"),
    ):
        fires = _contract_advisories(trace, root, dead)
        assert len(fires) == 1 and token in fires[0], dead


def test_the_tripwire_declines_to_judge_names_that_are_not_ours(tmp_path):
    # The false-positive classes that would have made this rule unusable, each
    # pinned: another library's symbols, the registry's own column notation,
    # English slashes, and a filename read as an attribute access.
    from conftest import load_script

    trace = load_script("trace")
    root = _surface_root(tmp_path, _LIVE_MODULE)

    for benign in (
        "reads csv.DictReader rows",
        "passes sys.executable through",
        "joins TC.Evidence to LLR.Module",
        "gates the identity/PII classes",
        "drives the claim/work/merge cycle",
        "delivered as a library plus CLI at widget.py",
    ):
        assert _contract_advisories(trace, root, benign) == [], benign


def test_a_named_path_must_exist_unless_the_repo_declares_its_absence(tmp_path):
    from conftest import load_script

    trace = load_script("trace")
    root = _surface_root(tmp_path, _LIVE_MODULE)

    # A path whose first segment is a real directory is judged; sentence
    # punctuation is not part of it.
    assert _contract_advisories(trace, root, "writes docs/stack.ini.") == []
    fires = _contract_advisories(trace, root, "writes docs/report.md.")
    assert len(fires) == 1 and "docs/report.md" in fires[0]
    assert "nothing at that path exists" in fires[0]

    # A path the repo has DECLARED it does not carry is resolved, not dangling —
    # the reading `docs/declared-absences` already has for two other readers.
    (root / "docs" / "declared-absences").write_text(
        "docs/report.md — the layer is off here\n", encoding="utf-8"
    )
    assert _contract_advisories(trace, root, "writes docs/report.md.") == []

    # A token whose top-level directory does not exist at all is NOT judged: the
    # one test that separates a path from an English slash needs no extension
    # list, and this is the cost it pays, stated rather than hidden.
    assert _contract_advisories(trace, root, "writes nowhere/at/all.md") == []


def test_the_tripwire_is_vacuous_with_no_source_surface(tmp_path):
    # An EMPTY surface would report every named symbol in the registry as dead,
    # which is the loudest possible false positive — so "no surface" must be
    # distinguishable from "a surface with nothing in it".
    from conftest import load_script

    trace = load_script("trace")

    assert _contract_advisories(trace, None, "emits the SCHED_* states") == []

    root = _surface_root(tmp_path, _LIVE_MODULE)
    (root / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = src\n\n[arch-map]\nmode = files\n", encoding="utf-8"
    )
    assert _contract_advisories(trace, root, "emits the SCHED_* states") == []


# --- OI-61's sub-question: the `VerifiedBy` seam-tier pointer -----------------


def test_verified_by_is_optional_and_its_pointer_must_resolve():
    from conftest import load_script

    trace = load_script("trace")
    tcs, llrs = {"TC-014"}, {"LLR-014"}

    def flags(cell):
        return trace.if_verified_by_advisories(
            [_if_row(**{"VerifiedBy": cell})], tcs, llrs
        )

    # EMPTY IS AN ANSWER — "verified in its own right" — and it is the ordinary
    # case, so it must never report.
    assert flags("") == []
    # Both tiers are legitimate: the test itself, or the parent design row whose
    # tests cover the seam.
    assert flags("TC-014") == []
    assert flags("LLR-014") == []
    # A pointer that resolves to nothing is the whole of what is checked.
    fires = flags("TC-999")
    assert len(fires) == 1 and "TC-999" in fires[0] and "test-cases" in fires[0]
    # An id of the wrong tier says so in its own words rather than reporting
    # "unknown" — an SR is a plausible mistake and a confusing finding.
    fires = flags("SR-014")
    assert len(fires) == 1 and "not a TC-### or LLR-### id" in fires[0]
