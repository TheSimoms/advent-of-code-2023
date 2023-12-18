import re
from abc import ABCMeta, abstractmethod


class Task(metaclass=ABCMeta):
    def __init__(self):
        self.input = None
        self.data = None

    def run(self, args):
        self.input = self._read_input(args)
        self.data = [line.strip() for line in self.input.split('\n') if line]

        print(f'Part one: {self.part_one()}')
        print(f'Part two: {self.part_two()}')

    @abstractmethod
    def part_one(self):
        pass

    @abstractmethod
    def part_two(self):
        pass

    def _read_input(self, args) -> str:
        task_number = re.findall(r'([0-9]+)', type(self).__name__)[0].rjust(2, '0')
        filename = f'{task_number}-test' if args.test else task_number

        with open(f'data/{filename}.txt', 'r') as file:
            return file.read().strip()
