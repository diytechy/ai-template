# WI-798 checkpoint adjudication at b1afd77 (amendment; first-approval)

This sitting re-sits the rows sitting 012 returned or did not bless, as
reworked in b1afd77. I read each row's cells and chain. I checked them against
the code and tests at this tip:

- Every test the in-scope TCs cite exists.
- Every test in `tests/test_accounts.py` is now cited by a TC; sitting 012
  found 17 uncited.
- `tests/test_run_devsetup.py` drives the token, login-not-signed-in and
  unresolved-entry readings on both launcher families.

One arm is still undriven: the workstation report's line for a signed-in login
account (`login:signed-in`, with its UNVERIFIED variant).

## amendment

All seven rows change meaning against the anchor at 41375927d. Six now carry
text I would bless; one goes back.

- [MEANING+BLESS] LLR-321 Detail -> signed-in only for a readable token; missing when the token cannot be read -> also signed-in for a documented signed-in status from the account's own home; missing for an unreadable token file, a login account not signed in, or an unresolved adjudicator entry -> new readings. Sitting 012's finding is answered: the missing arms now match the report's `login:missing` and unresolved branches, and the text names no carrier. The new signed-in arm still has no driving test; that gap sits in TC-344, below, not in this row's text
- [MEANING] TC-344 Expected+Method -> signed-in, missing or unknown reported accurately for readable, missing and unreadable inputs -> a readable token or a documented account-home login reads signed-in; an unreadable token, an unsigned login account or an unresolved entry reads missing -> new cases, carried by both cells. I would NOT bless it. The Expected promises that a documented account-home login reads signed-in, but the Method drives no signed-in login account, and no cited test does: the only login-account test (test_a_login_account_is_named_its_provisioning_and_offered_no_token) asserts `[missing]`. So the report's `login:signed-in` branch, including its UNVERIFIED line for an unverified non-ambient login, runs under no test. That is the "new signed-in source" sitting 012 asked to be verified. Every other arm is driven, on both families: token readings, login not signed in, unresolved entry (tests/test_run_devsetup.py, the `sh` and `ps1` arms)
- [MEANING+BLESS] LLR-044 Detail -> routing, selection and cooldowns by route -> each enable-list line is one entry carried by selection, preference and cooldowns; a row is read through the entry's route; a qualified key is ROUTE@ACCOUNT -> a new identity rule. This answers sitting 012's naming finding: the added sentence names no function, and TC-046 holds it
- [MEANING+BLESS] LLR-072 Detail -> two fresh planner sessions with the fallback -> each session also carries its enabled entry, and its model is the route that entry selects -> a new carried field. The attribute name is gone; TC-072 holds it
- [MEANING+BLESS] LLR-270 Detail+Rationale -> a per-family dedicated home under the store; family, route and scope identity -> LLR-305's environment (the account home or ambient) with no per-family home; account in the lease-only record and the identity; a mismatched or account-less record mints once -> the Detail carries the meaning, unchanged from the text sitting 012 blessed. The Rationale now answers 012's follow-up: only a qualified account home keeps a transcript out of a person's sessions, and an unqualified entry retains in its ambient environment. That matches the code and LLR-336
- [MEANING+BLESS] LLR-305 Detail+Rationale+Title -> a family-level token and dedicated home, with refuse_competing for a token route -> the entry's account supplies environment, home and token; every declared account is checked for a declared source ranked above its home; `--bare` and the token variable are refused for token accounts only; a qualified OpenCode launch starts from its declared base plus kit-owned names -> the credential boundary moved from family to account. Both of sitting 012's findings are answered: the added function name is gone ("names compare under platform case rules"), and the boundary's tests are now cited by TC-362, which verifies this row. "Competing credential names" in the composition sentence reads, as defined in the same cell, as the sources ranked above a declared account's home, so an unqualified entry has none; that matches the code
- [MEANING+BLESS] TC-324 Expected+Method -> only a family with a dedicated home needs a readable sign-in -> a retained token account needs its own readable token file and a retained login account its own documented signed-in status; missing or unknown refuses before any state change; an unqualified entry has no gate -> the subject moved from family to account. This answers sitting 012's finding: the Expected now covers both account kinds, consistent with its token-file arm and with LLR-305. The Method runs again the cited test that holds the unqualified-entry arm

Rung status: the LLR and TC rungs are released, so the later act turn
re-attests the six rows marked `[MEANING+BLESS]`. TC-324 sits in the same
registry as TC-344, which is not blessed and stays drifted, so I expect the
copy of `docs/test/test-cases.toml` to be refused until TC-344's rework lands.
That holds TC-324 with it, and the first approvals below. The LLR registry has
no unblessed drift left among the rows judged here.

## Returns answered in the lane

Answered in the lane (coordinator, 2026-10-20 headless leg 04): commits 88324f6b4 and 49d91cd, re-sat at sitting 014. No row is minted from these drafts.

```toml
title = "TC-344: drive the workstation report's signed-in login-account reading, including its unverified line, on both launcher families"
workstream = "process"
buildtier = "strong"
sr_refs = ["SR-032"]
priority = 3
specref = "docs/reviews/wi-798/013-ADJUDICATE-b1afd77.md#amendment"
```

What the draft owes:

1. **The test:** run dev-setup's check on both families with the adjudicator
   on a login account whose own home reads signed in, verified and unverified.
2. **What the test asserts:** the `[ok] ... its own home` reading, and the
   UNVERIFIED annotation for the unverified case.
3. **TC-344:** cite that test, and add the case to its Method so that the
   Expected's signed-in login reading is verified.

VERDICT: MEANING rows=7

## first-approval

All three rows are ready. Each answers sitting 012's findings against it.

- [APPROVE] TC-362 -> every launch and probe uses its selected account's environment: two homes per CLI, precedence, conflicts, the declared-account credential boundary, the OpenCode base, unqualified behaviour -> Verifies is now SR-154, SR-222, SR-227, LLR-266/267/268, LLR-305 and LLR-336, each earned by a cited test; the unearned SR-239 is gone. Its evidence now cites the five credential-boundary tests, the user-config-dir platform rule and the token-before-home refusal, so LLR-305's account arms are verified -> ready
- [APPROVE] TC-364 -> retained state never crosses an account boundary: legacy, other-account and marker records; scoped pins; keep-warm on resolvable entries -> Verifies is SR-154, SR-227, SR-239, LLR-270 and LLR-336, and SR-238 is gone. SR-239 is earned by the scoped-pin test, and LLR-270 by the record-identity tests -> ready
- [APPROVE] TC-365 -> the adjudicator refuses invalid account and registry input, accounts report only their own credential state, and dev-setup neither signs in nor exposes credentials -> Verifies is SR-154, SR-227, SR-231, LLR-305, LLR-306 and LLR-336, and SR-239 is gone. Its Method asserts conditions, and it now cites the sign-in reporting tests (ambient or unresolved entry, the documented-pairs reader) and the registry-error tests -> ready

The later act may find the copy of `docs/test/test-cases.toml` refused while
TC-344 stays drifted (see the amendment section). If it is, these approvals
wait for that rework too.

OUTCOME: APPROVE rows=3

SITTING: JUDGED kinds=amendment;first-approval
