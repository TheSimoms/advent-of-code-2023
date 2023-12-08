import re
from math import gcd
from typing import Optional

from task import Task


class Node:

    def __init__(self, name: str, left: str, right: str):
        self.name = name
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f'{self.name} ({self.left}, {self.right})'

    def step(self, left_right: str) -> str:
        return self.left if left_right == 'L' else self.right

    @property
    def is_target(self) -> bool:
        return self.name.endswith('Z')


class Input:
    def __init__(self, left_right: str, start_nodes: list[Node], network: dict[str, Node]):
        self.left_right = left_right
        self.start_nodes = start_nodes
        self.network = network


class Task08(Task):
    REGEX = re.compile(r'([0-9A-Z]+) = \(([0-9A-Z]+), ([0-9A-Z]+)\)')

    def part_one(self) -> int:
        data = self._parse_input()
        start_node = [node for node in data.start_nodes if node.name == 'AAA'][0]

        return self._traverse(data, start_node)

    def part_two(self) -> int:
        data = self._parse_input()
        path_lengths = [self._traverse(data, node) for node in data.start_nodes]

        return self._lcm(path_lengths)

    def _parse_input(self) -> Input:
        left_right, _, *raw_nodes = self.input.split('\n')
        nodes = [Node(*self.REGEX.findall(node)[0]) for node in raw_nodes]
        network = {node.name: node for node in nodes}
        start_nodes = [node for node in nodes if node.name.endswith('A')]

        return Input(left_right, start_nodes, network)

    @staticmethod
    def _traverse(data: Input, node: Node) -> int:
        index = 0
        first_target: Optional[Node] = None
        paths: list[int] = list()

        while True:
            step = data.left_right[index % len(data.left_right)]
            node = data.network[node.step(step)]
            index = index + 1

            if node.is_target:
                if node == first_target:
                    return paths[0]
                else:
                    paths.append(index)
                    first_target = node

    @staticmethod
    def _lcm(numbers: list[int]) -> int:
        res = 1

        for number in numbers:
            res = (number * res) // gcd(number, res)

        return res
