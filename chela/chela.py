
def basic_check_formula(formula):
    """Check the basic correctness of the chemical formula,i.e. empty string, absent element, presence of non alphanumeric value"""
    #Check if the string is empty
    if not formula:
        raise EmptyFormula
    #Check if the first element is present
    if formula[0].isnumeric():
        raise FirstElementAbsent
    #Check the presence of non alphanumeric values, included -
    if not formula.isalnum():
        raise NonAlphaNumericValue

class EmptyFormula(ValueError):
    pass

class FirstElementAbsent(ValueError):
    pass

class NonAlphaNumericValue(ValueError):
    pass

class NegativeQuantityElement(ValueError):
    pass

class NonExistentElement(ValueError):
    pass

class ZeroQuantityElement(ValueError):
    pass

class RepeatedElement(ValueError):
    pass

def advanced_check_formula(formula):
    """Check the advanced correctness fo the chemical formula, i.e. wrong chemical element, zero value, repeated element"""

    dict_formula = from_string_to_dict(formula)
    chemical_element = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']

    #Check the presence of a element with 0 quantity
    for value in dict_formula.values():
        if value == 0:
            raise ZeroQuantityElement
    #Check the presence of inexistent or mispelled element
    for element in dict_formula.keys():
        if not element in chemical_element:
            raise NonExistentElement

    #Check if an element is repeated in the formula, using the fact that a dictionary overwrite a key if alredy present
    letters = ''.join(str(element) for element in dict_formula.keys())
    float_numbers = ''.join(str(number[0]) for number in dict_formula.values() if not number[0].is_integer())
    int_numbers = ''.join(str(int(number[0])) for number in dict_formula.values() if number[0].is_integer() and number[0] != 1)
    complete_formula = letters + float_numbers + int_numbers

    if len(complete_formula) != len(formula):
        raise RepeatedElement

def check_formula(formula):
    basic_check_formula(formula)
    advanced_check_formula(formula)



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

                dict_formula[chemical_element] = [float(quantity_element)]
            else:
                dict_formula[chemical_element] = [1.0]
    return dict_formula


def csv_to_dataframe(path=path,header = False,property = [],robust = False):
    """Load a csv file containing chemical formula and transform it into a DataFrame"""

    import pandas as pd
    import numpy as np

    #Columns name of the DataFrame
    names = ['formula']
    #Load csv file from path
    #Header is True if the csv file doesn't contain the header
    if header:
        #Property is used if more property of the material are needed
        if property:
            names = names + property
        formula_dataset = pd.read_csv(path,names = names,index_col=False)
    else:
        formula_dataset = pd.read_csv(path)
    #Symbols of chemical elements
    chemical_element = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']

    #Transient data structure to store data of chemical formula
    dict_formula = {}
    #Pandas DataFrame to store chemical formula
    chem_dataset = pd.DataFrame(columns=chemical_element)
    #Loop for every chemical formula present in the csv file
    for material in formula_dataset['formula']:
        #Control if the formula are correct
        #Robust to don't interrupt the loop and pass to the
        if robust:
            try:
                check_formula(material)
            except:
                #Pass to the next iteration
                continue

        else:
            check_formula(material)
            #Create dictiornary containing chemical formula
            dict_formula = from_string_to_dict(material)
            #Convert the dictionary into a DataFrame
            chem_dataset = chem_dataset.append(pd.DataFrame(dict_formula))
            dict_formula = {}
    #Put 0 on the element non present in the chemical formula
    chem_dataset = chem_dataset.replace(np.nan,0)
    #Reset the index
    chem_dataset = chem_dataset.reset_index(drop=True)
    #If formula == True add a column with the chemical formula
    for name in names:
        chem_dataset[name] = formula_dataset[name]

    return chem_dataset
#%%
csv_to_dataframe(path,header = True,property = ['col'])
import sys
sys.path.append('/home/claudio/chela/env_chela/lib/python3.6/site-packages')
#%%

@pd.api.extensions.register_dataframe_accessor("chemdata")
class ChemDataFrame:


    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    @classmethod
    def from_string_to_dict(self,formula):
        return from_string_to_dict(formula)
#%%

data = pd.DataFrame(from_string_to_dict('H2O'))
data
data.chemdata.chemprint()

d = data.chemdata.from_string_to_dict('H2O')
pd.DataFrame.chemdata.from_string_to_dict('H2O')
