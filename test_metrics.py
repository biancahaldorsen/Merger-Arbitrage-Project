from spread import calculate_spread, calculate_offer_value, calculate_annualized_return, calculate_implied_p
import pytest
#
# Test cases for implied probability : a normal case, p above 1, p below 0, and the zero-divisor case. 
def test_normal_implied_p(): 
    normal_implied_p = calculate_implied_p(6,4,2)
    assert normal_implied_p == 0.5

def test_pG1_implied_p(): 
    pG1_implied_p = calculate_implied_p(4,6,2)
    assert pG1_implied_p == 2.0

def test_pL0_implied_p(): 
    pL0_implied_p = calculate_implied_p (2,6,4)
    assert pL0_implied_p == -1.0

def test_dividebyZero_implied_p(): 
    dividebyZero_implied_p = calculate_implied_p (4,6,4)
    assert dividebyZero_implied_p is None 

#Test cases for offer value: 
# case with just cash 
# case with no cash
# cash with both 
def test_justcash_ov(): 
    offer_value = calculate_offer_value(50)
    assert offer_value == 50
def test_nocash_ov():
    offer_value = calculate_offer_value(0, 1.11, 36.72)
    assert offer_value == pytest.approx(40.7592)
def test_both_ov(): 
    offer_value = calculate_offer_value (96, 0.9693, 64.15)
    assert offer_value ==  pytest.approx(158.180595)
#Test cases for annualized return: 
# normal case where offer value is greater than the target
# case where offer value is less than the target 
# case where the target is = 0, case where days expected to close is <= 0. 
def test_normal_ar(): 
    annualized_return = calculate_annualized_return(10, 8, 20)
    assert annualized_return == pytest.approx(4.5625)
def test_offer_lessthan(): 
    annualized_return = calculate_annualized_return(8, 10, 20)
    assert annualized_return == pytest.approx(-3.65)
def test_target_is_negative(): 
    annualized_return = calculate_annualized_return(10, -8, 20)
    assert annualized_return is None
def test_days_is_zero(): 
    annualized_return = calculate_annualized_return(10, 8, 0)
    assert annualized_return is None
def test_days_is_negative():
    annualized_return = calculate_annualized_return(10, 8, -20)
    assert annualized_return is None