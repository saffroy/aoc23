TEST_DATA = '''7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
'''

TEST_RESULT = 8

def connects_to(grid, pos):
    (x, y) = pos
    tile = grid[pos]
    match tile:
        case '.': return []
        case '|': return [(x, y-1), (x, y+1)]
        case '-': return [(x-1, y), (x+1, y)]
        case 'L': return [(x, y-1), (x+1, y)]
        case 'J': return [(x, y-1), (x-1, y)]
        case '7': return [(x-1, y), (x, y+1)]
        case 'F': return [(x+1, y), (x, y+1)]
        case 'S': return [(x, y-1), (x-1, y), (x+1, y), (x, y+1)]
        case _: assert False, (tile, pos)
    return [] # workaround for https://github.com/pylint-dev/pylint/issues/5288

def parse(lines):
    # parse lines into grid, w/ padding
    nlines = len(lines)
    ncols = len(lines[0])
    assert all(len(line) == ncols for line in lines)

    def tile(x, y):
        if (x == 0 or x == ncols+1
            or y == 0 or y == nlines+1):
            return '.' # padding
        return lines[y-1][x-1]

    grid = dict(
        ((x,y), tile(x, y))
        for x in range(ncols+2)
        for y in range(nlines+2)
    )

    # starting set of points = {S}
    # iterate:
    # - compute neighbours
    #   NB: a neighbour connects *back*
    # - new set of points = neighbours minus ancestors
    # - mark points with ++step
    # - end when nothing left to mark

    [start] = [k for (k,v) in grid.items() if v == 'S']

    steps = 0
    points = {start}
    marks = dict((k, None) for k in grid.keys())

    while points:
        print(points, steps)
        next_points = set()
        for p in points:
            ns = connects_to(grid, p)
            for n in ns:
                if (marks[n] is None
                    and p in connects_to(grid, n)):
                    # p and n connect together
                    next_points.add(n)
        points = next_points.difference(points)
        for p in points:
            marks[p] = steps
        steps += 1

    return steps-1

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
