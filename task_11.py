from task import Task


class Task11(Task):

    def part_one(self) -> int:
        return self._calculate_distances(rate=2)

    def part_two(self) -> int:
        return self._calculate_distances(rate=1000000)

    def _calculate_distances(self, rate: int) -> int:
        galaxies, empty_rows, empty_columns = self._parse_input()

        self._expand_universe(galaxies, empty_rows, empty_columns, rate)

        pairs = self._generate_galaxy_pairs(galaxies)
        res = 0

        for (galaxy_a_index, galaxy_b_index) in pairs:
            x_a, y_a = galaxies[galaxy_a_index]
            x_b, y_b = galaxies[galaxy_b_index]

            res += abs(x_a - x_b) + abs(y_a - y_b)

        return res

    @staticmethod
    def _expand_universe(galaxies: list[list[int, int]], empty_rows: set[int], empty_columns: set[int], rate: int):
        for galaxy in galaxies:
            x, y = galaxy

            galaxy[0] += len([column for column in empty_columns if column < x]) * (rate - 1)
            galaxy[1] += len([row for row in empty_rows if row < y]) * (rate - 1)

    def _parse_input(self) -> tuple[list[list[int, int]], set[int], set[int]]:
        height = len(self.data)
        width = len(self.data[0])

        height_range = range(height)
        width_range = range(width)

        non_empty_rows = set()
        non_empty_columns = set()
        galaxies = []

        for y in range(height):
            for x in range(width):
                tile = self.data[y][x]

                if tile == '#':
                    galaxies.append([x, y])
                    non_empty_rows.add(y)
                    non_empty_columns.add(x)

        empty_rows = set(height_range) - non_empty_rows
        empty_columns = set(width_range) - non_empty_columns

        return galaxies, empty_rows, empty_columns

    @staticmethod
    def _generate_galaxy_pairs(galaxies) -> list[tuple[int, int]]:
        number_of_galaxies = len(galaxies)
        pairs = []

        for i in range(number_of_galaxies - 1):
            for j in range(i + 1, number_of_galaxies):
                pairs.append((i, j))

        return pairs
