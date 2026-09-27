bd9b4074 SOUND

- No findings. `project-trajectory/AGENTS.template.md:45` carries the exact substring mapped at `tests/test_held_rung_doctrine.py:31,40`.
- Removing it triggers the missing-pointer assertion at `tests/test_held_rung_doctrine.py:103-105`.
- Focused tests pass: 3 passed.