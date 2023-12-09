from task import Task


class Task09(Task):
    def part_one(self) -> int:
        return sum(sum(history[-1] for history in histories) for histories in self._build_histories())

    def part_two(self) -> int:
        res = 0

        for histories in self._build_histories():
            previous_value = 0

            for history in histories[::-1]:
                previous_value = history[0] - previous_value

            res += previous_value

        return res

    def _build_histories(self) -> list[list[list[int]]]:
        differences = []

        for line in self.data:
            latest_history = [int(number) for number in line.split()]
            histories = [latest_history]

            while True:
                new_history = []
                all_zeroes = True

                for i in range(len(latest_history) - 1):
                    diff = latest_history[i + 1] - latest_history[i]
                    new_history.append(diff)

                    if diff:
                        all_zeroes = False

                histories.append(new_history)

                latest_history = new_history

                if all_zeroes:
                    break

            differences.append(histories)

        return differences
