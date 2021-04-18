from lexer import Lexer
lex = Lexer("text.txt")
while not lex.end_state():
    print(lex.get_lexem().print_parameters())