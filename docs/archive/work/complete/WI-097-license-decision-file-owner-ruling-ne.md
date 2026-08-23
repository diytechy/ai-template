+++
id = "WI-097"
title = "LICENSE decision + file (owner ruling needed; H3)"
workstream = "docs"
safety_class = "protected"
order = 96
+++

## Deliverable

Apache-2.0 ruled (OI-4, 2026-07-25) and applied: root LICENSE + NOTICE, an identical copy INSIDE the portable unit (project-trajectory/LICENSE) so the terms survive the copy-in step, a README license paragraph, and bootstrap.py's new write_kit_license() stamping the full text into every scaffold at docs/kit-license under a header scoping it to the copied kit files only (the adopter's code and generated artifacts stay theirs). Guards: test_kit_license_travels_inside_the_portable_unit (root/kit copies byte-identical) + test_scaffold_records_the_kit_license_and_its_scope. Clears deep-review H-3.
