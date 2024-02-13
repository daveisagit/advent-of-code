"""In order to output to the terminal without using colorma or curses
This has been kindly posted on SO
https://stackoverflow.com/questions/27612545/how-to-change-the-location-of-the-pointer-in-python/27612978#27612978

Simply offers a print_at function, you probably need to issue some blank prints to make space

It handles the scrolling of the terminal whilst running in VS code so what's not to like
"""

import ctypes
from ctypes import c_ulong, c_void_p, c_wchar_p


def stdout_handle():
    return ctypes.windll.kernel32.GetStdHandle(-11)


def adjust_for_console_scroll(coord: int):
    kernel32 = ctypes.windll.kernel32
    sbi = _ScreenBufferInfo()
    kernel32.GetConsoleScreenBufferInfo(stdout_handle(), ctypes.byref(sbi))
    whole_buffer_height = sbi.window.right
    visible_buffer_height = sbi.window.right - sbi.window.left

    if int(coord) < int(visible_buffer_height):
        return coord

    if int(whole_buffer_height) > int(coord):
        coord = whole_buffer_height

    return coord


class _Coord(ctypes.Structure):
    _fields_ = [("x", ctypes.c_short), ("y", ctypes.c_short)]


class _SmallRect(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_short),
        ("top", ctypes.c_short),
        ("right", ctypes.c_short),
        ("bottom", ctypes.c_short),
    ]


class _ScreenBufferInfo(ctypes.Structure):
    _fields_ = [
        ("size", _Coord),
        ("cursor_pos", _Coord),
        ("attrs", ctypes.c_int),
        ("window", _SmallRect),
        ("max_window_size", _Coord),
    ]


def print_at(text: str, x: int, y: int):
    kernel32 = ctypes.windll.kernel32
    sbi = _ScreenBufferInfo()
    kernel32.GetConsoleScreenBufferInfo(stdout_handle(), ctypes.byref(sbi))
    original_position = sbi.cursor_pos

    # Adjustment is required as the values are read starting from "1", but we
    # need to have zero-indexed values instead.
    x = x - 1
    y = y - 1
    y = adjust_for_console_scroll(y)
    position = x + (y << 16)
    kernel32.SetConsoleCursorPosition(stdout_handle(), position)
    kernel32.WriteConsoleW(
        stdout_handle(), c_wchar_p(text), c_ulong(len(text)), c_void_p(), None
    )
    kernel32.SetConsoleCursorPosition(stdout_handle(), original_position)
