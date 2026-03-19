import hashlib
import string
import itertools
import time
import os

from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait


def hash_password(password: str) -> str:
    encoded_password = password.encode("utf-8")
    hash_object = hashlib.sha256(encoded_password)
    return hash_object.hexdigest()


def find_match_in_batch(candidates: list[str], hash_to_crack: str) -> str | None:
    for candidate in candidates:
        if hash_password(candidate) == hash_to_crack:
            return candidate
    return None


class BruteForce:

    @staticmethod
    def brute_force_attack(hash_to_crack: str, max_length: int = 5) -> str | None:
        core = os.cpu_count() or 1
        max_in_flight = core * 4
        batch_size = 500
        print(f"Using {core} processes for the attack.")

        print(f"Hash to crack: {hash_to_crack}")
        print(f"Starting brute-force attack with max password length: {max_length}")

        timer_start = time.time()
        attempts = 0

        characters = string.ascii_lowercase + string.digits + string.punctuation

        executor = ProcessPoolExecutor(max_workers=core)
        shutdown_called = False
        try:
            pending = set()

            def stop_pending_work() -> None:
                nonlocal shutdown_called
                if shutdown_called:
                    return
                for future in list(pending):
                    future.cancel()
                pending.clear()
                executor.shutdown(wait=False, cancel_futures=True)
                shutdown_called = True

            def collect_completed(completed_futures) -> str | None:
                nonlocal shutdown_called
                for future in completed_futures:
                    pending.remove(future)
                    matched_candidate = future.result()
                    if matched_candidate is not None:
                        print(f"Password found: {matched_candidate}")
                        print(f"Time taken: {time.time() - timer_start:.2f} seconds")
                        stop_pending_work()
                        return matched_candidate
                return None

            for length in range(1, max_length + 1):
                batch: list[str] = []
                for password_tuple in itertools.product(characters, repeat=length):
                    candidate = ''.join(password_tuple)
                    attempts += 1
                    if attempts % 100000 == 0:
                        print(f"Attempts: {attempts}, Time elapsed: {time.time() - timer_start:.2f} seconds")

                    batch.append(candidate)
                    if len(batch) >= batch_size:
                        pending.add(executor.submit(find_match_in_batch, batch, hash_to_crack))
                        batch = []

                    if len(pending) >= max_in_flight:
                        done, _ = wait(pending, return_when=FIRST_COMPLETED)
                        match = collect_completed(done)
                        if match is not None:
                            return match

                if batch:
                    pending.add(executor.submit(find_match_in_batch, batch, hash_to_crack))

                while pending:
                    done, _ = wait(pending, return_when=FIRST_COMPLETED)
                    match = collect_completed(done)
                    if match is not None:
                        return match

            print("Failed to crack the hash with brute-force attack.")
            return None
        finally:
            if not shutdown_called:
                executor.shutdown(wait=True, cancel_futures=False)
