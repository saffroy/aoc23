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

TEST_RESULT = 64

TEST_CYCLE = '''.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
'''

def north_load(lines):
    return sum(len(lines) - y
               for y in range(len(lines))
               for x in range(len(lines[0]))
               if lines[y][x] == 'O')

def tilt_lines(lines, way):
    # NB: modifies lines in place
    for line in lines:
        for i in range(len(line)):
            if line[i] == '#':
                continue
            l = list(itertools.takewhile(lambda x: x != '#', line[i:]))
            k = len(l)
            line[i:i+k] = sorted(l, key=lambda c: way if c == 'O' else 1-way)
            i += k

def transpose_lines(lines):
    return list(list(lines[y][x]
                     for y in range(len(lines)))
                     for x in range(len(lines[0])))

def tilt_cycle(lines):
    # start with un-transposed lines, i.e. as parsed
    # lines from north to south, line offset from west to east

    lines = transpose_lines(lines)
    tilt_lines(lines, 0) # north
    lines = transpose_lines(lines) # back

    tilt_lines(lines, 0) # west

    lines = transpose_lines(lines)
    tilt_lines(lines, 1) # south
    lines = transpose_lines(lines) # back

    tilt_lines(lines, 1) # east
    # end with un-transposed lines
    return lines

def state_tuples(state):
    return tuple(tuple(c for c in line) for line in state)

def state_str(state):
    return '\n'.join(''.join(c for c in line) for line in state)

def parse(lines):
    state = transpose_lines(transpose_lines(lines))
    cycle = 0
    seen = dict()

    # run cycle until we find a repeated state
    while True:
        print('cycle:', cycle, 'load:', north_load(state))
        state = tilt_cycle(state)
        cycle += 1
        k = state_tuples(state)
        if k in seen:
            break
        seen[k] = cycle

    first = seen[k]
    period = cycle - first
    final = first + (10**9 - first) % period
    [st] = [st for (st, c) in seen.items() if c == final]

    load = north_load(st)
    return load

def test_cycle():
    lines = TEST_DATA.splitlines()
    assert TEST_DATA.strip() == '\n'.join(lines)
    assert TEST_DATA.strip() == state_str(lines)

    state = transpose_lines(transpose_lines(lines))
    assert TEST_DATA.strip() == state_str(state)

    assert transpose_lines(transpose_lines(state)) == state

    for d in TEST_CYCLE.split('\n\n'):
        state = tilt_cycle(state)
        assert d.strip() == state_str(state)
    
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
