4d943d27 NOT YET SOUND

- **major** `docs/test/test-cases.toml:1337` — TC-137 still describes a “red composed-tree bar” and “candidate parked.” Its evidence explicitly tests the replacement refresh-bar behavior: the claimed branch remains, and no candidate branch is created (`tests/test_dispatch.py:777-808`). Fix: say the red refresh bar stops the run with the claimed branch retained.

LLR-140, LLR-143, and WI-669’s adjudication census/list are otherwise consistent and minimal.