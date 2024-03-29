# List Tokens
# Comparison
import re 

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
special_symbols = r'[£$^&#_:@?]'
numbers = r'[0|[1-9]\d*]'
punctuators = r'[\(\)\{\}\[\];]'

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

identifier ={
    "identifiers" : identifiers,
}

special_symbol = {
    "special symbols" : special_symbols,
}

number = {
    "numbers" : numbers,
}

punctuators = {
    "punctuators" : punctuators,
}

arithmetic_operators = r'[+\-*/%]'
logical_operators = r'(&&|\|\||!)'
comparison_operators = r'(==|!=|<|<=|>|>=)'



# Read file and split contents into the different words
# Need to test this part
filename = "test.py" #Add filename
try:
    with open(filename, 'r') as file:
        file_contents = file.read()
        lexemes = file_contents.split()
        #maybe replace the top 2 lines with "for line in file" to read line by line without storing
except FileNotFoundError:
    print(f"File {filename} not found")

# For each word, search tokens to find the match



import sys

print("hello, my name is", sys.argv[1])
