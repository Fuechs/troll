from curses.ascii import isspace
from this import d
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
        self.idx = 0
        self.ident_incl = ascii_letters+"_"
        
    def cur(self) -> str:
        return self.source[self.idx]
    
    def adv(self, steps: int = 1) -> None:
        for _ in range(steps):
            if self.idx < len(self.source) - 1:
                self.idx += 1
    
    def lex_ident(self) -> str:
        lexeme = ""
        while not self.cur().isspace() and self.cur() in self.ident_incl:
            lexeme += self.cur()
            self.adv()
        self.adv()
        return lexeme
    
    def lex_str(self) -> str:
        lexeme = ""
        self.adv()
        while self.cur() != '"':
            lexeme += self.cur()
            self.adv()
        self.adv()
        return lexeme
    
    def lex_op(self) -> tuple[str, TrollResult]:
        
        if self.cur() in "+-/*^":
            return self.cur(), TrollResult()
        else:
            return "", TrollResult(False)
            
    
    def lex(self) -> tuple[list[Token], TrollResult]:
        
        tokens = []
        lexeme = ""
        result = TrollResult()
        
        while self.idx < len(self.source) - 1:
            
            if self.cur() in self.ident_incl:
                lexeme = self.lex_ident()
                tokens.append(Token(IDENTIFIER, lexeme))
                
            elif self.cur() == '"':
                lexeme = self.lex_str()
                tokens.append(Token(STRING, lexeme))
                
            elif self.cur().isspace():
                self.adv()
                
            else:
                lexeme, result = self.lex_op()
                if result.success is False:
                    return tokens, result
                tokens.append(Token(OPERATOR, lexeme))
                
        
        return tokens, result
        