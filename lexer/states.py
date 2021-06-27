from enum import Enum

class States (Enum):
    integer = "integer"
    null = "null"
    string = "string"
    identifier = "identifier"
    real = "real"
    operation = "operation"
    comment = "comment"
    separator = "separator"
    error = "error"
    reserved = "reserved"
    predefined = "predefined"
    int_16 = "int_16"