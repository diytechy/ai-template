Reviewed: {sha}

Verified: drove the shipped launch path on a real interpreter.

Coverage:
- [run] lines: TC-047 and the new real-interpreter regression pass for an older interpreter on PATH, with independently confirmed red-before behavior. POSIX shim execution is UNCOVERED here because sh fails before executing it.
- [TC-HARDEN] add a TC that launches through cmd's current-directory lookup.

- [MAJOR] project-trajectory/scripts/run_menu.py:223 -> bare python is not exact on Windows when cmd's current-directory lookup is enabled -> make the launch boundary exclude current-directory lookup -> @Software-Engineer
- [MAJOR] .claude/settings.json:1 -> the coordinator workstation has no guard hooks after the committed-hook removal -> complete the workstation opt-in before landing -> @Driver
- [MINOR] docs/requirements/system-requirements.toml:133 -> for clarity: SR-020 names the obsolete module -> name the shared probe -> @System-Engineer
VERDICT: CHANGES-REQUESTED findings=3
