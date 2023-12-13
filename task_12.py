from task import Task


class Task12(Task):
    def part_one(self):
        res = 0

        for line in self.data:
            springs, all_groups = line.split()
            groups = [int(group_size) for group_size in all_groups.split(',')]

            res += self.number_of_permutations(springs, groups)

        return res

    def part_two(self):
        res = 0

        for line in self.data:
            springs, all_groups = line.split()
            groups = [int(group_size) for group_size in all_groups.split(',')]

            res += self.number_of_permutations('?'.join([springs] * 5), groups * 5)

        return res

    def number_of_permutations(self, springs: str, groups: list[int], solutions: dict[str, int] = None) -> int:
        if solutions is None:
            solutions = dict()

        if not groups:
            return int('#' not in springs)

        if not springs:
            return int(not groups)

        key = self.key(springs, groups)

        if key in solutions:
            return solutions[key]

        res = 0
        next_spring = springs[0]
        next_group_size = groups[0]

        if next_spring != "#":
            res += self.number_of_permutations(springs[1:], groups, solutions)

        if next_spring != "." and next_group_size <= len(springs):
            next_spring_group = springs[:next_group_size]

            if '.' in next_spring_group:
                return res

            if next_group_size == len(springs) or springs[next_group_size] != "#":
                res += self.number_of_permutations(springs[next_group_size + 1:], groups[1:], solutions)

        solutions[key] = res

        return res

    @staticmethod
    def key(springs: str, groups: list[int]) -> str:
        return f'{springs}{groups}'
