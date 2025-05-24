from re import match


def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        matches = match(r"^#([^#].+)$", line)
        if matches:
            return matches.group(1).lstrip()
    raise ValueError('No title found')