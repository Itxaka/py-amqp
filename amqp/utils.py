import logging
import os

from typing import (
    Any, AnyStr, Callable, Generator, Optional, Union, cast,
)

# enables celery 3.1.23 to start again
from vine import promise                # noqa
from vine.utils import wraps

from .types import Fd

try:
    import fcntl
except ImportError:  # pragma: no cover
    fcntl = None   # noqa


def set_cloexec(fd: Fd, cloexec: bool) -> None:
    if not isinstance(fd, int):
        fd = fd.fileno()
    os.set_inheritable(fd, cloexec)


def coro(gen: Callable) -> Callable:

    @wraps(gen)
    def _boot(*args, **kwargs) -> Generator:
        co = gen(*args, **kwargs)
        next(co)
        return co

    return _boot


def str_to_bytes(s: AnyStr) -> bytes:
    if isinstance(s, str):
        return cast(str, s).encode()
    return s


def bytes_to_str(s: AnyStr) -> str:
    if isinstance(s, bytes):
        return cast(bytes, s).decode()
    return s


def get_logger(logger: Optional[Union[logging.Logger, str]]) -> logging.Logger:
    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    if not logger.hasHandlers():
        logger.addHandler(logging.NullHandler())
    return logger
