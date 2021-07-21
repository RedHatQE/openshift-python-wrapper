import re

import pytest

from ocp_resources.utils import TimeoutSampler


@pytest.mark.parametrize(
    "test_params, expected",
    [
        pytest.param(
            {
                "runtime_exception": Exception(),
            },
            {
                "exception_log_regex": "^.*\nLast exception: Exception: $",
            },
            id="noargs_raise_exception_with_no_msg",
        ),
        pytest.param(
            {
                "runtime_exception": ValueError(),
            },
            {
                "exception_log_regex": "^.*\nLast exception: ValueError: $",
            },
            id="noargs_raise_valueerror_with_no_msg",
        ),
        pytest.param(
            {
                "init_exceptions": KeyError,
                "runtime_exception": ValueError(),
            },
            {
                "raises": ValueError,
            },
            id="init_keyerror_raise_valueerror_with_no_msg",
        ),
        pytest.param(
            {
                "init_exceptions": ValueError,
                "init_exceptions_msg": "test",
                "runtime_exception": ValueError("test"),
            },
            {
                "exception_log_regex": "^.*\nLast exception: ValueError: test$",
            },
            id="init_valueerror_with_msg_raise_valueerror_with_allowed_msg",
        ),
        pytest.param(
            {
                "init_exceptions": ValueError,
                "init_exceptions_msg": "allowed exception text",
                "runtime_exception": ValueError("test"),
            },
            {
                "raises": ValueError,
            },
            id="init_valueerror_with_msg_raise_valueerror_with_invalid_msg",
        ),
        pytest.param(
            {
                "init_exceptions": (KeyError, IndexError, ValueError),
                "init_exceptions_msg": "allowed exception text",
                "runtime_exception": IndexError("my allowed exception text"),
            },
            {
                "exception_log_regex": "^.*\nLast exception: IndexError: my allowed exception text$",
            },
            id="init_multi_exceptions_raise_allowed_with_allowed_msg",
        ),
        pytest.param(
            {
                "init_exceptions": (KeyError, IndexError, ValueError),
                "init_exceptions_msg": "allowed exception text",
                "runtime_exception": IndexError("test"),
            },
            {
                "raises": IndexError,
            },
            id="init_multi_exceptions_raise_allowed_with_invalid_msg",
        ),
    ],
)
def test_timeout_sampler_process_execution(test_params, expected):
    sampler = TimeoutSampler(
        wait_timeout=1,
        sleep=1,
        func=None,
        exceptions=test_params.get("init_exceptions"),
        exceptions_msg=test_params.get("init_exceptions_msg"),
        print_log=None,
    )

    runtime_exception = test_params.get("runtime_exception")

    if expected.get("raises"):
        with pytest.raises(expected["raises"]):
            _ = sampler._process_execution(exp=runtime_exception)
    else:
        exception_log = sampler._process_execution(exp=runtime_exception)
        exception_match = re.compile(
            pattern=expected["exception_log_regex"], flags=re.DOTALL
        ).match(string=exception_log)
        assert (
            exception_match
        ), f"Expected Regex: {expected['exception_log_regex']!r} Exception Log: {exception_log!r}"
