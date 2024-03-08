"""For handling all AoC kinda stuff"""

from functools import wraps
from os import environ, path
import sys
from time import time


ENCODING = "utf-8"


def get_filename(fn, input_type):
    """The get filepath
    if a input_type given (i.e. ex or my) then returns a path
    {AOC_DATA_PATH}/year/day_nn/my.txt
    We keep the data in a separate repository (private) as it is under copyright
    """
    if len(input_type) == 2:
        aoc_data_path = environ.get("AOC_DATA_PATH")
        day = str(path.basename(fn))[4:6]
        year = path.basename(path.dirname(fn))
        new_fn = f"{aoc_data_path}/{year}/day_{day}/{input_type}.txt"
        return new_fn
    return fn


def dump_path(fn):
    """The get a filepath for dumping output"""
    aoc_data_path = environ.get("AOC_DATA_PATH")
    day = str(path.basename(fn))[4:6]
    year = path.basename(path.dirname(fn))
    dump_path = f"{aoc_data_path}/{year}/day_{day}/dump.txt"
    return dump_path


def file_to_list(filename: str):
    """Read text file to list of strings"""
    with open(filename, encoding=ENCODING) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def file_to_list_rstrip(filename: str):
    """Read text file to list of strings"""
    with open(filename, encoding=ENCODING) as f:
        lines = f.readlines()
    return [line.rstrip() for line in lines]


def file_to_list_no_strip(filename: str):
    """Read text file to list of strings"""
    with open(filename, encoding=ENCODING) as f:
        lines = f.readlines()
    return [line[:-1] for line in lines]


def file_to_string(filename: str):
    """Read whole file as string"""
    with open(filename, encoding=ENCODING) as f:
        content = f.read()
    return content


def aoc_part(func):
    """Decorator which will log the runtime etc."""

    @wraps(func)
    def aoc_part_wrapper(*args, **kwargs):
        part = str(func.__name__)[-1].upper()
        print()
        # module_name = (sys.modules[func.__module__]).__file__
        print(f"Solving part {part}")
        if len(args) > 0:
            try:
                input_size = len(args[0])
                print(f"Input size: {input_size}")
            except TypeError:
                pass

        start_time = time()
        answer = func(*args, **kwargs)
        print(f"Answer: {answer}")
        end_time = time()

        elapsed_time = end_time - start_time
        print(f"Duration: {elapsed_time:.3f} s")

        return answer

    return aoc_part_wrapper
