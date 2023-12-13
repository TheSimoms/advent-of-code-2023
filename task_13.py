from task import Task


class Task13(Task):
    def part_one(self):
        patterns = self.input.split('\n\n')
        res = 0

        for pattern in patterns:
            rows = pattern.split('\n')
            columns = list(zip(*rows))

            res += 100 * self._find_reflection_one(rows)
            res += self._find_reflection_one(columns)

        return res

    def part_two(self):
        patterns = self.input.split('\n\n')
        res = 0

        for pattern in patterns:
            rows = pattern.split('\n')
            columns = list(zip(*rows))

            res += 100 * self._find_reflection_two(rows)
            res += self._find_reflection_two(columns)

        return res

    @staticmethod
    def _find_reflection_one(items) -> int:
        length = len(items)

        for split_line in range(1, length):
            for step in range(min(split_line, length - split_line)):
                if items[split_line - step - 1] != items[split_line + step]:
                    break
            else:
                return split_line

        return 0

    @staticmethod
    def _find_reflection_two(items) -> int:
        length = len(items)
        width = len(items[0])

        for split_line in range(1, length):
            smudge = None

            for step in range(min(split_line, length - split_line)):
                before_split = items[split_line - step - 1]
                after_split = items[split_line + step]

                if before_split != after_split:
                    if smudge is not None:
                        break

                    line_has_smudge = False

                    for i in range(width):
                        if before_split[i] != after_split[i]:
                            if line_has_smudge:
                                break

                            line_has_smudge = True
                    else:
                        smudge = step

                        continue

                    break
            else:
                if smudge is not None:
                    return split_line

        return 0
