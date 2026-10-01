# un-author

A [pre-commit](https://pre-commit.com) hook that strips AI `Co-authored-by` trailers
and "Generated with Claude Code" lines from commit messages.

By default it removes co-authors that match a known AI tool (Cursor, Claude, Anthropic,
Copilot, OpenAI, ChatGPT, Codex, Gemini, Aider, Devin, Windsurf, Codeium, Jules) and keeps
every human co-author.

## Usage

```yaml
default_install_hook_types: [pre-commit, commit-msg]

repos:
  - repo: https://github.com/jepanana/un-author
    rev: v0.1.0
    hooks:
      - id: un-author
```

```console
pre-commit install --hook-type commit-msg
```

## Options

Pass options with `args`:

| Option | Effect |
| --- | --- |
| `--all` | Remove every `Co-authored-by` trailer |
| `--keep REGEX` | Never remove co-authors matching `REGEX` (repeatable) |
| `--remove REGEX` | Also remove co-authors matching `REGEX` (repeatable) |

Patterns are case-insensitive and match the trailer value (name and email).

```yaml
      - id: un-author
        args: [--all, --keep, "@example\\.com"]
```

Run it directly with `un-author [options] <commit-message-file>`.

## Credits

Based on [mherod's global prepare-commit-msg hook](https://gist.github.com/mherod/e9edfb3102ffe19bb973643f077eaa26).
