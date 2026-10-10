"""The one reading of a shell command line: its simple commands, each the list
of its words, with the shell's own quoting.

WHY THIS EXISTS (WI-834, REVIEW-A F1). The coordinator guard's hook decides,
inside the blackout window, whether a main session's `Bash` or `PowerShell`
call starts a model CLI. It read the line with regexes that ignored quoting:
`FOO="two words" claude -p x` read the command `words`, `env -S 'claude -p
x'` read none, and `echo 'pause; claude notes'` split at the quoted `;`. A
command line is another process's input (the agent CLI's shell tool), so it is
read once, here, the way its shell reads it, and the guard consumes only the
words this returns. Pure functions over text: no file, no process.

What it reads, per dialect:

  * `posix` (the Bash tool): single quotes, double quotes (in which a
    backslash escapes only `$`, a backtick, `"`, `\\` and a newline, and
    substitutions act), backslash escapes, `$'...'`, comments, the operators
    `&&`, `||`, `;;`, `|&`, `;`, `|`, `&`, `(`, `)` and newlines as command
    boundaries, redirections with their targets, and here-document bodies
    (to their delimiter line);
  * `powershell` (the PowerShell tool): single quotes with a doubled quote
    inside, double quotes with backtick escapes and doubled quotes, backtick
    escapes, `@'...'@` and `@"..."@` here-strings, comments, the same
    operators plus `{` and `}` as boundaries, and redirections.

In both, the command lines nested in `$(...)` (and POSIX backticks) are read
too and appended as further commands. A body the shell expands (a
here-document whose delimiter is unquoted, a `@"..."@` here-string) is read
the way the shell reads it: its substitutions are read, its escapes act and
its quotes are literal characters (REVIEW-A round 2, F1). A body the shell
keeps literal (a delimiter with any quote or backslash in it, a `@'...'@`
here-string) is data and is not read. A quoted operator is part of its word,
never a boundary.

Each word is a `Word`: its text, plus `spans`, the offsets of every quoted
piece in it, so every character is known to be quoted or not. The text alone
cannot tell PowerShell's `$r = 'claude'` (a value) from `$r = claude` (a
command), nor the operator in `$h['answer']=claude` from the `=` in
`$h['k=v']`; the spans can (round 016 F1, decision D-020; round 020 O1).

A line it cannot read (an unclosed quote, substitution or here-string) raises
`Unreadable`; the caller decides what that means (the guard refuses it inside
the window: decision D-010 in docs/decisions/wi-834.toml).
"""

import re

DIALECTS = ("posix", "powershell")
# Each dialect's command boundaries (longest first) and the characters that
# end an unquoted word.
_OPERATORS = {
    "posix": ("&&", "||", ";;", "|&", ";", "|", "&", "(", ")", "\n"),
    "powershell": ("&&", "||", ";", "|", "&", "(", ")", "{", "}", "\n"),
}
_WORD_END = {
    "posix": frozenset(" \t\r\n;&|()<>"),
    "powershell": frozenset(" \t\r\n;&|(){}<>"),
}
# A descriptor duplication (`2>&1`, `>&-`) is whole; any other redirection
# takes the next word as its target (a here-document's, its delimiter).
_DUPLICATION = re.compile(r"(?:\d+|\*)?[<>]&(?:\d+-?|-)(?=[\s;&|()<>]|$)")
_REDIRECTION = re.compile(r"(?:\d+|\*)?(<<<|<<-|<<|>>|&>>|&>|>\||<>|>&|<&|>|<)")
_HERE_STRING = re.compile(r"@(['\"])\r?\n")


class Word(str):
    """One word's text, quotes and escapes removed. `spans` holds the
    half-open `(start, end)` offsets of each quoted piece in it (a quote, a
    `$'...'` or a here-string), in order; a character is quoted when a span
    holds it.

    Implements: SR-229, LLR-300
    """

    spans = ()

    def quoted(self, i):
        """Whether the character at offset `i` was quoted."""
        return any(start <= i < end for start, end in self.spans)

    @property
    def opens_quoted(self):
        """Whether the word begins with a quoted piece (an empty `''`
        included): in PowerShell, a value rather than a command."""
        return bool(self.spans) and self.spans[0][0] == 0


class Unreadable(ValueError):
    """A shell command line that cannot be read: an unclosed quote,
    substitution or here-string. Its text names which.

    Implements: SR-229, LLR-300
    """


