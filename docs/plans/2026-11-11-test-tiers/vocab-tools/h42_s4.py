"""HANDOFF 4.2/4.3, the dial: hand edits after r42_s4_dial.py.

The note explaining why the key was not called "attest level" goes: the key's
new name says what it holds, and the method it was avoiding is now `Vouch`.
The migrator ships: its manifest row.
"""

NOTE = (
    '# Named `operator_accepts_through`, never "attest level": `Vouch` is already\n'
    "# a Verification method in the SR vocabulary and the collision would be\n"
    "# permanent.\n"
)

EDITS = [
    ("project-trajectory/process.toml.template", "# level held before.\n#\n" + NOTE, "# level held before.\n"),
    ("docs/process.toml", "# level held before.\n#\n" + NOTE, "# level held before.\n#\n"),
    ("project-trajectory/scripts/kitlib/bootstrap_manifest.py",
     '    ("scripts/migrate_decisions.py", "scripts/migrate_decisions.py", "SR-225"),\n',
     '    ("scripts/migrate_decisions.py", "scripts/migrate_decisions.py", "SR-225"),\n'
     "    # The vocabulary migrator: every adopter runs it once, at the re-sync that\n"
     "    # brings the unified vocabulary in, since no reader of an earlier spelling\n"
     "    # is kept. Imports nothing from the kit.\n"
     '    ("scripts/migrate_vocabulary.py", "scripts/migrate_vocabulary.py", "SR-247"),\n'),
]
