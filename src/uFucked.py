import sys

def string_with_arrows(text, pos_start, pos_end):
    result = ""

    idx_start = max(text.rfind("\n", 0, pos_start.idx), 0)
    idx_end = text.find("\n", idx_start + 1)
    if idx_end < 0: idx_end = len(text)
    
    line_count = pos_end.ln - pos_start.ln + 1
    for i in range(line_count):
        line = text[idx_start:idx_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1

        result += line + "\n"
        result += " " * col_start + "^" * (col_end - col_start)

        idx_start = idx_end
        idx_end = text.find("\n", idx_start + 1)
        if idx_end < 0: idx_end = len(text)

    return result.replace("\t", "")

### Errors

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f"{self.error_name}: {self.details}\n"
        result += f"File {self.pos_start.fn}, line {self.pos_start.ln + 1}"
        result += "\n\n" + \
            string_with_arrows(self.pos_start.ftxt,
                               self.pos_start, self.pos_end)
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)

### Token Types

T_ADV = "ADV"
T_PLUS = "PLUS"
T_EQ = "EQ"

### Position

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

### Token Maker

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"

### Lexer

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char == ">":
                tokens.append(Token(T_ADV, pos_start=self.pos))
                self.advance()
            elif self.current_char == "+":
                tokens.append(Token(T_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == "=":
                tokens.append(Token(T_EQ, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None

### Translator

class Translate:
    def __init__(self, tokens):
        self.tokens = tokens
        self.translated = []
    
    def translate(self):
        c = 0
        for i in self.tokens:
            if i.matches(T_ADV, None):
                c += 1
            if i.matches(T_PLUS, None):
                try:
                    self.translated.append(chr(c))
                    c = 0
                except Exception as e:
                    print(e)
                    sys.exit()
            if i.matches(T_EQ, None):
                print("".join(self.translated))

if __name__ == "__main__":
    while True:
        if len(sys.argv) == 2:
            f = open(sys.argv[1], "r")
            code = f.read()
            f.close()
            lexer = Lexer(sys.argv[1], code)
            tokens, error = lexer.make_tokens()
            if error: print(error.as_string())
            else: Translate(tokens).translate()
            break
        else:
            code = input("uF - ")
            lexer = Lexer("<stdin>", code)
            tokens, error = lexer.make_tokens()
            if error: print(error.as_string())
            else: Translate(tokens).translate()