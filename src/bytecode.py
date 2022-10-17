from error import TrollResult

class Optimizer:
    
    def __init__(self, ast: dict) -> None:
        self.ast = ast
        self.idx = 0
        
    def optimize(self) -> tuple[dict, TrollResult]:
        self.ast["name"] = "ast (opt)"
        return self.ast, TrollResult()
    
OP_HALT  = 0x0
OP_PUTS  = 0x1
OP_LABEL = 0x2
OP_JUMP  = 0x3


def debugBytecode(bytecode: list[hex]) -> None:
    idx = 0
    print("-- Chunk --")
    
    def cur() -> int:
        nonlocal idx
        return bytecode[idx]
    
    def adv() -> None:
        nonlocal idx
        if idx < len(bytecode):
            idx += 1
            
    while idx < len(bytecode):
        
        if cur() == OP_HALT:
            adv()
            print(idx, "OP_HALT")
            
        elif cur() == OP_PUTS:
            adv()
            print(idx, "OP_PUTS")
            data = cur().to_bytes(cur().bit_length(), "little")
            print("|    ", data.decode("utf-8"))
            adv()
        
        elif cur() == OP_LABEL:
            adv()
            print(idx, "OP_LABEL")
            data = cur().to_bytes(cur().bit_length(), "little")
            print("|    ", data.decode("utf-8"))
            adv()
        
        elif cur() == OP_JUMP:
            adv()
            print(idx, "OP_JUMP")
            data = cur().to_bytes(cur().bit_length(), "little")
            print("|    ", data.decode("utf-8"))
            adv()

        else:
            adv()
            print(idx, "UNKNOWN")
    
class Generator:
    
    def __init__(self, ast: dict) -> None:
        self.ast = ast
        self.bytecode = []
        self.idx = 0
        
    def cur(self) -> list:
        return self.ast["statements"][self.idx]

    def adv(self) -> None:
        if self.idx < len(self.ast["statements"]):
            self.idx += 1
        
    def generate(self) -> tuple[list[hex], TrollResult]:
        
        while self.idx < len(self.ast["statements"]):
                        
            if self.cur()[0] == "lab":
                self.bytecode.append(OP_LABEL)
                raw_data = self.cur()[1].value
                data = int.from_bytes(raw_data.encode("utf-8"), "little")
                self.bytecode.append(data)
                self.adv()
            
            elif self.cur()[0] == "jmp":
                self.bytecode.append(OP_JUMP)
                raw_data = self.cur()[1].value
                data = int.from_bytes(raw_data.encode("utf-8"), "little")
                self.bytecode.append(data)
                self.adv()
                
            elif self.cur()[0] == "put":
                self.bytecode.append(OP_PUTS)
                raw_data = self.cur()[1].value
                data = int.from_bytes(raw_data.encode("utf-8"), "little")
                self.bytecode.append(data)
                self.adv()
                
            else:
                return [], TrollResult(False)
        
        self.bytecode.append(OP_HALT)
                
        return self.bytecode, TrollResult()