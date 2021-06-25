from parser_expressions.node import Node

class BinOperNode(Node):
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def print(self, priority = 1):
        operation = self.operation.get_value()
        right = self.right.print(priority + 1)
        left = self.left.print(priority + 1)
        tab = "        "
        return f"{operation}\n{tab * priority}{left}\n{tab * priority}{right}"
