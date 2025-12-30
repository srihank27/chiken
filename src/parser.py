from src.nodes import (
    NumberNode,
    StringNode,
    VarAccessNode,
    VarAssignNode,
    BinOpNode,
    UnaryOpNode,
    PrintNode,
    FunctionCallNode,
    ComparisonNode,
    IfNode,
    RepeatNode,
    FunctionDefNode,
    ReturnNode,
)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def advance(self):
        self.current_token = self.lexer.get_next_token()

    def parse(self):
        statements = []

        while self.current_token.type != "EOF":
            stmt = self.statement()
            statements.append(stmt)

        return statements

    def statement(self):
        if self.current_token.type == "HAVE":
            return self.var_assign()
        elif self.current_token.type == "SAY":
            return self.print_stmt()
        elif self.current_token.type == "IF":
            return self.if_stmt()
        elif self.current_token.type == "REPEAT":
            return self.repeat_stmt()
        elif self.current_token.type == "FUNC":
            return self.func_def()
        elif self.current_token.type == "RETURN":
            return self.return_stmt()
        else:
            raise Exception(f"Unexpected token: {self.current_token}")

    def var_assign(self):
        self.advance()  # skip HAVE

        if self.current_token.type != "IDENTIFIER":
            raise Exception("Expected variable name")

        var_name = self.current_token.value
        self.advance()

        if self.current_token.type != "EQUALS":
            raise Exception("Expected '='")

        self.advance()
        expr = self.expr()
        # After expr(), current_token points to the token after the expression
        # (e.g., SAY or EOF or a newline). No need to advance further.

        return VarAssignNode(var_name, expr)

    def print_stmt(self):
        self.advance()  # skip SAY
        expr = self.expr()
        # After expr(), current_token points to the token after the expression
        # (e.g., HAVE or EOF or a newline). No need to advance further.
        return PrintNode(expr)

    def if_stmt(self):
        self.advance()  # skip IF

        if self.current_token.type != "LPAREN":
            raise Exception("Expected '(' after 'if'")
        self.advance()  # skip LPAREN

        condition = self.expr()

        if self.current_token.type != "RPAREN":
            raise Exception("Expected ')' after condition")
        self.advance()  # skip RPAREN

        if self.current_token.type != "LBRACE":
            raise Exception("Expected '{' after condition")
        self.advance()  # skip LBRACE

        then_block = []
        while self.current_token.type != "RBRACE" and self.current_token.type != "EOF":
            then_block.append(self.statement())

        if self.current_token.type != "RBRACE":
            raise Exception("Expected '}' to close if block")
        self.advance()  # skip RBRACE

        else_block = None
        if self.current_token.type == "ELSE":
            self.advance()  # skip ELSE

            if self.current_token.type != "LBRACE":
                raise Exception("Expected '{' after 'else'")
            self.advance()  # skip LBRACE

            else_block = []
            while self.current_token.type != "RBRACE" and self.current_token.type != "EOF":
                else_block.append(self.statement())

            if self.current_token.type != "RBRACE":
                raise Exception("Expected '}' to close else block")
            self.advance()  # skip RBRACE

        return IfNode(condition, then_block, else_block)

    def repeat_stmt(self):
        self.advance()  # skip REPEAT

        if self.current_token.type != "LPAREN":
            raise Exception("Expected '(' after 'repeat'")
        self.advance()  # skip LPAREN

        condition = self.expr()

        if self.current_token.type != "RPAREN":
            raise Exception("Expected ')' after repeat condition")
        self.advance()  # skip RPAREN

        if self.current_token.type != "LBRACE":
            raise Exception("Expected '{' after repeat condition")
        self.advance()  # skip LBRACE

        body = []
        while self.current_token.type != "RBRACE" and self.current_token.type != "EOF":
            body.append(self.statement())

        if self.current_token.type != "RBRACE":
            raise Exception("Expected '}' to close repeat block")
        self.advance()  # skip RBRACE

        return RepeatNode(condition, body)

    def expr(self):
        return self.or_expr()

    def or_expr(self):
        left = self.and_expr()

        while self.current_token.type == "OR":
            op = self.current_token
            self.advance()
            right = self.and_expr()
            left = BinOpNode(left, op, right)

        return left

    def and_expr(self):
        left = self.not_expr()

        while self.current_token.type == "AND":
            op = self.current_token
            self.advance()
            right = self.not_expr()
            left = BinOpNode(left, op, right)

        return left

    def not_expr(self):
        if self.current_token.type == "NOT":
            op = self.current_token
            self.advance()
            operand = self.not_expr()
            return UnaryOpNode(op, operand)

        return self.comparison()

    def comparison(self):
        left = self.arithmetic()

        while self.current_token.type in ["GT", "LT", "GTE", "LTE", "EQ", "NEQ"]:
            op = self.current_token
            self.advance()
            right = self.arithmetic()
            left = ComparisonNode(left, op, right)

        return left

    def arithmetic(self):
        left = self.multiply()

        while self.current_token.type in ["PLUS", "MINUS"]:
            op = self.current_token
            self.advance()
            right = self.multiply()
            left = BinOpNode(left, op, right)

        return left

    def multiply(self):
        left = self.term()

        while self.current_token.type in ["MUL", "DIV", "MOD"]:
            op = self.current_token
            self.advance()
            right = self.term()
            left = BinOpNode(left, op, right)

        return left

    def term(self):
        tok = self.current_token

        if tok.type == "NUMBER":
            self.advance()
            return NumberNode(tok.value)

        if tok.type == "STRING":
            self.advance()
            return StringNode(tok.value)

        if tok.type == "IDENTIFIER":
            name = tok.value
            self.advance()
            # Check if this is a function call
            if self.current_token.type == "LPAREN":
                return self.function_call(name)
            return VarAccessNode(name)

        if tok.type == "LPAREN":
            self.advance()  # skip LPAREN
            expr = self.expr()
            if self.current_token.type != "RPAREN":
                raise Exception("Expected ')' to close parenthesized expression")
            self.advance()  # skip RPAREN
            return expr

        raise Exception(f"Unexpected token in expression: {tok}")

    def function_call(self, func_name):
        # current_token is LPAREN
        self.advance()  # skip LPAREN
        args = []
        
        # Parse arguments
        if self.current_token.type != "RPAREN":
            args.append(self.expr())
            while self.current_token.type == "COMMA":
                self.advance()  # skip COMMA
                args.append(self.expr())
        
        if self.current_token.type != "RPAREN":
            raise Exception(f"Expected ')' in function call, got {self.current_token}")
        
        self.advance()  # skip RPAREN
        
        from src.nodes import FunctionCallNode
        return FunctionCallNode(func_name, args)

    def func_def(self):
        self.advance()  # skip FUNC
        
        if self.current_token.type != "IDENTIFIER":
            raise Exception("Expected function name")
        func_name = self.current_token.value
        self.advance()
        
        if self.current_token.type != "LPAREN":
            raise Exception("Expected '(' after function name")
        self.advance()  # skip LPAREN
        
        params = []
        if self.current_token.type == "IDENTIFIER":
            params.append(self.current_token.value)
            self.advance()
            while self.current_token.type == "COMMA":
                self.advance()  # skip COMMA
                if self.current_token.type != "IDENTIFIER":
                    raise Exception("Expected parameter name")
                params.append(self.current_token.value)
                self.advance()
        
        if self.current_token.type != "RPAREN":
            raise Exception("Expected ')' after parameters")
        self.advance()  # skip RPAREN
        
        if self.current_token.type != "LBRACE":
            raise Exception("Expected '{' to start function body")
        self.advance()  # skip LBRACE
        
        body = []
        while self.current_token.type != "RBRACE" and self.current_token.type != "EOF":
            body.append(self.statement())
        
        if self.current_token.type != "RBRACE":
            raise Exception("Expected '}' to close function body")
        self.advance()  # skip RBRACE
        
        return FunctionDefNode(func_name, params, body)

    def return_stmt(self):
        self.advance()  # skip RETURN
        
        if self.current_token.type in ["RBRACE", "EOF"]:
            return ReturnNode(None)
        
        expr = self.expr()
        return ReturnNode(expr)
