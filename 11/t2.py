TEST_DATA = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
'''

SHIFT_FACTOR = 10**6

TEST_RESULT = {
    2: 374,
    10**1: 1030,
    10**2: 8410,
}

def parse(lines, shift_factor):
    nlines = len(lines)
    ncols = len(lines[0])
    assert all(len(line) == ncols for line in lines)

    empty_lines = [True] * nlines
    empty_cols = [True] * ncols
    galaxies = dict()
    for y in range(nlines):
        for x in range(ncols):
            if lines[y][x] != '.':
                galaxies[(x,y)] = True
                empty_cols[x] = False
                empty_lines[y] = False

    # yes, True is worth 1 in Python too...
    y_shift = [
        sum(empty_lines[:i]) * (shift_factor - 1) for i in range(nlines)
    ]
    x_shift = [
        sum(empty_cols[:i]) * (shift_factor - 1) for i in range(ncols)
    ]

    def dist(x1, y1, x2, y2):
        # manhattan distance
        return abs((x2 + x_shift[x2] - x1 - x_shift[x1])) \
            + abs((y2 + y_shift[y2] - y1 - y_shift[y1]))

    sum_dist = 0
    for (x1,y1) in galaxies.keys():
        for (x2,y2) in galaxies.keys():
            if x1 < x2 or (x1 == x2 and y1 < y2):
                sum_dist += dist(x1, y1, x2, y2)

    return sum_dist

def test():
    lines = TEST_DATA.splitlines()
    for (k, v) in TEST_RESULT.items():
        result = parse(lines, k)
        assert result == v, (result, v, k)

def main():
    with open('input', encoding='ascii') as f:
        lines = list(map(str.strip, f.readlines()))
    result = parse(lines, SHIFT_FACTOR)
    print(result)

if __name__ == '__main__':
    main()
