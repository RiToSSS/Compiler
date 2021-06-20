from parser_expressions.node import Node

class RealNode(Node):
    def __init__(self, lexem):
        self.lexem = lexem

    def print(self):
        return str(self.lexem.get_value())

    def get_value(self):
        return self.lexem.get_value()