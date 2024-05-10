# CFGs
CFGs = {
"Keywords": [
    ["Keyword", "Keywords"], [""]
],
"Keyword": [
    ["int"], ["float"], ["char"], ["if"], ["elseif"], ["else"], ["while"], ["for"], ["return"]
],
"Strings": [
    ["Doublequotestring"], ["Singlequotestring"]
],
"Doublequotestring": [
    ['"', "Doublequotecontent", '"']
],
"Singlequotestring": [
    ["'", "Singlequotecontent", "'"]
],
"Doublequotecontent": [
    ["Nonquotecharacters"], ["Escapecharacter"], ["Doublequotestring"]
],
"Singlequotecontent": [
    ["Nonquotecharacters"], ["Escapecharacter"], ["Singlequotestring"]
],
"Nonquotecharacter": [
    "Letters", "Zerotonine", "Specialsymbols", "Punctuators"
],
"Nonquotecharacters": [
    ["Nonquotecharacter", "Nonquotecharacters"], [""]
],
"Identifier": [
    ["Letters", "Anotherletter"]
],
"Anotherletter": [
    [""], ["Character", "Anotherletter"]
],
"Character": [
    ["Letters"], ["Zerotonine"]
],
"S": [
    ["Number", "Operator", "Number"], ["Number", "++"], ["Number", "--"],
    ["Identifier", "Operator", "Identifier"], ["Identifier", "++"], ["Identifier", "--"]
],
"Number": [
    ["Integer"], ["Float"]
],
"Integer": [
    ["Sign", "Digits"], ["Digits"]
],
"Digits": [
    ["Zerotonine"], ["Zerotonine", "Digits"]
],
"Float": [
    ["Sign", "floatDigit", ".", "floatDigit"], ["floatDigit", ".", "floatDigit"]
],
"floatDigit": [
    ["Zerotonine"], ["Zerotonine", "floatDigit"]
],
"Letters": [
    ["a"], ["b"], ["c"], ["d"], ["e"], ["f"], ["g"], ["h"], ["i"], ["j"], ["k"], ["l"], ["m"], ["n"], ["o"], ["p"], ["q"], ["r"], ["s"], ["t"], ["u"], ["v"], ["w"], ["x"], ["y"], ["z"],
    ["A"], ["B"], ["C"], ["D"], ["E"], ["F"], ["G"], ["H"], ["I"], ["J"], ["K"], ["L"], ["M"], ["N"], ["O"], ["P"], ["Q"], ["R"], ["S"], ["T"], ["U"], ["V"], ["W"], ["X"], ["Y"], ["Z"]
],
"Zerotonine": [
    ["0"], ["1"], ["2"], ["3"], ["4"], ["5"], ["6"], ["7"], ["8"], ["9"]
],
"Specialsymbols": [
    ["!"], ["@"], ["£"], ["#"], ["$"], ["^"], ["&"], ["*"], ["+"], ["-"], ["_"], ["="], ["<"], [">"], ["?"]
],
"Punctuators": [
    ["("], [")"], ["{"], ["}"], ["["], ["]"], ["."], [","], [";"]
],
"Escapecharacter": [
    ["\\n"]
],
"Operator": [
    ["+"], ["-"], ["*"], ["/"], ["<="], [">="], ["=="], ["!="], ["<"], [">"]
],
"Sign": [
    ["+"], ["-"]
],
"LogicalOp": [
    ["&&"], ["||"]
],
"Program": [
    ["Type", "Funcname", "(", "Arglist", ")", "{", "Statements", "}"]
],
"Type": [
    ["void"], ["int"], ["float"], ["double"], ["char"]
],
"Funcname": [
    ["main"], ["Identifier"]
],
"Arglist": [
    ["Identifier"], ["Type", "Identifier"], [""]
],
"Arglists": [
    ["Arglist", "Arglists"], [""]
],
"Statements": [
    ["Statement", "Statements"], [""]
],
"Statement": [
    ["Variabledec"], ["Ifstatement"], ["Whileloop"], ["Forloop"], ["Expressionstatement"], ["Returnstatement"]
],
"Variabledec": [
    ["Type", "Identifier", "=", "Expression"]
],
"Expression": [
    ["Assignmentexp"], ["Logicalexp"], ["Equalityexp"], ["Arithmeticexp"], ["Relationalexp"]
],
"Ifstatement": [
    ["if", "(", "Expression", ")", "{", "Statements", "}"],
    ["if", "(", "Expression", ")", "{", "Statements", "}", "else", "{", "Statements", "}"],
    ["if", "(", "Expression", ")", "{", "Statements", "}", "Elseifstatements", "else", "{", "Statements", "}"]
],
"Elseifstatements": [
    ["Elseifstatement"], [""]
],
"Elseifstatement": [
    ["else", "if", "(", "Expression", ")", "{", "Statements", "}"]
],
"Forloop": [
    ["for", "(", "Expression", ";", "Expression", ";", "Expression", ")", "{", "Statements", "}"]
],
"Whileloop": [
    ["while", "(", "Expression", ")", "{", "Statements", "}"]
],
"Returnstatement": [
    ["return", "Expression", ";"]
],
"Assignmentexp": [
    ["Identifier", "=", "Expression"]
],
"Logicalexp": [
    ["Factors", "LogicalOp", "Factors"]
],
"Equalityexp": [
    ["Factors", "==", "Factors"]
],
"Arithmeticexp": [
    ["Number", "Operator", "Number"], ["Number", "++"], ["Number", "--"],
    ["Identifier", "Operator", "Identifier"], ["Identifier", "++"], ["Identifier", "--"]
],
"Factors": [
    ["Identifier"], ["Statement"], ["Expression"], ["Number"]
],

"ID": [],  # Placeholder for actual identifiers



}

