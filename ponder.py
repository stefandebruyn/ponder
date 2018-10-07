import sys


PARENS_OPEN = '('
PARENS_CLOSE = ')'
LOGICAL_NOT = '!'
LOGICAL_AND = '&'
LOGICAL_OR = '|'
LOGICAL_XOR = '^'
LOGICAL_IMPLICATION = '>'
LOGICAL_BICONDITIONAL = '%'
LOGICAL_EQUIVALENT = '='


# Purges whitespace from an expression and returns it as a list of characters
def parse(expr):
    return list("".join(expr.split()))


# Evaluates a unary operation at ind in expr given props, a map of propositions character to their truth values
def evaluate_unary(expr, props, ind):
    # Evaluate the operand
    operand = expr[ind + 1]
    val = operand if isinstance(operand, bool) else props[operand]
    op = expr[ind]
    truth = None

    # Evaluate the operation
    if op is LOGICAL_NOT:
        truth = val is False

    # Replace the operand and operator with the final evaluation
    expr[ind] = truth
    del expr[ind + 1]


# Evaluates a binary operation at ind in expr given props, a map of proposition characters to their truth values
def evaluate_binary(expr, props, ind):
    # Evaluate each operand
    lhs, rhs = expr[ind - 1], expr[ind + 1]
    lhs_truth = lhs if isinstance(lhs, bool) else props[lhs]
    rhs_truth = rhs if isinstance(rhs, bool) else props[rhs]

    op = expr[ind]
    truth = None

    # Evaluate the operation
    if op is LOGICAL_AND:
        truth = lhs_truth and rhs_truth
    elif op is LOGICAL_OR:
        truth = lhs_truth or rhs_truth
    elif op is LOGICAL_XOR:
        truth = lhs_truth is not rhs_truth
    elif op is LOGICAL_IMPLICATION:
        truth = lhs_truth is False or lhs_truth and rhs_truth
    elif op is LOGICAL_BICONDITIONAL:
        truth = lhs_truth is rhs_truth

    # Replace the operator and operands with the final evaluation
    expr[ind - 1] = truth
    del expr[ind]; del expr[ind]


# Computes the truth value of an unparsed expression given a mapping of propositions to their values
def evaluate(expr, props):
    expr = parse(expr)

    # Evaluate nested expressions
    while PARENS_OPEN in expr:
        # Isolate the nested expression and evaluate it
        ind_open, ind_close = expr.index(PARENS_OPEN), expr.index(PARENS_CLOSE)
        nested_eval = evaluate("".join(expr[ind_open+1:ind_close]), props)

        # Cut out the nested expression and replace it with the evaluation
        expr[ind_open] = nested_eval
        for i in range(ind_open + 1, ind_close + 1):
            del expr[ind_open + 1]

    # Evaluate NOTs
    while LOGICAL_NOT in expr:
        ind = expr.index(LOGICAL_NOT)
        evaluate_unary(expr, props, ind)

    # Evaluate ANDs
    while LOGICAL_AND in expr:
        ind = expr.index(LOGICAL_AND)
        evaluate_binary(expr, props, ind)

    # Evaluate ORs and XORs
    while LOGICAL_OR in expr or LOGICAL_XOR in expr:
        ind1 = expr.index(LOGICAL_OR) if LOGICAL_OR in expr else -1  # Earliest OR index
        ind2 = expr.index(LOGICAL_XOR) if LOGICAL_XOR in expr else -1  # Earliest XOR index
        ind = min(ind1, ind2) if ind1 is not -1 and ind2 is not -1 else ind1 if ind1 is not -1 else ind2  # Earliest ind
        evaluate_binary(expr, props, ind)

    # Evaluate IMPLICATIONs
    while LOGICAL_IMPLICATION in expr:
        ind = expr.index(LOGICAL_IMPLICATION)
        evaluate_binary(expr, props, ind)

    # Evaluate BICONDITIONALs
    while LOGICAL_BICONDITIONAL in expr:
        ind = expr.index(LOGICAL_BICONDITIONAL)
        evaluate_binary(expr, props, ind)

    # At this point, if there isn't a single value left in the expression, the original expression was syntactically
    # incorrect
    if len(expr) is not 1:
        raise RuntimeError("Expression could not be evaluated; check syntax")

    final_eval = expr[0]
    return final_eval if isinstance(final_eval, bool) else props[final_eval]


# Generates a truth table from an unparsed expression
def ponder(expr):
    # Compile a list of all propositions in the expression
    props = []
    for char in expr:
        if 'A' <= char <= 'Z' or 'a' <= char <= 'z':
            props.append(char)

    # Top row of the table
    for prop in props:
        print(prop + " ", end="")

    print(" " + "".join(expr))

    # For every combination of truth values in the propositions, evaluate and print
    combos = 2 ** len(props)
    upper_bin = "{0:b}".format(combos - 1)

    for i in range(combos):
        # Generate bit string and pad it to the correct length
        binstr = "{0:b}".format(i)

        while len(binstr) < len(upper_bin):
            binstr = "0" + binstr

        # Build truth value mapping
        truth_map = {}

        for p in range(len(props)):
            # T and F are special constant propositions
            bit = True if (props[p] is 'T' or (props[p] is not 'F' and binstr[p] is '1')) else False

            print(("1" if bit is True else "0") + " ", end="")
            truth_map[props[p]] = bit

        # Evaluate
        evaluation = evaluate(expr, truth_map)
        print(" " + ("1" if evaluation is True else "0"))


# Command line usage
if len(sys.argv) != 2:
    raise RuntimeError("Usage: py ponder.py <expression>")

ponder(sys.argv[1])
