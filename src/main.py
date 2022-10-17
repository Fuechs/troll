"""

    TROLL
    by Fuechs
    Copyright (c) 2022 Fuechs

"""

from subprocess import call
from sys import argv
from error import TrollResult
from lexer import Lexer, Token

clear = lambda: call("clear")
    
def main(argc: int, argv: list[str]) -> TrollResult:
    clear()
    argv.append("src/test/main.troll")
    res = None
    
    with open(argv[1], 'r') as file:
        content = file.readlines()
        
    lexer = Lexer(content)
    tokens, res = lexer.lex()
    print(tokens)
    
    if res.success is False: 
        return res

    # interpreter = Interpreter(tokens)
    
    return res


if __name__ == "__main__":
    print(main(len(argv), argv))