def findingFirstSets(CFGs):
    firstSets = {} #intialized dictionary to store first sets

    for nonTerminals in CFGs:
        firstSets[nonTerminals] = set()
    
    #  Computes First set of nonTerminals recursively 
    def computeFirst(nonTerminals, visited):
        #  Already visited, return an empty set to break the cycle
        if nonTerminals in visited:
            return set()
        visited.add(nonTerminals)


        #  the non terminal that was passed is not a nonTerminal but a terminal add to first set (Filtering of terminals and non terminals)
        if nonTerminals in terminals:
            return {nonTerminals} #First set is a terminal
        
        #  Handles ε productions
        elif nonTerminals == '':
            return {''}
        else: # when the first set is a non terminal genuinely

            first = set() #stores first set of current non Terminal symbol

            # Loop through RH_Production for a given non Terminal
            for production in CFGs[nonTerminals]: 
                # Iterate through every Symbol in a single production rule
                for i, nonTerminals_i in enumerate(production):

                    # Compute First of the first Symbol in production
                    first_i = computeFirst(nonTerminals_i, visited)
                    # Add First(of_firstsymbol) seen
                    first.update(first_i)
                    # If First(of_firstsymbol) does not contain lambda stop
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

    #  Add $ as a follow set of start symbol first rule
    followSets[startSymbol].add('$')

    # Compute follow sets
    def computeFollowSets(nonTerminal, visited):
        if nonTerminal in visited:
            return
        visited.add(nonTerminal)

        for nonTerminals in CFGs:
            for production in CFGs[nonTerminals]:
                #Checks if current non terminal is in the production  
                if nonTerminal in production:
                    indexing = production.index(nonTerminal)
                    # second rule
                    #if it is then it assign an index
                    if indexing < len(production) - 1:
                        for symbol in production[indexing + 1:]: #considers the next symbol that follows the non terminal in question
                            if symbol in terminals: #if a terminal it includes it
                                followSets[nonTerminal].add(symbol)

                            elif symbol in CFGs: # if its a non terminal take the first set of this non terminal that follows it
                                followSets[nonTerminal].update(
                                    firstSets[symbol] - {''}
                                )
                                if '' in firstSets[symbol]:
                                    computeFollowSets(symbol, visited)

                    # Rule 3 if non terminal is the last symbol at RH production or empty
                    # Updates the follow with the follow of LH non terminal
                    if indexing == len(production) - 1 or '' in firstSets.get(production[indexing + 1], []):
                        followSets[nonTerminal].update(
                            followSets[nonTerminals]
                        )
                        computeFollowSets(nonTerminals, visited)

    # Iterates through each non-terminal
    for nonTerminal in CFGs:
        visited = set()
        computeFollowSets(nonTerminal, visited)

    return followSets


# Getting terminal symbols
terminals = []
for RH_Production in CFGs.values(): # .Values gets the values of the dictionary
    for production in RH_Production: #Iterates over the values in the production rule
        for anySymbol in production:
            if anySymbol not in CFGs and anySymbol != '': #if the anySymbol is not a key in the CFG and is not empty then its a terminal
                terminals.append(anySymbol)
                
terminals = set(terminals)


#First sets computation for each non-terminal
firstSets = findingFirstSets(CFGs)
print("Non Terminals First sets")
for nonTerminals, firstSet in firstSets.items():
    print("\tFirst(" + nonTerminals + "):", firstSet)

# Follow sets computation for each non terminal

# Start symbol from the CFG

#can be changed to program once we have the full CFG
startSymbol = "Keywords"
followSets = findingFollowSets(CFGs, firstSets, terminals)
print("\nNon Terminals Follow Sets")
# Printing Follow sets
for nonTerminal, followSet in followSets.items():
    print("\tFollow(" + nonTerminal + "):", followSet)
