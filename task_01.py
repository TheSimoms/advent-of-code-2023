import re

from task import Task


class Task01(Task):
    REGEX_ONE = re.compile(r'[0-9]')
    REGEX_TWO = re.compile(r'(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))')
    NUMBERS = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
    }

    def part_one(self) -> int:
        digits = [self._find_digits(line) for line in self.data]

        return self._sum_lines(digits)

    def part_two(self) -> int:
        digits_and_numbers = [self._find_digits_and_numbers(line) for line in self.data]

        return self._sum_lines(digits_and_numbers)

    def _find_digits(self, line: str) -> list[int]:
        return [int(number) for number in self.REGEX_ONE.findall(line)]

    def _find_digits_and_numbers(self, line: str) -> list[int]:
        return [int(number) if number.isdigit() else self.NUMBERS[number] for number in self.REGEX_TWO.findall(line)]

    @staticmethod
    def _sum_lines(lines: list[list[int]]) -> int:
        return sum([int(f"{line[0]}{line[-1]}") for line in lines])
