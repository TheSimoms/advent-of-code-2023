import re

from src.util.input import read_input


NUMBERS_MAP = {
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

REGEX_ONE = re.compile(r'[0-9]')


def find_digits(line: str) -> list[int]:
    return [int(number) for number in REGEX_ONE.findall(line)]


def find_digits_and_numbers(line: str) -> list[int]:
    res = []

    for i in range(len(line)):
        if line[i].isdigit():
            res.append(int(line[i]))
        else:
            substring = line[i:]

            for number, digit in NUMBERS_MAP.items():
                if substring.startswith(number):
                    res.append(digit)

    return res


def sum_lines(lines: list[list[int]]) -> int:
    return sum([int(f"{line[0]}{line[-1]}") for line in lines])


def part_one(data: list[str]):
    digits = [find_digits(line) for line in data]

    print(f'Part 1: {sum_lines(digits)}')


def part_two(data: list[str]):
    digits_and_numbers = [find_digits_and_numbers(line) for line in data]

    print(f'Part 2: {sum_lines(digits_and_numbers)}')


def run():
    data = read_input(1)

    part_one(data)
    part_two(data)


if __name__ == '__main__':
    run()
