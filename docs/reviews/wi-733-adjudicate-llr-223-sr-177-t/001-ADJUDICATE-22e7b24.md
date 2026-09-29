# ADJUDICATE — WI-733 — amendment at 22e7b24

Independent adjudication, spine-acts batch I, of six approved rows whose
approved cells moved after their last attestation. The brief's question is
whether each amendment changed the row's MEANING or only its CLARITY. I read
the brief (`adjudicate_brief.compose`) in full. It measures against
`docs/archive/last_approved` as last written:

- the SR registry, copied at 6f6613e2;
- the LLR registry, copied at 2d264589;
- the TC registry, copied at e40ae0ae.

For SR-177 and SR-193 the before-text is batch G's re-attested text. For
LLR-222 and LLR-223 it is the text from before WI-723 built the joint-delivery
class. For LLR-286 it predates WI-721's carrier widening, and for TC-267 it is
the method batch H left.

The coordinator's carry-over (LLR-222, LLR-286 and SR-193, blessed in batches
G and H but never anchored) was judged afresh on its current text. The
verdicts of WI-724, WI-726, WI-728, WI-730 and WI-731 are context, not
authority. What WI-732 changed was read from its archived spec and from
`git show 03debc71`, and its review and ruling 1 of `ARBITRATION.md` were read
too. The WI-735 spot check of WI-732's close was passed to me as chain
evidence. I ruled its observations 3, 4 and 5, which touch these rows, below.

The routed pointer cells were read from the registries and ruled:

- `SR-Refs`: SR-193 for LLR-222 and LLR-223; SR-226 for LLR-286.
- `Verifies`:
  - SR-227, LLR-270, IF-247 and IF-248 for TC-267;
  - TC-191 verifies SR-177;
  - TC-220 verifies SR-193, LLR-222 and LLR-223;
  - TC-299 and TC-300 verify LLR-286.
- `SN-Refs`: SN-027 for SR-177; SN-043 for SR-193.
- `Boundary-Refs`: B-09 for SR-177 and SR-193.
- `Delivered-With`: SR-156 and SR-170 for SR-177, unchanged since batch G re-attested it.
- `Coincident`: SR-193's waiver, unchanged.

Every one HOLDS.

- [CLARITY] SR-177 Rationale -> the before-text builds a per-run report of lanes configured, lanes occupied and work integrated per wall-hour from recorded telemetry, with no numeric target, and the aggregation is the build gap that the telemetry columns alone do not satisfy. It argues this through the charter, the refused improvement target, this repository's undeclared lanes dial and a "not decomposed" receipt -> the after-text asks the same: the same three quantities per run, no target ("observable rather than budgeted"), and "the telemetry columns alone cannot distinguish configured capacity from run-level utilisation", with the per-run aggregation named as the gap -> the same obligation. The deleted sentences were arguments and receipts: the plans citation, the lanes=1 example, and "no seam to pin and no test to cite … lands Drafted-undecomposed". They were not obligations. The before-text's "nothing aggregates … by lane or by run" described an absence and asked for no per-lane breakdown, and the acceptance asks for none. A report correct under the old text is correct under the new one, and the reverse also holds. Batch H's MEANING finding was on the intervening "must … token telemetry … by lane and by run", and that is gone. BLESSED. The text changed, so the row is named in `--reattests` so the record holds the text blessed. Observation 4 of the spot check is ruled below.
- [CLARITY] SR-193 Rationale -> the before-text gives the reasons for the waiver, for keeping the need link on the requirement, and for reporting rather than failing -> the after-text gives the same reasons, plus two argued points: a sibling requirement is neither a premise about the world nor a sole-delivery claim, and Delivered-With re-opens attestation while DA-Refs does not -> the obligation is identical. Both added points argue what the unchanged approved AcceptanceCriteria already require ("classified joint"; "changing assumption citations re-opens no attestation, while declaring or changing Delivered-With or the waiver re-opens the requirement's"). There is no citation frame, and every sentence is a standing reason. BLESSED, as batch H found. It is named in `--reattests`: the SR registry can now be copied.
- [MEANING] LLR-222 Detail, Title -> the before-text: the requirement tier gains `da_refs` and `coincident`, and the template carries both -> the after-text: the tier also carries `delivered_with` (a list, in `REF_COLS`), Delivered-With is in `SPINE_APPROVED_CELLS` while DA-Refs stays traced, SR-000 carries all three keys, and the Title names the joint-delivery siblings -> a new key and a new approved-cell membership, so meaning. The Title change is clarity inside a row that is meaning. I checked each claim at HEAD: `migrate_carrier.REF_COLS` holds both DA-Refs and Delivered-With; `spine_carrier`'s column map declares `coincident` once, beside `da_refs` and `delivered_with`; `kitlib/spine.py` lists the three keys; `acceptance_record.SPINE_APPROVED_CELLS` holds Delivered-With; and the template's SR-000 carries all three. BLESSED; re-attested in this act.
- [MEANING] LLR-223 Detail -> the before-text: bridged, coincident, unclassified and "both", from DA-Refs and Coincident, with an undeclared assumption failing -> the after-text: a row is joint when Delivered-With names one or more declared siblings sharing one of its needs, even beside DA-Refs, and it imports no sibling assumptions. Otherwise a row is bridged or coincident, and none is unclassified. "A joint row with Coincident, or a non-joint row with both DA-Refs and Coincident, is an advisory naming the contradiction". A disjoint sibling is an advisory. An undeclared assumption or requirement is a failure -> a new class and new rules, so meaning. Batch H's finding is answered. I read `_classify` and `sr_classification_advisories`, and the contradiction sentence now matches the code on each case it names: joint plus waiver, and joint plus DA-Refs plus waiver, give the joint-waiver advisory only; non-joint DA-Refs plus waiver gives the `both` advisory; a disjoint-only sibling plus waiver gives `coincident`, with the disjoint advisory only. This agrees with SR-193's acceptance and TC-220. BLESSED; re-attested in this act. Observation 3 of the spot check is ruled below.
- [MEANING] LLR-286 Detail -> the before-text: `retire` refuses unless the id is a live row of its tier's TOML registry -> the after-text: the id must be live in whichever carrier form the kit's registry reader resolves -> the obligation widened, and the old text allowed what the new one forbids: a live row carried in a legacy form reads as not live. Checked at HEAD: `retire.live_ids` reads every tier through `spine_carrier.load`/`load_need_tier`, and `retire` and the missing-record finding both use it. This brings the design row into line with SR-226's acceptance, which says a live id is not reported. BLESSED; re-attested in this act.
- [MEANING] TC-267 Method -> the before-text: an adjudication meeting a keep-warm lease runs unretained -> the after-text: it runs unretained "with the stated reason naming the holder" -> an added assertion, so meaning. `test_an_adjudication_waits_out_a_keep_warm_lease_then_runs_unretained` asserts `"held by keep-warm:x"` on stderr (`tests/test_session_keep.py:518`). That is SR-227's "stating why", and LLR-270's "saying why". The rest of the Method is byte-identical. SR-227 is RETURNED in WI-734 on clauses this case does not touch, so the Method stays true under that fix. BLESSED; re-attested in this act.

