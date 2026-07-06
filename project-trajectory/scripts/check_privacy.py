#!/usr/bin/env python3
"""Secrets + privacy-leak lint — the deterministic floor (stdlib only).

Two classes of pattern, two gates (Thread 44):

  * **Secrets floor — always on** (opt-out). Private-key headers and a few
    universal credential shapes (GitHub, Slack, AWS, `sk-…` API keys) have
    nothing to do with identity, so they are scanned in **every** repo — the
    security net an ordinary identified project gets too. Opt out by tracking
    the one word `off` in `docs/secrets-scan` (same first-line parse as every
    declared-policy file; absent or any other value reads *on*, the safe
    default) — the deliberate exit for a repo whose content *is* secret-shaped
    (mark individual lines with `privacy-ok` first; `off` is the last resort).

  * **Identity-leak layer — policy-gated.** Only when `docs/commit-identity`
    declares an email pattern (anything but `inherit`) is the repo
    anonymous/pseudonymous, so these classes run under that policy alone:
      - home-directory path shapes carrying an OS username
        (`C:\\Users\\<x>`, `/home/<x>`, `/Users/<x>`) — placeholder-shaped
        usernames (`<x>`, `$HOME`, `%USERPROFILE%`, "username", ...) are exempt;
      - the current OS account name and hostname appearing anywhere;
      - email addresses that fail the declared policy pattern (RFC 2606 example
        domains are exempt — documentation needs examples);
      - the real name/email from **global** git config appearing in content
        (only when that global identity is not itself the declared one).

An `inherit` repo with `docs/secrets-scan: off` therefore exits 0 immediately,
paying nothing; every other repo runs at least the secrets floor.

Modes (each runs whichever of the two layers is active):

    (default)        scan the **staged diff** (added lines) — wired into
                     `.githooks/pre-commit`, blocks before the commit exists.
    --repo           sweep every tracked text file — wired as a process step in
                     `check.py` (catches what slipped in before the policy
                     existed or past `--no-verify`); CI-runnable.
    --range <spec>   scan a **commit range** the way `git log -p` shows it:
                     added lines, commit messages, and author lines of every
                     commit in the range — so a leak added in one commit and
                     removed in a later one is still caught (it ships in
                     history even though the final tree is clean). Used by
                     `.githooks/pre-push` over the outgoing range and by the
                     sync ritual's scrub base pass (process-options.md "Agent
                     iteration branch & sync").

False-positive affordance: a line containing `privacy-ok` (any case) is skipped
— mark documented example paths instead of training yourself to bypass the
hook. This file exempts itself from scanning (it is made of the patterns).

Honesty boundary (process-options.md "Commit identity & anonymity"): this is a
pattern lint, not a guarantee and not a DLP product. Judgment-layer review is
the pre-push reviewer / sync scrub; deep secrets scanning is a named external
category (gitleaks, trufflehog — product-layer, never rebuilt in the kit).
Exit codes: 0 clean/skipped, 1 findings, 2 usage or environment error.
"""

import argparse
import fnmatch
import getpass
import re
import socket
import subprocess
import sys
from pathlib import Path

# The inline allowlist marker: a line carrying it is never flagged.
ALLOW_MARKER = "privacy-ok"

# This script is made of the patterns it hunts, so it never scans itself (the
# one honest self-exemption; hiding a leak here is out of threat model).
SELF_NAME = "check_privacy.py"

# Home-dir path shapes. The username segment is deliberately word-ish only, so
# placeholder spellings (`<x>`, `${HOME}`, `%USERPROFILE%`, `{{user}}`, `*`)
# never match at all; generic real-dir names are exempted below.
HOME_RE = re.compile(
    r"(?:[A-Za-z]:[\\/]+(?:Users|home)|/home|/Users)[\\/]+([A-Za-z0-9._-]+)"
)
PLACEHOLDER_USERS = {
    "user",
    "username",
    "yourname",
    "your-name",
    "yourusername",
    "you",
    "someone",
    "somebody",
    "example",
    "name",
    "public",
    "default",
    "administrator",
    "admin",
}

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# RFC 2606/6761 reserved names — documentation examples, never real identities.
EXAMPLE_DOMAINS = ("example.com", "example.org", "example.net")
EXAMPLE_SUFFIXES = (".example", ".invalid", ".test", ".localhost")

