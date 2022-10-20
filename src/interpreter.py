from typing import Any
from error import TrollResult
from parser import StackTop, String, Number
from time import sleep

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
        for _ in range(steps):
            if self.idx+1 < len(self.stmts):
                self.idx += 1
    
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
    
    def interpret(self, once: bool = False) -> TrollResult:
        
        # old_idx = -1
        
        while self.idx < len(self.stmts):
            
            # if self.idx == old_idx: break
            # old_idx = self.idx
                    
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
                    del label
                    self.adv()
                else:
                    return TrollResult(False, "unknown jump location "+label)
                                
            elif self.cur()[0] == "hlt":
                return TrollResult(False, "__if__break__")
            
            elif self.cur()[0] == "def":
                name = self.cur()[1].value
                value = self.cur()[2].value
                self.vmap[name] = value
                del name, value
                self.adv()
            
            elif self.cur()[0] == "psh":
                value = self.get_inst(self.cur()[1])
                self.stack.append(value)
                del value
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
                del op, op1, op2, res
                self.adv()

            elif self.cur()[0] == "equ":
                
                left = self.get_inst(self.cur()[1])
                right = self.get_inst(self.cur()[2])
                
                if left == right:
                    _stmts, _idx = self.stmts, self.idx
                    self.stmts, self.idx = self.cur()[3]["stmts"], 0
                    
                    result = self.interpret(True)
                    if result.message == "__if__break__":
                        break
                    elif result.success is False:
                        return result
                    
                    self.stmts, self.idx = _stmts, _idx
                    del _stmts, _idx
                
                del left, right
                
                self.adv()
                                
            else:
                return TrollResult(False, "unknown statement "+str(self.cur())) 
            
            if once is True:
                break
                
        return TrollResult()