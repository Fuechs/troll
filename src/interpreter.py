from typing import Any
from error import TrollResult
from parser import StackTop, String, Number

class Interpreter:

    def __init__(self, ast: dict) -> None:
        self.ast = ast
        self.stmts = ast["stmts"]
        self.idx = 0
        self.vmap: dict[str, int] = {} # variable map
        self.lmap: dict[str, int] = {} # label map
        self.stack: list[int] = []
        
    def cur(self) -> list[str, String|Number|Any]:
        return self.stmts[self.idx]
    
    def adv(self, steps: int = 1) -> None:
        if self.idx < len(self.stmts):
            self.idx += steps
    
    def interpret(self) -> TrollResult:
        
        while self.idx < len(self.stmts):
                    
            if self.cur()[0] == "put":
                if isinstance(self.cur()[1], String):
                    print(self.cur()[1].value)
                elif isinstance(self.cur()[1], StackTop):
                    print(self.stack.pop())
                self.adv()
            
            elif self.cur()[0] == "lab":
                self.lmap[self.cur()[1].value] = self.idx
                self.adv()
            
            elif self.cur()[0] == "jmp":
                label = self.cur()[1].value
                if label in self.lmap:
                    self.idx = self.lmap[label]
                else:
                    return TrollResult(False, "unknown jump location "+label)
                                
            elif self.cur()[0] == "hlt":
                break
            
            elif self.cur()[0] == "def":
                name = self.cur()[1].value
                value = self.cur()[2].value
                self.vmap[name] = value
                self.adv()
            
            elif self.cur()[0] == "psh":
                self.stack.append(self.cur()[1].value)
                self.adv()
                
            elif self.cur()[0] == "add":
                op1 = self.cur()[1]
                if isinstance(op1, String):
                    op1 = self.vmap[op1.value]
                elif isinstance(op1, Number):
                    op1 = op1.value
                elif isinstance(op1, StackTop):
                    op1 = self.stack.pop()
                    
                op2 = self.cur()[2]
                if isinstance(op2, String):
                    op2 = self.vmap[op2.value]
                elif isinstance(op2, Number):
                    op2 = op2.value
                elif isinstance(op2, StackTop):
                    op2 = self.stack.pop()
                
                self.stack.append(op1+op2)
                self.adv()

                                
            else:
                return TrollResult(False, "unknown statement "+str(self.cur()))                
        
        return TrollResult()