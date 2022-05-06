"""Module containg test of chela modules"""

import sys
sys.path.append('chela/')
import chela
import pandas as pd
import numpy as np
import pytest


@pytest.mark.parametrize('basic_check_formula',
                                   [
                                   '',
                                   '1',
                                   '123H',
                                   'Al9o2',
                                   '3O',
                                   '?Ge',
                                   'Mn!',
                                   'O#F',
                                   ])

class TestBasicFormula:
    """Tests for basic check formula as function and as method.

       Test if the check_formula detect void formulas,incorrect characters,formulas starting with numbers, only numbers.
    """

    def test_basic_check_formula(self,basic_check_formula):
        with pytest.raises(ValueError):
            chela.basic_check_formula(basic_check_formula)


    def test_first_part_check_formula(self,basic_check_formula):
        with pytest.raises(ValueError):
            chela.check_formula(basic_check_formula)

    def test_pandas_ext_check_formula(self,basic_check_formula):
        with pytest.raises(ValueError):
            pd.DataFrame().chela.check_formula(basic_check_formula)

@pytest.mark.parametrize('basic_check_formula',
                                   [
                                   'H',
                                   'Al9',
                                   'OH',
                                   'Ge',
                                   'Mn91Al1',
                                   'OFH',
                                   'Mn42.3Al63.1Fe21.0'
                                   ])

class TestBasicFormula:
    """Tests for basic check formula as function and as method.

       Test if the check_formula detect void formulas,incorrect characters,formulas starting with numbers, only numbers.
    """

    def test_basic_check_formula(self,basic_check_formula):
        assert not chela.basic_check_formula(basic_check_formula)


    def test_first_part_check_formula(self,basic_check_formula):
        assert not chela.check_formula(basic_check_formula)

    def test_pandas_ext_check_formula(self,basic_check_formula):
        assert not pd.DataFrame().chela.check_formula(basic_check_formula)


@pytest.mark.parametrize('advanced_check_formula',
                                    [
                                    'H0',
                                    'H2O0',
                                    'Xu',
                                    'Yoyo2',
                                    'HH',
                                    'HOFO',
                                    'N2H6N2',
                                     ])

class TestAdvancedFormula:
    """Tests for advanced check formula as function and as method.

       Test if the check_formula detect 0 quantity, inexistent atomic symbols, repeated elements.
    """

    def test_advanced_check_formula(self,advanced_check_formula):
        with pytest.raises(ValueError):
            chela.advanced_check_formula(advanced_check_formula)

    def test_second_part_check_formula(self,advanced_check_formula):
        with pytest.raises(ValueError):
            chela.check_formula(advanced_check_formula)

    def test_pandas_ext_check_formula(self,advanced_check_formula):
        with pytest.raises(ValueError):
            pd.DataFrame().chela.check_formula(advanced_check_formula)


@pytest.mark.parametrize('advanced_check_formula',
                                   [
                                   'H',
                                   'Al9',
                                   'OH',
                                   'Ge',
                                   'Mn91Al1',
                                   'OFH',
                                   'Mn42.3Al63.1Fe21.0'
                                   ])

class TestAdvancedFormula:
    """Tests for advanced check formula as function and as method.

       Test if the check_formula detect 0 quantity, inexistent atomic symbols, repeated elements.
    """

    def test_advanced_check_formula(self,advanced_check_formula):
        assert not chela.advanced_check_formula(advanced_check_formula)

    def test_second_part_check_formula(self,advanced_check_formula):
        assert not chela.check_formula(advanced_check_formula)

    def test_pandas_ext_check_formula(self,advanced_check_formula):
        assert not pd.DataFrame().chela.check_formula(advanced_check_formula)

@pytest.mark.parametrize('string_formula,dict_formula',
                                   [
                                   ('H',{'H':1}),
                                   ('H2O',{'H':2,'O':1}),
                                   ('OH',{'H':1,'O':1}),
                                   ('NH3',{'N':1,'H':3}),
                                   ('Al2O3',{'Al':2,'O':3}),
                                   ('CaCO3',{'Ca':1,'C':1,'O':3}),
                                   ('Na2CO3',{'Na':2,'C':1,'O':3}),
                                   ('Al63.0Fe20.1Mn10.2',{'Al':63.0,'Fe':20.1,'Mn':10.2}),
                                   ])

class TestStringoToDict:
    """Test the correctness of the conversion from string to dictionary"""

    def test_from_string_to_dict(self,string_formula,dict_formula):
        assert chela.from_string_to_dict(string_formula) == dict_formula


    def test_pandas_ext_from_string_to_dict(self,string_formula,dict_formula):
         assert pd.DataFrame().chela.from_string_to_dict(string_formula) == dict_formula



@pytest.mark.parametrize("elements,header",[
                            ('./tests/test_data/elements.csv',True,),
                            ('./tests/test_data/elements_header_property.csv',True,),
                            ])

