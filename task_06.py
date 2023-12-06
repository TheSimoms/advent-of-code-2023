from task import Task


class Task06(Task):
    def part_one(self) -> int:
        res = 1

        for (time, record) in zip(map(int, self.data[0].split(':')[1].split()), map(int, self.data[1].split(':')[1].split())):
            number_of_ways_to_win = 0

            for seconds_to_hold in range(time):
                distance = (time - seconds_to_hold) * seconds_to_hold

                if distance > record:
                    number_of_ways_to_win += 1
                elif number_of_ways_to_win > 0:
                    break

            res *= number_of_ways_to_win

        return res

    def part_two(self):
        time = int(self.data[0].split(':')[1].replace(' ', ''))
        record = int(self.data[1].split(':')[1].replace(' ', ''))

        number_of_ways_to_win = 0

        for seconds_to_hold in range(time):
            distance = (time - seconds_to_hold) * seconds_to_hold

            if distance > record:
                number_of_ways_to_win += 1
            elif number_of_ways_to_win > 0:
                break

        return number_of_ways_to_win
