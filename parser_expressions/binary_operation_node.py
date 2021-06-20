from parser_expressions.node import Node

class BinOperNode(Node):
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def print(self, priority):
        left = self.left.get_value()
        right = self.right.get_value()
        operation = self.operation.get_value()
        if isinstance(self.right, BinOperNode):
            right = self.right.print(priority + 1)
        if isinstance(self.left, BinOperNode):
            left = self.left.print(priority + 1)
        tab = "        "
        return f"{operation}\n{tab * priority}{left}\n{tab * priority}{right}"

    def get_value(self):
        pass