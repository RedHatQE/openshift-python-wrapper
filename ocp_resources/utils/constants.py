from kubernetes.dynamic.exceptions import (
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    ServerTimeoutError,
)
from urllib3.exceptions import MaxRetryError, ProtocolError

DEFAULT_CLUSTER_RETRY_EXCEPTIONS: dict[type[Exception], list[str]] = {
    MaxRetryError: [],
    ConnectionAbortedError: [],
    ConnectionResetError: [],
    InternalServerError: [
        "etcdserver: leader changed",
        "etcdserver: request timed out",
        "Internal error occurred: failed calling webhook",
        "rpc error:",
    ],
    ServerTimeoutError: [],
    ForbiddenError: ["context deadline exceeded"],
}
PROTOCOL_ERROR_EXCEPTION_DICT: dict[type[Exception], list[str]] = {ProtocolError: []}
NOT_FOUND_ERROR_EXCEPTION_DICT: dict[type[Exception], list[str]] = {NotFoundError: []}

TIMEOUT_1SEC: int = 1
TIMEOUT_5SEC: int = 5
TIMEOUT_10SEC: int = 10
TIMEOUT_30SEC: int = 30
TIMEOUT_1MINUTE: int = 60
TIMEOUT_2MINUTES: int = 2 * 60
TIMEOUT_4MINUTES: int = 4 * 60
TIMEOUT_10MINUTES: int = 10 * 60
