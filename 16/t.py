from enum import Enum

TEST_DATA = r'''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
'''

TEST_RESULT = 46

Direction = Enum('Direction',
                 'NORTHWARD SOUTHWARD EASTWARD WESTWARD'.split())

class Cell:
    def __init__(self, x, y, content):
        self.x = x
        self.y = y
        self.content = content
        self.ingress = []

def dir2vec(direction):
    match direction:
        case Direction.NORTHWARD: return (0, -1)
        case Direction.SOUTHWARD: return (0, 1)
        case Direction.EASTWARD: return (1, 0)
        case Direction.WESTWARD: return (-1, 0)
    # workaround for https://github.com/pylint-dev/pylint/issues/5288
    assert False, direction
    return (0, 0)

def bounce(content, direction):
    match content:
        case '.':
            return [direction]
        case '/':
            match direction:
                case Direction.EASTWARD: return [Direction.NORTHWARD]
                case Direction.NORTHWARD: return [Direction.EASTWARD]
                case Direction.WESTWARD: return [Direction.SOUTHWARD]
                case Direction.SOUTHWARD: return [Direction.WESTWARD]
        case '\\':
            match direction:
                case Direction.EASTWARD: return [Direction.SOUTHWARD]
                case Direction.NORTHWARD: return [Direction.WESTWARD]
                case Direction.WESTWARD: return [Direction.NORTHWARD]
                case Direction.SOUTHWARD: return [Direction.EASTWARD]
        case '|':
            match direction:
                case Direction.EASTWARD|Direction.WESTWARD:
                    return [Direction.NORTHWARD, Direction.SOUTHWARD]
                case Direction.NORTHWARD|Direction.SOUTHWARD:
                    return [direction]
        case '-':
            match direction:
                case Direction.NORTHWARD|Direction.SOUTHWARD:
                    return [Direction.EASTWARD, Direction.WESTWARD]
                case Direction.EASTWARD|Direction.WESTWARD:
                    return [direction]
    # workaround for https://github.com/pylint-dev/pylint/issues/5288
    assert False, (content, direction)
    return []

def show_active(grid, xmax, ymax):
    for y in range(ymax):
        print(''.join('#' if grid[(x,y)].ingress else '.'
                      for x in range(xmax)))

def parse(lines):
    xmax = len(lines[0])
    ymax = len(lines)
    grid = {(x,y): Cell(x, y, lines[y][x])
            for x in range(xmax)
            for y in range(ymax)}

    beams = [(0, 0, Direction.EASTWARD)]
    while beams:
        (x, y, direction) = beams.pop()
        c = grid.get((x,y))
        if c is None:
            continue
        if direction in c.ingress:
            continue
        c.ingress.append(direction)
        for newdir in bounce(c.content, direction):
            (vx, vy) = dir2vec(newdir)
            beams.append((x+vx, y+vy, newdir))

    # show_active(grid, xmax, ymax)
    return sum(1 for c in grid.values() if c.ingress)

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