KEY_RE = re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")
TOKEN_RES = (
    ("github token", re.compile(r"ghp_[A-Za-z0-9]{36}")),
    ("github fine-grained token", re.compile(r"github_pat_[A-Za-z0-9_]{22,}")),
    ("slack token", re.compile(r"xox[abprs]-[A-Za-z0-9-]{10,}")),
    ("aws access key id", re.compile(r"(?<![A-Z0-9])AKIA[0-9A-Z]{16}(?![A-Z0-9])")),
    (
        "api secret key",
        re.compile(r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{24,}(?![A-Za-z0-9_-])"),
    ),
)

# Identity terms shorter than this are too collision-prone to word-match.
MIN_TERM_LEN = 3
GENERIC_TERMS = PLACEHOLDER_USERS | {"localhost", "desktop", "laptop", "runner"}


def _utf8_console():
    """Emit UTF-8 whatever the OS console codepage is (same guard as check.py)."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def _first_declared_line(path):
    """The first non-empty, non-comment line of a declared-policy file, or None
    (absent/empty) — the parse every reader shares (hooks, agent_loop.py)."""
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    return None


def read_policy(root):
    """The first non-comment line of docs/commit-identity, or 'inherit'."""
    return _first_declared_line(root / "docs" / "commit-identity") or "inherit"


def read_secrets_scan(root):
    """Whether the always-on secrets floor is enabled. `docs/secrets-scan` with
    the one word `off` opts out; absent or any other value reads on (the safe
    default) — so an ordinary repo gets the floor without declaring anything."""
    return (_first_declared_line(root / "docs" / "secrets-scan") or "").lower() != "off"


def git(root, *args):
    """Run git in the repo; returns (returncode, stdout). Never raises on a
    missing git — the caller decides whether that is fatal for its mode."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root)] + list(args),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return proc.returncode, proc.stdout
    except OSError:
        return 127, ""


def _word_re(term):
    return re.compile(
        r"(?<![A-Za-z0-9_])" + re.escape(term) + r"(?![A-Za-z0-9_])", re.IGNORECASE
    )


class Scanner:
    """Compiles the active leak classes for one run.

    `secrets_on` gates the always-on credential floor (key/token shapes);
    `identity_on` gates the anonymity-only classes (home-dir usernames,
    account/hostname, off-policy emails, the global git identity). At least one
    is true whenever a Scanner is built — main() exits early otherwise."""

    def __init__(self, policy, root, secrets_on=True, identity_on=True):
        self.policy = policy.lower()
        self.secrets_on = secrets_on
        self.identity_on = identity_on
        self.identity_terms = []  # (label, compiled regex)
        if not identity_on:
            return  # the machine-identity probes are pure cost when unused

        def add_term(label, term):
            term = (term or "").strip()
            if len(term) >= MIN_TERM_LEN and term.lower() not in GENERIC_TERMS:
                self.identity_terms.append((label, _word_re(term)))

        try:
            add_term("current OS account", getpass.getuser())
        except Exception:  # no identity resolvable — nothing to match
            pass
        try:
            add_term("hostname", socket.gethostname())
        except OSError:
            pass
        # The *global* git identity is the machine's real one; in content it is
        # a leak — unless it is the declared identity itself (then the email
        # class already rules, and the name is presumably the public persona).
        rc, email = git(root, "config", "--global", "user.email")
        rc2, name = git(root, "config", "--global", "user.name")
        email, name = email.strip(), name.strip()
        if rc == 0 and email and not self._email_ok(email):
            add_term("global git email", email)
            if rc2 == 0 and name:
                add_term("global git name", name)

    def _email_ok(self, email):
        email = email.lower()
        domain = email.rsplit("@", 1)[-1]
        if domain in EXAMPLE_DOMAINS or domain.endswith(EXAMPLE_SUFFIXES):
            return True
        return fnmatch.fnmatchcase(email, self.policy)

    def scan_line(self, text):
        """Yield (class-label, excerpt) findings for one line of content."""
        if ALLOW_MARKER in text.lower():
            return
        if self.identity_on:
            for m in HOME_RE.finditer(text):
                if m.group(1).lower() not in PLACEHOLDER_USERS:
                    yield "home-dir path", m.group(0)
            for m in EMAIL_RE.finditer(text):
                if not self._email_ok(m.group(0)):
                    yield "email fails policy", m.group(0)
            for label, rx in self.identity_terms:
                m = rx.search(text)
                if m:
                    yield label, m.group(0)
        if self.secrets_on:
            m = KEY_RE.search(text)
            if m:
                yield "private key header", m.group(0)
            for label, rx in TOKEN_RES:
                m = rx.search(text)
                if m:
                    yield label, m.group(0)


def scan_diff_text(text, scanner):
    """Findings from `git diff` / `git log -p` output.

    Scans **added** lines (never removals — deleting a leak must not block),
    and outside diff bodies the commit message + Author lines, so a range scan
    covers what ships in *history*, not just the final tree. Returns a list of
    (location, label, excerpt)."""
    findings = []
    in_diff = False
    path = ""
    commit = ""
    new_line = 0

    def loc_commit():
        return "commit {}".format(commit[:9]) if commit else "(uncommitted)"

    for line in text.splitlines():
        if line.startswith("commit ") and re.match(r"commit [0-9a-f]{7,40}\b", line):
            in_diff = False
            commit = line.split()[1]
            continue
        if line.startswith("diff --git"):
            in_diff = True
            path = ""
            continue
        if in_diff:
            if line.startswith("+++ "):
                path = line[4:].strip()
                if path.startswith("b/"):
                    path = path[2:]
                continue
            if line.startswith("@@"):
                m = re.match(r"@@ -\S+ \+(\d+)", line)
                new_line = int(m.group(1)) if m else 0
                continue
            if line.startswith("+"):
                if not path.endswith(SELF_NAME):
                    for label, excerpt in scanner.scan_line(line[1:]):
                        findings.append(
                            ("{}:{}".format(path or "?", new_line), label, excerpt)
                        )
                new_line += 1
            continue
        # Outside a diff body: commit-message lines (indented) and the Author
        # line — a wrong author identity in outgoing history is itself a leak.
        if line.startswith("    ") or line.startswith("Author:"):
            for label, excerpt in scanner.scan_line(line):
                findings.append((loc_commit(), label, excerpt))
    return findings


def is_binary(data):
    return b"\0" in data[:8000]


def iter_repo_files(root):
    """Tracked files via git; fall back to a filesystem walk (skipping VCS and
    generated dirs) when the tree isn't a git checkout."""
    rc, out = git(root, "ls-files", "-z")
    if rc == 0 and out:
        for rel in out.split("\0"):
            if rel:
                yield rel
        return
    skip = {".git", "out", "node_modules", ".venv", "__pycache__"}
    for path in sorted(root.rglob("*")):
        if path.is_file() and not (set(path.relative_to(root).parts[:-1]) & skip):
            yield path.relative_to(root).as_posix()


def scan_repo(root, scanner):
    findings = []
    for rel in iter_repo_files(root):
        if rel.endswith(SELF_NAME):
            continue
        path = root / rel
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if is_binary(data):
            continue
        for n, line in enumerate(
            data.decode("utf-8", errors="replace").splitlines(), 1
        ):
            for label, excerpt in scanner.scan_line(line):
                findings.append(("{}:{}".format(rel, n), label, excerpt))
    return findings


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument(
        "--repo",
        action="store_true",
        help="sweep every tracked text file instead of the staged diff",
    )
    mode.add_argument(
        "--range",
        dest="rev_range",
        default=None,
        metavar="SPEC",
        help="scan a commit range as `git log -p` shows it (diffs + messages "
        "+ author lines), e.g. origin/main..HEAD or a lone SHA for a "
        "not-yet-published branch's full history",
    )
    ap.add_argument(
        "--root", default=".", help="repo root (default: current directory)"
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()

    policy = read_policy(root)
    identity_on = policy != "inherit"
    secrets_on = read_secrets_scan(root)
    if not identity_on and not secrets_on:
        print(
            "check_privacy: commit-identity 'inherit' and docs/secrets-scan "
            "'off' — nothing to check."
        )
        return 0

    layers = []
    if identity_on:
        layers.append("identity ({})".format(policy))
    if secrets_on:
        layers.append("secrets floor")
    layers_desc = " + ".join(layers)

    scanner = Scanner(policy, root, secrets_on=secrets_on, identity_on=identity_on)
    if args.repo:
        what = "repo sweep"
        findings = scan_repo(root, scanner)
    elif args.rev_range:
        what = "range " + args.rev_range
        rc, out = git(
            root, "log", "--no-color", "--unified=0", "-p", args.rev_range, "--"
        )
        if rc != 0:
            print(
                "check_privacy: git log failed for range {!r} (is this a git "
                "repo with that range?)".format(args.rev_range),
                file=sys.stderr,
            )
            return 2
        findings = scan_diff_text(out, scanner)
    else:
        what = "staged diff"
        rc, out = git(root, "diff", "--cached", "--no-color", "--unified=0")
        if rc != 0:
            print(
                "check_privacy: git diff --cached failed (not a git repo?)",
                file=sys.stderr,
            )
            return 2
        findings = scan_diff_text(out, scanner)

    if not findings:
        print("check_privacy: clean ({}; {}).".format(what, layers_desc))
        return 0
    for location, label, excerpt in findings:
        print("{}: [{}] {}".format(location, label, excerpt))
    print(
        "check_privacy: {} finding(s) in {} [{}]. Remove/rotate the secret or "
        "anonymize the content before it lands; a documented example line may "
        "carry '{}' to be exempt. The always-on secrets floor is opt-out via "
        'docs/secrets-scan (process-options.md "Commit identity & '
        'anonymity").'.format(len(findings), what, layers_desc, ALLOW_MARKER)
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
