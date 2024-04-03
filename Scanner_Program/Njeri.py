import re

keywords = {"int", "float", "char", "if", "else if", "else", "while", "return", "const"}

string_regex = r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\''

identifier_regex = r'\b(?!(?:' + '|'.join(re.escape(keyword) for keyword in keywords) + r')\b)(?!^\d)[A-Za-z_][A-Za-z0-9_]{0,29}\b'

token_regex = {
    "int": r'\bint\b',
    "float": r'\bfloat\b',
    "char": r'\bchar\b',
    "if": r'\bif\b',
    "else_if": r'\belse\s+if\b',
    "else": r'\belse\b',
    "while": r'\bwhile\b',
    "return": r'\breturn\b',
    "const": r'\bconst\b',
    "identifier": identifier_regex, 
    "special_symbol": r'[£$^&#_:@?]',
    "number": r'\b(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?\b',
    "punctuator": r'[\(\)\{\}\[\];]',
    "string": string_regex,
    "operators": r'[+\-*/%<>&^|=!~]|<<|>>|\+\+|\-\-|&&|\|\||\+=|-=|\*=|/=|%=|<<=|>>=|&=|\|=|\^=|==|!=|<=|>=|->'
}

# Function to tokenize input code
def tokenize(code):
    tokens = {}

    for token_name, regex in token_regex.items():
        tokens[token_name] = re.findall(regex, code)
        
    strings = re.findall(string_regex, code)

    # Look for words in strings incorrectly grouped as identifiers
    filtered_identifiers = tokens["identifier"]
    for string in strings:
        for identifier in re.findall(identifier_regex, string):
            if identifier in filtered_identifiers:
                filtered_identifiers.remove(identifier)
    
    tokens["identifier"] = filtered_identifiers
    
    return tokens

# read file content and group lexemes
def scan_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
        tokens = tokenize(file_content)
        return tokens
    
# C file path
file_path = '/home/njeriii/Documents/school/csc326/Scanner_Program/minic.c'

tokens = scan_file(file_path)

for token_name, token_values in tokens.items():
    print(token_name.capitalize() ,"found:", list(set(token_values)))
    print("\n")
