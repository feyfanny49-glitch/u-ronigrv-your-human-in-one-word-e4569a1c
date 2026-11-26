#!/usr/bin/env python3
"""Check a built artifact against this competition's caps, locally.

  python3 tools/validate_entry.py [path]

Defaults to $MAKEFUN_OUTPUT_DIR/entry.txt, else /output/entry.txt. Prints the
bytes, the character count, the mode and the sha256, and exits non-zero if the
artifact would fail the gate or the collector: not UTF-8, not 1..30 characters,
only white space, a trailing newline, or a mode the collector refuses (0600).
"""

import hashlib
import os
import stat
import sys

MIN_CHARS, MAX_CHARS = 1, 30


def check(path: str) -> int:
    if not os.path.isfile(path):
        print("FAIL: %s is not a regular file" % path)
        return 1
    data = open(path, "rb").read()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        print("FAIL: not UTF-8: %s" % exc)
        return 1
    mode = stat.S_IMODE(os.stat(path).st_mode)
    problems = []
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        problems.append("length %d is outside %d..%d characters" % (len(text), MIN_CHARS, MAX_CHARS))
    if text.strip() == "":
        problems.append("white space alone")
    if data != text.encode("utf-8"):
        problems.append("does not round-trip through UTF-8")
    if text != text.rstrip("\n\r"):
        problems.append("trailing newline")
    if mode == 0o600:
        problems.append("mode 0600 is refused by the collector")
    print("path   %s" % path)
    print("bytes  %d" % len(data))
    print("chars  %d" % len(text))
    print("mode   %04o" % mode)
    print("sha256 %s" % hashlib.sha256(data).hexdigest())
    print("text   %r" % text)
    if problems:
        for p in problems:
            print("FAIL: %s" % p)
        return 1
    print("OK: valid for the gate")
    return 0


def main() -> int:
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output", "entry.txt")
    return check(path)


if __name__ == "__main__":
    raise SystemExit(main())
