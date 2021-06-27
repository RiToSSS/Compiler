from parser_expressions.node import Node

class UnOperNode(Node):
    def __init__(self, operation, left):
        self.operation = operation
        self.left = left

    def print(self, priority = 1):
        operation = self.operation.get_value()
        left = self.left.print(priority + 1)
        return f"{operation}{left}"