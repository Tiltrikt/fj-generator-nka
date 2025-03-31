from Lexer import TokenType

class StateNode:
    def __init__(self):
        self.transitions = {}  # Transitions from this state to other states.

    def add_transition(self, symbol, destination_node):
        if symbol not in self.transitions:
            self.transitions[symbol] = set()
        self.transitions[symbol].add(destination_node)


class NKA:
    def __init__(self):
        self.start_state = None
        self.accepted_states = set()

    def get_all_destinations(self):
       return self.accepted_states


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def consume(self, expected_token_type):
        if self.current_token.type == expected_token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError(f"Syntaktická chyba: očakávaný token {expected_token_type}, "
                               f"získaný {self.current_token.type}")

    def regular(self) -> NKA:
        result = self.alternative()
        return result

    def alternative(self) -> NKA:
        result = self.sequence()
        while self.current_token.type == TokenType.PIPE:
            print("alternative")
            self.consume(TokenType.PIPE)
            left_nka = result
            right_nka = self.sequence()

            new_start = StateNode()
            alternative_nka = NKA()

            alternative_nka.start_state = new_start
            new_start.add_transition(left_nka, left_nka.start_state)
            new_start.add_transition('', right_nka.start_state)
            alternative_nka.accepted_states = left_nka.accepted_states.union(right_nka.accepted_states)
            result = alternative_nka

        return result

    def sequence(self) -> NKA:
        result = self.element()
        while self.current_token.type == TokenType.SYMBOL:
            print("sequence")
            left_nka = result
            right_nka = self.element()

            for accept_state in left_nka.accepted_states:
                accept_state.add_transition('', right_nka.start_state)

            left_nka.accepted_states = right_nka.accepted_states
            result = left_nka
        return result

    def element(self) -> NKA:
        if self.current_token.type == TokenType.SYMBOL:
            symbol = self.current_token.attribute

            start_node = StateNode()
            accept_node = StateNode()
            nka = NKA()

            start_node.add_transition(symbol, accept_node)
            nka.start_state = start_node
            nka.accepted_states.add(accept_node)
            self.consume(TokenType.SYMBOL)
            return nka

    def parse(self) -> NKA:
        return self.regular()
