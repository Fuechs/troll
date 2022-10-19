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
        
    def __str__(self) -> str:
        return f"<Token, {self.type}, '{self.lexeme}'>"
    
    def __repr__(self) -> str:
        return str(self)

    
class Lexer:
    
    def __init__(self, source: str = None) -> None:
        if source.endswith("\n"):
            self.source = source
        else:
            self.source = source+"\n"
            # workaround for advancing
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
    
    def lex_num(self) -> str:
        lexeme = ""
        while not self.cur().isspace() and self.cur().isdecimal():
            lexeme += self.cur()
            self.adv()
        return lexeme
            
    def lex_op(self) -> tuple[str, TrollResult]:
        
        if self.cur() in "+-/*^":
            op = self.cur()
            self.adv()
            return op, TrollResult()
        else:
            return "", TrollResult(False, "unknown operator "+self.cur())
            
    
    def lex(self) -> tuple[list[Token], TrollResult]:
        
        tokens = []
        lexeme = ""
        result = TrollResult()
        
        while self.idx < len(self.source) - 1:
            
            if self.cur() in self.ident_incl:
                lexeme = self.lex_ident()
                tokens.append(Token(IDENTIFIER, lexeme))
                if lexeme == "TROLL":
                    break
                
            elif self.cur() == '"':
                lexeme = self.lex_str()
                tokens.append(Token(STRING, lexeme))
                
            elif self.cur().isspace():
                self.adv()
                
            elif self.cur().isdigit():
                lexeme = self.lex_num()
                tokens.append(Token(NUMBER, lexeme))
                
            elif self.cur() == '#':
                while self.cur() != '\n':
                    self.adv()
                self.adv()
                
            else:
                lexeme, result = self.lex_op()
                if result.success is False:
                    return tokens, result
                tokens.append(Token(OPERATOR, lexeme))
                
        
        return tokens, result
        