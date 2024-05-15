from tabulate import tabulate
from CFG import grammar

def findingFirstSets(grammar):
    """
    Recursive function that computes the first sets for a given non terminal.

    Args:
        nonTerminals (str): The non-terminal symbol.
        visited: set of visited symbols

    Return:
        firstSet: the computed First set, which is a set of terminal symbols.

    Description:
        If the non-terminal symbol is already visited or a terminal symbol,  returns an empty set
        or a set containing the symbol itself, respectively.
        If the non-terminal symbol is an empty string, it returns a set with an empty string.
        Otherwise, iterates through the productions of the non-terminal symbol in the grammar dictionary,
        recursively computes the First set for each symbol in the production, and updates the First set accordingly.
    """

    firstSets = {}

    for nonTerminal in grammar:
        firstSets[nonTerminal] = set()

    def computeFirst(nonTerminals, visited):
        if nonTerminals in visited:
            return set()
        visited.add(nonTerminals)

        if nonTerminals in terminals:
            return {nonTerminals}

        elif nonTerminals == '':
            return {''}
        else:
            first = set()

            for production in grammar[nonTerminals]:
                for i, nonTerminals_i in enumerate(production):
                    first_i = computeFirst(nonTerminals_i, visited)
                    first.update(first_i)
                    if '' not in first_i:
                        break
                    if i == len(production) - 1:
                        first.add('')
            return first

    for nonTerminals in grammar:
        visited = set()
        firstSets[nonTerminals].update(computeFirst(nonTerminals, visited))

    return firstSets


def findingFollowSets(grammar, firstSets, terminals):
    """
    A function to compute the follow sets for a given context-free grammar (CFG).

    Args:
        grammar: The context-free grammars represented as a dictionary.
        firstSets: The first sets of the non-terminals.
        terminals: The set of terminal symbols in the grammar.

    Returns:
    - followSets: dictionary containing the follow sets for each non-terminal symbol.
    """
    followSets = {}

    for nonTerminal in grammar:
        followSets[nonTerminal] = set()

    followSets[startSymbol].add('$')

    def computeFollowSets(nonTerminal, visited):
        if nonTerminal in visited:
            return
        visited.add(nonTerminal)

        for nonTerminals in grammar:
            for production in grammar[nonTerminals]:
                # Checks if current non terminal is in the production
                if nonTerminal in production:
                    indexing = production.index(nonTerminal)
                    # If it is, assign an index
                    if indexing < len(production) - 1:
                        for symbol in production[indexing + 1:]:
                            if symbol in terminals:  # If a terminal, include it
                                followSets[nonTerminal].add(symbol)
                            elif symbol in grammar:  # If it's a non terminal, take the first set
                                followSets[nonTerminal].update(
                                    firstSets[symbol] - {''})
                                if '' in firstSets[symbol]:
                                    computeFollowSets(symbol, visited)

                    # Rule 3: If non terminal is the last symbol at RH production or empty,
                    # Updates the follow with the follow of LH non terminal
                    if indexing == len(production) - 1 or '' in firstSets.get(production[indexing + 1], []):
                        followSets[nonTerminal].update(followSets[nonTerminals])
                        computeFollowSets(nonTerminals, visited)

    # Iterate through each non-terminal
    for nonTerminal in grammar:
        visited = set()
        computeFollowSets(nonTerminal, visited)

    return followSets
# Getting terminal symbols
terminals = []
for RH_Production in grammar.values():
    for production in RH_Production:
        for anySymbol in production:
            if anySymbol not in grammar and anySymbol != '':
                terminals.append(anySymbol)

terminals = set(terminals)


firstSets = findingFirstSets(grammar)
print("Non Terminals First sets")
for nonTerminals, firstSet in firstSets.items():
    print("-First(" + nonTerminals + "):", firstSet)

startSymbol = list(grammar.keys())[0]
followSets = findingFollowSets(grammar, firstSets, terminals)
print("\nNon Terminals Follow Sets")
for nonTerminal, followSet in followSets.items():
    print("-Follow(" + nonTerminal + "):", followSet)

#==============Code added from here=============
# Create the parse table structure
# Create the parse table structure
parse_table = {}
for nonTerminal in grammar:
  parse_table[nonTerminal] = {}
  for terminal in terminals:
    parse_table[nonTerminal][terminal] = None

