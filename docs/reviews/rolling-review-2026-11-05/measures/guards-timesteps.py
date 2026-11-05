import subprocess, sys, time
steps = sys.argv[1:]
total = 0.0
for s in steps:
    t = time.time()
    p = subprocess.run([sys.executable, "project-trajectory/scripts/check.py", "--run-step", s], capture_output=True, text=True)
    dt = time.time() - t; total += dt
    last = [l for l in (p.stdout + p.stderr).splitlines() if l.strip()][-1:] or [""]
    print(f"{dt:6.2f}s  {s:20} rc={p.returncode}  {last[0][:110]}")
print(f"{total:6.2f}s  TOTAL ({len(steps)} steps, sequential)")
