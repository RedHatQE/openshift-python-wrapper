import json
import re
import shlex
import subprocess
import sys
from collections import OrderedDict


def remove_at_index(chr_index: int, string_: str) -> str:
    """
    Remove a character at the specified index from a string.

    Args:
        chr_index: The index of the character to remove
        string_: The original string

    Returns:
        The string with the character at chr_index removed
    """
    return string_[:chr_index] + string_[chr_index + 1 :]


def format_line_for_json(line: str) -> str:
    # In case line is not formatted for json for example:
    # '{"title": "Revert "feat: Use git cliff to generate the change log. (#2322)" (#2324)", "commit": "137331fd", "author": "Meni Yakove", "date": "2025-02-16"}'
    # title have `"` inside the external `"` `"Revert "feat: Use git cliff to generate the change log. (#2322)" (#2324)"`
    line_split = line.split(",")
    title_key = line_split[0].split(":")[0]
    title_split = line_split.pop(0).split(":", 1)[-1]

    if title_split.count('"') > 2:
        # Find all `"` indexes
        quote_match = [match.start() for match in re.finditer('"', title_split)]

        # Remove first and last matched `"`
        quote_to_remove = quote_match[1:-1]

        for idx, _index in enumerate(quote_to_remove):
            # send _index -1 if not the first iter since the title_split changed (removed one character on first iter)
            _index_to_send = _index if idx == 0 else _index - 1
            title_split = remove_at_index(chr_index=_index_to_send, string_=title_split)

        line_split.insert(0, f"{title_key}: {title_split.strip()}")
        line = ",".join(line_split)

    return line


def main(from_tag: str, to_tag: str) -> str:
    title_to_type_map: dict[str, str] = {
        "ci": "CI:",
        "docs": "Docs:",
        "feat": "New Feature:",
        "fix": "Bugfixes:",
        "refactor": "Refactor:",
        "test": "Tests:",
        "release": "New Release:",
        "cherrypicked": "Cherry Pick:",
        "merge": "Merge:",
    }
    changelog_dict: OrderedDict[str, list[dict[str, str]]] = OrderedDict([
        ("New Feature:", []),
        ("Bugfixes:", []),
        ("CI:", []),
        ("New Release:", []),
        ("Docs:", []),
        ("Refactor:", []),
        ("Tests:", []),
        ("Other Changes:", []),
        ("Cherry Pick:", []),
        ("Merge:", []),
    ])

    changelog: str = "## What's Changed\n"
    _format: str = """{"title": "%s", "commit": "%h", "author": "%an", "date": "%as"}"""

    try:
        proc = subprocess.run(
            shlex.split(f"git log --pretty=format:'{_format}' {from_tag}...{to_tag}"),
            stdout=subprocess.PIPE,
            text=True,
        )
        if proc.returncode != 0:
            print("Error executing git log command")
            sys.exit(1)

        res = proc.stdout
    except Exception as ex:
        print(f"Error executing git log command: {ex}")
        sys.exit(1)

    for line in res.splitlines():
        line = format_line_for_json(line=line)

        try:
            _json_line = json.loads(line)
        except json.decoder.JSONDecodeError:
            print(f"Error parsing json line: {line}")
            sys.exit(1)

        try:
            prefix = _json_line["title"].split(":", 1)[0]
            if prefix.lower() in title_to_type_map:
                _map = title_to_type_map[prefix]
                changelog_dict[_map].append(_json_line)

            else:
                changelog_dict["Other Changes:"].append(_json_line)
        except IndexError:
            changelog_dict["Other Changes:"].append(_json_line)

    for section, _changelogs in changelog_dict.items():
        if not _changelogs:
            continue

        changelog += f"#### {section}\n"
        for _change in _changelogs:
            _title = _change["title"].split(":", 1)[1] if section != "Other Changes:" else _change["title"]
            changelog += f"-{_title} ({_change['commit']}) by {_change['author']} on {_change['date']}\n"

        changelog += "\n"

    changelog += (
        f"**Full Changelog**: https://github.com/RedHatQE/openshift-python-wrapper/compare/{from_tag}...{to_tag}"
    )

    return changelog


if __name__ == "__main__":
    """
    Generate a changelog between two Git tags, formatted as markdown.

    This script parses Git commit logs between two specified tags and categorizes them
    by commit type (feat, fix, ci, etc.). It formats the output as a markdown document
    with sections for different types of changes, intended for use with release-it.

    Each commit is expected to follow the conventional commit format:
    <type>: <description>

    where <type> is one of: feat, fix, docs, style, refactor, test, chore, etc.
    Commits that don't follow this format are categorized under "Other Changes".

    Generate a changelog between two tags, output as markdown

    Usage: python generate-changelog.py <from_tag> <to_tag>
    """
    if len(sys.argv) != 3:
        print("Usage: python generate-changelog.py <from_tag> <to_tag>")
        sys.exit(1)

    print(main(from_tag=sys.argv[1], to_tag=sys.argv[2]))
