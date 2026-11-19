EDITS = [
    ("tests/test_done_when_blessing.py",
     "a call that exits 0 with a valid verdict is recorded\n    ACCEPTED by the route that ran it, and only then covers.",
     "a call that exits 0 with a valid verdict gets the\n    outcome RECORDED from the route that ran it, and only then covers."),
    ("tests/test_snapshot_readers.py",
     "so it must be covered by an ACCEPTED\n    verdict of each kind",
     "so it must be covered by a RECORDED\n    verdict of each kind"),
]
