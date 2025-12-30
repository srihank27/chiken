# chiken.py
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
import textwrap

if __name__ == "__main__":
    # Test new features
    code = textwrap.dedent("""
        # String concatenation
        have greeting = "Hello, "
        have name = "ChIkEn"
        say greeting + name
        
        # Arithmetic with *, /, %
        say 10 * 5
        say 20 / 4
        say 17 % 5
        
        # Custom function
        func add_numbers(a, b) {
            have result = a + b
            return result
        }
        
        say add_numbers(7, 3)
        
        # Factorial function
        func factorial(n) {
            if (n <= 1) {
                return 1
            } else {
                return n * factorial(n - 1)
            }
        }
        
        say factorial(5)
    """)

    # Lexing
    lexer = Lexer(code)

    # Parsing
    parser = Parser(lexer)
    statements = parser.parse()

    # Interpreting
    interpreter = Interpreter()
    for stmt in statements:
        interpreter.visit(stmt)