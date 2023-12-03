from collections import defaultdict
import re
import os

test_data = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''

test_result = 467835

def rectangle(x0, x1, y0, y1):
    assert x1 > x0 and y1 > y0
    for x in range(x0, x1 + 1):
        yield (x, y0)
        yield (x, y1)
    for y in range(y0+1, y1):
        yield (x0, y)
        yield (x1, y)

def debug(*posarg):
    if os.environ.get('INSIDE_EMACS'):
        print(*posarg)

def parse(lines):
    rows = len(lines)
    columns = len(lines[0])

    # pad lines with extra '.' in all directions
    pad_line = '.' * len(lines[0])
    grid = list(map(lambda l: '.' + l + '.',
                [pad_line] + lines + [pad_line]))
    # must have rows of equal length
    assert all(len(r) == columns+2 for r in grid)

    # scan grid rows for numbers, check the rectangle around each
    # NB: position col x, row y is grid[y][x]
    gear_adjacency = defaultdict(list)
    for y in range(1, rows+1):
        x = 1
        while True:
            debug()
            debug((x, y))
            row = grid[y][x:]
            debug(row)

            m = re.search(r'[^\d]*(\d+)', row)
            if not m:
                # next line
                break
            (nstr,) = m.groups()

            rect = (x+m.start(1)-1, x+m.end(1), y-1, y+1)
            debug('-> ', nstr, m.span(1), rect)

            for (xi, yi) in rectangle(*rect):
                if grid[yi][xi] == '*':
                    gear_adjacency[(xi, yi)].append((x, y, int(nstr)))

            x += m.end(1)

    sum_ratios = 0
    for k in gear_adjacency.keys():
        if len(gear_adjacency[k]) == 2:
            sum_ratios += gear_adjacency[k][0][2] * gear_adjacency[k][1][2]

    return sum_ratios

def test():
    lines = test_data.splitlines()
    sum_ratio = parse(lines)
    assert sum_ratio == test_result

def main():
    with open('input', encoding='ascii') as f:
        lines = list(map(str.strip, f.readlines()))
    sum_parts = parse(lines)
    print(sum_parts)

if __name__ == '__main__':
    main()
