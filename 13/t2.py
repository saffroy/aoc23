TEST_DATA = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
'''

TEST_RESULT = 400

def differing_chars(l1, l2):
    return sum(c1 != c2 for c1, c2 in zip (l1, l2))

def find_vert_reflection(pattern):
    for n, (l1, l2) in enumerate(zip(pattern, pattern[1:]), start=1):
        if differing_chars(l1, l2) <= 1:
            if all(differing_chars(ll1, ll2) <= 1
                   for (ll1, ll2) in zip(pattern[n:], reversed(pattern[:n]))):
                if sum(differing_chars(ll1, ll2)
                       for (ll1, ll2) in zip(pattern[n:], reversed(pattern[:n]))) == 1:
                    return n
    return 0

def find_reflections(pattern):
    n = 100*find_vert_reflection(pattern)
    if n == 0:
        # transpose
        tpattern = [
            ''.join(pattern[y][x]
                    for y in range(len(pattern)))
            for x in range(len(pattern[0]))
        ]
        n = find_vert_reflection(tpattern)
    return n

def parse(lines):
    if lines[-1]:
        lines.append('')

    sum_patterns = 0
    pattern = []
    for line in lines:
        if line:
            pattern.append(line)
        else:
            sum_patterns += find_reflections(pattern)
            pattern = []
    return sum_patterns

def test():
    lines = TEST_DATA.splitlines()
    result = parse(lines)
    assert result == TEST_RESULT, (result, TEST_RESULT)

def main():
    with open('input', encoding='ascii') as f:
        lines = list(map(str.strip, f.readlines()))
    result = parse(lines)
    print(result)

def bench():
    import timeit
    t = timeit.timeit('main()', number=1, globals=globals())
    print('time: {:3.2f} ms/call'.format(t*1000))

if __name__ == '__main__':
    main()
