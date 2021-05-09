from lexer import Lexer
import os
#Compiler -L -F text.txt
#Compiler -L -D lexer/tests
command = input()
test = command.split(" ")
if test[0].lower() == "compiler":
    if test[1] == "-L":

        if test[2] == "-F":
            lex = Lexer(test[3])
            while lex.text != "":
                print(lex.get_lexem().print_parameters())
            print(lex.get_lexem().print_parameters())

        elif test[2] == "-D":
            if os.path.isdir(test[3]):
                all_tests = 0
                not_pass = 0
                for file in os.listdir(test[3]):
                    if file[len(file)-10:] == "(code).txt":
                        all_tests += 1
                        path_answer = os.path.join("lexer","tests", file.replace("(code)", ""))
                        file_answer = open(path_answer, "r", encoding="utf-8")
                        lex = Lexer(os.path.join("lexer","tests", file))
                        flag = True
                        while lex.text != "":
                            point = lex.get_lexem().print_parameters()
                            if point != file_answer.readline().replace("\n", ""):
                                flag = False
                                not_pass += 1
                                print(point)
                                break
                        if flag:
                            print(file, "- пройден")
                        else:
                            print(file, "- не пройден")
                print("Всего тестов =", all_tests, "Непройдено тестов =", not_pass)