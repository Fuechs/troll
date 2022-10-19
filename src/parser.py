from operator import truediv
from typing import Any
from error import TrollResult
from lexer import Token, IDENTIFIER, STRING, NUMBER, OPERATOR

KEY_START = "troll"
KEY_END = "TROLL"
KEY_LABEL = "Troll"
KEY_GOTO = "trolL"
KEY_EXIT = "TrolL"
KEY_TOP = "trOll"
KEY_WAIT = "tRoll"

def debugAST(ast: dict) -> None:
    name = ast["name"]
    stmts = ast["stmts"]
    
    print("---", name, "---")
    for count, stmt in enumerate(stmts):
        print(count, end=" ")
        for arg in stmt:
            print(arg, end=" ")
        print()
    print()
        
class String:
    def __init__(self, value: str) -> None:
        self.value: str = value
        
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
        self.ast = {"name": "root", "stmts": []}
        
    def cur(self) -> Token:
        return self.tokens[self.idx]
        
    # def peek(self, offset: int = 1) -> Token:
    #     if self.idx+offset < self.tokens - 1:
    #         return self.tokens[self.idx + offset]
    #     return None
        
    def adv(self, steps: int = 1) -> None:
        for _ in range(steps):
            if self.idx+1 < len(self.tokens):
                self.idx += 1
    
    def back(self, steps: int = 1) -> None:
        for _ in range(steps):
            if self.idx - 1 >= 0:
                self.idx -= 1
                
    # def expect(self, lexeme: str) -> bool:
    #     comp = self.cur().lexeme == lexeme
    #     self.adv()
    #     return comp
    
    def parse_def(self) -> bool:
        name = self.cur().lexeme
        self.adv()
        if self.cur().type == NUMBER:
            val = self.cur().lexeme
            self.adv()
            # (def String Number)
            self.ast["stmts"].append(["def", String(name), Number(val)])
            return True
        self.back()
        return False
    
    def parse_operand(self) -> String|Number|StackTop|TrollResult:
        if self.cur().type == NUMBER:
            operand = Number(self.cur().lexeme)
        elif self.cur().type in [STRING, IDENTIFIER]:
            operand = String(self.cur().lexeme)
        elif self.cur().lexeme == "^":
            operand = StackTop()
        else:
            operand = TrollResult(False, "invalid expression operand "+str(self.cur()))
        self.adv()
        return operand
    
    def parse_operation(self) -> str:
        op = self.cur().lexeme
        
        if op == '+':   op = "add"
        elif op == '-': op = "sub"
        elif op == '*': op = "mul"
        elif op == '/': op = "div"
        else:           return None
        
        self.adv()
        return op

    def parse_expr(self) -> bool:
        op1 = self.parse_operand()
        if (isinstance(op1, TrollResult)): 
            print(op1)
            exit()
            
        op = self.parse_operation()
        if op is None: 
            self.back()
            return False
        
        op2 = self.parse_operand()
        if (isinstance(op2, TrollResult)):
            print(op2)
            exit()
        
        # (op op1 op2)
        self.ast["stmts"].append([op, op1, op2])
        return True
        
    def parse_push(self) -> bool:
        item = self.parse_operand()
        # (psh item)
        self.ast["stmts"].append(["psh", item])
        return True

    def parse(self) -> tuple[dict[Any, Any], TrollResult]:
                                
        if self.cur().lexeme != KEY_START:
            return None, TrollResult(False, "missing troll to start program")
        self.adv()
        
        while self.idx < len(self.tokens) - 1:
            
            if self.cur().lexeme == KEY_END:
                break
            
            elif self.cur().type == STRING:
                # (put String)
                self.ast["stmts"].append(["put", String(self.cur().lexeme)])
                self.adv()
                
            elif self.cur().type == NUMBER:
                if (not self.parse_expr() 
                and not self.parse_push()):   
                    return None, TrollResult(False, "random number")
                
            elif self.cur().lexeme == KEY_LABEL:
                self.adv()
                # (lab String)
                self.ast["stmts"].append(["lab", String(self.cur().lexeme)])
                self.adv()
            
            elif self.cur().lexeme == KEY_GOTO:
                self.adv()
                # (jmp String)
                self.ast["stmts"].append(["jmp", String(self.cur().lexeme)])
                self.adv()
                
            elif self.cur().lexeme == KEY_EXIT:
                self.adv()
                # (hlt)
                self.ast["stmts"].append(["hlt"])
                
            elif self.cur().lexeme == KEY_TOP:
                self.adv()
                # (put StackTop)
                self.ast["stmts"].append(["put", StackTop()])
                self.adv()
                
            elif self.cur().lexeme == KEY_WAIT:
                self.adv()
                if self.cur().type != NUMBER:
                    return None, TrollResult(False, "invalid number of seconds to wait")
                # (hlt Number)
                self.ast["stmts"].append(["hlt", Number(self.cur().lexeme)])
                self.adv()
                
            elif self.cur().type == IDENTIFIER:
                if (not self.parse_def() 
                and not self.parse_expr() 
                and not self.parse_push()):     
                    return None, TrollResult(False, "random identifier")  
            
            else:
                return None, TrollResult(False, "unknown token "+str(self.cur()))
                
                        
        return self.ast, TrollResult()