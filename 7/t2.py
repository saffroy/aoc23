from collections import Counter
from enum import Enum

TEST_DATA = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''

TEST_RESULT = 5905

CARD_VALUE = dict((c,v) for (v,c) in enumerate('J23456789TQKA'))

HandType = Enum('HandType', [
    # ordered from low to high strength
    'HIGH_CARD', 'ONE_PAIR', 'TWO_PAIR',
    'THREE_KIND', 'FULL_HOUSE', 'FOUR_KIND', 'FIVE_KIND'
])

def hand_type(cards):
    # set jokers aside, count other cards, add jokers to most frequent
    # special case: 5 jokers
    jokers = len([c for c in cards if c == 'J'])
    if jokers == 5:
        return HandType.FIVE_KIND

    ct = Counter(c for c in cards if c != 'J')
    counts = tuple(c for (_,c) in ct.most_common())
    counts = (counts[0]+jokers, ) + counts[1:]

    match counts:
        case (5,):
            return HandType.FIVE_KIND
        case (4, 1):
            return HandType.FOUR_KIND
        case (3, 2):
            return HandType.FULL_HOUSE
        case (3, 1, 1):
            return HandType.THREE_KIND
        case (2, 2, 1):
            return HandType.TWO_PAIR
        case (2, 1, 1, 1):
            return HandType.ONE_PAIR
        case (1, 1, 1, 1, 1):
            return HandType.HIGH_CARD
        case _:
            assert False, (cards, counts)

class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = bid
        self.hand_type = hand_type(cards)
        self.card_values = tuple(CARD_VALUE[c] for c in cards)
        self.hand_value = (self.hand_type.value, self.card_values)

def parse(lines):
    hands = []
    for line in lines:
        cards, bid = line.split()
        hand = Hand(cards, int(bid))
        hands.append(hand)

    winnings = sum(rank * hand.bid
                   for (rank, hand) in enumerate(
                           sorted(hands, key=lambda h: h.hand_value),
                           start=1))
    return winnings

def test():
    lines = TEST_DATA.splitlines()
    result = parse(lines)
    assert result == TEST_RESULT

def main():
    with open('input', encoding='ascii') as f:
        lines = list(map(str.strip, f.readlines()))
    result = parse(lines)
    print(result)

if __name__ == '__main__':
    main()
