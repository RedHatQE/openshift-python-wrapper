import json
import shlex
import subprocess
import sys
from collections import OrderedDict


def main(from_tag: str, to_tag: str) -> str:
    """
    Generate a changelog between two tags, output as markdown
    """
    title_to_type_map: dict[str, str] = {
        "ci": "CI:",
        "docs": "Docs:",
        "feat": "New Feature:",
        "fix": "Bugfixs:",
        "refactor": "Refactor:",
        "test": "Tests:",
        "release": "New Release:",
        "CherryPicked": "Cherry Pick:",
        "merge": "Merge:",
    }
    changelog_dict: OrderedDict[str, list[dict[str, str]]] = OrderedDict([
        ("New Feature:", []),
        ("Bugfixs:", []),
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
    _format: str = '{"title": "%s", "commit": "%h", "author": "%an", "date": "%as"}'
    res = subprocess.run(
        shlex.split(f"git log --pretty=format:'{_format}' {from_tag}...{to_tag}"), stdout=subprocess.PIPE, text=True
    ).stdout

    for line in res.splitlines():
        _json_line = json.loads(line)

        try:
            _map = title_to_type_map[_json_line["title"].split(":", 1)[0]]
            changelog_dict[_map].append(_json_line)
        except Exception:
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
    print(main(from_tag=sys.argv[1], to_tag=sys.argv[2]))
