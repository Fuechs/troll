from error import TrollResult
from parser import String, Number, StackTop
from typing import Any

class Optimizer: 
    
    def __init__(self, ast: dict[str, list]) -> None:
        self.ast = ast
        self.stmts = ast["stmts"]
        self.idx = 0
        self.insert = False
        
    def cur(self) -> list[str, String|Number|Any]:
        return self.stmts[self.idx]

    def peek(self, offset: int = 1) -> list[str, String|Number|Any]:
        if self.idx+offset < len(self.stmts):
            return self.stmts[self.idx+offset]
        return None
    
    def adv(self, steps: int = 1) -> None:
        if self.idx < len(self.stmts):
            self.idx += steps

    def optimize(self) -> tuple[dict[str, list], TrollResult]:
        self.ast["name"] = self.ast["name"]+" (optimized)"
        
        while self.idx < len(self.stmts):
            
            if self.cur()[0] == "psh": 
                """
                replace
                    (psh x)
                    (BOP Any|StackTop Any|StackTop)
                with
                    (BOP Any|x Any|x) 
                """
                # if self.peek()[0] in ["add", "sub", "mul", "div"]:
                #     if isinstance(self.peek()[1], StackTop):
                #         self.peek()[1] = self.cur()[1]
                #         self.insert = True
                #     if isinstance(self.peek()[2], StackTop):
                #         self.peek()[2] = self.cur()[1]
                #         self.insert = True
                #     if self.insert is True:
                #         self.insert = False
                #         del self.stmts[self.idx]
                
                # ! breaks loops that increment
                        
            elif self.cur()[0] == "put":
                """
                replace
                    (put String(x))
                    (put String(y))
                with
                    (put String(x+y))
                """
                while self.peek() is not None and self.peek()[0] == "put":
                    if (isinstance(self.cur()[1], String)
                    and isinstance(self.peek()[1], String)):
                        self.stmts[self.idx][1] = String(self.cur()[1].value + self.peek()[1].value)
                        del self.stmts[self.idx+1]
                    else:
                        break
                
                                 
            self.adv()
        
        self.ast["stmts"] = self.stmts
        return self.ast, TrollResult()