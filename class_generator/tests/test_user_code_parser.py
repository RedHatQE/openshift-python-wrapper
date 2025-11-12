"""Tests for user_code_parser module."""

import tempfile
from pathlib import Path

import pytest

from class_generator.parsers.user_code_parser import parse_user_code_from_file


class TestUserCodeParser:
    """Test cases for parse_user_code_from_file function."""

    def test_parse_file_with_user_code_and_imports(self):
        """Test parsing a file with both user code and user imports."""
        content = '''# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any
from ocp_resources.resource import NamespacedResource
import custom_module
from custom_package import CustomClass


class MyResource(NamespacedResource):
    """My resource class."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # End of generated code

    def custom_method(self):
        """User-added method."""
        return "custom"

    @property
    def custom_property(self):
        """User-added property."""
        return self.instance.get("customField")
'''

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(content)
            f.flush()

            user_code, user_imports = parse_user_code_from_file(file_path=f.name)

        Path(f.name).unlink()

        # Check user code
        assert "def custom_method(self):" in user_code
        assert "def custom_property(self):" in user_code
        assert 'return "custom"' in user_code
        assert 'return self.instance.get("customField")' in user_code

        # Check user imports (should only include non-template imports)
        assert "import custom_module" in user_imports
        assert "from custom_package import CustomClass" in user_imports
        assert "from typing import Any" not in user_imports  # Template import
        assert "from ocp_resources.resource import NamespacedResource" not in user_imports  # Template import

    def test_parse_file_without_end_marker(self):
        """Test parsing a file without the end of generated code marker."""
        content = '''# Generated file without marker

from typing import Any
from ocp_resources.resource import Resource


class MyResource(Resource):
    """My resource class."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
'''

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(content)
            f.flush()

            user_code, user_imports = parse_user_code_from_file(file_path=f.name)

        Path(f.name).unlink()

        # Should return empty strings when marker is not found
        assert user_code == ""
        assert user_imports == ""

    def test_parse_file_with_multiline_imports(self):
        """Test parsing a file with multi-line imports."""
        content = '''# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any
from ocp_resources.resource import Resource
from my_module import (
    ClassA,
    ClassB,
    ClassC
)
from another_module import (
    LongClassName1, LongClassName2,
    LongClassName3
)


class MyResource(Resource):
    """My resource class."""

    # End of generated code

    def custom_method(self):
        return True
'''

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(content)
            f.flush()

            _user_code, user_imports = parse_user_code_from_file(file_path=f.name)

        Path(f.name).unlink()

        # Check that multi-line imports are captured correctly
        assert "from my_module import (" in user_imports
        assert "ClassA," in user_imports
        assert "ClassB," in user_imports
        assert "ClassC" in user_imports
        assert "from another_module import (" in user_imports
        assert "LongClassName1, LongClassName2," in user_imports
        assert "LongClassName3" in user_imports

    def test_parse_file_with_different_template_imports(self):
        """Test parsing with different combinations of template imports."""
        content = '''# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError
from custom_validators import validate_name
import json


class MyResource(NamespacedResource):
    """My resource class."""

    # End of generated code

    def validate(self):
        validate_name(self.name)
'''

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(content)
            f.flush()

            _user_code, user_imports = parse_user_code_from_file(file_path=f.name)

        Path(f.name).unlink()

        # Check that only non-template imports are included
        assert "from custom_validators import validate_name" in user_imports
        assert "import json" in user_imports
        assert "from typing import Any" not in user_imports
        assert "from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError" not in user_imports

    def test_parse_empty_file(self):
        """Test parsing an empty file."""
        content = ""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(content)
            f.flush()

            user_code, user_imports = parse_user_code_from_file(file_path=f.name)

        Path(f.name).unlink()

        assert user_code == ""
        assert user_imports == ""

    def test_parse_file_with_only_marker(self):
        """Test parsing a file with only the marker and no user code."""
        content = '''# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any
from ocp_resources.resource import Resource


class MyResource(Resource):
    """My resource class."""

    # End of generated code
'''

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(content)
            f.flush()

            user_code, user_imports = parse_user_code_from_file(file_path=f.name)

        Path(f.name).unlink()

        # Should have empty user_imports (no custom imports) but user_code should be the content after marker
        assert user_code.strip() == ""  # Only whitespace after marker
        assert user_imports == ""

    def test_parse_file_with_syntax_error(self):
        """Test parsing a file with syntax errors in imports section."""
        content = '''# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any
from ocp_resources.resource import Resource
from # Invalid syntax


class MyResource(Resource):
    """My resource class."""

    # End of generated code

    def custom_method(self):
        return True
'''

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(content)
            f.flush()

            # Should raise SyntaxError when parsing
            with pytest.raises(SyntaxError):
                parse_user_code_from_file(file_path=f.name)

        Path(f.name).unlink()
