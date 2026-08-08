#!/usr/bin/env python3
"""Secrets + privacy-leak lint — the deterministic floor (stdlib only).

Two classes of pattern, two gates (Thread 44; identity->privacy reframe):

  * **Secrets floor — always on** (opt-out). Private-key headers and a few
    universal credential shapes (GitHub, Slack, AWS, `sk-…` API keys) have
    nothing to do with identity, so they are scanned in **every** repo — the
    security net an ordinary identified project gets too. Opt out by tracking
    the one word `off` in `docs/secrets-scan` (same first-line parse as every
    declared-policy file; absent or any other value reads *on*, the safe
    default) — the deliberate exit for a repo whose content *is* secret-shaped
    (mark individual lines with `privacy-ok` first; `off` is the last resort).

  * **Privacy layer — toggle-gated.** Only when `docs/privacy-check` is `true`
    does the repo run the PII/identity-leak classes. It defends *privacy* (no
    real, contactable person), not *attribution* (which account authored is the
    user's own git config, not pinned here):
      - the commit **author email** must be in the exempt allowlist
        (EXEMPT_EMAILS below) — a private author blocks (`--author` mode);
      - home-directory path shapes carrying an OS username
        (`C:\\Users\\<x>`, `/home/<x>`, `/Users/<x>`) — placeholder-shaped
        usernames (`<x>`, `$HOME`, `%USERPROFILE%`, "username", ...) are exempt;
      - the current OS account name and hostname appearing anywhere;
      - email addresses not in the exempt allowlist (RFC 2606 example domains
        are always exempt — documentation needs examples);
      - the real name/email from **global** git config appearing in content
        (only when that global identity is not itself exempt).

A repo with `docs/privacy-check` off and `docs/secrets-scan: off` therefore
exits 0 immediately, paying nothing; every other repo runs at least the
secrets floor.

Modes (each runs whichever of the two layers is active):

    (default)        scan the **staged diff** (added lines) — wired into
                     `.githooks/pre-commit`, blocks before the commit exists.
    --author         check the commit **author email** (git var
                     GIT_AUTHOR_IDENT) against the exempt allowlist — wired into
                     `.githooks/pre-commit`; a private author blocks. Privacy
                     layer only (a no-op when docs/privacy-check is off).
    --message <file> scan a **commit-message file** — wired into
                     `.githooks/commit-msg`, so a leak in the title/body blocks
                     at the first commit, not only at push.
    --repo           sweep every tracked text file — wired as a process step in
                     `check.py` (catches what slipped in before the gate was
                     enabled or past `--no-verify`); CI-runnable.
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

Honesty boundary (process-options.md "Commit identity & privacy"): this is a
pattern lint, not a guarantee and not a DLP product. Judgment-layer review is
the pre-push reviewer / sync scrub; deep secrets scanning is a named external
category (gitleaks, trufflehog — product-layer, never rebuilt in the kit).
Exit codes: 0 clean/skipped, 1 findings, 2 usage or environment error.

Contracts: IF-005, IF-032, IF-043 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import fnmatch
import getpass
import re
import socket
import subprocess
import sys
import tomllib
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

# Exempt-email allowlist for the privacy layer — addresses that may appear as
# author or in content without flagging. This is the PRIVACY allowlist (not an
# identity pin): a no-reply / provider-anonymized address carries no contactable
# person, so it is not a PII leak even if it carries an attribution handle.
# fnmatch globs, matched case-insensitively; the RFC 2606 example domains above
# are exempt separately.
#
# DEFAULT `*noreply*` — any no-reply-form address. Broad on purpose (privacy, not
# identity): it also admits handle-bearing forms like GitHub's
# ID+USERNAME@users.noreply.github.com, so it is a PII-risk reduction, not an
# anonymity guarantee. For a stricter posture, replace it with the enumerated
# exact-form list below:
#     EXEMPT_EMAILS = [
#         "*@users.noreply.github.com",   # GitHub per-user no-reply
#         "*@users.noreply.gitlab.com",   # GitLab per-user no-reply
#         "noreply@anthropic.com",        # Claude / Anthropic co-author trailer
#         # add other LLM / obscured-service no-reply addresses here
#     ]
EXEMPT_EMAILS = ["*noreply*"]

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


def _process_gate(root, key):
    """One `[policies]` gate out of `docs/process.toml` (SN-028), read the way
    the git hooks read it — which is the whole point of this function.

    Returns True (on), False (off), or None (this file has nothing to say;
    fall through to the legacy one-word file).

    FAILS CLOSED IN THE SAME DIRECTION THE HOOKS DO. Two grammars read this
    file — `tomllib` here, a pure-sh `grep -E` in the hooks (M-42: a
    Python-less box must still refuse to skip a declared privacy gate) — and
    every shape only one of them understands is a silent flip of a security
    gate. So a file that EXISTS but does not parse, or that declares the key
    as something other than a boolean, reads ON here exactly as it does there:
    loud, and never a quiet opt-out. A MIXED config (this file and the legacy
    one both declaring the gate) reads ON for the same reason.

    A LOCAL reader, per the F5 independently-copyable-script rule that already
    keeps `_first_declared_line` here rather than importing the coordinator
    layer. `tests/test_process_config.py` pins this and the hooks' sh equal
    over a table of adversarial file shapes."""
    path = root / "docs" / "process.toml"
    if not path.is_file():
        return None
    try:
        # utf-8-sig: a BOM is not legal TOML but is invisible to the hooks'
        # read — the two must not diverge over one byte.
        data = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return True  # unparseable but present: fail closed, like the hooks
    table = data.get("policies")
    value = table.get(key) if isinstance(table, dict) else None
    if value is None:
        # The key may still be somewhere the hooks WILL act on (a dotted key,
        # the wrong section). Their read is textual, so ours must be too
        # before it concludes "not declared".
        return True if _text_declares(path, key) else None
    return value if isinstance(value, bool) else True


_DECLARED_RE_CACHE = {}


def _text_declares(path, key):
    """Whether the file's TEXT declares `key` on a non-comment line — the
    hooks' broad `declared` test, mirrored so this reader cannot conclude
    "absent" about a key they would act on."""
    pattern = _DECLARED_RE_CACHE.get(key)
    if pattern is None:
        pattern = _DECLARED_RE_CACHE[key] = re.compile(
            r"(?:^|[^A-Za-z0-9_])" + re.escape(key) + r"\s*="
        )
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return False
    return any(
        pattern.search(line)
        for line in text.splitlines()
        if not line.lstrip().startswith("#")
    )


def read_privacy_enabled(root):
    """Whether the privacy layer is on: `docs/process.toml` `[policies]
    privacy_check = true`, else (migration window) docs/privacy-check's first
    non-comment line being `true` (any case). Absent/any other value → False
    (off) — the successor to the old commit-identity `inherit` default.

    A MIXED config — both homes declaring the gate — reads ON. The Python
    coordinator layer REFUSES that state outright; this checker cannot refuse
    (it is called from hooks that must still make a decision), so it takes the
    only safe reading."""
    declared = _process_gate(root, "privacy_check")
    legacy = (
        _first_declared_line(root / "docs" / "privacy-check") or ""
    ).lower() == "true"
    if declared is None:
        return legacy
    return bool(declared) or legacy


def email_ok(email):
    """True when an email is exempt from privacy flagging: an RFC 2606 example
    domain, or a match against any EXEMPT_EMAILS glob (case-insensitive)."""
    email = email.lower()
    domain = email.rsplit("@", 1)[-1]
    if domain in EXAMPLE_DOMAINS or domain.endswith(EXAMPLE_SUFFIXES):
        return True
    return any(fnmatch.fnmatchcase(email, pat.lower()) for pat in EXEMPT_EMAILS)


def read_secrets_scan(root):
    """Whether the always-on secrets floor is enabled. `docs/process.toml`
    `[policies] secrets_scan = false` opts out; else (migration window)
    `docs/secrets-scan` with the one word `off`; absent or any other value
    reads on (the safe default) — so an ordinary repo gets the floor without
    declaring anything."""
    declared = _process_gate(root, "secrets_scan")
    if declared is not None:
        return bool(declared)
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
    `privacy_on` gates the privacy classes (home-dir usernames, account/
    hostname, non-exempt emails, the global git identity). At least one is true
    whenever a Scanner is built — main() exits early otherwise."""

    def __init__(self, root, secrets_on=True, privacy_on=True):
        self.secrets_on = secrets_on
        self.privacy_on = privacy_on
        self.identity_terms = []  # (label, compiled regex)
        if not privacy_on:
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
        # a leak — unless it is itself exempt (an exempt email is not PII, and
        # the name is then presumably the public persona).
        rc, email = git(root, "config", "--global", "user.email")
        rc2, name = git(root, "config", "--global", "user.name")
        email, name = email.strip(), name.strip()
        if rc == 0 and email and not email_ok(email):
            add_term("global git email", email)
            if rc2 == 0 and name:
                add_term("global git name", name)

    def scan_line(self, text):
        """Yield (class-label, excerpt) findings for one line of content."""
        if ALLOW_MARKER in text.lower():
            return
        if self.privacy_on:
            for m in HOME_RE.finditer(text):
                if m.group(1).lower() not in PLACEHOLDER_USERS:
                    yield "home-dir path", m.group(0)
            for m in EMAIL_RE.finditer(text):
                if not email_ok(m.group(0)):
                    yield "email not in exempt allowlist", m.group(0)
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


