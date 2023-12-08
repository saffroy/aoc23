import re

TEST_DATA = '''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
'''

TEST_RESULT = 6

def parse(lines):
    insn = lines[0]
    graph = {}
    for line in lines[1:]:
        m = re.match(r'(\w+) = \((\w+), (\w+)\)', line)
        if m is None:
            continue
        (node, left, right) = m.groups()
        graph[node] = {'L': left, 'R': right}

    node = 'AAA'
    count = 0
    K = len(insn)
    while node != 'ZZZ':
        step = insn[count % K]
        node = graph[node][step]
        count += 1
    return count

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
