from tabulate import tabulate
import sys
import os

# import scanner from Scanner_Program in parent dir
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from Scanner_Program.scanner import scan_file


grammar = {
    'Program': [['int', 'main', 'OpenParen', 'CloseParen', 'OpenBrace', 'Stmts', 'ReturnStmt' ,'CloseBrace']],
    'Stmts': [['Declaration'], ['Assignment'], ['Arithmetic']],
    'Declaration': [['Type', 'Identifier', ';']],
    'Assignment': [['Type', 'Identifier', '=', 'Num', ';']],
    'Type': [['int'], ['char'], ['float']],
    'Identifier': [['x'], ['y']],
    'ReturnStmt': [['return', '0', ';']],
    'Arithmetic': [['Num', 'Op', 'Num', ';']],
    'Num': [['0']],
    'Op': [['+']],
    'OpenParen': [['(']],
    'CloseParen': [[')']],
    'OpenBrace': [['{']],
    'CloseBrace': [['}']],
}

def find_first(grammar, non_terminal, visited=None):
    if visited is None:
        visited = set()
    if non_terminal not in grammar:
        return {non_terminal}
    first_set = set()
    for production in grammar[non_terminal]:
        if production[0] == non_terminal and non_terminal not in visited:
            visited.add(non_terminal)
            first_set |= find_first(grammar, production[1], visited)
        else:
            first_set |= find_first(grammar, production[0], visited)
    return first_set

def find_follow(grammar, non_terminal, start_symbol, follow_set=None):
    if follow_set is None:
        follow_set = set()
    for symbol, productions in grammar.items():
        for production in productions:
            if non_terminal in production:
                index = production.index(non_terminal)
                if index == len(production) - 1:
                    if symbol != non_terminal:
                        follow_set |= find_follow(grammar, symbol, start_symbol, follow_set)
                elif production[index + 1] not in grammar:
                    follow_set.add(production[index + 1])
                elif production[index + 1] in grammar:
                    first_of_next = find_first(grammar, production[index + 1]) - {''}
                    if '' in first_of_next:
                        follow_set |= find_follow(grammar, symbol, start_symbol, follow_set)
                    follow_set |= first_of_next
    if non_terminal == start_symbol:
        follow_set.add('$')
    return follow_set

def generate_parse_table(grammar, first_sets, follow_sets, filename):
    tables = {}
    for non_terminal, productions in grammar.items():
        for production in productions:
            first_of_production = find_first(grammar, production[0])
            for terminal in first_of_production:
                if terminal != '#':
                    tables[non_terminal, terminal] = production
            if '#' in first_of_production:
                for terminal in follow_sets[non_terminal]:
                    tables[non_terminal, terminal] = production

    # Create table data
    headers = list(set(terminal for non_terminal, terminal in tables))
    headers.sort()
    headers.insert(0, " ")
    table = []
    for non_terminal in grammar:
        row = [non_terminal]
        for terminal in headers[1:]:
            row.append(tables.get((non_terminal, terminal), " "))
        table.append(row)

    # Save table to file
    with open(filename, "w") as file:
        file.write(tabulate(table, headers, tablefmt="grid"))

    print(f"\nSuccess: Parse table saved to {filename}\n")
    return tables


def ll1_algorithm(parse_table, start_symbol, token_list):
    stack = ["$"]
    stack.append(start_symbol)
    input_string = [token[1] for token in token_list]
    input_string.append("$")
    input_string.reverse()

    header = ["stack", "input", "action"]
    table = []
    while stack and input_string:
        row = [stack, list(input_string)]

        if stack[-1] == input_string[-1] == "$":
            row.append("String accepted")
            table.append(row)
            break

        if stack[-1] == input_string[-1]:
            stack.pop()
            input_string.pop()
            row.append("pop")
            table.append(row)
        else:
            production = parse_table.get((stack[-1], input_string[-1]))
            print("Production: ", production)
            if production is None:
                row.append(f"Syntax error at token {input_string[-1]}")
                table.append(row)
                break
            stack.pop()
            if production != "#":
                production = list(production)
                production.reverse()
                stack += production
            row.append(production)
            table.append(row)

        if not stack:
            stack.append("$")
        if not input_string:
            input_string.append("$")

    print(tabulate(table, header, tablefmt="grid") + "\n")
    return



def use_tokens():
    input_file = '../Scanner_Program/mini2.c'
    tokens = scan_file(input_file)
    all_tokens = [token for sublist in tokens for token in sublist]
    return all_tokens

if __name__ == "__main__":
    tokens = use_tokens()

    start_symbol = list(grammar.keys())[0]
    first_sets = {non_terminal: find_first(grammar, non_terminal) for non_terminal in grammar}
    follow_sets = {non_terminal: find_follow(grammar, non_terminal, start_symbol) for non_terminal in grammar}

    print("\nFIRST sets:")
    for non_terminal, first_set in first_sets.items():
        print(f"-FIRST({non_terminal}) = {first_set}")

    print("\nFOLLOW sets:")
    for non_terminal, follow_set in follow_sets.items():
        print(f"-FOLLOW({non_terminal}) = {follow_set}")

    parse_table = generate_parse_table(grammar, first_sets, follow_sets, "parse_table.txt")


    # parsing
    ll1_algorithm(parse_table, start_symbol, tokens)