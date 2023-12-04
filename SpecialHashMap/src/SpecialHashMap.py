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
        if 0 <= index < len(sorted_keys):
            key = sorted_keys[index]
            return self.special_hash_map[key]
        else:
            raise IndexError("Index out of range")


class Ploc:
    def __init__(self, special_hash_map):
        self.special_hash_map = special_hash_map

    def __getitem__(self, requirement):
        requirements = self.parse_param(requirement)
        return {key: self.special_hash_map[key] for key in self.special_hash_map if self.satisfies_condition(key, requirements)}

    def parse_param(self, params):
        return [param.strip() for param in params.replace('(', '').replace(')', '').split(',')]

    def parse_operator(self, operators):
        valid_operators = ['>', '<', '=']
        operator = ''.join(char for char in operators if char in valid_operators)
        if not operator:
            raise ValueError(f"Invalid operator: {operators}")
        return operator

    def compare_values(self, left_value, right_value, operator):
        try:
            left_value = float(left_value)
            right_value = float(right_value)
        except ValueError:
            return False

        match operator:
            case '>':
                return left_value > right_value
            case '<':
                return left_value < right_value
            case '>=':
                return left_value >= right_value
            case '<=':
                return left_value <= right_value
            case '=':
                return left_value == right_value
            case '<>':
                return left_value != right_value

    def satisfies_condition(self, key, requirements):
        split_key = self.parse_param(key)

        if len(requirements) == len(split_key):
            for i in range(len(requirements)):
                operator = self.parse_operator(requirements[i])
                right_value = requirements[i].replace(operator, '')

                left_value = split_key[i] if isinstance(split_key[i], (int, float)) else str(split_key[i])

                if not self.compare_values(left_value, right_value, operator):
                    return False
            return True
        return False



