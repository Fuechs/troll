"""

    TROLL - Designed to hurt you
    Copyright (c) 2022 Fuechs

"""

from subprocess import call
from sys import argv
from error import TrollResult
from lexer import Lexer, Token
from parser import Parser, debugAST
from interpreter import Interpreter
from optimizer import Optimizer

clear = lambda: call("clear")
    
def main(argc: int, argv: list[str]) -> TrollResult:
    clear()
    argv.append("src/test/main.troll")
    res = None
    
    with open(argv[1], 'r') as file:
        content = file.read()
        
    lexer = Lexer(content)
    tokens, res = lexer.lex()
        
    if res.success is False: 
        return res

    parser = Parser(tokens)
    ast, res = parser.parse()
    
    if res.success is False:
        return res
    
    # debugAST(ast)
            
    optimizer = Optimizer(ast)
    ast, res = optimizer.optimize()
    
    if res.success is False:
        return res
    
    # debugAST(ast)
    
    interpreter = Interpreter(ast);
    res = interpreter.interpret()
    
    return res


if __name__ == "__main__":
    print('\n   ', main(len(argv), argv))