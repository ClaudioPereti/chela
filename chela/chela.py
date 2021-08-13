
def basic_check_formula(formula):
    """Check the basic correctness of the chemical formula,i.e. empty string, absent element, presence of non alphanumeric value

    Args:
        formula: A string representing the chemical formula

    Raises:
        EmptyFormula: ValueError indicating the string is empty
        FirstElementAbsent: ValueError indicating the string starts with a number; the first atom is absent
        NonAlphaNumericValue: ValueError indicating the presence of symbol different from numbers and letters
    """

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
    """Check the advanced correctness fo the chemical formula, i.e. wrong chemical element, zero value, repeated element

    Args:
        formula: A string representing the chemical formula

    Raises:
        ZeroQuantityElement: ValueError indicating the presence of element with  quantity 0 in the formula
        NonExistentElement: ValueError indicating the presence of letters non representing atomic symbol
        RepeatedElement: ValueError indicating the repetition of an atomic symbol

    """

    dict_formula = from_string_to_dict(formula)
    chemical_element = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']

    #Check the presence of a element with 0 quantity
    for value in dict_formula.values():
        if value[0] == 0:
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
    """Complete check of the correctness of the chemical formula

    Args:
        formula: A string representing the chemical formula

    Raises:
        EmptyFormula: ValueError indicating the string is empty
        FirstElementAbsent: ValueError indicating the string starts with a number; the first atom is absent
        NonAlphaNumericValue: ValueError indicating the presence of symbol different from numbers and letters
        ZeroQuantityElement: ValueError indicating the presence of element with  quantity 0 in the formula
        NonExistentElement: ValueError indicating the presence of letters non representing atomic symbol
        RepeatedElement: ValueError indicating the repetition of an atomic symbol

    """
    basic_check_formula(formula)
    advanced_check_formula(formula)



def from_string_to_dict(formula):
    """Transform the chemical formula from a string to a dict

    Transform the string representing the chemical formula into a dictionary,
    where the keys are the atomic symbols and the values are list containing quantity.

    Args:
        formula: A string representing the chemical formula

    Returns:
        A dictionary containing the atomic symbols are keys and the list of quantity as values
    """

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


def csv_to_dataframe(path,header = False,property = [],robust = False):
    """Load a csv file containing chemical formula and transform it into a DataFrame

    Load a csv file containig chemical formula in a column into a pandas DataFrame. The Pandas DataFrame has element symbols and chemical formula as columns;
    If property is not a empty list there are preperty names too as columns. Every row represent a material with the relative quantity written in the columns.

    Args:
        path: A string containig the path and the name of the csv file
        header: Optional (Default:False); A boolean indicating if the csv file have as first row the word 'formula'
        property: Optional; A list containg the name of other property, excluded 'formula', of the material both written in the csv file
        robust: Optional ( Default:False); A Boolean stopping the conversion into a DataFrame if mispelled or wrong formula are found.
                If robust is set to True it continue skipping the problematic formula

    Return:
        A pandas DataFrame with columns set as element symbols, as chemical formula and as property element if present
    """

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
        formula_dataset = pd.read_csv(path,index_col=False)
        names = list(formula_dataset.columns)
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
            except ValueError:
                #Pass to the next iteration
                continue
        #controlla funzionamento con robust e senza
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

import sys
sys.path.append('/home/claudio/chela/env_chela/lib/python3.6/site-packages')
import pandas as pd
#%%

@pd.api.extensions.register_dataframe_accessor("chemdata")
class ChemDataFrame:
    """Extention of the pandas dataframe to deal with chemical data"""

    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def __repr__(self):
        return self._obj.head()

    #Transform a string containing a chemical formula into a dict
    @staticmethod
    def from_string_to_dict(formula):
        """Transform the chemical formula from a string to a dict

        Transform the string representing the chemical formula into a dictionary,
        where the keys are the atomic symbols and the values are list containing quantity.

        Args:
            formula: A string representing the chemical formula

        Returns:
            A dictionary containing the atomic symbols are keys and the list of quantity as values
        """

        return from_string_to_dict(formula)

    #Transform a csv file containing chemical formulas into a pandas dataframe
    @staticmethod
    def csv_to_dataframe(path,header = False,property = [],robust = False):
        """Load a csv file containing chemical formula and transform it into a DataFrame

        Load a csv file containig chemical formula in a column into a pandas DataFrame. The Pandas DataFrame has element symbols and chemical formula as columns;
        If property is not a empty list there are preperty names too as columns. Every row represent a material with the relative quantity written in the columns.

        Args:
            path: A string containig the path and the name of the csv file
            header: Optional (Default:False); A boolean indicating if the csv file doesn't have as first row the word 'formula'
            property: Optional; A list containg the name of other property, excluded 'formula', of the material both written in the csv file
            robust: Optional ( Default:False); A Boolean stopping the conversion into a DataFrame if mispelled or wrong formula are found.
                        If robust is set to True it continue skipping the problematic formula

        Return:
            A pandas DataFrame with columns set as element symbols, as chemical formula and as property element if present
        """

        return csv_to_dataframe(path,header = header,property = property,robust = robust)

    #Check the correctness of the chemical formula
    @staticmethod
    def check_formula(formula):
        """Complete check of the correctness of the chemical formula

        Args:
            formula: A string representing the chemical formula

        Raises:
            EmptyFormula: ValueError indicating the string is empty
            FirstElementAbsent: ValueError indicating the string starts with a number; the first atom is absent
            NonAlphaNumericValue: ValueError indicating the presence of symbol different from numbers and letters
            ZeroQuantityElement: ValueError indicating the presence of element with  quantity 0 in the formula
            NonExistentElement: ValueError indicating the presence of letters non representing atomic symbol
            RepeatedElement: ValueError indicating the repetition of an atomic symbol

        """

        return check_formula(formula)


    def drop_heavy_elements(self,Z):
        """Drop heavier element with atomic number greater than Z

        Drops chemical formula containing atoms with atomic number strictly greater than Z

        Args:
            Z: Atomic number of the greatest atoms that can be present in the chemical formulas

        Return:
            Pandas DataFrame with the selected materials
        """
        chem_data = self._obj
        Z -=1
        chem_data = chem_data[chem_data.iloc[:,Z:].sum(axis=1) == 0]

        return chem_data
