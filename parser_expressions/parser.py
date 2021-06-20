from parser_expressions.binary_operation_node import BinOperNode
from parser_expressions.identifier_node import IdentifierNode
from parser_expressions.int_node import IntNode
from parser_expressions.real_node import RealNode
from lexer.states import States

class Parser:
    def __init__(self,lexer):
        self.lexer = lexer
        self.lexer.get_lexem()

    def parser_expr(self):
        left = self.parser_term()
        operation = self.lexer.current_lexem()
        while operation.get_value() == "+" or operation.get_value() == "-":
            self.lexer.get_lexem()
            right = self.parser_term()
            left = BinOperNode(operation, left, right)
            operation = self.lexer.current_lexem()
        return left

    def parser_term(self):
        left = self.parser_factor()
        operation = self.lexer.current_lexem()
        while operation.get_value() == "*" or operation.get_value() == "/":
            self.lexer.get_lexem()
            right = self.parser_factor()
            left = BinOperNode(operation, left, right)
            operation = self.lexer.current_lexem()
        return left

    def parser_factor(self):
        lexem = self.lexer.current_lexem()
        self.lexer.get_lexem()
        if lexem.get_type() == States.identifier.value:
            return IdentifierNode(lexem)
        if lexem.get_type() == States.integer.value:
            return IntNode(lexem)
        if lexem.get_type() == States.real.value:
            return RealNode(lexem)
        if lexem.get_value() == "(":
            left = self.parser_expr()
            lexem = self.lexer.current_lexem()
            if lexem.get_value() != ")":
                raise RuntimeError(") was expected")
            self.lexer.get_lexem()
            return left
        raise RuntimeError("Unexpected", lexem.get_text)