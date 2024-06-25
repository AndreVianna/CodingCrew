import asyncio

from typing import Callable, TypeVar

from .terminal import start_spinner


_R = TypeVar("_R")

async def wait_for(func: Callable[[], _R],
             /,
             text: str | None = None,
             timeout: float = 5.0,
             raise_timeout_error: bool = True) -> _R | None:
    if timeout <= 0:
        raise ValueError("Timeout must be greater than 0.")

    text = "Processing" if text is None else text

    stop_spinner = asyncio.Event()
    long_run: asyncio.Task[_R] = asyncio.create_task(asyncio.to_thread(func))
    spinner: asyncio.Task[None] = asyncio.create_task(start_spinner(text, stop_spinner))
    combined = asyncio.wait([long_run, spinner], timeout=timeout, return_when=asyncio.FIRST_COMPLETED)
    try:
        await combined
        if long_run.done():
            stop_spinner.set()
        else:
            long_run.cancel()
            spinner.cancel()
            if raise_timeout_error:
                raise asyncio.TimeoutError("The operation timed out!")
        return long_run.result() if long_run.done() else None
    except asyncio.CancelledError:
        spinner.cancel()
        return None
    finally:
        await spinner
        combined.close()
