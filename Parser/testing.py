from scanner2 import scan_file
from tabulate import tabulate
from collections import deque
import os
import sys

# Define grammar rules using a dictionary
grammar_dict = {
    'Program': [['Type', 'Identifier', '(', 'Arglists', ')', '{', 'Statements', '}']],
    'Type': [['Keyword']],
    'Arglists': [['Arglist'], ['Arglist', 'Arglists'], ['']],
    'Arglist': [['Type', 'Identifier']],
    'Statements': [['Statement', 'Statements'], ['']],
    'Statement': [['Ifstatement'], ['Whileloop'], ['Forloop'], ['Expression'], ['Returnstatement'], ['Variabledec']],
    'Ifstatement': [['if', '(', 'Expression', ')', '{', 'Statements', '}'],
                    ['if', '(', 'Expression', ')',
                     '{', 'Statements', '}', 'else', '{', 'Statements', '}'],
                    ['if', '(', 'Expression', ')', '{', 'Statements', '}', 'Elseifstatements', 'else', '{', 'Statements', '}']],
    'Elseifstatements': [['Elseifstatement'], ['Elseifstatement', 'Elseifstatements'], ['']],
    'Elseifstatement': [['else', 'if', '(', 'Expression', ')', '{', 'Statements', '}']],
    'Whileloop': [['while', '(', 'Expression', ')', '{', 'Statements', '}']],
    'Forloop': [['for', '(', 'Expression', ';', 'Expression', ';', 'Expression', ')', '{', 'Statements', '}']],
    'Returnstatement': [['Return', 'Value', ';'], ['Return', 'Identifier', ';']],
    'Variabledec': [['Type', 'Identifier', ';'], ['Type', 'Assignmentexp']],
    'Expression': [['Assignmentexp'], ['Logicalexp'], ['Equalityexp'], ['Arithmeticexp'], ['Relationalexp']],
    'Assignmentexp': [['Identifier', 'AssignmentOp', 'Value', ';']],
    'Value': [['String'], ['Integer'], ['Float']],
    'Operator': [['LogicalOp'], ['ArithmeticOp'], ['RelationalOp'], ['EqualityOp'], ['AssignmentOp']],
    'Logicalexp': [['Expression', 'LogicalOp', 'Expression']],
    'Relationalexp': [['Expression', 'RelationalOp', 'Expression']],
    'Equalityexp': [['Expression', 'EqualityOp', 'Expression']],
    'Arithmeticexp': [['Term'], ['Arithmeticexp', 'ArithmeticOp', 'Term'], ['Term', 'IncrementalOp'], ['Term', 'DecrementalOp']],
    'Term': [['Factor'], ['Term', 'Operator', 'Factor'], ['Term', 'Operator', 'Factor']],
    'Factor': [['Integer'], ['Float'], ['(', 'Arithmeticexp', ')']],
}

# Node class to represent parse tree nodes


class ParseTreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.value) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

    def pretty_print(self, prefix='', is_last=True):
        ret = prefix + ("└── " if is_last else "├── ") + str(self.value) + "\n"
        prefix += "    " if is_last else "│   "
        child_count = len(self.children)
        for i, child in enumerate(self.children):
            is_last_child = (i == child_count - 1)
            ret += child.pretty_print(prefix, is_last_child)
        return ret


class IntermediateCodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0

    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def generate_code(self, node):
        if not node.children:
            return node.value

        # Handle different types of nodes specifically
        if node.value == 'Assignmentexp':
            identifier = self.generate_code(node.children[0])
            operator = node.children[1].value
            value = self.generate_code(node.children[2])
            self.code.append((identifier, operator, value))
            return identifier

        elif node.value == 'Expression':
            return self.generate_code(node.children[0])

        elif node.value == 'Arithmeticexp':
            if len(node.children) == 1:
                return self.generate_code(node.children[0])
            else:
                left = self.generate_code(node.children[0])
                op = node.children[1].value
                right = self.generate_code(node.children[2])
                temp = self.new_temp()
                self.code.append((temp, '=', left, op, right))
                return temp

        elif node.value == 'Term':
            if len(node.children) == 1:
                return self.generate_code(node.children[0])
            else:
                left = self.generate_code(node.children[0])
                op = node.children[1].value
                right = self.generate_code(node.children[2])
                temp = self.new_temp()
                self.code.append((temp, '=', left, op, right))
                return temp

        elif node.value == 'Factor':
            if len(node.children) == 1:
                return self.generate_code(node.children[0])
            elif node.children[0].value == '(':
                return self.generate_code(node.children[1])

        # By default, handle node with single child
        if len(node.children) == 1:
            return self.generate_code(node.children[0])

        # General handling for other types of nodes
        for child in node.children:
            self.generate_code(child)

    def __repr__(self):
        return "\n".join([" ".join(instr) for instr in self.code])

