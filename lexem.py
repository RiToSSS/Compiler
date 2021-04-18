class Lexem:
    def __init__(self, coordinate, type, text, value):
        self.coordinate = coordinate
        self.type = type
        self.text = text
        self.value = value

    def print_parameters(self):
        if self.type != "end":
            return '{}:{}        {}        "{}"        {}'.format(self.coordinate[0], self.coordinate[1], self.type, self.text, self.value)
        else:
            return ""
