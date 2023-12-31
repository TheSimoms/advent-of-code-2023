from collections import namedtuple, defaultdict
from typing import Optional

from task import Task
from util import Position, Direction


Beam = namedtuple('Beam', ['start', 'end', 'direction'])


class Mirror:

    def __init__(self, x: int, y: int, symbol: str) -> None:
        self.x = x
        self.y = y
        self.symbol = symbol

        self.previous_x: Optional[Mirror] = None
        self.next_x: Optional[Mirror] = None

        self.previous_y: Optional[Mirror] = None
        self.next_y: Optional[Mirror] = None

    def __repr__(self) -> str:
        return f'{self.position} {self.symbol}'

    @property
    def position(self) -> Position:
        return Position(self.x, self.y)


class Grid:

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.mirrors: dict[Position, Mirror] = {}
        self.mirrors_row = defaultdict(list)
        self.mirrors_column = defaultdict(list)

    def is_mirror(self, position: Position) -> bool:
        return position in self.mirrors

    def add_mirror(self, mirror: Mirror) -> None:
        self.mirrors[mirror.position] = mirror

        mirrors_row = self.mirrors_row[mirror.y]
        mirrors_column = self.mirrors_column[mirror.x]

        if mirrors_row:
            mirror.previous_x = mirrors_row[-1]
            mirrors_row[-1].next_x = mirror

        if mirrors_column:
            mirror.previous_y = mirrors_column[-1]
            mirrors_column[-1].next_y = mirror

        mirrors_row.append(mirror)
        mirrors_column.append(mirror)

    def shoot_beam(self, mirror: Mirror, direction: Direction) -> list[Beam]:
        beams = []

        for new_direction in self._new_directions(mirror, direction):
            if new_direction == Direction.R:
                end = mirror.next_x.position if mirror.next_x else Position(self.width - 1, mirror.y)
            elif new_direction == Direction.L:
                end = mirror.previous_x.position if mirror.previous_x else Position(0, mirror.y)
            elif new_direction == Direction.D:
                end = mirror.next_y.position if mirror.next_y else Position(mirror.x, self.height - 1)
            else:
                end = mirror.previous_y.position if mirror.previous_y else Position(mirror.x, 0)

            if mirror.position != end:
                beams.append(
                    Beam(
                        start=mirror.position,
                        end=end,
                        direction=new_direction,
                    )
                )

        return beams

    @staticmethod
    def _new_directions(mirror: Mirror, direction: Direction) -> list[Direction]:
        if mirror.symbol == '\\':
            if direction == Direction.R:
                return [Direction.D]
            elif direction == Direction.L:
                return [Direction.U]
            elif direction == Direction.D:
                return [Direction.R]
            else:
                return [Direction.L]
        elif mirror.symbol == '/':
            if direction == Direction.R:
                return [Direction.U]
            elif direction == Direction.L:
                return [Direction.D]
            elif direction == Direction.D:
                return [Direction.L]
            else:
                return [Direction.R]
        elif mirror.symbol == '|':
            if direction in [Direction.D, Direction.U]:
                return [direction]
            else:
                return [Direction.D, Direction.U]
        elif mirror.symbol == '-':
            if direction in [Direction.R, Direction.L]:
                return [direction]
            else:
                return [Direction.R, Direction.L]
        else:
            raise Exception(f'Invalid symbol={mirror.symbol}')


class Task16(Task):

    def part_one(self):
        grid = self._parse_input()
        start_beam = Beam(Position(0, 0), grid.mirrors_row[0][0].position, Direction.R)

        return self.count_energized_tiles(grid, start_beam)

    def part_two(self):
        grid = self._parse_input()
        start_beams: list[Beam] = []

        for y in range(grid.height):
            mirrors = grid.mirrors_row[y]

            if mirrors:
                start_beams.append(
                    Beam(
                        start=Position(0, y),
                        end=mirrors[0].position,
                        direction=Direction.R,
                    )
                )

                start_beams.append(
                    Beam(
                        start=Position(grid.width - 1, y),
                        end=mirrors[-1].position,
                        direction=Direction.L,
                    )
                )

        for x in range(grid.width):
            mirrors = grid.mirrors_column[x]

            if mirrors:
                start_beams.append(
                    Beam(
                        start=Position(x, 0),
                        end=mirrors[0].position,
                        direction=Direction.D,
                    )
                )

                start_beams.append(
                    Beam(
                        start=Position(x, grid.height - 1),
                        end=mirrors[-1].position,
                        direction=Direction.U,
                    )
                )

        return max(self.count_energized_tiles(grid, beam) for beam in start_beams)

    @staticmethod
    def count_energized_tiles(grid: Grid, start_beam: Beam):
        beams = [start_beam]

        for (start, end, direction) in beams:
            if grid.is_mirror(end):
                for beam in grid.shoot_beam(grid.mirrors[end], direction):
                    if beam not in beams:
                        beams.append(beam)

        positions: set[Position] = set()

        for (start, end, direction) in beams:
            if start.x != end.x:
                for x in [start.x + x * direction.value[0] for x in range(abs(start.x - end.x) + 1)]:
                    positions.add(Position(x, start.y))
            else:
                for y in [start.y + y * direction.value[1] for y in range(abs(start.y - end.y) + 1)]:
                    positions.add(Position(start.x, y))

        return len(positions)

    def _parse_input(self) -> Grid:
        height = len(self.data)
        width = len(self.data[0])

        grid = Grid(width, height)

        for y in range(height):
            for x in range(width):
                symbol = self.data[y][x]

                if symbol != '.':
                    grid.add_mirror(Mirror(x, y, symbol))

        return grid
