import pytest
from app import check_age, check_email, check_name, check_tel, process_query


def test_knows_about_dinosaurs():
    assert process_query("dinosaurs") == \
           "Dinosaurs ruled the Earth 200 million years ago"


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_knows_name():
    assert process_query("What is your name?") == "itsarainyday"


def test_which_of_the_following():
    assert process_query(
        "Which of the following numbers is the largest: 40, 29, 49?") == "49"


def test_sum():
    assert process_query("What is 57 plus 55") == "112"


def test_mult():
    assert process_query("What is 88 multiplied by 45") == "3960"


def test_is_sq_and_cube():
    assert process_query(
        "square and cube: 64, 3626, 1254, 1, 36, 2095, 3933") == "64, 1"


def test_subtract():
    assert process_query("75 minus 30") == "45"


def test_is_prime():
    assert process_query("primes: 55, 85, 97, 5, 12") == "[97, 5]"


@pytest.mark.parametrize("test_input,expected",
                         [("Matthew", True),
                          ("M@tthew", False),
                          ("12345", False)])
def test_check_name(test_input, expected):
    assert check_name(test_input) == expected


@pytest.mark.parametrize("test_input,expected",
                         [("12", True),
                          ("Matthew", False),
                          ("12!", False)])
def test_check_age(test_input, expected):
    assert check_age(test_input) == expected


@pytest.mark.parametrize("test_input,expected",
                         [("0123456789", True),
                          ("123456789", False),
                          ("+441234567", False)])
def test_check_tel(test_input, expected):
    assert check_tel(test_input) == expected


@pytest.mark.parametrize("test_input,expected",
                         [("test@ic.ac.uk", True),
                          ("test@gmail.com", False),
                          ("test@ic.ac.uk@gmail.com", False)])
def test_check_email(test_input, expected):
    assert check_email(test_input) == expected
