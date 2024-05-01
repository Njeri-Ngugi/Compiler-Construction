import re
import time # To calculate execution time
start_time = time.time()

keywords = {"int", "float", "char", "if", "else if", "else", "while", "return", "const", "for"}

string_regex = r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\''

identifier_regex = r'\b(?!(?:' + '|'.join(re.escape(keyword) for keyword in keywords) + r')\b)(?!^\d)[A-Za-z_][A-Za-z0-9_]{0,29}\b'

# token types and their regex
token_regex = {
    "keywords": r'\b(?:int|float|char|if|else if|else|while|for|return)\b',
    "identifier": identifier_regex, 
    "special_symbol": r"(?<!\S)[£$^#_:@&?](?!\S)",
    "number": r'\b(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?\b',
    "punctuator": r'[\(\)\{\}\[\];]',
    "string": string_regex,
    "operators": r'[+\-/%<>^=!~]|<<|>>|\+\+|\-\-|&&|\|\||\+=|-=|\=|/=|%=|<<=|>>=|&=|\|=|\^=|==|!=|<=|>=|->'
}

# Function to assign lexemes to token types
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
file_path = '/home/njeriii/Documents/school/csc326/Scanner_Program/miniC.c'

tokens = scan_file(file_path)

for token_name, token_values in tokens.items():
    print(token_name.capitalize() ,"found:", token_values)
    print("\n")


end_time = time.time()

execution_time = end_time - start_time

print("Execution Time", execution_time )
