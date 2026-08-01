+++
id = "WI-303"
title = "Single-click onboarding dead-ends on a fresh Mac - dev-setup.command installs the Command Line Tools, but CLT ships Python 3.9 and macOS has no first-party 3.11+, so the double-click path reaches '[missing] runtime' and every remedy requires leaving the flow. Owner goal 2026-07-25: all dependencies sprout from one double-click."
workstream = "scripts"
needs = ["WI-302"]
buildtier = "medium"
safety_class = "ordinary"
order = 300
+++

## Deliverable

Landed 2026-07-25. dev-setup.command gains a runtime rung between the CLT step and the hand-off: when no 3.11+ is found it shows exactly what will be installed and from where, takes ONE consented [y/N], then downloads the PINNED python.org macOS .pkg and verifies it TWICE before executing anything - pinned SHA-256 (integrity: the exact artifact the kit was tested against) then pkgutil --check-signature for the Python Software Foundation team id BMM5U3QVKW plus Apple notarization (authenticity). Any gate failing refuses and exits 1 with nothing run. Pinned: Python 3.13.14, sha256 8e58affb...d2e8. OWNER RULINGS (2026-07-25) encoded here: (a) mechanism = signed .pkg over uv/brew, because it is Apple-notarized, one hop, and lands on PATH where discovery finds it; (b) blast radius = THIS REPO ONLY - dev-setup.template.command and dev-setup.sh stay detect-only so adopters inherit no network fetch until this is proven; (c) consent = one prompt, matching the repo's consent-first posture. This REFINES rather than reverses WI-302: that ruling forbids executing UNVERIFIABLE code (curl|sh is unverifiable by construction - a server can serve different bytes to a pipe); a pinned, notarized, signature-checked artifact is verifiable provenance. Verified live end-to-end with fakes: tampered download -> CHECKSUM MISMATCH, exit 1, sudo/installer never reached; hash-valid but wrong team id -> SIGNATURE CHECK FAILED, nothing run; real artifact -> both gates pass and it reaches installer -pkg. Tests pin the ORDER (verification precedes execution - the invariant a refactor would silently break), the pin's well-formedness and floor-satisfaction, fail-closed on each gate, and that the shipped template stays detect-only. MAINTENANCE: re-stamp the version+hash when the kit moves Python; the re-stamp command is in the file.
