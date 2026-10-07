# WI-841 amendment adjudication at f5f24c2

Question: did each amendment change the requirement's MEANING, or only its CLARITY?
Judged on the before/after cells only, against the anchor copied at de1b1cde.

- [MEANING] LLR-277 Detail -> load_need_tier is the one need-tier row loader, and baseline_snapshot._tier_rows reads every NEED_TIERS tier through it -> the same, plus two new obligations: tier_carriers picks the supported carriers for every tier (need carriers for SN-ID and STK-ID, row carriers otherwise), and tier_rows_from_text reads one tier's registry text under the carrier its file was read from (TOML, CSV or legacy markdown needs). _tier_rows now names load_need_tier explicitly -> two functions and their contracts entered the obligation, which an implementation correct under the old text need not have
- [MEANING] LLR-262 Detail -> at merge intake evaluates each claimed non-adjudication row whose closed Done-when changed; nothing is said about a missing or unreadable claim -> an unreadable claim refuses the merge-time mint, naming why, while the merge itself stands; an absent claim mints nothing and writes intake's stderr line that the check did not run; a readable changed claim goes through the existing arms unchanged -> two new arms, a refusal and a stated skip. An intake that was correct under the old text, and that minted or stayed silent on a missing or unreadable claim, fails the new text
- [MEANING] LLR-278 Detail -> a snapshot is WIDENED only when the act neither flipped nor re-attested a row "in that registry" -> the same rule over REGISTRY IDENTITY: every carrier path of an authorized registry is authorized, including a deleted obsolete carrier copy, while an unauthorized registry's copy is WIDENED on every carrier path -> the new text pins what counts as the registry and adds two cases. A carrier copy deleted by a conversion is now authorized, and an unauthorized registry is WIDENED whichever carrier its copy uses. An implementation keyed on one path per registry met a literal reading of the old text. It fails the new one: it refuses as WIDENED the obsolete copy a conversion deletes, or misses a copy written under a second carrier

All three rows are MEANING, and the tier's rung is RELEASED, so the blessing is the adjudicator's to give. I would bless each new text:

- LLR-277 answers adjudication 004's return: _tier_rows names `load_need_tier`, which is what `baseline_snapshot._tier_rows` calls, and "reads one tier's registry text" has a referent. `spine_carrier.tier_carriers` and `tier_rows_from_text` match the text.
- LLR-262 is the restatement adjudication 004 found ready, and it matches `intake.py`'s `kdone.claim_copy` arm.
- LLR-278 matches `acceptance_record.adjudication_approval_refusal`, which compares both sides through `_registry_identity` over `spine_carrier.tier_carriers`.

The re-attestation is taken in its own act.

VERDICT: MEANING rows=3
