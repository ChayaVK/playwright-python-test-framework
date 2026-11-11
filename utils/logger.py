"""A tiny step logger: prints each step so the console and the HTML report show what the test did."""
import logging
from contextlib import contextmanager

log = logging.getLogger("tests")


@contextmanager
def step(title: str):
    log.info("STEP: %s", title)
    yield
