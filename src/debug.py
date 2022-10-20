def debugDict(ast: dict) -> None:
    stmts = ast["stmts"]
    
    for _, stmt in enumerate(stmts):
        print("\n|    ", end=" ")
        for arg in stmt:
            print(arg, end=" ")

def debugAST(ast: dict) -> None:
    name = ast["name"]
    stmts = ast["stmts"]
    
    print("----", name, "----")
    for i, stmt in enumerate(stmts):
        print(i, end=" ")
        for arg in stmt:
            if type(arg) is dict:
                debugDict(arg)
            else:
                print(arg, end=" ")
        print()
    print("-"*(len(name)+10), end="\n\n")