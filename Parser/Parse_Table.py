from tabulate import tabulate
from CFG import CFGs

def findingFirstSets(CFGs):
    firstSets = {}  # Dictionary to store first sets

    for nonTerminals in CFGs:
        firstSets[nonTerminals] = set()

    # Computes First set of nonTerminals recursively
    def computeFirst(nonTerminals, visited):
        # Already visited, return an empty set to break the cycle
        if nonTerminals in visited:
            return set()
        visited.add(nonTerminals)

        # If the non terminal is a terminal, add it to the first set
        if nonTerminals in terminals:
            return {nonTerminals}  # First set is a terminal

        # Handles ε productions
        elif nonTerminals == '':
            return {''}
        else:
            first = set()  # Stores first set of current non Terminal symbol

            # Loop through RH_Production for a given non Terminal
            for production in CFGs[nonTerminals]:
                # Iterate through every Symbol in a single production rule
                for i, nonTerminals_i in enumerate(production):
                    # Compute First of the first Symbol in production
                    first_i = computeFirst(nonTerminals_i, visited)
                    # Add First(of_firstsymbol) seen
                    first.update(first_i)
                    # If First(of_firstsymbol) does not contain lambda, stop
                    if '' not in first_i:
                        break
                    # If it's the last anySymbol in the production, add ε to First(of_firstsymbol)
                    if i == len(production) - 1:
                        first.add('')
            return first

    # Iterate through non-terminals and compute their First sets
    for nonTerminals in CFGs:
        visited = set()
        firstSets[nonTerminals].update(computeFirst(nonTerminals, visited))

    return firstSets


def findingFollowSets(CFGs, firstSets, terminals):
    followSets = {}  # Dictionary to store follow sets

    # Initialize follow sets for each non-terminal
    for nonTerminal in CFGs:
        followSets[nonTerminal] = set()

    # Add $ as a follow set of start symbol first rule
    followSets[startSymbol].add('$')

    # Compute follow sets
    def computeFollowSets(nonTerminal, visited):
        if nonTerminal in visited:
            return
        visited.add(nonTerminal)

        for nonTerminals in CFGs:
            for production in CFGs[nonTerminals]:
                # Checks if current non terminal is in the production
                if nonTerminal in production:
                    indexing = production.index(nonTerminal)
                    # If it is, assign an index
                    if indexing < len(production) - 1:
                        for symbol in production[indexing + 1:]:
                            if symbol in terminals:  # If a terminal, include it
                                followSets[nonTerminal].add(symbol)
                            elif symbol in CFGs:  # If it's a non terminal, take the first set
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
    for nonTerminal in CFGs:
        visited = set()
        computeFollowSets(nonTerminal, visited)

    return followSets


# Getting terminal symbols
terminals = []
for RH_Production in CFGs.values():  # Get the values of the dictionary
    for production in RH_Production:  # Iterate over the values in the production rule
        for anySymbol in production:
            if anySymbol not in CFGs and anySymbol != '':  # If it's not a key in the CFG and is not empty, it's a terminal
                terminals.append(anySymbol)

terminals = set(terminals)


# First sets computation for each non-terminal
firstSets = findingFirstSets(CFGs)
print("Non Terminals First sets")
for nonTerminals, firstSet in firstSets.items():
    print("\tFirst(" + nonTerminals + "):", firstSet)

# Follow sets computation for each non terminal

# Start symbol from the CFG
# Can be changed to program once we have the full CFG
startSymbol = "Keywords"
followSets = findingFollowSets(CFGs, firstSets, terminals)
print("\nNon Terminals Follow Sets")
# Printing Follow sets
for nonTerminal, followSet in followSets.items():
    print("\tFollow(" + nonTerminal + "):", followSet)


# Populate the parse table with production numbers based on First and Follow sets
parse_table = {}

# Define function to get production number
def get_production_number(non_terminal, production):
    return production_numbers[(non_terminal, tuple(production))]

# Define production_numbers dictionary and populate it with production numbers
production_numbers = {}
count = 1
for non_terminal, productions in CFGs.items():
    for production in productions:
        production_numbers[(non_terminal, tuple(production))] = count
        count += 1

# Iterate over non-terminals
for non_terminal, productions in CFGs.items():
    for production in productions:
        # If production is ε, add follow set of non-terminal to parse table
        if production == ['ε']:
            for terminal in followSets[non_terminal]:
                if (non_terminal, terminal) in parse_table:
                    print("Conflict detected:", (non_terminal, terminal))
                parse_table[(non_terminal, terminal)] = get_production_number(non_terminal, production)
        else:
            # Get First set of production
            first_set = set()
            for symbol in production:
                if symbol in terminals or symbol == 'ε':
                    first_set.add(symbol)
                else:
                    first_set.update(firstSets[symbol])
                    if '' not in firstSets[symbol]:
                        break
            # Add production number to parse table for each terminal in First set
            for terminal in first_set:
                if (non_terminal, terminal) in parse_table:
                    print("Conflict detected:", (non_terminal, terminal))
                parse_table[(non_terminal, terminal)] = get_production_number(non_terminal, production)

print("\nParse Table:")
for key, value in parse_table.items():
    print(key, ":", value)


# Extract non-terminals (column names) and terminals (row names)
non_terminals = set(CFGs.keys())  # Convert non-terminals to a set for efficient lookup
terminals = set()
for rules in CFGs.values():
    for rule in rules:
        for item in rule:
            if item not in non_terminals:
                terminals.add(item)

# Convert terminals set to list for printing
terminals_list = list(terminals)

# Create 2D array with non-terminals in the first column and terminals in the first row
array_2d = [[''] + terminals_list]  # Initialize the array with an empty cell in the top-left corner
for non_terminal in non_terminals:
    array_2d.append([non_terminal] + [''] * len(terminals_list))

# Populate the first row with terminals, each value having its own index
for i, terminal in enumerate(terminals_list, start=1):  # Start from index 1 since the first column is non-terminals
    array_2d[0][i] = terminal

# Display the entire first row with terminals
print("First Row with Terminals:", *terminals_list)

# Display the entire first column with non-terminals
print("First Column with Non-Terminals:")
for non_terminal in non_terminals:
    print(non_terminal)

print("\nParse Table:")
for non_terminal in non_terminals:
    for terminal in terminals_list:
        if (non_terminal, terminal) in parse_table:
            print(f"{non_terminal} -> {terminal} : {parse_table[(non_terminal, terminal)]}")
        else:
            print(f"{non_terminal} -> {terminal} : ")