class TestCsvToDataframe:
    """Test the correctness of the conversion from csv file containing all the atoms to pandas DataFrame"""
    def test_pandas_ext_build_dataframe_all_elements(self,elements,header):

        #Transform the csv file into a pandas DataFrame
        if header:
            dataset = pd.read_csv(elements)
        else:
            dataset = pd.read_csv(elements,names=['formula'])

        data = pd.DataFrame.chela.build_dataframe(dataset)

        #The data are all the atoms, so 118 elements
        #Peel off other columns that aren't atomic symbols
        data = data.iloc[:,:118]
        assert ((data.to_numpy() - np.eye(118,118))<0.0001).all()
        #if other columns are present check if they are the wanted ones
        if data.shape > (118,118):
            assert 'formula' in list(data.columns)

    def test_build_dataframe_all_elements(self,elements,header):

        #Transform the csv file into a pandas DataFrame
        dataset = pd.read_csv(elements)
        data = pd.DataFrame.chela.build_dataframe(dataset)
        #The data are all the atoms, so 118 elements
        #Peel off other columns that aren't atomic symbols
        data_pure = data.iloc[:,:118]
        assert (data_pure.to_numpy() == np.eye(118,118)).all()
        #if other columns are present check if they are the wanted ones
        if data.shape > (118,118):
            assert 'formula' in list(data.columns)



@pytest.mark.parametrize("chemical_formula,header,chemical_formula_checked",[
                            ('tests/test_data/chemical_formula.csv',True,'tests/test_data/chemical_formula_checked.csv'),
                            ('tests/test_data/chemical_formula_property.csv',True,'tests/test_data/chemical_formula_property_checked.csv'),
                             ])

class TestCsvToDataframeMolecules:
    """Test the correctness of the conversion from csv file containing molecules to pandas DataFrame"""
    def test_pandas_ext_build_dataframe_all_elements(self,chemical_formula,header,chemical_formula_checked):

        #Transform the data, chemical formulas, into a pandas dataframe
        dataset = pd.read_csv(chemical_formula)
        data = pd.DataFrame.chela.build_dataframe(dataset)
        data_checked = pd.read_csv(chemical_formula_checked)
        #remove string columns to compare them
        data = data.iloc[:,:118]
        data_checked = data_checked.iloc[:,:118]

        assert ((data - data_checked)<0.001).all().all()

    def test_build_dataframe_all_elements(self,chemical_formula,header,chemical_formula_checked):

        #Transform the data, chemical formulas, into a pandas dataframe
        dataset = pd.read_csv(chemical_formula)
        data = pd.DataFrame.chela.build_dataframe(dataset)
        data_checked = pd.read_csv(chemical_formula_checked)
        #remove string columns
        data = data.iloc[:,:118]
        data_checked = data_checked.iloc[:,:118]

        assert ((data - data_checked)<0.001).all().all()



@pytest.mark.parametrize("chemical_formula,header,chemical_formula_checked",[
                        ('tests/test_data/10000_chemical_formulas_with_labels.csv',True,'tests/test_data/10000_chemical_formulas_with_labels_checked.csv'),
                        ('tests/test_data/10000_chemical_formulas.csv',True,'tests/test_data/10000_chemical_formulas_checked.csv'),

                         ])

def test_pandas_ext_build_dataframe(chemical_formula,header,chemical_formula_checked):

    #Transform the data, chemical formulas, into a pandas dataframe
    dataset = pd.read_csv(chemical_formula)
    data = pd.DataFrame.chela.build_dataframe(dataset)

    data = data.drop(axis = 0,columns = data.iloc[:,96:118].columns)
    data_checked = pd.read_csv(chemical_formula_checked)

    data = data.iloc[:,:96]
    data_checked = data_checked.iloc[:,:96]


    assert ((data - data_checked)<0.001).all().all()



@pytest.mark.parametrize("elements,header",[
                            ('./tests/test_data/elements_robust.csv',True),
                            ])

def test_build_dataframe_all_elements(elements,header):
    """Test if wrong formulas block the conversion into a dataframe"""

    with pytest.warns(UserWarning,match="Some chemical formulas have been skipped because they are wrong or written in an unrecognized format"):
        #Transform the csv file into a pandas DataFrame
        dataset = pd.read_csv(elements)
        data = pd.DataFrame.chela.build_dataframe(dataset)

        #The data are all the atoms, so 118 elements
        #Peel off other columns that aren't atomic symbols
        data_pure = data.iloc[:,:118]
        assert (data_pure.to_numpy() == np.eye(118,118)).all()
        #if other columns are present check if they are the wanted ones
        if data.shape > (118,118):
            assert 'formula' in list(data.columns)

@pytest.mark.parametrize("chemical_formula,header,chemical_formula_checked",[
                            ('tests/test_data/chemical_formula_robust.csv',True,'tests/test_data/chemical_formula_checked.csv'),
                            ])

def test_build_dataframe_all_elements(chemical_formula,header,chemical_formula_checked):
    """Test if wrong formulas block the conversion into a dataframe"""
    #Transform the csv file into a pandas DataFrame
    dataset = pd.read_csv(chemical_formula)
    data = pd.DataFrame.chela.build_dataframe(dataset)

    #Load the correct Dataframe containg the formulas
    data_checked = pd.read_csv(chemical_formula_checked)
    #Compare the two daraframe
    assert (data == data_checked).all().all()


@pytest.mark.parametrize("chemical_formula",[
                            ('tests/test_data/chemical_formula.csv'),
                            ])

def test_drop_heavy_elements(chemical_formula):

    #Transform the data, chemical formulas, into a pandas dataframe
    dataset = pd.read_csv(chemical_formula)
    data = pd.DataFrame.chela.build_dataframe(dataset)

    # Drop manually the formula with Z greater than 8
    data_checked = data.drop(axis = 0,index = [0,3,4])
    # Drop using the method
    data = data.chela.drop_heavy_elements(8)
    assert (data == data_checked).all().all()
