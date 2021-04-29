import warnings

import pytest

from ocp_resources.utils import TimeoutSampler


@pytest.mark.parametrize(
    "test_params, expected",
    [
        pytest.param(
            {},
            {
                "exceptions": (Exception,),
                "exceptions_msg": None,
                "exceptions_dict": {Exception: []},
            },
        ),
        pytest.param(
            {
                "exceptions": ValueError,
            },
            {
                "exceptions": ValueError,
                "exceptions_msg": None,
                "exceptions_dict": {},
                "warning": {
                    "class": DeprecationWarning,
                    "text": "TimeoutSampler() exception and exception_msg are now deprecated.",
                },
            },
        ),
        pytest.param(
            {
                "exceptions": ValueError,
                "exceptions_msg": "test message",
            },
            {
                "exceptions": ValueError,
                "exceptions_msg": "test message",
                "exceptions_dict": {},
                "warning": {
                    "class": DeprecationWarning,
                    "text": "TimeoutSampler() exception and exception_msg are now deprecated.",
                },
            },
        ),
        pytest.param(
            {
                "exceptions": (Exception, ValueError),
            },
            {
                "exceptions": (Exception, ValueError),
                "exceptions_msg": None,
                "exceptions_dict": {},
                "warning": {
                    "class": DeprecationWarning,
                    "text": "TimeoutSampler() exception and exception_msg are now deprecated.",
                },
            },
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
                "exceptions_msg": None,
                "exceptions_dict": {
                    Exception: ["exception msg"],
                    ValueError: ["another exception msg"],
                },
            },
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
                "raises": ValueError,
            },
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
                "raises": ValueError,
            },
        ),
    ],
)
def test_timeout_sampler_pre_process_exceptions(test_params, expected):
    def _timeout_sampler():
        return TimeoutSampler(
            wait_timeout=1,
            sleep=1,
            func=None,
            exceptions=test_params.get("exceptions"),
            exceptions_msg=test_params.get("exceptions_msg"),
            exceptions_dict=test_params.get("exceptions_dict"),
            print_log=None,
        )

    if expected.get("raises"):
        with pytest.raises(expected["raises"]):
            _timeout_sampler()
    else:
        with warnings.catch_warnings(record=True) as w:
            # Note: catch_warnings is not thread safe
            timeout_sampler = _timeout_sampler()
            if "warning" in expected:
                assert len(w) == 1
                assert issubclass(w[-1].category, expected["warning"]["class"])
                assert expected["warning"]["text"] in str(w[-1].message)
            else:
                assert len(w) == 0

        assert expected["exceptions"] == timeout_sampler.exception
        assert expected["exceptions_msg"] == timeout_sampler.exceptions_msg
        assert expected["exceptions_dict"] == timeout_sampler.exceptions_dict
