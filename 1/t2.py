# AOC'23 day 1 part 2

import re

test_data = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''

test_result = [ 29, 83, 13, 24, 42, 14, 76 ]

def revstr(s):
    return ''.join(reversed(s))

def parse(lines):
    # zero isn't used but it's simpler this way
    digits_words = [
        'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'
    ]
    assert len(digits_words) == 10

    # map words representing digits to corresponding integers
    digits_map = dict((digits_words[i], i) for i in range(10))
    # words made of a single digit char
    digits_map.update(((str(i), i) for i in range(10)))

    # ... reversed words
    digits_map_rev = dict(((revstr(digits_words[i]), i) for i in range(10)))
    # words made of a single digit char
    digits_map_rev.update(((str(i), i) for i in range(10)))

    # re.compile('(zero|one|two|three|four|five|six|seven|eight|nine|0|1|2|3|4|5|6|7|8|9)')
    head = re.compile(f'({"|".join(digits_map.keys())})')
    # re.compile('(orez|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin|0|1|2|3|4|5|6|7|8|9)')
    tail = re.compile(f'({"|".join(digits_map_rev.keys())})')

    sum = 0
    coords = []
    junk = []
    for line in lines:
        m = head.search(line)
        if not m:
            junk.append(line)
            continue
        (d1,) = m.groups()

        m = tail.search(revstr(line))
        if not m:
            junk.append(line)
            continue
        (d2,) = m.groups()

        coord = digits_map[d1] * 10 + digits_map_rev[d2]
        sum += coord
        coords.append(coord)

    print('junk lines:', len(junk))
    print('sum:', sum)

    assert len(junk) == 0
    return coords

def test():
    assert test_result == parse(test_data.splitlines())

def main():
    with open('input') as f:
        lines = f.readlines()
    parse(lines)

if __name__ == '__main__':
    main()
