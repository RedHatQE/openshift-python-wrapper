import time

from ocp_resources.logger import get_logger


LOGGER = get_logger(name=__name__)


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
        exceptions_dict (dict): Exception handling definition
        print_log (bool): Print elapsed time to log
    """

    def __init__(
        self,
        wait_timeout,
        sleep,
        func,
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

        self.exceptions_dict = exceptions_dict or {Exception: []}
        self._exceptions = tuple(self.exceptions_dict.keys())

    def _get_func_info(self, _func, type_):
        # If func is partial function.
        if getattr(_func, "func", None):
            return self._get_func_info(_func=_func.func, type_=type_)

        res = getattr(_func, type_, None)
        if res:
            # If func is lambda function.
            if _func.__name__ == "<lambda>":
                if type_ == "__module__":
                    return f"{res}.{_func.__qualname__.split('.')[1]}"

                elif type_ == "__name__":
                    free_vars = _func.__code__.co_freevars
                    free_vars = f"{'.'.join(free_vars)}." if free_vars else ""
                    return f"lambda: {free_vars}{'.'.join(_func.__code__.co_names)}"
            return res

    @property
    def _func_log(self):
        """
        Returns:
            string: `func` information to include in log message
        """
        _func_kwargs = f"Kwargs: {self.func_kwargs}" if self.func_kwargs else ""
        _func_module = self._get_func_info(_func=self.func, type_="__module__")
        _func_name = self._get_func_info(_func=self.func, type_="__name__")
        return f"Function: {_func_module}.{_func_name} {_func_kwargs}".strip()

    def __iter__(self):
        """
        Iterator

        Yields:
            any: Return value from `func`
        """
        timeout_watch = TimeoutWatch(timeout=self.wait_timeout)
        if self.print_log:
            LOGGER.info(
                f"Waiting for {self.wait_timeout} seconds, retry every {self.sleep} seconds. ({self._func_log})"
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

        # Prevent match if provided with empty string
        return any(msg and msg in str(exp) for msg in exception_messages)

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
