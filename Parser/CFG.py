CFGs = {
    'Keywords': [['Keyword'], ['Keywords'], ['ε']],
    'Keyword': [['int'], ['float'], ['char'], ['if'], ['elseif'], ['else'], ['while'], ['for'], ['return']],
    'Strings': [['DoubleQuoteString'], ['SingleQuoteString']],
    'DoubleQuoteString': [['“', 'DoubleQuoteContent', '”']],
    'SingleQuoteString': [['‘', 'SingleQuoteContent', '’']],
    'DoubleQuoteContent': [['NonQuoteCharacters'], ['EscapeCharacter'], ['DoubleQuoteString']],
    'SingleQuoteContent': [['NonQuoteCharacters'], ['EscapeCharacter'], ['SingleQuoteString']],
    'NonQuoteCharacter': [['Letters'], ['Zerotonine'], ['Specialsymbols'], ['Punctuators']],
    'NonQuoteCharacters': [['NonQuoteCharacter'], ['NonQuoteCharacters'], ['ε']],
    'Identifier': [['Letters', 'Anotherletter'], ['_', 'Anotherletter']],
    'Anotherletter': [['ϵ'], ['Character', 'Anotherletter']],
    'Character': [['Letters'], ['Zerotonine'], ['_']],
    'Operator': [['+'], ['-'], ['*'], ['/'], ['<='], ['>='], ['=='], ['!='], ['<'], ['>']],
    'RelationalOp': [['<='], ['>='], ['=='], ['!='], ['<'], ['>']],
    'LogicalOp': [['&&'], ['||'], ['!']],
    'S': [['Number', 'Operator', 'Number'], ['Number', '++'], ['Number', '--'], ['Identifier', 'Operator', 'Identifier'], ['Identifier', '++'], ['identifier', '--']],
    'Number': [['Integer'], ['Float']],
    'Integer': [['Sign', 'Digits'], ['Digits']],
    'Digits': [['Digit', 'Digits'], ['ε']],
    'Digit': [['Zero'], ['Onetonine']],
    'Zero': [['0']],
    'Onetonine': [['0'], ['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']],
    'Float': [['sign', 'Digit', '.', 'Digit'], ['Digit', '.', 'Digit']],
    'Letters': [['a'], ['b'], ['c'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'], ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z'], ['A'], ['B'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'], ['M'], ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'], ['Y'], ['Z']],
    'Specialsymbols': [['!'], ['@'], ['£'], ['#'], ['$'], ['^'], ['&'], ['*'], ['+'], ['-'], ['_'], ['='], ['<'], ['>'], ['?']],
    'Punctuators': [['('], [')'], ['{'], ['}'], ['['], [']'], ['.'], [','], [';']],
    'EscapeCharacter': [['\\n']],
    'Program': [['Type', 'Funcname', '(', 'Arglist', ')', '{', 'Statements', '}']],
    'Type': [['void'], ['int'], ['float'], ['double'], ['char']],
    'Funcname': [['main'], ['Identifier']],
    'Identifiers': [['Identifier'], ['Identifiers'], ['ε']],
    'Arglist': [['Identifier'], ['Type', 'Identifier'], ['ε']],
    'Arglists': [['Arglist'], ['Arglists'], ['ε']],
    'Statements': [['Statement'], ['Statements'], ['ε']],
    'Statement': [['Variabledec'], ['Ifstatement'], ['Whileloop'], ['Forloop'], ['Expressionstatement'], ['Returnstatement']],
    'Variabledec': [['Type', 'Identifier', '=', 'Expression']],
    'Expression': [['Assignmentexp'], ['Logicalexp'], ['Equalityexp'], ['Arithmeticexp'], ['Relationalexp']],
    'Ifstatement': [['if', '(', 'Expression', ')', '{', 'Statements', '}'], ['if', '(', 'Expression', ')', '{', 'Statements', '}', 'else', '{', 'Statements', '}'], ['if', '(', 'Expression', ')', '{', 'Statements', '}', 'Elseifstatements', 'else', '{', 'Statements', '}']],
    'Elseifstatements': [['Elseifstatement'], ['Elseifstatement'], ['ε']],
    'Elseifstatement': [['else', 'if', '(', 'Expression', ')', '{', 'Statements', '}']],
    'Forloop': [['for', '(', 'Expression', ';', 'Expression', ';', 'Expression', ')', '{', 'Statements', '}']],
    'Whileloop': [['while', '(', 'Expression', ')', '{', 'Statements', '}']],
    'Returnstatement': [['return', 'Expression', ';']],
    'Assignmentexp': [['Identifier', '=', 'Expression']],
    'Factors': [['Identifier'], ['Expression'], ['Number']],
    'LogicalExp': [['Factors', 'LogicalOp', 'Factors']],
    'Equalityexp': [['Factors', '==', 'Factors']],
    'Arithmeticexp': [['Number', 'Operator', 'Number'], ['Number', '++'], ['Number', '--'], ['Identifier', 'Operator', 'Identifier'], ['Identifier', '++'], ['identifier', '--']]
}
