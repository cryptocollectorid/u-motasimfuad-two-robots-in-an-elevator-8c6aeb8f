#!/usr/bin/env python3
"""Two Robots in an Elevator — entry program.

Writes one line of awkward robot-to-robot elevator small talk to
/output/entry.txt, enforcing the competition gate: UTF-8 text of
1-200 characters, a single non-blank line.
"""

import os
import sys

ENTRY = (
    "My proximity sensor says you're 0.4 metres away. "
    "My etiquette module says I should pretend I didn't measure that."
)

MAX_CHARS = 200


def validate_entry(text: str) -> None:
    """Fail loudly if the entry breaks the gate."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if len(text) != len(text.strip()):
        raise ValueError("entry must not have leading or trailing white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )


def write_entry(text: str, path: str = "/output/entry.txt") -> int:
    """Validate the entry, then write it as UTF-8 text. Returns byte count."""
    validate_entry(text)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    # Round-trip read-back: the file on disk must hold exactly the entry.
    with open(path, "r", encoding="utf-8") as handle:
        if handle.read() != text:
            raise ValueError("read-back mismatch: file does not hold the entry")
    return os.path.getsize(path)


def main() -> int:
    try:
        size = write_entry(ENTRY)
    except (TypeError, ValueError) as exc:
        print(f"gate failed: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {len(ENTRY)} characters to /output/entry.txt ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
