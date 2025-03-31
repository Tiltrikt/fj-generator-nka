from Lexer import Lexer
from Parser import Parser

class Calculator:
    def evaluate(self, expression):
        try:
            lexer = Lexer(expression)
            parser = Parser(lexer)
            result = parser.parse()
            return result
        except Exception as e:
            return f"Chyba: {str(e)}"

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


def print_transition_table(start_state):
    transition_table = collect_transitions(start_state)

    print("_transition_table = {")
    for state_id, transitions in transition_table.items():
        transition_str = ", ".join(f"'{symbol}': {destination_ids}" for symbol, destination_ids in transitions.items())
        print(f"    {state_id}: {{{transition_str}}},")
    print("}")


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


if __name__ == "__main__":
    calc = Calculator()
    input_text = input("> ")

    while input_text != "quit":
        if input_text != "":
            nka = calc.evaluate(input_text)
            start_state = nka.start_state

            assign_ids(start_state)

            print_transition_table(start_state)

            accepted_states = set()
            for state in nka.accepted_states:
                accepted_states.add(state.id)

            print("_accepted_states = {")
            print(f"    {', '.join(map(str, accepted_states))},")
            print("}")
        input_text = input("> ")
