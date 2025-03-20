import json
import shlex
import subprocess
import sys
from collections import OrderedDict


def main(from_tag: str, to_tag: str) -> str:
    title_to_type_map: dict[str, str] = {
        "ci": "CI:",
        "docs": "Docs:",
        "feat": "New Feature:",
        "fix": "Bugfix:",
        "refactor": "Refactor:",
        "test": "Tests:",
        "release": "New Release:",
        "CherryPicked": "Cherry Pick:",
        "merge": "Merge:",
    }
    changelog_dict: OrderedDict[str, list[dict[str, str]]] = OrderedDict([
        ("New Feature:", []),
        ("Bugfix:", []),
        ("CI:", []),
        ("New Release:", []),
        ("Docs:", []),
        ("Refactor:", []),
        ("Tests:", []),
        ("Other Changes:", []),
        ("Cherry Pick:", []),
        ("Merge:", []),
    ])

    changelog: str = ""
    _format = '{"title": "%s", "commit": "%h", "author": "%an", "date": "%as"}'
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

        changelog += f"{section}\n"
        for _change in _changelogs:
            _title = _change["title"].split(":", 1)[1] if section != "Other Changes:" else _change["title"]
            changelog += f"    {_title} ({_change['commit']}) by {_change['author']} on {_change['date']}\n"

        changelog += "\n"

    return changelog


if __name__ == "__main__":
    from_tag, to_tag = sys.argv[1], sys.argv[2]
    generated_changelog = main(from_tag=from_tag, to_tag=to_tag)
    print(generated_changelog)
