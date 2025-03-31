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
            return f"Chyba: {str(e)}"   # Vrátenie chyby

if __name__ == "__main__":
    calc = Calculator()
    input_text=input("> ")

    while input_text!="quit":
        if input_text != "":
            nka = calc.evaluate(input_text)
            print(nka.start_state.transitions)

        input_text=input("> ")