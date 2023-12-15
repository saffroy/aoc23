import collections
import re

TEST_DATA = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'

TEST_RESULT = 145

def hashfun(s):
    h = 0
    for c in map(ord, s):
        h += c
        h *= 17
        h %= 256
    return h

def parse(lines):
    boxes = [collections.OrderedDict() for _ in range(256)]
    for insn in lines[0].split(','):
        label, focal = re.split(r'[-=]', insn)
        boxnum = hashfun(label)
        if focal == '':
            boxes[boxnum].pop(label, None)
        else:
            boxes[boxnum][label] = int(focal)
    return sum((boxnum+1) * slot * focal
               for boxnum in range(256)
               for slot, focal in enumerate(boxes[boxnum].values(), 1))

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
