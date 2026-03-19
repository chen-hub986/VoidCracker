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
            's': ['5', '$'], 'S': ['5', '$'],
            't': ['7', '+'], 'T': ['7', '+'],
            'l': ['1', '|'], 'L': ['1', '|'],
            'g': ['9'], 'G': ['9'],
            'b': ['8'], 'B': ['8'],
            'z': ['2'], 'Z': ['2']
        }

        current_stage1 = list(mutations)
        for mutation in current_stage1:
            for char, subs in substitutions.items():
                if char in mutation:
                    for sub in subs:
                        mutations.add(mutation.replace(char, sub))
                        mutations.add(mutation.replace(char, sub.upper()))

        common_suffixes = ['123', '1234', '!', '@', '#', '2024', '2025', 'password', 'admin']
        common_prefixes = ['!', '@', '#', 'the', 'my']
        separators = ['_', '-', '.']

        current_stage2 = list(mutations)
        for mutation in current_stage2:
            for suffix in common_suffixes:
                mutations.add(mutation + suffix)
                mutations.add(suffix + mutation)
            for prefix in common_prefixes:
                mutations.add(prefix + mutation)
            for sep in separators:
                mutations.add(mutation + sep + '123')
                mutations.add(mutation + sep + '2024')
                mutations.add(mutation + sep + '2025')

        current_stage3 = list(mutations)
        for mutation in current_stage3:
            if len(mutation) > 1:
                mutations.add(mutation[::-1])

        return list(mutations)


if __name__ == "__main__":
    test_password = "password123"
    mutated_passwords = MutationEngine.mutate_password(test_password)
    print(mutated_passwords)
