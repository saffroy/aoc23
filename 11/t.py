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

TEST_RESULT = 374

def parse(lines):
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
    y_shift = [sum(empty_lines[:i]) for i in range(nlines)]
    x_shift = [sum(empty_cols[:i]) for i in range(ncols)]

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
    result = parse(lines)
    assert result == TEST_RESULT, (result, TEST_RESULT)

def main():
    with open('input', encoding='ascii') as f:
        lines = list(map(str.strip, f.readlines()))
    result = parse(lines)
    print(result)

if __name__ == '__main__':
    main()
