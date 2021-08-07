
def check_formula(formula):
    """Check the correctness of the chemical formula"""

    if not formula:
        raise EmptyFormula

    if formula[0].isnumeric:
        raise FirstElementAbsent



class EmptyFormula(ValueError):
    pass

class FirstElementAbsent(ValueError):
    pass



def from_string_to_dict(formula):
    """Transform the chemical formula from a string to a dict"""

    #Locate the capitalized letter
    #The capitalized letter indicate the start of the chemical element's name

    capitalized_letter = [letter for letter in formula if letter.isupper()]
    dict_formula = {}

    for index,letter in enumerate(formula):
        chemical_element = ''
        quantity_element = ''
        i = 0

        if letter in capitalized_letter:
            while not formula[index+i].isnumeric():
                chemical_element += formula[index+i]
                i +=1

            while formula[index+i].isnumeric():
                quantity_element += formula[index+i]
                i +=1

                if index+i == len(formula):
                    break

            dict_formula[chemical_element] = float(quantity_element)
    return dict_formula
