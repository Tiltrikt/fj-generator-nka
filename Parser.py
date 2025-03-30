from Lexer import TokenType


# Syntaktický analyzátor - implementuje rekurzívny zostup podľa gramatiky
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer  # Lexikálny analyzátor, ktorý dodáva tokeny
        self.current_token = self.lexer.get_next_token()  # Načítame prvý token

    def consume(self, expected_token_type):
        """
        Kontrolná metóda - kontroluje, či aktuálny token je očakávaného typu.
        Ak áno, posunie sa na ďalší token. Ak nie, vyhodí chybu.

        Táto metóda implementuje prediktívnu analýzu - očakávame konkrétny token
        na základe gramatických pravidiel.
        """
        if self.current_token.type == expected_token_type:
            self.current_token = self.lexer.get_next_token()  # Prejdeme na ďalší token
        else:
            raise SyntaxError(f"Syntaktická chyba: očakávaný token {expected_token_type}, "
                              f"získaný {self.current_token.type}")

    def regular(self):
        result = self.alternative()
        return result

    def alternative(self):
        result = self.sequence()
        while self.current_token.type == TokenType.PIPE:
            token = self.current_token
            self.consume(TokenType.PIPE)
            result += self.sequence()
        return result

    def sequence(self):
        result = self.element()
        while self.current_token.type == TokenType.SYMBOL:

    def element(self):
        pass

    def E(self):
        """
        Implementuje gramatické pravidlo:
        E ::= T {("+" | "-") T}

        Spracuje sčítanie a odčítanie s ľavou asociativitou.
        Najnižšia priorita operácií v gramatike.

        """
        # Najprv vyhodnotíme prvé F
        result = self.T()

        # Potom spracujeme všetky ďalšie operácie sčítania a odčítania
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token

            if token.type == TokenType.PLUS:
                self.consume(TokenType.PLUS)  # Overíme a posunieme sa za '+'
                result += self.T()  # Vyhodnotíme hodnotu F a pripočítame ju do výsledku

            elif token.type == TokenType.MINUS:
                self.consume(TokenType.MINUS)  # Overíme a posunieme sa za '-'
                result -= self.T()  # Vyhodnotíme hodnotu F a odčítame ju od výsledku

        return result

    def T(self):
        """
        Implementuje gramatické pravidlo:
        T ::= F {"*" F}
        """

        result = self.F()

        while self.current_token.type == TokenType.MULTIPLY:
            self.consume(TokenType.MULTIPLY)
            result *= self.F()

        return result

    def F(self):
        """
        TODO: Implementujte gramatické pravidlo:
        F ::= P ["^" F]
        """

        result = self.P()

        if self.current_token.type == TokenType.POWER:
            self.consume(TokenType.POWER)  # Overíme a posunieme sa za '+'
            result = pow(result, self.F())  # Vyhodnotíme hodnotu F a pripočítame ju do výsledku

        return result

    def P(self):
        """
        Implementuje gramatické pravidlo:
        P ::= ["-"] cislo | "(" E ")"

        Spracuje základné prvky výrazu - buď číslo alebo výraz v zátvorke.
        Najvyššia priorita v gramatike.
        """
        token = self.current_token
        if token.type == TokenType.MINUS:
            self.consume(TokenType.MINUS)
            token = self.current_token
            self.consume(TokenType.NUMBER)
            return -1 * token.attribute

        if token.type == TokenType.NUMBER:
            # Jednoducho vrátime hodnotu čísla
            self.consume(TokenType.NUMBER)  # Overíme a posunieme sa za číslo
            return token.attribute

        if token.type == TokenType.LPAREN:
            # Vyhodnotíme výraz v zátvorkách
            self.consume(TokenType.LPAREN)  # Overíme a posunieme sa za '('
            result = self.E()  # Rekurzívne vyhodnotíme výraz medzi zátvorkami
            self.consume(TokenType.RPAREN)  # Overíme a posunieme sa za ')'
            return result

        else:
            # Ak nie je ani číslo ani zátvorka, ide o chybu
            raise SyntaxError(f"Syntaktická chyba: Neočakávaný token {token}")

    def parse(self):
        """
        Začne syntaktickú analýzu a vráti výsledok výrazu.
        Vstupný bod pre parser.
        """
        return self.E()  # Začíname volaním funkcie zopdovedajúcej zažiatočnému symbolu gramatiky
