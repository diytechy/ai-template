+++
id = "WI-192"
title = "Trace golden masters are platform-sensitive - Windows-generated goldens embed os.sep backslashes + mojibake em-dashes so the WI-081 golden net fails on POSIX; normalize the compared body + regenerate deliberately and verify on both platforms"
workstream = "scripts"
needs = ["WI-081"]
buildtier = "quick"
order = 199
+++

## Deliverable

WI-192 (2026-07-16): the WI-081 trace golden net made platform-stable, both artifacts living in the stdout capture path. (1) conftest.run_py now decodes captured output with encoding=utf-8 instead of a bare text=True - the kit scripts emit UTF-8 via _utf8_console (trace.py reconfigures stdout unconditionally), and text=True decoded through the Windows console codepage, mojibaking em-dashes AND section-signs into the goldens; the report.md portion was already clean (read via read_text utf-8), which is why only the ===STDOUT=== half forked. (2) test_trace_golden._normalize now forces POSIX separators on the compared body so a Windows os.sep 'Report -> docs\test\report.md' tail matches the forward-slash POSIX form (report.md itself is already POSIX via .as_posix()). Goldens regenerated deliberately (UPDATE_TRACE_GOLDEN=1) from the fixed capture; diff confined to the ===STDOUT=== portions (real em-dashes + forward slashes, no counts moved). Now identical across platforms by construction (UTF-8 emit + UTF-8 decode + POSIX-normalize); live Windows confirmation defers to the cross-OS CI on push (OI-3), the class the matrix exists to catch. Two new stability tests guard against a silent per-platform re-fork: test_normalize_forces_posix_separators (unit) + test_goldens_are_platform_stable (the checked-in goldens carry no backslash and no cp1252 mojibake). Full suite 944p/2s; no product-script/spine/byte-budgeted change (test-only fix).
