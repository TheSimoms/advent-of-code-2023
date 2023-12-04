import re

from task import Task


class Card:
    REGEX_CARD_NUMBERS = re.compile('\\s+')

    def __init__(self, index: str, winning_numbers: str, drawn_numbers: str):
        self.index: int = int(index) - 1
        self.winning_numbers: list[int] = [int(number) for number in self.REGEX_CARD_NUMBERS.split(winning_numbers)]
        self.drawn_numbers: list[int] = [int(number) for number in self.REGEX_CARD_NUMBERS.split(drawn_numbers)]

        self.winners = [number for number in self.drawn_numbers if number in self.winning_numbers]
        self.number_of_winners = len(self.winners)
        self.points = 2 ** (self.number_of_winners - 1) if self.number_of_winners else 0
        self.new_card_indices = [] if not self.number_of_winners else [self.index + 1 + i for i in range(self.number_of_winners)]

    def __repr__(self):
        return (f'Card {self.index + 1}: {self.points} points, {self.winners} '
                f'([{", ".join([str(number) for number in self.winning_numbers])}], '
                f'[{", ".join([str(number) for number in self.drawn_numbers])}])')


class Task04(Task):
    REGEX_CARD = re.compile('Card\\s+(?P<card_number>[0-9]+):\\s+(?P<winning_numbers>.*)\\s+\\|\\s+(?P<drawn_numbers>.*)')

    def part_one(self) -> int:
        return int(sum(card.points for card in self.parse_cards()))

    def part_two(self):
        cards = list(self.parse_cards())
        cards_in_play = cards.copy()
        i = 0

        while i < len(cards_in_play):
            cards_in_play.extend([cards[i] for i in cards_in_play[i].new_card_indices])

            i += 1

        return len(cards_in_play)

    def parse_cards(self) -> list[Card]:
        for line in self.data:
            try:
                index, winning_numbers, drawn_numbers = self.REGEX_CARD.findall(line)[0]
            except Exception as exception:
                print(f'Exception with line {line}')
                print(exception)

                raise exception

            yield Card(index, winning_numbers, drawn_numbers)
