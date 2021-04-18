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
        self.operations = {'+', '-', '*', '/', '=', '<', '>', "**", ">=", "<="}

        self.assignment = {"+=", "-=", "*=", "/="}

        self.service_words = {"abs", "arctan", "boolean", "char", "chr", "cos", "dispose", "eoln", "exp",
                           "false", "get", "input", "integer", "ln", "maxint", "new", "odd", "ord", "output",
                           "pack", "page", "pred", "put", "read", "readln", "real", "reset", "rewrite", "round",
                           "sin", "sqr", "sqrt", "succ", "text", "true", "trunc", "unpack", "write", "writeln"}

        self.reserved = {"and", "array", "asm", "begin", "case", "const", "consatructor", "destructor", "div", "do",
                         "downto", "else", "end", "exports", "file", "for", "function", "goto", "if", "implementation",
                         "in", "inherited", "inline", "interface", "label", "library", "mod", "nil", "not", "object",
                         "of", "or", "packed", "procedure", "program", "record", "repeat", "set", "shl", "shr",
                         "string", "then", "to", "type", "unit", "until", "uses", "var", "while", "with", "xor"}
        self.end = "eof"


    def end_state (self):
        return self.state == "end"

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
         found = False
         while not found:
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
                    self.state = "number"
                    self.save_coordinate()
                    self.next_index()

                 else:
                     self.state = "error"
                     self.buffer(self.text)
                     self.save_coordinate()
                     self.next_index()

             if self.state == "identifier":

                 if self.text.isalpha() or self.text.isdigit() or self.text == "_":
                    self.buffer(self.text)
                    self.next_index()

                 elif self.buff.lower() == self.end:
                     self.state = "end"
                     lex = Lexem(self.mas_index,"end", self.buff, self.buff.lower())
                     found = True

                 elif self.text in self.spaces or self.text in self.separators or self.text in self.operations:
                     type_lexem = ""

                     if self.buff.lower() in self.reserved:
                         type_lexem = "reserved"

                     elif self.buff.lower() in self.service_words:
                         type_lexem = "prewritten"

                     else:
                         type_lexem = "identifier"

                     lex = Lexem(self.mas_index, type_lexem, self.buff, self.buff.lower())
                     found = True
                     self.clean_buff()
                     self.state = "null"

                 else:
                     self.state = "error"
                     self.buffer(self.text)
                     self.next_index()

         return lex









