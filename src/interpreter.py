from src.nodes import NumberNode, StringNode, VarAccessNode, VarAssignNode, BinOpNode, UnaryOpNode, PrintNode, FunctionCallNode, ComparisonNode, IfNode, RepeatNode, FunctionDefNode, ReturnNode
import math

class Interpreter:
    def __init__(self):
        self.symbol_table = {}
        self.functions = {}
        self.return_value = None

    def visit(self, node):
        if isinstance(node, NumberNode):
            return node.value

        elif isinstance(node, StringNode):
            return node.value

        elif isinstance(node, VarAccessNode):
            if node.name in self.symbol_table:
                return self.symbol_table[node.name]
            else:
                raise Exception(f"Variable '{node.name}' not defined")

        elif isinstance(node, VarAssignNode):
            value = self.visit(node.value_node)
            self.symbol_table[node.name] = value
            return value

        elif isinstance(node, BinOpNode):
            left = self.visit(node.left_node)
            right = self.visit(node.right_node)
            if node.op_token.type == "PLUS":
                return left + right
            elif node.op_token.type == "MINUS":
                return left - right
            elif node.op_token.type == "MUL":
                return left * right
            elif node.op_token.type == "DIV":
                if right == 0:
                    raise Exception("Division by zero")
                return left / right
            elif node.op_token.type == "MOD":
                if right == 0:
                    raise Exception("Modulo by zero")
                return left % right
            elif node.op_token.type == "AND":
                return left and right
            elif node.op_token.type == "OR":
                return left or right
            else:
                raise Exception(f"Unknown operator {node.op_token.type}")

        elif isinstance(node, UnaryOpNode):
            operand = self.visit(node.operand)
            if node.op_token.type == "NOT":
                return not operand
            else:
                raise Exception(f"Unknown unary operator {node.op_token.type}")

        elif isinstance(node, PrintNode):
            value = self.visit(node.value_node)
            print(value)
            return value

        elif isinstance(node, FunctionCallNode):
            return self.call_function(node.name, node.args)

        elif isinstance(node, ComparisonNode):
            left = self.visit(node.left_node)
            right = self.visit(node.right_node)
            op_type = node.op_token.type
            
            if op_type == "GT":
                return left > right
            elif op_type == "LT":
                return left < right
            elif op_type == "GTE":
                return left >= right
            elif op_type == "LTE":
                return left <= right
            elif op_type == "EQ":
                return left == right
            elif op_type == "NEQ":
                return left != right
            else:
                raise Exception(f"Unknown comparison operator: {op_type}")

        elif isinstance(node, IfNode):
            condition = self.visit(node.condition)
            
            if condition:
                for stmt in node.then_block:
                    self.visit(stmt)
            elif node.else_block:
                for stmt in node.else_block:
                    self.visit(stmt)

        elif isinstance(node, RepeatNode):
            while self.visit(node.condition):
                for stmt in node.body:
                    self.visit(stmt)

        elif isinstance(node, FunctionDefNode):
            self.functions[node.name] = node
            return None

        elif isinstance(node, ReturnNode):
            if node.value_node:
                self.return_value = self.visit(node.value_node)
            else:
                self.return_value = None
            return self.return_value

        # 👇 New: handle any "say" statement nodes dynamically
        elif hasattr(node, 'type') and node.type.lower() == 'say':
            value = self.visit(node.value_node)
            print(value)
            return value

        else:
            raise Exception(f"Unknown node type: {type(node)}")

    def call_function(self, name, args):
        # Check if it's a user-defined function
        if name in self.functions:
            func_def = self.functions[name]
            if len(args) != len(func_def.params):
                raise Exception(f"{name}() expects {len(func_def.params)} arguments, got {len(args)}")
            
            # Evaluate arguments in current scope
            arg_values = [self.visit(arg) for arg in args]
            
            # Create new scope for function
            old_symbol_table = self.symbol_table
            self.symbol_table = old_symbol_table.copy()  # Copy to preserve outer scope access
            
            # Bind parameters
            for param, value in zip(func_def.params, arg_values):
                self.symbol_table[param] = value
            
            # Execute function body
            self.return_value = None
            for stmt in func_def.body:
                self.visit(stmt)
                if self.return_value is not None:
                    break
            
            result = self.return_value
            self.return_value = None
            
            # Restore old scope
            self.symbol_table = old_symbol_table
            
            return result
        
        # Built-in functions
        arg_values = [self.visit(arg) for arg in args]
        
        # Input function
        if name == "input":
            if len(arg_values) > 1:
                raise Exception(f"input() expects 0 or 1 argument, got {len(arg_values)}")
            prompt = arg_values[0] if arg_values else ""
            try:
                result = input(str(prompt))
                # Try to parse as number
                try:
                    return int(result)
                except ValueError:
                    try:
                        return float(result)
                    except ValueError:
                        return result
            except EOFError:
                return ""
        
        # Math functions
        if name == "add":
            if len(arg_values) != 2:
                raise Exception(f"add() expects 2 arguments, got {len(arg_values)}")
            return arg_values[0] + arg_values[1]
        
        elif name == "subtract" or name == "sub":
            if len(arg_values) != 2:
                raise Exception(f"{name}() expects 2 arguments, got {len(arg_values)}")
            return arg_values[0] - arg_values[1]
        
        elif name == "multiply" or name == "mul":
            if len(arg_values) != 2:
                raise Exception(f"{name}() expects 2 arguments, got {len(arg_values)}")
            return arg_values[0] * arg_values[1]
        
        elif name == "divide" or name == "div":
            if len(arg_values) != 2:
                raise Exception(f"{name}() expects 2 arguments, got {len(arg_values)}")
            if arg_values[1] == 0:
                raise Exception("Division by zero")
            return arg_values[0] / arg_values[1]
        
        elif name == "power" or name == "pow":
            if len(arg_values) != 2:
                raise Exception(f"{name}() expects 2 arguments, got {len(arg_values)}")
            return arg_values[0] ** arg_values[1]
        
        elif name == "sqrt":
            if len(arg_values) != 1:
                raise Exception(f"sqrt() expects 1 argument, got {len(arg_values)}")
            if arg_values[0] < 0:
                raise Exception("Cannot take sqrt of negative number")
            return math.sqrt(arg_values[0])
        
        elif name == "abs":
            if len(arg_values) != 1:
                raise Exception(f"abs() expects 1 argument, got {len(arg_values)}")
            return abs(arg_values[0])
        
        elif name == "min":
            if len(arg_values) < 2:
                raise Exception(f"min() expects at least 2 arguments, got {len(arg_values)}")
            return min(arg_values)
        
        elif name == "max":
            if len(arg_values) < 2:
                raise Exception(f"max() expects at least 2 arguments, got {len(arg_values)}")
            return max(arg_values)
        
        else:
            raise Exception(f"Unknown function: {name}")