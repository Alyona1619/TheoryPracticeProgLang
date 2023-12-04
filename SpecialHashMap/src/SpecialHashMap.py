class SpecialHashMap(dict):
    def __init__(self):
        super().__init__()
        self.iloc = Iloc(self)
        self.ploc = Ploc(self)


class Iloc:
    def __init__(self, special_hash_map):
        self.special_hash_map = special_hash_map

    def __getitem__(self, index):
        sorted_keys = sorted(self.special_hash_map.keys())
        try:
            key = sorted_keys[index]
            return self.special_hash_map[key]
        except IndexError:
            return None


class Ploc:
    def __init__(self, special_hash_map):
        self.special_hash_map = special_hash_map

    def __getitem__(self, requirement):
        requirements = self.parse_param(requirement)
        return {key: self.special_hash_map[key] for key in self.special_hash_map if self.satisfies_condition(key, requirements)}

    def parse_param(self, params):
        return [param.strip() for param in params.replace('(', '').replace(')', '').split(',')]

    def parse_operator(self, operators):
        return ''.join(char for char in operators if char in ['>', '<', '='])

    def satisfies_condition(self, key, requirements):
        split_key = self.parse_param(key)

        if len(requirements) == len(split_key):
            for i in range(len(requirements)):
                operator = self.parse_operator(requirements[i])
                right_value = requirements[i].replace(operator, '')

                # Handle both string and tuple keys
                left_value = split_key[i] if isinstance(split_key[i], (int, float)) else str(split_key[i])

                if operator == '>':
                    if not self.compare(left_value, right_value, operator):
                        return False
                elif operator == '<':
                    if not self.compare(left_value, right_value, operator):
                        return False
                elif operator == '>=':
                    if not self.compare(left_value, right_value, operator):
                        return False
                elif operator == '<=':
                    if not self.compare(left_value, right_value, operator):
                        return False
                elif operator == '=':
                    if not self.compare(left_value, right_value, operator):
                        return False
                elif operator == '<>':
                    if not self.compare(left_value, right_value, operator):
                        return False
                else:
                    raise ValueError("Invalid operator")
            return True
        return False

    def compare(self, left_value, right_value, operator):
        try:
            left_value = float(left_value)
            right_value = float(right_value)
        except ValueError:
            return False

        if operator == '>':
            return left_value > right_value
        elif operator == '<':
            return left_value < right_value
        elif operator == '>=':
            return left_value >= right_value
        elif operator == '<=':
            return left_value <= right_value
        elif operator == '=':
            return left_value == right_value
        elif operator == '<>':
            return left_value != right_value
        else:
            return False

    # def satisfies_condition(self, key, requirements):
    #     split_key = self.parse_param(key)
    #
    #     if len(requirements) == len(split_key):
    #         for i in range(len(requirements)):
    #             operator = self.parse_operator(requirements[i])
    #             right_value = requirements[i].replace(operator, '')
    #
    #             # Handle both string and tuple keys
    #             left_value = split_key[i] if isinstance(split_key[i], (int, float)) else str(split_key[i])
    #
    #             if operator == '>':
    #                 if left_value <= right_value:
    #                     return False
    #             elif operator == '<':
    #                 if left_value >= right_value:
    #                     return False
    #             elif operator == '>=':
    #                 if left_value < right_value:
    #                     return False
    #             elif operator == '<=':
    #                 if left_value > right_value:
    #                     return False
    #             elif operator == '=':
    #                 if left_value != right_value:
    #                     return False
    #             elif operator == '<>':
    #                 if left_value == right_value:
    #                     return False
    #             else:
    #                 raise ValueError("Invalid operator")
    #         return True
    #     return False

