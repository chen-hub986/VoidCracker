from concurrent.futures import Executor, Future


def stop_pending_work(pending: set[Future], executor: Executor, shutdown_called: bool) -> bool:
    """Cancel pending futures and stop the executor once."""
    if shutdown_called:
        return True

    for future in list(pending):
        future.cancel()
    pending.clear()
    executor.shutdown(wait=False, cancel_futures=True)
    return True

