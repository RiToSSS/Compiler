from lexem import Lexem
class Lexer:
    def __init__(self, path):
        self.file = open(path, "r", encoding="utf-8")
        self.text = self.file.read(1)
        self.state = "null"
        self.buff = ""
        self.index = 1
        self.line = 1
        self.mas_index = [1,1]
        self.separators = {".", ",", ":", ";", "[", "]", "(", ")"}
        self.spaces =  {' ', '\n', '\t', '\0', '\r'}
        self.operations = {"+=", "-=", "*=", "/=", '+', '-', '*', '/', '=', '<', '>', "**", ">=", "<="}
        self.service_words = {"abs", "arctan", "boolean", "char", "chr", "cos", "dispose", "eoln", "exp",
                           "false", "get", "input", "integer", "ln", "maxint", "new", "odd", "ord", "output",
                           "pack", "page", "pred", "put", "read", "readln", "real", "reset", "rewrite", "round",
                           "sin", "sqr", "sqrt", "succ", "text", "true", "trunc", "unpack", "write", "writeln"}
        self.reserved = {"and", "array", "asm", "begin", "case", "const", "consatructor", "destructor", "div", "do",
                         "downto", "else", "end", "exports", "file", "for", "function", "goto", "if", "implementation",
                         "in", "inherited", "inline", "interface", "label", "library", "mod", "nil", "not", "object",
                         "of", "or", "packed", "procedure", "program", "record", "repeat", "set", "shl", "shr",
                         "string", "then", "to", "type", "unit", "until", "uses", "var", "while", "with", "xor"}

    def next_index (self):
        self.text = self.file.read(1)
        self.index += 1

    def buffer (self, buff):
        self.buff += buff

    def save_coordinate (self):
        self.mas_index = [self.line, self.index]

    def clean_buff (self):
        self.buff = ""

    def get_lexem (self):
         self.clean_buff()
         while self.text != "" or self.buff != "":
             if self.state == "null":

                 if self.text in self.spaces:
                    if self.text == "\n":
                        self.line += 1
                        self.index = 0
                    self.next_index()

                 elif self.text.isalpha():
                    self.buffer(self.text)
                    self.state = "identifier"
                    self.save_coordinate()
                    self.next_index()

                 elif self.text.isdigit():
                    self.buffer(self.text)
                    self.state = "integer"
                    self.save_coordinate()
                    self.next_index()

                 elif self.text == "'":
                    self.buffer(self.text)
                    self.state = "string"
                    self.save_coordinate()
                    self.next_index()

                 elif self.text in self.separators:
                    self.buffer(self.text)
                    self.save_coordinate()
                    self.next_index()
                    return Lexem(self.mas_index,"separator", self.buff, self.buff)

                 elif self.text in self.operations:
                    self.buffer(self.text)
                    self.save_coordinate()
                    self.next_index()
                    self.state = "operations"

                 else:
                    self.state = "error"
                    self.buffer(self.text)
                    self.save_coordinate()
                    self.next_index()

             elif self.state == "identifier":

                 if self.text.isalpha() or self.text.isdigit() or self.text == "_":
                    self.buffer(self.text)
                    self.next_index()

                 else :
                     if self.buff.lower() in self.reserved:
                         type_lexem = "reserved"

                     elif self.buff.lower() in self.service_words:
                         type_lexem = "prewritten"

                     else:
                         type_lexem = "identifier"

                     self.state = "null"
                     return Lexem(self.mas_index, type_lexem, self.buff, self.buff.lower())

             elif self.state == "integer":

                 if self.text.isdigit():
                     self.buffer(self.text)
                     self.next_index()

                 elif self.text == ".":
                     self.buffer(self.text)
                     self.next_index()
                     self.state = "real"

                 else:
                     if self.text.isalpha():
                        self.state = "error"
                        self.buffer(self.text)
                     else:
                        self.state = "null"
                        return Lexem(self.mas_index, "integer", self.buff, int(self.buff))

             elif self.state == "real":

                 if self.text.isdigit():
                     self.buffer(self.text)
                     self.next_index()

                 else:
                     if self.text.isalpha():
                         self.state = "error"
                         self.buffer(self.text)
                     else:
                         self.state = "null"
                         return Lexem(self.mas_index, "real", self.buff, float(self.buff))

             elif self.state == "string":

                 if self.text == "'":
                     self.buffer(self.text)
                     self.next_index()
                     self.state = "null"
                     return Lexem(self.mas_index, "string", self.buff, self.buff[1:-1])

                 elif self.text == "\n" or self.text == "":
                     self.state = "error"

                 else:
                     self.buffer(self.text)
                     self.next_index()

             elif self.state == "operations":
                 if self.buff + self.text in self.operations:
                     self.buffer(self.text)
                     self.next_index()

                 elif self.buff + self.text == "//":
                     self.state = "comment"
                     self.next_index()

                 else:
                     self.state = "null"
                     return Lexem(self.mas_index, "operation", self.buff, self.buff)

             elif self.state == "comment":
                 if self.text == "\n":
                     self.line += 1
                     self.index = 0
                     self.state = "null"
                     self.clean_buff()
                 self.next_index()

             elif self.state == "error":
                 self.text = ""
                 return Lexem(self.mas_index, "error", self.buff, self.buff.lower())


         self.save_coordinate()
         return Lexem(self.mas_index,"eof","", "")









