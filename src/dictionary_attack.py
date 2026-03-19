import hashlib
import os
import time

from src.mutation_engine import MutationEngine
from src.executor_utils import stop_pending_work
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait


def check_password_candidate(password: str, hash_to_crack: str) -> str | None:
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if hashed_password == hash_to_crack:
        return password
    return None


class DictionaryAttack:
    def __init__(self, hash_to_crack: str, dictionary_file: str) -> None:
        self.hash_to_crack = hash_to_crack
        self.dictionary_file = dictionary_file

    @staticmethod
    def _load_passwords(dictionary_file: str) -> list[str]:
        # Try common encodings used by editors on Windows before failing.
        encodings = ("utf-8", "utf-8-sig", "cp1252", "cp950", "latin-1")
        for encoding in encodings:
            try:
                with open(dictionary_file, 'r', encoding=encoding) as file:
                    return [line.strip() for line in file if line.strip()]
            except UnicodeDecodeError:
                continue
        raise UnicodeDecodeError("unknown", b"", 0, 1, "Cannot decode dictionary file with supported encodings")

    def attack(self) -> str | None:
        timer_start = time.time()

        core = max(1, os.cpu_count() or 1)
        print(f"Using {core} processes for the attack.")

        print(f"looking for {self.dictionary_file}")
        print(f"hash to crack: {self.hash_to_crack}")

        try:
            passwords = self._load_passwords(self.dictionary_file)

            mutated_passwords_set: set[str] = set()
            for password in passwords:
                mutated_passwords_set.update(MutationEngine.mutate_password(password))
            mutated_passwords = list(mutated_passwords_set)

            max_in_flight = core * 4
            executor = ProcessPoolExecutor(max_workers=core)
            shutdown_called = False
            try:
                pending = set()

                def collect_completed(completed_futures) -> str | None:
                    nonlocal shutdown_called
                    for future in completed_futures:
                        pending.remove(future)
                        result = future.result()
                        if result:
                            print(f"Password found: {result}")
                            print(f"Time taken: {time.time() - timer_start}")
                            shutdown_called = stop_pending_work(pending, executor, shutdown_called)
                            return result
                    return None

                for password in mutated_passwords:
                    pending.add(executor.submit(check_password_candidate, password, self.hash_to_crack))

                    if len(pending) >= max_in_flight:
                        done, _ = wait(pending, return_when=FIRST_COMPLETED)
                        match = collect_completed(done)
                        if match is not None:
                            return match

                while pending:
                    done, _ = wait(pending, return_when=FIRST_COMPLETED)
                    match = collect_completed(done)
                    if match is not None:
                        return match
            finally:
                if not shutdown_called:
                    executor.shutdown(wait=True, cancel_futures=False)
            print("failed to crack the hash with the provided dictionary.")
            return None
        except FileNotFoundError:
            print("Dictionary file not found. Please check the file path.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
