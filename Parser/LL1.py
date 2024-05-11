from CFG import CFGs
from Parse_Table import parse_table
from Parse_Table import non_terminals


def ll1_parser(CFG=CFGs, parse_table=parse_table, input="int i"):
    # temporary sample input for now
    """
    Parses an input string using the LL1 algorithm

    Args:
        CFG (dict): A dictionary of CFGs
        parse_table (dict): A dictionary representing the parse table
        input (str): The input string to be parsed

    Return:
        True if input string is accepted by the grammar, else False
    """
    stack = ["$"]
    stack.append(CFG['Keywords'])  # start symbol

    input_str = list(input) + ["$"]

    while stack and input_str:
        top = stack[-1]
        current_input_symbol = input_str[0]
        print("Top -> ", top)
        print("Current Input Symbol -> ", current_input_symbol)

        # if top of stack matches current input symbol, remove both
        if top == current_input_symbol:
            stack.pop()
            input_str.pop(0)
            continue

        # if top of stack is non-terminal look up its production in parse table
        if top in non_terminals:
            production = parse_table.get((top, current_input_symbol), None)

            # if rule exists, replace top with RHS of the rule in reverse
            if production is not None:
                stack.pop()

                # if rule is epsilon simply pop the stack,
                # else apply the production
                if production != "ε":
                    for symbol in reversed(production):
                        stack.append(symbol)
                else:
                    stack.pop()
            else:
                print("Error: No production rule available.")
                return False

        # if stack top is $ and input string is empty, accept
        elif top == "$" and current_input_symbol == "$":
            print("Syntax correct")
            return True

        # if stack top is $ but input string is not empty, reject
        else:
            print("Error: Syntax wrong.")
            return False

    print("Error: Parsing failed.")
    return False
