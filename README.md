# Troll

## *Designed to hurt you*

### Syntax

> Tokens are seperated by spaces or newlines \
> Comments begin with '#'

```brainfuck
# hello world program
troll
"Hello World!" 
TROLL
```

- `troll` Marks beginning of program
- `TROLL` Marks end of prorgam (lexer stops here)
- `Troll identifier` sets label
- `trolL identifier` goes to label (--> goto)
- `TrolL` exits program
- `trOll` outputs top of stack
- `"..."` Prints out a string
- `identifier number` defines variable
- `number` pushes constant onto stack
- `+` adds two operands together and pushes result onto stack (soon: `- / *`)
- `^` top of the stack (does not works as first operand lol)

```python
troll 

a 1         # a = 1
1           # push 1
a + ^       # push a + top of stack
trOll       # put top of stack

TROLL 
```