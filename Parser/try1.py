from tabulate import tabulate

# Define grammar rules using a dictionary
grammar_dict = {
    'Keywords': [['Keyword'], ['Keyword', 'Keywords'], ['']],
    'Keyword': [['int'], ['float'], ['char'], ['if'], ['else if'], ['else'], ['while'], ['for'], ['return']],

    'Strings': [['DoubleQuoteString'], ['SingleQuoteString']],
    'DoubleQuoteString': [['"', "DoubleQuoteContent", '"']],
    'SingleQuoteString': [["'", "SingleQuoteContent", "'"]],
    'DoubleQuoteContent': [["NonQuoteCharacters"], ["EscapeCharacter"], ["DoubleQuoteString"]],
    'SingleQuoteContent': [["NonQuoteCharacters"], ["EscapeCharacter"], ["SingleQuoteString"]],
    'NonQuoteCharacter': [["Letters"], ["Digits"], ["SpecialSymbol"], ["Punctuator"]],
    'NonQuoteCharacters': [["NonQuoteCharacter", "NonQuoteCharacters"], ['']],
    'EscapeCharacter': [["\\"], ["\\n"], ["\\t"], ['\\"'], ["\\'"]],

    'Identifiers': [['Identifier'], ['Identifier', 'Identifiers'], ['']],
    'Identifier': [["Letters", "Anotherletter"], ["_", "Anotherletter"]],
    'Anotherletter': [[''], ["Character", "Anotherletter"]],
    'Character': [["Letters"], ["Digit"], ["_"]],
    'Letters': [['a'], ['b'], ['c'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'], ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z'], ['A'], ['B'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'], ['M'], ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'], ['Y'], ['Z']],
    'SpecialSymbol': [['!'], ['@'], ['£'], ['#'], ['$'], ['^'], ['&'], ['*'], ['+'], ['-'], ['_'], ['='], ['<'], ['>'], ['?']],
    'Punctuator': [['('], [')'], ['{'], ['}'], ['['], [']'], ['.'], [','], [';']],

    'Program': [['Type', 'Funcname', '(', 'Arglist', ')', '{', 'Statements', '}']],
    'Type': [['void'], ['int'], ['float'], ['double'], ['char']],
    'Funcname': [['main'], ['Identifier']],
    'Arglist': [['Identifier'], [''], ['Type', 'Identifier']],
    'Arglists': [['Arglist'], ['Arglist', 'Arglists'], ['']],
    'Statements': [['Statement', 'MoreStatements']],
    'MoreStatements': [['Statement', 'MoreStatements'], ['']],
    'Statement': [['Variabledec'], ['Ifstatement'], ['Whileloop'], ['Forloop'], ['Expression'], ['Returnstatement']],
    'Variabledec': [['Type', 'Identifier'], ['Type', 'Assignmentexp']],
    'Expression': [['Assignmentexp'], ['Logicalexp'], ['Equalityexp'], ['Arithmeticexp'], ['Relationalexp']],
    'Ifstatement': [['if', '(', 'Expression', ')', '{', 'Statements', '}'], 
                   ['if', '(', 'Expression', ')', '{', 'Statements', '}', 'else', '{', 'Statements', '}'], 
                   ['if', '(', 'Expression', ')', '{', 'Statements', '}', 'Elseifstatements', 'else', '{', 'Statements', '}']],
    'Elseifstatements': [['Elseifstatement'], ['Elseifstatement', 'Elseifstatements'], ['']],
    'Elseifstatement': [['else', 'if', '(', 'Expression', ')', '{', 'Statements', '}']],
    'Forloop': [['for', '(', 'Expression', ';', 'Expression', ';', 'Expression', ')', '{', 'Statements', '}']],
    'Whileloop': [['while', '(', 'Expression', ')', '{', 'Statements', '}']],
    'Returnstatement': [['return', 'Expression']],

    'Number': [['Integer'], ['Float']],
    'Integer': [['Sign', 'Digits'], ['Digits']],
    'Sign': [["+"], ["-"]],
    'Digits': [['Digit',], ['Digit', 'Digits'], ['']],
    'Digit': [['Zero'], ['Onetonine']],
    'Zero': [['0']],
    'Onetonine': [['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']],
    'Float': [['Sign', 'Digits', '.', 'Digits'], ['Digits', '.', 'Digits']],

    'Assignmentexp': [['Identifier', '=', 'Expression']],
    'Logicalexp': [['Expression', 'LogicalOp', 'Expression']],
    'LogicalOp': [['&&'], ['||']],
    'Relationalexp': [['Expression', 'RelationalOp', 'Expression']],
    'RelationalOp': [['<'], ['>'], ['<='], ['>=']],
    'Equalityexp': [['Expression', 'EqualityOp', 'Expression']],
    'EqualityOp': [['=='], ['!=']],
    'Arithmeticexp': [['Term'],['Arithmeticexp', 'ArithmeticOp', 'Term'], ['Term', 'IncrementalOp']],
    'ArithmeticOp': [['+'], ['-'], ['*'], ['/'], ['^'], ['%']],
    'IncrementalOp': [['++'], ['--']],
    'Term': [['Factor'],['Term', '*', 'Factor'],['Term', '/', 'Factor']],
    'Factor': [['Digit'],['Identifier'],['(', 'Arithmeticexp', ')']],

}

