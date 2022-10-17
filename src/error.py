# from colorama import Fore as color

class TrollResult:
    
    def __init__(self, success: bool = True) -> None:
        self.success = success
    
    def __repr__(self) -> str:
        if self.success is False:
            return "[Error]: interpretation failed."
        else:
            return "Finished interpretation."