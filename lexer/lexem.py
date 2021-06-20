class Lexem:
    def __init__(self, coordinate, type, text, value):
        self.coordinate = coordinate
        self.type = type
        self.text = text
        self.value = value

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

    def get_text(self):
        return self.text

    def print_parameters(self):
        return '{}:{}        {}        "{}"        {}'.format(self.coordinate[0], self.coordinate[1], self.type, self.text, self.value)