# Convert dictionary to string representation of the grammar
# grammar_string = "\n".join(f"{key} -> {' | '.join(' '.join(prod) for prod in value)}" for key, value in grammar_dict.items())

# # ##################### FIRST AND FOLLOW SETS ########################## #
# def find_first(grammar, non_terminal, visited=None, memo=None):
#     if visited is None:
#         visited = set()
#     if memo is None:
#         memo = {}
#     if non_terminal in visited:
#         return set()
#     visited.add(non_terminal)
#     if non_terminal in memo:
#         return memo[non_terminal]

#     first_set = set()
#     if non_terminal not in grammar:
#         first_set.add(non_terminal)
#     else:
#         for production in grammar[non_terminal]:
#             if production[0] != non_terminal:
#                 first_set |= find_first(grammar, production[0], visited, memo)
#             else:
#                 first_set |= find_first(grammar, production[1], visited, memo)
#     memo[non_terminal] = first_set
#     return first_set

# def find_follow(grammar, non_terminal, start_symbol, visited=None, memo=None):
#     if visited is None:
#         visited = set()
#     if memo is None:
#         memo = {}
#     if non_terminal in visited:
#         return set()
#     visited.add(non_terminal)
#     if non_terminal in memo:
#         return memo[non_terminal]

#     follow_set = set()
#     for symbol, productions in grammar.items():
#         for production in productions:
#             if non_terminal in production:
#                 index = production.index(non_terminal)
#                 if index == len(production) - 1:
#                     if symbol != non_terminal:
#                         follow_set |= find_follow(grammar, symbol, start_symbol, visited, memo)
#                 elif production[index + 1] not in grammar:
#                     follow_set.add(production[index + 1])
#                 else:
#                     first_of_next = find_first(grammar, production[index + 1], visited, memo) - {'#'}
#                     follow_set |= first_of_next
#                     if '#' in first_of_next:
#                         follow_set |= find_follow(grammar, symbol, start_symbol, visited, memo)
#     if non_terminal == start_symbol:
#         follow_set.add('$')
#     memo[non_terminal] = follow_set
#     return follow_set


# # ####################################### PARSE TABLE ########################################### #
# def parsing_table(grammar, first_sets, follow_sets):
#     tables = {}
#     for non_term, prods in grammar.items():
#         for prod in prods:
#             first_of_prod = find_first(grammar, prod[0])
#             for term in first_of_prod:
#                 if term != '#':
#                     tables[non_term, term] = prod
#             if '#' in first_of_prod:
#                 for term in follow_sets[non_term]:
#                     tables[non_term, term] = prod
#     headers = sorted(set(term for non_term, term in tables))
#     headers.insert(0, " ")
#     table = []
#     for non_term in grammar:
#         row = [non_term]
#         for term in headers[1:]:
#             row.append(tables.get((non_term, term), " "))
#         table.append(row)
#     return table

# # ####################################### STACK IMPLEMENTATION ################################## #
# # Define function to parse productions
# def parse_production(production):
#     if isinstance(production, list):
#         return production
#     else:
#         return production.split()

# # Convert string representation to CFG rules
# grammar_rules = []
# for key, value in grammar_dict.items():
#     for production in value:
#         grammar_rules.append((key, [parse_production(production)]))

# # Example usage: parsing a sentence
# def parse_sentence(sentence):
#   tokens = sentence.split()
#   stack = ["$"]
#   stack.append("Program")
#   input_tokens = tokens[:]
#   input_tokens.append("$")
#   input_tokens.reverse()

#   table = [["Stack", "Input", "Action"]]
#   while stack and input_tokens:
#     stack_str = " ".join(stack)
#     input_str = " ".join(input_tokens)
#     if stack[-1] == input_tokens[-1]:
#       action = "Match"
#       stack.pop()
#       input_tokens.pop()
#     else:
#       top_of_stack = stack[-1]
#       current_input_token = input_tokens[-1]
#       production = None
#       for non_terminal, expansion in grammar_rules:
#         if non_terminal == top_of_stack:
#           print(non_terminal)
#           for production in expansion:
#             print(f"{production} : {expansion}")
#             if production == [''] and expansion[0] == ['']:
#               print("MATCH FOUND: empty string")
#               break
#             if current_input_token == production[0]:
#               print("MATCH FOUND")
#               break
      
