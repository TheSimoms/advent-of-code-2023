from typing import Optional

from task import Task


class Tile:
    def __init__(self, symbol: str, x: int, y: int, height: int, width: int, previous_direction: Optional[str] = None):
        self.symbol = symbol

        self.x = x
        self.y = y

        self.height = height
        self.width = width

        self.next = self.calculate_next_move(previous_direction)

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'

    @property
    def is_goal(self) -> bool:
        return self.symbol == 'S'

    def calculate_next_move(self, previous_direction: str) -> Optional[tuple[str, tuple[int, int]]]:
        north = self.north if previous_direction != 'S' else None
        east = self.east if previous_direction != 'W' else None
        south = self.south if previous_direction != 'N' else None
        west = self.west if previous_direction != 'E' else None

        next_move = None

        if self.symbol == '|':
            next_move = ('N', north) if north else ('S', south)
        elif self.symbol == '-':
            next_move = ('E', east) if east else ('W', west)
        elif self.symbol == 'L':
            next_move = ('N', north) if north else ('E', east)
        elif self.symbol == 'J':
            next_move = ('N', north) if north else ('W', west)
        elif self.symbol == '7':
            next_move = ('S', south) if south else ('W', west)
        elif self.symbol == 'F':
            next_move = ('E', east) if east else ('S', south)

        return next_move

    @property
    def north(self) -> Optional[int]:
        return (self.x, self.y - 1) if self.y > 0 else None

    @property
    def east(self) -> Optional[int]:
        return (self.x + 1, self.y) if self.x < self.width - 1 else None

    @property
    def south(self) -> Optional[int]:
        return (self.x, self.y + 1) if self.y < self.height - 1 else None

    @property
    def west(self) -> Optional[int]:
        return (self.x - 1, self.y) if self.x > 0 else None


class Task10(Task):
    def part_one(self) -> int:
        data = self._parse_input()
        loop = self._find_loop(data)

        return len(loop) // 2 + len(loop) % 2

    def part_two(self) -> int:
        data = self._parse_input()
        loop = {(tile.x, tile.y): True for tile in self._find_loop(data)}
        res = 0

        enter_symbols = ['F', 'L']
        exit_symbols = ['7', 'J']

        for y in range(len(data)):
            enter_symbol = None
            is_inside = False

            for x in range(len(data[0])):
                symbol = data[y][x]

                if (x, y) in loop:
                    if symbol == '|':
                        is_inside = not is_inside
                    elif symbol in enter_symbols:
                        enter_symbol = symbol
                    elif symbol in exit_symbols:
                        if (enter_symbol == 'F' and symbol == '7') or (enter_symbol == 'L' and symbol == 'J'):
                            pass
                        else:
                            is_inside = not is_inside

                        enter_symbol = None
                elif is_inside:
                    res += 1

        return res

    def _find_loop(self, data: list[list[str]]) -> list[Tile]:
        height = len(self.data)
        width = len(self.data[0])

        start = self._find_start(data)
        previous = self._first_move(start, height, width)

        loop: list[Tile] = [previous]

        while True:
            (direction, (x, y)) = previous.next

            next_tile = Tile(self.data[y][x], x, y, height, width, direction)

            loop.append(next_tile)

            if next_tile.is_goal:
                final = loop[0]

                if final.y < next_tile.y:
                    next_tile.direction = 'N'
                elif final.x > next_tile.x:
                    next_tile.direction = 'E'
                elif final.y > next_tile.y:
                    next_tile.direction = 'S'
                else:
                    next_tile.direction = 'W'

                break

            previous = next_tile

        return loop

    def _find_start(self, data: list[list[str]]) -> Tile:
        height = len(data)
        width = len(data[0])

        for y in range(height):
            for x in range(width):
                if self.data[y][x] == 'S':
                    north_allowed = y > 0 and self.data[y - 1][x] in ['|', 'F', '7']
                    east_allowed = x < width - 1 and self.data[y][x + 1] in ['-', '7', 'J']
                    south_allowed = y < height - 1 and self.data[y + 1][x] in ['|', 'J', 'L']
                    west_allowed = x > 0 and self.data[y][x - 1] in ['-', 'F', 'L']

                    if north_allowed and south_allowed:
                        symbol = '|'
                    elif east_allowed and west_allowed:
                        symbol = '-'
                    elif north_allowed and east_allowed:
                        symbol = 'L'
                    elif north_allowed and west_allowed:
                        symbol = 'J'
                    elif south_allowed and east_allowed:
                        symbol = 'F'
                    elif south_allowed and west_allowed:
                        symbol = '7'
                    else:
                        raise Exception('Unexpected start symbol')

                    data[y][x] = symbol

                    return Tile(symbol, x, y, height, width)

    def _first_move(self, start, height, width) -> Tile:
        x = start.x
        y = start.y

        if y > 0 and self.data[y - 1][x] in ['|', '7', 'F']:
            next_move = ('N', (x, y - 1))
        elif x < width - 1 and self.data[y][x + 1] in ['-', 'J', '7']:
            next_move = ('E', (x + 1, y))
        elif y < height - 1 and self.data[y][x + 1] in ['|', 'L', 'J']:
            next_move = ('S', (x, y + 1))
        else:
            next_move = ('W', (x - 1, y))

        direction, (x, y) = next_move

        return Tile(self.data[y][x], x, y, height, width, direction)

    def _parse_input(self) -> list[list[str]]:
        return [list(line) for line in self.data]
