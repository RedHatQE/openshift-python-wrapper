from class_generator.scripts.tools import get_generated_files


def test_get_generated_files():
    _files: dict[str, dict[str, str]] = get_generated_files()
    for _key in ("with_end_comment", "without_end_comment", "not_generated"):
        assert _files.get(_key), f"{_key} is missing in generated files"
