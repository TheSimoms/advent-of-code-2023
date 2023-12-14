from task import Task


class Task14(Task):
    def part_one(self):
        return self._total_load(self._tilt_platform(self.data))

    def part_two(self):
        iterations = 1000000000
        i = 0

        layout = tuple(tuple(line) for line in self.data)
        known_layouts = dict()

        while i < iterations:
            i += 1

            for _ in range(4):
                layout = self._tilt_platform(layout)
                layout = tuple(zip(*layout[::-1]))

            if layout in known_layouts:
                cycle = i - known_layouts[layout]

                i += ((iterations - i) // cycle) * cycle

            known_layouts[layout] = i

        return self._total_load(layout)

    @staticmethod
    def _tilt_platform(layout) -> list[list[str]]:
        height = len(layout)
        width = len(layout[0])

        new_layout = [['.'] * width for _ in range(height)]
        next_row: list = [-1] * width

        for y in range(height):
            for x in range(width):
                symbol = layout[y][x]

                if symbol == 'O':
                    next_row[x] += 1
                    new_layout[next_row[x]][x] = 'O'
                elif symbol == '#':
                    new_layout[y][x] = '#'
                    next_row[x] = y

        return new_layout

    @staticmethod
    def _total_load(layout) -> int:
        height = len(layout)
        res = 0

        for row_number, row in enumerate(layout):
            res += (height - row_number) * row.count('O')

        return res
