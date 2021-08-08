
def check_formula(formula):
    """Check the correctness of the chemical formula"""

    if not formula:
        raise EmptyFormula

    if formula[0].isnumeric():
        raise FirstElementAbsent

    if not formula.isalnum():
        raise NonAlphaNumericValue

class EmptyFormula(ValueError):
    pass

class FirstElementAbsent(ValueError):
    pass

class NonAlphaNumericValue(ValueError):
    pass



def from_string_to_dict(formula):
    """Transform the chemical formula from a string to a dict"""

    #Locate the capitalized letter
    #The capitalized letter indicate the start of the chemical element's name

    capitalized_letter = [letter for letter in formula if letter.isupper()]
    dict_formula = {}

    #Runs on every letter of the chemical formula,looking for the Capitalized letter to locate the start of the chemical element
    for index,letter in enumerate(formula):
        chemical_element = ''
        quantity_element = ''
        i = 0

        if letter in capitalized_letter:
            #From the capitalized letter it start writing the chemical element's name untill it find a numeric value
            while not formula[index+i].isnumeric():
                chemical_element += formula[index+i]
                i +=1
                #Stop the iteration when the formula doesn't have any other letter or number or the next letter is of another element's name
                if index+i == len(formula) or formula[index+i].isupper():
                    break
            #If the formula contain more than one element and the next letter is not the one of another element's name
            if index+i < len(formula) and not formula[index+i].isupper():

                #From the first encountered it start writing the chemical element's quantity untill it find the next chemical element's name
                while formula[index+i].isnumeric():
                    quantity_element += formula[index+i]
                    i +=1
                    #Stop the iteration when the formula doesn't have any other letter or number
                    if index+i == len(formula):
                        break

                dict_formula[chemical_element] = quantity_element
            else:
                dict_formula[chemical_element] = 1.0
    return dict_formula