# Populate the parse table
for nonTerminal, productions in grammar.items():
  for production in productions:
    # Check for empty production (epsilon)
    if production == []:
      parse_table[nonTerminal]['$'] = production
      continue

    # Check if the first symbol in the production is a terminal
    if production and production[0] in terminals:
      parse_table[nonTerminal][production[0]] = production

    # More complex case: Non-terminal as the first symbol
    else:
      first_i = firstSets.get(production[0], set())
      for symbol in first_i:
        if symbol == '':
          # Check follow of the first non-terminal
          follow_nt = followSets[production[0]]
          for follow_symbol in follow_nt:
            parse_table[nonTerminal][follow_symbol] = production
        else:
          parse_table[nonTerminal][symbol] = production

# Print the parse table
print("\nParse Table:")
print(tabulate(parse_table, headers=list(terminals) + ['$'], showindex=True))

#==============Code added till here=============

#===Previous code (replaced) from here to the end of the file====
# parse_table = {}

# def get_production_number(non_terminal, production):
#     """
#     Gets the production number based on the non-terminal and the production.

#     Args:
#         non_terminal: non-terminal symbol.
#         production: production itself

#     Returns:
#         Production number corresponding to the non-terminal and production.
#     """
#     return production_numbers[(non_terminal, tuple(production))]


# # Define production_numbers dictionary and populate it with production numbers
# production_numbers = {}
# count = 1
# for non_terminal, productions in grammar.items():
#     for production in productions:
#         production_numbers[(non_terminal, tuple(production))] = count
#         count += 1

# # Iterate over non-terminals
# for non_terminal, productions in grammar.items():
#     for production in productions:
#         # If production is ε, add follow set of non-terminal to parse table
#         if production == ['ε']:
#             for terminal in followSets[non_terminal]:
#                 if (non_terminal, terminal) in parse_table:
#                     # print("Conflict detected:", (non_terminal, terminal))
#                     pass
#                 parse_table[(non_terminal, terminal)] = get_production_number(non_terminal, production)
#         else:
#             # Get First set of production
#             first_set = set()
#             for symbol in production:
#                 print("***Symbol: ", symbol)
#                 if symbol in terminals or symbol == 'ε':
#                     first_set.add(symbol)
#                 else:
#                     first_set.update(firstSets[symbol])
#                     if '' not in firstSets[symbol]:
#                         break
#             # Add production number to parse table for each terminal in First set
#             for terminal in first_set:
#                 if (non_terminal, terminal) in parse_table:
#                     # print("Conflict detected:", (non_terminal, terminal))
#                     pass
#                 parse_table[(non_terminal, terminal)] = get_production_number(non_terminal, production)

# # print("\nParse Table:")
# # for key, value in parse_table.items():
# #     print(key, ":", value)


# # Extract non-terminals (column names) and terminals (row names)
# non_terminals = set(grammar.keys())  # Convert non-terminals to a set for efficient lookup
# terminals = set()
# for rules in grammar.values():
#     for rule in rules:
#         for item in rule:
#             if item not in non_terminals:
#                 terminals.add(item)

# # Convert terminals set to list for printing
# terminals_list = list(terminals)

# # Create 2D array with non-terminals in the first column and terminals in the first row
# array_2d = [[''] + terminals_list]  # Initialize the array with an empty cell in the top-left corner
# for non_terminal in non_terminals:
#     array_2d.append([non_terminal] + [''] * len(terminals_list))

# # Populate the first row with terminals, each value having its own index
# for i, terminal in enumerate(terminals_list, start=1):  # Start from index 1 since the first column is non-terminals
#     array_2d[0][i] = terminal

# # # Display the entire first row with terminals
# # print("First Row with Terminals:", *terminals_list)

# # # Display the entire first column with non-terminals
# # print("First Column with Non-Terminals:")
# # for non_terminal in non_terminals:
# #     print(non_terminal)

# # # print("\nParse Table:")
# # # for non_terminal in non_terminals:
# # #     for terminal in terminals_list:
# # #         if (non_terminal, terminal) in parse_table:
# # #             print(f"{non_terminal} -> {terminal} : {parse_table[(non_terminal, terminal)]}")
# # #         else:
# # #             print(f"{non_terminal} -> {terminal} : ")