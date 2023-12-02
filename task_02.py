import re

from task import Task


class Draw:
    def __init__(self, cubes: dict[str, int]):
        self.blue = cubes.get('blue', 0)
        self.green = cubes.get('green', 0)
        self.red = cubes.get('red', 0)


class Game:
    REGEX = re.compile(r'(?P<count>[0-9]+) (?P<colour>[a-z]+)')

    def __init__(self, line: str):
        name, draws = line.split(': ')

        self.number = self.parse_name(name)
        self.draws = self.parse_draws(draws)

    @staticmethod
    def parse_name(name: str) -> int:
        return int(name.split(' ')[1])

    def parse_draws(self, draws: str) -> list[Draw]:
        return [Draw({cube['colour']: int(cube['count']) for cube in self.REGEX.finditer(draw)}) for draw in draws.split('; ')]

    def is_legal(self, blue: int, green: int, red: int) -> bool:
        for draw in self.draws:
            if draw.blue > blue or draw.green > green or draw.red > red:
                return False

        return True


class Task2(Task):
    def part_one(self) -> int:
        blue = 14
        green = 13
        red = 12

        games = [Game(line) for line in self.data]
        total = 0

        for game in games:
            if game.is_legal(blue, green, red):
                total += game.number

        return total

    def part_two(self) -> int:
        games = [Game(line) for line in self.data]
        total = 0

        for game in games:
            blue = max([draw.blue for draw in game.draws])
            green = max([draw.green for draw in game.draws])
            red = max([draw.red for draw in game.draws])

            total += blue * green * red

        return total
