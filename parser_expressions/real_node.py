from parser_expressions.node import Node

class RealNode(Node):
    def __init__(self, lexem):
        self.lexem = lexem

    def print(self, priority = None):
        return str(self.lexem.get_value())
