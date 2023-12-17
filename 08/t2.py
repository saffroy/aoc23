import re
from fractions import math

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

def orbit(graph, insn, start, max_steps):
    history = []
    node = start
    K = len(insn)
    for count in range(max_steps):
        history.append(node)
        step = insn[count % K]
        node = graph[node][step]
    return history

def diag(graph, insn):
    start = set(k for k in graph.keys() if k.endswith('A'))

    Ki = []
    for s in start:
        history = orbit(graph, insn, s, len(insn)*1000)
        steps_endnodes = [(i,n) for (i,n) in enumerate(history) if n.endswith('Z')]
        ll = [t[0] for t in steps_endnodes]
        diffs = [t1-t0 for (t0, t1) in zip(ll, ll[1:])]
        print('start:', s)
        print('  steps, end nodes:', steps_endnodes)
        print('  differences:', diffs)
        print('  steps modulo # insn:', [k % len(insn) for (k,_) in steps_endnodes])
        k = steps_endnodes[0][0]
        assert {k} == set(diffs), (k, set(diffs))
        Ki.append(k)

    print('Ki:', Ki)

    # all lines 'steps mod...' are [0, 0, ...]
    # every start point reaches a SINGLE end point, and loops back to it,
    #  with the SAME number of steps!
    # we can see that every path i reaches an end point after steps:
    #     sn = n*Ki, for any n >= 1
    # where Ki is the constant on lines "differences" above
    # we want S such that there exists a set of ni that verifies:
    #   for all i, S = ni*Ki
    #          IOW S = LCM(Ki)

    return math.lcm(*Ki)

def parse(lines):
    insn = lines[0]
    graph = {}
    for line in lines[1:]:
        m = re.match(r'(\w+) = \((\w+), (\w+)\)', line)
        if m is None:
            continue
        (node, left, right) = m.groups()
        graph[node] = {'L': left, 'R': right}

    # brute forcing doesn't work
    # instead, do data analysis in REPL
    # this leads to comments in diag(), and solution
    # which is ~ 18E+12, so brute forcing was out...

    return diag(graph, insn)

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
