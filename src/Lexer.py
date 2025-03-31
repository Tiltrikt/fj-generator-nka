from enum import Enum, auto

class TokenType(Enum):
    SYMBOL = auto()
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LCBRA = auto()   # {
    RCBRA = auto()   # }
    LBRACK = auto()  # [
    RBRACK = auto()  # ]
    PIPE = auto()    # |
    EOF = auto()

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.attribute = value

    def __repr__(self):
        if self.attribute is not None:
            return f"Token({self.type}, {self.attribute})"
        return f"Token({self.type})"


class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.pos = 0
        self.current_char = self.input_text[0] if input_text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.input_text):
            self.current_char = self.input_text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            match self.current_char:
                case '(':
                    self.advance()
                    return Token(TokenType.LPAREN)
                case ')':
                    self.advance()
                    return Token(TokenType.RPAREN)
                case '{':
                    self.advance()
                    return Token(TokenType.LCBRA)
                case '}':
                    self.advance()
                    return Token(TokenType.RCBRA)
                case '[':
                    self.advance()
                    return Token(TokenType.LBRACK)
                case ']':
                    self.advance()
                    return Token(TokenType.RBRACK)
                case '|':
                    self.advance()
                    return Token(TokenType.PIPE)
                case _:
                    token = Token(TokenType.SYMBOL, self.current_char)
                    self.advance()
                    return token

        return Token(TokenType.EOF)