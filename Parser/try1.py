from tabulate import tabulate

# Define grammar rules using a dictionary
grammar_dict = {
    "Program": ["Arithmeticexp", "Forloop"],
    "Arithmeticexp": ["Number Operator Number", "Number '++'", "Number '--'", "Identifier Operator Identifier", "Identifier '++'", "Identifier '--'"],
    "Number": ["Integer", "Float"],
    "Identifiers": ["Identifier Identifiers", "Identifier"],
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
    "Forloop": ["'for' Openbracket Expression Semicolon Expression Semicolon Expression Closebracket Openbrace Statements Closebrace"],
    "Expression": ["Assignmentexp", "Logicalexp", "Equalityexp", "Arithmeticexp", "Relationalexp"],
    "Assignmentexp": ["Identifier '=' Expression"],
    "Logicalexp": ["Factors", "LogicalOp", "Factors"],
    "LogicalOp": ["'&&'", "'||'", "'!'"],
    'Factors': ["Identifier", "'(' Expression ')'", "Number"],
    "Equalityexp": ["Factors '==' Factors"],
    'RelationalOp': ["'<='", "'>='", "'=='", "'!='", "'<'", "'>'"],
    'Statements': ["Equalityexp"],
    "Semicolon": ["';'"],
    "Openbracket": ["'('"],
    "Closebracket": ["')'"],
    "Openbrace": ["'{'"],
    "Closebrace": ["'}'"],
}

# Convert dictionary to string representation of the grammar
grammar_string = "\n".join(f"{key} -> {' | '.join(value)}" for key, value in grammar_dict.items())

# Define function to parse productions
def parse_production(production):
    tokens = production.split()
    if len(tokens) == 1 and tokens[0][0] == "'":
        return tokens[0].strip("'")
    else:
        return tokens

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
          for production in expansion:
            if current_input_token in production:
              break
          if production:
            break
      if production:
        stack.pop()
        action = f"Derive {top_of_stack} -> {' '.join(production)}"
        if production != ['ε']:
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
sentence = "for ( 4 == 4 ; 4 == 4 ; 4 == 4 ) { 4 == 4 }"  # Corrected sentence
print("Input string: ", sentence)
parse_sentence(sentence)