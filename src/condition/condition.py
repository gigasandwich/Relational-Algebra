import re

"""
The goal of this module is to change expressions like
    (("fako" == "fako" and 2 != 4) and True == True) or False == True
To
    ((True and True) and True == True) or False == True
and then evaluate them
"""

def main():
    condition = '(("fako" == "fako" and 2 != 4) and True == True) or False == True'
    print(simplify(condition))
    print(eval(condition))

def simplify_and_evaluate(expression: str) -> bool:
    """
    Simplifies and evaluates a given logical or mathematical expression.

    Example:
        Input: "(1 < 2) and (3 > 2)"
        Output: True
    """
    simplified_expression = simplify(expression)
    try:
        result = eval(simplified_expression)
    except Exception:
        raise ValueError(f"Failed to evaluate {expression}")
    return result

def simplify(expression: str) -> str:
    """
    Simplifies an expression by processing parentheses and resolving comparisons.

    Example:
        Input: "(1 < 2) and (3 > 2)"
        Intermediate: "True and (3 > 2)"
        Output: "True and True"
    """
    expression = process_parentheses(expression)
    comparison_pattern = re.compile(r'(\S+)\s*(==|!=|<=|<|>=|>|in|not in)\s*(\S+)') # >= before > because of the pattern order
    simplified_expression = comparison_pattern.sub(evaluate_comparison, expression)
    simplified_expression = simplified_expression.replace("true", "True").replace("false", "False")
    return simplified_expression

def process_parentheses(expression: str) -> str:
    """
    Resolves nested parentheses by recursively evaluating inner expressions.

    Example:
        Input: "(1 < 2) and (3 > 2)"
        Step 1: "True and (3 > 2)"
        Step 2: "True and True"
        Output: "True and True"
    """
    parentheses_pattern = re.compile(r'\(([^()]+)\)')

    def resolve_parentheses(match): # TODO Should be a lambda expression to make it easier 
        inner_expression = match.group(1)
        return str(simplify_and_evaluate(inner_expression))

    while '(' in expression:
        expression = parentheses_pattern.sub(resolve_parentheses, expression)
    return expression

def evaluate_comparison(match) -> str:
    """
    Evaluates a comparison operation like 2 < 3 and returns 'true' or 'false'.

    Example:
        Input: Match object for "2 < 3"
        Output: "true"
    """
    left, operator, right = match.groups()
    left = safe_eval(left)
    right = safe_eval(right)

    if type(left) != type(right):
        return "false"

    if operator == "==":
        result = str(left == right).lower()
    elif operator == "!=":
        result = str(left != right).lower()
    elif operator == ">":
        result = str(left > right).lower()
    elif operator == "<":
        result = str(left < right).lower()
    elif operator == ">=":
        result = str(left >= right).lower()
    elif operator == "<=":
        result = str(left <= right).lower()
    elif operator == "in":
        result = str(left in right).lower()
    elif operator == "not in":
        result = str(left not in right).lower()
    else:
        raise ValueError(f"Unsupported operator: {operator}")

    return result

def safe_eval(value):
    """
    Safely evaluates a value or returns it as a stripped string if evaluation fails.

    Example:
        Input: "1"
        Output: 1

        Input: "'abc'"
        Output: "abc"
    """
    try:
        return eval(value)
    except:
        return value.strip("'").strip('"')
    
if __name__ == "__main__":
    main()    