from app import process_query, check_name, check_age, check_tel, check_email
import pytest


def test_knows_about_dinosaurs():
    assert process_query("dinosaurs") == \
           "Dinosaurs ruled the Earth 200 million years ago"


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


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
