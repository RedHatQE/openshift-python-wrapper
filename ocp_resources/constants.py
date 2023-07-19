from kubernetes.dynamic.exceptions import ForbiddenError
from openshift.dynamic.exceptions import (
    InternalServerError,
    NotFoundError,
    ServerTimeoutError,
)
from urllib3.exceptions import MaxRetryError, ProtocolError

DEFAULT_CLUSTER_RETRY_EXCEPTIONS = {
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
PROTOCOL_ERROR_EXCEPTION_DICT = {ProtocolError: []}
NOT_FOUND_ERROR_EXCEPTION_DICT = {NotFoundError: []}

TIMEOUT_10SEC = 10
TIMEOUT_1MINUTE = 60
TIMEOUT_2MINUTES = 2 * 60
TIMEOUT_4MINUTES = 4 * 60
TIMEOUT_10MINUTES = 10 * 60
