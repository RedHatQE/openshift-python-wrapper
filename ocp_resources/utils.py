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

    Feel free to set the instance variables.
    """

    def __init__(
        self,
        wait_timeout,
        sleep,
        func,
        exceptions=None,
        exceptions_msg=None,
        print_log=True,
        **func_kwargs,
    ):
        self.wait_timeout = wait_timeout
        self.sleep = sleep
        self.func = func
        self.func_kwargs = func_kwargs
        self.exception = exceptions or Exception
        self.elapsed_time = None
        self.exceptions_msg = exceptions_msg
        self.print_log = print_log

    @property
    def _func_log(self):
        return f"Function: {self.func} Kwargs: {self.func_kwargs}"

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
                yield self.func(**self.func_kwargs)
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

    def _process_execution(self, exp=None):
        exp_name = exp.__class__.__name__ if exp else "N/A"
        last_exception_log = f"Last exception: {exp_name}: {exp}"

        log = "{timeout}\n{func_log}\n{last_exception_log}".format(
            timeout=self.wait_timeout,
            func_log=self._func_log,
            last_exception_log=last_exception_log,
        )

        if self.exceptions_msg:
            if self.exceptions_msg not in str(exp):
                LOGGER.error(log)
                raise exp
            else:
                LOGGER.warning(f"{self.exceptions_msg}: Retrying")

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
