import os
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

token_regex = '|'.join('(?P<{}>{})'.format(token_name, regex) for token_name, regex in token_types.items())

def tokenize_and_print_line(line, line_number):
    """
    Tokenizes a line of code and prints token types for the lexemes

    Args:
        line - line of code to tokenize
        line_number - current line number in the input code

    Returns:
        token_list - list of tokens and lexemes
    """
    token_list = []
    if line.strip():
        print("============ LINE", line_number, "============")
        invalid_tokens = []

        for match in re.finditer(token_regex, line):
            for name, value in match.groupdict().items():
                if value:
                    print("{:<16}: {}".format(name.capitalize(), value))
                    token_list.append((name.capitalize(), value))
                    break

        all_tokens = re.findall(r'(?<!\S)\S+|\b\w+\b', line)
        invalid_tokens = [token for token in all_tokens if not any(re.match(regex, token) for regex in token_types.values())]

        if invalid_tokens:
            print("{:<16}: {}".format("Invalid tokens", invalid_tokens))
    else:
        print("No tokens in line", line_number)

    return token_list

def scan_file(file_path):
    """
    Scans a file and tokenizes its content line by line

    Args:
        file_path - path to the file with code to tokenize

    Returns:
        token_list - list of tokens and lexemes for each line of code
    """
    token_list = []
    with open(file_path, 'r') as file:
        line_number = 1
        for line in file:
            token_list.append(tokenize_and_print_line(line.strip(), line_number))
            line_number += 1
    return token_list # list of tuples (token_type, token_value)


if __name__ == "__main__":
    start_time = time.time()
    input_file = 'Scanner_Program/mini2.c'
    tokens = scan_file(input_file)

    end_time = time.time()
    execution_time = end_time - start_time
    print("\nExecution Time:", execution_time)
