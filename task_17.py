import heapq
from collections import namedtuple
from enum import Enum
from typing import Callable

from task import Task

Position = namedtuple('Position', ['x', 'y'])
Step = namedtuple('Step', ['x', 'y', 'direction', 'direction_repeats'])


class Direction(Enum):
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    DOWN = (0, 1)
    UP = (0, -1)


class Tile:
    def __init__(self, step: Step, total_cost: int):
        self.step = step
        self.total_cost = total_cost

    def __repr__(self) -> str:
        return f'({self.step.x}, {self.step.y}): {self.total_cost} - {self.step.direction} - {self.step.direction_repeats}'

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def __gt__(self, other):
        return self.total_cost > other.total_cost


class City:
    def __init__(self, data: list[str]):
        self.height = len(data)
        self.width = len(data[0])

        self.costs: list[list[int]] = [[] * self.width for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                self.costs[y].append(int(data[y][x]))

    def is_valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height


class Task17(Task):
    def part_one(self):
        city = City(self.data)
        end = Position(city.height - 1, city.width - 1)

        return self.find_cost(
            city=city,
            start=Position(0, 0),
            end_condition=lambda step: step.x == end.x and step.y == end.y,
            turn_is_valid=lambda step, direction: True,
            step_is_valid=lambda direction_repeats: direction_repeats <= 3,
        )

    def part_two(self):
        city = City(self.data)
        end = Position(city.height - 1, city.width - 1)

        return self.find_cost(
            city=city,
            start=Position(0, 0),
            end_condition=lambda step: step.x == end.x and step.y == end.y and step.direction_repeats >= 4,
            turn_is_valid=lambda step, direction: step.direction == direction or step.direction_repeats >= 4,
            step_is_valid=lambda direction_repeats: direction_repeats <= 10,
        )

    @staticmethod
    def find_cost(city: City, start: Position, end_condition: Callable[[Step], bool],
                  turn_is_valid: Callable[[Step, Direction], bool], step_is_valid: Callable[[int], bool]) -> int:
        queue = [Tile(Step(start.x, start.y, None, 0), 0)]
        used_steps: dict[Step, int] = {}

        while queue:
            tile = heapq.heappop(queue)

            step = tile.step
            total_cost = tile.total_cost

            if end_condition(step):
                return tile.total_cost

            if step in used_steps:
                continue

            used_steps[step] = tile.total_cost

            for direction in Direction:
                if step.direction and not turn_is_valid(step, direction):
                    continue

                direction_repeats = step.direction_repeats + 1 if step.direction == direction else 1

                if not step_is_valid(direction_repeats):
                    continue

                if step.direction:
                    if not ((step.direction.value[0] + direction.value[0]) or (
                            step.direction.value[1] + direction.value[1])):
                        continue

                x = step.x + direction.value[0]
                y = step.y + direction.value[1]

                if not city.is_valid(x, y):
                    continue

                new_step = Step(x, y, direction, direction_repeats)

                if new_step in used_steps:
                    continue

                heapq.heappush(queue, Tile(new_step, total_cost + city.costs[y][x]))
