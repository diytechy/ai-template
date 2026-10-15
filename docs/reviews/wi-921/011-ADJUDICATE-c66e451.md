# WI-921 adjudication 011: amendment checkpoint at c66e451cf

This re-sits the five amended rows on the text at `c66e451cf`, after D-018 discarded sitting 010 (its verdict's form was refused by the parser) and the lane reworked 010's returns. The LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**What I checked:**
- **Only two rows changed since `0668ff387`:** LLR-309 and LLR-019. LLR-307, TC-325 and TC-019 are the text 010 judged, and I re-read each against the code and tests below.
- **LLR-307's arms match `kitlib/done_when.py`:** `classify_delta`, `staged_changes`, `_staged_base` and `staged_hold`.
- **Every test named by TC-325 exists and is in its Evidence.**
- **TC-019's new file `tests/test_commit_floor_census.py` holds the four census cases** its Method describes.
- **The residues are owner-ruled** (the spec's Trust section, D-014).

## amendment

- [MEANING] LLR-019 Detail -> run the integrity scan and the secrets scan on staged content and block a failing commit -> it also requires every built-in check step to be classified exactly once: run in the commit floor, run by the hook by name, or not run at commit with a stated reason -> a new rule over the floor's composition. **Blessed.** It states the floor-membership rule that TC-019's census pins and that 010 asked for. Upward, SR-019's "run the integrity + secrets floor on every commit" needs a floor whose membership is declared, and this rule closes the class the row fixes: a registered step that silently never runs at commit. Downward, TC-019's census verifies it. It has no `shall`.
- [MEANING] TC-019 Method -> run the pre-commit-hook suite: a failing integrity or secrets check blocks the commit -> it also runs the commit-floor census (each built-in step classified exactly once; an unclassified step, a duplicate or a listed non-step fails) -> a new verification obligation. **Blessed.** It now verifies a rule LLR-019 states, and its four tests exist.
- [MEANING] LLR-307 Detail -> the reader: claim and current copies, the cover rules, and `staged_closes` naming index moves out of active -> it adds:
  - the staged-change classifier (anything but a lone addition is a change, a close when paired with a terminal addition);
  - the three judging bases (own branch: closes against the integration base; trunk: every change against the parent; elsewhere: closes against the current commit);
  - failed-read holds for the staged set and the branch identity, and nothing judged off a work tree;
  - the close listing carrying its unreadable reason, and lossless, unquoted path reading;
  - the commit-time reach compared with HEAD, and its owner-ruled residues, each caught after the fact only by the merge-time mint.

  New behaviour and holds. **Blessed.** Upward, judging trunk changes against their parent extends SR-156's "the record a merge judges stays as its author committed it" to hand landings. Each arm matches the code and has a TC-325 clause. The residue sentences state limits, an owner-ruled boundary, and are now this boundary's one home: LLR-309 cites them instead of restating them.
- [MEANING] LLR-309 Detail -> hold points: build and rework dispatch, the merge ladder and the pre-commit staged-close arm, each naming the digest and changes, with the editing commit and test runs exempt -> it adds:
  - on the trunk, an ordinary commit that changes a claimed Done-when is judged against its parent and refuses without a binding blessing;
  - the commit-time base and residues are cited to LLR-307;
  - the editing-commit exemption is narrowed to a non-close change on the claim's own lane, and "off the trunk and the claim's own lane, only a close is judged".

  A new hold point and a narrowed exemption. **Blessed.** Both of 010's findings are answered. The exemption sentence now names the trunk explicitly, so it agrees with the trunk arm ("ordinary commit ... judged against its parent") instead of contradicting it. The residues have one home, in LLR-307. Downward, TC-325's trunk-amendment, two-commit-landing and shipped-floor assertions verify the new arm and the narrowed exemption.
- [MEANING] TC-325 Expected and Method -> verify the in-lane hold at dispatch, staged close and merge, the absent, unreadable and deleted-section cases, and the exemptions -> it adds:
  - a trunk commit changing a claimed Done-when held against its parent until blessed, for an ordinary integration-branch commit;
  - unreadable staged-set and branch-identity holds, and nothing judged off a work tree;
  - the shipped and scaffold commit floors running the staged-close step;
  - the claim-copy classifier;
  - a quoted-path claim judged like any other.

  New verification obligations. **Blessed.** It is closed over LLR-307's and LLR-309's new arms, and its seven new tests exist. The residues carry no TC evidence, and the arms map says so: they are owner-ruled limits, not behaviour these rows claim.

VERDICT: MEANING rows=5

**Aftermath:** this session re-attests all five rows on the released rung, in their own act commit:

`python project-trajectory/scripts/intake.py snapshot --reattests LLR-019,LLR-307,LLR-309,TC-019,TC-325`

SITTING: JUDGED kinds=amendment
