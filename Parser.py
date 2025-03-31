from Lexer import TokenType

class StateNode:
    def __init__(self):
        self.transitions = {}
        self.id = None

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
            self.consume(TokenType.PIPE)
            left_nka = result
            right_nka = self.sequence()

            new_start = StateNode()
            alternative_nka = NKA()

            alternative_nka.start_state = new_start
            new_start.add_transition('', left_nka.start_state)
            new_start.add_transition('', right_nka.start_state)
            alternative_nka.accepted_states = left_nka.accepted_states.union(right_nka.accepted_states)
            result = alternative_nka

        return result

    def sequence(self) -> NKA:
        result = self.element()
        while self.current_token.type == TokenType.SYMBOL:
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
        elif self.current_token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            nka = self.alternative()
            self.consume(TokenType.RPAREN)
        elif self.current_token.type == TokenType.LCBRA:
            self.consume(TokenType.LCBRA)

            start_node = StateNode()
            transitive_nka = NKA()
            nka = self.alternative()
            start_node.add_transition('', nka.start_state)
            transitive_nka.accepted_states = nka.accepted_states.copy()
            transitive_nka.accepted_states.add(start_node)
            for accept_state in nka.accepted_states:
                accept_state.add_transition('', start_node)
            transitive_nka.start_state = start_node
            nka = transitive_nka

            self.consume(TokenType.RCBRA)
        elif self.current_token.type == TokenType.LBRACK:
            self.consume(TokenType.LBRACK)

            start_node = StateNode()
            additional_node = StateNode()
            optional_nka = NKA()
            nka = self.alternative()
            start_node.add_transition('', nka.start_state)
            start_node.add_transition('', additional_node)
            optional_nka.accepted_states = nka.accepted_states.copy()
            optional_nka.accepted_states.add(additional_node)
            optional_nka.start_state = start_node
            nka = optional_nka

            self.consume(TokenType.RBRACK)
        return nka

    def parse(self) -> NKA:
        return self.regular()