def report(findings, what, layers_desc):
    """Print findings for a scan of `what`; return the process exit code."""
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
        'privacy").'.format(len(findings), what, layers_desc, ALLOW_MARKER)
    )
    return 1


def check_author(root):
    """Validate the commit author email against the exempt allowlist — the
    identity->privacy cross-check. Reads `git var GIT_AUTHOR_IDENT`, the identity
    the next commit would carry."""
    rc, ident = git(root, "var", "GIT_AUTHOR_IDENT")
    if rc != 0 or not ident.strip():
        print(
            "check_privacy: could not resolve the commit author identity "
            "(git var GIT_AUTHOR_IDENT) — is git configured?",
            file=sys.stderr,
        )
        return 2
    m = re.search(r"<([^>]*)>", ident)
    email = (m.group(1) if m else "").strip()
    if email and email_ok(email):
        print("check_privacy: clean (author {}).".format(email))
        return 0
    print(
        "check_privacy: commit author email {!r} is not in the exempt allowlist "
        "(EXEMPT_EMAILS); a private identity must not author commits on a "
        "privacy-checked repo. Set a repo-local no-reply identity, e.g.:\n"
        "  git config user.email <you>@users.noreply.github.com".format(
            email or "unset"
        ),
        file=sys.stderr,
    )
    return 1


