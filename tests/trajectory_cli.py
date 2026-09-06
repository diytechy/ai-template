"""Command helpers split by the public trajectory surface under test."""

from conftest import SCRIPTS, run_py


def run_trajectory(root, *args):
    return run_py([SCRIPTS / "gen_trajectory.py", "--root", root, *args], cwd=root)


def run_status(root, *args):
    return run_trajectory(root, "--status", *args)
