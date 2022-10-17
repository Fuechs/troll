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
- `TROLL` Marks end of prorgam
- `"..."` Prints out a string

###### soon

- `Troll identifier` sets label
- `trolL identifier` goes to label (--> goto)


```brainfuck
Troll loop
"SPAM"
trolL loop
```

- `identifier integer` defines variable
- `integer` pushes constant onto stack
- `+` adds two operands together and pushes result onto stack (also available: `- / *`)
- `^` returns top of the stack

```brainfuck
a 1
1
a + ^
# top of stack: 2
a 2 
a * ^
# top of stack: 4
```