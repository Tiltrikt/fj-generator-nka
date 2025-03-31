from Lexer import TokenType
from PrettyPrint import PrettyPrintTree

class Tree:
    def __init__(self, value):
        self.val = value
        self.children = []

    def add_child(self, child):
        if isinstance(child, str):
            child = Tree(child)
        self.children.append(child)
        return child

class StateNode:
    def __init__(self):
        self.transitions = {}
        self.id = None

    def add_transition(self, symbol, destination_node):
        if symbol not in self.transitions:
            self.transitions[symbol] = set()
        self.transitions[symbol].add(destination_node)

    def __str__(self):
        return f"StateNode(id={self.id}, transitions={self.transitions})"

class NKA:
    def __init__(self):
        self.start_state = None
        self.accepted_states = set()

    def get_all_destinations(self):
        return self.accepted_states

    def __str__(self):
        return f"NKA(start_state={self.start_state}, accepted_states={self.accepted_states})"

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def consume(self, expected_token_type, tree):
        if self.current_token.type == expected_token_type:
            tree.add_child(str(self.current_token))
            self.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError(f"Syntaktická chyba: očakávaný token {expected_token_type}, "
                               f"získaný {self.current_token.type}")

    def regular(self) -> NKA:
        pt = PrettyPrintTree(lambda x: x.children, lambda x: x.val)
        tree = Tree("regular")
        result = self.alternative(tree)
        pt(tree)
        return result

    def alternative(self, tree) -> NKA:
        node = tree.add_child("alternative")
        result = self.sequence(node)
        while self.current_token.type == TokenType.PIPE:
            self.consume(TokenType.PIPE, node)
            left_nka = result
            right_nka = self.sequence(node)

            new_start = StateNode()
            alternative_nka = NKA()
            alternative_nka.start_state = new_start
            new_start.add_transition('', left_nka.start_state)
            new_start.add_transition('', right_nka.start_state)
            alternative_nka.accepted_states = left_nka.accepted_states.union(right_nka.accepted_states)
            result = alternative_nka
        return result

    def sequence(self, tree) -> NKA:
        node = tree.add_child("sequence")
        result = self.element(node)
        while self.current_token.type in (TokenType.SYMBOL, TokenType.LPAREN, TokenType.LCBRA, TokenType.LBRACK):
            left_nka = result
            right_nka = self.element(node)
            for accept_state in left_nka.accepted_states:
                accept_state.add_transition('', right_nka.start_state)
            left_nka.accepted_states = right_nka.accepted_states
            result = left_nka
        return result

    def element(self, tree) -> NKA:
        node = tree.add_child("element")
        if self.current_token.type == TokenType.SYMBOL:
            symbol = self.current_token.attribute
            start_node = StateNode()
            accept_node = StateNode()
            nka = NKA()
            start_node.add_transition(symbol, accept_node)
            nka.start_state = start_node
            nka.accepted_states.add(accept_node)
            self.consume(TokenType.SYMBOL, node)
        elif self.current_token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN, node)
            nka = self.alternative(node)
            self.consume(TokenType.RPAREN, node)
        elif self.current_token.type == TokenType.LCBRA:
            self.consume(TokenType.LCBRA, node)
            start_node = StateNode()
            transitive_nka = NKA()
            nka = self.alternative(node)
            start_node.add_transition('', nka.start_state)
            transitive_nka.accepted_states = nka.accepted_states.copy()
            transitive_nka.accepted_states.add(start_node)
            for accept_state in nka.accepted_states:
                accept_state.add_transition('', start_node)
            transitive_nka.start_state = start_node
            nka = transitive_nka
            self.consume(TokenType.RCBRA, node)
        elif self.current_token.type == TokenType.LBRACK:
            self.consume(TokenType.LBRACK, node)
            start_node = StateNode()
            additional_node = StateNode()
            optional_nka = NKA()
            nka = self.alternative(node)
            start_node.add_transition('', nka.start_state)
            start_node.add_transition('', additional_node)
            optional_nka.accepted_states = nka.accepted_states.copy()
            optional_nka.accepted_states.add(additional_node)
            optional_nka.start_state = start_node
            nka = optional_nka
            self.consume(TokenType.RBRACK, node)
        return nka

    def parse(self) -> NKA:
        return self.regular()