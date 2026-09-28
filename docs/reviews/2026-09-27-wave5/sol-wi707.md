<!-- Codex Sol (gpt-5.6-sol, medium) review of WI-707, build/wi-707 32687d47..ee1d68ff, read-only; rulings 46-47. Links re-rooted from the removed worktree. -->

ee1d68ff NOT YET SOUND

- [major] Seven of thirteen waivers still fail the “effect alone” test:

  - SR-015 checks off-spine PB references; it does not deliver SN-002’s verified `SN→SR→LLR→TC` chain ([system-requirements.toml:75](../../../docs/requirements/system-requirements.toml), [stakeholder-needs.toml:114](../../../docs/requirements/stakeholder-needs.toml)).
  - SR-024 generates cases but does not verify the need-to-test chain ([system-requirements.toml:160](../../../docs/requirements/system-requirements.toml)).
  - SR-033 emits a checklist but does not make a gate pass only when its bar is met; the approver supplies that outcome ([system-requirements.toml:244](../../../docs/requirements/system-requirements.toml), [stakeholder-needs.toml:131](../../../docs/requirements/stakeholder-needs.toml)).
  - SR-111 supplies a re-sync prerequisite, expressly leaving the re-sync to another requirement; it does not prevent clobbering alone ([system-requirements.toml:425](../../../docs/requirements/system-requirements.toml)).
  - SR-129 preserves registry cells but does not itself derive or dispatch deterministic next work ([system-requirements.toml:475](../../../docs/requirements/system-requirements.toml), [stakeholder-needs.toml:235](../../../docs/requirements/stakeholder-needs.toml)).
  - SR-174 supplies unique identity, a prerequisite rather than the deterministic frontier/dispatch outcome SN-025 states ([system-requirements.toml:1001](../../../docs/requirements/system-requirements.toml)).
  - SR-177 explicitly concedes that SR-156 delivers SN-027’s outcome and that this row merely measures it ([system-requirements.toml:1050](../../../docs/requirements/system-requirements.toml)).

  Fix: re-parent only where another need states the row’s effect; otherwise remove `coincident`, label the derivation, and cite a falsifiable DA that bridges the effect to the cited need.

- [major] SR-223 and SR-225 cannot use `coincident` while declaring that no clause of their cited need is their outcome ([system-requirements.toml:1665](../../../docs/requirements/system-requirements.toml), [system-requirements.toml:1692](../../../docs/requirements/system-requirements.toml)). That makes the gate accept exactly the relationship the cells deny. Fix: replace each waiver with an appropriate `da_refs` bridge—or leave it unclassified until the need owner adds the missing outcome.

- [major] Two of the six amended rationale sentences remain semantically false: SR-111 says it “Realizes” merely the base needed by SN-001, and SR-174 says unique allocation realizes deterministic dispatch ([system-requirements.toml:419](../../../docs/requirements/system-requirements.toml), [system-requirements.toml:1002](../../../docs/requirements/system-requirements.toml)). Fix them with the waiver/DA correction. The six edits otherwise changed only their respective `Realizes` sentences; the remaining rationale bytes are unchanged.

The other six waivers—SR-011, SR-031, SR-040, SR-112, SR-147 and SR-149—pass, and their re-parenting drops no obligation those rows deliver.

No finding on SR-223’s narrowing or TC-290(c): the arm is non-vacuous across physical sources, delivery destinations, the repository guardrails directory, and a nonempty shipped-model roster ([test_guardrails_payload.py:60](../../../tests/test_guardrails_payload.py)). The TC-272/TC-297 split is also correct: only TC-272 cites IF-112 and exercises its in-memory `check_docs` caller; TC-297 carries only the two slow repository pointers ([test-cases.toml:2797](../../../docs/test/test-cases.toml), [test-cases.toml:2808](../../../docs/test/test-cases.toml)).