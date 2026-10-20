# WI-798 checkpoint adjudication at 49d91cd (amendment)

This re-sits TC-344, which sitting 013 did not bless. I read its amended cells
and checked them against the tests at this tip:

- The new case, tests/test_run_devsetup.py::test_a_signed_in_login_account_is_reported_ok_on_its_own_home,
  exists, and TC-344's Evidence cites it. It runs on both launcher families
  (`sh` and `ps1`), each verified and unverified.
- The case asserts three things: an `[ok]` reading on the account's own home,
  no token offer, and the UNVERIFIED annotation exactly when the account is
  unverified.
- I ran it together with the login-not-signed-in case: 6 passed in 12.68 s.

## amendment

- [MEANING+BLESS] TC-344 Expected+Method -> the sign-in item is off when retention is off, and otherwise reports signed-in, missing or unknown accurately, checked with readable, missing and unreadable inputs -> a readable token or a documented account-home login reads signed-in; an unreadable token, an unsigned login account or an unresolved entry reads missing; an unverified signed-in login account carries its annotation; each case is run on both families -> new cases and a new annotation check, so a test passing the anchored text could fail this one: meaning, carried by both cells. I would bless it. Sitting 013's finding is answered: the Expected's signed-in login reading is now driven by a cited test, verified and unverified, on both families. Every arm of LLR-321 now has a cited test, and the cells name no implementation carrier

The TC rung is released, so the later act turn re-attests TC-344. Sitting 013
expected TC-344's unblessed drift to hold back the copy of
`docs/test/test-cases.toml`; that hold should now be lifted.

VERDICT: MEANING rows=1

SITTING: JUDGED kinds=amendment
