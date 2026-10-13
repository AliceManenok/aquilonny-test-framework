"""Polling helper: wait for a condition with a timeout instead of sleeping for a fixed time."""

import time
from collections.abc import Callable


def wait_until[T](  # Returns to wait_until the value returned by condition()
    condition: Callable[[], T],  # Callable takes no arguments, returns a value of type T
    timeout: float = 10,
    interval: float = 0.5,
    description: str = "condition",
) -> T:
    """Call condition() every `interval` seconds until it returns a truthy value, and return it.

    Raises TimeoutError naming the description and the last value once `timeout` runs out.
    """
    deadline = time.monotonic() + timeout
    while True:  # Repeats till the condition is met or timeout occurs
        result = condition()
        if result:
            return result
        if time.monotonic() >= deadline:
            raise TimeoutError(f"Waited {timeout}s for {description}; last value: {result!r}")
        time.sleep(interval)
