"""ChIkEn command-line interface"""

import sys
import argparse
from pathlib import Path

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

def main():
    """Main entry point for the chiken CLI"""
    parser = argparse.ArgumentParser(
        description="ChIkEn Programming Language interpreter",
        prog="chiken"
    )
    
    parser.add_argument(
        "file",
        nargs="?",
        help="ChIkEn source file to run (.chiken)"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    parser.add_argument(
        "-c", "--code",
        help="Run code directly from command line"
    )
    
    args = parser.parse_args()
    
    if args.code:
        # Run code from -c flag
        code = args.code
    elif args.file:
        # Run code from file
        try:
            with open(args.file, 'r') as f:
                code = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(0)
    
    try:
        lexer = Lexer(code)
        parser_obj = Parser(lexer)
        statements = parser_obj.parse()
        interpreter = Interpreter()
        
        for stmt in statements:
            interpreter.visit(stmt)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
