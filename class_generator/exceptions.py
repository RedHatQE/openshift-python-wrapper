"""Custom exceptions for class generator."""


class ResourceNotFoundError(Exception):
    """Raised when a resource kind is not found."""

    def __init__(self, kind: str, message: str | None = None) -> None:
        self.kind = kind
        if message is None:
            message = f"Resource kind '{kind}' not found"
        super().__init__(message)
