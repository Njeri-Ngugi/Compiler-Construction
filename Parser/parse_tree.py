import nltk
from nltk import CFG

# Define grammar rules using a dictionary
grammar_dict = {
    # "Keywords": ["Keyword Keywords", "ε"],
    # "Keyword": ["'int'", "'float'", "'char'", "'if'", "'elseif'", "'else'", "'while'", "'for'", "'return'"],
    "Program": ["Arithmeticexp", "Forloop"],
    "Arithmeticexp": ["Number Operator Number", "Number '++'", "Number '--'", "Identifier Operator Identifier", "Identifier '++'", "Identifier '--'"],
    "Number": ["Integer", "Float"],
    "Identifiers": ["Identifier Identifiers", "''"],
    "Identifier": ["Letters Anotherletter", "'_' Anotherletter"],
    "Anotherletter": ["Character Anotherletter", "Character"],
    "Character": ["Letters", "Zerotonine", "'_'"],
    "Letters": ["'a'", "'b'", "'c'", "'d'", "'e'", "'f'", "'g'", "'h'", "'i'", "'j'", "'k'", "'l'", "'m'", "'n'", "'o'", "'p'", "'q'", "'r'", "'s'", "'t'", "'u'", "'v'", "'w'", "'x'", "'y'", "'z'", "'A'", "'B'", "'C'", "'D'", "'E'", "'F'", "'G'", "'H'", "'I'", "'J'", "'K'", "'L'", "'M'", "'N'", "'O'", "'P'", "'Q'", "'R'", "'S'", "'T'", "'U'", "'V'", "'W'", "'X'", "'Y'", "'Z'"],
    "Operator": ["'+'", "'-'", "'*'", "'/'", "'<='", "'>='", "'=='", "'!='", "'<'", "'>'"],
    "Integer": ["Sign Digits", "Digits"],
    'Float': ["Sign Digit '.' Digit", "Digit '.' Digit"],
    "Sign": ["'+'", "'-'"],
    "Digits": ["Digit Digits" , "Digit"],
    "Digit": ["Zerotonine"],
    "Zerotonine": ["'0'", "'1'", "'2'", "'3'", "'4'", "'5'", "'6'", "'7'", "'8'", "'9'"],
    "Forloop": ["'for' '(' Expression ';' Expression ';' Expression ')' '{' Statements '}'"],
    "Expression": ["Assignmentexp", "Logicalexp", "Equalityexp", "Arithmeticexp", "Relationalexp"],
    "Assignmentexp": ["Identifier '=' Expression"],
    "Logicalexp": ["Factors", "LogicalOp", "Factors"],
    "LogicalOp": ["'&&'", "'||'", "'!'"],
    'Factors': ["Identifier", "'(' Expression ')'", "Number"],
    "Equalityexp": ["Factors '==' Factors"],
    'RelationalOp': ["'<='", "'>='", "'=='", "'!='", "'<'", "'>'"],
    'Statements': ["Equalityexp"],
    }

# Convert dictionary to string representation of the grammar
grammar_string = "\n".join(f"{key} -> {' | '.join(value)}" for key, value in grammar_dict.items())

# print(grammar_string)
# Create CFG from string representation
grammar = CFG.fromstring(grammar_string)
# print(grammar)

# Example usage: parsing a sentence
parser = nltk.ChartParser(grammar)
sentence = "4 / 4 . 4"  # Corrected sentence
print("Input string: ",sentence)
tokens = nltk.word_tokenize(sentence)
# print(tokens)

for tree in parser.parse(tokens):
    tree.pretty_print()
