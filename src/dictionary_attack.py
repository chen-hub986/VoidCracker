import hashlib

import src.mutation_engine as mutation_engine


class DictionaryAttack:
    def __init__(self, hash_to_crack: str, dictionary_file: str) -> None:
        self.hash_to_crack = hash_to_crack
        self.dictionary_file = dictionary_file

    def attack(self) -> str | None:
        print(f"looking for {self.dictionary_file}")
        print(f"hash to crack: {self.hash_to_crack}")

        try:
            with open(self.dictionary_file, 'r', encoding='utf-8') as file:
                for line in file:
                    password = line.strip()
                    mutations = mutation_engine.MutationEngine.mutate_password(password)
                    for mutated_password in mutations:
                        encoded_password = mutated_password.encode('utf-8')
                        hash_object = hashlib.sha256(encoded_password)
                        generated_hash = hash_object.hexdigest()

                        if generated_hash == self.hash_to_crack:
                            print(f"Password found: {mutated_password}")
                            return mutated_password
                        
            print("failed to crack the hash with the provided dictionary.")
            return None
        except FileNotFoundError:
            print("Dictionary file not found. Please check the file path.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
