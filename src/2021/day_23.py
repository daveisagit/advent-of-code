"""Advent of code 2021
--- Day 23: Amphipod ---

Part B
add lines to data in between 1st & last
  #D#C#B#A#
  #D#B#A#C#
"""

from collections import deque
from common.aoc import file_to_list_rstrip, aoc_part, get_filename

AMPHIPODS = "ABCD"
amphipod_energy = {a: 10**i for i, a in enumerate(AMPHIPODS)}
amphipod_room = {a: i * 2 + 3 for i, a in enumerate(AMPHIPODS)}


def parse_data(raw_data):
    """Parse the input, returns a graph of the floor plan,
    starting position and type of each amphipod"""
    rooms = []
    for _ in range(4):
        rooms.append([])
    for ri, line in enumerate(raw_data):
        for ci, c in enumerate(line):
            if c in AMPHIPODS:
                r = (ci - 3) // 2
                rooms[r].append(c)

    return rooms


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""

    rooms = data
    corridor = [" "] * 11
    room_size = len(data[0])

    initial_state = (0, tuple(corridor), tuple(tuple(r) for r in rooms))
    lowest_energy_solution = None

    bfs = deque()
    seen = set()
    bfs.append(initial_state)

    while bfs:
        state = bfs.popleft()
        energy, corridor, rooms = state
        if state in seen:
            continue
        seen.add(state)

        todo = {
            ri
            for ri, room in enumerate(rooms)
            for a in room
            if AMPHIPODS.index(a) != ri
        }

        ready_rooms = {
            ri
            for ri, room in enumerate(rooms)
            if ri not in todo and len(room) < room_size
        }

        done_rooms = {
            ri
            for ri, room in enumerate(rooms)
            if ri not in todo and len(room) == room_size
        }

        if len(done_rooms) == 4:
            if lowest_energy_solution is None or lowest_energy_solution > energy:
                lowest_energy_solution = energy
            continue

        for r in ready_rooms:
            rp = (r * 2) + 2
            a = AMPHIPODS[r]

            # room to room
            sources = [
                s for s in range(4) if r != s and len(rooms[s]) > 0 and rooms[s][0] == a
            ]
            for s in sources:
                sp = (s * 2) + 2
                blockers = [b for b in corridor[min(rp, sp) : max(rp, sp)] if b != " "]
                if blockers:
                    continue
                new_rooms = list(list(r) for r in rooms)
                new_rooms[s].pop(0)
                new_rooms[r].insert(0, a)
                dist = (
                    room_size
                    - len(new_rooms[s])
                    + abs(rp - sp)
                    + room_size
                    - len(new_rooms[r])
                    + 1
                )
                energy_rqd = amphipod_energy[a] * dist
                bfs.append(
                    (energy + energy_rqd, corridor, tuple(tuple(r) for r in new_rooms))
                )

            # corridor to room
            sources = [ci for ci, ca in enumerate(corridor) if ca == a]
            for sp in sources:
                if sp < rp:
                    blockers = [b for b in corridor[sp + 1 : rp] if b != " "]
                else:
                    blockers = [b for b in corridor[rp:sp] if b != " "]
                if blockers:
                    continue
                new_rooms = list(list(r) for r in rooms)
                new_rooms[r].insert(0, a)
                new_corridor = list(corridor)
                new_corridor[sp] = " "
                dist = abs(rp - sp) + room_size - len(new_rooms[r]) + 1
                energy_rqd = amphipod_energy[a] * dist
                bfs.append(
                    (
                        energy + energy_rqd,
                        tuple(new_corridor),
                        tuple(tuple(r) for r in new_rooms),
                    )
                )

        # room to corridor
        for r in todo:
            rp = (r * 2) + 2
            left = 0
            for i in range(rp, left - 1, -1):
                if corridor[i] != " ":
                    left = i + 1
                    break

            right = len(corridor) - 1
            for i in range(rp, right + 1):
                if corridor[i] != " ":
                    right = i - 1
                    break

            for tp in range(left, right + 1):
                if tp % 2 == 0 and 2 <= tp <= 8:
                    continue
                new_rooms = list(list(r) for r in rooms)
                new_corridor = list(corridor)
                a = new_rooms[r].pop(0)
                new_corridor[tp] = a
                dist = abs(rp - tp) + room_size - len(new_rooms[r])
                energy_rqd = amphipod_energy[a] * dist
                bfs.append(
                    (
                        energy + energy_rqd,
                        tuple(new_corridor),
                        tuple(tuple(r) for r in new_rooms),
                    )
                )

    return lowest_energy_solution


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return len(data)


EX_RAW_DATA = file_to_list_rstrip(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list_rstrip(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

# solve_part_b(EX_DATA)
# solve_part_b(MY_DATA)
