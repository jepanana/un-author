import argparse
import re

AI = r"\b(cursor|claude|anthropic|copilot|openai|chatgpt|codex|gemini|aider|devin|windsurf|codeium|jules)\b"
CO_AUTHOR = re.compile(r"^\s*co-authored-by:(.*)$", re.IGNORECASE)
SIGNATURE = re.compile(r"generated with .*claude code", re.IGNORECASE)


def strip(message, remove_all=False, keep=(), remove=()):
    removable = [re.compile(p, re.IGNORECASE) for p in (AI, *remove)]
    kept = [re.compile(p, re.IGNORECASE) for p in keep]
    lines = []
    for line in message.splitlines():
        author = CO_AUTHOR.match(line)
        if author:
            name = author.group(1)
            if not any(p.search(name) for p in kept) and (remove_all or any(p.search(name) for p in removable)):
                continue
        elif SIGNATURE.search(line):
            continue
        lines.append(line)
    return "\n".join(lines).rstrip() + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Strip co-author trailers from a commit message file.")
    parser.add_argument("--all", action="store_true", help="remove every Co-authored-by trailer, not only AI ones")
    parser.add_argument("--keep", action="append", default=[], metavar="REGEX", help="never remove co-authors matching REGEX")
    parser.add_argument("--remove", action="append", default=[], metavar="REGEX", help="also remove co-authors matching REGEX")
    parser.add_argument("file", help="commit message file")
    args = parser.parse_args(argv)

    with open(args.file, encoding="utf-8") as f:
        original = f.read()
    cleaned = strip(original, args.all, args.keep, args.remove)
    if cleaned != original:
        with open(args.file, "w", encoding="utf-8") as f:
            f.write(cleaned)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
