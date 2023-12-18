import re
from collections import namedtuple

from task import Task
from util import Position, Direction


Dig = namedtuple('Dig', ['direction', 'distance'])


class Task18(Task):

    def part_one(self):
        digs: list[Dig] = []

        for line in self.data:
            direction, dig_distance, _ = line.split()

            digs.append(Dig(Direction[direction], int(dig_distance)))

        return self._calculate_volume(digs)

    def part_two(self):
        regex = re.compile(r'\(#([a-f0-9]{5})([0-3])\)')
        digs: list[Dig] = []
        directions = list(Direction)

        for line in self.data:
            _, _, colour = line.split()

            dig_distance, direction = regex.findall(colour)[0]

            digs.append(Dig(directions[int(direction)], int(dig_distance, 16)))

        return self._calculate_volume(digs)

    @staticmethod
    def _calculate_volume(digs: list[Dig]) -> int:
        edge_distance = 0
        corners = [Position(0, 0)]

        for direction, distance in digs:
            last_corner = corners[-1]

            edge_distance += distance

            corners.append(Position(last_corner.x + direction.value[0] * distance, last_corner.y + direction.value[1] * distance))

        number_of_corners = len(corners)
        res = 0

        for i in range(number_of_corners):
            res += corners[i - 1].x * corners[i].y - corners[i - 1].y * corners[i].x

        return (abs(res) // 2) + (edge_distance // 2) + 1
