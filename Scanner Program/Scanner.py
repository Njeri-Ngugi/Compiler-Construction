# List Tokens
# Comparison
import re #regular expression library


token_list = {
    "T_KEYWORDS" : ["int","float","char","float","if","else if","else","while","for","return"],
    "T_" : "",
    "T_SPECIALSYMBOLS" : "",
    "" : "",
    "" : "",
    "" : "",
    "" : "",
    "" : "",
    "" : "",
    "" : "",
}

tokens_regex = [
    {"Token_Name": "Keywords", "lexeme" : "int", "Regular_expression" : ""},


    {"Token_Name": "Identifiers", "lexeme" : "A-Z", "Regular_expression" : "[A-Z]"}
]


integer_values = r'0|[+-]?[1-9][0-9]*'
float_values = r'[+-]?[0-9]*\.[0-9]+'
integers = r'\bint\b'
floats =  r'\bfloat\b'
chars =  r'\bchar\b'
ifs = r'\bif\b'
else_ifs = r'\belseif\b'
elses = r'\belse\b'
whiles = r'\bwhile\b'
returns = r'\breturn\b'
consts = r'\bconst\b'
identifiers = r'^[A-Za-z_][A-Za-z0-9_]{30}$'

Keywords = {
    "int" : integers,
    "float" : floats,
    "char" : chars,
    "if" : ifs,
    "else if" : else_ifs,
    "else" : elses,
    "whiles" : whiles,
    "return" : returns,
    "const" : consts,
}

identifiers ={
    "identifiers" : identifiers,
}

special_symbols = r'[£$^&#_:@?]'

numbers = r'[0|[1-9]\d*]'




