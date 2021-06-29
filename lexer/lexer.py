from lexer.lexem import Lexem
from lexer.states import States

class Lexer:
    def __init__(self, path):
        self.file = open(path, "r", encoding="utf-8")
        self.text = self.file.read(1)
        self.state = States.null
        self.buff = ""
        self.index = 1
        self.line = 1
        self.coordinates = [1, 1]
        self.separators = {".", ",", ":", ";", "[", "]", "(", ")"}
        self.spaces = {' ', '\n', '\t', '\0', '\r', ""}
        self.operations = {"+=", "-=", "*=", "/=", '+', '-', '*', '/', '=', '<', '>', "**", ">=", "<="}
        self.reserved = {
            "abs", "arctan", "boolean", "char", "chr", "cos", "dispose", "eoln", "exp",
            "false", "get", "input", "integer", "ln", "maxint", "new", "odd", "ord", "output",
            "pack", "page", "pred", "put", "read", "readln", "real", "reset", "rewrite", "round",
            "sin", "sqr", "sqrt", "succ", "text", "true", "trunc", "unpack", "write", "writeln",
            "and", "array", "asm", "begin", "case", "const", "consatructor", "destructor", "div", "do",
            "downto", "else", "end", "exports", "file", "for", "function", "goto", "if", "implementation",
            "in", "inherited", "inline", "interface", "label", "library", "mod", "nil", "not", "object",
            "of", "or", "packed", "procedure", "program", "record", "repeat", "set", "shl", "shr",
            "string", "then", "to", "type", "unit", "until", "uses", "var", "while", "with", "xor"}

    def replace_code(self, string):
        open = False
        sharp = False
        output = ""
        buf = ""
        s = 0
        while s < len(string):
            if sharp and string[s].isdigit():
                buf += string[s]
            elif sharp and not string[s].isdigit():
                sharp = False
                output += chr(int(buf))
                buf = ""
                s -= 1
            elif string[s] == "'":
                open = not open
            elif string[s] == "#" and not open:
                sharp = True
            else:
                output += string[s]
            s += 1
        if buf:
            output += chr(int(buf))
        return output

    def get_symbol (self):
        self.text = self.file.read(1)
        self.index += 1

    def buffer (self, buff):
        self.buff += buff

    def save_coordinate (self):
        self.coordinates = [self.line, self.index]

    def clean_buff (self):
        self.buff = ""

    def current_lexem (self):
        return self.lexem

    def get_lexem (self):
         self.clean_buff()
         while self.text != "" or self.buff != "":
             if self.state == States.null:

                 if self.text in self.spaces:
                    if self.text == "\n":
                        self.line += 1
                        self.index = 0
                    self.get_symbol()

                 elif self.text.isalpha():
                    self.buffer(self.text)
                    self.state = States.identifier
                    self.save_coordinate()
                    self.get_symbol()

                 elif self.text.isdigit():
                    self.buffer(self.text)
                    self.state = States.integer
                    self.save_coordinate()
                    self.get_symbol()

                 elif self.text == "$":
                    self.buffer(self.text)
                    self.state =States.int_16
                    self.save_coordinate()
                    self.get_symbol()

                 elif self.text == "'":
                    self.buffer(self.text)
                    self.state = States.string
                    self.save_coordinate()
                    self.get_symbol()

                 elif self.text in self.separators:
                    self.buffer(self.text)
                    self.save_coordinate()
                    self.get_symbol()
                    self.lexem = Lexem(self.coordinates, States.separator.value, self.buff, self.buff)
                    return self.lexem

                 elif self.text in self.operations:
                    self.buffer(self.text)
                    self.save_coordinate()
                    self.get_symbol()
                    self.state = States.operation

                 elif self.text == "{":
                     self.get_symbol()
                     self.state = States.comment_block

                 else:
                    self.state = States.error
                    self.buffer(self.text)
                    self.save_coordinate()
                    self.get_symbol()

             elif self.state == States.identifier:

                 if self.text.isalpha() or self.text.isdigit() or self.text == "_":
                    self.buffer(self.text)
                    self.get_symbol()

                 else :
                     if self.buff.lower() in self.reserved:
                         type_lexem = States.reserved

                     else:
                         type_lexem = States.identifier

                     self.state = States.null
                     self.lexem = Lexem(self.coordinates, type_lexem.value, self.buff, self.buff.lower())
                     return self.lexem

             elif self.state == States.integer:

                 if self.text.isdigit():
                     self.buffer(self.text)
                     self.get_symbol()

                 elif self.text.lower() == "e":
                     self.state = States.real_e
                     self.buffer(self.text)
                     self.get_symbol()

                 elif self.text == ".":
                     self.buffer(self.text)
                     self.get_symbol()
                     self.state = States.real

                 else:
                     if self.text.isalpha():
                        self.state = States.error
                        self.buffer(self.text)
                        self.get_symbol()
                     else:
                        self.state = States.null
                        self.lexem = Lexem(self.coordinates, States.integer.value, self.buff, int(self.buff))
                        return self.lexem

             elif self.state == States.int_16:
                if self.text.isdigit():
                    self.buffer(self.text)
                    self.get_symbol()
                elif (self.text.lower() <= "f") and (self.text.lower() >= "a"):
                    self.buffer(self.text)
                    self.get_symbol()
                elif self.text.isalpha():
                    self.state = States.error
                else:
                    self.state = States.null
                    self.lexem = Lexem(self.coordinates, States.integer.value, self.buff, int(self.buff[1:], 16))
                    return self.lexem


             elif self.state == States.real:

                 if self.text.isdigit():
                     self.buffer(self.text)
                     self.get_symbol()

                 elif self.text.lower() == "e":
                     if self.buff[len(self.buff)-1] == ".":
                         self.state = States.error
                     else:
                         self.state = States.real_e
                     self.buffer(self.text)
                     self.get_symbol()

                 elif self.text.isalpha():
                     self.state = States.error
                     self.buffer(self.text)
                     self.get_symbol()

                 else:
                     self.state = States.null
                     self.lexem = Lexem(self.coordinates, States.real.value, self.buff, float(self.buff))
                     return self.lexem

             elif self.state == States.real_e:

                 if self.text in {"+", "-"}:
                     if self.buff[len(self.buff)-1].lower() == "e":
                         self.buffer(self.text)
                         self.get_symbol()
                     elif not self.buff[len(self.buff)-1].lower() in {"+", "-"}:
                         self.state = States.null
                         self.lexem = Lexem(self.coordinates, States.real.value, self.buff, float(self.buff))
                         return self.lexem
                     else:
                         self.state = States.error
                         self.buffer(self.text)
                         self.get_symbol()

                 elif self.text.isdigit():
                     self.buffer(self.text)
                     self.get_symbol()

                 else:
                     if self.buff[len(self.buff)-1].lower() == "e":
                         self.state = States.error
                     else:
                         self.state = States.null
                         self.lexem = Lexem(self.coordinates, States.real.value, self.buff, float(self.buff))
                         return self.lexem

             elif self.state == States.string:

                 if self.text == "'":
                     self.buffer(self.text)
                     self.get_symbol()
                     self.state = States.null
                     if self.text == "#":
                         self.state = States.string_literal
                         self.buffer(self.text)
                         self.get_symbol()
                     else:
                         buff2 = self.replace_code(self.buff)
                         self.lexem = Lexem(self.coordinates, States.string.value, self.buff, buff2)
                         return self.lexem

                 elif self.text == "\n" or self.text == "":
                     self.state = States.error

                 else:
                     self.buffer(self.text)
                     self.get_symbol()

             elif self.state == States.string_literal:
                 if self.text == "#" and self.buff[len(self.buff)-1].isdigit():
                     self.buffer(self.text)
                     self.get_symbol()
                 elif self.text.isdigit():
                     self.buffer(self.text)
                     self.get_symbol()
                 elif self.buff[len(self.buff)-1].isdigit() and self.text == "'":
                     self.state = States.string
                     self.buffer(self.text)
                     self.get_symbol()
                 else:
                     self.state = States.null
                     self.get_symbol()
                     buff2 = self.replace_code(self.buff)
                     self.lexem = Lexem(self.coordinates, States.string.value, self.buff, buff2)
                     return self.lexem



             elif self.state == States.operation:
                 if self.buff + self.text in self.operations and self.text != "":
                     self.buffer(self.text)
                     self.get_symbol()

                 elif self.buff + self.text == "//":
                     self.state = States.comment
                     self.get_symbol()

                 else:
                     self.state = States.null
                     self.lexem = Lexem(self.coordinates, States.operation.value, self.buff, self.buff)
                     return self.lexem

             elif self.state == States.comment:
                 if self.text == "\n":
                     self.line += 1
                     self.index = 0
                     self.state = States.null
                     self.clean_buff()
                 elif not self.text:
                     self.state = States.null
                     self.clean_buff()
                 self.get_symbol()

             elif self.state == States.comment_block:
                 if self.text == "}":
                     self.state = States.null
                     self.get_symbol()
                 elif self.text == "\n":
                     self.line += 1
                     self.index = 0
                     self.get_symbol()
                 else:
                     self.get_symbol()
                     if self.text == "":
                        raise RuntimeError(f"{self.line}:{self.index}        " + "} was expected")

             elif self.state == States.error:
                 if self.text in self.spaces or self.text in self.separators:
                     raise RuntimeError(f'{self.coordinates[0]}:{self.coordinates[1]}        Unexpected symbol in "{self.buff}"')
                 self.buffer(self.text)
                 self.get_symbol()


         self.save_coordinate()
         self.lexem = Lexem(self.coordinates, "eof", "end of file", "")
         return self.lexem
