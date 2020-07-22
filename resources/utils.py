import logging
import subprocess
import time


_DELETE_NUDGE_DELAY = 30
_DELETE_NUDGE_INTERVAL = 5
LOGGER = logging.getLogger(__name__)


class TimeoutExpiredError(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f"Timed Out: {self.value}"


class TimeoutSampler(object):
    """
    Samples the function output.

    This is a generator object that at first yields the output of function
    `func`. After the yield, it either raises instance of `TimeoutExpiredError` or
    sleeps `sleep` seconds.

    Yielding the output allows you to handle every value as you wish.

    Feel free to set the instance variables.
    """

    def __init__(
        self, timeout, sleep, func, exceptions=None, *func_args, **func_kwargs
    ):
        self.timeout = timeout
        self.sleep = sleep
        self.func = func
        self.func_args = func_args
        self.func_kwargs = func_kwargs
        self.start_time = None
        self.last_sample_time = None
        self.exception = exceptions if exceptions else Exception

    def __iter__(self):
        caught_exception = None
        if self.start_time is None:
            self.start_time = time.time()
        while True:
            self.last_sample_time = time.time()
            try:
                yield self.func(*self.func_args, **self.func_kwargs)
            except self.exception as e:
                caught_exception = e
                pass

            if self.timeout < (time.time() - self.start_time):
                raise TimeoutExpiredError(
                    f"{self.timeout} {caught_exception}"
                    if caught_exception
                    else self.timeout
                )
            time.sleep(self.sleep)


class TimeoutWatch:
    """
    A time counter allowing to determine the time remaining since the start
    of a given interval
    """

    def __init__(self, timeout):
        self.timeout = timeout
        self.start_time = time.time()

    def remaining_time(self):
        """
        Return the remaining part of timeout since the object was created.
        """
        new_timeout = self.start_time + self.timeout - time.time()
        if new_timeout > 0:
            return new_timeout
        raise TimeoutExpiredError(self.timeout)


class NudgeTimers:
    """
    A holder for two values needed to time deletion of an object properly.
    """

    def __init__(self):
        self.nudge_start_time = time.time()
        self.last_nudge = 0


# TODO: remove the nudge when the underlying issue with namespaces stuck in
# Terminating state is fixed.
# Upstream bug: https://github.com/kubernetes/kubernetes/issues/60807
def nudge_delete(name, timers):
    # remember the time of the first delete attempt
    if not timers.nudge_start_time:
        timers.nudge_start_time = time.time()
    # delay active nudging in hope regular delete procedure will succeed
    current_time = time.time()
    if current_time - _DELETE_NUDGE_DELAY < timers.nudge_start_time:
        return
    # don't nudge more often than once in 5 seconds
    if timers.last_nudge + _DELETE_NUDGE_INTERVAL > current_time:
        return
    LOGGER.info(f"Nudging namespace {name} while waiting for it to delete")
    try:
        # kube client is deficient so we have to use curl to kill stuck
        # finalizers
        subprocess.check_output(["./scripts/clean-namespace.sh", name])
        timers.last_nudge = time.time()
    except subprocess.CalledProcessError as e:
        # deliberately ignore all errors since an intermittent nudge
        # failure is not the end of the world
        LOGGER.info(f"Error happened while nudging namespace {name}: {e}")
