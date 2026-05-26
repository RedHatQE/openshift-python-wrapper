"""Exception classes for fake Kubernetes client"""

# Import exceptions from kubernetes.dynamic - use real ones for compatibility
try:
    from kubernetes.dynamic.exceptions import (
        ApiException,
        ConflictError,
        ForbiddenError,
        MethodNotAllowedError,
        NotFoundError,
        ResourceNotFoundError,
        ServerTimeoutError,
    )
except ImportError:
    # Fallback implementations if kubernetes module is not available
    class FakeClientApiException(Exception):
        def __init__(self, status: int | None = None, reason: str | None = None, body: str | None = None) -> None:
            super().__init__(f"API Exception: {status} - {reason}")
            self.status = status
            self.reason = reason
            self.body = body

    class FakeClientNotFoundError(FakeClientApiException):
        def __init__(self, reason: str = "Not Found") -> None:
            super().__init__(status=404, reason=reason)

    class FakeClientConflictError(FakeClientApiException):
        def __init__(self, reason: str = "Conflict") -> None:
            super().__init__(status=409, reason=reason)

    class FakeClientForbiddenError(FakeClientApiException):
        def __init__(self, reason: str = "Forbidden") -> None:
            super().__init__(status=403, reason=reason)

    class FakeClientMethodNotAllowedError(FakeClientApiException):
        def __init__(self, reason: str = "Method Not Allowed") -> None:
            super().__init__(status=405, reason=reason)

    class FakeClientResourceNotFoundError(FakeClientApiException):
        def __init__(self, reason: str = "Resource Not Found") -> None:
            super().__init__(status=404, reason=reason)

    class FakeClientServerTimeoutError(FakeClientApiException):
        def __init__(self, reason: str = "Server Timeout") -> None:
            super().__init__(status=504, reason=reason)

    # Create aliases with expected names
    ApiException = FakeClientApiException
    NotFoundError = FakeClientNotFoundError
    ConflictError = FakeClientConflictError
    ForbiddenError = FakeClientForbiddenError
    MethodNotAllowedError = FakeClientMethodNotAllowedError
    ResourceNotFoundError = FakeClientResourceNotFoundError
    ServerTimeoutError = FakeClientServerTimeoutError
