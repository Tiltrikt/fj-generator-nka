from Lexer import Lexer
from Parser import Parser

template = """

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
        if nka.evaluate_expression(input_text, 0):
            print(f"Word '{input_text}' is ACCEPTED!")
        else:
            print(f"Word '{input_text}' is NOT ACCEPTED!")
        input_text = input("Enter a word: ")

if __name__ == '__main__':
    main()
"""

class Generator:
    def generate(self, expression):
            lexer = Lexer(expression)
            parser = Parser(lexer)
            result = parser.parse()
            return result

def assign_ids(start_state, state_counter=None, visited=None):
    if state_counter is None:
        state_counter = [0]
    if visited is None:
        visited = set()

    if start_state is None:
        return

    if id(start_state) in visited:
        return

    visited.add(id(start_state))

    start_state.id = state_counter[0]
    state_counter[0] += 1

    for destination in start_state.transitions.values():
        for next_state in destination:
            assign_ids(next_state, state_counter, visited)


def capture_transition_table(start_state):
    transition_table = collect_transitions(start_state)

    result = "_transition_table = {\n"
    for state_id, transitions in transition_table.items():
        transition_str = ", ".join(f"'{symbol}': {destination_ids}" for symbol, destination_ids in transitions.items())
        result += f"    {state_id}: {{{transition_str}}},\n"
    result += "}"

    return result


def collect_transitions(start_state, visited=None):
    if visited is None:
        visited = set()

    transition_table = {}

    if start_state is None:
        return transition_table

    if id(start_state) in visited:
        return transition_table

    visited.add(id(start_state))

    state_transitions = {}
    for symbol, destination_nodes in start_state.transitions.items():
        destination_ids = {node.id for node in destination_nodes}
        state_transitions[symbol] = destination_ids

    transition_table[start_state.id] = state_transitions

    for symbol, destination_nodes in start_state.transitions.items():
        for node in destination_nodes:
            sub_transitions = collect_transitions(node, visited)
            transition_table.update(sub_transitions)

    return transition_table


def write_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    generator = Generator()
    input_text = input("Enter regular expression:")
    print("Derivation tree:\n")

    try:
        nka = generator.generate(input_text)
        start_state = nka.start_state

        assign_ids(start_state)

        transition_table_content = capture_transition_table(start_state)

        accepted_states = set()
        for state in nka.accepted_states:
            accepted_states.add(state.id)

        accepted_states_content = "_accepted_states = {\n"
        accepted_states_content += f"    {', '.join(map(str, accepted_states))},\n"
        accepted_states_content += "}"

        output_content = transition_table_content + "\n" + accepted_states_content + template
        write_to_file("nka.py", output_content)
        print("\n\nFile nka.py was generated")
    except Exception as e:
        print(f"Chyba: {str(e)}")