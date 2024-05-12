class Scanner:
    def __init__(self, text):
        self.tokens = text.split()
        self.current_token = 0

    def next_token(self):
        if self.current_token < len(self.tokens):
            token = self.tokens[self.current_token]
            self.current_token += 1
            return token
        else:
            return None


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = self.scanner.next_token()

    def match(self, expected_token):
        if self.current_token == expected_token:
            self.current_token = self.scanner.next_token()
        else:
            raise Exception("Syntax error: expected '{}'".format(expected_token))

    def expr(self):
        node = self.term()
        node = self.expr_tail(node)
        return node

    def expr_tail(self, left):
        if self.current_token == '+':
            self.match('+')
            right = self.term()
            node = {'type': 'add', 'left': left, 'right': self.expr_tail(right)}
            return node
        else:
            return left

    def term(self):
        node = self.factor()
        node = self.term_tail(node)
        return node

    def term_tail(self, left):
        if self.current_token == '*':
            self.match('*')
            right = self.factor()
            node = {'type': 'mul', 'left': left, 'right': self.term_tail(right)}
            return node
        else:
            return left

    # Modified factor method to handle identifiers
    def factor(self):
        if self.current_token == '(':
            self.match('(')
            node = self.expr()
            self.match(')')
            return node
        elif self.current_token.isdigit():
            node = {'type': 'number', 'value': self.current_token}
            self.match(self.current_token)
            return node
        elif self.current_token.isalpha():
            node = {'type': 'identifier', 'name': self.current_token}
            self.match(self.current_token)
            return node
        else:
            raise Exception("Syntax error: unexpected token '{}'".format(self.current_token))

    def parse(self):
        return self.expr()


def main():
    text = input("Enter an arithmetic expression: ")
    scanner = Scanner(text)
    parser = Parser(scanner)
    parse_tree = parser.parse()
    print("Parse Tree:", parse_tree)


if __name__ == "__main__":
    main()
