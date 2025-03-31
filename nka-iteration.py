from copy import deepcopy

class NKA:

    def __init__(self, transition_table: dict, accepted_states: set):
        self.transition_table = transition_table
        self.accepted_states = accepted_states

    def evaluate_expression(self, expression: str, actual_state):
        if len(expression) == 0:
            if actual_state in _accepted_states:
                return True
            for key in self.transition_table[actual_state].keys():
                if key == '':
                    for state in self.transition_table[actual_state].get(key):
                        result = self.evaluate_expression(deepcopy(expression), state)
                        if result:
                            return True
            return False

        for key in self.transition_table[actual_state].keys():
            if key == '':
                for state in self.transition_table[actual_state].get(key):
                    result = self.evaluate_expression(deepcopy(expression), state)
                    if result:
                        return True
            elif key == expression[0]:
                for state in self.transition_table[actual_state].get(key):
                    result = self.evaluate_expression(deepcopy(expression[1:]), state)
                    if result:
                        return True
        return False


# _transition_table = {
#     0: {'': {1, 3}, '1': {2, 4}},
#     1: {'0': {2}},
#     2: {},
#     3: {'1': {4}},
#     4: {'': {5}},
#     5: {'': {6}},
#     6: {'': {7, 9}},
#     7: {'0': {8}},
#     8: {'': {6}},
#     9: {'1': {10}},
#     10: {'': {6}}
# }

_transition_table = {
    0: {'': {1}},
    1: {'': {2, 4}},
    2: {'0': {3}},
    3: {'': {0}},
    4: {'1': {5}},
    5: {'': {0}},
}
_accepted_states = {
    0, 3, 5,
}


def main():
    word = input("Enter a word: ")
    nka = NKA(_transition_table, _accepted_states)
    if nka.evaluate_expression(word, 0):
        print(f'Word "{word}" accepted')
    else:
        print(f'Word "{word}" rejected')


if __name__ == '__main__':
    main()