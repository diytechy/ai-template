dc3f8c6b NOT YET SOUND

- [major] `project-trajectory/scripts/check_test_first.py:267` — A readable legacy `Approved` row is treated as inherently inexact at TOML cutover. The fixture at `tests/test_check_test_first.py:434` proves the false failure: TC approved in CSV, implementation later, cutover last should produce no report under SR-217, but now reports UNREAD. Walk interpretable older-carrier approvals and reserve inexact bounds for genuinely ambiguous legacy states.

- [minor] `docs/test/test-cases.toml:2578` — TC-250 was not amended for whole-history TC approval, cutover/inexact behavior, or strict failure; the new inexact tests also never assert `--strict` exits 1. Update and reapprove/reattest TC-250 and add that assertion.

- [minor] `project-trajectory/README.md:60` — It says every inexact approval is reported unread, while the implementation correctly suppresses one bounded at/before landing. Qualify this here, in `process.toml.template:325`, and `RESYNC_PACK.md:5294`.