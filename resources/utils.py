import logging
import subprocess
import time


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
    """

    def __init__(
        self,
        wait_timeout,
        sleep,
        func,
        exceptions=None,
        exceptions_msg=None,
        print_log=True,
        *func_args,
        **func_kwargs,
    ):
        self.wait_timeout = wait_timeout
        self.sleep = sleep
        self.func = func
        self.func_args = func_args
        self.func_kwargs = func_kwargs
        self.exception = exceptions if exceptions else Exception
        self.elapsed_time = None
        self.exceptions_msg = exceptions_msg
        self.print_log = print_log
        self.last_exception_log = None

    def _func_log(self):
        return (
            f"Function: {self.func} Args: {self.func_args} Kwargs: {self.func_kwargs}"
        )

    def __iter__(self):
        timeout_watch = TimeoutWatch(timeout=self.wait_timeout)
        if self.print_log:
            LOGGER.info(
                f"Waiting for {self.wait_timeout} seconds, retry every {self.sleep} seconds"
            )

        while True:
            try:
                self.elapsed_time = self.wait_timeout - timeout_watch.remaining_time(
                    log=self._func_log if self.print_log else None
                )
                yield self.func(*self.func_args, **self.func_kwargs)
                self.elapsed_time = None
                time.sleep(self.sleep)

            except self.exception as exp:
                log = self._process_execution(exp=exp)
                self.elapsed_time = None
                timeout_watch.remaining_time(log=log)

                time.sleep(self.sleep)

            finally:
                if self.elapsed_time and self.print_log:
                    LOGGER.info(f"Elapsed time: {self.elapsed_time}")

    def _process_execution(self, exp):
        exp_name = exp.__class__.__name__
        #  timeout_watch.remaining_time() (line 67) raise TimeoutExpiredError.
        #  TimeoutExpiredError shouldn't be the last exception for log.
        if exp_name != TimeoutExpiredError.__name__:
            self.last_exception_log = f"Last exception: {exp_name}: {exp}"

        log = "{timeout}\n{func_log}\n{last_exception_log}".format(
            timeout=self.wait_timeout,
            func_log=self._func_log,
            last_exception_log=self.last_exception_log,
        )

        if self.exceptions_msg:
            if self.exceptions_msg not in str(exp):
                LOGGER.error(log)
                raise
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
        new_timeout = self.start_time + self.timeout - time.time()
        if new_timeout > 0:
            return new_timeout

        raise TimeoutExpiredError(log or self.timeout)


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
