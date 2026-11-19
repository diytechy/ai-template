"""AGENTS.template.md has a hard cap of 10,000 bytes (test_bootstrap), and
h47g_prose.py took it to 10,019. The three "bar"s there mean a stage gate,
so "gate" (one byte over "bar") replaces the longer words h47g_prose wrote.
With h47h_step's "shared step" (one byte under "stage") the file is back
under the cap."""

LINES = [
    ("project-trajectory/AGENTS.template.md", 39, "before a stage is accepted.", "before a gate."),
    ("project-trajectory/AGENTS.template.md", 46, "The check harness is the standard:", "The check harness is the gate:"),
    ("project-trajectory/AGENTS.template.md", 153, "  stage. When reality", "  gate. When reality"),
]

# and six bytes of headroom, from a sentence the edit already touched
LINES.append(
    ("project-trajectory/AGENTS.template.md", 38, "The matrix is generated (`scripts/trace.py`) and must", "The generated matrix (`scripts/trace.py`) must")
)
