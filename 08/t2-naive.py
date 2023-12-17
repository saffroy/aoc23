import re

TEST_DATA = '''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
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

    nodevec = tuple(k for k in graph.keys() if k.endswith('A'))
    end = set(k for k in graph.keys() if k.endswith('Z'))
    print('start:', set(nodevec))
    print('end:', end)
    count = 0
    K = len(insn)

    while not all(node in end for node in nodevec):
        step = insn[count % K]
        nodevec = tuple(graph[node][step] for node in nodevec)
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