# Define the generate_intermediate_code function
def generate_intermediate_code(parse_tree):
    icg = IntermediateCodeGenerator()
    icg.generate_code(parse_tree)
    return icg



def use_tokens():
    input_file = 'mini2.c'
    tokens = scan_file(input_file)
    all_tokens = [token for sublist in tokens for token in sublist]
    return all_tokens


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
                        first_of_next = find_first(
                            grammar, next_symbol, visited, memo) - {''}
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
                        follow_set |= find_follow(
                            grammar, symbol, start_symbol, visited, memo)
    memo[non_terminal] = follow_set
    return follow_set


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


def parse_sentence(grammar, parse_table, tokens):
    print("Tokens: ", tokens)
    tokens.append(('$', '$'))
    stack = deque(['$', 'Program'])
    root = ParseTreeNode('Program')
    parse_tree_stack = deque([root])
    actions = []

    index = 0
    while stack:
        top = stack.pop()
        current_token_type, current_token_value = tokens[index]

        # Synchronize the parse tree stack
        if parse_tree_stack:
            current_tree_node = parse_tree_stack.pop()
        else:
            current_tree_node = None

        if top == current_token_value or top == current_token_type:
            index += 1
            actions.append(("Match", top, " ".join(
                token[1] for token in tokens[index:])))
            if top == 'EOF':
                break
        elif (top, current_token_type) in parse_table:
            production = parse_table[(top, current_token_type)]
            if production != ['']:
                print(f"Production: {top} : {' '.join(production)}")
                stack.extend(production[::-1])

                # Add new nodes to parse tree stack
                new_nodes = [ParseTreeNode(symbol)
                             for symbol in production[::-1]]
                for node in new_nodes:
                    if current_tree_node is not None:
                        current_tree_node.add_child(node)
                parse_tree_stack.extend(new_nodes)
            actions.append((f"Derive {top} -> {' '.join(production)}",
                           " ".join(token[1] for token in tokens[index:]), list(stack)))
        elif top in grammar and [''] in grammar[top]:
            print(f"Handling lambda production for {top}")
            actions.append(
                (f"Derive {top} -> λ", " ".join(token[1] for token in tokens[index:]), list(stack)))
        else:
            print(f"Exiting on Production: {top} : {current_token_value}")
            actions.append(("Error", (top, current_token_value),
                           " ".join(token[1] for token in tokens[index:])))
            break

    print(tabulate(actions, headers=[
          "Action", "Input", "Stack"], tablefmt="grid"))
    if stack or index < len(tokens):
        print("Parsing failed! The string is rejected by the grammar.")
    else:
        print("Parsing successful! The string is accepted by the grammar.")
        print("Parse Tree:")
        print(root.pretty_print())

        icg = generate_intermediate_code(root)
        print("Intermediate Code:")
        print(icg)


if __name__ == "__main__":
    tokens = use_tokens()
    print(tokens)
    first_sets = {nt: find_first(grammar_dict, nt) for nt in grammar_dict}
    follow_sets = {nt: find_follow(grammar_dict, nt, 'Program')
                   for nt in grammar_dict}

    parse_table = parsing_table(grammar_dict, first_sets, follow_sets)

    terminals = sorted(set(term for _, term in parse_table.keys()))
    headers = ["Non-Terminal"] + terminals
    parse_sentence(grammar_dict, parse_table, tokens)
