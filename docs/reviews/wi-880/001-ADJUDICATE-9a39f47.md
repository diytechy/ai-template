# WI-880 lane checkpoint: adjudication sitting 001 at 9a39f47

## amendment

Anchor: `docs/archive/last_approved` (system-requirements.toml at fb1990aa; low-level-requirements.toml and test-cases.toml at d0a4b623).

- [MEANING] SR-019 AcceptanceCriteria -> the hook runs the integrity floor and secrets scan on staged content, blocks a commit failing either, and a `--no-verify` bypass is caught by the hosted re-run -> the same, PLUS: with no interpreter at the runtime floor the commit hooks refuse the commit, name the developer-setup install step, and neither run the floor below it nor skip it -> not the same: a new acceptance case. A hook that skipped or crashed on a box with no 3.11+ interpreter met the old text and fails the new. BLESSED. Note: the clause says "the commit hooks", which also takes in commit-msg under a row whose Requirement names the pre-commit hook. The code meets it (commit-msg sources the same probe), and it is not a reason to send the row back.
- [MEANING] LLR-021 Detail -> a hook probe that RUNS candidates (never a PATH name test) and skips or reports clearly when none works, shared by pre-commit and pre-push -> `kit_python`, one probe sourced by pre-commit, commit-msg and pre-push: the two venv candidates, then the developer-setup runtime search in its order, taking the first that reports 3.11+, with every hook step on that path; with none it REFUSES, naming the install step (overridable by `KIT_DEV_SETUP_INSTALL`), never running an older interpreter or skipping a floor whatever the privacy policy or loop marker; its post-venv candidates equal developer setup's search -> not the same: "skip-or-report" became "refuse"; there is a 3.11 floor where there was none; commit-msg was added; candidate parity is a new constraint. BLESSED: `project-trajectory/hooks/kit-python.sh` and all three hooks match it line for line.
- [MEANING] TC-021 Expected + Method -> run the hooks' probe cases, where a missing or aliased python3 reports without crashing -> drive all three hooks with non-runnable stand-ins and a real pre-3.11 interpreter, and pre-commit with a real 3.11+ venv; inspect the hooks and a fresh scaffold for the one shared probe; compare its candidates with developer setup's search -> not the same: new acceptance conditions (refusal content, floor, venv preference, one probe, candidate parity). BLESSED: it covers each new LLR-021 arm, and the named tests pass (below).
- [MEANING] SR-020 AcceptanceCriteria -> scan the push range and block a secret, or a PII class under privacy-check -> the same, PLUS: with no interpreter at the runtime floor it refuses the push, names the install step, and neither scans below the floor nor skips the scan -> not the same: a new acceptance case. BLESSED: pre-push sources `kit_python ... push || exit 1`.
- [MEANING] SR-032 AcceptanceCriteria -> the scaffolded onboard/dev-setup scripts run to a green setup -> the same, PLUS: when a Windows developer setup has no interpreter at the floor, its attended install operation offers one consent-first through an available provisioner, searches again after acceptance, and otherwise exits with the install step; declining runs no provisioner -> not the same: a new behaviour and a new acceptance case. NOT BLESSED. SR-032's Requirement binds "the onboarding and dev-setup TEMPLATES", so the new clause, read against it, binds the shipped `dev-setup.template.ps1`. That template's install offers only the adopter-configured `$RuntimeInstall` (empty by default): it detects no available provisioner (uv or winget) and never searches again. Only this repository's own `scripts/dev-setup.ps1` (LLR-326) does. The clause therefore states, about the delivered artifact class, a behaviour the delivered templates do not have, and it does not say which Windows developer setup it means. That is an unnamed actor in an acceptance condition.
- [MEANING] TC-345 Expected + Method -> the opt-in merges only the guard's commands, bound to the opt-in's interpreter, idempotently; a decline or an example without guard hooks changes nothing; an installed hook denies with an older Python first; the local file is git-ignored -> the same, PLUS: this repository's committed settings contain no guard group; its inert example carries every served guard group at the repository guard path; its readiness report names the opt-in as on or off with where it is offered -> not the same: three new acceptance conditions. NOT BLESSED. TC-345 verifies SR-032 and LLR-322, and neither row states any of the three new obligations. LLR-322 says the opt-in never WRITES the committed settings, not that they carry no guard group. No row in the LLR registry states the readiness report's hooks item or the inert example's content; a grep for "opt-in", "guard group" and "inert example" finds only LLR-322. The owner's ruling D-004 and the spec's Trust section are where these live today, and neither is a spine row. A TC asserting obligations nobody stated is verification without a requirement, and it cannot be traced or re-judged when the ruling moves.
- [MEANING] SR-046 AcceptanceCriteria -> the existing menu, direct, discovery, readiness and delegation conditions -> the same, PLUS: a declared command invoking the language runtime by its bare name runs on the floor-resolved interpreter rather than the first one on the search path -> not the same: a new acceptance case. BLESSED as the right obligation at this tier. Note that it binds every bare name of the runtime, `python3` included; the LLR-047 finding below is where the code falls short of it.
- [MEANING] LLR-047 Detail -> the parse, list, direct, launch, menu and launcher-resolution contract -> the same, PLUS: `launch` puts first on PATH a directory whose bare `python` AND `python3` run the menu interpreter exactly: on Windows the interpreter's own directory, on POSIX per-launch exec shims (shims, not links, to keep a venv's configuration) -> not the same: a new mechanism and guarantee. NOT BLESSED: the Windows half of that guarantee is false.
  - A Windows interpreter directory holds `python.exe` and no `python3.exe`. That is true of both this box's venv (`.venv/Scripts`) and its python.org 3.11 install.
  - Reproduced: a `[run]` line `python3 -c "...print(sys.executable)"` run through `run_menu.py` on the python.org 3.11, with PATH reduced to System32, prints `'python3' is not recognized`. With the full PATH it reaches the WindowsApps Python Manager alias instead of the menu's interpreter.
  - So on Windows, bare `python3` falls through to whatever is next on PATH: exactly the failure SR-046's new clause forbids.
