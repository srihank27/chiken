"""ChIkEn Programming Language"""

__version__ = "1.0.0"
__author__ = "Your Name"

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

def run(code):
    """Run ChIkEn code and return output"""
    lexer = Lexer(code)
    parser = Parser(lexer)
    statements = parser.parse()
    interpreter = Interpreter()
    
    for stmt in statements:
        interpreter.visit(stmt)

__all__ = ["Lexer", "Parser", "Interpreter", "run"]
