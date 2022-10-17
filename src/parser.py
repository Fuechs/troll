from typing import Any
from error import TrollResult
from lexer import Token, IDENTIFIER, STRING, NUMBER, OPERATOR

class Parser:
    
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.idx = 0
        
    def cur(self) -> Token:
        return self.tokens[self.idx]
        
    def peek(self, offset: int = 1) -> Token:
        if self.idx+offset < self.tokens - 1:
            return self.tokens[self.idx + offset]
        return None
        
    def adv(self, steps: int = 1) -> None:
        for _ in range(steps):
            if self.idx < len(self.tokens) - 1:
                self.idx += 1
                
    def expect(self, lexeme: str) -> bool:
        comp = self.cur().lexeme == lexeme
        self.adv()
        return comp
    
    def parse(self) -> tuple[Any, TrollResult]:
        
        print("parsing:", self.tokens)
        
        if self.expect("troll") is False:
            return None, TrollResult(False)
        
        while self.idx < len(self.tokens) - 1:
            
            if self.cur().lexeme == "TROLL":
                break
            
            if self.cur().type == STRING:
                print(self.cur().lexeme) # testing for now
                # would be (put "Hello World!")
                self.adv()
        
        return None, TrollResult()