def scan_message(msg_path, scanner, layers_desc):
    """Scan a commit-message file (title + body). git's own comment lines
    (stripped from the final message) are skipped."""
    try:
        text = Path(msg_path).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(
            "check_privacy: cannot read message file {!r}: {}".format(msg_path, exc),
            file=sys.stderr,
        )
        return 2
    findings = []
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith("#"):
            continue
        for label, excerpt in scanner.scan_line(line):
            findings.append(("commit message:{}".format(n), label, excerpt))
    return report(findings, "commit message", layers_desc)


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
    mode.add_argument(
        "--author",
        action="store_true",
        help="check the commit author email (git var GIT_AUTHOR_IDENT) against "
        "the exempt allowlist; a private author blocks (privacy layer only)",
    )
    mode.add_argument(
        "--message",
        dest="message_file",
        default=None,
        metavar="FILE",
        help="scan a commit-message file (wired into .githooks/commit-msg)",
    )
    ap.add_argument(
        "--root", default=".", help="repo root (default: current directory)"
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()

    privacy_on = read_privacy_enabled(root)
    secrets_on = read_secrets_scan(root)
    if not privacy_on and not secrets_on:
        print(
            "check_privacy: privacy check and secrets floor are both OFF "
            "(docs/process.toml [policies]) — nothing to check."
        )
        return 0

    layers = []
    if privacy_on:
        layers.append("privacy")
    if secrets_on:
        layers.append("secrets floor")
    layers_desc = " + ".join(layers)

    if args.author:
        # Author identity is a privacy-layer concern; the secrets floor does not
        # apply to an email. A no-op when the privacy layer is off.
        if not privacy_on:
            print(
                "check_privacy: privacy check off (docs/process.toml "
                "[policies] privacy_check) — "
                "author not checked."
            )
            return 0
        return check_author(root)

    scanner = Scanner(root, secrets_on=secrets_on, privacy_on=privacy_on)
    if args.message_file:
        return scan_message(args.message_file, scanner, layers_desc)
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

    return report(findings, what, layers_desc)


if __name__ == "__main__":
    sys.exit(main())
