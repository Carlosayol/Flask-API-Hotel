import re
from urllib.parse import urlparse

def has_numbers(inputString):
    """
    Check if given string contains digits
    @param {inputString}: string
    returns: Boolean
    """
    return any(char.isdigit() for char in inputString)


def is_valid_email(inputString):
    """
    Check if given string is a valid email
    @param {inputString}: string
    returns: Boolean
    """
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return bool(re.search(email_regex, inputString))

def is_valid_url(inputString):
    """
    Check if given string is a valid email
    @param {inputString}: string
    returns: Boolean
    """
    try:
        result = urlparse(inputString)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False