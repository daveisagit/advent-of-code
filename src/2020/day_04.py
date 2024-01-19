"""Advent of code 2020
--- Day 4: Passport Processing ---
"""

import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    person = {}
    for line in raw_data:
        if not line:
            data.append(person)
            person = {}
            continue
        arr = tok(line)
        for i in arr:
            arr = tok(i, ":")
            v = None
            if len(arr) > 1:
                v = arr[1]
            person[arr[0]] = v

    data.append(person)
    return data


EXPECTED = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}


def is_valid(person):
    """Is the passport valid"""
    check = EXPECTED.copy()
    given = set(person.keys())
    check.difference_update(given)
    return not check or check == {"cid"}


def is_valid_b(person):
    """Is the passport valid B"""

    def valid_number(n, low, upp):
        try:
            n = int(n)
            return low <= n <= upp
        except ValueError:
            return False

    valid = is_valid(person)
    if not valid:
        return valid

    v = person["byr"]
    if not valid_number(v, 1920, 2002):
        return False

    v = person["iyr"]
    if not valid_number(v, 2010, 2020):
        return False

    v = person["eyr"]
    if not valid_number(v, 2020, 2030):
        return False

    v = person["hgt"]
    if v.endswith("cm"):
        v = v[:-2]
        valid = valid_number(v, 150, 193)
    elif v.endswith("in"):
        v = v[:-2]
        valid = valid_number(v, 59, 76)
    else:
        valid = False
    if not valid:
        return False

    v = person["hcl"]
    m = re.match(r"#[a-f0-9]{6}$", v)
    if not m:
        return False

    v = person["ecl"]
    if v not in (tok("amb blu brn gry grn hzl oth")):
        return False

    v = person["pid"]
    m = re.match(r"\d{9}$", v)
    if not m:
        return False

    return True


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return len([person for person in data if is_valid(person)])


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return len([person for person in data if is_valid_b(person)])


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
