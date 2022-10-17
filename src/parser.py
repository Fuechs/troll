from typing import Any
from error import TrollResult
from lexer import Token, IDENTIFIER, STRING, NUMBER, OPERATOR

KEY_START = "troll"
KEY_END = "TROLL"
KEY_LABEL = "Troll"
KEY_GOTO = "trolL"

def debugAST(ast: dict) -> None:
    name = ast["name"]
    stmts = ast["statements"]
    
    print("---", name, "---")
    for count, stmt in enumerate(stmts):
        print(count, end=" ")
        for arg in stmt:
            print(arg, end=" ")
        print()
        
class String:
    def __init__(self, value: str) -> None:
        self.value = value
        
    def __repr__(self) -> str:
        return f"'{self.value}'"

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
    
    def parse(self) -> tuple[dict[Any, Any], TrollResult]:
        
        ast = {"name": "root", "statements": []}
                        
        if self.expect(KEY_START) is False:
            return None, TrollResult(False)
        
        while self.idx < len(self.tokens) - 1:
            
            if self.cur().lexeme == KEY_END:
                break
            
            elif self.cur().type == STRING:
                ast["statements"].append(["put", String(self.cur().lexeme)])
                self.adv()
                
            elif self.cur().lexeme == KEY_LABEL:
                self.adv()
                ast["statements"].append(["lab", String(self.cur().lexeme)])
                self.adv()
            
            elif self.cur().lexeme == KEY_GOTO:
                self.adv()
                ast["statements"].append(["jmp", String(self.cur().lexeme)])
                self.adv()
                        
        return ast, TrollResult()