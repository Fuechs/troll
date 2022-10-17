"""

    TROLL
    by Fuechs
    Copyright (c) 2022 Fuechs

"""

from subprocess import call
from sys import argv
from bytecode import Optimizer, Generator, debugBytecode
from error import TrollResult
from lexer import Lexer, Token
from parser import Parser, debugAST
from pickle import dump

clear = lambda: call("clear")
    
def main(argc: int, argv: list[str]) -> TrollResult:
    clear()
    argv.append("src/test/main.troll")
    res = None
    
    with open(argv[1], 'r') as file:
        content = file.read()
        
    lexer = Lexer(content)
    tokens, res = lexer.lex()
    # print(tokens)
    
    if res.success is False: 
        return res

    parser = Parser(tokens)
    ast, res = parser.parse()
    
    if res.success is False:
        return res
    
    # debugAST(ast)
    
    # nothing to optimize here yet
    
    # optimizer = Optimizer(ast)
    # ast, res = optimizer.optimize()
    
    # if res.success is False:
    #     return res
    
    # debugAST(ast)
    
    generator = Generator(ast)
    code, res = generator.generate()
    
    debugBytecode(code)
        
    with open("out.bin", "wb") as outb:
        dump(code, outb)
    
    if res.success is False:
        return res
    
    
    # interpret ...
    
    return res


if __name__ == "__main__":
    print(main(len(argv), argv))