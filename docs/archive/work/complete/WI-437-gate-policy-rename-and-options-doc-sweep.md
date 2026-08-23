+++
id = "WI-437"
title = "OI-25 execution: rename the live runtime label that collides with the retired gate_policy configuration enum, and sweep PROCESS_OPTIONS.md's ten instructional lines onto current vocabulary, as ONE change. The new name describes WHO IS HOLDING a session (human-held/loop-held) and must follow the OI-21 stage semantics — it must not re-teach vocabulary the ladder retires. Leave the two hyphenated occurrences untouched (the live bootstrap.py --gate-policy flag and the docs/gate-policy.md deviation-register filename — a live interface, not residue). Verified precondition: no spine cell names the runtime label, so no re-attest window opens. Payoff: the four stale-text verdicts blocked on the collision unblock; re-run them and record the outcomes."
workstream = "lock-program"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 1
+++

## Deliverable

Completed 2026-08-13. The live runtime label renamed `gate_policy` →
`session_hold` (banner `session-hold`; values `human-held`/`loop-held`
unchanged) across agent_loop/intake and every prose reader; PROCESS_OPTIONS.md
swept off the retired enum (+316 B, baseline re-stamped through the
materializer); the `--gate-policy` flag and `docs/gate-policy.md` untouched as
live interfaces; three new tests pin the new name; zero registry edits. The
four blocked stale-text verdicts (SR-082/085/108/125) UNBLOCK — "gate policy"
in those rows can now only mean the retired enum, so each is judgeable; they
join the sitting batch rather than being resolved inline. The adversarial
round found two residues the sweep missed and both are fixed in the review
commit: the shipped README taught "under `attended` gate-policy" as live
admission vocabulary (now the `human_ratification_through` wording), and one
softer "declared gate policy" launcher line. One follow-on recorded, not
fixed: the gate-advance skill still teaches the enum at three lines — absorbed
by WI-445, which rewrites that skill wholesale. Build totals: full suite 2313
passed / 6 skipped on the branch; the rename's targeted modules 362 passed.
