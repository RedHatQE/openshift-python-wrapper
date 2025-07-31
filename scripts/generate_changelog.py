import json
import shlex
import subprocess
import sys
from collections import OrderedDict


def json_line(line: str) -> dict:
    """
    Format str line to str that can be parsed with json.

    In case line is not formatted for json for example:
    '{"title": "Revert "feat: Use git cliff to generate the change log. (#2322)" (#2324)", "commit": "137331fd", "author": "Meni Yakove", "date": "2025-02-16"}'
    title have `"` inside the external `"` `"Revert "feat: Use git cliff to generate the change log. (#2322)" (#2324)"`
    """
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        # split line like by `,`
        # '{"title": "Revert "feat: Use git cliff to generate the change log. (#2322)" (#2324)", "commit": "137331fd", "author": "Meni Yakove", "date": "2025-02-16"}'
        line_split = line.split(",")

        # Pop and save `title key` and `title body` from '{"title": "Revert "feat: Use git cliff to generate the change log. (#2322)" (#2324)"'
        title_key, title_body = line_split.pop(0).split(":", 1)

        if title_body.count('"') > 2:
            # reconstruct the `title_body` without the extra `"`
            # "Revert "feat: Use git cliff to generate the change log. (#2322)" (#2324)"'
            # replace all `"` with empty char and add `"` char to the beginning and the end of the string
            stripted_body = title_body.replace('"', "")
            title_body = f'"{stripted_body}"'

            line_split.append(f"{title_key}: {title_body.strip()}")
            line = ",".join(line_split)

        return json.loads(line)


def execute_git_log(from_tag: str, to_tag: str) -> str:
    """Executes git log and returns the output, or raises an exception on error."""
    _format: str = '{"title": "%s", "commit": "%h", "author": "%an", "date": "%as"}'

    try:
        command = f"git log --pretty=format:'{_format}' {from_tag}...{to_tag}"
        proc = subprocess.run(
            shlex.split(command), stdout=subprocess.PIPE, text=True, check=True
        )  # Use check=True to raise an exception for non-zero return codes
        return proc.stdout
    except subprocess.CalledProcessError as ex:
        print(f"Error executing git log: {ex}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: git not found.  Please ensure git is installed and in your PATH.")
        sys.exit(1)


def parse_commit_line(line: str) -> dict:
    """Parses a single JSON formatted git log line."""
    try:
        return json_line(line=line)
    except json.decoder.JSONDecodeError as ex:
        print(f"Error parsing JSON: {line} - {ex}")
        return {}


def categorize_commit(commit: dict, title_to_type_map: dict, default_category: str = "Other Changes:") -> str:
    """Categorizes a commit based on its title prefix."""
    if not commit or "title" not in commit:
        return default_category
    title = commit["title"]
    try:
        prefix = title.split(":", 1)[0].lower()  # Extract the prefix before the first colon
        return title_to_type_map.get(prefix, default_category)
    except IndexError:
        return default_category


def format_changelog_entry(change: dict, section: str) -> str:
    """Formats a single changelog entry."""
    title = change["title"].split(":", 1)[1] if section != "Other Changes:" else change["title"]
    return f"- {title} ({change['commit']}) by {change['author']} on {change['date']}\n"


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

    res = execute_git_log(from_tag=from_tag, to_tag=to_tag)

    for line in res.splitlines():
        commit = parse_commit_line(line=line)
        if commit:
            category = categorize_commit(commit=commit, title_to_type_map=title_to_type_map)
            changelog_dict[category].append(commit)

    for section, changes in changelog_dict.items():
        if not changes:
            continue

        changelog += f"#### {section}\n"
        for change in changes:
            changelog += format_changelog_entry(change, section)
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
