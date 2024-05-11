import re
import time

keywords = {"int", "float", "char", "void", "if", "else if", "else", "while", "return", "const", "for"}
identifier_regex = r'\b(?!(?:' + '|'.join(re.escape(keyword) for keyword in keywords) + r')\b)(?!^\d)[A-Za-z_][A-Za-z0-9_]*\b'

token_types = {
    "keyword": r'\b(?:int|float|char|if|else if|else|while|for|return|void)\b',
    "identifier": identifier_regex,
    "special_symbol": r"(?<!\S)[£$^#_:@&?](?!\S)",
    "integer" : r'-?\b(?<!\.)[-+]?\d+\b(?!\.\d)',
    "float" : r'-?\b\d+\.\d+\b',
    "punctuator": r'[\(\)\{\}\[\];]',
    "string": r'\".*?\"|\'(?:\\.|[^\\\'])*\'',
    "operator": r'[+\-/%<>^=!~]|<<|>>|\+\+|\-\-|&&|\|\||\+=|-=|\=|/=|%=|<<=|>>=|&=|\|=|\^=|==|!=|<=|>=|->'
}

# Combined regex for all token types
token_regex = '|'.join('(?P<{}>{})'.format(token_name, regex) for token_name, regex in token_types.items())

# Function to tokenize a line of code and print tokens
def tokenize_and_print_line(line, line_number):
    print("============ LINE", line_number, "============")
    invalid_tokens = []

    for match in re.finditer(token_regex, line):
        for name, value in match.groupdict().items():
            if value:
                print("{:<16}: {}".format(name.capitalize(), value))
                break

    all_tokens = re.findall(r'(?<!\S)\S+|\b\w+\b', line)
    invalid_tokens = [token for token in all_tokens if not any(re.match(regex, token) for regex in token_types.values())]

    if invalid_tokens:
        print("{:<16}: {}".format("Invalid tokens", invalid_tokens))


# scan a file and tokenize its content line by line
def scan_file(file_path):
    with open(file_path, 'r') as file:
        line_number = 1
        for line in file:
            tokenize_and_print_line(line.strip(), line_number)
            line_number += 1

# Entry point
if __name__ == "__main__":
    start_time = time.time()
    file_path = 'miniC.c'

    scan_file(file_path)

    end_time = time.time()
    execution_time = end_time - start_time
    print("\nExecution Time:", execution_time)
