from colorama import Fore as c

class TrollResult:
    
    def __init__(self, success: bool = True, message: str = "missing") -> None:
        self.success = success
        self.message = message
    
    def __repr__(self) -> str:
        if self.success is False:
            return f"[{c.RED}Error{c.RESET}]: interpretation failed: "+self.message
        else:
            return "Finished interpretation."