Spot-check observations on these rows, ruled:

- **Observation 3** (LLR-223 does not say that a row with an undeclared reference is failed and never classified). It HOLDS as a fact about the code: `_classify` returns no class when a reference is undeclared, so such a row gets the reference failures and any disjoint-sibling advisory, and no class advisory. It does NOT stop the blessing:
  - every rule the Detail states is exact for each row the check does not fail;
  - a row that does fail is named as a failure, which is the loud outcome;
  - the Detail, SR-193 and TC-220 all leave the precedence between a failure and a class unstated, and the code's precedence is documented where it lives (`classify_srs`: "left out, because `sr_classification_advisories` fails it instead").

  Both earlier returns of this row were on a condition that changed the result for a row the check passes. This is an unstated precedence in a corner where the check already fails, naming the row. It is recorded here and not drafted. If the coordinator wants it closed, the smallest exact fix is one clause in LLR-223, after "is a failure": ", and a row with such an entry is left unclassified, so it draws no class advisory". The fix also needs one assertion in TC-220, and both are approved rows re-opened by that edit.
- **Observation 4** (SR-177's acceptance ends "the aggregation itself is the row's stated build gap"). It HOLDS: that clause is not a pass/fail condition, and the Rationale's "The existing telemetry does not join …" is a present-state claim. Both become false when the aggregation ships. The AcceptanceCriteria cell is not amended here: it was blessed by an earlier act and is outside this brief's question. The Rationale sentence is still a true reason today, which is why it is blessed. No work item builds the aggregation. The work that does must amend both cells in the same change. Recorded here and not drafted.
- **Observation 5** (a store-lock wait names no holder). It agrees with TC-267, which claims the holder only for the keep-warm lease it drives. There is no finding.

Checks I ran at 22e7b24 (results seen, not claimed):

- `python -m pytest -q -n auto tests/test_assumption_rules.py tests/test_cell_classes.py tests/test_session_adapters.py tests/test_session_service.py tests/test_session_keep.py tests/test_retire.py -p no:cacheprovider` gave **353 passed in 113.73s**.
- Snapshot pre-check, read-only (`baseline_snapshot.refresh_refusal`), on the exact act (`--approves` for the LLR registry, `--reattests SR-177,SR-193,LLR-222,LLR-223,LLR-286,TC-267`): **accepted**. Within its three registries the drifted approved rows are exactly these six. With SR-177 left out, the same call is REFUSED naming `SR-177: Rationale`, so the gate was live.

The act: every row is re-attested in batch I's one act commit, and no
`Status` moves. SR-177 and SR-193 are anchored with the SR registry, LLR-222,
LLR-223 and LLR-286 with the LLR registry, and TC-267 with the TC registry.
No registry cell was edited by this sitting.

VERDICT: MEANING rows=6
