from openshift.dynamic.exceptions import NotFoundError
from urllib3.exceptions import ProtocolError


PROTOCOL_ERROR_EXCEPTION_DICT = {ProtocolError: []}
NOT_FOUND_ERROR_EXCEPTION_DICT = {NotFoundError: []}
TIMEOUT_4MINUTES = 240