#           if production == [''] and expansion[0] == ['']:
#             break
#           if current_input_token == production[0]:
#             break
#       if production:
#         print("POPPING ", production)
#         stack.pop()
#         action = f"Derive {top_of_stack} -> {' '.join(production)}"
#         if production != ['']:
#           stack.extend(reversed(production))
#       else:
#         action = "Error"
#         break
#     table.append([stack_str, input_str, action])

#   print(tabulate(table, headers="firstrow", tablefmt="grid"))

#   # Check for successful parsing and print acceptance message
#   if stack == ["$"] and input_tokens == ["$"]:
#     print("Parsing successful! The string is accepted by the grammar.")
#   else:
#     print("Parsing failed! The string is rejected by the grammar.")

# # Example usage
# sentence = "int main ( ) { int x ; x = 42 ; return x ; }"  # Corrected sentence
# print("Input string: ", sentence)
# parse_sentence(sentence)

# ##################### FIRST AND FOLLOW SETS ########################## #
def find_first(grammar, non_terminal, visited=None, memo=None):
    if visited is None:
        visited = set()
    if memo is None:
        memo = {}
    if non_terminal in visited:
        return set()
    visited.add(non_terminal)
    if non_terminal in memo:
        return memo[non_terminal]

    first_set = set()
    if non_terminal not in grammar:
        first_set.add(non_terminal)
    else:
        for production in grammar[non_terminal]:
            if production[0] != non_terminal:
                first_set |= find_first(grammar, production[0], visited, memo)
            else:
                first_set |= find_first(grammar, production[1], visited, memo)
    memo[non_terminal] = first_set
    return first_set

def find_follow(grammar, non_terminal, start_symbol, visited=None, memo=None):
    if visited is None:
        visited = set()
    if memo is None:
        memo = {}
    if non_terminal in visited:
        return set()
    visited.add(non_terminal)
    if non_terminal in memo:
        return memo[non_terminal]

    follow_set = set()
    for symbol, productions in grammar.items():
        for production in productions:
            if non_terminal in production:
                index = production.index(non_terminal)
                if index == len(production) - 1:
                    if symbol != non_terminal:
                        follow_set |= find_follow(grammar, symbol, start_symbol, visited, memo)
                elif production[index + 1] not in grammar:
                    follow_set.add(production[index + 1])
                else:
                    first_of_next = find_first(grammar, production[index + 1], visited, memo) - {'#'}
                    follow_set |= first_of_next
                    if '#' in first_of_next:
                        follow_set |= find_follow(grammar, symbol, start_symbol, visited, memo)
    if non_terminal == start_symbol:
        follow_set.add('$')
    memo[non_terminal] = follow_set
    return follow_set


# ####################################### PARSE TABLE ########################################### #
def parsing_table(grammar, first_sets, follow_sets):
    tables = {}
    for non_term, prods in grammar.items():
        for prod in prods:
            first_of_prod = find_first(grammar, prod[0])
            for term in first_of_prod:
                if term != '#':
                    tables[non_term, term] = prod
            if '#' in first_of_prod:
                for term in follow_sets[non_term]:
                    tables[non_term, term] = prod
    headers = sorted(set(term for non_term, term in tables))
    headers.insert(0, " ")
    table = []
    for non_term in grammar:
        row = [non_term]
        for term in headers[1:]:
            row.append(tables.get((non_term, term), " "))
        table.append(row)
    return table

# ##################### FUNCTION TO PRINT FIRST AND FOLLOW SETS ########################## #
def print_first_sets(first_sets):
    print("First Sets:")
    for non_terminal, first_set in first_sets.items():
        print(f"{non_terminal}: {first_set}")

def print_follow_sets(follow_sets):
    print("\nFollow Sets:")
    for non_terminal, follow_set in follow_sets.items():
        print(f"{non_terminal}: {follow_set}")
        
