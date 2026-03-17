import hashlib
import string
import itertools
import time


class Password:
    def __init__(self, password: str) -> None:
        self.password = password


def hash_password(password: str) -> str:
    encoded_password = password.encode("utf-8")
    hash_object = hashlib.sha256(encoded_password)
    return hash_object.hexdigest()


class BruteForce:

    @staticmethod
    def brute_force_attack(hash_to_crack: str, max_length: int = 5) -> str | None:
        print(f"Hash to crack: {hash_to_crack}")
        print(f"Starting brute-force attack with max password length: {max_length}")

        timer_start = time.time()
        attempts = 0

        characters = string.ascii_lowercase + string.digits + string.punctuation

        for length in range(1, max_length + 1):
            for combination in itertools.product(characters, repeat=length):
                attempts += 1
                password = ''.join(combination)
                if hash_password(password) == hash_to_crack:
                    print(f"Password found: {password}")
                    print(f"Attempts: {attempts}")
                    print(f"Time taken: {time.time() - timer_start}")
                    return password

        print("Failed to crack the hash with brute-force attack.")
        return None
