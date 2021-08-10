import re
import warnings

import pytest

from ocp_resources.utils import (
    InvalidArgumentsError,
    TimeoutExpiredError,
    TimeoutSampler,
)


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

    @pytest.mark.parametrize(
        "test_params, expected",
        [
            pytest.param(
                {},
                {
                    "exceptions": (Exception,),
                    "exceptions_dict": {Exception: []},
                },
                id="noargs",
            ),
            pytest.param(
                {
                    "exceptions": ValueError,
                },
                {
                    "exceptions": (ValueError,),
                    "exceptions_dict": {ValueError: []},
                    "warning": {
                        "class": DeprecationWarning,
                        "text": "TimeoutSampler() exception and exception_msg are now deprecated.",
                    },
                },
                id="init_valueerror_expect_deprecation_warning",
            ),
            pytest.param(
                {
                    "exceptions": ValueError,
                    "exceptions_msg": "test message",
                },
                {
                    "exceptions": (ValueError,),
                    "exceptions_dict": {ValueError: ["test message"]},
                    "warning": {
                        "class": DeprecationWarning,
                        "text": "TimeoutSampler() exception and exception_msg are now deprecated.",
                    },
                },
                id="init_valueerror_with_msg_expect_deprecation_warning",
            ),
            pytest.param(
                {
                    "exceptions": (Exception, ValueError),
                },
                {
                    "exceptions": (Exception, ValueError),
                    "exceptions_dict": {
                        Exception: [],
                        ValueError: [],
                    },
                    "warning": {
                        "class": DeprecationWarning,
                        "text": "TimeoutSampler() exception and exception_msg are now deprecated.",
                    },
                },
                id="init_multi_exception_with_no_msg_expect_deprecation_warning",
            ),
            pytest.param(
                {
                    "exceptions_dict": {
                        Exception: ["exception msg"],
                        ValueError: ["another exception msg"],
                    },
                },
                {
                    "exceptions": (Exception, ValueError),
                    "exceptions_dict": {
                        Exception: ["exception msg"],
                        ValueError: ["another exception msg"],
                    },
                },
                id="init_dict",
            ),
            pytest.param(
                {
                    "exceptions_dict": {
                        Exception: [],
                        ValueError: [],
                    },
                },
                {
                    "exceptions": (Exception, ValueError),
                    "exceptions_dict": {
                        Exception: [],
                        ValueError: [],
                    },
                },
                id="init_dict_no_msgs",
            ),
            pytest.param(
                {
                    "exceptions": TypeError,
                    "exceptions_dict": {
                        Exception: ["exception msg"],
                        KeyError: ["another exception msg"],
                    },
                },
                {
                    "raises": InvalidArgumentsError,
                },
                id="init_deprecated_exceptions_and_new_dict_expect_raise_invalid_arguments",
            ),
            pytest.param(
                {
                    "exceptions_msg": "test exception message",
                    "exceptions_dict": {
                        Exception: ["exception msg"],
                        KeyError: ["another exception msg"],
                    },
                },
                {
                    "raises": InvalidArgumentsError,
                },
                id="init_deprecated_msg_and_new_dict_expect_raise_invalid_arguments",
            ),
        ],
    )
    def test_timeout_sampler_pre_process_exceptions(self, test_params, expected):
        # TODO: Remove this test when _pre_process_exceptions() is removed from TimeoutSampler
        def _timeout_sampler():
            return TimeoutSampler(
                wait_timeout=1,
                sleep=1,
                func=lambda: True,
                exceptions=test_params.get("exceptions"),
                exceptions_msg=test_params.get("exceptions_msg"),
                exceptions_dict=test_params.get("exceptions_dict"),
                print_log=False,
            )

        if expected.get("raises"):
            with pytest.raises(expected["raises"]):
                _timeout_sampler()
        else:
            with warnings.catch_warnings(record=True) as caught_warnings:
                # Note: catch_warnings is not thread safe
                timeout_sampler = _timeout_sampler()
                if "warning" in expected:
                    assert len(caught_warnings) == 1
                    assert issubclass(
                        caught_warnings[-1].category, expected["warning"]["class"]
                    )
                    assert expected["warning"]["text"] in str(
                        caught_warnings[-1].message
                    )
                else:
                    assert len(caught_warnings) == 0

            assert expected["exceptions"] == timeout_sampler._exceptions
            assert expected["exceptions_dict"] == timeout_sampler.exceptions_dict
