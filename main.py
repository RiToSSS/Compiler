from lexer.lexer import Lexer
from parser_expressions.parser import Parser
import os
import sys
# -L -F text.txt
# -L -D lexer/tests
# -P -F parser.txt
# -P -D parser_expressions/pars_tests
test = sys.argv
if test[1] == "-L":

    if test[2] == "-F":
        lex = Lexer(test[3])
        try:
            lexem = lex.get_lexem()
            while not lexem.eof():
                print(lexem.print_parameters())
                lexem = lex.get_lexem()

        except RuntimeError as error:
            print(error)

    elif test[2] == "-D":
        if os.path.isdir(test[3]):
            all_tests = 0
            not_pass = 0
            for file in os.listdir(test[3]):
                if file[len(file)-10:] == "(code).txt":
                    all_tests += 1
                    path_answer = os.path.join("lexer", "tests", file.replace("(code)", ""))
                    file_answer = open(path_answer, "r", encoding="utf-8")
                    lex = Lexer(os.path.join("lexer", "tests", file))
                    flag = True
                    point = ""
                    try:
                        lexem = lex.get_lexem()
                        point = lexem.print_parameters()
                        while not lexem.eof():
                            lexem = lex.get_lexem()
                            point += "\n"+lexem.print_parameters() if not lexem.eof() else ""
                        if point != file_answer.read():
                            flag = False
                            not_pass += 1

                    except RuntimeError as error:
                        error = point + "\n" + str(error) if point else str(error)
                        if error != file_answer.read():
                            flag = False
                            not_pass += 1
                    if flag:
                        print(file, "- пройден")
                    else:
                        print(file, "- не пройден")
            print("Всего тестов =", all_tests, "Непройдено тестов =", not_pass)

if test[1] == "-P":

        if test[2] == "-F":
            try:
                lex = Lexer(test[3])
                pars = Parser(lex)
                print(pars.parser_expr().print())

            except RuntimeError as error:
                print(error)

        elif test[2] == "-D":
            if os.path.isdir(test[3]):
                all_tests = 0
                not_pass = 0
                for file in os.listdir(test[3]):
                    if file[len(file)-10:] == "(code).txt":
                        all_tests += 1
                        path_answer = os.path.join("parser_expressions", "pars_tests", file.replace("(code)", ""))
                        file_answer = open(path_answer, "r", encoding="utf-8")
                        lex = Lexer(os.path.join("parser_expressions", "pars_tests", file))
                        flag = True
                        try:
                            point = Parser(lex).parser_expr().print()
                            if point != file_answer.read():
                                flag = False
                                not_pass += 1
                                print(point)
                                break
                        except RuntimeError as error:
                            error = str(error)
                            if error != file_answer.read():
                                flag = False
                                not_pass += 1
                                print(error)
                        if flag:
                            print(file, "- пройден")
                        else:
                            print(file, "- не пройден")
                print("Всего тестов =", all_tests, "Непройдено тестов =", not_pass)
# lexer = Lexer("parser_expressions\pars_tests\pars1.txt")
# result = Parser(lexer).parser_expr()
# print(result.print(1))
