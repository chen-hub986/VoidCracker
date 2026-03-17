import hashlib

class HashGenerator:
    @staticmethod
    def generate_hash(password: str) -> str:
        encoded_password = password.encode("utf-8")
        hash_object = hashlib.sha256(encoded_password)
        return hash_object.hexdigest()
