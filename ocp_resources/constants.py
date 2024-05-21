from __future__ import annotations

from typing import Dict, List
from kubernetes.dynamic.exceptions import (
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    ServerTimeoutError,
)
from urllib3.exceptions import MaxRetryError, ProtocolError

DEFAULT_CLUSTER_RETRY_EXCEPTIONS: Dict[type[Exception], List[str]] = {
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
PROTOCOL_ERROR_EXCEPTION_DICT: Dict[type[Exception], List[str]] = {ProtocolError: []}
NOT_FOUND_ERROR_EXCEPTION_DICT: Dict[type[Exception], List[str]] = {NotFoundError: []}

TIMEOUT_10SEC: int = 10
TIMEOUT_1MINUTE: int = 60
TIMEOUT_2MINUTES: int = 2 * 60
TIMEOUT_4MINUTES: int = 4 * 60
TIMEOUT_10MINUTES: int = 10 * 60
