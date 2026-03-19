import sys

from src.hash_generator import HashGenerator
from src.dictionary_attack import DictionaryAttack
from src.brute_force import BruteForce

import hashlib
import os


def welcome_logo() -> None:
    logo = r"""
                                                                 
                (      (                       )             
 (   (     (    )\ )   )\   (       )       ( /(    (   (    
 )\  )\ (  )\  (()/( (((_)  )(   ( /(   (   )\())  ))\  )(   
((_)((_))\((_)  ((_)))\___ (()\  )(_))  )\ ((_)\  /((_)(()\  
\ \ / /((_)(_)  _| |((/ __| ((_)((_)_  ((_)| |(_)(_))   ((_) 
 \ V // _ \| |/ _` | | (__ | '_|/ _` |/ _| | / / / -_) | '_| 
  \_/ \___/|_|\__,_|  \___||_|  \__,_|\__| |_\_\ \___| |_|   
                                                             
                                                             
    """
    print(logo)


def dictionary_path() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dictionary_file = os.path.join(current_dir, 'passwords.txt')
    return dictionary_file


def generate_salted_hash(password: str, salt: str) -> str:
    salted_password = password + salt
    encoded_password = salted_password.encode("utf-8")
    hash_object = hashlib.sha256(encoded_password)
    return hash_object.hexdigest()


def prompt_positive_int(message: str) -> int | None:
    while True:
        user_input = input(message).strip()
        try:
            value = int(user_input)
            if value <= 0:
                print("Please enter a positive integer.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def main():
    while True:
        print("\nPassword Cracking Tool")
        print("1. Generate Hash")
        print("2. Generate salted Hash")
        print("3. Dictionary Attack")
        print("4. Brute Force Attack")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            password = input("Enter the password to hash: ")
            hashed_password = HashGenerator.generate_hash(password)
            print(f"Hash: {hashed_password}")

        elif choice == '2':
            password = input("Enter the password to hash: ")
            salt = os.urandom(16).hex()
            hashed_password = generate_salted_hash(password, salt)
            print(f"Salt: {salt}")
            print(f"Salted Hash: {hashed_password}")

        elif choice == '3':
            hash_to_crack = input("Enter the hash to crack: ")
            dictionary_file = dictionary_path()
            attack = DictionaryAttack(hash_to_crack, dictionary_file)
            attack.attack()

        elif choice == '4':
            hash_to_crack = input("Enter the hash to crack: ")
            max_length = prompt_positive_int("Enter the maximum password length for brute-force attack: ")
            BruteForce.brute_force_attack(hash_to_crack, max_length)

        elif choice == '5':
            print("Exiting the tool.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    welcome_logo()
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting the tool.")
        sys.exit(0)
