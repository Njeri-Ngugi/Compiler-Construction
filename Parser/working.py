from tabulate import tabulate
from CFG import grammar

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
                    first_of_next = find_first(grammar, production[index + 1]) - {'#'}
                    if '#' in find_first(grammar, production[index + 1]):
                        follow_set |= find_follow(grammar, symbol, start_symbol, follow_set)
                    follow_set |= first_of_next
    if non_terminal == start_symbol:
        follow_set.add('$')
    return follow_set


def generate_parse_table(grammar, first_sets, follow_sets):
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
    headers = list(set(terminal for non_terminal, terminal in tables))
    headers.sort()
    headers.insert(0, " ")
    table = []
    for non_terminal in grammar:
        row = [non_terminal]
        for terminal in headers[1:]:
            row.append(tables.get((non_terminal, terminal), " "))
        table.append(row)
    print(tabulate(table, headers, tablefmt="grid"))
    return tables

def ll1_algorithm(parse_tables, start_symbol, input_string):
    stack = ["$"]
    stack.append(start_symbol)
    input_string = input_string.split()
    input_string.append("$")
    input_string.reverse()

    header = ["stack", "input", "action"]
    parse_table = []
    while stack and input_string:
        row = [stack, ' '.join(input_string)]
        if stack[-1] == input_string[-1] == "$":
            row.append("String accepted")
            parse_table.append(row)
            break
        if stack[-1] == input_string[-1]:
            stack.pop()
            input_string.pop()
            row.append("pop")
            parse_table.append(row)
        else:
            production = parse_tables.get((stack[-1], input_string[-1]))
            if production is None:
                row.append("String not accepted")
                parse_table.append(row)
                break
            stack.pop()
            if production != "#":
                production = list(production)
                production.reverse()
                stack += production
            row.append(production)
            parse_table.append(row)
        if not stack:
            stack.append("$")
        if not input_string:
            input_string.append("$")
    print(tabulate(parse_table, header, tablefmt="grid"))
    return


def main():
  start_symbol = list(grammar.keys())[0]
  first_sets = {non_terminal: find_first(grammar, non_terminal) for non_terminal in grammar}
  follow_sets = {non_terminal: find_follow(grammar, non_terminal, start_symbol) for non_terminal in grammar}


  print("\nFIRST sets:")
  for non_terminal, first_set in first_sets.items():
    print(f"-FIRST({non_terminal}) = {first_set}")
  print("\nFOLLOW sets:")
  for non_terminal, follow_set in follow_sets.items():
    print(f"-FOLLOW({non_terminal}) = {follow_set}")

  print("\nParse Table:")
  parse_table = generate_parse_table(grammar, first_sets, follow_sets)
  input_string = "int main() { return 0; }"
  ll1_algorithm(parse_table, start_symbol, input_string)

if __name__ == "__main__":
  main()
