from enum import Enum

class States (Enum):
    integer = "integer"
    null = "null"
    string = "string"
    identifier = "identifier"
    real = "real"
    real_e = "real_e"
    operation = "operation"
    comment = "comment"
    comment_block = "comment_block"
    separator = "separator"
    error = "error"
    reserved = "reserved"
    predefined = "predefined"
    int_16 = "int_16"