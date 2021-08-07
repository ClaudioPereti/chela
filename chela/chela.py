
def check_formula(formula):
    """Check the correctness of the chemical formula"""

    if not formula:
        raise EmptyFormula



class EmptyFormula(ValueError):
    pass
