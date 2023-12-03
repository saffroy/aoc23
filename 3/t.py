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

test_result = 4361

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
    sum_parts = 0
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
            if any(grid[yi][xi] != '.' for (xi, yi) in rectangle(*rect)):
                debug('*')
                sum_parts += int(nstr)
            else:
                debug('/')

            x += m.end(1)

    return sum_parts

def test():
    lines = test_data.splitlines()
    sum_parts = parse(lines)
    assert sum_parts == test_result

def main():
    with open('input', encoding='ascii') as f:
        lines = list(map(str.strip, f.readlines()))
    sum_parts = parse(lines)
    print(sum_parts)

if __name__ == '__main__':
    main()
