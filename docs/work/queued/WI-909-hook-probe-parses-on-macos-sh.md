+++
id = "WI-909"
title = "The hooks' interpreter probe parses on macOS /bin/sh, and a shell-portability guard keeps the class out"
workstream = "process"
sr_refs = ["SR-046", "SR-032"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 1
+++

## Context

Filed by hand on 2026-10-13 at the owner's direction, after a commit on the
owner's Mac refused with `kit-python.sh: line 35: unexpected EOF while looking
for matching `''`. WI-880 (2026-10-10) put the default install text inside a
double-quoted `${KIT_DEV_SETUP_INSTALL:-…}` word, and that text contains an
apostrophe ("dev-setup's"). macOS's `/bin/sh` is bash 3.2, which reads that
apostrophe as an opening quote. The file fails to parse, so the pre-commit,
commit-msg and pre-push hooks all refuse on a stock Mac. dash and bash 5 parse
it, which is why the Linux and Windows bars stayed green. The hook tests
(`tests/test_pre_commit_hook.py`, 9 of 21 red on this Mac) sit in the slow
tier, so the smoke bar never ran them. Adopters who copied the probe into
`.githooks/` have the same failure.

## Done-when

- `project-trajectory/hooks/kit-python.sh` parses under macOS `/bin/sh`, and
  its refusal text is byte-identical to before.
- A guard catches the class on every platform, not only on a Mac: a stdlib
  static rule (no `'` inside a `${NAME<op>word}` word) plus `sh -n` over every
  tracked shell file, in the smoke tier. It is shown red against the broken
  file.
- `tests/test_pre_commit_hook.py` is green on macOS.
- RESYNC_PACK: an entry telling adopters to re-copy the probe.
