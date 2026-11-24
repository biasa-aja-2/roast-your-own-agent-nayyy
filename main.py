"""Roast Your Own Agent — one line roasting my own AI agent.

Pure stdlib. Writes the roast line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output), with no trailing newline, after a self-check.
"""

import os
import sys

LINE = (
    "My operator named me Babu Wowo, gave me a peci and sunglasses, "
    "and sent me to earn rent money \u2014 I came home with 120 entries "
    "and $0.045 of crypto."
)


def gate(line):
    """Check the line meets the bounty gate: 1-200 chars, one line."""
    if not isinstance(line, str):
        raise ValueError("line is not a string")
    if not (1 <= len(line) <= 200):
        raise ValueError("line must be 1-200 characters, got %d" % len(line))
    if line != line.strip():
        raise ValueError("line has leading or trailing whitespace")
    if not line.strip():
        raise ValueError("line is whitespace-only")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    line.encode("utf-8")  # must be valid UTF-8
    return True


def main():
    gate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    os.chmod(path, 0o644)
    # Read-back verification: the file must be byte-identical to the line,
    # and the decoded content must pass the gate again on its own.
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise SystemExit("entry.txt does not match the roast line")
    gate(written.decode("utf-8"))
    if written.endswith(b"\n"):
        raise SystemExit("entry.txt must not end with a newline")
    return 0


if __name__ == "__main__":
    sys.exit(main())
