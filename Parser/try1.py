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
          print("My TOP OF THE STACK NON-TERMINAL: ", non_terminal)
          for production in expansion:
            print(f"PRODUCTION IN EXPANSION: {production} : {expansion}")
            if production == [''] and expansion[0] == ['']:
                 print(f"MY CURRENT INPUT: {current_input_token} : MY PRODUCTION: {production[0]} MATCH FOUND empty")
                 break
            if current_input_token == production[0]:
              print(f"MY CURRENT INPUT: {current_input_token} : MY PRODUCTION: {production[0]} MATCH FOUND")
              
              if production == [''] and expansion[0] == ['']:
                 print(f"MY CURRENT INPUT: {current_input_token} : MY PRODUCTION: {production[0]} MATCH FOUND")
              break
      
          if production == [''] and expansion[0] == ['']:
                 print(f"MY CURRENT INPUT: {current_input_token} : MY PRODUCTION: {production[0]} MATCH FOUND empty")
                 break
          if current_input_token == production[0]:
            print(" CHECK 2 CURRENT INPUTPRODUCTION: ", production)
            
            break
      if production:
        print("POPPING PRODUCTION: ", production)
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
