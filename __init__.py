import math

PERSON_SLOT = "person"


def is_float(input):
    if not input:
        return False
    try:
        num = float(input)
    except ValueError:
        return False
    return True


def is_int(input):
    if not input:
        return False
    try:
        num = int(input)
    except ValueError:
        return False
    return True


def round_up_10(x):
    return int(math.ceil(x / 10.0)) * 10
