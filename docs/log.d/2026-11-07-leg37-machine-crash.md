## 2026-11-07 — Headless leg 37 killed by a machine crash; the lease released (attended)

Leg 1 of run 20261107T160637Z-f93900 continued WI-996 and WI-1002. Three
attests read red because the leg's own wrapper exported `MSYS_NO_PATHCONV=1`,
which breaks git's `file://` shallow clones on Windows. With it removed, both
lanes' tests-first commits attested and committed. The leg then had both code
builds under way when the machine crashed at 13:48 (bugcheck 0xE2), killing the
launcher, the leg and its builders with no close-out and the lease held. At the
owner's direction, an attended session released the lease and ran `check-lane`
on both lanes (both pass) in place of the missed audit. The handoff
`handoff-2026-11-07c-attended-coordinator.md` records both lanes' uncommitted
builds, so the next run continues them.
