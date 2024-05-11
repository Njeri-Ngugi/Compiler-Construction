from tabulate import tabulate
from CFG import CFGs
from First_FollowSets import findingFirstSets, findingFollowSets
from Parse_Table import parse_table, terminals, non_terminals


def ll1_parser(tables, start_symbol, input_string):
    """
    Parses the input string using LL(1) parsing technique.

    Args:
        tables (dict): Lookup table for LL(1) parsing.
        start_symbol (str): The starting symbol for parsing.
        input_string (str): The input string to be parsed.
    """

    # add '$' and start symbol to stack
    stack = ["$"]
    stack.append(start_symbol)
    input_string = list(input_string) + ["$"]
    input_string.reverse()
    top = stack[-1]

    # intialize table that tracks the steps taken in parsing
    header = ["stack", "input", "action"]
    table = []

    # loop until both stack and input string are empty
    while stack and input_string:
        row = [stack, ''.join(input_string)]

        # if both stack and input string are empty, string accepted
        if top == input_string[-1] == "$":
            row.append("String accepted")
            table.append(row)
            break

        # if top of stack and input string are same, pop
        if top == input_string[-1]:
            stack.pop()
            input_string.pop()
            row.append("pop")
            table.append(row)

        # if top of stack and input string are not same, get production
        else:
            production = tables.get((top, input_string[-1]))

            # if no production, string not accepted
            if production is None:
                row.append("String not accepted")
                table.append(row)
                break
            stack.pop()

            # if a rule exists, apply it to stack
            if production != "ε":
                production = list(production)
                production.reverse()
                stack += production

            # update table
            row.append(production)
            table.append(row)

        # if stack or input string is empty, add '$'
        if not stack:
            stack.append("$")
        if not input_string:
            input_string.append("$")

    # display the table
    print(tabulate(table, header, tablefmt="grid"))
    return


# yet to be edited
def main():
  grammar = CFGs
  input_string = "int main"

  # No need for user input for productions
  start_symbol = list(grammar.keys())[0]

  first_sets = {non_terminal: findingFirstSets(grammar) for non_terminal in grammar}
  follow_sets = {non_terminal: findingFollowSets(grammar, first_sets, terminals) for non_terminal in grammar}

  print("Input grammar::")
  print(grammar)

  print("\nFIRST sets:")
  for non_terminal, first_set in first_sets.items():
    print(f"FIRST({non_terminal}) = {first_set}")
  print("\nFOLLOW sets:")
  for non_terminal, follow_set in follow_sets.items():
    print(f"FOLLOW({non_terminal}) = {follow_set}")

  # Print the parsing table
  print("\nParsing table:")
  table = parse_table(grammar, first_sets, follow_sets)

  ll1_parser(table, start_symbol, input_string)

if __name__ == "__main__":
  main()
