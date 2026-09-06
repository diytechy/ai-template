# redesign-code-closure — adversarial review

Requested route: Opus 5, high; declared CLI stream-json pattern.

Subject SHA256: `eee60250bbae88bf381f5b6ed595b2da3429f2066666c5f9f11f2d2edbbabb03`

Tracked invocation: [session log](../iteration/call_55bce3666ac140e1acfd6c608308de39-20260906-100820.log).

Review uses supplied source with tools disabled. It is an independent
assessment, not a requirement approval or a test execution.

**APPROVE**

**B1 — resolved.** `Path(NEEDS_REL).with_suffix(".md").as_posix()` yields `docs/requirements/stakeholder-needs.md` under both `PurePosixPath` and `PureWindowsPath`, so the alias set no longer carries a native-separator member. Aliasing `NEEDS_REL` to `hats_roster.NEEDS_REL` removes the second home, and because it stays a fixed constant (not carrier-dependent), both spellings are accepted regardless of which carrier is live — which is what makes the `suffix="toml"` arm pass against a `need_carrier="md"` fixture.

**B2 — resolved, non-vacuously.** The `PureWindowsPath` monkeypatch test fails against the pre-fix source *on POSIX* (`str(...)` → backslashes → no set match → `None`), so it is a real regression pin rather than a Windows-only aspiration. The `SN-404` arm makes the parametrized test discriminating: it can only raise if the fragment was parsed and the carrier resolved, so replacing the function body with `return None` now breaks it. Parametrizing over both suffixes covers the exact-match branch and the alias branch separately.

**B3 — adequately discharged.** Placing the instruction in §1.3 step 3 is stronger than the §3 entry I asked for, not weaker: §3 entries are range-selected against `docs/kit-version`, while step 3 is read on every re-sync. It scopes correctly to "after taking the prompt templates and their generator," names the exact command, and states the fresh-only boundary without relaxing the `created` gate — which the disposition correctly identifies as load-bearing.

**Non-blocking, for the freeze run:**

1. The `unknown SN id(s)` refusal is raised outside the supplied excerpt (`_parent_need_ids` only raises the SR-side message). I could not verify from source that the string matches `"unknown SN id.*SN-404"`; confirm the new arm actually fails on a mismatch rather than erroring elsewhere.
2. The promised version-anchored §3 entry is an open obligation until the implementation commit exists. Track it so it does not fall out — the §1.3 text does not carry a `[since <sha>]`, so nothing mechanical will notice its absence.

My prior freeze-run list (scaffold byte-comparison, SR-163 delivery-inventory, the unmapped-entry warning) still stands unrun.
