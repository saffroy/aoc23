import re

TEST_DATA = '''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
'''

TEST_RESULT = 19114

def comparison(part, args):
    (field, op, const, target) = args
    match op:
        case '>':
            if part[field] > const:
                return target
        case '<':
            if part[field] < const:
                return target
    return None

def branch(_, args):
    (label,) = args
    return label

def evaluate(flows, part):
    label = 'in'
    while label not in ['A', 'R']:
        for fun, args in flows[label]:
            target = fun(part, args)
            if target:
                break
        assert label
        label = target
    return label

def parse(lines):
    in_flows = True
    flows = dict()
    s = 0
    for line in lines:
        if not line:
            in_flows = False
            continue
        if in_flows:
            m = re.match(r'(\w+){(.*)}', line)
            label, rules = m.groups()
            flows[label] = []
            for r in rules.split(','):
                m = re.match(r'(\w)([<>])(\d+):(\w+)', r)
                if m:
                    field, op, const, target = m.groups()
                    flows[label].append((comparison,
                                         (field, op, int(const), target)))
                else:
                    target = r
                    flows[label].append((branch, (target,)))
        else:
            part = eval(f'dict({line[1:-1]})')
            rc = evaluate(flows, part)
            if rc == 'A':
                s += sum(part.values())
    return s

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