- [MEANING] TC-047 Expected + Method -> "Satisfies SR-046 AcceptanceCriteria" and the run-menu suite -> the same, PLUS: a bare-python capability runs on the menu interpreter with a pre-3.11 first on PATH; on POSIX it stays exact beside another python, and each shim keeps its venv -> not the same: new acceptance conditions. NOT BLESSED, together with LLR-047. LLR-047's claim that bare `python3` is exact goes unverified on Windows (the method drives only `python` there, and the POSIX-only case skips on Windows), which is how the defect above got through. When LLR-047 is corrected, TC-047 must drive `python3` on every platform where the LLR claims it.

Verification run this session: the arms-map tests for LLR-021, LLR-047, LLR-322 and LLR-326 gave 21 passed and 1 skipped. The skip is the POSIX-only `..._exact_where_its_directory_holds_another`, because this box is Windows.

VERDICT: MEANING rows=9

Aftermath, as this section rules it:
- Blessed and owed `--reattests`: SR-019, SR-020, SR-046, LLR-021, TC-021.
- Not blessed, left unanchored: SR-032, TC-345, LLR-047, TC-047.
- Each registry holds one row I am not blessing (SR-032; LLR-047; TC-345 and TC-047). The snapshot copy is refused while those drift, so the blessed rows cannot be re-anchored until the lane answers the findings. The act's outcome is recorded in the report.

### Dispositions

WI-880 is an ordinary work lane, not an adjudication-kind spec, so intake would not mint drafts written into its spec. The findings are the lane's own to answer before it merges. The drafts below are the corrective work, in the shape intake reads, for the coordinator to route back to the WI-880 lane or file:

```toml
title = "WI-880 return: SR-032's Windows install clause binds an artifact class it does not hold for"
safety_class = "ordinary"
```

SR-032's Requirement is about the shipped onboarding and dev-setup templates, and the new clause holds only for this repository's own `scripts/dev-setup.ps1`. Either:
- scope the clause, and its child LLR-326, to a home that names this repository's developer setup;
- or make the shipped `dev-setup.template.ps1` (and `.sh`, for parity) detect an available provisioner and search again, so that the clause holds for the delivered artifact class.

Then re-submit SR-032, LLR-326 and TC-350 together.

```toml
title = "WI-880 return: TC-345's this-repository assertions verify obligations no row states"
safety_class = "ordinary"
```

State in LLR-322, or in a row whose parent calls for it, the three obligations TC-345 now asserts:
- this repository's committed settings carry no guard group (owner ruling D-004);
- the inert example carries each served guard group at the repository guard path;
- the readiness report names the opt-in as on or off and where it is offered.

Then re-submit TC-345 against that text.

```toml
title = "WI-880 return: a [run] line's bare python3 is not the menu interpreter on Windows"
safety_class = "ordinary"
```

LLR-047 claims that the directory `launch` puts first on PATH makes bare `python` and `python3` exact on Windows. The interpreter's own directory has no `python3.exe`, so `python3` falls through PATH; this is reproduced above. Either:
- make it exact (for example, a per-launch directory on Windows too, holding `python3` beside `python`);
- or narrow the claim and SR-046's reading explicitly.

Extend TC-047 to drive bare `python3` on each platform the LLR covers, and re-submit LLR-047 and TC-047.

## first-approval

- [RETURN] LLR-326 -> at an attended Windows `-Install` with no 3.11+ interpreter, `Find-Runtime` searches, `Offer-Python` offers one available provisioner (uv before winget) consent-first, and the search runs again after acceptance; a decline runs no provisioner; still missing exits 1 with the install step -> its parent SR-032, as approved, asks only that the dev-setup TEMPLATES scaffold and run to a green setup. The only text calling for this row is SR-032's amended clause, which the amendment section returns for binding the template class to behaviour only this repository's `scripts/dev-setup.ps1` has. The code (`scripts/dev-setup.ps1` lines 349-360) matches the row -> not ready: reading upward, the row answers a requirement the approved parent does not make. Its sibling TC-350 also disagrees with it: TC-350 says BOTH paths search again, while LLR-326 says the search runs again "after acceptance". The code searches again on both, so the LLR understates it. Small wording point to fix with it: "offers one available provisioner ... only after consent" should say that the provisioner RUNS only after consent, since the offer is the request for consent.
- [RETURN] TC-350 -> at a Windows console with only a pre-3.11 runtime, decline and accept the install offer; a decline runs no provisioner, acceptance runs the declared one, and both search again and exit 1 with the install step -> it verifies LLR-326, which goes back. Its "both paths search again" contradicts LLR-326's "after acceptance" -> not ready: it must be re-judged with LLR-326 once SR-032's home for this behaviour is settled. The test it names passes (above), so this is about the text, not the evidence.

OUTCOME: RETURN rows=2

No registry cell was changed and no approval snapshot was taken. The corrective work is the first draft under the amendment section's Dispositions, which covers SR-032, LLR-326 and TC-350 together.

SITTING: JUDGED kinds=amendment;first-approval
