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
    
    """
    checks arg for instance and returns value
    """
    def get_inst(self, arg: String|Number|StackTop) -> Any:
        if (isinstance(arg, String)):
            arg = self.vmap[arg.value]
        elif (isinstance(arg, Number)):
            arg = arg.value
        elif (isinstance(arg, StackTop)):
            arg = self.stack.pop()
        return arg
    
    def interpret(self) -> TrollResult:
        
        while self.idx < len(self.stmts):
                    
            if self.cur()[0] == "put":
                if isinstance(self.cur()[1], String):
                    print(self.cur()[1].value.replace("\\n", "\n"), end="")
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
                
            elif self.cur()[0] in ["add", "sub", "mul", "div"]:
                
                op = self.cur()[0]
                op1 = self.get_inst(self.cur()[1])            
                op2 = self.get_inst(self.cur()[2])
                
                if op == "add":     res = op2+op1
                elif op == "sub":   res = op2-op1
                elif op == "mul":   res = op2*op1
                elif op == "div":   res = op2//op1
                
                self.stack.append(res)
                self.adv()

                                
            else:
                return TrollResult(False, "unknown statement "+str(self.cur()))                
        
        return TrollResult()