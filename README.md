# ChIkEn Programming Language

A simple, beginner-friendly programming language for learning and building things.

## Features

- **Easy Syntax**: Intuitive keywords like `have`, `say`, `repeat`, `if`, `func`
- **Data Types**: Numbers, strings, and booleans
- **Functions**: Define and call reusable functions with parameters
- **Control Flow**: If/else statements and repeat loops
- **Operators**: Full arithmetic, comparison, and boolean operators
- **Built-in Math**: Functions like `sqrt`, `abs`, `max`, `min`, etc.
- **Comments**: Support for code documentation

## Installation

```bash
pip install chiken-lang
```

Or from source:

```bash
git clone https://github.com/yourusername/chiken.git
cd chiken
pip install -e .
```

## Quick Start

### Create a file: `hello.chiken`

```
have name = "World"
say "Hello, " + name
```

### Run it:

```bash
chiken hello.chiken
```

## Language Guide

### Variables

```
have x = 5
have greeting = "Hello"
have pi = 3.14
```

### Output

```
say "Hello, World"
say x
say x + 10
```

### Arithmetic

```
say 10 + 5        # 15
say 10 - 3        # 7
say 4 * 5         # 20
say 20 / 4        # 5
say 17 % 5        # 2
```

### Comparisons

```
have x = 10
if (x > 5) { say "Greater" }
if (x == 10) { say "Equal" }
if (x != 0) { say "Not zero" }
```

### Boolean Logic

```
if (x > 5 and x < 20) {
  say "Between 5 and 20"
}

if (age < 18 or age > 65) {
  say "Not working age"
}

if (not (x == 0)) {
  say "Not zero"
}
```

### Loops

```
have i = 1
repeat (i <= 5) {
  say i
  have i = i + 1
}
```

### Functions

```
func greet(name) {
  say "Hello, " + name
}

greet("Alice")
```

### Return Values

```
func add(a, b) {
  have result = a + b
  return result
}

have sum = add(5, 3)
say sum  # 8
```

### Recursion

```
func factorial(n) {
  if (n <= 1) {
    return 1
  } else {
    return n * factorial(n - 1)
  }
}

say factorial(5)  # 120
```

### Comments

```
# This is a comment
have x = 5  # Inline comment
```

## Built-in Functions

- **Math**: `add`, `sub`, `mul`, `div`, `pow`, `sqrt`, `abs`, `min`, `max`
- **String**: Concatenation with `+`

## Examples

### Calculator

```
func calculate(a, b, op) {
  if (op == "add") {
    return add(a, b)
  } else if (op == "mul") {
    return multiply(a, b)
  } else {
    return 0
  }
}

say calculate(10, 5, "add")   # 15
say calculate(10, 5, "mul")   # 50
```

### Fibonacci

```
func fib(n) {
  if (n <= 1) {
    return n
  } else {
    return fib(n - 1) + fib(n - 2)
  }
}

have i = 0
repeat (i < 10) {
  say fib(i)
  have i = i + 1
}
```

### Check Prime

```
func is_prime(n) {
  if (n <= 1) {
    return 0
  }
  have i = 2
  repeat (i * i <= n) {
    if (n % i == 0) {
      return 0
    }
    have i = i + 1
  }
  return 1
}

have num = 17
if (is_prime(num)) {
  say "Prime"
} else {
  say "Not prime"
}
```

## Project Structure

```
chiken/
├── src/
│   ├── __init__.py
│   ├── lexer.py        # Tokenizer
│   ├── parser.py       # AST builder
│   ├── nodes.py        # AST node definitions
│   ├── interpreter.py  # Evaluator
│   └── errors.py       # Error handling
├── chiken/
│   ├── __init__.py
│   └── cli.py          # Command-line interface
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   └── test_interpreter.py
├── examples/
│   ├── hello.chiken
│   ├── factorial.chiken
│   └── fibonacci.chiken
├── setup.py
└── README.md
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## Author

Your Name

## Support

For issues and questions, please open an issue on GitHub.
