def debugAST(ast: dict) -> None:
    name = ast["name"]
    stmts = ast["stmts"]
    
    print("----", name, "----")
    for i, stmt in enumerate(stmts):
        print(i, end=" ")
        for arg in stmt:
            print(arg, end=" ")
        print()
    print("-"*(len(name)+10), end="\n\n")