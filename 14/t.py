import itertools

TEST_DATA = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
'''

TEST_RESULT = 136

def load_line(loads, line):
    l = list(filter(lambda t: t[1] == '#', enumerate(['#'] + line, start=-1)))
    s = 0
    for i, _ in l:
        rounds = list(filter(lambda x: x == 'O',
                        itertools.takewhile(
                            lambda x: x != '#', line[i+1:])))
        s += sum(loads[i+1:i+1+len(rounds)])
    return s

def parse_lines(transposed):
    loads = range(len(transposed[0]), 0, -1)
    return sum(load_line(loads, line) for line in transposed)

def parse(lines):
    transposed = list(list(lines[y][x] for y in range(len(lines)))
                     for x in range(len(lines[0])))
    return parse_lines(transposed)

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
