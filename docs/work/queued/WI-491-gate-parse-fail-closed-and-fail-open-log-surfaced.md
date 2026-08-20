+++
id = "WI-491"
title = "Align the subagent gate's present-but-unparseable arm fail-closed and surface the fail-open log in the session banner (OI-46 ruled (1a)+(2a), 2026-08-20)"
specref = "docs/requirements/open-items.toml#OI-46"
workstream = "scripts"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Executes OI-46's ruling — (1a) + (2a) as recommended, both halves in this
one WI.

- **(1a) The parse asymmetry aligns.** `subagent_gate.py` currently maps an
  unreadable OR unparseable `docs/process.toml` to undeclared-therefore-
  allow, while its two twin readers (the hook's grep reader, the loop's
  tomllib reader) read a PRESENT-but-broken file as fail-closed. After this
  WI: present-but-unparseable = ask/hold (fail-closed), ABSENCE stays allow
  — the ruled opt-in posture is untouched, and the change can only NARROW
  the fail-open window. The tool-error fail-open arm stays (SN-006's
  relaxed posture keeps it).
- **(2a) The fail-open log becomes auditable.** Every allow-on-error
  appends to `out/subagent-gate.log` and nothing reads it. After this WI
  the session banner surfaces its tail count, and a test pins that the
  surface exists — the cheapest form in which the record becomes a record.
- **Tests:** WI-477's M-13 contract tests pin the CURRENT divergence
  honestly; extend them to pin the new fail-closed arm and the banner
  count. Three readers, one answer, one test surface.
- **RESYNC entry owed:** this is a behavior change in shipped supervision
  machinery (the gate holds where it used to allow, on a corrupted policy
  file).
