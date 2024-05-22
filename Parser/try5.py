
from tabulate import tabulate
from collections import deque

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
    #'Identifiers': [['Identifier'], ['Identifier', 'Identifiers'], ['']],

    'Identifier': [['Letters', 'Anotherletter', 'Assignedvalue'], ["_", 'Anotherletter', 'Assignedvalue']],
    'Assignedvalue': [['Assignmentexp']],


    'Identifier': [["Letters", "Anotherletter"], ["_", "Anotherletter"]],
    'Anotherletter': [[''], ["Character", "Anotherletter"]],
    'Character': [["Letters"], ["Digit"], ["_"]],
    'Letters': [['a'], ['b'], ['c'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'], ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z'], ['A'], ['B'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'], ['M'], ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'], ['Y'], ['Z']],
    'SpecialSymbol': [['!'], ['@'], ['£'], ['#'], ['$'], ['^'], ['&'], ['*'], ['+'], ['-'], ['_'], ['='], ['<'], ['>'], ['?']],
    'Punctuator': [['('], [')'], ['{'], ['}'], ['['], [']'], ['.'], [','], [';']],
    'Program': [['Type', 'Funcname', '(', 'Arglist', ')', '{', 'Statements', '}']],
    'Type': [['void'], ['int'], ['float'], ['double'], ['char']],
    'Funcname': [['main'], ['Identifier']],
    'Arglist': [['Type', 'Identifier'], ['']],
    'Arglists': [['Arglist'], ['Arglist', 'Arglists'], ['']],
    'Statements': [['Statement', 'MoreStatements']],
    'MoreStatements': [['Statement', 'MoreStatements'], ['']],
    'Statement': [['Variabledec'], ['Ifstatement'], ['Whileloop'], ['Forloop'], ['Expression'], ['Returnstatement']],
    'Variabledec': [['Type', 'Identifier', ';'], ['Type', 'Assignmentexp', ';']],
    'Expression': [['Assignmentexp'], ['Logicalexp'], ['Equalityexp'], ['Arithmeticexp'], ['Relationalexp']],




    'Ifstatement': [['if', '(', 'Expression', ')', '{', 'Statements', '}'], 
                    ['if', '(', 'Expression', ')', '{', 'Statements', '}', 'else', '{', 'Statements', '}'], 
                    ['if', '(', 'Expression', ')', '{', 'Statements', '}', 'Elseifstatements', 'else', '{', 'Statements', '}']],
    'Elseifstatements': [['Elseifstatement'], ['Elseifstatement', 'Elseifstatements'], ['']],
    'Elseifstatement': [['else', 'if', '(', 'Expression', ')', '{', 'Statements', '}']],
    'Forloop': [['for', '(', 'Expression', ';', 'Expression', ';', 'Expression', ')', '{', 'Statements', '}']],
    'Whileloop': [['while', '(', 'Expression', ')', '{', 'Statements', '}']],
    
    'Returnstatement': [['return', 'Identifier']],


    
    'Number': [['Integer'], ['Float']],
    'Integer': [['Sign', 'Digits'], ['Digits']],
    'Sign': [["+"], ["-"]],
    'Digits': [['Digit'], ['Digit', 'Digits'], ['']],
    'Digit': [['Zero'], ['Onetonine']],
    'Zero': [['0']],
    'Onetonine': [['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']],
    'Float': [['Sign', 'Digits', '.', 'Digits'], ['Digits', '.', 'Digits']],
    'Assignmentexp': [['Identifier', '=', 'Onetonine']],
    #'Assignedvalue': [['Number'], ['Letters'], ['SpecialSymbol'], ['Strings']],
    'Logicalexp': [['Expression', 'LogicalOp', 'Expression']],
    'LogicalOp': [['&&'], ['||']],
    'Relationalexp': [['Expression', 'RelationalOp', 'Expression']],
    'RelationalOp': [['<'], ['>'], ['<='], ['>=']],
    'Equalityexp': [['Expression', 'EqualityOp', 'Expression']],
    'EqualityOp': [['=='], ['!=']],
    'Arithmeticexp': [['Term'], ['Arithmeticexp', 'ArithmeticOp', 'Term'], ['Term', 'IncrementalOp']],
    'ArithmeticOp': [['+'], ['-'], ['*'], ['/'], ['^'], ['%'], ['-', '-'], ['+','+']],
    'Term': [['Factor'], ['Term', '*', 'Factor'], ['Term', '/', 'Factor']],
    'Factor': [['Digit'], ['Identifier'], ['(', 'Arithmeticexp', ')']],
}

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
            if production[0] == '':
                first_set.add('')
            else:
                for symbol in production:
                    symbol_first = find_first(grammar, symbol, visited, memo)
                    first_set |= symbol_first
                    if '' not in symbol_first:
                        break
                    first_set.discard('')
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
    if non_terminal == start_symbol:
        follow_set.add('$')
    for symbol, productions in grammar.items():
        for production in productions:
            if non_terminal in production:
                index = production.index(non_terminal)
                while index < len(production) - 1:
                    next_symbol = production[index + 1]
                    if next_symbol in grammar:
                        first_of_next = find_first(grammar, next_symbol, visited, memo) - {''}
                        follow_set |= first_of_next
                        if '' in find_first(grammar, next_symbol, visited, memo):
                            index += 1
                        else:
                            break
                    else:
                        follow_set.add(next_symbol)
                        break
                else:
                    if symbol != non_terminal:
                        follow_set |= find_follow(grammar, symbol, start_symbol, visited, memo)
    memo[non_terminal] = follow_set
    return follow_set

