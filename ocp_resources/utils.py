import logging
import time
from warnings import warn


LOGGER = logging.getLogger(__name__)


class InvalidArgumentsError(Exception):
    pass


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

    If an exception is raised within `func`:
        Example exception inheritance:
            class Exception
            class AExampleError(Exception)
            class BExampleError(AExampleError)

        The raised exception's class will fall into one of three categories:
            1. An exception class specifically declared in exceptions_dict
                exceptions_dict: {BExampleError: []}
                raise: BExampleError
                result: continue

            2. A child class inherited from an exception class in exceptions_dict
                exceptions_dict: {AExampleError: []}
                raise: BExampleError
                result: continue

            3. Everything else, this will always re-raise the exception
                exceptions_dict: {BExampleError: []}
                raise: AExampleError
                result: raise

    Args:
        wait_timeout (int): Time in seconds to wait for func to return a value equating to True
        sleep (int): Time in seconds between calls to func
        func (function): to be wrapped by TimeoutSampler
        exceptions (tuple): Deprecated: Tuple containing all retry exceptions
        exceptions_msg (str): Deprecated: String to match exception against
        exceptions_dict (dict): Exception handling definition
        print_log (bool): Print elapsed time to log
    """

    def __init__(
        self,
        wait_timeout,
        sleep,
        func,
        exceptions=None,  # TODO: Deprecated and will be removed, use exceptions_dict
        exceptions_msg=None,  # TODO: Deprecated and will be removed, use exceptions_dict
        exceptions_dict=None,
        print_log=True,
        **func_kwargs,
    ):
        self.wait_timeout = wait_timeout
        self.sleep = sleep
        self.func = func
        self.func_kwargs = func_kwargs
        self.elapsed_time = None
        self.print_log = print_log

        # TODO: when exceptions arg removed replace with: self.exceptions_dict = exceptions_dict or {Exception: []}
        self.exceptions_dict = self._pre_process_exceptions(
            exceptions=exceptions,
            exceptions_msg=exceptions_msg,
            exceptions_dict=exceptions_dict,
        )
        self._exceptions = tuple(self.exceptions_dict.keys())

    def _pre_process_exceptions(self, exceptions, exceptions_msg, exceptions_dict):
        """
        Convert any deprecated `exceptions` and `exceptions_msg` arguments to an `exceptions_dict`

        TODO: Deprecation: This method should be removed when the 'exceptions' argument is removed from __init__

        Args:
            exceptions (tuple): Deprecated: Tuple containing all retry exceptions
            exceptions_msg (str): Deprecated: String to match exception against
            exceptions_dict (dict): Exception handling definition

        Returns:
            dict: exceptions_dict compatible input
        """
        output = {}
        if exceptions_dict and (exceptions or exceptions_msg):
            raise InvalidArgumentsError(
                "Must specify either exceptions_dict or exceptions/exception_msg, not both"
            )

        elif exceptions or exceptions_msg:
            warn(
                "TimeoutSampler() exception and exception_msg are now deprecated. "
                "Please update to use exceptions_dict by Oct 12, 2021",
                DeprecationWarning,
            )

        if exceptions_dict:
            output.update(exceptions_dict)

        elif exceptions is None:
            output[Exception] = []

        else:
            if not isinstance(exceptions, tuple):
                exceptions = (exceptions,)

            for exp in exceptions:
                if exceptions_msg:
                    output[exp] = [exceptions_msg]
                else:
                    output[exp] = []

        return output

    @property
    def _func_log(self):
        """
        Returns:
            string: `func` information to include in log message
        """
        return f"Function: {self.func} Kwargs: {self.func_kwargs}"

    def __iter__(self):
        """
        Iterator

        Yields:
            any: Return value from `func`
        """
        timeout_watch = TimeoutWatch(timeout=self.wait_timeout)
        if self.print_log:
            LOGGER.info(
                f"Waiting for {self.wait_timeout} seconds, retry every {self.sleep} seconds"
            )

        last_exp = None
        while timeout_watch.remaining_time() > 0:
            try:
                self.elapsed_time = self.wait_timeout - timeout_watch.remaining_time()
                yield self.func(**self.func_kwargs)
                self.elapsed_time = None

                time.sleep(self.sleep)

            except self._exceptions as exp:
                last_exp = exp
                last_exp_log = self._get_exception_log(exp=last_exp)
                if self._is_raisable_exception(exp=last_exp):
                    LOGGER.error(last_exp_log)
                    raise exp

                self.elapsed_time = None
                time.sleep(self.sleep)

            finally:
                if self.elapsed_time and self.print_log:
                    LOGGER.info(f"Elapsed time: {self.elapsed_time}")

        raise TimeoutExpiredError(self._get_exception_log(exp=last_exp))

    @staticmethod
    def _is_exception_matched(exp, exception_messages):
        """
        Args:
            exp (Exception): Exception object raised by `func`
            exception_messages (list): Either an empty list allowing all text,
                                       or a list of allowed strings to match against the exception text.

        Returns:
            bool: True if exception text is allowed or no exception text given, False otherwise
        """
        if not exception_messages:
            return True

        for msg in exception_messages:
            # Prevent match if provided with empty string
            if msg and msg in str(exp):
                return True

        return False

    def _is_raisable_exception(self, exp):
        """
        Verify whether exception should be raised during execution of `func`

        Args:
            exp (Exception): Exception object raised by `func`

        Returns:
            bool: True if exp should be raised, False otherwise
        """

        for entry in self.exceptions_dict:
            if isinstance(exp, entry):  # Check inheritance for raised exception
                exception_messages = self.exceptions_dict.get(entry)
                if self._is_exception_matched(
                    exp=exp, exception_messages=exception_messages
                ):
                    return False

        return True

    def _get_exception_log(self, exp):
        """
        Args:
            exp (any): Raised exception

        Returns:
            string: Log message for exception
        """
        exp_name = exp.__class__.__name__ if exp else "N/A"

        last_exception_log = f"Last exception: {exp_name}: {exp}"
        return f"{self.wait_timeout}\n{self._func_log}\n{last_exception_log}"


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
