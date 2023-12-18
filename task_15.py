import re

from task import Task


class Lens:
    def __init__(self, label: str, focal_length: int, index: int):
        self.label = label
        self.focal_length = focal_length
        self.index = index

    def __repr__(self) -> str:
        return f'[{self.label} {self.focal_length} {self.index}]'


class Box:
    def __init__(self, index: int):
        self.index = index
        self.lenses: dict[str, Lens] = {}
        self.lens_index = 0

    def __repr__(self) -> str:
        return f'Box {self.index}: {self.lenses.values()}'

    def sorted_lenses(self) -> list[tuple[int, Lens]]:
        return [lens for lens in enumerate(sorted(self.lenses.values(), key=lambda x: x.index))]

    def add_lens(self, label, focal_length):
        if label in self.lenses:
            self.lenses[label].focal_length = focal_length
        else:
            self.lenses[label] = Lens(label, focal_length, self.lens_index)
            self.lens_index += 1

    def remove_lens(self, label):
        self.lenses.pop(label, None)


class Operation:
    REGEX = re.compile(r'([a-z]+)([-=])([1-9]?)')
    HASHMAP: dict[str, int] = {}

    def __init__(self, step: str):
        label, operation, focal_length = self._parse(step)

        self.box = self._hash(label)
        self.label = label
        self.operator = operation
        self.focal_length = int(focal_length) if operation == '=' else None

    def __repr__(self) -> str:
        return f'{self.box:03}-{self.label}{self.operator}{self.focal_length if self.focal_length else ""}'

    def _parse(self, step: str) -> list[str]:
        return self.REGEX.findall(step)[0]

    def _hash(self, label) -> int:
        hashed_label = self.HASHMAP.get(label)

        if hashed_label is None:
            hashed_label = Task15.hash(label)

            self.HASHMAP[label] = hashed_label

        return hashed_label


class Task15(Task):
    def part_one(self):
        return sum(self.hash(step) for step in self.input.strip().split(','))

    def part_two(self):
        boxes = {i: Box(i) for i in range(256)}

        for step in self.input.strip().split(','):
            operation = Operation(step)
            box = boxes[operation.box]

            if operation.operator == '-':
                box.remove_lens(operation.label)
            else:
                box.add_lens(operation.label, operation.focal_length)

        res = 0

        for box in boxes.values():
            for lens_index, lens in box.sorted_lenses():
                res += (box.index + 1) * (lens_index + 1) * lens.focal_length

        return res

    @staticmethod
    def hash(step) -> int:
        res = 0

        for char in step:
            res = ((res + ord(char)) * 17) % 256

        return res
