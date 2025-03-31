_transition_table = {
    0: {'': {1, 9}},
    1: {'1': {2}},
    2: {'': {3}},
    3: {'': {4}},
    4: {'': {5, 7}},
    5: {'0': {6}},
    6: {'': {3}},
    7: {'1': {8}},
    8: {'': {3}},
    9: {'0': {10}},
    10: {},
}
_accepted_states = {
    8, 10, 3, 6,
}

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

def main():
    input_text = input("Enter a word: ")
    nka = NKA(_transition_table, _accepted_states)

    while input_text != "quit":
        if input_text != "":
            if nka.evaluate_expression(input_text, 0):
                print(f'Word "{input_text}" ACCEPTED')
            else:
                print(f'Word "{input_text}" REJECTED')
        input_text = input("Enter a word: ")

if __name__ == '__main__':
    main()