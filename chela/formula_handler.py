"""Module containg functions and pandas extention to help handling chemical formula string.
   The functions and the pandas extension methods are almost the same, the pandas extension
   has the 'drop_heavy_elements' method that is not avaible as function and the functions
   have the possibility to use 'basic_check_formula' and 'advanced_check_formula' separately.
   The pandas extension's method are written in a functional way, they will always return the
   pandas DataFrame elaborathed as output.
"""

from chela.chela_error import *
import pandas as pd
import numpy as np
import re


def basic_check_formula(formula):
    """Check the basic correctness of the chemical formula,i.e. empty string, absent element, presence of non alphanumeric value,non existent element

    Args:
        formula: A string representing the chemical formula

    Raises:
        EmptyFormula: ValueError indicating the string is empty
        FirstElementAbsent: ValueError indicating the string starts with a number; the first atom is absent
        NonAlphaNumericValue: ValueError indicating the presence of symbol different from numbers and letters excluded 0
        NonExistentElement: ValueError indicating the presence of non existent atomic symbol
    """

    #Check if the string is empty
    if not formula:
        raise EmptyFormula
    #Check if the first element is present
    if formula[0].isnumeric():
        raise FirstElementAbsent
    #Check the presence of non alphanumeric values, excluded . and included negative quantity
    alphanumplus = [(lambda letter: letter.isalnum() or letter == '.')(letter) for letter in formula]
    if not all(alphanumplus):
        raise NonAlphaNumericValue
    #Check for inexistent atomic symbols
    for index,letter in enumerate(formula):
        if letter.islower() and formula[index-1].isnumeric():
            raise NonExistentElement


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
        if value == 0:
            raise ZeroQuantityElement

    #Check the presence of inexistent or mispelled element
    for element in dict_formula.keys():
        if not element in chemical_element:
            raise NonExistentElement

    #Check if an element is repeated in the formula, using the fact that a dictionary overwrite a key if alredy present
    atoms_symbols = ''.join(list(from_string_to_dict(formula).keys()))
    complete_atoms_symbols = [letter for letter in formula if letter.isalpha()]

    if len(complete_atoms_symbols) != len(atoms_symbols):
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

    #Split the string in groups of chemical element (symbol) and quantity
    list_formula = list(filter(None,re.split('([A-Z][a-z]?(?=[A-Z])|[0-9]+[.][0-9]*|[.][0-9]+|[0-9]+)',formula)))
    dict_formula= {}
    #Runs over the list looking for atomic symbols
    for index,symbol_or_quantity in enumerate(list_formula):

        if symbol_or_quantity.isalpha():

            atom = symbol_or_quantity
            #If the last element is a symbol it means it has 1 as quantity
            if index+1 >= len(list_formula):
                dict_formula[atom] = 1.0
                break
            #Set the quantity as a value of the dictionary with the relative symbol/key
            if list_formula[index+1].replace('.','1').isdigit():
                dict_formula[atom] = float(list_formula[index+1])
            #In case the quantity equal to 1 is implied
            if list_formula[index+1].isalpha():
               dict_formula[atom] = 1.0

    return dict_formula


def csv_to_dataframe(path,header = True):
    """Load a csv file containing chemical formula and transform it into a DataFrame

    Turn a csv file containig chemical formula and other property in columns into a pandas DataFrame.
    The Pandas DataFrame has element symbols and chemical formula (and other property if present
    in the file) as columns;
    Each row represent a material formula: the relative quantity is written fir each chemical element in the columns.

    First column must contain the chemical formulas written as strings.

    Args:
        path: A string containig the path and the name of the csv file
        header: Optional (Default:True); A boolean indicating if the csv file has as first row the word 'formula'

    Return:
        A pandas DataFrame with columns set as element symbols, as chemical formula and as property element if present
    """


    #Load csv file from path
    #Header is True if the csv file contain the header
    if header:
        dataset_formula = pd.read_csv(path,index_col=False)
        names = list(dataset_formula.columns)
        dataset_formula = dataset_formula.rename(columns = {names[0]:'formula'})
    #If False we rename the first column(that contain the chemical formulas as string) with formula
    else:
        dataset_formula = pd.read_csv(path,header = None,index_col=False)
        dataset_formula = dataset_formula.rename(columns = {0:'formula'})


    #Symbols of chemical elements
    chemical_element = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']


    list_material_as_dictionary = [from_string_to_dict(material['formula']) for _,material in dataset_formula.iterrows() if take_good_formula_skip_bad_formula(material['formula'])]
    dataset_material = pd.DataFrame(list_material_as_dictionary,columns = chemical_element)
    dataset_material = dataset_material.replace(np.nan,0)

    #Send a warning if dataset_formula contain wrong formulas
    if len(list_material_as_dictionary) != dataset_formula.shape[0]:
        import warnings
        warnings.warn("Some chemical formulas have been skipped because they are wrong or written in an unrecognized format")

    #Add property to the material dataset
    if header:
        dataset_material.loc[:,names] = dataset_formula.loc[:,names]

    return dataset_material



def take_good_formula_skip_bad_formula(formula):
    """Return True if the formula si correct, False otherwise"""

    try:
        check_formula(formula)
        return True
    except ValueError:
        return False



@pd.api.extensions.register_dataframe_accessor("chela")
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
    def csv_to_dataframe(path,header = True):
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

        return csv_to_dataframe(path,header = header)

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
        # Keep only rows with 0 for elements greater than Z
        chem_data = chem_data[chem_data.iloc[:,Z:].sum(axis=1) == 0]

        return chem_data
