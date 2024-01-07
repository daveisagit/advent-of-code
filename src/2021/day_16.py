"""Advent of code 2021
--- Day 16: Packet Decoder ---
"""

from collections import namedtuple
import math
from common.aoc import file_to_string, aoc_part, get_filename

Packet = namedtuple(
    "Packet",
    ["version", "type", "value"],
)


def make_packet(bin_str) -> tuple:
    """Make a packet from the given string and add it as a sub packet to a given parent"""
    version = int(bin_str[:3], 2)
    typ = int(bin_str[3:6], 2)
    sub_packets = []
    bin_str = bin_str[6:]

    # literal
    if typ == 4:
        lit = ""
        while True:
            chunk = bin_str[:5]
            bin_str = bin_str[5:]
            digit = f"{(int(chunk[1:], 2)):01x}"
            lit += digit
            if chunk[0] == "0":
                break
        value = int(lit, 16)

    # operator
    else:
        length_type = bin_str[0]
        bin_str = bin_str[1:]
        if length_type == "0":
            length = int(bin_str[:15], 2)
            bin_str = bin_str[15:]
            start_length = len(bin_str)
            while start_length - length < len(bin_str):
                packet, bin_str = make_packet(bin_str)
                sub_packets.append(packet)

        else:
            length = int(bin_str[:11], 2)
            bin_str = bin_str[11:]
            for _ in range(length):
                packet, bin_str = make_packet(bin_str)
                sub_packets.append(packet)

        value = sub_packets

    return Packet(version, typ, value), bin_str


def version_sum(packet: Packet) -> int:
    """Return the version sum of a packet"""
    vs = packet.version
    sub_sum = 0
    if isinstance(packet.value, list):
        sub_sum = sum(version_sum(sp) for sp in packet.value)
    return vs + sub_sum


def evaluate_packet(packet: Packet) -> int:
    """Return the value a packet"""
    if isinstance(packet.value, int):
        return packet.value

    # sum
    if packet.type == 0:
        return sum(evaluate_packet(sp) for sp in packet.value)
    # prod
    if packet.type == 1:
        return math.prod(evaluate_packet(sp) for sp in packet.value)
    # min
    if packet.type == 2:
        return min(evaluate_packet(sp) for sp in packet.value)
    # max
    if packet.type == 3:
        return max(evaluate_packet(sp) for sp in packet.value)
    # >
    if packet.type == 5:
        v = [evaluate_packet(sp) for sp in packet.value]
        return 1 if v[0] > v[1] else 0
    # <
    if packet.type == 6:
        v = [evaluate_packet(sp) for sp in packet.value]
        return 1 if v[0] < v[1] else 0
    # =
    if packet.type == 7:
        v = [evaluate_packet(sp) for sp in packet.value]
        return 1 if v[0] == v[1] else 0


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


def hex_to_bin(hex_serial):
    """Serial hex to binary"""
    return "".join([f"{int(h, 16):04b}".format(int(h, 16)) for h in hex_serial])


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    binary_string = hex_to_bin(data)
    packet, _ = make_packet(binary_string)
    return version_sum(packet)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    binary_string = hex_to_bin(data)
    packet, _ = make_packet(binary_string)
    return evaluate_packet(packet)


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
