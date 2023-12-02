from abc import ABCMeta, abstractmethod


class Task(metaclass=ABCMeta):
    def __init__(self):
        self.data = None

    def run(self, args):
        self.data = self._read_input(args)

        print(f'Part one: {self.part_one()}')
        print(f'Part two: {self.part_two()}')

    @abstractmethod
    def part_one(self):
        pass

    @abstractmethod
    def part_two(self):
        pass

    @staticmethod
    def _read_input(args) -> list[str]:
        filename = f'{args.task}-test' if args.test else str(args.task)

        with open(f'data/{filename}.txt', 'r') as file:
            return [line.strip() for line in file if line]
