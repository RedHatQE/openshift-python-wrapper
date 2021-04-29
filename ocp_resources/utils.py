import logging
import subprocess
import time
from warnings import warn


LOGGER = logging.getLogger(__name__)


class TimeoutExpiredError(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f"Timed Out: {self.value}"


class TimeoutSampler:
    """
    Samples the function output.

    This is a generator object that at first yields the output of function
    `func`. After the yield, it either raises instance of `TimeoutExpiredError` or
    sleeps `sleep` seconds.

    Yielding the output allows you to handle every value as you wish.

    Feel free to set the instance variables.

    exceptions_dict should be in the following format:
    {
        exception0: [exception0_msg0],
        exception1: [
            exception1_msg0,
            exception1_msg1
        ],
        exception2: []
    }

    Args:
        wait_timeout (int): Time in seconds to wait for func to return a value equating to True
        sleep (int): Time in seconds between calls to func
        func (function): to be wrapped by TimeoutSampler
        exceptions (tuple): Deprecated: Tuple containing all retry exceptions to pass to TimeoutSampler
        exceptions_msg (str): Deprecated: String to match exception against
        exceptions_dict (dict): Definition for exception handling
        print_log (bool): Print elapsed time to log
    """

    def __init__(
        self,
        wait_timeout,
        sleep,
        func,
        exceptions=None,  # Deprecated
        exceptions_msg=None,  # Deprecated
        exceptions_dict=None,
        print_log=True,
        *func_args,
        **func_kwargs,
    ):
        self.wait_timeout = wait_timeout
        self.sleep = sleep
        self.func = func
        self.func_args = func_args
        self.func_kwargs = func_kwargs
        self.elapsed_time = None
        self.print_log = print_log

        self.exceptions_dict = {}
        self.exception = None  # TODO: Set when exceptions arg removed
        self.exceptions_msg = None  # TODO: Remove when exceptions_msg arg removed
        self._pre_process_exceptions(
            exceptions=exceptions,
            exceptions_msg=exceptions_msg,
            exceptions_dict=exceptions_dict,
        )

    def _pre_process_exceptions(self, exceptions, exceptions_msg, exceptions_dict):
        """
        Process exception input for use within _process_execution()

        TODO: Deprecation: This method should be removed when the 'exceptions' argument is removed from __init__

        Validate exception inputs:
            exceptions
            exceptions_msg
            exceptions_dict
        """

        if exceptions_dict and (exceptions or exceptions_msg):
            raise ValueError(
                "Must specify either exceptions_dict or exceptions/exception_msg, not both"
            )

        elif exceptions or exceptions_msg:
            warn(
                "TimeoutSampler() exception and exception_msg are now deprecated. "
                "Please update to use exceptions_dict by 2021-MM-DD",
                DeprecationWarning,
            )

        if exceptions_dict:
            self.exceptions_dict.update(exceptions_dict)
            self.exception = tuple(self.exceptions_dict.keys())

        elif exceptions is None:
            self.exceptions_dict[Exception] = []
            self.exception = (Exception,)

        else:
            self.exception = exceptions
            self.exceptions_msg = exceptions_msg

    @property
    def _func_log(self):
        return (
            f"Function: {self.func} Args: {self.func_args} Kwargs: {self.func_kwargs}"
        )

    def __iter__(self):
        last_exp = None
        timeout_watch = TimeoutWatch(timeout=self.wait_timeout)
        if self.print_log:
            LOGGER.info(
                f"Waiting for {self.wait_timeout} seconds, retry every {self.sleep} seconds"
            )

        while timeout_watch.remaining_time() > 0:
            try:
                self.elapsed_time = self.wait_timeout - timeout_watch.remaining_time()
                yield self.func(*self.func_args, **self.func_kwargs)
                self.elapsed_time = None

                time.sleep(self.sleep)

            except self.exception as exp:
                last_exp = exp
                self.elapsed_time = None

                time.sleep(self.sleep)

            finally:
                if self.elapsed_time and self.print_log:
                    LOGGER.info(f"Elapsed time: {self.elapsed_time}")

        raise TimeoutExpiredError(self._process_execution(exp=last_exp))

    @staticmethod
    def _check_exp_msgs(msgs, _exp, log):
        for msg in msgs:
            if msg in str(_exp):
                return

        LOGGER.error(log)
        raise _exp

    def _process_execution(self, exp=None):
        if exp and hasattr(exp, "__name__"):
            # Exceptions that inherit from Exception
            exp_name = exp.__name__
        elif exp:
            # Exceptions that inherit from object eg: AttributeError
            exp_name = exp.__class__.__name__
        else:
            exp_name = "N/A"

        last_exception_log = f"Last exception: {exp_name}: {exp}"
        log = "{timeout}\n{func_log}\n{last_exception_log}".format(
            timeout=self.wait_timeout,
            func_log=self._func_log,
            last_exception_log=last_exception_log,
        )

        if exp in self.exceptions_dict:
            self._check_exp_msgs(msgs=self.exceptions_dict[exp], _exp=exp, log=log)
        elif self.exceptions_msg:
            # TODO: Remove this elif when exceptions_msg is no longer an input
            self._check_exp_msgs(msgs=[self.exceptions_msg], _exp=exp, log=log)

        return log


class TimeoutWatch:
    """
    A time counter allowing to determine the time remaining since the start
    of a given interval
    """

    def __init__(self, timeout):
        self.timeout = timeout
        self.start_time = time.time()

    def remaining_time(self, log=None):
        """
        Return the remaining part of timeout since the object was created.
        """
        return self.start_time + self.timeout - time.time()


# TODO: remove the nudge when the underlying issue with namespaces stuck in
# Terminating state is fixed.
# Upstream bug: https://github.com/kubernetes/kubernetes/issues/60807
def nudge_delete(name):
    LOGGER.info(f"Nudging namespace {name} while waiting for it to delete")
    try:
        # kube client is deficient so we have to use curl to kill stuck
        # finalizers
        subprocess.check_output(["./scripts/clean-namespace.sh", name])
    except subprocess.CalledProcessError as exp:
        # deliberately ignore all errors since an intermittent nudge
        # failure is not the end of the world
        LOGGER.error(f"Error happened while nudging namespace {name}: {exp}")
        raise
