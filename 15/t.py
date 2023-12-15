TEST_DATA = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'

TEST_RESULT = 1320

def hashfun(s):
    h = 0
    for c in map(ord, s):
        h += c
        h *= 17
        h %= 256
    return h

def parse(lines):
    return sum(map(hashfun, lines[0].split(',')))

def test():
    assert hashfun('HASH') == 52
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