def print_parse_table(grammar_dict):
    # Print out all non-terminals
    print("Non-terminals:")
    for non_terminal in grammar_dict.keys():
        print(non_terminal)

    # Print out numbered productions
    print("\nNumbered Productions:")
    production_num = 1
    for non_terminal, productions in grammar_dict.items():
        for production in productions:
            print(f"{production_num}. {non_terminal} -> {' '.join(production)}")
            production_num += 1

    # Print out everything that is not a non-terminal and is found in the production
    print("\nTerminals:")
    terminals = set()
    for productions in grammar_dict.values():
        for production in productions:
            for symbol in production:
                if symbol not in grammar_dict.keys():
                    terminals.add(symbol)
    for terminal in terminals:
        print(terminal)

    # Create a parse table as a 2D array
    non_terminals = list(grammar_dict.keys())
    terminals = list(terminals)
    parse_table = [[""] * (len(terminals) + 1) for _ in range(len(non_terminals) + 1)]

    # Populate index[1:][0] with a non-terminal in each index
    for i, non_terminal in enumerate(non_terminals):
        parse_table[i + 1][0] = non_terminal

    # Populate index[0][1:] with everything that is not a non-terminal
    parse_table[0][1:] = terminals

    # Leave index[0][0] empty
    parse_table[0][0] = ""

    # Iterate over each non-terminal symbol in the grammar rules
    for non_terminal, productions in grammar_dict.items():
        first_set = find_first(grammar_dict, non_terminal)
        follow_set = find_follow(grammar_dict, non_terminal, start_symbol="Program")
        
        # For each terminal symbol in the first set, populate the parse table with the production rule associated with that non-terminal symbol
        for terminal in first_set:
            if terminal != '#':
                for production in productions:
                    parse_table[non_terminals.index(non_terminal) + 1][terminals.index(terminal) + 1] = production
        
        # If the empty string '#' is in the first set, iterate over the follow set of the non-terminal symbol
        if '#' in first_set:
            for terminal in follow_set:
                for production in productions:
                    parse_table[non_terminals.index(non_terminal) + 1][terminals.index(terminal) + 1] = production

    # Print the first ten rows and columns of the parse table using tabulate
    first_five_rows = parse_table[:5]
    first_five_columns = [row[:5] for row in first_five_rows]

    # Ensure the first cell of the first row is empty
    first_five_columns[0][0] = ""

    # Populate the first row with terminals
    first_five_columns[0][1:] = terminals

    # Print the first five rows and columns
    print("\nFirst five rows and columns of the parse table:")
    print(tabulate(first_five_columns, headers="firstrow", tablefmt="grid"))

# ####################################### STACK IMPLEMENTATION ################################## #
# Define function to parse productions
def parse_production(production):
    if isinstance(production, list):
        return production
    else:
        return production.split()

# Convert string representation to CFG rules
grammar_rules = []
for key, value in grammar_dict.items():
    for production in value:
        grammar_rules.append((key, [parse_production(production)]))

# Example usage: parsing a sentence
def parse_sentence(sentence):
    tokens = sentence.split()
    stack = ["$"]
    stack.append("Program")
    input_tokens = tokens[:]
    input_tokens.append("$")
    input_tokens.reverse()

    table = [["Stack", "Input", "Action"]]
    while stack and input_tokens:
        stack_str = " ".join(stack)
        input_str = " ".join(input_tokens)
        if stack[-1] == input_tokens[-1]:
            action = "Match"
            stack.pop()
            input_tokens.pop()
        else:
            top_of_stack = stack[-1]
            current_input_token = input_tokens[-1]
            production = None
            for non_terminal, expansion in grammar_rules:
                if non_terminal == top_of_stack:
                    print(non_terminal)
                    for production in expansion:
                        print(f"{production} : {expansion}")
                        if production == [''] and expansion[0] == ['']:
                            print("MATCH FOUND: empty string")
                            break
                        if current_input_token == production[0]:
                            print("MATCH FOUND")
                            break

                    if production == [''] and expansion[0] == ['']:
                        break
                    if current_input_token == production[0]:
                        break
            if production:
                print("POPPING ", production)
                stack.pop()
                action = f"Derive {top_of_stack} -> {' '.join(production)}"
                if production != ['']:
                    stack.extend(reversed(production))
            else:
                action = "Error"
                break
        table.append([stack_str, input_str, action])

    print(tabulate(table, headers="firstrow", tablefmt="grid"))

    # Check for successful parsing and print acceptance message
    if stack == ["$"] and input_tokens == ["$"]:
        print("Parsing successful! The string is accepted by the grammar.")
    else:
        print("Parsing failed! The string is rejected by the grammar.")

# Example usage
sentence = "int main ( ) { int x ; x = 42 ; return x ; }"  # Corrected sentence
print("Input string: ", sentence)
parse_sentence(sentence)

# Calculate and print first sets
first_sets = {}
for non_terminal in grammar_dict:
    first_sets[non_terminal] = find_first(grammar_dict, non_terminal)
print_first_sets(first_sets)

# Calculate and print follow sets
start_symbol = "Program"  # Assuming "Program" is the start symbol
follow_sets = {}
for non_terminal in grammar_dict:
    follow_sets[non_terminal] = find_follow(grammar_dict, non_terminal, start_symbol)
print_follow_sets(follow_sets)

# Create and print parse table
parse_table = parsing_table(grammar_dict, first_sets, follow_sets)
print_parse_table(grammar_dict)
