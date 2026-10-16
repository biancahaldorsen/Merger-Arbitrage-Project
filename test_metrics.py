from spread import calculate_spread, calculate_offer_value, calculate_annualized_return, calculate_implied_p
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

