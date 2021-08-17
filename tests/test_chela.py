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
            pd.DataFrame().chemdata.check_formula(basic_check_formula)

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
        assert not pd.DataFrame().chemdata.check_formula(basic_check_formula)


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
            pd.DataFrame().chemdata.check_formula(advanced_check_formula)


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
        assert not pd.DataFrame().chemdata.check_formula(advanced_check_formula)

@pytest.mark.parametrize('string_formula,dict_formula',
                                   [
                                   ('H',{'H':[1]}),
                                   ('H2O',{'H':[2],'O':[1]}),
                                   ('OH',{'H':[1],'O':[1]}),
                                   ('NH3',{'N':[1],'H':[3]}),
                                   ])

class TestStringoToDict:
    """Test the correctness of the conversion from string to dictionary"""

    def test_from_string_to_dict(self,string_formula,dict_formula):
        assert chela.from_string_to_dict(string_formula) == dict_formula


    def test_pandas_ext_from_string_to_dict(self,string_formula,dict_formula):
         assert pd.DataFrame().chemdata.from_string_to_dict(string_formula) == dict_formula



@pytest.mark.parametrize("elements,header,property",[
                            ('./tests/test_data/elements.csv',False,[]),
                            ('./tests/test_data/elements_non_header.csv',True,[]),
                            ('./tests/test_data/elements_header_property.csv',False,[]),
                            ('./tests/test_data/elements_non_header_property.csv',True,['atomic_number'])
                            ])

class TestCsvToDataframe:
    """Test the correctness of the conversion from csv file containing all the atoms to pandas DataFrame"""
    def test_pandas_ext_csv_to_dataframe_all_elements(self,elements,header,property):

        #Transform the csv file into a pandas DataFrame
        data = pd.DataFrame.chemdata.csv_to_dataframe(path = elements,header=header,property=property)
        #The data are all the atoms, so 118 elements
        #Peel off other columns that aren't atomic symbols
        data = data.iloc[:,:118]
        assert (data.to_numpy() == np.eye(118,118)).all()
        #if other columns are present check if they are the wanted ones
        if data.shape > (118,118):
            #assert ['formula','atomic number'] in list(data.columns)
            assert 'formula' in list(data.columns)
            #assert 'atomic number' in list(data.columns)

    def test_csv_to_dataframe_all_elements(self,elements,header,property):

        #Transform the csv file into a pandas DataFrame
        data = chela.csv_to_dataframe(path = elements,header=header,property=property)
        #The data are all the atoms, so 118 elements
        #Peel off other columns that aren't atomic symbols
        data_pure = data.iloc[:,:118]
        assert (data_pure.to_numpy() == np.eye(118,118)).all()
        #if other columns are present check if they are the wanted ones
        if data.shape > (118,118):
            assert 'formula' in list(data.columns)
            if data.shape > (118,119):
                assert 'atomic_number' in list(data.columns)



@pytest.mark.parametrize("chemical_formula,header,property,chemical_formula_checked",[
                            ('tests/test_data/chemical_formula.csv',False,[],'tests/test_data/chemical_formula_checked.csv'),
                            ('tests/test_data/chemical_formula_property.csv',False,[],'tests/test_data/chemical_formula_property_checked.csv'),
                            ('tests/test_data/chemical_formula_non_header.csv',True,[],'tests/test_data/chemical_formula_non_header_checked.csv'),
                            ('tests/test_data/chemical_formula_non_header_property.csv',True,['property'],'tests/test_data/chemical_formula_non_header_property_checked.csv')
                             ])

class TestCsvToDataframeMolecules:
    """Test the correctness of the conversion from csv file containing molecules to pandas DataFrame"""
    def test_pandas_ext_csv_to_dataframe_all_elements(self,chemical_formula,header,property,chemical_formula_checked):

        #Transform the data, chemical formulas, into a pandas dataframe
        data = pd.DataFrame.chemdata.csv_to_dataframe(path = chemical_formula,header=header,property=property)
        data_checked = pd.read_csv(chemical_formula_checked)
        assert (data == data_checked).all().all()

    def test_csv_to_dataframe_all_elements(self,chemical_formula,header,property,chemical_formula_checked):

        #Transform the data, chemical formulas, into a pandas dataframe
        data = pd.DataFrame.chemdata.csv_to_dataframe(path = chemical_formula,header=header,property=property)
        data_checked = pd.read_csv(chemical_formula_checked)
        assert (data == data_checked).all().all()


@pytest.mark.parametrize("elements,header,property,robust",[
                            ('./tests/test_data/elements_robust.csv',False,[],True),
                            ])

def test_csv_to_dataframe_all_elements(elements,header,property,robust):
    """Test if wrong formulas block the conversion into a dataframe"""

    #Transform the csv file into a pandas DataFrame
    data = chela.csv_to_dataframe(path = elements,header=header,property=property,robust=robust)
    #The data are all the atoms, so 118 elements
    #Peel off other columns that aren't atomic symbols
    data_pure = data.iloc[:,:118]
    assert (data_pure.to_numpy() == np.eye(118,118)).all()
    #if other columns are present check if they are the wanted ones
    if data.shape > (118,118):
        assert 'formula' in list(data.columns)
        if data.shape > (118,119):
            assert 'atomic_number' in list(data.columns)

@pytest.mark.parametrize("chemical_formula,header,property,robust,chemical_formula_checked",[
                            ('tests/test_data/chemical_formula_robust.csv',False,[],True,'tests/test_data/chemical_formula_checked.csv'),
                            ])

def test_csv_to_dataframe_all_elements(chemical_formula,header,property,robust,chemical_formula_checked):
    """Test if wrong formulas block the conversion into a dataframe"""

    #Transform the data, chemical formulas, into a pandas dataframe
    data = pd.DataFrame.chemdata.csv_to_dataframe(path = chemical_formula,header=header,property=property,robust=robust)
    #Load the correct Dataframe containg the formulas
    data_checked = pd.read_csv(chemical_formula_checked)
    #Compare the two daraframe
    assert (data == data_checked).all().all()
