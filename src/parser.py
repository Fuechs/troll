from typing import Any
from error import TrollResult
from lexer import Token, IDENTIFIER, STRING, NUMBER, OPERATOR

KEY_START = "troll"
KEY_END = "TROLL"
KEY_LABEL = "Troll"
KEY_GOTO = "trolL"
KEY_EXIT = "TrolL"
KEY_TOP = "trOll"

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
    
class Number:
    def __init__(self, value: int) -> None:
        self.value = int(value)
    
    def __repr__(self) -> str:
        return f"#{self.value}"
    
class StackTop:
    def __repr__(self) -> str:
        return f"^" 
    
class Parser:
    
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.idx = 0
        
    def cur(self) -> Token:
        return self.tokens[self.idx]
        
    # def peek(self, offset: int = 1) -> Token:
    #     if self.idx+offset < self.tokens - 1:
    #         return self.tokens[self.idx + offset]
    #     return None
        
    def adv(self, steps: int = 1) -> None:
        for _ in range(steps):
            if self.idx < len(self.tokens) - 1:
                self.idx += 1
                
    # def expect(self, lexeme: str) -> bool:
    #     comp = self.cur().lexeme == lexeme
    #     self.adv()
    #     return comp
    
    def parse_operand(self) -> String|Number|StackTop:
        if self.cur().type == NUMBER:
            operand = Number(self.cur().lexeme)
        elif self.cur().type == STRING:
            operand = String(self.cur().lexeme)
        elif self.cur().lexeme == "^":
            operand = StackTop()
        self.adv()
        return operand
    
    def parse(self) -> tuple[dict[Any, Any], TrollResult]:
        
        ast = {"name": "root", "statements": []}
                        
        if self.cur().lexeme != KEY_START:
            return None, TrollResult(False, "missing troll to start program")
        self.adv()
        
        while self.idx < len(self.tokens) - 1:
            
            if self.cur().lexeme == KEY_END:
                break
            
            elif self.cur().type == STRING:
                # (put String)
                ast["statements"].append(["put", String(self.cur().lexeme)])
                self.adv()
                
            elif self.cur().type == NUMBER:
                # (psh Number)
                ast["statements"].append(["psh", Number(self.cur().lexeme)])
                self.adv()
                
            elif self.cur().lexeme == KEY_LABEL:
                self.adv()
                # (lab String)
                ast["statements"].append(["lab", String(self.cur().lexeme)])
                self.adv()
            
            elif self.cur().lexeme == KEY_GOTO:
                self.adv()
                # (jmp String)
                ast["statements"].append(["jmp", String(self.cur().lexeme)])
                self.adv()
                
            elif self.cur().lexeme == KEY_EXIT:
                self.adv()
                # (hlt)
                ast["statements"].append(["hlt"])
                
            elif self.cur().lexeme == KEY_TOP:
                self.adv()
                # (put StackTop)
                ast["statements"].append(["put", StackTop()])
                self.adv()
                
            elif self.cur().type == IDENTIFIER: # definition or expression
                name = self.cur().lexeme
                self.adv()
                if self.cur().type == NUMBER: # variable
                    val = self.cur().lexeme
                    self.adv()
                    # (def String Number)
                    ast["statements"].append(["def", String(name), Number(val)])
                elif self.cur().lexeme in "+-/*": # expression 
                    match self.cur().lexeme:
                        case '+': op = "add"
                        case '-': op = "sub"
                        case '/': op = "div"
                        case '*': op = "mul"
                    self.adv()
                    operand = self.parse_operand()
                    # (OP String OPERAND)
                    ast["statements"].append([op, String(name), operand])
            
            else: # could be variable definition
                if self.cur().type != IDENTIFIER:
                    return None, TrollResult(False, "not suitable type for variable name")
                name = self.cur().lexeme
                self.adv()
                if self.cur().type != NUMBER:
                    return None, TrollResult(False, "not suitable type for variable value")
                val = self.cur().lexeme
                self.adv()
                # (def String Number)
                ast["statements"].append(["def", String(name), Number(val)])
                
                        
        return ast, TrollResult()