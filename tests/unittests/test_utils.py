import re

import pytest

from ocp_resources.utils import TimeoutExpiredError, TimeoutSampler


class TestTimeoutSampler:
    @staticmethod
    def _raise_exception(runtime_exception):
        if runtime_exception:
            raise runtime_exception

    def _trigger_func_exception_during_iter(self, exceptions_dict, runtime_exception):
        for _ in TimeoutSampler(
            wait_timeout=1,
            sleep=1,
            func=self._raise_exception,
            exceptions_dict=exceptions_dict,
            print_log=False,
            runtime_exception=runtime_exception,
        ):
            continue

    @pytest.mark.parametrize(
        "test_params, expected",
        [
            pytest.param(
                {
                    "init_exceptions_dict": {
                        KeyError: [],
                    },
                    "runtime_exception": ValueError(),
                },
                {
                    "raises": ValueError,
                },
                id="init_keyerror_raise_valueerror_with_no_msg",
            ),
            pytest.param(
                {
                    "init_exceptions_dict": {
                        ValueError: ["allowed exception text"],
                    },
                    "runtime_exception": ValueError("test"),
                },
                {
                    "raises": ValueError,
                },
                id="init_valueerror_with_msg_raise_valueerror_with_invalid_msg",
            ),
            pytest.param(
                {
                    "init_exceptions_dict": {
                        KeyError: ["allowed exception text"],
                        IndexError: ["allowed exception text"],
                        ValueError: ["allowed exception text"],
                    },
                    "runtime_exception": IndexError("test"),
                },
                {
                    "raises": IndexError,
                },
                id="init_multi_exceptions_raise_allowed_with_invalid_msg",
            ),
        ],
    )
    def test_timeout_sampler_raises(self, test_params, expected):
        with pytest.raises(expected["raises"]):
            self._trigger_func_exception_during_iter(
                exceptions_dict=test_params.get("init_exceptions_dict"),
                runtime_exception=test_params.get("runtime_exception"),
            )

    @pytest.mark.parametrize(
        "test_params, expected",
        [
            pytest.param(
                {},
                {
                    "exception_log_regex": "^.*\nLast exception: N/A: None$",
                },
                id="noargs_timeout_only",
            ),
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
                    "init_exceptions_dict": {
                        ValueError: ["test"],
                    },
                    "runtime_exception": ValueError("test"),
                },
                {
                    "exception_log_regex": "^.*\nLast exception: ValueError: test$",
                },
                id="init_valueerror_with_msg_raise_valueerror_with_allowed_msg",
            ),
            pytest.param(
                {
                    "init_exceptions_dict": {
                        KeyError: ["allowed exception text"],
                        IndexError: ["allowed exception text"],
                        ValueError: ["allowed exception text"],
                    },
                    "runtime_exception": IndexError("my allowed exception text"),
                },
                {
                    "exception_log_regex": "^.*\nLast exception: IndexError: my allowed exception text$",
                },
                id="init_multi_exceptions_raise_allowed_with_allowed_msg",
            ),
        ],
    )
    def test_timeout_sampler_raises_timeout(self, test_params, expected):
        exception_match = None
        exception_log = None
        try:
            self._trigger_func_exception_during_iter(
                exceptions_dict=test_params.get("init_exceptions_dict"),
                runtime_exception=test_params.get("runtime_exception"),
            )
        except TimeoutExpiredError as exp:
            exception_log = str(exp)
            exception_match = re.compile(
                pattern=expected["exception_log_regex"], flags=re.DOTALL
            ).match(string=exception_log)

        assert (
            exception_match
        ), f"Expected Regex: {expected['exception_log_regex']!r} Exception Log: {exception_log!r}"
