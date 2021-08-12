import sys
sys.path.append('chela/')
import chela
import pandas as pd
import pytest


@pytest.mark.parametrize('basic_check_formula',
                                   [
                                   '',
                                   '1',
                                   '123H',
                                   '3O',
                                   '?Ge',
                                   'Mn!',
                                   'O#F',
                                   ])

class TestBasicFormula:

    def test_basic_check_formula(self,basic_check_formula):
        with pytest.raises(ValueError):
            chela.basic_check_formula(basic_check_formula)


    def test_first_part_check_formula(self,basic_check_formula):
        with pytest.raises(ValueError):
            chela.check_formula(basic_check_formula)

    def test_pandas_ext_check_formula(self,basic_check_formula):
        with pytest.raises(ValueError):
            pd.DataFrame().chemdata.check_formula(basic_check_formula)

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
    def test_advanced_check_formula(self,advanced_check_formula):
        with pytest.raises(ValueError):
            chela.advanced_check_formula(advanced_check_formula)

    def test_second_part_check_formula(self,advanced_check_formula):
        with pytest.raises(ValueError):
            chela.check_formula(advanced_check_formula)

    def test_pandas_ext_check_formula(self,advanced_check_formula):
        with pytest.raises(ValueError):
            pd.DataFrame().chemdata.check_formula(advanced_check_formula)


@pytest.mark.parametrize('string_formula,dict_formula',
                                   [
                                   ('H',{'H':[1]}),
                                   ('H2O',{'H':[2],'O':[1]}),
                                   ('OH',{'H':[1],'O':[1]}),
                                   ('NH3',{'N':[1],'H':[3]}),
                                   ])

class TestStringoToDict:
    def test_from_string_to_dict(self,string_formula,dict_formula):
        assert chela.from_string_to_dict(string_formula) == dict_formula


    def test_pandas_ext_from_string_to_dict(self,string_formula,dict_formula):
         assert pd.DataFrame().chemdata.from_string_to_dict(string_formula) == dict_formula
