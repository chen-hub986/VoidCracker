class MutationEngine:
    @staticmethod
    def mutate_password(password: str) -> list[str]:
        mutations = set()

        mutations.add(password)

        mutations.add(password.lower())
        mutations.add(password.upper())
        mutations.add(password.capitalize())

        substitutions = {
            'a': ['@', '4'], 'A': ['@', '4'],
            'e': ['3'], 'E': ['3'],
            'i': ['1', 'l'], 'I': ['1', 'l'],
            'o': ['0'], 'O': ['0'],
            's': ['5', '$'], 'S': ['5', '$']
        }

        current_stage1 = list(mutations)
        for mutation in current_stage1:
            for char, subs in substitutions.items():
                if char in mutation:
                    for sub in subs:
                        mutations.add(mutation.replace(char, sub))
                        mutations.add(mutation.replace(char, sub.upper()))

        common_suffixes = ['123', '!', '2024', 'password']

        current_stage2 = list(mutations)
        for mutation in current_stage2:
            for suffix in common_suffixes:
                mutations.add(mutation + suffix)
                mutations.add(suffix + mutation)
        return list(mutations)


if __name__ == "__main__":
    test_password = "password123"
    mutated_passwords = MutationEngine.mutate_password(test_password)
    print(mutated_passwords)