def segments(command, dialect="posix"):
    """The simple commands of `command` read as `dialect` reads it, each the
    list of its words with quotes and escapes removed, in order, followed by
    those of the command lines nested in its substitutions. Empty commands
    are dropped. Raises `Unreadable`.

    Implements: SR-229, LLR-300
    """
    scanner = _Scanner(command, dialect)
    found = [[]]
    for kind, text in scanner.tokens():
        if kind == "op":
            found.append([])
        elif kind == "word":
            found[-1].append(text)
    for inner in scanner.nested:
        found.extend(segments(inner, dialect))
    return [words for words in found if words]


class _Scanner:
    """One pass over a command line in one dialect: its tokens
    (`("word", text)` unquoted, `("op", text)` a command boundary,
    `("redirect", text)`) and, in `nested`, the command lines of the
    substitutions met inside words."""

    def __init__(self, text, dialect, start=0):
        self.text, self.i, self.dialect = text, start, dialect
        self.posix = dialect == "posix"
        self.escape = "\\" if self.posix else "`"
        self.nested = []
        self._heredocs = []

    def tokens(self, closing=False):
        """Every token to the end, or with `closing` to the `)` that closes
        a substitution."""
        out, depth = [], 0
        while True:
            self._blank()
            if self.i >= len(self.text):
                if closing:
                    raise Unreadable("an unclosed $( substitution")
                return out
            token = self._token()
            if closing and depth == 0 and token == ("op", ")"):
                return out
            depth += {("op", "("): 1, ("op", ")"): -1}.get(token, 0)
            out.append(token)

    def _blank(self):
        """Past blanks, escaped newlines and a comment."""
        t = self.text
        while self.i < len(t):
            if t[self.i] in " \t\r":
                self.i += 1
            elif t.startswith(self.escape + "\n", self.i):
                self.i += 2
            elif t[self.i] == "#":
                end = t.find("\n", self.i)
                self.i = len(t) if end < 0 else end
            else:
                return

    def _token(self):
        t = self.text
        whole = _DUPLICATION.match(t, self.i)
        if whole:
            self.i = whole.end()
            return ("redirect", whole.group())
        redirect = _REDIRECTION.match(t, self.i)
        if redirect:
            return self._redirect(redirect)
        for op in _OPERATORS[self.dialect]:
            if t.startswith(op, self.i):
                self.i += len(op)
                if op == "\n":
                    self._heredoc_bodies()
                return ("op", op)
        return ("word", self._word())

    def _redirect(self, match):
        """A redirection with its target; a here-document's body is passed
        over where its line ends."""
        self.i = match.end()
        self._blank()
        start = self.i
        target = self._word()
        if self.posix and match.group(1) in ("<<", "<<-"):
            # Any quote or backslash in the delimiter keeps the body literal.
            literal = any(q in self.text[start : self.i] for q in "'\"\\")
            self._heredocs.append((target, match.group(1) == "<<-", literal))
        return ("redirect", match.group())

    def _heredoc_bodies(self):
        """Past the bodies of the here-documents the ended line opened; a
        body whose delimiter is unquoted is read for its substitutions."""
        for delimiter, tabs, literal in self._heredocs:
            body = self._heredoc_body(delimiter, tabs)
            if not literal:
                self.nested.extend(_Scanner(body, self.dialect)._expansions())
        self._heredocs = []

    def _heredoc_body(self, delimiter, tabs):
        """One here-document body, to its delimiter line (or the end of the
        text), `<<-`'s leading tabs removed. The body is found before it is
        read, as the shell finds it."""
        t, lines = self.text, []
        while self.i < len(t):
            end = t.find("\n", self.i)
            end = len(t) if end < 0 else end
            line = t[self.i : end].rstrip("\r")
            self.i = min(end + 1, len(t))
            line = line.lstrip("\t") if tabs else line
            if line == delimiter:
                break
            lines.append(line)
        return "\n".join(lines)

    def _expansions(self):
        """The command lines of the substitutions in an expandable body: the
        whole text read as the shell expands a here-document or a `@"`
        here-string, where an escape and `$(...)` (and a POSIX backtick) act
        and a quote is a literal character. Raises `Unreadable`."""
        t = self.text
        while self.i < len(t):
            if t[self.i] == self.escape:
                self.i += 2
            elif t.startswith("$(", self.i):
                self._substitution()
            elif self.posix and t[self.i] == "`":
                self._backtick()
            else:
                self.i += 1
        return self.nested

    def _word(self):
        """One word, its quotes and escapes removed, as a `Word` that keeps
        the span of each quoted piece."""
        parts, spans, size = [], [], 0
        ends = _WORD_END[self.dialect]
        while self.i < len(self.text) and self.text[self.i] not in ends:
            quoted = self._opens_quote()
            piece = self._piece()
            if quoted:
                spans.append((size, size + len(piece)))
            parts.append(piece)
            size += len(piece)
        word = Word("".join(parts))
        word.spans = tuple(spans)
        return word

    def _opens_quote(self):
        """Whether the piece at the cursor is quoted: a quote, a POSIX `$'`
        or a PowerShell here-string."""
        t = self.text
        if t[self.i] in "'\"":
            return True
        if self.posix:
            return t.startswith("$'", self.i)
        return bool(_HERE_STRING.match(t, self.i))

    def _piece(self):
        t, c = self.text, self.text[self.i]
        if not self.posix and _HERE_STRING.match(t, self.i):
            return self._here_string()
        if c == "'":
            return self._single()
        if c == '"':
            return self._double()
        if c == self.escape:
            return self._escaped(quoted=False)
        if t.startswith("$(", self.i):
            return self._substitution()
        if self.posix and t.startswith("$'", self.i):
            end = self._unescaped(self.i + 2, "'", "$' quote")
            start, self.i = self.i + 2, end + 1
            return t[start:end]
        if c == "`":
            return self._backtick()
        self.i += 1
        return c

    def _single(self):
        """A single-quoted string, literal; PowerShell doubles a quote in it."""
        t, out = self.text, []
        self.i += 1
        while True:
            end = t.find("'", self.i)
            if end < 0:
                raise Unreadable("an unclosed ' quote")
            out.append(t[self.i : end])
            self.i = end + 1
            if self.posix or not t.startswith("'", self.i):
                return "".join(out)
            out.append("'")
            self.i += 1

    def _double(self):
        """A double-quoted string, in which escapes and substitutions act."""
        t, out = self.text, []
        self.i += 1
        while self.i < len(t):
            c = t[self.i]
            if not self.posix and t.startswith('""', self.i):
                out.append('"')
                self.i += 2
            elif c == '"':
                self.i += 1
                return "".join(out)
            elif c == self.escape:
                out.append(self._escaped(quoted=True))
            elif t.startswith("$(", self.i) or c == "`":
                out.append(self._substitution() if c == "$" else self._backtick())
            else:
                out.append(c)
                self.i += 1
        raise Unreadable('an unclosed " quote')

    def _escaped(self, quoted):
        """An escaped character; inside POSIX double quotes a backslash
        escapes only `$`, a backtick, a quote, a backslash or a newline."""
        nxt = self.text[self.i + 1 : self.i + 2]
        self.i += 2
        if nxt == "\n":
            return ""
        if quoted and self.posix and nxt not in '$`"\\':
            return "\\" + nxt
        return nxt

    def _substitution(self):
        """A `$(...)`, its command line kept for reading."""
        inner = _Scanner(self.text, self.dialect, self.i + 2)
        inner.tokens(closing=True)
        self.nested.append(self.text[self.i + 2 : inner.i - 1])
        start, self.i = self.i, inner.i
        return self.text[start : self.i]

    def _backtick(self):
        """A POSIX backtick substitution, its command line kept for reading."""
        end = self._unescaped(self.i + 1, "`", "` substitution")
        self.nested.append(self.text[self.i + 1 : end].replace("\\`", "`"))
        start, self.i = self.i, end + 1
        return self.text[start : self.i]

    def _unescaped(self, j, mark, what):
        """The index of the next `mark` not escaped by a backslash."""
        t = self.text
        while j < len(t) and t[j] != mark:
            j += 2 if t[j] == "\\" else 1
        if j >= len(t):
            raise Unreadable("an unclosed " + what)
        return j

    def _here_string(self):
        """A PowerShell here-string, `@'` or `@"` to its closing line; a `@"`
        body is read for its substitutions."""
        quote = self.text[self.i + 1]
        end = self.text.find("\n" + quote + "@", self.i + 2)
        if end < 0:
            raise Unreadable("an unclosed @{} here-string".format(quote))
        body, self.i = self.text[self.i + 2 : end], end + 3
        if quote == '"':
            self.nested.extend(_Scanner(body, self.dialect)._expansions())
        return body.strip("\r\n")
