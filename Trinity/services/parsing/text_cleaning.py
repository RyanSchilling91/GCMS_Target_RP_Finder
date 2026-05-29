import re

_ESCAPE_RE = re.compile(r"\x1b[@-_][0-?]*[ -/]*[@-~]")


def strip_escape_sequences(text: str) -> str:
    return _ESCAPE_RE.sub("", text)
