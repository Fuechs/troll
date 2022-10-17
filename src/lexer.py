from error import TrollResult
from string import ascii_letters

IDENTIFIER  = "Identifier"
OPERATOR    = "Operator"
STRING      = "String"
NUMBER      = "Number"
EOF         = "EOF"

class Token:
    def __init__(self, type: str = None, lexeme: str = None) -> None:
        self.type = type
        self.lexeme = lexeme
    
    def __repr__(self) -> str:
        return f"<Token, {self.type}, '{self.lexeme}'>"
    
class Lexer:
    
    def __init__(self, source: str = None) -> None:
        self.source = source
        self.line = 0
        self.col = 0
        
    def current(self) -> str:
        return self.source[self.line][self.col]

    def advance(self, steps: int = 1) -> None:
        for _ in range(steps):
            if self.current() == "\n":
                self.line += 1
                self.col = 0
                return
            self.col += 1
        
    def lex_ident(self) -> str:
        lexeme = self.current()
        self.advance()
        while not self.current().isspace():
            lexeme += self.current()
            self.advance()
        return lexeme
    
    def lex(self) -> tuple[list[Token], TrollResult]:
        
        tokens = []
        ident_incl = ascii_letters+"_"
        lexeme = ""
        result = TrollResult()
        
        while True:
                    
            if not self.source:
                return tokens, TrollResult(False)
                
            if self.current() in ident_incl:
                lexeme = self.lex_ident()
                tokens.append(Token(IDENTIFIER, lexeme))
                
            elif self.current().isdecimal():
                #lexeme = self.lex_num()
                pass
            
            elif self.current() == '"':
                #lexeme = self.lex_str()
                pass
            
            elif self.current() in ['\n', ' ', '\t']:
                if self.current() == '\n':
                    self.line += 1
                    self.col = 0
                else:
                    self.col += 1
                
            else:
                tokens.append(Token(OPERATOR, self.current()))
                self.advance()
                
            if self.line+1 == len(self.source) and self.col+1 == len(self.source[self.line]):
                # check if end of file was reached
                tokens.append(Token(EOF, "EOF"))
                break
        
        return tokens, TrollResult()
        