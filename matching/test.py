from helper import *

def test_suffix_website():
    tests = [('https://www.airbus.com', 'airbus.com'), ('http://www.paprec.com', 'paprec.com'), ('www.microsoft.com', 'microsoft.com')]
    for entry, desired in tests:
        assert(suffix_website(entry) == desired)
        
def test_suffix_phone():
    tests = [('+33 5 57 83 12 35', '57831235'), ('557831235', '57831235'), ('33 1 42 04 05 87', '42040587'), ('01 42 04 05 87', '42040587')]
    for entry, desired in tests:
        assert(suffix_phone(entry) == desired)
        
def test_decompose_name():
    tests = [('Daiichi Sankyo Europe GmbH', {'daiichi', 'sankyo', 'europe', 'gmbh'}), ('JPMorgan Chase & Co.',  {'jpmorgan', 'chase', '&', 'co.'})]
    for entry, desired in tests:
        assert(decompose_name(entry) == desired)
        
        
test_suffix_website()
test_suffix_phone()
test_decompose_name()