# ####################################### PARSE TABLE ########################################### #
def parsing_table(grammar, first_sets, follow_sets):
    tables = {}
    for non_term, prods in grammar.items():
        for prod in prods:
            first_of_prod = find_first(grammar, prod[0])
            for term in first_of_prod:
                if term != '':
                    tables[non_term, term] = prod
            if '' in first_of_prod:
                for term in follow_sets[non_term]:
                    tables[non_term, term] = prod
    return tables

# ##################### FUNCTION TO PRINT FIRST AND FOLLOW SETS ####################### #
def print_sets(sets, title):
    headers = [title, "Set"]
    table = [[symbol, ', '.join(sorted(set_))] for symbol, set_ in sets.items()]
    print(tabulate(table, headers=headers, tablefmt="grid"))

# ##################### FUNCTION TO PRINT PARSE TABLE ####################### #
def print_parse_table(parse_table, headers):
    table = []
    non_terminals = set(non_term for non_term, term in parse_table)
    for non_term in non_terminals:
        row = [non_term]
        for term in headers[1:]:
            row.append(' '.join(parse_table.get((non_term, term), " ")))
        table.append(row)
    print(tabulate(table, headers=headers, tablefmt="grid"))

# ####################################### PARSING FUNCTION ########################################### #
def parse_sentence(grammar, parse_table, sentence):
    print("Input string: ", sentence)
    tokens = sentence.split()
    tokens.append('$')
    stack = deque(['$', 'Program'])
    actions = []

    while stack:
        top = stack.pop()
        current_token = tokens[0]

        if top == current_token:
            tokens.pop(0)
            actions.append(("Match", top, " ".join(tokens)))
            if top == '$':
                break
        elif (top, current_token) in parse_table:
            production = parse_table[(top, current_token)]
            if production != ['']:
                print(f"Production: {top} : {current_token}")
                stack.extend(production[::-1])
            actions.append((f"Derive {top} -> {' '.join(production)}", " ".join(tokens), list(stack)))
        else:
            print(f"Exiting on Production: {top} : {current_token}")
            actions.append(("Error", (top, current_token), " ".join(tokens)))
            break

    print(tabulate(actions, headers=["Action", "Input", "Stack"], tablefmt="grid"))
    if stack or tokens:
        print("Parsing failed! The string is rejected by the grammar.")
    else:
        print("Parsing successful! The string is accepted by the grammar.")




# ##################### MAIN EXECUTION ##################### #
first_sets = {nt: find_first(grammar_dict, nt) for nt in grammar_dict}
follow_sets = {nt: find_follow(grammar_dict, nt, 'Program') for nt in grammar_dict}

parse_table = parsing_table(grammar_dict, first_sets, follow_sets)

# print_sets(first_sets, "FIRST")
# print_sets(follow_sets, "FOLLOW")

# Create headers for the parse table
terminals = sorted(set(term for _, term in parse_table.keys()))
headers = ["Non-Terminal"] + terminals

# print_parse_table(parse_table, headers)

# Example usage
sentence = "int main ( ) { int x = 4 ; return x }"
parse_sentence(grammar_dict, parse_table, sentence)