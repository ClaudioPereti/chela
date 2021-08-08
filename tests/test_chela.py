import sys
sys.path.append('chela/')
import chela
import pytest

@pytest.mark.parametrize('check_formula',
                                   ['',
                                   '1',
                                   '123H',
                                   '3O',
                                   '?Ge',
                                   'Mn!',
                                   'O#F',
                                   ])


def test_check_formula(check_formula):
    with pytest.raises(ValueError):
        chela.check_formula(check_formula)

@pytest.mark.parametrize('string_formula,dict_formula',
                                   [
                                   ('H',{'H':1}),
                                   ('H2O',{'H':2,'O':1}),
                                   ('OH',{'H':1,'O':1}),
                                   ('NH3',{'N':1,'H':3}),
                                   ])

def test_from_string_to_dict(string_formula,dict_formula):
    assert chela.from_string_to_dict(string_formula) == dict_formula
