class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return f"Token({self.type}:{self.value})"
        return f"Token({self.type})"


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[0] if text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        # Skip comment until end of line
        while self.current_char and self.current_char != "\n":
            self.advance()

    def string(self, quote_char):
        result = ""
        self.advance()  # skip opening quote
        while self.current_char and self.current_char != quote_char:
            if self.current_char == "\\":
                self.advance()
                if self.current_char == "n":
                    result += "\n"
                elif self.current_char == "t":
                    result += "\t"
                elif self.current_char == "\\":
                    result += "\\"
                elif self.current_char == quote_char:
                    result += quote_char
                else:
                    result += self.current_char
                self.advance()
            else:
                result += self.current_char
                self.advance()
        
        if self.current_char == quote_char:
            self.advance()  # skip closing quote
        else:
            raise Exception("Unterminated string")
        
        return Token("STRING", result)

    def number(self):
        result = ""
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token("NUMBER", int(result))

    def identifier(self):
        result = ""
        while self.current_char and (self.current_char.isalnum() or self.current_char == "_"):
            result += self.current_char
            self.advance()

        if result == "have":
            return Token("HAVE")
        if result == "say":
            return Token("SAY")
        if result == "if":
            return Token("IF")
        if result == "else":
            return Token("ELSE")
        if result == "repeat":
            return Token("REPEAT")
        if result == "and":
            return Token("AND")
        if result == "or":
            return Token("OR")
        if result == "not":
            return Token("NOT")
        if result == "func":
            return Token("FUNC")
        if result == "return":
            return Token("RETURN")

        return Token("IDENTIFIER", result)

    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char == "#":
                self.skip_comment()
                continue
            if self.current_char == '"':
                return self.string('"')
            if self.current_char == "'":
                return self.string("'")
            if self.current_char.isdigit():
                return self.number()
            if self.current_char.isalpha() or self.current_char == "_":
                return self.identifier()
            if self.current_char == "+":
                self.advance()
                return Token("PLUS")
            if self.current_char == "-":
                self.advance()
                return Token("MINUS")
            if self.current_char == "*":
                self.advance()
                return Token("MUL")
            if self.current_char == "/":
                self.advance()
                return Token("DIV")
            if self.current_char == "%":
                self.advance()
                return Token("MOD")
            if self.current_char == "(":
                self.advance()
                return Token("LPAREN")
            if self.current_char == ")":
                self.advance()
                return Token("RPAREN")
            if self.current_char == ",":
                self.advance()
                return Token("COMMA")
            if self.current_char == "{":
                self.advance()
                return Token("LBRACE")
            if self.current_char == "}":
                self.advance()
                return Token("RBRACE")
            if self.current_char == ">":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token("GTE")
                return Token("GT")
            if self.current_char == "<":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token("LTE")
                return Token("LT")
            if self.current_char == "=":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token("EQ")
                return Token("EQUALS")
            if self.current_char == "!":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token("NEQ")
                raise Exception(f"Invalid character: !")
            raise Exception(f"Invalid character: {self.current_char}")

        return Token("EOF")
