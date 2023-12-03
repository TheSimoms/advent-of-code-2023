from task import Task
from abc import ABCMeta


class Element(metaclass=ABCMeta):
    pass


class Number(Element):
    def __init__(self, first_digit: str):
        self.string_value = first_digit

    def add_digit(self, digit: str):
        self.string_value += digit

    def value(self):
        return int(self.string_value)

    def __repr__(self):
        return f'Number({self.string_value})'


class Symbol(Element):
    def __init__(self, x: int, y: int, value: str):
        self.x = x
        self.y = y
        self.value = value

    def __repr__(self):
        return f'Symbol({self.x}, {self.y})'

    def adjacent_cells(self, layout: list[list[Element]]) -> list[tuple[int, int]]:
        max_x = len(layout[0])
        max_y = len(layout)

        adjacent_cells = [(x, y) for x in range(self.x - 1, self.x + 2) for y in range(self.y - 1, self.y + 2)]
        valid_adjacent_cells = []

        for (x, y) in adjacent_cells:
            if x < 0 or y < 0:
                continue

            if x >= max_x or y >= max_y:
                continue

            valid_adjacent_cells.append((x, y))

        return valid_adjacent_cells

    def adjacent_numbers(self, layout: list[list[Element]]) -> set[Number]:
        adjacent_elements: list[Element] = [layout[y][x] for (x, y) in self.adjacent_cells(layout)]

        return set(element for element in adjacent_elements if type(element) is Number)

    def gear_ratio(self, layout: list[list[Element]]) -> int:
        if self.value == '*' and len(self.adjacent_numbers(layout)) == 2:
            parts = list(self.adjacent_numbers(layout))

            return parts[0].value() * parts[1].value()
        else:
            return 0


class NoOp(Element):
    def __repr__(self):
        return 'NoOp()'


class Engine:
    def __init__(self, data):
        self.height = len(data)
        self.width = len(data[0])

        self.layout: list[list[Element]] = [[NoOp()] * self.width for _ in range(self.height)]
        self.symbols: list[Symbol] = []

    def element_at(self, x: int, y: int) -> Element:
        return self.layout[y][x]

    def add_symbol(self, symbol: Symbol):
        self.symbols.append(symbol)

    def add_element(self, x, y, element: Element):
        self.layout[y][x] = element


class Task3(Task):
    def part_one(self) -> int:
        engine = self.parse_engine()
        parts: set[Number] = set()

        for symbol in engine.symbols:
            for adjacent_number in symbol.adjacent_numbers(engine.layout):
                parts.add(adjacent_number)

        return sum(part.value() for part in parts)

    def part_two(self):
        engine = self.parse_engine()

        return sum(symbol.gear_ratio(engine.layout) for symbol in engine.symbols)

    def parse_engine(self) -> Engine:
        engine = Engine(self.data)

        for y in range(len(self.data)):
            current_element = None

            for x in range(len(self.data[y])):
                char = self.data[y][x]

                if char.isdigit():
                    if type(current_element) is Number:
                        current_element.add_digit(char)
                    else:
                        current_element = Number(char)
                elif char == '.':
                    current_element = NoOp()
                else:
                    current_element = Symbol(x, y, char)

                    engine.add_symbol(current_element)

                engine.add_element(x, y, current_element)

        return engine
