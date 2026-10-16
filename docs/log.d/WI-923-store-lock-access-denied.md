## 2026-10-15 — WI-923: the store lock's access-denied create, stress-run on Windows

The builder's two readings of the Windows stress run (D7), before the
coordinator's re-run. The harness is the scratch script stress_dir_lock.py,
kept outside the lane: six threads each take and release the real `dir_lock`
on one fresh temporary directory, with the default wait, for 10 s; inside the
lock a shared holder count records any overlap, and every exception is caught,
counted by type, and the loop goes on. Interpreter: Python 3.11.9 on the
Windows box.

- Trunk's code (`session_keep` at 4c216fd2f): `holds=9802 overlaps=0 escaped=PermissionError: 143`, exit 1. <!-- fig: cmd="python -B stress_dir_lock.py --scripts <4c216fd2f's project-trajectory/scripts> --threads 6 --seconds 10" rev=4c216fd2f -->
- The change (the lane's `session_keep`, uncommitted on 61c6d2afa): `holds=10308 overlaps=0 escaped=none`, exit 0. <!-- fig: cmd="python -B stress_dir_lock.py --scripts project-trajectory/scripts --threads 6 --seconds 10" rev="61c6d2afa + the round-1 build" -->

The coordinator's re-run (2026-10-15h session), the same harness and
parameters, both run at below-normal priority (the owner's setting for local
test jobs), trunk's code from a detached scratch worktree at the lane's trunk
base, removed afterwards; the change at the lane's committed tip, whose
`session_keep` is unchanged since build round 1:

- Trunk's code (`session_keep` at 4c216fd2f): `holds=15833 overlaps=0 escaped=PermissionError: 161`, exit 1. <!-- fig: cmd="python -B stress_dir_lock.py --scripts <4c216fd2f's project-trajectory/scripts> --threads 6 --seconds 10" rev=4c216fd2f -->
- The change (the lane's `session_keep` at b971ea636): `holds=16184 overlaps=0 escaped=none`, exit 0. <!-- fig: cmd="python -B stress_dir_lock.py --scripts project-trajectory/scripts --threads 6 --seconds 10" rev=b971ea636 -->

D7 holds: trunk's code lets the access refusal escape under contention, the
change takes and releases the lock without an overlap or an escape.
