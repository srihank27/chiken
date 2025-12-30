# AST Nodes for ChIkEn
# AST Nodes for ChIkEn


class NumberNode:
    def __init__(self, value):
        self.value = value


class StringNode:
    def __init__(self, value):
        self.value = value


class VarAccessNode:
    def __init__(self, name):
        self.name = name


class VarAssignNode:
    def __init__(self, name, value_node):
        self.name = name
        self.value_node = value_node


class BinOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node


class UnaryOpNode:
    def __init__(self, op_token, operand):
        self.op_token = op_token
        self.operand = operand


class PrintNode:
    def __init__(self, value_node):
        self.value_node = value_node


class FunctionCallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args  # list of argument nodes


class ComparisonNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node


class IfNode:
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block  # list of statements
        self.else_block = else_block  # list of statements or None


class RepeatNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body  # list of statements


class FunctionDefNode:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params  # list of parameter names
        self.body = body  # list of statements


class ReturnNode:
    def __init__(self, value_node):
        self.value_node = value_node
