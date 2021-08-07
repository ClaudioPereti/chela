import sys
sys.path.append('chela/')
import chela
import pytest

@pytest.mark.parametrize('formula',['','H'])


def tests_check_formula(formula):
    with pytest.raises(ValueError):
        chela.check_formula(formula)
