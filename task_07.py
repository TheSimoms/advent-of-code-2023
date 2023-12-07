from collections import defaultdict
from functools import total_ordering
from typing import Any

from task import Task


@total_ordering
class Hand:
    RANKS_NO_JOKER = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    RANKS_JOKER = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']

    def __init__(self, raw_hand: str, use_jokers: bool = False):
        self.raw_hand = raw_hand
        self.hand = self._parse_hand(raw_hand, use_jokers)
        self.card_values = [self.RANKS_JOKER.index(card) if use_jokers else self.RANKS_NO_JOKER.index(card) for card in raw_hand]
        self.hand_type = self._type()

    def __repr__(self) -> str:
        return f'{self.raw_hand}, type: {self.hand_type} ({self.hand})'

    @staticmethod
    def _parse_hand(hand: str, use_jokers: bool) -> dict[Any, int]:
        cards = defaultdict(int)

        for card in hand:
            cards[card] += 1

        if use_jokers and 0 < cards.get('J', 0) < 5:
            number_of_jokers = cards.pop('J')

            cards[max(cards.items(), key=lambda x: x[1])[0]] += number_of_jokers

        return dict(cards)

    def _type(self) -> int:
        card_counts = [card[1] for card in sorted(self.hand.items(), key=lambda x: x[1], reverse=True)]

        if card_counts[0] == 5:
            return 6
        elif card_counts[0] == 4:
            return 5
        elif card_counts[0] == 3:
            if card_counts[1] == 2:
                return 4
            else:
                return 3
        elif card_counts[0] == 2:
            if card_counts[1] == 2:
                return 2
            else:
                return 1
        else:
            return 0

    def __gt__(self, other) -> bool:
        if self.hand_type == other.hand_type:
            return self._compare_cards(other) > 0

        return self.hand_type > other.hand_type

    def __eq__(self, other) -> bool:
        if self.hand_type != other.hand_type:
            return False

        return self._compare_cards(other) == 0

    def _compare_cards(self, other) -> int:
        for self_index, other_index in zip(self.card_values, other.card_values):
            if self_index < other_index:
                return 1
            elif other_index < self_index:
                return -1

        return 0


class Task07(Task):

    def part_one(self) -> int:
        return self._generate_winnings()

    def part_two(self) -> int:
        return self._generate_winnings(use_jokers=True)

    def _generate_winnings(self, use_jokers: bool = False) -> int:
        hands = []

        for cards, bid in [line.split() for line in self.data]:
            hands.append((Hand(cards, use_jokers), int(bid)))

        return sum(bid * (i + 1) for i, (_, bid) in enumerate(sorted(hands, key=lambda x: x[0])))
